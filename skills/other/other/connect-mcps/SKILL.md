---
name: connect-mcps
description: Connect MCPs for real-time tool integration
version: 1.0
user-invocable: true
modifies-workspace: true
---

# `/connect-mcps` - MCP Integration & Connection Manager

Connect Model Context Protocol (MCP) servers to your PM OS workspace for real-time data access from your tools.

## Quick Start

Tell me which tool to connect (e.g., "connect to Amplitude") and I will guide you through setup. Or say "batch" to connect multiple tools at once.

1. Name the tool: "connect to [tool name]"
2. I search for official MCP servers (remote first, then local)
3. I guide you through credentials and authentication
4. I test the connection and discover available tools
5. I update your PM OS skills and CLAUDE.md routing automatically

**Example:** `/connect-mcps connect to linear`

**Output:** MCP connected, skills updated, integration log saved to `outputs/mcp-integration-logs/`

**Time:** 5-20 minutes per tool depending on setup method

## When to Use

- **Initial workspace setup** - Connect your analytics, project management, and research tools
- **Adding new tools** - When you start using a new tool that has an MCP server
- **After installing MCP servers** - Once you've installed an MCP server locally or have access to one

## Usage Patterns

### Individual Connection (Recommended)
```
/connect-mcps connect to amplitude
/connect-mcps connect to linear
/connect-mcps connect to notion
```

### Batch Connection (Advanced)
```
/connect-mcps batch
```
Then provide multiple tool names when prompted.

## How It Works

When you run `/connect-mcps connect to [tool name]`, I will:

1. **Check for official remote MCP server** - Search for hosted MCP servers (priority method)
2. **If remote server exists** - Guide you to use `claude mcp add --transport http [tool] [url]`
3. **If no remote server** - Research manual setup (OAuth, API tokens)
4. **Guide credential entry** - Prompt you for required credentials
5. **Test connection** - Verify the connection works and discover available tools
6. **Map to skills** - Automatically determine which PM OS skills benefit from this MCP
7. **Update workspace** - Add integration instructions to relevant skills and update CLAUDE.md registry
8. **Enable intelligent routing** - Your natural language queries will automatically route to the right MCP

**Priority Order:**
- ✅ **First:** Check for official remote MCP server (e.g., Figma, Stripe)
- ⚙️ **Second:** Local MCP server via NPM/Docker
- 🔑 **Last:** Manual OAuth/API token setup

## Step-by-Step Workflow

### Step 1: Parse Tool Name

When you run `/connect-mcps connect to amplitude`:
- Extract tool name: "amplitude"
- Normalize and validate the name
- Check if already connected (skip if duplicate)

### Step 2: Check for Official Remote MCP Server (Priority #1)

**IMPORTANT:** Always check for official remote MCP servers FIRST before manual setup.

I'll search the web for:
- "[tool name] official MCP server"
- "[tool name] remote MCP server"
- "[tool name] MCP server documentation 2026"

**If I find a remote server URL** (e.g., `https://mcp.figma.com/mcp`):

✅ **I'll tell you to use the simple method:**
```bash
claude mcp add --transport http [tool] [url]
```

Then manage it via `/mcp` in Claude Code to authenticate.

**Example remote MCP servers:**
- **Figma:** `https://mcp.figma.com/mcp`
- **Stripe:** Check Stripe docs for MCP endpoint
- **Others:** Search "[tool] MCP remote server"

---

### Step 3: Manual Setup (Fallback Only)

**Only if no remote server exists**, I'll search for:
- "[tool name] MCP integration guide"
- "[tool name] Claude MCP setup"
- "[tool name] API authentication requirements"

From the search results, I extract:
- NPM package name or local server setup
- Required authentication (API keys, OAuth tokens, workspace IDs)
- Configuration parameters needed
- Tool names and capabilities
- Setup instructions and documentation links

### Step 4: Guide You Through Connection

I'll present what's needed:
```
To connect Amplitude, I need:
1. Amplitude API Key (Settings → API Keys)
2. Project ID (Settings → Projects)

[Link to Amplitude documentation]
```

Then prompt for each credential:
```
Enter your Amplitude API Key: [you paste here]
Enter your Project ID: [you paste here]
```

**Note:** Your credentials are handled by the MCP system securely. I don't store them in files.

### Step 5: Test Connection & Discover Tools

Once credentials are provided:
- Test the connection to verify it works
- Query the MCP server to discover available tools
- Extract tool names, descriptions, and parameters
- Document capabilities for routing

Example discovered tools for Amplitude:
- `query_insights` - Query product analytics data
- `get_funnels` - Retrieve funnel analysis
- `cohort_analysis` - Analyze user cohorts
- `event_tracking` - Track custom events

### Step 6: Intelligent Skill Mapping

Based on the MCP category, I automatically map it to relevant skills:

