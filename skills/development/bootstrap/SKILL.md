---
name: bootstrap
description: 'Two-phase codebase analysis. Phase 1: discover features from code. Phase
  2: trace workflows.'
---

---
name: bootstrap
description: Two-phase codebase analysis. Phase 1: discover features from code. Phase 2: trace workflows.
---

# Bootstrap Feature Tree

Two-phase process to populate Feature Tree from an existing codebase:
- **Phase 1**: Feature Discovery (bottom-up, code → features)
- **Phase 2**: Workflow Identification (top-down, features → workflows)

Both phases are optional. Run Phase 1 alone, skip to Phase 2 with manual guidance, or run both.

---

## Phase 1: Feature Discovery

### Step 1.1: Module Detection

Scan the codebase structure and propose modules:

1. Read top-level directories (especially `src/`, `lib/`, `app/`)
2. Check config files (package.json, pyproject.toml) for hints
3. Present proposed modules to user:

```
I found these potential modules:

| Module | Path | Notes |
|--------|------|-------|
| auth | src/auth | login, session, oauth files |
| payments | src/payments | stripe, checkout |
| users | src/users | profile, settings |
| utils | src/utils | shared helpers → likely INFRA |

Add, remove, or rename any? [Enter to confirm]
```

Log module detection: `bootstrap_log("Proposed modules: auth, payments, users, utils", "MODULE_DETECT")`

### Step 1.2: Parallel Subagent Dispatch

For each confirmed module, spawn an Explore subagent with Feature Tree context:

```python
Task(
    subagent_type="Explore",
    prompt=f"""
## Context: Feature Tree Bootstrap

Feature Tree tracks atomic features and infrastructure for AI-assisted development.

**FEATURE** = Atomic, user-facing capability
- Something you'd say "implement the X feature"
- Examples: AUTH.login, PAYMENT.checkout, USER.profile_update
- Must be completable in one Claude session

**INFRASTRUCTURE** = Shared utilities, not user-facing alone
- Use INFRA.* prefix: INFRA.rate_limiter, INFRA.logger, INFRA.validation
- Gets linked to features via `uses` field

**CONFIDENCE:**
- HIGH: Obvious from names/structure (file literally named login.ts with handleLogin export)
- MEDIUM: Reasonable inference from patterns
- LOW: Ambiguous, might be wrong

## Your Task

Analyze module: {module_name}
Path: {module_path}

1. Identify features (user-facing capabilities)
2. Identify infrastructure (shared utilities)
3. Note cross-module dependencies

Return JSON:
{{
  "module": "{module_name}",
  "features": [
    {{
      "id": "DOMAIN.name",
      "name": "Human Readable Name",
      "description": "What it does",
      "files": ["path/to/file.ts"],
      "code_symbols": ["functionName", "ClassName"],
      "confidence": "MEDIUM"
    }}
  ],
  "infrastructure": [
    {{
      "id": "INFRA.name",
      "name": "Human Readable Name",
      "files": ["path/to/file.ts"],
      "code_symbols": ["helperFn"],
      "confidence": "HIGH"
    }}
  ],
  "cross_refs": [
    {{
      "target": "@other_module",
      "reason": "calls their exported function",
      "symbols": ["importedSymbol"]
    }}
  ]
}}
"""
)
```

**Launch all subagents in a single message** (parallel execution).

### Step 1.3: Inline Synthesis

After collecting all subagent results:

1. **Merge duplicates**: Same feature ID from multiple modules → combine files/symbols
2. **Process cross_refs**: Convert to `uses` relationships
   - `@auth` referencing `validateToken` → feature uses `AUTH.token_validation`
3. **Resolve conflicts**: Same code claimed by multiple features → pick best fit or flag for user
4. **Separate INFRA**: Infrastructure items use INFRA.* prefix, will be linked via `uses`

### Step 1.4: Save to Database

For each synthesized feature:

```python
add_feature(
    id="AUTH.login",
    name="User Login",
    description="Validates credentials, creates session",
    confidence="MEDIUM",
    uses=["INFRA.rate_limiter"]  # from cross_refs
)

update_feature(
    id="AUTH.login",
    files=["src/auth/login.ts", "src/auth/session.ts"],
    code_symbols=["handleLogin", "createSession", "validateCredentials"]
)

bootstrap_log("Created AUTH.login (MEDIUM)", "FEATURE_CREATE")
```

### Step 1.5: User Checkpoint

Present results and offer choices:

