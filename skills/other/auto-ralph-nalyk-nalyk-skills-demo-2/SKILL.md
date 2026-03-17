---
name: auto-ralph
description: >-
  PROACTIVELY activates for ANY task with clear success criteria.
  This skill should be used when the user provides tasks like:
  "fix the bug", "add tests", "implement feature X", "refactor Y".

  Explicit triggers: "ralph this", "auto ralph", "loop it", "iterate".

  Auto-detects Ralph-suitable tasks (score >= 3/4):
  - Clear success criteria (tests pass, error gone, feature works)
  - Benefits from iteration (not one-shot)
  - Well-defined scope (specific files/functions)
  - Verifiable completion (can honestly output promise)

  Does NOT activate for: explanations, questions, vague requests.

  Output: Romanian. Input: Any (ro/en/ru/mixed).
---

# auto-ralph

Skill proactiv care detectează automat task-uri potrivite pentru Ralph Loop și le execută.

## Prefix de Activare (OBLIGATORIU)

**Când skill-ul activează, PRIMUL lucru afișat trebuie să fie:**

```
(AUTONALYK) ═══════════════════════════════════
  Task detectat: [tip task]
  Scor: [X]/4 → [Ralph mode / Normal mode]
═══════════════════════════════════════════════
```

**Exemple:**
```
(AUTONALYK) ═══════════════════════════════════
  Task detectat: bug fix
  Scor: 4/4 → Ralph mode
═══════════════════════════════════════════════
```

```
(AUTONALYK) ═══════════════════════════════════
  Task detectat: întrebare
  Scor: 1/4 → Normal mode
═══════════════════════════════════════════════
```

**De ce prefix:**
- Utilizatorul știe imediat că skill-ul a activat
- Transparență totală despre decizia scoring
- Debugging ușor dacă ceva merge prost

## Faza 0: Verificare Loop Activ (OBLIGATORIU - P0 FIX)

**ÎNAINTE de orice scoring, verifică dacă Ralph Loop e deja activ:**

```bash
if [[ -f ".claude/ralph-loop.local.md" ]]; then
    # STOP - nu porni alt loop!
fi
```

**Dacă loop activ:**
```
(AUTONALYK) ═══════════════════════════════════
  ⚠️  Ralph Loop DEJA ACTIV!
  Iterația curentă: [citește din fișier]

  Opțiuni:
  1. Așteaptă să termine
  2. /cancel-ralph pentru a opri
  3. Adaugă cerința la loop-ul curent (manual)
═══════════════════════════════════════════════
```

**NU încerca să pornești al doilea loop - va corupe starea!**

## Workflow Automat

```
USER INPUT → CHECK ACTIVE LOOP → SCORING → (>= 3?) → CONTEXT → PROMPT → CONFIRM → EXECUTE
                    ↓                         ↓
              (loop activ?)              (< 3?) → RĂSPUNS NORMAL
                    ↓
              AVERTIZARE + STOP
```

**ZERO întrebări până la confirmarea finală.**

## Faza 1: Scoring Automat

Calculează scor 0-4 pentru fiecare task:

| Criteriu | +1 punct dacă |
|----------|---------------|
| Criterii clare | Keywords pozitive detectate (vezi tabel mai jos) |
| Iterație utilă | Bug fix, feature, refactor (nu întrebări) |
| Scop definit | Fișiere/funcții specificate |
| Verificabil | Teste disponibile sau eroare concretă |

### Keywords Multilingve (P1 FIX)

**IMPORTANT:** Recunoaște keywords în TOATE limbile:

| Limba | Keywords Pozitive (+1) | Keywords Negative (0) |
|-------|------------------------|----------------------|
| **EN** | fix, repair, add, implement, create, build, test, refactor | explain, help, what, why, how, understand |
| **RO** | repară, fixează, adaugă, implementează, creează, fă, fă-mi, testează, refactorizează | explică, ce face, cum, de ce, ajută-mă |
| **RU** | исправь, добавь, создай, сделай, протестируй, рефактор | объясни, что, как, почему, помоги |

**Exemple:**
- "fă-mi un API" → "fă-mi" = RO pentru "make me" → +1 criteriu clar
- "repară bug-ul" → "repară" = RO pentru "fix" → +1 criteriu clar
- "ce face funcția?" → "ce face" = întrebare → 0 puncte

**Decizie:**
- Scor >= 3 → AUTO-RALPH
- Scor < 3 → Răspuns normal Claude

## Faza 1.5: Pre-Analiză cu Explore Agent (OPȚIONAL)

**Când să folosești Explore ÎNAINTE de Ralph Loop:**

| Scor | Task Type | Explore? | Motiv |
|------|-----------|----------|-------|
| 4/4 | Bug fix cu stack trace clar | NU | Direct Ralph - context evident |
| 4/4 | Refactor >500 linii | DA | Mapează dependențe înainte |
| 3/4 | Feature în cod necunoscut | DA | Înțelege arhitectura |
| 3/4 | Test funcție izolată | NU | Scop mic, direct Ralph |

**Regula simplă:** Explore când ai nevoie să înțelegi structura ÎNAINTE de a modifica.

### Template-uri Explore

**Bug Fix Explore:**
```
Task(subagent_type="Explore", prompt="Investigate [ERROR]: 1) Find source file, 2) Map call chain, 3) Identify related tests, 4) Find similar patterns")
```

**Feature Explore:**
```
Task(subagent_type="Explore", prompt="Plan feature [NAME]: 1) Find similar implementations, 2) Map integration points, 3) Identify test patterns, 4) Check config files")
```

