---
name: x-cmd-system
description: This skill provides comprehensive system administration and monitoring tools through x-cmd CLI, including process management, macOS system utilities, network configuration, disk health monitoring, and storage analysis. This skill should be used when users need to perform system administration tasks, monitor system performance, manage network configurations, or troubleshoot system issues from command line interfaces.
---

# x-cmd System Administration Tools

## Overview

This skill provides professional system administration and monitoring capabilities through the x-cmd ecosystem. The tools enable system administrators, developers, and power users to manage processes, monitor system health, configure network settings, and analyze storage directly from the terminal.

## Available Tools

### Process Management (ps)
Enhanced process monitoring and management with interactive interfaces.

- **Usage**: `x ps [flags]`
- **Key features**:
  - Interactive CSV application for process viewing
  - FZF-based interactive process selection
  - Multiple output formats (CSV, TSV, JSON)
  - Process data conversion utilities
- **Examples**:
  - `x ps` - Interactive process viewer
  - `x ps fz` - FZF-based process selection
  - `x ps --csv` - CSV format output
  - `ps -ef | x ps --tojson` - Convert process data to JSON

### macOS System Utilities (mac)
Comprehensive macOS management and automation tools.

- **Usage**: `x mac [subcommand]`
- **Key subcommands**:
  - `info` - Display system information
  - `battery` - Battery status and health
  - `disk` - Disk management
  - `vol` - Volume control
  - `lock` - Desktop lock screen
  - `sleep` - Enter sleep mode
  - `net` - Network management
  - `wifi` - Wi-Fi configuration
- **Examples**:
  - `x mac info` - Display system information
  - `x mac b` - Get battery information
  - `x mac vol set 24` - Set output volume to 24%
  - `x mac lock` - Lock desktop
  - `x mac net test` - Test network quality

### Network Configuration (ip)
Advanced IP address management and network analysis.

- **Usage**: `x ip [subcommand]`
- **Key subcommands**:
  - `ls` - List all local IP addresses
  - `geolite` - IP geolocation lookup
  - `config` - Network interface configuration
  - `addr` - IP address information
  - `cidr` - CIDR network calculations
  - `map` - Active host discovery
  - `tcp-portscan` - TCP port scanning
- **Examples**:
  - `x ip` - List all local IP addresses
  - `x ip geolite 8.8.8.8` - Get IP geolocation
  - `x ip map` - Discover active hosts in network
  - `x ip tcp-portscan` - TCP port discovery

### Disk Health Monitoring (smart)
SMART disk health monitoring and analysis.

- **Usage**: `x smart [flags] [device]`
- **Key features**:
  - Interactive disk selection interface
  - Comprehensive SMART data display
  - Root privilege handling automation
  - Integration with AI analysis tools
- **Examples**:
  - `x smart` - Interactive disk health viewer
  - `x smart -a /dev/disk0` - Display all SMART info for disk0
  - `x smart -a /dev/disk0 | @gemini generate a report` - AI-generated disk health report
  - `x smart : disk health` - Search disk health information

### Storage Analysis (df)
Enhanced disk space monitoring with multiple output formats.

- **Usage**: `x df [flags]`
- **Key features**:
  - Automatic TUI/TSV output based on terminal type
  - Multiple output formats (CSV, TSV, TUI)
  - Cross-platform compatibility
  - Interactive table interface
- **Examples**:
  - `x df` - Auto-detect output format (TUI/TSV)
  - `x df --csv` - CSV format output
  - `x df --tsv` - TSV format output
  - `x df --app` - Interactive TUI application

## System Administration Use Cases

### System Monitoring
- Use `x ps` for real-time process monitoring
- Use `x df` for disk space analysis
- Use `x mac info` for system health overview
- Use `x smart` for disk health monitoring

### Network Management
- Use `x ip ls` for network interface analysis
- Use `x ip geolite` for IP geolocation
- Use `x ip map` for network discovery
- Use `x mac net` for macOS network management

### System Maintenance
- Use `x mac disk` for disk management
- Use `x mac trash` for system cleanup
- Use `x mac battery` for power management
- Use `x mac vol` for audio control

### Security and Access Control
- Use `x mac lock` for workstation security
- Use `x mac tidsudo` for TouchID authentication
- Use `x mac fw` for firewall management
- Use `x mac sshd` for SSH server configuration

## Installation and Setup

### Prerequisites
- x-cmd CLI installed
- Appropriate system permissions
- Internet connection (for geolocation and search features)

### Platform-Specific Requirements

#### macOS
- Most `x mac` commands work natively
- Some features require administrator privileges
- TouchID integration available for supported systems

#### Linux
- `x smart` automatically handles sudo privileges
- Network tools work across distributions
- Process management compatible with standard Linux ps

#### Windows
- Limited macOS-specific functionality
- Network and process tools available
- Storage analysis works across platforms

### Configuration

#### Process Management
```bash
x ps --help  # View all available options
```

#### macOS System
```bash
x mac alias enable m  # Set alias for quick access
```

#### Network Tools
```bash
x ip --help  # View network analysis options
```

## Integration with Other Tools

### Data Processing
- Pipe output to `x jq` for JSON processing
- Use with `@zh` for Chinese translation
- Export to CSV/TSV for spreadsheet analysis

### AI Integration
- Use `@gemini` for AI-powered analysis
- Generate reports from system data
- Get recommendations for system optimization

### Automation
- Combine with shell scripts for automated monitoring
- Schedule regular system health checks
- Create custom system administration workflows

## Troubleshooting

### Common Issues
- **Permission errors**: Ensure appropriate privileges for system commands
- **Network connectivity**: Check internet connection for geolocation services
- **Device detection**: Verify disk devices are accessible for SMART monitoring
- **Platform compatibility**: Some tools are macOS-specific

### Performance Optimization
- Use specific queries rather than broad searches
- Cache results when appropriate for monitoring
- Use interactive interfaces for complex analysis

### System-Specific Considerations
- **macOS**: Some commands require SIP (System Integrity Protection) considerations
- **Linux**: SMART monitoring requires appropriate device permissions
- **Cross-platform**: Output formats standardized across platforms

## Support and Resources

- **x-cmd System Documentation**: https://x-cmd.com/mod/system
- **Process Management**: https://x-cmd.com/mod/ps
- **macOS Utilities**: https://x-cmd.com/mod/mac
- **Network Tools**: https://x-cmd.com/mod/ip
- **Disk Health**: https://x-cmd.com/mod/smart
- **Storage Analysis**: https://x-cmd.com/mod/df

For additional help:
- Use `x [tool] --help` for specific tool documentation
- Visit individual module pages for detailed usage
- Check platform-specific requirements for each tool