**Analytics MCPs** (Amplitude, Mixpanel, Posthog, Pendo)
→ feature-metrics, impact-sizing, retention-analysis, activation-analysis, feature-results, metrics-framework, experiment-metrics

**Project Management MCPs** (Linear, Jira)
→ create-tickets, meeting-notes, status-update, prioritize

**Research MCPs** (Dovetail)
→ user-interview, user-research-synthesis, interview-guide

**Transcription MCPs** (Otter.ai, Fireflies)
→ meeting-notes, meeting-cleanup, user-interview

**Communication MCPs** (Slack)
→ slack-message, status-update, meeting-notes

**Documentation MCPs** (Notion, Confluence)
→ decision-doc, status-update, meeting-notes

**Design MCPs** (Figma)
→ generate-ai-prototype, napkin-sketch, prototype-feedback

**Web Search MCPs**
→ competitor-analysis, competitive-intel

**Multi-category MCPs** are mapped to multiple skill groups.

### Step 7: Update Skill Files

For each mapped skill, I will:
1. Read the current SKILL.md file
2. Find the right insertion point (after Prerequisites or How It Works)
3. Add an MCP integration section:

```markdown
### Using [MCP Name] (If Connected)

[MCP Name] provides [capability description].

**Available Tools:**
- `tool_name` - [purpose]
- `tool_name_2` - [purpose]

**Integration Example:**
```pseudocode
# Query Amplitude for feature metrics
amplitude.query_insights({
  "event": "feature_used",
  "feature_name": "checkout",
  "date_range": "last_14_days"
})
```

**Benefits:**
- Real-time data instead of manual exports
- Query on-demand without switching tools
- Segment and filter programmatically

**Fallback:** If Amplitude not connected, you can upload exported CSV data to `context-library/metrics/` and I'll analyze that instead.
```

4. Write the updated SKILL.md back to disk
5. Log the change for the integration summary

### Step 8: Update CLAUDE.md Registry

I update two critical sections in CLAUDE.md:

**A) MCP Registry Table** - Lists all connected MCPs

| MCP | Purpose | Category | Used In | Key Tools |
|-----|---------|----------|---------|-----------|
| Amplitude | Product analytics | Analytics | feature-metrics, impact-sizing | query_insights, get_funnels |

**B) Intelligent Query Routing Logic** - Maps query patterns to MCPs

This enables me to automatically understand queries like:
- "Give me metrics on the login feature" → Route to Amplitude
- "Show my open tasks" → Route to Linear
- "What did users say about feature X" → Route to Dovetail

### Step 9: Generate Integration Summary

After successful integration, I:
- Save a detailed log to `outputs/mcp-integration-logs/[timestamp]-[tool-name].md`
- Display a summary showing:
  - Tools discovered
  - Skills updated
  - How to use the MCP with natural language queries
- Provide next steps

## MCP Intelligence Gathering

### What I Look For in Documentation

When researching an MCP, I extract:

**1. Setup Requirements**
- NPM package name or server URL
- Authentication method (API key, OAuth, token)
- Required configuration (workspace ID, project ID, etc.)
- Environment variables needed

**2. Tool Catalog**
- Available tools/functions
- Tool purposes and descriptions
- Parameter requirements (required vs optional)
- Return value structures

**3. Common Use Cases**
- Typical queries and operations
- Example workflows
- Best practices
- Rate limits or constraints

**4. Category Classification**
- Primary category (analytics, PM, research, etc.)
- Secondary categories if multi-purpose
- Keywords for routing logic

### Web Search Strategy

I use multiple search queries to find comprehensive information:

1. **"[tool] MCP server documentation 2026"** - Official MCP docs
2. **"[tool] MCP integration guide"** - Setup tutorials
3. **"[tool] Claude MCP setup"** - Claude-specific instructions
4. **"[tool] API authentication requirements"** - Auth details

I parse the results looking for:
- API key locations in the tool's settings
- Step-by-step setup instructions
- Code examples showing MCP usage
- Tool lists and function signatures

## Category Detection & Mapping Rules

### How I Determine MCP Category

**Analytics/Metrics Keywords:**
analytics, metrics, data, dashboard, reporting, charts, insights, KPI, measurement, funnel, cohort, retention, events

**Project Management Keywords:**
tickets, issues, tasks, projects, sprints, backlog, epics, stories, roadmap, planning

**Research/Interviews Keywords:**
research, interviews, transcripts, insights, quotes, themes, tagging, synthesis, user feedback

**Transcription Keywords:**
transcription, audio, recording, speech-to-text, meeting recording, voice notes

**Communication Keywords:**
slack, email, messaging, notifications, chat, channels, DMs

**Documentation Keywords:**
docs, wiki, knowledge base, pages, workspace, notes

