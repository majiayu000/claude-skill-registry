---
name: openstack-networking-debug
description: "OpenStack networking debug operations skill for SDN troubleshooting, packet tracing, and flow analysis. Covers OVS/OVN debugging (ovs-vsctl, ovs-ofctl, ovs-appctl, ovn-nbctl, ovn-sbctl, ovn-trace), security group analysis via OVS flow rules and conntrack, DHCP troubleshooting through namespace inspection and dnsmasq diagnostics, floating IP diagnosis with NAT rule and ARP verification, network namespace inspection (ip netns), MTU chain analysis for overlay networks, DNS resolution debugging, and east-west traffic diagnosis. Use when diagnosing network connectivity failures, tracing packets through the SDN stack, or analyzing flow tables in a running OpenStack cloud."
user-invocable: true
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-23"
      triggers:
        intents:
          - "network debug"
          - "packet trace"
          - "flow analysis"
          - "connectivity"
          - "OVS"
          - "OVN"
          - "DHCP"
          - "floating IP"
          - "security group"
          - "namespace"
          - "MTU"
        contexts:
          - "troubleshooting network connectivity"
          - "debugging SDN"
          - "analyzing packet flows"
          - "diagnosing floating IP issues"
---

# OpenStack Networking Debug -- SDN Troubleshooting Operations

Networking debug is the most hands-on troubleshooting domain in cloud operations. Virtual networks add multiple abstraction layers between user intent and physical packets -- an instance's traffic passes through a tap device, a Linux bridge or OVS port, integration bridge flows, tunnel encapsulation, and physical NIC before reaching the wire. When connectivity breaks, the operator must trace through every layer to find where packets stop flowing.

**The debugging mental model:** Start at the instance and trace outward. The packet path for a tenant instance is: instance vNIC -> tap device -> qbr bridge (if OVS with iptables) -> OVS br-int -> tunnel or VLAN tag -> OVS br-ex (for external traffic) -> physical NIC. For OVN, the path simplifies: instance vNIC -> OVS br-int (with OVN flows) -> tunnel or physical port. Every hop is inspectable. Every hop can be the failure point.

This skill is the primary reference for the CRAFT-network agent when diagnosing connectivity issues during Phase E operations.

## Deploy

### Debug Tooling Setup

Verify all diagnostic tools are available before beginning any debug session.

**OVS diagnostic commands** (available inside `openvswitch_vswitchd` container):

```bash
# Verify OVS tools are accessible
docker exec openvswitch_vswitchd ovs-vsctl --version
docker exec openvswitch_vswitchd ovs-ofctl --version
docker exec openvswitch_vswitchd ovs-appctl --version

# Show complete OVS configuration
docker exec openvswitch_vswitchd ovs-vsctl show
```

**OVN diagnostic commands** (available inside `ovn_northd` and `ovn_controller` containers):

```bash
# Verify OVN tools
docker exec ovn_northd ovn-nbctl --version
docker exec ovn_northd ovn-sbctl --version

# OVN trace (powerful logical packet tracing)
docker exec ovn_controller ovn-trace --version
```

**Network namespace tools** (on the host or inside Neutron containers):

```bash
# List all network namespaces
ip netns list
# Expected: qrouter-<id>, qdhcp-<id> (OVS backend)
# OVN uses fewer namespaces (metadata only)
```

**Packet capture** (tcpdump inside containers or namespaces):

```bash
# Capture on a tap interface (instance-facing)
tcpdump -i tap<port-id-prefix> -n -c 50

# Capture inside a network namespace
ip netns exec qrouter-<router-id> tcpdump -i qr-<port-prefix> -n -c 50

# Capture on physical NIC
tcpdump -i eth1 -n port 4789  # VXLAN traffic
```

### Kolla-Ansible Debug Container Options

For persistent debug environments, Kolla-Ansible provides tooling containers:

