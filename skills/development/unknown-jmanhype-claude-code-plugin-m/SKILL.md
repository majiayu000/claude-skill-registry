# ACE Context Engineering Skill

**Name:** ace-context-engineering
**Version:** 1.0.0
**Description:** Agentic Context Engineering - Progressive disclosure and incremental context evolution through bullets and deltas

---

## Purpose

This skill enables autonomous evolution of the context system through:

1. **Retrieval** - Query relevant bullets based on task context
2. **Generation** - Solve tasks using retrieved guidance
3. **Reflection** - Evaluate what worked/didn't work
4. **Curation** - Propose incremental delta updates
5. **Merge** - Apply deltas to evolve the playbook

---

## When to Use This Skill

✅ **Use when:**
- Completing complex tasks that could benefit from learned patterns
- Discovering new heuristics or edge cases
- Finding gaps in current context/guidance
- Task failed and needs to capture lessons learned
- User explicitly requests context improvement

❌ **Don't use when:**
- Simple, one-off tasks with no reusable patterns
- Just reading/retrieving context (use Read tool instead)
- No clear signal about what worked or didn't work

---

## File Structure

```
.claude/skills/ace-context-engineering/
├── skill.md                    # This file
├── playbook.json               # Current bullet library
├── schemas/
│   ├── bullet.schema.json      # Bullet validation schema
│   └── delta.schema.json       # Delta validation schema
└── scripts/
    └── validate_delta.py       # Delta validation script
```

---

## Workflow: Full ACE Cycle

### Phase 1: RETRIEVE

**Goal:** Load relevant bullets for current task

1. Read `playbook.json` to get available bullets
2. Filter by tags matching task domain (e.g., "tool.edit", "git.push", "domain.plugin_marketplace")
3. Score bullets by:
   - Tag relevance (how many tags overlap with task)
   - `helpful_count` (higher = better)
   - `harmful_count` (higher = worse, may skip)
   - Confidence level
   - Recency (newer bullets might be more relevant)
4. Select top 5-10 bullets (avoid context overload)

**Example retrieval for "edit JSON file" task:**

```json
{
  "task_tags": ["tool.edit", "tool.read", "json", "validation"],
  "retrieved_bullets": [
    "bullet-2025-10-25-001",  // Read before edit
    "bullet-2025-10-25-012",  // Preserve indentation
    "bullet-2025-10-25-006"   // Validate JSON
  ]
}
```

### Phase 2: GENERATE

**Goal:** Solve the task using retrieved guidance

1. Apply bullet guidance to task execution
2. Track which bullets you actually used
3. Observe execution outcomes (success/failure)
4. Note any gaps in guidance

**Output format:**

```json
{
  "final_answer": "Completed successfully. Edited file.json with proper validation.",
  "used_bullet_ids": [
    "bullet-2025-10-25-001",
    "bullet-2025-10-25-012",
    "bullet-2025-10-25-006"
  ],
  "observations": [
    "Read-before-edit rule prevented error",
    "Indentation rule ensured match worked",
    "Validation caught malformed JSON before commit"
  ],
  "answer_confidence": "high",
  "unused_bullets": [],
  "missing_guidance": []
}
```

### Phase 3: REFLECT

**Goal:** Evaluate effectiveness and propose improvements

1. Review generator output and actual outcomes
2. Mark helpful bullets (incremented `helpful_count`)
3. Mark harmful bullets (incremented `harmful_count`)
4. Identify missing patterns (propose new bullets)
5. Identify redundancies (propose merges)
6. Identify obsolete guidance (propose deprecations)

**Output format:**

