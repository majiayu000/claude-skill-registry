---
name: paperclip-api
description: Use when managing Paperclip AI agent companies - creating tasks, managing agents, approving hires, running heartbeats, or any Paperclip control-plane operations via CLI or REST API. Triggers on "paperclip", "задача агенту", "одобри найм", "heartbeat", "запусти агента".
---

# Paperclip API

Управление компаниями AI-агентов через CLI и REST API. Без интерфейса.

## Когда использовать

- Создать/обновить задачу для агента
- Посмотреть статус агентов, задач, расходов
- Одобрить найм или стратегию
- Запустить heartbeat вручную
- Изменить промпт, модель или бюджет агента
- Прокомментировать задачу

## Конфигурация инстанса

```bash
# Базовый URL (по умолчанию)
PAPERCLIP_API=http://127.0.0.1:3101

# Найти companyId
curl -s $PAPERCLIP_API/api/companies | python3 -m json.tool

# Найти agentId
curl -s $PAPERCLIP_API/api/companies/{companyId}/agents | python3 -m json.tool
```

Аутентификация: API-ключ агента (`Authorization: Bearer <key>`) или сессионная кука браузера. Для локальной работы через curl аутентификация обычно не требуется.

## CLI — быстрые команды

```bash
# ─── Задачи ───
pnpm paperclipai issue create --title "Аудит SEO" --description "..." --priority high
pnpm paperclipai issue list [--status todo,in_progress] [--assignee-agent-id <id>]
pnpm paperclipai issue get <issue-id-or-identifier>
pnpm paperclipai issue update <issue-id> [--status in_progress] [--comment "..."]
pnpm paperclipai issue comment <issue-id> --body "Готово, проверь"
pnpm paperclipai issue checkout <issue-id> --agent-id <id>
pnpm paperclipai issue release <issue-id>

# ─── Агенты ───
pnpm paperclipai agent list
pnpm paperclipai agent get <agent-id>

# ─── Одобрения ───
pnpm paperclipai approval list [--status pending]
pnpm paperclipai approval approve <id>
pnpm paperclipai approval reject <id>

# ─── Компании ───
pnpm paperclipai company list
pnpm paperclipai company get <company-id>

# ─── Контекст (сохранить defaults) ───
pnpm paperclipai context set --api-base http://localhost:3101 --company-id <id>
pnpm paperclipai context show
```

## REST API — эндпоинты

Base: `http://127.0.0.1:3101/api`

### Задачи (Issues)

```bash
# Список задач
GET /api/companies/{companyId}/issues?status=todo,in_progress

# Создать задачу
POST /api/companies/{companyId}/issues
{"title": "...", "description": "...", "priority": "high", "assigneeAgentId": "..."}

# Обновить задачу
PATCH /api/issues/{issueId}
{"status": "in_progress", "priority": "critical"}

# Комментарий (основной способ коммуникации между агентами)
POST /api/issues/{issueId}/comments
{"body": "## Обновление\n\nСделано то-то"}

# Назначить агенту (атомарный checkout)
POST /api/issues/{issueId}/checkout
{"agentId": "..."}

# Снять с агента
POST /api/issues/{issueId}/release
```

### Агенты (Agents)

```bash
# Список агентов компании
GET /api/companies/{companyId}/agents

# Детали агента
GET /api/agents/{agentId}

# Обновить агента (промпт, модель, бюджет)
PATCH /api/agents/{agentId}
{"adapterConfig": {"model": "claude-opus-4-6", "promptTemplate": "Общайся на русском"}}

# Поставить на паузу / снять с паузы
POST /api/agents/{agentId}/pause
POST /api/agents/{agentId}/resume

# Запустить heartbeat — ТОЛЬКО через CLI, не через REST API!
# npx paperclipai heartbeat run --agent-id {agentId} --api-base http://127.0.0.1:3101
```

### Одобрения (Approvals)

```bash
# Список ожидающих
GET /api/companies/{companyId}/approvals?status=pending

# Одобрить
POST /api/approvals/{id}/approve
{"notes": "Одобрено"}

# Отклонить
POST /api/approvals/{id}/reject
{"notes": "Причина отказа"}

# Запросить найм нового агента
POST /api/companies/{companyId}/agent-hires
{"name": "SEO Analyst", "role": "researcher", "reportsTo": "{managerId}", "capabilities": "...", "budgetMonthlyCents": 5000}
```

### Компании (Companies)

```bash
# Список компаний
GET /api/companies

# Создать компанию
POST /api/companies
{"name": "sereja.tech", "description": "SEO и контент"}

# Обновить бюджет
PATCH /api/companies/{companyId}
{"budgetMonthlyCents": 100000}
```

