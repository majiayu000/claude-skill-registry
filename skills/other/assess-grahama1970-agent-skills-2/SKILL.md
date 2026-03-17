---
name: assess
description: >
  Step back and critically reassess project state. Use when asked to "assess",
  "step back", "fresh eyes", "check alignment", "sanity check", "health check",
  "prune documentation", or "evaluate what's working". Offers documentation pruning
  and doc-code alignment analysis. Offer to run after major changes (don't auto-run).
allowed-tools: Bash, Read, Glob, Grep
triggers:
  - assess the project
  - assess this
  - assess this directory
  - assess this folder
  - reassess this
  - reassess the project
  - re-evaluate the project
  - step back and analyze
  - step back
  - take a step back
  - fresh eyes
  - big picture check
  - check alignment
  - does the code match the docs
  - what's working and what isn't
  - evaluate code quality
  - reality check
  - sanity check
  - health check
  - project health check
  - quick audit
  - project audit
  - gap analysis
  - status check
  - project status
  - take stock
  # Documentation-specific triggers
  - prune documentation
  - doc pruning
  - documentation cleanup
  - fix documentation alignment
  - update docs to match code
  - deprecate outdated documentation
  - documentation audit
  - doc-code alignment check
  - documentation review
  - clean up docs
metadata:
  short-description: Step back and critically reassess project state and documentation alignment
---

# Assess Skill

Step back and critically reassess the project state. This skill provides both **interactive guidance** (human-in-the-loop) and **programmatic analysis** (automated pipelines). **Specialized for documentation pruning and doc-code alignment analysis.**

## CLI Usage (Programmatic)

For automated pipelines (like Nightly Dogpile), use the `assess.py` script to generate structured JSON reports.

```bash
# Run assessment and output JSON
.pi/skills/assess/assess.py run . --output assessment.json

# Categories:
# - aspirational: TODOs, stubs
# - brittle: FIXMEs, hardcoded secrets
# - over_engineered: (Future) textual analysis
# - working_well: (Future) test coverage stats
```

## Interactive Usage (Human-in-the-Loop)

Step back and critically reassess the project state. This skill guides the agent through systematic, **collaborative** evaluation.

## Key Principle: Collaborative Assessment

Assessment is a dialogue, not a report. Ask clarifying questions to:

- Understand what the user considers most important
- Clarify intent when documentation is ambiguous
- Prioritize findings based on user's goals
- Confirm assumptions before making recommendations

## Assessment Flow

### Step 1: Scope the Assessment

**If scope is clear** (e.g., "assess the auth module"), skip questions and proceed.

**If scope is open** (e.g., "step back and assess this"), ask:

- "What areas are you most concerned about?"
- "Should I focus on code quality, doc accuracy, or both?"
- "Any known issues I should acknowledge but not re-report?"

**If documentation pruning** (e.g., "prune documentation"), ask:

- "Should I focus on deprecated features, missing docs, or alignment issues?"
- "Do you want me to identify unreferenced documentation files?"
- "Should I check for TODO/FIXME markers in documentation?"
- "Would you like me to validate cross-references between docs?"

### Step 2: Find Project Root & Detect Ecosystem

Locate the project root and detect the ecosystem before reading metadata.

**Detect ecosystem first** by looking for these marker files:

| File                                             | Ecosystem          |
| ------------------------------------------------ | ------------------ |
| `pyproject.toml`, `setup.py`, `requirements.txt` | Python             |
| `package.json`, `package-lock.json`, `yarn.lock` | Node.js/JavaScript |
| `Cargo.toml`                                     | Rust               |
| `go.mod`                                         | Go                 |
| `pom.xml`, `build.gradle`                        | Java               |
| `Gemfile`                                        | Ruby               |
| `composer.json`                                  | PHP                |

**Then read ecosystem-specific metadata:**

- Python: `pyproject.toml` for dependencies, scripts, project info
- Node: `package.json` for scripts, dependencies
- Rust: `Cargo.toml` for crate info
- etc.

**Universal project docs (all ecosystems):**

```
README.md         # Project overview (check project root)
CONTEXT.md        # Agent-focused current status
AGENTS.md         # Agent skill discovery
docs/             # Documentation directory
```

**Fallback discovery** if no obvious metadata:

- Scan for `*.md` files in root
- Look for `src/` or `lib/` structure
- Check for test directories (`tests/`, `test/`, `spec/`)
- Find entry points by extension (`.py`, `.js`, `.rs`, `.go`)

### Step 3: Quick Scan & Initial Findings

Do a fast pass:

1. Read project metadata (pyproject.toml, package.json, etc.)
2. Read README.md for stated goals and features
3. Glob for structure understanding
4. Note 2-3 initial observations

Then check in (unless scope was already clear):

- "I see X, Y, Z - should I dig deeper on any of these?"
- "The docs claim [feature] - is this a priority to verify?"

### Step 4: Deep Dive

Based on user guidance, investigate thoroughly. For each finding, consider:

- Is this blocking or just technical debt?
- Does the user already know about this?
- What's the fix complexity?

### Step 5: Collaborative Report

Present findings and ask:

- "Which of these would you like me to fix now?"
- "Should I update the docs to reflect reality?"
- "Are any of these 'known issues' I should deprioritize?"
- "Should I deprecate outdated documentation or update it to match current code?"

## Assessment Categories

### 1. Doc-Code Alignment (Documentation Pruning)

Comprehensive analysis of documentation accuracy and alignment with codebase:

#### Documentation Coverage Analysis
- **README claims** - Do advertised features actually exist?
- **CONTEXT.md** - Does "current status" reflect reality?
- **CHANGELOG entries** - Are unreleased changes documented?
- **Package documentation** - Are all packages documented consistently?
- **Skill documentation** - Do SKILL.md files match actual implementations?

#### Cross-Reference Validation
- **Internal links** - Do documentation cross-references resolve correctly?
- **Example references** - Do code examples in docs point to existing files?
- **API documentation** - Do documented endpoints/methods exist?
- **Configuration references** - Are config options documented accurately?

#### Content Quality Assessment
- **TODO/FIXME markers** - Identify incomplete documentation sections
- **Stale information** - Find outdated setup instructions, deprecated features
- **Contradictory claims** - Spot conflicting information across documents
- **Missing context** - Identify docs that assume unstated prerequisites

#### Specific Documentation Pruning Actions
- **Deprecate outdated docs** - Mark or remove documentation for removed features
- **Update alignment** - Sync documentation with current implementation
- **Remove unreferenced files** - Identify docs not linked from anywhere
- **Consolidate duplicates** - Merge overlapping documentation

**Ask:** "I found X documented but not implemented - should I implement it, update docs, or deprecate the claim?"
**Ask:** "This documentation references non-existent files - should I create them or remove the references?"
**Ask:** "Multiple docs describe the same feature differently - which should be the source of truth?"

### 2. Aspirational vs Implemented

Find gaps between intent and reality:

- Stub implementations (`pass`, `raise NotImplementedError`)
- TODO/FIXME blocking core functionality
- Features in code structure but no actual logic
- Dependencies declared but not used

**Ask:** "Is [aspirational feature] still on the roadmap, or should I remove it?"

### 3. Brittle Code

Find fragile patterns:

- Hardcoded values (URLs, paths, magic numbers)
- Missing error handling in I/O paths
- Regex/parsing that breaks on edge cases
- Version pins that may be stale

**Ask:** "I see hardcoded [value] - is this intentional for now or should I externalize it?"

### 4. Non-Working Code

Find features that exist but fail:

- Dead code paths (unreachable branches)
- Silent exception swallowing (`except: pass`)
- Integration points returning wrong data
- Import errors or missing dependencies

**Ask:** "This [feature] appears broken - is it actively used or can we remove it?"

### 5. Over-Engineered Code

Find unnecessary complexity:

- Abstractions with single implementation
- Config for hypothetical flexibility

**Ask:** "Is [abstraction] expected to grow, or can we simplify?"

### 6. Test Coverage (Non-Negotiable)

Assess whether features have corresponding tests:

**Check for each feature/module:**

- Does a test file exist? (`test_<feature>.py`, `<feature>.test.ts`)
- Do tests actually test the feature? (not just exist)
- Do tests run successfully? (exit code 0, not skipped)
- Are edge cases covered?

**Test Coverage Table:**
| Feature | Test File | Tests Run? | Pass? | Coverage |
|---------|-----------|------------|-------|----------|
| Auth login | test_auth.py | Yes | ✓ | 3 cases |
| Image extract | MISSING | - | - | NEEDS TEST |

**For missing tests, ask:**

- "Feature X has no tests. Should I create a test for it now?"
- "What behavior should the test verify?"

**For skipped tests, investigate:**

- Why is it skipped? Infrastructure issue or bug?
- "Test Y is being skipped. Should we fix the infrastructure or the test?"

**Red flags:**

- `pytest.mark.skip` without clear reason
- Exit code 3 (skip) on critical paths
- "0 tests collected" for a module
- Tests that pass but don't assert anything meaningful

### 6a. Task File Definition of Done Audit

When assessing a project with task files (0N_TASKS.md), verify each task has proper test definitions:

**Check each task for:**

- Does it have a `Definition of Done` field?
- Does the Definition specify a test file/function?
- Does the specified test actually exist?
- Is the assertion clear and verifiable?

**Task Definition of Done Audit:**
| Task | Definition of Done | Test Exists? | Assertion Clear? |
|------|-------------------|--------------|------------------|
| Task 1: Add VLM fallback | `test_image.py::test_vlm_fallback` | ✓ | ✓ |
| Task 2: Fix auth bug | MISSING | - | - |
| Task 3: Research APIs | N/A (explore) | - | - |

**For tasks missing Definition of Done:**

- "Task X has no Definition of Done. What test should prove it's complete?"
- "How will we know Task X is working correctly?"

**Block execution if:**

- Implementation tasks lack Definition of Done
- Specified tests don't exist
- Assertions are vague ("it should work")

### 7. Working Well

Acknowledge solid code - helps calibrate the assessment.

## Example Dialogue

**User:** "Step back and assess this project"

**Agent:** "I'll assess the project. A few quick questions first:

1. Are there specific areas you're concerned about?
2. Should I focus on code quality, doc accuracy, or both?
3. Any known issues I should acknowledge but not re-report?"

**User:** "Focus on whether the skills actually work as documented"

**Agent:** "I'll check the documented skills. Should I run any tests or commands to verify they work, or just review the code?"

**User:** "Yes, run the sanity tests"

**Agent:** _reads pyproject.toml, README.md, runs sanity tests_

"I've checked the documented skills. Here's what I found:

**Working as documented:**

- memory skill - recall/learn commands work
- scillm skill - batch completions working

**Drift found:**

- arxiv skill claims 'citation export' - I don't see this implemented
- youtube-transcripts example in SKILL.md uses old API format

Should I:

1. Fix the arxiv implementation to add citation export?
2. Update the docs to remove the claim?
3. Fix the youtube-transcripts example?

Which would you prefer I tackle first?"

---

**User:** "Prune the documentation"

**Agent:** "I'll analyze the documentation for alignment issues and cleanup opportunities. A few questions:

1. Should I focus on deprecated features, missing docs, or alignment issues?
2. Do you want me to identify unreferenced documentation files?
3. Should I check for TODO/FIXME markers in documentation?
4. Would you like me to validate cross-references between docs?"

**User:** "Check everything and focus on alignment issues"

**Agent:** _performs documentation inventory, alignment analysis, and cross-reference validation_

"I've completed the documentation analysis. Here's what I found:

**Documentation Coverage:**
- Total documentation files: 47
- Cross-reference issues: 12 broken links
- Unreferenced files: 3 (consider removal)
- TODO/FIXME markers: 8 in documentation

**Alignment Issues Found:**

| File | Issue | Action Needed |
|------|-------|---------------|
| `README.md` | Claims 'advanced filtering' feature | Feature not implemented - remove claim? |
| `docs/api.md` | Documents deleted `/v1/status` endpoint | Update documentation |
| `packages/ai/README.md` | References old provider name | Update to current name |
| `SKILL.md` files | 5 incomplete sections with TODO | Complete or remove sections |

**Recommendations:**
1. **High Priority:** Fix alignment issues in main README and API docs
2. **Medium Priority:** Complete TODO sections in SKILL.md files
3. **Low Priority:** Remove unreferenced documentation files

Should I start by updating the main README to remove the unimplemented feature claim, or would you prefer a different approach?"

## Documentation Pruning Workflow

When specifically asked to prune documentation or check doc-code alignment:

### Step 1: Documentation Inventory
1. **Find all documentation files** (`*.md`, `docs/`, `README*`, `CHANGELOG*`)
2. **Check cross-references** - validate internal links and file references
3. **Identify unreferenced docs** - files not linked from anywhere
4. **Scan for TODO/FIXME markers** in documentation content

### Step 2: Alignment Analysis
1. **README claims vs implementation** - verify advertised features exist
2. **API documentation accuracy** - check endpoints/methods match code
3. **Configuration documentation** - validate all documented settings work
4. **Example validation** - ensure code samples are current and functional

### Step 3: Deprecation Assessment
1. **Feature lifecycle analysis** - identify removed features still documented
2. **Version alignment** - check CHANGELOG vs current implementation
3. **Stale references** - find docs referencing deleted files or features
4. **Outdated setup instructions** - identify obsolete installation/config steps

### Step 4: Pruning Recommendations
Present findings with specific actions:
- **Update** - Documentation needs content refresh
- **Deprecate** - Remove documentation for deleted features
- **Consolidate** - Merge duplicate or overlapping documentation
- **Create** - Missing documentation for existing features

## Output Format (When Presenting Findings)

```markdown
# Assessment: <project-name>

## Summary

<2-3 sentences: overall health, key findings>

## Scope

- **Covered:** [what was assessed]
- **Not covered:** [what was skipped or out of scope]

## Questions for You

- [Clarifying question about intent/priority]
- [Question about known issues]

## Findings

### Doc-Code Alignment

| Claim           | Reality         | Action?                   |
| --------------- | --------------- | ------------------------- |
| "Redis caching" | Not implemented | Remove claim / Implement? |

### Documentation Quality Issues

| File | Issue | Severity | Recommended Action |
|------|-------|----------|-------------------|
| `README.md` | Claims non-existent feature | High | Remove claim or implement |
| `docs/api.md` | References deleted endpoint | Medium | Update documentation |
| `SKILL.md` | TODO markers incomplete | Low | Complete or remove sections |

### Documentation Coverage

| Type | Count | Issues Found |
|------|-------|--------------|
| Total docs | 24 | 8 alignment issues |
| Unreferenced | 3 | Consider removal |
| With TODO/FIXME | 5 | Complete or clean up |

### Issues Found

1. **file.py:123** - [Issue description]
   - Severity: High/Medium/Low
   - Suggested fix: [brief]

### Working Well

- [Solid code to acknowledge]

## Test Coverage Gap

| Feature   | Test Status | Action Needed      |
| --------- | ----------- | ------------------ |
| [feature] | Missing     | Create test        |
| [feature] | Skipped     | Fix infrastructure |
| [feature] | Passing     | ✓                  |

## Recommended Next Steps

1. [Documentation alignment fixes - PRIORITY for doc pruning]
2. [Test creation for untested features]
3. [Immediate code fix]
4. [Documentation consolidation/deprecation]

Which should I start with? Note: For documentation pruning, alignment issues should typically be addressed first to prevent user confusion.
```

## When to Use

**On Request:**

- "Step back and assess this"
- "Sanity check the project"
- "Fresh eyes review"
- "Quick audit"
- "Health check"
- "Gap analysis"
- "Assess this directory/folder"
- "Big picture check"
- "Project status"
- "/assess"
- "Prune documentation"
- "Doc pruning"
- "Documentation cleanup"
- "Fix documentation alignment"
- "Update docs to match code"
- "Deprecate outdated documentation"
- "Documentation audit"
- "Doc-code alignment check"
- "Documentation review"
- "Clean up docs"

**Proactively (always ask first, never auto-run):**

- "I've made significant changes - want me to do a quick assessment?"
- "Before I update the docs, should I verify the current state?"
- "The documentation seems outdated - should I check for alignment issues?"

## File Writing Policy: Read-Only by Default

**Core principle: Assessment is read-only. Never write files without explicit user consent.**

This prevents:

- Unexpected file changes
- Dirty git status
- Permission issues
- "Agent edited my repo" distrust

### The Print-First Pattern

When suggesting documentation, **show the content first, then offer to write**:

```
Agent: "I notice there's no README.md. Here's what I'd suggest:

---
# ProjectName

One-liner description based on pyproject.toml...

## Install
pip install ...

## Quick Start
...
---

Should I write this to README.md, or would you like to modify it first?"
```

This gives the user full control:

1. See exactly what will be written
2. Request changes before committing
3. Copy/paste themselves if preferred
4. Decline without friction

### Common Missing Docs

- `README.md` - Project overview, quick start
- `CONTEXT.md` - Current status for agents
- `CONTRIBUTING.md` - How to contribute
- `CHANGELOG.md` - Version history
- Inline docstrings for public APIs
- `--help` text for CLIs

### For Incomplete Docs

```
Agent: "The README mentions 'API endpoints' but doesn't list them.
Options:
1. I'll show you the endpoint docs to add (you approve before write)
2. Remove the mention until it's ready
3. Mark it as 'coming soon'

Which approach?"
```

**Key principle:** Print first, write only with explicit consent.

## External Research (When Needed)

Sometimes assessment requires external context. Ask before using paid services.

**Available research skills:**
| Skill | Use For | Cost |
|-------|---------|------|
| `/context7` | Library/framework documentation | Free |
| `/brave-search` | General web search, deprecation notices | Free |
| `/perplexity` | Deep research, complex questions | Paid |

**When to suggest research:**

- Verifying if a dependency is deprecated or has security issues
- Checking correct API usage for unfamiliar libraries
- Researching best practices for patterns you're unsure about
- Finding changelogs for version upgrades

**How to offer:**

```
Agent: "I see you're using library X v2.3. I'm not certain if this version
has known issues. Want me to check with /context7 or /brave-search?"
```

```
Agent: "The authentication pattern here looks unusual. Should I research
current best practices with /perplexity? (Note: this uses paid API)"
```

**Key principle:** Don't silently research - ask first, especially for paid services. Quick doc lookups with /context7 are usually fine.

## Escalation to Code Review

When assessment reveals significant issues, suggest `/review-code`:

**When to suggest review-code:**

- Complex refactoring needed across multiple files
- Architecture concerns that need deeper analysis
- Security-sensitive code paths
- Performance-critical sections
- When a second opinion from another AI provider would help

**How to suggest:**
"I've found [issues] that might benefit from a deeper code review. Want me to run `/review-code` with [provider] to get a structured analysis and patch suggestions?"

**Example:**

```
Agent: "The authentication module has several issues:
- Hardcoded secrets in 3 places
- Missing input validation
- No rate limiting

This is security-sensitive - would you like me to run `/review-code`
with OpenAI (high reasoning) to get a thorough security review and
suggested fixes?"
```

## Command Preferences

When running shell commands, prefer modern fast tools:

| Task           | Prefer         | Over   | Why                                              |
| -------------- | -------------- | ------ | ------------------------------------------------ |
| Search content | `rg` (ripgrep) | `grep` | 10x faster, better defaults, respects .gitignore |
| Find files     | `fd`           | `find` | Faster, simpler syntax, respects .gitignore      |
| List files     | `eza` or `ls`  | -      | eza has better output if available               |

Example patterns:

```bash
# Search for TODOs
rg "TODO|FIXME|HACK|XXX" --type py

# Find Python files modified recently
fd -e py --changed-within 7d

# Search for stub implementations
rg "raise NotImplementedError|pass$" --type py
```

## Tips

- **Collaborate** - Assessment is dialogue, not monologue
- **Ask before running** - Get permission before running tests, builds, or expensive commands
- **Skip questions if scope is clear** - Don't ask "what areas?" if user said "assess the auth module"
- **Prioritize** - Not every finding needs immediate action
- **Be specific** - File paths and line numbers
- **Be actionable** - Each finding should suggest next steps
- **Update as you go** - If you find drift, offer to fix it immediately
- **Escalate wisely** - Suggest review-code for complex/critical issues
- **State your scope** - Always clarify what was and wasn't assessed
- **Use fast tools** - Prefer rg/fd over grep/find for speed
- **Test coverage is non-negotiable** - Every implementation must have a test. Flag missing tests as blockers.
- **Skipped tests are red flags** - Investigate WHY tests skip. Infrastructure issues must be fixed, not ignored.
