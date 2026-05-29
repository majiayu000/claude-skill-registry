---
name: network-diagnostics
description: Automated network troubleshooting and diagnostics for WSL/Linux environments
---

# Network-diagnostics

## Instructions

For network troubleshooting:
1. **MTU Issues** (common in WSL)
   - Check current MTU: ip link show
   - Test different MTU: sudo ip link set dev eth0 mtu 1350
   - Common WSL MTU: 1300-1400
2. **DNS Resolution**
   - Check /etc/resolv.conf
   - Test with: dig google.com, nslookup google.com
   - Try different DNS: 8.8.8.8, 1.1.1.1
3. **Connectivity Tests**
   - Ping gateway: ip route | grep default
   - Traceroute to destination
   - Test ports: nc -zv host port, telnet host port
4. **Firewall/Routing**
   - Check iptables: sudo iptables -L
   - Review routes: ip route show
   - WSL: Check Windows Firewall
5. **Service Status**
   - Verify service is running
   - Check listening ports: ss -tlnp, netstat -tlnp
- Generate scripts to persist fixes
- Include checks for WSL vs native Linux
- Add rollback mechanisms


## Examples

Add examples of how to use this skill here.

## Notes

- This skill was auto-generated
- Edit this file to customize behavior
