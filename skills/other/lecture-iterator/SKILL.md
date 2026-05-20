---
name: lecture-iterator
description: Iterate on physician course lectures based on feedback. Processes written notes, voice transcripts, PDFs, and documents to make methodical, audited changes to lecture JSON files.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, mcp__google-drive__list_files, mcp__google-drive__export_google_doc, mcp__google-drive__get_file_content
user_invocable: true
argument-hint: <feedback-source> [--physician NAME] [--course NAME] [--lecture N]
---

# Physician Lecture Iterator

Methodically iterate on generated physician lectures based on feedback from physicians like Dr. Rose and Dr. Husain. Takes a Ralph-like approach: deliberate, measured, and autonomous with full audit logging.

## Overview

This skill processes physician feedback in various formats (text notes, voice transcripts, PDFs, Word documents, Google Drive files) and applies changes to lecture JSON files systematically. Each change is logged for review.

**Key Principles:**
- **Deliberate**: Parse feedback into discrete tasks before executing
- **Measured**: One change at a time with verification
- **Methodical**: Follow consistent patterns for each edit type
- **Audited**: Every change logged with before/after context

## Invocation

```bash
/lecture-iterator <feedback-source> [options]
```

**Arguments:**
- `<feedback-source>` - Feedback input (inline text, file path, or Google Drive ID)
- `--physician NAME` - Target physician slug (e.g., `dr-robin-rose`)
- `--course NAME` - Target course slug (e.g., `long-covid`)
- `--lecture N` - Target specific lecture number

**Examples:**
```bash
# Inline text feedback
/lecture-iterator "In lecture 3, the dosing for rapamycin should be 5mg weekly, not 6mg"

# File-based feedback
/lecture-iterator ./feedback/dr-rose-notes.txt

# Voice note transcript
/lecture-iterator ./transcripts/dr-husain-voice-note-2026-01-14.txt

# Google Drive file
/lecture-iterator --gdrive 1ABC123def456 --physician dr-robin-rose

# Target specific lecture
/lecture-iterator "Update the NAD+ section" --physician dr-abid-husain --course systems-cardiology-expanded --lecture 3
```

## Execution Flow

The skill follows a **Ralph-like iterative loop**:

```
┌─────────────────────────────────────────────────────────────────┐
│                     /lecture-iterator                            │
│                                                                  │
│  ┌────────────────┐   ┌────────────────┐   ┌────────────────┐  │
│  │  PHASE 1       │   │  PHASE 2       │   │  PHASE 3       │  │
│  │  Parse         │──▶│  Generate      │──▶│  Execute       │  │
│  │  Feedback      │   │  Tasks         │   │  Changes       │  │
│  └────────────────┘   └────────────────┘   └────────────────┘  │
│         │                    │                    │             │
│         ▼                    ▼                    ▼             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    AUDIT LOG                               │ │
│  │  Every action recorded with before/after context           │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Quick Start

1. **Gather feedback** from physician (notes, voice memo, annotated PDF)
2. **Invoke skill** with feedback source
3. **Review parsed tasks** (skill will show what it plans to change)
4. **Monitor execution** (autonomous with audit log)
5. **Review changelog** at completion

## When to Use This Skill

Use `/lecture-iterator` when:
- A physician has provided feedback on their course lectures
- You have corrections, additions, or restructuring requests
- Feedback spans multiple lectures in a course
- You need an audit trail of all changes made

Do NOT use when:
- Creating new lectures from scratch (use `/physician-course-builder`)
- Generating course outlines (use `/generate-outline`)
- Need simulated physician feedback (use `/physician-feedback-agent`)

## Current Physicians & Courses

| Physician | Slug | Course | Lectures |
|-----------|------|--------|----------|
| Dr. Abid Husain | `dr-abid-husain` | `systems-cardiology` | 5 |
| Dr. Abid Husain | `dr-abid-husain` | `systems-cardiology-expanded` | 15 |
| Dr. Robin Rose | `dr-robin-rose` | `long-covid` | 11 |

---

## Supported Input Formats

The skill accepts feedback in multiple formats. All formats are processed into a unified internal representation before task generation.

### 1. Inline Text Feedback

Direct text in the invocation. Best for quick, targeted corrections.

```bash
/lecture-iterator "In lecture 5, change the rapamycin dose from 6mg to 5mg weekly"
```

**Characteristics:**
- Immediate processing, no file I/O
- Best for 1-3 specific changes
- Physician/course inferred from content or requires `--physician` flag

### 2. Local File Paths

Text files, markdown, or transcripts stored locally.

```bash
# Plain text file
/lecture-iterator ./feedback/dr-rose-review-2026-01-14.txt

# Markdown notes
/lecture-iterator ./feedback/husain-course-notes.md

# Voice note transcript (from transcription service)
/lecture-iterator ./transcripts/dr-rose-voice-memo.txt
```

**Supported extensions:** `.txt`, `.md`, `.markdown`

**Reading method:** Uses `Read` tool to load file contents.

### 3. Google Drive Files

Documents stored in Google Drive, accessed via file ID.

```bash
# Using Google Drive file ID
/lecture-iterator --gdrive 1ABC123def456GHI --physician dr-robin-rose

# Alternative: full URL (ID extracted automatically)
/lecture-iterator --gdrive "https://docs.google.com/document/d/1ABC123def456GHI/edit"
```

**Supported Google formats:**
- Google Docs (exported as HTML, converted to text)
- Google Sheets (for structured feedback tables)
- Uploaded PDFs (text extraction)
- Uploaded Word documents (.docx)

**MCP Tools used:**
- `mcp__google-drive__get_file_metadata` - Verify file exists
- `mcp__google-drive__export_google_doc` - Export Google Docs as text/HTML
- `mcp__google-drive__get_file_content` - Download non-Google files

### 4. PDF Documents

PDFs are read directly using the `Read` tool which extracts text and visual content.

```bash
/lecture-iterator ./feedback/annotated-slides.pdf --physician dr-abid-husain
```

**Handling:**
- Text extraction from PDF pages
- Annotations and highlights captured where possible
- Images described for context
- Page numbers preserved for reference

### 5. Voice Note Transcripts

Transcribed audio from physician voice memos. Expects pre-transcribed text (from services like Whisper, Otter.ai, etc.).

```bash
/lecture-iterator ./voice-notes/dr-rose-2026-01-14-transcript.txt
```

**Best practices for voice transcripts:**
- Include speaker identification if multiple speakers
- Timestamps help locate specific feedback
- Clean up obvious transcription errors before processing

**Example voice transcript format:**
```
[00:00] Dr. Rose: Looking at lecture 3, the section on viral persistence...
[00:15] The mechanism diagram needs to show the spike protein binding more clearly.
[00:30] Also, can we add a clinical note about patient selection criteria?
[01:00] For lecture 4, the dosing table has an error - metformin should be 500mg BID, not TID.
```

### 6. Multi-Format Input (Combining Sources)

For comprehensive feedback sessions, combine multiple sources by invoking multiple times or referencing a manifest file.

**Sequential invocation:**
```bash
# First pass: written notes
/lecture-iterator ./feedback/dr-husain-written-notes.md --physician dr-abid-husain

# Second pass: voice additions
/lecture-iterator ./transcripts/dr-husain-followup-call.txt --physician dr-abid-husain
```

**Manifest file approach:**
Create a `.txt` file listing all feedback sources:
```
# feedback-manifest.txt
# Sources for Dr. Husain course review

