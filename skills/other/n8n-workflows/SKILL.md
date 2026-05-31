---
name: n8n-workflows
description: "n8n otomasyon workflow'lari. Webhook, cron trigger, API entegrasyon, CI/CD otomasyon."
---

# n8n Workflows

## n8n MCP Server Kurulumu

### NPM Kurulum

```bash
npm install -g n8n
n8n start  # http://localhost:5678
```

### Docker Kurulum

```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=<strong-password> \
  n8nio/n8n
```

### MCP Server Config

```json
{
  "mcpServers": {
    "n8n": {
      "command": "npx",
      "args": ["-y", "@anthropic/n8n-mcp-server"],
      "env": {
        "N8N_API_URL": "http://localhost:5678/api/v1",
        "N8N_API_KEY": "<n8n-api-key>"
      }
    }
  }
}
```

### API Key Olusturma

```
n8n UI > Settings > API > Create API Key
Scope: workflow:read, workflow:write, execution:read
```

## Workflow Olusturma

### Temel Yapi

```json
{
  "name": "My Workflow",
  "nodes": [
    {
      "name": "Trigger",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300],
      "parameters": {
        "path": "my-webhook",
        "httpMethod": "POST"
      }
    },
    {
      "name": "Process",
      "type": "n8n-nodes-base.function",
      "position": [450, 300],
      "parameters": {
        "functionCode": "return items.map(item => ({ json: { processed: true, ...item.json } }));"
      }
    }
  ],
  "connections": {
    "Trigger": {
      "main": [[{ "node": "Process", "type": "main", "index": 0 }]]
    }
  }
}
```

### MCP ile Workflow Olustur

```
n8n.create_workflow({
  name: "Deploy Notification",
  nodes: [...],
  connections: {...},
  active: true
})
```

### Workflow Listele

```
n8n.list_workflows({
  active: true,
  tags: ["production"]
})
```

### Workflow Calistir

```
n8n.execute_workflow({
  workflow_id: "123",
  data: {
    environment: "production",
    version: "v1.2.3"
  }
})
```

## Trigger Tipleri

### Webhook Trigger

```json
{
  "type": "n8n-nodes-base.webhook",
  "parameters": {
    "path": "deploy-hook",
    "httpMethod": "POST",
    "authentication": "headerAuth",
    "options": {
      "responseMode": "responseNode",
      "responseCode": 200
    }
  }
}
```

### Cron Trigger

```json
{
  "type": "n8n-nodes-base.cron",
  "parameters": {
    "triggerTimes": {
      "item": [
        { "mode": "everyDay", "hour": 9, "minute": 0 },
        { "mode": "custom", "cronExpression": "0 */6 * * *" }
      ]
    }
  }
}
```

### Event Trigger'lar

| Trigger | Kaynak | Kullanim |
|---------|--------|----------|
| Webhook | Dis sistem | GitHub push, Stripe payment |
| Cron | Zamanlama | Gunluk rapor, cleanup |
| Email (IMAP) | Email | Support ticket olusturma |
| RSS | Feed | Icerik izleme |
| Telegram | Bot mesaj | Komut isleme |
| GitHub | Repo event | CI/CD tetikleme |
| Slack | Mesaj/mention | Team notification |
| Database | Row change | Data sync |

### Poll Trigger

```json
{
  "type": "n8n-nodes-base.pollTrigger",
  "parameters": {
    "pollTimes": {
      "item": [{ "mode": "everyMinute", "minute": 5 }]
    },
    "url": "https://api.example.com/status"
  }
}
```

## Node Tipleri ve Kullanimi

### HTTP Request

```json
{
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://api.example.com/data",
    "method": "POST",
    "authentication": "predefinedCredentialType",
    "nodeCredentialType": "httpHeaderAuth",
    "sendBody": true,
    "bodyParameters": {
      "parameters": [
        { "name": "key", "value": "={{ $json.value }}" }
      ]
    },
    "options": {
      "timeout": 10000,
      "retry": { "maxRetries": 3, "retryInterval": 1000 }
    }
  }
}
```

### Function Node (JavaScript)

```json
{
  "type": "n8n-nodes-base.function",
  "parameters": {
    "functionCode": "const results = [];\nfor (const item of items) {\n  const data = item.json;\n  results.push({\n    json: {\n      name: data.name.toUpperCase(),\n      processed_at: new Date().toISOString()\n    }\n  });\n}\nreturn results;"
  }
}
```

### IF Node (Kosul)

```json
{
  "type": "n8n-nodes-base.if",
  "parameters": {
    "conditions": {
      "string": [
        {
          "value1": "={{ $json.status }}",
          "operation": "equal",
          "value2": "success"
        }
      ]
    }
  }
}
```

### Switch Node

