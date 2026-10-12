# Zero-Trust Edge Security with nftables and NetworkManager

Date: 2026-10-12

## Objective

Build a RHEL 10 edge-routing and packet-filtering lab using NetworkManager
and native nftables.

The objective is to develop Linux networking, packet-filtering, segmentation,
routing, NAT, security-policy and infrastructure-automation skills.

## Architecture

DingasHost1 remains the Ansible and Git control node.

DingasHost2 remains the application managed node.

DingasHost3 operates as the experimental edge router/firewall.


                          Internet
                             |
                      VirtualBox NAT
                             |
                      enp0s8 - WAN
                       10.0.3.15/24
                             |
                    +----------------+
                    |  DingasHost3   |
                    |  RHEL 10 Edge  |
                    +----------------+
                      /      |      \
                     /       |       \
                    v        v        v

             Corporate      DMZ       IoT
               enp0s9     enp0s10    enp0s16
          172.20.10.1/24  .20.1/24  .30.1/24


Management plane:

Windows / Host1
       |
10.10.10.0/24
       |
enp0s3
10.10.10.103/24

Interface Mapping
Interface	Purpose	Address
enp0s3	Management	10.10.10.103/24
enp0s8	WAN / NAT	DHCP - 10.0.3.15/24 during testing
enp0s9	Corporate	172.20.10.1/24
enp0s10	DMZ	172.20.20.1/24
enp0s16	IoT	172.20.30.1/24


NetworkManager owns interface configuration and routing.
The management interface is explicitly prevented from installing a default
route. The WAN interface provides the default route.

Router Hardening
IPv4 forwarding is enabled through a persistent sysctl configuration.
Additional network-stack controls include:
- ICMP redirect rejection
- source-route rejection
- reverse-path filtering
- martian packet logging
- broadcast ICMP protection
- TCP SYN cookies

Configuration:
networking/sysctl/90-edge-router.conf
nftables Architecture
The native nftables ruleset uses:
- stateful connection tracking
- default-deny input policy
- default-deny forwarding policy
- named address sets
- named service-port sets
- interface-to-policy verdict maps
- anti-spoofing controls
- management-plane restrictions
- SSH connection-rate tracking
- API connection-rate tracking
- temporary abuse sets
- rate-limited deny logging
- Corporate / DMZ / IoT segmentation
- IPv4 masquerading toward the WAN interface

Configuration:
networking/nftables/edge-zero-trust.nft
Management Security
Management SSH is restricted to approved systems on the management network.
Current trusted management endpoints:
- 10.10.10.1 - Windows workstation
- 10.10.10.100 - DingasHost1 / Ansible control node
Management traffic remains separated from Corporate, DMZ and IoT routing.

Zero-Trust Policy Model
Corporate:
- may reach approved Internet services
- may reach DMZ HTTP/HTTPS services
- does not receive unrestricted access to IoT
DMZ:
- may use approved outbound update/DNS services
- cannot initiate unrestricted Corporate, IoT or management connections
IoT:
- receives highly restricted Internet access
- may use HTTPS, DNS and NTP
- may reach a future DMZ TLS MQTT service on TCP/8883
- cannot initiate unrestricted Corporate or management access
WAN:
- unsolicited inbound forwarding is denied

Validation
The nftables parser validated both the main ruleset and persistent loader:
nft --check --file /etc/nftables/edge-zero-trust.nft
exit status: 0

nft --check --file /etc/sysconfig/nftables.conf
exit status: 0

During controlled cutover testing, nftables loaded successfully and exposed:
table inet edge_filter
table ip edge_nat

A new Windows-to-Host3 TCP/22 connection also succeeded while the ruleset
was active.
Safety Engineering

Firewall changes were protected by a temporary systemd rollback timer.
The rollback procedure:
1. flushed the experimental nftables ruleset
2. stopped nftables
3. restored firewalld

The timer later restored the safe firewall state, demonstrating that the
rollback mechanism operated as designed.
At the end of this phase the host was intentionally left with firewalld
active and nftables inactive rather than claiming a permanent production
cutover.

Next Phase
The next iteration will:
- automate NetworkManager profiles with RHEL System Roles
- template the nftables ruleset with Ansible
- perform repeatable idempotent deployment
- add test workloads to Corporate, DMZ and IoT networks
- validate permitted and denied paths
- collect nftables counters and deny logs
- perform reboot persistence testing
