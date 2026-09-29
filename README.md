## Linux Engineering Homelab

Multi-node Linux engineering environment built to practice enterprise
Linux administration, troubleshooting, security, automation and
cross-distribution infrastructure engineering/management.


## Architecture

| Host 		| OS 		   | Role 		     | Management IP |
| DingasHost1 	| RHEL 10 	   | Control / Ansible Node  | 10.10.10.11 |
| DingasHost2 	| RHEL 10 	   | Application Server      | 10.10.10.12 |
| DingasHost3 	| Ubuntu 26.04 LTS | Application Server      | 10.10.10.21 |
| DingasHost4 	| Ubuntu 26.04 LTS | Monitoring / Logging    | 10.10.10.22 |


## Management Network

10.10.10.0/24

VirtualBox host-only interface:

10.10.10.1

Each VM also uses a separate NAT interface for outbound Internet access connected through adapter 1.


## Current State

- RHEL 10 control node configured
- RHEL 10 application node configured
- SSH key-based management established
- Dedicated Ansible service account
- Ansible privilege escalation configured
- SELinux enforcing
- firewalld management zone
- Nginx application workload
- Git-based infrastructure documentation


## Planned

- Ubuntu application node
- Ubuntu monitoring/logging node
- Cross-distribution Ansible roles
- Centralized logging
- Monitoring
- Backup and recovery
- Controlled failure scenarios
- Troubleshooting scenarios
- Python-linux auditting and polling of device health and status
