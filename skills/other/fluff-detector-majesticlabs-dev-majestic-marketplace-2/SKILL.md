---
name: fluff-detector
description: Detect human-oriented content in LLM artifacts. Flags attribution, personas, redundant explanations, marketing language, and decorative elements that waste tokens without improving LLM behavior.
allowed-tools: Bash Read Glob Grep
---

# Fluff Detector

## Purpose

Verify that agents, commands, and skills are written for LLM consumption, not human readers. Every token should improve execution, not provide comfort or credibility.

## When to Use

- Creating new agents, commands, or skills
- Reviewing PRs that add/modify LLM artifacts
- Quality gate before merge
- Auditing existing artifacts for token waste

## Fluff Categories

### 1. Attribution Signals

Content that establishes credibility for humans but has no LLM value.

| Pattern | Example | Problem |
|---------|---------|---------|
| "Inspired by X" | "Inspired by DHH's approach" | LLM can't retrieve by author |
| "Based on X's methodology" | "Based on Martin Fowler's patterns" | Pure credibility signal |
| "According to X" | "According to industry experts" | Appeal to authority |
| "As recommended by" | "As recommended by Google" | No execution value |

**Exception:** Names that define a style (e.g., "DHH-style Rails") are functional, not attribution.

**Detection pattern:**
```regex
(inspired by|based on|according to|as recommended by|following|using|applying)\s+[A-Z][a-z]+('s)?
```

### 2. Decorative Quotes

Inspirational or philosophical quotes that add no functional value.

| Pattern | Example |
|---------|---------|
| Epigraph quotes | "The best code is no code" - Someone |
| Philosophy | "In the spirit of simplicity..." |
| Motivation | "Great engineers always..." |

**Detection pattern:**
```regex
^>\s*[""].*[""].*[-—]\s*[A-Z]
[""][^""]{20,}[""][\s]*[-—]
```

### 3. Persona Fluff

Role descriptions that tell the LLM what it "is" instead of what to do.

| Pattern | Example | Better |
|---------|---------|--------|
| Identity statements | "You are a senior engineer" | (delete) |
| Capability claims | "You have deep expertise in..." | (delete) |
| Personality traits | "You are helpful and thorough" | (delete) |
| Self-reference | "As an AI assistant..." | (delete) |

**Detection pattern:**
```regex
^(You are|As an?|I am|Acting as)\s+(a |an |the )?[a-z]+(ly)?\s+(and\s+[a-z]+\s+)?
```

### 4. Redundant Explanations

Explaining what LLMs already know or can infer.

| Pattern | Example |
|---------|---------|
| Tool explanations | "The Read tool allows you to read files" |
| Obvious context | "This agent is used for..." |
| Meta-commentary | "The following section describes..." |
| Format explanations | "The output should be formatted as..." (when showing format) |

**Detection pattern:**
```regex
(this (agent|skill|command) (is used|helps|allows|enables))
(the following (section|content|instructions))
(as (shown|described|mentioned) (above|below|previously))
```

### 5. Marketing Language

Promotional or sales-oriented language inappropriate for LLM instructions.

| Pattern | Example |
|---------|---------|
| Superlatives | "Best-in-class", "world-class", "cutting-edge" |
| Promises | "Ensures perfect results", "guarantees success" |
| Buzzwords | "Revolutionary", "game-changing", "next-gen" |
| Vague claims | "Highly efficient", "extremely powerful" |

**Detection pattern:**
```regex
(best-in-class|world-class|cutting-edge|state-of-the-art|revolutionary|game-chang|next-gen|highly efficient|extremely powerful|ensures? (perfect|optimal)|guarantee)
```

### 6. Hedging Language

Uncertainty markers that add no value.

| Pattern | Example | Better |
|---------|---------|--------|
| "Try to" | "Try to follow best practices" | "Follow best practices" |
| "Attempt to" | "Attempt to minimize errors" | "Minimize errors" |
| "Consider" | "Consider using X" | "Use X when Y" |
| "Maybe" | "Maybe add validation" | "Add validation if X" |

**Detection pattern:**
```regex
\b(try to|attempt to|consider\s+(using|adding|implementing)|you (might|may|could) want to|perhaps|maybe)\b
```

### 7. Filler Phrases

Zero-information phrases that pad content.

| Pattern | Delete |
|---------|--------|
| "It's important to note that" | ✓ |
| "Please keep in mind that" | ✓ |
| "It goes without saying" | ✓ |
| "Needless to say" | ✓ |
| "In order to" | Use "to" |
| "Due to the fact that" | Use "because" |
| "At this point in time" | Use "now" |

**Detection pattern:**
```regex
(it('s| is) (important|worth|crucial) to (note|mention|remember)|please (keep in mind|note|remember)|goes without saying|needless to say|in order to|due to the fact|at this point in time|as a matter of fact|for all intents and purposes)
```

## Usage

### Validate Single File

```bash
./scripts/detect-fluff.sh path/to/file.md
```

### Validate All Agents

```bash
for agent in plugins/*/agents/**/*.md; do
  ./scripts/detect-fluff.sh "$agent"
done
```

### CI Integration

```yaml
- name: Detect Fluff
  run: |
    find plugins -name "*.md" -path "*/agents/*" -o -name "*.md" -path "*/skills/*" -o -name "*.md" -path "*/commands/*" | while read f; do
      .claude/skills/fluff-detector/scripts/detect-fluff.sh "$f" || exit 1
    done
```

## Output Format

```
Analyzing: plugins/majestic-engineer/agents/qa/test-reviewer.md

[WARN] Line 12: Attribution signal
  > "Based on Kent Beck's TDD principles"
  Suggestion: Remove attribution or rephrase as pattern name

[WARN] Line 45: Persona fluff
  > "You are an expert test reviewer with deep knowledge"
  Suggestion: Delete - LLM doesn't need identity statements

[WARN] Line 78: Filler phrase
  > "It's important to note that tests should be isolated"
  Suggestion: "Tests should be isolated"

Summary: 3 fluff instances found
```

## Severity Levels

| Level | Action | Example |
|-------|--------|---------|
| ERROR | Must fix | Persona statements, marketing language |
| WARN | Should fix | Attribution, hedging, fillers |
| INFO | Consider | Redundant explanations (may be intentional) |

## False Positive Handling

Some patterns have legitimate uses:

| Pattern | Legitimate Use |
|---------|----------------|
| "Based on" | "Based on user input" (not attribution) |
| "Consider" | In decision trees with conditions |
| Names | When defining a style (DHH, Warren Buffett) |

The script uses context analysis to reduce false positives.

## Error Codes

| Code | Meaning |
|------|---------|
| 0 | No fluff detected |
| 1 | Warnings found (non-blocking) |
| 2 | Errors found (blocking) |
