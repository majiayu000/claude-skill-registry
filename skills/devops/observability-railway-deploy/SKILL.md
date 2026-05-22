---
name: observability-railway-deploy
description: Deploy LGTM observability stack to Railway cloud. Use when deploying cloud-hosted observability with team access.
---

# Observability Railway Deploy

Deploy Grafana, Loki, Tempo, Prometheus, and Alloy to Railway for cloud-hosted observability.

## Workflow

1. **Verify Railway CLI** installed and authenticated
2. **Deploy Template 8TLSQD** (Grafana stack)
3. **Configure Environment Variables** (admin credentials, retention)
4. **Attach Persistent Volumes** (Grafana, Loki, Tempo, Prometheus data)
5. **Get Public URLs** (Grafana dashboard, Alloy OTLP endpoint)
6. **Generate Claude Code Config** for Railway endpoint
7. **Verify Deployment** (health checks, telemetry flow)

## Output

```
✅ Railway Stack Deployed!

Access URLs:
  Grafana: https://your-grafana-abc123.railway.app
  OTLP Endpoint: https://your-alloy-abc123.railway.app:443

Next: Use claude-code-telemetry-enable --mode railway --endpoint <OTLP_URL>
```

## Cost Estimate
- Free tier: $5 credit/month (testing)
- Production: $15-25/month (5 services, 10GB volumes)

## Scripts
- `scripts/deploy-to-railway.sh` - Automated Railway deployment
- `scripts/get-railway-urls.sh` - Fetch public URLs
