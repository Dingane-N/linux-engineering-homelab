# DingasHost4

OS: Ubuntu 26.04.1 LTS

Role:
- PostgreSQL database host
- storage node
- centralized rsyslog collector
- audit/security evidence node

Management IP:

    10.10.10.22/24

NAT interface:

    enp0s3
    DHCP
    10.0.2.15/24

Management interface:

    enp0s8
    10.10.10.22/24

Controller:

    dingashost1.lab.test
    10.10.10.11

## Current Services

- OpenSSH
- rsyslog
- auditd
- NetworkManager

## Security Model

Ubuntu security controls differ from the RHEL nodes.

RHEL nodes:
- SELinux
- firewalld

Ubuntu node:
- AppArmor
- UFW/nftables

## Configuration Management

Managed from DingasHost1 using SSH and Ansible.

Administrative SSH:

    ssh dingane@10.10.10.22

Planned Ansible SSH:

    ssh host4

Ansible service account:

    ansible

## Current Status

Network connectivity: working

Administrative SSH: working

auditd: active

rsyslog: active

SSH service: active

Ansible authentication: pending final validation

Persistent storage configuration: pending
