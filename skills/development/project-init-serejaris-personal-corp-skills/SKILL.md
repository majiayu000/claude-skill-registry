---
name: project-init
description: Use when setting up a new project for AI-agent-driven management, generating OKR, connecting GitHub as a command center, or when user says "init project", "настрой проект", "set up my project", "initialize", "okr setup", "оформи okr". First skill in the Personal Corp framework.
---

# Project Init

Разовая настройка проекта под AI-агентское управление. Skill идёт через guided интервью, проверяет что уже существует, не перезаписывает чужое, создаёт только недостающее.

## Phase 0 — Меню настройки (ПЕРВОЕ действие)

Skill начинает с меню. Дождись явного выбора пользователя — никаких действий до этого.

Покажи пользователю:

```
Что настраиваем? Отметь нужное:

☐ 1. Локальные файлы — tasks.md · okr.md · decisions.md · AGENTS.md или CLAUDE.md (config block)
☐ 2. Настройка GitHub — Project + labels + список репо

«всё» = обе опции
```

Если пользователь выбрал «всё» или «1, 2» — запустить обе ветки по порядку (сначала 1, потом 2). Если выбрал только одну — пропустить вторую полностью на всех фазах.

**Не действуй пока ответа нет.** Это первое и единственное действие Phase 0.

## Phase 1 — Что уже есть (verify, только для выбранного)

Цель: до интервью узнать что existing, чтобы не задавать лишних вопросов и не overwrite'ить чужое.

### Если выбрана опция 1 — Локальные файлы

```bash
# Базовая папка проекта (стандарт: 0_hq/, но может быть любой)
ls -la 0_hq/ 2>/dev/null || echo "0_hq нет"

# Канонические файлы
for f in tasks.md okr.md decisions.md; do
  if [ -f 0_hq/$f ]; then echo "✓ 0_hq/$f"; else echo "— нет 0_hq/$f"; fi
done

# AGENTS.md / CLAUDE.md — для config block
# Используем тот что existing. Если оба есть — primary тот что не симлинк.
# Если ни одного — спросим в Phase 2 какой создать (по типу агента).
for f in AGENTS.md CLAUDE.md; do
  if [ -L 0_hq/$f ]; then echo "↪ 0_hq/$f → $(readlink 0_hq/$f)"
  elif [ -f 0_hq/$f ]; then echo "✓ 0_hq/$f ($(wc -l < 0_hq/$f) строк)"
  else echo "— нет 0_hq/$f"
  fi
done

# Если AGENTS.md или CLAUDE.md существует — есть ли уже config block?
grep -lA 5 "Agent Operations Config" 0_hq/AGENTS.md 0_hq/CLAUDE.md 2>/dev/null

# Если okr.md существует — какой период?
head -10 0_hq/okr.md 2>/dev/null
```

Записать в session: что уже existing, что отсутствует. На следующих фазах задавать вопросы только про missing.

### Если выбрана опция 2 — GitHub

```bash
# Какой github username?
gh api user --jq '.login'

# Существующие projects пользователя
gh project list --owner <username>

# Существующие репо
gh repo list <username> --limit 30 --json name,description

# Если знаем репо проекта — существующие labels
for repo in <repos>; do
  gh label list -R $repo --limit 50 | grep -iE "retro|epic|backlog|^W[0-9]"
done
```

Записать: есть ли подходящий Project, какие labels уже созданы, какие репо в scope.

## Phase 2 — Интервью (по одному вопросу, только под gap)

Правила:
- **Один вопрос за раз** — не overwhelm
- **Не спрашивать про existing** — если файл/конфиг уже есть, в интервью пропустить
- **Записывать каждый ответ сразу** — не копи в голове

### Если выбрана опция 1 — Локальные файлы

#### 1.1 Базовая папка проекта

Только если папки нет.

> «В какой папке держать канонические файлы? По умолчанию `0_hq/`.»

#### 1.2 Контекст бизнеса

