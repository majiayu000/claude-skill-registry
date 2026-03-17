# 🗄️ Skill: Database Reliability

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `sre-database-reliability` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `database`, `postgresql`, `mysql`, `mongodb`, `replication`, `backup`, `failover`, `connection-pooling` |
| **Referencia** | [PostgreSQL High Availability](https://www.postgresql.org/docs/current/high-availability.html) |

## 🔑 Keywords para Invocación

- `database-reliability`
- `database-replication`
- `database-backup`
- `failover`
- `connection-pooling`
- `database-monitoring`
- `@skill:database-reliability`

### Ejemplos de Prompts

```
Implementa database replication y failover para PostgreSQL
```

```
Configura backup y recovery strategy para base de datos
```

```
Setup connection pooling y database monitoring
```

```
@skill:database-reliability - Alta disponibilidad de base de datos
```

## 📖 Descripción

Database reliability es fundamental para servicios confiables. Este skill cubre replication, failover, backups, connection pooling, monitoring, y disaster recovery para bases de datos en producción.

### ✅ Cuándo Usar Este Skill

- Bases de datos en producción
- Servicios con requisitos de alta disponibilidad
- Datos críticos
- SLAs estrictos
- Compliance requirements

### ❌ Cuándo NO Usar Este Skill

- Desarrollo local con datos de prueba
- Prototipos sin datos reales
- Sistemas de solo lectura sin disponibilidad crítica

## 🏗️ Arquitectura de Alta Disponibilidad

```
┌─────────────────────────────────────────┐
│           Application Layer             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │   App   │  │   App   │  │   App   │  │
│  └────┬────┘  └────┬────┘  └────┬────┘  │
└───────┼────────────┼────────────┼───────┘
        │            │            │
        └────────────┼────────────┘
                     │
              ┌──────▼──────┐
              │ Connection  │
              │    Pool     │
              └──────┬──────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────▼────┐  ┌────▼───┐  ┌─────▼────┐
   │Primary  │  │Replica │  │  Replica │
   │(Master) │  │(Read)  │  │  (Read)  │
   └────┬────┘  └────────┘  └──────────┘
        │
        │ Replication
        │
   ┌────▼────┐
   │ Standby │
   │ (DR)    │
   └─────────┘
```

## 💻 Implementación

> **📁 Scripts Ejecutables:** Este skill incluye scripts Python ejecutables en la carpeta [`scripts/`](scripts/):
> - [`postgresql_backup.py`](scripts/postgresql_backup.py) - Automatización de backups y restauración
> - [`requirements.txt`](scripts/requirements.txt) - Dependencias (ninguna, usa stdlib)
> 
> Ver [`scripts/README.md`](scripts/README.md) para documentación de uso.

### 1. PostgreSQL Replication Setup

#### 1.1 Primary Configuration

```conf
# postgresql.conf (Primary)
# Connection Settings
listen_addresses = '*'
max_connections = 200

# Replication Settings
wal_level = replica
max_wal_senders = 3
max_replication_slots = 3
hot_standby = on

# Performance
shared_buffers = 4GB
effective_cache_size = 12GB
maintenance_work_mem = 1GB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 20MB
min_wal_size = 1GB
max_wal_size = 4GB

# Logging
log_destination = 'stderr'
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_rotation_age = 1d
log_rotation_size = 100MB
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '
log_timezone = 'UTC'
```

```conf
# pg_hba.conf (Primary)
# Allow replication from replicas
host replication replicator 10.0.0.0/24 md5
```

#### 1.2 Replica Configuration

```bash
# Setup replication (on replica server)
# 1. Stop PostgreSQL
sudo systemctl stop postgresql

# 2. Backup primary
pg_basebackup -h primary-host -D /var/lib/postgresql/data -U replicator -P -W -R -S replication_slot_1

# 3. Configure recovery
# postgresql.conf (Replica)
hot_standby = on
max_standby_streaming_delay = 30s
wal_receiver_status_interval = 10s
hot_standby_feedback = on
```

```conf
# postgresql.auto.conf (Auto-generated)
primary_conninfo = 'host=primary-host port=5432 user=replicator password=xxx application_name=replica1'
primary_slot_name = 'replication_slot_1'
```

#### 1.3 Replication Slot Management

```sql
-- Create replication slot
SELECT pg_create_physical_replication_slot('replication_slot_1');

-- List replication slots
SELECT * FROM pg_replication_slots;

-- Monitor replication lag
SELECT 
    client_addr,
    state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn,
    sync_state,
    sync_priority
FROM pg_stat_replication;

-- Check lag in bytes
SELECT 
    pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag_bytes,
    client_addr,
    application_name
FROM pg_stat_replication;
```

### 2. Automatic Failover (Patroni)

```yaml
# patroni/patroni.yml
scope: postgres-cluster
namespace: /db/
name: postgres-node1

restapi:
  listen: 0.0.0.0:8008
  connect_address: 10.0.1.1:8008
  auth: 'username:password'

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 30
    maximum_lag_on_failover: 1048576
    postgresql:
      use_pg_rewind: true
      parameters:
        max_connections: 200
        max_worker_processes: 8
        wal_level: replica
        hot_standby: on
        wal_keep_segments: 8
        max_wal_senders: 3
        max_replication_slots: 3
        synchronous_commit: 'on'
        synchronous_standby_names: 'ANY 1 (postgres-node2,postgres-node3)'
  initdb:
    - encoding: UTF8
    - data-checksums
  pg_hba:
    - host replication replicator 0.0.0.0/0 md5
    - host all all 0.0.0.0/0 md5
  users:
    admin:
      password: admin
      options:
        - createrole
        - createdb

postgresql:
  listen: 0.0.0.0:5432
  connect_address: 10.0.1.1:5432
  data_dir: /var/lib/postgresql/data
  pgpass: /tmp/pgpass
  authentication:
    replication:
      username: replicator
      password: replicator
    superuser:
      username: postgres
      password: postgres
  parameters:
    unix_socket_directories: '/var/run/postgresql'
  recovery_conf:
    restore_command: 'cp /backup/%f %p'

tags:
  nofailover: false
  noloadbalance: false
  clonefrom: false
  nosync: false
```

### 3. Connection Pooling (PgBouncer)

```ini
# pgbouncer/pgbouncer.ini
[databases]
mydb = host=primary-host port=5432 dbname=mydb

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 5
reserve_pool_size = 5
reserve_pool_timeout = 3
max_db_connections = 100
max_user_connections = 50
server_round_robin = 1
ignore_startup_parameters = extra_float_digits

# Logging
log_connections = 1
log_disconnections = 1
log_pooler_errors = 1

# Admin console
admin_users = admin
stats_users = stats

# Health check
server_check_query = SELECT 1
server_check_delay = 30
server_lifetime = 3600
server_idle_timeout = 600

# Connection limits
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 5
```

### 4. Backup Strategy

```bash
#!/bin/bash
# scripts/backup.sh

BACKUP_DIR="/backup/postgresql"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Full backup
pg_basebackup \
  -h localhost \
  -D "$BACKUP_DIR/full_$DATE" \
  -U backup_user \
  -Ft \
  -z \
  -P

# WAL archiving (continuous)
# In postgresql.conf:
# archive_mode = on
# archive_command = 'test ! -f /backup/wal/%f && cp %p /backup/wal/%f'

# Cleanup old backups
find "$BACKUP_DIR" -type d -mtime +$RETENTION_DAYS -exec rm -rf {} \;

# Verify backup
pg_verifybackup -D "$BACKUP_DIR/full_$DATE"
```

**Script ejecutable:** [`scripts/postgresql_backup.py`](scripts/postgresql_backup.py)

Script CLI completo para automatizar backups, restauración y limpieza de PostgreSQL.

#### Cuándo ejecutar

- **Backups programados:** Como parte de cron jobs o tareas automatizadas
- **Restauración de emergencia:** Para restaurar bases de datos desde backups
- **Limpieza de backups:** Para mantener el espacio de almacenamiento bajo control
- **Verificación de backups:** Para validar la integridad de backups antes de restaurar

#### Uso como CLI

```bash
# Crear backup completo
python scripts/postgresql_backup.py backup \
  --host localhost \
  --user backup_user \
  --backup-dir /backup/postgresql

# Listar backups disponibles
python scripts/postgresql_backup.py list \
  --backup-dir /backup/postgresql

# Limpiar backups antiguos (dry-run primero)
python scripts/postgresql_backup.py cleanup \
  --backup-dir /backup/postgresql \
  --retention-days 30 \
  --dry-run

# Ejecutar limpieza real
python scripts/postgresql_backup.py cleanup \
  --backup-dir /backup/postgresql \
  --retention-days 30

# Restaurar desde backup
python scripts/postgresql_backup.py restore \
  --backup-path /backup/postgresql/full_20240115_120000 \
  --target-dir /var/lib/postgresql/data
```

#### Uso como módulo

```python
from scripts.postgresql_backup import PostgreSQLBackup

# Crear instancia
backup = PostgreSQLBackup(
    host="localhost",
    port=5432,
    user="backup_user",
    backup_dir="/backup/postgresql"
)

# Crear backup
backup_path = backup.full_backup(verify=True)

# Limpiar backups antiguos
backup.cleanup_old_backups(retention_days=30)

# Listar backups
backup.list_backups()
```

#### Características

- ✅ Backup físico completo con `pg_basebackup`
- ✅ Verificación automática de backups
- ✅ Restauración automatizada
- ✅ Limpieza de backups antiguos con política de retención
- ✅ Listado de backups disponibles
- ✅ Modo dry-run para limpieza
- ✅ Manejo de errores robusto

### 5. Database Monitoring

```yaml
# prometheus/database-metrics.yml
scrape_configs:
  - job_name: 'postgres-exporter'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'postgresql'
    static_configs:
      - targets: ['localhost:9187']
```

```sql
-- Custom metrics queries
-- Connection pool usage
SELECT 
    datname,
    numbackends as active_connections,
    max_connections,
    (numbackends::float / max_connections * 100) as connection_pct
FROM pg_stat_database;

-- Replication lag
SELECT 
    EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp())) AS lag_seconds;

-- Table bloat
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) AS bloat
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;

-- Slow queries
SELECT 
    pid,
    now() - pg_stat_activity.query_start AS duration,
    query,
    state
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes'
  AND state = 'active';

-- Index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;
```

### 6. Alert Rules

```yaml
# prometheus/alerts/database-alerts.yml
groups:
  - name: database_alerts
    interval: 30s
    rules:
      # High connection usage
      - alert: DatabaseHighConnections
        expr: |
          (pg_stat_database_numbackends / pg_stat_database_max_connections) > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High connection usage in {{ $labels.datname }}"
          description: "{{ $value | humanizePercentage }} of connections in use"

      # Replication lag
      - alert: DatabaseReplicationLag
        expr: |
          pg_replication_lag_seconds > 30
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High replication lag"
          description: "Replication lag is {{ $value }} seconds"

      # Database down
      - alert: DatabaseDown
        expr: |
          up{job="postgres-exporter"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Database exporter is down"

      # Slow queries
      - alert: DatabaseSlowQueries
        expr: |
          pg_stat_activity_max_tx_duration > 300
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Slow query detected"
          description: "Query running for {{ $value }} seconds"
```

## 🎯 Mejores Prácticas

### 1. Replication

✅ **DO:**
- Use synchronous replication for critical data
- Monitor replication lag
- Test failover regularly
- Use replication slots

❌ **DON'T:**
- Ignore replication lag
- Skip failover testing
- Use async replication for critical writes

### 2. Backups

✅ **DO:**
- Test restore procedures regularly
- Use point-in-time recovery
- Store backups off-site
- Encrypt backups

❌ **DON'T:**
- Assume backups work without testing
- Keep all backups in one location
- Skip backup verification

### 3. Connection Pooling

✅ **DO:**
- Use connection pooling
- Set appropriate pool sizes
- Monitor pool usage
- Handle connection errors gracefully

❌ **DON'T:**
- Exceed database connection limits
- Use too large pools
- Ignore pool exhaustion

## 🚨 Troubleshooting

### Replication Lag

1. Check network connectivity
2. Monitor WAL generation rate
3. Check replica performance
4. Consider increasing resources

### Connection Exhaustion

1. Reduce connection pool size
2. Close idle connections
3. Use connection pooling
4. Increase database max_connections

### Backup Failures

1. Check disk space
2. Verify permissions
3. Test backup commands manually
4. Review backup logs

## 📚 Recursos Adicionales

- [PostgreSQL High Availability](https://www.postgresql.org/docs/current/high-availability.html)
- [Patroni Documentation](https://patroni.readthedocs.io/)
- [PgBouncer Documentation](https://www.pgbouncer.org/)

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025  
**Total líneas:** 1,100+

