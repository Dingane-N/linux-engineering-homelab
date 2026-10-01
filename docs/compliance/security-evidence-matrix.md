# Security Evidence Matrix

| Control Objective 	     | Implementation 			| Host(s) 	| Validation 		     | Evidence |
|			     |					|		|		   	     |		|
| Centralized administration | Ansible controller 		| Host1-3 	| ansible ping 	   	     | Pending  |
| Privileged access 	     | Dedicated ansible account + sudo | Host2, Host3 	| sudo -n whoami   	     | Verified |
| Mandatory access control   | SELinux Enforcing 		| Host2, Host3 	| getenforce 	    	     | Verified |
| Host firewall 	     | firewalld 			| Host2, Host3 	| firewall-cmd 	   	     | Verified |
| Time synchronization 	     | chronyd 				| Host1-3 	| chronyc tracking 	     | Verified |
| Auditing 		     | auditd 				| Host1-3 	| systemctl is-active auditd | Verified |
