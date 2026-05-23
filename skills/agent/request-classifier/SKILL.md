---
name: request-classifier
description: "Classify any user request into a structured format for prompt generation. Use this skill whenever you need to understand what type of task a request represents, determine complexity, decide whether planning is needed, or route a request to the right skills and agent strategy. Trigger on: any request that needs to be analyzed before generating a Claude Code prompt, when someone says 'classify this', 'what kind of task is this', when the prompt-generator or prompt-router skills need input classification, or when deciding between solo agent vs subagent vs tmux team execution."
---

# Request Classifier

Classify a user request into a structured JSON object that downstream skills (prompt-router, prompt-generator) use to decide: what type of task this is, how complex it is, and whether to enter plan mode before generating a Claude Code prompt.

**Read the full taxonomy** at `references/taxonomy.md` before classifying. It contains the complete keyword lists, scoring rules, and decision tree. The sections below give you the process and worked examples.

---

## How to Classify

### Step 1 — Read the request

Extract the raw text of the user's request. If the request is embedded in a longer conversation, focus on the most recent action request, not background context.

### Step 2 — Load the taxonomy

Read `references/taxonomy.md`. Pay attention to:
- The 8 request type definitions and their keyword lists
- The scoring dimensions table in the Complexity Scoring Algorithm section
- The Plan Mode Decision Tree

### Step 3 — Identify the request type

Match keywords and signals against the 8 types in priority order:

1. **pipeline** — check first; graph/node/state/LangGraph signals override other types
2. **bug-fix** — error/crash/failing signals are strong
3. **feature** — "add/implement/create/new" + new capability
4. **improvement** — existing functionality, better/faster/cleaner
5. **research** — investigation/analysis without a code outcome yet
6. **frontend** — UI/component/React/Next.js, no backend involvement
7. **documentation** — docs/README/docstring only
8. **quick-task** — everything else that is small and single-action

When multiple types match, use the priority order above. `pipeline` beats `feature`; `bug-fix` beats `improvement`.

### Step 4 — Score complexity

Use the four scoring dimensions from the taxonomy:
- Word count of the request body
- Number of files/modules mentioned or implied
- Action breadth (single → multiple related → cross-cutting)
- Request type baseline score

Add any amplifiers (contains "across", "all", "entire", cross-backend+frontend). Cap at 10.

Map to level: 1–3 = simple, 4–6 = medium, 7–10 = complex.

### Step 5 — Apply the plan mode decision tree

Check for explicit overrides first ("no plan" → off; "plan first" → on). Then:
- Types [feature, bug-fix, research, improvement, pipeline] → plan ON
- Types [frontend, quick-task, documentation] → plan ON only if complexity >= 7

Select the plan type from the type→plan_type mapping in the taxonomy.

### Step 6 — Output the classification JSON

Emit the JSON using the schema in `references/taxonomy.md`. Every field must be present. Use `null` (not `""`) for absent optional values.

### Step 7 — Handle ambiguity

If two types are plausible and the priority ordering doesn't resolve them clearly, explain your reasoning briefly before the JSON, and optionally ask the user to confirm. Do not silently guess when both interpretations would lead to meaningfully different outcomes.

---

## Edge Cases

**"Fix AND improve"** — When a request bundles a bug fix with an enhancement, pick the primary action. If the fix is driving the request ("the page is broken, and while you're there clean up the CSS"), classify as `bug-fix`. If improvement is primary ("refactor the grid and also fix that one null check"), classify as `improvement`. Note both in `keywords_matched`.

**"Investigate then fix"** — A request that asks for root-cause analysis before fixing is `research` (the research is the deliverable; the fix is implied future work). Example: "Figure out why extractions are timing out and document your findings" = `research`, not `bug-fix`.

**"Frontend feature with new API"** — A feature that requires both a new endpoint and new UI is `feature`, not `frontend`. `frontend` is reserved for UI-only changes with no backend modification.

**"Rename all occurrences across the codebase"** — The word "all" and "across" are amplifiers, but if the action is still mechanical (find/replace a symbol name), it remains `quick-task` with a higher complexity score (score 4–5). A rename is still a rename even if it touches many files.

**"Add docs for X"** — `documentation` even if X is technically complex. The task itself is writing, not engineering.

**"Investigate and then implement"** — Two-part requests: if both parts are non-trivial, classify by the heavier phase. Investigation + implementation = `research` if framed as "figure out the right approach first," or `feature` if the implementation is the dominant concern.

---

## Override Handling

Explicit user preferences in the request text always take precedence over automatic detection.

| User says | Effect |
|-----------|--------|
| "no plan", "skip planning", "just do it", "don't plan" | Force `plan_mode: false`, `plan_type: null` |
| "with planning", "plan first", "plan mode", "think this through" | Force `plan_mode: true`, set plan_type by type |
| "treat this as a quick task" | Override type to `quick-task` |
| "this is complex, treat it accordingly" | Add +2 to complexity score |

Set `override: "on"` or `override: "off"` in the output JSON when an override is detected. Set `override: null` otherwise.

---

## 10 Worked Examples

