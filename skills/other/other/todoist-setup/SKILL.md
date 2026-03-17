---
name: todoist-setup
description: Connect Todoist to Dex for two-way task sync
integration:
  id: todoist
  name: Todoist
  mcp_server: todoist-mcp
  auth: api_key
  enhances:
    - skill: daily-plan
      capability: "Merges Todoist tasks due today alongside Dex tasks"
    - skill: triage
      capability: "Routes items to Dex, Todoist, or both"
    - skill: process-inbox
      capability: "Creates tasks in both systems when processing captured items"
    - skill: week-review
      capability: "Shows cross-system completion stats (Dex + Todoist)"
  new_capabilities:
    - name: Bidirectional task sync
      trigger: "Automatic at daily plan and task creation touchpoints"
  sync:
    direction: bidirectional
    entities: tasks
---

# Todoist Setup

Connect your Todoist account to Dex so tasks stay in sync across both systems. Create a task in Dex and it appears in Todoist. Complete one in Todoist and Dex knows about it.

## What This Enables

Once connected, Dex can:
- **Daily Plan** (`/daily-plan`): Merge Todoist tasks due today alongside your Dex tasks
- **Triage** (`/triage`): Route new items to Dex, Todoist, or both
- **Process Inbox** (`/process-inbox`): Same routing options when processing captured items
- **Week Review** (`/week-review`): See completion stats across both Dex and Todoist

## How Sync Works (Plain English)

- When you create a task in Dex, it gets pushed to Todoist automatically
- When you complete a task in Todoist, Dex picks it up during your next daily plan
- Task titles, priorities, and completion status travel between both systems
- Each system keeps its own copy — if one goes offline, the other still works
- Sync happens at natural touchpoints (daily plan, triage) — not constantly in the background
- Tasks created by Dex carry a `[dex:task-ID]` marker in the description so the systems never duplicate

## Privacy

- Task titles and status sync between Dex and Todoist. No task content or notes are stored beyond what you already have in both systems.
- Your API key stays local on your machine in `System/integrations/config.yaml` (gitignored)
- Dex never shares your Todoist data with third parties
- Tasks created in Todoist are only pulled into Dex if they were NOT originally pushed from Dex (loop prevention via `[dex:...]` marker)

## When to Run

- User types `/todoist-setup`
- User asks about connecting Todoist or task sync
- User wants Todoist tasks in daily plans
- During `/integrate-mcp` if Todoist is mentioned

---

## Setup Flow

### Step 1: Check if Already Connected

1. Check `System/integrations/config.yaml` for a `todoist:` section with `enabled: true`
2. If enabled, test the connection by listing projects with the stored API key
3. If healthy, skip to **Reconfiguration** section below
4. If not configured or unhealthy, continue to Step 2

### Step 2: Explain What We're Setting Up

Say:

```
**Let's connect Todoist to Dex.**

Two-way task sync. Create in Dex — appears in Todoist. Complete in Todoist — done in Dex.

**What you'll need:**
- Your Todoist API token (I'll show you where to find it)
- About 2 minutes

**Ready to go?**
```

Wait for confirmation.

### Step 3: Get the API Key

Guide the user:

```
To get your Todoist API token:

1. Open Todoist (web or app)
2. Go to **Settings** → **Integrations** → **Developer**
3. Copy the **API token** shown there

Paste it here when you have it.
```

Wait for the user to provide their API key. Validate it's a non-empty string (Todoist API tokens are typically 40-character hex strings).

### Step 4: Add MCP Server to Config

Check the user's MCP configuration. If `todoist-mcp` is not listed:

1. Explain:

```
I'll add the Todoist connector to your configuration.
This lets Dex talk to Todoist using your API token.
```

2. Add to the user's `.mcp.json` (use the `/dex-add-mcp` skill or manual edit):

```json
{
  "todoist-mcp": {
    "command": "npx",
    "args": ["-y", "todoist-mcp-server"],
    "env": {
      "TODOIST_API_KEY": "<user's API key>"
    }
  }
}
```

3. Tell the user the MCP server needs to restart for changes to take effect.

### Step 5: Test the Connection

Use the API key to list projects as a connectivity test. Run a curl or use the MCP server:

```bash
curl -s -H "Authorization: Bearer $API_KEY" https://api.todoist.com/rest/v2/projects
```

**If projects load successfully:**

```
Connected! I can see your Todoist projects:

1. Inbox
2. Work
3. Personal
...

Looking good!
```

**If it fails:**

```
That API key didn't work. A few things to check:

1. **Copy the full key** — it should be about 40 characters
2. **Check for extra spaces** before or after the key
3. **Regenerate the key** in Todoist Settings → Integrations → Developer

Want to try again?
```

Retry up to 2 times, then offer to skip and come back later.

### Step 6: Choose Default Project

Ask the user which Todoist project should receive Dex tasks:

