---
name: container-manage
description: Container management skill for development and operations containers. Use this when managing system resources, processes, services, environment configuration, Docker containers, logs, or performing system diagnostics and monitoring tasks.
---

# Container Management Skill

This skill helps manage development and operations containers with common administrative tasks.

## Capabilities

### 1. System Information & Monitoring
- Check system resource usage (CPU, memory, disk)
- View system information and kernel version
- Monitor running processes
- Check network configuration and connectivity

### 2. Process Management
- List and manage running processes
- Start/stop/restart services
- Monitor process resource usage
- Check service status

### 3. Docker Container Management
- List running containers
- Start/stop/restart containers
- View container logs
- Inspect container configuration
- Check container resource usage
- Execute commands in containers

### 4. Environment Configuration
- Manage environment variables
- View and edit configuration files
- Set up shell configurations
- Manage SSH keys and credentials

### 5. Log Management
- View system logs
- Analyze application logs
- Search and filter log files
- Archive and rotate logs

### 6. Package Management
- Install/update/remove packages
- Check installed packages
- Update package repositories
- Manage dependencies

### 7. Network Operations
- Check network interfaces
- Test connectivity (ping, curl)
- View open ports and connections
- Configure firewall rules

### 8. Disk & Storage
- Check disk usage and free space
- Manage files and directories
- Clean up temporary files
- Backup and restore data

### 9. Security & Permissions
- Manage file permissions
- Check user and group information
- Audit security settings
- Manage access controls

### 10. Univers Developer Session Management
- Restart all univers-* development sessions or specific ones
- Start/stop individual development sessions (server, ui, web, claude, etc.)
- Monitor status of all development sessions with categorized display
- Attach to specific development sessions
- Support for session groups: all, core, dev-views, developer
- Manage backend API server, UI development, web server, Claude terminal, and development views

## Common Tasks

### System Health Check
```bash
# CPU and memory usage
top -b -n 1 | head -20

# Disk usage
df -h

# Running processes
ps aux | head -20
```

### Docker Operations
```bash
# List containers
docker ps -a

# View container logs
docker logs <container-name>

# Execute command in container
docker exec -it <container-name> /bin/bash
```

### Log Analysis
```bash
# View recent system logs
journalctl -n 100

# Search application logs
grep -i "error" /var/log/app.log
```

### Univers Developer Session Management
```bash
# Restart all univers-* development sessions
cm dev restart

# Restart core development sessions only
cm dev restart core

# Restart specific session
cm dev restart univers-server
cm dev restart univers-ui
cm dev restart univers-web

# Show status of all sessions
cm dev status

# Attach to specific session
cm dev attach univers-server
cm dev attach univers-ui
cm dev attach univers-developer

# List all available sessions
cm dev list

# Start/stop sessions
cm dev start
cm dev stop
```

## Best Practices

1. Always check current status before making changes
2. Create backups before modifying critical configurations
3. Use appropriate permissions and avoid running as root when possible
4. Monitor resource usage regularly
5. Keep logs organized and rotated
6. Document configuration changes
7. Test changes in non-production environments first

## Safety Guidelines

- Never delete system files without confirmation
- Always verify commands before execution
- Keep credentials secure and never commit to git
- Use environment variables for sensitive data
- Regularly update and patch the system
- Monitor for unusual activity or resource usage

## Version History

- v3.0 (2025-12-06): Complete univers session management - all univers-* sessions supported with individual, group, and categorized control
- v2.0 (2025-12-06): Added univers-developer session management capabilities  
- v1.0 (2025-10-24): Initial container management skill
