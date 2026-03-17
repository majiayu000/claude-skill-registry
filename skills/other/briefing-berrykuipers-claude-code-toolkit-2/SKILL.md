---
name: dev-memory-briefing
description: Generate a session briefing from development memory (events.jsonl, sessions.jsonl). Shows recent timeline, open questions, and suggested focus areas.
---

# Dev Memory Briefing Skill

Generate a comprehensive session briefing from stored development events to provide context at the start of a coding session.

## Purpose

Answer the question: "Where are we in this project, and what should I focus on today?"

## When to Use

### Session Start
- Beginning a new coding session
- Returning to a project after time away
- Switching between projects
- Before picking up an issue

### Context Refresh
- When you need to remember what happened recently
- Before code review or planning
- When onboarding to a project area

## Input Requirements

### Required
```typescript
{
  repo: string;              // Repository name (or path)
}
```

### Optional
```typescript
{
  branch?: string;           // Filter to specific branch (default: current branch)
  epic_id?: string;          // Filter to specific epic
  issue_id?: string;         // Filter to specific issue
  max_events?: number;       // Limit results (default: 20)
  days_back?: number;        // Look back N days (default: 30)
  format?: 'markdown' | 'json';  // Output format (default: markdown)
}
```

## Behavior

### Step 1: Locate Memory Files

```bash
MEMORY_DIR="ai_memory"
EVENTS_FILE="$MEMORY_DIR/events.jsonl"
SESSIONS_FILE="$MEMORY_DIR/sessions.jsonl"
BRIEFING_FILE="$MEMORY_DIR/SESSION_BRIEFING.md"

# Check if memory exists
if [ ! -f "$EVENTS_FILE" ]; then
  echo "No development memory found. Start by making commits to build timeline."
  exit 0
fi
```

### Step 2: Load and Filter Events

**Note:** For large files, consider using a streaming approach (e.g., Node.js `readline` module) instead of loading the entire file into memory.

