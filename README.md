# DingasHost4 Data and Security Services

DingasHost4 is the supporting data, logging, security, and compliance-services node for the homelab.

Unlike DingasHost2 and DingasHost3, which primarily operate as RHEL application servers, DingasHost4 runs Ubuntu 26.04.1 LTS and introduces cross-distribution administration into the environment.

The node is intended to centralize services that support the application tier and the wider security architecture of the lab.

Current platform:

```text
Hostname:         dingashost4.lab.test
Operating System: Ubuntu 26.04.1 LTS
Management IP:   10.10.10.22/24
NAT Interface:   enp0s3
Management NIC:  enp0s8
Controller:       DingasHost1 - 10.10.10.11
```

The long-term role of DingasHost4 includes:

- PostgreSQL database services
- PostgreSQL data storage
- PostgreSQL backup storage
- centralized rsyslog collection
- auditd security auditing
- Ubuntu firewall enforcement
- security-log retention
- compliance evidence storage
- compliance verification
- security-event analysis
- future SIEM-style correlation and alerting
- cross-distribution Ansible management

Conceptually, DingasHost4 will provide the following supporting services:

```text
                     DingasHost4
                   Ubuntu 26.04.1
                    10.10.10.22
                          |
        +-----------------+------------------+
        |                 |                  |
        v                 v                  v
    PostgreSQL       Central Logging      Compliance
      Database           rsyslog          Verification
        |                 |                  |
        v                 v                  v
     Storage         Security Events       Evidence
     Backups          / Audit Logs        Collection
                          |
                          v
                    Future SIEM Layer
```

---

## Current Host4 State

The original DingasHost4 implementation used RHEL 10.

That VM experienced stability problems during storage configuration and reboot testing. The node was therefore rebuilt using Ubuntu 26.04.1 LTS while retaining the same logical role and management IP address.

Current verified functionality:

| Component | Status |
|---|---|
| Ubuntu 26.04.1 LTS | Running |
| Hostname | `dingashost4.lab.test` |
| Management address | `10.10.10.22/24` |
| NAT connectivity | Working |
| Management-network connectivity | Working |
| Connectivity to DingasHost1 | Working |
| Interactive SSH using `dingane` | Working |
| OpenSSH service | Active |
| rsyslog | Active |
| auditd | Active |
| Dedicated `ansible` account | Created |
| Ansible SSH authentication | In progress |
| Passwordless Ansible sudo | Validation pending |
| Ubuntu firewall hardening | Pending |
| PostgreSQL | Pending |
| Persistent database storage | Pending |
| Centralized remote logging | Pending |
| Compliance scanning | Pending |
| SIEM-style analytics | Future phase |

The Ubuntu rebuild also creates a useful cross-distribution engineering scenario because DingasHost1, DingasHost2, and DingasHost3 remain RHEL systems.

---

## Host4 Network Architecture

DingasHost4 uses two network interfaces.

```text
enp0s3
    |
    +-- NAT
    +-- DHCP
    +-- Internet access
    +-- Ubuntu package repositories
    +-- Software updates

enp0s8
    |
    +-- 10.10.10.22/24
    +-- Host-only management network
    +-- SSH administration
    +-- Ansible
    +-- PostgreSQL traffic
    +-- rsyslog traffic
    +-- Security management
```

The management network is:

```text
10.10.10.0/24
```

Current addressing:

```text
10.10.10.1     Windows / VirtualBox Host
10.10.10.11    DingasHost1 - RHEL Controller
10.10.10.12    DingasHost2 - RHEL App Node A
10.10.10.21    DingasHost3 - RHEL App Node B
10.10.10.22    DingasHost4 - Ubuntu Data/Security Node
```

Internet traffic must continue through the NAT interface.

Expected default route:

```text
default via 10.0.2.2 dev enp0s3
```

The `10.10.10.0/24` interface is reserved for lab-management and service-to-service communication.

---

## Host4 Security Services Roadmap

DingasHost4 will act as the primary security-services node for the lab.

Its planned security responsibilities include:

- Ubuntu firewall configuration
- management-network access restrictions
- centralized log collection
- audit-event collection
- security-log retention
- authentication monitoring
- compliance evidence storage
- security-event investigation
- log searching
- detection logic
- future SIEM-style correlation
- future security alerting

The implementation will progress in controlled stages.

```text
Ubuntu baseline
      |
      v
Firewall hardening
      |
      v
Centralized rsyslog
      |
      v
auditd collection
      |
      v
Security log repository
      |
      v
Compliance evidence
      |
      v
Security-event analysis
      |
      v
Correlation and alerting
      |
      v
SIEM-style capabilities
```

