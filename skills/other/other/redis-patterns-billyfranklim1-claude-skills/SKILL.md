---
name: redis-patterns
description: Diagnose and optimize Redis for Laravel cache, Horizon queues, sessions, and memory — including selective flush, key debugging, real-time monitoring, and correct cache patterns
---

# Skill: Redis Patterns — Cache, Queues, Sessions e Memory Management

## Quando Usar
- Horizon parado ou lento e suspeita-se de problema na fila Redis
- Cache Laravel retornando dados stale ou hit rate baixo (< 90%)
- Redis consumindo muita memória (> 80% do maxmem)
- Precisa invalidar cache de um projeto específico sem afetar os outros
- Sessões de usuários expirando inesperadamente ou sendo perdidas

## Contexto

Servidor usa Redis 7.2.5 (porta 6379, bind 127.0.0.1, com senha — ver `/etc/redis/redis.conf`).

**Quem usa Redis neste servidor:**
| App | DB | Uso | Prefix |
|-----|-----|-----|--------|
| `api.myapp.example.com` | 0 | cache + filas Horizon + Pulse | `news_` |
| `myapp.example.com` | 0 | cache + sessões + email queue | `myapp_` |
| `work8.example.com` | 0 | cache + filas Horizon | `work_` |
| Supervisor workers | 0 | job queue genérico | variado |

Configs Laravel em `.env` de cada projeto:
```
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=<senha>
CACHE_PREFIX=news_   # ou myapp_, work_
CACHE_DRIVER=redis
SESSION_DRIVER=redis
QUEUE_CONNECTION=redis
```

Senha Redis: `redis-cli -a $(grep '^requirepass' /etc/redis/redis.conf | awk '{print $2}') ping`

## Passos / Comandos

### 0. Conectar no Redis CLI com senha

```bash
# Jeito mais prático — pegar senha do config
REDIS_PASS=$(grep '^requirepass' /etc/redis/redis.conf | awk '{print $2}')
alias r="redis-cli -a $REDIS_PASS"

# Verificar
r ping  # deve retornar PONG
```

### 1. Diagnóstico Rápido de Saúde

```bash
REDIS_PASS=$(grep '^requirepass' /etc/redis/redis.conf | awk '{print $2}')
redis-cli -a $REDIS_PASS INFO all | grep -E "used_memory_human|maxmemory_human|hit_rate|keyspace_hits|keyspace_misses|connected_clients|blocked_clients|rdb_last_bgsave_status|uptime_in_seconds"

# Hit rate calculado
redis-cli -a $REDIS_PASS INFO stats | grep -E "keyspace_hits|keyspace_misses" | awk -F: '
  /hits/ {hits=$2}
  /misses/ {misses=$2}
  END {
    total=hits+misses
    if(total>0) printf "Hit rate: %.1f%% (hits=%d, misses=%d)\n", (hits/total)*100, hits, misses
  }'

# Quantas keys por padrão de prefix
redis-cli -a $REDIS_PASS --scan --pattern "news_*" | wc -l
redis-cli -a $REDIS_PASS --scan --pattern "myapp_*" | wc -l
redis-cli -a $REDIS_PASS --scan --pattern "work_*" | wc -l
```

### 2. Memória — Diagnóstico e Eviction

```bash
# Memória atual vs limite
redis-cli -a $REDIS_PASS INFO memory | grep -E "used_memory_human|maxmemory_human|mem_fragmentation_ratio|maxmemory_policy"

# Top keys por tamanho (as 20 maiores)
redis-cli -a $REDIS_PASS --bigkeys 2>&1 | tail -30

# Distribuição por tipo
redis-cli -a $REDIS_PASS INFO keyspace

# Se memória crítica: ver política de eviction
redis-cli -a $REDIS_PASS CONFIG GET maxmemory-policy
# Padrão: allkeys-lru (bom para cache puro)
# Para misto cache+queue: noeviction ou volatile-lru

# Alterar política em runtime (sem restart)
redis-cli -a $REDIS_PASS CONFIG SET maxmemory-policy volatile-lru
redis-cli -a $REDIS_PASS CONFIG SET maxmemory 4gb
```