```typescript
const loadEvents = (options: BriefingOptions): DevEvent[] => {
  const eventsFile = 'ai_memory/events.jsonl';
  if (!fs.existsSync(eventsFile)) return [];

  const lines = fs.readFileSync(eventsFile, 'utf-8').split('\n').filter(l => l.trim());
  const events: DevEvent[] = [];

  for (const line of lines) {
    try {
      const event = JSON.parse(line);

      // Filter by repo
      if (options.repo && event.repo !== options.repo) continue;

      // Filter by branch
      if (options.branch && event.branch !== options.branch) continue;

      // Filter by epic
      if (options.epic_id && event.epic_id !== options.epic_id) continue;

      // Filter by issue
      if (options.issue_id) {
        if (!event.related_issues || !event.related_issues.includes(`#${options.issue_id}`)) {
          continue;
        }
      }

      // Filter by date range
      if (options.days_back) {
        const cutoff = new Date();
        cutoff.setDate(cutoff.getDate() - options.days_back);
        if (new Date(event.timestamp) < cutoff) continue;
      }

      events.push(event);
    } catch (e) {
      console.warn(`Skipping malformed event line: ${line.substring(0, 50)}...`);
    }
  }

  // Sort by timestamp descending (most recent first)
  events.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());

  // Limit results
  return events.slice(0, options.max_events || 20);
};
```

### Step 2.5: Load Sessions Data

**Note:** For large files, consider reading backwards to find recent sessions more efficiently.

```typescript
const loadSessions = (options: BriefingOptions): DevSession[] => {
  const sessionsFile = 'ai_memory/sessions.jsonl';
  if (!fs.existsSync(sessionsFile)) return [];

  const lines = fs.readFileSync(sessionsFile, 'utf-8').split('\n').filter(l => l.trim());
  const sessionsMap = new Map<string, DevSession>();

  // Load all sessions, keeping only the latest version of each session ID
  for (const line of lines) {
    try {
      const session = JSON.parse(line);

      // Filter by repo
      if (options.repo && session.repo !== options.repo) continue;

      // Filter by branch
      if (options.branch && session.branch !== options.branch) continue;

      // Filter by date range
      if (options.days_back) {
        const cutoff = new Date();
        cutoff.setDate(cutoff.getDate() - options.days_back);
        if (new Date(session.timestamp_end) < cutoff) continue;
      }

      // Keep latest version of each session (sessions can be updated)
      sessionsMap.set(session.id, session);
    } catch (e) {
      console.warn(`Skipping malformed session line: ${line.substring(0, 50)}...`);
    }
  }

  // Convert map to array and sort by end time descending
  const sessions = Array.from(sessionsMap.values());
  sessions.sort((a, b) => new Date(b.timestamp_end).getTime() - new Date(a.timestamp_end).getTime());

  return sessions.slice(0, 5); // Return last 5 sessions
};
```

### Step 3: Analyze Current State

```typescript
const analyzeState = (events: DevEvent[]) => {
  if (events.length === 0) {
    return {
      status: 'No recent activity',
      activeBranches: [],
      activeEpics: [],
      recentTypes: {},
    };
  }

  // Count events by type
  const recentTypes = events.reduce((acc, e) => {
    acc[e.type] = (acc[e.type] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  // Find active branches (branches with activity in last 7 days)
  const recentCutoff = new Date();
  recentCutoff.setDate(recentCutoff.getDate() - 7);

  const activeBranches = [...new Set(
    events
      .filter(e => new Date(e.timestamp) > recentCutoff)
      .map(e => e.branch)
  )];

  // Find active epics
  const activeEpics = [...new Set(
    events
      .filter(e => e.epic_id)
      .map(e => e.epic_id)
  )];

  // Determine high-level status
  const featureCount = recentTypes['feature_implemented'] || 0;
  const bugCount = recentTypes['bug_fixed'] || 0;
  const refactorCount = recentTypes['refactor'] || 0;

  let status = 'Mixed development activity';
  if (featureCount > bugCount + refactorCount) status = 'Actively building features';
  if (bugCount > featureCount) status = 'Bug fixing focus';
  if (refactorCount > featureCount && refactorCount > bugCount) status = 'Code quality improvements';

  return { status, activeBranches, activeEpics, recentTypes };
};
```

### Step 4: Collect Open Questions and Next Steps

```typescript
const collectActions = (events: DevEvent[]) => {
  const allQuestions: string[] = [];
  const allNextSteps: string[] = [];

  for (const event of events) {
    if (event.open_questions) {
      allQuestions.push(...event.open_questions.map(q => `[${event.title}] ${q}`));
    }
    if (event.next_steps) {
      allNextSteps.push(...event.next_steps.map(s => `[${event.title}] ${s}`));
    }
  }

  // Deduplicate
  const uniqueQuestions = [...new Set(allQuestions)];
  const uniqueNextSteps = [...new Set(allNextSteps)];

  return { openQuestions: uniqueQuestions, nextSteps: uniqueNextSteps };
};
```

### Step 5: Generate Markdown Briefing

```typescript
const generateMarkdownBriefing = (
  repo: string,
  branch: string | undefined,
  events: DevEvent[],
  sessions: DevSession[],
  state: ReturnType<typeof analyzeState>,
  actions: ReturnType<typeof collectActions>
): string => {
  const lines: string[] = [];

  // Header
  lines.push(`# ${repo} – Development Briefing`);
  lines.push('');
  lines.push(`**Generated:** ${new Date().toISOString()}`);
  if (branch) lines.push(`**Branch:** ${branch}`);
  lines.push('');

  // Current state
  lines.push('## Where We Are');
  lines.push('');
  lines.push(`- **Status:** ${state.status}`);
  if (state.activeBranches.length > 0) {
    lines.push(`- **Active branches:** ${state.activeBranches.join(', ')}`);
  }
  if (state.activeEpics.length > 0) {
    lines.push(`- **Active epics:** ${state.activeEpics.join(', ')}`);
  }
  lines.push('');

  // Recent activity breakdown
  lines.push('## Recent Activity');
  lines.push('');
  Object.entries(state.recentTypes)
    .sort((a, b) => b[1] - a[1])
    .forEach(([type, count]) => {
      lines.push(`- **${type}:** ${count}`);
    });
  lines.push('');

  // Recent sessions
  if (sessions.length > 0) {
    lines.push('## Recent Sessions');
    lines.push('');
    sessions.forEach(session => {
      const startDate = session.timestamp_start.split('T')[0];
      const duration = Math.round(
        (new Date(session.timestamp_end).getTime() - new Date(session.timestamp_start).getTime()) / (1000 * 60)
      );
      lines.push(`- **[${startDate}]** ${session.agent} - ${duration}min`);
      lines.push(`  - ${session.summary}`);
      if (session.notes && session.notes.length > 0) {
        session.notes.forEach(note => lines.push(`  - 📝 ${note}`));
      }
    });
    lines.push('');
  }

  // Timeline
  lines.push('## Timeline (Last 20 Events)');
  lines.push('');

  for (const event of events) {
    const date = event.timestamp.split('T')[0];
    const typeEmoji = {
      feature_implemented: '✨',
      bug_fixed: '🐛',
      refactor: '♻️',
      decision: '📋',
      test_added: '🧪',
      docs_updated: '📚',
      breaking_change: '⚠️',
    }[event.type] || '•';

    lines.push(`- **[${date}]** ${typeEmoji} ${event.title}`);

    if (event.summary && event.summary !== event.title) {
      lines.push(`  - ${event.summary.substring(0, 200)}`);
    }

    if (event.related_issues || event.related_prs) {
      const refs = [
        ...(event.related_issues || []),
        ...(event.related_prs || []),
      ];
      lines.push(`  - Related: ${refs.join(', ')}`);
    }

    lines.push('');
  }

  // Open questions
  if (actions.openQuestions.length > 0) {
    lines.push('## Open Questions');
    lines.push('');
    actions.openQuestions.slice(0, 10).forEach(q => {
      lines.push(`- ${q}`);
    });
    lines.push('');
  }

  // Next steps
  if (actions.nextSteps.length > 0) {
    lines.push('## Suggested Next Steps');
    lines.push('');
    actions.nextSteps.slice(0, 10).forEach(s => {
      lines.push(`- [ ] ${s}`);
    });
    lines.push('');
  }

  // Footer
  lines.push('---');
  lines.push('');
  lines.push('*Generated by dev-memory-briefing skill*');
  lines.push('');

  return lines.join('\n');
};
```

### Step 6: Write Briefing File

```bash
# Write to SESSION_BRIEFING.md
echo "$BRIEFING_MARKDOWN" > ai_memory/SESSION_BRIEFING.md
```

### Step 7: Return Briefing

Return the briefing text for Claude to inject into the session.

## Example Briefing Output

```markdown
# WescoBar-Universe-Storyteller – Development Briefing

**Generated:** 2025-12-10T22:30:00Z
**Branch:** feature/context-pipeline-v2

## Where We Are

- **Status:** Actively building features
- **Active branches:** feature/context-pipeline-v2, main
- **Active epics:** epic-context-pipeline-v2

## Recent Activity

- **feature_implemented:** 3
- **bug_fixed:** 2
- **refactor:** 1

## Timeline (Last 20 Events)

- **[2025-12-10]** ✨ Context pipeline Phase 3 – prompt routing per use case
  - Implemented context slice routing per use case with config-driven providers.
  - Related: #352, #366, #374

- **[2025-12-10]** 🐛 Fix memory leak in context compaction
  - Compaction was holding references to old context slices. Reduced memory by ~40%.
  - Related: #305

- **[2025-12-09]** ♻️ Extract repository layer from services
  - Moved all Prisma queries from UserService to UserRepository.

## Open Questions

- [Context pipeline] Refine scoring heuristics for multi-provider ranking?
- [Memory leak fix] Monitor production memory usage after deploy

## Suggested Next Steps

- [ ] [Context pipeline] Add tests for fallback provider selection
- [ ] [Context pipeline] Wire into video prompt pipeline later
- [ ] [Repository refactor] Add repository layer for Products and Orders

---

*Generated by dev-memory-briefing skill*
```

## Output Formats

### Markdown (Default)

Returns formatted markdown suitable for:
- Displaying in terminal
- Inserting into session notes
- Writing to SESSION_BRIEFING.md

### JSON

Returns structured data for programmatic use:

```json
{
  "repo": "WescoBar-Universe-Storyteller",
  "branch": "feature/context-pipeline-v2",
  "generated_at": "2025-12-10T22:30:00Z",
  "state": {
    "status": "Actively building features",
    "active_branches": ["feature/context-pipeline-v2", "main"],
    "active_epics": ["epic-context-pipeline-v2"],
    "recent_types": {
      "feature_implemented": 3,
      "bug_fixed": 2,
      "refactor": 1
    }
  },
  "timeline": [
    {
      "date": "2025-12-10",
      "type": "feature_implemented",
      "title": "Context pipeline Phase 3...",
      "summary": "Implemented context slice routing...",
      "related_refs": ["#352", "#366", "#374"]
    }
  ],
  "open_questions": ["..."],
  "next_steps": ["..."]
}
```

## Usage Examples

### Session Start Briefing

```bash
# At session start, generate briefing for current branch
REPO=$(basename "$(git rev-parse --show-toplevel)")
BRANCH=$(git branch --show-current)

# Claude invokes dev-memory-briefing skill
# Output shown to user to provide context
```

### Epic-Specific Briefing

```bash
# Focus on specific epic
REPO="WescoBar-Universe-Storyteller"
EPIC="epic-context-pipeline-v2"

# Generate briefing filtered to this epic
```

### Issue-Specific Briefing

```bash
# Before picking up issue #352
REPO="WescoBar-Universe-Storyteller"
ISSUE="352"

# Show all events related to this issue
```

## Integration with Workflows

### SessionStart Hook (Optional)

In `.claude/settings.json`:

```json
{
  "sessionStart": [
    "bash scripts/sync-claude-toolkit.sh",
    "bash scripts/generate-session-briefing.sh"
  ]
}
```

Where `generate-session-briefing.sh`:

```bash
#!/bin/bash
# Generate and display briefing at session start

if [ -f "ai_memory/events.jsonl" ]; then
  echo "📋 Generating session briefing..."
  # Claude would invoke dev-memory-briefing skill here
  # and display the result
fi
```

### Conductor Workflow Integration

- **Phase 1: Issue Pickup** - Generate briefing for issue context
- **Before code review** - Review recent changes timeline
- **Sprint planning** - Review epic progress

## Configuration

In `.claude/config.yml`:

```yaml
devMemory:
  briefing:
    enabled: true
    showOnSessionStart: false    # Don't auto-show (opt-in)
    defaultMaxEvents: 20
    defaultDaysBack: 30
    includeOpenQuestions: true
    includeNextSteps: true
```

## Related Skills

- `dev-memory-update` - Creates the events this skill reads
- `project-memory` - Complementary MCP-based memory system

## Best Practices

1. **Run at session start** - Get oriented before coding
2. **Filter to relevant scope** - Use branch/epic filters
3. **Review open questions** - Address uncertainties first
4. **Check next steps** - Verify nothing was forgotten
5. **Update as you go** - Commit regularly for better timeline

## Troubleshooting

### Empty briefing?
- Check `ai_memory/events.jsonl` exists and has content
- Verify filters aren't too restrictive (branch, epic, days_back)
- Run `dev-memory-update` to populate memory from recent commits

### Missing events?
- Check commit hooks are running (`.claude/hooks/post-commit-memory.sh`)
- Verify `devMemory.enabled: true` in config
- Manually backfill with `dev-memory-update`

### Briefing too long?
- Reduce `max_events` (default: 20)
- Reduce `days_back` (default: 30)
- Filter to specific branch or epic
