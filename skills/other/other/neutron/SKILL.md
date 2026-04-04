---
name: openstack-neutron
description: "OpenStack Neutron software-defined networking service. Provides network abstraction for cloud instances including security groups, floating IPs, DHCP, L3 routing, ML2 plugin architecture with OVN/OVS backends, network namespaces, provider and tenant networks, VXLAN/VLAN/flat network types, and port management. Use for deploying, configuring, operating, and troubleshooting OpenStack networking."
user-invocable: true
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-23"
      triggers:
        intents:
          - "neutron"
          - "network"
          - "subnet"
          - "router"
          - "floating ip"
          - "security group"
          - "SDN"
          - "OVN"
          - "OVS"
          - "DHCP"
          - "L3"
          - "port"
        contexts:
          - "deploying openstack networking"
          - "configuring SDN"
          - "troubleshooting network connectivity"
          - "managing security groups"
---

# OpenStack Neutron -- Software-Defined Networking

Neutron is OpenStack's networking service and the most complex component in the stack. It provides the network abstraction layer that connects every instance, container, and service in the cloud. Where physical networking uses cables, switches, and routers, Neutron virtualizes all of these into software constructs that operators manage through APIs.

## Architecture

Neutron uses the **ML2 (Modular Layer 2) plugin** architecture, which separates the network model from the mechanism that implements it. The ML2 plugin supports multiple mechanism drivers -- the two primary backends for Kolla-Ansible deployments are:

- **OVN (Open Virtual Network):** The recommended backend for new deployments. OVN provides distributed virtual routing, native DHCP, and security group implementation without requiring separate agents. It uses a northbound/southbound database architecture for state management.
- **OVS (Open vSwitch):** The legacy backend that uses separate agents for L3 routing, DHCP, and metadata. Each function runs in its own network namespace. More mature but more complex operationally.

**Network types supported:** flat (untagged), VLAN (802.1Q tagged), VXLAN (overlay tunnels), GRE (generic routing encapsulation). Single-node deployments typically use flat for provider networks and VXLAN for tenant networks.

**The agent model (OVS backend):** Neutron runs multiple agents -- `neutron-openvswitch-agent` (L2 connectivity), `neutron-l3-agent` (routing and NAT), `neutron-dhcp-agent` (IP assignment), `neutron-metadata-agent` (instance metadata). Each agent manages its domain through network namespaces. OVN consolidates these into `ovn-controller` on each node.

## Deploy

### Kolla-Ansible Configuration

Key settings in `globals.yml`:

```yaml
# Backend selection (choose one)
neutron_plugin_agent: "ovn"          # Recommended for new deployments
# neutron_plugin_agent: "openvswitch"  # Legacy, more agents to manage

# External network interface (the physical NIC for provider networks)
neutron_external_interface: "eth1"    # Adjust to your hardware

# Provider networks (required for floating IPs and external access)
enable_neutron_provider_networks: "yes"

# DVR (Distributed Virtual Router) -- disable for single-node
enable_neutron_dvr: "no"

# Network types
neutron_tenant_network_types: "vxlan"
neutron_type_drivers: "flat,vlan,vxlan"
```

### Network Bridge Configuration

The external bridge (`br-ex`) connects Neutron to the physical network:

```bash
# Verify the bridge exists after deployment
docker exec openvswitch_vswitchd ovs-vsctl show
# Should show br-ex with neutron_external_interface as a port

# For OVN: verify integration bridge
docker exec openvswitch_vswitchd ovs-vsctl show | grep br-int
```

### Container Verification

```bash
# List Neutron containers
docker ps --format '{{.Names}}' | grep neutron

# Expected containers (OVN backend):
# neutron_server, neutron_ovn_metadata_agent
# Plus OVN containers: ovn_controller, ovn_northd, ovsdb-nb, ovsdb-sb

# Expected containers (OVS backend):
# neutron_server, neutron_openvswitch_agent, neutron_l3_agent,
# neutron_dhcp_agent, neutron_metadata_agent

# Check agent status
openstack network agent list
# All agents should show "alive" and "UP"
```

## Configure

### Provider Networks vs Tenant Networks

- **Provider networks** are mapped to physical network infrastructure. They provide external connectivity and floating IP pools. Created by admins only.
- **Tenant networks** are virtual overlay networks (VXLAN) that tenants create for their instances. Isolated from each other by default.

