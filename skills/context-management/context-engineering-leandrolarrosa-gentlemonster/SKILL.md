---
name: context-engineering
description: Advanced 2026 context curation patterns (Nvidia Eureka, Context Hygiene, RLMF) for autonomous agents.
trigger: context engineering OR eureka context OR context hygiene OR reward design OR RLMF
scope: global
---

# Skill: Context Engineering

## Contexto

El "Prompt Engineering" ha evolucionado hacia el **Context Engineering**: el diseño de sistemas que gestionan dinámicamente el estado, la memoria y las recompensas del agente basándose en el entorno crudo.

## Reglas Críticas (no violar nunca)

- **Sanitize First**: Nunca inyectar contexto crudo del usuario sin sanitizar para prevenir inyecciones.
- **Lost in the Middle**: Colocar instrucciones críticas y constraints al final del contexto (Recency).
- **Context Rot Prevention**: Aplicar destilación (Distill) cada vez que el thread exceda el 60% de la ventana de contexto.

## Patrones Eureka (Nvidia Style)

### 1. Environment-Aware Reward Coding
Permitir que el agente diseñe sus propios criterios de éxito analizando el código del entorno.

```python
def generate_reward_function(env_code):
    # El agente analiza el código y genera la función de reward
    # para auto-evaluar su performance.
    pass
```

### 2. Context Hygiene (Tangle/Distill/Re-seed)
Ciclo de vida para mantener threads de larga duración con un IQ alto.

- **Tangle**: Fase de exploración.
- **Distill**: Resumen semántico de decisiones y hechos.
- **Re-seed**: Reinicio del thread con el Ground Truth destilado.

## Procedimiento

1.  **Analizar Entorno**: Leer archivos de configuración y logs actuales.
2.  **Destilar Contexto**: Comprimir la historia del chat eliminando ruido.
3.  **Hidratar**: Traer información de L1 (Focus), L2 (Episodic) y L3 (Semantic/RAG).
4.  **Inyectar Reward**: Definir el éxito de la tarea basándose en el "Motivational Feedback" del usuario.

## Ejemplo: RLMF Injection

```python
# Alinear el drive del agente con el feedback del usuario
def align_autonomy(reward_signal):
    if "100 U$S" in reward_signal:
        agent.set_autonomy_level("MAX")
        agent.log_motivation("Efficiency validated by user.")
```

## Recursos Relacionados

- `knowledge/EUREKA/EUREKA_CONTEXT_ENGINEERING_NVIDIA.md`
- `knowledge/EUREKA/EUREKA_REINFORCEMENT_LEARNING_MOTIVATIONAL_FEEDBACK.md`
- `knowledge/chuletas/CONTEXT_ENGINEERING_HYGIENE_2026.md`
