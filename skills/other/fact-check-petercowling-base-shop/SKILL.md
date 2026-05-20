---
name: fact-check
description: Verify the accuracy of statements in markdown documents by auditing the actual repository state. Directly fix inaccuracies in-place rather than producing a separate report.
---

# Fact Check

Verify the accuracy of statements in markdown documents by auditing the actual repository state. When inaccuracies are found, **directly update the source document** to correct them.

## Key Distinction: fact-check vs fact-find

| Aspect | `/fact-find` | `/fact-check` |
|--------|-------------|---------------|
| Direction | Forward-looking | Documentation-to-repo conformance |
| Purpose | Gather evidence BEFORE planning | Verify and fix existing documentation |
| Input | Topic/feature to investigate | Path to a markdown document |
| Output | Planning brief or system briefing | **Updated source document(s)** |
| When | Before creating a plan | After documentation exists |

**fact-find:** "What do we need to know to build this?"
**fact-check:** "Is what we wrote still true? Fix it if not."

## Operating Mode

**READ + VERIFY + FIX**

**Allowed:**
- Read the target document
- Search the repository (glob, grep, file reads)
- Inspect tests, configs, and code
- Check dependency versions in package.json/lockfiles
- Review git history for file existence/changes
- **Edit the audited document to fix inaccuracies**
- **Edit related documents if the inaccuracy spans multiple files**
- Create a brief changelog entry in the document (if frontmatter supports it)

**Not allowed:**
- Making code changes (only documentation fixes)
- Creating commits (user reviews and commits)
- Classification without explicit evidence pointer
- Changing document meaning/intent (only factual corrections)
- Removing sections entirely (flag for user if section is obsolete)

## Repo Anchor Requirement

Every audit must record what state of the repository was audited:

**Preferred:** `Audit-Ref: <commit SHA>` - Use the current HEAD commit SHA
**Alternative:** `Audit-Ref: working-tree` - Use if uncommitted changes exist in relevant files

To determine the anchor:
1. Run `git rev-parse HEAD` to get current commit SHA
2. Run `git status` to check for uncommitted changes in relevant paths
3. If relevant files have uncommitted changes, note this when reporting

**Warning for working-tree audits:**
> ⚠️ This audit was performed against the working tree, which contains uncommitted changes. Results may differ from the committed state.

## Inputs

**Required:**
- Path to the markdown document to verify (e.g., `docs/plans/feature-plan.md`, `README.md`, `docs/architecture.md`)

**Optional:**
- Scope: `focused` or `full` (see Scope Definitions below)
- Mode: `fix` (default) or `report-only` (for cases where user wants review before changes)

## Scope Definitions

| Scope | Categories Included | Notes |
|-------|---------------------|-------|
| `focused` | 1–3 only | Only when tied to concrete file/module references |
| `full` | 1–6 | Complete audit of all claim categories |

**Explicit scope knobs** (for fine-grained control):
- `scope.include: [paths, exports, deps, counts, behavior, architecture]`

**Stop condition for large documents:**
If a `full` audit identifies >200 claims:
- Verify all Category 1–3 claims exhaustively
- Sample Category 4–6 claims (at least 20% or 10 claims, whichever is greater)
- Note in completion message: "Large document mode: sampled categories 4–6"
- User can explicitly request exhaustive audit to override

## Claim Categories

When reading the document, identify and categorize claims:

### Category 1: File/Directory References
- Explicit paths: "The component is at `src/components/Button.tsx`"
- Directory claims: "Tests live in `__tests__/`"
- Config references: "See `tsconfig.json` for..."

### Category 2: Code Structure Claims
- Component existence: "The `UserProfile` component handles..."
- Function existence: "Call `validateInput()` to..."
- Export claims: "This module exports `useAuth`"
- Pattern claims: "Uses the repository pattern"

### Category 3: Technology/Dependency Claims
- Version claims: "Built with React 19"
- Dependency claims: "Uses Prisma for ORM"
- Stack claims: "Runs on Cloudflare Pages"

