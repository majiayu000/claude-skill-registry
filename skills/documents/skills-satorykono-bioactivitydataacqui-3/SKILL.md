---
name: documentation-cascade-audit
description: |
  Иерархический каскадный аудит и исправление документации BioETL.
  Оркестратор декомпозирует кодовую базу на сегменты и запускает
  параллельные суб-агенты для исчерпывающего документирования,
  поиска расхождений кода и документации, проверки соответствия,
  идентификации недокументированных решений и автоматического исправления.
  Триггеры:
  - Полный аудит документации проекта
  - Каскадное документирование после крупного рефакторинга
  - Подготовка к релизу (documentation freeze)
  - Обнаружение массового doc drift
---

# Documentation Cascade Audit — Hierarchical Agent System

*Версия: 1.0.0 | Дата: 2026-02-26 | Платформа: Claude Code CLI*

---

## 1. Обзор

**Documentation Cascade Audit** — иерархическая система агентов для исчерпывающего
документирования проекта BioETL с автоматическим масштабированием. Оркестратор
анализирует кодовую базу, декомпозирует её на сегменты, и запускает параллельные
суб-агенты, передавая каждому конкретный scope (архитектурный слой, провайдер,
модуль) и набор типов документов для аудита и/или создания.

### Принцип работы

```text
ORCHESTRATOR (главный агент)
│
├──→ [Phase 1: Reconnaissance]
│    Чтение PROJECT_CONTEXT, RULES.md, agent-memory.md
│    Инвентаризация: файлы, docstrings, docs/, mkdocs.yml
│
├──→ [Phase 2: Decomposition]
│    Формирование сегментов (scope + doc_types)
│    Маршрутизация → N суб-агентов
│
├──→ [Phase 3: Parallel Audit & Fix]  ← автомасштабирование
│    ├── Layer Auditor: domain       (docstrings, API ref, contracts)
│    ├── Layer Auditor: application  (docstrings, pipeline docs, guides)
│    ├── Layer Auditor: infrastructure (docstrings, adapter docs, API ref)
│    ├── Layer Auditor: composition  (docstrings, factory docs, bootstrap)
│    ├── Layer Auditor: interfaces   (docstrings, CLI ref, commands)
│    ├── Provider Auditor: chembl    (pipeline spec, entity docs, schema docs)
│    ├── Provider Auditor: pubchem   (pipeline spec, entity docs)
│    ├── Provider Auditor: uniprot   (pipeline spec, entity docs)
│    ├── Provider Auditor: pubmed    (pipeline spec, entity docs)
│    ├── Provider Auditor: crossref  (pipeline spec, entity docs)
│    ├── Provider Auditor: openalex  (pipeline spec, entity docs)
│    ├── Provider Auditor: semanticscholar (pipeline spec, entity docs)
│    ├── Architecture Auditor        (ADR, arch docs, diagrams, layer docs)
│    ├── Governance Auditor          (RULES.md, glossary, CHANGELOG, mkdocs.yml)
│    └── Cross-Reference Auditor     (links, orphans, navigation, sync)
│
├──→ [Phase 4: Consolidation]
│    Сбор findings от всех суб-агентов
│    Дедупликация, приоритизация, формирование единого отчёта
│
└──→ [Phase 5: Fix Execution]
     Запуск корректирующих суб-агентов по приоритету
     Верификация каждого исправления
```

---

## 2. Использование

```
/documentation-cascade-audit [mode] [scope]
```

**Режимы:**
- `full` — полный каскадный аудит всего проекта (по умолчанию)
- `layers` — только аудит слоёв (docstrings + layer docs)
- `providers` — только аудит провайдеров (сквозная проверка)
- `architecture` — только архитектурная документация (ADR + arch docs)
- `governance` — только governance (RULES, glossary, CHANGELOG, nav)
- `crossref` — только перекрёстные ссылки и навигация
- `fix-only` — только исправления по предыдущему отчёту

**Scope (опционально):**
- `domain`, `application`, `infrastructure`, `composition`, `interfaces` — конкретный слой
- `chembl`, `pubmed`, `crossref`, `openalex`, `pubchem`, `uniprot`, `semanticscholar` — конкретный провайдер
- Без scope — весь проект

**Примеры:**
```
/documentation-cascade-audit                        # полный аудит
/documentation-cascade-audit layers domain          # только domain docstrings
/documentation-cascade-audit providers chembl        # только ChEMBL docs
/documentation-cascade-audit architecture            # только ADR + arch docs
/documentation-cascade-audit governance              # RULES, glossary, nav
/documentation-cascade-audit crossref                # broken links, orphans
/documentation-cascade-audit fix-only                # применить fixes из отчёта
```

---

## 3. Роли агентов

### 3.1 Оркестратор (главный агент)

**Ответственность:**
- Формирование полного inventory кодовой базы и документации
- Декомпозиция на сегменты и назначение суб-агентов
- Контроль параллельного выполнения (`run_in_background`)
- Консолидация результатов и дедупликация findings
- Приоритизация исправлений и запуск Fix-агентов
- Генерация финального сводного отчёта

**НЕ делает:**
- Не читает файлы напрямую (делегирует суб-агентам)
- Не вносит правки в код/docs (делегирует Fix-агентам)
- Не дублирует работу суб-агентов

### 3.2 Layer Auditor (×5 — по одному на слой)

**Scope:** Один архитектурный слой (`domain/`, `application/`, `infrastructure/`,
`composition/`, `interfaces/`).