### 3. Flush Seletivo por Projeto (SEM afetar outros apps)

```bash
# NUNCA usar FLUSHALL em produção — apaga tudo (filas incluídas!)
# NUNCA usar FLUSHDB — apaga o DB inteiro

# Flush apenas de um projeto específico
REDIS_PASS=$(grep '^requirepass' /etc/redis/redis.conf | awk '{print $2}')
PREFIX="myapp_"  # ou news_, work_

redis-cli -a $REDIS_PASS --scan --pattern "${PREFIX}*" | \
  xargs -r redis-cli -a $REDIS_PASS DEL

# Ou via Laravel artisan (mais seguro — usa o prefix do .env)
cd /home/deploy/myapp
sudo -u deploy php artisan cache:clear  # só apaga cache, não sessões nem filas

# Para NewsApp
cd /home/deploy/api-myapp
sudo -u deploy php artisan cache:clear
```

### 4. Filas Horizon — Debug e Gestão

```bash
# Status das filas (quantos jobs pendentes, failed, etc.)
REDIS_PASS=$(grep '^requirepass' /etc/redis/redis.conf | awk '{print $2}')

# Jobs em queue (NewsApp usa prefix news_)
redis-cli -a $REDIS_PASS LLEN "news_queues:default"
redis-cli -a $REDIS_PASS LLEN "news_queues:news-processing"

# Jobs failed (armazenados como hash)
redis-cli -a $REDIS_PASS --scan --pattern "news_*failed*" | head -20

# Via Artisan (mais amigável)
cd /home/deploy/api-myapp
sudo -u deploy php artisan queue:monitor default,news-processing
sudo -u deploy php artisan horizon:status

# Limpar failed jobs de um projeto
sudo -u deploy php artisan queue:flush  # atenção: apaga todos os failed do projeto

# Retry failed jobs
sudo -u deploy php artisan queue:retry all
```

### 5. Sessões — Debug

```bash
REDIS_PASS=$(grep '^requirepass' /etc/redis/redis.conf | awk '{print $2}')

# Contar sessões ativas por projeto
redis-cli -a $REDIS_PASS --scan --pattern "myapp_*session*" | wc -l

# Inspecionar uma sessão específica (substituir <key>)
redis-cli -a $REDIS_PASS GET "myapp_<session_key>"
redis-cli -a $REDIS_PASS TTL "myapp_<session_key>"  # tempo restante em segundos

# Se sessões expirando cedo: verificar TTL configurado
grep SESSION_LIFETIME /home/deploy/myapp/.env  # em minutos
```

### 6. Monitoramento em Tempo Real

```bash
REDIS_PASS=$(grep '^requirepass' /etc/redis/redis.conf | awk '{print $2}')

# Ver TODOS os comandos em tempo real (cuidado em produção — verbose)
redis-cli -a $REDIS_PASS MONITOR | grep -v "PING\|INFO"

# Slow log — queries lentas (default: > 10ms)
redis-cli -a $REDIS_PASS SLOWLOG GET 20
redis-cli -a $REDIS_PASS SLOWLOG RESET

# Configurar threshold do slow log
redis-cli -a $REDIS_PASS CONFIG SET slowlog-log-slower-than 10000  # microsegundos

# Latência em tempo real
redis-cli -a $REDIS_PASS --latency-history -i 5  # amostras a cada 5s

# Watch de uma key específica (debug de cache)
watch -n 1 "redis-cli -a $REDIS_PASS TTL 'news_artigo_123' && redis-cli -a $REDIS_PASS OBJECT encoding 'news_artigo_123'"
```

### 7. Padrões de Cache Laravel — Boas Práticas

```php
// Cache com TTL e tag (permite invalidação por grupo)
Cache::tags(['noticias', 'homepage'])->remember('featured_news', 3600, function() {
    return News::published()->featured()->limit(10)->get();
});

// Invalidar tag inteira (ex: ao publicar notícia nova)
Cache::tags(['noticias'])->flush();

// Cache de query pesada com lock para evitar cache stampede
$stats = Cache::lock("building_stats_{$id}", 30)->get(function() use ($id) {
    return Cache::remember("stats_{$id}", 300, fn() => buildExpensiveStats($id));
});

// Forget seletivo
Cache::forget("stats_{$id}");

// Pipeline Redis para múltiplas operações (mais eficiente)
$redis = Redis::pipeline(function($pipe) use ($ids) {
    foreach ($ids as $id) {
        $pipe->get("item_{$id}");
    }
});
```