```bash
# Create a provider network (flat, mapped to physnet1)
openstack network create --share --external \
  --provider-physical-network physnet1 \
  --provider-network-type flat \
  provider-net

# Create a provider subnet with allocation pool
openstack subnet create --network provider-net \
  --subnet-range 192.168.1.0/24 \
  --gateway 192.168.1.1 \
  --allocation-pool start=192.168.1.100,end=192.168.1.200 \
  --dns-nameserver 8.8.8.8 \
  provider-subnet
```

### Subnet Configuration

Key parameters for every subnet: CIDR range, gateway IP, DHCP allocation pool (avoid overlap with static IPs), DNS nameservers, and host routes.

```bash
# Create a tenant subnet with DHCP
openstack subnet create --network tenant-net \
  --subnet-range 10.0.0.0/24 \
  --gateway 10.0.0.1 \
  --dns-nameserver 8.8.8.8 \
  tenant-subnet
```

### Router Configuration

Routers connect tenant networks to provider networks and provide SNAT for outbound traffic and DNAT for floating IPs.

```bash
# Create a router and set its external gateway
openstack router create main-router
openstack router set --external-gateway provider-net main-router
openstack router add subnet main-router tenant-subnet
```

### Security Groups

Default security group policy: **deny all ingress, allow all egress**. Every instance gets the default security group unless overridden.

```bash
# Allow SSH and ICMP
openstack security group rule create --protocol tcp --dst-port 22 default
openstack security group rule create --protocol icmp default

# Allow HTTP/HTTPS
openstack security group rule create --protocol tcp --dst-port 80 default
openstack security group rule create --protocol tcp --dst-port 443 default
```

### Floating IP Pool

Floating IPs are allocated from the provider network's allocation pool and associated with instance ports for external access.

```bash
# Create and assign a floating IP
openstack floating ip create provider-net
openstack server add floating ip my-instance <floating-ip>
```

### MTU Configuration

VXLAN adds 50 bytes of overhead. If your physical MTU is 1500, tenant network MTU must be 1450 or less. Configure jumbo frames (MTU 9000) on the physical network to avoid fragmentation with overlays.

```bash
# Set global MTU in globals.yml
# neutron_mtu: 1500  # Physical network MTU
# Tenant networks auto-calculate: physical_mtu - overlay_overhead
```

### Port Security and Allowed Address Pairs

Port security prevents IP/MAC spoofing. Disable only when required (e.g., for load balancers, VPN gateways).

```bash
# Disable port security on a specific port
openstack port set --no-security-group --disable-port-security <port-id>

# Allow additional IP/MAC pairs on a port
openstack port set --allowed-address ip-address=10.0.0.0/24 <port-id>
```

## Operate

### Network and Subnet Management

```bash
# List networks and subnets
openstack network list
openstack subnet list

# Show detailed network info
openstack network show <network-name>

# Delete a network (must remove all ports first)
openstack port list --network <network-name>
openstack port delete <port-id>
openstack network delete <network-name>
```

### Floating IP Management

```bash
# List floating IPs
openstack floating ip list

# Disassociate and release
openstack server remove floating ip <server> <floating-ip>
openstack floating ip delete <floating-ip>
```

### Security Group Management

```bash
# List security groups and their rules
openstack security group list
openstack security group rule list <group-name>

# Create a custom security group
openstack security group create web-servers --description "HTTP/HTTPS access"
openstack security group rule create --protocol tcp --dst-port 80 web-servers
openstack security group rule create --protocol tcp --dst-port 443 web-servers
```

### Network Namespace Debugging (OVS backend)

```bash
# List all network namespaces
ip netns list
# Format: qdhcp-<network-id>, qrouter-<router-id>

# Execute commands inside a namespace
ip netns exec qrouter-<router-id> ip addr show
ip netns exec qrouter-<router-id> iptables -t nat -L -n -v

# Check DHCP namespace
ip netns exec qdhcp-<network-id> ps aux | grep dnsmasq
```

### Port Diagnostics

```bash
# Show port details including binding status
openstack port show <port-id>

# Check port binding
openstack port show <port-id> -c binding_vif_type -c binding_host_id

# binding_vif_type should be "ovs" or "ovn" -- "binding_failed" means trouble
```

### QoS Policies

