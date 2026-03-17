---
name: best-practices-skills
description: >
  Best practices for designing and structuring agent skills: SKILL.md frontmatter rules,
  triggers, progressive disclosure, and when to use scripts vs references.
triggers:
  - best practices skills
  - skill structure
  - skill design
  - skill frontmatter
  - skill template
  - skill checklist
metadata:
  short-description: Skill structure and design patterns
provides:
  - skill-validation
  - skill-scaffolding
  - composition-rules
composes:
  - task-monitor

taxonomy:
  - validation
  - compliance
  - composition
---

# Skills Best Practices

Use this skill when creating or reviewing skills under `.pi/skills/`.

## ArangoDB Access Policy (NON-NEGOTIABLE)

- `/memory` is the ONLY skill that accesses ArangoDB directly
- `/ops-arango` handles admin ops (backups, indexes, migrations)
- `monitor-memory` has read-only exception for health probes (documented)
- ALL other skills MUST use `memory/run.sh` subcommands:
  - `memory recall` — semantic + BM25 search
  - `memory learn` — store lessons/data
  - `memory sample` — random document sampling
  - `memory tag` — post-insert tag stamping
  - `memory count` — collection statistics
  - `memory archive-session` — episodic archival
- NEVER: `from arango import ArangoClient`
- NEVER: `sys.path.insert(0, MEMORY_PATH)`
- NEVER: hardcoded passwords or raw `/_api/cursor` calls

## Storage Policy (NON-NEGOTIABLE)

**The root NVMe is for CODE ONLY.** All heavy artifacts MUST live on the 12TB drive
and be symlinked back. This is enforced by `/skills-broadcast` and `/ops-workstation`.

### What MUST be on `/mnt/storage12tb`

| Category | Examples | Storage Path |
|----------|----------|--------------|
| **Model weights** | `.safetensors`, `.gguf`, `.bin`, `.pt` | `/mnt/storage12tb/skills/<skill-name>/models/` |
| **Training logs** | RVC logs, checkpoints, tensorboard | `/mnt/storage12tb/skills/<skill-name>/logs/` |
| **Extracted data** | `extracted_runs/`, PDF extractions | `/mnt/storage12tb/skills/<skill-name>/extracted_runs/` |
| **Generated outputs** | batch results, GRPO outputs | `/mnt/storage12tb/skills/<skill-name>/outputs/` |
| **Datasets** | training data, WAV files, corpora | `/mnt/storage12tb/skills/<skill-name>/data/` |
| **Work dirs** | temp processing, intermediate files | `/mnt/storage12tb/skills/<skill-name>/work/` |
| **Backups** | `.backups/`, snapshots | `/mnt/storage12tb/backups/<project>/` |

### What MUST NEVER be synced by `/skills-broadcast`

These directories are **excluded from rsync** and must not exist as real directories
in skill folders (only as symlinks to `/mnt/storage12tb/`):

`.venv`, `node_modules`, `__pycache__`, `models`, `rvc`, `outputs`, `logs`, `data`,
`pods`, `extracted_runs`, `work`, `weights`, `checkpoints`, `artifacts`, `sessions`,
`papers`, `datasets`, `*.safetensors`, `*.gguf`, `*.bin`, `*.pt`

### How to set up a new heavy artifact directory

```bash
# 1. Create the storage location on 12TB drive
mkdir -p /mnt/storage12tb/skills/<skill-name>/models

# 2. Move existing data (if any)
mv /path/to/skill/models/* /mnt/storage12tb/skills/<skill-name>/models/

# 3. Remove the directory and create symlink
rmdir /path/to/skill/models
ln -s /mnt/storage12tb/skills/<skill-name>/models /path/to/skill/models
```

### Enforcement

- `/skills-broadcast sanity` FAILS if any skill has non-symlinked dirs >100MB
- `/ops-workstation slim` reports storage policy violations
- `.gitignore` in every skill should exclude heavy artifact patterns

## Required structure

- A skill is a folder with a required `SKILL.md` at the root.
- `SKILL.md` must start with YAML frontmatter (no code fences).
- Frontmatter delimiters must be standalone lines: opening `---` on line 1 and closing `---` on its own line.
- Frontmatter must include `name` and `description`.
- The `description` should contain explicit trigger contexts (what users will say).
- Keep `SKILL.md` concise; move large content into `references/` or `scripts/`.
- Avoid extra docs (README/CHANGELOG) inside the skill folder.

