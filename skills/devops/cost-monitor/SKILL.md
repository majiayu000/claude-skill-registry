---
name: cost-monitor
description: Monitor and optimize operational costs to stay under the $50/month budget. Use when reviewing infrastructure costs, optimizing API usage, or tracking service expenses. Trigger when discussing budget, costs, or optimization.
metadata: {"clawdbot":{"emoji":"💰","project":"investment-analysis-platform"}}
---

# Cost Monitor Skill

Track and optimize all operational costs to maintain the strict $50/month budget.

## Budget Breakdown Target

```
Total Monthly Budget: $50

Infrastructure Allocation:
├── Database Hosting     $0-15  (self-hosted PostgreSQL/TimescaleDB)
├── Redis Cache          $0-5   (self-hosted or free tier)
├── Compute              $0-20  (self-hosted or spot instances)
├── Monitoring           $0     (self-hosted Prometheus/Grafana)
├── CI/CD                $0     (GitHub Actions free tier)
├── Data APIs            $0     (free tier usage only)
├── Domain/SSL           $0-10  (Let's Encrypt for SSL)
└── Buffer               $10-15 (unexpected costs)
```

## API Cost Tracking

### Free Tier Limits (CRITICAL)

| API Provider | Daily Limit | Per Minute | Monthly |
|--------------|-------------|------------|---------|
| Alpha Vantage | 25 calls | 5 calls | ~750 |
| Finnhub | Unlimited | 60 calls | Free |
| Polygon | Unlimited | 5 calls | Free tier |
| NewsAPI | 100 calls | - | 3,000 |

### Monitoring API Usage

```python
# Check current API usage
from backend.services.api_tracker import APIUsageTracker

tracker = APIUsageTracker()

# Get daily usage report
usage = tracker.get_daily_usage()
print(f"""
API Usage Report:
- Alpha Vantage: {usage['alpha_vantage']}/25 calls
- Finnhub: {usage['finnhub']} calls (60/min limit)
- Polygon: {usage['polygon']} calls (5/min limit)
- NewsAPI: {usage['news_api']}/100 calls
""")

# Check if approaching limits
alerts = tracker.check_rate_limits()
for alert in alerts:
    print(f"WARNING: {alert}")
```

## Cost Tracking Commands

```bash
# Check current month's infrastructure costs
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Database storage usage
docker exec postgres psql -U postgres -c "
  SELECT pg_size_pretty(pg_database_size('investment_platform')) as db_size;
"

# Redis memory usage
docker exec redis redis-cli INFO memory | grep used_memory_human

# Check disk usage
df -h /var/lib/docker

# Estimate monthly costs
python -c "
from backend.services.cost_tracker import CostTracker

tracker = CostTracker()
estimate = tracker.estimate_monthly_cost()
print(f'Estimated monthly cost: \${estimate:.2f}')
print(f'Budget remaining: \${50 - estimate:.2f}')

if estimate > 45:
    print('WARNING: Approaching budget limit!')
"
```

## Cost Optimization Strategies

### 1. Database Optimization
```sql
-- Check table sizes and optimize
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- Enable TimescaleDB compression for old data
SELECT add_compression_policy('stock_prices', INTERVAL '7 days');

-- Set retention policy
SELECT add_retention_policy('stock_prices', INTERVAL '2 years');
```

### 2. Cache Optimization
```python
# Increase cache hit rate to reduce API calls
from backend.services.cache import CacheAnalyzer

analyzer = CacheAnalyzer()
stats = analyzer.get_hit_rate()
print(f"Cache hit rate: {stats['hit_rate']*100:.1f}%")

# Identify cache misses
misses = analyzer.get_frequent_misses()
print("Consider caching these keys:", misses[:10])
```

### 3. API Call Batching
```python
# Batch API calls to maximize free tier value
# Instead of 6000 individual calls, batch by sector/priority

from backend.services.api_optimizer import APIOptimizer

optimizer = APIOptimizer()

# Prioritize high-value stocks for detailed analysis
priority_stocks = optimizer.get_priority_stocks(limit=25)  # Alpha Vantage limit

# Use Finnhub for bulk quotes (60/min = 86,400/day)
all_stocks = optimizer.get_all_stocks()
```

### 4. Compute Optimization
```yaml
# Docker resource limits to prevent overages
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

## Daily Cost Report

```bash
# Generate daily cost report
python -c "
from backend.services.cost_tracker import CostTracker
from datetime import date

tracker = CostTracker()
report = tracker.generate_daily_report(date.today())

print('=== Daily Cost Report ===')
print(f'Date: {report[\"date\"]}')
print(f'API Calls: {report[\"total_api_calls\"]}')
print(f'DB Storage: {report[\"db_storage_mb\"]} MB')
print(f'Cache Memory: {report[\"cache_memory_mb\"]} MB')
print(f'Estimated Cost: \${report[\"estimated_cost\"]:.2f}')
print(f'MTD Cost: \${report[\"mtd_cost\"]:.2f}')
print(f'Budget Status: {\"OK\" if report[\"mtd_cost\"] < 40 else \"WARNING\"}')
"
```

## Alerts Configuration

```yaml
# Prometheus alert rules for cost monitoring
groups:
  - name: cost-alerts
    rules:
      - alert: HighAPIUsage
        expr: api_calls_daily > 20
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "High API usage approaching daily limit"

      - alert: HighDiskUsage
        expr: (node_filesystem_used_bytes / node_filesystem_size_bytes) > 0.85
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Disk usage above 85%"

      - alert: BudgetApproaching
        expr: monthly_cost_estimate > 40
        labels:
          severity: critical
        annotations:
          summary: "Monthly cost approaching $50 limit"
```

## Quick Actions

| Situation | Action |
|-----------|--------|
| API limit near | Increase cache TTL, reduce analysis frequency |
| Disk full | Run compression, clear old logs |
| Memory high | Reduce Redis maxmemory, restart services |
| Cost > $40 | Review and reduce resource limits |