The intention is to understand and configure the underlying Linux security services before introducing a larger SIEM platform.

---

## Ubuntu Firewall Architecture

The RHEL nodes use `firewalld`.

DingasHost4 will use Ubuntu-native firewall tooling, primarily UFW backed by nftables.

Conceptually:

```text
UFW
 |
 v
nftables
 |
 v
Linux Kernel Packet Filtering
```

The intended security model is based on restrictive inbound access.

```text
Incoming Traffic
       |
       v
+--------------------+
| Ubuntu Firewall    |
| UFW / nftables     |
+--------------------+
       |
       +--> SSH
       |    Allowed from management network
       |
       +--> PostgreSQL
       |    Allowed only from approved application nodes
       |
       +--> rsyslog
       |    Allowed from managed lab systems
       |
       +--> Other traffic
            Denied unless explicitly required
```

Planned policy:

```text
ALLOW SSH from 10.10.10.0/24

ALLOW rsyslog from approved managed nodes

ALLOW PostgreSQL from approved application systems

DENY unnecessary inbound services
```

Firewall rules will eventually be deployed and validated through Ansible.

The firewall configuration itself will also become part of the compliance evidence collected by the lab.

---

## Centralized Logging Architecture

DingasHost4 will become the centralized rsyslog receiver.

Target architecture:

```text
                 DingasHost1
                RHEL Controller
                 10.10.10.11
                      |
                      |
                      |
DingasHost2 ----------+
RHEL App Node A       |
10.10.10.12           |
                      |
DingasHost3 ----------+
RHEL App Node B       |
10.10.10.21           |
                      |
                      v
                 DingasHost4
                  Ubuntu 26
                 10.10.10.22
                      |
                      v
              Central Log Repository
```

The objective is to move selected logs from individual systems into a central repository.

Planned event sources include:

- SSH authentication events
- sudo events
- systemd service failures
- kernel messages
- firewall events
- auditd events
- Nginx access logs
- Nginx error logs
- PostgreSQL logs
- application events
- security-policy violations
- configuration-management events

A future log structure may resemble:

```text
/var/log/remote/
|
+-- dingashost1/
|
+-- dingashost2/
|
+-- dingashost3/
|
+-- dingashost4/
```

This design creates a single location from which infrastructure and security events can be investigated.

---

## auditd Security Auditing

`auditd` is installed and active on DingasHost4.

auditd is used for security-focused system auditing and is separate from normal system logging.

rsyslog primarily handles operating-system and application messages.

auditd can provide detailed information about events such as:

- privileged command execution
- sensitive file access
- file permission changes
- account changes
- identity changes
- security-policy changes
- process execution
- selected system calls
- administrative configuration changes

Future audit rules will be designed around scenarios relevant to the PCI DSS-aligned lab.

The environment should eventually be able to answer questions such as:

```text
Who modified a security-sensitive file?

Who executed a privileged command?

Who changed the firewall configuration?

Who changed SSH configuration?

Who modified an application configuration?

Was a protected file changed or deleted?

When did the event occur?

Which account performed the action?
```

---

## Security Log Repository

Centralized logging and SIEM are not the same thing.

The initial goal is to make DingasHost4 a reliable security-log repository.

```text
Managed Linux Nodes
        |
        v
rsyslog forwarding
        |
        v
DingasHost4
        |
        v
Central Log Storage
        |
        v
Search and Investigation
        |
        v
Detection Logic
        |
        v
Alerting
```

A basic log server primarily receives and stores events.

A SIEM generally adds capabilities such as:

- event normalization
- centralized searching
- correlation
- detection rules
- alert generation
- dashboards
- event investigation
- security reporting

DingasHost4 will therefore not be described as a complete SIEM until those capabilities have actually been implemented.

---

## Future SIEM Capabilities

The long-term objective is to evolve DingasHost4 from a centralized logging server into a small security-monitoring platform.

Possible detection scenarios include:

```text
Repeated SSH authentication failures

SSH brute-force attempts

Unexpected privileged-account activity

Repeated sudo failures

Firewall-denial events

Unexpected PostgreSQL connections

Application service failures

Changes to SSH configuration

Changes to firewall configuration

Changes to sudo configuration

Changes to audit configuration

Suspicious authentication patterns

Audit-rule violations
```

The exact SIEM technology will be selected later.

The project will first establish reliable native Linux logging and auditing before another security platform is introduced.

The engineering progression is therefore:

