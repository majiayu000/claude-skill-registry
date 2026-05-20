---
name: note-organizer
description: This skill should be used when the user asks to "organize notes", "process notes", "structure my notes", mentions "[raw]" or "[organized]" tags, or needs systematic note processing and extraction of actionable items.
version: 1.0.0
---

# Note Organizer

## Purpose

Transform unstructured notes into organized, actionable format using the framework's tag-based workflow. Extract decisions, actions, questions, and insights from raw text.

## When to Use

- User has raw notes to process
- User wants structured analysis
- User mentions `[raw]` tag
- User wants to extract actions/decisions
- User needs note summarization
- User wants systematic organization

## Core Workflow

### Step 1: Identify Raw Notes

Look for:
- `[raw]` tag explicitly
- Unstructured text blocks
- Meeting notes
- Brainstorming dumps
- Research notes

### Step 2: Extract Structure

Analyze content for:
- **Topics/Themes**: Main subject areas discussed
- **Decisions Made**: Choices, commitments, agreements
- **Actions Required**: Tasks, todos, deliverables
- **Questions Raised**: Open questions, uncertainties
- **Key Insights**: Learnings, realizations, patterns
- **References**: Links, citations, resources mentioned

### Step 3: Apply Tag Taxonomy

Use framework's tag system (see `references/tag-taxonomy.md`):

**Document State**:
- `[raw]` → `[organized]`

**Content Classification**:
- `[decision]` - Decisions made
- `[action]` - Tasks to complete
- `[question]` - Open questions
- `[insight]` - Key learnings
- `[reference]` - External resources
- `[blocker]` - Impediments
- `[risk]` - Potential issues

**Priority Levels**:
- `[urgent]` - Immediate attention
- `[high]` - Important, not urgent
- `[medium]` - Normal priority
- `[low]` - Can defer

### Step 4: Generate Organized Output

**Standard Format**:

```markdown
[organized]

## Summary
[1-2 sentence overview of what notes cover]

## Topics Covered
- Topic 1: [Brief description]
- Topic 2: [Brief description]
- Topic 3: [Brief description]

## Decisions Made
- [decision] Decision 1: [Description + rationale]
- [decision] Decision 2: [Description + rationale]

## Actions Required
- [ ] [urgent] [action] Action 1 - [Owner if known] - [Deadline if known]
- [ ] [high] [action] Action 2 - [Owner] - [Deadline]
- [ ] [medium] [action] Action 3

## Open Questions
- [question] Question 1: [What needs to be answered]
- [question] Question 2: [Context + why it matters]

## Key Insights
- [insight] Insight 1: [What was learned]
- [insight] Insight 2: [Pattern noticed / Realization]

## Blockers & Risks
- [blocker] Blocker 1: [What's blocking + impact]
- [risk] Risk 1: [Potential issue + mitigation idea]

## References
- [reference] [Resource 1 with link]
- [reference] [Resource 2 with link]

## Next Steps
1. [Most important action]
2. [Second priority]
3. [Third priority]
```

### Step 5: Suggest Project Association

If notes relate to active project:
- Tag: `[project:project-name]`
- Suggest: "Add to .projects/[name]/.context.md?"
- Link to project roadmap if relevant

### Step 6: Offer Integration

After organizing, suggest:
- **Save to logs**: Add to daily log (`providers/claude/logs/daily/YYYY.MM.DD.md`)
- **Update project**: Merge decisions/actions into project context
- **Create todos**: Extract actions to todo list
- **Schedule follow-up**: Set reminders for pending items

## Integration with Framework

### Workflow Compatibility

This skill implements: `.workflow-claude-notes-organization.md`

**Traditional workflow**:
```
User writes [raw] notes → Runs /organize → Claude processes → [organized] output
```

**With this skill** (automatic):
```
User mentions "organize" → Skill loads → Processes → [organized] output
```

**Benefit**: No need to remember `/organize` command; conversational trigger

### Tag Extraction Utility

Use bundled script for automatic tag detection:

```bash
echo "[raw] content..." | python ~/.claude/skills/note-organizer/scripts/extract_tags.py
```

