---
name: mysql-performance
description: Diagnose slow queries, index tables, analyze EXPLAIN plans, tune MySQL 8 in production with Laravel
---

# Skill: MySQL Performance — Diagnóstico e Tuning

## Quando Usar
- Uma rota Laravel está lenta e suspeita-se de query pesada
- `SHOW PROCESSLIST` mostra queries travadas ou rodando há >1s
- O slow query log acumulou entradas e precisa de análise
- CPU do MySQL alta e não se sabe qual query está causando

## Contexto
Servidor: MySQL 8.0.44, porta 3306, bind 127.0.0.1 (hardened)
Databases: `myapp_db`, `news_db`, `work_db`, `nn_db`, `extra_db`
Users app: `app1_user`, `app2_user`, `app3_user`, `app4_user` @localhost
User backup: `backup_sre`@localhost (SELECT only)
Laravel apps usam Eloquent — N+1 é o problema mais comum
Redis disponível para cache de queries pesadas

## Passos / Comandos

### 1. Diagnóstico Rápido
```bash
# Ver o que está rodando agora
mysql -e "SHOW FULL PROCESSLIST\G" | grep -v Sleep | head -60

# Quantas conexões por estado
mysql -e "SELECT command, count(*) FROM information_schema.processlist GROUP BY command;"

# Top queries por tempo acumulado (sem Percona, usa events_statements)
mysql -e "
SELECT LEFT(digest_text,80) AS query, count_star, avg_timer_wait/1e9 AS avg_sec, sum_timer_wait/1e9 AS total_sec
FROM performance_schema.events_statements_summary_by_digest
ORDER BY sum_timer_wait DESC LIMIT 10\G"
```

### 2. Slow Query Log
```bash
# Verificar se está ativo
mysql -e "SHOW VARIABLES LIKE 'slow_query%'; SHOW VARIABLES LIKE 'long_query_time';"

# Ativar em runtime (sem restart) — threshold 1s
mysql -e "SET GLOBAL slow_query_log = 'ON'; SET GLOBAL long_query_time = 1; SET GLOBAL slow_query_log_file = '/var/log/mysql/slow.log';"

# Analisar o log
mysqldumpslow -s t -t 10 /var/log/mysql/slow.log

# Ver últimas entradas raw
tail -50 /var/log/mysql/slow.log
```

### 3. EXPLAIN — Analisar Plano de Execução
```bash
# Formato tabela (básico)
mysql myapp_db -e "EXPLAIN SELECT * FROM users WHERE status = 'ativo' AND entity_id = 1\G"

# Formato JSON (mais detalhado — mostra cost estimates)
mysql myapp_db -e "EXPLAIN FORMAT=JSON SELECT ...\G"

# Com análise real de execução (MySQL 8+)
mysql myapp_db -e "EXPLAIN ANALYZE SELECT ...\G"
```

**Red flags no EXPLAIN:**
| Campo | Perigo | Ação |
|-------|--------|------|
| `type: ALL` | Full table scan | Criar índice |
| `type: index` | Full index scan | Refinar índice |
| `rows` > 10k | Muitas linhas | Filtro ou índice composto |
| `Extra: Using filesort` | Sort sem índice | Índice na coluna ORDER BY |
| `Extra: Using temporary` | Temp table | Índice ou redesign |

### 4. Criar Índices Seguros em Produção
```bash
# Ver índices existentes
mysql myapp_db -e "SHOW INDEX FROM users\G"

# Índice simples
mysql myapp_db -e "ALTER TABLE users ADD INDEX idx_status_entity (status, entity_id);"

# Índice sem travar tabela (MySQL 8 default, mas explícito)
mysql myapp_db -e "ALTER TABLE users ADD INDEX idx_email (email) ALGORITHM=INPLACE, LOCK=NONE;"

# Ver tamanho das tabelas (priorizar indexação nas grandes)
mysql -e "
SELECT table_schema, table_name,
  ROUND(data_length/1024/1024,2) AS data_mb,
  ROUND(index_length/1024/1024,2) AS index_mb,
  table_rows
FROM information_schema.tables
WHERE table_schema IN ('myapp_db','news_db','work_db')
ORDER BY data_length DESC LIMIT 20;"
```