```bash
# Create a bandwidth limit policy
openstack network qos policy create bw-limiter
openstack network qos rule create --type bandwidth-limit \
  --max-kbps 10000 --max-burst-kbits 1000 bw-limiter

# Apply to a port
openstack port set --qos-policy bw-limiter <port-id>
```

## Troubleshoot

### Instance Has No Network Connectivity

**Symptoms:** Instance boots but cannot reach its gateway, no IP assigned, or no connectivity to other instances.

**Diagnostic sequence:**

1. **Check port binding:** `openstack port list --server <instance>` -- look at `binding_vif_type`. If `binding_failed`, the mechanism driver could not wire the port. Check neutron-server and agent logs.
2. **Check security groups:** `openstack port show <port-id> -c security_group_ids`. Ensure rules allow the traffic. Default denies all ingress.
3. **Check DHCP:** `openstack port show <port-id> -c fixed_ips`. If IP is assigned but instance does not have it, DHCP may have failed. Check the DHCP agent or OVN DHCP options.
4. **Check network namespace (OVS):** `ip netns exec qdhcp-<net-id> ping <instance-ip>`. If this works, the issue is between the namespace and the instance (OVS flows).
5. **Check OVS flows:** `docker exec openvswitch_vswitchd ovs-ofctl dump-flows br-int | grep <port-tag>`. Missing flows indicate agent synchronization issues.
6. **Check OVN (if applicable):** `docker exec ovn_northd ovn-nbctl show` and `ovn-sbctl show` to verify logical switch and port bindings.

### Floating IP Not Reachable

**Symptoms:** Floating IP assigned but not pingable or accessible from external network.

**Diagnostic sequence:**

1. **Check router gateway:** `openstack router show <router>` -- verify `external_gateway_info` is set to the provider network.
2. **Check SNAT/DNAT rules (OVS):** `ip netns exec qrouter-<router-id> iptables -t nat -L -n -v`. Look for DNAT rules mapping the floating IP to the fixed IP.
3. **Check external bridge:** `docker exec openvswitch_vswitchd ovs-vsctl show` -- verify `br-ex` exists and the physical interface is attached.
4. **Check ARP:** From the external network, `arping <floating-ip>`. If no response, the L3 agent is not responding for this IP.
5. **Check security groups:** Floating IP traffic must pass through security group rules on the instance port. Ensure ICMP/SSH/HTTP is allowed.
6. **Check OVN gateway chassis:** `docker exec ovn_northd ovn-nbctl lr-nat-list <router>` to verify NAT rules exist.

### DHCP Failures

**Symptoms:** Instance boots without an IP address or gets the wrong IP.

**Diagnostic sequence:**

1. **Check agent status:** `openstack network agent list | grep dhcp`. Agent must be alive.
2. **Check namespace (OVS):** `ip netns exec qdhcp-<net-id> ps aux | grep dnsmasq`. The dnsmasq process should be running.
3. **Check lease file:** `ip netns exec qdhcp-<net-id> cat /var/lib/neutron/dhcp/<net-id>/leases`. Verify the instance MAC is listed.
4. **Check subnet DHCP:** `openstack subnet show <subnet> -c enable_dhcp`. Must be `True`.
5. **Check port DHCP options:** `openstack port show <port-id> -c extra_dhcp_opts`.
6. **OVN DHCP:** `docker exec ovn_northd ovn-nbctl list DHCP_Options` to verify DHCP options are programmed.

### Security Group Rules Not Applying

**Symptoms:** Traffic that should be allowed is blocked, or traffic that should be blocked passes through.

**Diagnostic sequence:**

1. **Verify rules:** `openstack security group rule list <group>`. Check direction (ingress/egress), protocol, port range, and remote IP prefix.
2. **Check port security:** `openstack port show <port-id> -c port_security_enabled`. If disabled, security groups are bypassed entirely.
3. **Check OVS flows (OVS backend):** `docker exec openvswitch_vswitchd ovs-ofctl dump-flows br-int | grep <port-tag>`. Stale flows may not reflect current rules. Restart the OVS agent to force a resync.
4. **Check conntrack:** Stateful rules track connections. A rule change does not affect existing connections. Restart the instance or flush conntrack entries.
5. **OVN ACLs:** `docker exec ovn_northd ovn-nbctl acl-list <logical-switch>` to verify ACL rules match security group intent.

### Network Creation Fails

**Symptoms:** `openstack network create` returns an error about VLAN IDs, provider network, or type driver.

**Diagnostic sequence:**

