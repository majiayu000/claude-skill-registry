---
name: PheroPath
description: A filesystem-based stigmergy communication protocol. Use this to leave invisible "pheromones" (signals) on files to communicate context, risks, or status to other agents or your future self without modifying file content.
---

# PheroPath Agent Skill

PheroPath allows you to attach context (DANGER, TODO, SAFE, INSIGHT) to files using Extended Attributes (or a sidecar fallback).

## Usage Guide

### 1. Secrete (Leave a Signal)
**Script:** `scripts/secrete.py`

**When to use:**
- **DANGER**: You found a bug/risk you cannot fix immediately.
- **TODO**: You are leaving untidied code or suggestions.
- **SAFE**: You verified a module is robust.
- **INSIGHT**: You want to explain *why* something is implemented this way.

**Bash Examples (Few-Shot):**

```bash
# Example 1: Mark a file as dangerous due to a race condition
python3 scripts/secrete.py "src/concurrency.py" "DANGER" "Rate limit race condition under high load" --intensity 1.0

# Example 2: Leave a TODO note for refactoring
python3 scripts/secrete.py "src/legacy_api.py" "TODO" "Needs migration to v2 API schema"

# Example 3: Mark a test file as verified
python3 scripts/secrete.py "tests/test_auth.py" "SAFE" "Passed all penetration tests"

# Example 4: Add architectural insight
python3 scripts/secrete.py "src/core/engine.py" "INSIGHT" "Core loop logic derived from paper X" --ttl 168
```

### 2. Sniff (Read Signals)
**Script:** `scripts/sniff.py`

**When to use:**
- **ALWAYS** before starting a task in an unfamiliar directory.
- Before modifying critical files to check for `DANGER`.

**Bash Examples (Few-Shot):**

```bash
# Example 1: Sniff a specific file
python3 scripts/sniff.py "src/main.py"

# Example 2: Sniff an entire directory (recursive) to gather context
python3 scripts/sniff.py "src/" --min-intensity 0.1

# Example 3: Parse output (it is JSON)
python3 scripts/sniff.py "src/" | jq '.[].message'
```

### 3. Cleanse (Remove Signals)
**Script:** `scripts/cleanse.py`

**When to use:**
- After fixing a bug (remove `DANGER`).
- After completing a task (remove `TODO`).

**Bash Examples (Few-Shot):**

```bash
# Example 1: Remove signal from a specific file (e.g. after fixing it)
python3 scripts/cleanse.py "src/concurrency.py"

# Example 2: Prune weak signals (intensity < 0.2) from a directory
python3 scripts/cleanse.py "src/" --prune 0.2

# Example 3: Clear ALL signals from a directory (Reset)
python3 scripts/cleanse.py "src/" --all
```
