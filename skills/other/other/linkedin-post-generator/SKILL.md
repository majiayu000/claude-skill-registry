---
name: linkedin-post-generator
description: >
  LinkedIn post generation from meeting transcripts, Slack dumps, and other source material,
  written in the user's personal writing style. Use this skill when: generating LinkedIn posts,
  creating social content from internal material, ghostwriting LinkedIn content, or when the user
  mentions LinkedIn, social posts, or content generation from transcripts/notes.
  Supports personal style profiles stored locally per user.
  Can auto-pull source material from Fireflies.ai, Slack channels, and Google Drive.
---

# LinkedIn Post Generator

Generate LinkedIn posts from shared source material, written in each user's personal style.

## How It Works

1. **Personal style profile** — stored locally at `~/.config/casper/linkedin-style.md` (never committed)
2. **Source config** — stored locally at `~/.config/casper/linkedin-sources.md` (never committed)
3. **Shared source material** — meeting transcripts, Slack dumps, docs in `source-material/`
4. **Prompt template** — extraction rules, voice guidelines, few-shot examples in `references/prompt-template.md`

## First Run: Style Setup

Check if `~/.config/casper/linkedin-style.md` exists.

**If it does NOT exist**, run the style setup flow:

1. Say: "Welcome to the LinkedIn Post Generator! Before we start, I need to understand your writing style."
2. Say: "Share 3 LinkedIn posts that match the style you want. You can either paste the post links (e.g. `https://linkedin.com/posts/...`) or paste the text directly."
3. Wait for the user to provide 3 posts
4. **If the user provides LinkedIn URLs**, fetch the post content using the apify-scrapers skill:
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/skills/apify-scrapers/scripts/scrape_linkedin_posts.py search "{url}" --max-posts 1
   ```
   Extract the post text from the JSON output. If a URL fails to fetch, ask the user to paste that post's text instead.
5. Analyze the posts for: tone, sentence length, vocabulary, formatting habits, hook style, CTA style, use of questions, paragraph length, overall energy
6. Create `~/.config/casper/` directory if it doesn't exist
7. Save the analysis to `~/.config/casper/linkedin-style.md` using this format:

```markdown
# LinkedIn Style Profile
Generated: [date]

## Tone
[analysis]

## Structure Patterns
[paragraph length, line breaks, formatting habits]

## Hook Style
[how they open posts]

## CTA / Closing Style
[how they end posts — questions, challenges, etc.]

## Vocabulary & Phrases
[distinctive phrases, word choices, energy level]