## Composition Frontmatter (Valence Shell)

Skills are like chemical elements — they bind to each other through defined interfaces.
The `provides:` and `composes:` frontmatter fields declare a skill's **valence shell**:
what it offers to others and what it needs from others.

### Required composition fields

```yaml
---
name: my-skill
description: >
  What this skill does and trigger phrases.
triggers:
  - natural language phrase users will say
  - another trigger phrase
provides:
  - capability-a       # What this skill outputs/offers
  - capability-b
composes:
  - memory             # Skills this delegates to (by name)
  - scillm
  - extractor
---
```

### Field definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `triggers` | list[str] | **Yes** | Natural-language phrases users will say. Parsed at runtime by `skill-selector` extension for BM25-style matching. Skills without triggers are invisible to implicit routing. |
| `provides` | list[str] | Yes | Capabilities this skill makes available. Used by `/skill-lab` gap detector. |
| `composes` | list[str] | Yes | Skills this skill delegates to via subprocess/import. Empty list `[]` if self-contained. Parsed at runtime by `skill-selector` extension for dependency expansion — when a skill is selected, its `composes` deps are automatically included in context. |
| `taxonomy` | list[str] | Recommended | Federated taxonomy bridge tags for multi-hop discovery via `/memory`. Uses standard vocabulary: `precision`, `resilience`, `fragility`, `corruption`, `loyalty`, `stealth`, plus domain tags. |

### Runtime consumption (skill-selector extension)

The `.pi/extensions/skill-selector.ts` extension reads frontmatter at session start:

- **`triggers`** → Built into an inverted token index. When users type natural language
  (no `/skill-name` ref), the extension scores the prompt against triggers+descriptions
  to select relevant skills. **Skills without triggers are invisible to implicit routing.**
- **`composes`** → Parsed into a dependency map. When a skill is selected (explicitly or
  via trigger match), all its `composes` dependencies are automatically pulled into context.
  This replaced a hardcoded static map (Feb 2026) — the extension now reads live frontmatter.
- **`provides`** → Used by `/skill-lab` for gap detection and capability graph traversal.
  Not yet consumed by skill-selector (future: reverse-index for "I need X capability" queries).

### Binding affinity rules

1. **Skills MUST declare all skills they delegate to** in `composes:`.
2. **Skills MUST declare what they output** in `provides:`.
3. **Self-contained skills** (no external dependencies) use `composes: []`.
4. **Lab skills** (prompt-lab, gpt-lab, classifier-lab) are **catalysts** — they
   create new skills without being consumed. They `provide: [skill-creation]`.
5. **Composite skills** are molecules — stable combinations of existing skills
   wired together by a thin orchestrator.

### Capability vocabulary (standardized provides values)

| Capability | Skills that provide it |
|------------|----------------------|
| `llm-completion` | scillm, codex |
| `embedding` | embedding |
| `memory-recall` | memory |
| `memory-learn` | memory |
| `web-search` | brave-search, dogpile |
| `pdf-extraction` | extractor, review-pdf |
| `security-scan` | hack, security-scan |
| `skill-creation` | prompt-lab, gpt-lab, classifier-lab |
| `skill-validation` | skills-ci, best-practices-skills |
| `competitive-selection` | battle |
| `hardening` | anvil |
| `docker-isolation` | battle, hack |
| `human-interview` | interview |
| `task-planning` | plan |
| `task-orchestration` | orchestrate |
| `taxonomy-tagging` | taxonomy |
| `progress-tracking` | task-monitor |

New capabilities should be added to `references/capability_vocabulary.yml`.

### Graph Registration (Multi-Hop Discovery)

Skills SHOULD be registered in `/memory` as nodes in the knowledge graph.
This enables multi-hop traversal — when `/skill-lab` needs a capability,
it can traverse `composes` edges to find transitive dependencies, just like
`/memory` traverses `relates_to` edges for knowledge discovery.

```
skill:extractor ──composes──► skill:memory
                 ──composes──► skill:scillm
                 ──provides──► capability:pdf-extraction

skill:learn-datalake ──composes──► skill:extractor
                      ──composes──► skill:review-pdf
                      ──composes──► skill:memory
```

