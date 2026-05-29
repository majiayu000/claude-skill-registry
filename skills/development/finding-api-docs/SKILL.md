---
name: api-documentation-discovery
description: Use when APIs fail repeatedly with version-related errors (method not found, wrong arguments, unknown flag) or when about to use library APIs with uncertain knowledge - guides finding current, accurate documentation instead of guessing from training data
---

# API Documentation Discovery

## Overview

When your training data conflicts with current API versions, STOP guessing and START discovering. This skill guides you to find current, accurate documentation using language-specific tools.

**Core principle:** Training data ages. Installed versions are truth. Use discovery tools to find what's actually there.

## When to Use

### Reactive Triggers (MUST use after these):
- ✅ 2+ failed attempts with same library/API
- ✅ Error patterns: "method not found", "wrong number of arguments", "unknown flag", "undefined method"
- ✅ Version mismatch symptoms in stack traces

### Proactive Red Flags (STOP and check docs when you notice):
- ⚠️ You're confident about API usage but haven't verified current version
- ⚠️ User is confident but their syntax keeps failing
- ⚠️ You're making "one more tweak" to syntax
- ⚠️ You're using phrases like "should work", "likely correct", "probably just"
- ⚠️ You're pattern-matching from training data without verification
- ⚠️ You're about to claim something is "documented" without checking

**When NOT to use:**
- First attempt with clear error message pointing to fix
- Errors unrelated to API usage (logic bugs, type errors in your code)

## The Discovery Workflow

### Step 1: STOP Guessing
Recognize the trigger. Don't make another attempt based on patterns or user confidence.

### Step 2: Identify Context
- What library/framework is failing? (check imports, stack traces, go.mod/Gemfile)
- What version is installed? (language tools show this)
- What operation are you trying? (the actual goal, not the syntax attempt)

### Step 3: Use Language Discovery Tools
Check language-specific reference for HOW to discover documentation:
- `references/go.md` - Go module exploration
- `references/ruby.md` - Ruby gem exploration

Follow progressive discovery: **docs → examples → source**

### Step 4: Load Framework Reference (if available)
If framework-specific reference exists, load it for curated patterns:
- `references/go/cobra.md` - Cobra CLI patterns
- `references/ruby/rails.md` - Rails patterns
- `references/ruby/karafka.md` - Karafka patterns

### Step 5: Verify Before Using
- Found API signature? Verify it matches your use case
- Found example? Adapt it, don't just copy pattern from memory
- Found docs? Read them, don't skim for confirmation

## Common Anti-Patterns

| Rationalization | Reality |
|----------------|---------|
| "User is confident, syntax is probably right" | User confidence ≠ current API. Verify. |
| "Training data shows this pattern" | Training data ages. Check installed version. |
| "Let me try one more variation" | Guessing wastes time. Check docs now. |
| "This is documented somewhere" | Then go READ it before claiming confidence. |
| "Should be simple, just tweak syntax" | Simplicity bias. Use discovery tools. |
| "We've spent enough time on this" | Sunk cost fallacy. 2 min checking docs beats 20 min guessing. |

## Navigation: Language References

**Available language discovery guides:**
- `references/go.md` - Go: `go doc`, `go list`, example/test scanning
- `references/ruby.md` - Ruby: `bundle info`, `ri`, gem exploration

**Path issues:** Some languages need tool managers (mise, asdf). If `go` or `bundle` not found, try `mise exec -- <command>`.

**Extending this skill:** To add a new language reference, see `references/WRITING.md` for principles and template.

## Navigation: Framework References

**Available framework cheat sheets:**
- `references/go/cobra.md` - Cobra CLI library patterns
- `references/ruby/rails.md` - Rails framework patterns (coming)
- `references/ruby/karafka.md` - Karafka framework patterns (coming)

## Red Flags - When You're About to Fail

**STOP immediately if you catch yourself:**
- Making confident API claims without checking current docs
- Accepting user's confident syntax without verification
- Trying "one more variation" based on pattern-matching
- Using phrases: "should work", "likely", "probably", "common pattern"
- Creating narrative about what "likely happened" without evidence
- Claiming something is "documented" without reading it

**All of these mean: Use discovery tools NOW.**

## After Finding Documentation

1. **Verify**: API signature matches your use case
2. **Adapt**: Use the pattern for your specific need
3. **Test**: Try the verified approach
4. **Update understanding**: Note what changed from your training data

## Real-World Impact

**Without this skill:**
- 15+ minutes guessing at syntax variations
- Confident claims based on outdated training data
- User frustration from repeated failures

**With this skill:**
- 2 minutes checking current docs
- Accurate API usage from installed version
- Fast resolution based on truth, not patterns