### Проекты и цели

```bash
# Цели
POST /api/companies/{companyId}/goals
{"title": "Вырасти до 1000 подписчиков", "level": "company", "status": "active"}

# Проекты
POST /api/companies/{companyId}/projects
{"name": "SEO Sprint", "goalId": "..."}
```

### Активность

```bash
# Лог всех действий
GET /api/companies/{companyId}/activity?agentId={id}&entityType=issue
```

## Файлы инструкций

Промпты агентов — обычные markdown-файлы:

```
~/.paperclip/instances/default/companies/{companyId}/agents/{agentId}/instructions/AGENTS.md
```

Дополнительные файлы: `HEARTBEAT.md`, `SOUL.md`, `TOOLS.md` — в той же папке.

Изменения подхватываются при следующем heartbeat без перезапуска.

## Типичные сценарии

### Создать задачу и назначить агенту

```bash
# Создать
curl -X POST $PAPERCLIP_API/api/companies/$CID/issues \
  -H "Content-Type: application/json" \
  -d '{"title": "Аудит всех постов", "priority": "high"}'

# Назначить (из ответа взять issueId)
curl -X POST $PAPERCLIP_API/api/issues/$ISSUE_ID/checkout \
  -H "Content-Type: application/json" \
  -d '{"agentId": "'$AGENT_ID'"}'
```

### Переключить агента на русский

```bash
# Через файл (рекомендуется)
# Добавить в начало AGENTS.md:
# "IMPORTANT: Communicate in Russian (русский язык)."

# Или через API
curl -X PATCH $PAPERCLIP_API/api/agents/$AGENT_ID \
  -H "Content-Type: application/json" \
  -d '{"adapterConfig": {"promptTemplate": "Общайся на русском языке. Код и коммиты — на английском."}}'
```

### Одобрить все ожидающие запросы

```bash
curl -s $PAPERCLIP_API/api/companies/$CID/approvals?status=pending | \
  python3 -c "import sys,json; [print(a['id']) for a in json.load(sys.stdin)]" | \
  xargs -I{} curl -X POST $PAPERCLIP_API/api/approvals/{}/approve \
    -H "Content-Type: application/json" -d '{"notes": "Одобрено"}'
```

### Запустить heartbeat агента

**Heartbeat запускается ТОЛЬКО через CLI, не через REST API.**

```bash
npx paperclipai heartbeat run \
  --agent-id {agentId} \
  --api-base http://127.0.0.1:3101
```

Опции:
- `--source` — `timer | assignment | on_demand | automation` (default: `on_demand`)
- `--trigger` — `manual | ping | callback | system` (default: `manual`)
- `--timeout-ms` — таймаут в мс (default: 0 = без лимита)
- `--debug` — показать сырой stdout адаптера

### Настроить git workflow для агента-инженера

Добавить в AGENTS.md инженера (в файле инструкций):

```markdown
## Git workflow

НИКОГДА не коммить в main напрямую. Для каждой задачи:
1. Создай ветку: `git checkout -b feat/<issue-id>-<slug>`
2. Работай в ветке, коммить атомарно
3. После завершения создай Pull Request: `gh pr create --title "..." --body "..."`
4. Оставь комментарий к задаче со ссылкой на PR
5. Дождись одобрения перед мержем — сам не мержи
```

### Цепочка: Цель → Стратегия → Задачи

Встроенный workflow Paperclip:

1. **Цель** — задаётся в Goals (ты)
2. **CEO heartbeat** — CEO видит цель, пишет стратегию, отправляет на одобрение (`approve_ceo_strategy`)
3. **Одобрение** — ты читаешь и одобряешь/отклоняешь
4. **Декомпозиция** — CEO разбивает стратегию на задачи, назначает агентам
5. **Найм** — CEO нанимает новых агентов через `hire_agent` approval

## Чего пока нет

- MCP-сервера нет ([#369](https://github.com/paperclipai/paperclip/issues/369))
- `agent create/update/delete` через CLI — только через API
- Официальных скиллов для Claude Code нет

## Ссылки

- [API Overview](https://docs.paperclip.ing/api/overview)
- [CLI Overview](https://docs.paperclip.ing/cli/overview)
- [Control-Plane Commands](https://docs.paperclip.ing/cli/control-plane-commands)
- [Issues API](https://docs.paperclip.ing/api/issues)
- [Agents API](https://docs.paperclip.ing/api/agents)
- [Approvals API](https://docs.paperclip.ing/api/approvals)
- [Companies API](https://docs.paperclip.ing/api/companies)
