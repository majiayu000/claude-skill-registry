---
name: x-cmd-network
description: This skill provides comprehensive network administration and diagnostic tools through x-cmd CLI, including network scanning with Nmap, ARP table management, DNS configuration, routing table analysis, and enhanced ping utilities. This skill should be used when users need to perform network diagnostics, troubleshoot connectivity issues, analyze network topology, or monitor network performance from command line interfaces.
---

# x-cmd Network Administration Tools

## Overview

This skill provides professional network administration and diagnostic capabilities through the x-cmd ecosystem. The tools enable network administrators, security professionals, and system administrators to perform comprehensive network analysis, troubleshoot connectivity issues, and monitor network infrastructure directly from the terminal.

## Available Tools

### Network Scanning (nmap)
Comprehensive network discovery and security scanning.

- **Usage**: `x nmap [options] [targets]`
- **Key capabilities**:
  - Host discovery and port scanning
  - Service and version detection
  - OS fingerprinting
  - Scriptable vulnerability scanning
  - Network mapping and topology discovery
- **Examples**:
  - `x nmap -v -A scanme.nmap.org` - Comprehensive scan with OS detection
  - `x nmap -v -sn 192.168.0.0/16` - Host discovery only
  - `x nmap -p 22,80,443 192.168.1.0/24` - Targeted port scanning
  - `x nmap -O --traceroute target.com` - OS detection with traceroute

### ARP Table Management (arp)
Enhanced ARP cache analysis with multiple output formats.

- **Usage**: `x arp [flags]`
- **Key features**:
  - Interactive TUI application for ARP table viewing
  - Multiple output formats (CSV, TSV, TUI)
  - MAC address vendor lookup
  - Suspicious entry detection
  - Complete ARP table display
- **Examples**:
  - `x arp` - Auto-detect output format (TUI/TSV)
  - `x arp --all` - Show all ARP entries including incomplete
  - `x arp --csv` - CSV format output
  - `x arp --app` - Interactive TUI application

### DNS Configuration (dns)
Domain Name System management and troubleshooting.

- **Usage**: `x dns [subcommand]`
- **Key subcommands**:
  - `current` - View current DNS configuration
  - `ls` - List available DNS servers
  - `refresh` - Flush DNS cache
  - `set` - Configure DNS settings (experimental)
- **Examples**:
  - `x dns` - View current DNS configuration
  - `x dns current` - Detailed DNS configuration
  - `x dns refresh` - Flush DNS cache
  - `x dns ls` - List available DNS servers

### Routing Table Analysis (route)
Enhanced routing table management and analysis.

- **Usage**: `x route [subcommand]`
- **Key features**:
  - Route table display and analysis
  - Multiple output formats
  - Experimental status with ongoing development
- **Examples**:
  - `x route` - Display routing table
  - `x route --csv` - CSV format output
  - `x route ls` - List routing information

### Enhanced ICMP Ping (ping)
Advanced ping utility with visualization capabilities.

- **Usage**: `x ping [flags] [target]`
- **Key features**:
  - Default ping to bing.com for quick testing
  - Heatmap visualization of ping results
  - Bar chart display of latency data
  - Multiple output formats (CSV, TSV, raw)
  - Visual processing of existing ping data
- **Examples**:
  - `x ping` - Default ping to bing.com
  - `x ping 8.8.8.8` - Ping specific target
  - `x ping --heatmap 8.8.8.8` - Heatmap visualization
  - `x ping --bar google.com` - Bar chart display
  - `ping google.com | x ping vis --heatmap` - Process existing ping data

### TCP Port Ping (tping)
TCP-based connectivity testing for service availability.

- **Usage**: `x tping [flags] [target:port]`
- **Key features**:
  - TCP connectivity testing using curl
  - Default port 80 testing
  - Heatmap and bar chart visualizations
  - Multiple output formats
  - Integration with cosmo curl for better compatibility
