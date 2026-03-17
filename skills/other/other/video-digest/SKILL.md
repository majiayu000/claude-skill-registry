---
name: video-digest
context: orchestrate
description: Triage new videos, generate watch recommendations
model: opus
hooks:
  Stop:
    - type: command
      command: >-
        test -f "Daily/$(date +%Y)/Daily - $(date +%Y-%m-%d).md" &&
        grep -q "## Video Digest" "Daily/$(date +%Y)/Daily - $(date +%Y-%m-%d).md"
      statusMessage: "Verifying digest in daily note"
---

# /video-digest

Intelligently triage new videos from subscribed YouTube channels, process selectively based on relevance, and generate a daily digest with watch recommendations.

## Usage

```
/video-digest                    # Full triage and processing
/video-digest --triage-only      # Score videos without processing
/video-digest --report           # Show current queue status
/video-digest --watched <video>  # Mark video as watched (removes from queue)
```

## Examples

```
/video-digest
/video-digest --triage-only
/video-digest --watched "YouTube - AI Security Patterns"
```

## Model Strategy

| Phase             | Model  | Rationale                |
| ----------------- | ------ | ------------------------ |
| RSS fetch         | Haiku  | Simple data extraction   |
| Title/desc triage | Haiku  | Fast relevance scoring   |
| Worth Processing  | Sonnet | Full transcript analysis |
| Quick Capture     | Haiku  | Brief summary only       |
| Digest generation | Sonnet | Quality recommendations  |

## Instructions

### Phase 1: Gather New Videos

**Model:** Haiku (parallel subagents)

1. **Read subscriptions** from `.claude/subscriptions.yaml`

2. **For each channel** (in parallel), fetch RSS feed:

   ```
   https://www.youtube.com/feeds/videos.xml?channel_id={{channel_id}}
   ```

   Use `WebFetch` with prompt: "Extract video entries: title, video_id, published_date, description (first 500 chars)"

3. **Identify new videos**:
   - Compare video IDs against `last_video_id`
   - Select videos published since last check
   - If first check, take only most recent video

4. **Collect candidates** with basic metadata:
   - video_id, title, description, duration (if available)
   - channel_name, channel_trust_score, always_watch

### Phase 2: Rapid Triage

**Model:** Haiku

For each candidate video, compute triage score:

#### Scoring Algorithm

```
TRParentCorpE_SCORE = (
    PROJECT_RELEVANCE * 0.35 +    # 0-100
    DOMAIN_RELEVANCE * 0.25 +     # 0-100
    FRESHNESS_BOOST * 0.20 +      # 0-100
    CHANNEL_TRUST * 0.20          # 0-100 (from trust_score * 5)
)
```

#### Relevance Matching

**Project Relevance** (read `.claude/context/projects.md`):

Match title + description against project keywords:

| Project      | Keywords                                                       |
| ------------ | -------------------------------------------------------------- |
| Beta         | ERPSystem, MRO, Swiss-AS, EWS, modernisation, aviation, maintenance |
| Alpha       | SAP, DataPlatform, data products, Kafka, Datasphere, integration       |
| AlertHub    | AWS Bedrock, AI agents, safety, incident, LLM, Claude          |
| Delta         | AircraftMfg, Gatelink, EFB, aircraft, AvionicsVendor, avionics             |
| Cyber Uplift | security, IAM, compliance, LLD, AWS security, threat           |
| DataPlatform         | data platform, Snowflake, analytics, data engineering          |

**Domain Relevance** (read `.claude/rules/tag-taxonomy.md` `domain/` section):

Match against domain keywords:

- `domain/engineering`: systems, architecture, design, modernisation
- `domain/data`: analytics, data products, streaming, Kafka, databases
- `domain/cloud`: AWS, Azure, infrastructure, serverless, containers
- `domain/security`: IAM, encryption, compliance, threats, vulnerabilities
- `domain/ai`: LLM, agents, machine learning, Claude, GPT, automation

**Freshness Boost**:

- Check if topic keywords appear in notes modified in last 14 days
- Higher score = more recently active topics
- Use Graph search: `node .claude/scripts/graph-query.js --search="<keywords>" --since=$(date -v-14d +%Y-%m-%d) --json`

**Channel Trust**:

- Use `trust_score` from subscriptions.yaml (0-20, default 10)
- Scale to 0-100 by multiplying by 5

#### Boost Keywords

Apply additional boosts from `triage_settings.boost_keywords`:

