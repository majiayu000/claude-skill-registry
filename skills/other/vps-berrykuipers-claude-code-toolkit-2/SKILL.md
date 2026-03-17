---
name: vps
description: |
  Direct VPS operations via SSH MCP. Manage Docker containers, check logs,
  run commands, and troubleshoot services on registered VPS servers.
examples:
  - "/vps status"
  - "/vps logs api"
  - "/vps exec 'docker ps'"
  - "/vps restart api"
  - "/vps health"
---

# VPS Operations Skill

Direct SSH access to VPS servers for container management and troubleshooting.

## Usage

```bash
/vps                           # Show VPS status for current project
/vps status                    # Container status + resource usage
/vps logs <service>            # View service logs (tail -100)
/vps logs <service> --follow   # Stream logs
/vps exec '<command>'          # Execute arbitrary command on VPS
/vps restart <service>         # Restart specific container
/vps health                    # Run health checks on all services
/vps resources                 # Show CPU, memory, disk usage
/vps backup                    # Backup database to NAS
```

## Project Detection

Reads project from:
1. Current git remote URL
2. `deployments.registry.json` lookup

## Common Operations

### Container Management

```bash
# List all containers
ssh ${USER}@${HOST} "docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"

# Restart service
ssh ${USER}@${HOST} "docker compose -f ${COMPOSE_PATH} restart ${SERVICE}"

# View logs
ssh ${USER}@${HOST} "docker logs ${CONTAINER} --tail 100"

# Execute in container
ssh ${USER}@${HOST} "docker exec ${CONTAINER} npm run db:migrate"
```

### Health Monitoring

```bash
# System resources
ssh ${USER}@${HOST} "free -h && df -h && uptime"

# Docker resource usage
ssh ${USER}@${HOST} "docker stats --no-stream"

# Nginx status
ssh ${USER}@${HOST} "sudo systemctl status nginx"

# Active connections
ssh ${USER}@${HOST} "netstat -an | grep ESTABLISHED | wc -l"
```

### Database Operations

```bash
# Backup database
ssh ${USER}@${HOST} "docker exec ${DB_CONTAINER} pg_dump -U postgres ${DB} > /backup/${DB}_$(date +%Y%m%d).sql"

# Copy backup to NAS
scp ${USER}@${HOST}:/backup/${DB}_*.sql berry@10.0.0.23:/volume1/backups/

# Check database connections
ssh ${USER}@${HOST} "docker exec ${DB_CONTAINER} psql -U postgres -c 'SELECT count(*) FROM pg_stat_activity;'"
```

### Troubleshooting

```bash
# Check for OOM kills
ssh ${USER}@${HOST} "dmesg | grep -i 'out of memory' | tail -10"

# Check docker events
ssh ${USER}@${HOST} "docker events --since '1h' --until 'now'"

# Check failed services
ssh ${USER}@${HOST} "docker ps -a --filter 'status=exited' --format '{{.Names}}: {{.Status}}'"
```

## Safety

- NEVER run `pkill node` - will kill Claude Code
- NEVER run destructive commands without confirmation
- ALWAYS check what you're about to do with `--dry-run` first
- Use `docker compose restart` instead of killing containers

## MCP Tool Reference

```
mcp__project-vps__exec    # Execute commands on project VPS
mcp__home-nas__exec       # Execute commands on home NAS
```
