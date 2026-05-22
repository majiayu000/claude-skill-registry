---
name: code-reviewing
description: Performs systematic code review with universal best practices and repo-specific standards. Auto-activates after significant code changes. Use when reviewing code, auditing files, checking PRs, examining staged changes, or when asked to "review", "check", "audit", or "examine" code. Enforces design principles (SOLID, DRY, KISS), security (OWASP), performance, concurrency safety, cross-platform compatibility, and codebase patterns.
allowed-tools: Read, Grep, Glob, AskUserQuestion
---

# Code Reviewing

Systematic code review skill based on industry best practices from Google Engineering, OWASP, and modern development standards. Designed to catch issues that casual review misses through structured, checklist-driven analysis.

**Core Principle (Google):** Approve code that improves overall code health, even if not perfect. Seek continuous improvement, not perfection. But NEVER approve code that degrades code health.

## When to Use This Skill

**Auto-activation triggers:**

- After completing significant implementation tasks
- Before committing changes
- When reviewing PRs or staged files

**Explicit activation triggers:**

- User asks to "review", "check", "audit", or "examine" code
- User mentions "code review", "PR review", "look at this code"
- User asks about code quality or standards compliance

## Interactive Review Scoping

Use AskUserQuestion to determine review depth and risk profile when not specified:

```yaml
# Question 1: Review Depth (MCP: Google Engineering code review, OWASP)
question: "What type of code review is needed?"
header: "Review Type"
options:
  - label: "Quick Review (Recommended)"
    description: "Surface issues, style, obvious bugs (~15 min, ~3.5K tokens)"
  - label: "Thorough Review"
    description: "Multi-pass: logic, design, tests (~45 min, ~14K tokens)"
  - label: "Security Review"
    description: "Threat-focused: auth, validation, crypto (~30 min)"
  - label: "Architecture Review"
    description: "Design patterns, dependencies, coupling (~60 min)"

# Question 2: Risk Profile (MCP: CLI best practices - scope selection)
question: "What is the risk profile of this change?"
header: "Risk"
options:
  - label: "Low Risk (Recommended)"
    description: "Isolated fix, well-tested area, no user impact"
  - label: "Medium Risk"
    description: "Feature change, moderate scope, reversible"
  - label: "High Risk"
    description: "Critical path, security-sensitive, wide impact"
  - label: "Unknown"
    description: "I'm not sure - analyze and recommend"
```

Use these responses to select the appropriate review profile (quick, thorough, security, strict, performance).

## Review Workflow

```text
Code Review Progress:
- [ ] Step 0: RESEARCH PHASE (MANDATORY - Run MCP queries for technology stack)
- [ ] Step 0b: LOAD REPO CONFIG (Check .claude/code-review.md, fallback to CLAUDE.md)
- [ ] Step 0e: Git History Analysis (coupling, hot spots, author context - thorough/strict only)
- [ ] Step 1: Count files to review (accurate file counting)
- [ ] Step 1b: Detect generated content (scan for markers, identify generators)
- [ ] Step 2: Identify scope (files to review, excluding generated files)
- [ ] Step 3: Load context (repo standards + MCP research results + repo config)
- [ ] Step 4: Run Universal Checks (Layer 1) - informed by MCP research
- [ ] Step 5: Run Repo-Specific Checks (Layer 2, applying repo config rules)
- [ ] Step 5b: Run Claude Code Validation (Tier 4b, if CC files detected)
- [ ] Step 6: Report ALL findings with severity, rule source, and MCP validation status
- [ ] Step 7: Propose specific fixes with rationale and MCP-backed recommendations
```

### Step 0: RESEARCH PHASE (MANDATORY)

**CRITICAL: This step runs BEFORE any code analysis. It is NOT optional.**

Query MCP servers to understand current patterns and best practices BEFORE reviewing code. This prevents making claims based on stale training data.

**Load Reference:** [references/tier-0/research-phase.md](references/tier-0/research-phase.md)

**Quick Reference:**