Each example shows the request, the classification reasoning, and the output JSON.

---

### Example 1 — Quick rename

**Request:** "Rename extract_items to extract_acm_items"

**Reasoning:**
- Type: `quick-task` — "rename" is a primary keyword; 5-word request; single action on a function name
- Complexity: word count <25 (0) + files 1 implied (0) + single action (0) + quick-task baseline (0) = Score 1 (simple)
- Plan mode: quick-task → OFF (complexity < 7)

```json
{
  "request_type": "quick-task",
  "complexity": { "score": 1, "level": "simple", "reasoning": "Single mechanical rename action, one function name across likely 1-2 files." },
  "plan_mode": false,
  "plan_type": null,
  "keywords_matched": ["rename"],
  "files_mentioned": [],
  "domain_signals": ["extraction"],
  "override": null
}
```

---

### Example 2 — Bug fix with stack trace context

**Request:** "The correction node is running on every extraction even when confidence is 100%. Fix it — it's wasting tokens and slowing things down."

**Reasoning:**
- Type: `bug-fix` — "fix" is primary; "running when it shouldn't" is a classic should-but-doesn't signal; "wasting tokens/slowing down" are symptoms
- Complexity: 25–80 words (1) + 2–3 files implied (orchestrator, correct_node) (1) + single action (0) + bug-fix baseline (1) = Score 3 (simple)
- Plan mode: bug-fix → ON, plan type: debug

```json
{
  "request_type": "bug-fix",
  "complexity": { "score": 3, "level": "simple", "reasoning": "Clear bug with a known symptom; likely 2-3 files in the pipeline layer." },
  "plan_mode": true,
  "plan_type": "debug",
  "keywords_matched": ["fix", "running when it shouldn't"],
  "files_mentioned": [],
  "domain_signals": ["pipeline", "langgraph", "extraction"],
  "override": null
}
```

---

### Example 3 — New feature with cross-layer scope

**Request:** "Add a CSV export button to the item grid that calls a new /api/acm/export endpoint and streams the file download using SSE."

**Reasoning:**
- Type: `feature` — "add" + new capability + new endpoint mentioned
- Complexity: 25–80 words (1) + 5+ files (frontend component, hook, store, backend router, service) (3) + cross-cutting backend+frontend (2) + feature baseline (2) = 8, amplifiers cross-backend+frontend (+1) = 9 (complex)
- Plan mode: feature → ON, plan type: full

```json
{
  "request_type": "feature",
  "complexity": { "score": 9, "level": "complex", "reasoning": "Cross-cutting: new frontend component, API hook, and new backend endpoint with SSE streaming." },
  "plan_mode": true,
  "plan_type": "full",
  "keywords_matched": ["add", "new", "endpoint", "streams"],
  "files_mentioned": ["frontend/src/components/acm/", "api/routers/"],
  "domain_signals": ["frontend", "fastapi", "extraction"],
  "override": null
}
```

---

### Example 4 — Research investigation

**Request:** "Investigate why the orchestrator is making 3 LangGraph LLM calls when the structure stage should only need 1. Check Langfuse traces for the last 10 runs and document findings."

**Reasoning:**
- Type: `research` — "investigate", "why", "check traces", "document findings" all point to knowledge-gathering, not implementation
- Complexity: 25–80 words (1) + multiple implied (orchestrator, Langfuse, acm_extraction) (1) + multiple actions (investigate + check + document) (2) + research baseline (2) = 6, amplifiers: cross-system (+1) = 7 (complex)
- Plan mode: research → ON, plan type: research

```json
{
  "request_type": "research",
  "complexity": { "score": 7, "level": "complex", "reasoning": "Open-ended investigation spanning graph code, observability traces, and a written deliverable." },
  "plan_mode": true,
  "plan_type": "research",
  "keywords_matched": ["investigate", "why", "check", "document findings"],
  "files_mentioned": [],
  "domain_signals": ["langgraph", "pipeline", "observability"],
  "override": null
}
```

---

### Example 5 — Refactor (improvement)

**Request:** "Refactor the pre-extraction stages to reduce LLM calls. The structure and preflight nodes are making redundant calls — consolidate them."

**Reasoning:**
- Type: `improvement` — "refactor", "reduce", "consolidate" are primary; no broken behavior implied
- Complexity: 25–80 words (1) + 2–4 files (structure_node, preflight_node, orchestrator) (1) + multiple related actions (1) + improvement baseline (1) + amplifier: none = Score 4 (medium)
- Plan mode: improvement → ON, plan type: refactor

```json
{
  "request_type": "improvement",
  "complexity": { "score": 4, "level": "medium", "reasoning": "Refactor within the pipeline layer; 2-3 node files, no cross-layer changes." },
  "plan_mode": true,
  "plan_type": "refactor",
  "keywords_matched": ["refactor", "reduce", "consolidate"],
  "files_mentioned": [],
  "domain_signals": ["pipeline", "langgraph"],
  "override": null
}
```

---

### Example 6 — Pipeline graph change

**Request:** "Add a caching layer to the extraction graph so that if the same PDF has been processed before, we skip Docling and return cached results from SurrealDB."

