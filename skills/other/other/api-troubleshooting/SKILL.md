---
name: api-troubleshooting
description: Debug external and internal API failures — timeout, rate limit, authentication, webhook, latency, retry
---

# Skill: API Troubleshooting — Debug de Integrações

## Quando Usar
- Job Laravel falha silenciosamente ao chamar Gemini, ElevenLabs, Late API, Meta Ads ou Asaas
- Webhook do AutoFix Pipeline (`glitchtip.example.com/autofix/callback/`) não chega ou chega duplicado
- Google Indexing retorna 429 ou 403 e artigos param de ser indexados
- `api.myapp.example.com/health` OK mas pipeline de notícias trava numa etapa específica

## Contexto

**APIs externas em produção neste servidor:**

| API | Usado por | Tipo de Auth | Rate Limit típico |
|-----|-----------|-------------|-------------------|
| Gemini | NewsApp Image + Blog | API Key | 60 req/min (free) |
| ElevenLabs | NewsApp Podcast | API Key | quota mensal |
| Late API | NewsApp Social + SR Social Bot | API Key | por plano |
| Meta Ads Graph v22 | NewsApp + SR Ads | Bearer Token (expira abr/2026) | 200 calls/hr/user |
| Meta CAPI | NewsApp Newsletter | Access Token | — |
| Asaas | MyApp billing | API Key | — |
| Google Indexing | NewsApp + SR | Service Account OAuth2 | 200 URLs/dia (quota compartilhada!) |
| Cloudflare API | DNS, R2, Tunnels | API Token | — |
| GlitchTip Webhook | AutoFix Pipeline | HMAC secret | — |

**Paths relevantes:**
```
/home/deploy/api-myapp/.env          # API keys + tokens
/home/deploy/myapp/.env     # META_ADS_TOKEN, META_CAPI_TOKEN, ASAAS_API_KEY
/root/.autofix/                           # AutoFix pipeline
/root/.sre-config/                        # Scripts SRE
```

**Quota crítica:** Google Indexing = 200 URLs/dia **compartilhada** entre NewsApp e MyApp. Se NewsApp processar muitas news num dia, MyApp para de indexar.

## Passos / Comandos

### 1. Diagnóstico rápido de falha externa

```bash
# Ver últimos erros de HTTP em jobs Laravel
cd /home/deploy/api-myapp
grep -i "curl\|guzzle\|http\|timeout\|connect\|refused\|429\|401\|403\|500" storage/logs/laravel.log | tail -50

# Mesma coisa para MyApp
grep -i "curl\|guzzle\|http\|timeout\|429\|401" /home/deploy/myapp/storage/logs/laravel.log | tail -30

# Jobs falhados na fila
sudo -u deploy php /home/deploy/api-myapp/artisan queue:failed | head -20
sudo -u deploy php /home/deploy/api-myapp/artisan queue:failed --show-batch | grep -A5 "google\|gemini\|late\|eleven"
```

### 2. Testar API manualmente com curl verboso

```bash
# Testar Gemini (pegar GEMINI_API_KEY do .env)
GEMINI_KEY=$(grep GEMINI_API_KEY /home/deploy/api-myapp/.env | cut -d= -f2)
curl -sv -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"ping"}]}]}' \
  2>&1 | grep -E "^[<>*]|HTTP|error|rate"

# Testar endpoint interno de saúde
curl -sv https://api.myapp.example.com/health 2>&1 | grep -E "^[<>*]|HTTP|time"

# Testar com timing detalhado (latência breakdown)
curl -w "\ndns:%{time_namelookup} connect:%{time_connect} ssl:%{time_appconnect} ttfb:%{time_starttransfer} total:%{time_total}\n" \
  -o /dev/null -s https://api.myapp.example.com/health
```

### 3. Debug de rate limiting (429)

```bash
# Google Indexing — checar quota do dia
cd /home/deploy/api-myapp
sudo -u deploy php artisan tinker --execute="
\$count = \App\Models\News::whereDate('updated_at', today())
    ->where('indexed_at', '>=', today())
    ->count();
echo 'URLs indexadas hoje: ' . \$count . '/200';
"

# Meta Ads — token expira em abr/2026, checar validity
META_TOKEN=$(grep META_ADS_TOKEN /home/deploy/myapp/.env | cut -d= -f2)
curl -s "https://graph.facebook.com/v22.0/me?access_token=${META_TOKEN}" | python3 -m json.tool | grep -E "id|name|error"

# Late API — checar status
LATE_KEY=$(grep LATE_API_KEY /home/deploy/api-myapp/.env | cut -d= -f2 2>/dev/null || echo "nao encontrado")
echo "Late API Key presente: ${#LATE_KEY} chars"
```

