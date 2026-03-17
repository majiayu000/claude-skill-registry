---
name: smart-rules
description: "[Utility] Analyzes user prompts and efficiently loads only relevant rule documents. Auto-generates category-document mapping config file on first invocation by scanning project documents. Supports both automatic and manual invocation. (project)"
user_invocable: true
---

# Smart Rules

A skill that analyzes user prompts and efficiently loads only relevant rule/guide documents.

## Key Features

- **Auto-initialization**: Scans project documents and auto-generates config file on first invocation
- **Config-based**: Category-document mapping defined in project-specific `smart-rules.yaml`
- **Efficient loading**: Skips if no match, loads only what's needed
- **Dual invocation**: Auto-execute before tasks or manual `/smart-rules` command
- **Post-TodoWrite trigger**: Analyzes todo content and loads relevant rules after TodoWrite

---

## ⛔ CRITICAL: Auto-Invocation Rules

**AI MUST automatically invoke smart-rules in these situations:**

### 1. After TodoWrite Tool Usage

When AI uses the `TodoWrite` tool, AI MUST invoke smart-rules to analyze the todo content and load relevant rules:

```
[AI uses TodoWrite tool]
        ↓
[Analyze todo content keywords]
        ↓
[Smart Rules] Loaded documents for: [matched categories based on todo content]
```

**Example:**
```
TodoWrite: "Export 다이얼로그 UI 구현"
        ↓
Keywords: Export, 다이얼로그, UI, 구현
        ↓
[Smart Rules] Loaded 3 documents for categories: [ui, design, patterns]
  - Docs/UX/IA.md
  - Docs/UX/DesignSystem/Components.md
  - Docs/Patterns/Flutter-Desktop-Window-Management-Pattern.md
```

**Why?** 에이전트가 작업할 todo와 관련된 규칙을 미리 숙지하여 올바른 패턴과 컨벤션을 따르도록 합니다.

### 2. Before Implementation Tasks

When user requests feature implementation, bug fix, or code changes:

```
[User requests implementation]
        ↓
[Smart Rules] Analyzing keywords...
[Smart Rules] Loaded documents for: [coding, patterns, ...]
```

### Auto-Invocation Triggers

| Trigger | Action |
|---------|--------|
| **TodoWrite 사용 직후** | Todo 내용 키워드 분석 → 관련 규칙 로드 |
| 구현 요청 | 사용자 요청 키워드 분석 → 관련 규칙 로드 |
| 버그 수정 요청 | 사용자 요청 키워드 분석 → 관련 규칙 로드 |
| 리팩토링 요청 | 사용자 요청 키워드 분석 → 관련 규칙 로드 |

---

## Commands

| Command | Description |
|---------|-------------|
| `/smart-rules init` | Scan project and generate config file |
| `/smart-rules rescan` | Delete existing config and rescan |
| `/smart-rules` | Load documents based on current context |
| `/smart-rules [category]` | Load specific category documents only |
| `/smart-rules all` | Load all category documents |

---

## Workflow

### 1. Initialization (init) - When config file missing

```
[1. Detect Missing Config]
    └─ Check if smart-rules.yaml exists
           ↓
[2. Scan Project Documents]
    └─ Scan standard paths:
       - .claude/rules/*.md
       - Docs/**/*.md
       - .claude/CLAUDE.md, CLAUDE.md
       - README.md
           ↓
[3. Analyze & Categorize]
    └─ Classify discovered documents by category
           ↓
[4. Extract Keywords]
    └─ Extract keywords from document titles/headers
           ↓
[5. Generate Config]
    └─ Create smart-rules.yaml file
    └─ Report generated config to user
```

### 2. Document Loading - When config file exists

```
[1. Load Config]
    └─ Read smart-rules.yaml
           ↓
[2. Analyze Prompt]
    └─ Extract keywords from user prompt
           ↓
[3. Match Categories]
    └─ Match keywords → categories
    └─ Check composite categories
           ↓
[4. Skip if No Match]
    └─ Skip if no matches found
           ↓
[5. Load Documents]
    └─ Load matched category documents
    └─ Remove duplicates, apply max_documents limit
           ↓
[6. Report]
    └─ Output loaded document list
```

---

## Auto-categorization Rules

Documents are auto-classified by filename/path patterns during scanning:

