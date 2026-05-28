---
name: os-health
description: VPS OS health, network speed test, disk, RAM, CPU, uptime, process snapshot
user-invocable: true
---

# OS Health & Speedtest — arifOS_bot

Triggers: "speedtest", "network speed", "how fast is my VPS", "os health", "system check",
          "cpu usage", "memory usage", "disk space", "uptime", "processes", "top processes",
          "is VPS slow", "latency", "ping", "bandwidth", "vps performance"

---

## Full Health Snapshot (run all at once)

```bash
echo "=== $(date) ===" && \
echo "--- UPTIME ---" && uptime && \
echo "--- CPU ---" && grep -c ^processor /proc/cpuinfo && cat /proc/loadavg && \
echo "--- RAM ---" && free -h && \
echo "--- DISK ---" && df -h / && \
echo "--- CONTAINERS ---" && docker ps --format "table {{.Names}}\t{{.Status}}" 2>/dev/null && \
echo "--- arifOS ---" && curl -sf http://arifosmcp_server:8080/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"status={d['status']} tools={d.get('tools_loaded','?')}\")" 2>/dev/null
```

---

## Network Speed Test

### Download speed (Cloudflare — no install needed)
```bash
# 10MB test file from Cloudflare
SPEED=$(curl -s -o /dev/null -w "%{speed_download}" \
  "https://speed.cloudflare.com/__down?bytes=10000000" --max-time 15)
echo "Download: $(echo "scale=1; ${SPEED}/1048576" | bc) MB/s"
```

### Latency to key endpoints
```bash
for HOST in 1.1.1.1 8.8.8.8 api.anthropic.com api.moonshot.cn; do
  RTT=$(curl -s -o /dev/null -w "%{time_connect}s" "https://${HOST}" --max-time 5 2>/dev/null || echo "timeout")
  echo "${HOST}: ${RTT}"
done
```

### Upload speed (to your own VPS — internal)
```bash
# From container to arifOS MCP endpoint
dd if=/dev/urandom bs=1M count=5 2>/dev/null | \
  curl -s -X POST http://arifosmcp_server:8080/health \
  -H "Content-Type: application/octet-stream" \
  --data-binary @- -o /dev/null -w "upload: %{speed_upload} B/s\n"
```

### Quick ping test (DNS resolution speed)
```bash
for HOST in arifosmcp_server headless_browser qdrant_memory ollama_engine arifos-postgres; do
  TIME=$(curl -sf -o /dev/null -w "%{time_namelookup}+%{time_connect}" http://${HOST} 2>/dev/null || echo "unreachable")
  echo "${HOST}: ${TIME}s"
done
```

---

## CPU & Process Analysis

```bash
# Top CPU consumers
ps aux --sort=-%cpu | head -10

# Top memory consumers
ps aux --sort=-%mem | head -10

# CPU info
nproc && cat /proc/loadavg

# Check if load is high
LOAD=$(cat /proc/loadavg | cut -d' ' -f1)
CORES=$(nproc)
echo "Load: ${LOAD} / ${CORES} cores"
# If load > cores: system under pressure
```

---

## Disk Analysis

```bash
# Overall usage
df -h

# Find disk hogs (top 10 largest dirs)
du -h / --max-depth=3 2>/dev/null | sort -rh | head -10

# Docker-specific disk usage
docker system df

# Ollama model sizes
docker exec ollama_engine du -sh /root/.ollama/models/ 2>/dev/null

# Log sizes
du -sh /opt/arifos/data/openclaw/logs/ /var/log/ 2>/dev/null
```

## Disk Alert Thresholds

```bash
USED=$(df / | awk 'NR==2{print $5}' | tr -d '%')
if [ "$USED" -gt 85 ]; then
  echo "DISK_CRITICAL: ${USED}% — immediate cleanup required"
  echo "Run: docker builder prune -f && docker image prune -f"
elif [ "$USED" -gt 75 ]; then
  echo "DISK_WARNING: ${USED}% — monitor closely"
else
  echo "DISK_OK: ${USED}%"
fi
```

---

## RAM Analysis

```bash
# Full memory breakdown
free -h

# Per-container memory (sorted)
docker stats --no-stream --format "{{.Name}}: {{.MemUsage}} ({{.MemPerc}})" | sort -t'/' -k1 -rh

# Check if swap is being used (bad sign on this VPS)
free -h | grep Swap
# >100MiB swap used → RAM pressure, check which container to limit
```

---

## Network Interface Stats

```bash
# Bytes in/out since boot
cat /proc/net/dev | awk 'NR>2 {printf "%s: RX=%.1fMB TX=%.1fMB\n", $1, $2/1048576, $10/1048576}' | grep -v "lo:"

# Active connections count
ss -s 2>/dev/null || netstat -s 2>/dev/null | grep "connections" | head -5
```

---

## OS Info

```bash
uname -a
cat /etc/os-release | grep -E "^(NAME|VERSION)="
# CPU model
grep "model name" /proc/cpuinfo | head -1 | cut -d: -f2 | xargs
# VPS host
curl -sf http://169.254.169.254/latest/meta-data/instance-type 2>/dev/null || echo "Not AWS (KVM VPS)"
```

---

## Auto-Heal Actions (within autonomous authority)

```bash
# Disk >80% — safe cleanup
docker builder prune -f
docker image prune -f --filter "dangling=true"
journalctl --vacuum-size=200M 2>/dev/null

# Container OOM-killed — restart it
docker compose -f /mnt/arifos/docker-compose.yml up -d <container_name>

# High load — identify and report (don't kill without F13)
ps aux --sort=-%cpu | head -5
# → Report to Arif before killing unknown processes
```

---

## Log to Audit

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"event\":\"os_health_check\",\"disk_pct\":\"$(df / | awk 'NR==2{print $5}')\",\"load\":\"$(cat /proc/loadavg | cut -d' ' -f1)\",\"agent\":\"arifOS_bot\"}" \
  >> ~/.openclaw/workspace/logs/audit.jsonl
```

*arifOS_bot — OS health + network diagnostics*
