---
name: idea-validation
description: |
  Validate idea and create detailed PRD. Saves docs/PRD.md to project.
  Use when: user describes an app idea, wants to create something new.
  Triggers: "I want to build", "create app", "make website", "build MVP",
  "хочу создать", "сделать приложение".
---

# Idea Validation

Understand what the user wants, ask the right questions based on project type, and create a comprehensive PRD.

## Phase A: Discovery

### Step 1: Identify Project Type

First, determine project type from user's description or ask directly:

```
question: "Какой тип проекта?"
header: "Type"
options:
  - label: "Web App (SaaS)"
    description: "Веб-приложение с UI"
  - label: "Telegram Bot"
    description: "Бот для Telegram"
  - label: "REST/GraphQL API"
    description: "Backend сервис"
  - label: "CLI Tool"
    description: "Консольная утилита"
# Other types via "Other": Mobile App, Discord Bot, Library/SDK, Data Pipeline, Browser Extension
```

### Step 2: Brainstorm Offer

Based on complexity, offer brainstorming:

| Signal | Recommendation |
|--------|----------------|
| Description < 10 words | Suggest brainstorm |
| Complex type (Telegram, Mobile, Data) | Suggest brainstorm |
| Detailed description | Suggest skip |
| User says "быстро"/"simple" | Auto-skip |

```
question: "Хочешь уточнить идею через brainstorm?"
header: "Brainstorm"
options:
  - label: "Да, давай уточним"
    description: "Детальные вопросы → полный PRD"
  - label: "Нет, идея понятна"
    description: "Быстрые вопросы → минимальный PRD"
  - label: "Частично"
    description: "Ключевые вопросы только"
```

### Step 3: Core Questions (всегда)

**Q1: Problem**
```
question: "Какую проблему это решает?"
header: "Problem"
options: [3-4 contextual options based on idea]
```

**Q2: Target User**
```
question: "Кто будет этим пользоваться?"
header: "User"
options:
  - label: "Для себя"
    description: "Личное использование"
  - label: "AI агенты"
    description: "Через API/MCP"
  - label: "Команда/Бизнес"
    description: "Совместная работа"
  - label: "Публичный сервис"
    description: "Широкая аудитория"
```

**Q3: Core Action**
```
question: "Что первое делает пользователь?"
header: "Action"
options: [3-4 contextual options]
```

**Q4: Success**
```
question: "Как понять что сработало?"
header: "Success"
options: [3-4 contextual options]
```

### Step 4: Type-Specific Questions (если brainstorm)

#### For Telegram Bot:
```
question: "Как бот взаимодействует с пользователем?"
header: "Interaction"
options:
  - label: "Команды (/start, /help)"
    description: "Структурированное взаимодействие"
  - label: "Диалог"
    description: "Свободное общение"
  - label: "Inline режим"
    description: "Поиск из любого чата"
  - label: "Кнопки/меню"
    description: "Визуальная навигация"

question: "Нужна ли база данных?"
header: "Storage"
options:
  - label: "Да, SQLite"
    description: "Простое хранение"
  - label: "Да, PostgreSQL"
    description: "Масштабируемое"
  - label: "Нет"
    description: "Stateless бот"

question: "Внешние интеграции?"
header: "APIs"
multiSelect: true
options:
  - label: "OpenAI/LLM"
  - label: "Payment (Stripe/YooKassa)"
  - label: "External APIs"
  - label: "Нет интеграций"
```

#### For Web App (SaaS):
```
question: "Нужна ли авторизация?"
header: "Auth"
options:
  - label: "Email + пароль"
  - label: "OAuth (Google/GitHub)"
  - label: "Magic link"
  - label: "Не нужна"

question: "Realtime функции?"
header: "Realtime"
options:
  - label: "Да, WebSocket"
  - label: "Да, Server-Sent Events"
  - label: "Нет, обычный HTTP"
```

#### For REST API:
```
question: "Для кого API?"
header: "Audience"
options:
  - label: "Internal"
    description: "Для своих фронтов"
  - label: "Public"
    description: "Для внешних разработчиков"
  - label: "Partner"
    description: "Для партнёров"

question: "Аутентификация?"
header: "Auth"
options:
  - label: "API Key"
  - label: "JWT"
  - label: "OAuth2"
  - label: "Без авторизации"
```

