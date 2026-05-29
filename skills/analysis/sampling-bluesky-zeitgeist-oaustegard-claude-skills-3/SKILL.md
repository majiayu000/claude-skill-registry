---
name: sampling-bluesky-zeitgeist
description: DEPRECATED - Use browsing-bluesky skill instead. Sample and analyze Bluesky firehose to identify trending topics and content clusters. Use when user asks about "what's happening on Bluesky", "Bluesky trends", "zeitgeist", "firehose analysis", or wants to see real-time topic clusters from the network.
metadata:
  version: 0.1.0
  deprecated: true
  superseded_by: browsing-bluesky
---

# Sampling Bluesky Zeitgeist

**⚠️ DEPRECATED: This skill has been consolidated into the `browsing-bluesky` skill.**

Use `browsing-bluesky` for firehose sampling via the `sample_firehose()` function.

---

## Legacy Documentation

Capture and analyze multiple windows of Bluesky firehose data, identify content clusters, and present results showing both individual sample windows and aggregate trends.

## Workflow

### 1. Setup

Install dependencies:

```bash
cd /home/claude && npm install ws https-proxy-agent 2>/dev/null
```

### 2. Run Sample Windows

Execute 3 consecutive 10-second samples:

```bash
node /mnt/skills/user/sampling-bluesky-zeitgeist/scripts/zeitgeist-sample.js --duration 10 > /home/claude/sample1.json 2>/dev/null
node /mnt/skills/user/sampling-bluesky-zeitgeist/scripts/zeitgeist-sample.js --duration 10 > /home/claude/sample2.json 2>/dev/null
node /mnt/skills/user/sampling-bluesky-zeitgeist/scripts/zeitgeist-sample.js --duration 10 > /home/claude/sample3.json 2>/dev/null
```

### 3. Analyze & Build DATA Object

Parse each JSON file and aggregate:
- Sum totalPosts, calculate avgPostsPerSecond
- Merge topWords, topPhrases, entities across windows
- Calculate per-minute rates: `(count / totalDurationSec) * 60`
- Detect trends by comparing window counts

### 4. Identify Content Clusters

Group related terms into thematic clusters. For each cluster:
- **name**: Descriptive label
- **emoji**: Visual identifier
- **terms**: Keywords that belong to this cluster
- **searchQuery**: OR-joined terms for Bsky search (e.g., `"trump OR republican OR congress"`)
- **totalMentions**: Sum across all windows
- **mentionsPerMin**: `(totalMentions / totalDurationSec) * 60`
- **trend**: "up" if last window > first by 30%, "down" if <30%, else "stable"
- **samples**: 2-3 example posts matching cluster

### 5. Create Artifact via Template

Copy template and inject DATA:

```bash
cp /mnt/skills/user/sampling-bluesky-zeitgeist/assets/zeitgeist-template.html /mnt/user-data/outputs/zeitgeist.html
```

Then use str_replace to inject the DATA object:

```
old_str: const DATA = {"aggregate":{"totalPosts":0,"totalDurationSec":30,"avgPostsPerSecond":0,"timestamp":""},"windows":[],"clusters":[],"entities":[],"phrases":[],"languages":{}};
new_str: const DATA = {YOUR_ACTUAL_DATA_OBJECT};
```

See `references/artifact-template.md` for the complete DATA schema.

## Output Format

Present the artifact link, then provide a brief prose summary:
- What's dominating the conversation (top 1-2 clusters)
- Any notable velocity spikes
- Interesting patterns (e.g., "Japanese-language posts spiking around [topic]")

Keep summary to 2-3 sentences. The artifact is the main deliverable.

## Refresh Workflow

When user asks to refresh/update/sample again:

1. Run new sample windows (same 3x10s pattern)
2. Update the DATA object with new results
3. Use str_replace to swap the DATA line in the existing artifact
4. Report what changed: "Trump mentions up 20% from last sample, M23 discussion fading"

For comparison, track previous aggregate totals and show delta:
```
Previous: trump 50/min → Current: trump 62/min (+24%)
```

## Topic Monitoring Workflow

When user specifies a topic to monitor (e.g., "track the Lakers game", "what's happening with the drone sightings"):

### Option A: Filtered Sampling
Run samples with the --filter flag to capture only matching posts:

```bash
node zeitgeist-sample.js --duration 15 --filter "lakers" > /home/claude/topic1.json 2>/dev/null
```

This gives deeper analysis of a specific topic but misses broader context.

### Option B: General + Topic Velocity (Recommended)
Run general samples, then:
1. Calculate topic-specific velocity from the results
2. Add a dedicated "Monitored Topic" cluster at the top
3. Include sample posts matching the topic

In the DATA object, add a `monitoredTopic` field:
```json
{
  "monitoredTopic": {
    "query": "lakers",
    "totalMentions": 45,
    "mentionsPerMin": 90.0,
    "trend": "up",
    "windowCounts": [12, 15, 18],
    "samples": ["Lakers up by 10 in the 4th!", "LeBron with another triple double"]
  }
}
```

### Responding to Topic Requests

**At start of conversation:**
- "What's happening with the drone sightings?" → Run general sample, highlight drone-related content as monitored topic
- "Track mentions of Claude AI" → Same approach, focus on that term

**Mid-conversation:**
- "Can you focus on the M23 conflict?" → Re-run samples, add M23 as monitored topic
- "What about Japanese content specifically?" → Filter for lang:ja or highlight existing Japanese cluster

**Follow-up pattern:**
User: "refresh but focus on the game"
→ Run new samples, keep monitored topic, update all data

## Error Handling

If WebSocket connection fails:
- Check that `*.bsky.network` is in allowed domains
- Retry once with shorter duration (5s)
- If still failing, report the error and suggest user check network settings

If sample returns zero posts:
- Likely network/proxy issue
- Report and do not create artifact

## Customization Options

User may request:
- **Longer samples**: Increase duration per window or add more windows
- **Topic focus**: After initial sample, run filtered samples for specific clusters
- **Comparison**: Run samples at different times and compare