## Sample Posts
[the 3 original posts, for reference]
```

8. Confirm: "Got it! Your style profile is saved. You can update it anytime with `/casper:generate-linkedin-post --setup`"

## First Run: Source Material Check

After style setup completes (or if style exists but source-material/ is empty), check for source material:

1. Check if `source-material/` contains any `.md` files besides `README.md`
2. **If empty**, guide the user:
   - Say: "You don't have any source material yet. I need content to generate posts from — meeting transcripts, notes, Slack conversations, etc."
   - Present options:
     - **"Connect integrations"** — run the `--setup-sources` flow to configure Fireflies, Slack, or Google Drive auto-pulling
     - **"Paste something manually"** — run the `--add-source` flow to let the user paste a transcript, notes, or other content
   - Wait for user choice and proceed with the selected flow
3. **If source material exists**, proceed with generation

## Normal Run: Post Generation

**If style config exists and source material is available**, proceed with generation:

1. Read `~/.config/casper/linkedin-style.md`
2. Read ALL files in `${CLAUDE_PLUGIN_ROOT}/skills/linkedin-post-generator/source-material/` (excluding README.md)
3. Read `${CLAUDE_PLUGIN_ROOT}/skills/linkedin-post-generator/references/prompt-template.md`
4. Apply the confidentiality rules from the prompt template (no financials, no client names, no pipeline, no team member names)
5. Generate 2-4 post options based on the source material, written in the user's personal style
6. Present them in a clean, copy-paste-ready format

## Flags

| Flag | Behavior |
|------|----------|
| (none) | Normal generation flow |
| `--setup` | Re-run style setup, overwrite existing config |
| `--setup-sources` | Configure which Fireflies, Slack, and Drive sources to pull from |
| `--refresh` | Pull fresh source material from configured integrations, then generate |
| `--view-style` | Read and display `~/.config/casper/linkedin-style.md` |
| `--view-sources` | List and summarize all files in `source-material/` |
| `--add-source` | Prompt user to paste new content, save as new `.md` file in `source-material/` |

## Flag Details

### `--setup-sources`

Interactive setup for automatic source pulling. Read `references/source-integrations.md` for full details.

1. Ask: "What's your work email address? This is used to filter transcripts to only meetings you attended."
   - Save as `user_email` in the config
2. Ask: "Which sources do you want to connect?" Present options:
   - **Fireflies.ai** — pulls meeting transcripts (needs `FIREFLIES_API_KEY` env var)
   - **Slack** — pulls messages from channels (needs `SLACK_BOT_TOKEN` env var)
   - **Google Drive** — pulls docs and transcripts (needs OAuth setup via google-workspace skill)
3. For each selected source, check if the required env var / credentials exist. If missing, provide setup instructions:
   - **Fireflies**: "Set `FIREFLIES_API_KEY` in your environment. Get your API key from https://app.fireflies.ai/api"
   - **Slack**: "Set `SLACK_BOT_TOKEN` in your environment. Create a Slack app at https://api.slack.com/apps"
   - **Google Drive**: "Run the google-workspace skill setup to configure OAuth."
4. For each enabled source, gather configuration:
   - **Fireflies**: search terms (or leave empty for all recent) and days_back
   - **Slack**: which channels to pull from — list available channels if possible, otherwise ask the user
   - **Google Drive**: search terms, days_back
5. Save to `~/.config/casper/linkedin-sources.md`
6. Confirm: "Source config saved. Run `/casper:generate-linkedin-post --refresh` to pull fresh content."

### `--refresh`

Pull fresh source material from all configured integrations before generating posts. Read `references/source-integrations.md` for the full integration workflow.

**Summary of the flow:**

1. Read `~/.config/casper/linkedin-sources.md` — if missing, run `--setup-sources` first
2. For each enabled source, call the existing Casper skill scripts:
   - **Fireflies**: `python ${CLAUDE_PLUGIN_ROOT}/skills/transcript-search/scripts/fireflies_transcript_search.py "{term}" --days-back {N} --content --json`
     - After fetching, filter results to only transcripts where `user_email` (from source config) appears in the transcript's `participants` array
   - **Slack**: `python ${CLAUDE_PLUGIN_ROOT}/skills/slack-automation/scripts/slack_search.py read "{channel}" --days {N}`
   - **Google Drive**: `python ${CLAUDE_PLUGIN_ROOT}/skills/google-workspace/scripts/gdrive_search.py files "{term}" --modified-days {N} --json`
3. Convert JSON output to clean markdown and save to `source-material/`:
   - Fireflies: `fireflies-{YYYY-MM-DD}-{title-slug}.md`
   - Slack: `slack-{channel}-{YYYY-MM-DD}.md`
   - Google Drive: `gdrive-{title-slug}-{YYYY-MM-DD}.md`
4. Proceed with normal generation

### `--view-style`

Read `~/.config/casper/linkedin-style.md` and display it. If it doesn't exist, say "No style profile found. Run `/casper:generate-linkedin-post --setup` to create one."

### `--view-sources`

List all `.md` files in `${CLAUDE_PLUGIN_ROOT}/skills/linkedin-post-generator/source-material/` (excluding `README.md`). For each file, show the filename and a 1-line summary of its contents.

### `--add-source`

1. Ask: "Paste the content you want to add as source material (meeting transcript, Slack dump, notes, etc.)"
2. Ask: "What should I name this source file? (e.g., `team-standup-jan-2025`)"
3. Save as `${CLAUDE_PLUGIN_ROOT}/skills/linkedin-post-generator/source-material/[name].md`
4. Confirm: "Source material saved. It will be included in future post generation."

## Reference Files

| File | When to Read |
|------|-------------|
| `references/prompt-template.md` | Every generation run — contains voice rules, few-shot examples, confidentiality rules |
| `references/source-integrations.md` | When running `--refresh` or `--setup-sources` — contains script paths, arguments, output conversion |
| `references/style-setup.md` | When running `--setup` — contains analysis framework for style profiling |
| `source-material/*.md` | Every generation run — raw content to extract post ideas from |
