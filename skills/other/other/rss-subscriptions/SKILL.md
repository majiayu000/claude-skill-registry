---
context: fork
---

# /rss-check

Check subscribed YouTube channels for new videos and add them to today's daily note.

## Usage

```
/rss-check                    # Check all subscribed channels
/rss-check <channel-name>     # Check specific channel only
/rss-check --list             # List all subscriptions
/rss-check --add <url>        # Add new channel subscription
/rss-check --remove <name>    # Remove channel subscription
```

## Examples

```
/rss-check
/rss-check "Nate B Jones"
/rss-check --add https://www.youtube.com/@NateBJones
/rss-check --list
```

## Subscription Config

Subscriptions are stored in `.claude/subscriptions.yaml`:

```yaml
youtube_channels:
  - name: "Nate B Jones"
    channel_id: "UCxxxxxxxxxx"
    channel_url: "https://www.youtube.com/@NateBJones"
    last_checked: "2026-01-12T00:00:00Z"
    last_video_id: "0TpON5T-Sw4"
    create_page: true           # Create full Page analysis
    tags: [ai, productivity]    # Default tags for this channel

settings:
  auto_create_page: true        # Default: create Page for all new videos
  auto_create_weblink: true     # Default: create Weblink for all new videos
  add_to_daily: true            # Add entries to daily note
  extract_links: true           # Extract links from video descriptions
```

## Instructions

### List Subscriptions (`--list`)

1. Read `.claude/subscriptions.yaml`
2. Display formatted table of subscriptions:
   ```
   | Channel | Last Checked | Last Video |
   |---------|--------------|------------|
   | Nate B Jones | 2026-01-12 | Why 2026 Is... |
   ```

### Add Subscription (`--add <url>`)

1. Parse YouTube channel URL (supports `@handle`, `/channel/ID`, `/c/name` formats)
2. Use `mcp__MCP_DOCKER__get_video_info` on a recent video to get channel info
3. Extract channel ID from video info or page
4. Add entry to `.claude/subscriptions.yaml`:
   ```yaml
   - name: "Channel Name"
     channel_id: "UCxxxxxxxxxx"
     channel_url: "https://www.youtube.com/@handle"
     last_checked: null
     last_video_id: null
     create_page: true
     tags: []
   ```
5. Confirm addition

### Remove Subscription (`--remove <name>`)

1. Find channel by name (case-insensitive partial match)
2. Remove from `.claude/subscriptions.yaml`
3. Confirm removal

### Check for New Videos (default)

1. **Read subscriptions** from `.claude/subscriptions.yaml`

2. **For each channel**, fetch RSS feed:
   ```
   https://www.youtube.com/feeds/videos.xml?channel_id={{channel_id}}
   ```
   Use `WebFetch` with prompt: "Extract video entries: title, video_id, published date, description"

3. **Identify new videos**:
   - Compare video IDs against `last_video_id`
   - Select videos published after last check
   - If first check, take only the most recent video

4. **For each new video**:

   a. **Fetch full details**:
      ```
      mcp__MCP_DOCKER__get_video_info(url)
      mcp__MCP_DOCKER__get_transcript(url)
      ```

   b. **Extract links from description**:
      - Parse URLs from video description
      - Categorise: website, substack, github, twitter, etc.
      - Store for inclusion in notes

   c. **Create Weblink note** (if `auto_create_weblink: true`):
      - Follow `/youtube` skill Weblink template
      - Include extracted links in Resources section

   d. **Create Page note** (if channel `create_page: true`):
      - Follow `/youtube` skill Page template
      - Full transcript analysis
      - Include all extracted links

   e. **Add to Daily Note**:
      - Open/create today's daily note (`+Daily/{{year}}/{{date}}.md`)
      - Add entry under `## New Videos` section:
        ```markdown
        ## New Videos

        ### [[Weblink - {{video title}}]]
        **Channel:** [[Nate B Jones]]
        **Duration:** {{duration}}

        {{2-3 sentence summary}}

        **Links mentioned:**
        - [Resource 1](url)
        - [Resource 2](url)
        ```

5. **Update subscription config**:
   - Set `last_checked` to current timestamp
   - Set `last_video_id` to most recent video ID

6. **Report results**:
   ```
   Checked 3 channels:
   - Nate B Jones: 1 new video
     - "Why 2026 Is the Year to Build a Second Brain"
     - Created: Weblink + Page
   - Channel 2: No new videos
   - Channel 3: 2 new videos
     - "Video Title 1" (Weblink + Page)
     - "Video Title 2" (Weblink + Page)

   Added 3 entries to today's daily note.
   ```

## Daily Note Integration

The skill adds a `## New Videos` section to the daily note. If the section doesn't exist, create it. If it exists, append new entries.

**Daily note location:** `+Daily/{{year}}/{{YYYY-MM-DD}}.md`

**Entry format:**
```markdown
### [[Weblink - {{title}}]]
**Channel:** [[{{channel name}}]]
**Duration:** {{duration}}

{{brief summary from video analysis}}

**Links mentioned:**
- [{{link title}}]({{url}})
```

## Link Extraction

From video descriptions, extract and categorise:

| Type | Pattern | Example |
|------|---------|---------|
| Website | Personal domains | natebjones.com |
| Newsletter | Substack, Beehiiv | natesnewsletter.substack.com |
| GitHub | github.com/* | github.com/user/repo |
| Twitter/X | twitter.com, x.com | x.com/handle |
| LinkedIn | linkedin.com | linkedin.com/in/name |
| Product | Product URLs | notion.so, zapier.com |

Include these in:
1. Weblink note `## Resources` section
2. Page note `## Resources` section
3. Daily note entry `**Links mentioned:**`

## Error Handling

- **RSS fetch fails:** Log error, continue to next channel
- **Transcript unavailable:** Create notes without transcript, note in output
- **Daily note doesn't exist:** Create it using `/daily` skill template
- **Config file missing:** Create default config with instructions

## Channel ID Discovery

YouTube channel IDs can be found:
1. From any video by that channel (in video info)
2. From channel page source (search for `channelId`)
3. From RSS feed URL if already subscribed

When adding via `--add`, attempt to:
1. Fetch the channel page
2. Extract channel ID from page content
3. Get latest video to verify

## Quality Standards

- **Always** update config after checking
- **Always** link Person note if exists for channel creator
- **Always** extract and include description links
- **Never** duplicate videos already captured
- **Use** UK English throughout
- **Create** daily note if it doesn't exist