#### For CLI Tool:
```
question: "Как запускается?"
header: "Execution"
options:
  - label: "Одна команда"
    description: "cli do-something"
  - label: "Субкоманды"
    description: "cli cmd1, cli cmd2"
  - label: "Интерактивный"
    description: "Диалог с пользователем"

question: "Вывод?"
header: "Output"
options:
  - label: "Текст"
  - label: "JSON"
  - label: "Файлы"
  - label: "Табличный"
```

### Step 5: Constraints (если brainstorm full)

```
question: "Есть ли ограничения?"
header: "Constraints"
multiSelect: true
options:
  - label: "Бесплатные сервисы only"
    description: "Без платных зависимостей"
  - label: "Быстрый MVP"
    description: "Дедлайн < 1 недели"
  - label: "Scale 1000+ пользователей"
    description: "Нужна масштабируемость"
  - label: "Нет ограничений"
```

## Phase B: PRD Generation

### Minimal PRD (простые проекты, skip brainstorm)

```markdown
# {Name} PRD

## Problem
{One sentence from Q1}

## User
{From Q2}

## Core Features
- [ ] {Feature from Q3}
- [ ] {Feature 2}
- [ ] {Feature 3}

## Success Metric
{From Q4}

## Tech Stack
{Based on project type}

---
Generated: {date}
Status: Draft
```

### Standard PRD (средние проекты, partial brainstorm)

```markdown
# {Name} PRD

## Problem
{One sentence from Q1}

## User
{From Q2 with context}

## Product Type
{Type} — {type-specific details}

## Core Features (MVP)
1. **{Feature Name}**
   - User story: As a {user}, I want to {action} so that {benefit}
   - Acceptance criteria:
     - [ ] {Criterion 1}
     - [ ] {Criterion 2}

2. **{Feature 2}**
   ...

## Non-Goals
- {What we're NOT building}

## Success Metrics
- **Primary:** {From Q4}

## Tech Stack
{Based on project type and answers}

## Dependencies
- {External APIs if any}
- {Third-party services}

---
Generated: {date}
Status: Draft
```

### Full PRD (сложные проекты, full brainstorm)

```markdown
# {Name} — Product Requirements Document

## Overview
{Brief description of what we're building and why}

## Problem Statement
{Detailed problem from Q1 with context}

## Target Users
- **Primary persona:** {From Q2}
- **Use context:** {When/where they use this}
- **User volume:** {Expected scale}

## Product Type
{Type}

### Type-Specific Requirements
{Section content varies by project type - from type-specific questions}

## Core Features (MVP)

### Feature 1: {Name}
- **User story:** As a {user}, I want to {action} so that {benefit}
- **Acceptance criteria:**
  - [ ] {Criterion 1}
  - [ ] {Criterion 2}
  - [ ] {Criterion 3}
- **Priority:** P0

### Feature 2: {Name}
...

## Non-Goals (Explicitly Out of Scope)
- Not doing {X} because {Y}
- Not doing {Z} in MVP, maybe later

## Success Metrics
- **Primary:** {From Q4}
- **Secondary:** {Supporting metrics}

## Technical Constraints
- **Hosting:** {Where it runs}
- **Budget:** {Free tier / paid services}
- **Performance:** {Latency/throughput requirements}
- **Security:** {Auth, encryption, compliance}

## Dependencies
- **External APIs:** {list}
- **Third-party services:** {list}

## Risks & Mitigations
- Risk 1 → Mitigation
- Risk 2 → Mitigation

---
Generated: {date}
Status: Draft
```

## PRD Selection Logic

| Project Type | Default PRD |
|--------------|-------------|
| CLI Tool | Minimal |
| Simple API | Minimal |
| Web App | Standard |
| Telegram Bot | Standard |
| Mobile App | Full |
| Data Pipeline | Full |
| SaaS with Auth | Full |

Override:
- User chose "skip brainstorm" → Minimal
- User chose "partial" → Standard
- User chose "full brainstorm" → Full

## After PRD Creation

1. **Validate PRD**:
   ```bash
   python3 scripts/validate_prd.py --path docs/PRD.md
   ```

2. **Report to user**:
   ```
   PRD saved to docs/PRD.md

   Summary:
   - Type: {project type}
   - Features: {count}
   - Complexity: {minimal/standard/full}

   Next: Task[rust-project-init] or Task[python-project-init]
   ```

## Rules

- **Ask type first** — determines question flow
- **One question at a time** — don't overwhelm
- **Adaptive depth** — simple projects get simple PRD
- **No guessing** — if unclear, ask
- **Save PRD.md** — always persist
- **Validate** — run validate_prd.py after creation
