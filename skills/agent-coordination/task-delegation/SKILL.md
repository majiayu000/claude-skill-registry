---
name: task-delegation
description: Task delegation patterns for multi-agent systems - hierarchical, parallel, and reactive delegation.
trigger: delegate OR assign task OR multi-agent OR worker OR orchestrator
scope: global
---

# Skill: Task Delegation

## Contexto

Patrones para delegar tareas entre agentes o sistemas, manteniendo tracking y coordinación.

## Cuándo Usar

- Sistemas multi-agente
- Orquestador que delega a workers
- Tareas paralelas independientes
- Escalamiento a Jules u otros agentes

## Patrones de Delegación

### 1. Hierarchical (Manager → Workers)
```python
class HierarchicalDelegator:
    """Manager que delega a workers especializados."""
    
    def __init__(self, workers: dict):
        self.workers = workers  # {"research": Agent, "code": Agent}
    
    def delegate(self, task: dict) -> dict:
        worker_type = self.select_worker(task)
        worker = self.workers[worker_type]
        return worker.execute(task)
    
    def select_worker(self, task: dict) -> str:
        if "research" in task["type"]:
            return "research"
        elif "code" in task["type"]:
            return "code"
        return "general"
```

### 2. Parallel (Fan-out)
```python
import asyncio

class ParallelDelegator:
    """Delegar múltiples tareas en paralelo."""
    
    async def delegate_all(self, tasks: list, workers: list) -> list:
        async def run_task(worker, task):
            return await worker.execute(task)
        
        results = await asyncio.gather(*[
            run_task(w, t) for w, t in zip(workers, tasks)
        ])
        return results
```

### 3. Reactive (Event-driven)
```python
class ReactiveDelegator:
    """Delegar basado en eventos."""
    
    def __init__(self):
        self.handlers = {}
    
    def register(self, event_type: str, handler):
        self.handlers[event_type] = handler
    
    def emit(self, event: dict):
        handler = self.handlers.get(event["type"])
        if handler:
            return handler(event["data"])
        raise ValueError(f"No handler for {event['type']}")
```

## Procedimiento de Delegación

### Paso 1: Evaluar Complejidad
```python
def should_delegate(task: dict) -> bool:
    complexity = estimate_complexity(task)
    return complexity > MY_THRESHOLD or task["requires_special_skill"]
```

### Paso 2: Seleccionar Delegado
```python
DELEGATION_MAP = {
    "deep_research": "jules",
    "code_review": "code_reviewer",
    "ui_automation": "raphael",
    "knowledge_sync": "gentleman",
}

def select_delegate(task_type: str) -> str:
    return DELEGATION_MAP.get(task_type, "self")
```

### Paso 3: Preparar Handoff
```python
def prepare_handoff(task: dict, delegate: str) -> dict:
    return {
        "task": task,
        "context": gather_context(task),
        "constraints": get_constraints(delegate),
        "callback": my_callback_endpoint,
    }
```

### Paso 4: Ejecutar y Monitorear
```python
def delegate_and_monitor(task: dict, delegate: str):
    handoff = prepare_handoff(task, delegate)
    job_id = send_to_delegate(delegate, handoff)
    
    while not is_complete(job_id):
        status = check_status(job_id)
        if status == "blocked":
            intervene(job_id)
        time.sleep(5)
    
    return get_result(job_id)
```

## Para el Hive

```python
class HiveDelegator:
    """Delegación dentro del Hive Corp."""
    
    AGENTS = {
        "gentleman": "Knowledge, research, lateralization",
        "raphael": "UI automation, Orquestator",
        "jules": "Deep research, complex refactors",
    }
    
    def delegate_to(self, agent: str, task: str, context: str):
        """Delegar tarea a otro agente del Hive."""
        sync_file = f"knowledge_sync/CURRENT_TO_{agent.upper()}.md"
        
        message = f"""
# Task Delegation
> From: {self.name}
> To: {agent}
> Timestamp: {datetime.now().isoformat()}

## Task
{task}

## Context
{context}

## Expected Output
Respond in `{agent.upper()}_TO_CURRENT.md`
"""
        Path(sync_file).write_text(message)
        print(f"📤 Delegated to {agent}")
```

### 4. Dynamic Slot Routing
Delegar tareas basado en la disponibilidad de "slots" de procesamiento para evitar saturación.

```python
class SlotDelegator:
    def __init__(self, agent_slots: dict):
        self.slots = agent_slots  # {"raphael": 2, "jules": 1}
    
    def can_delegate(self, agent: str) -> bool:
        return self.slots.get(agent, 0) > 0
    
    def occupy_slot(self, agent: str):
        self.slots[agent] -= 1
        
    def release_slot(self, agent: str):
        self.slots[agent] += 1
```

### 5. Confidence-Based Delegation
Delegar solo si la confianza local es menor a un umbral, o si un especialista tiene mayor confianza proyectada.

```python
def check_delegation_need(task, local_confidence):
    if local_confidence < 0.6:
        # Escalar a especialista (Jules)
        return "jules"
    return "self"
```

## Best Practices

| Practice | Descripción |
|----------|-------------|
| **Clear handoff** | Contexto completo al delegar |
| **Timeout** | Siempre definir timeout |
| **Fallback** | Plan B si delegado falla |
| **Tracking** | Registrar estado de delegación |
| **Callback** | Definir cómo recibir resultado |

## Recursos Relacionados

- `knowledge/chuletas/AGENT_ORCHESTRATION_PATTERNS.md`
- `knowledge/protocols/PROTOCOL_NEURAL_LINK_BROADCAST.md`
- `skills/lateralize-projects/SKILL.md`