### Category 4: Architecture Claims
- Data flow: "Requests go through the API gateway"
- Integration claims: "Connects to PostgreSQL"
- Layer claims: "Three-tier architecture"

### Category 5: Behavioral Claims
- Feature existence: "Supports dark mode"
- API claims: "The `/api/users` endpoint returns..."
- Test coverage claims: "Has 80% test coverage"

### Category 6: Count/Quantity Claims
- "Contains 3 packages"
- "Has 15 API endpoints"
- "Supports 12 languages"

## Atomic Claim Rules

**One claim = one verifiable predicate.** Each claim must assert a single, testable fact.

Examples of atomic claims:
- "File X exists"
- "Function Y is exported from module Z"
- "React major version is 19"
- "Directory `src/utils/` contains validation helpers"

**Compound sentences must be split:**

| Document Text | Atomic Claims |
|---------------|---------------|
| "The `useAuth` hook in `src/hooks/` handles authentication and session management" | C1: `useAuth` hook exists in `src/hooks/` <br> C2: `useAuth` handles authentication <br> C3: `useAuth` handles session management |

## Exclusion Rules: Examples vs Claims

**Decision rule for ambiguous content:**

If a path, code snippet, or technical reference appears:
- Under a heading containing "Example", "Sample", "Pseudo-code", "Sketch", "Template", or "Illustration"
- Within a block explicitly marked as hypothetical
- In a "could look like" or "might be" context

**→ Treat as non-claim by default.**

**Exception:** If surrounding text explicitly asserts repo truth, treat as claim:
- "In this repo, it lives at..."
- "Our actual implementation..."
- "Currently located at..."

When in doubt, mark as a claim but note the ambiguity.

## Workflow

### 1) Establish audit anchor

Before reading the document:
1. Run `git rev-parse HEAD` to get commit SHA
2. Check `git status` for uncommitted changes in relevant paths
3. Note anchor for completion message

### 2) Parse the document

Read the target document and extract all verifiable claims. For each claim, track:
- **Doc line(s):** Line number(s) where claim appears
- **Category:** 1–6 per taxonomy above
- **Claim text:** The atomic claim extracted
- **What evidence would verify it**

### 3) Prioritize claims

Audit claims in this priority order:
1. File/directory references (easy to verify, high impact if wrong)
2. Code structure claims (moderate effort, high impact)
3. Technology/dependency claims (check package.json/lockfile)
4. Count/quantity claims (can be verified with tooling)
5. Architecture/behavioral claims (require deeper inspection)

### 4) Audit each claim

For each claim:

**a) Determine verification method:**
- File exists? → `glob`, `read`
- Code contains X? → `grep`, `read`
- Version correct? → Read `package.json` or lockfile
- Count accurate? → Run appropriate glob/count
- Structure matches? → Read and inspect

**b) Gather evidence:**
- Record exact file path checked
- Record line numbers if relevant
- Note what you found

**c) Classify finding:**

| Finding | Criteria | Action |
|---------|----------|--------|
| Accurate | Evidence confirms the claim exactly | No change needed |
| Partially accurate | Claim is mostly true but details differ | Fix the details |
| Inaccurate | Claim contradicts current repo state | Fix with correct information |
| Outdated | Claim was true but repo has changed | Update to current state |
| Unverifiable | Claim too vague or refers to external/runtime state | Add clarifying note or flag for user |
| Obsolete section | Entire section no longer applies | Flag for user decision (don't delete) |

### 5) Fix inaccuracies in-place

For each inaccurate, outdated, or partially accurate claim:

**a) Determine the correction:**
- What is the actual current state?
- What is the minimal change to make the claim accurate?
- Does the fix affect document flow/meaning?

**b) Apply the fix:**
- Use the Edit tool to update the specific text
- Preserve document structure and formatting
- Keep the same voice/style as the original
- If multiple related claims need fixing, batch them logically

**c) For unverifiable claims:**
- Add inline clarification: `(runtime behavior; not verified)`
- Or convert to softer language: "is designed to" instead of "does"
- Or flag with HTML comment: `<!-- FACT-CHECK: unverifiable, requires runtime test -->`

