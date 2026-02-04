---
name: text-anti-slop
description: >
  Enforce professional technical writing standards. Prevents generic AI patterns
  through clear, direct prose. Eliminates overused transitions, buzzwords, and
  meta-commentary. Use when writing or reviewing documentation, reports, or technical content.
applies_to:
  - "**/*.md"
  - "**/*.txt"
  - "**/*.rst"
tags: [writing, documentation, technical-writing, clarity]
related_skills:
  - external/humanizer
  - r/anti-slop
  - python/anti-slop
version: 2.0.0
---

# Text Anti-Slop Skill for Technical Writing

## When to Use This Skill

Use text-anti-slop when:
- ✓ Writing technical documentation, README files, or guides
- ✓ Reviewing AI-generated documentation before publishing
- ✓ Cleaning up marketing language in technical content
- ✓ Editing academic or research writing
- ✓ Preparing content for professional publication
- ✓ Teaching writing standards to teams

Do NOT use when:
- Writing creative fiction (different standards)
- Legal documents (require specific phrasings)
- Marketing copy (intentionally uses persuasive language)
- Following specific style guides (AP, Chicago, etc.)

For the **24-pattern Wikipedia humanizer checklist**, use the separate **humanizer** skill.

## Quick Example

**Before (AI Slop)**:
> In this document, we will delve into the complexities of API design. It's important to note that in today's fast-paced world, leveraging best practices is crucial for success. We'll navigate through various approaches, ultimately providing you with actionable insights to empower your development workflow.

**After (Anti-Slop)**:
> This guide covers API design principles. We explain three approaches: RESTful, GraphQL, and gRPC. Each section includes code examples and trade-offs.

**What changed**:
- ✓ Removed meta-commentary ("In this document, we will...")
- ✓ Eliminated filler ("delve into", "navigate through")
- ✓ Replaced buzzwords ("leverage", "empower")
- ✓ Removed obvious transitions ("ultimately", "it's important to note")
- ✓ Led with the point directly

## When to Use What

| If you see... | Replace with... | Details |
|---------------|-----------------|---------|
| "delve into" | "examine" or delete | reference/transitions.md |
| "leverage" | "use" | reference/buzzwords.md |
| "in order to" | "to" | reference/filler.md |
| "It's important to note that" | Delete and state the point | reference/meta-commentary.md |
| "navigate the complexities" | Specific challenge or delete | reference/transitions.md |
| Meta-commentary | Direct statement | reference/meta-commentary.md |
| Long wordy phrases | Simple alternatives | reference/filler.md |

## Core Workflow

### 3-Step Quality Check

1. **Remove meta-commentary**
   ```markdown
   # Bad
   In this section, we will discuss error handling.
   Let's take a closer look at the implementation.

   # Good
   Error handling uses try/catch blocks.
   The implementation checks for three error types:
   ```

2. **Replace filler and buzzwords**
   ```markdown
   # Bad
   In order to leverage the power of our framework, users need to
   utilize the config file to enable the feature.

   # Good
   To use the framework, set `enable_feature: true` in `config.yml`.
   ```

3. **Lead with the point**
   ```markdown
   # Bad
   It's important to note that before you proceed with installation,
   you should be aware that Python 3.8+ is required.

   # Good
   Requires Python 3.8 or later.
   ```

## Quick Reference Checklist

Before publishing technical writing, verify:

- [ ] No meta-commentary ("In this guide...", "Let's explore...")
- [ ] No high-risk transitions ("delve into", "navigate complexities")
- [ ] No corporate buzzwords ("leverage", "synergistic", "paradigm shift")
- [ ] No wordy constructions ("in order to" → "to")
- [ ] Paragraphs lead with the point, not preambles
- [ ] Concrete examples, not abstract statements
- [ ] Varied sentence structure and length
- [ ] Active voice where possible
- [ ] Specific terms, not generic ("data", "things", "items")
- [ ] Direct statements, not excessive hedging

## Common Workflows

### Workflow 1: Clean Up README or Documentation

**Context**: AI generated a README with generic patterns.

**Steps**:

1. **Run detection script**
   ```bash
   python toolkit/scripts/detect_slop.py README.md --verbose
   ```

2. **Remove meta-commentary**
   ```markdown
   # Before
   ## Introduction
   In this project, we aim to provide developers with a comprehensive
   solution for managing configuration files. Let me walk you through
   the key features that make this tool essential.

   # After
   ## Features
   - Hot reload configuration without restart
   - Environment-specific configs
   - Schema validation with JSON Schema
   ```

3. **Replace buzzwords**
   ```markdown
   # Before
   Our solution leverages cutting-edge technology to empower developers
   and unlock the full potential of configuration management.

   # After
   Validates and reloads config files automatically.
   ```

4. **Simplify wordy phrases**
   ```markdown
   # Before
   Due to the fact that the system has the ability to detect changes,
   it will automatically reload in order to apply the new settings.

   # After
   The system detects changes and reloads automatically.
   ```

5. **Run automated cleanup**
   ```bash
   python toolkit/scripts/clean_slop.py README.md --save
   ```

**Expected outcome**: Clear, direct documentation with score <30

---

### Workflow 2: Review Technical Blog Post

**Context**: Cleaning up a technical blog post before publication.

**Steps**:

