---
name: ground
description: Verify external libraries, APIs, and frameworks against current documentation. Use when implementing external dependencies, when unsure if a pattern is current, when the user mentions "ground", "verify docs", "exa", or "current API".
---

# Ground — External Documentation

Verify external dependencies against current documentation before implementation. Direct execution.

> **Design rationale:** This skill executes directly rather than spawning subagents because grounding is a simple query + verification sequence (~300 tokens), not substantial analytical work. Per Lita research: "Simple agents achieve 97% of complex system performance with 15x less code."

## When This Applies

| Signal | Action |
|--------|--------|
| About to write `import` for external lib | Ground first |
| Using API/SDK methods | Verify current syntax |
| Framework-specific patterns | Check version compatibility |
| Auth/security code | Always verify current best practices |
| User says "ground" or "verify" | Run full grounding check |
| New library or major version | Deep grounding |

**Default: When uncertain about external APIs, ground.**

---

## Tool Reference

### Exa MCP Tools
| Tool | Purpose |
|------|---------|
| `web_search_exa(query)` | General documentation search |
| `get_code_context_exa(query)` | Code examples from GitHub/tutorials |
| `crawling(url)` | Extract content from specific URLs |

---

## Decision Tree

```
Where does truth live?

EXTERNAL DOCS ──► /ground (this skill)
                 "What's the current API for X?"

CODEBASE ───────► /explore (warp-grep)
                 "How does X work in our code?"

HISTORY ────────► /recall (cm + cass)
                 "How did we do this before?"

TASKS ──────────► bv --robot-*
                 "What should I work on?"
```

---

## Execution Flow

Execute these steps directly. No subagents needed.

### Step 1: Identify What Needs Grounding

Categories that need verification:

| Category | Why | Risk |
|----------|-----|------|
| **Imports/Initialization** | Syntax changes between versions | High |
| **API Methods** | Methods get renamed/deprecated | High |
| **Configuration** | Options/flags evolve | Medium |
| **Async Patterns** | Async APIs vary significantly | Medium |
| **Auth/Security** | Security best practices change | Critical |
| **Data Validation** | Validators/schemas evolve | Medium |

---

### Step 2: Construct Query

**Formula:**
```
{library_name} {specific_feature} {version_if_known} 2024 2025
```

**Examples:**
```
FastAPI Pydantic v2 model_validator 2024 2025
Next.js 14 app router server components
React useOptimistic hook 2024
Prisma findMany where clause 2024
```

**Strengthening queries:**
- Add version number if known
- Add year for recency (2024, 2025)
- Add "official" or "docs" for authoritative sources
- Add "migration" if moving between versions

---

### Step 3: Execute Search

**For documentation:**
```python
web_search_exa("{library} {feature} {version} 2024 2025")
```

**For code examples:**
```python
get_code_context_exa("{library} {pattern} implementation example")
```

**For specific page:**
```python
crawling("{url}")
```

---

### Step 4: Verify Results

| Criterion | Pass If |
|-----------|---------|
| **Source** | Official docs or reputable repo |
| **Freshness** | Updated within 12 months |
| **Version** | Matches your dependency |
| **Completeness** | Full import + usage pattern |
| **Status** | Not deprecated |

---

### Step 5: Record Grounding Status

Track in your work:

```markdown
## Grounding Status
| Pattern | Query | Source | Status |
|---------|-------|--------|--------|
| `@model_validator` | "Pydantic v2 2024" | docs.pydantic.dev | ✅ Verified |
| `useOptimistic` | "React 19 2024" | react.dev | ✅ Verified |
```

**Status values:**
- ✅ Verified — Matches current docs
- ⚠️ Changed — API changed, updated approach
- ❌ Deprecated — Found alternative
- ❓ Unverified — Couldn't confirm, flagged

---

## Query Patterns

### Current API Documentation
```
"{library} {method} documentation 2024"
"{library} {feature} API reference"
"{library} official docs {feature}"
```

### Migration Between Versions
```
"{library} v{old} to v{new} migration"
"{library} {version} breaking changes"
"{library} upgrade guide {version}"
```

