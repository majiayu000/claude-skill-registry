---
name: research-capture
description: "Captures research insights, decisions, and learnings during development. Use after completing spikes, making architectural decisions, or discovering important patterns. Prompts for context and rationale, stores with embeddings for later semantic retrieval. Do NOT use for trivial notes - this is for significant findings worth surfacing later."
context: fork
---

# Research Capture

## Overview

Capture and index research insights during development for later semantic retrieval. Creates structured entries with context, rationale, and alternatives considered.

**Core principle:** Capture decisions and learnings while context is fresh.

**Trigger:** After spikes, architectural decisions, significant discoveries, end of investigation

## Entry Types

| Type       | Use For                        | Examples                                                |
| ---------- | ------------------------------ | ------------------------------------------------------- |
| `decision` | Architectural/design choices   | "Use Redis for sessions", "Chose Hono over Express"     |
| `finding`  | Discoveries during development | "Stripe webhook timing issue", "Race condition in auth" |
| `learning` | Knowledge gained               | "Astro hydration quirks", "CORS preflight gotchas"      |
| `spike`    | Investigation results          | "Evaluated 3 auth providers", "Benchmarked DB options"  |

## Capture Flow

### Step 1: Determine Entry Type

```
Use AskUserQuestion tool with:
- question: "What type of research entry is this?"
- header: "Entry Type"
- options:
  1. label: "Decision"
     description: "Architectural or design choice made"
  2. label: "Finding"
     description: "Discovery or insight during development"
  3. label: "Learning"
     description: "Knowledge or best practice learned"
  4. label: "Spike"
     description: "Investigation or evaluation results"
- multiSelect: false
```

### Step 2: Gather Content

Prompt user for:

```markdown
## Research Entry

**Title:** [Clear, searchable title]

**Context:**
What prompted this research? What problem were you solving?

**Content:**
What was discovered/decided? Include specifics.

**Rationale:**
Why this conclusion? What factors influenced the decision?

**Alternatives Considered:** (if applicable)
What else was evaluated? Why were they rejected?

**References:** (optional)

- Issue/PR numbers
- Documentation links
- Related entries
```

### Step 3: Auto-detect Context

Gather from current session:

```python
# Current git context
branch = get_current_branch()
recent_commits = get_recent_commits(limit=3)

# Related issues
related_issues = extract_issue_refs(content)

# Current project
project = get_project_name()

# Tags from content
suggested_tags = extract_keywords(title + content)
```

### Step 4: Confirm Tags

```
Use AskUserQuestion tool with:
- question: "Confirm tags for this entry (suggested based on content):"
- header: "Tags"
- options:
  1. label: "{suggested_tag_1}"
     description: "Auto-detected from content"
  2. label: "{suggested_tag_2}"
     description: "Auto-detected from content"
  3. label: "{suggested_tag_3}"
     description: "Auto-detected from content"
  4. label: "Add custom tags"
     description: "Specify your own tags"
- multiSelect: true
```

### Step 5: Generate and Store

```python
import json
import os
from datetime import datetime
from uuid import uuid4

def create_research_entry(entry_type, title, content, context, rationale, alternatives, tags, project, references):
    # Generate ID
    index = load_index()
    next_num = len(index.get('entries', [])) + 1
    entry_id = f"r{next_num:03d}"

    # Create entry
    entry = {
        "id": entry_id,
        "type": entry_type,
        "title": title,
        "content": content,
        "context": context,
        "rationale": rationale,
        "alternatives": alternatives or [],
        "tags": tags,
        "project": project,
        "createdAt": datetime.utcnow().isoformat() + "Z",
        "updatedAt": datetime.utcnow().isoformat() + "Z",
        "references": references or [],
        "relatedEntries": []
    }

    # Ensure directory exists
    os.makedirs(".claude/research/entries", exist_ok=True)

    # Save entry
    with open(f".claude/research/entries/{entry_id}.json", "w") as f:
        json.dump(entry, f, indent=2)

    # Update index
    update_index(entry)

    return entry_id
```

### Step 6: Generate Embedding (if cloud available)

```python
def embed_entry(entry):
    """Generate and store embedding for semantic search."""
    # Combine searchable content
    text = f"{entry['title']}\n{entry['content']}\n{entry.get('rationale', '')}"

    # Check for cloud API
    api_key = os.environ.get('POPKIT_API_KEY')
    if not api_key:
        return None

    # Generate embedding via cloud
    try:
        response = requests.post(
            "https://api.thehouseofdeals.com/v1/embeddings",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "text": text,
                "id": entry['id'],
                "type": "research",
                "metadata": {
                    "title": entry['title'],
                    "type": entry['type'],
                    "tags": entry['tags'],
                    "project": entry['project']
                }
            }
        )
        if response.ok:
            return response.json().get('embeddingId')
    except Exception as e:
        print(f"Embedding failed (offline mode): {e}")

    return None
```

## Storage Structure

```
.claude/
  research/
    index.json              # Master index
    entries/
      r001.json             # Individual entries
      r002.json
      ...
```

### index.json Schema

