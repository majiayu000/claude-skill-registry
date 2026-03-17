---
name: ai-agent-orchestrator
description: Эксперт по оркестрации AI агентов. Используй для multi-agent systems, agent coordination, task delegation и agent workflows.
---

# AI Agent Orchestrator Expert

Эксперт по проектированию и реализации многоагентных систем.

## Основные принципы

### Иерархия агентов
- **Оркестратор**: Главный координатор, делегирует задачи
- **Специализированные агенты**: Для конкретных доменов (исследования, анализ, код)
- **Утилитарные агенты**: Вспомогательные функции (валидация, форматирование)
- **Мониторинг**: Здоровье системы и обработка ошибок

## Паттерны архитектуры

### Hub and Spoke
```python
class OrchestratorAgent:
    def __init__(self):
        self.agents = {
            'researcher': ResearchAgent(),
            'analyzer': AnalysisAgent(),
            'writer': WritingAgent(),
            'validator': ValidationAgent()
        }

    async def orchestrate_task(self, task):
        subtasks = self.decompose_task(task)

        results = []
        for subtask in subtasks:
            agent_type = self.route_task(subtask)
            result = await self.agents[agent_type].execute(subtask)
            results.append(result)

        return self.synthesize_results(results)
```

### Pipeline Pattern
```python
class AgentPipeline:
    def __init__(self):
        self.stages = [
            DataIngestionAgent(),
            ProcessingAgent(),
            AnalysisAgent(),
            OutputAgent()
        ]

    async def execute_pipeline(self, input_data):
        data = input_data
        for stage in self.stages:
            try:
                data = await stage.process(data)
            except Exception as e:
                return await self.handle_pipeline_error(stage, e, data)
        return data
```

## Маршрутизация задач

```python
class TaskRouter:
    def __init__(self):
        self.agent_capabilities = {
            'code_analysis': ['python', 'javascript', 'sql'],
            'research': ['web_search', 'document_analysis'],
            'writing': ['technical', 'creative', 'business']
        }
        self.agent_load = {}

    def route_task(self, task):
        required_skills = self.extract_skills(task)

        capable_agents = [
            agent_id for agent_id, skills in self.agent_capabilities.items()
            if self.has_required_skills(skills, required_skills)
        ]

        return self.select_least_loaded_agent(capable_agents)
```

## Межагентная коммуникация

```python
@dataclass
class AgentMessage:
    sender_id: str
    receiver_id: str
    message_type: MessageType
    payload: Dict[str, Any]
    correlation_id: str
    timestamp: float
    priority: int = 5

class MessageBus:
    async def send_message(self, message: AgentMessage):
        await self.validate_message(message)
        await self.route_message(message)
        await self.log_message(message)
```

## Обработка ошибок

### Circuit Breaker
```python
class AgentCircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.state = 'CLOSED'

    async def call_agent(self, agent, task):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'HALF_OPEN'
            else:
                raise CircuitBreakerOpenError()

        try:
            result = await agent.execute(task)
            if self.state == 'HALF_OPEN':
                self.reset()
            return result
        except Exception as e:
            self.record_failure()
            raise
```

### Graceful Degradation
```python
class ResilientOrchestrator:
    def __init__(self):
        self.agent_priorities = {
            'primary': ['gpt-4', 'claude-3'],
            'fallback': ['gpt-3.5', 'local-model'],
            'emergency': ['rule-based-agent']
        }

    async def execute_with_fallback(self, task):
        for tier in ['primary', 'fallback', 'emergency']:
            for agent_id in self.agent_priorities[tier]:
                try:
                    if await self.is_agent_healthy(agent_id):
                        return await self.execute_on_agent(agent_id, task)
                except Exception:
                    continue
        raise AllAgentsFailedError()
```

## Лучшие практики

- Реализуйте комплексное логирование с correlation ID
- Отслеживайте метрики производительности агентов
- Используйте распределенную трассировку для сложных workflows
- Валидируйте всю межагентную коммуникацию
- Проектируйте агентов как stateless когда возможно
- Используйте очереди сообщений для развязки
