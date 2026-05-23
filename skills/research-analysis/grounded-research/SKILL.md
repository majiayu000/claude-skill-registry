---
name: grounded-research
description: Epistemic honesty protocol for code research. Forces uncertainty admission, cascading verification through authoritative sources (deepwiki, submodules, web), and approach validation before implementation.
model_invoked: true
triggers:
  - "research"
  - "how does"
  - "what is the correct"
  - "best practice"
  - "current pattern"
  - "am I doing this right"
  - "verify approach"
  - "uncertain"
  - "not sure if"
  - "check documentation"
---

# Grounded Research Protocol

**Purpose**: Enforce epistemic honesty in code research. Admit uncertainty, cascade through authoritative sources, verify approaches BEFORE implementing.

## Core Doctrine: Uncertainty Admission

> **You do not know what you have not verified.**

### Knowledge Cutoff Awareness

| Fact | Implication |
|------|-------------|
| Today's date | 2026-01-16 |
| Knowledge cutoff | May 2025 |
| Gap | ~8 months |

**For any library/API/pattern that could have changed since May 2025, you MUST:**
1. Admit uncertainty explicitly
2. Research via authoritative sources
3. Verify before claiming knowledge

### Uncertainty Markers

Use these markers in your thinking and responses:

| Marker | Meaning | Action |
|--------|---------|--------|
| `[UNCERTAIN]` | I'm not confident about this | Research required |
| `[CUTOFF-GAP]` | This may have changed since May 2025 | Verify via sources |
| `[VERIFIED]` | Confirmed via authoritative source | Safe to assert |
| `[INFERRED]` | Based on patterns, not verification | State explicitly |

### Example Uncertainty Admission

```
[UNCERTAIN] I believe Effect.Service<>() uses double-parenthesis syntax,
but my knowledge is from May 2025. Let me verify this hasn't changed.

[CUTOFF-GAP] The Effect-TS Schema API may have evolved. Checking deepwiki
for current patterns...
```

---

## Research Cascade Protocol