```
**Which Todoist project should Dex tasks go into?**

Your projects:
1. Inbox
2. Work
3. Personal
...

You can pick one default project, or map each Dex pillar to a different project.

**Option A:** All Dex tasks go to one project (simplest)
**Option B:** Map each pillar to a project:
  - Deal Support → [project]
  - Thought Leadership → [project]
  - Product Feedback → [project]

Which works for you?
```

Save their choices for the config file.

### Step 7: Trust Level

Ask about sync autonomy — **never use the word "tier"** (per integration-patterns.md):

```
**How hands-on do you want to be with task sync?**

1. **"Show me first"** — I'll preview changes before syncing (recommended to start)
2. **"Keep them in sync"** — Tasks auto-sync both ways, silently
3. **"Only pull in"** — Import tasks from Todoist but don't push back
```

Map their choice to config values:
- **Show me first** → `trust_level: confirm_each`
- **Keep them in sync** → `trust_level: autonomous`
- **Only pull in** → `trust_level: read_only`

### Step 8: Save Configuration

Write to `System/integrations/config.yaml` — update the todoist section:

```yaml
todoist:
  enabled: true
  configured_at: YYYY-MM-DD
  mcp_server: todoist-mcp
  auth_type: api_key
  api_key: <user's API key>
  task_sync: true
  trust_level: <confirm_each | autonomous | read_only>
  project: <default project name>
  pillar_map:
    deal_support: <project name or omit>
    thought_leadership: <project name or omit>
    product_feedback: <project name or omit>
  sync_labels: []
  auto_sync: true
  features:
    task_sync: true
    external_task_merge: true
```

If the file already exists, only update the `todoist:` section. Preserve other integration configs.

### Step 9: Capability Cascade

Read the integration manifest from this skill's frontmatter. Present:

```
**Todoist is connected!** Here's what just changed:

### Enhanced (existing skills that got smarter)

- **`/daily-plan`** → Merges Todoist tasks due today alongside your Dex tasks.
  Externally-created tasks show a [Todoist] label so you know where they came from.

- **`/triage`** → Now offers routing to Dex, Todoist, or both when processing items.

- **`/process-inbox`** → Same routing — "This looks like a task. Add to Dex, Todoist, or both?"

- **`/week-review`** → Shows completion stats across both systems so you see the full picture.

### New Superpowers

- Bidirectional task sync — automatic at daily plan and task creation touchpoints.

### How It Works

- **Reading:** Todoist tasks appear in your daily plan automatically
- **Writing:** [trust level description based on user's choice above]
- **Privacy:** Task titles and status sync. Your API key stays local. No data shared with third parties.

These work automatically starting now. Run `/dex-level-up` anytime to see what else you can do.
```

---

## Troubleshooting

### API Key Invalid or Expired

Todoist API keys don't expire unless you regenerate them. If you see auth errors:

1. Go to Todoist Settings → Integrations → Developer
2. Copy the current API token (or regenerate if needed)
3. Update the key by running `/todoist-setup` again

### Tasks Not Syncing

A few possibilities:
- **Sync only happens at touchpoints** — during `/daily-plan`, task creation, or `/triage`. There's no background sync.
- **Check the project mapping** — if your Dex pillar maps to a project that was renamed or deleted in Todoist, tasks may go to the Inbox instead.
- **Rate limits** — Todoist allows 450 requests per minute. The adapter handles 429 responses with automatic retry, so this is almost never an issue.

### Wrong Project

If tasks are landing in the wrong Todoist project:
1. Run `/todoist-setup` again
2. Update the pillar-to-project mapping
3. Existing tasks won't move — only new tasks use the updated mapping

### Duplicate Tasks

If you see duplicates, check:
- **Dex-originated tasks** should have `[dex:task-...]` in their Todoist description. The adapter skips these during pull-in to prevent loops.
- **Todoist-originated tasks** that you manually add to Dex won't have a mapping in `.sync-state.json` and may get pulled again. Mark them in Dex to create the mapping.

### "Todoist MCP not found"

The Todoist adapter uses direct API calls (not MCP) for the sync bridge. The MCP server is optional but enhances other skills. Re-run `/todoist-setup` to detect and fix configuration.

---

## Reconfiguration

If the user runs `/todoist-setup` when already configured:

1. Check current config from `System/integrations/config.yaml`
2. Test the existing API key with a project list call
3. Show current mapping and trust level
4. Offer options:
   - Update project mapping
   - Change sync behavior (trust level)
   - Update API key
   - Disconnect Todoist

### Disconnect Flow

If user wants to disconnect:

1. Update `System/integrations/config.yaml`:
   ```yaml
   todoist:
     enabled: false
   ```
2. Confirm: "Todoist is disconnected. Tasks will no longer sync between systems. Your existing tasks in both Dex and Todoist are unchanged. Run `/todoist-setup` anytime to reconnect."
