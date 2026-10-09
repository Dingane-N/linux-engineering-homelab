# Linux Engineering & Security Homelab

This repository documents a multi-node Red Hat Enterprise Linux 10 homelab focused on Linux systems administration, network security, infrastructure automation, troubleshooting, security hardening, and configuration management.

The purpose of the environment is not simply to install services. The lab is being built around repeatable engineering practices:

- configuration
- validation
- troubleshooting
- automation
- persistence testing
- recovery
- security hardening
- infrastructure documentation
- Git-based change tracking

The environment is currently being rebuilt around RHEL 10 after previous multi-distribution experiments.

---

# Current Architecture

The active lab currently consists of three RHEL 10 virtual machines running in Oracle VirtualBox.

The architecture will continue evolving as new Linux engineering projects are introduced.
DingasHost1 — Linux Engineering Control Node
Operating System: Red Hat Enterprise Linux 10
Role: Linux administration, Ansible control, Git integration, provisioning, storage engineering and infrastructure automation
Management Address: 10.10.10.100/24
DingasHost1 acts as the primary Linux engineering workstation and management node for the environment.
Current and planned responsibilities include:
- Linux systems administration
- Ansible configuration management
- Git and GitHub integration
- SSH administration
- infrastructure documentation
- Python automation
- Bash scripting
- Kickstart provisioning
- LVM management
- network configuration
- service management
- systemd administration
- firewall configuration
- logging and auditing
- configuration validation
- troubleshooting
- infrastructure recovery testing
The VM currently contains two network interfaces:
enp0s3 -> VirtualBox NAT / Internet connectivity
enp0s8 -> Host-only Linux lab network

The management network is configured persistently using NetworkManager and nmcli.
DingasHost1 Storage Architecture
DingasHost1 currently contains two virtual disks:
/dev/sda -> 30 GB
/dev/sdb -> 20 GB

The RHEL installation currently uses LVM.
Current physical volumes include:
/dev/sda3
/dev/sdb1

Both physical volumes belong to the RHEL volume group:
rhel

Current logical volumes include:
rhel-root
rhel-swap

The root logical volume currently spans storage from both virtual disks.
This configuration will later be used for deeper Linux storage engineering exercises involving:
- Physical Volumes
- Volume Groups
- Logical Volumes
- filesystem expansion
- capacity management
- XFS
- persistent mounts
- /etc/fstab
- storage monitoring
- filesystem recovery
- backup storage
- LVM troubleshooting
DingasHost2 — Application Engineering Node
Operating System: Red Hat Enterprise Linux 10
Role: Managed Linux application server
DingasHost2 will represent a typical enterprise Linux application server.
Planned work includes:
- Nginx
- application service management
- systemd
- SSH administration
- SELinux
- firewalld
- nftables
- centralized logging
- auditd
- package management
- application directories
- filesystem permissions
- service accounts
- configuration management
- network troubleshooting
- automated deployment through Ansible
The node will progressively become a target for application deployment, troubleshooting, monitoring, security hardening and configuration automation.
DingasHost3 — Engineering and Orchestration Node
Operating System: Red Hat Enterprise Linux 10
Role: Isolated Linux engineering, container, CI/CD and orchestration node
DingasHost3 will be used to explore more advanced Linux engineering concepts.
Planned technologies include:
- Podman
- Linux namespaces
- cgroups
- container networking
- rootless containers
- systemd-managed containers
- persistent container storage
- Jenkins
- CI/CD
- Kubernetes
- container security
- automation testing
The intention is to understand the Linux technologies underneath container orchestration before relying heavily on Kubernetes abstractions.
The planned progression is:
Linux Processes
      |
      v
Namespaces
      |
      v
cgroups
      |
      v
Linux Capabilities
      |
      v
Container Images
      |
      v
Rootless Containers
      |
      v
Container Networking
      |
      v
Persistent Storage
      |
      v
systemd Integration
      |
      v
CI/CD
      |
      v
Kubernetes

Linux Systems Administration
A major part of the lab focuses on core Linux administration.
Topics include:
- users and groups
- permissions
- ownership
- sudo
- SSH
- package management
- processes
- signals
- systemd
- services
- timers
- boot process
- journald
- kernel parameters
- filesystem management
- mounts
- LVM
- swap
- networking
- DNS
- routing
- logs
- troubleshooting
- recovery
The goal is to become comfortable administering Linux systems from the command line without depending on graphical tools.
Linux Networking
Networking is a major component of the lab.
Technologies and utilities being developed include:
nmcli
nmtui
ip
ss
ping
mtr
traceroute
tcpdump
nft
firewall-cmd

Topics include:
- static addressing
- DHCP
- default routes
- persistent NetworkManager profiles
- multiple network interfaces
- host-only networks
- NAT networks
- routing tables
- DNS
- VLAN concepts
- bonding
- interface troubleshooting
- socket inspection
- packet capture
- traffic filtering
- service exposure
Networking configurations are tested before and after reboots to verify persistence.
Linux Security Engineering
Security is treated as part of Linux engineering rather than as a completely separate discipline.
The lab will progressively include:
- SELinux
- firewalld
- nftables
- SSH hardening
- sudo management
- PAM
- password policies
- file permissions
- auditd
- rsyslog
- journald
- logrotate
- file integrity monitoring
- security baselines
- system hardening
- service isolation
- network segmentation
Security controls will normally be implemented manually first.
Once their behavior is understood, they can be converted into Ansible automation.
Configuration Management with Ansible
Ansible will be the primary configuration-management platform used throughout the lab.
The intended workflow is:
Understand the requirement
        |
        v
Configure manually
        |
        v
Validate
        |
        v
Troubleshoot
        |
        v
Document
        |
        v
Convert to Ansible
        |
        v
Test idempotency
        |
        v
