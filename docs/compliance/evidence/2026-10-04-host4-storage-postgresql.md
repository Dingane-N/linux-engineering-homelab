# Evidence — DingasHost4 LVM and PostgreSQL Storage

Date: 2026-10-04

Host:
	dingashost4.lab.test
	10.10.10.22
	Ubuntu 26.04.1 LTS


#Objective

Create isolated persistent storage for PostgreSQL data, PostgreSQL backups and centralized security logs.

Physical Storage
Secondary disk:
/dev/sdb
25 GiB

LVM physical volume:
/dev/sdb

Volume group:
vg_long_storage

Logical Volumes
lv_pgdata     10G
lv_pgbackup    5G
lv_logs        8G

Mountpoints
lv_pgdata
/var/lib/postgresql

lv_pgbackup
/var/backups/postgresql

lv_logs
/var/log/remote

#All service filesystems use XFS.
Verification Commands
sudo pvs
sudo vgs
sudo lvs

lsblk -f

findmnt /var/lib/postgresql
findmnt /var/backups/postgresql
findmnt /var/log/remote

df -hT \
/var/lib/postgresql \
/var/backups/postgresql \
/var/log/remote

PostgreSQL Verification
Installed version:
PostgreSQL 18.6

Cluster:
18 main

Final cluster state:
online

Cluster owner:
postgres

Database:
labdb

Database owner:
labapp

#Verification:
sudo pg_lsclusters
sudo -u postgres psql -c 'SELECT version();'
sudo -u postgres psql -c '\l'
sudo -u postgres psql -c '\du'

#Engineering Outcome

The database cluster now runs from a dedicated LVM-backed XFS filesystem rather than competing with the Ubuntu root filesystem.
Separate logical volumes also exist for database backups and future centralized security logs.
This design provides a foundation for later backup, retention, monitoring and PCI-aligned logging exercises.
