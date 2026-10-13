# RHEL 10 Security Engineering Roadmap

## Completed / In Progress

- [x] Three-node RHEL 10 lab
- [x] Static management addressing
- [x] SSH key-based administration
- [x] Ansible inventory
- [x] Per-host Ansible Vault variables
- [x] Security baseline auditing
- [x] AIDE installation
- [x] AIDE database initialization
- [x] AIDE integrity checking
- [x] Controlled AIDE change testing
- [x] SELinux enforcing validation
- [x] SELinux context inspection
- [x] nftables edge-security experimentation
- [x] Network segmentation lab
- [ ] Complete persistent auditd policy
- [ ] auditd event investigation
- [ ] Centralized security logging

## Storage Security

- [ ] Add dedicated virtual data disks
- [ ] Create LUKS2 containers
- [ ] Create filesystems inside encrypted devices
- [ ] Configure persistent mounts
- [ ] Manage LUKS key slots
- [ ] Rotate passphrases
- [ ] Back up LUKS headers
- [ ] Test header recovery
- [ ] Deploy Tang
- [ ] Bind encrypted devices using Clevis
- [ ] Configure NBDE
- [ ] Test automatic boot-time unlocking
- [ ] Test Tang outage behavior
- [ ] Test manual recovery

## Security Operations

- [ ] Build reusable audit reports
- [ ] Query AVC denials
- [ ] ausearch workflows
- [ ] aureport workflows
- [ ] Central rsyslog collector
- [ ] Forward Host2 logs
- [ ] Forward Host3 logs
- [ ] Log integrity validation

## Hardening

- [ ] SSH daemon hardening
- [ ] sudo policy hardening
- [ ] systemd service reduction
- [ ] File permission auditing
- [ ] World-writable file auditing
- [ ] Kernel security parameters
- [ ] OpenSCAP evaluation
- [ ] CIS-aligned remediation testing

## Recovery Engineering

- [ ] Recover incorrect SELinux contexts
- [ ] Recover broken firewall policy
- [ ] Recover failed network configuration
- [ ] Recover LUKS access
- [ ] Restore AIDE baseline
- [ ] Restore security configuration using Ansible