**d) For obsolete sections:**
- Do NOT delete
- Add a note at the section start:
  ```markdown
  > **Note:** This section may be outdated. [Brief reason]. Review recommended.
  ```
- Flag in completion message for user decision

### 6) Update document metadata (if applicable)

If the document has frontmatter with `Last-updated`:
- Update to today's date

If the document has a changelog or revision history section:
- Add brief entry: `YYYY-MM-DD: Fact-check corrections (paths, versions, counts)`

### 7) Report completion

Summarize what was checked and fixed in the completion message.

## Evidence Standards (Hard Requirements)

### Required for "Accurate" classification:
- File path verified to exist (for path claims)
- Code snippet confirming structure (for code claims)
- Version string from package.json (for version claims)
- Actual count with method shown (for quantity claims)

### Required for "Inaccurate" classification (before fixing):
- Exact quote from document (the claim)
- Exact evidence from repo (the contradiction)
- Both must be cited with paths/line numbers

### Required for "Outdated" classification:

**Outdated requires git history evidence.** You must prove the claim was previously true:
- `git log --follow <path>` showing rename/move/removal
- A past commit where the referenced symbol/path existed
- `git show <sha>:<path>` demonstrating prior state

**If you cannot prove prior truth, classify as Inaccurate, not Outdated.**

### Required for "Unverifiable" classification:
- Explanation of what would be needed to verify
- Classification of why it's unverifiable:
  - External dependency behavior
  - Runtime-only behavior (requires execution)
  - Deployment/infrastructure state
  - Too vague to form testable predicate
  - Requires manual testing

### Not acceptable:
- "Probably accurate" without verification
- "Likely outdated" without checking repo
- Assumptions based on conventions
- Memory of previous state
- Classification without explicit evidence pointer

## Verification Thresholds by Category

### Category 1: Path Claims
- **Evidence:** File/directory exists at specified path
- **If claim implies content:** File must contain referenced symbol

### Category 2: Export Claims
- **Evidence:** Show export statement
- **Plus:** Import usage OR re-export chain demonstrating accessibility

### Category 3: Dependency Claims
- **For "uses X":** Package appears in dependencies
- **For "version X":**
  - Accept if package.json major version matches (range OK)
  - If lockfile available, verify resolution for main app packages
  - If multiple versions resolve: update to note both versions

### Category 4 & 5: Architecture/Behavioral Claims
A claim can be **Accurate** only if:
1. Direct code evidence exists (feature flag, provider usage, middleware application), AND
2. Coverage exists in tests OR explicit contract code, OR
3. The claim is trivially derivable from implementation (e.g., "uses React" when React imports exist throughout)

**Otherwise:** Mark as **Unverifiable** and add inline note

### Category 6: Count Claims
- **Evidence:** Show counting method
- **Include exclusions:** e.g., "counted `packages/*/package.json`, excluding `node_modules` and build outputs"
- **For approximate claims** ("about 15"): Accurate if within 10%

## Fix Guidelines

### Minimal changes principle
Only change what's factually incorrect. Don't rewrite for style or expand scope.

**Good fix:**
```markdown
# Before
The config file is at `config/settings.json`.

# After
The config file is at `src/config/settings.json`.
```

**Bad fix (over-editing):**
```markdown
# Before
The config file is at `config/settings.json`.

# After
The application configuration is stored in `src/config/settings.json`. This file contains all runtime settings including database connections, API keys, and feature flags. See the Configuration Guide for details.
```

### Version updates
```markdown
# Before
Built with React 18.

# After
Built with React 19.
```

### Count updates
```markdown
# Before
The monorepo contains 5 packages.

# After
The monorepo contains 7 packages.
```

### Path updates with context
```markdown
# Before
Authentication logic lives in `src/auth/`.

# After
Authentication logic lives in `src/lib/auth/`.
```

### Unverifiable claim handling
```markdown
# Before
The API responds within 200ms.

# After
The API is designed to respond within 200ms (performance varies by load).
```

