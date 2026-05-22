---
name: genetic-algorithms
description: Genetic Algorithms for AI optimization - EvoPrompt, hyperparameter tuning, evolutionary strategies.
trigger: genetic OR evolution OR optimize prompts OR hyperparameter tuning OR GA
scope: global
---

# Skill: Genetic Algorithms

## Contexto

Algoritmos genéticos para optimización de prompts, hyperparámetros, y búsqueda en espacios complejos donde gradientes no existen.

## Cuándo Usar

- Optimizar prompts automáticamente
- Tuning de hyperparámetros (learning rate, batch size, etc.)
- Búsqueda en espacios discretos/no diferenciables
- Cuando necesitás múltiples soluciones (no solo una)

## Reglas Críticas

1. **Fitness rápido** - Evaluación debe ser eficiente
2. **Seeds diversos** - Población inicial variada
3. **Elitismo** - Siempre preservar mejores individuos
4. **Stopping criterio** - Definir cuándo parar

## Procedimiento

### 1. Definir Representación Genética
```python
# Para prompts: texto
gene = "Step by step, analyze..."

# Para hyperparams: dict
gene = {"lr": 0.001, "batch": 32}
```

### 2. Crear Función de Fitness
```python
def fitness(gene) -> float:
    """Evaluar calidad del gene. Mayor = mejor."""
    result = test_gene(gene)
    return accuracy(result)
```

### 3. Implementar Operadores
```python
# Crossover
def crossover(p1, p2):
    point = random.randint(1, len(p1)-1)
    return p1[:point] + p2[point:]

# Mutation
def mutate(gene, rate=0.1):
    if random.random() < rate:
        return apply_mutation(gene)
    return gene
```

### 4. Ejecutar Loop Evolutivo
```python
population = initialize(seeds)
for gen in range(max_generations):
    evaluate(population)
    selected = tournament_select(population)
    population = breed(selected)
```

## Ejemplo Completo (EvoPrompt)

```python
class EvoPrompt:
    def __init__(self, pop_size=20, gens=50):
        self.pop_size = pop_size
        self.gens = gens
        self.population = []
    
    def evolve(self, seeds: list, fitness_fn) -> str:
        # Initialize
        self.population = [{"text": s, "score": 0} for s in seeds]
        while len(self.population) < self.pop_size:
            self.population.append({
                "text": self.mutate(random.choice(seeds)),
                "score": 0
            })
        
        # Evolve
        for gen in range(self.gens):
            # Evaluate
            for ind in self.population:
                ind["score"] = fitness_fn(ind["text"])
            
            # Select & breed
            self.population.sort(key=lambda x: x["score"], reverse=True)
            elite = self.population[:5]  # Keep top 5
            
            new_pop = elite.copy()
            while len(new_pop) < self.pop_size:
                p1, p2 = random.sample(elite, 2)
                child = self.crossover(p1["text"], p2["text"])
                child = self.mutate(child)
                new_pop.append({"text": child, "score": 0})
            
            self.population = new_pop
        
        return max(self.population, key=lambda x: x["score"])["text"]
    
    def crossover(self, p1: str, p2: str) -> str:
        w1, w2 = p1.split(), p2.split()
        point = random.randint(1, min(len(w1), len(w2))-1)
        return " ".join(w1[:point] + w2[point:])
    
    def mutate(self, text: str) -> str:
        mutations = [
            lambda t: t + " Be concise.",
            lambda t: "Step by step: " + t,
            lambda t: t.replace("please", ""),
        ]
        return random.choice(mutations)(text)
```

## Best Practices

| Practice | Valor Típico |
|----------|-------------|
| Population size | 20-100 |
| Mutation rate | 0.1-0.2 |
| Crossover rate | 0.7-0.8 |
| Tournament size | 3-5 |
| Elitism | Top 10% |

## Recursos Relacionados

- `knowledge/chuletas/GENETIC_ALGORITHMS_AI_OPTIMIZATION.md`
- `knowledge/chuletas/DSPY_PROMPT_OPTIMIZATION.md`