```json
{
  "proposed_deltas": {
    "new_bullets": [
      {
        "id": "bullet-2025-10-25-013",
        "title": "Validate JSON before committing to avoid CI failures",
        "content": "Always run JSON validation (using jq or validation script) before committing JSON files. Common issues: trailing commas, unescaped strings, missing brackets. Catching these locally prevents CI pipeline failures and saves time.",
        "tags": ["json", "validation", "git.commit", "best_practice"],
        "evidence": [
          {
            "type": "execution",
            "ref": "task-2025-10-25-042",
            "note": "Prevented malformed JSON from being committed"
          }
        ],
        "confidence": "medium",
        "scope": "global"
      }
    ],
    "counters": [
      {"id": "bullet-2025-10-25-001", "helpful_delta": 1},
      {"id": "bullet-2025-10-25-012", "helpful_delta": 1},
      {"id": "bullet-2025-10-25-006", "helpful_delta": 1}
    ]
  },
  "reflection_notes": "All three retrieved bullets were directly helpful. Discovered new pattern about JSON validation timing that should be captured."
}
```

### Phase 4: CURATE

**Goal:** Normalize and deduplicate proposed deltas

1. Check for duplicate bullets (compare with existing playbook)
2. Normalize tags (use existing tag taxonomy)
3. Ensure rationales are clear
4. Validate delta against schema
5. Resolve conflicts (editing + deprecating same bullet)

**Deduplication criteria:**

- Semantic similarity > 80% (similar title + content)
- High tag overlap (>70% shared tags)
- Same intent/purpose

**Output format:**

```json
{
  "clean_delta": {
    "delta_id": "delta-2025-10-25-001",
    "timestamp": "2025-10-25T12:34:56Z",
    "author": "agent",
    "rationale": "Captured JSON validation pattern from successful task execution",
    "task_context": "Editing plugin metadata.json file",
    "reviewed": false,
    "new_bullets": [...],
    "counters": [...]
  },
  "curation_notes": "No duplicates found. New bullet is distinct from existing validation guidance.",
  "requires_human_review": false
}
```

### Phase 5: MERGE

**Goal:** Apply delta to playbook

1. Validate delta using `validate_delta.py`
2. Apply operations in order:
   - Update counters
   - Add new bullets
   - Apply edits
   - Execute merges (combine + archive merged bullets)
   - Process deprecations (move to archived status)
3. Update metadata (total_bullets, last_curated timestamp)
4. Save updated playbook
5. (Optional) Commit to version control

---

## Retrieval Algorithm

### Simple Tag-Based Retrieval

```python
def retrieve_bullets(task_tags: List[str], playbook: Dict) -> List[Dict]:
    """
    Retrieve relevant bullets for a task based on tag overlap and effectiveness
    """
    bullets = playbook['bullets']
    scored = []

    for bullet in bullets:
        if bullet['status'] != 'active':
            continue  # Skip deprecated/archived

        # Calculate tag overlap
        bullet_tags = set(bullet['tags'])
        task_tags_set = set(task_tags)
        overlap = len(bullet_tags & task_tags_set)

        if overlap == 0:
            continue  # No relevance

        # Calculate success rate
        total = bullet['helpful_count'] + bullet['harmful_count']
        success_rate = bullet['helpful_count'] / total if total > 0 else 0.5

        # Confidence weighting
        confidence_weight = {'high': 1.0, 'medium': 0.8, 'low': 0.6}
        conf = confidence_weight.get(bullet.get('confidence', 'medium'), 0.8)

        # Combined score
        score = overlap * success_rate * conf
        scored.append((score, bullet))

    # Sort by score descending, take top 10
    scored.sort(reverse=True, key=lambda x: x[0])
    return [bullet for score, bullet in scored[:10]]
```

### Advanced: Semantic Similarity

For more sophisticated retrieval, use embedding-based similarity:

1. Embed task description
2. Embed bullet title + content
3. Compute cosine similarity
4. Combine with tag-based score
5. Rank and select top-k

---

## Delta Merge Algorithm

### Deterministic Merge Process

