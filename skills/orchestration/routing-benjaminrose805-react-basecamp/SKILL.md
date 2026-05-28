---
name: routing
description: Analyze spec content and route /implement to appropriate agents.
---

# Routing Skill

Analyze spec content and route `/implement` to appropriate agents based on what the spec defines.

## When Used

| Command      | Routing Logic                                   |
| ------------ | ----------------------------------------------- |
| `/implement` | Read approved spec → detect type → route agents |

**NOT used by:** `/start`, `/plan`, `/ship`, `/guide`, `/mode` (direct routing)

## Implement Routing

### Decision Flow

```text
/implement
    │
    ▼
┌────────────────────────────────────────────────────┐
│  1. FIND: Locate approved spec                     │
│     Check: specs/{feature}/design.md               │
│     Verify: "Status: Approved" in frontmatter      │
└────────────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────────────┐
│  2. ANALYZE: Read spec content                     │
│     Parse: design.md sections and keywords         │
│     Identify: Backend, frontend, docs, eval scope  │
└────────────────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────────────────┐
│  3. ROUTE: Based on detected type                  │
└────────────────────────────────────────────────────┘
    │
    ├── Backend only → code-agent
    │
    ├── Frontend only → ui-agent
    │
    ├── Backend + Frontend → code-agent → ui-agent (sequential)
    │
    ├── Documentation only → docs-agent
    │
    ├── Evaluation only → eval-agent
    │
    └── Mixed → Route to multiple agents per section
```

### Spec Content Detection

| Detected In Spec                                   | Type     | Routes To  |
| -------------------------------------------------- | -------- | ---------- |
| tRPC, Prisma, API, database, model, schema, server | Backend  | code-agent |
| React, component, form, UI, hook, page, layout     | Frontend | ui-agent   |
| README, documentation, guide, tutorial             | Docs     | docs-agent |
| evaluation, grader, benchmark, pass@k, LLM test    | Eval     | eval-agent |

### Section-Based Detection

The spec's `design.md` sections determine routing:

```text
## Architecture
├── "Database" subsection → Backend component
├── "API" subsection → Backend component
├── "Components" subsection → Frontend component
└── "Pages" subsection → Frontend component

## Implementation
├── Tasks mention Prisma/tRPC → Backend
├── Tasks mention React/shadcn → Frontend
└── Tasks mention both → Mixed (code-agent → ui-agent)
```

### Examples

| Spec Content                     | Detected Type | Route                   |
| -------------------------------- | ------------- | ----------------------- |
| Prisma schema + tRPC router only | Backend       | code-agent              |
| React components + forms only    | Frontend      | ui-agent                |
| Prisma + tRPC + React components | Full-stack    | code-agent → ui-agent   |
| README + API docs                | Docs          | docs-agent              |
| Grader + test cases + benchmarks | Eval          | eval-agent              |
| Prisma + README                  | Mixed         | code-agent + docs-agent |

---

## No Spec Found

When `/implement` is called but no approved spec exists:

```text
┌─────────────────────────────────────────────────────────────────┐
│  /implement                                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ERROR: No approved spec found                                   │
│                                                                  │
│  Checked locations:                                              │
│  • specs/{feature}/design.md - Not found                         │
│  • specs/{feature}/requirements.md - Not found                   │
│                                                                  │
│  To create a spec, run:                                          │
│  /plan                                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Ambiguous Spec

When spec content is unclear:

```text
┌─────────────────────────────────────────────────────────────────┐
│  /implement                                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Spec found but type unclear: specs/utils/design.md              │
│                                                                  │
│  What type of implementation is this?                            │
│                                                                  │
│  1. Backend (API, database, server logic)     → code-agent       │
│  2. Frontend (UI, components, styling)        → ui-agent         │
│  3. Full-stack (both)                         → code → ui        │
│  4. Documentation                             → docs-agent       │
│  5. LLM evaluation                            → eval-agent       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Routing Decision Matrix

