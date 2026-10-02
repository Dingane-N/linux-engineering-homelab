# DingasHost4 Security Services Implementation Evidence

**Date:** 2026-10-05 
**System:** dingashost4.lab.test 
**Operating System:** Ubuntu 26.04.1 LTS 
**Management Address:** 10.10.10.22/24 
**Role:** Database, centralized logging, storage, security and compliance services

---

## Objective

The objective of this lab session was to continue transforming DingasHost4 from a basic Ubuntu managed node into the centralized data and security-services system for the four-node Linux homelab.

The work focused on four areas:
1. Ubuntu firewall hardening
2. PostgreSQL remote-access restrictions
3. Centralized rsyslog collection
4. Preparation for Ubuntu compliance scanning

The session also included SSH/Ansible privilege validation, time-synchronization troubleshooting and multiple configuration syntax troubleshooting exercises.

---

# 1. Ansible Privilege Escalation Validation

DingasHost4 had previously accepted SSH authentication for the `ansible` service account but denied sudo execution.

The sudoers configuration was corrected using:

```ansible ALL=(ALL:ALL) NOPASSWD: ALL
/etc/sudoers.d/ansible

The sudo configuration was validated with:
	sudo visudo -c
	sudo -l -U ansible

Remote validation from DingasHost1:
	ssh host4 'whoami'
	ssh host4 'sudo -n whoami'

Expected and verified identities:
ansible
root

Ansible privilege escalation was subsequently verified across all managed systems:
	ansible 'dingashost*' -b -m command -a 'whoami'

Result:
	dingashost2 -> root
	dingashost3 -> root
	dingashost4 -> root

This confirmed that Host1 can centrally manage all three managed nodes.


# 2. Ubuntu UFW Firewall Hardening
DingasHost4 uses two network interfaces:
	enp0s3 -> NAT / Internet connectivity
	enp0s8 -> 10.10.10.22/24 management network

UFW was configured using a default-deny inbound model.
Baseline:
	sudo ufw default deny incoming
	sudo ufw default allow outgoing
	sudo ufw default deny routed
	sudo ufw logging low

SSH was restricted to the controller:
	sudo ufw allow in on enp0s8 \
	from 10.10.10.11 \
	to any port 22 proto tcp \
	comment 'SSH Ansible from host1'

PostgreSQL was restricted to the two application nodes:
	sudo ufw allow in on enp0s8 \
	from 10.10.10.12 \
	to any port 5432 proto tcp \
	comment 'PostgreSQL from host2'

	sudo ufw allow in on enp0s8 \
	from 10.10.10.21 \
	to any port 5432 proto tcp \
	comment 'PostgreSQL from host3'

	Centralized syslog reception was restricted to Hosts 1-3:
	sudo ufw allow in on enp0s8 \
	from 10.10.10.11 \
	to any port 514 proto tcp \
	comment 'rsyslog from Host1'

	sudo ufw allow in on enp0s8 \
	from 10.10.10.12 \
	to any port 514 proto tcp \
	comment 'rsyslog from Host2'

	sudo ufw allow in on enp0s8 \
	from 10.10.10.21 \
	to any port 514 proto tcp \
	comment 'rsyslog from Host3'

The original broad SSH rule allowing TCP/22 from anywhere was removed.
Final policy:
	10.10.10.11 -> TCP/22
	10.10.10.12 -> TCP/5432
	10.10.10.21 -> TCP/5432
	10.10.10.11 -> TCP/514
	10.10.10.12 -> TCP/514
	10.10.10.21 -> TCP/514

All other unsolicited inbound traffic is denied.


# 3. PostgreSQL Remote Access Hardening
PostgreSQL 18.6 is running on DingasHost4.
The server was configured to listen only on:
	127.0.0.1
	10.10.10.22

Configuration:
	listen_addresses = '127.0.0.1,10.10.10.22'

Listener validation:
	sudo ss -tulnp | grep ':5432'

Verified listeners:
	127.0.0.1:5432
	10.10.10.22:5432

The PostgreSQL service therefore does not listen on Host4's NAT interface.
pg_hba.conf Access Control
Application database access was restricted to the two application systems.
Configuration:
	host    labdb    labapp    10.10.10.12/32    scram-sha-256
	host    labdb    labapp    10.10.10.21/32    scram-sha-256
	host    labdb    labapp    0.0.0.0/0          reject

Password encryption was verified:
	SHOW password_encryption;

Result:
	scram-sha-256

The labapp role was configured with LOGIN capability and its password was reset interactively.
No database password was stored in documentation or shell commands.
PostgreSQL Remote Testing
The PostgreSQL client was installed on DingasHost2 and DingasHost3 through Ansible:
	ansible app -b -m package \
	-a "name=postgresql state=present"

Testing from DingasHost2:
	psql -h 10.10.10.22 \
	-U labapp \
	-d labdb \
	-W \
	-c 'SELECT inet_client_addr();'

Verified result:
10.10.10.12

Testing from DingasHost3 produced:
10.10.10.21

This demonstrated that both approved application nodes can connect to PostgreSQL through the management network.
4. Centralized rsyslog Collection
DingasHost4 was configured as the central log receiver.
Logs are stored on the dedicated XFS logical volume mounted at:
	/var/log/remote

Receiver configuration:
	/etc/rsyslog.d/10-central-receiver.conf

	Final configuration:
	module(load="imtcp")

	template(
	    name="RemotePerProgram"
	    type="string"
	    string="/var/log/remote/%HOSTNAME%/%PROGRAMNAME%.log"
	)

	ruleset(name="RemoteLogs") {
	    action(
	        type="omfile"
	        dynaFile="RemotePerProgram"
	        createDirs="on"
	        dirCreateMode="0750"
	        fileCreateMode="0640"
	    )
	}

	input(
	    type="imtcp"
	    Address="10.10.10.22"
	    port="514"
	    ruleset="RemoteLogs"
	)

The configuration was validated before restarting:
	sdcxzvsudo rsyslogd -N1

Successful result:
	End of config validation run. Bye.

The service was then restarted:
	sudo systemctl restart rsyslog
	sudo systemctl is-active rsyslog

Result:
	active

Listener verification:
	sudo ss -tulnp | grep ':514'

Final listener:
	10.10.10.22:514

This replaced the original:
	0.0.0.0:514
	[::]:514

configuration and prevents rsyslog from unnecessarily listening on every Host4 interface.


# 5. Rsyslog Sender Configuration
Hosts 1, 2 and 3 forward logs to DingasHost4.
Sender configuration:
	/etc/rsyslog.d/90-forward-host4.conf

The configuration was deployed to the managed application nodes through Ansible.
Example deployment:
	ansible app -b -m copy \
	-a "src=/tmp/90-forward-host4.conf dest=/etc/rsyslog.d/90-forward-host4.conf owner=root group=root mode=0644"

Configuration validation uses the daemon executable:
	/usr/sbin/rsyslogd -N1

Ansible validation:
	ansible app -b -m command \
	-a '/usr/sbin/rsyslogd -N1'

The rsyslog services were then restarted on the managed application nodes.


# 6. Centralized Logging Verification
Test events were generated with:
	logger -t pci-lab-test \
	"central rsyslog test from $(hostname -f)"

Host4 successfully created files for all three RHEL systems.
Examples:
/var/log/remote/dingashost1/pci-lab-test.log
/var/log/remote/dingashost2/pci-lab-test.log
/var/log/remote/dingashost3/pci-lab-test.log

Additional centrally collected logs included:
sudo.log
systemd.log
systemd-logind.log
rsyslogd.log
python3.log
sshd-session.log

Verification:
	sudo grep -R \
	"central rsyslog test" \
	/var/log/remote

Logs generated on Hosts 1, 2 and 3 were successfully received by DingasHost4.


# 7. Rsyslog Troubleshooting
Several configuration problems were deliberately diagnosed during implementation.
An initial Ansible validation attempted:
	rsyslog -N1

This failed because the executable is:
	rsyslogd

Correct command:
	rsyslogd -N1

A second problem occurred while restricting the rsyslog listener to the management interface.
The configuration accidentally contained:
	Address-"10.10.10.22"

instead of:
	Address="10.10.10.22"

The malformed character caused:
invalid character '-' in object definition
syntax error

The mistake was corrected and validated with:
	sudo rsyslogd -N1

After restarting rsyslog, the listener changed successfully from:
	0.0.0.0:514
	[::]:514

to:
	10.10.10.22:514

This reinforced the importance of configuration validation before restarting production-style services.


# 8. Time Synchronization Incident
APT initially produced errors similar to:
Release file ... is not valid yet

Chrony diagnostics revealed that Host4's system clock was approximately 130,000 seconds behind the NTP reference.
The system used Chrony rather than systemd-timesyncd.
Installing systemd-timesyncd would have removed Chrony, so that change was aborted.
Chrony status was inspected with:
	chronyc tracking
	chronyc sources -v

The clock was corrected using:
	sudo chronyc makestep

Final validation:
	System clock synchronized: yes
	NTP service: active
	Leap status: Normal

The system clock and virtual RTC were subsequently synchronized.
This resolved the repository timestamp problem.


# 9. OpenSCAP Status
OpenSCAP is installed on DingasHost4.
Version:
OpenSCAP command line tool (oscap) 1.4.3

Verification:
	oscap --version

The currently installed SCAP Security Guide package provides Ubuntu content for:
ssg-ubuntu2204-ds.xml
ssg-ubuntu2404-ds.xml

The expected Ubuntu 26.04 datastream:
ssg-ubuntu2604-ds.xml

is not present in the currently installed distribution package.


An Ubuntu 24.04 profile will not be presented as Ubuntu 26.04 compliance evidence.
The next compliance phase will therefore obtain or build Ubuntu 26.04-compatible ComplianceAsCode content before running the first formal assessment.
10. Current Architecture
                         DingasHost1
                      RHEL 10 Controller
                         10.10.10.11
                               |
               SSH / Ansible / rsyslog
                               |
              +----------------+----------------+
              |                |                |
              v                v                v
        DingasHost2       DingasHost3       DingasHost4
          RHEL 10           RHEL 10        Ubuntu 26.04.1
          App A             App B          Data/Security
       10.10.10.12       10.10.10.21       10.10.10.22
              |                |                |
              |                |                |
              +---- 5432 ------+--------------->|
              |                                 |
              +----------- TCP/514 ------------>|
                                                |
                                         PostgreSQL 18.6
                                         Central rsyslog
                                         UFW firewall
                                         auditd
                                         LVM/XFS storage
                                         OpenSCAP

# 11. Security Controls Demonstrated
The current lab demonstrates:
- source-restricted firewall policy
- default-deny inbound filtering
- management-plane isolation
- least-exposure service binding
- PostgreSQL host-based authentication
- SCRAM-SHA-256 database authentication
- centralized log forwarding
- centralized log retention
- dedicated LVM/XFS service storage
- SSH public-key authentication
- Ansible centralized configuration management
- sudo privilege escalation
- configuration validation before service restart
- NTP troubleshooting
- security-baseline preparation


# 12. Remaining Work
The next implementation stages are:
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

The current unrestricted Ansible NOPASSWD: ALL rule remains intentional technical debt during the build phase and will later be replaced with a more restrictive privilege model.