```yaml
boost_keywords:
  - keyword: "architecture"
    boost: 10
  - keyword: "Claude Code"
    boost: 15
```

#### Never Process Keywords

Skip videos containing `triage_settings.never_process_keywords`:

```yaml
never_process_keywords:
  - "reaction"
  - "drama"
  - "podcast"
  - "unboxing"
```

#### Duration Filtering

Skip videos outside `minimum_duration` / `maximum_duration` thresholds.

#### Category Assignment

| Category         | Score Range | Action                       |
| ---------------- | ----------- | ---------------------------- |
| Must Watch       | 80-100      | Flag for user with reasoning |
| Worth Processing | 50-79       | Full `/youtube` processing   |
| Quick Capture    | 25-49       | Weblink only, brief summary  |
| Skip             | 0-24        | Log reason, no files created |

### Phase 3: Selective Processing

**Model:** Sonnet (parallel for Worth Processing tier)

#### Must Watch (80-100)

**Do NOT process automatically.** Instead:

1. **Update video queue** (`.claude/video-queue.yaml`):

   ```yaml
   must_watch:
     - video_id: "abc123"
       title: "Video Title"
       url: "https://youtube.com/watch?v=abc123"
       channel: "Channel Name"
       score: 92
       first_recommended: "2026-02-05T08:00:00Z"
       always_watch_channel: false
       reasoning:
         - "Directly relevant to [[Project - AlertHub]] - discusses AI agent security"
         - "Knowledge gap: No vault content on 'AI firewall' patterns"
         - "Channel trust: 2.8 nodes/video historical yield"
       potential_nodes: 4
   ```

2. **Include in digest** with full reasoning

#### Worth Processing (50-79)

Launch parallel `/youtube` processing:

1. For each video in this tier, invoke `/youtube <url>`:
   - Follow full `/youtube` skill workflow
   - Create YouTube node with transcript analysis
   - Spawn Concept/Pattern nodes as appropriate

2. **Track results**:
   - Count spawned nodes
   - Update `processing_stats` in subscriptions.yaml

#### Quick Capture (25-49)

**Model:** Haiku

Create minimal Weblink note:

**Filename:** `Weblink - {{sanitised title}}.md`

```markdown
---
type: Reference
title: "{{title}}"
url: "{{youtube_url}}"
domain: youtube.com
createdAt: "{{ISO timestamp}}"
description: "{{brief summary from description}}"
created: { { DATE } }
modified: { { DATE } }
tags:
  - video
  - activity/research

relatedTo: []
---

# {{title}}

**Channel:** {{channel name}}
**Duration:** {{duration}}
**Source:** [Watch on YouTube]({{url}})

## Summary

{{2-3 sentence summary based on title and description}}

## Relevance

Quick captured due to moderate relevance (score: {{score}}/100).

_Full processing not warranted based on triage criteria._
```

#### Skip (0-24)

Log to digest only. No files created.

### Phase 4: Queue Management

#### Check Must Watch Expiry

1. Read `.claude/video-queue.yaml`
2. For each video in `must_watch`:
   - If `always_watch_channel: true` → Keep in must_watch
   - If age > `must_watch_expiry_days` (default 5) → Move to `backlog`

3. Update queue file with moves

#### Backlog Structure

```yaml
backlog:
  - video_id: "ghi789"
    title: "Older Video"
    url: "https://youtube.com/watch?v=ghi789"
    channel: "Some Channel"
    expired_from_must_watch: "2026-02-05"
    original_score: 85
    reasoning:
      - "Was relevant to [[Project - Beta]]"
```

### Phase 5: Generate Digest

**Model:** Sonnet

Add `## Video Digest` section to today's daily note.

1. **Find daily note**: Check both formats:
   - `Daily/{{year}}/{{YYYY-MM-DD}}.md` (actual format used)
   - `Daily/{{year}}/Daily - {{YYYY-MM-DD}}.md` (documented format)
2. **Create if missing**: Use `/daily` skill
3. **Insert digest section** (before `## End of Day Review` if present, otherwise at end)

#### Digest Template