This is analogous to chemical bonding — the graph reveals which elements
naturally form molecules. `/taxonomy` tags provide the bridge keywords
that enable cross-domain discovery (a security skill and an extraction skill
might share `taxonomy:validation` tags).

Registration pattern:
```python
from common.memory_client import learn, MemoryScope

# Register skill as a knowledge node
learn(
    problem=f"What does {skill_name} provide?",
    solution=f"Provides: {', '.join(provides)}. Composes: {', '.join(composes)}",
    scope=MemoryScope.OPERATIONAL,
    tags=["skill_registry", skill_name] + provides,
)
```

### Machine-parseable rules

See `references/rules.yml` for the complete machine-parseable rule set
that `/skills-ci` and `/skill-lab` validate against.
See `references/composition_manifest.yml` for the schema `/skill-lab` uses
when planning new composite skills.
Run `./sanity.sh` in this skill to enforce the strict frontmatter gate across all skills.

## Design patterns

1. **Progressive disclosure**
   - Layer 1: Frontmatter (`name`, `description`) for routing.
   - Layer 2: `SKILL.md` body for the workflow map.
   - Layer 3: `scripts/`, `references/`, `assets/` for details on demand.

2. **Guardrails vs freedom**
   - High-variance tasks: instructions only.
   - Fragile/repetitive tasks: scripts with parameters.
   - Mixed tasks: decision tree in `SKILL.md` + references/scripts.

3. **Single source of truth**
   - Put schemas, long examples, and variants in `references/`.
   - `SKILL.md` should point to references, not duplicate them.

## Checklist (creation/review)

- Frontmatter is valid YAML (no markdown fences).
- Frontmatter has opening and closing `---` on standalone lines.
- `name` matches the directory name.
- `description` contains clear trigger phrases, uses YAML fold syntax (`>`) — **never inline**.
- **`triggers`** list contains natural-language phrases users will say. **Required** — skills without triggers are invisible to implicit routing via skill-selector.
- **`provides`** list declares capabilities this skill outputs. **Required.**
- **`composes`** list declares all skills this delegates to. **Required** (use `[]` if self-contained). Parsed at runtime for automatic dependency inclusion.
- `run.sh` exists only if the skill needs execution.
- `sanity.sh` exists if the skill runs non-trivial scripts.
- **CLI: Typer only** — all Python CLIs use `typer`. NEVER `argparse` or `click`.
- **No bespoke reimplementations** — if a helper skill exists, the new skill delegates to it.
- **PyYAML dependency** — any script that parses SKILL.md frontmatter MUST depend on
  `pyyaml` (not a fallback regex parser). The `>` and `|` YAML block scalars, nested
  objects, and multi-line strings are only reliably parsed by a real YAML parser.

## Anti-patterns

- Missing or fenced frontmatter.
- Overlong `SKILL.md` that duplicates references.
- Multiple README/CHANGELOG files inside a skill.
- Hidden dependencies or undocumented environment assumptions.
- **Rolling your own YAML parser** — use `pyyaml`. Minimal/fallback parsers silently
  break on `>` fold syntax, `|` literal blocks, nested dicts, and quoted strings.
  The `/skill-lab` scan_soup.py bug (Feb 2026) caused ALL 166 skill descriptions to
  register as empty `[]` in `/memory` because the fallback parser treated `>` as a
  list indicator. This made capability-aware routing useless — BM25 couldn't match
  task queries to skills because the description field was blank.
- **Reimplementing helper skills** — if a helper skill already exists, import/call it
  instead of writing bespoke code. Skills compose, not duplicate. Key delegations:
  - YouTube ops → `ingest-youtube` (search, download, transcripts, IPRoyal rotation)
  - Stem separation → `create-stems`
  - LLM completions → `scillm`
  - Embeddings → `embedding`
  - Web search → `brave-search`, `dogpile`
  - PDF extraction → `extractor`
  - Memory recall/learn → `memory`
- **Using argparse or click** — all Python CLIs use `typer`. Argparse and click are banned.
  The codebase has been fully migrated (Feb 2026). Do not re-introduce them.
