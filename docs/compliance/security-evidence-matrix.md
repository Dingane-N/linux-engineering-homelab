# Security Evidence Matrix

| Control Objective 	     | Implementation 			| Host(s) 	| Validation 		     | Evidence |
|			     |					|		|		   	     |		|
| Centralized administration | Ansible controller 		| Host1-3 	| ansible ping 	   	     | Pending  |
| Privileged access 	     | Dedicated ansible account + sudo | Host2, Host3 	| sudo -n whoami   	     | Verified |
| Mandatory access control   | SELinux Enforcing 		| Host2, Host3 	| getenforce 	    	     | Verified |
| Host firewall 	     | firewalld 			| Host2, Host3 	| firewall-cmd 	   	     | Verified |
| Time synchronization 	     | chronyd 				| Host1-3 	| chronyc tracking 	     | Verified |
| Auditing 		     | auditd 				| Host1-3 	| systemctl is-active auditd | Verified |

## DingasHost4 Data and Logging Infrastructure

| Area | Implementation | Evidence |
|---|---|---|
| Database isolation | PostgreSQL data placed on dedicated LVM/XFS storage | `docs/compliance/evidence/2026-10-04-host4-storage-postgresql.md` |
| Backup preparation | Dedicated PostgreSQL backup logical volume | `docs/compliance/evidence/2026-10-04-host4-storage-postgresql.md` |
| Logging preparation | Dedicated `/var/log/remote` filesystem | `docs/compliance/evidence/2026-10-04-host4-storage-postgresql.md` |
| Operational resilience | PostgreSQL mount-over-data incident diagnosed and recovered | `incidents/2026-10-04-postgresql-lvm-mount-recovery.md` |
| Database access | `labdb` and non-superuser `labapp` role created | `docs/compliance/evidence/2026-10-04-host4-storage-postgresql.md` |

These controls are lab engineering evidence and do not constitute formal PCI DSS compliance certification or assessment.


