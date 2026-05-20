# 💥 Skill: Chaos Engineering

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `sre-chaos-engineering` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `chaos-engineering`, `chaos-monkey`, `litmus`, `failure-injection`, `resilience-testing`, `chaos-experiments` |
| **Referencia** | [Chaos Engineering Principles](https://principlesofchaos.org/) |

## 🔑 Keywords para Invocación

- `chaos-engineering`
- `chaos-monkey`
- `litmus`
- `failure-injection`
- `resilience-testing`
- `chaos-experiments`
- `@skill:chaos-engineering`

### Ejemplos de Prompts

```
Implementa chaos engineering con Litmus para resilience testing
```

```
Configura chaos experiments y failure injection
```

```
Setup Chaos Monkey para probar resiliencia del sistema
```

```
@skill:chaos-engineering - Chaos engineering completo
```

## 📖 Descripción

Chaos engineering es la práctica de inyectar fallos intencionalmente para probar la resiliencia de sistemas. Este skill cubre chaos experiments, failure injection, resilience testing, y herramientas como Litmus y Chaos Monkey.

### ✅ Cuándo Usar Este Skill

- Sistemas en producción
- Testing de resiliencia
- Validación de failover
- Identificación de puntos débiles
- Mejora de reliability

### ❌ Cuándo NO Usar Este Skill

- Sistemas en desarrollo temprano
- Sin monitoring adecuado
- Sin rollback procedures
- Sin equipo preparado

## 🏗️ Chaos Engineering Process

```
Hypothesis
    ↓
Experiment Design
    ↓
Execute Experiment
    ↓
Observe & Measure
    ↓
Learn & Improve
```

## 💻 Implementación

> **📁 Scripts Ejecutables:** Este skill incluye scripts ejecutables en la carpeta [`scripts/`](scripts/):
> - **Chaos Monkey:** [`scripts/chaos_monkey.py`](scripts/chaos_monkey.py) - Chaos Monkey para Kubernetes
> - **Experiments:** [`scripts/experiments.py`](scripts/experiments.py) - Framework para chaos experiments
>
> Ver [`scripts/README.md`](scripts/README.md) para documentación de uso completa.

### 1. Litmus Chaos Experiments

```yaml
# chaos/pod-delete-experiment.yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: pod-delete-chaos
  namespace: default
spec:
  annotationCheck: 'true'
  engineState: 'active'
  chaosServiceAccount: litmus-admin
  monitoring: true
  jobCleanUpPolicy: 'retain'
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: '60'
            - name: CHAOS_INTERVAL
              value: '10'
            - name: FORCE
              value: 'false'
            - name: RAMP_TIME
              value: '10'
        probe:
          - name: check-app-health
            type: httpProbe
            httpProbeInputs:
              url: http://app-service/health
              insecureSkipVerify: false
            mode: Continuous
            runProperties:
              probeTimeout: 5
              interval: 2
              retry: 1
```

```yaml
# chaos/network-chaos.yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: network-chaos
spec:
  engineState: 'active'
  chaosServiceAccount: litmus-admin
  experiments:
    - name: network-chaos
      spec:
        components:
          env:
            - name: NETWORK_INTERFACE
              value: 'eth0'
            - name: NETWORK_PACKET_LOSS_PERCENTAGE
              value: '100'
            - name: TARGET_CONTAINER
              value: 'app-container'
            - name: TARGET_PODS
              value: 'app-.*'
            - name: TOTAL_CHAOS_DURATION
              value: '120'
```

### 2. Chaos Monkey Implementation

**Script ejecutable:** [`scripts/chaos_monkey.py`](scripts/chaos_monkey.py)

Chaos Monkey para Kubernetes que elimina aleatoriamente pods y recursos para probar resiliencia.

**Cuándo ejecutar:**
- Testing de resiliencia en producción
- Validación de failover
- Identificación de puntos débiles

**Uso:**
```bash
# Ejecutar experimento (pod-delete)
python scripts/chaos_monkey.py run --experiment-type pod-delete

# Habilitar/deshabilitar
python scripts/chaos_monkey.py enable
python scripts/chaos_monkey.py disable

# Configurar probabilidad
python scripts/chaos_monkey.py set-probability --probability 0.1
```

**Características:**
- ✅ Eliminación aleatoria de pods
- ✅ Probabilidad configurable
- ✅ Filtrado por annotations (`chaos.enabled=true`)
- ✅ Múltiples tipos de experimentos

### 3. Chaos Experiments

**Script ejecutable:** [`scripts/experiments.py`](scripts/experiments.py)

Framework para ejecutar y gestionar chaos experiments con hipótesis y resultados.

**Cuándo ejecutar:**
- Ejecución de experiments estructurados
- Gestión de múltiples experiments
- Registro de nuevos experiments

**Uso:**
```bash
# Ejecutar experimento
python scripts/experiments.py run --name pod-delete

# Listar experimentos
python scripts/experiments.py list
```

**Características:**
- ✅ Framework de experiments estructurado
- ✅ Hipótesis y expected behavior
- ✅ Tracking de resultados
- ✅ Registro de experiments

### 4. Automated Chaos Testing

```yaml
# chaos/chaos-test-schedule.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: chaos-monkey
spec:
  schedule: "0 */6 * * *"  # Every 6 hours
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: chaos-monkey
            image: chaos-monkey:latest
            env:
            - name: ENABLED
              value: "true"
            - name: PROBABILITY
              value: "0.1"
            - name: EXPERIMENT_TYPES
              value: "pod-delete,cpu-stress"
            command:
            - python
            - chaos_monkey.py
            - --schedule
          restartPolicy: OnFailure
```

### 5. Chaos Metrics

```python
# chaos/metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Metrics
chaos_experiments_total = Counter(
    'chaos_experiments_total',
    'Total chaos experiments run',
    ['experiment_type', 'status']
)

chaos_experiment_duration = Histogram(
    'chaos_experiment_duration_seconds',
    'Duration of chaos experiments',
    ['experiment_type']
)

system_recovery_time = Histogram(
    'system_recovery_time_seconds',
    'Time for system to recover from chaos',
    ['experiment_type']
)

chaos_experiments_active = Gauge(
    'chaos_experiments_active',
    'Number of active chaos experiments'
)

def record_experiment(experiment_type: str, status: str, duration: float):
    """Record chaos experiment metrics."""
    chaos_experiments_total.labels(
        experiment_type=experiment_type,
        status=status
    ).inc()

    chaos_experiment_duration.labels(
        experiment_type=experiment_type
    ).observe(duration)
```

## 🎯 Mejores Prácticas

### 1. Experiment Design

✅ **DO:**
- Start with hypothesis
- Test in non-production first
- Start small and increase
- Monitor during experiments

❌ **DON'T:**
- Run experiments without hypothesis
- Start in production
- Run multiple experiments simultaneously
- Ignore monitoring

### 2. Safety

✅ **DO:**
- Use feature flags
- Have rollback procedures
- Set experiment duration limits
- Monitor system health

❌ **DON'T:**
- Run experiments without safety measures
- Ignore system health
- Exceed experiment duration
- Skip rollback procedures

### 3. Learning

✅ **DO:**
- Document results
- Share learnings
- Improve based on results
- Regular experiments

❌ **DON'T:**
- Skip documentation
- Ignore results
- Run experiments randomly
- Stop after first success

## 🚨 Troubleshooting

### Experiments Causing Issues

1. Stop experiment immediately
2. Review experiment design
3. Check system health
4. Adjust experiment parameters

### No Recovery

1. Check failover mechanisms
2. Review monitoring
3. Investigate root cause
4. Fix underlying issues

## 📚 Recursos Adicionales

- [Chaos Engineering Principles](https://principlesofchaos.org/)
- [Litmus Documentation](https://litmuschaos.io/docs/)
- [Chaos Monkey](https://github.com/Netflix/chaosmonkey)

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
**Total líneas:** 1,100+