- **Missing dotenv loading** — any `.py` file that calls `os.getenv()` MUST load `.env`
  at module level before the first call. Use `dotenv_helper.load_env()` or the inline
  `load_dotenv(find_dotenv(usecwd=True), override=False)` pattern. See
  `best-practices-python/rules/conventions-dotenv-required.md` for details.
- **Incomplete pyproject.toml dependencies** — every `import` in a skill's `.py` files
  MUST have a corresponding entry in `pyproject.toml` `[project.dependencies]`. After
  adding/modifying any Python file, cross-check imports against declared deps. Run
  `uv sync && uv run python -c "import <module>"` to verify. This is a hard gate —
  missing deps cause `ModuleNotFoundError` after venv recreation, a silent regression
  that only surfaces when the skill runs in isolation or after `/skills-broadcast`.

---

# Runtime Integration Patterns

These patterns ensure skills integrate well with the broader agent ecosystem.

## Task-Monitor Integration (MANDATORY — No Exceptions)

**ALL skills MUST report to `/task-monitor`.** This is non-negotiable. Every skill — whether batch, nightly, one-shot, or continuous — must start a session, report accomplishments, and end the session. Without task-monitor integration, skill execution is invisible: failures go undetected, progress is unmeasured, and the system cannot self-diagnose.

Skills that process multiple items should additionally report per-item progress.

### Minimum Pattern: Session Start/End (ALL skills)

Every skill must at minimum call `start-session` and `end-session`:

```python
import subprocess
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent
TM_RUN = SKILLS_DIR / "task-monitor" / "run.sh"

def _tm(args: list[str]) -> bool:
    if not TM_RUN.exists():
        return False
    try:
        return subprocess.run(
            [str(TM_RUN), *args],
            capture_output=True, text=True, timeout=30,
        ).returncode == 0
    except Exception:
        return False

# At start of any run:
_tm(["start-session", "--project", "my-skill"])

# After each meaningful phase:
_tm(["add-accomplishment", "--text", "Phase 1: processed 42 items"])

# At end of run:
_tm(["end-session", "--notes", "Completed successfully: 42 items processed"])
```

### Pattern: task_monitor_client.py (Batch Operations)

For skills that process multiple items, create a `task_monitor_client.py` that additionally:

1. Registers tasks in `~/.pi/task-monitor/registry.json`
2. Writes state to `<skill_name>_task_state.json`
3. Updates progress per item (not just on completion)

```python
# task_monitor_client.py - Minimal structure
from pathlib import Path
import json, time, os
from datetime import datetime

TASK_MONITOR_REGISTRY = Path.home() / ".pi" / "task-monitor" / "registry.json"
STATE_FILE = Path(__file__).parent / "my_skill_task_state.json"

class MySkillTaskClient:
    def __init__(self, task_name: str, total_items: int):
        self.task_name = task_name
        self.total_items = total_items
        self.completed = 0
        self.start_time = time.time()
        self._register_task()
        self._write_state()

    def _register_task(self):
        # Register in ~/.pi/task-monitor/registry.json
        registry = {}
        if TASK_MONITOR_REGISTRY.exists():
            registry = json.loads(TASK_MONITOR_REGISTRY.read_text())
        registry[f"my-skill:{self.task_name}"] = {
            "state_file": str(STATE_FILE),
            "total": self.total_items,
            "project": "my-skill",
        }
        TASK_MONITOR_REGISTRY.write_text(json.dumps(registry, indent=2))

    def _write_state(self, final=False):
        # Write state atomically
        state = {
            "completed": self.completed,
            "total": self.total_items,
            "progress_pct": round(self.completed / self.total_items * 100, 1),
            "status": "completed" if final else "running",
        }
        tmp = STATE_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, indent=2))
        os.replace(tmp, STATE_FILE)

    def update(self, **metrics):
        self.completed += 1
        self._write_state()

    def finish(self):
        self._write_state(final=True)
```

### State File Schema (Minimum)

```json
{
  "completed": 50,
  "total": 100,
  "progress_pct": 50.0,
  "status": "running",
  "last_updated": "2026-02-04 08:30:00"
}
```

### CLI Integration

Add these options to batch commands:

| Option                             | Default | Description                 |
| ---------------------------------- | ------- | --------------------------- |
| `--task-monitor/--no-task-monitor` | true    | Enable/disable task-monitor |
| `--json-stream`                    | false   | NDJSON output per item      |