| Pattern | Category |
|---------|----------|
| architecture, arch, structure | `architecture` |
| coding, convention, style, lint | `coding` |
| UX, UI, screen, layout, component | `ui` |
| design, color, theme, typography | `design` |
| task, todo, backlog | `task` |
| spec, prd, requirement | `spec` |
| pattern | `patterns` |
| security, critical | `security` |
| others | `misc` |

## Excluded Categories

**AI MUST NOT scan or load documents for these categories:**

| Pattern | Reason |
|---------|--------|
| label, labeling | 라벨링 시스템 - 필요시 수동 조회 |
| history | 히스토리 로깅 - 작업 완료 시만 사용 |
| brain, canvas | Brain 캔버스 - 별도 스킬로 관리 |

**These files should be excluded from scanning:**
- `.claude/rules/labeling.md`
- `.claude/rules/history.md`
- `Docs/Labels/**/*.md`
- `Docs/History/**/*.md`
- `Docs/Brain/**/*`

---

## Config File Schema (smart-rules.yaml)

```yaml
version: 1

# 스캔된 문서 경로 (자동 생성 시 기록)
scanned_paths:
  - .claude/rules/
  - Docs/

# 옵션
options:
  max_documents: 5          # 최대 로드 문서 수
  auto_invoke: true         # 작업 시작 전 자동 실행 여부
  show_loaded_report: true  # 로드된 문서 목록 출력 여부

# 카테고리 정의
categories:
  category_name:
    keywords:
      - 키워드1
      - keyword2
    documents:
      - path/to/document1.md
      - path/to/document2.md

# 복합 카테고리 (여러 카테고리 조합)
composites:
  composite_name:
    keywords:
      - 복합 키워드
    includes:
      - category1
      - category2
```

---

## Usage Examples

### Example 1: Feature Implementation Request

```
User: "로그인 화면을 구현해줘"

AI Analysis:
- Keywords: 로그인, 화면, 구현
- Matched: ui, design, coding

[Smart Rules] Loaded 3 documents for categories: [ui, design, coding]
  - Docs/UX/IA.md
  - Docs/UX/DesignSystem/Components.md
  - Docs/Index/CODING_CONVENTIONS.md
```

### Example 2: Specific Category Load

```
User: "/smart-rules task"

[Smart Rules] Category 'task' loaded:
  - .claude/rules/task-management.md
```

### Example 3: No Match

```
User: "git commit 해줘"

[Smart Rules] No matching rules for this task. Proceeding without rule documents.
```

---

## Output Format

### On Match Success
```
[Smart Rules] Loaded N documents for categories: [cat1, cat2]
  - path/to/doc1.md
  - path/to/doc2.md
```

### On No Match
```
[Smart Rules] No matching rules for this task. Proceeding without rule documents.
```

### On Initialization
```
[Smart Rules] Initializing...
Scanned paths: .claude/rules/, Docs/
Found N documents across M categories.

Generated: .smart-rules.yaml

Categories created:
  - architecture (2 docs)
  - coding (2 docs)
  - ui (3 docs)
  ...
```

---

## Limitations

| Item | Default | Description |
|------|---------|-------------|
| max_documents | 5 | Maximum documents to load at once |
| Keyword matching | Case-insensitive | Supports both Korean and English |
| No config file | Auto init | Auto-initializes if smart-rules.yaml missing |

---

## Config File Location

**IMPORTANT: Config file is stored in project root, SEPARATELY from skill definition.**

```
.smart-rules.yaml                     ← Project-specific config (generated at root)
.claude/skills/smart-rules/SKILL.md   ← Skill definition only (do NOT touch)
```

| File Type | Location | Purpose |
|-----------|----------|---------|
| **Skill Definition** | `.claude/skills/smart-rules/SKILL.md` | Read-only skill spec (managed by Droid) |
| **Project Config** | `.smart-rules.yaml` (project root) | Project-specific category mappings |

### Why Separate?
- Skill folder is managed by Droid (synced, updated, reset)
- Config file is project-specific and persists across skill updates
- Prevents "folder already exists" conflicts during `init`

### Init Behavior
- `/smart-rules init` checks for `.smart-rules.yaml` in project root
- If missing → scans project and creates `.smart-rules.yaml` at root
- If exists → uses existing config (no conflict with skill folder)
- `/smart-rules rescan` deletes `.smart-rules.yaml` and rescans