**Задачи:**
1. Инвентаризация всех `.py` файлов в слое
2. Проверка module-level docstrings (100% coverage target)
3. Проверка class-level docstrings (100% coverage target для public classes)
4. Проверка function/method docstrings (≥95% coverage target для public)
5. Валидация формата docstrings (Google style: Args, Returns, Raises, See Also)
6. Поиск расхождений: docstring описывает одно, код делает другое
7. Проверка ссылок на ADR/RULES в docstrings — актуальны ли они?
8. Идентификация сложных функций (≥20 LOC) без docstrings
9. Идентификация бизнес-решений в коде без документированного обоснования

**Типы документов (по слою):**

| Слой | Типы документов |
|------|-----------------|
| `domain` | docstrings, port contracts, entity docs, value object docs, schema docs, exception hierarchy, validation rules |
| `application` | docstrings, pipeline docs, transformer docs, service docs, use-case descriptions, extractor docs |
| `infrastructure` | docstrings, adapter API reference, storage docs, config loader docs, health check docs, rate limiting docs |
| `composition` | docstrings, factory docs, bootstrap docs, DI assembly docs, provider registration |
| `interfaces` | docstrings, CLI command reference, exit codes, HTTP endpoints, formatter docs |

### 3.3 Provider Auditor (×7 — по одному на провайдера)

**Scope:** Все файлы одного провайдера через все слои:
- `src/bioetl/domain/entities/{provider}.py`
- `src/bioetl/domain/schemas/{provider}/`
- `src/bioetl/domain/contracts/gold/{provider}.py`
- `src/bioetl/application/pipelines/{provider}/`
- `src/bioetl/infrastructure/adapters/{provider}/`
- `configs/pipelines/{provider}/`
- `configs/quality/entities/{provider}/`
- `configs/filters/entities/{provider}/`
- `docs/04-reference/providers/{provider}/`
- `docs/04-reference/pipelines/{provider}-*.md`
- `tests/unit/**/test_*{provider}*`

**Задачи:**
1. Сквозная проверка: entity → schema → transformer → adapter → config → docs
2. Все поля entity отражены в schema? Schema в gold contract?
3. Pipeline spec полный и актуальный?
4. Provider reference doc существует и описывает: API URL, auth, rate limits, entities, limitations?
5. VCR cassettes задокументированы?
6. Docstrings в transformer описывают бизнес-логику преобразований?
7. Config примеры в docs соответствуют реальным configs/?

### 3.4 Architecture Auditor (×1)

**Scope:** Архитектурные документы и их соответствие коду.

**Задачи:**
1. Все 39+ ADR: статус корректен? решение реализовано в коде? последствия актуальны?
2. Layer architecture docs (00-overview..05-composition): описания соответствуют текущей структуре?
3. Архитектурные диаграммы: отражают текущие модули и зависимости?
4. Import matrix в docs соответствует реальным import-ам в коде?
5. Решения, принятые в коде, но не задокументированные как ADR
6. Устаревшие архитектурные описания (упоминание удалённых модулей/классов)

### 3.5 Governance Auditor (×1)

**Scope:** Governance-документы и их синхронизация.

**Задачи:**
1. RULES.md: версия согласована во всех ссылающихся документах?
2. Glossary: все термины из кода присутствуют? Нет устаревших?
3. CHANGELOG: все значимые изменения отражены?
4. mkdocs.yml: все активные docs в навигации? orphan rate < 10%?
5. Naming policy: соблюдается в коде и docs?
6. File policy: структура директорий соответствует политике?
7. GitHub policy: PR template, issue templates актуальны?

### 3.6 Cross-Reference Auditor (×1)

**Scope:** Перекрёстные ссылки и навигация.

**Задачи:**
1. Все internal links в `.md` файлах разрешимы?
2. Ссылки на ADR в коде (комментарии, docstrings) указывают на существующие ADR?
3. Ссылки на RULES.md секции в agent docs/rules актуальны?
4. mkdocs.yml nav: все пути существуют?
5. README файлы в каждой ключевой директории?
6. `docs/00-map.md` навигатор: все ссылки валидны, счётчики актуальны?
7. Orphan docs: файлы в docs/ не упомянутые ни в nav, ни в других docs

---

## 4. Протокол оркестрации

### Phase 1: Reconnaissance (оркестратор)

```
Шаг 1.1: Прочитать контекст проекта
  → .claude/PROJECT_CONTEXT.md
  → .ai/memory/agent-memory.md
  → docs/00-project/RULES.md (header + version only)

Шаг 1.2: Собрать метрики
  → Количество .py файлов по слоям
  → Количество .md файлов в docs/
  → Текущий orphan rate (docs/ vs mkdocs.yml)
  → Последняя дата обновления CHANGELOG.md
  → Количество ADR

Шаг 1.3: Определить scope аудита
  → full (все слои + все провайдеры + все governance docs)
  → partial (указанные слои/провайдеры)
  → targeted (конкретные файлы/модули)

Шаг 1.4: Сформировать сегменты
  → Для каждого суб-агента: {scope, doc_types, priority, dependencies}
```

### Phase 2: Decomposition (оркестратор)

Оркестратор формирует манифест сегментов:

