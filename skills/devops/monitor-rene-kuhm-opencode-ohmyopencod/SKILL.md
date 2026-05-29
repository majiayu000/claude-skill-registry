---
description: "Monitorear métricas del proyecto en tiempo real. Uso de recursos, errores, performance, costos de Claude."
user-invocable: true
argument-hint: "[status|errors|performance|costs|all]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - WebFetch
---

# Monitor Skill

Monitorea el estado y métricas de tu proyecto y sesiones de Claude Code en tiempo real.

## Comandos

### STATUS - Estado General

```bash
/monitor status
/monitor  # Default
```

**Verifica:**
- Dev server corriendo
- Database conectada
- Servicios externos (Redis, etc.)
- Últimos errores en logs

**Output:**
```
📊 PROJECT STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Service          Status    Latency
─────────────────────────────────
Dev Server       🟢 UP     12ms
Database         🟢 UP     5ms
Redis            🟢 UP     2ms
External API     🟡 SLOW   850ms

Recent Errors: 2 (last 1h)
Memory Usage: 45%
CPU Usage: 12%
```

### ERRORS - Errores Recientes

```bash
/monitor errors
/monitor errors --last 24h
```

**Busca en:**
```bash
# Logs de aplicación
tail -100 logs/error.log

# Logs de Next.js
grep -i "error\|exception\|failed" .next/server/logs/*

# Sentry (si configurado)
# Usa MCP de Sentry
```

**Output:**
```
🔴 RECENT ERRORS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[2024-12-25 14:30:22] TypeError
  File: src/services/user.service.ts:42
  Message: Cannot read property 'id' of undefined
  Count: 15 occurrences

[2024-12-25 14:28:15] DatabaseError
  File: src/lib/prisma.ts:18
  Message: Connection timeout
  Count: 3 occurrences
```

### PERFORMANCE - Métricas de Rendimiento

```bash
/monitor performance
```

**Verifica:**
```bash
# Bundle size
ls -lh .next/static/chunks/*.js | head -10

# Build time
cat .next/build-manifest.json | jq '.buildTime'

# Lighthouse (si disponible)
npx lighthouse http://localhost:3000 --output=json --quiet
```

**Output:**
```
⚡ PERFORMANCE METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Bundle Size
  Total: 456 KB (gzipped)
  Largest: _app.js (125 KB)

Build Time: 12.5s

Core Web Vitals (estimated)
  LCP: ~1.8s  ✅
  FID: ~45ms  ✅
  CLS: ~0.05  ✅

Database
  Avg Query Time: 15ms
  Slow Queries: 2
```

### COSTS - Costos de Claude Code

```bash
/monitor costs
/monitor costs --today
/monitor costs --week
```

**Lee de:**
```bash
# Stats de Claude Code
cat ~/.claude/stats-cache.json | jq '.'

# Historial de sesiones
cat ~/.claude.json | jq '.projects[].lastCost'
```

**Output:**
```
💰 CLAUDE CODE COSTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Today
  Sessions: 5
  Tokens: 125,000
  Estimated Cost: $2.45

This Week
  Sessions: 23
  Tokens: 890,000
  Estimated Cost: $18.50

By Model
  Opus 4.5:   $12.00 (65%)
  Sonnet 4:   $5.50 (30%)
  Haiku 4.5:  $1.00 (5%)

Top Projects
  1. acuamarina-ceramica: $8.20
  2. mi-sitio: $5.30
  3. telecomunicasiones: $5.00
```

### ALL - Dashboard Completo

```bash
/monitor all
```

Muestra todos los dashboards combinados.

## Alertas Automáticas

El skill puede detectar y alertar sobre:

| Condición | Severidad | Acción |
|-----------|-----------|--------|
| Error rate > 5% | 🔴 Critical | Notificar inmediatamente |
| Response time > 2s | 🟠 Warning | Investigar |
| Disk usage > 80% | 🟠 Warning | Limpiar |
| Memory > 90% | 🔴 Critical | Reiniciar servicio |
| Cost > $10/day | 🟡 Info | Revisar uso |

## Integración con MCP

Si tienes configurados:
- **Sentry MCP**: Muestra errores de producción
- **Datadog MCP**: Métricas en tiempo real
- **Supabase MCP**: Estado de la base de datos

## Output Final

```
╔══════════════════════════════════════════════════════╗
║              📊 PROJECT MONITOR                       ║
╠══════════════════════════════════════════════════════╣
║  Status: 🟢 HEALTHY                                  ║
║  Uptime: 99.9%                                       ║
║  Last Deploy: 2h ago                                 ║
╠══════════════════════════════════════════════════════╣
║  🔴 Errors (1h): 2                                   ║
║  ⚠️  Warnings (1h): 5                                ║
║  📈 Requests (1h): 1,234                             ║
╠══════════════════════════════════════════════════════╣
║  💰 Today's Cost: $2.45                              ║
║  🎯 Performance: 92/100                              ║
╚══════════════════════════════════════════════════════╝
```