**Design/Prototyping Keywords:**
design, prototype, mockup, wireframe, UI, UX, Figma, components

**Web Search Keywords:**
search, browse, web, internet, competitor, market research

### Mapping Logic Examples

**Amplitude MCP detected** →
- Category: Analytics (keywords: analytics, metrics, events, funnel, cohort)
- Maps to: feature-metrics, impact-sizing, retention-analysis, activation-analysis, feature-results, metrics-framework, experiment-metrics

**Linear MCP detected** →
- Category: Project Management (keywords: issues, projects, tickets)
- Maps to: create-tickets, meeting-notes, status-update, prioritize

**Dovetail MCP detected** →
- Category: Research + Transcription (keywords: research, interviews, transcripts, insights)
- Maps to: user-interview, user-research-synthesis, interview-guide, meeting-notes

## Update Patterns & Templates

### Skill File Update Template

```markdown
### Using [MCP Name] (If Connected)

[1-2 sentence description of what this MCP provides]

**Available Tools:**
- `tool_name` - [Brief description]
- `tool_name_2` - [Brief description]

**Integration Example:**
```pseudocode
# [Example showing typical usage in this skill's context]
[tool_name].method({
  param1: value1,
  param2: value2
})
```

**Benefits:**
- [Benefit 1 - e.g., Real-time data access]
- [Benefit 2 - e.g., No manual exports needed]

**Fallback:** [What happens when MCP not available - e.g., "Upload CSV data to context-library/metrics/ for manual analysis"]
```

### Insertion Point Logic

1. **If "Prerequisites" section exists** → Insert immediately after
2. **If "How It Works" section exists** → Insert immediately after
3. **Otherwise** → Insert after title and frontmatter, before main content

This ensures MCP integration info appears early but doesn't interrupt the skill's primary instructions.

### CLAUDE.md Registry Format

**Registry Table:**
```markdown
| MCP | Purpose | Category | Used In | Key Tools |
|-----|---------|----------|---------|-----------|
| Amplitude | Product analytics | Analytics | feature-metrics, impact-sizing, retention-analysis | query_insights, get_funnels, cohort_analysis |
| Linear | Project management | PM Tools | create-tickets, meeting-notes, status-update | create_issue, update_issue, search_issues |
| Dovetail | User research | Research | user-interview, user-research-synthesis | search_insights, get_themes, export_quotes |
```

**Routing Logic:**
```markdown
**Analytics Queries** → Analytics MCPs (Amplitude, Mixpanel, Posthog)
- Pattern: "give me metrics on X", "show funnel for Y", "retention for Z"
- Multi-MCP: Ask user which tool to use
- Fallback: Check context-library/metrics/

**Task Queries** → PM MCPs (Linear, Jira)
- Pattern: "show my tasks", "create ticket for X", "status of epic Y"
- Multi-MCP: Ask user which tool to use
- Fallback: Check context-library/meetings/ for action items
```

## Example Integrations

### Example 0: Figma (Design - Remote MCP Server) ⭐ RECOMMENDED METHOD

```
User: /connect-mcps connect to figma

Me:
Let me help you connect Figma to your PM OS workspace.

[Searches: "Figma official MCP server"]
[Finds: https://developers.figma.com/docs/figma-mcp-server/]

✅ **Great news! Figma has an official remote MCP server.**

**This is the easiest method:**

1. Run this command in your terminal:
   ```bash
   claude mcp add --transport http figma https://mcp.figma.com/mcp
   ```

2. After adding, type `/mcp` in Claude Code

3. You'll see Figma in your MCP list (disconnected)

4. Press Enter on Figma to log in with your Figma account

5. Authenticate and you're done!

**No API keys needed, no OAuth setup, just authenticate and go.**

**Once connected, you can:**
- "Get the latest version of the checkout flow from Figma"
- "Export the mobile mockups from our design file"
- "Show me feedback comments on the dashboard design"
- "What components are in our design system?"

Full documentation: https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/
```

---

### Example 1: Amplitude (Analytics)