### Code Examples
```python
get_code_context_exa("{library} {pattern} implementation example")
get_code_context_exa("{library} {use_case} tutorial")
```

### Security/Auth Patterns
```
"{auth_method} best practices 2024"
"{library} authentication {pattern} security"
"OAuth PKCE {language} 2024"
```

### Error Resolution
```
"{library} {error_message} fix"
"{library} {error_type} troubleshooting"
```

---

## Grounding Depth Levels

| Depth | When | What to Check |
|-------|------|---------------|
| **Quick** | Familiar pattern, just confirming | One query, verify method exists |
| **Standard** | Normal implementation | Query + check for deprecation warnings |
| **Deep** | Security/auth, new library, major version | Multiple queries, read changelog, check issues |

---

## Version Sensitivity Signals

Ground more carefully when you see:

| Signal | Risk |
|--------|------|
| Major version in deps (v1 → v2) | Breaking changes likely |
| Library < 2 years old | API still evolving |
| "experimental" or "beta" in docs | May change without notice |
| Security-related code | Best practices evolve |
| AI training data gap | Libs released after training cutoff |

---

## Failure Handling

| Issue | Response |
|-------|----------|
| No results | Broaden query, try alternate terms |
| Conflicting info | Official docs > GitHub > tutorials |
| Only outdated info | Mark ❓, proceed with caution, add TODO |
| Can't verify | Flag for human review |

---

## Query Anti-Patterns

| Bad Query | Problem | Better Query |
|-----------|---------|--------------|
| `"how to use {library}"` | Too vague | `"{library} {specific_feature} 2024"` |
| `"{library} tutorial"` | May be outdated | `"{library} {feature} official docs"` |
| `"best {library}"` | Opinion, not docs | `"{library} {pattern} documentation"` |
| `"{library}"` alone | No specificity | Add feature + version + year |

---

## Query Strengthening

If initial query returns poor results:

1. **Add version**: `"React 19 useOptimistic"` vs `"React useOptimistic"`
2. **Add year**: `"FastAPI middleware 2024"` vs `"FastAPI middleware"`
3. **Add "official"**: `"Next.js official docs app router"`
4. **Be more specific**: `"Prisma findMany where clause"` vs `"Prisma queries"`
5. **Try alternate terms**: `"authentication"` vs `"auth"` vs `"login"`

---

## Progressive Grounding

For large implementations:

1. **Start**: Ground the core imports/setup
2. **As you go**: Ground each new external method before using
3. **Before commit**: Review grounding table, verify nothing ❓

Don't try to ground everything upfront — ground just-in-time as you encounter external deps.

---

## Integration with Workflow

### Before implementing (via /advance)
```python
# Check external dependencies
web_search_exa("{library} {feature} 2024")
```

### During implementation
```python
# Just-in-time verification
get_code_context_exa("{specific_method} example")
```

### Before commit
Review grounding table, ensure all ❓ are resolved or documented.

---

## Requirements

Requires Exa API key configured:

```bash
claude mcp add exa -s user \
  -e EXA_API_KEY=your-key \
  -- npx -y @anthropic-labs/exa-mcp-server
```

---

## Quick Reference

```python
# Documentation search
web_search_exa("{library} {feature} {version} 2024 2025")

# Code examples
get_code_context_exa("{library} {pattern} implementation example")

# Specific page
crawling("{url}")
```

**Query formula:**
```
{library} {feature} {version} 2024 2025
```

---

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Skip grounding for external APIs | Training data may be stale | Ground before using |
| Use tutorials over docs | Tutorials get outdated | Prefer official docs |
| Ignore version mismatches | Breaking changes exist | Verify version compatibility |
| Ground everything upfront | Wastes time | Ground just-in-time |
| Skip grounding for "familiar" libs | APIs change | Quick verify is still worth it |

---

## See Also

- `/recall` — Past session patterns
- `/explore` — Codebase search
- `/advance` — Bead workflow (includes grounding step)
