# Lab Session - 2026-10-03

## Objective

Continue building the four-node Linux Engineering homelab and restore
management connectivity after replacing DingasHost4 with Ubuntu 26.04.1 LTS.

Primary objectives:

- Verify management connectivity with all 4 nodes
- Restore SSH connectivity between DingasHost1 and managed nodes
- Repair SSH key authentication for DingasHost3
- Bootstrap DingasHost4 as an Ubuntu managed node
- Install and verify auditd on Ubuntu
- Prepare Host4 for Ansible management
- Preserve troubleshooting evidence before continuing storage/database work

---

## Current Architecture

| Host | OS | Management IP | Role | Status |
|------|----|---------------|------|--------|
| DingasHost1 | RHEL 10 | 10.10.10.11 | Ansible controller / management node | Operational |
| DingasHost2 | RHEL 10 | 10.10.10.12 | Application Node A | SSH operational |
| DingasHost3 | RHEL 10 | 10.10.10.21 | Application Node B | SSH repaired |
| DingasHost4 | Ubuntu 26.04.1 LTS | 10.10.10.22 | Planned PostgreSQL / storage / logging / compliance node | Bootstrap in progress |

---

## Network Validation

DingasHost4 successfully reached:

- Internet: 1.1.1.1
- VirtualBox host-only network: 10.10.10.1
- DingasHost1: 10.10.10.11

Management interface:

    enp0s8 -> 10.10.10.22/24

NAT interface:

    enp0s3 -> 10.0.2.15/24

Default routing remains through the NAT interface.

This confirms that Host4 networking is functioning independently of
the remaining SSH and Ansible authentication configuration.

---

## SSH Troubleshooting

Interactive SSH using the administrative user was successfully tested.

Working examples:

    ssh dingane@10.10.10.12
    ssh dingane@10.10.10.21
    ssh dingane@10.10.10.22

### DingasHost3 issue

The Ansible SSH alias failed because the configured private key could
not be found:

    no such identity: /home/dingane/.ssh/id_ed25519_lab

The Host1 public key was recopied and the authorized_keys file on
DingasHost3 was rebuilt.

Successful validation:

    ssh -i ~/.ssh/id_ed25519_lab \
      -o IdentitiesOnly=yes \
      ansible@10.10.10.21

Results:

    whoami
    ansible

    sudo -n whoami
    root

This confirmed both SSH key authentication and passwordless sudo
privilege escalation.

---

## DingasHost4 Replacement

The previous RHEL-based DingasHost4 experienced VM instability and was
replaced with Ubuntu 26.04.1 LTS.

New hostname:

    dingashost4.lab.test

New management address:

    10.10.10.22/24

NetworkManager connection names:

    nat-uplink
    lab-mgmt

Host4 can currently be reached using:

    ssh dingane@10.10.10.22

---

## Ubuntu Service Configuration

The following services were validated:

    ssh      active
    rsyslog  active
    auditd   active

auditd initially failed because the package was not installed.

Incorrect assumption:

    systemctl enable --now auditd

Result:

    Unit auditd.service does not exist

Resolution:

    sudo apt update
    sudo apt install -y auditd audispd-plugins

Validation:

    systemctl is-active auditd

Result:

    active

This reinforced the distinction between package installation and
systemd service management.

---

## Ansible Account Bootstrap

The Ubuntu Ansible service account was created:

    sudo adduser --disabled-password --gecos "" ansible

SSH directory:

    /home/ansible/.ssh

Required permissions:

    .ssh             700
    authorized_keys  600

Planned sudo configuration:

    /etc/sudoers.d/ansible

Required entry:

    ansible ALL=(ALL) NOPASSWD: ALL

Host4 Ansible key authentication still requires final validation from
DingasHost1.

---

## Host Key Change

Because DingasHost4 was rebuilt, Host1 detected a different SSH host
fingerprint for 10.10.10.22.

Observed message:

    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!

This was expected because the IP address remained the same while the
operating system and SSH host keys changed.

The obsolete known_hosts entry was removed and the new host key was
accepted after verifying that DingasHost4 had intentionally been rebuilt.

---

## Key Lessons

Network reachability, SSH authentication and Ansible authentication
must be treated as separate troubleshooting layers.

A successful ping does not prove SSH authentication.

A successful interactive SSH login as `dingane` does not prove the
`ansible` service account is configured correctly.

A successful Ansible ping does not automatically prove privilege
escalation works.

The full management path therefore requires separate verification:

    IP connectivity
        ->
    SSH connectivity
        ->
    SSH key authentication
        ->
    Ansible inventory resolution
        ->
    sudo/become privilege escalation

---

## Remaining Work

DingasHost4 requires final Ansible key authentication and sudo
validation.

After that:

    ansible dingashost4 -m ping

and:

    ansible dingashost4 -b -m command -a 'whoami'

must succeed.

Before configuring PostgreSQL or permanent storage, verify that
DingasHost4 is booted from the installed operating system rather than
the Ubuntu live environment.

Previous filesystem evidence showed:

    /cow mounted on /

This must be investigated before storing persistent PostgreSQL data.

Future Host4 services:

- PostgreSQL
- dedicated storage
- PostgreSQL backup storage
- centralized rsyslog collection
- audit logging
- compliance evidence storage