```
User: /connect-mcps connect to amplitude

Me:
Let me help you connect Amplitude to your PM OS workspace.

[Searches: "Amplitude MCP server documentation 2026"]
[Finds: GitHub repo, NPM package, setup guide]

**To connect Amplitude, I need:**
1. Amplitude API Key (Settings → API Keys)
2. Project ID (Settings → Projects)

Find these at: https://analytics.amplitude.com/settings

**Enter your Amplitude API Key:**

User: [pastes: ak_live_abc123...]

Me: **Enter your Project ID:**

User: [pastes: 12345]

Me:
Testing connection... ✓ Connected successfully!

**Discovered Amplitude tools:**
- `query_insights` - Query product analytics data
- `get_funnels` - Retrieve funnel analysis
- `cohort_analysis` - Analyze user cohorts
- `event_tracking` - Track custom events
- `user_properties` - Get user property data

**Category:** Analytics

**Integrating with PM OS skills...**
✓ feature-metrics updated
✓ impact-sizing updated
✓ retention-analysis updated
✓ activation-analysis updated
✓ feature-results updated
✓ metrics-framework updated
✓ experiment-metrics updated

**Updating CLAUDE.md registry...**
✓ MCP registry table updated
✓ Query routing logic updated

**Amplitude connected! 🎉**

You can now ask analytics questions in natural language:

Examples:
- "Give me metrics on the checkout feature in the last 2 weeks"
- "Show me the funnel for user onboarding"
- "What's the retention rate for users who signed up in December"
- "Compare conversion rates between mobile and web"

I'll automatically query Amplitude and return the data with insights.

Full log: outputs/mcp-integration-logs/2026-01-30-amplitude.md
```

### Example 2: Linear (Project Management)

```
User: /connect-mcps connect to linear

Me:
Let me help you connect Linear to your PM OS workspace.

[Searches: "Linear MCP server documentation 2026"]

**To connect Linear, I need:**
1. Linear API Key (Settings → API → Personal API Keys)
2. Team ID (optional, for team-specific queries)

Find your API key at: https://linear.app/settings/api

**Enter your Linear API Key:**

User: [pastes: lin_api_...]

Me: **Enter your Team ID (or press Enter to skip):**

User: [presses Enter]

Me:
Testing connection... ✓ Connected successfully!

**Discovered Linear tools:**
- `create_issue` - Create new issues/tickets
- `update_issue` - Update existing issues
- `search_issues` - Search and filter issues
- `get_team_issues` - Get all team issues
- `create_project` - Create projects/epics

**Category:** Project Management

**Integrating with PM OS skills...**
✓ create-tickets updated
✓ meeting-notes updated
✓ status-update updated
✓ prioritize updated

**Updating CLAUDE.md registry...**
✓ MCP registry updated
✓ Query routing logic updated

**Linear connected! 🎉**

You can now manage tasks naturally:

Examples:
- "Show my open tickets"
- "Create a ticket for the login bug"
- "What's the status of the redesign project"
- "Update ticket LIN-123 to mark it as done"

I'll automatically query Linear and perform operations.

Full log: outputs/mcp-integration-logs/2026-01-30-linear.md
```

### Example 3: Batch Connection

```
User: /connect-mcps batch

Me:
Let's connect multiple MCPs at once.

**Common PM tools:**
- Analytics: Amplitude, Mixpanel, Posthog, Pendo
- Project Management: Linear, Jira
- Research: Dovetail
- Documentation: Notion
- Communication: Slack

**Which tools would you like to connect?** (comma-separated)

User: amplitude, linear, notion

Me:
I'll connect these 3 MCPs. Starting with Amplitude...

**1/3: Amplitude**
To connect Amplitude, I need:
1. API Key (Settings → API Keys)
2. Project ID (Settings → Projects)

Enter your Amplitude API Key:

[... continues with guided setup for each tool ...]

**All 3 MCPs connected! 🎉**

Summary:
✓ Amplitude (Analytics) - 7 skills updated
✓ Linear (PM Tools) - 4 skills updated
✓ Notion (Documentation) - 3 skills updated

You can now:
- Ask analytics questions → I'll query Amplitude
- Manage tasks → I'll use Linear
- Access docs → I'll search Notion

Full logs saved to: outputs/mcp-integration-logs/2026-01-30-batch/
```

## Natural Language Query Routing (After Setup)

Once MCPs are connected, you can ask questions naturally and I'll route them automatically.

### Example: Analytics Query

```
User: Give me metrics on the login feature in the last 2 weeks

Me:
[Checks CLAUDE.md registry]
[Finds: Amplitude connected for analytics]
[Routes to: Amplitude MCP query_insights tool]

**Login Feature Metrics (Last 2 Weeks)**
Source: Amplitude

📊 **Volume:**
- Total logins: 45,832
- Unique users: 12,443
- Sessions with login: 38,291

✅ **Success Rate: 94.2%**
- Successful logins: 43,174
- Failed attempts: 2,658 (5.8%)

⏱️ **Performance:**
- Average time to login: 3.2 seconds
- Median time: 2.8 seconds

📈 **Trends (vs previous 2 weeks):**
- Login volume: +12% ↑
- Success rate: +2.1% (was 92.1%) ↑
- Avg time: -0.4s (faster) ↑

🔍 **Insights:**
- Mobile login success rate (91.3%) is 5.5% lower than web (96.8%)
- Password reset requests up 8% - may indicate login friction
- Peak login times: 9-10 AM and 2-3 PM

**Want me to:**
- Dig into mobile vs web differences?
- Analyze failed login reasons?
- Compare to last month?
```

