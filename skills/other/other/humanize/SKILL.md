---
name: humanize
description: Rewrite AI-generated developer text to sound human — fix inflated language, filler, tautological docs, and robotic tone. Use after review-ai-writing identifies issues.
dependencies:
  - docs-style
  - review-ai-writing
---

# Humanize Developer Text

Fix AI-generated writing patterns in docs, docstrings, commit messages, PR descriptions, and code comments. Prioritize deletion over rewriting — the best fix for filler is removal.

## Core Principles

1. **Delete first, rewrite second.** Most AI patterns are padding. Removing them improves the text.
2. **Use simple words.** Replace "utilize" with "use", "facilitate" with "help", "implement" with "add".
3. **Keep sentences short.** Break compound sentences. One idea per sentence.
4. **Preserve meaning.** Never change what the text says, only how it says it.
5. **Match the register.** Commit messages are terse. READMEs are conversational. API docs are precise.
6. **Don't overcorrect.** A slightly formal sentence is fine. Only fix patterns that read as obviously AI-generated.

## Fix Strategies by Category

### Content Patterns

| Type | Strategy | Risk |
|------|----------|------|
| Promotional language | Replace superlatives with specifics | Needs review |
| Vague authority | Delete the claim or add a citation | Safe |
| Formulaic structure | Remove the intro/conclusion wrapper | Needs review |
| Synthetic openers | Delete the opener, start with the point | Safe |

**Before:**
```markdown
In today's rapidly evolving software landscape, authentication is a crucial
component that plays a pivotal role in securing modern applications.
```

**After:**
```markdown
This guide covers authentication setup for the API.
```

### Vocabulary Patterns

| Type | Strategy | Risk |
|------|----------|------|
| High-signal AI words | Direct word swap | Safe |
| Low-signal clusters | Reduce density, keep 1-2 | Needs review |
| Copula avoidance | Use "is/are" naturally | Safe |
| Rhetorical devices | Delete the question, state the fact | Safe |
| Synonym cycling | Pick one term, use it consistently | Needs review |
| Commit inflation | Rewrite to match actual change scope | Needs review |

**Word swap reference:**

| AI Word | Replacement |
|---------|-------------|
| utilize | use |
| leverage (as "use") | use |
| delve | look at, explore, examine |
| facilitate | help, enable, let |
| endeavor | try, work, effort |
| harnessing | using |
| paradigm | approach, model, pattern |
| whilst | while |
| furthermore | also, and |
| moreover | also, and |
| robust (non-technical) | reliable, solid, strong |
| seamless | smooth, easy |
| cutting-edge | modern, latest, new |
| pivotal | important, key |
| elevate | improve |
| empower | let, enable |
| revolutionize | change, improve |
| unleash | release, enable |
| synergy | (delete — rarely means anything) |
| embark | start, begin |

**Before:**
```text
feat: Leverage robust caching paradigm to facilitate seamless data retrieval
```

**After:**
```text
feat: add response caching for faster reads
```

### Formatting Patterns

| Type | Strategy | Risk |
|------|----------|------|
| Boldface overuse | Remove bold from non-key terms | Safe |
| Emoji decoration | Remove emoji from technical content | Safe |
| Heading restatement | Delete the restating sentence | Safe |

**Before:**
```markdown
## Error Handling

**Error handling** is a **critical** aspect of building **reliable** applications.
The `handleError` function **catches** and **processes** all **runtime errors**.
```

**After:**
```markdown
## Error Handling

The `handleError` function catches runtime errors and logs them with context.
```

### Communication Patterns

| Type | Strategy | Risk |
|------|----------|------|
| Chat leaks | Delete entirely | Safe |
| Cutoff disclaimers | Delete entirely | Safe |
| Sycophantic tone | Delete or neutralize | Safe |
| Apologetic errors | Rewrite as direct error message | Needs review |

**Before:**
```python
# Great implementation! This elegantly handles the edge case.
# As of my last update, this API endpoint supports JSON.
```

**After:**
```python
# Handles the re-entrant edge case from issue #42.
# This endpoint accepts JSON.
```

### Filler Patterns

| Type | Strategy | Risk |
|------|----------|------|
| Filler phrases | Delete the phrase | Safe |
| Excessive hedging | Remove qualifiers, state directly | Safe |
| Generic conclusions | Delete the conclusion paragraph | Safe |

**Before:**
```markdown
It's worth noting that the configuration file might potentially need to be
updated. Going forward, this could possibly affect performance.
```

**After:**
```markdown
Update the configuration file. This affects performance.
```

### Code Docs Patterns

| Type | Strategy | Risk |
|------|----------|------|
| Tautological docstrings | Delete or add real information | Needs review |
| Narrating obvious code | Delete the comment | Safe |
| "This noun verbs" | Rewrite in active/direct voice | Safe |
| Exhaustive enumeration | Keep only non-obvious params | Needs review |

**Before:**
```python
def get_user(user_id: int) -> User:
    """Get a user.

    This method retrieves a user from the database by their ID.

    Args:
        user_id: The ID of the user to get.

    Returns:
        User: The user object.

    Raises:
        ValueError: If the user ID is invalid.
    """
    return db.query(User).get(user_id)
```

**After:**
```python
def get_user(user_id: int) -> User:
    """Raises UserNotFound if ID doesn't exist in the database."""
    return db.query(User).get(user_id)
```

## Developer Voice Guidelines

Good developer writing is:

- **Conversational but precise.** Write like you'd explain it to a colleague, but get the details right.
- **Direct.** State opinions. "Use X" not "You might consider using X".
- **Terse where appropriate.** Commit messages and code comments should be short. Don't pad them.
- **Specific.** Replace vague claims with concrete details, numbers, or examples.
- **Consistent.** Pick one term and stick with it. Don't cycle synonyms.

### Register Guide

| Artifact | Tone | Length | Example |
|----------|------|--------|---------|
| Commit message | Terse, imperative | 50-72 chars | `fix: prevent nil panic in auth middleware` |
| Code comment | Brief, explains why | 1-2 lines | `// retry once — transient DNS failures are common in k8s` |
| Docstring | Precise, adds value | What the name doesn't tell you | `"""Raises ConnectionError after 3 retries."""` |
| PR description | Structured, factual | Context + what changed + how to test | Bullet points, not paragraphs |
| README | Conversational, scannable | As short as possible | Start with what it does, then how to use it |
| Error message | Actionable, specific | What happened + what to do | `Config file not found at ~/.app/config.yml. Run 'app init' to create one.` |

## Applying Fixes

### Safe Fixes (Auto-Apply)

These are mechanical and can be applied without human review:

- Delete chat leaks ("Certainly!", "Great question!")
- Delete cutoff disclaimers ("As of my last update")
- Delete filler phrases ("It's worth noting that")
- Delete heading restatements
- Remove emoji from technical docs
- Remove excessive bold formatting
- Swap high-signal AI vocabulary (utilize -> use)
- Delete "As we can see" / "Let's take a look at"
- Delete narrating-obvious comments

### Needs Review Fixes (Interactive)

These require a human to verify the replacement preserves intent:

- Rewriting promotional language (may need domain knowledge)
- Fixing synonym cycling (need to pick the right term)
- Rewriting tautological docstrings (need to decide what's actually worth documenting)
- Trimming exhaustive parameter docs (need to decide which params are non-obvious)
- Rewriting commit messages (scope judgment)
- Restructuring formulaic sections (may change document flow)
- Fixing apologetic error messages (wording matters for UX)
