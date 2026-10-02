# Management Access Evidence - 2026-10-03

Management traffic uses the isolated 10.10.10.0/24 network.

Controller:

    DingasHost1
    10.10.10.11

Managed systems:

    DingasHost2  10.10.10.12
    DingasHost3  10.10.10.21
    DingasHost4  10.10.10.22

Administrative SSH connectivity was successfully verified to all
three managed nodes using the `dingane` account.

Dedicated Ansible service accounts use SSH public-key authentication.

Passwordless sudo is configured through:

    /etc/sudoers.d/ansible

The management architecture separates:

- interactive administration
- automation identities
- privilege escalation
- application services