### Example: Multi-MCP Disambiguation

```
User: Show me the checkout funnel

Me:
I found 2 analytics tools connected: Amplitude and Mixpanel.

Which one should I use for this query?
A) Amplitude
B) Mixpanel

User: A

Me:
[Queries Amplitude for funnel data]

**Checkout Funnel (Last 30 Days)**
Source: Amplitude

1. **Add to cart** → 25,432 users (100.0%)
2. **View cart** → 18,901 users (74.3%) ↓ 25.7% drop-off
3. **Enter payment** → 14,223 users (55.9%) ↓ 24.8% drop-off
4. **Complete purchase** → 11,887 users (46.7%) ↓ 16.4% drop-off

**Overall Conversion Rate: 46.7%**

**Biggest Drop-offs:**
1. Add to cart → View cart (25.7%)
2. View cart → Enter payment (24.8%)

**Segments:**
- New users: 38.2% conversion
- Returning users: 52.1% conversion
- Mobile: 41.3% conversion
- Web: 49.8% conversion

Want me to analyze why users drop off at specific steps?
```

### Example: Task Management Query

```
User: Show my open tasks in Linear

Me:
[Checks registry: Linear connected]
[Queries Linear: get_team_issues filtered by assignee]

**Your Open Tasks (8 total)**
Source: Linear

**High Priority (2):**
- LIN-234: Fix login bug on mobile Safari (Due: Tomorrow)
- LIN-189: Review Q1 metrics dashboard (Due: Friday)

**Medium Priority (4):**
- LIN-267: User interview synthesis
- LIN-255: Update PRD for checkout redesign
- LIN-241: Competitive analysis - payment flows
- LIN-228: Roadmap planning for H2

**Low Priority (2):**
- LIN-201: Document API endpoints
- LIN-177: Update team wiki

Want me to:
- Create tickets from our conversation?
- Update status of any tickets?
- Show details for a specific ticket?
```

## Error Handling & Edge Cases

### Common Issues & Solutions

**1. MCP Documentation Not Found**
```
Me: I couldn't find setup documentation for [tool] MCP.

Do you have a link to the documentation or know the setup requirements?

User: [provides link or details]

Me: [proceeds with setup using provided info]
```

**2. Invalid Credentials**
```
Me: Connection test failed. The API key appears to be invalid.

Please double-check:
- API key is copied completely (no extra spaces)
- API key has required permissions
- API key hasn't expired

Want to try again? Enter your API key:
```

**3. MCP Already Connected**
```
User: /connect-mcps connect to amplitude

Me: Amplitude is already connected!

Current configuration:
- Category: Analytics
- Tools: query_insights, get_funnels, cohort_analysis
- Used in: 7 skills

Want to:
- Test connection (verify it still works)
- Reconfigure (update credentials)
- View integration details
```

**4. Skill File Read-Only**
```
Me: ⚠️ Warning: Couldn't update feature-metrics skill (file locked)

I'll continue with other skills and log this issue.

14 out of 15 skills updated successfully.

Check: outputs/mcp-integration-logs/[timestamp]-errors.md
```

**5. Ambiguous Category**
```
Me: I found [tool] MCP but I'm unsure which category it fits.

The tool appears to handle:
- Feature flagging
- A/B testing
- Analytics

Which PM OS skills should integrate with this MCP?
A) Analytics skills (metrics, retention, experiments)
B) Product skills (PRD, decisions)
C) Both A and B

User: C

Me: [maps to both skill groups]
```

## Pro Tips

1. **Connect MCPs during initial setup** - The first-time workspace setup will prompt you to connect your tools. Do it then for a seamless experience.

2. **Use natural language after setup** - Don't think about which MCP to call. Just ask your question naturally and I'll figure out the routing.

3. **Batch connect if you can** - If you're setting up multiple tools, use `/connect-mcps batch` to go through them all at once.

4. **Test with simple queries first** - After connecting, try a simple query like "show me X" to verify the connection works before complex queries.

5. **Keep credentials handy** - Have your API keys and workspace IDs ready before running `/connect-mcps connect to [tool]` to speed up setup.

6. **Check the integration log** - Each connection creates a log in `outputs/mcp-integration-logs/` with full details about what was updated.

7. **MCPs are optional** - If an MCP isn't connected, skills will gracefully fall back to manual workflows (e.g., "Upload CSV to context-library/metrics/").

8. **Re-run `/connect-mcps connect` to update** - If credentials change or expire, just run the connect command again to reconfigure.

9. **Check CLAUDE.md registry** - View `CLAUDE.md` → "MCP Integrations" section to see all connected MCPs and routing logic.

10. **Skills auto-update** - When you connect an MCP, relevant skills are automatically updated with integration instructions. No manual work needed.

