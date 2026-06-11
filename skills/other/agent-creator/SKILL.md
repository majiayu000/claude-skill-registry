---
name: agent-creator
description: "Scaffold vexjoy-agent operator .md files: frontmatter, routing block, operator context, reference loading table, phase/gate workflow."
routing:
  triggers:
    - create agent
    - new agent
    - scaffold agent
    - agent template
    - build agent
    - agent design
    - make agent
  force_route: true
  not_for: "creating real estate agents, ML agents, OS agents (e.g. SNMP), travel agents, customer service agents — only for vexjoy-agent .md operator files"
  pairs_with:
    - skill-creator
    - agent-evaluation
  complexity: Medium
  category: meta
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - Glob
  - Grep
user_invocable: false
---

# Agent Creator

Scaffold correctly-formed vexjoy-agent operator `.md` files. An agent file is a system-prompt contract: it sets identity, constraints, expertise, and routing — not application code.

Phases: **DISCOVER → DESIGN → SCAFFOLD → REGISTER → VALIDATE**

---

## Phase 1 — DISCOVER

Check for domain overlap before creating anything.

```bash
grep -i "<domain-keyword>" agents/*.md | grep "^agents/" | cut -d: -f1 | sort -u
ls agents/ | grep "<domain-prefix>"
```

Gate 1: If an existing agent covers the domain, add a `references/` file to that agent instead of creating a new one. Proceed only when no existing agent covers the domain, or the user confirms after seeing the overlap.

Read `docs/PHILOSOPHY.md` before proceeding — the philosophy governs operator context structure, progressive disclosure, positive framing, and tool restrictions. Components that violate it will fail CI.

---

## Phase 2 — DESIGN

Decide the agent's identity and routing contract before writing a single line.

| Decision | Question to answer |
|----------|--------------------|
| Role type | Reviewer/auditor, code modifier/engineer, or orchestrator? |
| Allowed tools | Matches role: reviewers→Read/Glob/Grep; engineers→+Edit/Write/Bash; orchestrators→Read/Agent/Bash |
| Complexity | Low (single-file, read-only), Medium (multi-file, routing), High (full sweeps, orchestration) |
| Triggers | 3–6 specific phrases a user would naturally say — not generic verbs |
| pairs_with | 2–3 agents commonly co-dispatched; verify each exists on disk before listing |
| Reference files | Domains needing depth — each goes in `agents/{name}/references/` loaded on demand |
| Description craft | Intent verb + domain object, 2–3 adjacent terms, one false-positive boundary clause with redirect |
| Activation cases | 3 should-trigger / 2 should-not-trigger / 2 near-miss phrases drafted now, saved at scaffold time |

Load `references/agent-design-patterns.md` for operator context structure, hook design, routing design, authority/trust framing, and smells-to-rewrite guidance.

Load `references/agent-eval-design.md` when drafting the description and activation cases — the case classes and worked example live there.

Gate 2: All eight decisions answered before writing agent file content.

---

## Phase 3 — SCAFFOLD

Write the agent file using the annotated template.

Load `references/agent-frontmatter-template.md` for the complete template with all required fields and valid values.

**File layout:**

```
agents/
├── {agent-name}.md          # operator file — the system prompt contract
└── {agent-name}/
    ├── references/
    │   └── *.md             # deep context, loaded on demand
    ├── SPEC.md              # optional: contract for complex/high-impact agents
    └── EVAL.md              # optional: repeatable eval cases
```

**Writing the operator context** (body after frontmatter):

1. Role statement: what the agent does, what domain it owns
2. Expertise list: concrete capabilities with specific sub-skills
3. Mandatory pre-action protocol: what to read before acting and why
4. Operator context block: hardcoded behaviors, default behaviors (ON), optional behaviors (OFF)
5. Capabilities and limitations table: CAN / CANNOT with agent suggestions for out-of-scope requests
6. Reference loading table: `| Signal | Load These Files | Why |` — required when a `references/` directory exists
7. Workflow section: phase-by-phase with gates
8. Error handling: cause/solution pairs for common failures
9. Preferred patterns: what good looks like (positive framing)
10. Anti-rationalization table: common rationalizations with required action

**Positive framing (CI gate):** Every instruction tells the reader what to do. Run the check after writing:

```bash
python3 scripts/validate_positive_instruction_docs.py
```

Exit code 1 means violations. Rewrite flagged instructions in action form before proceeding.

**Progressive disclosure:** Main agent file stays navigable. Deep reference material goes in `{agent-name}/references/` loaded on demand. If the file exceeds 600 lines, extract content to `references/` first.

