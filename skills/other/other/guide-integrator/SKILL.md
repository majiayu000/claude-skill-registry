---
name: guide-integrator
description: "Use when designing features - loads plugin methodology refs and delegates to dev-guides-navigator for online Drupal domain knowledge. Trigger: 'load guides', 'get reference docs', 'methodology references'. Use proactively during Phase 2 design — loads SOLID, Library-First, DRY, TDD, Security guides."
version: 4.0.0
user-invocable: false
---

# Guide Integrator

Load development references and integrate into architecture documents. Two sources: plugin methodology refs and online dev-guides (via navigator).

## Built-in References (Methodology)

| Topic | Reference File |
|-------|----------------|
| Test-Driven Development | `references/tdd-workflow.md` |
| SOLID Principles | `references/solid-drupal.md` |
| DRY Patterns | `references/dry-patterns.md` |
| Library-First/CLI-First | `references/library-first.md` |
| Quality Gates | `references/quality-gates.md` |
| Purposeful Code | `references/purposeful-code.md` |

## Activation

**PROACTIVE:** Activate at the START of every phase activity — do not wait for explicit request.

Activate when:
- **Any Phase 1 activity** — load guides for the task's Drupal domain before research
- **Any Phase 2 activity** — load architecture decision guides before design
- **Any Phase 3 activity** — load security, SDC, JS guides before implementation
- Designing features that match reference topics
- User mentions specific patterns (TDD, SOLID, DRY)
- Architecture drafting for any feature
- Auto-triggered by `architecture-drafter` agent

**Skip if:** The relevant guide was already loaded earlier in this session (check conversation context).

## Auto-Load Rules (Plugin References)

| Keywords Detected | Reference to Load |
|-------------------|-------------------|
| "test", "TDD", "unit test", "kernel test" | `references/tdd-workflow.md` |
| "service", "dependency", "inject", "SOLID" | `references/solid-drupal.md` |
| "duplicate", "reuse", "DRY", "extract" | `references/dry-patterns.md` |
| "form", "drush", "command", "service first" | `references/library-first.md` |
| "complete", "done", "quality", "gate" | `references/quality-gates.md` |

## Workflow

### 1. Load Plugin References (Methodology)

Based on detected keywords in the task:
1. Identify which methodology references apply (see Auto-Load Rules)
2. Read each applicable reference file
3. Extract patterns relevant to current task

### 2. Delegate Online Guides to Navigator

For Drupal-specific architecture decisions, invoke the `dev-guides-navigator` skill with the task keywords. The navigator handles:
- Hash-based caching of `llms.txt` (no redundant fetches)
- Topic matching with KG metadata disambiguation
- Routing to the correct guide via topic `index.md`
- Fetching the specific guide content

Do NOT fetch `llms.txt` or dev-guides URLs directly — the navigator does this with caching and disambiguation.

### 3. Extract Applicable Patterns

From all loaded sources (methodology refs + navigator results), identify:
- Patterns that apply to current feature
- Checklists to follow
- Warnings or anti-patterns
- Recommended approaches

### 4. Add to Architecture

Use `Edit` to add references section to architecture file:

```markdown
## Development References

### Plugin References (Methodology)
| Reference | Key Patterns |
|-----------|--------------|
| solid-drupal.md | Single responsibility, DI |
| library-first.md | Service → Form → Route |
| tdd-workflow.md | Red-Green-Refactor |

### Dev-Guides Applied (via Navigator)
| Topic | Key Decisions |
|-------|--------------|
| drupal/forms/ | ConfigFormBase vs FormBase |
| drupal/entities/ | Content entity vs config entity |

### Enforcement Points
| Phase | Principle | Source |
|-------|-----------|--------|
| Design | Library-First | references/library-first.md |
| Design | SOLID | references/solid-drupal.md |
| Design | Drupal patterns | dev-guides (via navigator) |
| Implement | TDD | references/tdd-workflow.md |
| Implement | DRY | references/dry-patterns.md |
| Complete | Quality Gates | references/quality-gates.md |
| Complete | Security | dev-guides drupal/security/ |
```

### 5. Summarize

Tell user what was integrated from each source: plugin methodology and dev-guides topics.

## Reference Locations

| Type | Location |
|------|----------|
| Plugin references (methodology) | `{plugin_path}/references/*.md` |
| Dev-guides (online) | Via `dev-guides-navigator` skill |

## Stop Points

STOP and ask user:
- Before adding patterns that conflict with existing architecture