```text
Linux logging
      |
      v
rsyslog
      |
      v
auditd
      |
      v
Central storage
      |
      v
Log searching
      |
      v
Detection rules
      |
      v
Correlation
      |
      v
Alerting
      |
      v
SIEM tooling
```

---

## PostgreSQL Database Role

DingasHost4 will provide PostgreSQL database services for future application scenarios.

The planned architecture is:

```text
                     Application Tier

              +-----------------------+
              |                       |
              v                       v

         DingasHost2             DingasHost3
          App Node A              App Node B
         10.10.10.12             10.10.10.21
              |                       |
              +-----------+-----------+
                          |
                          v
                     DingasHost4
                      PostgreSQL
                     10.10.10.22
```

PostgreSQL should not be exposed indiscriminately across the network.

Future access controls should permit database communication only from systems that require it.

Conceptually:

```text
DingasHost2 ----\
                 \
                  +----> PostgreSQL TCP/5432
                 /
DingasHost3 ----/

Other unauthorized systems ----> DENY
```

This creates practical experience with service segmentation and database access control.

---

## Storage Engineering

DingasHost4 will also provide dedicated storage for several services.

Planned storage purposes include:

```text
PostgreSQL database data

PostgreSQL backups

Centralized logs

Security logs

Compliance evidence

Security reports
```

The previous RHEL Host4 implementation used a second virtual disk and experimented with LVM.

The Ubuntu replacement will rebuild this storage architecture after the persistent operating-system installation and block-device layout have been fully verified.

Conceptual storage design:

```text
Additional Virtual Disk
         |
         v
Physical Volume
         |
         v
Volume Group
         |
         +--------------------+
         |                    |
         v                    v
 PostgreSQL Storage      Log / Backup Storage
```

The storage project will provide practice with:

- block-device discovery
- partitions
- physical volumes
- volume groups
- logical volumes
- XFS or appropriate Ubuntu filesystems
- mount points
- UUID-based mounting
- `/etc/fstab`
- persistent storage
- filesystem ownership
- filesystem permissions
- database storage
- backup storage
- troubleshooting failed mounts

Persistent storage will only be considered complete after surviving reboot and filesystem-validation testing.

---

## Compliance Services

DingasHost4 will also become a compliance-supporting system.

The purpose of the project is not to claim that the homelab is formally PCI DSS compliant.

Instead, PCI DSS concepts are being used as a framework for practicing infrastructure security engineering.

Potential compliance evidence includes:

- firewall policy
- SSH configuration
- sudo configuration
- audit rules
- active services
- package state
- logging configuration
- filesystem permissions
- authentication events
- security logs
- database access controls
- SELinux state on RHEL
- AppArmor state on Ubuntu
- Ansible configuration results
- configuration-change evidence

Evidence will be maintained under:

```text
docs/compliance/
```

Future evidence collection may use:

```text
Ansible
Bash
Python
OpenSCAP
Security Content Automation Protocol tooling
```

The objective is to automate evidence collection instead of depending entirely on manual screenshots and command execution.

---

## Cross-Distribution Security Engineering

DingasHost4 creates a deliberate difference between the RHEL infrastructure and the Ubuntu infrastructure.

The security goals remain similar even when the implementation differs.

| Security Area | RHEL Nodes | Ubuntu Host4 |
|---|---|---|
| Mandatory Access Control | SELinux | AppArmor |
| Firewall Frontend | firewalld | UFW |
| Firewall Backend | nftables | nftables |
| Package Manager | dnf | apt |
| SSH Service | sshd | ssh |
| Auditing | auditd | auditd |
| Logging | rsyslog | rsyslog |
| Service Manager | systemd | systemd |
| Networking | NetworkManager | NetworkManager |

This allows the project to distinguish between a security requirement and the distribution-specific technology used to implement that requirement.

For example:

```text
Security Objective:
Restrict inbound network access

RHEL Implementation:
firewalld + nftables

Ubuntu Implementation:
UFW + nftables
```

The security objective remains the same even though the administration syntax differs.

---

## Ansible Management of Host4

DingasHost4 will ultimately be configured centrally from DingasHost1.

Target management path:

```text
DingasHost1
RHEL 10 Controller
10.10.10.11
      |
      | SSH ED25519 Key
      |
      v
ansible@dingashost4
10.10.10.22
      |
      | sudo / become
      |
      v
root privileges
      |
      v
Configuration Management
```

DingasHost4 currently belongs to multiple Ansible groups because it performs several infrastructure functions.