## Common Mistakes to Avoid

❌ **Don't paste credentials in chat without the prompt** - Wait for me to explicitly ask for your API key. Don't volunteer it unprompted.

❌ **Don't skip the tool name** - Use `/connect-mcps connect to amplitude`, not just `/connect-mcps amplitude` or `/connect-mcps connect amplitude`.

❌ **Don't connect before installing** - Install the MCP server locally first (via NPM, Docker, etc.), then run `/connect-mcps connect to [tool]`.

❌ **Don't assume immediate availability** - After connecting, I'll tell you it's ready. Don't start querying until you see the success message.

❌ **Don't manually edit CLAUDE.md** - Let me update the registry automatically. Manual edits can break the routing logic.

❌ **Don't connect duplicate MCPs** - If you already have Amplitude connected, don't run `/connect-mcps connect to amplitude` again unless you're reconfiguring.

❌ **Don't ignore errors** - If connection fails, read the error message. It usually tells you exactly what's wrong (expired key, wrong format, etc.).

❌ **Don't use both individual and batch modes together** - Pick one. Use individual for one tool, batch for multiple. Don't mix them in the same command.

❌ **Don't forget to check prerequisites** - Some MCPs require specific permissions or scopes on the API key. Check the tool's documentation.

❌ **Don't skip the fallback** - Even with MCPs connected, keep some exported data in `context-library/` as backup for offline work.

## Troubleshooting

### "I couldn't find documentation for [tool] MCP"

**Solution:** The tool may not have an official MCP server yet. Check:
- The tool's official docs for MCP support
- GitHub for community MCP implementations
- The Anthropic MCP directory

If no MCP exists, you can still use the tool manually and store outputs in `context-library/`.

### "Connection test failed"

**Solution:**
1. Verify credentials are correct (no typos, no extra spaces)
2. Check API key hasn't expired
3. Confirm API key has required permissions/scopes
4. Test the API key in the tool's web interface first
5. Check for network/firewall issues blocking MCP server

### "Skills weren't updated"

**Solution:**
1. Check the integration log in `outputs/mcp-integration-logs/`
2. Look for error messages indicating which skills failed
3. Verify skill files aren't read-only or locked
4. Re-run `/connect-mcps connect to [tool]` to retry updates

### "Queries aren't routing to my MCP"

**Solution:**
1. Check `CLAUDE.md` → "MCP Integrations" → Verify MCP is listed
2. Verify routing logic includes your MCP category
3. Try being more explicit: "Use Amplitude to show me metrics on X"
4. Check if MCP connection is still active (test with simple query)

### "I want to disconnect an MCP"

**Solution:** Currently, to disconnect:
1. Remove the MCP from your system (uninstall server/remove credentials)
2. Edit `CLAUDE.md` to remove the MCP from the registry table
3. Optionally, remove MCP sections from skill files

(Future enhancement: `/mcp disconnect [tool]` command)

---

## Recommended PM Tools to Connect

Based on real PM workflows, here's which MCPs provide the highest value. Start with Priority Tier, then add others as needed.

### Priority Tier: Must-Have MCPs ⭐⭐⭐⭐⭐

Connect these first. They provide immediate ROI for product managers.

#### 1. Analytics Tools (Amplitude, Mixpanel, Posthog, Pendo)

**Why connect:** Self-serve analytics without waiting on data team. Ask questions and get answers in seconds.

**What you can do:**
- "What's the funnel conversion rate for onboarding?"
- "Show me retention by signup cohort for last quarter"
- "Which features correlate with power user behavior?"
- "Pull session recordings for users who churned last week"

**Setup:** Run `/connect-mcps connect to amplitude` (or your analytics tool)

**Tools discovered:** query_insights, get_funnels, cohort_analysis, event_tracking, session_replays

**Best for:** Feature performance analysis, A/B test results, user behavior research

---

#### 2. Project Management (Linear, Jira, Asana)

**Why connect:** Batch create tickets from meeting notes. Generate sprint reports. Track engineering progress without tab-switching.

**What you can do:**
- "Take these action items and create Linear tickets"
- "Show completed tickets from current sprint"
- "List all blocked tickets and their reasons"
- "Update ticket LIN-123 to mark it as done"

**Setup:** Run `/connect-mcps connect to linear` (or your PM tool)

**Tools discovered:** create_issue, update_issue, search_issues, get_project_status

**Best for:** Meeting follow-ups, sprint planning, progress tracking

---

#### 3. Communication (Slack, Microsoft Teams)

**Why connect:** Share analysis summaries. Search past decisions. Draft announcements without leaving Claude.

**What you can do:**
- "Summarize this week's work and post to #engineering-updates"
- "Search Slack for conversations about pricing from last month"
- "Draft an announcement for the feature launch"
- "Find the decision about API versioning we discussed"

