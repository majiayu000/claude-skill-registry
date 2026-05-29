---
name: conversational-ai-flow
description: Эксперт conversational AI. Используй для chatbot flows, dialog design, NLU intents и conversational UX.
---

# Conversational AI Flow Expert

Эксперт по проектированию и реализации потоков разговорного ИИ.

## Основные принципы дизайна

### Управление состоянием
```python
class ConversationState:
    def __init__(self):
        self.current_intent = None
        self.entities = {}
        self.conversation_history = []
        self.flow_position = "start"
        self.confidence_threshold = 0.7

    def update_context(self, user_input, intent, entities):
        self.conversation_history.append({
            "user_input": user_input,
            "intent": intent,
            "entities": entities
        })
        self.entities.update(entities)
        self.current_intent = intent
```

## Паттерны архитектуры потоков

### Маршрутизация на основе намерений
```yaml
flows:
  booking_flow:
    entry_conditions:
      - intent: "book_appointment"
    steps:
      - name: "collect_datetime"
        prompt: "When would you like to schedule?"
        validation: "datetime_validator"
      - name: "confirm_booking"
        prompt: "Confirm booking on {datetime}?"
        actions: ["create_booking", "send_confirmation"]

  fallback_flow:
    triggers: ["low_confidence", "unknown_intent"]
    strategy: "clarification_questions"
```

### Паттерн заполнения слотов
```python
def slot_filling_handler(state, required_slots):
    missing_slots = [s for s in required_slots if s not in state.entities]

    if missing_slots:
        return generate_slot_prompt(missing_slots[0], state)

    return proceed_to_next_step(state)
```

## Обработка ошибок и восстановление

### Прогрессивное раскрытие
```python
class ErrorRecovery:
    def handle_misunderstanding(self, state, attempt_count):
        strategies = {
            1: "I didn't quite catch that. Could you rephrase?",
            2: "Let me try differently. Are you looking to: [options]?",
            3: "Let me connect you with a human agent."
        }
        return strategies.get(attempt_count, strategies[3])
```

## Генерация ответов

### Контекстуальные шаблоны
```python
class ResponseGenerator:
    templates = {
        "confirmation": [
            "Got it! {summary}. Is that correct?",
            "Let me confirm: {summary}. Does this look right?"
        ],
        "progress": [
            "Great! We've got {completed}. Next, {next_step}.",
            "Perfect! Just need {remaining} and we're done."
        ]
    }
```

## Мультимодальные ответы

```json
{
  "response_type": "rich",
  "text": "Here are your options:",
  "components": [
    {
      "type": "quick_replies",
      "options": [
        {"title": "Schedule Appointment", "payload": "intent:book"},
        {"title": "Check Status", "payload": "intent:status"}
      ]
    }
  ]
}
```

## Аналитика и оптимизация

```python
def track_flow_metrics(conversation_id, metrics):
    return {
        "completion_rate": metrics.completed / metrics.started,
        "average_turns": metrics.total_turns / metrics.conversations,
        "fallback_rate": metrics.fallbacks / metrics.total_turns,
        "abandonment_points": identify_drop_off_points(conversation_id)
    }
```

## Лучшие практики

- Определите четкую личность и тон бота
- Предвосхищайте потребности пользователей
- Используйте резюме для длинных диалогов
- Тестируйте все пути и edge cases
- Мониторьте реальные разговоры для улучшения