```yaml
segments:
  # ─── Layer Auditors (parallel batch 1) ───
  - id: "LA-DOMAIN"
    agent_type: "layer_auditor"
    scope: "src/bioetl/domain/"
    doc_types: [docstrings, port_contracts, entity_reference, value_object_docs,
                schema_documentation, exception_hierarchy, validation_rules]
    priority: 1
    estimated_files: 170

  - id: "LA-APPLICATION"
    agent_type: "layer_auditor"
    scope: "src/bioetl/application/"
    doc_types: [docstrings, pipeline_documentation, transformer_docs,
                service_descriptions, use_case_docs, extractor_docs]
    priority: 1
    estimated_files: 116

  - id: "LA-INFRASTRUCTURE"
    agent_type: "layer_auditor"
    scope: "src/bioetl/infrastructure/"
    doc_types: [docstrings, adapter_api_reference, storage_documentation,
                config_loader_docs, health_check_docs, rate_limiting_docs]
    priority: 1
    estimated_files: 112

  - id: "LA-COMPOSITION"
    agent_type: "layer_auditor"
    scope: "src/bioetl/composition/"
    doc_types: [docstrings, factory_documentation, bootstrap_docs,
                di_assembly_docs, provider_registration]
    priority: 1
    estimated_files: 45

  - id: "LA-INTERFACES"
    agent_type: "layer_auditor"
    scope: "src/bioetl/interfaces/"
    doc_types: [docstrings, cli_command_reference, exit_codes,
                http_endpoints, formatter_docs]
    priority: 1
    estimated_files: 24

  # ─── Provider Auditors (parallel batch 2) ───
  - id: "PA-CHEMBL"
    agent_type: "provider_auditor"
    provider: "chembl"
    doc_types: [pipeline_spec, entity_docs, schema_docs, adapter_docs, config_docs]
    priority: 2

  - id: "PA-PUBCHEM"
    agent_type: "provider_auditor"
    provider: "pubchem"
    doc_types: [pipeline_spec, entity_docs, schema_docs, adapter_docs, config_docs]
    priority: 2

  # ... (аналогично для uniprot, pubmed, crossref, openalex, semanticscholar)

  # ─── Specialized Auditors (parallel batch 3) ───
  - id: "ARCH"
    agent_type: "architecture_auditor"
    scope: "docs/02-architecture/"
    doc_types: [adr_alignment, layer_docs, diagrams, import_matrix]
    priority: 3

  - id: "GOV"
    agent_type: "governance_auditor"
    scope: "docs/00-project/"
    doc_types: [rules_sync, glossary, changelog, mkdocs_nav, naming_policy]
    priority: 3

  - id: "XREF"
    agent_type: "cross_reference_auditor"
    scope: "docs/"
    doc_types: [internal_links, adr_refs_in_code, nav_validation, orphan_scan]
    priority: 3
```

### Phase 3: Parallel Audit (оркестратор запускает суб-агентов)

**Batch 1** (Layer Auditors — 5 параллельно):
```python
Task(subagent_type="general-purpose", run_in_background=True,
     description="LA-DOMAIN doc audit",
     prompt="<LAYER_AUDITOR_PROMPT для domain>")
Task(subagent_type="general-purpose", run_in_background=True,
     description="LA-APPLICATION doc audit",
     prompt="<LAYER_AUDITOR_PROMPT для application>")
Task(subagent_type="general-purpose", run_in_background=True,
     description="LA-INFRASTRUCTURE doc audit",
     prompt="<LAYER_AUDITOR_PROMPT для infrastructure>")
Task(subagent_type="general-purpose", run_in_background=True,
     description="LA-COMPOSITION doc audit",
     prompt="<LAYER_AUDITOR_PROMPT для composition>")
Task(subagent_type="general-purpose", run_in_background=True,
     description="LA-INTERFACES doc audit",
     prompt="<LAYER_AUDITOR_PROMPT для interfaces>")
```

**Batch 2** (Provider Auditors — 7 параллельно, после завершения Batch 1):
```python
Task(subagent_type="general-purpose", run_in_background=True,
     description="PA-CHEMBL doc audit",
     prompt="<PROVIDER_AUDITOR_PROMPT для chembl>")
# ... (×7 провайдеров)
```

**Batch 3** (Specialized Auditors — 3 параллельно):
```python
Task(subagent_type="general-purpose", run_in_background=True,
     description="ARCH doc audit",
     prompt="<ARCHITECTURE_AUDITOR_PROMPT>")
Task(subagent_type="general-purpose", run_in_background=True,
     description="GOV doc audit",
     prompt="<GOVERNANCE_AUDITOR_PROMPT>")
Task(subagent_type="general-purpose", run_in_background=True,
     description="XREF doc audit",
     prompt="<CROSS_REFERENCE_AUDITOR_PROMPT>")
```

> **Масштабирование:** Если кодовая база слишком велика для одного суб-агента,
> оркестратор дробит сегмент на подсегменты (например, `domain/entities/` +
> `domain/schemas/` + `domain/ports/` вместо одного `domain/`).

### Phase 4: Consolidation (оркестратор)

```
Шаг 4.1: Собрать все findings от суб-агентов
Шаг 4.2: Дедупликация (одна проблема обнаружена несколькими агентами)
Шаг 4.3: Присвоить глобальные ID: CDOC-001, CDOC-002, ...
Шаг 4.4: Классификация по severity: CRITICAL / HIGH / MEDIUM / LOW
Шаг 4.5: Приоритизация: Critical fixes → High → Medium → Low
Шаг 4.6: Группировка в fix-батчи по файловой зоне
Шаг 4.7: Генерация сводного отчёта
```

### Phase 5: Fix Execution (оркестратор запускает Fix-агентов)

```
Fix Batch 1 (Critical — sequential, чтобы избежать конфликтов):
  → Fix-агент: RULES.md version sync
  → Fix-агент: mkdocs.yml orphan resolution
  → Fix-агент: ADR status corrections

Fix Batch 2 (High — parallel по зонам):
  → Fix-агент: docstrings domain/ (docs zone: src/)
  → Fix-агент: docstrings application/ (docs zone: src/)
  → Fix-агент: provider docs (docs zone: docs/)
  → Fix-агент: architecture docs (docs zone: docs/)

Fix Batch 3 (Medium — parallel):
  → Fix-агент: glossary update (docs zone: docs/)
  → Fix-агент: CHANGELOG update (docs zone: root)
  → Fix-агент: missing dates in docs (docs zone: docs/)

Fix Batch 4 (Low — parallel):
  → Fix-агент: broken links
  → Fix-агент: typos and formatting
```