./feedback/written-notes.md
./feedback/annotated-pdf.pdf
--gdrive 1ABC123def456
./transcripts/voice-memo.txt
```

Then process:
```bash
/lecture-iterator ./feedback-manifest.txt --physician dr-abid-husain
```

### Format Detection Logic

The skill automatically detects input format:

| Input Pattern | Detected Format |
|---------------|-----------------|
| Starts with `"` or `'` | Inline text |
| Ends with `.txt`, `.md` | Local text file |
| Ends with `.pdf` | PDF document |
| Contains `--gdrive` | Google Drive file |
| Starts with `http` | URL (Google Drive or web) |
| Directory path | Scan for feedback files |

### Input Validation

Before processing, the skill validates:

1. **File exists** - For local paths, verify file is readable
2. **Google auth** - For Drive files, verify MCP connection
3. **Content present** - Non-empty feedback content
4. **Target identifiable** - Physician/course can be determined

If validation fails, the skill will ask for clarification before proceeding.

---

## Phase 1: Feedback Parsing

After loading feedback content, the skill parses it into structured change requests. This is the foundation for all subsequent task generation.

### Step 1.1: Identify Target Lectures

The skill extracts lecture references from feedback using pattern matching:

**Explicit references (preferred):**
```
"In lecture 3..."
"Lecture 5, slide 2..."
"The mitochondrial lecture..."
"Update lectures 3-5..."
```

**Implicit references (context-based):**
```
"The NAD+ section needs..." → Search for NAD+ content across lectures
"Where we discuss rapamycin..." → Find rapamycin mentions
"The introduction slide..." → Match against slide titles
```

**Reference resolution priority:**
1. Command-line args (`--lecture 3`) - Highest priority
2. Explicit lecture numbers in text
3. Slide IDs or titles mentioned
4. Topic-based search across course

**Lecture reference patterns:**

| Pattern | Example | Resolution |
|---------|---------|------------|
| `lecture N` | "lecture 3" | Direct: lecture-3.json |
| `lectures N-M` | "lectures 2-4" | Range: lecture-2, 3, 4 |
| `slide about X` | "slide about glycocalyx" | Search slide titles |
| `the X section` | "the NAD+ section" | Search content |
| `where we discuss X` | "where we discuss BPC-157" | Full-text search |

### Step 1.2: Extract Change Requests

Each piece of feedback is parsed into discrete change requests. A single feedback item may contain multiple changes.

**Example parsing:**
```
Input: "In lecture 3, the rapamycin dose should be 5mg not 6mg,
        and add a clinical note about contraindications."

Parsed:
  Change 1: { type: "factual_correction", target: "lecture-3",
              find: "6mg", replace: "5mg", context: "rapamycin" }
  Change 2: { type: "add_callout", target: "lecture-3",
              callout_type: "clinicalNote", topic: "contraindications" }
```

### Step 1.3: Categorize Changes

Each change request is assigned a category that determines processing:

#### Category 1: Factual Correction
Simple text corrections for accuracy.
```
Examples:
- "Change 6mg to 5mg"
- "The year should be 2024, not 2023"
- "Dr. Smith's credential is MD, not PhD"
- "NAD+ not NAD"

Processing: Find-and-replace with context verification
Risk: Low
```

#### Category 2: Content Edit
Modifications to existing text without structural changes.
```
Examples:
- "Expand the explanation of mitochondrial dysfunction"
- "Simplify the mechanism description"
- "Add more detail about dosing protocol"
- "Clarify the patient selection criteria"

Processing: Edit content block in place
Risk: Low-Medium
```

#### Category 3: Structure Change
Adding, removing, or reordering slides or sections.
```
Examples:
- "Add a new slide on EBOO-F protocols"
- "Remove the outdated section on hydroxychloroquine"
- "Move the dosing table earlier in the lecture"
- "Split this slide into two parts"

Processing: Modify slides array, update IDs
Risk: Medium
```

#### Category 4: Diagram Update
Changes to visual elements (SVG diagrams).
```
Examples:
- "Make the pathway diagram show spike protein binding"
- "Add a fourth phase to the timeline"
- "Change colors in the comparison chart"
- "The network diagram is missing the liver node"

Processing: Edit diagramHtml SVG content
Risk: Medium-High (SVG complexity)
```

#### Category 5: Add/Remove Slide
Creating entirely new slides or deleting existing ones.
```
Examples:
- "Add a slide on patient monitoring protocols"
- "Delete the outdated drug interaction slide"
- "Insert a case study after slide 5"

Processing: Create/delete slide object, update order
Risk: Medium
```

#### Category 6: Callout Modification
Adding, editing, or removing callout boxes.
```
Examples:
- "Add a clinical note about off-label use"
- "Update the evidence callout with new citation"
- "Remove the warning - it's no longer relevant"
- "Change the pro tip to a key takeaway"

Processing: Modify callouts array
Risk: Low
```

#### Category 7: Reference Update
Changes to citations and references.
```
Examples:
- "Add the 2025 meta-analysis citation"
- "Update the PMID for the NAD+ study"
- "Remove outdated 2018 reference"

Processing: Edit references array
Risk: Low
```

### Step 1.4: Handle Ambiguous Feedback

When feedback cannot be confidently parsed, the skill pauses and asks for clarification.

**Ambiguity triggers:**

| Trigger | Example | Clarification Needed |
|---------|---------|---------------------|
| Missing target | "Update the dosing" | Which lecture? Which drug? |
| Conflicting info | "Change to 5mg" but 5mg exists | What's the current value? |
| Unclear scope | "Fix the mechanism section" | What specifically is wrong? |
| Multiple interpretations | "Make it clearer" | Clearer how? Examples? |
| Missing context | "Add Dr. Smith's protocol" | What is the protocol? |

**Clarification flow:**
```
1. Identify ambiguous element
2. Present specific question with options (AskUserQuestion)
3. Wait for response
4. Log clarification in changelog
5. Continue parsing
```

**Example clarification:**
```
Feedback: "The dosing needs to be updated"

Clarification question:
"Which dosing information needs updating?"
  A) Rapamycin (currently 6mg weekly in lecture 3)
  B) Metformin (currently 500mg BID in lecture 5)
  C) NAD+ precursors (currently 300mg NR in lecture 4)
  D) Other (please specify)
```

### Step 1.5: Generate Parsed Output

After parsing, the skill produces a structured representation:

```json
{
  "sessionId": "iter-2026-01-14-dr-rose",
  "physician": "dr-robin-rose",
  "course": "long-covid",
  "feedbackSource": "./feedback/dr-rose-notes.txt",
  "parsedAt": "2026-01-14T18:30:00.000Z",
  "changeRequests": [
    {
      "id": "CR-001",
      "category": "factual_correction",
      "target": {
        "lecture": "lecture-3",
        "slide": "viral-persistence-slide",
        "contentIndex": 2
      },
      "description": "Change rapamycin dose from 6mg to 5mg",
      "originalText": "6mg weekly",
      "newText": "5mg weekly",
      "confidence": "high",
      "source": "line 15 of feedback"
    },
    {
      "id": "CR-002",
      "category": "add_callout",
      "target": {
        "lecture": "lecture-3",
        "slide": "viral-persistence-slide"
      },
      "description": "Add clinical note about contraindications",
      "calloutType": "clinicalNote",
      "content": "TBD - will be generated during execution",
      "confidence": "medium",
      "source": "line 16 of feedback"
    }
  ],
  "clarificationsNeeded": [],
  "summary": {
    "totalChanges": 2,
    "byCategory": {
      "factual_correction": 1,
      "add_callout": 1
    },
    "lecturesAffected": ["lecture-3"]
  }
}
```

### Step 1.6: Present Parsed Summary

Before proceeding to task generation, present the parsed summary to the user:

```
FEEDBACK PARSED
━━━━━━━━━━━━━━━

Source: ./feedback/dr-rose-notes.txt
Physician: Dr. Robin Rose
Course: long-covid

Found 7 change requests:
  - 2 factual corrections
  - 3 content edits
  - 1 diagram update
  - 1 add callout

Lectures affected: 3, 4, 5

Clarifications needed: 0

Ready to generate tasks. Proceed?
```

---

## Phase 2: Task Generation

After parsing feedback into change requests, convert them into atomic, ordered tasks for execution.

### Step 2.1: Create Atomic Tasks

Each change request becomes one or more atomic tasks. A task should be completable in a single operation.

**Task template:**
```json
{
  "taskId": "T-001",
  "changeRequestId": "CR-001",
  "category": "factual_correction",
  "action": "edit_content_block",
  "target": {
    "file": "content/physician-courses/dr-robin-rose/long-covid/lecture-3.json",
    "path": "slides[2].content[1].text",
    "slideId": "viral-persistence-slide"
  },
  "operation": {
    "type": "find_replace",
    "find": "6mg weekly",
    "replace": "5mg weekly"
  },
  "priority": 1,
  "dependencies": [],
  "status": "pending",
  "riskLevel": "low"
}
```

**Atomic task rules:**
- One file modification per task (exception: related imports)
- Single logical change
- Independently verifiable
- Rollback-friendly

### Step 2.2: Prioritization Rules

Tasks are prioritized by risk and dependency order:

**Priority 1: Safety & Accuracy (CRITICAL)**
```
- Factual corrections (dosing, citations, medical accuracy)
- Remove dangerous/outdated information
- Fix contraindication warnings

Rationale: Patient safety first. These must be correct.
```

**Priority 2: Structural Foundation**
```
- Add/remove slides
- Reorder content
- Split/merge slides

Rationale: Structure changes affect subsequent edits.
```

**Priority 3: Content Modifications**
```
- Expand/simplify explanations
- Add new content blocks
- Update callouts

Rationale: Content changes within existing structure.
```

**Priority 4: Visual Elements**
```
- Diagram updates
- SVG modifications
- Color/style changes

Rationale: Visual changes don't affect content accuracy.
```

**Priority 5: Polish & Refinement**
```
- Wording improvements
- Formatting consistency
- Minor clarifications

Rationale: Low-impact, low-risk improvements.
```

### Step 2.3: Dependency Ordering

Some tasks must complete before others can begin:

**Dependency rules:**
```
1. Structural changes BEFORE content edits on affected slides
2. Slide creation BEFORE content population
3. Slide deletion AFTER content migration (if any)
4. Reference additions BEFORE citation callouts
5. Diagram structure BEFORE diagram styling
```

**Example dependency chain:**
```
T-003: Add new slide after slide 5
  └─▶ T-004: Add paragraph to new slide
        └─▶ T-005: Add clinical note to new slide
              └─▶ T-006: Add diagram to new slide
```

**Dependency detection:**
```json
{
  "taskId": "T-004",
  "dependencies": ["T-003"],
  "blockedBy": [],
  "blocks": ["T-005", "T-006"]
}
```

### Step 2.4: Task Queue Structure

The complete task queue ready for execution:

```json
{
  "sessionId": "iter-2026-01-14-dr-rose",
  "generatedAt": "2026-01-14T18:35:00.000Z",
  "taskQueue": [
    {
      "taskId": "T-001",
      "changeRequestId": "CR-001",
      "category": "factual_correction",
      "description": "Fix rapamycin dose: 6mg → 5mg",
      "target": {
        "file": "lecture-3.json",
        "slideId": "viral-persistence-slide"
      },
      "priority": 1,
      "dependencies": [],
      "status": "pending"
    },
    {
      "taskId": "T-002",
      "changeRequestId": "CR-003",
      "category": "structure_change",
      "description": "Add new slide for monitoring protocols",
      "target": {
        "file": "lecture-3.json",
        "insertAfter": "treatment-slide"
      },
      "priority": 2,
      "dependencies": [],
      "status": "pending"
    },
    {
      "taskId": "T-003",
      "changeRequestId": "CR-003",
      "category": "content_edit",
      "description": "Add monitoring protocol content to new slide",
      "target": {
        "file": "lecture-3.json",
        "slideId": "monitoring-slide"
      },
      "priority": 3,
      "dependencies": ["T-002"],
      "status": "blocked"
    }
  ],
  "summary": {
    "totalTasks": 3,
    "byPriority": { "1": 1, "2": 1, "3": 1 },
    "byStatus": { "pending": 2, "blocked": 1 }
  }
}
```

### Step 2.5: Present Task Queue Summary

Before execution, show the generated task queue:

```
TASKS GENERATED
━━━━━━━━━━━━━━━

Session: iter-2026-01-14-dr-rose
Total Tasks: 12

Execution Order:
┌─────┬──────────┬─────────────────────────────────────────┐
│ #   │ Priority │ Description                             │
├─────┼──────────┼─────────────────────────────────────────┤
│ T-1 │ P1       │ Fix rapamycin dose (6mg → 5mg)          │
│ T-2 │ P1       │ Correct NAD+ precursor timing           │
│ T-3 │ P2       │ Add monitoring protocols slide          │
│ T-4 │ P3       │ ├── Populate monitoring content         │
│ T-5 │ P3       │ └── Add clinical note callout           │
│ T-6 │ P3       │ Expand mechanism explanation            │
│ ... │ ...      │ ...                                     │
└─────┴──────────┴─────────────────────────────────────────┘

Dependency chains: 1 (T-3 → T-4 → T-5)

Ready to execute. This will modify 3 lecture files.
Begin execution?
```

### Step 2.6: Initialize TodoWrite

Sync tasks to TodoWrite for visual progress tracking:

```javascript
// Sync to TodoWrite
const todos = taskQueue.map(task => ({
  content: `${task.taskId}: ${task.description}`,
  status: task.status === 'pending' ? 'pending' : 'blocked',
  activeForm: `Executing ${task.description}`
}));

// Call TodoWrite tool
TodoWrite({ todos });
```

This enables real-time progress visibility in the Claude interface.

---

## Phase 3: Execution

Execute tasks one at a time, modifying lecture JSON files while preserving validity.

### Step 3.1: Load Target Lecture

Read the lecture JSON file and parse into editable structure:

```javascript
// Read lecture file
const lecturePath = `content/physician-courses/${physician}/${course}/lecture-${n}.json`;
const lectureJson = Read({ file_path: lecturePath });
const lecture = JSON.parse(lectureJson);
```

**Lecture JSON top-level structure:**
```json
{
  "id": "lecture-3",
  "title": "The Spike Paradigm: Viral Persistence & Reservoirs",
  "module": "Long COVID Mechanisms",
  "duration": "45 min",
  "videoUrl": "",
  "slides": [...],
  "keyTakeaways": [...],
  "references": [...]
}
```

### Step 3.2: Navigate to Target Element

Use the task's target path to locate the element:

```javascript
// Example: Edit content block in slide 3, content index 2
const slide = lecture.slides.find(s => s.id === "viral-persistence-slide");
const contentBlock = slide.content[2];
```

**Slide structure:**
```json
{
  "id": "viral-persistence-slide",
  "title": "Viral Persistence Mechanisms",
  "content": [...],        // Array of ContentBlocks
  "diagramHtml": "...",    // SVG string or null
  "callouts": [...]        // Array of Callouts
}
```

### Step 3.3: Edit Content Blocks

Each content block type has a specific editing pattern:

#### Paragraph Block
```json
// Before
{ "type": "paragraph", "text": "Rapamycin at 6mg weekly..." }

// Edit
Edit({
  file_path: lecturePath,
  old_string: '"text": "Rapamycin at 6mg weekly',
  new_string: '"text": "Rapamycin at 5mg weekly'
});
```

#### Bullets Block
```json
// Before
{ "type": "bullets", "items": ["Point 1", "Point 2"] }

// Add item
{ "type": "bullets", "items": ["Point 1", "Point 2", "New point"] }

// Edit item
Edit({
  old_string: '"items": ["Point 1", "Point 2"]',
  new_string: '"items": ["Point 1", "Updated point 2"]'
});
```

#### Numbered Block
```json
// Same pattern as bullets, but with "type": "numbered"
{ "type": "numbered", "items": ["Step 1", "Step 2", "Step 3"] }
```

#### Definition Block
```json
// Before
{ "type": "definition", "term": "NAD+", "definition": "..." }

// Edit
Edit({
  old_string: '"term": "NAD+", "definition": "Old definition"',
  new_string: '"term": "NAD+", "definition": "Updated definition"'
});
```

#### Quote Block
```json
{ "type": "quote", "text": "Quote text", "attribution": "Dr. Smith" }
```

#### Case Study Block
```json
{
  "type": "caseStudy",
  "title": "Patient Case",
  "scenario": "...",
  "approach": "...",
  "outcome": "..."
}
```

#### Formula Block
```json
{ "type": "formula", "label": "Half-life", "expression": "t½ = 0.693/k", "note": "..." }
```

#### Comparison Text Block
```json
{
  "type": "comparisonText",
  "items": [
    { "label": "Option A", "description": "..." },
    { "label": "Option B", "description": "..." }
  ]
}
```

#### Highlight Block
```json
{ "type": "highlight", "text": "Important emphasized text" }
```

#### Table Block
```json
{
  "type": "table",
  "headers": ["Drug", "Dose", "Frequency"],
  "rows": [
    ["Rapamycin", "5mg", "Weekly"],
    ["Metformin", "500mg", "BID"]
  ]
}
```

### Step 3.4: Modify Callouts

Callouts appear in the `callouts` array of each slide:

#### Clinical Note
```json
{ "type": "clinicalNote", "text": "Clinical guidance text..." }
```

#### Key Takeaway
```json
{ "type": "keyTakeaway", "text": "Key point to remember..." }
```

#### Evidence Callout
```json
{ "type": "evidence", "study": "PMID:12345678", "finding": "Study results..." }
```

#### Warning Callout
```json
{ "type": "warning", "text": "Safety warning text..." }
```

#### Pro Tip Callout
```json
{ "type": "proTip", "text": "Practical tip for clinicians..." }
```

**Adding a callout:**
```javascript
// Find the callouts array end and insert before closing bracket
Edit({
  old_string: '"callouts": [\n    { "type": "clinicalNote"',
  new_string: '"callouts": [\n    { "type": "warning", "text": "New warning" },\n    { "type": "clinicalNote"'
});
```

### Step 3.5: Update Diagrams

Diagrams are stored as SVG strings in `diagramHtml`. Exercise caution when editing.

**Diagram considerations:**
- SVG is complex - prefer targeted text replacements
- Preserve viewBox and namespace declarations
- Maintain valid XML structure
- Test rendering after changes

**Safe diagram edits:**
```javascript
// Change text content in SVG
Edit({
  old_string: '<text>Old Label</text>',
  new_string: '<text>New Label</text>'
});

// Change color (use colorPalette values)
Edit({
  old_string: 'fill="#E03E2F"',
  new_string: 'fill="#5C8A6B"'
});
```

**Risky diagram edits (require careful review):**
- Adding new SVG elements
- Restructuring paths
- Changing viewBox dimensions

### Step 3.6: Add/Remove Slides

**Adding a slide:**
```json
// New slide template
{
  "id": "new-slide-id",
  "title": "New Slide Title",
  "content": [
    { "type": "paragraph", "text": "Initial content..." }
  ],
  "diagramHtml": null,
  "callouts": []
}
```

**Insert position:**
```javascript
// Find the slide to insert after
const insertAfterIndex = lecture.slides.findIndex(s => s.id === "target-slide");

// Insert new slide
lecture.slides.splice(insertAfterIndex + 1, 0, newSlide);
```

**Removing a slide:**
```javascript
// Find and remove
const removeIndex = lecture.slides.findIndex(s => s.id === "obsolete-slide");
lecture.slides.splice(removeIndex, 1);
```

### Step 3.7: Update References

References array at lecture level:

```json
{
  "references": [
    {
      "id": "ref-1",
      "authors": "Smith J, et al.",
      "title": "Study Title",
      "journal": "Journal Name",
      "year": "2024",
      "doi": "10.1000/example",
      "pmid": "12345678"
    }
  ]
}
```

### Step 3.8: Preserve JSON Validity

**CRITICAL: Every edit must preserve valid JSON.**

**Validation steps after each edit:**
1. Parse JSON to verify syntax: `JSON.parse(content)`
2. Check for dangling commas
3. Verify balanced brackets/braces
4. Confirm string escaping

**Common JSON pitfalls:**
```json
// WRONG: Trailing comma
{ "items": ["a", "b", "c",] }

// CORRECT: No trailing comma
{ "items": ["a", "b", "c"] }

// WRONG: Unescaped quotes
{ "text": "He said "hello"" }

// CORRECT: Escaped quotes
{ "text": "He said \"hello\"" }

// WRONG: Single quotes
{ 'key': 'value' }

// CORRECT: Double quotes
{ "key": "value" }
```

**Recovery on invalid JSON:**
```
1. Restore from git: git checkout -- [file]
2. Re-attempt edit with corrected syntax
3. If repeated failure, log and skip task
```

### Step 3.9: Write Changes

After successful edit, write the modified file:

```javascript
// For simple edits: Edit tool handles atomic writes
// For complex restructuring: Write entire file
Write({
  file_path: lecturePath,
  content: JSON.stringify(lecture, null, 2)
});
```

### Step 3.10: Verify Change

After writing, verify the change was applied correctly:

```javascript
// Re-read file
const verifyContent = Read({ file_path: lecturePath });
const verified = JSON.parse(verifyContent);

// Check target element
const targetSlide = verified.slides.find(s => s.id === targetSlideId);
// Confirm change is present
```

### Task Completion Criteria

A task is complete when:
1. Target element is modified as specified
2. JSON remains valid (parseable)
3. No unintended changes to other elements
4. Change is logged to audit trail

---

## Audit Logging

Every change is logged for review and accountability. The audit log serves as the permanent record of what was changed, why, and when.

### Changelog File Creation

At session start, create a new changelog file:

**File naming pattern:**
```
.claude/skills/lecture-iterator/changelogs/
  iter-{YYYY-MM-DD}-{physician-slug}-{HHmmss}.md
```

**Example:**
```
iter-2026-01-14-dr-robin-rose-183000.md
```

**Initialization:**
```javascript
// Generate session ID
const sessionId = `iter-${date}-${physicianSlug}-${time}`;

// Create changelog directory if needed
Bash({ command: 'mkdir -p .claude/skills/lecture-iterator/changelogs' });

// Initialize changelog from template
const template = Read({
  file_path: '.claude/skills/lecture-iterator/templates/changelog-template.md'
});

// Fill in header values
const changelog = template
  .replace('[iter-YYYY-MM-DD-physician-slug]', sessionId)
  .replace('[Full Name (slug)]', `${physician.name} (${physician.id})`)
  .replace('[Course Title (slug)]', `${course.title} (${course.id})`)
  .replace('[ISO timestamp]', new Date().toISOString());

Write({
  file_path: `.claude/skills/lecture-iterator/changelogs/${sessionId}.md`,
  content: changelog
});
```