```json
{
  "type": "n8n-nodes-base.switch",
  "parameters": {
    "dataType": "string",
    "value1": "={{ $json.priority }}",
    "rules": {
      "rules": [
        { "value2": "critical", "output": 0 },
        { "value2": "high", "output": 1 },
        { "value2": "low", "output": 2 }
      ]
    }
  }
}
```

### Merge Node

```json
{
  "type": "n8n-nodes-base.merge",
  "parameters": {
    "mode": "mergeByKey",
    "propertyName1": "id",
    "propertyName2": "userId"
  }
}
```

### Yaygin Node'lar

| Node | Amac | Ornek |
|------|------|-------|
| HTTP Request | API cagir | REST endpoint |
| Function | Kod calistir | Data transform |
| IF/Switch | Dallanma | Kosula gore yonlendir |
| Set | Data ata | Field ekle/degistir |
| Merge | Birlestir | Iki kaynak birlestir |
| Split In Batches | Parcala | Rate limiting |
| Wait | Bekle | Delay/approval |
| Error Trigger | Hata yakala | Hata notification |
| Slack | Mesaj gonder | Team bildirim |
| Gmail | Email gonder | Notification |
| Postgres/MySQL | DB islem | CRUD |
| Redis | Cache | Key-value store |

## API Entegrasyonu

### Credential Yonetimi

```
n8n UI > Settings > Credentials > New Credential
Tipler: API Key, OAuth2, Basic Auth, Header Auth

// Workflow'da kullanim
"authentication": "predefinedCredentialType",
"nodeCredentialType": "slackApi"
```

### REST API Cagirma

```json
{
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://api.github.com/repos/{{ $json.owner }}/{{ $json.repo }}/pulls",
    "method": "GET",
    "authentication": "predefinedCredentialType",
    "nodeCredentialType": "githubApi",
    "options": {
      "response": { "response": { "fullResponse": true } }
    }
  }
}
```

### Pagination Handling

```javascript
// Function node: paginated API cagirma
const allResults = [];
let page = 1;
let hasMore = true;

while (hasMore) {
  const response = await this.helpers.httpRequest({
    url: `https://api.example.com/items?page=${page}&per_page=100`,
    method: 'GET',
  });
  allResults.push(...response.data);
  hasMore = response.data.length === 100;
  page++;
}

return allResults.map(item => ({ json: item }));
```

## Error Handling

### Try/Catch Pattern

```json
{
  "nodes": [
    {
      "name": "Try",
      "type": "n8n-nodes-base.httpRequest",
      "continueOnFail": true,
      "parameters": { "url": "https://api.example.com/data" }
    },
    {
      "name": "Check Error",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "boolean": [
            { "value1": "={{ $json.error }}", "value2": true }
          ]
        }
      }
    },
    {
      "name": "Error Handler",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel": "#alerts",
        "text": "Workflow error: {{ $json.error.message }}"
      }
    }
  ]
}
```

### Error Workflow

```
n8n UI > Workflow Settings > Error Workflow
Global error handler: her basarisiz workflow bu workflow'u tetikler

Error workflow node'lari:
1. Error Trigger → hata bilgisini al
2. Function → hatayi formatla
3. Slack/Email → bildirim gonder
4. HTTP Request → incident sisteme kaydet
```

### Retry Stratejisi

```json
{
  "parameters": {
    "options": {
      "retry": {
        "maxRetries": 3,
        "retryInterval": 2000,
        "retryOnTimeout": true
      }
    }
  }
}
```

## Workflow Debugging

### Execution Log

```
n8n.list_executions({
  workflow_id: "123",
  status: "error",
  limit: 10
})
```

### Execution Detayi

```
n8n.get_execution({
  execution_id: "456",
  include_data: true
})
// Her node'un input/output data'sini gosterir
```

### Debug Teknikleri

```
1. Manual execution: UI'da "Execute Workflow" tikla
2. Node output: Her node'un ciktisini incele
3. Expression editor: {{ $json.field }} ifadelerini test et
4. Console log: Function node'da console.log() kullan
5. Test webhook: Postman/curl ile webhook'u test et
6. Pin data: Test data'yi node'a sabitle (development icin)
```

## CI/CD Entegrasyonu

### GitHub Actions ile n8n

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        run: ./deploy.sh
      - name: Notify n8n
        run: |
          curl -X POST https://n8n.example.com/webhook/deploy-complete \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer ${{ secrets.N8N_WEBHOOK_TOKEN }}" \
            -d '{
              "repo": "${{ github.repository }}",
              "branch": "${{ github.ref_name }}",
              "commit": "${{ github.sha }}",
              "actor": "${{ github.actor }}"
            }'
```

### Claude Code'dan Workflow Tetikleme

