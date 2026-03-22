---
name: frappe-ops-performance
description: >
  Use when tuning MariaDB, configuring Redis memory, sizing Gunicorn workers, setting up CDN, or profiling slow queries.
  Prevents performance bottlenecks from default configurations, memory exhaustion, and unoptimized database queries.
  Covers MariaDB tuning, Redis configuration, Gunicorn worker sizing, CDN setup, slow query log analysis, Python profiling, request profiling.
  Keywords: performance, MariaDB, Redis, Gunicorn, CDN, slow query, profiling, tuning, optimization, workers.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Performance Tuning

Frappe/ERPNext performance depends on four layers: database (MariaDB), cache (Redis), application server (Gunicorn), and background workers (RQ). ALWAYS tune all four layers together — optimizing one while ignoring others creates new bottlenecks.

## Quick Reference

```bash
# Check system health
bench doctor

# Show pending background jobs
bench --site mysite.com show-pending-jobs

# Clear all caches
bench --site mysite.com clear-cache
bench --site mysite.com clear-website-cache

# Purge stuck background jobs
bench purge-jobs

# Enable MariaDB slow query log
# In /etc/mysql/mariadb.conf.d/50-server.cnf:
# slow_query_log = 1
# slow_query_log_file = /var/log/mysql/slow.log
# long_query_time = 1

# Check Gunicorn worker count
# In Procfile or supervisor config: -w [workers]
# Formula: workers = (2 * CPU_CORES) + 1
```

---

## Performance Decision Tree

```
What is slow?
|
+-- Page loads are slow?
|   +-- Check Gunicorn workers (are they saturated?)
|   +-- Check MariaDB slow query log
|   +-- Check Redis memory (is cache evicting?)
|   +-- Enable CDN for static assets
|
+-- Background jobs are delayed?
|   +-- bench doctor (check worker count and pending jobs)
|   +-- Increase RQ worker count
|   +-- Check for long-running jobs blocking queues
|
+-- Database queries are slow?
|   +-- Enable slow query log
|   +-- Run EXPLAIN on slow queries
|   +-- Add indexes on frequently filtered columns
|   +-- Use get_cached_value instead of get_value
|
+-- Server runs out of memory?
|   +-- Reduce Gunicorn workers
|   +-- Set Redis maxmemory
|   +-- Check MariaDB innodb_buffer_pool_size
|   +-- Look for memory leaks in custom code
|
+-- High CPU usage?
|   +-- Profile Python code (cProfile)
|   +-- Check for N+1 query patterns
|   +-- Review custom scheduled jobs
```

---

## MariaDB Tuning

### Critical Settings

```ini
# /etc/mysql/mariadb.conf.d/50-server.cnf
[mysqld]
# InnoDB buffer pool — MOST important setting
# Set to 50-70% of available RAM on dedicated DB server
# Set to 25-40% of RAM on shared server
innodb_buffer_pool_size = 2G

# Buffer pool instances (1 per GB of buffer pool)
innodb_buffer_pool_instances = 2

# Log file size (larger = better write performance, slower recovery)
innodb_log_file_size = 256M

# Flush method — use O_DIRECT to avoid double buffering
innodb_flush_method = O_DIRECT

# Character set (ALWAYS use utf8mb4 for Frappe)
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

# Key buffer for MyISAM (Frappe uses InnoDB, keep small)
key_buffer_size = 32M

# Query cache (DISABLE for MariaDB 10.4+ / MySQL 8.0+)
query_cache_type = 0
query_cache_size = 0

# Connection limits
max_connections = 200
wait_timeout = 600
interactive_timeout = 600

# Temp tables
tmp_table_size = 64M
max_heap_table_size = 64M

# Slow query log
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 1
```

### Slow Query Analysis

```bash
# Enable slow query log (runtime, no restart needed)
SET GLOBAL slow_query_log = 1;
SET GLOBAL long_query_time = 1;

# Analyze slow queries with mysqldumpslow
mysqldumpslow -t 10 -s c /var/log/mysql/slow.log
# -t 10: top 10 queries
# -s c: sort by count (use -s t for total time)

# Use EXPLAIN to analyze specific queries
EXPLAIN SELECT * FROM `tabSales Invoice` WHERE customer = 'ABC';
# Look for: type=ALL (full table scan), rows > 10000, Using filesort
```

