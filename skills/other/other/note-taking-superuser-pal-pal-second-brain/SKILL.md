---
name: note-taking
description: Manage notes with semantic structure and knowledge graph. USE WHEN process notes OR organize notes OR add frontmatter OR distribute notes OR ingest PDF OR ingest document OR convert document OR inbox notes OR note management OR scan inbox OR move notes to domain OR braindump OR brain dump OR capture thoughts OR dump thoughts OR url dump OR save link OR bookmark url OR capture url OR save for later OR categorize observations OR add relations OR link notes OR knowledge graph OR export life summary OR life report OR generate life summary.
user-invocable: false
---

# note-taking

Unified note management skill with semantic structure (observation categories, entity types, relation types) that transforms flat notes into a connected knowledge graph inside Obsidian.

## Semantic Features

- **Observation Categories** (10 types): fact, idea, decision, technique, requirement, question, insight, problem, solution, action
- **Entity Types** (12 types): concept, decision, reference, meeting, idea, note, belief, frame, lesson, model, goal, plan
- **Relation Types** (10 types): part_of, supports, contradicts, evolved_from, informs, blocks, inspired_by, relates_to, originated_with, follows
- **Dedup Check**: Detects similar notes before creating duplicates
- **Action Extraction**: Automatically creates tasks from `[action]` observations
- **Multi-Theme Splitting**: Braindumps with distinct themes can split into separate notes

## Note Substantiality Rules

Thresholds for determining if a note warrants a standalone page:

**Minimum thresholds:**
- **Word count:** >= 50 words (excluding frontmatter)
- **Observations:** >= 3 structured observations
- **Logic:** Note must meet BOTH thresholds to be substantial

**Special cases:**
- Notes with only `[action]` observations → Treat as task list (extract only)
- Notes with `project: [name]` → Always substantial (project context)


**Detection triggers:**
- If `word_count < 50 AND observation_count < 3` → Flag as insubstantial
- Prompt user for routing decision during distribution

## Workflow Routing

| Workflow | Trigger | File |
| :--- | :--- | :--- |
| **braindump** | "braindump", "brain dump", "capture thoughts", "dump thoughts" | `workflows/braindump.md` |
| **process_notes** | "process inbox", "add frontmatter", "scan notes" | `workflows/process_notes.md` |
| **distribute_notes** | "distribute notes", "move notes to domains", "organize notes" | `workflows/distribute_notes.md` |
| **ingest_longform** | "ingest PDF", "convert document", "ingest document" | `workflows/ingest_longform.md` |
| **url_dump** | "url dump", "save link", "bookmark url", "capture url" | `workflows/url_dump.md` |
| **export_life_summary** | "export life summary", "life report", "generate life summary" | `workflows/export_life_summary.md` |

## Examples

**Example 1: Capture raw thoughts with braindump**
```
User: "braindump"
-> Invokes braindump workflow
-> Collects stream-of-consciousness input
-> Analyzes for themes, insights, action items
-> Domain Detection (Step 4a):
   - Scores content against all domains (PALBuilder, LifeOS, Studio, etc.)
   - Uses patterns defined in DOMAINS_REGISTRY.md (see templates/note_schema.md)
   - Confidence threshold: >= 60% triggers suggestion
-> If LifeOS detected: also runs category detection (beliefs, goals, etc.)
-> If non-LifeOS domain: sets domain, category = notes
-> If multiple domains match (>= 70%): asks user to choose
-> If no match: presents domain selection menu
-> Saves to Inbox/Notes/topic-DD-MM-YYYY.md
-> Next: distribute_notes to route to correct domain
```

**Example 2: Process raw notes in inbox**
```
User: "Process my inbox notes"
-> Invokes process_notes workflow
-> Scans Inbox/Notes/ for .md files without YAML frontmatter
-> Prompts user for domain, project, category assignment
-> Adds standardized YAML frontmatter
-> Notes ready for distribution
```

**Example 2: Distribute processed notes to domains**
```
User: "Distribute my notes to their domains"
-> Invokes distribute_notes workflow
-> Scans Inbox/Notes/ for notes with status: ready
-> Moves each note to domains/[domain]/02_PAGES/
-> Adds reference link to PROJECT_*.md if project field set
-> Leaves notes without frontmatter in place
```

**Example 3: Ingest a PDF document**
```
User: "Ingest the PDF in my ports folder"
-> Invokes ingest_longform workflow
-> Scans ports/In/ for PDF, DOCX, TXT files
-> Converts content to structured markdown
-> AI generates summary and key ideas
-> Adds YAML frontmatter with source metadata
-> Outputs to Inbox/Notes/ ready for processing
```

**Example 4: Save a URL with insights**
```
User: "save this link: https://example.com/article"
-> Invokes url_dump workflow
-> Fetches URL content via WebFetch
-> Detects content type (article vs tool)
-> Extracts key insights and summary
-> Auto-detects category (research, reference, etc.)
-> Saves to Inbox/Notes/article-title-16-02-2026.md
-> If tool detected: includes evaluation checklist
-> Next: distribute_notes to move to domain
```

**Example 5: Export life summary report**
```
User: "export life summary"
-> Invokes export_life_summary workflow
-> Reads all 7 LifeOS files (mission, beliefs, frames, models, learned, goals, projects)
-> Generates structured summary report
-> Outputs to domains/LifeOS/03_OUTPUT/life_summary_YYYY-MM-DD.md
-> Logs export to 04_SESSIONS/UPDATES.md
```

## Quick Reference

**Folder Locations:**
- Raw notes: `Inbox/Notes/`
- Document input: `ports/In/`
- Processed notes destination: `domains/[domain]/02_PAGES/`
- Project updates: `domains/[domain]/01_PROJECTS/`

**Full Documentation:**
- Note Schema: `templates/note_schema.md`