### Logging Each Change

After each successful task execution, append to the changelog:

**Change entry format:**
```markdown
--- CHANGE 003 | T-003 | content_edit ---
Timestamp:    2026-01-14T18:35:42.000Z
Lecture:      lecture-3
Slide:        viral-persistence-slide
Target:       content[2].text

Description:  Expanded mechanism explanation per Dr. Rose feedback

Before:
```
The spike protein binds to ACE2 receptors.
```

After:
```
The spike protein binds to ACE2 receptors on endothelial cells,
triggering a cascade of inflammatory responses including IL-6
and TNF-alpha elevation that persists for weeks post-infection.
```

Rationale:    Dr. Rose requested more detail on inflammatory cascade
Feedback Ref: Voice note transcript, 02:15
Status:       APPLIED

---
```

**Logging code:**
```javascript
// Append change entry to changelog
const changeEntry = `
--- CHANGE ${changeNum} | ${task.taskId} | ${task.category} ---
Timestamp:    ${new Date().toISOString()}
Lecture:      ${task.target.lecture}
Slide:        ${task.target.slideId || 'lecture-level'}
Target:       ${task.target.path}

Description:  ${task.description}

Before:
\`\`\`
${beforeContent}
\`\`\`

After:
\`\`\`
${afterContent}
\`\`\`

Rationale:    ${task.rationale}
Feedback Ref: ${task.feedbackRef}
Status:       APPLIED

---
`;

// Append to changelog
Edit({
  file_path: changelogPath,
  old_string: '================================================================================\nCHANGE LOG',
  new_string: `================================================================================\nCHANGE LOG\n${changeEntry}`
});
```

### Logging Clarifications

When user clarification is requested and received:

```markdown
--- CLARIFICATION 001 ---
Timestamp:    2026-01-14T18:40:00.000Z
Question:     Which NAD+ precursor dosing should be updated?
Options:      A) NR 300mg, B) NMN 500mg, C) Both
Response:     A) NR 300mg
Applied To:   T-005, T-006

---
```

### Session Completion Summary

At the end of execution, update the changelog summary:

```javascript
// Update summary statistics
Edit({
  file_path: changelogPath,
  old_string: 'Total Changes:  [N]',
  new_string: `Total Changes:  ${totalChanges}`
});

// Update category counts
Edit({
  file_path: changelogPath,
  old_string: '- Factual Corrections:  [N]',
  new_string: `- Factual Corrections:  ${counts.factual_correction}`
});

// ... repeat for each category

// Update files modified table
const filesTable = modifiedFiles.map(f =>
  `| ${f.path} | ${f.changeCount} | Modified |`
).join('\n');

Edit({
  file_path: changelogPath,
  old_string: '| File | Changes | Status |',
  new_string: `| File | Changes | Status |\n|------|---------|--------|\n${filesTable}`
});

// Mark session complete
Edit({
  file_path: changelogPath,
  old_string: '[ISO timestamp or "In Progress"]',
  new_string: new Date().toISOString()
});
```

### Changelog Storage

**Storage location:**
```
.claude/skills/lecture-iterator/changelogs/
├── iter-2026-01-14-dr-robin-rose-183000.md
├── iter-2026-01-14-dr-abid-husain-142500.md
├── iter-2026-01-12-dr-robin-rose-091500.md
└── ...
```

**Retention:** Changelogs are kept indefinitely for audit purposes.

**Accessing changelogs:**
```bash
# List recent changelogs
ls -la .claude/skills/lecture-iterator/changelogs/

# View specific changelog
cat .claude/skills/lecture-iterator/changelogs/iter-2026-01-14-dr-robin-rose-183000.md

# Search across changelogs
grep -r "rapamycin" .claude/skills/lecture-iterator/changelogs/
```

### Example Complete Changelog Entry

```markdown
--- CHANGE 001 | T-001 | factual_correction ---
Timestamp:    2026-01-14T18:32:15.000Z
Lecture:      lecture-3
Slide:        treatment-protocols-slide
Target:       content[1].rows[0][1]

Description:  Corrected rapamycin dosing from 6mg to 5mg weekly

Before:
```
["Rapamycin", "6mg", "Weekly"]
```

After:
```
["Rapamycin", "5mg", "Weekly"]
```

Rationale:    Dr. Rose specified 5mg weekly in feedback notes
Feedback Ref: dr-rose-notes.txt, line 15
Status:       APPLIED

---
```

---

## Multi-Lecture Batch Processing

When feedback spans multiple lectures, the skill processes them systematically while maintaining consistency.

### Detecting Lecture References

The skill scans feedback for lecture references and groups changes accordingly:

**Detection patterns:**
```javascript
const lecturePatterns = [
  /lecture\s*(\d+)/gi,           // "lecture 3", "Lecture 5"
  /lectures?\s*(\d+)\s*[-–to]+\s*(\d+)/gi,  // "lectures 3-5", "lecture 3 to 7"
  /slide\s*(\d+)/gi,             // May indicate lecture by slide number
  /in\s+the\s+(.*?)\s+lecture/gi // "in the mitochondrial lecture"
];
```

**Example feedback with multiple lectures:**
```
Feedback file content:
"In lecture 3, update the rapamycin dose to 5mg.

For lecture 5, add a clinical note about monitoring protocols.

Lectures 7-9 need updated references for the 2025 studies."
```

**Detected references:**
```json
{
  "lectureReferences": [
    { "lecture": 3, "source": "line 1" },
    { "lecture": 5, "source": "line 3" },
    { "lectures": [7, 8, 9], "source": "line 5" }
  ]
}
```

### Grouping Changes by Lecture

After parsing, changes are grouped by target lecture:

```json
{
  "changesByLecture": {
    "lecture-3": [
      { "taskId": "T-001", "category": "factual_correction", ... },
      { "taskId": "T-002", "category": "content_edit", ... }
    ],
    "lecture-5": [
      { "taskId": "T-003", "category": "add_callout", ... }
    ],
    "lecture-7": [
      { "taskId": "T-004", "category": "reference_update", ... }
    ],
    "lecture-8": [
      { "taskId": "T-005", "category": "reference_update", ... }
    ],
    "lecture-9": [
      { "taskId": "T-006", "category": "reference_update", ... }
    ]
  }
}
```

### Processing Order

Process lectures sequentially to maintain focus and enable consistency checks:

**Order rules:**
1. **Lower lecture numbers first** - Process lecture-3 before lecture-5
2. **Complete all tasks for one lecture before moving to next**
3. **Verify lecture validity after all its tasks complete**
4. **Log progress between lectures**

**Execution flow:**
```
┌────────────────────────────────────────────────────────┐
│                  BATCH PROCESSING                       │
│                                                         │
│  lecture-3 ─────────────────────────────────────────▶  │
│    T-001 ✓  T-002 ✓  [Verify] [Log]                    │
│                                                         │
│  lecture-5 ─────────────────────────────────────────▶  │
│    T-003 ✓  [Verify] [Log]                             │
│                                                         │
│  lecture-7 ─────────────────────────────────────────▶  │
│    T-004 ✓  [Verify] [Log]                             │
│                                                         │
│  lecture-8 ─────────────────────────────────────────▶  │
│    T-005 ✓  [Verify] [Log]                             │
│                                                         │
│  lecture-9 ─────────────────────────────────────────▶  │
│    T-006 ✓  [Verify] [Log]                             │
│                                                         │
│  [Final Summary]                                        │
└────────────────────────────────────────────────────────┘
```

### Cross-Lecture Consistency Checks

When processing multiple lectures, check for consistency:

**Consistency checks:**

| Check | Description | Action |
|-------|-------------|--------|
| Terminology | Same terms used across lectures | Flag inconsistencies |
| Dosing | Drug doses consistent unless explicitly different | Warn on discrepancies |
| References | Same studies cited consistently | Verify PMIDs match |
| Naming | Proper names spelled consistently | Auto-correct if clear |

**Example consistency check:**
```
Processing lecture-5...