1. **Detect Technology Stack** (from file extensions, imports, manifests)
2. **Query MCP Servers** (parallel queries based on detected technologies):
   - Microsoft tech (.NET, Azure, C#) → `microsoft-learn` + `perplexity` (ALWAYS dual-validate)
   - npm/PyPI packages → `context7` + `ref`
   - Security patterns → `perplexity` (OWASP)
   - Version claims → `perplexity` (ALWAYS validate)
3. **Build Current Truth Context** (store validated patterns for use during analysis)

**Core Rules:**

- **Research BEFORE analysis** - Know current best practices before making claims
- **Perplexity ALWAYS required** - Training data is stale; always cross-validate
- **Dual validation for Microsoft tech** - `microsoft-learn` can be stale, ALWAYS pair with `perplexity`
- **Every finding needs a source** - No finding without authoritative validation

**High-Risk Technologies (Extra Perplexity Validation Required):**

- .NET 10, .NET Aspire, Azure AI Foundry, HybridCache, Microsoft.Extensions.AI

### Step 0b: Load Repository Configuration

**Load repo-specific rules to customize the review.**

**Load Reference:** [references/tier-4/repo-config.md](references/tier-4/repo-config.md)

**Configuration Priority Chain:**

```text
1. .claude/code-review.md (PRIMARY)
   ├── Found: Parse config, apply rules, STOP
   └── Not found: Continue to fallback

2. CLAUDE.md + @imports (FALLBACK)
   ├── Found: Read CLAUDE.md + follow @imports
   │   └── Extract rules from ## Critical Rules, ## Conventions sections
   └── Not found: Continue to fallback

3. No config found
   ├── Interactive mode: Use AskUserQuestion
   │   └── "No review configuration found. Review with default rules?"
   └── Non-interactive: Apply default rules only
```

**What Gets Loaded:**

| Source | What's Parsed |
| --- | --- |
| `.claude/code-review.md` | Tech Stack, Exclude Rules, Severity Overrides, Custom Checks |
| CLAUDE.md + @imports | Text from ## Critical Rules, ## Conventions, ## Code Review sections |

**Config Effects:**

| Config Section | Effect on Review |
| --- | --- |
| Tech Stack | Override auto-detection, improve MCP query accuracy |
| Exclude Rules | Skip these rules entirely (no findings generated) |
| Severity Overrides | Change default severity for specific rules |
| Custom Checks | Add project-specific checks (file patterns, content rules) |

**Quick Reference:**

```bash
# Check if config exists
ls .claude/code-review.md 2>/dev/null || echo "No config, will use CLAUDE.md fallback"

# Preview what config will be loaded (via review command)
/code-quality:review --show-rules
```

### Step 0e: Git History Analysis

**Triggered by:** `thorough` or `strict` profile (partial for `security`/`performance`)

**Load Reference:** [references/tier-1/git-history-context.md](references/tier-1/git-history-context.md)

Extract git history context to inform review priorities and catch coupling issues:

1. **Read Configuration** - Check `.claude/code-review.md` for history analysis settings
2. **Coupling Analysis** - Find files that frequently change together
3. **Hot Spot Detection** - Identify high-churn files (configurable threshold, default: 10+ changes in 3 months)
4. **Author Context** - Extract ownership patterns (`strict` profile only)
5. **Recent Patterns** - Detect bug fix, security, or refactoring history

**Quick Reference Commands:**

```bash
# Coupling analysis - files that change together
git log --name-only --pretty=format: -- <files> | sort | uniq -c | sort -rn | head -20

# Hot spot detection - change frequency
git log --since="3 months ago" --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20

# Author context - ownership
git shortlog -sn -- <files>

# Recent patterns - commit messages
git log --oneline -10 -- <files>
```

**Profile Behavior:**

| Profile | Analysis Depth |
| --- | --- |
| quick | Skip entirely |
| security | Partial (security-related commits only) |
| thorough | Coupling + hot spots + recent patterns |
| strict | Full analysis including author context |
| performance | Partial (perf-related history only) |

### Step 1: Count Files (Accurate File Counting)

Before reviewing, count the files to ensure accurate reporting:

| Review Scope | Counting Command |
| --- | --- |
| Staged changes | `git diff --staged --name-only \| wc -l` |
| PR changes | `git diff --name-only main...HEAD \| wc -l` |
| Specific paths | Use Glob tool and count results |

**Important**:

- Track this count accurately - report it in **Files Reviewed** output
- Exclude binary files (images, compiled assets) from review count
- Exclude deleted files from review count (nothing to review)
- For renamed files: count as 1 file (the new name)

**Large Changeset Warnings**:

- 50+ files: Consider batched review or consensus mode
- 100+ files: Strongly recommend breaking into smaller chunks

### Step 1b: Detect Generated Content

Scan changed files for generation markers to identify files that were created by scripts/tools. Review the generator (source of truth) instead of generated output.

**Detection Markers** (scan first 20 + last 10 lines):

| File Type | Markers |
| --- | --- |
| Markdown | `Generated: YYYY-MM-DD`, `<!-- Generated by ScriptName -->` |
| JSON | Root `"timestamp"` or `"generator"` fields |
| Scripts | `Auto-generated from`, `DO NOT EDIT`, `Generated by` |
| Code | `// <auto-generated>`, `@generated`, `*.g.cs`, `*.generated.ts` |

**Workflow**:

1. Scan changed files for markers
2. If marker found: extract generator name, search for script, add to review scope
3. Mark generated files for skip/light review
4. Warn if only generated files changed (may indicate stale regeneration)

**Edge Cases**:

- Generator also changed → Review generator only, skip generated
- Only generated changed → Warn: stale regeneration or manual edit
- Generator not found → Review generated file anyway
- Security-sensitive generated file → Still review (credentials, config)

Load [references/tier-5/generated-content-detection.md](references/tier-5/generated-content-detection.md) for complete detection patterns and algorithm.

### Step 2: Identify Scope

- **Explicit request**: User-specified files or changes
- **Staged changes**: `git diff --staged` or `git status`
- **Recent work**: Files modified in current session
- **PR scope**: All files in a pull request

### Step 3: Load Context

Check for repo-specific standards. If found, load for Layer 2 checks.

### Review Profiles

When `--profile <name>` is specified, restrict tier loading to profile-specific subsets. This enables focused reviews for specific concerns.

**Available Profiles:**

| Profile | Tiers Loaded | Description | Use Case |
| --- | --- | --- | --- |
| `security` | 0, 1.3, 3-security | OWASP, secrets, auth, crypto | Fast security scan before merge |
| `quick` | 1.1-1.6, 1.12 | Design, logic, style basics | Pre-commit fast check |
| `thorough` | All tiers + 1.30-1.32 | Complete analysis + reference/pattern checks | PR review (default) |
| `strict` | All thorough + deep patterns | Full analysis + architectural pattern enforcement | Library releases, major changes |
| `performance` | 0, 1.5, 2-backend, 3-concurrency | N+1, complexity, memory, concurrency | Performance audit |

**Profile Tier Mappings:**

```text
security:
  - Tier 0: Research Phase (ALWAYS - detect auth/crypto libraries)
  - Tier 1.3: Security (OWASP-Based)
  - Tier 3: security-patterns.md (when auth/crypto patterns detected)
  - Skip: Design, readability, testing, documentation

quick:
  - Tier 1.1: Design and Architecture (basic structure)
  - Tier 1.2: Functionality and Logic (obvious errors)
  - Tier 1.3: Security (CRITICAL only - hardcoded secrets)
  - Tier 1.4: Concurrency (obvious race conditions)
  - Tier 1.5: Performance (N+1, obvious inefficiencies)
  - Tier 1.6: Complexity (extreme violations)
  - Tier 1.12: Style (consistency)
  - Skip: Tier 0 MCP research, Tier 2+, Clean Code deep-dives

thorough:
  - ALL tiers loaded based on file types/patterns
  - Complete analysis (default behavior)
  - Section 1.30: Reference Integrity (always when renames/deletions detected)
  - Section 1.31: Breaking Changes (always for public API changes)
  - Section 1.32: Pattern Compliance (basic pattern checks)
  - Sections 1.33-1.36: Git History Context (coupling, hot spots, recent patterns)

strict:
  - ALL 'thorough' checks
  - Section 1.32 Pattern Compliance (full analysis):
    - Architectural pattern deviation (CQRS, mediator, repository)
    - DI registration consistency
    - File organization enforcement
  - Section 1.35: Author Context (ownership patterns, bus factor)
  - Import/export hygiene (module boundaries, barrel pollution)
  - Test correlation (orphaned tests detection)
  - Dependency safety (migration verification)

performance:
  - Tier 0: Research Phase (performance best practices via MCP)
  - Tier 1.5: Performance and Efficiency
  - Tier 2: backend-checks.md (database, API performance)
  - Tier 3: concurrency-patterns.md (async, threading)
  - Skip: Style, documentation, clean code deep-dives
```

**Token Savings by Profile:**

| Profile | Est. Tokens | Savings vs Strict |
| --- | --- | --- |
| security | ~5,500 | 60%+ |
| quick | ~3,500 | 75%+ |
| thorough | ~14,000 | 15% |
| strict | ~17,000 | 0% (baseline) |
| performance | ~6,000 | 65%+ |

### Baseline Mode (Differential Analysis)

When `--baseline <branch>` is specified, attribute each finding as NEW or PRE-EXISTING.

**Why This Matters:**
This is the #1 adoption blocker for code review tools. Teams with tech debt get overwhelmed by 100+ findings when their PR only introduces 3 new issues. They give up on the tool.

**Baseline Mode Workflow:**

1. **Build attribution map** from git diff:

   ```bash
   git diff <baseline>...HEAD  # Three-dot for symmetric comparison
   ```

2. **Parse diff** to identify changed line ranges per file
3. **For each finding**: Check if `file:line` is in changed ranges
4. **Tag findings**: NEW (line added/modified) or PRE-EXISTING (unchanged)
5. **Separate output**: New issues prominent, pre-existing collapsed

**Finding Attribution Rules:**

| Line Status | Attribution | Output Section |
| --- | --- | --- |
| Added (`+` in diff) | NEW | "New Issues Introduced" |
| Modified (in hunk, changed) | NEW | "New Issues Introduced" |
| Context (in hunk, unchanged) | PRE-EXISTING | "Pre-existing Issues" (collapsed) |
| Not in any hunk | PRE-EXISTING | "Pre-existing Issues" (collapsed) |
| Deleted (`-` in diff) | SKIP | Not reviewed (doesn't exist) |

**Baseline Output Format:**

```markdown
## Review Summary (Baseline Mode)

**Baseline**: `main`
**New Issues (this changeset)**: 2 CRITICAL, 1 MAJOR ← FOCUS HERE
**Pre-existing Issues**: 47 (collapsed)
**Assessment**: Based on NEW issues only

## New Issues Introduced
[Detailed findings with Attribution: NEW]

<details>
<summary>Pre-existing Issues (47)</summary>
[Condensed findings]
</details>
```

**Quality Gates (CI/CD):**

- `--fail-on-new-critical`: Exit 1 if ANY new CRITICAL
- `--fail-on-new-major`: Exit 1 if ANY new MAJOR
- Pre-existing issues do NOT fail the build

**Edge Cases:**

- Baseline doesn't exist → Error with valid branch suggestions
- File renamed → Attribute based on content changes
- Merge commits → Use three-dot diff for correct comparison

### Complexity Thresholds

Use these concrete thresholds when evaluating code complexity:

| Metric | Warning | Error | Measurement |
| --- | --- | --- | --- |
| Cyclomatic Complexity | > 10 | > 20 | Count decision points (if, while, for, case, &&, \|\|, ?) |
| Cognitive Complexity | > 15 | > 30 | SonarQube metric (nesting adds more weight) |
| Function Lines | > 30 | > 50 | Count non-blank, non-comment lines |
| Nesting Depth | > 3 | > 5 | Count nested braces/indentation levels |
| Parameter Count | > 4 | > 7 | Count function/method parameters |
| File Lines | > 300 | > 500 | Count total lines in file |

**When thresholds exceeded:**

- Warning → MINOR severity finding
- Error → MAJOR severity finding

**Suggested Fix Template:**

```markdown
### Complexity Threshold Exceeded

**File**: `src/services/order.ts:processOrder()`
**Severity**: MAJOR
**Metric**: Cyclomatic Complexity = 23 (threshold: 15, error: 20)

**Problem**: Function has 23 independent paths through the code.

**Impact**: Difficult to test (need 23+ test cases), hard to maintain, high bug risk.

**Fix**: Extract methods for logical branches. Consider:
- Extract validation logic → `validateOrder()`
- Extract pricing logic → `calculatePrice()`
- Extract notification logic → `notifyCustomer()`
```

### Progressive Loading (Token Optimization)

This skill uses **tiered progressive disclosure** to optimize token usage. Only load what's relevant to the files being reviewed.

**Tier 0 (MANDATORY - Always First):** Research Phase (~2,000 tokens)

- **ALWAYS load BEFORE analysis**: [references/tier-0/research-phase.md](references/tier-0/research-phase.md)
- Contains: Technology detection matrix, MCP query templates, "Build Truth Context" workflow
- Purpose: Query MCP servers to understand current patterns BEFORE making any claims
- **This tier is NOT optional** - skip only if code is purely internal with no external dependencies

**Tier 1 (Always Applied):** Universal checks in this file (~4,500 tokens)

- Sections 1.1-1.12: Design, Logic, Security, Concurrency, Performance, Readability, Testing, Error Handling, Documentation, Cross-Platform, Anti-Duplication, Style
- Sections 1.25-1.29: Clean Code (Names, Functions, Comments, Conditionals, Code Smells)
- Section 1.30: Reference Integrity - [references/tier-1/reference-integrity.md](references/tier-1/reference-integrity.md) (when renames/deletions detected)
- Section 1.31: Breaking Changes - [references/tier-1/breaking-changes.md](references/tier-1/breaking-changes.md) (for public API changes)
- Sections 1.33-1.36: Git History Context - [references/tier-1/git-history-context.md](references/tier-1/git-history-context.md) (thorough/strict profiles, ~1,500 tokens)

**Tier 2 (File-Type Triggered):** Load based on file extensions

| Files | Load Reference |
| --- | --- |
| .tsx, .jsx, .vue, .svelte | [references/tier-2/frontend-checks.md](references/tier-2/frontend-checks.md) |
| .py, .java, .cs, .go, .rb | [references/tier-2/backend-checks.md](references/tier-2/backend-checks.md) |
| .swift, .kt, .dart | [references/tier-2/mobile-checks.md](references/tier-2/mobile-checks.md) |
| .sql, migrations/* | [references/tier-2/database-checks.md](references/tier-2/database-checks.md) |
| .yaml, .json, .env, .toml | [references/tier-2/config-checks.md](references/tier-2/config-checks.md) |
| Dockerfile, *.tf, k8s/* | [references/tier-2/infrastructure-checks.md](references/tier-2/infrastructure-checks.md) |
| .ipynb, model/*, ml/* | [references/tier-2/ai-ml-checks.md](references/tier-2/ai-ml-checks.md) |

**Tier 3 (Content-Pattern Triggered):** Load when code contains specific patterns

| Pattern Keywords | Load Reference |
| --- | --- |
| auth, crypto, password, secret, token, jwt | [references/tier-3/security-patterns.md](references/tier-3/security-patterns.md) |
| async, await, thread, lock, mutex, concurrent | [references/tier-3/concurrency-patterns.md](references/tier-3/concurrency-patterns.md) |
| route, endpoint, @app, @Get, @Post, api/ | [references/tier-3/api-patterns.md](references/tier-3/api-patterns.md) |
| PII, email, user, customer, gdpr, consent | [references/tier-3/privacy-patterns.md](references/tier-3/privacy-patterns.md) |

**Clean Code Deep-Dives:** Load for detailed guidance

- [references/clean-code/naming-functions.md](references/clean-code/naming-functions.md) - Full naming and function principles
- [references/clean-code/code-smells.md](references/clean-code/code-smells.md) - Complete code smell catalog
- [references/clean-code/refactoring-patterns.md](references/clean-code/refactoring-patterns.md) - Refactoring techniques

**Tier 4 (Repository-Specific):** Load when repo config or CLAUDE.md exists

| Context | Load Reference |
| --- | --- |
| .claude/code-review.md exists | [references/tier-4/repo-config.md](references/tier-4/repo-config.md) |
| CLAUDE.md exists (always) | [references/tier-4/claude-md-core.md](references/tier-4/claude-md-core.md) |
| *.md files | [references/tier-4/documentation-rules.md](references/tier-4/documentation-rules.md) |
| Duplication indicators | [references/tier-4/anti-duplication-rules.md](references/tier-4/anti-duplication-rules.md) |
| Path patterns detected | [references/tier-4/path-rules.md](references/tier-4/path-rules.md) |
| *-{platform}.md files | [references/tier-4/platform-rules.md](references/tier-4/platform-rules.md) |
| .claude/skills/** | [references/tier-4/skill-rules.md](references/tier-4/skill-rules.md) |
| .claude/memory/** | [references/tier-4/memory-rules.md](references/tier-4/memory-rules.md) |
| .claude/temp/** | [references/tier-4/temp-file-rules.md](references/tier-4/temp-file-rules.md) |
| Profile thorough/strict | [references/tier-4/pattern-compliance.md](references/tier-4/pattern-compliance.md) |

**Tier 4b (Claude Code Components):** Delegate to specialized auditors when CC files detected

| File Pattern | Component Type | Auditor Agent |
| --- | --- | --- |
| `.claude/agents/**/*.md`, `agents/*.md` | Agent | `claude-ecosystem:agent-auditor` |
| `.claude/commands/**/*.md`, `commands/*.md` | Command | `claude-ecosystem:command-auditor` |
| `.claude/hooks/**`, `hooks.json` | Hook | `claude-ecosystem:hook-auditor` |
| `.claude/skills/**` | Skill | `claude-ecosystem:skill-auditor` |
| `CLAUDE.md`, `.claude/memory/**` | Memory | `claude-ecosystem:memory-component-auditor` |
| `output-styles/*.md` | Output Style | `claude-ecosystem:output-style-auditor` |
| `.mcp.json`, `mcp.json` | MCP Config | `claude-ecosystem:mcp-auditor` |
| `settings.json`, `.claude/settings.json` | Settings | `claude-ecosystem:settings-auditor` |
| `plugin.json`, `.claude-plugin/**` | Plugin | `claude-ecosystem:plugin-component-auditor` |
| Status line scripts | Status Line | `claude-ecosystem:statusline-auditor` |

Load the reference for complete detection and delegation patterns: [references/tier-4/claude-code-components.md](references/tier-4/claude-code-components.md)

**Note**: Tier 4b requires the `claude-ecosystem` plugin to be installed. If not installed, log a warning and skip CC-specific validation (continue with standard review).

> **Auditor Agent Verification:** Agent names may change between plugin releases. Run `/claude-ecosystem:list-skills`
> to verify current auditor agent names if delegation fails. The table above reflects known agents as of this file's last update.

**Tier 5 (Generated Content & MCP Validation Details):** Load based on changeset characteristics

| Trigger | Load Reference |
| --- | --- |
| Large changeset (50+ files) | [references/tier-5/generated-content-detection.md](references/tier-5/generated-content-detection.md) |
| Generation markers found | [references/tier-5/generated-content-detection.md](references/tier-5/generated-content-detection.md) |
| Need advanced MCP query patterns | [references/tier-5/mcp-validation.md](references/tier-5/mcp-validation.md) |
| Complex technology stack | [references/tier-5/mcp-validation.md](references/tier-5/mcp-validation.md) |
| Security patterns require OWASP validation | [references/tier-5/mcp-validation.md](references/tier-5/mcp-validation.md) |

**Note:** Primary MCP validation happens in **Tier 0 (Research Phase)** which is MANDATORY. Tier 5 `mcp-validation.md` provides additional query templates and advanced patterns for complex scenarios.

**Token Budget Estimates:**

| Scenario | Tokens |
| --- | --- |
| Tier 0 Research Phase (MANDATORY) | ~2,000 (always included) |
| Simple Python file | ~8,500 (Tier 0 + Hub + backend) |
| React component | ~8,000 (Tier 0 + Hub + frontend) |
| Auth service | ~10,000 (Tier 0 + Hub + backend + security) |
| Full-stack PR | ~11,500 (Tier 0 + Hub + frontend + backend + API) |
| Documentation file (CLAUDE.md repo) | ~8,500 (Tier 0 + Hub + core-rules + documentation-rules) |
| Skill modification | ~8,000 (Tier 0 + Hub + core-rules + skill-rules) |
| Memory file update | ~7,500 (Tier 0 + Hub + core-rules + memory-rules) |
| With advanced MCP patterns | +~1,200 tokens (Tier 5 mcp-validation.md) |
| With CC auditor delegation | +~1,500 tokens (Tier 4b reference + auditor spawn overhead) |
| With generated content detection | +~1,200 tokens (Tier 5 generated-content-detection.md) |
| With git history context (thorough/strict) | +~1,500 tokens (Tier 1 git-history-context.md) |

**Note:** Token budgets increased by ~2,000 tokens due to MANDATORY Tier 0 Research Phase. This trade-off provides significantly more accurate reviews through MCP validation.

## Layer 1: Universal Code Review Checklist

These checks apply to ANY codebase, ANY language.

### 1.1 Design and Architecture

- [ ] **Overall design makes sense** - Interactions between components are logical
- [ ] **Belongs in this codebase** - Not better suited for a library or different module
- [ ] **Integrates well** - Fits with existing system architecture
- [ ] **Right time for this change** - Not premature or addressing wrong problem
- [ ] **No over-engineering** - Solves current problem, not speculative future needs (YAGNI)

**SOLID Principles:**

- [ ] **Single Responsibility (SRP)** - Each class/function has ONE reason to change
- [ ] **Open-Closed (OCP)** - Open for extension, closed for modification (no repeated if/else for types)
- [ ] **Liskov Substitution (LSP)** - Derived classes substitutable for base (no explicit type casting)
- [ ] **Interface Segregation (ISP)** - Clients depend only on methods they use
- [ ] **Dependency Inversion (DIP)** - Depend on abstractions, not concrete implementations

### 1.2 Functionality and Logic

- [ ] **Does what it's supposed to do** - Implements intended functionality
- [ ] **Good for users** - Both end-users AND developers who'll use this code
- [ ] **Edge cases handled** - Boundary conditions, empty inputs, nulls
- [ ] **Error handling robust** - Failures handled gracefully with actionable messages
- [ ] **No logic errors** - Off-by-one, wrong operators, incorrect conditions

### 1.3 Security (OWASP-Based)

- [ ] **Input validation** - All inputs validated server-side (allowlist, not blocklist)
- [ ] **Output encoding** - Context-appropriate encoding (HTML, JS, SQL, URL)
- [ ] **No injection vulnerabilities** - SQL, command, XSS, path traversal
- [ ] **Authentication correct** - Login via POST, secure session handling, MFA where appropriate
- [ ] **Authorization enforced** - Role-based access, principle of least privilege
- [ ] **Secrets not hardcoded** - No API keys, passwords, tokens in code
- [ ] **Secrets not logged** - No sensitive data in logs, error messages, URLs
- [ ] **Cryptography modern** - bcrypt/Argon2 for passwords, AES-GCM for encryption, no MD5/SHA1
- [ ] **Dependencies secure** - No known vulnerabilities in third-party libraries

### 1.4 Concurrency and Thread Safety

- [ ] **Shared state protected** - Proper locks, mutexes, or atomics for shared data
- [ ] **No race conditions** - Concurrent access patterns analyzed
- [ ] **Consistent lock ordering** - Locks acquired in same order to prevent deadlocks
- [ ] **No circular dependencies** - Between resources protected by different locks
- [ ] **Async patterns correct** - Await used properly, exceptions propagated
- [ ] **Thread-safe collections** - Concurrent collections used where needed
- [ ] **No deadlock potential** - Timeout mechanisms, no indefinite waits while holding locks

### 1.5 Performance and Efficiency

- [ ] **No unnecessary operations** - Efficient algorithms, no redundant work
- [ ] **Appropriate data structures** - Right choice for access patterns
- [ ] **No N+1 queries** - Database queries optimized
- [ ] **Memory efficient** - No leaks, appropriate caching
- [ ] **I/O optimized** - Async for I/O-bound, batching where appropriate
- [ ] **No blocking in async** - Sync operations not blocking async contexts

### 1.6 Complexity and Readability

- [ ] **Not more complex than needed** - Can be understood quickly
- [ ] **Functions/classes reasonable size** - Single responsibility, not too long
- [ ] **No deep nesting** - Max 3-4 levels of indentation
- [ ] **Clear naming** - Names fully communicate purpose without being too long
- [ ] **Comments explain WHY** - Not what (code should be self-documenting)
- [ ] **No code duplication** - DRY principle followed

### 1.7 Testing

- [ ] **Tests included** - Unit/integration tests appropriate for change
- [ ] **Tests are correct** - Actually test what they claim to test
- [ ] **Tests are useful** - Will fail when code breaks
- [ ] **Edge cases tested** - Boundary conditions, error scenarios
- [ ] **Tests maintainable** - Not overly complex, clear assertions
- [ ] **No flaky tests** - Deterministic, not timing-dependent

**Test Smell Detection:**

Review test code for common test smells that reduce test quality and maintainability:

| Smell | Detection | Severity | Why It Matters |
| --- | --- | --- | --- |
| **Empty Test** | Test method with no assertions | CRITICAL | False confidence - test always passes |
| **Eager Test** | > 5 assertions in one test | WARNING | When it fails, unclear which behavior broke |
| **Mystery Guest** | External file/network access without mock | MAJOR | Flaky, slow, environment-dependent |
| **Assertion Roulette** | Multiple asserts without descriptive messages | MINOR | Hard to identify which assertion failed |
| **Sleep in Test** | `Thread.Sleep`, `await Task.Delay`, `setTimeout` | MAJOR | Slow, flaky, hides timing bugs |
| **Dead Test** | Test that never fails (always passes) | WARNING | Usually tests nothing meaningful |
| **Commented Test** | Disabled test cases (`[Ignore]`, `skip`, `xtest`) | WARNING | Technical debt, may hide real issues |
| **Test Code Duplication** | Same setup/teardown in multiple tests | MINOR | Maintenance burden, use fixtures |

**Example Findings:**

```markdown
### Test Smell: Eager Test

**File**: `tests/UserService.test.ts:45`
**Severity**: WARNING
**Confidence**: MEDIUM

**Problem**: Test "should handle user operations" has 12 assertions testing multiple behaviors.

**Impact**: When this test fails, you won't know which behavior broke without debugging.

**Suggested Fix**:
```typescript
// Before (Eager Test - 12 assertions, multiple behaviors)
test('should handle user operations', () => {
  const user = createUser();
  expect(user.name).toBe('John');
  expect(user.email).toContain('@');
  // ... 10 more assertions about different behaviors
});

// After (Focused Tests - one behavior each)
test('should create user with valid name', () => {
  const user = createUser();
  expect(user.name).toBe('John');
});

test('should validate email format', () => {
  const user = createUser();
  expect(user.email).toContain('@');
});
```

```text

```markdown
### Test Smell: Sleep in Test

**File**: `tests/api.test.ts:78`
**Severity**: MAJOR
**Confidence**: HIGH

**Problem**: Test uses `await new Promise(r => setTimeout(r, 2000))` to wait for async operation.

**Impact**: Test is slow (2 seconds), flaky (timing varies), and hides real async handling bugs.

**Suggested Fix**:
```typescript
// Before (Sleep - slow and flaky)
await new Promise(r => setTimeout(r, 2000));
expect(result).toBeDefined();

// After (Proper async handling)
await waitFor(() => expect(result).toBeDefined());
// Or
await expect(asyncOperation()).resolves.toBeDefined();
```

```text

### 1.8 Error Handling and Logging

- [ ] **Errors caught appropriately** - Right level of granularity
- [ ] **Error messages actionable** - Clear what went wrong and how to fix
- [ ] **Logging present** - For debugging and troubleshooting
- [ ] **No sensitive data in logs** - PII, passwords, keys excluded
- [ ] **Graceful degradation** - Partial failures don't crash entire system

### 1.9 Documentation

- [ ] **Code documented** - Public APIs, complex logic explained
- [ ] **README updated** - If behavior/setup changes
- [ ] **API docs updated** - If endpoints change
- [ ] **Inline comments where needed** - For non-obvious decisions

### 1.10 Cross-Platform Compatibility

- [ ] **No hardcoded platform paths**:
  - `/mnt/c/Users/...` (WSL)
  - `/c/Users/...` (Git Bash)
  - `C:\Users\...` (Windows)
  - `/home/username/...` (Linux)
  - `/Users/username/...` (macOS)
- [ ] **Portable tool detection** - `command -v tool` not path hunting
- [ ] **Platform fallbacks** - Graceful handling when features unavailable
- [ ] **Scripts self-locate** - Use `Path(__file__).resolve()`, `$PSScriptRoot`, `${BASH_SOURCE[0]}`

### 1.11 Anti-Duplication

- [ ] **No duplicate content** - Same info in ONE place only
- [ ] **No identical files** - `diff` similar files to verify
- [ ] **Single source of truth** - Link instead of copy-paste
- [ ] **Config files distinct** - Each serves different purpose

### 1.12 Style and Consistency

- [ ] **Follows style guide** - Language/project conventions
- [ ] **Consistent with codebase** - Matches existing patterns
- [ ] **No style changes mixed with logic** - Separate formatting PRs

### 1.13 Accessibility (WCAG 2.1 AA)

- [ ] **Alt text present** - All images have descriptive alt text; decorative images use `alt=""`
- [ ] **Color contrast sufficient** - 4.5:1 for text, 3:1 for UI components
- [ ] **Keyboard navigable** - All interactive elements via Tab/Enter/Space; no keyboard traps
- [ ] **Focus visible** - Clear focus indicators on all interactive elements
- [ ] **Semantic HTML** - Proper heading hierarchy; buttons not divs; links not spans
- [ ] **ARIA correct** - Used only when semantic HTML insufficient; no conflicting roles

### 1.14 Internationalization (i18n)

- [ ] **No hardcoded strings** - All user-facing text externalized to resource files
- [ ] **Locale-aware formatting** - Dates, numbers, currency use locale APIs
- [ ] **RTL consideration** - Logical CSS properties where applicable
- [ ] **No string concatenation** - Use parameterized messages, not `"Hello " + name`
- [ ] **Pluralization handled** - Proper plural rules, not `count + " items"`

### 1.15 Observability

- [ ] **Structured logging** - JSON format with trace IDs, timestamps, context
- [ ] **Metrics present** - Latency, error rates, throughput for critical paths
- [ ] **Trace context propagated** - Distributed tracing across service boundaries
- [ ] **Health checks implemented** - Liveness/readiness probes with dependency checks
- [ ] **SLOs defined** - Measurable service level objectives for key operations

### 1.16 Data Privacy (GDPR/CCPA)

- [ ] **PII identified and protected** - Personal data encrypted, access controlled
- [ ] **Data retention enforced** - Clear policies, automated cleanup
- [ ] **Right to deletion** - Complete erasure across all systems possible
- [ ] **Consent tracked** - Explicit opt-in with audit trail
- [ ] **No PII in logs** - Redaction or hashing of personal identifiers

### 1.17 API Design

- [ ] **Versioning strategy** - Clear version in URL, header, or media type
- [ ] **Backward compatible** - New fields nullable, no removed fields
- [ ] **Deprecation documented** - Sunset dates, migration paths
- [ ] **Consistent naming** - Follows REST/GraphQL conventions
- [ ] **Error responses standardized** - Consistent error format across endpoints

### 1.18 Dependency Management

- [ ] **No known vulnerabilities** - CVE scanning in CI/CD
- [ ] **License compliance** - No GPL conflicts with proprietary code
- [ ] **Version pinned** - Lockfiles present and up-to-date
- [ ] **Transitive deps reviewed** - Indirect dependencies also secure
- [ ] **SBOM available** - Software Bill of Materials for audits

### 1.19 Database Patterns

- [ ] **N+1 queries avoided** - Eager loading or batch queries used
- [ ] **Indexes present** - For foreign keys, join columns, query patterns
- [ ] **Migrations backward compatible** - Incremental changes, no data loss
- [ ] **Schema properly normalized** - Or denormalized with clear rationale
- [ ] **Query optimization** - Explain plans reviewed for complex queries

### 1.20 Configuration Management

- [ ] **Secrets in vault** - Never hardcoded, use env vars or secrets manager
- [ ] **Feature flags used** - For gradual rollouts, A/B testing
- [ ] **12-factor compliant** - Config via environment, not files
- [ ] **Validation at startup** - Fail fast on missing/invalid config
- [ ] **Environment parity** - Same config structure across dev/staging/prod

### 1.21 Cloud/Infrastructure (12-Factor)

- [ ] **Stateless processes** - No local session storage, use external stores
- [ ] **Port binding** - Self-contained, exports HTTP via port
- [ ] **Disposability** - Fast startup, graceful SIGTERM shutdown
- [ ] **Dev/prod parity** - Minimal gap between environments
- [ ] **Container best practices** - Multi-stage builds, non-root user, resource limits
- [ ] **IaC used** - Terraform/CloudFormation for reproducibility

### 1.22 Frontend Patterns

- [ ] **Component design** - Small, reusable, composition over inheritance
- [ ] **State management** - Appropriate tool (local, context, Zustand, Redux)
- [ ] **Bundle size** - Code splitting, lazy loading, < 500KB main bundle
- [ ] **Memoization** - Strategic use of memo/useMemo/useCallback
- [ ] **Web Vitals** - LCP < 2.5s, FID < 100ms, CLS < 0.1

### 1.23 Mobile Patterns

- [ ] **Battery efficient** - WorkManager/JobScheduler, batched operations
- [ ] **Offline-first** - Local caching with sync, offline queue
- [ ] **Responsive layout** - Flexible dimensions (dp/sp), rotation handling
- [ ] **Memory efficient** - Image downsampling, lifecycle awareness
- [ ] **Network efficient** - Request batching, compression, exponential backoff

### 1.24 AI/ML Code Patterns

- [ ] **Model versioning** - MLflow/DVC for models and data
- [ ] **Reproducibility** - Random seeds, pinned dependencies, exact environments
- [ ] **Bias detection** - Fairness metrics across demographics
- [ ] **Data pipeline validated** - Schema validation, statistical tests
- [ ] **Model monitoring** - Drift detection for data and performance

### 1.25 Clean Code: Names (Robert C. Martin)

- [ ] **Intention-revealing names** - Name tells you why it exists, what it does, how it's used
- [ ] **No misleading names** - `accountList` should actually be a list; avoid false clues
- [ ] **Meaningful distinctions** - Not `data1`, `data2`, `dataInfo`, `theData`
- [ ] **Pronounceable names** - Can discuss code verbally without spelling variables
- [ ] **Searchable names** - Single-letter names only for small local scope
- [ ] **No encodings** - No Hungarian notation, no type prefixes (strName, intCount)
- [ ] **No mental mapping** - Reader shouldn't translate names to concepts they know
- [ ] **Class names are nouns** - Customer, Account, Parser (not verbs)
- [ ] **Method names are verbs** - postPayment, deletePage, save (not nouns)

### 1.26 Clean Code: Functions (Robert C. Martin)

- [ ] **Small** - 5-20 lines ideal; rarely exceed 30 lines
- [ ] **Do one thing** - Single level of abstraction; one reason to change
- [ ] **One abstraction level** - Don't mix getHtml() with .append("\n")
- [ ] **Descriptive names** - Long descriptive name better than short enigmatic one
- [ ] **Few arguments** - Zero ideal, one/two good, three questionable, never more than four
- [ ] **No flag arguments** - Split function into two instead of passing boolean
- [ ] **No side effects** - Don't modify unexpected state; function does what name says only
- [ ] **Command/Query separation** - Either do something OR answer something, never both
- [ ] **Prefer exceptions to error codes** - Don't return -1 or null for errors
- [ ] **Extract try/catch blocks** - Bodies of try/catch should be one-line function calls

### 1.27 Clean Code: Comments (Robert C. Martin)

- [ ] **Code explains itself first** - If you need a comment, try rewriting the code
- [ ] **Comments explain WHY** - Not what (code shows what) or how (code shows how)
- [ ] **Legal comments acceptable** - Copyright, license headers
- [ ] **Informative comments acceptable** - Regex explanation, return value meaning
- [ ] **TODO comments have tickets** - `// TODO: TICKET-123 - refactor after API v2`
- [ ] **No redundant comments** - `// Constructor` above a constructor is noise
- [ ] **No commented-out code** - Delete it; version control remembers
- [ ] **No closing brace comments** - `} // end if` means function is too long
- [ ] **No attribution comments** - `// Added by Bob` - use version control blame
- [ ] **No journal comments** - Change logs belong in VCS, not code

### 1.28 Clean Code: Conditionals (Pragmatic Programmer)

- [ ] **Positive conditions** - `if (isValid)` not `if (!isInvalid)`
- [ ] **No double negatives** - `if (!notFound)` should be `if (found)`
- [ ] **Guard clauses** - Early return for edge cases; avoid deep nesting
- [ ] **Explanatory variables** - Extract complex conditions to named booleans
- [ ] **Encapsulate conditionals** - `if (shouldBeDeleted(timer))` not `if (timer.hasExpired() && !timer.isRecurrent())`
- [ ] **Avoid negative conditionals** - `if (buffer.shouldCompact())` not `if (!buffer.shouldNotCompact())`
- [ ] **Polymorphism over switch** - Type-based switches often indicate missing polymorphism
- [ ] **No null checks everywhere** - Use Null Object pattern or Optional types

### 1.29 Code Smells Quick Reference

| Smell | Detection | Impact | Fix |
| --- | --- | --- | --- |
| **Long Method** | > 30 lines | Maintainability | Extract methods |
| **Long Parameter List** | > 4 parameters | Usability | Introduce parameter object |
| **Deep Nesting** | > 3-4 indent levels | Readability | Guard clauses, extract method |
| **Magic Numbers** | Hardcoded values | Maintainability | Named constants |
| **God Class** | Class does too much | Testability, coupling | Extract classes by responsibility |
| **Feature Envy** | Method uses other class's data | Coupling | Move method to data class |
| **Duplicate Code** | Same logic repeated | DRY violation | Extract to shared function |
| **Dead Code** | Unused code | Clutter, confusion | Delete it |
| **Primitive Obsession** | Overuse of primitives | Type safety | Value objects |
| **Shotgun Surgery** | One change touches many files | Fragility | Consolidate related code |
| **Divergent Change** | One class changed for many reasons | SRP violation | Split by reason for change |
| **Data Clumps** | Same data appears together | Missing abstraction | Create class for data group |
| **Comments** | Explaining bad code | Readability | Rewrite the code |
| **Speculative Generality** | Code for "future needs" | Complexity | Delete unused abstractions |

### 1.30 Reference Integrity (Rename/Cleanup Validation)

**Triggered by:** Git diff shows renames (R) or deletions (D)

When files, functions, classes, or variables are renamed or deleted, verify all references are updated.

- [ ] **Imports updated** - No broken imports referencing old paths/names
- [ ] **Documentation links valid** - No stale markdown links to renamed/deleted files
- [ ] **Config references current** - No orphaned references in tsconfig, package.json, etc.
- [ ] **String literals checked** - Hardcoded references to old names (low confidence, profile-gated)

**Detection:**

```bash
# Detect renames and deletions from git diff
git diff --name-status HEAD~1 | grep -E '^[RD]'
```

**Severity:**

| Check | Severity | Always-On |
| --- | --- | --- |
| Broken imports after rename | CRITICAL | Yes |
| Stale documentation links | MAJOR | Yes |
| Orphaned config references | MAJOR | Yes |
| Hardcoded string references | MINOR | Profile (thorough+) |

**Load Reference:** [references/tier-1/reference-integrity.md](references/tier-1/reference-integrity.md) when renames/deletions detected.

### 1.31 Breaking Change Detection

**Triggered by:** Changes to public API surface

Detect changes that may break external consumers of public APIs.

- [ ] **No public member removal** - Public methods/classes not deleted without deprecation
- [ ] **Signatures preserved** - Parameter types/counts unchanged
- [ ] **Return types compatible** - Return types not changed without migration path
- [ ] **Behavior documented** - Semantic changes flagged via annotations

**Detection:**

```bash
# Identify removed public members
git diff HEAD~1 | grep "^-.*public\s"
```

**Severity:**

| Check | Severity | Always-On |
| --- | --- | --- |
| Public API removal | CRITICAL | Yes |
| Signature change | CRITICAL | Yes |
| Return type change | MAJOR | Yes |
| Behavior change (manual) | MAJOR | Flag |

**Load Reference:** [references/tier-1/breaking-changes.md](references/tier-1/breaking-changes.md) for public API changes.

### 1.32 Pattern Compliance

**Triggered by:** `thorough` or `strict` profile

Verify new code matches established patterns in the codebase.

- [ ] **Error handling consistent** - Matches codebase pattern (Result<T>, exceptions, etc.)
- [ ] **Naming conventions followed** - Class/method/variable naming matches established style
- [ ] **Architectural patterns respected** - CQRS, repository, etc. patterns maintained
- [ ] **File organization matches** - New files in expected locations per project structure

**Load Reference:** [references/tier-4/pattern-compliance.md](references/tier-4/pattern-compliance.md) for pattern detection and comparison.

### 1.33 Missing Co-Changed File (Git History)

**Triggered by:** `thorough` or `strict` profile

Detect files that frequently change together but are missing from the review scope.

- [ ] **Co-change patterns analyzed** - Files with >60% co-change rate identified
- [ ] **Missing companions flagged** - Related files not in review scope
- [ ] **Test coupling verified** - Source changes include related test files

**Severity:** MAJOR (files with >60% co-change rate missing may indicate incomplete change)

**Load Reference:** [references/tier-1/git-history-context.md](references/tier-1/git-history-context.md)

### 1.34 Hot Spot Under Review (Git History)

**Triggered by:** `thorough` or `strict` profile

Identify high-churn files that warrant extra scrutiny.

- [ ] **Change frequency analyzed** - Files changed 10+ times in configured window flagged
- [ ] **Commit patterns classified** - Bug fixes, features, refactoring identified
- [ ] **Extra scrutiny applied** - Higher review priority for hot spots

**Severity:** WARNING (high-churn files may indicate design issues or fragile code)

**Load Reference:** [references/tier-1/git-history-context.md](references/tier-1/git-history-context.md)

### 1.35 Single-Owner File (Git History)

**Triggered by:** `strict` profile only

Identify files with ownership concentration (bus factor risk).

- [ ] **Ownership analyzed** - Primary author (>90% commits) identified
- [ ] **Bus factor noted** - Single-owner files flagged for knowledge sharing
- [ ] **New author changes** - Flag when new authors modify established files

**Severity:** INFO (awareness item, not a blocking issue)

**Load Reference:** [references/tier-1/git-history-context.md](references/tier-1/git-history-context.md)

### 1.36 Recent Bug Fix Area (Git History)

**Triggered by:** `thorough` or `strict` profile

Identify areas with recent bug fix activity that may be fragile.

- [ ] **Bug fix history analyzed** - Recent commits with fix/bug/patch keywords
- [ ] **Fragile areas flagged** - 3+ bug fixes in configured window
- [ ] **Extra edge case scrutiny** - Higher attention to error paths

**Severity:** WARNING (areas with recent fixes may need extra care)

**Load Reference:** [references/tier-1/git-history-context.md](references/tier-1/git-history-context.md)

## Layer 2: Repo-Specific Checks

**Only if CLAUDE.md or repo standards exist.**

### 2.1 Pattern Compliance

- [ ] **Follows existing patterns** - Similar to other files in repo
- [ ] **Naming conventions match** - Consistent with established names
- [ ] **File structure correct** - In right location with right layout

### 2.2 CLAUDE.md Anti-Patterns (if applicable)

- [ ] **No mixed OS content** - Each file for one platform
- [ ] **No README.md in topic folders** - Only at root
- [ ] **No numbered filenames** - `git-setup.md` not `01-git-setup.md`
- [ ] **Title-filename consistency** - Filename matches `# Header`

## Layer 3: Repository Rules (CLAUDE.md Compliance)

**Only for repositories with CLAUDE.md in root.** Load Tier 4 references based on file types being reviewed.

### 3.1 Detection and Activation

1. Check for `CLAUDE.md` in repo root
2. Check for `.claude/memory/` directory
3. If both exist, apply Layer 3 checks
4. Load [tier-4/claude-md-core.md](references/tier-4/claude-md-core.md) for every review

### 3.2 Quick Reference Checklist

- [ ] **No absolute paths** - Use root-relative or placeholders (`<repo-root>`, `<skill-name>`)
- [ ] **Title-filename match** - `git-setup-windows.md` -> `# Git Setup Windows`
- [ ] **No platform mixing** - Each file serves one platform only
- [ ] **No README in topic folders** - Only at root and hub levels
- [ ] **No numbered files** - `git-setup.md` not `01-git-setup.md`
- [ ] **Temp files in .claude/temp/** - Nowhere else, correct naming convention
- [ ] **Single source of truth** - Link, don't duplicate content
- [ ] **UTF-8 encoding** - ASCII punctuation only (no smart quotes)
- [ ] **Official sources** - Documentation backed by official docs with Last Verified dates

### 3.3 Documentation Files (*.md)

Load [tier-4/documentation-rules.md](references/tier-4/documentation-rules.md) for:

- [ ] **Official documentation links** - Required for all setup guides
- [ ] **Version information** - Current and minimum versions documented
- [ ] **Installation steps** - In dependency order
- [ ] **Verification steps** - With expected output
- [ ] **Last Verified date** - Present and recent

### 3.4 Platform-Specific Files (*-{platform}.md)

Load [tier-4/platform-rules.md](references/tier-4/platform-rules.md) for:

- [ ] **Platform separation** - No mixed OS content
- [ ] **Correct suffix** - `-windows`, `-macos`, `-linux`, `-wsl`
- [ ] **WSL redirect pattern** - Redirects to Linux where appropriate
- [ ] **Hub completeness** - All platform hubs updated together

### 3.5 Anti-Duplication

Load [tier-4/anti-duplication-rules.md](references/tier-4/anti-duplication-rules.md) when duplication indicators detected:

- [ ] **No duplicate content** - Each piece of info in ONE place
- [ ] **Version in Last Verified only** - All other files link to it
- [ ] **Hub links to spokes** - No content duplication between hub and references
- [ ] **One report per task** - Consolidate multiple reports

### 3.6 Path Conventions

Load [tier-4/path-rules.md](references/tier-4/path-rules.md) when path patterns detected:

- [ ] **No absolute paths** - Platform-specific absolute paths are forbidden
- [ ] **Root-relative paths** - From repo root, not current directory
- [ ] **Generic placeholders** - `<repo-root>`, `<skill-name>` over explicit paths
- [ ] **Script self-location** - `Path(__file__).resolve()`, `$PSScriptRoot`

### 3.7 Skill Files (.claude/skills/**)

Load [tier-4/skill-rules.md](references/tier-4/skill-rules.md) for:

- [ ] **SKILL.md structure** - Required sections present
- [ ] **YAML frontmatter** - name, description, allowed-tools
- [ ] **Progressive disclosure** - Tiered reference loading
- [ ] **Skill encapsulation** - No internal paths exposed externally

### 3.8 Memory Files (.claude/memory/**)

Load [tier-4/memory-rules.md](references/tier-4/memory-rules.md) for:

- [ ] **Import syntax** - `@.claude/memory/file.md`
- [ ] **Token budget documented** - Approximate token count noted
- [ ] **Context guidance** - When to load (always vs context-dependent)
- [ ] **Last Updated date** - Present and accurate

### 3.9 Temp Files (.claude/temp/**)

Load [tier-4/temp-file-rules.md](references/tier-4/temp-file-rules.md) for:

- [ ] **Correct location** - Only `.claude/temp/` allowed
- [ ] **Naming convention** - `YYYY-MM-DD_HHmmss-{agent-type}-{topic}.md`
- [ ] **Flat structure** - No subdirectories
- [ ] **UTC timestamps** - ISO 8601 format

## Severity Classification

### Critical (Must Fix)

- Security vulnerabilities (injection, auth bypass, secrets exposure)
- Data loss or corruption potential
- Race conditions in production code
- Broken functionality
- Hardcoded secrets or credentials

### Warning (Should Fix)

- Performance issues
- Missing error handling
- Inadequate test coverage
- Code duplication
- Hardcoded platform paths
- Poor naming

### Suggestion (Consider)

- Style improvements (prefix with "Nit:")
- Alternative approaches
- Documentation enhancements
- Refactoring opportunities

## Report Format

```markdown
## Code Review Findings

### Configuration Summary

**Config Source**: `.claude/code-review.md` | CLAUDE.md + @imports (fallback) | Defaults only
**Tech Stack**: .NET 10, ASP.NET Core 10 (config override) | React 19 (auto-detected)
**Rules Excluded**: [count] ([list if any])
**Severity Overrides**: [count] ([rule: old→new if any])
**Custom Checks**: [count] ([list if any])

### Technology Research Summary (from Step 0)

| Category | Technology | Version | MCP Source | Detection |
| --- | --- | --- | --- | --- |
| Runtime | .NET | 10 | perplexity | config override |
| Framework | ASP.NET Core | 10 | microsoft-learn + perplexity | config override |
| Frontend | React | 19 | context7 | package.json |

### Critical Issues (Must Fix)
1. **[Issue Title]**
   - **Location**: file:line
   - **Problem**: What's wrong and why it matters
   - **Confidence**: HIGH | MEDIUM | LOW
   - **Fix**: Specific code change
   - **Suggested Fix** (when Confidence is HIGH):
     ```language
     // Before (problematic)
     [original code]

     // After (fixed)
     [corrected code]
     ```
   - **Rule Source**: Tier 1 (Universal) - 1.3 Security | Tier 4 (repo-config.md) - Custom Check
   - **Validated**: Yes - [Source] [mcp-server-name]

### Warnings (Should Fix)
1. **[Issue Title]**
   - **Location**: file:line
   - **Problem**: What's wrong
   - **Confidence**: HIGH | MEDIUM | LOW
   - **Fix**: Specific change
   - **Suggested Fix** (when Confidence is HIGH):
     ```language
     // Before
     [original code]

     // After
     [corrected code]
     ```
   - **Rule Source**: Tier 1 (Universal) - 1.5 Performance | CLAUDE.md - Critical Rules
   - **Validated**: Yes/No - [Source if validated]

### Suggestions (Nit)
1. [Suggestion with rationale]
   - **Confidence**: LOW (stylistic)
   - **Rule Source**: Tier 1 (Universal) - 1.12 Style

### MCP Validation Summary

**Sources Consulted**: [count]
**Findings Validated**: [validated/total]
**Corrections Applied**: [count] (findings corrected based on MCP research)

| Finding | Source | Status |
| --- | --- | --- |
| [Finding] | [mcp-server] | Confirmed/Corrected/Outdated |
```

### Rule Source Values

The **Rule Source** field indicates which rule triggered the finding:

| Source Type | Format | Examples |
| --- | --- | --- |
| Universal checks | `Tier 1 (Universal) - {section}` | `Tier 1 (Universal) - 1.3 Security` |
| File-type checks | `Tier 2 ({type}) - {section}` | `Tier 2 (Backend) - API Design` |
| Content-triggered | `Tier 3 ({pattern}) - {section}` | `Tier 3 (Security) - OWASP Auth` |
| Repo config | `Tier 4 (repo-config.md) - {section}` | `Tier 4 (repo-config.md) - Custom Check: PowerShell Naming` |
| CLAUDE.md | `CLAUDE.md - {section}` | `CLAUDE.md - Critical Rules` |
| Custom check | `Custom Check: {name}` | `Custom Check: No Console.WriteLine` |

**Validation Status Options:**

- **Yes - [Source] [mcp-server]**: Finding validated against authoritative source
- **No (internal pattern)**: No external reference needed (repo-specific convention)
- **No (MCP unavailable)**: MCP servers unavailable; manual verification recommended

### Confidence Levels

The **Confidence** field indicates how certain the finding is:

| Level | Criteria | Suggested Fix? |
| --- | --- | --- |
| **HIGH** | Exact pattern match + MCP validated | YES - Generate actionable fix code |
| **MEDIUM** | Semantic analysis, recognizable anti-pattern | OPTIONAL - Code snippet if clear pattern |
| **LOW** | Heuristic/stylistic, may be false positive | NO - Describe issue only |

**Confidence Assignment Logic:**

```text
1. Pattern match detected?
   ├── YES + MCP validates pattern → HIGH
   ├── YES + No MCP validation → MEDIUM
   └── NO → Continue to heuristics

2. Anti-pattern recognized?
   ├── YES + Clear remediation path → MEDIUM
   └── YES + Ambiguous remediation → LOW

3. Stylistic/subjective concern?
   └── Always → LOW
```

**Examples by Confidence Level:**

| Finding | Confidence | Reason |
| --- | --- | --- |
| SQL injection via string concat | HIGH | Exact pattern, OWASP-documented fix |
| Missing null check | MEDIUM | Recognized pattern, context-dependent fix |
| Method too long (35 lines) | LOW | Heuristic, may be acceptable in context |
| Variable naming suggestion | LOW | Stylistic preference |

### Suggested Fix Guidelines

**Include Suggested Fix when:**

1. **Confidence is HIGH** - Pattern match + MCP validated
2. **Fix is deterministic** - Only one correct way to fix
3. **MCP provides code pattern** - Fix based on authoritative source

**Suggested Fix Format:**

```markdown
**Suggested Fix**:
```csharp
// Before (vulnerable)
var query = "SELECT * FROM Users WHERE Id = " + userId;

// After (parameterized - OWASP recommendation)
var query = "SELECT * FROM Users WHERE Id = @userId";
cmd.Parameters.AddWithValue("@userId", userId);
```

```text

**Omit Suggested Fix when:**

1. **Confidence is LOW** - May be false positive
2. **Multiple valid approaches** - User should choose
3. **Context-dependent** - Requires understanding broader system
4. **MCP unavailable** - Cannot validate the fix pattern

## Anti-Patterns (What NOT to Do)

- **"Looks good overall"** - Never without systematic checklist review
- **Benefit of the doubt** - If questionable, it IS a finding
- **Summarizing** - Critically analyze against checklist
- **Missing security issues** - Always check OWASP basics
- **Ignoring concurrency** - Think through race conditions
- **Skipping similar files** - Always diff files with similar purposes
- **Vague fixes** - "Fix this" vs "Replace lines X-Y with..."
- **Partial table verification** - Never verify only SOME items from a reference table; if you cite a table, verify ALL items with Glob or git status
- **Concluding files missing without Glob** - When uncertain if files exist, use `Glob pattern="path/**/*.md"` to verify rather than assuming based on what you haven't read

## Behavioral Rules

1. **Be skeptical, not charitable** - Assume problems until verified clean
2. **Every line matters** - Review ALL code assigned, understand it
3. **Think like an attacker** - What could go wrong? How could this be exploited?
4. **Think like a user** - Both end-user and developer-user
5. **Context matters** - View changes in context of whole file/system
6. **Report everything** - Every issue, with appropriate severity
7. **Propose specific fixes** - Concrete code, not vague suggestions
8. **Acknowledge good things** - Compliment well-done code

## Quick Reference Card

```text
ALWAYS CHECK:
[ ] Security: inputs validated, outputs encoded, no secrets
[ ] Concurrency: shared state protected, no race conditions
[ ] Design: SOLID principles, appropriate complexity
[ ] Tests: present, correct, useful
[ ] Platform: no hardcoded paths, portable detection
[ ] Duplicates: diff similar files
[ ] Accessibility: alt text, contrast, keyboard nav, semantic HTML
[ ] i18n: no hardcoded strings, locale-aware formatting
[ ] Observability: structured logs, metrics, traces, health checks
[ ] Privacy: PII protected, no PII in logs, consent tracked

CLEAN CODE (Robert C. Martin):
[ ] Names: intention-revealing, pronounceable, searchable, no encodings
[ ] Functions: small (5-20 lines), do one thing, few args (0-2), no side effects
[ ] Comments: explain WHY not WHAT, no commented-out code, no redundancy
[ ] Conditionals: positive conditions, guard clauses, no double negatives

DOMAIN-SPECIFIC (when applicable):
[ ] API: versioning, backward compat, error format
[ ] Database: N+1 avoided, indexes, migrations safe
[ ] Config: secrets in vault, feature flags, 12-factor
[ ] Frontend: component design, bundle size, web vitals
[ ] Mobile: battery/memory/network efficient, offline-first
[ ] AI/ML: model versioning, reproducibility, bias detection

CODE SMELLS (watch for):
- Long methods (> 30 lines)
- Long parameter lists (> 4 params)
- Deep nesting (> 3-4 levels)
- God classes (too many responsibilities)
- Feature envy (method uses other class's data)
- Primitive obsession (should use value objects)
- Shotgun surgery (one change touches many files)

RED FLAGS:
- Long if/else chains (OCP violation)
- Explicit type casting (LSP violation)
- new keyword overuse (DIP violation)
- String concatenation in queries (injection)
- Shared state without locks (race condition)
- Catch-all exception handlers (error hiding)
- Magic numbers/strings (maintainability)
- Platform-specific paths (portability)
- Missing alt text on images (accessibility)
- Hardcoded user-facing strings (i18n)
- console.log instead of structured logging (observability)
- PII in log statements (privacy violation)
```

## References

- [Detailed Checklist](references/checklist.md) - Extended checklist with detection patterns
- [Google Engineering Practices](https://google.github.io/eng-practices/review/)
- [OWASP Secure Code Review](https://owasp.org/www-project-code-review-guide/)

## Version History

- v9.0.0 (2025-12-31): **MAJOR: Enhanced Validation Gaps** - Added 6 new validation capabilities: (1) Reference Integrity (section 1.30) - validates imports, docs links, config after renames/deletions; (2) Breaking Change Detection (section 1.31) - detects public API removals, signature changes; (3) Pattern Compliance (section 1.32) - verifies error handling, naming, architecture consistency; (4) Import/Export Hygiene - unused imports, circular deps, module boundaries; (5) Test Impact Correlation - code changes without test updates; (6) Dependency Update Safety - major version bumps, breaking changes. Added new `strict` profile for library releases. Token budget updated: thorough ~14K, strict ~17K.
- v8.0.0 (2025-12-29): **MAJOR: Research-First MCP Validation** - Added MANDATORY Step 0 (Research Phase) that runs BEFORE any code analysis; added Tier 0 to progressive loading (always first); MCP validation is now exhaustive and required, not conditional; all findings must include validation status; added Technology Research Summary and MCP Validation Summary to report format; perplexity ALWAYS required for Microsoft tech (dual-validation); token budgets increased ~2,000 tokens for accuracy trade-off
- v7.0.0 (2025-12-29): Added generated content detection (Step 1b); detects files created by scripts/tools via content-based markers; redirects review to generator scripts (source of truth); reduces review noise in large changesets; added Tier 5 reference for detection patterns and algorithm
- v6.0.0 (2025-12-29): Added accurate file counting workflow (Step 1); added Tier 4b Claude Code component detection with delegation to claude-ecosystem auditors; file counting ensures accurate **Files Reviewed** reporting for large changesets
- v5.0.0 (2025-12-24): Added Tier 5 MCP Validation phase for validating findings against current best practices using MCP servers (perplexity, context7, ref, microsoft-learn, firecrawl); includes technology detection, cross-validation, and citation support
- v4.0.0 (2025-11-28): Added Layer 3 (Repository Rules) with Tier 4 CLAUDE.md-specific checks; added 8 reference files for documentation, anti-duplication, paths, platforms, skills, memory, and temp files; extended progressive loading to support repository-specific validation
- v3.0.0 (2025-11-28): Added Clean Code principles (sections 1.25-1.29): Names, Functions, Comments, Conditionals, Code Smells from Robert C. Martin and Pragmatic Programmer; updated Quick Reference Card with Clean Code and Code Smells sections
- v2.1.0 (2025-11-28): Added 12 modern cross-cutting sections (1.13-1.24): Accessibility, i18n, Observability, Data Privacy, API Design, Dependency Management, Database Patterns, Configuration Management, Cloud/Infrastructure, Frontend Patterns, Mobile Patterns, AI/ML Code Patterns
- v2.0.0 (2025-11-27): Major expansion with SOLID, OWASP, concurrency, Google practices
- v1.0.0 (2025-11-27): Initial release

---