**Reasoning:**
- Type: `pipeline` — "extraction graph", caching within the graph, affects ExtractionState flow; pipeline takes priority over feature
- Complexity: 25–80 words (1) + 3–4 files (acm_extraction, store_node, database layer) (1) + multiple related actions (1) + pipeline baseline (2) = 5, amplifier: none = Score 5 (medium)
- Plan mode: pipeline → always ON, plan type: full

```json
{
  "request_type": "pipeline",
  "complexity": { "score": 5, "level": "medium", "reasoning": "Graph-layer change with cache lookup logic; touches extraction state and DB layer." },
  "plan_mode": true,
  "plan_type": "full",
  "keywords_matched": ["extraction graph", "caching", "skip", "cached results"],
  "files_mentioned": ["open_notebook/graphs/acm_extraction.py"],
  "domain_signals": ["pipeline", "langgraph", "surrealdb"],
  "override": null
}
```

---

### Example 7 — Simple frontend change (no plan)

**Request:** "Change the Export button color in ItemGrid to match the Tailwind `blue-600` design token."

**Reasoning:**
- Type: `frontend` — component, CSS, Tailwind; no backend
- Complexity: <25 words (0) + 1 file (ItemGrid component) (0) + single action (0) + frontend baseline (1) = Score 1 (simple)
- Plan mode: frontend with complexity < 7 → OFF

```json
{
  "request_type": "frontend",
  "complexity": { "score": 1, "level": "simple", "reasoning": "Single CSS color change in one component file." },
  "plan_mode": false,
  "plan_type": null,
  "keywords_matched": ["button", "color", "Tailwind"],
  "files_mentioned": ["frontend/src/components/acm/ItemGrid"],
  "domain_signals": ["frontend"],
  "override": null
}
```

---

### Example 8 — Documentation update

**Request:** "Update CLAUDE.md to document the new plan mode decision tree and add a section explaining how the request-classifier skill works."

**Reasoning:**
- Type: `documentation` — "update", "document", ".md" file, "explaining how" are all documentation signals
- Complexity: 25–80 words (1) + 1 file (CLAUDE.md) (0) + single action (0) + documentation baseline (0) = Score 1 (simple)
- Plan mode: documentation → OFF

```json
{
  "request_type": "documentation",
  "complexity": { "score": 1, "level": "simple", "reasoning": "Single markdown file update with two new sections." },
  "plan_mode": false,
  "plan_type": null,
  "keywords_matched": ["update", "document", "explaining"],
  "files_mentioned": ["CLAUDE.md"],
  "domain_signals": ["configuration"],
  "override": null
}
```

---

### Example 9 — User overrides plan mode off

**Request:** "Add error boundary components to every page in the app — just do it, no plan needed."

**Reasoning:**
- Type: `feature` — "add" + new components
- Complexity: <25 words (0) + 5+ files implied (all page files) (3) + multiple actions (1) + feature baseline (2) + amplifier "every" = +1 = 7 (complex)
- Plan mode: would be ON for feature, but "no plan needed" is an explicit override → OFF
- override: "off"

```json
{
  "request_type": "feature",
  "complexity": { "score": 7, "level": "complex", "reasoning": "Touches every page file in the app; 5+ components to update." },
  "plan_mode": false,
  "plan_type": null,
  "keywords_matched": ["add", "every", "no plan needed"],
  "files_mentioned": ["frontend/src/app/"],
  "domain_signals": ["frontend"],
  "override": "off"
}
```

---

### Example 10 — Ambiguous (fix + improve)

**Request:** "The building sidebar is slow to render when there are 50+ buildings — fix the performance issue and while you're at it, refactor it to use React.memo and virtualization."

**Reasoning:**
- Primary action: performance bug ("slow to render", "fix") → `bug-fix`
- Secondary: "refactor", "React.memo", "virtualization" → improvement signals
- Priority: bug-fix is primary since the request is driven by broken performance expectations; the refactor is incidental ("while you're at it")
- Complexity: 25–80 words (1) + 2 files (BuildingSidebar component) (1) + multiple related actions (1) + bug-fix baseline (1) = Score 4 (medium)
- Plan mode: bug-fix → ON, plan type: debug

```json
{
  "request_type": "bug-fix",
  "complexity": { "score": 4, "level": "medium", "reasoning": "Performance bug in one component; fix is primary, refactor is secondary work bundled in." },
  "plan_mode": true,
  "plan_type": "debug",
  "keywords_matched": ["fix", "slow", "performance", "refactor"],
  "files_mentioned": ["frontend/src/components/acm/BuildingSidebar"],
  "domain_signals": ["frontend"],
  "override": null
}
```

---

## Downstream Consumers

This skill's JSON output is consumed by:
- **prompt-router** (S3) — uses `request_type`, `plan_mode`, and `complexity.level` to route to the correct prompt template
- **prompt-generator** (S4) — uses the full classification to populate prompt scaffolds with context-appropriate sections and agent strategy recommendations

The classification must be accurate because downstream skills do not re-classify; they trust this output.
