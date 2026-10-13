# RHEL 10 Linux Security Engineering Lab

A hands-on Linux security engineering environment built around three Red Hat Enterprise Linux 10 virtual machines.

The purpose of this repository is not to demonstrate every Linux administration topic. Its primary focus is implementing, automating, testing, breaking, validating, and recovering security controls on RHEL 10 systems.

## Current Architecture

| Host | Role | Management IP | Primary Security Purpose |
|---|---|---:|---|
| DingasHost1 | Automation / Control Node | 10.10.10.100 | Ansible control, security orchestration, evidence collection |
| DingasHost2 | Application Node | 10.10.10.102 | Security baseline target and application-system testing |
| DingasHost3 | Edge Security Node | 10.10.10.103 | nftables, segmentation, routing and edge-security testing |

All hosts run RHEL 10.

## Security Engineering Areas

### Ansible Security Automation

The lab uses Ansible from DingasHost1 to manage security configuration across the three-node environment.

Implemented concepts include:

- Static inventory design
- Host and security role groups
- SSH public-key authentication
- Privilege escalation
- Per-host encrypted variables
- Ansible Vault
- Idempotent security playbooks
- Security validation across multiple RHEL systems

Per-host privilege escalation credentials are encrypted with Ansible Vault and are excluded from Git.

### AIDE File Integrity Monitoring

AIDE is deployed across the RHEL hosts to establish cryptographic filesystem baselines.

Work performed includes:

- Package deployment through Ansible
- AIDE database initialization
- Detection of existing databases
- Idempotent deployment logic
- Filesystem integrity scanning
- Controlled filesystem modification testing
- Analysis of changed filesystem objects

AIDE answers:

> What changed on the filesystem?

A non-zero AIDE result does not automatically indicate an intrusion. It indicates that the current filesystem differs from the stored integrity baseline and requires investigation.

### Linux Audit Framework / auditd

The lab uses the Linux audit subsystem to investigate security-relevant operating system activity.

Security auditing work includes:

- auditd status validation
- Persistent audit-rule development
- Identity-file monitoring
- SSH configuration monitoring
- Privilege escalation auditing
- Firewall configuration monitoring
- Network configuration monitoring
- Storage configuration monitoring

auditd answers:

> What security-relevant action occurred, when did it occur, and under which identity?

### SELinux

All three RHEL 10 systems operate with SELinux enabled and enforcing.

Current work includes:

- SELinux state validation
- Security-context inspection
- passwd and shadow context validation
- File-label analysis
- `matchpathcon`
- `restorecon`
- Controlled context manipulation
- Ansible-driven SELinux auditing

SELinux provides mandatory access control and limits what processes can access even when traditional Unix permissions would otherwise permit access.

### Network Security

DingasHost3 is being developed as the lab's edge-security node.

Current work includes:

- Native nftables
- Stateful packet filtering
- Network segmentation
- Management-network separation
- Corporate network simulation
- DMZ network simulation
- IoT network simulation
- NAT
- Traffic-policy testing
- NetworkManager integration
- Firewall validation and rollback testing

### SSH Security

SSH is used as the primary management transport.

The lab currently demonstrates:

- ED25519 authentication
- Dedicated Ansible control key
- ssh-agent
- IdentitiesOnly
- authorized_keys management
- restrictive SSH file permissions
- Ansible SSH transport

## Security Architecture


                         Windows Host
                      VirtualBox / PowerShell
                              |
                       10.10.10.0/24
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
 +----------------+   +----------------+   +----------------+
 | DingasHost1    |   | DingasHost2    |   | DingasHost3    |
 | Control Node   |   | Application    |   | Edge Security  |
 | 10.10.10.100   |   | 10.10.10.102   |   | 10.10.10.103   |
 +----------------+   +----------------+   +----------------+
 | Ansible        |   | AIDE           |   | nftables       |
 | Vault          |   | auditd         |   | segmentation   |
 | AIDE           |   | SELinux        |   | AIDE           |
 | auditd         |   | hardening      |   | auditd         |
 | SELinux        |   |                |   | SELinux        |
 +----------------+   +----------------+   +----------------+



Security Control Model
The technologies in the lab serve different purposes:
Technology	Security Function
SELinux	Mandatory access control
AIDE	File integrity monitoring
auditd	Security event auditing
nftables	Network policy enforcement
SSH	Secure remote administration
Ansible	Automated security configuration
Ansible Vault	Protection of automation secrets
NetworkManager	Persistent network configuration


Planned Storage Security Work
The next major security area is data-at-rest protection.
Planned labs include:
- LUKS2 encrypted block devices
- Creating and managing encrypted filesystems
- Persistent encrypted mounts
- LUKS key slots
- Passphrase rotation
- Recovery-key procedures
- Clevis
- Tang
- Network Bound Disk Encryption (NBDE)
- Automated unlocking
- Recovery when the Tang server is unavailable
- Backup and recovery of LUKS metadata
- Disaster-recovery exercises

The objective is to understand both normal encrypted-storage operations and failure/recovery scenarios.

Engineering Method

Security controls in this repository are treated as testable engineering systems.
The general workflow is:
Observe
   ↓
Configure
   ↓
Validate
   ↓
Introduce controlled failure/change
   ↓
Detect
   ↓
Remediate
   ↓
Verify persistence
   ↓
Collect evidence

This repository is therefore intentionally focused on practical RHEL 10 Linux security engineering rather than broad Linux administration coverage.
