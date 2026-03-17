---
name: pre-flight-check
description: Checks essential information and project status before starting a task.
context: fork
---

# Pre-Flight Check Skill

**Role**: Check essential info and project status before starting work to reduce omissions.

## Inputs
- Feature name/branch name (optional)
- Required doc paths: CLAUDE.md, context.md, etc.

## Checklist
- UI spec version/design assets availability
- API spec availability
- Similar feature references
- git status/branch, build status
- context.md freshness, unresolved items in pending-questions.md
- **Document Memory Policy check**:
  - context.md token usage (warn if > 6,000 tokens, ~80% of limit)
  - specification.md exists and is summarized (if large spec)
  - archives/ directory structure in place

## Output (example)
```markdown
# Pre-flight Check Results

## Required Info
OK UI spec: v3 (YYYY-MM-DD)
OK API spec: draft available
WARN similar feature reference: not found

## Project Status
OK git status: clean
OK branch: feature/{feature-name}
OK build status: success

## Docs
OK CLAUDE.md: latest
WARN context.md: missing (needs creation)

## Document Memory Policy
OK context.md tokens: ~3,200 (under 8,000 limit)
OK specification.md: summarized (full in archives/)
OK archives/ directory: exists

## Recommended Actions
1. [HIGH] Create context.md (ContextBuilder Agent)
2. [MEDIUM] Verify design assets (invoke design-spec-extractor)
```

---

## Anti-Pattern Check

> Detect common mistakes based on "How to write a good spec for AI agents" guide

### Checklist

| Anti-Pattern | Detection Method | Status |
|--------------|-----------------|--------|
| **Vague prompts** | "Make something cool", "Make it work better" | ⚠️ |
| **Large context without summary** | specification.md > 3,000 tokens + no summary | ⚠️ |
| **Missing 6 core areas** | PROJECT.md lacks commands/tests/structure/style/Git/boundaries | ⚠️ |
| **Vibe coding ↔ Production confusion** | Attempting production deploy without tests | ⚠️ |
| **Ignoring deadly trinity** | Proceeding without verification for speed/non-determinism/cost | ⚠️ |

### Recommended Actions on Detection

| Detected Anti-Pattern | Recommended Action |
|----------------------|-------------------|
| Vague request | Invoke `requirements-analyzer` to clarify |
| Large document | Follow `document-memory-policy.md` to summarize |
| Missing areas | Recommend PROJECT.md review, reference template sections |
| No tests | Recommend writing tests before `completion-verifier` |

### Output Example

```markdown
## Anti-Pattern Check Results

| Item | Status | Action |
|------|--------|--------|
| Clear request | ✅ | - |
| Context size | ✅ | ~2,500 tokens |
| 6 core areas | ⚠️ | Git workflow undefined |
| Test defined | ✅ | - |

**Recommended Actions:**
1. [MEDIUM] Add Git Workflow section to PROJECT.md
```

## References
- `.claude/docs/guidelines/document-memory-policy.md`

