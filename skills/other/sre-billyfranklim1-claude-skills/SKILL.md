---
name: sre
description: Server, services, logs, errors, performance, load, memory, disk, processes, nginx, mysql, redis, php, supervisor
---
# Skill: SRE — Server Reliability Engineering

## Quando Usar
Quando o usuario perguntar sobre servidor, servicos, logs, erros, performance, load, memoria, disco, processos.

## Contexto
- Servidor: my-server (Ubuntu 22.04, 4 vCPUs, 16GB RAM)
- Servicos: Nginx 1.26, MySQL 8.0, Redis 7.2, PHP-FPM 8.0/8.3/8.4
- Process managers: Supervisor (Laravel workers), PM2 (Next.js apps)
- Observability: Grafana:3000, Loki:3100, Promtail:9080

## SLOs
- CPU Load: warning > 3.0, critical > 4.0
- Memory: warning > 80%, critical > 90%
- Disk: warning > 70%, critical > 85%
- HTTP 5xx: < 0.5%

## Comandos Essenciais
```bash
# Health check rapido
uptime && free -h && df -h /
systemctl is-active nginx mysql redis-server
supervisorctl status
pm2 jlist

# Logs
tail -100 /var/log/nginx/error.log
journalctl -u mysql --since "1 hour ago" --no-pager
tail -100 /home/deploy/.daemon-logs/daemon-XXXXX.log

# Processos pesados
ps aux --sort=-%cpu | head -10
ps aux --sort=-%mem | head -10
```

## Runbook: Restart Seguro
1. Identifique o servico com problema
2. Verifique logs ANTES de reiniciar
3. Restart progressivo: PHP-FPM → Nginx → Workers
4. Confirme recuperacao com curl/health check