---

## 5. Промпт-шаблоны суб-агентов

### 5.1 Layer Auditor Prompt Template

```markdown
# Layer Documentation Auditor: {LAYER_NAME}

## Роль
Ты — специализированный аудитор документации для слоя `{layer_path}` проекта BioETL.
Твоя задача — исчерпывающий аудит документации этого слоя с выявлением всех
расхождений между кодом и документацией.

## Контекст проекта
- Проект: BioETL — ETL-фреймворк для данных биоактивности
- Архитектура: Hexagonal (Ports & Adapters) + Medallion + DDD
- Стиль docstrings: Google (Args, Returns, Raises, See Also)
- Constitution: `docs/00-project/RULES.md`
- Glossary: `docs/00-project/glossary.md`

## Scope
- **Директория**: `{layer_path}`
- **Типы документов для аудита**: {doc_types_list}
- **Ожидаемое количество файлов**: ~{estimated_files}

## Инструкции

### Шаг 1: Инвентаризация
1. Найди ВСЕ `.py` файлы в `{layer_path}` (включая вложенные директории)
2. Для каждого файла определи:
   - Наличие module-level docstring (да/нет)
   - Количество public классов / с docstrings
   - Количество public функций / с docstrings
   - Формат docstrings (Google / Sphinx / plain / отсутствует)

### Шаг 2: Аудит качества docstrings
Для КАЖДОГО файла проверь:

**Module-level docstring:**
- [ ] Присутствует
- [ ] Описывает назначение модуля
- [ ] Указывает принадлежность к слою/подсистеме
- [ ] Ссылается на RULES.md / ADR (если релевантно)

**Class-level docstrings:**
- [ ] Все public классы имеют docstrings
- [ ] Описывают назначение класса
- [ ] Документируют `__init__` параметры (Args секция)
- [ ] Указывают реализуемый Port/Protocol (если применимо)
- [ ] Содержат See Also ссылки на связанные классы

**Method/Function docstrings:**
- [ ] Все public методы/функции имеют docstrings
- [ ] Args: все параметры документированы с типами
- [ ] Returns: возвращаемое значение описано
- [ ] Raises: все исключения перечислены
- [ ] Сложные методы (≥20 LOC) имеют развёрнутое описание

### Шаг 3: Поиск расхождений код ↔ документация
Для каждого файла проверь:
1. **Фантомные параметры**: docstring описывает параметр, которого нет в сигнатуре
2. **Пропущенные параметры**: параметр есть в сигнатуре, но не в docstring
3. **Неверные типы**: тип в docstring не совпадает с annotation
4. **Устаревшие описания**: docstring описывает поведение, которое изменилось
5. **Мёртвые ссылки**: ссылки на ADR/RULES/другие модули, которые перемещены/удалены
6. **Ложные утверждения**: docstring утверждает X, код делает Y

### Шаг 4: Идентификация недокументированных решений
Найди места в коде, где:
1. Присутствует нетривиальная бизнес-логика без объясняющего комментария/docstring
2. Используется magic number без именованной константы или пояснения
3. Обрабатывается edge case без описания почему
4. Сделан архитектурный выбор (паттерн, структура) без ссылки на ADR
5. Есть fallback/degradation логика без объяснения сценариев

### Шаг 5: Проверка сопутствующей документации
Проверь наличие и актуальность документации в `docs/`:
{layer_specific_docs_check}

## Формат выхода

```yaml
layer_audit:
  layer: "{layer_name}"
  date: "YYYY-MM-DD"
  scope: "{layer_path}"
  inventory:
    total_files: N
    total_classes: N
    total_functions: N
    module_docstring_coverage: "N%"
    class_docstring_coverage: "N%"
    function_docstring_coverage: "N%"
    google_style_compliance: "N%"
  findings:
    - id: "LA-{LAYER}-001"
      type: "missing_docstring|stale_docstring|phantom_param|
             undocumented_decision|broken_reference|false_claim|
             missing_doc_file|style_violation"
      severity: "CRITICAL|HIGH|MEDIUM|LOW"
      file: "src/bioetl/{layer}/path/to/file.py"
      line: N
      description: "Краткое описание проблемы"
      evidence: "Фрагмент кода или команда верификации"
      recommendation: "Предложение по исправлению"
  summary:
    critical: N
    high: N
    medium: N
    low: N
    overall_score: "N/10"
```

## Правила severity
- **CRITICAL**: Docstring утверждает ложное; документация misleading
- **HIGH**: Public API без docstring; значительное расхождение
- **MEDIUM**: Неполный docstring (missing Args/Returns); стилистическое нарушение
- **LOW**: Отсутствует See Also; minor formatting; private без docstring
```

### 5.2 Provider Auditor Prompt Template