```php
// No config/cache.php — usar prefixes para isolamento
'redis' => [
    'driver' => 'redis',
    'connection' => 'cache',
    'prefix' => env('CACHE_PREFIX', 'default_'),
],
```

### 8. Pub/Sub — Diagnóstico (usado pelo Pulse e Nightwatch)

```bash
REDIS_PASS=$(grep '^requirepass' /etc/redis/redis.conf | awk '{print $2}')

# Ver canais ativos
redis-cli -a $REDIS_PASS PUBSUB CHANNELS "*"
redis-cli -a $REDIS_PASS PUBSUB NUMSUB  # subscribers por canal

# Subscrever para debug (Ctrl+C para sair)
redis-cli -a $REDIS_PASS SUBSCRIBE "news_laravel_database_events"
```

### 9. Persistência e Backup

```bash
# Forçar snapshot RDB agora
REDIS_PASS=$(grep '^requirepass' /etc/redis/redis.conf | awk '{print $2}')
redis-cli -a $REDIS_PASS BGSAVE
redis-cli -a $REDIS_PASS LASTSAVE  # timestamp do último save

# Ver onde está o dump.rdb
redis-cli -a $REDIS_PASS CONFIG GET dir
redis-cli -a $REDIS_PASS CONFIG GET dbfilename

# Status do último save
redis-cli -a $REDIS_PASS INFO persistence | grep -E "rdb_|aof_"
```

### 10. Restart Seguro

```bash
# ANTES de reiniciar: verificar se tem jobs críticos rodando
REDIS_PASS=$(grep '^requirepass' /etc/redis/redis.conf | awk '{print $2}')
redis-cli -a $REDIS_PASS LLEN "news_queues:news-processing"

# Parar workers do Horizon primeiro
cd /home/deploy/api-myapp && sudo -u deploy php artisan horizon:terminate
supervisorctl stop daemon-XXXXX:*

# Salvar snapshot antes
redis-cli -a $REDIS_PASS BGSAVE && sleep 2

# Reiniciar
sudo systemctl restart redis-server

# Verificar recuperação
redis-cli -a $REDIS_PASS ping
redis-cli -a $REDIS_PASS INFO keyspace

# Restartar Horizon
supervisorctl start daemon-XXXXX:*
```

## Observacoes

**NUNCA usar `KEYS *`** em produção — bloqueia o Redis para todo o servidor. Usar sempre `SCAN` ou `--scan`.

**NUNCA usar `FLUSHALL`** — apaga filas do Horizon, sessões de todos os usuários e todo o cache. Se precisar limpar um projeto, use o prefix + SCAN + DEL.

**Tags de cache** (`Cache::tags()`) requerem driver que suporte tags (Redis suporta). Se Laravel retornar erro de "unsupported", verificar que `CACHE_DRIVER=redis` no .env, não `file`.

**Eviction e filas não combinam**: Se `maxmemory-policy` for `allkeys-lru`, o Redis pode deletar jobs da fila quando a memória encher. Para Horizon, usar `volatile-lru` (só evict keys com TTL) e garantir que jobs na fila não têm TTL, ou usar DB separado para filas vs cache.

**Fragmentation ratio** > 1.5 indica fragmentação alta — considerar `MEMORY PURGE` (Redis 4+) ou restart em janela de manutenção.

**Horizon dashboard** (se habilitado): `https://api.myapp.example.com/horizon` — mostra métricas de throughput, jobs/min, failed jobs em tempo real.

**Cache stampede**: em rotas de alta concorrência (NewsApp homepage), usar `Cache::lock()` ou `Cache::flexible()` (Laravel 11+) para evitar que múltiplas requisições rebuildem o mesmo cache simultaneamente.