```ini
[database]
dingashost4

[log_servers]
dingashost4

[compliance]
dingashost4
```

This is intentional.

Ansible groups describe roles and responsibilities rather than requiring a separate VM for every group.

This allows commands such as:

```bash
ansible database -m ping

ansible log_servers -m ping

ansible compliance -m ping
```

Future Host4 Ansible roles may include:

```text
ubuntu_baseline

ubuntu_firewall

auditd

rsyslog_server

postgresql

storage

compliance

security_logging
```

---

## Host4 Management Validation

Configuration work must be validated at several layers.

### Network connectivity

```bash
ping -c 3 10.10.10.22
```

### Administrative SSH

```bash
ssh dingane@10.10.10.22
```

### Ansible service account

```bash
ssh host4
```

### Ansible connectivity

From DingasHost1:

```bash
cd ~/linux-lab/ansible

ansible dingashost4 -m ping
```

Expected successful result:

```text
dingashost4 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

### Privilege escalation

```bash
ansible dingashost4 \
-b \
-m command \
-a 'whoami'
```

Expected result:

```text
root
```

### Service validation

SSH:

```bash
ansible dingashost4 \
-b \
-m command \
-a 'systemctl is-active ssh'
```

rsyslog:

```bash
ansible dingashost4 \
-b \
-m command \
-a 'systemctl is-active rsyslog'
```

auditd:

```bash
ansible dingashost4 \
-b \
-m command \
-a 'systemctl is-active auditd'
```

---

## Host4 Implementation Phases

The implementation will progress in stages.

```text
PHASE 1
Ubuntu Baseline
      |
      +-- Hostname
      +-- Network configuration
      +-- SSH
      +-- auditd
      +-- rsyslog
      +-- Ansible account
      +-- Ansible connectivity


PHASE 2
Firewall Hardening
      |
      +-- UFW / nftables
      +-- Default inbound policy
      +-- SSH restrictions
      +-- Logging-service rules
      +-- PostgreSQL restrictions
      +-- Firewall validation


PHASE 3
Centralized Logging
      |
      +-- rsyslog receiver
      +-- RHEL log forwarding
      +-- Ubuntu log collection
      +-- Remote log directories
      +-- Log retention
      +-- Testing


PHASE 4
Security Auditing
      |
      +-- auditd rules
      +-- Privileged activity
      +-- Authentication events
      +-- Configuration changes
      +-- Evidence collection


PHASE 5
Database and Storage
      |
      +-- Persistent storage
      +-- PostgreSQL
      +-- Restricted database access
      +-- Database logging
      +-- Backup storage
      +-- Backup validation


PHASE 6
Compliance Engineering
      |
      +-- Configuration checks
      +-- Security evidence
      +-- OpenSCAP
      +-- Automated validation
      +-- Compliance reporting


PHASE 7
Security Analytics
      |
      +-- Log searching
      +-- Event filtering
      +-- Detection rules
      +-- Correlation
      +-- Alerting
      +-- SIEM-style capabilities
```

---

## Desired Host4 End State

When complete, DingasHost4 should provide:

```text
Ubuntu 26.04.1 LTS
        |
        +-- SSH management
        |
        +-- Ansible management
        |
        +-- UFW / nftables firewall
        |
        +-- PostgreSQL
        |
        +-- Persistent database storage
        |
        +-- PostgreSQL backup storage
        |
        +-- Centralized rsyslog
        |
        +-- auditd
        |
        +-- Security-log retention
        |
        +-- Compliance evidence
        |
        +-- Security-event analysis
        |
        +-- Detection and alerting
        |
        +-- Future SIEM capabilities
```

Combined with the remaining infrastructure:

```text
                         DingasHost1
                    RHEL 10 Controller
                       10.10.10.11
                            |
                     Ansible / SSH
                            |
                +-----------+-----------+
                |                       |
                v                       v
           DingasHost2             DingasHost3
           RHEL App A              RHEL App B
          10.10.10.12             10.10.10.21
                |                       |
                +-----------+-----------+
                            |
                            v
                       DingasHost4
                     Ubuntu 26.04.1
                      10.10.10.22
                            |
           +----------------+----------------+
           |                |                |
           v                v                v
       PostgreSQL       Central Logs     Compliance
                            |
                            v
                    Security Analytics
                            |
                            v
                       Future SIEM
```

The completed architecture will allow the homelab to demonstrate Linux administration, cross-distribution configuration management, automation, application infrastructure, database services, network security, centralized logging, auditing, compliance validation, security monitoring, storage engineering, and production-style troubleshooting.


