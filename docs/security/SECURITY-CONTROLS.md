# Security Control Layers

The RHEL 10 lab deliberately uses multiple security controls because no single technology provides complete host protection.

## SELinux

Purpose:

Mandatory access control.

Primary question:

"What is this process allowed to access?"

## AIDE

Purpose:

Filesystem integrity monitoring.

Primary question:

"What changed compared with the trusted baseline?"

## auditd

Purpose:

Kernel-level security auditing.

Primary question:

"What security-relevant event happened and under which identity?"

## nftables

Purpose:

Kernel-level network policy enforcement.

Primary question:

"What network traffic is permitted to cross the system?"

## SSH

Purpose:

Secure administrative transport.

Primary question:

"Who is permitted to establish an administrative session?"

## Ansible

Purpose:

Repeatable security configuration and validation.

Primary question:

"Can the intended security state be reproduced consistently?"

## Ansible Vault

Purpose:

Protect secrets required by automation.

Primary question:

"How can automation use secrets without storing them as plaintext in source control?"

## Future: LUKS2 and NBDE

Purpose:

Protect data at rest and control encrypted-device unlocking.

Primary question:

"Can data remain inaccessible when the underlying storage is stolen or accessed outside the authorized system?"