```markdown
## Video Digest

_Generated at {{timestamp}}_

### 📊 Summary

| Category         | Count | Action                       |
| ---------------- | ----- | ---------------------------- |
| Must Watch       | {{n}} | Review recommendations below |
| Worth Processing | {{n}} | Auto-processed               |
| Quick Capture    | {{n}} | Weblink created              |
| Skipped          | {{n}} | Not relevant                 |

### 🎯 Must Watch

{{For each must-watch video:}}

#### [[YouTube - {{title}}]] _(not yet created)_

**Channel:** {{channel}} | **Duration:** {{duration}} | **Score:** {{score}}/100

**Why watch:**
{{For each reasoning point:}}

- {{reasoning}}

**If skipped:** Will extract ~{{potential_nodes}} concepts including {{top concepts}}

---

### ✅ Auto-Processed

| Video | Channel | Score | Nodes Created |
| ----- | ------- | ----- | ------------- |

{{For each processed video:}}
| [[YouTube - {{title}}]] | {{channel}} | {{score}} | {{nodes_count}} |

### 📎 Quick Captures

{{For each quick capture:}}

- [[Weblink - {{title}}]] - {{brief reason}}

### ⏭️ Skipped

| Video | Channel | Reason |
| ----- | ------- | ------ |

{{For each skipped video:}}
| "{{title}}" | {{channel}} | {{skip_reason}} |

{{If backlog not empty:}}

### ⏳ When You Get Time (Backlog)

Videos that expired from Must Watch after {{expiry_days}} days:

| Video | Channel | Original Score | Days in Queue |
| ----- | ------- | -------------- | ------------- |

{{For each backlog video:}}
| [[YouTube - {{title}}]] | {{channel}} | {{score}} | {{days}} |
```

### Phase 6: Update State

1. **Update subscriptions.yaml**:
   - Set `last_checked` to current timestamp
   - Set `last_video_id` to most recent video per channel
   - Increment `processing_stats` counters

2. **Update video-queue.yaml**:
   - Add new must-watch videos
   - Move expired videos to backlog
   - Remove watched videos (via `--watched` flag)

## Handling --watched Flag

When invoked as `/video-digest --watched <video>`:

1. Parse video identifier (title or video_id)
2. Search `must_watch` and `backlog` in queue
3. Remove matching entry
4. Confirm removal

## Handling --report Flag

When invoked as `/video-digest --report`:

1. Read `.claude/video-queue.yaml`
2. Display summary:

```
Video Queue Status
==================

Must Watch: {{count}}
{{For each:}}
  - "{{title}}" ({{channel}}) - Score: {{score}} - {{days_old}} days old

Backlog: {{count}}
{{For each:}}
  - "{{title}}" ({{channel}}) - Expired {{days_ago}} days ago

Last Digest: {{timestamp}}
```

## Handling --triage-only Flag

When invoked as `/video-digest --triage-only`:

- Execute Phases 1-2 only
- Output scoring results without processing
- Do not update subscriptions.yaml (except last_checked)
- Useful for testing triage algorithm

## Quality Standards

- **Always** generate digest in daily note
- **Always** provide reasoning for must-watch recommendations
- **Always** update queue state after execution
- **Never** process must-watch automatically (user should decide)
- **Never** create duplicate YouTube nodes for already-processed videos
- **Use** UK English throughout
- **Update** subscriptions.yaml after every run
- **Track** spawned nodes for trust score calibration

## Example Output

For a run with 2 channels, 8 new videos:

```
Video Digest Results
====================

Checked 2 channels, found 8 new videos.

📊 Triage Results:
  Must Watch: 1
    - "AI Security for Autonomous Agents" (IndyDevDan) - Score: 92
  Worth Processing: 2
    - "AWS Bedrock Deep Dive" - Score: 68
    - "Kafka Streaming Patterns" - Score: 55
  Quick Capture: 2
  Skipped: 3

✅ Processed 2 videos:
  - [[YouTube - AWS Bedrock Deep Dive]] → 2 concepts, 1 pattern
  - [[YouTube - Kafka Streaming Patterns]] → 1 concept

📎 Created 2 quick captures:
  - [[Weblink - Tech News Weekly]]
  - [[Weblink - Developer Productivity Tips]]

📝 Updated today's daily note with digest.
📋 1 video added to must-watch queue.
```

## Error Handling

- **RSS fetch fails**: Log warning, continue to next channel
- **Transcript unavailable**: Process with description-only analysis
- **Daily note missing**: Create using `/daily` skill
- **Queue file missing**: Create with empty arrays
- **Config missing**: Use default thresholds

## Related Skills

- `/rss-check` - Channel subscription management
- `/youtube` - Full video processing
- `/daily` - Daily note creation
- `/schedule` - Scheduled execution setup