### 5. Detectar N+1 no Laravel
```bash
# Ativar query log temporário no projeto
cd /home/deploy/myapp
sudo -u deploy php artisan tinker --execute="
DB::listen(fn(\$q) => logger(\$q->sql));
// agora faça a request que está lenta
"

# Ou via Telescope (se instalado)
mysql myapp_db -e "SELECT COUNT(*) FROM telescope_entries WHERE type='query' AND created_at > NOW() - INTERVAL 1 HOUR;"

# N+1 clássico: >50 queries idênticas variando só o ID
tail -200 storage/logs/laravel.log | grep "select \* from" | sort | uniq -c | sort -rn | head -20
```

### 6. Deadlocks
```bash
# Ver último deadlock
mysql -e "SHOW ENGINE INNODB STATUS\G" | grep -A 40 "LATEST DETECTED DEADLOCK"

# Monitorar deadlocks em tempo real
watch -n 5 "mysql -e \"SHOW GLOBAL STATUS LIKE 'Innodb_deadlocks';\""
```

### 7. InnoDB Buffer Pool (principal parâmetro de performance)
```bash
# Ver configuração atual
mysql -e "SHOW VARIABLES LIKE 'innodb_buffer_pool_size';"

# Ver hit ratio (deve ser >99%)
mysql -e "
SELECT 
  ROUND((1 - (s2.variable_value / s1.variable_value)) * 100, 2) AS hit_ratio_pct
FROM performance_schema.global_status s1
JOIN performance_schema.global_status s2 
  ON s1.variable_name='Innodb_buffer_pool_read_requests'
  AND s2.variable_name='Innodb_buffer_pool_reads';"

# Buffer pool atual: verificar em /etc/mysql/mysql.conf.d/mysqld.cnf
grep -i buffer_pool /etc/mysql/mysql.conf.d/mysqld.cnf
```

**Regra**: Buffer pool = 70% da RAM disponível para MySQL.
Servidor tem 16GB RAM, múltiplas apps → recomendado 4-6GB.

### 8. Kill Query Problemática
```bash
# Ver PID das queries lentas
mysql -e "SELECT id, user, host, db, time, state, LEFT(info,100) FROM information_schema.processlist WHERE time > 5 AND command != 'Sleep' ORDER BY time DESC;"

# Kill (substitui <PID>)
mysql -e "KILL QUERY <PID>;"   # Cancela só a query, mantém conexão
mysql -e "KILL <PID>;"          # Encerra conexão inteira
```

### 9. Cache com Redis para Queries Pesadas (Laravel)
```php
// Em vez de query direta, usar cache
$stats = Cache::remember("entity_{$id}_stats", 300, function() use ($id) {
    return Entity::withCount(['users', 'eventos'])->find($id);
});

// Invalidar ao salvar
Cache::forget("entity_{$id}_stats");
```

### 10. Monitorar via Grafana/Loki
```logql
# Queries lentas no Loki (se Promtail lê /var/log/mysql/slow.log)
{job="mysql-slow"} | regexp `Query_time: (?P<time>[0-9.]+)` | time > 2

# Contar deadlocks por hora
count_over_time({job="mysql"} |= "deadlock" [1h])
```

## Observações

**NUNCA** rodar `OPTIMIZE TABLE` em produção sem janela de manutenção — trava a tabela inteira.

**NUNCA** mudar `innodb_buffer_pool_size` sem restart do MySQL (não é runtime no 8.0 com múltiplos chunks sem cuidado).

**Cuidado com `ALTER TABLE` em tabelas grandes** (users, noticias com >500k rows) — usar `pt-online-schema-change` ou `gh-ost` se disponível, ou fazer em janela de baixo tráfego.

**Laravel Telescope** é o jeito mais fácil de ver N+1 — instalar em staging ao menos.

**Índices compostos**: ordem importa. `(status, entity_id)` serve para `WHERE status = X` e `WHERE status = X AND entity_id = Y`, mas NÃO para `WHERE entity_id = Y` sozinho.