### Index Optimization

```sql
-- Check for missing indexes on frequently filtered columns
SHOW INDEX FROM `tabSales Invoice`;

-- Add index for common filter patterns
ALTER TABLE `tabSales Invoice` ADD INDEX idx_customer_date (customer, posting_date);

-- Frappe way: add index via DocType definition
-- In doctype JSON: set "in_list_view" or "search_index" on fields
-- OR use hooks.py:
-- after_migrate = ["myapp.patches.add_custom_indexes"]
```

---

## Redis Configuration

### Memory Management

```conf
# /etc/redis/redis.conf (or bench config/redis_cache.conf)

# Set maximum memory — NEVER let Redis use all available RAM
maxmemory 512mb

# Eviction policy — allkeys-lru is best for cache use
maxmemory-policy allkeys-lru

# Disable persistence for cache Redis (performance boost)
save ""
appendonly no
```

### Frappe Redis Architecture

Frappe uses THREE Redis instances:

| Instance | Default Port | Purpose | Memory Guide |
|---|---|---|---|
| redis-cache | 13000 | Document cache, session data | 256MB-1GB |
| redis-queue | 11000 | RQ job queues | 128MB-512MB |
| redis-socketio | 12000 | Real-time events | 64MB-256MB |

ALWAYS set `maxmemory` on redis-cache. Without it, Redis grows unbounded and can trigger OOM killer.

### Frappe Caching API

```python
import frappe

# Basic Redis cache
frappe.cache.set_value("my_key", {"data": "value"})
result = frappe.cache.get_value("my_key")

# get_cached_value — cached database lookup (ALWAYS prefer over get_value for reads)
value = frappe.db.get_cached_value("Customer", "CUST-001", "customer_name")
# Equivalent to get_value but caches in Redis — dramatically faster for repeated reads

# Hashed cache (group related values)
frappe.cache.hset("settings", "key1", "value1")
frappe.cache.hget("settings", "key1")

# Clear specific cache
frappe.cache.delete_value("my_key")
frappe.cache.delete_keys("prefix*")

# Clear all cache (use sparingly)
# bench --site mysite.com clear-cache
```

---

## Gunicorn Workers

### Worker Count Formula

```
workers = (2 * CPU_CORES) + 1

Examples:
  2 CPU cores  →  5 workers
  4 CPU cores  →  9 workers
  8 CPU cores  → 17 workers
```

### Configuration

```bash
# Traditional: edit Procfile or supervisor config
# In supervisor.conf:
command=/home/frappe/frappe-bench/env/bin/gunicorn \
    -b 127.0.0.1:8000 \
    -w 9 \                    # Worker count
    --timeout 120 \           # Request timeout (seconds)
    --graceful-timeout 30 \   # Graceful shutdown timeout
    --max-requests 5000 \     # Restart worker after N requests (prevents memory leaks)
    --max-requests-jitter 500 \
    frappe.app:application

# Docker: set via environment variable or command override
```

### Memory Calculation

Each Gunicorn worker consumes 150-300MB RAM. ALWAYS verify total memory fits:

```
Required RAM = workers * 300MB + MariaDB buffer pool + Redis + OS overhead

Example (4 CPU, 8GB RAM server):
  9 workers * 300MB = 2.7GB (Gunicorn)
  + 2GB (MariaDB innodb_buffer_pool_size)
  + 1GB (Redis total)
  + 1.5GB (OS + other)
  = 7.2GB — fits in 8GB
```

NEVER set more workers than your RAM allows. Swapping kills performance.

---

## Background Workers (RQ)

### Worker Queues

| Queue | Purpose | Default Workers |
|---|---|---|
| short | Quick tasks (< 5 min) | 1 |
| default | Standard tasks | 1 |
| long | Heavy tasks (reports, bulk ops) | 1 |

### Tuning Worker Count

