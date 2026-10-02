# Incident — PostgreSQL Cluster Hidden by LVM Mount

Date: 2026-10-04

Host: dingashost4.lab.test


Summary
PostgreSQL became unavailable after a new XFS logical volume was mounted directly on /var/lib/postgresql.
The PostgreSQL 18 cluster had already been created in that directory before the new filesystem was mounted.
Symptoms
pg_lsclusters reported:
18 main 5432 down <unknown> /var/lib/postgresql/18/main

Local PostgreSQL connections failed with:
connection to server on socket
"/var/run/postgresql/.s.PGSQL.5432"
failed

The mounted directory appeared empty.
Root Cause
The new lv_pgdata filesystem was mounted on top of an existing populated directory:
/var/lib/postgresql

Linux mount semantics caused the existing PostgreSQL directory hierarchy to become hidden beneath the newly mounted filesystem.
The original PostgreSQL files were not deleted.
Recovery
The new logical volume was unmounted.
The original PostgreSQL cluster became visible again under:
/var/lib/postgresql/18/main

The new logical volume was temporarily mounted at:
/mnt/pgdata-new

The database hierarchy was copied with:
sudo rsync -aHAX --numeric-ids \
/var/lib/postgresql/ \
/mnt/pgdata-new/

The filesystem was returned to its permanent mountpoint:
/var/lib/postgresql

The PostgreSQL cluster was then started with:
sudo pg_ctlcluster 18 main start

Resolution
Final cluster state:
18 main 5432 online postgres /var/lib/postgresql/18/main

Lessons Learned
Storage must be designed before placing application data in a mountpoint.
Mounting a filesystem over an existing directory hides the underlying data.
pg_lsclusters reports PostgreSQL cluster state but does not start a cluster.
Cluster control is performed with:
pg_ctlcluster

LVM naming errors can be corrected without destroying the volume group using:
vgrename

Future storage migrations will use the following sequence:
- stop service
- verify service is stopped
- mount new filesystem temporarily
- copy existing data
- verify ownership and permissions
- switch mountpoint
- start service
- verify application