```bash
# Enter the neutron_server container for API-level debugging
docker exec -it neutron_server /bin/bash

# Enter openvswitch_vswitchd for flow-level debugging
docker exec -it openvswitch_vswitchd /bin/bash

# Enter the relevant agent container for namespace access
docker exec -it neutron_l3_agent /bin/bash   # OVS backend
docker exec -it neutron_dhcp_agent /bin/bash # OVS backend
```

## Configure

### OVS Logging Levels

Adjust OVS logging to capture more detail during active debugging, then restore to production levels.

```bash
# Increase OVS daemon logging (temporary, resets on restart)
docker exec openvswitch_vswitchd ovs-appctl vlog/set vswitchd:dbg
docker exec openvswitch_vswitchd ovs-appctl vlog/set ofproto:dbg

# Restore production logging
docker exec openvswitch_vswitchd ovs-appctl vlog/set vswitchd:warn
docker exec openvswitch_vswitchd ovs-appctl vlog/set ofproto:warn

# Check current log levels
docker exec openvswitch_vswitchd ovs-appctl vlog/list
```

### OVN Tracing Enablement

OVN trace simulates a packet through the logical pipeline without sending real traffic.

```bash
# Trace a packet from a logical port through OVN
docker exec ovn_controller ovn-trace <datapath> \
  'inport == "<logical-port>" && eth.src == <mac> && eth.dst == <mac> \
   && ip4.src == <src-ip> && ip4.dst == <dst-ip> && ip.ttl == 64'
```

### Neutron Agent Debug Logging

Enable debug logging on individual agents for detailed event tracing.

```bash
# Check current log level
docker exec neutron_server grep -i "debug" /etc/neutron/neutron.conf

# Enable debug via Kolla-Ansible config override
# In /etc/kolla/config/neutron/neutron.conf:
# [DEFAULT]
# debug = True

# After config change, reconfigure the service
# kolla-ansible -i inventory reconfigure --tags neutron
```

### Packet Capture Setup

```bash
# Identify the tap device for an instance port
openstack port show <port-id> -c id
# Tap device name: tap<first-11-chars-of-port-id>

# Identify the OVS port number for correlation with flow tables
docker exec openvswitch_vswitchd ovs-vsctl --columns=name,ofport list Interface | grep tap

# Set up continuous capture with rotation (for intermittent issues)
tcpdump -i tap<prefix> -n -w /tmp/capture-%H%M.pcap -G 300 -W 12
```

### Flow Table Inspection Setup

```bash
# Dump all flow tables on br-int (primary integration bridge)
docker exec openvswitch_vswitchd ovs-ofctl dump-flows br-int

# Dump flows for a specific table (table 0 = ingress classification)
docker exec openvswitch_vswitchd ovs-ofctl dump-flows br-int table=0

# Watch flows in real-time (shows packet/byte counts)
docker exec openvswitch_vswitchd ovs-ofctl dump-flows br-int --no-stats=false
```

## Operate

### Connectivity Diagnosis Workflow

**Scenario:** Instance cannot reach the external network.

**Step-by-step trace from instance outward:**

1. **Verify the instance has an IP:** `openstack server show <instance> -c addresses`
2. **Check the port is bound:** `openstack port show <port-id> -c binding_vif_type` -- must be `ovs` or `ovn`, not `binding_failed`
3. **Check the tap device exists:** `ip link show tap<port-prefix>` -- if missing, the port was not wired by the agent
4. **Check OVS port attachment:** `docker exec openvswitch_vswitchd ovs-vsctl list-ports br-int | grep <port-prefix>`
5. **Trace through br-int flows:** `docker exec openvswitch_vswitchd ovs-ofctl dump-flows br-int | grep <port-tag>` -- look for matching ingress/egress rules
6. **Check the router namespace (OVS):** `ip netns exec qrouter-<router-id> ip route` -- verify the default route points to the external gateway
7. **Check br-ex configuration:** `docker exec openvswitch_vswitchd ovs-vsctl list-ports br-ex` -- the physical NIC must be attached
8. **Check the physical NIC:** `ip link show <nic>` -- verify it is UP, check for errors with `ip -s link show <nic>`

### DHCP Troubleshooting