## NDJSON Streaming (Required for Long-Running Batch)

Skills with batch operations MUST support `--json-stream` for real-time progress:

```bash
./run.sh batch items.txt --json-stream | tee results.jsonl

# Each line is valid JSON:
# {"item": "url1", "success": true, "timing_ms": 1234}
# {"item": "url2", "success": false, "error": "timeout"}
```

### Benefits

- Real-time monitoring: `tail -f results.jsonl | jq`
- Resume from partial runs (parse last line for progress)
- Integration with streaming parsers
- Separates progress from final summary

## Self-Correction Loops (Recommended for Validation Tasks)

Skills that validate LLM outputs SHOULD implement self-correction:

### Pattern: Send Invalid Back to LLM

```
1. Call LLM with vocabulary/schema in prompt
2. Validate response (Pydantic, JSON schema, etc.)
3. If invalid:
   a. Send correction message: "Invalid tags: X. Valid options: Y"
   b. Ask LLM to fix
   c. Track correction rounds
4. Record metrics: corrections_needed, correction_success_rate
```

### Example Correction Prompt

```
Your response contained invalid values.

Invalid: {rejected_values}
Valid options: {allowed_vocabulary}

Please correct your response. Return ONLY valid JSON with values from the allowed list.
```

### Strategy Exhaustion (Alternative Pattern)

For fetch/extraction skills, use strategy exhaustion instead:

```
1. Try learned strategy from /memory (if exists)
2. Try default strategies in order
3. On success: store winning strategy to /memory
4. On all fail: trigger /interview for human help
```

## Quality Gates (Required for Validation Tasks)

Skills that validate outputs MUST define quality gates with thresholds:

### LLM Non-Determinism Tolerance

Use 99.5% thresholds instead of 100% to account for LLM non-determinism:

```python
# Bad: Fails on any imperfection
if success_rate < 1.0:
    raise QualityGateFailed()

# Good: Tolerates LLM variance
if success_rate < 0.995:  # 99.5%
    raise QualityGateFailed()
```

### Gate Metrics Pattern

Track pass/fail per gate:

```python
@dataclass
class GateMetrics:
    passed: int = 0
    failed: int = 0

    @property
    def rate(self) -> float:
        total = self.passed + self.failed
        return self.passed / total if total > 0 else 1.0
```

## Memory Integration (Recommended)

Skills that learn from experience SHOULD integrate with `/memory`:

### Pattern: Learn from Success

```python
# On successful operation
from memory_bridge import learn_strategy

result = try_operation(url)
if result.success:
    learn_strategy(
        url=url,
        strategy_used=result.winning_strategy,
        timing_ms=result.timing_ms,
    )
```

### Pattern: Recall Before Try

```python
# Before trying default approach
from memory_bridge import get_best_strategy

learned = get_best_strategy(url)
if learned:
    # Try learned strategy first
    result = try_strategy(url, learned.strategy)
```

## Human-in-the-Loop (Recommended for Unrecoverable Failures)

Skills with automated workflows SHOULD integrate with `/interview` for human collaboration:

### When to Trigger Interview

- All automated strategies exhausted
- Ambiguous input that needs clarification
- Decision point with significant consequences

### Interview Integration Pattern

```python
from interview_generator import generate_interview

if all_strategies_failed:
    interview = generate_interview(
        context={"url": url, "errors": errors},
        questions=[
            "Do you have credentials for this site?",
            "Should we try a mirror URL?",
            "Skip this URL?",
        ]
    )
    # Write interview JSON for /interview skill
```

---

## Minimal template

```markdown
---
name: example-skill
description: >
  One-sentence description with trigger phrases (what users will ask for).
---

# Example Skill

Short workflow map here. Link to references/scripts as needed.
```

## Batch Skill Template

For skills with batch operations, include these sections in SKILL.md:

```markdown
## Task-Monitor Integration

skill-name integrates with task-monitor for live progress tracking:

\`\`\`bash

# Run with task-monitor (enabled by default)

./run.sh batch items.txt

# View progress

cat skill_name_task_state.json | jq
\`\`\`

## NDJSON Streaming

\`\`\`bash
./run.sh batch items.txt --json-stream | tee results.jsonl
\`\`\`
```
