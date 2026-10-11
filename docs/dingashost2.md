# DingasHost2
## Role: Application Node

Platform:
- RHEL 10
- Management IP: 10.10.10.102/24
- Managed by DingasHost2 using Ansible
- SSH key-based management enabled


## Ansible Classification

[managed]
dingashost2

[application]
dingashost2


## Security Automation
Dingashost2 participates in the multi-node security baseline.

Current Automated checks include:
- SELinux State
- sshd state
- firewalld state
- critical account-file permissions
- operating-system facts
- kernel information
- AIDE installation state


# Current Finding
AIDE is not currently installed. The next implementation stage will deploy and initialize AIDE through Ansible and use the host as a controlled file-integrity monitoring target.