Только если ни `AGENTS.md`, ни `CLAUDE.md` нет, или ни в одном из них нет config block'а.

> «Чем занимаешься? Тип бизнеса, solo или с командой?»
> «Какие продукты/услуги продаёшь? Цены, где они живут (лендинг, бот, и т.д.)»

Если ни один из файлов не существует, дополнительно спросить:

> «Какой агент основной — Claude Code или Codex/другой? От этого зависит имя файла: `CLAUDE.md` для Claude Code, `AGENTS.md` для универсального. Можно создать оба и связать симлинком — но обычно один.»

#### 1.3 OKR / North Star (только если `okr.md` отсутствует или период устарел)

Если файл есть и период current — пропустить, только перепривязать в config.

##### 1.3.a — Период и North Star

> «На какой горизонт ставим цели? (Q2 = квартал / H2 = полугодие / 2026 = год)»
> «Сформулируй North Star одним предложением: к концу периода у тебя/нас будет ___».

Anti-pattern: если ответ начинается с «увеличить X на Y%» — это KR, не North Star. Уточни: «А что у тебя будет когда X вырастет на Y%? Это и есть North Star».

##### 1.3.b — Objectives (1-3 на период)

> «Какие 1-3 крупных направления должны двигаться чтобы North Star стал реальностью?»

Спрашивать по одному. Per O ещё:
- Название (короткое — 3-7 слов)
- **Why** одно предложение мотивации

Anti-pattern: 4+ Objectives на квартал для founder-of-one. STOP, попросить сократить до топ-3.

##### 1.3.c — Key Results (2-4 на каждый Objective)

Per O спросить 2-4 KR. Per KR:

> «Как поймём что O двигается? (a) к дате X есть Y — binary, или (b) метрика Z достигла N — численное»
> «Где это будет measure'иться? Конкретный путь — файл, sales.db query, GitHub issue, dashboard».

Anti-pattern: **KR без source-of-truth pointer**. STOP, спросить «где будем мерить?». Без pointer'а KR превратится в воздух.

##### 1.3.d — Guard rails (опционально)

> «Какие метрики хочешь мониторить как guard rails — не достигать, а держать в норме? Например "выручка/неделя ≥ $X" или "доля исходящих ≥ N в неделю". Это защита от Goodhart's law: KR можно загейминговать, guard rails ловят перекос.»

Можно пропустить если пользователь не готов.

##### 1.3.e — Cadence

> «Когда ревьюим OKR? По умолчанию — в `weekly-retro` Phase 1.5 (еженедельно прогресс) + monthly snapshot. Подходит?»

### Если выбрана опция 2 — GitHub

#### 2.1 Репо

Если репо ещё не определены.

> «Какие репо относятся к этому проекту? Возьми 5-7 ключевых для weekly operations, остальные подключим позже. Категоризировать: execution / growth / infrastructure.»

Для каждого репо спросить категорию (одна из трёх).

#### 2.2 Project

Если Project уже existing — спросить:
> «Использовать `<Project N>` (нашли в gh project list) или создать новый?»

Если нет:
> «Название Project'а? Например "Personal Corp" или "<Brand> ops".»

#### 2.3 Routing

> «Какие задачи идут в какой репо? Pattern → repo. Например: "bot, broadcast" → hsl-mozg, "lessons" → teach-vibecoding.»

Минимум 3 routing rule. Можно дополнять позже.

## Phase 3 — Создание (per selected only)

### Опция 1 — Локальные файлы

#### 3.1.a Создать структуру

```bash
mkdir -p <project-folder>/retros/

# Stubs — НЕ overwrite existing
[ ! -f <project-folder>/tasks.md ] && touch <project-folder>/tasks.md
[ ! -f <project-folder>/decisions.md ] && touch <project-folder>/decisions.md

# AGENTS.md / CLAUDE.md — файл инструкций для агентов.
# Логика: используем тот что existing. Если ни одного — создаём по выбору пользователя из 1.2.
# Симлинк второго на первый — опционально, если пользователь явно попросил.
AGENT_FILE="<выбран в 1.2 или existing из Phase 1>"  # AGENTS.md либо CLAUDE.md
[ ! -f <project-folder>/$AGENT_FILE ] && touch <project-folder>/$AGENT_FILE
```

