# DingasLab

## Network

Management subnet: 10.10.10.0/24

Windows VirtualBox Host:
10.10.10.1

## Nodes

##DingasHost1
OS: RHEL 10
Role: Control / Management Node
Management IP: 10.10.10.11

## DingasHost2
OS: RHEL 10
Role: Managed RHEL Server
Management IP: 10.10.10.12

## DingasHost3

OS: RHEL 10

Role: Application Server - App Node B

Management IP: 10.10.10.21

Management:

- SSH
- Ansible
- Managed from DingasHost1

Application:

- Nginx

Security:

- SELinux Enforcing
- firewalld
- auditd

---

## DingasHost4

OS: Ubuntu 26.04.1 LTS

Role: Data, Logging, Security and Compliance Services Node

Management IP: 10.10.10.22

Management:
- SSH
- Ansible
- Managed from DingasHost1

Current services:

- OpenSSH
- rsyslog
- auditd

Planned services:

- PostgreSQL
- OpenSSH
- auditd
- rsyslog
- LVM / XFS storage

Storage:
/dev/sdb
   |
   +-- vg_long_storage
         |
         +-- lv_pgdata    -> /var/lib/postgresql
         +-- lv_pgbackup  -> /var/backups/postgresql
         +-- lv_logs      -> /var/log/remote

Current PostgreSQL database:
labdb

Application database role:
labapp

Future responsibilities:
- centralized rsyslog collection
- PostgreSQL backup automation
- security-log retention
- compliance evidence storage
- OpenSCAP testing
- SIEM-style security analysis.