WARNING: Terminology inconsistency detected
  - Lecture 3: "NAD+ precursors"
  - Lecture 5: "NAD precursors" (missing +)

Recommendation: Standardize to "NAD+ precursors"

Apply fix? [Y/n]
```

### Batch Progress Tracking

Track progress across all lectures:

```
BATCH PROGRESS
━━━━━━━━━━━━━━

Lectures: 5 total
  ✓ lecture-3 (2 tasks) - COMPLETE
  → lecture-5 (1 task)  - IN PROGRESS
  ○ lecture-7 (1 task)  - PENDING
  ○ lecture-8 (1 task)  - PENDING
  ○ lecture-9 (1 task)  - PENDING

Tasks: 6 total
  Completed: 2
  In Progress: 1
  Pending: 3

ETA: ~3 tasks remaining
```

### Batch Summary at Completion

```
BATCH PROCESSING COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━

Session: iter-2026-01-14-dr-robin-rose-183000

Lectures Modified: 5
  - lecture-3: 2 changes
  - lecture-5: 1 change
  - lecture-7: 1 change
  - lecture-8: 1 change
  - lecture-9: 1 change

Total Tasks: 6
  Completed: 6
  Failed: 0

Consistency Checks:
  - Terminology: PASSED
  - Dosing: PASSED
  - References: PASSED

Changelog: .claude/skills/lecture-iterator/changelogs/iter-2026-01-14-dr-robin-rose-183000.md

Review all changes:
  git diff HEAD~6 content/physician-courses/dr-robin-rose/long-covid/
```

---

## Handling Ambiguous Feedback

When feedback is unclear or incomplete, the skill pauses and requests clarification before proceeding.

### Ambiguity Triggers

The skill identifies these situations as requiring clarification:

| Trigger | Example | Why It's Ambiguous |
|---------|---------|-------------------|
| **Missing target** | "Update the dosing" | Which lecture? Which drug? |
| **Conflicting info** | "Change to 5mg" when 5mg exists | What's the intended change? |
| **Unclear scope** | "Fix the mechanism section" | What specifically is wrong? |
| **Multiple interpretations** | "Make it clearer" | Clearer how? |
| **Missing content** | "Add Dr. Smith's protocol" | What is the protocol? |
| **Vague reference** | "That slide about mitochondria" | Multiple slides match |
| **Contradictory requests** | "Remove but also expand" | Which action to take? |

### Clarification Flow

When ambiguity is detected:

```
┌─────────────────────────────────────────────────────────┐
│              CLARIFICATION WORKFLOW                      │
│                                                          │
│  1. Detect ambiguity during parsing                      │
│       ↓                                                  │
│  2. Gather context (what we know, what's unclear)        │
│       ↓                                                  │
│  3. Formulate specific question with options             │
│       ↓                                                  │
│  4. Present to user via AskUserQuestion                  │
│       ↓                                                  │
│  5. PAUSE - Wait for user response                       │
│       ↓                                                  │
│  6. Log clarification in changelog                       │
│       ↓                                                  │
│  7. Resume parsing/execution with clarified info         │
└─────────────────────────────────────────────────────────┘
```

### Using AskUserQuestion

The skill uses the `AskUserQuestion` tool to get specific, actionable clarification:

**Question template:**
```javascript
AskUserQuestion({
  questions: [
    {
      question: "Which [element] should be updated?",
      header: "Clarify target",
      options: [
        { label: "Option A", description: "Specific description with context" },
        { label: "Option B", description: "Alternative with context" },
        { label: "Option C", description: "Third possibility" },
        { label: "Skip this change", description: "Don't apply this feedback item" }
      ],
      multiSelect: false
    }
  ]
});
```

### Clarification Examples

#### Example 1: Missing Target Lecture

**Feedback:** "The rapamycin dosing needs to be updated"

**Detected issue:** Rapamycin is mentioned in lectures 3, 5, and 8

**Clarification question:**
```javascript
AskUserQuestion({
  questions: [{
    question: "Which lecture's rapamycin dosing should be updated?",
    header: "Target lecture",
    options: [
      { label: "Lecture 3", description: "Currently shows 6mg weekly in treatment protocols slide" },
      { label: "Lecture 5", description: "Currently shows 5mg weekly in combination therapy slide" },
      { label: "Lecture 8", description: "Currently shows 5-6mg range in advanced protocols slide" },
      { label: "All of the above", description: "Update rapamycin dosing in all lectures" }
    ],
    multiSelect: false
  }]
});
```

#### Example 2: Unclear Change Request

**Feedback:** "Make the mechanism section clearer"

**Detected issue:** "Clearer" is subjective and unactionable

**Clarification question:**
```javascript
AskUserQuestion({
  questions: [{
    question: "How should the mechanism section be clarified?",
    header: "Clarification type",
    options: [
      { label: "Simplify language", description: "Reduce jargon, use simpler terms" },
      { label: "Add more detail", description: "Expand explanations with specifics" },
      { label: "Add visual diagram", description: "Create or enhance diagram for clarity" },
      { label: "Restructure content", description: "Reorder for better logical flow" }
    ],
    multiSelect: true
  }]
});
```

#### Example 3: Missing Content

**Feedback:** "Add Dr. Johnson's protocol for post-viral fatigue"

**Detected issue:** Protocol content not provided

**Clarification question:**
```javascript
AskUserQuestion({
  questions: [{
    question: "What is Dr. Johnson's protocol for post-viral fatigue?",
    header: "Missing content",
    options: [
      { label: "Provide protocol", description: "I'll describe it now" },
      { label: "Reference document", description: "I'll provide a file or link" },
      { label: "Search existing content", description: "Look for similar protocols in course materials" },
      { label: "Skip this addition", description: "Don't add this protocol for now" }
    ],
    multiSelect: false
  }]
});
```

### Execution Pause Behavior

When clarification is needed:

1. **Immediate pause** - No changes are made until clarification received
2. **Context preservation** - All parsed feedback is retained
3. **Progress tracking** - TodoWrite shows "Awaiting clarification"
4. **Clear prompt** - User knows exactly what information is needed

**Status during pause:**
```
AWAITING CLARIFICATION
━━━━━━━━━━━━━━━━━━━━━━

Feedback item: "Update the dosing"
Issue: Multiple lectures contain dosing information

Waiting for user response...

[Once answered, execution will resume]
```

### Logging Clarifications

All clarifications are logged in the changelog:

```markdown
--- CLARIFICATION 001 ---
Timestamp:    2026-01-14T18:40:00.000Z
Feedback:     "The rapamycin dosing needs to be updated"
Ambiguity:    Multiple lectures contain rapamycin dosing
Question:     "Which lecture's rapamycin dosing should be updated?"
Options:
  A) Lecture 3 (6mg weekly)
  B) Lecture 5 (5mg weekly)
  C) Lecture 8 (5-6mg range)
  D) All of the above
Response:     A) Lecture 3
Applied To:   T-001

