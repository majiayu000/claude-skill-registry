---
name: performance-profiling
description: Profile and diagnose performance bottlenecks in PHP/Laravel, Next.js, and MySQL — Xdebug, Blackfire, flame graphs, load testing with k6
---

# Skill: Performance Profiling — PHP, Next.js e MySQL

## Quando Usar
- Uma rota Laravel ou endpoint da `api.myapp.example.com` está lento (>500ms P95) mas logs não revelam a causa
- `frontend.example.com` ou `myapp.example.com` têm picos de CPU sem query lenta óbvia no MySQL
- Antes de um lançamento ou campanha de tráfego pago (Meta Ads MyApp), validar que o servidor aguenta a carga

## Contexto

**Apps críticas neste servidor:**
| App | PHP | Workers | Risco de gargalo |
|-----|-----|---------|-----------------|
| `api.myapp.example.com` | 8.3 | Horizon + nightwatch | Pipeline AI (GPT/Gemini calls) |
| `myapp.example.com` | 8.4 | – | Queries Eloquent complexas (entities/users) |
| `frontend.example.com` | Node 24 / Next.js | systemd | SSR com fetch de API externa |
| `work8.example.com` | 8.3 | Horizon | Fila de jobs |

**PHP-FPM pools:**
- PHP 8.3: `/etc/php/8.3/fpm/pool.d/`
- PHP 8.4: `/etc/php/8.4/fpm/pool.d/`

**Slow query log MySQL:** `/var/log/mysql/slow.log` (se habilitado)

---

## Passos / Comandos

### 1. Diagnóstico rápido — onde está o tempo?

```bash
# Latência real de endpoints (sem cache)
curl -o /dev/null -s -w "DNS:%{time_namelookup} Connect:%{time_connect} TTFB:%{time_starttransfer} Total:%{time_total}\n" \
  https://api.myapp.example.com/health

curl -o /dev/null -s -w "TTFB:%{time_starttransfer} Total:%{time_total}\n" \
  https://myapp.example.com/

# PHP-FPM: workers ativos vs max
php-fpm8.4 -tt 2>&1 | grep "pm.max_children"
cat /var/log/php8.4-fpm.log | grep "max_children\|reached" | tail -20

# CPU por processo
ps aux --sort=-%cpu | grep -E "php|node|nginx|mysql" | head -15

# Conexões MySQL abertas
mysql -e "SHOW STATUS LIKE 'Threads_connected';"
mysql -e "SHOW PROCESSLIST;" | grep -v Sleep | head -20
```

### 2. Load test simples com Apache Bench (já instalado no servidor)

```bash
# Teste de throughput — 100 requests, 10 concorrentes
ab -n 100 -c 10 -H "Accept-Encoding: gzip" \
  https://myapp.example.com/ 2>&1 | grep -E "Requests per|Time per|Failed"

# Teste de API autenticada (com header)
ab -n 50 -c 5 \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Accept: application/json" \
  https://api.myapp.example.com/api/news 2>&1 | tail -20

# Endpoint de cadastro (simular campanha Meta Ads)
ab -n 200 -c 20 https://myapp.example.com/cadastrar 2>&1 | \
  grep -E "Requests per|Time per|Failed|50%|95%|99%"
```

### 3. Instalar e usar k6 (load test avançado, se ab não bastar)

```bash
# Instalar k6
curl -s https://dl.k6.io/key.gpg | gpg --dearmor | sudo tee /usr/share/keyrings/k6-archive-keyring.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update && sudo apt-get install k6 -y

# Script básico /tmp/test-myapp.js
cat > /tmp/test-myapp.js << 'EOF'
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 },  // ramp up
    { duration: '1m',  target: 20 },  // carga sustentada
    { duration: '30s', target: 0 },   // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'],  // SLO: P95 < 1s
    http_req_failed:   ['rate<0.01'],   // < 1% erro
  },
};

export default function () {
  const res = http.get('https://myapp.example.com/');
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
EOF

k6 run /tmp/test-myapp.js
```

### 4. Profiling PHP com Xdebug (ambiente de debug temporário)

```bash
# Instalar Xdebug no PHP 8.4 (apenas se necessário, REMOVER depois)
sudo apt-get install php8.4-xdebug -y

# Config mínima para profiling (NÃO ativar em produção full-time)
cat > /etc/php/8.4/mods-available/xdebug.ini << 'EOF'
zend_extension=xdebug.so
xdebug.mode=profile
xdebug.start_with_request=trigger
xdebug.output_dir=/tmp/xdebug-profiles
xdebug.profiler_output_name=cachegrind.out.%p.%t
EOF

mkdir -p /tmp/xdebug-profiles
sudo phpenmod -v 8.4 xdebug
sudo systemctl restart php8.4-fpm

# Disparar profiling com trigger (parâmetro na URL)
curl "https://myapp.example.com/login?XDEBUG_PROFILE=1" -o /dev/null

# Ver arquivo gerado
ls -lh /tmp/xdebug-profiles/
# Analisar com qcachegrind local ou:
php -r "
\$data = file_get_contents('/tmp/xdebug-profiles/$(ls /tmp/xdebug-profiles | tail -1)');
echo 'Arquivo gerado, tamanho: ' . strlen(\$data) . ' bytes';
"

# REMOVER após análise
sudo phpdismod -v 8.4 xdebug && sudo systemctl restart php8.4-fpm
rm -f /tmp/xdebug-profiles/*
```

