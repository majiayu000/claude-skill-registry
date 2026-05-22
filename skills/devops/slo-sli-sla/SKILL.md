# 📈 Skill: Service Level Objectives (SLO/SLI/SLA)

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `sre-slo-sli-sla` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `slo`, `sli`, `sla`, `error-budget`, `service-level`, `reliability`, `availability` |
| **Referencia** | [Google SRE Book - SLIs, SLAs, SLOs](https://sre.google/workbook/slo-document/) |

## 🔑 Keywords para Invocación

- `slo`
- `sli`
- `sla`
- `error-budget`
- `service-level`
- `reliability`
- `availability`
- `@skill:slo`

### Ejemplos de Prompts

```
Implementa SLOs y error budgets para servicios críticos
```

```
Define SLIs y configura monitoreo de SLOs
```

```
Setup SLA compliance y error budget tracking
```

```
@skill:slo - Sistema completo de SLO/SLI/SLA
```

## 📖 Descripción

Service Level Objectives (SLOs) definen objetivos de confiabilidad medibles para servicios. Este skill cubre la definición de SLIs (Service Level Indicators), creación de SLOs, cálculo de error budgets, y monitoreo de compliance con SLAs.

### ✅ Cuándo Usar Este Skill

- Servicios en producción con SLAs
- Productos con requisitos de confiabilidad
- Stakeholders requieren métricas de confiabilidad
- Error budget management
- Capacity planning basado en SLOs

### ❌ Cuándo NO Usar Este Skill

- Prototipos sin usuarios
- Servicios internos sin requisitos de confiabilidad
- Sistemas legacy sin capacidad de medición

## 🏗️ Framework SLO

```
SLI (Service Level Indicator)
    ↓
SLO (Service Level Objective) ← Error Budget
    ↓
SLA (Service Level Agreement)
```

## 💻 Implementación

> **📁 Scripts Ejecutables:** Este skill incluye scripts Python ejecutables en la carpeta [`scripts/`](scripts/):
> - [`error_budget.py`](scripts/error_budget.py) - Calculadora de error budget (CLI)
> - [`slo_api.py`](scripts/slo_api.py) - API REST para consultar SLOs desde Prometheus
> - [`requirements.txt`](scripts/requirements.txt) - Dependencias Python
> 
> Ver ejemplos de uso en [`examples/usage_example.py`](examples/usage_example.py)

### 1. Definición de SLIs

#### 1.1 SLI Types

```yaml
# sli-definitions.yml
service_level_indicators:
  # Availability SLI
  - name: request_availability
    type: availability
    metric: |
      (
        sum(rate(http_requests_total{status!~"5.."}[5m]))
        /
        sum(rate(http_requests_total[5m]))
      )
    window: 5m
    description: "Percentage of successful requests"

  # Latency SLI
  - name: request_latency_p99
    type: latency
    metric: |
      histogram_quantile(0.99,
        sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
      )
    window: 5m
    percentile: 99
    description: "99th percentile request latency"

  # Freshness SLI
  - name: data_freshness
    type: freshness
    metric: |
      time() - last_successful_data_update_timestamp
    threshold: 3600  # 1 hour
    description: "Age of most recent data update"

  # Correctness SLI
  - name: data_correctness
    type: correctness
    metric: |
      sum(rate(data_validation_errors_total[5m]))
      /
      sum(rate(data_operations_total[5m]))
    description: "Percentage of correct data operations"
```

### 2. SLO Definitions

```yaml
# slo-definitions.yml
service_level_objectives:
  - service: payment-service
    slo_name: availability
    sli: request_availability
    target: 99.95  # 99.95% availability
    window: 30d
    description: "Payment service must be available 99.95% of the time"
    
  - service: payment-service
    slo_name: latency_p99
    sli: request_latency_p99
    target: 1.0  # 1 second
    window: 30d
    description: "99th percentile latency must be under 1 second"
    
  - service: user-service
    slo_name: availability
    sli: request_availability
    target: 99.9  # 99.9% availability
    window: 30d
    description: "User service must be available 99.9% of the time"

  - service: analytics-service
    slo_name: data_freshness
    sli: data_freshness
    target: 3600  # 1 hour
    window: 30d
    description: "Analytics data must be updated within 1 hour"
```

### 3. Error Budget Calculation

**Script ejecutable:** [`scripts/error_budget.py`](scripts/error_budget.py)

Este script calcula y gestiona error budgets para SLOs. Puede ejecutarse como CLI o importarse como módulo.

#### Cuándo ejecutar

- **Análisis manual:** Calcular error budget para reportes o análisis
- **Validación:** Verificar si un servicio está consumiendo demasiado error budget
- **Planificación:** Calcular cuántos errores se pueden permitir antes de violar el SLO
- **Integración:** Importar la clase `ErrorBudget` en otros scripts

#### Uso como CLI

```bash
# Instalación (no requiere dependencias externas)
cd skills/system-reliability-engineering/slo-sli-sla

# Ejemplo básico
python scripts/error_budget.py \
  --slo-target 0.9995 \
  --total-requests 1000000 \
  --error-requests 400

# Modo interactivo
python scripts/error_budget.py \
  --slo-target 0.9995 \
  --interactive

# Ventana personalizada
python scripts/error_budget.py \
  --slo-target 0.9999 \
  --window-days 7 \
  --total-requests 500000 \
  --error-requests 10
```

#### Uso como módulo

```python
from scripts.error_budget import ErrorBudget

# Crear instancia
error_budget = ErrorBudget(slo_target=0.9995, window_days=30)

# Calcular estado
status = error_budget.calculate_remaining_budget(
    total_requests=1_000_000,
    error_requests=400
)

print(f"Status: {status['status']}")
print(f"Remaining: {status['remaining_percentage']:.2f}%")
```

#### Ejemplos completos

Ver [`examples/usage_example.py`](examples/usage_example.py) para más ejemplos de uso programático.

### 4. Prometheus SLO Queries

```promql
# SLO Compliance Query
# Availability SLO: 99.95% over 30 days

# Current availability (last 30 days)
(
  sum(rate(http_requests_total{service="payment-service", status!~"5.."}[5m]))[30d:]
  /
  sum(rate(http_requests_total{service="payment-service"}[5m]))[30d:]
) >= 0.9995

# Error budget remaining
(
  1 - (
    sum(rate(http_requests_total{service="payment-service", status=~"5.."}[5m]))[30d:]
    /
    sum(rate(http_requests_total{service="payment-service"}[5m]))[30d:]
  )
) / (1 - 0.9995)

# Error budget consumption rate
(
  sum(rate(http_requests_total{service="payment-service", status=~"5.."}[5m]))[30d:]
  /
  sum(rate(http_requests_total{service="payment-service"}[5m]))[30d:]
) / (1 - 0.9995)

# Burn rate (how fast we're consuming error budget)
# 2x burn rate = using 2x the allowed error rate
(
  sum(rate(http_requests_total{service="payment-service", status=~"5.."}[5m]))
  /
  sum(rate(http_requests_total{service="payment-service"}[5m]))
) / (1 - 0.9995) / (30 * 24 * 3600) * 86400

# Alert when error budget will be exhausted in 4 hours
(
  (
    sum(rate(http_requests_total{service="payment-service", status=~"5.."}[5m]))[30d:]
    /
    sum(rate(http_requests_total{service="payment-service"}[5m]))[30d:]
  ) / (1 - 0.9995)
  +
  (
    (
      sum(rate(http_requests_total{service="payment-service", status=~"5.."}[5m]))
      /
      sum(rate(http_requests_total{service="payment-service"}[5m]))
    ) / (1 - 0.9995) / (30 * 24 * 3600) * 14400
  )
) >= 1
```

### 5. SLO Monitoring Dashboard (Grafana)

```json
{
  "dashboard": {
    "title": "SLO Dashboard - Payment Service",
    "panels": [
      {
        "title": "Availability SLO (99.95%)",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{service=\"payment-service\", status!~\"5..\"}[5m]))[30d:] / sum(rate(http_requests_total{service=\"payment-service\"}[5m]))[30d:]",
            "legendFormat": "Current Availability"
          },
          {
            "expr": "0.9995",
            "legendFormat": "SLO Target"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Error Budget Remaining",
        "targets": [
          {
            "expr": "(1 - (sum(rate(http_requests_total{service=\"payment-service\", status=~\"5..\"}[5m]))[30d:] / sum(rate(http_requests_total{service=\"payment-service\"}[5m]))[30d:])) / (1 - 0.9995)",
            "legendFormat": "Remaining Budget %"
          }
        ],
        "type": "graph",
        "alert": {
          "conditions": [
            {
              "evaluator": {
                "params": [0.25],
                "type": "lt"
              },
              "operator": {
                "type": "and"
              },
              "query": {
                "params": ["A", "5m", "now"]
              },
              "reducer": {
                "params": [],
                "type": "last"
              },
              "type": "query"
            }
          ],
          "executionErrorState": "alerting",
          "for": "5m",
          "name": "Error Budget at Risk",
          "notifications": ["slack-alerts"]
        }
      },
      {
        "title": "Error Budget Burn Rate",
        "targets": [
          {
            "expr": "(sum(rate(http_requests_total{service=\"payment-service\", status=~\"5..\"}[5m])) / sum(rate(http_requests_total{service=\"payment-service\"}[5m]))) / (1 - 0.9995) / (30 * 24 * 3600) * 86400",
            "legendFormat": "Daily Burn Rate"
          },
          {
            "expr": "1",
            "legendFormat": "1x (Normal)"
          },
          {
            "expr": "14",
            "legendFormat": "14x (Critical)"
          }
        ],
        "type": "graph"
      }
    ]
  }
}
```

### 6. SLO Alert Rules

```yaml
# prometheus/alerts/slo-alerts.yml
groups:
  - name: slo_alerts
    interval: 30s
    rules:
      # Error budget at risk (25% remaining)
      - alert: ErrorBudgetAtRisk
        expr: |
          (
            1 - (
              sum(rate(http_requests_total{service="payment-service", status=~"5.."}[5m]))[30d:]
              /
              sum(rate(http_requests_total{service="payment-service"}[5m]))[30d:]
            )
          ) / (1 - 0.9995) < 0.25
        for: 5m
        labels:
          severity: warning
          slo: availability
        annotations:
          summary: "Error budget at risk for {{ $labels.service }}"
          description: "Only {{ $value }}% of error budget remaining"

      # Error budget will be exhausted soon
      - alert: ErrorBudgetExhaustionImminent
        expr: |
          (
            (
              sum(rate(http_requests_total{service="payment-service", status=~"5.."}[5m]))[30d:]
              /
              sum(rate(http_requests_total{service="payment-service"}[5m]))[30d:]
            ) / (1 - 0.9995)
            +
            (
              (
                sum(rate(http_requests_total{service="payment-service", status=~"5.."}[5m]))
                /
                sum(rate(http_requests_total{service="payment-service"}[5m]))
              ) / (1 - 0.9995) / (30 * 24 * 3600) * 14400
            )
          ) >= 1
        for: 5m
        labels:
          severity: critical
          slo: availability
        annotations:
          summary: "Error budget will be exhausted in 4 hours"
          description: "Current burn rate will consume remaining budget"

      # SLO violation
      - alert: SLOViolation
        expr: |
          (
            sum(rate(http_requests_total{service="payment-service", status!~"5.."}[5m]))[30d:]
            /
            sum(rate(http_requests_total{service="payment-service"}[5m]))[30d:]
          ) < 0.9995
        for: 1m
        labels:
          severity: critical
          slo: availability
        annotations:
          summary: "SLO violation for {{ $labels.service }}"
          description: "Availability is {{ $value }}, below SLO target of 99.95%"
```

### 7. SLO API Service

**Script ejecutable:** [`scripts/slo_api.py`](scripts/slo_api.py)

Servicio REST FastAPI para consultar el estado de SLOs y error budgets desde métricas de Prometheus.

#### Cuándo ejecutar

- **Servicio en producción:** Como microservicio corriendo continuamente
- **Integración con dashboards:** Para alimentar dashboards de Grafana u otros
- **Alertas automatizadas:** Para sistemas que necesitan consultar SLOs programáticamente
- **APIs internas:** Para que otros servicios consulten el estado de SLOs

#### Instalación

```bash
cd skills/system-reliability-engineering/slo-sli-sla
pip install -r scripts/requirements.txt
```

#### Ejecución

```bash
# Desarrollo (con auto-reload)
uvicorn scripts.slo_api:app --reload --host 0.0.0.0 --port 8000

# Producción
uvicorn scripts.slo_api:app --host 0.0.0.0 --port 8000 --workers 4

# Con Prometheus personalizado
PROMETHEUS_URL=http://prometheus:9090 uvicorn scripts.slo_api:app --reload
```

#### Endpoints

**Health Check:**
```bash
curl http://localhost:8000/health
```

**SLO Compliance:**
```bash
curl "http://localhost:8000/slo/payment-service/compliance?slo_target=0.9995&window_days=30"
```

**Error Budget Status:**
```bash
curl "http://localhost:8000/slo/payment-service/error-budget?slo_target=0.9995&window_days=30"
```

#### Documentación API

Una vez ejecutando, accede a:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

#### Configuración

Variables de entorno:
- `PROMETHEUS_URL`: URL de Prometheus (default: `http://localhost:9090`)

#### Ejemplo de respuesta

```json
{
  "service": "payment-service",
  "slo_target": 0.9995,
  "current_availability": 0.9998,
  "is_compliant": true,
  "error_budget_remaining": 0.6,
  "window_days": 30,
  "burn_rate": 0.8,
  "days_to_exhaustion": 22.5,
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🎯 Mejores Prácticas

### 1. SLI Selection

✅ **DO:**
- Choose SLIs that matter to users
- Make SLIs easy to measure
- Use percentiles for latency (p50, p95, p99)
- Align SLIs with business goals

❌ **DON'T:**
- Use internal metrics as SLIs
- Make SLIs too complex
- Ignore user experience

### 2. SLO Targets

✅ **DO:**
- Start with achievable targets
- Review and adjust regularly
- Different targets for different services
- Consider error budgets

❌ **DON'T:**
- Set targets too high initially
- Set same target for all services
- Ignore error budget consumption

### 3. Error Budgets

✅ **DO:**
- Track error budget consumption
- Alert when budget is at risk
- Use budget for release decisions
- Review budget trends

❌ **DON'T:**
- Ignore error budget consumption
- Deploy when budget is exhausted
- Set budgets too conservatively

## 🚨 Troubleshooting

### SLO Violations

1. Analyze root cause
2. Check recent changes
3. Review error patterns
4. Implement fixes
5. Document in post-mortem

### Error Budget Exhaustion

1. Stop new releases
2. Focus on stability
3. Fix known issues
4. Replenish budget before new features

## 📚 Recursos Adicionales

- [Google SRE - SLIs, SLAs, SLOs](https://sre.google/workbook/slo-document/)
- [SRE Error Budgets](https://sre.google/workbook/implementing-slos/)
- [SLO Calculator](https://www.atlassian.com/incident-management/kpis/sla-vs-slo-vs-sli)

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025  
**Total líneas:** 1,100+