**Refactor Explore:**
```
Task(subagent_type="Explore", prompt="Analyze [TARGET]: 1) Find all usages, 2) Map dependencies, 3) Assess test coverage, 4) Identify risk areas")
```

Vezi `references/explore-patterns.md` pentru template-uri complete și exemple.

## Faza 2: Detecție Context

Rulează `${CLAUDE_SKILL_DIR}/scripts/detect-context.sh [directory]` pentru:
- Git status (fișiere modificate)
- Framework test disponibil (sau `NO_TESTS_DETECTED`)
- Erori recente (npm, yarn, pytest, generic logs)
- Structură proiect
- **Docker status** (P2 FIX) - docker-compose, containere, logs

**Notă:** Scriptul verifică automat dacă `jq` e instalat și afișează instrucțiuni dacă lipsește.

## Faza 3: Generare Prompt

Selectează template din `references/prompt-patterns.md`:
- Bug fix → Pattern bug-fix
- Feature → Pattern feature
- Test → Pattern test
- Refactor → Pattern refactor
- Generic → Template general

Template include:
- Task-ul original (în limba userului)
- Context detectat
- Criterii de succes auto-inferate
- Promise: `<promise>GATA</promise>`
- Reminder: `/cancel-ralph` pentru anulare

## Faza 4: Confirmare (SINGURA ÎNTREBARE)

Prezintă prompt-ul generat și întreabă:

```
Prompt generat pentru Ralph Loop:
────────────────────────────────
[preview prompt]
────────────────────────────────

Execut? (max 25 iterații)
[Da - Recomandat] [Modifică prompt] [Nu]
```

## Faza 5: Execuție

Dacă "Da":
```bash
/ralph-loop "<prompt>" --max-iterations 25 --completion-promise "GATA"
```

## Reguli Limbă

- **Output:** MEREU Română
- **Input:** Acceptă orice (ro/en/ru/mixed) fără întrebări
- **Promise:** "GATA" (standard)

Exemplu:
```
User: "fix the auth bug, нужно чтобы работал login"

(AUTONALYK) ═══════════════════════════════════
  Task detectat: bug fix
  Scor: 4/4 → Ralph mode
═══════════════════════════════════════════════

Generez prompt...
```

## Triggers Explicite (override scoring)

Activare forțată Ralph:
- "ralph this", "auto ralph", "loop it"
- "iterate", "keep trying", "until done"

Dezactivare forțată:
- "just answer", "don't loop"
- "explain first", "one time"

## Resurse

- **`references/detection-rules.md`** - Reguli complete scoring
- **`references/prompt-patterns.md`** - Template-uri prompt
- **`scripts/detect-context.sh`** - Script detecție context
- **`examples/`** - Exemple prompt-uri generate

## Exemple Rapide

### Task potrivit (scor 4)
```
User: "fix the failing tests in auth module"

(AUTONALYK) ═══════════════════════════════════
  Task detectat: bug fix (teste)
  Scor: 4/4 → Ralph mode
═══════════════════════════════════════════════

Detectez context... [git, teste, erori]
Generez prompt...

Prompt generat pentru Ralph Loop:
────────────────────────────────
[preview]
────────────────────────────────

Execut? (max 25 iterații) [Da/Modifică/Nu]
```

### Task nepotrivit (scor 1)
```
User: "ce face funcția asta?"

(AUTONALYK) ═══════════════════════════════════
  Task detectat: întrebare/explicație
  Scor: 1/4 → Normal mode
═══════════════════════════════════════════════

[Răspuns normal Claude, fără Ralph]
```

## Safety

1. **Max iterations** - Default 25, MEREU setat
2. **Confirmare** - Un click "Da" înainte de execuție
3. **Escape** - `/cancel-ralph` menționat în fiecare prompt
4. **Promise onestă** - Instrucțiuni clare să NU mintă

## Anti-Patterns (CE NU FACE)

- NU întreabă despre limbă
- NU întreabă "quick sau thorough"
- NU cere clarificări inutile
- NU execută fără confirmare finală
- NU ignoră scor < 3 (răspunde normal)

## Settings Persistence

Auto-ralph citește configurația din `~/.claude/auto-ralph.local.md`:

### Structură Settings File

```yaml
---
max_iterations: 25
score_threshold: 3
skip_explore_for_score: 4
default_language: ro
auto_execute: false
docker_analysis: true
---

# Notes
Any markdown notes here.
```

### Parametri Disponibili

| Parametru | Default | Descriere |
|-----------|---------|-----------|
| `max_iterations` | 25 | Iterații maxime Ralph Loop |
| `score_threshold` | 3 | Scor minim pentru Ralph mode |
| `skip_explore_for_score` | 4 | Scor la care se sare peste Explore |
| `default_language` | ro | Limba output (ro/en/ru) |
| `auto_execute` | false | true = fără confirmare finală |
| `docker_analysis` | true | Include Docker în context detection |

### Override

Parametrii expliciți din comandă au prioritate peste settings:
```
User: "ralph this cu max 50 iterații"
→ Override max_iterations=50, ignoră settings
```

### Citire Settings

Script-ul `detect-context.sh` include funcție `read_settings()`:
```bash
read_settings() {
    local sf="$HOME/.claude/auto-ralph.local.md"
    if [[ -f "$sf" ]]; then
        sed -n '/^---$/,/^---$/p' "$sf" | grep -v '^---$'
    fi
}
```
