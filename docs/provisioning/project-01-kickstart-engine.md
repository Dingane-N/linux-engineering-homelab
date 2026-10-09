Project 1:
Python-Powered Automated Kickstart Provisioning Engine

Problem:
Manual RHEL installation is repetitive and inconsistent.

Objective:
Produce reproducible RHEL installations for managed VMs.

Inputs:
hosts.json
rhel10-server.ks.tmpl
provisioning public key

Processing:
render_kickstarts.py

Outputs:
dingashost2.cfg
dingashost3.cfg

Validation:
ksvalidator -v RHEL10

Network behavior:
Host2 -> NAT + management
Host3 -> isolated management only

Next:
Host Kickstart files over HTTP
Boot disposable VM from RHEL ISO
Pass inst.ks=
Verify unattended installation
Verify reboot
Verify SSH
Verify Ansible