Файлы заполнить минимальными templates (не фабриковать данные).

#### 3.1.b tasks.md template

```markdown
# Задачи

Обновлено: <date>
Протухает после: <date + 7 дней>

## Сейчас (W{NN})

| Приоритет | Работа | Почему | Источник |
|---:|---|---|---|
| 1 | ... | ... | ... |

## Решения недели

(заполняется в weekly-planning)

## Не сейчас

- ...
```

#### 3.1.c okr.md template (с user input из 1.4)

```markdown
# OKR

Обновлено: <date>
Период: <Q2 2026 / H2 2026 / etc>

## North Star

<aspirational sentence из 1.3.a>

## Objectives

### O1: <название из 1.3.b>

**Why:** <motivation>

**Key Results:**
- **KR1.1** — <формулировка из 1.3.c> · source: <path/query/issue>
- **KR1.2** — <...> · source: <...>

### O2: <...>

## Guard rails

(из 1.3.d, если есть)
- <metric>: floor ≥ X · source: <...>
- <metric>: ceiling ≤ Y · source: <...>

## Cadence

Review: <из 1.3.e>

---

## История

<append-only когда период закроется>
```

Anti-pattern: создавать okr.md без user input по 1.4. Если пользователь скипнул — НЕ генерировать пустой файл с placeholder'ами. Показать что генерация пропущена.

#### 3.1.d Config block

Записываем в файл из переменной `$AGENT_FILE` (AGENTS.md или CLAUDE.md). Если файл существует с контентом — **ADD блок в конец, НЕ overwrite**.

```markdown
## Agent Operations Config

### Канонические файлы
canonical:
  tasks: <path>/tasks.md
  okr: <path>/okr.md
  decisions: <path>/decisions.md

### Weekly cadence
weekly_cadence: <день недели — главный delivery>
retro_log_path: <path>/retros/

### Repos (если выбрана опция 2)
repos:
  - owner/repo-1   # execution — что делает
  - owner/repo-2   # growth — что делает
  - owner/repo-3   # infrastructure — что делает

### GitHub Project (если выбрана опция 2)
project_id: <N>
owner: <github-username>

### Task routing (если собирали в 2.3)
routing:
  - pattern: "bot, broadcast"
    repo: owner/bot-repo
  - pattern: "content, lessons"
    repo: owner/content-repo
```

### Опция 2 — Настройка GitHub

#### 3.2.a Project (если новый)

```bash
gh project create --owner <owner> --title "<name>"
```

Затем добавить custom fields через UI или API:
- **Status** (single-select): Todo / In Progress / Review / Done
- **Deadline** (date)
- **Week** (single-select): W1, W2, ... W52 — для retro/planning

#### 3.2.b Labels в каждом репо

```bash
for repo in <repos>; do
  gh label create "retro:W00" -R $repo --color "D4C5F9" \
    --description "Шаблон лейбла недельного ретро"
  gh label create "epic" -R $repo --color "5319e7" \
    --description "Длинный трек, не недельная задача"
  gh label create "backlog" -R $repo --color "ededed" \
    --description "Отложено вне retro-цикла"
done
```

Текущая неделя ретро (`retro:W{NN}`) создаётся отдельно при первом ретро через `weekly-retro` skill.

#### 3.2.c Repos в config block

Если опция 1 не выбрана — создать минимальный agent file (AGENTS.md или CLAUDE.md по типу agents) только с repos + project + routing. Если опция 1 выбрана — этот блок уже создан в 3.1.d, просто заполнить repos / project / routing.

## Phase 4 — Проверка

### Опция 1