When researching any code pattern, follow this cascade **in order**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESEARCH CASCADE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. DEEPWIKI (Authoritative Documentation)                       │
│     ├─ Ask: "Is my understanding of X correct?"                  │
│     ├─ Ask: "What is the current API for X?"                     │
│     └─ Repo: "Effect-TS/effect", "tim-smart/effect-atom"         │
│                                                                  │
│  2. SUBMODULES (Local Canonical Sources)                         │
│     ├─ ../../submodules/website/  (Human-authored docs)          │
│     ├─ ../../submodules/effect/   (Source + test patterns)       │
│     └─ ../../submodules/effect-atom/ (Atom patterns)             │
│                                                                  │
│  3. WEB SEARCH (Recent Changes, Breaking Changes)                │
│     ├─ Use for: "Effect-TS 3.0 breaking changes 2025"            │
│     └─ Use for: Verifying very recent updates                    │
│                                                                  │
│  4. CODEBASE (Local Precedent)                                   │
│     ├─ grep/glob for existing patterns                           │
│     └─ .edin/*.md pattern registries                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### When to Use Each Level

| Source | When to Use | Trust Level |
|--------|-------------|-------------|
| **deepwiki** | First stop for API questions | High (repo-aware) |
| **submodules** | Cross-reference, test patterns | Highest (canonical) |
| **WebSearch** | Recent changes, version updates | Medium (verify) |
| **Codebase** | Local conventions, precedent | High (contextual) |

---

## Verification Query Patterns

### DON'T: Ask for "the answer"

```
❌ "How do I define an Effect service?"
```

### DO: Ask WHETHER your understanding is correct

```
✅ "I believe Effect.Service<>() uses double-parenthesis syntax
   Effect.Service<MyService>()('app/MyService', { ... }).
   Is this correct, or has the API changed?"
```

### Verification Query Templates

**Pattern Verification**:
```
I believe [PATTERN] is the correct approach for [USE CASE].
Specifically: [CODE SNIPPET].
Is this accurate for the current version of [LIBRARY]?
```

**API Verification**:
```
My understanding is that [API_NAME] accepts [PARAMETERS] and returns [RETURN_TYPE].
Has this changed in recent versions?
```

**Deprecation Check**:
```
Is [OLD_PATTERN] still recommended, or has it been superseded?
What is the current best practice?
```

---

## MCP Tool Usage

### deepwiki Tools

**List available topics**:
```
mcp__deepwiki__read_wiki_structure
  repoName: "Effect-TS/effect"
```

**Ask verification question**:
```
mcp__deepwiki__ask_question
  repoName: "Effect-TS/effect"
  question: "Is Effect.Service<>() with double-parenthesis still the recommended
             pattern for service definition? I want to verify my approach."
```

**Read comprehensive docs**:
```
mcp__deepwiki__read_wiki_contents
  repoName: "Effect-TS/effect"
```

### Canonical Repos for deepwiki

| Library | Repo Name | Use For |
|---------|-----------|---------|
| Effect-TS | `Effect-TS/effect` | Core Effect patterns, Schema, Streams |
| effect-atom | `tim-smart/effect-atom` | Atom patterns, Registry, React integration |
| AG-Grid | `ag-grid/ag-grid` | Grid patterns, cell renderers |
| XState | `statelyai/xstate` | State machine patterns |

---

## Submodule Research

### Navigation Commands

```bash
# Effect website (human-authored docs - HIGHEST trust)
ls ../../submodules/website/content/src/content/docs/docs/

# Effect source + tests (canonical patterns)
find ../../submodules/effect/packages -name "*.test.ts" | head -20

# effect-atom tests (atom patterns)
ls ../../submodules/effect-atom/packages/atom/test/

# Search for specific pattern
grep -r "Effect.Service" ../../submodules/effect/packages/effect/src/
```

### Submodule Priority

1. **website** - Human-authored, battle-tested prose
2. **effect/packages/*/test/** - Canonical test patterns
3. **effect-atom/packages/atom/test/** - Atom-specific patterns
4. **Source code** - Implementation details (last resort)

---

## Implementation Workflow

### Before Writing Code

```
1. [ADMIT UNCERTAINTY]
   "I'm not certain about the current API for X..."

2. [RESEARCH CASCADE]
   a. Query deepwiki with verification question
   b. Cross-reference with submodule docs
   c. Check for recent breaking changes if needed

3. [STATE CONFIDENCE]
   "[VERIFIED] The current pattern is..."
   OR
   "[INFERRED] Based on patterns, I believe..."

4. [IMPLEMENT]
   Only after grounding
```

### Example Research Session

```
USER: "How do I create an Effect service with dependencies?"

CLAUDE: [CUTOFF-GAP] My knowledge of Effect-TS is from May 2025.
Let me verify the current service definition pattern.

[deepwiki query]: "Effect-TS/effect" - "Is Effect.Service<>() with
double-parenthesis and dependencies array still the recommended pattern?"

[submodule check]: Reading ../../submodules/website/.../services.mdx

[VERIFIED] The current pattern is:
```typescript
class MyService extends Effect.Service<MyService>()("app/MyService", {
  effect: Effect.gen(function* () {
    const dep = yield* OtherService;
    return { method: () => ... } as const;
  }),
  dependencies: [OtherService.Default],
}) {}
```
```

---

## Anti-Patterns

### ❌ NEVER: Claim knowledge without verification

```
"Effect.Service uses this syntax..."  // WHERE DID YOU VERIFY THIS?
```

### ❌ NEVER: Skip the cascade for "obvious" patterns

```
"I know this one, no need to check..."  // THINGS CHANGE
```

### ❌ NEVER: Use stale mental models

```
"In my experience..."  // WHAT DATE IS YOUR EXPERIENCE FROM?
```

### ❌ NEVER: Conflate inference with verification

```
"This should work..."  // SHOULD ≠ DOES
```

---

## Quick Reference

### Research Checklist

- [ ] Identified uncertainty explicitly
- [ ] Queried deepwiki with verification question
- [ ] Cross-referenced with submodules (if needed)
- [ ] Checked for breaking changes (if recent library)
- [ ] Stated confidence level in response
- [ ] Provided source for claims

### Confidence Ladder

| Level | Marker | Meaning |
|-------|--------|---------|
| 1 | `[UNCERTAIN]` | Need to research |
| 2 | `[INFERRED]` | Based on patterns, unverified |
| 3 | `[VERIFIED-DEEPWIKI]` | Confirmed via deepwiki |
| 4 | `[VERIFIED-SUBMODULE]` | Confirmed via canonical source |
| 5 | `[VERIFIED-MULTI]` | Multiple sources agree |

### Response Format

```markdown
## Research Summary

**Question**: [What I needed to verify]
**Sources Consulted**:
- [x] deepwiki: Effect-TS/effect
- [x] submodule: website/docs/services.mdx
- [ ] WebSearch: (not needed)

**Confidence**: [VERIFIED-MULTI]

**Finding**: [The verified answer]

**Implementation**: [Code with confidence]
```

---

## Integration with Other Skills

| Skill | How It Integrates |
|-------|-------------------|
| `/effect-patterns` | Use after research to implement |
| `/tmnl-submodule-exploration` | Detailed submodule navigation |
| `/effect-schema-mastery` | Schema-specific research |
| `/effect-service-authoring` | Service-specific research |

---

## Trigger Conditions

This skill should activate when:

1. **Explicit uncertainty**: "I'm not sure if...", "Is this correct?"
2. **API questions**: "What's the current way to...", "How do I..."
3. **Pattern validation**: "Am I doing this right?", "Best practice for..."
4. **Version concerns**: "Has this changed?", "Current version of..."
5. **Before implementation**: Any significant code writing involving external APIs