### 4. Debug de webhook (AutoFix Pipeline)

```bash
# Checar se callback endpoint está respondendo
curl -sv http://localhost:8096/health 2>&1 | grep -E "HTTP|error"

# Ver últimas requisições recebidas
journalctl -u autofix-pipeline.service --since "2 hours ago" --no-pager | grep -E "POST|GET|webhook|error" | tail -30

# Simular webhook GlitchTip (sem signature)
curl -X POST http://localhost:8096/webhook \
  -H 'Content-Type: application/json' \
  -d '{"test": true}' -v 2>&1 | tail -5

# Ver runs pendentes
ls -la /root/.autofix/runs/ 2>/dev/null | tail -10
```

### 5. Timeout e connection issues

```bash
# DNS resolution de APIs externas (detecta hijacking ou falha DNS)
for host in generativelanguage.googleapis.com graph.facebook.com api.asaas.com api.elevenlabs.io; do
  echo -n "$host → "; dig +short $host | head -1
done

# Testar conectividade direta (bypass DNS)
curl -sv --connect-timeout 5 --max-time 10 https://generativelanguage.googleapis.com/ 2>&1 | grep -E "connected|SSL|error|HTTP"

# Verificar se UFW está bloqueando saída (não deve, mas checar)
sudo ufw status | grep -E "ALLOW OUT|DENY OUT"

# Checar se IP do servidor não está em blocklist
SERVER_IP=$(curl -s ifconfig.me)
echo "Servidor IP: $SERVER_IP"
curl -s "https://api.abuseipdb.com/api/v2/check?ipAddress=${SERVER_IP}" 2>/dev/null | head -3
```

### 6. Analisar falhas em jobs falhados

```bash
cd /home/deploy/api-myapp

# Listar failed jobs com detalhes
sudo -u deploy php artisan queue:failed 2>/dev/null | head -30

# Ver detalhes de um job específico por ID
# sudo -u deploy php artisan queue:failed:show {id}

# Retry job específico
# sudo -u deploy php artisan queue:retry {id}

# Retry todos de uma fila específica
# sudo -u deploy php artisan queue:retry --queue=news-processing

# Flush failed jobs (após investigar!)
# sudo -u deploy php artisan queue:flush
```

### 7. Monitorar chamadas API em tempo real

```bash
# Capturar HTTP sair do servidor (tcpdump não invasivo)
sudo tcpdump -i any -n 'port 443' -A 2>/dev/null | grep -E "Host:|GET |POST " | head -20

# Ou via strace em worker específico (mais preciso)
WORKER_PID=$(pgrep -f "queue:work.*news-processing" | head -1)
[ -n "$WORKER_PID" ] && sudo strace -p $WORKER_PID -e trace=network -s 200 2>&1 | head -30

# Ver conexões abertas dos workers Laravel
ss -tp | grep php | head -20
```

### 8. Checar SSL/TLS de APIs externas

```bash
# Certificado do proprio servidor
echo | openssl s_client -servername api.myapp.example.com -connect api.myapp.example.com:443 2>/dev/null | openssl x509 -noout -dates

# Certificado do myapp
echo | openssl s_client -servername myapp.example.com -connect myapp.example.com:443 2>/dev/null | openssl x509 -noout -enddate

# Verificar todos de uma vez
for domain in api.myapp.example.com myapp.example.com frontend.example.com work8.example.com; do
  EXPIRY=$(echo | openssl s_client -servername $domain -connect $domain:443 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
  echo "$domain → expira: $EXPIRY"
done
```

## Observações

**Quota Google Indexing (CRÍTICO):** 200 URLs/dia compartilhadas. Se pipeline NewsApp rodar em burst (ex: após longo downtime), pode esgotar a quota e bloquear indexação do MyApp. Monitorar com o tinker acima.

**Meta Ads Token expira abr/2026.** Quando expirar, campanhas param de funcionar. Renovar em https://developers.facebook.com → token de longa duração. Novo token vai em: `$META_ADS_TOKEN` no `.bashrc` + `.env` de myapp.

**Late API:** Addons Analytics/Inbox NÃO contratados — não testar endpoints premium.

**Gemini free tier:** Sem key configurada cai no free tier (mais restrito). Checar se `GEMINI_API_KEY` está no `.env` e não expirou.

**Guzzle timeout padrão Laravel:** 30s. Se API externa demorar mais, o job falha com `ConnectionException`. Verificar se há `timeout` configurado no service provider da API.

**AutoFix callbacks:** URL pública `glitchtip.example.com` — se Cloudflare estiver com cache agressivo pode "swallow" o POST. Verificar regra de bypass de cache para `/autofix/callback/*`.