---
name: editorial-workflow
description: Manage editorial workflows for newsrooms and publications. Use when tracking story assignments, managing deadlines, coordinating editorial calendars, or establishing handoff protocols between reporters and editors. Includes templates for assignment tracking, editorial calendars, and workflow documentation.
---

# Editorial workflow management

Newsrooms run on systems. This skill provides templates and processes for tracking stories, managing deadlines, and coordinating between reporters and editors.

## When to use

- Setting up story tracking systems
- Creating editorial calendars
- Establishing assignment and handoff protocols
- Managing multiple stories and deadlines
- Training new editors on workflow

## Story status taxonomy

### Standard statuses

| Status | Meaning | Owner |
|--------|---------|-------|
| **Pitch** | Idea submitted, awaiting approval | Reporter |
| **Assigned** | Approved, reporter working | Reporter |
| **Reporting** | Active reporting in progress | Reporter |
| **Draft** | First draft submitted | Editor |
| **Edit** | Editor making changes | Editor |
| **Revision** | Back with reporter for changes | Reporter |
| **Copy** | Copy editing stage | Copy editor |
| **Final** | Ready for publication | Editor |
| **Scheduled** | Queued for specific date | System |
| **Published** | Live | Complete |
| **Hold** | Paused, not abandoned | Editor |
| **Kill** | Story abandoned | Editor |

### Status flow

```
Pitch → Assigned → Reporting → Draft → Edit → Revision (loop) → Copy → Final → Scheduled → Published
                                         ↓
                                       Hold/Kill
```

## Story assignment tracking

### Assignment record template

```markdown
## Story: [Slug/working title]

### Assignment details
- **Reporter:** [name]
- **Assigning editor:** [name]
- **Date assigned:** [date]
- **Deadline:** [date/time]
- **Target publication:** [outlet/section]

### Story specs
- **Format:** [brief, feature, enterprise, etc.]
- **Word count:** [target]
- **Multimedia:** [photos, video, graphics needed]
- **Sources required:** [minimum sources]

### The assignment
[What the story is, angle, key elements to include]

### Key contacts
[Sources to interview, PR contacts, experts]

### Background/resources
[Links to previous coverage, documents, data]

### Budget line
[One sentence for editorial budget meetings]

### Status history
| Date | Status | Notes |
|------|--------|-------|
| [date] | Assigned | |
| [date] | [status] | [note] |
```

### Assignment handoff checklist

When assigning a story:

```markdown
## Assignment handoff

### From editor to reporter
- [ ] Story scope clearly defined
- [ ] Deadline confirmed
- [ ] Word count/format specified
- [ ] Key sources identified
- [ ] Background materials shared
- [ ] Multimedia needs discussed
- [ ] Questions answered

### Reporter confirms
- [ ] Deadline is realistic
- [ ] Have access to necessary sources
- [ ] Understand the angle
- [ ] Know who to ask for help
```

## Editorial calendar

### Calendar template

```markdown
## Editorial calendar: [Week/Month of Date]

### Monday [date]
| Time | Story | Reporter | Status | Notes |
|------|-------|----------|--------|-------|
| AM | [story] | [name] | [status] | |
| PM | [story] | [name] | [status] | |

### Tuesday [date]
[same format]

### Evergreen queue
| Story | Reporter | Ready date | Notes |
|-------|----------|------------|-------|
| [story] | [name] | [date] | [can run anytime after this] |

### Upcoming (next 2 weeks)
| Story | Reporter | Target date | Status |
|-------|----------|-------------|--------|
| [story] | [name] | [date] | [status] |
```

### Planning meeting template

For weekly/daily editorial meetings:

```markdown
## Editorial meeting: [date]

### Today's lineup
| Story | Reporter | Status | Publish time | Notes |
|-------|----------|--------|--------------|-------|
| [story] | [name] | [status] | [time] | |

### Tomorrow's lineup
[same format]

### In progress (due this week)
| Story | Reporter | Due | Status | Blockers |
|-------|----------|-----|--------|----------|
| [story] | [name] | [date] | [status] | [any issues] |

### Pipeline (next 2+ weeks)
| Story | Reporter | Target | Status |
|-------|----------|--------|--------|
| [story] | [name] | [date] | [status] |

### Discussion items
- [Topic 1]
- [Topic 2]

### Action items
- [ ] [Action] - [Owner] - [Deadline]
```

## Deadline management

### Deadline types

| Deadline | Purpose | Typical lead time |
|----------|---------|-------------------|
| **Reporting** | Complete interviews/research | 2-5 days before draft |
| **First draft** | Submit to editor | 24-48 hours before edit |
| **Final draft** | After revisions | 12-24 hours before copy |
| **Art/photos** | Visuals ready | Same as first draft |
| **Copy edit** | Language/style review | 4-8 hours before publish |
| **Publish** | Goes live | Set time |

### Deadline tracking template