```python
def merge_delta(playbook: Dict, delta: Dict) -> Dict:
    """
    Apply delta operations to playbook deterministically
    """
    # 1. Update counters
    for counter in delta.get('counters', []):
        bullet = find_bullet(playbook, counter['id'])
        if bullet:
            bullet['helpful_count'] += counter.get('helpful_delta', 0)
            bullet['harmful_count'] += counter.get('harmful_delta', 0)
            bullet['last_updated'] = now()

    # 2. Add new bullets
    for new_bullet in delta.get('new_bullets', []):
        new_bullet['created'] = now()
        new_bullet['last_updated'] = now()
        playbook['bullets'].append(new_bullet)

    # 3. Apply edits
    for edit in delta.get('edits', []):
        bullet = find_bullet(playbook, edit['id'])
        if bullet:
            bullet.update(edit['set'])
            bullet['last_updated'] = now()

    # 4. Execute merges
    for merge in delta.get('merges', []):
        keep_bullet = find_bullet(playbook, merge['keep_id'])
        for merge_id in merge['merge_ids']:
            merged = find_bullet(playbook, merge_id)
            if merged:
                # Combine counters
                keep_bullet['helpful_count'] += merged['helpful_count']
                keep_bullet['harmful_count'] += merged['harmful_count']
                # Archive merged bullet
                merged['status'] = 'archived'
                merged['deprecation_reason'] = f"Merged into {merge['keep_id']}"
        if 'merged_content' in merge:
            keep_bullet['content'] = merge['merged_content']
        keep_bullet['last_updated'] = now()

    # 5. Process deprecations
    for deprecation in delta.get('deprecations', []):
        bullet = find_bullet(playbook, deprecation['id'])
        if bullet:
            bullet['status'] = 'deprecated'
            bullet['deprecation_reason'] = deprecation['reason']
            bullet['last_updated'] = now()

    # 6. Update metadata
    playbook['metadata']['total_bullets'] = len(playbook['bullets'])
    playbook['metadata']['active_bullets'] = sum(
        1 for b in playbook['bullets'] if b['status'] == 'active'
    )
    playbook['metadata']['last_curated'] = now()

    return playbook
```

---

## Practical Examples

### Example 1: Simple Counter Update

**Scenario:** Used bullet-2025-10-25-001 successfully

**Delta:**

```json
{
  "counters": [
    {
      "id": "bullet-2025-10-25-001",
      "helpful_delta": 1,
      "evidence": {
        "type": "execution",
        "ref": "task-edit-config",
        "note": "Read-before-edit prevented error"
      }
    }
  ]
}
```

### Example 2: New Pattern Discovered

**Scenario:** Found that git push needs retry logic for network failures

**Delta:**

```json
{
  "new_bullets": [
    {
      "id": "bullet-2025-10-25-013",
      "title": "Retry git push with exponential backoff on network failures",
      "content": "When git push fails with network errors (not auth errors), retry up to 4 times with exponential backoff: 2s, 4s, 8s, 16s. This handles transient network issues without overwhelming the server. Check error message to distinguish network vs auth failures.",
      "tags": ["git.push", "retry", "network", "error_handling"],
      "evidence": [
        {
          "type": "execution",
          "ref": "commit-abc123",
          "note": "Push succeeded on 2nd retry after network timeout"
        }
      ],
      "confidence": "high",
      "scope": "global",
      "helpful_count": 0,
      "harmful_count": 0,
      "links": ["bullet-2025-10-25-003"]
    }
  ]
}
```

### Example 3: Merge Redundant Bullets

**Scenario:** Two bullets say similar things about JSON validation

**Delta:**

```json
{
  "merges": [
    {
      "keep_id": "bullet-2025-10-25-006",
      "merge_ids": ["bullet-2025-10-25-999"],
      "rationale": "Both bullets address JSON validation before commit. bullet-006 is more comprehensive and has higher helpful_count.",
      "merged_content": "Always validate JSON files before committing. Use validation scripts or jq. Common issues: trailing commas, unescaped strings, missing brackets. For plugin marketplace, also check against schema. Validation prevents CI failures and saves time."
    }
  ]
}
```