1. **Check opening paragraphs**
   ```markdown
   # Bad
   In today's fast-paced world of software development, it's become
   increasingly important to understand the complexities of async programming.
   In this article, I will delve into the intricacies of async/await.

   # Good
   Async/await lets JavaScript handle concurrent operations without blocking.
   This post shows three common patterns and their trade-offs.
   ```

2. **Remove transition overload**
   ```markdown
   # Bad
   Furthermore, it's worth noting that moreover, the implementation
   ultimately provides developers with enhanced capabilities.

   # Good
   The implementation supports retries, timeouts, and cancellation.
   ```

3. **Replace vague terms with specifics**
   ```markdown
   # Bad
   The data shows interesting results. Various metrics indicate
   significant improvements. Things are looking positive.

   # Good
   Response time dropped from 200ms to 45ms. Memory usage decreased 30%.
   ```

4. **Check closing**
   ```markdown
   # Bad
   In conclusion, as we've explored throughout this article, it's clear
   that async programming plays a crucial role in modern development.

   # Good
   Use async/await for I/O operations. Avoid it for CPU-intensive work.
   ```

**Expected outcome**: Professional blog post that teaches, not pads

---

### Workflow 3: Clean Up API Documentation

**Context**: Auto-generated API docs need human touch.

**Steps**:

1. **Fix function descriptions**
   ```markdown
   # Bad
   ### `processData(data)`
   This function processes the data. It takes data as input and returns
   the processed result. This is a critical function for data processing.

   # Good
   ### `processData(data)`
   Validates and normalizes customer records.

   **Parameters:**
   - `data` (Array): Raw customer records from CSV import

   **Returns:** Array of validated records with normalized phone numbers
   ```

2. **Add concrete examples**
   ```markdown
   # Bad
   **Example:**
   ```js
   processData(data)
   ```

   # Good
   **Example:**
   ```js
   const raw = [{name: "Alice", phone: "555.1234"}]
   const clean = processData(raw)
   // => [{name: "Alice", phone: "555-1234"}]
   ```
   ```

3. **Remove obvious headers**
   ```markdown
   # Bad
   ## Overview
   This section provides an overview of the API.

   ## Getting Started
   To get started with the API, follow these steps.

   # Good
   ## Authentication
   Include your API key in the `Authorization` header:
   ```

**Expected outcome**: Docs that help developers, not slow them down

## Mandatory Rules Summary

### 1. No Meta-Commentary
**Delete stage directions about what the document will do**

Bad: "In this section..." "Let's explore..." "As we'll see..."
Good: Just say the thing.

### 2. Lead with the Point
**First sentence states the main idea**

Bad: Preamble → context → point
Good: Point → details

### 3. Specific Not Generic
**Use concrete terms**

Bad: "data", "things", "items", "various"
Good: "customer records", "API endpoints", "config files"

### 4. Simple Not Wordy
**Choose shorter alternatives**

- "in order to" → "to"
- "due to the fact that" → "because"
- "has the ability to" → "can"

### 5. Direct Not Hedged
**Be confident or be specific about uncertainty**

Bad: "may possibly", "could potentially", "it appears that"
Good: "does X" or "unclear whether X"

## Resources & Advanced Topics

### Reference Files

- **[reference/transitions.md](reference/transitions.md)** - Overused transition phrases to avoid
- **[reference/buzzwords.md](reference/buzzwords.md)** - Corporate jargon and replacements
- **[reference/filler.md](reference/filler.md)** - Wordy constructions and alternatives
- **[reference/meta-commentary.md](reference/meta-commentary.md)** - Self-referential patterns to delete
- **[reference/structure.md](reference/structure.md)** - Document organization principles

### Related Skills

- **humanizer** - Wikipedia's 24-pattern checklist for AI writing
- **r/anti-slop** - For R package documentation (roxygen, vignettes)
- **python/anti-slop** - For Python docstrings
- **quarto/anti-slop** - For reproducible research documents

### Tools

- `python toolkit/scripts/detect_slop.py` - Detect text patterns (score 0-100)
- `python toolkit/scripts/clean_slop.py` - Automated cleanup with backup

## Scoring Guide

Detection script scores (0-100, higher is worse):

| Score | Meaning | Action |
|-------|---------|--------|
| 0-20 | Low slop (authentic writing) | Minor tweaks |
| 20-40 | Moderate (some patterns) | Review flagged items |
| 40-60 | High (many patterns) | Significant cleanup needed |
| 60+ | Severe (heavily generic) | Consider rewriting |

## Context Awareness

Not all patterns are always slop. Consider:

- **Audience**: Academic writing may need more hedging
- **Purpose**: Legal docs need specific phrasing; marketing needs energy
- **Length**: Longer pieces need more transitions
- **Domain**: Technical docs have different norms than creative writing

The issue is **overuse** and **unconscious repetition**, not pattern existence.

## Integration with Humanizer Skill

This skill focuses on **structural clarity** (remove transitions, buzzwords, filler).

The **humanizer** skill adds **personality and voice** (Wikipedia's 24 patterns).

Use both for complete coverage:

| Task | Use This Skill | + Humanizer |
|------|----------------|-------------|
| Technical docs | text/anti-slop (structure) | + humanizer (voice) |
| README files | text/anti-slop (clarity) | + humanizer (natural flow) |
| Blog posts | text/anti-slop (direct) | + humanizer (personality) |
| Package docs | text/anti-slop (no filler) | + humanizer (human touch) |