- **Examples**:
  - `x tping bing.com` - TCP ping to port 80
  - `x tping --heatmap bing.com` - Heatmap visualization
  - `x tping --bar bing.com:80` - Bar chart display
  - `x tping google.com:443` - Test HTTPS connectivity

## Network Administration Use Cases

### Network Discovery and Mapping
- Use `x nmap` for comprehensive network scanning
- Use `x arp` for local network device discovery
- Use `x route` for routing topology analysis
- Use `x ping` for host availability testing

### Connectivity Troubleshooting
- Use `x ping` for basic ICMP connectivity testing
- Use `x tping` for TCP service availability testing
- Use `x dns` for DNS configuration verification
- Use `x dns refresh` for DNS cache troubleshooting

### Network Security Assessment
- Use `x nmap` for vulnerability scanning
- Use `x arp` for ARP spoofing detection
- Use `x tping` for service enumeration
- Use `x nmap -sS` for stealth port scanning

### Performance Monitoring
- Use `x ping --heatmap` for latency trend analysis
- Use `x tping --bar` for TCP connection performance
- Use `x nmap` for service response time measurement
- Use `x arp` for network device monitoring

## Installation and Setup

### Prerequisites
- x-cmd CLI installed
- Network connectivity for external testing
- Appropriate permissions for network scanning

### Platform-Specific Requirements

#### Network Scanning (nmap)
- Nmap installation required for full functionality
- Administrator/root privileges for certain scan types
- Network interface access for raw packet operations

#### DNS Management
- Works across all platforms
- May require administrative privileges for configuration changes
- Internet connectivity for external DNS testing

#### Enhanced Ping Utilities
- Works across all platforms
- No special privileges required for basic functionality
- Terminal support for visualizations

### Configuration

#### Nmap Integration
```bash
# Verify nmap installation
x nmap --help
```

#### DNS Configuration
```bash
# Check current DNS settings
x dns current
```

#### Network Interface Setup
```bash
# View ARP table for network analysis
x arp --app
```

## Integration with Other Tools

### Data Processing
- Pipe output to `x jq` for JSON processing
- Use with `@zh` for Chinese translation of network data
- Export to CSV/TSV for spreadsheet analysis

### Security Integration
- Combine with `x shodan` for external network intelligence
- Use with `x osv` for vulnerability correlation
- Integrate with `x kev` for known vulnerability checking

### Monitoring and Automation
- Combine with shell scripts for automated network monitoring
- Schedule regular network health checks
- Create custom network diagnostic workflows

## Troubleshooting

### Common Issues
- **Permission errors**: Ensure appropriate privileges for network operations
- **Network connectivity**: Verify internet connection for external testing
- **Scan limitations**: Some nmap features require elevated privileges
- **DNS resolution**: Check network configuration for DNS issues

### Performance Optimization
- Use specific scan targets rather than broad ranges
- Limit scan intensity for production networks
- Cache results when appropriate for monitoring
- Use visual interfaces for complex analysis

### Security Considerations
- **Responsible scanning**: Only scan networks you own or have permission to test
- **Legal compliance**: Ensure network scanning complies with local laws
- **Rate limiting**: Respect network resources and avoid aggressive scanning
- **Documentation**: Maintain records of authorized network testing

## Support and Resources

- **x-cmd Network Documentation**: https://x-cmd.com/mod/network
- **Nmap Official Documentation**: https://nmap.org/docs.html
- **ARP Management**: https://x-cmd.com/mod/arp
- **DNS Configuration**: https://x-cmd.com/mod/dns
- **Enhanced Ping**: https://x-cmd.com/mod/ping
- **TCP Ping**: https://x-cmd.com/mod/tping

For additional help:
- Use `x [tool] --help` for specific tool documentation
- Visit individual module pages for detailed usage
- Check platform-specific requirements for network operations
- Consult network administration best practices for responsible usage