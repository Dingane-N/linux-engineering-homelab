# Ansible Multi-Node Security Baseline

Date: 2026-10-11

## Objective

Configure DingasHost1 as an Ansible control node and establish secure automated management of the RHEL 10 managed nodes.

The implementation demonstrates:

- Ansible inventory management
- SSH key-based automation
- Managed-node grouping
- Remote system inspection
- Security baseline validation
- SELinux inspection
- SSH service inspection
- firewalld inspection
- Critical account-file permission auditing
- AIDE installation-state detection
- Automated evidence collection

## Architecture


DingasHost1
10.10.10.100
Ansible Control Node
        |
        | SSH / Ansible
        |
        +----------------------+
        |                      |
        v                      v
DingasHost2               DingasHost3
10.10.10.102              10.10.10.103
Application Node          Security / Engineering Node

Ansible Project Structure
ansible/
├── ansible.cfg
├── evidence/
├── files/
├── group_vars/
├── host_vars/
├── inventory/
│   └── hosts.ini
├── playbooks/
│   └── security-baseline-check.yml
├── roles/
└── templates/

Inventory Groups
The managed systems are divided into functional groups:
[managed]
dingashost2 ansible_host=10.10.10.102
dingashost3 ansible_host=10.10.10.103

[application]
dingashost2

[security]
dingashost3

This allows playbooks and ad-hoc operations to target either the entire managed estate or specific system roles.
Authentication

DingasHost1 uses a dedicated ED25519 SSH key for Ansible automation.
Private automation keys are stored outside the Git repository.

Managed nodes contain only the corresponding public key in the authorized_keys configuration.


Security Baseline Playbook

The security baseline playbook performs read-only validation of:
- RHEL distribution and kernel information
- SELinux enforcement state
- sshd service state
- firewalld service state
- /etc/passwd permissions
- /etc/group permissions
- /etc/shadow permissions
- /etc/gshadow permissions
- AIDE package installation state

The first implementation intentionally performs inspection only.
Remediation will be introduced after the baseline state has been documented and reviewed.


Result

The playbook completed successfully against both managed systems.
dingashost2 : ok=12 changed=0 unreachable=0 failed=0
dingashost3 : ok=12 changed=0 unreachable=0 failed=0

The changed=0 result confirms that the baseline playbook operated as a read-only audit.
The unreachable=0 result confirms successful Ansible transport and managed-node configuration.
The failed=0 result confirms successful execution of the baseline checks.

Findings
AIDE was not installed on either managed node during the baseline scan.
This creates the next security-hardening task:
1. Install AIDE through Ansible.
2. Initialize the AIDE database.
3. Define monitoring of critical files.
4. Perform controlled file modification.
5. Detect the modification.
6. Capture the result as compliance evidence.

Next Security Stages
Planned work includes:
- AIDE file-integrity monitoring
- SSH hardening
- firewalld policy enforcement
- SELinux validation
- systemd service reduction
- privileged-account auditing
- LUKS encrypted storage
- NBDE persistence
- automated security remediation