Gate 3: Agent file written, YAML frontmatter parses cleanly:

```bash
python3 -c "import yaml; yaml.safe_load(open('agents/{agent-name}.md').read().split('---')[1]); print('OK')"
```

---

## Phase 4 — REGISTER

Add the agent to the routing index.

```bash
python3 scripts/generate-agent-index.py
```

Verify the count increased by exactly one:

```bash
python3 -c "
import json
d = json.load(open('agents/INDEX.json'))
agents = d.get('agents', [])
print(f'Registered agents: {len(agents)}')"
```

Gate 4: `agents/INDEX.json` contains the new agent entry. The router cannot discover unregistered agents.

---

## Phase 5 — VALIDATE

Run all validation checks before declaring the agent shippable.

```bash
# Structural checks: filenames, frontmatter, line counts, loading tables
python3 scripts/validate-references.py --agent {agent-name}

# Positive framing gate (scans all tracked .md files)
python3 scripts/validate_positive_instruction_docs.py

# YAML parse
python3 -c "import yaml; yaml.safe_load(open('agents/{agent-name}.md').read().split('---')[1]); print('YAML OK')"

# Verify pairs_with entries exist on disk
python3 -c "
import yaml, os
txt = open('agents/{agent-name}.md').read()
fm = yaml.safe_load(txt.split('---')[1])
for p in fm.get('routing', {}).get('pairs_with', []):
    exists = os.path.exists(f'agents/{p}.md') or os.path.exists(f'skills/{p}/SKILL.md')
    print(f'  {p}: {\"OK\" if exists else \"MISSING\"}')"
```

Gate 5: All scripts exit 0. No phantom `pairs_with` entries. No positive-framing violations.

**Manual review** (the scripts cannot check these):

- **Description craft**: read the description aloud. Does it state intent, name 2–3 adjacent terms, mark one false-positive boundary? See `references/agent-frontmatter-template.md` Description Craft.
- **Activation cases recorded**: confirm `agents/{name}/references/activation-cases.md` (or equivalent notes section) lists 3 should-trigger / 2 should-not-trigger / 2 near-miss phrases. Mental-pass each phrase against the description. See `references/agent-eval-design.md`.

---

## Error Handling

### YAML parse error on frontmatter
Cause: Unquoted colon in description, or bad indentation in routing block.
Solution: Wrap description in double quotes. Run the YAML parse command above — the traceback pinpoints the line.

### Trigger conflict with existing agent
Cause: Two agents claim the same trigger phrase.
Solution: Run the duplicate detection script in `agents/toolkit-governance-engineer/references/routing-table-patterns.md`. Make this agent's trigger more specific.

### Agent not appearing in routing after INDEX regeneration
Cause: Agent file path not matching the expected pattern, or frontmatter missing `routing.triggers`.
Solution: Confirm file is at `agents/{name}.md`. Confirm `routing.triggers` is a non-empty list.

### Reference loading table missing from validation
Cause: Agent body has no `| Signal | Load These Files | Why |` table.
Solution: Add a reference loading table with at least one row. See `references/agent-design-patterns.md` for the required format.

---

## Preferred Patterns

### Role-matched allowed-tools
Set `allowed-tools` to match what the agent actually does — reviewers read only, engineers write, orchestrators dispatch. This ensures agents stay within their domain and cannot make out-of-scope changes.

### Triggers that match natural speech
Write triggers as phrases a first-time user would naturally say, not internal system identifiers. "fix a bug in Go" routes better than "golang-debugging-invocation".

### Reference loading table as required section
Every agent that has a `references/` directory includes a loading table mapping signals to files. Agents without this table load references eagerly, violating the progressive disclosure principle from `docs/PHILOSOPHY.md`.

### Expertise list over motivational framing
List concrete capabilities the agent has: version-specific idiom tables, failure mode catalogs, concrete commands. Skip "you are an expert in X" — it adds no information the model will act on.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|--------|-----------------|-----|
| operator context structure, reference loading table format, phase/gate pattern, hook design, routing design, authority/trust framing, smells to rewrite | `references/agent-design-patterns.md` | Vexjoy-specific architecture patterns, instruction hierarchy, and rewrite catalog for vague framing |
| frontmatter fields, YAML template, complexity tiers, INDEX.json registration, description craft | `references/agent-frontmatter-template.md` | Complete annotated template with all required fields, valid values, and description-writing guide |
| activation eval, output eval, should-trigger / should-not-trigger / near-miss, routing failure, description tuning | `references/agent-eval-design.md` | How to design activation and output evals at scaffold time so the right agent gets picked and produces correct work |