```markdown
## Story: [title]
**Final publish deadline:** [date/time]

### Working backward
| Milestone | Deadline | Status |
|-----------|----------|--------|
| Reporting complete | [date] | ☐ |
| First draft due | [date] | ☐ |
| Art/photos due | [date] | ☐ |
| Edit complete | [date] | ☐ |
| Revisions due | [date] | ☐ |
| Copy edit complete | [date] | ☐ |
| Final review | [date] | ☐ |
| Schedule/publish | [date] | ☐ |
```

### Missed deadline protocol

When a deadline is at risk:

1. **Notify immediately** - Don't wait until the deadline passes
2. **Explain briefly** - What's blocking progress
3. **Propose new deadline** - Realistic estimate
4. **Offer alternatives** - Shorter version? Different angle?

```markdown
## Deadline alert

**Story:** [title]
**Original deadline:** [date/time]
**Issue:** [what's blocking]
**New proposed deadline:** [date/time]
**Impact:** [what this affects]
**Alternatives:** [options if any]
```

## Edit handoff protocols

### Reporter → Editor

When submitting draft:

```markdown
## Draft submission: [story title]

**Draft location:** [link/file]
**Word count:** [count]

### What's in the draft
- [Key points covered]

### What's still needed
- [ ] [Outstanding item]
- [ ] [Waiting for source callback]

### Questions for editor
- [Question about structure, angle, etc.]

### Source notes
[Any attribution issues, off-record info, etc.]

### Multimedia status
- Photos: [ready/pending/needed]
- Graphics: [ready/pending/needed]
```

### Editor → Reporter

When returning for revision:

```markdown
## Edit notes: [story title]

**Overall:** [brief assessment - on track, needs work, etc.]

### Structural changes needed
- [Major reorg, missing elements, etc.]

### Specific fixes
- Line [X]: [issue/change]
- Line [X]: [issue/change]

### Questions to resolve
- [Question requiring reporter input]

### Deadline for revisions
[date/time]

### Discussion needed?
[Yes - let's talk before you revise / No - changes are clear]
```

## Publication checklist

### Pre-publish checklist

```markdown
## Pre-publish: [story title]

### Content
- [ ] Headline is accurate and compelling
- [ ] Dek/subhead summarizes well
- [ ] Lede works
- [ ] All facts verified
- [ ] All sources attributed correctly
- [ ] Quotes are accurate
- [ ] Numbers double-checked

### Style
- [ ] AP Style applied
- [ ] Consistent voice throughout
- [ ] No typos or grammatical errors
- [ ] Appropriate length

### Legal/Ethics
- [ ] No defamation risk
- [ ] Sources of comment contacted
- [ ] Corrections from previous versions applied
- [ ] Embargoes respected

### Multimedia
- [ ] Photos have captions and credits
- [ ] Alt text added
- [ ] Video/audio plays correctly
- [ ] Graphics are accurate

### Metadata
- [ ] SEO headline filled
- [ ] Meta description written
- [ ] Tags/categories applied
- [ ] Author byline correct
- [ ] Publication date/time set

### Final sign-off
- [ ] Reporter reviewed final
- [ ] Editor approved
- [ ] Copy editor signed off
```

### Post-publish checklist

```markdown
## Post-publish: [story title]

### Immediate (within 1 hour)
- [ ] Story displays correctly
- [ ] Links work
- [ ] Images load
- [ ] No obvious errors
- [ ] Social posts scheduled/published

### Same day
- [ ] Monitor comments/feedback
- [ ] Watch for corrections needed
- [ ] Track initial metrics
- [ ] Respond to any issues

### Follow-up
- [ ] Note any updates needed
- [ ] Document corrections made
- [ ] Capture reader response
- [ ] Plan follow-up stories if warranted
```

## Workflow documentation

### Process documentation template

For documenting your newsroom's workflows:

```markdown
## Workflow: [Name of process]

### Purpose
[What this workflow accomplishes]

### When to use
[Triggers for this workflow]

### Roles involved
| Role | Responsibility |
|------|----------------|
| [Role] | [What they do] |

### Process steps

**Step 1: [Name]**
- Owner: [role]
- Action: [what happens]
- Output: [what's produced]
- Next: [what triggers next step]

**Step 2: [Name]**
[same format]

### Tools used
- [Tool]: [what it's used for]

### Templates/Forms
- [Link to templates]

### Exceptions
- [When normal process doesn't apply]
- [What to do instead]

### Escalation
- [When to escalate]
- [Who to contact]
```

### Onboarding new staff

```markdown
## Editorial workflow onboarding

### Day 1
- [ ] Access to CMS granted
- [ ] Added to editorial chat/channels
- [ ] Received style guide
- [ ] Introduced to direct editor

### Week 1
- [ ] Shadow experienced reporter
- [ ] Review workflow documentation
- [ ] Complete first assignment (low-stakes)
- [ ] Learn deadline expectations

### Month 1
- [ ] Independently handle standard assignments
- [ ] Know escalation paths
- [ ] Understand publication calendar
- [ ] Comfortable with all tools

### Key contacts
| Need | Contact |
|------|---------|
| Assignment questions | [name] |
| Technical issues | [name] |
| Editorial disputes | [name] |
| HR/Admin | [name] |
```

---

*Good workflows disappear. You only notice them when they break.*
