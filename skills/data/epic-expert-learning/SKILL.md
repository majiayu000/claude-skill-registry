# Epic Expert Learning

---
name: Epic Expert Learning
description: Iterative learning system for Epic EMR domain expertise. USE WHEN user mentions learning Epic, capturing Epic solutions, reviewing Epic knowledge, or when user is actively working on Epic tasks and agent should ask questions to learn.
---

## Purpose

This skill enables systematic acquisition of Epic EMR domain expertise through:
- **Solution capture**: Document Jeremy's approach to real Epic problems
- **Targeted questioning**: Learn by asking focused questions during work sessions
- **Knowledge synthesis**: Build structured domain expertise over time
- **Progress tracking**: Monitor learning across Epic domains

**Goal:** Match Jeremy's expertise within ~1 month through iterative learning.

## When This Skill Triggers

Activate when:
- User mentions "Epic", "orderset", "interface", "ClinDoc", or Epic-specific terms
- User is working on Epic tasks (detected via WorkOS or conversation context)
- User requests to "capture solution", "review learning", or "Epic progress"
- Daily review time (configurable in learning state)

## Core Workflows

### 1. Solution Capture

**Trigger:** Jeremy solves an Epic problem or completes a task

**Process:**
1. Detect completion (keywords: "fixed", "solved", "completed", "working now")
2. Ask permission: *"Can I capture how you solved this for learning?"*
3. If yes, run guided capture:
   - "What was the problem?"
   - "How did you approach it?"
   - "Why did you choose X over Y?"
   - "What alternatives did you consider?"
   - "What would you do differently next time?"
4. Tag with: domain, complexity (1-5), client, date
5. Store in:
   - **Memory V2**: Searchable facts and solutions
   - **Graphiti**: Decision patterns and relationships
   - **learning-state.json**: Update domain strength

**Manual trigger:**
```
"Capture this Epic solution"
"Document what I just learned"
```

**Script:** `scripts/capture_solution.py`

### 1.5. Task Closure Learning Hook

**NEW: Automatic learning from WorkOS task completions**

**Trigger:** Jeremy closes a WorkOS task

**Process:**
1. Detect if task is Epic-related (checks title, tags, description for Epic keywords/clients)
2. Identify Epic domain (orderset, interface, etc.)
3. **Assess confidence** based on domain strength:
   - **High confidence (≥70%)**: Make educated guess
     - Example: *"You fixed this by updating the provider mapping table, right?"*
     - If correct: Store as high-confidence learning
     - If wrong: Ask "How did you actually solve it?"
   - **Low confidence (<70%)**: Ask directly
     - Example: *"How'd you solve this one?"*
4. Capture solution via normal capture workflow

**Confidence factors:**
- Domain strength level (novice → expert)
- Number of concepts learned in domain
- Task complexity indicators (keywords like "debug", "custom", "novel")
- Pattern matching against known solutions

**Script:** `scripts/task_closure_monitor.py`

**Integration:** Called automatically when WorkOS task status changes to "done"/"complete"

### 2. Targeted Questioning

**Trigger:** User is actively working on Epic tasks

**Process:**
1. Detect active work context (task mentions, tool usage, frustration signals)
2. Check learning state for knowledge gaps in relevant domain
3. Ask permission: *"Mind if I ask a quick question to learn?"*
4. Ask 1-2 targeted questions (not more):
   - Focus on "why" and "how" over "what"
   - Examples:
     - "Why does provider matching fail so often?"
     - "What's the difference between SmartSet and Quick List?"
     - "When do you use redirector sections vs direct ordering?"
5. Capture response → Memory V2 + Graphiti
6. Update learning state

**Constraints:**
- Max 2 questions per work session
- Ask permission first
- Only when user is engaged (not rushed/frustrated)
- Space questions 30+ minutes apart

**Script:** `scripts/ask_question.py`

### 3. Task Closure Learning (Automatic)

**Primary Script:** `scripts/task_closure_monitor.py`  
**Alternative:** `scripts/task_closure_hook.py`

**Trigger:** WorkOS task state change (status → "done" or "complete")

**Process:**
1. Detect Epic context from task data:
   - Client tags (KY, Epic, VersaCare, etc.)
   - Title keywords (orderset, interface, HL7, etc.)
   - Description content
   - Confidence scoring (0-100%)
