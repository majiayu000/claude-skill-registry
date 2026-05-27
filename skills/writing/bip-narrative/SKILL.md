---
name: bip.narrative
description: Generate thematic, prose-style narrative digests from GitHub activity
---

# /bip.narrative

Generate a themed narrative digest for a Slack channel.

## Usage

```
/bip.narrative <channel> [--since <period>] [--verbose]
```

**Arguments:**
- `<channel>` — Channel name (required, e.g., `dasm2`)
- `--since <period>` — Time period to cover (default: `1w`). Examples: `1w`, `2d`, `3d`
- `--verbose` — Include PR/issue body summaries in the raw activity

## Setup

The nexus path is configured in `~/.config/bip/config.json`. For the commands below, use the configured path (e.g., if `nexus_path` is `~/re/nexus`, substitute that).

## Workflow

Execute these steps in order:

### Step 1: Fetch Raw Activity

Run the bip digest command to get GitHub activity:

```bash
bip digest --channel {{channel}} --since {{since}} {{verbose_flag}}
```

Where:
- `{{channel}}` is the channel argument
- `{{since}}` defaults to `1w` if not specified
- `{{verbose_flag}}` is `--verbose` if the user passed that flag, otherwise empty

**If the command fails or returns no activity**, stop and report "No activity found for channel {{channel}} in the specified period."

### Step 2: Read Shared Preferences

Read the shared preferences file:

```bash
cat <nexus>/narrative/preferences.md
```

**If the file doesn't exist**, stop and report:
"Missing shared preferences file: <nexus>/narrative/preferences.md"

### Step 3: Read Channel Configuration

Read the channel-specific config:

```bash
cat <nexus>/narrative/{{channel}}.md
```

**If the file doesn't exist**, stop and report:
"Missing channel config: <nexus>/narrative/{{channel}}.md
Create this file with Themes and Repo Context sections."

### Step 4: Generate Narrative

Using the raw activity from Step 1, the preferences from Step 2, and the channel config from Step 3, generate a narrative digest following these rules:

**Structure:**
1. Start with header: `# {{channel}} Digest: {{date_range}}`
   - Date range should match the `bip digest` output (e.g., "Jan 18-25, 2026")
2. Organize content by themes from the channel config's `## Themes` section
3. End with a `## Looking Ahead` section for open items

**Theme Classification:**
- Read the themes from the channel config's `## Themes` section
- Assign each activity item to the most appropriate theme
- Only include themes that have activity
- Theme order follows the numbered list in the config

**Subheadings (if applicable):**
- Check the channel config's `## Project-Specific Preferences` section
- If it specifies subheadings (like "viral/antibody paragraphs"), use those within theme sections
- Subheadings are channel-specific—only use what the config specifies

**Formatting (Hybrid Style):**
- Use **prose** when describing connected work or narrative flow
- Use **bullets** for lists of discrete items or contributors
- Status prefixes for non-merged items:
  - `In progress:` for open PRs
  - `Open:` for open issues
- **CRITICAL: Every PR/issue mentioned MUST have a link** — never refer to work without its `[#N](url)` link inline
  - Bad: "A modular dataset registry was merged"
  - Good: "A modular dataset registry was merged ([#176](url))"

**Looking Ahead Section:**
- Focus on **open issues only** (not PRs, unless a PR directly addresses a new issue worth explaining)
- Use **prose style**, not bullets—this section introduces new material to readers
- Provide **substantial detail**: explain what the issue is about, why it matters, and what needs to happen
- Group related issues together in coherent paragraphs
- Omit this section if no open issues exist

**Content Guidelines (from preferences.md):**
- Follow all rules in the shared preferences file
- Typically includes: no attribution, factual descriptions only
- Stick to available information—do not invent context

**CRITICAL — Include ALL Activity:**
- You MUST include EVERY item from the raw activity output. Do NOT skip or omit ANY PR or issue.
- EVERY repository that appears in the raw output MUST be represented in the narrative.
- If a repo has activity, it MUST appear somewhere in the digest. Missing repos is a failure.
- When in doubt, include the item. Completeness is more important than brevity.

### Step 5: Write Output

Determine output path:
```
<nexus>/narrative/{{channel}}/{{YYYY-MM-DD}}.md
```

Where `{{YYYY-MM-DD}}` is today's date.

1. Create the directory if needed: `mkdir -p <nexus>/narrative/{{channel}}`
2. Write the generated narrative to the file
3. Open the file for review: `zed <nexus>/narrative/{{channel}}/{{YYYY-MM-DD}}.md`
4. Report success: "Narrative digest written to: narrative/{{channel}}/{{YYYY-MM-DD}}.md"

### Step 6: Ask About Posting to Slack

After the user has reviewed the narrative, ask if they want to post it to Slack.

**If user approves:**

1. Commit and push the narrative:
   ```bash
   cd <nexus>
   git add narrative/{{channel}}/{{YYYY-MM-DD}}.md
   git commit -m "Add {{channel}} narrative digest for {{date_range}}"
   git push
   ```

2. Post to Slack using `bip digest --post`:
   ```bash
   bip digest --channel {{channel}} --post
   ```

   The webhook URL comes from `slack_webhooks` in `~/.config/bip/config.json` or `SLACK_WEBHOOK_{{CHANNEL_UPPER}}` env var.

3. Report: "Posted to #{{channel}} with link to narrative."

**If user declines:** Report "Narrative saved but not posted."

## Example Output

```markdown
# dasm2 Digest: Jan 18-25, 2026

## Model Architecture

The training pipeline saw significant improvements this week. The structure-aware loss function was merged ([#142](url)), enabling better handling of hierarchical outputs. In progress: refactoring the attention mechanism for memory efficiency ([#147](url)).

## Data Processing

**Viral:**
New preprocessing filters were added for low-quality sequences ([#138](url)).

**Antibody:**
The germline alignment step now handles ambiguous calls gracefully ([#151](url)).

## Looking Ahead

Several architectural decisions are pending. The OOM issues on large batches ([#156](url)) need investigation—this is blocking production use on full-size datasets. Separately, the team is considering whether to refactor the attention mechanism for memory efficiency, which would enable scaling to longer sequences without proportional memory growth.
```

## Error Handling

- **Missing config file**: Report which file is missing and stop
- **No activity**: Report "No activity found" and stop
- **bip CLI fails**: Report the error and stop
- **Output directory creation fails**: Report the error and stop