```markdown
## Phase 1 Complete: 15 features discovered

| ID | Name | Confidence | Uses |
|----|------|------------|------|
| AUTH.login | User Login | MEDIUM | INFRA.rate_limiter |
| AUTH.register | User Registration | MEDIUM | INFRA.validation |
| INFRA.rate_limiter | Rate Limiter | HIGH | - |
| INFRA.validation | Input Validation | HIGH | - |
...

**Flagged for review:**
- UTILS.format_date — LOW confidence, might be INFRA
- AUTH.session vs USER.session — possible overlap

**What next?**
1. Continue to Phase 2 (workflow discovery)
2. Review/edit features first
3. Done for now
```

---

## Phase 2: Workflow Identification

### Step 2.1: Identify Starting Points

Find terminal features (natural workflow entry points):

1. Features with route/handler/command in files or symbols
2. Features not used by other features (no incoming `uses` edges)
3. Entry points from config (routes.ts, app.ts, main.py)

Present to user:

```
Starting points for workflow tracing:

| Feature | Entry Point |
|---------|-------------|
| AUTH.login | POST /auth/login |
| AUTH.register | POST /auth/register |
| PAYMENT.checkout | POST /checkout |

Add any entry points I missed? [Enter to confirm]
```

### Step 2.2: Parallel Workflow Tracing

For each starting point, spawn subagent:

```python
Task(
    subagent_type="Explore",
    prompt=f"""
## Context: Feature Tree Workflow Tracing

You're tracing a workflow from a known entry point. Map it to existing features.

**Known features in this codebase:**
{list_of_feature_ids_and_names}

## Your Task

Starting feature: {feature_id}
Entry point: {entry_file}:{entry_symbol}

1. Trace the code path from entry to completion
2. Map each step to a known feature ID (from list above)
3. Note the user-visible outcome

Return JSON:
{{
  "starting_feature": "{feature_id}",
  "trace": ["AUTH.login", "INFRA.rate_limiter", "DB.session_create"],
  "user_outcome": "User is logged in with session cookie",
  "confidence": "MEDIUM"
}}

IMPORTANT: Use existing feature IDs from the list. Don't invent new ones.
"""
)
```

### Step 2.3: Further Investigation (Optional)

Subagent traces are hints, not final answers. Review for gaps:

```
Traces collected from 5 workflows.

Potential gaps detected:
- AUTH.login trace doesn't show session storage mechanism
- PAYMENT.checkout trace unclear on error handling
- 2 traces reference "sendEmail" — not mapped to any feature

Investigate gaps before synthesis? [y/n]
```

If yes: Use Grep/Read to follow unclear paths, potentially discover missing features.

### Step 2.4: Synthesize Workflows

Transform raw traces to clean flows:

**Raw trace:**
```
["AUTH.login", "INFRA.rate_limiter", "DB.user_find", "AUTH.session_create"]
```

**Synthesized workflow:**
```python
add_workflow(
    id="AUTH.login_flow",
    name="User Login Flow",
    description="User submits credentials and receives session",
    depends_on=["AUTH.login", "AUTH.session_create"],  # exclude INFRA internals
    confidence="MEDIUM",
    mermaid="""
graph TD
    A[User submits credentials] --> B[AUTH.login]
    B --> C[AUTH.session_create]
    C --> D[User logged in]
"""
)

bootstrap_log("Created AUTH.login_flow (MEDIUM)", "WORKFLOW_CREATE")
```

**Synthesis rules:**
- Collapse INFRA.* into parent feature (implementation detail)
- Use feature IDs in mermaid, not function names
- Human-readable flow names and descriptions

### Step 2.5: Coverage Check

Verify all features appear in at least one workflow:

```
Coverage: 12/15 features in workflows

Uncovered:
- USER.settings (no workflow traces it)
- AUTH.password_reset (no workflow traces it)

Options:
1. Add these as starting points, trace again
2. Skip — I'll add workflows manually later
```

If option 1: Loop back to Step 2.2 with uncovered features.

### Step 2.6: Journey Grouping (Optional)

Group related flows into journeys:

```
Proposed journeys:

| Journey | Flows |
|---------|-------|
| USER_ONBOARDING | register_flow, verify_email_flow, first_login_flow |
| CHECKOUT | add_to_cart_flow, payment_flow, confirmation_flow |

Create these journey groupings? [y/n]
```

If yes: Create parent workflows with child flows.

---

## Guidelines

- **Atomic features**: "Calls Stripe API" is one feature, don't decompose further
- **ID hierarchy**: Use PARENT.child format (AUTH.login, PAYMENT.stripe)
- **INFRA prefix**: Shared utilities use INFRA.* (INFRA.rate_limiter, INFRA.logger)
- **Confidence is honest**: LOW means uncertain — that's okay, refine later
- **User guides process**: Always checkpoint with user before major actions
- **Iterative**: Can run again to discover more features/workflows
- **Log everything**: Use bootstrap_log() for audit trail