| Spec Content                        | Detected Scope | Route                   |
| ----------------------------------- | -------------- | ----------------------- |
| Prisma, tRPC, API only              | Backend        | code-agent              |
| React, components, UI only          | Frontend       | ui-agent                |
| Both backend + frontend sections    | Full-stack     | code-agent → ui-agent   |
| README, documentation only          | Docs           | docs-agent              |
| Evaluation, grader, benchmarks only | Eval           | eval-agent              |
| Backend + docs sections             | Mixed          | code-agent → docs-agent |
| Frontend + eval sections            | Mixed          | ui-agent → eval-agent   |
| Unclear or empty spec               | Unknown        | Ask for clarification   |

---

## Algorithm

```typescript
interface RoutingResult {
  agents: ("code-agent" | "ui-agent" | "docs-agent" | "eval-agent")[];
  reason: string;
  spec: { path: string; sections: string[] };
}

function routeImplement(specPath: string): RoutingResult {
  // 1. Read and parse spec
  const spec = readSpec(specPath);
  if (!spec) {
    throw new Error("No approved spec found. Run /plan first.");
  }

  // 2. Detect sections
  const sections = detectSections(spec.content);

  // 3. Build agent sequence
  const agents: RoutingResult["agents"] = [];

  if (hasBackendIndicators(sections)) {
    agents.push("code-agent");
  }

  if (hasFrontendIndicators(sections)) {
    agents.push("ui-agent");
  }

  if (hasDocsIndicators(sections)) {
    agents.push("docs-agent");
  }

  if (hasEvalIndicators(sections)) {
    agents.push("eval-agent");
  }

  // 4. Handle ambiguous case
  if (agents.length === 0) {
    throw new Error(
      "Unable to determine implementation type. Please clarify: backend, frontend, full-stack, docs, or eval?"
    );
  }

  return {
    agents,
    reason: `Detected: ${agents.join(", ")}`,
    spec: { path: specPath, sections },
  };
}

function detectSections(content: string): string[] {
  const indicators = {
    backend: /prisma|trpc|api|database|schema|mutation|query|server/i,
    frontend: /react|component|form|ui|hook|page|layout|shadcn/i,
    docs: /readme|documentation|guide|tutorial/i,
    eval: /evaluation|grader|benchmark|pass@k|llm test/i,
  };

  return Object.entries(indicators)
    .filter(([_, regex]) => regex.test(content))
    .map(([type]) => type);
}
```

---

## Error Handling

| Scenario             | Handling                                       |
| -------------------- | ---------------------------------------------- |
| No spec found        | Error: Run /plan first                         |
| Spec not approved    | Error: Get spec approved first                 |
| Spec unreadable      | Error: Cannot parse spec file                  |
| No sections detected | Ask user to clarify implementation type        |
| Multiple agent types | Execute sequentially (code → ui → docs → eval) |

---

## Output

### Successful Routing

```markdown
## Routing: SUCCESS

**Spec:** specs/user-authentication/design.md
**Detected:** Full-stack (backend + frontend)

### Execution Chain

1. **code-agent** (backend)
   - code-researcher → code-writer → code-validator
   - Scope: Prisma schema, tRPC router

2. **ui-agent** (frontend)
   - ui-researcher → ui-builder → ui-validator
   - Scope: Login form, auth context

3. **check-agent** (verification)
   - Parallel: build, types, lint, tests, security
```

### No Spec Found

```markdown
## Routing: ERROR

**Reason:** No approved spec found

### Next Steps

1. Run `/plan` to create a spec
2. Review and approve the spec
3. Run `/implement` again
```

### Clarification Needed

```markdown
## Routing: CLARIFY

**Spec:** specs/utils/design.md
**Reason:** Unable to determine implementation type

### Detected Content

- No backend keywords (Prisma, tRPC, API)
- No frontend keywords (React, component, UI)
- No docs keywords (README, guide)
- No eval keywords (grader, benchmark)

### Question

What type of implementation is this?

1. Backend (code-agent)
2. Frontend (ui-agent)
3. Full-stack (code-agent → ui-agent)
4. Documentation (docs-agent)
5. Evaluation (eval-agent)
```
