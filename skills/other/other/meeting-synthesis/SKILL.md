---
name: meeting-synthesis
description: Use when extracting product signals from meeting transcripts - systematically identifies asks, problems, quotes, and evidence across time windows with customer attribution
allowed-tools: Read, Grep, Glob
---

# Meeting Synthesis

## Purpose

Extract actionable product signals from meeting transcripts:
- Feature requests and capability asks
- Pain points and friction areas
- Customer quotes and verbatim feedback
- Evidence for epic creation and prioritization
- Pattern detection across multiple customers

## When to Use This Skill

Activate automatically when:
- `product-planning` workflow gathers signals for epics
- `cs-prep` workflow compiles customer context for QBRs
- `strategy-session` workflow needs customer insights
- User explicitly requests meeting synthesis
- Any workflow requires customer evidence extraction

## Signal Types

### 1. Feature Requests ("Asks")
Explicit requests for new capabilities or enhancements.

**Indicators:**
- "We need..."
- "Can you build..."
- "It would be great if..."
- "Our team wants..."

**Extract:**
- What capability is requested?
- Why is it needed? (business impact)
- Who requested it? (customer, role)
- When? (meeting date)

### 2. Pain Points ("Problems")
Friction, blockers, or inefficiencies users experience.

**Indicators:**
- "It's frustrating that..."
- "We struggle with..."
- "The current process is..."
- "Our team spends too much time..."

**Extract:**
- What is the pain point?
- How does it impact workflow/outcomes?
- Frequency/severity?
- Who experiences it?

### 3. Onboarding Friction
Specific difficulties during setup or first value realization.

**Indicators:**
- "Setup was confusing..."
- "Took us X weeks to..."
- "Couldn't figure out how to..."
- "Documentation unclear on..."

**Extract:**
- What step caused friction?
- How long did it take?
- Was it eventually resolved?
- Suggestions for improvement?

### 4. Integration Gaps
Missing connectors or data sync capabilities.

**Indicators:**
- "We use [Tool X] but can't connect..."
- "Data sync with [Platform Y]..."
- "Export to [System Z]..."

**Extract:**
- What integration is needed?
- What data needs to flow?
- Current workaround (if any)?
- Business impact of gap?

### 5. Performance Needs
Speed, scale, or reliability requirements.

**Indicators:**
- "Too slow when..."
- "Times out on..."
- "Can't handle X records..."
- "Need real-time..."

**Extract:**
- What operation is slow?
- Current performance vs. needed?
- Scale requirements?
- Impact on usage?

## Synthesis Process

### 1. Determine Time Window

**Inputs:**
- `days`: Explicit lookback window (e.g., 7, 14, 30)
- `last_run`: Timestamp from state file (e.g., `datasets/product/.meetings-to-backlog-state.json`)
- Default: 3 days if no inputs provided

**Calculate cutoff date:**
```
If days provided:
  cutoff_date = current_date - days
Else if last_run exists:
  cutoff_date = last_run timestamp
Else:
  cutoff_date = current_date - 3 days
```

### 2. Collect Meeting Files

**Scan paths:**
```
datasets/meetings/Customers/**/YYYY/*.md  (where date >= cutoff_date)
datasets/meetings/Internal/Product/YYYY/*.md  (where date >= cutoff_date)
```

**Use Glob to find files:**
```
Glob pattern: datasets/meetings/Customers/**/2025/*.md
Glob pattern: datasets/meetings/Internal/Product/2025/*.md
```

**Filter by date:**
- Extract date from filename (YYYY-MM-DD prefix)
- Compare to cutoff_date
- Keep only files >= cutoff_date

### 3. Extract Signals from Each Meeting

**For each meeting file:**

**A. Parse frontmatter:**
```yaml
date: "YYYY-MM-DD"
type: "sales|product|customersuccess|..."
customer: "Company Name"
participants: ["Person A", "Person B"]
tags: ["2025Q3", "keyword"]
```

**B. Read sections:**
- `## ⬇️ AI Summary` → High-level signals
- `## ⬇️ Action Items` → Commitments and follow-ups
- `## ⬇️ Full Transcript` → Detailed context and quotes

**C. Identify signal candidates:**
Use pattern matching:
```
Feature requests: grep -i "we need\|can you\|would be great\|want to" transcript
Pain points: grep -i "frustrat\|struggle\|difficult\|problem\|issue" transcript
Onboarding: grep -i "setup\|onboard\|getting started\|first" transcript
Integrations: grep -i "integrat\|connect\|sync\|export" transcript
Performance: grep -i "slow\|timeout\|performance\|scale" transcript
```

**D. Extract verbatim quotes:**
- Capture 1-3 sentence snippets around signal indicators
- Preserve exact wording for evidence
- Include speaker attribution if available

**E. Record metadata:**
For each signal:
```
{
  "signal_text": "Verbatim quote or paraphrase",
  "signal_type": "ask|problem|friction|integration|performance",
  "customer": "Company Name",
  "date": "YYYY-MM-DD",
  "meeting_type": "sales|product|customersuccess",
  "source_file": "/path/to/meeting.md",
  "section": "AI Summary|Action Items|Full Transcript"
}
```

### 4. Cluster Signals

**Semantic clustering:**
- Group similar signals across customers
- Identify common themes
- Label clusters with action-style names (Verb + Object + Outcome)

**Examples:**
- "Revamp onboarding to reduce TTFV" (multiple onboarding friction signals)
- "Add Google Sheets export capability" (multiple export/integration requests)
- "Improve dashboard load performance" (multiple performance complaints)

