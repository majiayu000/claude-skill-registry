# 💰 Skill: Cost Optimization & FinOps

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `sre-cost-optimization-finops` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 1.0.0 |
| **Keywords** | `cost-optimization`, `finops`, `cloud-costs`, `resource-optimization`, `cost-monitoring`, `budget-alerts` |
| **Referencia** | [FinOps Foundation](https://www.finops.org/) |

## 🔑 Keywords para Invocación

- `cost-optimization`
- `finops`
- `cloud-costs`
- `resource-optimization`
- `cost-monitoring`
- `budget-alerts`
- `@skill:cost-optimization`

### Ejemplos de Prompts

```
Implementa cost monitoring y budget alerts
```

```
Configura FinOps practices para cloud cost optimization
```

```
Setup resource optimization y cost allocation
```

```
@skill:cost-optimization - FinOps completo
```

## 📖 Descripción

FinOps (Financial Operations) combina prácticas financieras con DevOps para optimizar costos cloud. Este skill cubre cost monitoring, budget management, resource optimization, cost allocation, y cost optimization strategies.

### ✅ Cuándo Usar Este Skill

- Cloud infrastructure costs
- Multi-team cost allocation
- Budget management
- Resource optimization
- Cost visibility

### ❌ Cuándo NO Usar Este Skill

- On-premise only
- Fixed cost infrastructure
- Very small scale

## 🏗️ FinOps Framework

```
Inform
    ↓
Optimize
    ↓
Operate
    ↓
(Feedback Loop)
```

## 💻 Implementación

> **📁 Scripts Ejecutables:** Este skill incluye scripts Python ejecutables en la carpeta [`scripts/`](scripts/):
> - [`aws_cost_tracker.py`](scripts/aws_cost_tracker.py) - Tracking y análisis de costos AWS
> - [`budget_alert.py`](scripts/budget_alert.py) - Gestión de budgets y alertas
> - [`resource_optimizer.py`](scripts/resource_optimizer.py) - Análisis de recursos y optimización
> - [`auto_optimizer.py`](scripts/auto_optimizer.py) - Optimizador automático completo
> - [`requirements.txt`](scripts/requirements.txt) - Dependencias Python (boto3)
> 
> Ver [`scripts/README.md`](scripts/README.md) para documentación de uso.

### 1. Cost Monitoring

**Script ejecutable:** [`scripts/aws_cost_tracker.py`](scripts/aws_cost_tracker.py)

Script CLI completo para tracking y análisis de costos AWS usando Cost Explorer API.

#### Cuándo ejecutar

- **Reportes regulares:** Para generar reportes de costos diarios/semanales
- **Análisis de costos:** Para identificar servicios o tags con mayor costo
- **Exportación de datos:** Para integrar con otros sistemas o dashboards
- **Auditoría:** Para revisar costos históricos

#### Uso

```bash
# Instalar dependencias
pip install -r scripts/requirements.txt

# Costos diarios (últimos 30 días)
python scripts/aws_cost_tracker.py daily --days 30

# Costos por servicio
python scripts/aws_cost_tracker.py service EC2 --days 30

# Costos por tag
python scripts/aws_cost_tracker.py tag --tag-key Environment --days 30

# Exportar a CSV
python scripts/aws_cost_tracker.py daily --days 30 --output costs.csv
```

#### Características

- ✅ Costos diarios agrupados por servicio
- ✅ Costos por servicio específico
- ✅ Costos agrupados por tags
- ✅ Exportación a CSV
- ✅ Formato legible en consola
- ✅ Soporte para múltiples perfiles AWS

### 2. Budget Alerts

**Script ejecutable:** [`scripts/budget_alert.py`](scripts/budget_alert.py)

Gestor completo de budgets AWS con alertas automatizadas por email.

#### Cuándo ejecutar

- **Crear budgets:** Al establecer límites de gasto para servicios o proyectos
- **Monitoreo:** Para revisar estado de budgets existentes
- **Gestión:** Para listar, actualizar o eliminar budgets

#### Uso

```bash
# Crear budget con alertas
python scripts/budget_alert.py create \
  --name monthly-infrastructure-budget \
  --amount 10000 \
  --period monthly \
  --thresholds 50,80,100 \
  --email ops@example.com

# Listar todos los budgets
python scripts/budget_alert.py list

# Ver estado de un budget
python scripts/budget_alert.py status --name monthly-infrastructure-budget

# Eliminar budget
python scripts/budget_alert.py delete --name monthly-infrastructure-budget
```

#### Características

- ✅ Creación de budgets con múltiples umbrales de alerta
- ✅ Notificaciones por email automáticas
- ✅ Filtros por servicio (opcional)
- ✅ Listado y estado de budgets
- ✅ Gestión completa (crear, listar, eliminar)

#### Ejemplo de configuración YAML

```yaml
# aws/budgets.yml (para referencia)
budgets:
  - name: monthly-infrastructure-budget
    amount: 10000
    period: monthly
    thresholds: [50, 80, 100]
    email: ops@example.com
```

### 3. Resource Optimization

**Script ejecutable:** [`scripts/resource_optimizer.py`](scripts/resource_optimizer.py)

Analizador de recursos AWS que identifica oportunidades de optimización de costos.

#### Cuándo ejecutar

- **Análisis regular:** Para identificar recursos subutilizados
- **Antes de optimizar:** Para planificar cambios de recursos
- **Auditoría de costos:** Para encontrar oportunidades de ahorro

#### Uso

```bash
# Encontrar instancias idle (CPU < 10%)
python scripts/resource_optimizer.py idle --cpu-threshold 10

# Oportunidades de rightsizing
python scripts/resource_optimizer.py rightsize

# Volúmenes EBS no usados
python scripts/resource_optimizer.py unused-volumes
```

#### Características

- ✅ Detección de instancias idle (bajo CPU)
- ✅ Análisis de rightsizing (downsize/upsize)
- ✅ Detección de volúmenes no usados
- ✅ Estimación de costos y ahorros potenciales
- ✅ Análisis multi-región (opcional)

### 4. Cost Allocation Tags

```yaml
# k8s/cost-allocation-tags.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production
    cost-center: engineering
    team: backend
    project: payment-service
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
  labels:
    app: payment-service
    environment: production
    cost-center: engineering
    team: backend
    project: payment-service
spec:
  template:
    metadata:
      labels:
        app: payment-service
        environment: production
        cost-center: engineering
        team: backend
        project: payment-service
    spec:
      containers:
      - name: app
        image: payment-service:latest
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi
```

### 5. Automated Cost Optimization

**Script ejecutable:** [`scripts/auto_optimizer.py`](scripts/auto_optimizer.py)

Optimizador automático que combina múltiples estrategias de optimización y genera reportes completos.

#### Cuándo ejecutar

- **Análisis completo:** Para obtener visión general de todas las oportunidades
- **Reportes regulares:** Para generar reportes de optimización periódicos
- **Planificación:** Para planificar optimizaciones de costos

#### Uso

```bash
# Análisis completo
python scripts/auto_optimizer.py analyze

# Generar reporte detallado
python scripts/auto_optimizer.py report --output optimization-report.json
```

#### Características

- ✅ Análisis completo combinando múltiples estrategias
- ✅ Recomendaciones priorizadas por ahorro potencial
- ✅ Reportes detallados en JSON
- ✅ Estimación de ahorros totales
- ✅ Identificación de instancias idle, rightsizing, y recursos no usados

## 🎯 Mejores Prácticas

### 1. Cost Visibility

✅ **DO:**
- Tag all resources
- Track costs by team/service
- Set up budget alerts
- Review costs regularly

❌ **DON'T:**
- Ignore untagged resources
- Skip cost reviews
- Set unrealistic budgets

### 2. Optimization

✅ **DO:**
- Right-size resources
- Use reserved instances for steady workloads
- Implement auto-scaling
- Clean up unused resources

❌ **DON'T:**
- Over-provision
- Ignore idle resources
- Skip rightsizing

### 3. Governance

✅ **DO:**
- Establish cost policies
- Require approvals for large spends
- Track cost trends
- Share costs with teams

❌ **DON'T:**
- Allow unlimited spending
- Ignore cost trends
- Hide costs from teams

## 🚨 Troubleshooting

### Unexpected Costs

1. Check recent changes
2. Review cost reports
3. Identify cost drivers
4. Implement cost controls

### Budget Exceeded

1. Review spending
2. Identify overages
3. Optimize resources
4. Adjust budget if needed

## 📚 Recursos Adicionales

- [FinOps Foundation](https://www.finops.org/)
- [AWS Cost Management](https://aws.amazon.com/aws-cost-management/)
- [Cloud Cost Optimization](https://www.gartner.com/en/articles/10-cloud-cost-optimization-strategies)

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025  
**Total líneas:** 1,100+

