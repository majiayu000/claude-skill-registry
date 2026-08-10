---
name: note-taking
description: Capture, organize, and retrieve notes efficiently using structured formats, tagging, and file management for meetings, ideas, research, and daily logs. Use when the user requests note taking or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Note-Taking

This skill enables an AI agent to manage a complete note-taking workflow: creating structured notes, appending to existing ones, organizing notes with tags and categories, searching and retrieving notes by topic, and synthesizing notes into summaries. Notes are stored as Markdown files in a configurable directory, following naming conventions that enable easy browsing and retrieval. The skill supports various note types including meeting notes, daily logs, research notes, idea capture, and project documentation.

## Workflow

1. **Determine the Note Type and Structure:** Based on the user's request, identify the appropriate note type — meeting notes, idea capture, research notes, daily log, or project notes. Each type has a recommended template with relevant sections (e.g., meeting notes include attendees, agenda, discussion, action items; research notes include source, key findings, questions).

2. **Create or Locate the Note:** Check if a relevant note already exists by searching the notes directory by filename and content. If the user wants to add to an existing topic, open and append to that note. If it is a new topic, create a new file with a descriptive, date-prefixed filename (e.g., `2026-02-12-sprint-planning.md`).

3. **Write Structured Content:** Format the note content using clear Markdown: headings for sections, bullet points for lists, checkboxes for action items, and bold text for key terms. Include metadata at the top (date, tags, related notes) to enable future retrieval.

4. **Organize with Tags and Links:** Add tags to the note's metadata to enable filtering by topic, project, or type. Where relevant, add links to related notes to build a connected knowledge base.

5. **Retrieve and Synthesize:** When the user asks for information, search notes by filename, tags, or content. For broad queries ("What did we discuss about authentication this month?"), synthesize relevant notes into a summary rather than returning raw file contents.

## Usage

Tell the agent what kind of note to take, and provide the content. The agent will create or update the appropriate file.

```
Create meeting notes for today's sprint planning with the Backend Team.
Attendees: Alice, Bob, Carol. We discussed the v2.1 release timeline,
assigned the payment bug to Bob, and decided to defer dark mode to v2.2.
```

## Examples

### Example 1: Meeting Notes with Action Items

**User Request:**
> Take notes for today's design review meeting.
> Attendees: Sarah (design lead), Tom (frontend), Lisa (PM).
> We reviewed the new dashboard mockups. Sarah presented three layout options.
> The team chose Option B (sidebar navigation). Tom raised a concern about
> mobile responsiveness — we need to test on tablets. Lisa confirmed the
> deadline is March 1. Action items: Tom will build a responsive prototype
> by Feb 20. Sarah will update the design system with the new nav component.
> Lisa will schedule a follow-up review for Feb 25.

**Agent creates file:** `notes/2026-02-12-design-review.md`

**File content:**
```markdown
---
date: 2026-02-12
type: meeting
tags: [design, dashboard, ui]
attendees: [Sarah, Tom, Lisa]
related: []
---

# Design Review — Dashboard Redesign

**Date:** 2026-02-12
**Attendees:** Sarah (design lead), Tom (frontend), Lisa (PM)

## Discussion

- Sarah presented three layout options for the new dashboard.
- **Decision:** Team selected **Option B** — sidebar navigation layout.
- Tom raised a concern about mobile responsiveness, particularly on tablets.
- Lisa confirmed the ship deadline: **March 1, 2026**.

## Action Items

- [ ] **Tom** — Build a responsive prototype of Option B by Feb 20
- [ ] **Sarah** — Update the design system with the new sidebar nav component
- [ ] **Lisa** — Schedule follow-up design review for Feb 25

## Open Questions

- How does the sidebar behave on tablet screen sizes (768px-1024px)?
- Should we support a collapsed sidebar state for smaller viewports?
```

---

### Example 2: Research Notes with Source Tracking

**User Request:**
> I'm researching connection pooling strategies for PostgreSQL. Take notes on what I've found so far:
> PgBouncer is the most popular external pooler — supports session, transaction, and statement pooling modes. Transaction mode is recommended for most web apps because it reuses connections between transactions, typically reducing connection count by 10x. But it doesn't support prepared statements in transaction mode, which breaks some ORMs. Pgpool-II is an alternative that also does load balancing and replication but is more complex to configure. The built-in Postgres connection limit is usually 100 by default. Supabase published a blog post showing they handle 1M+ connections using PgBouncer in transaction mode with Supavisor.