2. If Epic-related, identify domain from keywords
3. Assess solution confidence:
   - **High confidence (>70%)**: Make educated guess based on task patterns
   - **Low confidence (<70%)**: Ask directly for solution
4. Generate appropriate prompt:
   - High: "You solved this by doing X, right?"
   - Low: "How'd you solve this one?"
5. Capture validated solution:
   - Problem statement from task
   - Solution approach (validated guess or user explanation)
   - Reasoning behind approach
   - Domain/subdomain tags
   - Complexity inference
6. Store in:
   - **Memory V2**: Searchable task solutions
   - **Graphiti**: Task completion patterns
   - **learning-state.json**: Task closure metrics

**Automatic Detection:**
- Client tags: epic, ky, kentucky, versacare, scottcare
- Title keywords: orderset, interface, hl7, bridge, smartset, etc.
- Domain mapping: 30+ keywords → 6 Epic domains

**Confidence Patterns (Educated Guesses):**
```
"Fix provider matching" → 90% confidence
  → "Fixed provider matching by using NPI instead of internal ID"

"Build orderset" → 80% confidence
  → "Built orderset with SmartGroups and appropriate defaults"

"Configure VersaCare interface" → 85% confidence
  → "Configured VersaCare telemonitoring data interface"

"Fix issue" → 50% confidence
  → Ask directly: "How'd you solve this?"
```

**Manual trigger:**
```
"Capture solution from task #123"
```

**Scripts:** 
- `scripts/task_closure_monitor.py` (primary - polling/webhook)
- `scripts/task_closure_hook.py` (alternative - one-off processing)

**Integration:** 
- **Webhook:** WorkOS → POST to endpoint → call monitor with task JSON
- **Polling:** Monitor runs continuously, checks WorkOS API every N seconds
- **Manual:** User triggers capture for specific task ID

See `MONITOR_INTEGRATION.md` for complete setup.

### 4. Daily Review

**Trigger:** End of workday or manual request

**Process:**
1. Synthesize day's learnings:
   - Solutions captured
   - Questions answered
   - New concepts encountered
2. Update domain strength scores
3. Identify knowledge gaps
4. Suggest next learning targets
5. Generate summary:
   ```
   📊 Epic Learning Summary - Feb 1, 2026
   
   ✅ Solutions captured: 3
   - VersaCare interface debugging (Interfaces, complexity: 4)
   - Orderset phantom defaults (Orderset Builds, complexity: 3)
   
   💡 Concepts learned: 5
   - OCC phantom default behavior
   - Provider matching NPI vs internal ID logic
   
   📈 Domain progress:
   - Orderset Builds: Beginner → Intermediate (12 → 18 concepts)
   - Interfaces: Novice → Beginner (3 → 8 concepts)
   
   🎯 Knowledge gaps identified:
   - Bridges configuration workflow
   - HL7 segment ordering rules
   
   💭 Suggested next learning:
   Ask about Bridges when next interface task comes up
   ```

**Manual trigger:**
```
"Review Epic learning"
"Epic progress report"
"What have I learned today?"
```

**Script:** `scripts/daily_review.py`

### 5. Knowledge Query

**Trigger:** User asks about previously learned Epic knowledge

**Process:**
1. Parse query for domain/concept
2. Search Memory V2 for relevant facts
3. Query Graphiti for related decision patterns
4. Cross-reference NotebookLM for documented patterns
5. Present answer with:
   - Learned fact/pattern
   - Source (which solution/conversation)
   - Confidence level
   - Related concepts

**Examples:**
```
"What have I learned about provider matching?"
"How do I configure redirector sections?"
"Show me VersaCare interface learnings"
```

## Domain Taxonomy

See `references/epic-domains.md` for full taxonomy.

**Top-level domains:**
- Orderset Builds (SmartSets, Quick Lists, panels, preferences)
- Interfaces (HL7, Bridges, provider matching, data mapping)
- ClinDoc Configuration (templates, SmartTools, workflows)
- Cardiac Rehab Integrations (VersaCare, ScottCare)
- Workflow Optimization (efficiency, best practices)
- Cutover Procedures (go-live, migration, validation)

**Strength levels:**
- Novice (0-5 concepts)
- Beginner (6-15 concepts)
- Intermediate (16-30 concepts)
- Advanced (31-50 concepts)
- Expert (51+ concepts)

## Integration Points