**For each cluster:**
```
{
  "cluster_label": "Action-style theme name",
  "mention_count": N,  # Total signal occurrences
  "unique_accounts": N,  # Distinct customers
  "unique_functions": N,  # Customer vs. internal sources
  "signals": [array of signal objects],
  "recentness_weight": calculated_score  # Newer = higher
}
```

### 5. Compute Signal Metrics

**For each cluster:**

**A. Mention count:**
Total occurrences across all meetings.

**B. Unique accounts:**
Distinct customer names in signal sources.

**C. Unique functions:**
Count of different source types:
- External customers
- Internal product team
- Partner/agency feedback

**D. Recentness weight:**
```
For each signal in cluster:
  days_ago = current_date - signal.date
  recentness_score = max(0, 30 - days_ago) / 30  # Linear decay over 30 days
Average recentness across all signals in cluster
```

**E. Source diversity:**
Mix of meeting types:
- Sales calls
- Product feedback sessions
- Customer success check-ins
- Onboarding calls

Higher diversity = stronger signal.

### 6. Output Synthesized Data

**Return structured object:**
```
{
  "time_window": {
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "days_scanned": N,
    "meetings_processed": N
  },
  "clusters": [
    {
      "label": "Cluster name",
      "mention_count": N,
      "unique_accounts": N,
      "unique_functions": N,
      "recentness_weight": 0.0-1.0,
      "source_diversity": 0.0-1.0,
      "signals": [
        {
          "text": "Quote or paraphrase",
          "customer": "Company",
          "date": "YYYY-MM-DD",
          "meeting_type": "...",
          "source_file": "..."
        }
      ]
    }
  ],
  "raw_signals": [all unclustered signals for reference]
}
```

## Filtering and Scoping

### Customer Filter

**Input:** `include_customers` (comma-separated list)

**Behavior:**
- If provided: Only process meetings where `customer` field matches list
- If not provided: Process all customers

**Example:**
```
include_customers: "PrettyBoy,CompoundStudio,Joy Organics"
→ Only synthesize signals from these three customers
```

### Function Filter

**Input:** `include_internal_functions` (comma-separated list)

**Behavior:**
- If provided: Only process internal meetings from specified functions
- Functions: Product, CS, Sales, Marketing, Ops

**Example:**
```
include_internal_functions: "Product,CS"
→ Process internal Product and CS meetings, skip Sales/Marketing/Ops
```

### Signal Thresholds

**Input filters:**
- `min_mentions`: Minimum total mentions to qualify (default: 1)
- `min_sources`: Minimum distinct sources (customers/functions) to qualify (default: 1)

**Application:**
After clustering, filter out clusters that don't meet thresholds:
```
Keep cluster if:
  cluster.mention_count >= min_mentions AND
  cluster.unique_accounts + cluster.unique_functions >= min_sources
```

### Type Exclusions

**Input:** `exclude_types` (comma-separated list)

**Behavior:**
Ignore signals matching certain categories.

**Default exclusions:**
```
exclude_types: "bugs,housekeeping"
```

**Examples:**
- "bugs": Bug reports (should go to issue tracker, not epics)
- "housekeeping": Internal cleanup tasks
- "research": Exploratory ideas (not ready for roadmap)

## Integration with Workflows

### Product Planning Integration

**Invoked by:**
- `product-planning` workflow

**Inputs:**
- Time window (days or last_run)
- Customer filter (optional)
- Function filter (optional)
- Thresholds (min_mentions, min_sources)

**Outputs:**
- Clustered signals ready for epic creation
- Evidence for epic "Why now" sections
- Customer quotes for epic proposals

### CS Prep Integration

**Invoked by:**
- `cs-prep` workflow

**Inputs:**
- Specific customer name
- Time window (typically 30-90 days for QBR prep)

**Outputs:**
- Customer-specific signal history
- Pain points and friction areas
- Feature requests and timeline
- Quotes for QBR discussion

### Strategy Session Integration

**Invoked by:**
- `strategy-session` workflow

**Inputs:**
- Time window (often broader, e.g., 90 days)
- Optional topic filter

**Outputs:**
- Cross-customer patterns
- Market trends from customer feedback
- Evidence for strategic decisions

## Success Criteria

Meeting synthesis complete when:
- All meetings in time window processed
- Signals extracted and categorized
- Clustering applied (semantic grouping)
- Metrics computed (mentions, accounts, recency)
- Output structured for consuming workflows
- Verbatim quotes preserved for evidence

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Paraphrasing customer quotes | Preserve verbatim text for accuracy |
| Ignoring meeting date filters | Respect cutoff_date strictly |
| Missing signal categorization | Tag each signal as ask/problem/friction/etc. |
| Not recording source file paths | Track every signal back to source meeting |
| Skipping semantic clustering | Group similar signals for pattern detection |

## Related Skills

- **meeting-schema-validation**: Validates meetings before synthesis
- **priority-scoring**: Uses synthesis output for epic prioritization
- **product-planning**: Primary consumer of synthesis output

## Anti-Rationalization Blocks

Common excuses that are **explicitly rejected**:

| Rationalization | Reality |
|----------------|---------|
| "Close enough" on quotes | Preserve exact wording or mark as paraphrase. |
| "Skip old meetings" | Process all meetings in time window. |
| "This signal doesn't fit categories" | Categorize as best match or flag as uncategorized. |
| "Single mention isn't worth tracking" | Track all signals, filter by thresholds later. |