```bash
# Supervisor: duplicate worker sections with unique names
# For high-volume sites, increase short/default workers:

[program:frappe-bench-frappe-worker-short-1]
command=bench worker --queue short
...

[program:frappe-bench-frappe-worker-short-2]
command=bench worker --queue short
...

# Docker: scale via docker compose
docker compose up -d --scale queue-short=3 --scale queue-long=2
```

### Diagnosing Job Backlogs

```bash
# Check overall health
bench doctor
# Expected: Workers online: N, no pending jobs

# Check specific site queues
bench --site mysite.com show-pending-jobs

# Clear stuck jobs (use when jobs are permanently stuck)
bench purge-jobs
```

---

## CDN Setup for Static Assets

```python
# site_config.json
{
    "cdn_url": "https://cdn.example.com"
}
# All /assets/ URLs will be prefixed with the CDN URL

# ALTERNATIVELY: configure at Nginx level
# location /assets {
#     alias /home/frappe/frappe-bench/sites/assets;
#     expires 1y;
#     add_header Cache-Control "public, immutable";
# }
```

---

## Monitoring

### bench doctor

```bash
bench doctor
# Output:
# -----Checking scheduler------
# mysite.com: scheduler is running
# Workers online: 3
# -----None Jobs-----
```

### Key Log Locations

| Log | Path | Contains |
|---|---|---|
| Frappe web log | `logs/web.log` | HTTP requests, errors |
| Worker log | `logs/worker.log` | Background job output |
| Scheduler log | `logs/scheduler.log` | Scheduled job execution |
| Site-level log | `sites/{site}/logs/` | Per-site errors (v13+) |
| Slow query log | `/var/log/mysql/slow.log` | Slow database queries |

### Scheduled Job Log (DocType)

Check **Setup > Scheduled Job Log** in ERPNext UI for:
- Job execution times
- Failed jobs with error details
- Frequency analysis

### RQ Dashboard (Optional)

```bash
# Install RQ dashboard for web-based job monitoring
pip install rq-dashboard
rq-dashboard --redis-url redis://localhost:11000
# Access at http://localhost:9181
```

---

## Common Bottleneck Diagnosis

| Symptom | Likely Cause | Solution |
|---|---|---|
| Slow page loads, high DB time | Missing indexes, N+1 queries | Add indexes, use `get_list` with filters |
| Worker queue growing | Too few workers, long jobs | Increase workers, optimize job code |
| High memory, OOM kills | Too many Gunicorn workers, Redis unbounded | Reduce workers, set `maxmemory` |
| Intermittent timeouts | Gunicorn timeout too low | Increase `--timeout` (default 120s) |
| Slow after cache clear | Cold cache, no warming | Pre-warm critical caches after deploy |
| Static assets slow | No CDN, no browser caching | Add CDN, set `expires` headers |

---

## Scaling Patterns

```
Vertical Scaling (single server):
  1. Add RAM → increase innodb_buffer_pool_size + Redis maxmemory
  2. Add CPU → increase Gunicorn workers + RQ workers
  3. Use SSD → dramatic improvement for database I/O

Horizontal Scaling (multiple servers):
  1. Separate DB server (MariaDB on dedicated host)
  2. Separate Redis server(s)
  3. Multiple app servers behind load balancer
  4. Read replicas for reporting queries
  5. Kubernetes with frappe_docker for auto-scaling
```

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---|---|---|---|
| Site-level logs | v13+ | Yes | Yes |
| `bench doctor` | Yes | Yes | Yes |
| Scheduled Job Log | Yes | Yes | Yes |
| `get_cached_value` | Yes | Yes | Yes |
| Background workers (RQ) | Yes | Yes | Yes |

---

## Reference Files

| File | Contents |
|---|---|
| [examples.md](references/examples.md) | Complete tuning configs and scripts |
| [anti-patterns.md](references/anti-patterns.md) | Common performance mistakes |
| [workflows.md](references/workflows.md) | Step-by-step tuning workflows |

## Related Skills

- `frappe-ops-deployment` — Production deployment setup
- `frappe-ops-backup` — Backup and disaster recovery
- `frappe-ops-bench` — Bench CLI reference
- `frappe-core-database` — Database API and query patterns
