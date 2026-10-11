# Linux Engineering Homelab — Network Topology

## Current Architecture

The current lab consists of three Red Hat Enterprise Linux 10 virtual machines running in Oracle VirtualBox.

The environment uses a dedicated VirtualBox Host-Only network:
10.10.10.0/24

DingasHost1 acts as the Linux engineering control node. DingasHost2 acts as the application node. DingasHost3 is intentionally isolated from direct Internet access and will be used for engineering, container, CI/CD and orchestration experiments.

Topology
                         Internet
                            |
                     VirtualBox NAT
                            |
                            |
                  +---------+---------+
                  |                   |
                  v                   v
            DingasHost1          DingasHost2
              RHEL 10              RHEL 10
           Control Node          Application Node

           enp0s3: NAT           enp0s3: NAT
           DHCP                  DHCP

           enp0s8:              enp0s8:
           10.10.10.100         10.10.10.102
                  |                   |
                  +---------+---------+
                            |
                     10.10.10.0/24
                   Host-Only Network
                            |
                            |
                            v
                      DingasHost3
                        RHEL 10
                 Isolated Engineering Node

                       enp0s3:
                     10.10.10.103

                     NO NAT adapter
                     NO direct Internet

Node Roles
Host	Operating System	Management IP	Role	Internet
DingasHost1	RHEL 10	10.10.10.100	Ansible, Git, provisioning and Linux engineering control node	Yes
DingasHost2	RHEL 10	10.10.10.102	Application and managed Linux server	Yes
DingasHost3	RHEL 10	10.10.10.103	Isolated engineering, containers, Jenkins and Kubernetes node	No


## Management Network

10.10.10.0/24
                         |
        +----------------+----------------+
        |                |                |
        v                v                v

+----------------+ +----------------+ +----------------+
| DingasHost1    | | DingasHost2    | | DingasHost3    |
| 10.10.10.100   | | 10.10.10.102   | | 10.10.10.103   |
|                | |                | |                |
| Ansible        | | Application    | | Security /     |
| Control Node   | | Managed Node   | | Engineering    |
+----------------+ +----------------+ +----------------+
        |                ^                ^
        |                |                |
        +------ SSH / Ansible ------------+

DingasHost1
Role:
- Ansible control node
- Git repository host
- Automation development node
- Provisioning services
Interfaces:
- NAT uplink
- Host-only management network
DingasHost2
Role:
- Application managed node
- Security-hardening target
Management address:
10.10.10.102/24

DingasHost3
Role:
- Security and engineering managed node
- Isolated experimentation target
Management address:
10.10.10.103/24

Automation Flow
Git Repository
      |
      v
DingasHost1
      |
      | Ansible + SSH
      |
 +----+----+
 |         |
 v         v
Host2     Host3

Security configuration is validated through Ansible before remediation is introduced.