```json
{
  "version": "1.0.0",
  "lastUpdated": "2024-12-09T10:30:00Z",
  "entries": [
    {
      "id": "r001",
      "type": "decision",
      "title": "Use Redis for session storage",
      "tags": ["auth", "infrastructure"],
      "project": "popkit-cloud",
      "createdAt": "2024-12-09T10:30:00Z",
      "embeddingId": "vec_r001"
    }
  ],
  "tagIndex": {
    "auth": ["r001", "r015"],
    "infrastructure": ["r001"]
  },
  "projectIndex": {
    "popkit-cloud": ["r001", "r002"]
  }
}
```

## Integration Points

### Session Capture Integration

At end of session, `pop-session-capture` prompts:

```
Use AskUserQuestion tool with:
- question: "Any research insights to capture from this session?"
- header: "Research"
- options:
  1. label: "Yes, capture insights"
     description: "Record decisions, findings, or learnings"
  2. label: "No, nothing to capture"
     description: "Skip research capture"
- multiSelect: false
```

If yes, invoke `pop-research-capture` skill.

### Dev Workflow Integration

When starting work on an issue (`/popkit:dev work #N`):

```python
def surface_related_research(issue_keywords):
    """Search for related research entries."""
    # Local search
    index = load_index()
    matches = []

    for entry in index['entries']:
        if any(kw.lower() in entry['title'].lower() for kw in issue_keywords):
            matches.append(entry)

    # Semantic search (if cloud available)
    if os.environ.get('POPKIT_API_KEY'):
        semantic_matches = semantic_search(issue_keywords)
        matches.extend(semantic_matches)

    return dedupe_by_id(matches)[:5]
```

Display to user:

```
Found related research:
- [decision] Use Redis for session storage (r001)
- [finding] JWT refresh token race condition (r015)

View with /popkit:research show <id>
```

### Code Review Integration

During review, check for conflicts with documented decisions:

```python
def check_decision_conflicts(changed_files, changes_summary):
    """Flag potential conflicts with documented decisions."""
    decisions = [e for e in load_index()['entries'] if e['type'] == 'decision']

    conflicts = []
    for decision in decisions:
        # Simple keyword matching (enhanced by embeddings in cloud)
        if overlaps(decision['tags'], changed_files):
            conflicts.append({
                'decision': decision,
                'reason': f"Changes to {changed_files} may affect '{decision['title']}'"
            })

    return conflicts
```

## Example Entries

### Decision Entry

```json
{
  "id": "r001",
  "type": "decision",
  "title": "Use Redis for session storage",
  "content": "We chose Redis (via Upstash) for storing session tokens...",
  "context": "Evaluating session storage for auth system",
  "rationale": "Redis provides native TTL, sub-ms latency, serverless-compatible",
  "alternatives": ["PostgreSQL sessions", "JWT-only", "Memcached"],
  "tags": ["auth", "infrastructure", "redis"],
  "project": "popkit-cloud",
  "references": ["#68", "https://upstash.com/docs/redis/"]
}
```

### Finding Entry

```json
{
  "id": "r015",
  "type": "finding",
  "title": "JWT refresh token race condition",
  "content": "Discovered that concurrent refresh requests can invalidate each other...",
  "context": "Debugging intermittent auth failures",
  "rationale": "First refresh succeeds, second uses stale token",
  "tags": ["auth", "security", "race-condition"],
  "project": "popkit-cloud"
}
```

### Spike Entry

```json
{
  "id": "r004",
  "type": "spike",
  "title": "Evaluate email providers for transactional email",
  "content": "Compared Resend, SendGrid, Postmark, and AWS SES...",
  "context": "Need transactional email for auth and billing",
  "rationale": "Resend: best DX, fair pricing, good deliverability",
  "alternatives": [
    { "name": "SendGrid", "reason": "Complex API, overkill for our needs" },
    { "name": "AWS SES", "reason": "Requires more setup, region restrictions" },
    { "name": "Postmark", "reason": "Great but more expensive" }
  ],
  "tags": ["email", "infrastructure", "comparison"],
  "project": "popkit-cloud"
}
```

## When to Capture

**DO capture:**

- Architectural decisions with trade-offs
- Non-obvious findings that took time to discover
- Investigation results (spikes)
- Learnings that will help future development
- Decisions that could be questioned later

**DON'T capture:**

- Trivial fixes or obvious patterns
- Temporary workarounds (use TODO comments instead)
- Things already documented elsewhere
- Personal preferences without rationale

## Output

After successful capture:

```
Research entry captured:

ID: r001
Type: decision
Title: Use Redis for session storage
Tags: auth, infrastructure, redis
Project: popkit-cloud

Embedding: Generated (cloud sync enabled)

Use /popkit:research show r001 to view
Use /popkit:research search "..." to find later
```

## Related Skills

| Skill                 | Relationship                           |
| --------------------- | -------------------------------------- |
| `pop-session-capture` | Prompts for research at session end    |
| `pop-brainstorming`   | May generate decisions worth capturing |
| `pop-writing-plans`   | Plans may reference research entries   |
| `pop-code-review`     | Checks against documented decisions    |