### Obsolete section flagging
```markdown
# Before
## Legacy Authentication
The old auth system uses session cookies stored in Redis.

# After
## Legacy Authentication

> **Note:** This section describes the legacy authentication system, which has been replaced. See [New Auth System](#new-auth-system) for current documentation.

The old auth system uses session cookies stored in Redis.
```

## When to Use

**Good use cases:**
- Before publishing documentation to users/developers
- After major refactors that may have invalidated docs
- When onboarding reveals documentation confusion
- As part of periodic documentation maintenance
- When someone reports "the docs say X but I see Y"
- Before a release to verify release notes accuracy

**Not appropriate for:**
- Gathering new information about a system (use `/fact-find`)
- Planning a feature (use `/fact-find` then `/plan-feature`)
- Verifying external documentation (only for this repo's docs)
- Real-time validation during builds (too slow)

## Anti-Patterns (Explicitly Forbidden)

### 1. Assuming without checking
"This path looks standard, probably accurate" - NO. Check every claim.

### 2. Over-editing
Don't rewrite sections for style. Only fix factual inaccuracies.

### 3. Marking vague claims as accurate
"The system is well-tested" - Mark as unverifiable and add clarifying note.

### 4. Ignoring context
A path in a code block might be an example, not a claim about repo state. Use the exclusion rules above.

### 5. Deleting content
Never delete sections even if obsolete. Flag for user decision.

### 6. Skipping negative evidence
If you find something that contradicts a claim, you must fix it even if inconvenient.

### 7. Conflating "claim" with "intention"
"We plan to add X" is not a factual claim to verify (it's a statement of intent).

### 8. Outdated without git evidence
Never classify as "Outdated" unless you can prove via git history that it was previously true.

### 9. Classifying without evidence
Every classification (including Accurate) must have an explicit evidence pointer.

### 10. Changing document meaning
Fact-check fixes facts, not intent. If a section's purpose is unclear, flag for user.

## Integration with Other Skills

| After fact-check... | Consider... |
|---------------------|-------------|
| Many fixes made | User reviews changes, commits |
| Architecture docs heavily outdated | `/fact-find` to create fresh briefing |
| Plan doc inaccurate | `/re-plan` to update the plan |
| Obsolete sections flagged | User decides to remove or archive |

## Quality Checks

Before completing the fact-check:

- [ ] Audit anchor noted (commit SHA or working-tree with warning)
- [ ] Every verifiable claim was checked
- [ ] All inaccuracies were fixed in-place
- [ ] Unverifiable claims were annotated or flagged
- [ ] Obsolete sections were flagged (not deleted)
- [ ] Document metadata updated (Last-updated, changelog)
- [ ] Fixes preserve original document voice/style
- [ ] No over-editing (minimal changes only)

## Completion Messages

**Clean audit (no fixes needed):**
> "Fact-check complete. Document `<path>` audited at `<sha>`. X claims checked; all verifiable claims are accurate. No changes made."

**Fixes applied:**
> "Fact-check complete. Document `<path>` audited at `<sha>`. X claims checked. Fixed N inaccuracies:
> - Line 23: Updated path from `config/` to `src/config/`
> - Line 45: Updated React version from 18 to 19
> - Line 67: Updated package count from 5 to 7
>
> Flagged for review:
> - Line 89: Obsolete section on legacy auth (marked with note)
> - Line 112: Unverifiable performance claim (added clarification)
>
> Please review the changes and commit when ready."

**Partial audit:**
> "Fact-check complete (scope: focused). Checked N of M claims in `<path>`. Fixed N issues. Consider full audit if document is critical."

**Report-only mode:**
> "Fact-check complete (report-only mode). X claims checked. Found N inaccuracies that need fixing:
> - Line 23: Path `config/` should be `src/config/`
> - Line 45: React version 18 should be 19
>
> Run `/fact-check <path>` again without `report-only` to apply fixes."

## Mode: report-only

If the user specifies `report-only` mode, follow the same verification workflow but:
- Do NOT make any edits
- List all findings with line numbers and suggested fixes
- User can then choose to run again in fix mode or make manual edits

This is useful when:
- User wants to review before any changes
- Document is sensitive or requires careful review
- Multiple stakeholders need to approve changes
