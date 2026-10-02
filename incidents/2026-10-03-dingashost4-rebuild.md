# Incident: DingasHost4 VM Failure and Rebuild

Date: 2026-10-03

## Summary

The original RHEL 10 DingasHost4 became unstable during storage and
filesystem configuration work.

The VM experienced boot/reboot problems and VirtualBox instability.
Rather than continue troubleshooting an unreliable guest, the node
was rebuilt using Ubuntu 26.04.1 LTS.

## Impact

DingasHost4 temporarily became unavailable to:

- SSH
- Ansible
- planned PostgreSQL services
- centralized logging
- storage services

The change also invalidated the existing SSH host fingerprint stored
on DingasHost1 because the rebuilt VM generated new SSH host keys.

## Recovery

A replacement Ubuntu VM was created.

Hostname:

    dingashost4.lab.test

Management IP:

    10.10.10.22/24

NAT IP:

    10.0.2.15/24

Verified connectivity:

    ping 1.1.1.1
    ping 10.10.10.1
    ping 10.10.10.11

SSH connectivity using the `dingane` account was restored.

## Follow-up

Complete Ansible key authentication for hosts 3 and 4.

Verify Host4 is installed to persistent disk before continuing storage
configuration.

Do not recreate PostgreSQL or logging storage until persistent root
filesystem status has been confirmed.