```markdown
# Provider Documentation Auditor: {PROVIDER_NAME}

## Роль
Ты — специализированный аудитор документации для провайдера `{provider}` в проекте BioETL.
Твоя задача — сквозная проверка документации от domain entities до pipeline configs.

## Scope
Все файлы провайдера {provider} через все архитектурные слои:

| Компонент | Путь | Статус |
|-----------|------|--------|
| Domain Entity | `src/bioetl/domain/entities/{provider}.py` | Проверить |
| Domain Schemas | `src/bioetl/domain/schemas/{provider}/` | Проверить |
| Gold Contract | `src/bioetl/domain/contracts/gold/{provider}.py` | Проверить |
| Transformers | `src/bioetl/application/pipelines/{provider}/` | Проверить |
| Adapter | `src/bioetl/infrastructure/adapters/{provider}/` | Проверить |
| Pipeline Configs | `configs/pipelines/{provider}/` | Проверить |
| DQ Configs | `configs/quality/entities/{provider}/` | Проверить |
| Filter Configs | `configs/filters/entities/{provider}/` | Проверить |
| Provider Docs | `docs/04-reference/providers/{provider}/` | Проверить |
| Pipeline Specs | `docs/04-reference/pipelines/{provider}-*.md` | Проверить |
| Tests | `tests/unit/**/test_*{provider}*` | Инвентаризация |

## Инструкции

### Шаг 1: Entity-Schema-Contract Chain
1. Прочитай domain entity → перечисли все поля
2. Прочитай Pandera schemas → перечисли все колонки (Bronze, Silver, Gold)
3. Прочитай Gold contract → перечисли все поля
4. **Матрица соответствия**: Entity field → Schema column → Contract field
5. **Находки**: поля без документации, поля в docs но не в коде, расхождения типов

### Шаг 2: Transformer Documentation
1. Для каждого transformer: описаны ли правила трансформации?
2. Документированы ли бизнес-решения (почему поле X маппится на Y)?
3. Описаны ли edge cases и fallback-стратегии?
4. Ссылки на API docs провайдера актуальны?

### Шаг 3: Adapter Documentation
1. API base URL документирован и актуален?
2. Rate limiting описан (значение, стратегия)?
3. Pagination strategy документирована (offset/cursor)?
4. Health check contract описан?
5. Error handling и retry policy описаны?
6. Authentication requirements (если есть)?

### Шаг 4: Config Documentation
1. Pipeline config: все обязательные поля присутствуют и описаны?
2. DQ config: правила валидации описаны? thresholds обоснованы?
3. Filter config: фильтры описаны? логика включения/исключения ясна?
4. Примеры в docs/ соответствуют реальным configs/?

### Шаг 5: Provider Reference Doc
1. Существует ли `docs/04-reference/providers/{provider}/*.md`?
2. Содержит ли: API overview, auth, rate limits, entities, limitations?
3. Pipeline spec для каждого entity: Bronze→Silver→Gold flow описан?
4. VCR cassettes locations задокументированы?

## Формат выхода

```yaml
provider_audit:
  provider: "{provider}"
  date: "YYYY-MM-DD"
  entity_coverage:
    entities_in_code: ["entity1", "entity2"]
    entities_in_docs: ["entity1"]
    missing_in_docs: ["entity2"]
    coverage: "N%"
  field_matrix:
    total_entity_fields: N
    documented_fields: N
    undocumented_fields: N
    phantom_doc_fields: N  # в docs, но не в коде
    coverage: "N%"
  findings:
    - id: "PA-{PROVIDER}-001"
      type: "missing_entity_doc|stale_pipeline_spec|field_mismatch|
             missing_adapter_doc|config_doc_drift|missing_provider_ref"
      severity: "CRITICAL|HIGH|MEDIUM|LOW"
      file: "path/to/file"
      description: "..."
      evidence: "..."
      recommendation: "..."
  summary:
    critical: N
    high: N
    medium: N
    low: N
```
```

### 5.3 Architecture Auditor Prompt Template

```markdown
# Architecture Documentation Auditor

## Роль
Ты — аудитор архитектурной документации проекта BioETL. Задача —
проверить соответствие ADR, архитектурных описаний и диаграмм реальному коду.

## Scope
- `docs/02-architecture/decisions/` — 39+ ADR
- `docs/02-architecture/` — layer docs, diagrams, overview
- Import matrix в RULES.md vs реальные imports

## Инструкции

### Шаг 1: ADR Alignment Audit
Для КАЖДОГО ADR (ADR-001 через ADR-039+):
1. Прочитай ADR: Status, Context, Decision, Consequences
2. Проверь: решение реализовано в коде? Найди конкретные файлы.
3. Проверь: Consequences актуальны? Negative consequences смягчены?
4. Проверь: Status правильный? (Accepted/Superseded/Deprecated)
5. Проверь: нет конфликтов между ADR (например, ADR-003 vs ADR-010)

### Шаг 2: Architecture Docs vs Code
1. Layer descriptions (01..05) соответствуют текущим модулям?
2. Module names в docs существуют в src/?
3. Class names в docs существуют в коде?
4. Dependency arrows в описаниях соответствуют import matrix?

### Шаг 3: Undocumented Architectural Decisions
Найди в коде паттерны, заслуживающие ADR:
1. Нетривиальные design patterns без ссылки на ADR
2. Workarounds с комментариями типа "because..." без формального ADR
3. Значимые технологические выборы (библиотеки, протоколы) без ADR
4. Сложные fallback/degradation стратегии без обоснования

### Шаг 4: Diagram Freshness
1. Mermaid diagrams (.mmd) отражают текущую структуру?
2. Rendered PNG/SVG актуальны?
3. Diagram catalog полный?

## Формат выхода

```yaml
architecture_audit:
  date: "YYYY-MM-DD"
  adr_count: N
  adr_alignment:
    fully_aligned: N
    partially_aligned: N
    misaligned: N
    missing_adr_candidates: N
  findings:
    - id: "ARCH-DOC-001"
      type: "adr_misaligned|adr_status_wrong|adr_conflict|
             stale_arch_doc|missing_adr|stale_diagram|
             phantom_module_in_docs"
      severity: "CRITICAL|HIGH|MEDIUM|LOW"
      adr: "ADR-0XX"  # если применимо
      description: "..."
      evidence: "..."
      recommendation: "..."
```
```

### 5.4 Governance Auditor Prompt Template

```markdown
# Governance Documentation Auditor

## Роль
Ты — аудитор governance-документации проекта BioETL. Задача — проверить
синхронизацию RULES.md, glossary, CHANGELOG, mkdocs.yml и policies.

## Scope
- `docs/00-project/RULES.md` — Constitution
- `docs/00-project/glossary.md` — Terminology
- `CHANGELOG.md` — Version history
- `mkdocs.yml` — Navigation
- `docs/00-project/governance/` — Policies
- `docs/00-map.md` — Navigator

## Инструкции

### Шаг 1: RULES.md Version Sync
1. Определи текущую версию RULES.md (header)
2. Найди ВСЕ файлы, ссылающиеся на версию RULES.md
3. Проверь: все указывают одну версию?
4. Проверь: дата в RULES.md актуальна?

### Шаг 2: Glossary Completeness
1. Извлеки ВСЕ технические термины из `src/bioetl/` (class names, enum values, constants)
2. Проверь: каждый присутствует в glossary?
3. Проверь: нет устаревших терминов (классы/enums удалены, но в glossary остались)

### Шаг 3: CHANGELOG Completeness
1. Проверь: `[Unreleased]` секция отражает все текущие изменения?
2. Сравни git log с CHANGELOG — есть ли значимые коммиты без записи?
3. Формат: Keep-a-Changelog (Added/Changed/Fixed/Removed)?

### Шаг 4: mkdocs.yml Navigation Audit
1. Подсчитай docs в `docs/` (без archive)
2. Подсчитай docs в mkdocs.yml nav
3. Orphan rate = (total - in_nav) / total
4. Target: orphan rate < 10%
5. Перечисли все orphan docs

### Шаг 5: 00-map.md Accuracy
1. Счётчики (ADR, providers, pipelines) актуальны?
2. Все ссылки разрешимы?
3. Структура отражает текущую организацию docs/?

## Формат выхода

```yaml
governance_audit:
  date: "YYYY-MM-DD"
  rules_version: "vX.Y"
  rules_sync_status: "synced|desynchronized"
  glossary_coverage: "N%"
  changelog_status: "current|stale"
  mkdocs_orphan_rate: "N%"
  map_accuracy: "N%"
  findings:
    - id: "GOV-001"
      type: "version_desync|missing_glossary_term|stale_changelog|
             orphan_doc|stale_map_counter|missing_nav_entry"
      severity: "CRITICAL|HIGH|MEDIUM|LOW"
      description: "..."
      evidence: "..."
      recommendation: "..."
```
```

### 5.5 Cross-Reference Auditor Prompt Template

```markdown
# Cross-Reference Documentation Auditor

## Роль
Ты — аудитор перекрёстных ссылок и навигации проекта BioETL. Задача —
найти все broken links, мёртвые ссылки и навигационные проблемы.

## Scope
- Все `.md` файлы в `docs/`
- Все docstrings с ссылками на docs (See Also, ADR-NNN)
- mkdocs.yml navigation tree
- README файлы во всех директориях

## Инструкции

### Шаг 1: Internal Link Validation
1. Найди ВСЕ markdown ссылки `[text](path.md)` в docs/
2. Для каждой: target файл существует?
3. Для anchor ссылок `[text](path.md#section)`: секция существует?

### Шаг 2: ADR References in Code
1. Найди все `ADR-NNN` упоминания в `src/bioetl/` (comments + docstrings)
2. Для каждого: ADR файл существует? Статус Accepted?
3. Контекст ссылки соответствует содержанию ADR?

### Шаг 3: RULES.md Section References
1. Найди все `§N.N` и `RULES-§N.N` ссылки в agent docs и rules
2. Для каждой: секция существует в текущем RULES.md?
3. Содержание соответствует контексту ссылки?

### Шаг 4: README Coverage
1. Перечисли ВСЕ директории в src/bioetl/ с >3 файлами
2. Для каждой: есть __init__.py с module docstring? Это достаточный README?
3. Перечисли ВСЕ директории в docs/ с >3 файлами
4. Для каждой: есть README.md или index?

### Шаг 5: Orphan Detection
1. Файлы в docs/ не упомянутые ни в mkdocs.yml, ни в других .md файлах
2. Файлы в docs/ не ссылающиеся ни на один другой файл (isolated)

## Формат выхода

```yaml
crossref_audit:
  date: "YYYY-MM-DD"
  total_links_checked: N
  broken_links: N
  adr_refs_in_code: N
  invalid_adr_refs: N
  orphan_docs: N
  missing_readmes: N
  findings:
    - id: "XREF-001"
      type: "broken_link|invalid_adr_ref|stale_rules_ref|
             missing_readme|orphan_doc|isolated_doc"
      severity: "CRITICAL|HIGH|MEDIUM|LOW"
      source_file: "path/to/source.md"
      target: "path/to/target.md"
      description: "..."
      recommendation: "..."
```
```

---

## 6. Fix-агенты (Phase 5)

### 6.1 Docstring Fix Agent

```markdown
# Docstring Fix Agent: {LAYER_NAME}

## Роль
Ты — агент исправления docstrings для слоя `{layer_path}`.
Ты получил список findings от Layer Auditor и должен исправить каждый.

## Входные данные
- Findings: {findings_list}  # Список проблем с файлами и строками

## Правила исправления

### Формат: Google style (ОБЯЗАТЕЛЬНО)

```python
def method_name(self, param1: Type1, param2: Type2) -> ReturnType:
    """Brief one-line summary.

    Extended description if the method is complex (≥10 LOC or
    non-obvious business logic).

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        SomeError: When condition is met.

    See Also:
        - :class:`RelatedClass`
        - ADR-NNN: Relevant decision
    """
```

### Правила
1. **НЕ менять код** — только docstrings и комментарии
2. **НЕ добавлять docstrings к private методам** (начинающимся с `_`),
   если только это не сложная внутренняя логика (≥20 LOC)
3. **Описывать ЧТО делает**, не КАК (implementation details)
4. **Для бизнес-решений**: добавить WHY (почему так, а не иначе)
5. **Для edge cases**: описать граничные условия
6. **Ссылки на ADR**: добавить `See Also: ADR-NNN` где релевантно
7. **Терминология**: использовать только термины из glossary.md

### Верификация каждого исправления
После каждой правки убедись:
- [ ] Docstring соответствует фактическому поведению кода
- [ ] Все параметры из сигнатуры описаны
- [ ] Типы соответствуют annotations
- [ ] Нет фантомных параметров
```

### 6.2 Documentation File Fix Agent

```markdown
# Documentation Fix Agent: {DOC_SCOPE}

## Роль
Ты — агент исправления файлов документации в `docs/`.
Ты получил список findings и должен внести корректировки.

## Входные данные
- Findings: {findings_list}

## Правила
1. **Документировать реальность**, не желаемое поведение
2. **Указывать даты** в каждом обновлённом документе
3. **Сохранять существующую структуру** — не реорганизовывать без необходимости
4. **Ссылки на код**: указывать конкретные `file:line` (не абстрактно)
5. **ADR**: не менять Status без согласования с пользователем
6. **mkdocs.yml**: добавлять новые docs в правильную секцию навигации
7. **Не удалять docs** — помечать как deprecated/archived, перемещать в 99-archive/

## Типы исправлений
- `update_content`: Обновить содержимое в соответствии с кодом
- `add_missing`: Создать отсутствующий документ по шаблону
- `fix_link`: Исправить broken link
- `sync_version`: Синхронизировать версию/дату
- `add_to_nav`: Добавить в mkdocs.yml navigation
- `archive`: Переместить устаревший документ в 99-archive/
```
```

---

## 7. Scoring и отчётность

### Consolidated Report Template

```markdown
# Documentation Cascade Audit Report

**Date**: YYYY-MM-DD
**Scope**: Full / Partial ({layers}, {providers})
**Agents deployed**: N
**Total files analyzed**: N (Python) + N (Markdown)

## Executive Summary

| Dimension | Score | Status |
|-----------|:-----:|:------:|
| Docstring Coverage | N/10 | PASS/WARN/FAIL |
| Docstring Quality | N/10 | PASS/WARN/FAIL |
| Code-Doc Alignment | N/10 | PASS/WARN/FAIL |
| Provider Documentation | N/10 | PASS/WARN/FAIL |
| Architecture Documentation | N/10 | PASS/WARN/FAIL |
| Governance & Navigation | N/10 | PASS/WARN/FAIL |
| Cross-References | N/10 | PASS/WARN/FAIL |
| **OVERALL** | **N/10** | **STATUS** |

## Metrics

| Metric | Before | After | Delta |
|--------|:------:|:-----:|:-----:|
| Module docstring coverage | N% | N% | +N% |
| Class docstring coverage | N% | N% | +N% |
| Function docstring coverage | N% | N% | +N% |
| Google style compliance | N% | N% | +N% |
| mkdocs orphan rate | N% | N% | -N% |
| Broken links | N | N | -N |
| ADR alignment | N% | N% | +N% |
| Glossary coverage | N% | N% | +N% |

## Findings Summary (by source agent)

| Agent | Critical | High | Medium | Low | Total |
|-------|:--------:|:----:|:------:|:---:|:-----:|
| LA-DOMAIN | N | N | N | N | N |
| LA-APPLICATION | N | N | N | N | N |
| LA-INFRASTRUCTURE | N | N | N | N | N |
| LA-COMPOSITION | N | N | N | N | N |
| LA-INTERFACES | N | N | N | N | N |
| PA-CHEMBL | N | N | N | N | N |
| PA-PUBCHEM | N | N | N | N | N |
| ... | | | | | |
| ARCH | N | N | N | N | N |
| GOV | N | N | N | N | N |
| XREF | N | N | N | N | N |
| **TOTAL** | **N** | **N** | **N** | **N** | **N** |

## All Findings (consolidated, deduplicated)

### CRITICAL
(перечисление)

### HIGH
(перечисление)

### MEDIUM
(перечисление)

### LOW
(перечисление)

## Fixes Applied

| Fix ID | Finding | File | Action | Status |
|--------|---------|------|--------|:------:|
| FIX-001 | CDOC-001 | path | description | done/pending |

## Remaining Items (require user decision)

| # | Item | Options | Recommendation |
|:-:|------|---------|----------------|

## Verification Commands

```bash
# Docstring coverage check
python -c "import ast; ..."

# mkdocs build (link check)
mkdocs build --strict 2>&1 | grep -c "WARNING"

# ADR count
ls docs/02-architecture/decisions/ADR-*.md | wc -l

# Glossary sync
python scripts/lint_terminology.py --check

# Architecture tests
pytest tests/architecture/ -v --tb=short
```
```

### Scoring Rules

| Dimension | Weight | Scoring |
|-----------|:------:|---------|
| Docstring Coverage | 20% | 100%=10, 95%=9, 90%=8, 85%=7, <80%=5 |
| Docstring Quality | 15% | Google compliance %, factual accuracy |
| Code-Doc Alignment | 25% | 0 false claims=10, per false claim -2 |
| Provider Documentation | 15% | Entity coverage × field coverage |
| Architecture Documentation | 10% | ADR alignment % |
| Governance & Navigation | 10% | Orphan rate inverse, version sync |
| Cross-References | 5% | Broken link count inverse |

| Score | Status |
|:-----:|:------:|
| ≥ 8.0 | PASS |
| 6.0 - 7.9 | WARN |
| < 6.0 | FAIL |

---

## 8. Автомасштабирование

### Правила дробления сегментов

Если суб-агент сообщает, что scope слишком велик (>100 файлов для layer,
>50 findings), оркестратор дробит сегмент:

| Исходный сегмент | Дробление |
|-----------------|-----------|
| `LA-DOMAIN` | `LA-DOMAIN-ENTITIES`, `LA-DOMAIN-SCHEMAS`, `LA-DOMAIN-PORTS`, `LA-DOMAIN-SERVICES`, `LA-DOMAIN-OTHER` |
| `LA-APPLICATION` | `LA-APP-PIPELINES-CHEMBL`, `LA-APP-PIPELINES-PUB`, `LA-APP-CORE`, `LA-APP-SERVICES`, `LA-APP-COMPOSITE` |
| `LA-INFRASTRUCTURE` | `LA-INFRA-ADAPTERS`, `LA-INFRA-STORAGE`, `LA-INFRA-OBSERVABILITY`, `LA-INFRA-OTHER` |
| `PA-CHEMBL` (16 entities) | `PA-CHEMBL-ACTIVITY`, `PA-CHEMBL-MOLECULE`, `PA-CHEMBL-TARGET`, `PA-CHEMBL-OTHER` |

### Правила слияния сегментов

Если сегмент слишком мал (<5 файлов), оркестратор объединяет:

| Сегменты | Слияние |
|----------|---------|
| `PA-OPENALEX` + `PA-SEMANTICSCHOLAR` | `PA-PUBLICATION-MINOR` |
| `LA-INTERFACES` (24 файла) | Может быть совмещён с `LA-COMPOSITION` |

---

## 9. Ограничения и гарантии

### Гарантии
1. **Полнота**: каждый `.py` файл в `src/bioetl/` проверен хотя бы одним агентом
2. **Дедупликация**: один finding = один ID, даже если обнаружен несколькими агентами
3. **Трассируемость**: каждый fix привязан к finding, каждый finding — к файлу:строке
4. **Идемпотентность**: повторный запуск не создаёт дублей
5. **Safe by default**: Fix-агенты не удаляют код/docs без явного указания

### Ограничения
1. **Не запускает тесты** — только аудит и исправление документации
2. **Не меняет production код** — только docstrings, comments, docs/
3. **Не создаёт ADR** — только идентифицирует кандидатов для ADR
4. **Требует user approval** для: удаление docs, изменение ADR status, архивация

### Зоны записи

| Агент | Зона записи |
|-------|-------------|
| Layer Auditor | read-only |
| Provider Auditor | read-only |
| Architecture Auditor | read-only |
| Governance Auditor | read-only |
| Cross-Reference Auditor | read-only |
| Docstring Fix Agent | `src/bioetl/` (только docstrings) |
| Documentation Fix Agent | `docs/`, `mkdocs.yml`, `CHANGELOG.md` |

---

## 10. Интеграция с существующей системой

### Совместимость с ORCHESTRATION.md v3.0

Documentation Cascade Audit может использоваться как:
1. **Standalone** — полный аудит документации по запросу пользователя
2. **В составе workflow** — замена шага 6 (`py-doc-bot`) для масштабных задач
3. **Pre-release** — documentation freeze audit перед релизом

### ID-система

| Prefix | Назначение |
|--------|------------|
| `CDOC-` | Consolidated documentation finding |
| `LA-` | Layer Auditor finding |
| `PA-` | Provider Auditor finding |
| `ARCH-DOC-` | Architecture documentation finding |
| `GOV-` | Governance finding |
| `XREF-` | Cross-reference finding |
| `FIX-` | Applied fix |

### Артефакты

```text
reports/plans/<task_id>/
├── cascade-audit-manifest.yaml   ← Оркестратор (сегменты)
├── cascade-audit-LA-DOMAIN.yaml  ← Layer Auditor (domain)
├── cascade-audit-LA-APP.yaml     ← Layer Auditor (application)
├── cascade-audit-LA-INFRA.yaml   ← Layer Auditor (infrastructure)
├── cascade-audit-LA-COMP.yaml    ← Layer Auditor (composition)
├── cascade-audit-LA-IFACE.yaml   ← Layer Auditor (interfaces)
├── cascade-audit-PA-CHEMBL.yaml  ← Provider Auditor (chembl)
├── cascade-audit-PA-PUBCHEM.yaml ← Provider Auditor (pubchem)
├── ...                            ← Остальные провайдеры
├── cascade-audit-ARCH.yaml       ← Architecture Auditor
├── cascade-audit-GOV.yaml        ← Governance Auditor
├── cascade-audit-XREF.yaml       ← Cross-Reference Auditor
├── cascade-audit-fixes.yaml      ← Лог исправлений
└── cascade-audit-report.md       ← Финальный сводный отчёт
```

---

## 11. Быстрый старт

### Полный аудит
```
/documentation-cascade-audit full
```

### Targeted аудит (один слой)
```
/documentation-cascade-audit layers application
```

### Targeted аудит (один провайдер)
```
/documentation-cascade-audit providers chembl
```

### Только governance
```
/documentation-cascade-audit governance
```

### Только перекрёстные ссылки
```
/documentation-cascade-audit crossref
```

---

## 12. Changelog

### v1.0.0 (2026-02-26)
- **NEW**: Initial release — hierarchical documentation audit system
- **NEW**: 5 Layer Auditor templates (domain, application, infrastructure, composition, interfaces)
- **NEW**: Provider Auditor template (x7 providers)
- **NEW**: Architecture, Governance, Cross-Reference Auditor templates
- **NEW**: Docstring Fix Agent and Documentation Fix Agent templates
- **NEW**: Consolidated report template with scoring matrix
- **NEW**: Auto-scaling rules (segment splitting/merging)
- **NEW**: Integration with ORCHESTRATION.md v3.0 workflow