**Scenario:** Instance gets no IP address.

1. **Check DHCP agent (OVS):** `openstack network agent list | grep dhcp` -- must show `alive` and `UP`
2. **Check DHCP namespace:** `ip netns exec qdhcp-<network-id> ps aux | grep dnsmasq` -- dnsmasq must be running
3. **Capture DHCP traffic:** `ip netns exec qdhcp-<network-id> tcpdump -i tap<dhcp-port-prefix> -n port 67 or port 68 -c 20`
   - Run `openstack server reboot <instance>` to trigger a DHCP request
   - Look for: DHCP Discover (from instance), DHCP Offer (from dnsmasq), DHCP Request, DHCP Ack
   - Missing Discover: instance network stack or tap device issue
   - Discover but no Offer: dnsmasq config or port mismatch
4. **Check lease file:** `ip netns exec qdhcp-<network-id> cat /var/lib/neutron/dhcp/<network-id>/leases`
5. **OVN DHCP:** `docker exec ovn_northd ovn-nbctl list DHCP_Options` -- verify DHCP options are programmed for the subnet

### Floating IP Diagnosis

**Scenario:** Cannot reach instance from external network via floating IP.

1. **Verify floating IP assignment:** `openstack floating ip show <fip>` -- check `fixed_ip_address` and `floating_ip_address` fields, confirm `port_id` is set
2. **Check router namespace (OVS):** `ip netns exec qrouter-<router-id> ip addr show` -- the floating IP must appear on the `qg-<port>` interface
3. **Check NAT rules:** `ip netns exec qrouter-<router-id> iptables -t nat -L -n -v` -- look for DNAT rule mapping floating IP to fixed IP
4. **Check ARP on external network:** `arping -I <external-iface> <floating-ip>` -- if no response, the L3 agent is not answering ARP for this IP
5. **Check security groups:** The instance port's security groups must allow the traffic (ICMP for ping, TCP 22 for SSH)
6. **OVN NAT:** `docker exec ovn_northd ovn-nbctl lr-nat-list <router-name>` -- verify dnat_and_snat entry exists

### Security Group Analysis

**Scenario:** Traffic blocked that should be allowed.

1. **List applied rules:** `openstack security group rule list <group> --long` -- check protocol, port range, direction, remote prefix
2. **Check port security is enabled:** `openstack port show <port-id> -c port_security_enabled` -- if `False`, security groups are bypassed entirely
3. **Decode OVS flows:** `docker exec openvswitch_vswitchd ovs-ofctl dump-flows br-int | grep <port-tag>` -- match flow rules against security group rules
4. **Check conntrack state:** Security groups are stateful. Existing connections persist after rule changes. Check conntrack: `conntrack -L | grep <instance-ip>`
5. **Force flow resync:** Restart the OVS agent to regenerate all flows: `docker restart neutron_openvswitch_agent`
6. **OVN ACLs:** `docker exec ovn_northd ovn-nbctl acl-list <logical-switch>` -- verify ACLs match security group intent

### MTU Issues

**Scenario:** Large packets fail, SSH works but SCP stalls, HTTP transfers hang.

1. **Check physical NIC MTU:** `ip link show <nic> | grep mtu` -- note the value (typically 1500 or 9000)
2. **Check overlay overhead:** VXLAN = 50 bytes, GRE = 42 bytes. Tenant MTU = physical MTU - overhead
3. **Test effective MTU:** `ping -M do -s 1400 <target>` -- decrease size until it works; that is the effective MTU
4. **Check DHCP-advertised MTU:** `openstack subnet show <subnet> -c mtu` -- must match the calculated tenant MTU
5. **Check instance MTU:** Inside the instance, `ip link show eth0 | grep mtu` -- must match the subnet MTU
6. **Fix:** Set `neutron_mtu` in `globals.yml` to match physical MTU, then `kolla-ansible reconfigure --tags neutron`

### DNS Resolution

**Scenario:** Instance cannot resolve hostnames.