**Setup:** Run `/connect-mcps connect to slack`

**Tools discovered:** read_channels, post_message, search_history, manage_threads

**Best for:** Team updates, decision archaeology, communication drafts

---

#### 4. Documentation (Notion, Confluence, Google Drive)

**Why connect:** Access PRDs and specs. Create documents from templates. Search institutional knowledge.

**What you can do:**
- "Search my Drive for customer interview notes from Q3"
- "Create a PRD for dark mode and save to Product Docs"
- "Read the Q4 roadmap and summarize key themes"
- "Update the onboarding guide with new screenshots"

**Setup:** Run `/connect-mcps connect to notion` (or your docs tool)

**Tools discovered:** read_pages, create_document, search_workspace, update_pages

**Best for:** Document creation, knowledge search, team alignment

---

### High Value Tier: Very Useful ⭐⭐⭐⭐

Not required day one, but add these once core setup is done.

#### 5. Design Tools (Figma, Sketch)

**Why connect:** Reference designs in conversations. Extract specs from mockups. Track design feedback.

**What you can do:**
- "Summarize feedback on the new dashboard design"
- "Export the mobile mockups as PNGs"
- "What's the latest version of the checkout flow?"

**Setup:** Run `/connect-mcps connect to figma`

**Best for:** Design review, spec extraction, version tracking

---

#### 6. Calendar (Google Calendar, Outlook)

**Why connect:** Analyze time allocation. Schedule research sessions. Find focus time patterns.

**What you can do:**
- "Analyze my calendar this week - where did I spend time?"
- "Find a 1-hour slot for user interviews next week"
- "Create recurring 1:1s with my reports"

**Setup:** Run `/connect-mcps connect to google-calendar`

**Best for:** Time management, meeting scheduling, calendar analysis

---

#### 7. Code Repository (GitHub, GitLab)

**Why connect:** Track engineering progress. Review technical discussions. Understand implementation details.

**What you can do:**
- "What PRs were merged in the mobile repo this week?"
- "Summarize the discussion in issue #234 about performance"
- "Create a PR to update the API documentation"

**Setup:** Run `/connect-mcps connect to github`

**Best for:** Engineering collaboration, progress tracking, technical context

---

### Specialized Tier: Niche But Powerful ⭐⭐⭐

For specific workflows or advanced users.

#### 8. Customer Support (Zendesk, Intercom)

**What you can do:**
- Analyze support tickets for patterns
- Find common user issues
- Track resolution times
- Identify bug clusters

**Setup:** Run `/connect-mcps connect to zendesk`

**Best for:** Support insights, bug prioritization, customer pain points

---

#### 9. Revenue Tools (Stripe, ChartMogul)

**What you can do:**
- Analyze subscription trends
- Track MRR changes
- Identify churn patterns
- Monitor payment issues

**Setup:** Run `/connect-mcps connect to stripe`

**Best for:** Revenue analysis, subscription health, payment insights

---

#### 10. Social Listening (Twitter/X, Reddit)

**What you can do:**
- Monitor competitor mentions
- Analyze user sentiment
- Find feature requests in the wild
- Track industry trends

**Setup:** Run `/connect-mcps connect to reddit`

**Best for:** Competitive intelligence, user research, trend spotting

---

### Choosing Your Stack

**For Solo PM:**
- Analytics + Project Management + Slack + Docs
- Setup time: 30-45 minutes
- Covers 80% of daily workflows

**For PM Team:**
- Solo stack + Design + Calendar + GitHub
- Setup time: 1-2 hours
- Full workflow coverage

**For PM Leader:**
- Team stack + Support + Revenue tools
- Setup time: 2-3 hours
- Complete analytics and insights

**Pro tip:** Start small. Add one MCP at a time as you discover needs. More MCPs ≠ better.

---

### Setup Difficulty Guide

**Easy (5-10 min):**
- Linear, Jira: API token only
- Slack: Workspace token
- GitHub: Personal access token

**Medium (10-20 min):**
- Amplitude, Mixpanel: API key + Project ID
- Notion: Integration setup required
- Figma: OAuth flow

**Advanced (20-30 min):**
- Google Drive: OAuth + permission scopes
- Database tools: Credentials + read-only setup
- Calendar: OAuth + calendar selection

---

### Analytics Tool Details

Since analytics is the #1 requested integration, here's the specifics:

**PostHog MCP**
- Official server: `@anthropic/posthog-mcp`
- What you need: API key, host URL (US/EU/self-hosted)
- Tools: Insights, funnels, experiments, feature flags, session replays
- Query language: SQL-like HogQL
- Best for: Self-hosted analytics, session replay analysis

**Amplitude MCP**
- Official server: `@anthropic/amplitude-mcp`
- What you need: API key, Project ID
- Tools: Insights, funnels, cohorts, user profiles
- Query language: AQL (Amplitude Query Language)
- Best for: Behavioral analytics, cohort analysis