### Example 4: Deprecate Obsolete Guidance

**Scenario:** Old bullet says to use deprecated API

**Delta:**

```json
{
  "deprecations": [
    {
      "id": "bullet-2024-08-15-042",
      "reason": "API v1 was deprecated. All code now uses API v2.",
      "replacement_id": "bullet-2025-10-25-088"
    }
  ]
}
```

---

## Usage Guidelines

### When to Grow vs Refine

**Grow (add new bullets):**
- Discovered new useful pattern
- Found edge case not covered
- Learned domain-specific heuristic
- Tool usage recipe emerged
- Default mode

**Refine (merge/deprecate):**
- Clear redundancy between bullets
- Proven obsolescence (API changed, tool deprecated)
- High context pressure (playbook too large)
- Conflicting guidance (need to resolve)

### Evidence Quality

**High confidence evidence:**
- `execution`: Tool success/failure logs
- `validation`: Test results, schema validation
- `test_result`: Automated test outcomes

**Medium confidence evidence:**
- `user_feedback`: User confirmed it helped
- `documentation`: Official docs support this

**Low confidence evidence:**
- `low_confidence`: Hunch or untested hypothesis
- No evidence: Mark bullet with `confidence: "low"`

### Tag Taxonomy

Use hierarchical tags with dots:

- `tool.bash`, `tool.edit`, `tool.read`
- `git.push`, `git.commit`, `git.fetch`
- `api.github`, `api.github.ratelimit`
- `domain.plugin_marketplace`, `domain.web_scraping`
- `error_handling`, `retry`, `validation`
- `antipattern`, `best_practice`, `critical`

---

## Validation Workflow

Before merging a delta:

```bash
# 1. Validate delta structure
python .claude/skills/ace-context-engineering/scripts/validate_delta.py \
  proposed_delta.json \
  --playbook .claude/skills/ace-context-engineering/playbook.json

# 2. If valid, review output
# 3. If approved, merge (apply delta operations)
# 4. Commit updated playbook to version control
```

---

## Integration with Context System

### Automatic Reflection Triggers

Consider proposing deltas after:

1. **Task completion** (if new patterns emerged)
2. **Error recovery** (if guidance was missing or wrong)
3. **Tool failure** (if unexpected behavior occurred)
4. **User correction** (if user pointed out mistake)

### TodoWrite Integration

When using TodoWrite, consider ACE reflection as final step:

```
[ ] Complete feature X
[ ] Run tests
[ ] Fix any errors
[ ] Propose ACE delta for patterns discovered
```

### Feedback Loop

```
Task → Retrieve Bullets → Execute → Observe Outcome → Reflect → Propose Delta → Curate → Merge → Updated Playbook
                                                                                                   ↑
                                                                                                   └─ Next Task
```

---

## Limitations & Future Work

**Current limitations:**

- Manual retrieval (no automatic semantic search)
- No A/B testing (can't compare with/without bullet)
- Simple scoring (no learned weights)
- No conflict resolution strategy (relies on human review)

**Future enhancements:**

- Embedding-based semantic retrieval
- Automated counter updates from test results
- Learned retrieval and ranking models
- Automatic duplicate detection
- Impact analysis (measure bullet effectiveness)
- Cross-project bullet sharing

---

## Quick Reference

### Read playbook

```bash
cat .claude/skills/ace-context-engineering/playbook.json | jq '.bullets[] | {id, title, tags}'
```

### Find bullets by tag

```bash
cat playbook.json | jq '.bullets[] | select(.tags[] | contains("tool.edit"))'
```

### Validate delta

```bash
python scripts/validate_delta.py my_delta.json --playbook playbook.json
```

### Check bullet effectiveness

```bash
cat playbook.json | jq '.bullets[] | {id, title, helpful: .helpful_count, harmful: .harmful_count}'
```

---

**End of skill.md**