```bash
# Webhook ile tetikle
curl -X POST http://localhost:5678/webhook/my-workflow \
  -H "Content-Type: application/json" \
  -d '{"action": "deploy", "version": "v1.2.3"}'

# API ile tetikle
curl -X POST http://localhost:5678/api/v1/workflows/123/execute \
  -H "X-N8N-API-KEY: <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"data": {"key": "value"}}'
```

### Workflow Export/Import (GitOps)

```bash
# Export (backup)
curl -s http://localhost:5678/api/v1/workflows \
  -H "X-N8N-API-KEY: <key>" | jq '.' > workflows-backup.json

# Import
curl -X POST http://localhost:5678/api/v1/workflows \
  -H "X-N8N-API-KEY: <key>" \
  -H "Content-Type: application/json" \
  -d @workflow.json
```

## Ornek Workflow'lar

### 1. Deploy Notification

```
Trigger: Webhook (GitHub Actions'dan)
  → Function: Deploy bilgisini formatla
  → Slack: #deployments kanalina bildir
  → IF: Production deploy mi?
    → YES: Telegram'a da bildir
    → NO: Sadece Slack
```

```json
{
  "name": "Deploy Notification",
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": { "path": "deploy-notify", "httpMethod": "POST" }
    },
    {
      "name": "Format",
      "type": "n8n-nodes-base.function",
      "parameters": {
        "functionCode": "const d = items[0].json;\nreturn [{ json: { text: `Deploy: ${d.repo} (${d.branch}) by ${d.actor}\\nCommit: ${d.commit.substring(0,7)}` } }];"
      }
    },
    {
      "name": "Slack",
      "type": "n8n-nodes-base.slack",
      "parameters": { "channel": "#deployments", "text": "={{ $json.text }}" }
    }
  ]
}
```

### 2. Issue Triage

```
Trigger: GitHub (issue opened)
  → Function: Label belirle (title/body analizi)
  → GitHub: Label ata
  → IF: Bug mu?
    → YES: Slack #bugs kanalina bildir, P1 ise mention
    → NO: Backlog'a ekle
```

### 3. PR Review Reminder

```
Trigger: Cron (her gun 10:00)
  → GitHub: Acik PR'lari listele
  → IF: 24+ saat review bekleyen var mi?
    → YES: Slack'te reviewer'a mention at
    → NO: Bos geç
```

### 4. Daily Standup Collector

```
Trigger: Cron (her gun 09:00)
  → Slack: #standup kanalina soru gonder
  → Wait: 2 saat
  → Slack: Cevaplari topla
  → Function: Ozet olustur
  → Notion: Standup sayfasina kaydet
```

### 5. Error Alert Pipeline

```
Trigger: Webhook (app error handler'dan)
  → Function: Error dedup (son 5dk ayni hata var mi)
  → IF: Yeni hata mi?
    → YES:
      → Switch (severity):
        → Critical: PagerDuty + Slack + Telegram
        → High: Slack + Email
        → Low: Slack only
    → NO: Counter artir, sessiz kal
```

## Best Practices

### Workflow Tasarimi

| Kural | Aciklama |
|-------|----------|
| Tek sorumluluk | Her workflow tek bir is yapsin |
| Error handling | Her dis API call'da continueOnFail |
| Idempotent | Ayni input, ayni output (retry-safe) |
| Timeout | HTTP request'lere timeout koy |
| Rate limit | Split In Batches ile API limit'e uy |
| Credential | Hardcode yapma, n8n credential store kullan |
| Naming | Node isimlerini aciklayici yap |
| Testing | Pin data ile test et, sonra production'a al |

### Guvenlik

```
1. Webhook'lara authentication ekle (header auth veya HMAC)
2. Credential'lari n8n credential store'da tut
3. Sensitive data'yi log'lama
4. Network: n8n'i public internet'e ACMA (reverse proxy kullan)
5. API key'leri environment variable'dan al
6. Workflow export'larinda credential'lar OLMAZ (import sonrasi set et)
```

### Performans

```
1. Batch processing: Split In Batches node kullan
2. Parallel execution: baska node'lara dallan
3. Caching: Redis node ile sik kullanilan data'yi cache'le
4. Pagination: Buyuk data set'lerde sayfalama yap
5. Timeout: Uzun workflow'lara timeout koy (workflow settings)
6. Cleanup: Eski execution log'larini sil (Settings > Pruning)
```

## Anti-Patterns

| Anti-Pattern | Dogru Yol |
|-------------|-----------|
| Monolithic workflow | Kucuk, tek sorumluluk workflow'lar |
| No error handling | continueOnFail + error workflow |
| Hardcoded credentials | n8n credential store |
| No retry | Retry config ekle |
| Polling every second | Webhook kullan veya 5min+ interval |
| No dedup | Duplicate event kontrolu ekle |
| No monitoring | Execution log + error alert workflow |