**Mixpanel MCP**
- Community server: `mcp-server-mixpanel`
- What you need: Project token, API secret
- Tools: Events, funnels, flows, retention
- Query language: JQL (Mixpanel JSON Query Language)
- Best for: Event-based analytics, user flows

**Pendo MCP**
- Beta status: Check Pendo docs for latest
- What you need: API key, subscription key
- Tools: Product usage, guides, NPS scores
- Best for: Product adoption analytics

**Common Analytics Queries:**
```
"What's our week-over-week active user growth?"
"Show me the conversion funnel for checkout"
"Which features have the highest correlation with retention?"
"Pull session recordings where users encountered errors"
"Create a cohort of power users who logged in 10+ times"
"What's the statistical significance of our pricing experiment?"
```

---

### Maintenance Tips

**Weekly:**
- Test critical integrations with simple queries
- Check MCP logs for errors (if issues arise)
- Update API tokens if expiring soon

**Monthly:**
- Update MCP servers to latest versions (`npm update`)
- Review permissions and access scopes
- Remove MCPs you haven't used

**Quarterly:**
- Evaluate new MCP releases
- Assess ROI of each integration
- Optimize configuration for performance

**Signs you need to update:**
- Connection errors or timeouts
- Missing tools that should be available
- Slow response times
- Authentication failures

---

### Security Best Practices

**API Keys:**
- Use read-only credentials whenever possible
- Store keys in environment variables, never in code
- Rotate keys quarterly or when team members leave
- Never share keys in Slack or email

**Permissions:**
- Grant minimum required scopes
- Audit access regularly
- Use separate keys for prod vs staging
- Revoke unused tokens immediately

**Data Privacy:**
- Don't query PII unless necessary
- Be mindful of GDPR/data regulations
- Use aggregated data when possible
- Don't export sensitive user data to logs

---

### Getting Help

**When MCP connection fails:**
1. Check API key is correct (no typos, extra spaces)
2. Verify token hasn't expired
3. Confirm required permissions are granted
4. Test the API key in the tool's web interface first
5. Check network/firewall isn't blocking MCP server

**Resources:**
- **MCP Documentation:** https://modelcontextprotocol.io
- **Anthropic Forums:** https://discuss.anthropic.com
- **GitHub Issues:** https://github.com/modelcontextprotocol/servers
- **Community Discord:** MCP Community server

**For PM-specific help:**
- Check `outputs/mcp-integration-logs/` for detailed error messages
- Ask in chat: "Why did my Amplitude connection fail?"
- Reference CLAUDE.md → MCP Integrations section for routing logic

---

## What Happens Behind the Scenes

When you run `/connect-mcps connect to amplitude`:

1. **I search the web** for Amplitude MCP documentation
2. **I parse** the results to extract setup requirements
3. **I prompt you** for each required credential
4. **I test** the connection to verify it works
5. **I discover** available tools by querying the MCP
6. **I categorize** the MCP (Analytics) based on keywords
7. **I map** to relevant skills (feature-metrics, impact-sizing, etc.)
8. **I read** each skill file to find insertion points
9. **I add** MCP integration sections to each skill
10. **I update** CLAUDE.md with registry entry and routing logic
11. **I create** an integration log with full details
12. **I confirm** success and show you how to use it

All of this happens automatically in seconds. You just provide credentials and I handle the rest.

---

**Ready to connect your first MCP? Try:**

```
/connect-mcps connect to [your analytics tool]
```

And I'll guide you through the rest!

---

## Output Quality Self-Check

Before confirming an MCP connection is complete, verify:

- [ ] **Connection tested successfully** -- A simple query returned valid results (not just "connected" status)
- [ ] **Tools discovered and documented** -- Available MCP tools are listed with descriptions
- [ ] **Category correctly assigned** -- MCP is mapped to the right category (Analytics, PM, Research, etc.)
- [ ] **Relevant skills updated** -- All skills that benefit from this MCP have integration sections added
- [ ] **CLAUDE.md registry updated** -- MCP appears in the registry table with purpose, category, used-in skills, and key tools
- [ ] **Routing logic updated** -- Natural language query patterns are mapped to this MCP in CLAUDE.md
- [ ] **Integration log saved** -- Detailed log written to `outputs/mcp-integration-logs/[timestamp]-[tool].md`
- [ ] **Fallback documented** -- Skills note what to do when this MCP is unavailable
- [ ] **No duplicate entries** -- MCP is not listed twice in registry or skill files
- [ ] **PM knows how to use it** -- Example natural language queries provided so the PM can start using the MCP immediately

If any check fails, fix it before declaring success. A half-connected MCP causes confusion when skills try to use it.
