# DingasHost4 — Data, Logging and Compliance Node

## System Overview

DingasHost4 is the data and security-services node in the Linux Engineering Homelab.

The server currently runs Ubuntu 26.04.1 LTS and is connected to the isolated lab management network.

Hostname: dingashost4.lab.test

Management address:
10.10.10.22/24

Primary roles:
- PostgreSQL database server
- dedicated PostgreSQL storage
- PostgreSQL backup storage
- centralized logging storage
- future rsyslog collector
- auditd-enabled security node
- future compliance evidence repository
- future security-event analysis node
DingasHost4 is managed remotely from DingasHost1.
Network Configuration
DingasHost4 uses two interfaces.
enp0s3
10.0.2.15/24
NAT / Internet uplink

enp0s8
10.10.10.22/24
Lab management network

The management interface does not provide the default route.
The isolated network is:
10.10.10.0/24

DingasHost1 management node:
10.10.10.11

DingasHost2 application node:
10.10.10.12

DingasHost3 application node:
10.10.10.21

Storage Architecture
A second 25 GiB virtual disk was attached to DingasHost4 as:
/dev/sdb

The entire disk was initialized as an LVM physical volume.
sudo pvcreate /dev/sdb

A volume group was created for long-term service storage.
Final volume group:
vg_long_storage

During implementation the volume group was initially created with the incorrect name:
vg_log_storage

The mistake was corrected with:
sudo vgrename vg_log_storage vg_long_storage

The final logical-volume layout is:
/dev/sdb
   |
   +-- vg_long_storage
         |
         +-- lv_pgdata      10 GiB
         +-- lv_pgbackup     5 GiB
         +-- lv_logs         8 GiB

All three logical volumes use XFS.
Logical Volume Mountpoints

PostgreSQL Data

Logical volume:
lv_pgdata

Size:
10 GiB

Filesystem:
XFS

Mountpoint:
/var/lib/postgresql

Filesystem UUID:
a5be62ed-440e-4d39-8ceb-9fc97d7a8bff

PostgreSQL Backup Storage
Logical volume:
lv_pgbackup

Size:
5 GiB

Filesystem:
XFS

Mountpoint:
/var/backups/postgresql

Filesystem UUID:
7e390582-719e-48d9-98eb-fe417ae74139

Centralized Log Storage
Logical volume:
lv_logs

Size:
8 GiB

Filesystem:
XFS

Mountpoint:
/var/log/remote

Filesystem UUID:
f737c997-3207-4af1-a7bd-9da774d7adc3

Persistent Mount Configuration
The new filesystems are configured in /etc/fstab.
UUID=a5be62ed-440e-4d39-8ceb-9fc97d7a8bff /var/lib/postgresql     xfs defaults 0 2
UUID=7e390582-719e-48d9-98eb-fe417ae74139 /var/backups/postgresql xfs defaults 0 2
UUID=f737c997-3207-4af1-a7bd-9da774d7adc3 /var/log/remote          xfs defaults 0 2

The configuration was validated with:
sudo systemctl daemon-reload
sudo mount -a

findmnt /var/lib/postgresql
findmnt /var/backups/postgresql
findmnt /var/log/remote

Current storage verification showed:
/dev/mapper/vg_long_storage-lv_pgdata
    XFS
    10G
    /var/lib/postgresql

/dev/mapper/vg_long_storage-lv_pgbackup
    XFS
    5G
    /var/backups/postgresql

/dev/mapper/vg_long_storage-lv_logs
    XFS
    8G
    /var/log/remote

PostgreSQL
DingasHost4 currently runs:
PostgreSQL 18.6

The PostgreSQL cluster is:
Version: 18
Cluster: main
Port: 5432
Owner: postgres
Data directory: /var/lib/postgresql/18/main
Status: online

Cluster status can be verified with:
sudo pg_lsclusters

The PostgreSQL database created for the application tier is:
labdb

Database owner:
labapp

Current PostgreSQL roles include:
postgres
labapp

The labapp account is intentionally not a PostgreSQL superuser.
PostgreSQL Storage Migration Incident
PostgreSQL was originally installed before the dedicated lv_pgdata logical volume was mounted.
This meant that the original PostgreSQL cluster existed under:
/var/lib/postgresql/18/main

When the new XFS filesystem was mounted directly over:
/var/lib/postgresql

the existing cluster files became hidden underneath the mount.
PostgreSQL subsequently appeared as:
18 main 5432 down <unknown>

and local psql connections failed because PostgreSQL was no longer running.
The underlying database files had not been deleted.
The logical volume was temporarily unmounted, exposing the original PostgreSQL cluster again.
The new logical volume was then mounted temporarily at:
/mnt/pgdata-new

The PostgreSQL hierarchy was migrated with:
sudo rsync -aHAX --numeric-ids \
/var/lib/postgresql/ \
/mnt/pgdata-new/

The logical volume was then returned to:
/var/lib/postgresql

PostgreSQL ownership remained:
postgres:postgres

The cluster was successfully started with:
sudo pg_ctlcluster 18 main start

Final verification:
sudo pg_lsclusters

returned the cluster as:
18 main 5432 online postgres /var/lib/postgresql/18/main

This incident demonstrated an important Linux filesystem concept:
Mounting a filesystem over a populated directory does not delete the original data. It hides the underlying directory contents until the filesystem is unmounted.
Security Services

The following services are currently available or planned on DingasHost4:
OpenSSH
PostgreSQL
rsyslog
auditd
LVM
XFS

The dedicated /var/log/remote filesystem will become the storage backend for centralized logging.
The dedicated PostgreSQL backup filesystem will be used for database backup and restore exercises.

Planned PostgreSQL Network Security

PostgreSQL currently requires additional remote-access hardening before application-tier connectivity is considered complete.

Planned PostgreSQL listener:
127.0.0.1
10.10.10.22

Planned pg_hba.conf application rules:
host    labdb    labapp    10.10.10.12/32    scram-sha-256
host    labdb    labapp    10.10.10.21/32    scram-sha-256

These rules will restrict labdb access to the two application nodes.
Security Roadmap

The next implementation stages are:

PostgreSQL storage
        |
        v
PostgreSQL network restrictions
        |
        v
Ubuntu firewall hardening
        |
        v
Centralized rsyslog collector
        |
        v
auditd integration
        |
        v
Security-log retention
        |
        v
Compliance evidence
        |
        v
Security-event detection
        |
        v
SIEM-style correlation and alerting

A full SIEM platform will not be introduced until centralized collection, storage, permissions, retention and event analysis are understood at the Linux level.
 
Current Status

Completed:
- Ubuntu 26.04.1 baseline
- Static management addressing
- SSH administration
- Dedicated LVM storage
- XFS filesystems
- Persistent fstab mounts
- PostgreSQL 18 installation
- labdb creation
- labapp database role
- PostgreSQL storage migration
- PostgreSQL cluster recovery
- PostgreSQL cluster online
- Dedicated PostgreSQL backup filesystem
- Dedicated centralized-log filesystem

Next:
- PostgreSQL network access hardening
- UFW / nftables policy
- Application-to-database connectivity testing
- Centralized rsyslog
- Remote audit/security logs
- Backup automation
- Compliance evidence collection
- OpenSCAP experimentation
- Security-event analysis
- SIEM-style alerting


