# DingasHost3

## Role

Security and engineering managed node.

## Platform
- RHEL 10
- Management IP: 10.10.10.103/24
- Isolated from the normal NAT architecture
- SSH key-based management enabled

## Ansible Classification

[managed]
dingashost3

[security]
dingashost3

## Security Automation
Dingashost3 participates in the multi-node security baseline.

Current automated checks include:
- SELinux state
- sshd state
- firewalld state
- critical account-file permissions
- operating-system facts
- kernel information
- AIDE installation state

# Current Finding
AIDE is not currently installed.
Future work will use DingasHost3 for security-specific automatoin, integrity monitoring, hardening experiments and controlled remediation.

