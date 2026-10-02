##DingasHost4 Security Services Configuration Milestone

DingasHost4 has progressed from a basic Ubuntu managed node into a centralized database and securiy (syslog) logging services node for the homelab.

Curret Platform:

Hostname:	dingashost4.lab.test
OS:		Ubuntu 26.04.1 LTS
Management IP:	10.10.10.22/24
Management NIC:	enp0s8 / renamed to lab-mgmt
NAT NIC:	enp0s3 / renamed to nat-uplink


##So far, what is operational in Ubuntu host4 server?

ufw has been enabled and configured to use a default-deny inbound security model but only permit certain management traffic such as:
10.10.10.11 -> 10.10.10.22 TCP/22    SSH / Ansible
10.10.10.12 -> 10.10.10.22 TCP/5432  PostgreSQL
10.10.10.21 -> 10.10.10.22 TCP/5432  PostgreSQL
10.10.10.11 -> 10.10.10.22 TCP/514   rsyslog
10.10.10.12 -> 10.10.10.22 TCP/514   rsyslog
10.10.10.21 -> 10.10.10.22 TCP/514   rsyslog

Broad SSH remote access was removed, only allowing Host1 to be able to perform SSH administrative tasks through the management interface.
The firewall baseline rule so far is:
Deny default incoming traffic and default routed. Allow default outgoing traffic. UFW logging has been enabled.

PostgreSQL 18.6 is running on Host4 and is restricted to 2 IPs and their respective ports:
127.0.0.1:5432 && 10.10.10.22:5432 disallowing this server to listen on the NAT interface.

Application access to labdb using labapp user role is restricted to Host2(.12) and Host3(.21) through pg_hba.conf file using scram-sha-256 authentication.
Remote PostgreSQL connectivity has been successfully validated on both host 2 and 3 machines through:
	psql -h 10.10.10.22 -U labapp -d labdb -W -c 'SELECT inet_client_addr();'


# Centralized logging
Host4 now operates as the centralized rsyslog receiver listening on 10.10.10.22:514/tcp
All logs are forwarded from the 3 RHEL hosts (1, 2, & 3) and stored under the file '/var/log/remote' in host4.

The logging structure seperates events by originating hostname and program. For example: /var/log/remote/dingashost1 for host1 (so on and so forth for the other hosts)

Custom 'logger' events from the 3 RHEL hosts has been used to validate centralized logging.



# Time Synchronization on Host4
A significant cost drift was noticed in host4 after VirtualBox VM state changes. The guest clock was approximately 36 hours behind the configured NTP source. Initially, this caused the APT repositories to reject Release metadata as being "not valid yet".

Ubuntu uses Chrony for time sync in this environment, to correct the issue:
	sudo chronyc makestep
From there I just made final validations to ensure system clock was syncronized and that NTP services were active in the timedatectl.


# Compliance Scanning

OpenSCAP 1.4.3 is installed and operational. The ubuntu-packaged SCAP security guide currently provides ssg-ubuntu(22&24)04-ds.xml

Native Ubuntu 26.04 SCAP content is not currently present in the installed package.
The next compliance phase will therefore use Ubuntu 26.04-compatible ComplianceAsCode content rather than incorrectly evaluating the system against an Ubuntu 24.04 datastream.


# Remaining Work:
Ubuntu 26.04 OpenSCAP content
        |
        v
Baseline compliance scan
        |
        v
Analyze failed controls
        |
        v
Selective remediation
        |
        v
Re-scan and compare
        |
        v
PostgreSQL backup automation
        |
        v
Log retention / rotation policy
        |
        v
Security event detection
        |
        v
SIEM-style correlation
        |
        v
Ansible least-privilege hardening