1. **Check type drivers:** Verify `neutron_type_drivers` in `globals.yml` includes the requested type.
2. **VLAN range exhaustion:** Check `ml2_conf.ini` for `network_vlan_ranges`. If the range is exhausted, extend it or clean up unused networks.
3. **Provider network misconfigured:** Verify `physnet` name matches between `ml2_conf.ini` (`flat_networks`, `network_vlan_ranges`) and `bridge_mappings` in the OVS agent config.
4. **VXLAN VNI range:** Check `vni_ranges` in ML2 config. Default range is large (1:65535) but can be exhausted in heavily used environments.

### MTU / Fragmentation Issues

**Symptoms:** Large packets fail, SSH works but SCP stalls, or HTTP transfers hang after initial handshake.

**Diagnostic sequence:**

1. **Check MTU chain:** Physical NIC MTU minus VXLAN overhead (50 bytes) must equal tenant network MTU. If physical is 1500, tenant must be 1450.
2. **Test with ping:** `ping -M do -s 1400 <target>` (do not fragment). Reduce size until it works to find the effective MTU.
3. **Check path MTU discovery:** Verify ICMP type 3 code 4 (fragmentation needed) is not blocked by security groups or firewalls.
4. **Jumbo frames:** If the physical network supports MTU 9000, set `neutron_mtu: 9000` in `globals.yml` to eliminate VXLAN overhead issues.

### OVN/OVS Specific Issues

**Symptoms:** Networking intermittently fails, port binding fails, or flows are stale.

**Diagnostic sequence:**

1. **OVS status:** `docker exec openvswitch_vswitchd ovs-vsctl show` -- check bridge configuration, port attachments, error states.
2. **OVN database sync:** `docker exec ovn_northd ovn-nbctl show` (northbound) and `docker exec ovn_controller ovn-sbctl show` (southbound). Compare expected vs actual logical topology.
3. **OVS flow table:** `docker exec openvswitch_vswitchd ovs-ofctl dump-flows br-int` -- look for flows with zero packet counts (unused) or unusually high counts (possible loop).
4. **OVN controller connectivity:** `docker exec ovn_controller ovn-appctl connection-status` -- should report `connected`. If not, check ovsdb-server connectivity.
5. **Database compaction:** Large OVN databases can slow operations. Check database size and compact if needed: `docker exec ovn_northd ovsdb-tool compact /var/lib/openvswitch/ovnnb_db.db`.

## Integration Points

- **Keystone:** All Neutron API calls require Keystone authentication. Neutron registers `network` service and endpoint in the Keystone catalog. Service user `neutron` authenticates against Keystone for internal operations.
- **Nova:** When an instance boots, Nova requests Neutron to create a port on the specified network. The port binding process wires the instance's virtual NIC to the OVS/OVN bridge. Nova also queries Neutron for security group rules and network metadata.
- **Metadata service:** Neutron proxies the metadata service (169.254.169.254) to Nova's metadata API. The metadata agent (or OVN metadata agent) runs in the network namespace and forwards requests.
- **Octavia (LBaaS):** Load Balancer as a Service uses Neutron networks for VIP allocation, member connectivity, and health monitoring. Octavia creates ports on Neutron networks for its amphora instances.
- **VPNaaS:** VPN as a Service extends Neutron with IPsec VPN capabilities. It creates router-based VPN connections using the L3 agent infrastructure.

## NASA SE Cross-References

| SE Phase | Neutron Activity | Reference |
|----------|-----------------|-----------|
| Phase B (Preliminary Design) | Design network topology: management, tenant, provider, and storage network separation. Select ML2 mechanism driver (OVN vs OVS). Plan VXLAN/VLAN segmentation. Define security group strategy. | SP-6105 SS 4.3-4.4 |
| Phase C (Final Design & Build) | Configure `globals.yml` networking parameters. Set up external bridge. Configure MTU and network type drivers. Define provider network mappings. | SP-6105 SS 5.1 |
| Phase D (Integration & Test) | Verify network connectivity end-to-end: instance-to-instance, instance-to-external, floating IP reachability. Verify security group enforcement. Test DHCP assignment. Verify metadata service. | SP-6105 SS 5.2-5.3 |
| Phase E (Operations) | Day-2 network management: create/modify networks and subnets, manage floating IPs, update security groups, monitor agent health, debug connectivity issues, manage QoS policies. | SP-6105 SS 5.4-5.5 |
