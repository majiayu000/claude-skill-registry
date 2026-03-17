---
name: deploy_monitoring
router_kit: DevOpsKit
description: Health checks, metrics, alerting ve rollback stratejileri.
metadata:
  skillport:
    category: operations
    tags: [automation, aws, bash scripting, ci/cd, cloud computing, containerization, deploy monitoring, deployment strategies, devops, docker, gitops, infrastructure, infrastructure as code, kubernetes, linux, logging, microservices, monitoring, orchestration, pipelines, reliability, scalability, security, server management, terraform]      - deploy-cicd
---

# 📊 Deploy Monitoring

> Monitoring, alerting ve rollback stratejileri.

---

## ❤️ Health Checks

```typescript
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', version: process.env.APP_VERSION });
});

app.get('/ready', async (req, res) => {
  await db.$queryRaw`SELECT 1`;
  res.json({ status: 'ready' });
});
```

---

## 📈 Metrics (Prometheus)

```typescript
const httpDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests',
  labelNames: ['method', 'route', 'status'],
});
```

---

## 🚨 Alert Rules

```yaml
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
  for: 5m
  labels:
    severity: critical
```

---

## ⏪ Rollback

```bash
# Kubernetes
kubectl rollout undo deployment/app

# Vercel
vercel rollback
```

---

## 🔄 Workflow

> **Kaynak:** [Google SRE Book - Monitoring](https://sre.google/sre-book/monitoring-distributed-systems/) & [Prometheus Best Practices](https://prometheus.io/docs/practices/instrumentation/)

### Aşama 1: Observability Instrumentation
- [ ] **Health Checks**: `/health` (Liveness) ve `/ready` (Readiness) uç noktalarını tanımla.
- [ ] **Custom Metrics**: Uygulamaya özel kritik metrikleri (Örn: Sipariş sayısı, Hata oranı) Prometheus/Grafana için dışa aktar.
- [ ] **Log Centralization**: Dağınık logları ELK (Elasticsearch/Logstash/Kibana) veya Datadog gibi bir merkezde topla.

### Aşama 2: SLI/SLO & Alerting Setup
- [ ] **Defining SLIs**: Başarı göstergelerini (Latency < 200ms, Error rate < %1) belirle.
- [ ] **Alert Groups**: Kritik hataları (P0) telefon/PagerDuty üzerinden, bilgilendirme amaçlı olanları Slack üzerinden bildir.
- [ ] **Error Budget**: SLO'nuzun ne kadar dışına çıkabileceğinizi (Hata Bütçesi) hesapla ve aşım yaklaştığında deployları durdur.

### Aşama 3: Analysis & Incident Response
- [ ] **Dashboarding**: Grafana üzerinde sistem sağlığını gösteren gerçek zamanlı panolar oluştur.
- [ ] **Post-Mortem**: Her büyük olaydan (Incident) sonra kök neden analizi (Root Cause Analysis) yap ve dökümante et.
- [ ] **Automated Rollback**: Kritik alert tetiklendiğinde sistemin otomatik bir önceki stabil versiyona dönmesini sağla.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Yeni bir servis eklendiğinde monitoring otomatik devreye giriyor mu? |
| 2 | Alertler "aksiyon alınabilir" (Actionable) bilgi içeriyor mu? |
| 3 | Loglarda PII (Kişisel veri) maskeleniyor mu? |

---
*Deploy Monitoring v1.5 - With Workflow*
