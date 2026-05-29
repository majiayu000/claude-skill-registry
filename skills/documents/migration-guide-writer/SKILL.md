---
name: migration-guide-writer
description: Creates problem-oriented migration guides following Diátaxis How-To pattern. Maps old APIs to new APIs with before/after examples, documents breaking changes, provides troubleshooting. Zero tolerance for fabricated APIs or unverified performance claims. Use when new system replaces old, breaking API changes occur, major version upgrades needed, service decomposition happens, deprecation notices required, or architectural changes documented.
version: 1.0.0
---

# Migration Guide Writer Skill

## Purpose

Create comprehensive migration guides for moving from old systems/APIs to new ones. Follows the Diátaxis How-To pattern for problem-oriented documentation. Verifies all APIs in both old and new systems before documenting, with zero tolerance for fabrication.

## Diátaxis Framework: How-To Guide

**How-To Type Characteristics:**

- **Problem-oriented** - Focused on specific migration goal
- **Assumes knowledge** - Not teaching from zero (that's tutorials)
- **Series of steps** - Path from old to new
- **Multiple approaches** - May show different migration strategies
- **Real-world scenarios** - Production migration patterns
- **Troubleshooting** - Common issues and solutions

**What NOT to Include:**

- ❌ Tutorials (learning from zero) - Use tutorial-writer skill
- ❌ Complete API reference - Link to api-doc-writer docs
- ❌ Deep explanations of WHY - Link to explanation docs
- ❌ Marketing comparisons - Technical facts only

## Critical Rules (Zero Tolerance)

### P0 - CRITICAL Violations (Must Fix)

1. **Fabricated Old APIs** - Old methods that never existed
2. **Fabricated New APIs** - New methods that don't exist in source
3. **Wrong Signatures** - Before/After code with incorrect APIs
4. **Unverified Performance Claims** - "10x faster" without benchmarks
5. **Invalid Migration Code** - Code that won't compile

### P1 - HIGH Violations (Should Fix)

6. **Missing Troubleshooting** - No guidance for common errors
7. **Incomplete Breaking Changes** - Not documenting all changes
8. **Unverified Timing Claims** - Fabricated latency numbers

### P2 - MEDIUM Violations

9. **Marketing Language** - Buzzwords instead of technical facts
10. **Missing Prerequisites** - Not stating version requirements

## Step-by-Step Workflow

### Quick 5-Phase Process

1. **Systems Analysis** - Verify old/new APIs, create mapping checklist, search for benchmarks
2. **Pattern Identification** - Identify migration patterns (CRUD, auth, config, errors, async)
3. **Documentation** - Write structured migration guide with Before/After examples
4. **Troubleshooting** - Anticipate common errors (compilation, runtime, logical)
5. **Verification** - Verify all code against source, remove unverified claims

**For detailed step-by-step instructions with examples, templates, and verification checklists, see `references/WORKFLOW-STEPS.md`.**

## Integration with Other Skills

### Works With:

- **api-doc-writer** - Link to new system API reference
- **tutorial-writer** - Link to getting started with new system
- **api-documentation-verify** - Verify migration guide accuracy

### Invokes:

- None (standalone skill)

### Invoked By:

- User (manual invocation)
- After major version releases
- When deprecating old systems

## Output Format

**Primary Output**: Markdown file with structured migration guide

**File Location**:

- `docs/migrations/[old]-to-[new].md`
- `MIGRATION.md` in project root
- `docs/how-to/migrate-from-[old].md`

## Common Pitfalls to Avoid

### 1. Unverified Performance Claims

```markdown
❌ BAD - No benchmark evidence
The new system is 10x faster than the old system

✅ GOOD - Factual architectural statement
The new system eliminates network overhead by using in-process calls
[If benchmarks exist]: See benchmarks/comparison.bench.ts for measurements
```

### 2. Fabricated New APIs

```markdown
❌ BAD - API doesn't exist
// After (New System)
await newSystem.easyMigrate(oldConfig) // This method was never implemented!

✅ GOOD - Real API from source
// After (New System)
const adapter = new ConfigAdapter(oldConfig)
await newSystem.initialize(adapter.transform())
```

### 3. Incomplete Breaking Changes

```markdown
❌ BAD - Missing changes
Major changes: Method renamed

✅ GOOD - Complete list
Breaking Changes:

1. CreateTask() renamed to Create()
2. Create() now requires ctx parameter
3. TaskParams.Owner changed from string to UserId type
4. UpdateTask() removed - use Patch() instead
5. Error type changed from string to TaskError
```

### 4. Missing Troubleshooting

```markdown
❌ BAD - No troubleshooting section
[Guide ends after migration patterns]

✅ GOOD - Comprehensive troubleshooting

## Troubleshooting

[Multiple common issues with solutions]
```

## Time Estimates

**Small Migration** (< 5 API changes): 45 minutes - 1.5 hours
**Medium Migration** (5-15 API changes): 1.5 - 3 hours
**Large Migration** (15+ changes): 3 - 6 hours
**System Replacement**: 4 - 8 hours

## Example Usage

```bash
# Manual invocation
/skill migration-guide-writer

# User request
User: "How do I migrate from the old TaskService to the new one?"
Assistant: "I'll use migration-guide-writer to create a comprehensive migration guide"
```

## Success Criteria

Migration guide is complete when:

- ✅ All new system APIs verified against source
- ✅ Before/After examples for all common patterns
- ✅ All breaking changes documented
- ✅ Troubleshooting section included
- ✅ No unverified performance claims
- ✅ No fabricated APIs
- ✅ Migration checklist provided
- ✅ Prerequisites clearly stated
- ✅ Configuration migration documented
- ✅ No marketing language

## References

- Diátaxis Framework: https://diataxis.fr/how-to-guides/
- Technical Documentation Expert Agent
- API Documentation Writer skill (for referencing APIs)

---

## Related Agent

For comprehensive documentation guidance that coordinates this and other documentation skills, use the **`documentation-coordinator`** agent.