1. **Check DHCP options:** `openstack subnet show <subnet> -c dns_nameservers` -- must have at least one DNS server
2. **Check inside instance:** `cat /etc/resolv.conf` -- should list the DNS server from DHCP options
3. **Check DNS connectivity:** `ip netns exec qdhcp-<network-id> nslookup google.com <dns-server>` -- test DNS from the DHCP namespace
4. **Check metadata agent:** DNS may fail if the metadata service is also broken: `curl http://169.254.169.254/latest/meta-data/` from inside the instance

## Troubleshoot

### Instance Has No Network Connectivity

**Symptoms:** Instance boots, may or may not have an IP, cannot reach gateway or other instances.

**Resolution steps:**
1. Run `openstack port list --server <instance>` -- get the port ID
2. Check `binding_vif_type` -- if `binding_failed`, check agent logs: `docker logs neutron_openvswitch_agent --tail 100`
3. Verify tap device exists on host: `ip link show tap<port-prefix>`
4. If tap missing: restart the OVS agent or the instance. Check if the compute host matches the port's `binding_host_id`
5. If tap exists but no connectivity: dump flows and trace packet path through OVS
6. Check for wrong VLAN tag: `docker exec openvswitch_vswitchd ovs-vsctl get port tap<prefix> tag` -- compare with expected network segmentation ID
7. Check namespace routing: `ip netns exec qrouter-<id> ip route` -- missing default route means no external connectivity

### Floating IP Unreachable from External

**Symptoms:** Floating IP assigned in OpenStack but not reachable from the external network.

**Resolution steps:**
1. Verify router has external gateway: `openstack router show <router> -c external_gateway_info`
2. Check qrouter namespace exists: `ip netns list | grep qrouter`
3. If namespace missing: restart L3 agent: `docker restart neutron_l3_agent`
4. Check NAT rules in namespace: `ip netns exec qrouter-<id> iptables -t nat -S` -- DNAT and SNAT rules must exist
5. If NAT rules absent: `openstack floating ip set --port <port-id> <fip>` to reassociate
6. Check ARP resolution: `arping -c 3 -I <external-iface> <floating-ip>` on a machine on the external network
7. If ARP fails: check br-ex has the physical interface: `docker exec openvswitch_vswitchd ovs-vsctl list-ports br-ex`

### Inter-Tenant Traffic Leaking

**Symptoms:** Instances in different projects can communicate when they should not.

**Resolution steps:**
1. Check VXLAN/VLAN segmentation IDs: `openstack network show <net1> -c provider:segmentation_id` and compare with net2 -- collision means shared L2 domain
2. Check security groups on both ports: `openstack port show <port> -c security_group_ids` -- default groups deny cross-tenant ingress
3. Inspect OVS flow tables: `docker exec openvswitch_vswitchd ovs-ofctl dump-flows br-int` -- look for flows that bridge between different tunnel IDs
4. Check for shared networks: `openstack network show <net> -c shared` -- shared networks are accessible across projects by design
5. Flow table corruption: restart OVS agent to force full flow resync: `docker restart neutron_openvswitch_agent`

### DHCP Failures

**Symptoms:** Instance boots without IP address, gets wrong IP, or IP assignment is delayed.

**Resolution steps:**
1. Check agent status: `openstack network agent list | grep dhcp` -- must be alive
2. Check namespace: `ip netns list | grep qdhcp-<network-id>` -- if missing, restart DHCP agent
3. Check dnsmasq process: `ip netns exec qdhcp-<network-id> ps aux | grep dnsmasq` -- if not running, check agent logs
4. Check port mismatch: compare `openstack port list --network <net> --device-owner network:dhcp` with the dnsmasq config file
5. OVN: `docker exec ovn_northd ovn-nbctl list DHCP_Options` -- verify subnet options exist and contain correct CIDR

### Metadata Service Unreachable

**Symptoms:** Instance cannot reach 169.254.169.254, cloud-init fails, SSH key injection fails.