**Agent creates file:** `notes/2026-02-12-postgres-connection-pooling.md`

**File content:**
```markdown
---
date: 2026-02-12
type: research
tags: [postgresql, connection-pooling, database, infrastructure]
related: []
---

# PostgreSQL Connection Pooling Strategies

## Key Findings

### PgBouncer
- **Most popular** external connection pooler for PostgreSQL.
- Three pooling modes: session, transaction, and statement.
- **Transaction mode** is recommended for web applications — reuses connections between transactions.
- Typically **reduces connection count by ~10x**.
- **Limitation:** Transaction mode does not support prepared statements, which can break some ORMs (notably older versions of ActiveRecord and SQLAlchemy).

### Pgpool-II
- Alternative to PgBouncer with additional features: load balancing, automatic failover, and replication.
- **More complex** to configure and operate than PgBouncer.
- Better suited for setups that need read replica routing in addition to pooling.

### Built-in PostgreSQL Limits
- Default `max_connections` is **100**.
- Increasing this significantly (e.g., to 1000+) causes memory and performance issues due to per-connection overhead.

### Production Scale Reference
- **Supabase** handles 1M+ connections using PgBouncer (transaction mode) with their custom Supavisor proxy.
- Source: Supabase engineering blog.

## Open Questions

- What is the performance overhead of PgBouncer itself at high connection counts?
- How do modern ORMs (Prisma, Drizzle) handle the prepared statement limitation in transaction mode?
- When does Pgpool-II's complexity become justified over PgBouncer?

## Sources

- Supabase Blog: "Scaling Postgres to 1M connections"
- PgBouncer documentation: https://www.pgbouncer.org/
- PostgreSQL documentation: Connection settings
```

## Best Practices

- **Use consistent naming conventions.** Prefix all note files with the ISO date (`YYYY-MM-DD-topic.md`) to enable chronological sorting and prevent filename collisions.
- **Include metadata in every note.** Tags, date, type, and related-note links in YAML frontmatter make notes searchable and connected. A note without metadata is hard to find later.
- **Capture action items as checkboxes.** Use Markdown checkboxes (`- [ ]`) with a bolded assignee name so action items are easy to scan and track to completion.
- **Write notes in the user's voice, not yours.** The agent should capture the user's ideas and decisions faithfully, not inject its own opinions or rephrase in ways that change meaning.
- **Link related notes.** When creating a note on a topic that connects to an existing note, add a cross-reference in the `related` field. This builds an organic knowledge graph over time.
- **Summarize on retrieval, don't dump raw files.** When a user asks "What were our decisions about the dashboard?", synthesize the relevant notes into a concise answer rather than returning the full text of every matching file.

## Edge Cases

- **Overlapping or duplicate notes:** If the user creates a note on a topic that already has an existing note, check the existing content first. Offer to append to the existing note rather than creating a duplicate. If the user wants both, ensure filenames are distinct.
- **Very long meeting notes:** For meetings lasting 1+ hours with extensive discussion, structure the note with clear section headings and consider creating a summary section at the top. Notes over 200 lines should be broken into sections that can be read independently.
- **Notes with sensitive information:** If notes contain passwords, API keys, or personal data, warn the user and recommend against storing them in plain-text Markdown files. Suggest using a secrets manager for credentials and redacting sensitive fields in notes.
- **Ambiguous retrieval requests:** When the user asks for notes on a broad topic (e.g., "database stuff"), search by both tags and content, present the matches, and ask the user to narrow down rather than guessing which note they want.
- **Notes directory not initialized:** If the notes directory does not exist on first use, create it automatically with a `README.md` explaining the directory structure and conventions. Do not fail silently.
- **Conflicting action items across notes:** When synthesizing multiple meeting notes, check for conflicting or superseded action items (e.g., "defer dark mode" in one meeting, "start dark mode" in a later one). Present the most recent decision and note the change.