---
```

### Handling "Other" Responses

When user selects "Other" or provides custom input:

```javascript
// User selected "Other" with custom text
if (response === "Other") {
  const customResponse = userProvidedText;

  // Parse custom response for actionable information
  const parsedCustom = parseCustomClarification(customResponse);

  // Log the custom clarification
  logClarification({
    question: originalQuestion,
    response: `Custom: ${customResponse}`,
    parsedAs: parsedCustom
  });

  // Continue with parsed information
  resumeWithClarification(parsedCustom);
}
```

### Clarification Limits

To prevent infinite clarification loops:

- **Max clarifications per feedback item:** 3
- **After limit reached:** Skip item and log as "Unable to clarify"
- **Offer to user:** "Would you like to provide this feedback in a different format?"

---

## Reference

Quick access to lecture system documentation and related resources.

### Key Files

| File | Description |
|------|-------------|
| [content/lectures/schema.ts](content/lectures/schema.ts) | TypeScript types for lecture JSON structure |
| [content/physician-courses/registry.ts](content/physician-courses/registry.ts) | Physician and course registry with lecture imports |
| [src/views/preview/PhysicianLectureViewer.tsx](src/views/preview/PhysicianLectureViewer.tsx) | Lecture rendering component |

### Related Skills

| Skill | Purpose |
|-------|---------|
| `/physician-course-builder` | Create new lectures from scratch |
| `/generate-lectures` | Generate lectures from course outline |
| `/physician-feedback-agent` | Simulate physician feedback personas |
| `/lecture-builder` | General lecture formatting |

### Content Block Types (10 types)

| Type | Structure | Usage |
|------|-----------|-------|
| `paragraph` | `{ text: string }` | Basic text content |
| `bullets` | `{ items: string[] }` | Unordered list |
| `numbered` | `{ items: string[] }` | Ordered list |
| `definition` | `{ term, definition }` | Key term explanation |
| `quote` | `{ text, attribution? }` | Quoted text |
| `caseStudy` | `{ title, scenario, approach, outcome }` | Patient case |
| `formula` | `{ label, expression, note? }` | Mathematical formula |
| `comparisonText` | `{ items: [{label, description}] }` | Side-by-side comparison |
| `highlight` | `{ text }` | Emphasized text |
| `table` | `{ headers, rows }` | Data table |

### Callout Types (5 types)

| Type | Structure | Display |
|------|-----------|---------|
| `clinicalNote` | `{ text }` | Blue info box |
| `keyTakeaway` | `{ text }` | Gold highlight box |
| `evidence` | `{ study, finding }` | Citation box |
| `warning` | `{ text }` | Red warning box |
| `proTip` | `{ text }` | Green tip box |

### Diagram Types (20+ types)

Common diagram patterns available in `diagramHtml`:

| Type | Description |
|------|-------------|
| `pathway` | Multi-step biological pathway |
| `comparison` | Side-by-side comparison chart |
| `process` | Linear process flow |
| `network` | Interconnected nodes |
| `hierarchy` | Tree structure |
| `timeline` | Chronological sequence |
| `matrix` | 2D grid comparison |
| `cycle` | Circular process |
| `venn` | Overlapping sets |
| `flowchart` | Decision/process flow |
| `gauge` | Meter/indicator |
| `stack` | Layered elements |
| `anatomy` | Body system illustration |
| `molecular` | Chemical structure |
| `cellular` | Cell diagram |
| `organ` | Organ system |
| `pharmacology` | Drug mechanism |
| `protocol` | Treatment protocol |
| `dosing` | Dosing chart |
| `labs` | Lab values reference |

### Color Palette

Standard colors for diagrams (from schema.ts):

| Name | Hex | Usage |
|------|-----|-------|
| `red` | #E03E2F | Warnings, hover states |
| `orange` | #D4845C | Caution, warm accent |
| `yellow` | #D4A84C | Subtle highlight |
| `green` | #5C8A6B | Positive, good status |
| `blue` | #5C7A8A | Informational |
| `purple` | #7A6C8A | Special, advanced |
| `gray` | #8B909A | Tertiary text |
| `ink` | #0A0B0C | Primary text |
| `gold` | #C5A572 | Brand accent |

### Lecture File Paths

```
content/physician-courses/
├── dr-abid-husain/
│   ├── systems-cardiology/
│   │   ├── lecture-1.json
│   │   ├── lecture-2.json
│   │   └── ... (5 lectures)
│   └── systems-cardiology-expanded/
│       ├── lecture-1.json
│       └── ... (15 lectures)
└── dr-robin-rose/
    └── long-covid/
        ├── lecture-1.json
        └── ... (11 lectures)
```

---

## Examples

Complete invocation examples showing different feedback scenarios.

### Example 1: Simple Text Feedback

**Scenario:** Quick correction from Dr. Rose about a drug dose.

**Invocation:**
```bash
/lecture-iterator "In lecture 3, the rapamycin dose should be 5mg weekly, not 6mg" --physician dr-robin-rose --course long-covid
```

**Expected behavior:**
1. Parse feedback → 1 factual correction identified
2. Locate rapamycin mention in lecture-3.json
3. Change "6mg" to "5mg" in treatment protocols slide
4. Log change with before/after context
5. Report completion

**Output:**
```
LECTURE ITERATOR COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━

Changes Applied: 1
  - T-001: Fix rapamycin dose (6mg → 5mg)

Lecture Modified: lecture-3.json
Changelog: iter-2026-01-14-dr-robin-rose-183000.md

Review: git diff HEAD~1 content/physician-courses/dr-robin-rose/long-covid/lecture-3.json
```

### Example 2: Voice Note Transcript

**Scenario:** Dr. Husain recorded a voice memo with multiple corrections.

**Voice transcript file (`dr-husain-feedback-2026-01-14.txt`):**
```
[00:00] Looking at lecture 5, the ApoB threshold should be less than 60, not 70.

[00:15] In lecture 7, can we add a clinical note about monitoring LDL-C during
GLP-1 therapy? Something about checking at 3 months.

[00:45] Also lectures 9 through 11 need the updated 2025 REDUCE-IT citation.

[01:00] Oh and the diagram in lecture 6 - the FFRct threshold should show 0.80,
I think it shows 0.75 currently.
```

**Invocation:**
```bash
/lecture-iterator ./feedback/dr-husain-feedback-2026-01-14.txt --physician dr-abid-husain --course systems-cardiology-expanded
```

**Expected behavior:**
1. Parse transcript → 4 change requests identified
2. Group by lecture: {5: 1, 6: 1, 7: 1, 9-11: 1}
3. Process in order: lecture-5, lecture-6, lecture-7, lecture-9, lecture-10, lecture-11
4. Log each change with timestamp reference from transcript
5. Report batch completion

**Output:**
```
BATCH PROCESSING COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━

Changes Applied: 6 (from 4 feedback items)

Lectures Modified:
  - lecture-5: 1 change (ApoB threshold)
  - lecture-6: 1 change (FFRct diagram)
  - lecture-7: 1 change (clinical note added)
  - lecture-9: 1 change (reference update)
  - lecture-10: 1 change (reference update)
  - lecture-11: 1 change (reference update)

Changelog: iter-2026-01-14-dr-abid-husain-142500.md
```

### Example 3: PDF Feedback

**Scenario:** Dr. Rose sent annotated PDF with corrections marked.

**Invocation:**
```bash
/lecture-iterator ./feedback/dr-rose-annotated-slides.pdf --physician dr-robin-rose
```

**Expected behavior:**
1. Read PDF using Read tool
2. Extract text annotations and highlights
3. Parse annotations into change requests
4. Clarify any ambiguous annotations via AskUserQuestion
5. Apply changes in priority order
6. Generate changelog with page references

**Note:** PDF parsing may require clarification for handwritten annotations or unclear highlights.

### Example 4: Google Drive Document

**Scenario:** Dr. Husain shared feedback in a Google Doc.

**Invocation:**
```bash
/lecture-iterator --gdrive 1ABC123def456GHI789 --physician dr-abid-husain --course systems-cardiology-expanded
```

**Expected behavior:**
1. Fetch document using `mcp__google-drive__export_google_doc`
2. Convert to text format
3. Parse feedback same as text file
4. Apply changes
5. Log source as Google Drive file ID

**Alternative with full URL:**
```bash
/lecture-iterator --gdrive "https://docs.google.com/document/d/1ABC123def456GHI789/edit" --physician dr-abid-husain
```

### Example 5: Multi-Lecture Batch with Mixed Feedback

**Scenario:** Comprehensive feedback session spanning multiple sources.

**Feedback manifest (`feedback-session-2026-01-14.txt`):**
```
# Dr. Rose Long COVID Course Review - January 2026
# Sources:

# Written notes from initial review
./feedback/dr-rose-written-notes.md

# Voice memo from follow-up call
./transcripts/dr-rose-voice-memo.txt

# Annotated slides PDF
./feedback/dr-rose-annotated.pdf

# Google Doc with additional changes
--gdrive 1ABC123supplementaryFeedback
```

**Invocation:**
```bash
/lecture-iterator ./feedback/feedback-session-2026-01-14.txt --physician dr-robin-rose --course long-covid
```

**Expected behavior:**
1. Parse manifest, identify 4 sources
2. Load and parse each source sequentially
3. Deduplicate overlapping feedback
4. Generate unified task queue
5. Process all lectures in order
6. Create single comprehensive changelog

**Output:**
```
COMPREHENSIVE FEEDBACK SESSION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sources Processed: 4
  - Written notes: 12 changes
  - Voice transcript: 8 changes
  - PDF annotations: 5 changes
  - Google Doc: 3 changes

Duplicates Removed: 4

Total Changes Applied: 24

Lectures Modified: 8 of 11
  - lecture-1: 2 changes
  - lecture-3: 5 changes
  - lecture-4: 3 changes
  - lecture-5: 4 changes
  - lecture-6: 2 changes
  - lecture-7: 3 changes
  - lecture-9: 3 changes
  - lecture-11: 2 changes

Consistency Checks: PASSED

Changelog: iter-2026-01-14-dr-robin-rose-comprehensive.md

Time: 12 minutes
```

### Example 6: Targeted Single Slide Edit

**Scenario:** Quick fix for a specific slide.

**Invocation:**
```bash
/lecture-iterator "Update the evidence callout to cite PMID:39876543 instead of the 2023 study" --physician dr-robin-rose --course long-covid --lecture 5
```

**Expected behavior:**
1. Load only lecture-5.json
2. Find evidence callout(s)
3. If multiple, clarify which one
4. Update PMID reference
5. Log minimal change

**Output:**
```
CHANGE APPLIED
━━━━━━━━━━━━━━

Lecture: 5
Slide: treatment-options-slide
Change: Evidence callout PMID updated (old: 38123456 → new: 39876543)

Changelog: iter-2026-01-14-dr-robin-rose-190000.md
```

---

## Anti-Patterns

Common mistakes to avoid when executing this skill.

### 1. Breaking JSON Validity

**Anti-pattern:** Making edits that corrupt JSON structure.

```json
// WRONG: Trailing comma after edit
"items": ["old", "new",]

// WRONG: Unbalanced brackets
"slides": [{ "id": "slide-1" }

// WRONG: Missing quotes
{ type: "paragraph" }
```

**Prevention:**
- Always verify JSON parses after each edit
- Use `JSON.parse()` check before committing
- Restore from git if JSON becomes invalid

### 2. Losing Content

**Anti-pattern:** Accidentally deleting content during edits.

```javascript
// WRONG: Replace too broadly
Edit({
  old_string: 'The patient',  // Matches multiple places!
  new_string: 'The individual'
});

// RIGHT: Include unique context
Edit({
  old_string: '"text": "The patient should be monitored',
  new_string: '"text": "The individual should be monitored'
});
```

**Prevention:**
- Always include sufficient context in `old_string`
- Review before/after in changelog
- Read back file to verify single change

### 3. Skipping Audit Log

**Anti-pattern:** Making changes without logging.

```
BAD: Change made → No changelog entry → User can't review
GOOD: Change made → Logged immediately → User can review
```

**Prevention:**
- Log EVERY change, no exceptions
- Include before/after context
- Log clarifications and decisions

### 4. Ignoring Ambiguity

**Anti-pattern:** Guessing instead of asking.

```
Feedback: "Fix the dose"

BAD: Assume which dose → Make wrong change
GOOD: Ask user which dose → Make correct change
```

**Prevention:**
- When in doubt, ASK
- Use AskUserQuestion for any ambiguity
- Better to pause than make wrong change

### 5. Batch Without Verification

**Anti-pattern:** Processing all feedback without intermediate checks.

```
BAD: Parse all → Execute all → Find errors at end
GOOD: Parse → Execute one → Verify → Log → Next
```

**Prevention:**
- Verify JSON after each task
- Check one lecture before moving to next
- Log progress incrementally

### 6. Editing Without Reading

**Anti-pattern:** Making edits based on assumptions.

```
BAD: Assume slide structure → Edit fails
GOOD: Read lecture first → Understand structure → Edit succeeds
```

**Prevention:**
- ALWAYS read target file before editing
- Understand current content before changing
- Verify target element exists

### 7. Inconsistent Changes Across Lectures

**Anti-pattern:** Applying changes differently in different lectures.

```
Lecture 3: "NAD+ precursors" (correct)
Lecture 5: "NAD precursors" (inconsistent)
Lecture 7: "NAD+ Precursors" (different capitalization)
```

**Prevention:**
- Run consistency checks for batch operations
- Standardize terminology during first occurrence
- Flag inconsistencies for user decision

---

## Quality Checklist

Complete this checklist before marking any iteration as complete.

### Pre-Edit Verification

- [ ] Read target lecture file
- [ ] Identified exact element to modify
- [ ] Confirmed change matches feedback
- [ ] No ambiguity in change request

### During Edit

- [ ] Using Edit tool with sufficient context
- [ ] Single logical change per edit
- [ ] Preserving JSON structure
- [ ] Not affecting unrelated content

### Post-Edit Verification

- [ ] JSON parses without errors
- [ ] Target element changed correctly
- [ ] No unintended changes elsewhere
- [ ] File can be re-read successfully

### Audit Logging

- [ ] Change entry added to changelog
- [ ] Before/after content captured
- [ ] Rationale documented
- [ ] Feedback source referenced

### Batch Operations

- [ ] All lectures in batch verified
- [ ] Consistency checks passed
- [ ] Progress logged between lectures
- [ ] Summary statistics accurate

### Session Completion

- [ ] All feedback items addressed
- [ ] Changelog summary updated
- [ ] Files modified list accurate
- [ ] Final review recommendations noted

---

## Session Completion Summary

When all tasks are complete:

```
LECTURE ITERATION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━

Session: iter-2026-01-14-dr-robin-rose-183000

Summary:
  - Feedback processed: 100%
  - Changes applied: [N]
  - Clarifications: [N]
  - Errors: 0

Quality Gates:
  ✓ All JSON files valid
  ✓ All changes logged
  ✓ Consistency checks passed

Files Modified:
  - lecture-3.json (5 changes)
  - lecture-5.json (2 changes)
  - lecture-7.json (3 changes)

Changelog: .claude/skills/lecture-iterator/changelogs/iter-2026-01-14-dr-robin-rose-183000.md

Next Steps:
  1. Review changelog for accuracy
  2. Preview lectures in browser
  3. Run: npm run check
  4. Commit when satisfied
```