**Resolution steps:**
1. Check metadata agent: `docker ps | grep metadata` -- container must be running
2. Check metadata proxy routing: `ip netns exec qrouter-<id> iptables -t nat -S | grep 169.254` -- a DNAT rule must redirect metadata requests
3. Check Nova metadata API: `curl http://localhost:8775/` from the controller -- must return metadata API version list
4. Check Neutron metadata proxy config: `docker exec neutron_metadata_agent cat /etc/neutron/metadata_agent.ini | grep nova_metadata`
5. OVN: metadata is served by `neutron_ovn_metadata_agent` running in a namespace on the chassis hosting the instance

### East-West Traffic Between Instances Fails

**Symptoms:** Instances on the same or different subnets cannot communicate.

**Resolution steps:**
1. **Same subnet:** Traffic stays on br-int. Check that both ports are on the same VLAN tag: `docker exec openvswitch_vswitchd ovs-vsctl get port tap<prefix1> tag` vs `tap<prefix2>`
2. **Different subnets:** Traffic routes through the router namespace. Check `ip netns exec qrouter-<id> ip route` -- both subnets must be present
3. Check security groups: default egress is allow-all, but default ingress denies all. Both instances need rules permitting each other's traffic
4. Check ARP tables inside namespaces: `ip netns exec qrouter-<id> arp -n` -- missing entries indicate L2 reachability problems
5. Test from namespace: `ip netns exec qrouter-<id> ping <instance-ip>` -- if this works, the issue is between the namespace and the instance

## Integration Points

- **Neutron skill:** Core networking knowledge. Networking-debug extends Neutron's troubleshooting section with deeper diagnostic procedures and systematic trace workflows. Load Neutron skill first for architecture context, then networking-debug for active troubleshooting.
- **Security skill:** Security group analysis is a core part of network debugging. When traffic is unexpectedly blocked, cross-reference security group rules with OVS flow tables. Security skill provides the policy layer; this skill provides the enforcement inspection layer.
- **Monitoring skill:** Network metrics (packet drops, interface errors, latency, bandwidth utilization) guide where to start debugging. High packet drops on br-int suggest flow issues. High latency on tunnel interfaces suggests overlay problems. Check monitoring dashboards before diving into packet traces.
- **Capacity skill:** Network resource exhaustion causes connectivity failures. Floating IP pool depletion prevents external access. Port quota exhaustion prevents new instances from getting network connectivity. Subnet address pool exhaustion prevents DHCP assignment. When debugging connectivity, verify resource availability first.
- **Nova skill:** Instance networking depends on Nova's port binding workflow. When an instance has no connectivity, the first question is whether Nova successfully requested a port from Neutron and whether the compute host wired the tap device. Nova logs contain the port binding request; Neutron logs contain the binding response.
- **CRAFT-network agent:** Primary consumer of this skill. The CRAFT-network agent activates networking-debug when keywords like "connectivity," "packet trace," "flow analysis," or "debug" appear in the problem context. The agent uses the systematic diagnostic workflows in this skill to trace issues methodically.

## NASA SE Cross-References

| SE Phase | Networking Debug Activity | Reference |
|----------|--------------------------|-----------|
| Phase D (Integration & Test) | Network integration testing: verify end-to-end connectivity through the SDN stack, validate security group enforcement, confirm DHCP assignment across all network types, test floating IP reachability from external networks. Each test exercises a different segment of the packet path. | SP-6105 SS 5.2 (Product Integration -- service interface verification) |
| Phase E (Operations) | Operational network troubleshooting: diagnose connectivity failures using the systematic trace workflows in this skill. Every troubleshooting procedure follows the "observe symptom, form hypothesis, test hypothesis, resolve or escalate" pattern from NASA's anomaly resolution process. | SP-6105 SS 5.4 (Product Validation -- operational environment verification) |
| Phase E (Sustainment) | Network configuration changes during operations: MTU adjustments, security group updates, new network creation. Each change requires verification using the diagnostic procedures in this skill to confirm the change achieved the intended effect without side effects. | NPR 7123.1 SS 5.4 (Sustainment -- operational baseline management) |