Validate resulting state

Planned Ansible automation includes:
- package installation
- users and groups
- SSH configuration
- firewall rules
- NetworkManager configuration
- service management
- systemd units
- audit configuration
- rsyslog
- security hardening
- filesystem configuration
- configuration validation
- evidence collection
The objective is not merely to write playbooks.
The objective is to understand what the playbook changes, why the change is required, and how to troubleshoot the system when automation fails.
Bash Automation
Bash will be used for operating-system-level automation where a full Ansible workflow is unnecessary.
Planned use cases include:
- system validation
- backup scripts
- log processing
- service checks
- disk-space monitoring
- configuration checks
- scheduled maintenance
- filesystem inspection
- reporting
- troubleshooting utilities
Scripts will use defensive practices such as:
set -Eeuo pipefail

where appropriate.
Python for Linux Engineering
Python will complement Bash and Ansible.
The emphasis will be on practical Linux automation rather than general-purpose application development.
Planned Python projects include:
- server health collection
- disk-space reporting
- filesystem analysis
- service-state validation
- firewall-rule inspection
- log parsing
- configuration validation
- compliance evidence generation
- SSH automation
- API interaction
- infrastructure provisioning
- Kickstart generation
Project 1 — Python-Powered Automated Kickstart Provisioning Engine
The first major infrastructure project in the rebuilt lab is automated RHEL provisioning.
Objective
Eliminate repetitive manual RHEL installations and create reproducible Linux server deployments.
The project will combine:
- RHEL Kickstart
- Python
- HTTP
- VirtualBox
- LVM
- SSH
- NetworkManager
- Git
- Ansible
The intended provisioning workflow is:
RHEL Kickstart Template
        |
        v
Python Configuration Generator
        |
        v
Host-Specific Kickstart
        |
        v
Python HTTP Server
        |
        v
VirtualBox VM
        |
        v
RHEL Installer
        |
        v
Automatic Disk Partitioning
        |
        v
LVM Configuration
        |
        v
Network Configuration
        |
        v
SSH Public Key Deployment
        |
        v
Package Installation
        |
        v
System Reboot
        |
        v
Ansible Management

The long-term objective is to make managed Linux nodes disposable.
A failed VM should eventually be replaceable through automated provisioning instead of requiring hours of manual reconstruction.
Infrastructure Persistence Testing
One of the most important lessons from rebuilding the environment has been the difference between a configuration that works temporarily and one that survives system lifecycle events.
The lab therefore includes deliberate reboot testing.
Configurations are tested for persistence across:
- service restart
- daemon reload
- network restart
- VM reboot
- cold boot
- package updates
- configuration changes
Important validation areas include:
Network configuration
        |
        v
SSH connectivity
        |
        v
Storage
        |
        v
Mounted filesystems
        |
        v
System services
        |
        v
Firewall state
        |
        v
Timers
        |
        v
Automation

A service working once is not sufficient evidence that the system is properly engineered.
Troubleshooting
Failures are deliberately documented rather than hidden.
Examples include:
- incorrect SSH paths
- SSH host-key changes
- permission problems
- sudo failures
- incorrect service configuration
- storage mistakes
- LVM troubleshooting
- systemd failures
- PostgreSQL recovery
- rsyslog syntax errors
- firewall mistakes
- failed VM reboot testing
- operating-system rebuilds
Troubleshooting evidence is useful because it demonstrates the process used to move from:
Failure
   |
   v
Observation
   |
   v
Diagnosis
   |
   v
Correction
   |
   v
Validation
   |
   v
Documentation

Git and Documentation
GitHub is used as the engineering record for the environment.
Repository:
https://github.com/Dingane-N/linux-engineering-homelab
The repository contains:
- architecture documentation
- Ansible configuration
- Linux configuration examples
- troubleshooting notes
- incident documentation
- compliance evidence
- automation scripts
- future Kickstart templates
- system diagrams
- implementation notes
The current DingasHost1 was rebuilt and successfully reconnected to the existing repository through SSH authentication.
Previous project history was preserved.
Sensitive information must not be committed, including:
- private SSH keys
- passwords
- API keys
- access tokens
- unprotected password hashes
- private certificates
- environment secrets
Current Engineering Priorities
The current development sequence is:
Stable RHEL Baseline
        |
        v
Persistent Networking
        |
        v
SSH Management
        |
        v
Git Integration
        |
        v
Ansible Connectivity
        |
        v
Linux Storage / LVM
        |
        v
Network Automation
        |
        v
Firewall Automation
        |
        v
Logging and Auditing
        |
        v
Kickstart Provisioning
        |
        v
Python and Bash Automation
        |
        v
Application Services
        |
        v
Container Engineering
        |
        v
CI/CD
        |
        v
Kubernetes

The focus is deliberately on Linux Engineering fundamentals before adding unnecessary complexity.
Long-Term Objective
The long-term objective of this homelab is to build practical Linux Engineering capability across:
Linux Administration
        +
Networking
        +
Storage
        +
Security
        +
Automation
        +
Troubleshooting
        +
Infrastructure as Code
        +
Containers
        +
Observability

The lab is intended to demonstrate the ability to build, administer, automate, secure, troubleshoot and recover Linux infrastructure rather than simply demonstrate familiarity with individual commands or tools.



                         GitHub
                           |
                           |
                    DingasHost1
                    RHEL 10.2
                 Ansible Controller
                 Git / Automation
                 Network Management
                    10.10.10.100
                           |
                           |
                 10.10.10.0/24
                 Host-Only Network
                           |
              +------------+------------+
              |                         |
              v                         v
        DingasHost2                DingasHost3
          RHEL 10                    RHEL 10
       Application Node        Isolated Engineering Node
                              Jenkins / Containers /
                              Kubernetes / CI-CD
