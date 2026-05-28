---
name: fibonacci-optimization
description: Optimización evolutiva y paramétrica basada en Fibonacci y el Número Áureo (phi).
trigger: fibonacci OR golden ratio OR evolutionary optimization OR search search OR spiral sampling
scope: global
---

# Skill: Fibonacci & Golden Ratio Optimization

## Contexto

El uso de la secuencia de Fibonacci y el Número Áureo ($\phi \approx 1.618$) para optimizar búsquedas, tamaños de población y distribución de parámetros. Inspirado en la eficiencia de la naturaleza.

## Cuándo Usar

- Optimización de hiperparámetros (tuning de temperatura, top-p, etc.).
- Gestión de población en algoritmos genéticos (FSGA).
- Búsquedas espaciales o muestreo uniforme (Spiral Sampling).
- Estrategias de reintento/backoff (Fibonacci backoff).

## Patrones de Implementación

### 1. Fibonacci Population Control (FSGA)
Dinámica de población que permite exploración amplia inicial y refinamiento denso posterior.

```python
def fib_pop_size(generation, base=10):
    a, b = 1, 1
    for _ in range(generation):
        a, b = b, a + b
    return b * base
```

### 2. Golden Section Search
Para encontrar el óptimo global en funciones unimodales sin usar derivadas.

```python
def golden_search(f, a, b, tol=1e-5):
    phi = (1 + 5**0.5) / 2
    resphi = 2 - phi
    c = a + resphi * (b - a)
    d = b - resphi * (b - a)
    # ... loop de reducción de intervalo ...
```

### 3. Fibonacci Spiral Sampling
Distribución uniforme de puntos para evitar sesgos en el espacio de parámetros.

```python
def gold_spiral(n):
    points = []
    phi = math.pi * (3. - math.sqrt(5.))
    for i in range(n):
        y = 1 - (i / float(n - 1)) * 2
        r = math.sqrt(1 - y * y)
        theta = phi * i
        points.append((math.cos(theta) * r, y, math.sin(theta) * r))
    return points
```

## Reglas Críticas

1. **Backoff Natural** - Usar [1, 1, 2, 3, 5, 8] para timeouts; es más balanceado que el exponencial puro.
2. **Corte Áureo** - Para selección de supervivientes, el top 61.8% ($1/\phi$) suele ser el punto de equilibrio óptimo entre elitismo y diversidad.
3. **Escalamiento Progresivo** - No saturar recursos; crecer siguiendo la secuencia para detectar fallos temprano.

## Recursos Relacionados

- `knowledge/chuletas/FIBONACCI_EVOLUTIONARY_OPTIMIZATION.md`
- `skills/genetic-algorithms/SKILL.md`
- `skills/prompt-engineering/SKILL.md`