**Output**:
```
Tags found:
  - [raw]
  - [decision]
  - [action]
  - [urgent]
```

## Best Practices

### Preserve Context

When organizing:
- Keep original meaning
- Don't invent information
- Flag assumptions clearly
- Preserve nuance

### Be Specific

In extraction:
- Decisions: Include rationale
- Actions: Specify owner + deadline if known
- Questions: Add context
- Insights: Explain significance

### Maintain Traceability

Link organized notes back to:
- Source (if from external doc)
- Date/time discussed
- Participants (if meeting)
- Project (if applicable)

### Handle Edge Cases

**Incomplete notes**:
- Flag missing info: `[unknown owner]`
- Mark uncertain: `[decision?]` vs `[decision]`

**Conflicting info**:
- Document both: "Option A vs Option B"
- Note needs resolution

**Sensitive info**:
- Apply PII tags: `[PII:NAME]` etc.
- Redact before sharing

## Examples

### Example 1: Meeting Notes

**Input**:
```
[raw]
Met with team about Q1 planning. Decided to focus on performance optimization.
Sarah will lead perf work. Need to decide on metrics by Friday. Risk: might
conflict with feature roadmap. Key learning: premature optimization killed us
last time. What's the baseline we're improving from?
```

**Output**:
```
[organized]

## Summary
Q1 planning meeting - Decided to prioritize performance optimization led by Sarah,
with metrics definition needed by Friday.

## Decisions Made
- [decision] Focus Q1 on performance optimization (rationale: customer complaints + competitive pressure)

## Actions Required
- [ ] [urgent] [action] Define performance metrics - Sarah - Friday

## Open Questions
- [question] What's our current performance baseline?
- [question] How does this affect feature roadmap?

## Blockers & Risks
- [risk] Performance focus may conflict with feature delivery roadmap

## Key Insights
- [insight] Premature optimization failed previously - ensure we have clear metrics first

## Next Steps
1. Sarah: Establish performance baselines
2. Team: Define success metrics by Friday
3. Leadership: Align with feature roadmap
```

### Example 2: Research Notes

**Input**:
```
[raw]
Reading about cloud sync patterns. Found 3 approaches: git-based, CRDTs, operational transforms.
Git pros: version control, familiar, free. Cons: conflicts, not real-time.
CRDTs cool but complex. OT used by Google Docs. Decision: start with git,
revisit if needed. Check out Automerge library for future.
```

**Output**:
```
[organized]

## Summary
Research on cloud sync patterns - Evaluated git, CRDTs, and operational transforms.
Chose git-based approach for initial implementation.

## Topics Covered
- Cloud sync architectural patterns
- Trade-offs: simplicity vs real-time vs conflict handling

## Decisions Made
- [decision] Use git-based sync initially (rationale: simple, familiar, free)
- [decision] Defer CRDT/OT exploration until proven need

## Key Insights
- [insight] Git conflicts acceptable for async multi-device, not real-time collab
- [insight] Operational transforms enable real-time (Google Docs approach)

## References
- [reference] Automerge library - CRDT implementation for future evaluation

## Next Steps
1. Implement git-based sync
2. Test with multiple devices
3. Revisit CRDTs if git conflicts become problem
```

## Resources

For detailed information:
- **`references/tag-taxonomy.md`** - Complete framework tag system
- **`scripts/extract_tags.py`** - Automatic tag extraction utility

## Troubleshooting

**Issue**: Tags not recognized
**Solution**: Check `references/tag-taxonomy.md` for valid tags; create custom tags if needed

**Issue**: Over-organization (too granular)
**Solution**: Group related items; not everything needs a tag

**Issue**: Missing context in organized notes
**Solution**: Include more from original; preserve ambiguity when unsure

**Issue**: Unsure how to classify item
**Solution**: Use multiple tags if needed: `[decision] [risk]` for risky decision

## Version History

**v1.0.0** (2025-12-28)
- Initial release
- Tag-based organization
- Framework workflow integration
- Extraction utility included
