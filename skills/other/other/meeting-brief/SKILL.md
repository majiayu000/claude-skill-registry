---
name: meeting-brief
description: Daily meeting preparation system that checks your calendar each morning, deeply researches external attendees (LinkedIn, company info, GitHub, past notes), and sends you personalized briefs via email (1 per person). Use when you want automated preparation for upcoming meetings with context about each person you're meeting.

graph:
  provides:
    - meeting-briefs       # Per-person research briefs sent to inbox
  requires:
    - calendar-access      # Google Calendar via gcalcli
    - email-access         # Gmail for sending briefs
  connects_to:
    - skill: gcalcli-calendar
      when: "Always — reads today's agenda as the first step"
      passes: nothing, reads calendar directly
    - skill: gmail
      when: "Always — sends the generated briefs via Gmail"
      passes: meeting-briefs
  capabilities: [read-calendar, web-search, send-email-via-gmail]
---

# Meeting Brief

Automated daily meeting preparation system that researches meeting attendees and sends you personalized briefs.

## What It Does

Every morning (configurable time):
1. Checks your calendar for today's meetings (via gcalcli)
2. Extracts attendees from each meeting
3. Filters out your team members (configurable)
4. Deep researches each external person:
   - LinkedIn profile (web search)
   - Company information
   - GitHub profile (if engineer)
   - Past interactions/notes (memory search)
   - Recent news/activity
5. Generates AI-powered brief per person
6. Sends 1 email per person to your inbox

## Setup

### 1. Configure Team Members

Edit `config.json` to list your team members (these will be skipped):

```json
{
  "team_members": [
    "alice@yourcompany.com",
    "bob@yourcompany.com",
    "team@yourcompany.com"
  ],
  "team_domains": [
    "@yourcompany.com"
  ],
  "schedule": "0 7 * * *",
  "timezone": "America/Los_Angeles",
  "your_email": "you@yourcompany.com",
  "brief_from": "Meeting Brief <briefbot@yourcompany.com>",
  "slack_webhook": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
  "send_email": true,
  "send_slack": true,
  "include_calendar_details": true,
  "research_depth": "standard"
}
```

**Config options:**
- `team_members`: Emails to skip (exact match)
- `team_domains`: Domain patterns to skip (e.g., skip all @yourcompany.com)
- `schedule`: Cron expression for daily run (default: 7am)
- `timezone`: Timezone for schedule
- `your_email`: Where to send briefs
- `brief_from`: From address for briefs
- `slack_webhook`: Slack incoming webhook URL (optional)
- `send_email`: Whether to send email briefs (default: true)
- `send_slack`: Whether to send Slack notifications (default: false)
- `include_calendar_details`: Include meeting time/location in brief
- `research_depth`: `quick` (web only), `standard` (web + GitHub), `deep` (web + GitHub + past notes)

### 2. Set Up Daily Cron Job

Use OpenClaw's cron tool to schedule the daily run:

```javascript
// Create cron job for daily meeting briefs
{
  name: "Meeting Brief - Daily",
  schedule: {
    kind: "cron",
    expr: "0 7 * * *",  // 7 AM daily (UTC)
    tz: "America/Los_Angeles"
  },
  payload: {
    kind: "agentTurn",
    message: "Run the meeting-brief skill for today's meetings",
    timeoutSeconds: 600
  },
  sessionTarget: "isolated"
}
```

Alternatively, run manually:
```bash
cd skills/meeting-brief
./scripts/run_daily.sh
```

## How It Works

### Main Workflow (`scripts/run_daily.sh`)

1. **Fetch today's meetings** (`scripts/check_calendar.sh`)
   - Uses gcalcli to get today's agenda
   - Parses meeting times, titles, attendees
   - Outputs JSON with meeting details

2. **Filter external attendees** (built into run_daily.sh)
   - Loads config.json
   - Filters out team members and team domains
   - Creates list of people to research

3. **Research each person** (`scripts/research_person.js`)
   - Web search: LinkedIn profile, company info
   - GitHub search: Profile and repos (if applicable)
   - Memory search: Past interactions/notes
   - News search: Recent activity
   - Outputs structured research JSON

4. **Generate brief** (`scripts/generate_brief.js`)
   - Uses OpenClaw session to generate AI brief
   - Inputs: research data + meeting context
   - Outputs: Two formats:
     - **Email**: Concise bullet-point brief
     - **Slack**: Rich paragraph-style story with deeper context and narrative

5. **Send brief** 
   - Email: Uses Gmail skill (`send_email: true`)
   - Slack: Uses webhook (`send_slack: true`, `scripts/send_slack.sh`)
   - Subject: "Meeting Brief: [Person Name] - [Meeting Title]"
   - Body: AI-generated brief with research

6. **Save to personal CRM** (`supernotes/people/`)
   - Each researched person saved as markdown file
   - Includes: research data, meeting context, date
   - Builds personal relationship database over time

7. **Track sent briefs** (logs to `data/sent/YYYY-MM-DD.json`)
   - Prevents duplicates
   - Enables analytics

## Research Process

For each external attendee, the system researches:

### Web Search (Always)
- LinkedIn profile (name + company)
- Company information
- Recent news mentions
- Professional background

### GitHub (If `research_depth` is `standard` or `deep`)
- GitHub profile lookup (by name/email)
- Recent repos and contributions
- Technical focus areas

### Memory/Past Notes (If `research_depth` is `deep`)
- Search MEMORY.md and daily notes
- Past meeting notes
- Previous interactions
- Context from past conversations

### Output Format

Research is structured as JSON:

```json
{
  "person": {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "company": "Example Corp",
    "title": "VP Engineering"
  },
  "linkedin": {
    "url": "...",
    "bio": "...",
    "experience": [...]
  },
  "github": {
    "username": "janedoe",
    "profile_url": "...",
    "recent_repos": [...]
  },
  "company": {
    "name": "Example Corp",
    "industry": "...",
    "recent_news": [...]
  },
  "past_interactions": [
    "Met at conference in 2024",
    "Discussed partnership opportunity"
  ]
}
```

## Brief Generation

The AI-generated brief comes in **two formats**:

### Email Format (Concise Bullets)

1. **Quick Overview**
   - Who they are (name, title, company)
   - Why you're meeting (meeting title/description)

2. **Background**
   - Professional background (LinkedIn)
   - Company context
   - Technical expertise (GitHub, if applicable)

3. **Conversation Starters**
   - Based on recent activity
   - Shared interests/connections
   - Relevant topics

4. **Action Items / Notes**
   - Past interactions (if any)
   - Things to remember
   - Follow-up items

### Slack Format (Rich Story)

Deeper, narrative-driven brief with:
- Paragraph-style storytelling about the person
- Context about their journey and recent work
- Compelling hooks and conversation angles
- More background color and detail
- Stronger narrative flow than bullet points

**Example Brief:**

```
Subject: Meeting Brief: Jane Doe - Product Partnership Discussion

Hi,

You're meeting with Jane Doe today at 2pm.

## Quick Overview
Jane is VP of Engineering at Example Corp, a B2B SaaS company in the dev tools space. She's been there for 3 years and previously worked at GitHub and Microsoft.

## Background
- Strong background in developer tooling and infrastructure
- Recently led Example Corp's API platform overhaul (launched Q4 2025)
- Active on GitHub (janedoe) - maintains several open-source CLI tools
- Technical blog focuses on API design and developer experience

## Conversation Starters
- Their new API platform (just launched, getting good traction)
- Recent blog post on GraphQL vs REST (published last week)
- Shared interest in developer experience (noted in her LinkedIn)

## Notes
- You met briefly at DevTools Summit 2024
- She mentioned interest in partnering on integration opportunities

---
Meeting: Product Partnership Discussion
Time: Today at 2:00 PM
Location: Zoom (link in calendar)
```

## Manual Usage

Run for a specific person:

```bash
# Research a person
node scripts/research_person.js "Jane Doe" "jane@example.com" "Example Corp"

# Generate brief
node scripts/generate_brief.js research_output.json meeting_context.json

# Send brief
./scripts/send_brief.sh brief.html "Jane Doe"
```

Run for today's meetings:

```bash
./scripts/run_daily.sh
```

## Data & Logs

```
meeting-brief/
├── data/
│   ├── sent/              # Sent brief logs (by date)
│   │   └── 2026-02-21.json
│   ├── research/          # Research cache (by person)
│   │   └── jane-doe.json
│   └── meetings/          # Meeting data (by date)
│       └── 2026-02-21.json
└── logs/
    └── run.log            # Execution logs
```

## Tips

1. **Test with dry-run first**: Set `DRY_RUN=true` in run_daily.sh to preview without sending
2. **Adjust research depth**: Start with `quick`, upgrade to `standard` or `deep` as needed
3. **Refine team filter**: Add domains/emails to skip internal meetings
4. **Review briefs**: Check data/sent/ logs to see what's being sent
5. **Iterate on prompts**: Edit generate_brief.js to customize AI prompt

## Troubleshooting

**No briefs sent:**
- Check gcalcli authentication (`gcalcli agenda today tomorrow`)
- Verify calendar has events with external attendees
- Check logs in `logs/run.log`

**Briefs missing information:**
- Increase `research_depth` in config.json
- Check web_search and GitHub CLI are working
- Review research data in `data/research/`

**Duplicate briefs:**
- Check `data/sent/` for already-sent tracking
- Verify cron job isn't running multiple times

## Integration with OpenClaw

This skill uses:
- **gcalcli-calendar**: For fetching today's meetings
- **web_search**: For LinkedIn and company research
- **GitHub CLI (`gh`)**: For GitHub profile lookup
- **memory_search**: For past interactions (deep mode)
- **gmail skill**: For sending brief emails
- **sessions_spawn**: For AI brief generation
- **cron**: For daily scheduling

## Privacy & Security

- Research data is cached locally in `data/research/`
- No external APIs (uses web_search, GitHub CLI, memory_search)
- Briefs sent only to configured email
- Team member filtering prevents leaking internal info
- All data stored in skill directory (no cloud storage)