### 5. Detectar N+1 e queries lentas no Laravel (sem Telescope)

```bash
# Habilitar slow query log MySQL temporariamente
mysql -e "SET GLOBAL slow_query_log = 'ON';"
mysql -e "SET GLOBAL long_query_time = 0.5;"  # queries > 500ms
mysql -e "SET GLOBAL slow_query_log_file = '/var/log/mysql/slow.log';"

# Monitorar em tempo real
tail -f /var/log/mysql/slow.log

# Após capturar, analisar com pt-query-digest (se instalado)
# mysqldumpslow -s t -t 10 /var/log/mysql/slow.log

# Desligar após análise (não deixar em produção)
mysql -e "SET GLOBAL slow_query_log = 'OFF';"

# Ver queries ativas agora
mysql -e "SELECT id, user, host, db, time, state, LEFT(info,100) as query 
          FROM information_schema.processlist 
          WHERE time > 1 AND command != 'Sleep'
          ORDER BY time DESC;"
```

### 6. Profiling Next.js — identificar SSR lento

```bash
# Verificar tempo de resposta por rota no frontend.example.com
for path in "/" "/pt" "/pt/news" "/pt/blog"; do
  printf "%-25s" "$path"
  curl -o /dev/null -s -w "%{time_starttransfer}s\n" "https://frontend.example.com$path"
done

# Logs do serviço frontend (systemd)
journalctl -u frontend --since "10 minutes ago" --no-pager | grep -i "slow\|timeout\|error\|warn"

# Memória do processo Next.js
ps -o pid,rss,vsz,comm -p $(pgrep -f "next-server.*3001") 2>/dev/null | \
  awk 'NR>1{printf "PID:%s RSS:%.1fMB VSZ:%.1fMB\n", $1, $2/1024, $3/1024}'

# Se o processo estiver acima de 1.5GB → restart preventivo
sudo -u deploy systemctl --user restart frontend || systemctl restart frontend
```

### 7. Verificar gargalo de Redis (cache miss rate)

```bash
# Stats em tempo real
redis-cli INFO stats | grep -E "keyspace_hits|keyspace_misses|instantaneous_ops"

# Cache hit rate
redis-cli INFO stats | awk -F: '
  /keyspace_hits/   { hits=$2+0 }
  /keyspace_misses/ { misses=$2+0 }
  END { 
    total=hits+misses
    if(total>0) printf "Hit rate: %.1f%% (%d hits, %d misses)\n", hits/total*100, hits, misses
  }'

# Latência média do Redis
redis-cli --latency -i 1 &  # Ctrl+C para parar

# Keys mais acessadas (sample)
redis-cli --hotkeys 2>/dev/null | head -20 || \
  redis-cli OBJECT FREQ <key>  # requer maxmemory-policy allkeys-lfu
```

### 8. Monitorar performance durante load test (live)

```bash
# Em um terminal — watch de recursos durante teste
watch -n 1 'echo "=LOAD=" && uptime | awk "{print \$10,\$11,\$12}" && \
  echo "=MEM=" && free -h | grep Mem | awk "{print \"Used:\"\$3\"/\"\$2}" && \
  echo "=MYSQL=" && mysql -e "SHOW STATUS LIKE \"Threads_connected\";" 2>/dev/null | tail -1 && \
  echo "=FPM=" && systemctl is-active php8.4-fpm php8.3-fpm'
```

---

## Observações

**⚠️ NUNCA deixar Xdebug ativo em produção** — degrada performance em 50-300%. Usar sempre com trigger e remover em seguida.

**⚠️ Slow query log** tem custo de I/O. Usar por períodos curtos (5-10 min) e desligar.

**Baseline atual do servidor:**
- CPU Load normal: 0.6–1.0 (4 vCPUs → crítico > 4.0)
- Memory normal: ~9.4GB/16GB (58%)
- PHP-FPM 8.4 pool (`myapp`): checar `pm.max_children` — padrão é 10

**Para campanhas Meta Ads (MyApp):**
- Antes de aumentar budget, rodar `ab -n 500 -c 50 https://myapp.example.com/cadastrar`
- SLO: P95 < 1s, taxa de erro < 1%
- Se P95 > 1s: investigar MySQL (N+1 no cadastro) ou aumentar `pm.max_children` no FPM

**Interpretando resultados do ab:**
```
Requests per second: 45.3  → throughput
Time per request:    22ms  → latência média
50%: 18ms / 95%: 89ms / 99%: 234ms  → percentis importantes
Failed requests: 0         → zero erros
```

**Quando escalar vs otimizar:**
- Se CPU > 80% durante load test → otimizar código antes de escalar
- Se `Threads_connected` > 80 → connection pooling no Laravel (`DB_POOL_MAX`)
- Se Redis hit rate < 70% → revisar TTL das chaves de cache no Laravel