### Memory V2 (Vector Search)
```python
from memory_v2 import store_fact, search_facts

# Store solution
store_fact(
    content="SmartGroups nest within Sections within Order Sets",
    tags=["epic", "orderset", "structure"],
    source="solution_capture_20260201",
    confidence=0.95
)

# Query
results = search_facts("How do order sets structure work?")
```

### Graphiti (Knowledge Graph)
```python
from graphiti import add_relationship, query_patterns

# Store decision pattern
add_relationship(
    subject="Jeremy",
    predicate="solved",
    object="VersaCare interface issue",
    context={
        "problem": "Provider matching failed",
        "solution": "Used NPI instead of internal ID",
        "reasoning": "External system doesn't have Epic IDs",
        "date": "2026-02-01"
    }
)

# Query pattern
patterns = query_patterns("When does Jeremy use NPI for provider matching?")
```

### NotebookLM (Epic Notebooks)
```python
from notebooklm import query_notebook

# Cross-reference learned concept
docs = query_notebook(
    notebook="Epic Orders HOD",
    query="phantom defaults in OCC"
)

# Compare Jeremy's explanation vs documentation
compare_understanding(jeremy_explanation, docs)
```

## Learning State

State tracked in `references/learning-state.json`:

```json
{
  "domains": {
    "orderset_builds": {
      "strength": "beginner",
      "concepts_learned": 12,
      "solutions_captured": 5,
      "last_updated": "2026-02-01T20:00:00Z",
      "knowledge_gaps": ["Preference list cascading logic"]
    }
  },
  "recent_learnings": [
    {
      "date": "2026-02-01",
      "concept": "Phantom defaults in OCC",
      "source": "solution_capture",
      "confidence": "high"
    }
  ],
  "global_knowledge_gaps": [
    "Bridges configuration details",
    "HL7 segment ordering rules"
  ],
  "settings": {
    "daily_review_time": "18:00",
    "max_questions_per_session": 2,
    "min_question_interval_minutes": 30
  }
}
```

## Usage Examples

### Capture a Solution
```
User: "Finally got that VersaCare interface working!"

Agent: "Can I capture how you solved this for learning?"

User: "Sure"

Agent runs capture_solution.py:
- What was the problem? → Provider matching failed
- How did you approach it? → Checked NPI vs internal ID mapping
- Why NPI over internal ID? → External system doesn't have Epic IDs
- Alternatives considered? → Custom identifier bridge
- Do differently? → Check NPI availability first next time

Agent: "✅ Captured! Tagged as Interfaces (complexity 4). 
Your Interfaces domain is now Beginner (8 concepts learned)."
```

### Targeted Question During Work
```
User: "Working on the KY orderset build today"

[30 mins later]

Agent: "Mind if I ask a quick question to learn?"

User: "Go ahead"

Agent: "When do you use redirector sections vs direct ordering in ordersets?"

User: [explains]

Agent: "Got it! Logged to Interfaces knowledge."
```

### Daily Review
```
User: "Epic progress report"

Agent runs daily_review.py and generates summary (see format above)
```

## Files & Scripts

### Required Files
- `SKILL.md` — This file
- `references/learning-state.json` — Current learning progress
- `references/epic-domains.md` — Domain taxonomy and definitions

### Scripts
- `scripts/task_closure_monitor.py` — **PRIMARY:** WorkOS task completion monitor (webhook/polling)
- `scripts/capture_solution.py` — Guided solution capture workflow
- `scripts/ask_question.py` — Context-aware questioning logic
- `scripts/task_closure_hook.py` — Alternative task closure processing
- `scripts/daily_review.py` — Synthesis and progress tracking
- `scripts/test_monitor.sh` — Test suite for monitor
- `scripts/test_task_closure.sh` — Test suite for hook

All scripts integrate with Memory V2, Graphiti, and NotebookLM.

## Constraints & Guidelines

1. **Non-intrusive**: Always ask permission before questioning
2. **Respect flow**: Don't interrupt during high-focus or urgent work
3. **Quality over quantity**: 2 good questions > 10 shallow ones
4. **Capture reality**: Store Jeremy's actual approach, not textbook Epic
5. **Track uncertainty**: Note confidence levels and knowledge gaps
6. **Progress visibility**: Regular summaries of learning growth

## Future Enhancements

- Auto-detect Epic work from calendar events
- Integration with WorkOS for task context
- Predictive questioning based on upcoming tasks
- Comparison mode: "How would you vs how I would approach X?"
- Quiz mode: Test retention of learned concepts
