## Linux Engineering Homelab

A Multi-node RHEL 10 Linux engineering environment built to practice enterprise
Linux administration, troubleshooting, security, automation, high availability, storage, database administration and PCI DSS-aligned infrastructure engineering management and controls..

This environment is managed centrally from a dedicated RHEL control node using SSH, ansible, git, bash and python.
There are future plans to use python installed inthe windows host to quey and manage the RHEL10 machines.

>This is a simulated lab environment designed to study PCI security compliance Linux engineering concepts.
>This is not to be presented as a PCI-DSS  certified compliant environment or CDE.


## Architecture

| Host 		| OS 		   | Role 		     		| Management IP |
| DingasHost1 	| RHEL 10 	   | Control / Git / Ansible Node  	| 10.10.10.11 	|
| DingasHost2 	| RHEL 10 	   | Application Server Node A		| 10.10.10.12 	|
| DingasHost3 	| RHEL 10	   | Application Server Node B  	| 10.10.10.21 	|
| DingasHost4 	| RHEL 10	   | PostgreSQl / Storage 		| 10.10.10.22 	|


## Management Network

10.10.10.0/24

VirtualBox host-only interface:

10.10.10.1

Each VM also uses a separate NAT interface for outbound Internet access connected through adapter 1.


---

## Logical Architecture

                         GitHub
                            |
                            |
                     DingasHost1
                  RHEL 10 Control Node
                     10.10.10.11
                            |
                    SSH / Ansible
                            |
               10.10.10.0/24 Management
                   /                  \
                  /                    \
                 v                      v
        DingasHost2                DingasHost3
        App Node A                 App Node B
        10.10.10.12                10.10.10.21
             \                         /
              \                       /
               \                     /
                    DingasHost4
               PostgreSQL / Storage
                   10.10.10.22

---

## Current Management Model

DingasHost1 is the administrative control plane.

Infrastructure configuration is maintained on the controller and version control is done through Git/GitHub.

Managed nodes are accessed using a dedicated `ansible` service account.

Authentication flow:

DingasHost1
    |
    | SSH private key
    v
ansible@managed-node
    |
    | sudo / Ansible become
    v
root

Private SSH keys remain only on DingasHost1.

Managed nodes receive only the corresponding public key in the file below:
/home/ansible/.ssh/authorized_keys

---

## Current RHEL Security Baseline

Managed RHEL nodes use:

- SELinux in Enforcing mode
- firewalld
- dedicated management interfaces
- SSH key authentication
- dedicated Ansible service accounts
- controlled sudo privilege escalation
- auditd
- chronyd
- systemd service management
- Git-tracked infrastructure configuration

All administrative traffic is intended to use the private management network instead of the NAT-facing interfaces.

---

## Application Tier

DingasHost2 and DingasHost3 form the application tier.

Both systems run Nginx and will eventually be configured identically through Ansible.

Current design:

DingasHost2
    RHEL 10
    Application Node A
    10.10.10.12

DingasHost3
    RHEL 10
    Application Node B
    10.10.10.21

Future labs will introduce load balancing, health checks, service failure, configuration drift, recovery, and high-availability concepts across these nodes.

---

## Database and Storage Tier

DingasHost4 is planned as the stateful infrastructure node.

Planned responsibilities:

PostgreSQL
LVM-backed storage
XFS filesystems
database data volumes
backup storage
backup verification
restore testing
filesystem expansion
storage troubleshooting

Application nodes will be permitted to reach PostgreSQL while unnecessary
database access from other systems will be restricted.

---

## PCI DSS-Aligned Lab Direction

This project uses payment-infrastructure scenarios as the primary security context.

The objective is not to claim compliance.

The objective is to demonstrate how Linux engineering controls can support security and compliance requirements in a simulated cardholder-data environment.

Areas to be explored include:

Network segmentation
Least privilege
Administrative access control
SSH hardening
Firewall policy
SELinux enforcement
System auditing
Centralized logging
Time synchronization
Patch management
Configuration management
Change tracking
File permissions
Service hardening
Database access restrictions
Backup and recovery
Security monitoring
Incident investigation

---

## Planned PCI-Style Environment

                       Management Plane
                         DingasHost1
                              |
                              |
                  -------------------------
                  |                       |
                  v                       v
             App Node A              App Node B
             Host2 .12               Host3 .21
                  \                       /
                   \                     /
                    \                   /
                       Database Tier
                        Host4 .22

The environment will be used to simulate security boundaries around systems
that could participate in or affect a cardholder-data environment.

---

## Current Progress

### DingasHost1

RHEL 10 control node configured.

Implemented:

Static management addressing at 10.10.10.11/24
Seperate Nat-uplink
Ansible
Git
GitHub SSH integration
Python
OpenSSH
NetworkManager
private management network
firewalld
SELinux
infrastructure documentation

### DingasHost2

RHEL 10 Application Node A.

Implemented:

static management addressing at 10.10.10.12/24
Seperate Nat-uplink
Nginx
SELinux Enforcing
firewalld
sshd
chronyd
auditd
dedicated Ansible account
SSH key authentication
Ansible remote management

### DingasHost3

RHEL 10 Application Node B.

Implemented:

static management address 10.10.10.21/24
separate NAT uplink
Nginx
SELinux Enforcing
firewalld
sshd
chronyd
auditd
dedicated Ansible account
SSH public-key authentication
passwordless Ansible privilege escalation
successful Ansible connectivity from DingasHost1

Verified from DingasHost1:

ansible dingashost3 -m ping

Result:

SUCCESS
ping: pong

Privilege escalation verified with:

ansible dingashost3 -b -m command -a 'whoami'

Result:

root

---

## Automation Roadmap

Manual configuration is being used initially to understand the underlying RHEL components.

The next stage is to convert working configurations into reusable Ansible roles.

Planned structure:

ansible/
├── inventory/
├── group_vars/
├── host_vars/
├── playbooks/
└── roles/
    ├── common/
    ├── ssh/
    ├── firewall/
    ├── nginx/
    ├── audit/
    ├── storage/
    └── postgresql/

The goal is for managed systems to be reproducible from configuration rather than dependent on undocumented manual changes.

---

## Planned Engineering Scenarios

Future labs will include controlled failures rather than only successful
deployments.

Examples:

Application service unavailable
Incorrect firewalld rule
SELinux access denial
Incorrect file ownership or permissions
SSH authentication failure
Ansible inventory error
Configuration drift
Failed systemd service
Disk space exhaustion
LVM extension
PostgreSQL connectivity failure
Database access-control failure
Backup corruption
Backup restoration
Application-node failure
High-availability failover

Each scenario will document:

Detection
Symptoms
Investigation
Root cause
Remediation
Validation
Preventive automation

---

## Repository Purpose

This repository serves as both:

1. Infrastructure source control
2. Technical engineering documentation

Configurations, Ansible automation, troubleshooting notes, incident reports, security controls, and validation evidence are committed as the lab evolves.

The emphasis is on reproducible engineering rather than isolated commands.

---

## Planned Repository Structure

linux-engineering-homelab/
├── README.md
├── ansible/
├── bash/
├── configs/
├── docs/
│   ├── architecture.md
│   ├── network-topology.md
│   ├── security-design.md
│   ├── compliance/
│   └── incidents/
├── monitoring/
├── python/
├── security/
└── systemd/

---

## Long-Term Goal

Develop production-relevant RHEL engineering capability across:

Linux systems administration
Troubleshooting
Automation
Infrastructure security
Networking
Storage
High availability
Observability
Database infrastructure
Compliance engineering

The environment will progressively move from manually configured systems to
fully reproducible infrastructure managed through Ansible and version control.