```bash
# Канонические файлы существуют
ls <path>/tasks.md <path>/okr.md <path>/decisions.md
ls -l <path>/AGENTS.md <path>/CLAUDE.md 2>/dev/null   # один или оба, симлинк показывает →

# Config block (в любом из двух)
grep -lA 5 "Agent Operations Config" <path>/AGENTS.md <path>/CLAUDE.md 2>/dev/null

# OKR sanity-check
head -25 <path>/okr.md
```

Показать пользователю результаты. Если что-то отсутствует — сообщить и предложить дозаполнить.

### Опция 2

```bash
# Project существует
gh project list --owner <owner> | grep "<project-name>"

# Labels в каждом репо
for repo in <repos>; do
  echo "=== $repo ==="
  gh label list -R $repo | grep -E "retro|epic|backlog"
done
```

## Что дальше

После init работают:

- **`manager`** — синк session work в GitHub issues (требует опцию 2)
- **`weekly-retro`** — структурированное ретро (требует опцию 1, опционально 2)
- **`weekly-planning`** — план недели (требует опцию 1)
- **`pm-metrics`** — ревью метрик с OKR alignment check Step 7 валидирует то что сгенерировано в 1.4

Каждый skill читает config block из CLAUDE.md — реconfigure не нужен.

## Red flags — STOP

- **Existing AGENTS.md или CLAUDE.md с контентом** → ADD config block в конец, не overwrite
- **Существуют ОБА файла как разные regular files** (не симлинк) → STOP, спросить какой primary; второй можно оставить или сделать симлинком на первый
- **Existing GitHub Project** → спросить «использовать или создать новый?»
- **Existing okr.md с current period** → спросить «обновить или импортировать как есть?»; не overwrite молча
- **User не использует GitHub** → опция 2 пропускается, локальные файлы работают самостоятельно
- **KR без source-of-truth pointer** (path / sales.db query / issue) → STOP, спросить «где будем мерить?»
- **5+ Objectives на квартал** → STOP, founder-of-one fit = 1-3 O. Попросить сократить
- **North Star = «увеличить X на Y%»** → это KR, не NSM. Уточнить «а что у тебя будет когда X вырастет?»
- **Запуск Phase 1+ без явного ответа на Phase 0 меню** → STOP, дождаться выбора

## Anti-patterns

- **Спросить всё сразу** — переусложнение, пользователь теряется. Один вопрос за раз
- **Overwrite существующих файлов** — silent data loss. Always check + append/extend
- **Auto-generate okr.md с placeholder'ами** — фабрикация ради «полного artefact'а». Лучше пропустить опцию OKR
- **Создавать labels во ВСЕХ репо пользователя** — overkill. Только в указанных в опции 2 репо
- **Игнорировать ответ на меню** — Phase 0 единственное действие до выбора, не запускать Phase 1 «на всякий случай»

## Частые вопросы

**«У меня 20+ репо»** — выбери 5-7 которые матерят для weekly operations. Остальные подключим позже отдельным запуском skill'а.

**«Структура проекта messy»** — нормально. Init создаёт чистый layer сверху, реорганизовывать существующее не нужно.

**«У меня уже есть OKR в Google Doc»** — в опции 1.4 выбери «уже есть, импортирую» — skill попросит paste содержимое и сохранит в `okr.md` с минимальной нормализацией.

**«Можно запустить skill второй раз чтобы добавить только OKR?»** — да. Phase 0 меню → выбрать только опцию 1 → Phase 1 verify покажет что existing → Phase 2 спросит только про OKR (остальное skip) → Phase 3 создаст только okr.md.

## Связанные skills

- `weekly-retro` — заполняет outcomes scorecard на базе KR из okr.md
- `weekly-planning` — превращает KR в weekly outcomes
- `pm-metrics` — Step 7 валидирует OKR alignment, Step 2 декомпозирует North Star → L1 → L2
- `manager` — синкает session work в GitHub issues, использует repos / labels из config
