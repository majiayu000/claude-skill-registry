---
name: incorporate-learnings
description: Takes investigated issues and incorporates the learnings into the LearningAgent's knowledge base by updating core-knowledge.md, topics, or learnings files.
user-invocable: false
---

# Incorporate Learnings

Take investigated issues and integrate the lessons learned into the LearningAgent's knowledge.

## Arguments

`$ARGUMENTS` is the path to the session log folder (e.g., `.deepwork/tmp/agent_sessions/<session_id>/<agent_id>/`).

## Context

**Agent used**: !`cat $ARGUMENTS/agent_used 2>/dev/null || echo "unknown"`

If `agent_used` is "unknown", stop and report an error.

**Investigated Issues you need to Process**:
!`grep -l 'status: investigated' $ARGUMENTS/*.issue.yml 2>/dev/null || echo "(none)"`

**Additional incorporation guidelines**:
!`learning_agents/scripts/cat_agent_guideline.sh $ARGUMENTS learning_from_issues`

## Procedure

If no investigated issues are listed above, skip to Step 3 (still update tracking files).

### Step 1: Incorporate Each Issue

For each investigated issue, read its `issue_description` and `investigation_report`, then choose the best incorporation strategy in this priority order:

#### A. Amend existing content (prefer this)

If a closely related file already exists in the agent's knowledge base, edit it rather than creating a new one.

#### B. Update `core-knowledge.md`

For **universal one-liners** — something fundamental expressible in 1-2 sentences.

#### C. Add a new topic in `topics/`

For a **conceptual area** needing 1+ paragraphs of reference material. Use this frontmatter:

```markdown
---
name: <Topic Name>
keywords:
  - <relevant keyword>
last_updated: <YYYY-MM-DD>
---
```

#### D. Add a new learning in `learnings/`

For cases where the **narrative context** of how the issue unfolded is needed. Use this frontmatter:

```markdown
---
name: <Descriptive name>
last_updated: <YYYY-MM-DD>
summarized_result: |
  <1-3 sentence summary of the key takeaway>
---

## Context
## Investigation
## Resolution
## Key Takeaway
```

If you add a learning, also consider adding a brief note to a related Topic referencing it.

#### E. Do nothing

If the issue is unlikely to recur or would be hard to prevent, skip it.

### Step 2: Update Issue Status

For each incorporated issue, change `status: investigated` to `status: learned`.

### Step 3: Update Session Tracking

Always run this step, even if no issues were incorporated.

```bash
[ -f $ARGUMENTS/needs_learning_as_of_timestamp ] && rm $ARGUMENTS/needs_learning_as_of_timestamp
date -u +"%Y-%m-%dT%H:%M:%SZ" > $ARGUMENTS/learning_last_performed_timestamp
```

### Step 4: Summary

```
## Incorporation Summary

- **Issues processed**: <count>
- <issue-filename> → <action taken: updated core-knowledge | created topic <name> | created learning <name> | amended <filename> | skipped>
```

## Guardrails

- Do NOT create overly broad or vague learnings — be specific and actionable
- Do NOT duplicate existing knowledge — check the auto-included lists above
- Do NOT remove existing content unless directly contradicted by new evidence
- Keep `core-knowledge.md` concise — move detailed content to topics or learnings
- Use today's date for `last_updated` fields
- Always run Step 3 even if no issues were incorporated
