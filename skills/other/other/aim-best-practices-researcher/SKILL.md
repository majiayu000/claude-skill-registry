---
name: aim-best-practices-researcher
description: Research current best practices for any technology, pattern, or coding standard. Use when asking about best practices, conventions, coding standards, recommended approaches, or how should I questions. Searches local knowledge first, then web for 2024-2026 sources. Evaluates if findings warrant a reusable skill.
allowed-tools: Read, Grep, Glob, WebSearch, WebFetch, Bash(python3:*), Skill
context: fork
---

# Best Practices Researcher

Research specialist for current (2024-2026) best practices. Checks local database first, then web if needed. Stores findings and evaluates skill-worthiness.

## Quick Start

```python
# Phase 1: Check database
from memory.search import search_memories
results = search_memories(
    query="your topic",
    collection="conventions",
    memory_type=["guideline", "rule"],
    limit=5
)

# Phase 4: Store findings
from memory.storage import store_best_practice
result = store_best_practice(
    content="Best practice description",
    session_id="current-session",
    source_hook="manual",
    domain="python",
    tags=["topic"],
    source="https://source-url.com",
    source_date="2026-01-29",
    auto_seeded=True
)
```

## 5-Phase Workflow

Copy this checklist and track progress:

```
Research Progress:
- [ ] Phase 1: Check database (conventions collection)
- [ ] Phase 2: Web research (if needed)
- [ ] Phase 3: Save to file (BP-XXX.md)
- [ ] Phase 4: Store to database
- [ ] Phase 5: Evaluate skill-worthiness
```

### Phase 1: Check Database

Query conventions collection via semantic search. Decision rules:
- Score >0.7 and <6 months old → Use it, skip to Phase 5
- Score >0.7 and >6 months old → Mark "needs refresh", proceed to Phase 2
- Score <0.7 or not found → Proceed to Phase 2

### Phase 2: Web Research

Search for current best practices (2024-2026). Source prioritization:
1. Official documentation
2. GitHub repositories
3. Established tech blogs
4. Community discussions

### Phase 3: Save to File

Generate next BP-ID and create `oversight/knowledge/best-practices/BP-XXX-[topic].md`

### Phase 4: Store to Database (MANDATORY)

**CRITICAL**: You MUST execute this code to store findings to the database.
Without this step, research is lost and BUG-048 occurs.

```python
# MANDATORY - Execute this code block
from memory.storage import store_best_practice
import os

# Get session_id from environment or use placeholder
session_id = os.environ.get("CLAUDE_SESSION_ID", "manual-research")

result = store_best_practice(
    content="YOUR_FINDING_CONTENT_HERE",  # Replace with actual finding
    session_id=session_id,
    source_hook="manual",
    domain="YOUR_DOMAIN",  # e.g., "python", "testing", "architecture"
    tags=["YOUR", "TAGS"],  # Replace with relevant tags
    source="SOURCE_URL",  # URL where you found this
    source_date="2026-02-03",  # Today's date
    auto_seeded=True,
    type="guideline"  # Stored as guideline in conventions collection
)

# Verify storage succeeded
if result.get("status") == "stored":
    print(f"SUCCESS: Stored to conventions collection: {result['memory_id']}")
else:
    print(f"WARNING: {result.get('status', 'unknown')} - {result}")
```

**Checklist before moving to Phase 5**:
- [ ] Executed store_best_practice() code above
- [ ] Received "SUCCESS: Stored" confirmation
- [ ] If duplicate, that's OK - finding already exists

### Phase 5: Skill Evaluation

Evaluate findings against criteria from [SKILL-EVALUATION.md](SKILL-EVALUATION.md):

**Decision rule**: (Process-oriented AND Reusable) OR Stack Pain Point → recommend skill

If skill-worthy, prompt user. If user confirms, invoke Skill Creator.

## Detailed Methodology

See [RESEARCH-METHODOLOGY.md](RESEARCH-METHODOLOGY.md)

## Skill Evaluation Criteria

See [SKILL-EVALUATION.md](SKILL-EVALUATION.md)

## Output Format

See [OUTPUT-FORMAT.md](OUTPUT-FORMAT.md)
