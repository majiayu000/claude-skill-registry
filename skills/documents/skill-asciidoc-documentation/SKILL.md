---
name: skill-asciidoc-documentation
description: "Write AsciiDoc documentation with  style and design system"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
metadata:
  type: implementation
  agents:
    - -doc-writer
    - -doc-reviewer
---

# Skill: Write AsciiDoc Documentation

This skill guides you through creating documentation following  standards. You will plan structure, write content with proper voice, add styled figures using the design system, and validate the result.

The workflow ensures consistent, professional documentation that follows 's human, clear, and direct voice.

## Prerequisites

- Topic or files to document identified
- Understanding of target audience
- Access to _design/figures/ directory for images

## Overview

1. Plan document structure (using -doc-writer)
2. Set up document header
3. Write content following voice guidelines
4. Add figures with design system styling
5. Include code with proper tags
6. Add icons for visual grouping
7. Validate (using -doc-reviewer)

## Step 1: Plan Structure

Invoke -doc-writer for an outline based on topic and audience.

### Action

Determine:
- Target audiences (architect, developer, operations, etc.)
- Main sections needed
- Figures required
- Code examples to include

## Step 2: Set Up Document Header

Every document starts with this header:

```asciidoc
:author_name: Mario Toffia
:author_email: mario.toffia@.com
:author: {author_name}
:email: {author_email}
:source-highlighter: highlightjs
:toc:
:toc-title: Table of Contents
:toclevels: 4
:homepage: www..com
:stem: latexmath
ifndef::doctype[:doctype: book]
ifndef::icons[:icons: font]
ifndef::imagesdir[:imagesdir: ../../../meta/assets]
```

Adjust `imagesdir` relative path based on depth from project root.

## Step 3: Write Content

Follow  voice guidelines strictly.

### Voice Guidelines

**Voice Characteristics:**
- Human, clear, calm, direct
- Specific and grounded
- Use I/you/we naturally
- Assume the reader is competent

**Use:**
- Clean verbs and nouns
- Straightforward statements
- Mix of sentence lengths. Short ones work.
- Concrete details over abstractions

### Words to Avoid

**AI-ish Vocabulary:**
align, enhance, delve, foster, emphasize, highlight, underscore, pivotal, intricate, leverage, streamline, robust, seamless, holistic, synergy, utilize, facilitate, optimize, empower, ecosystem

**Vague Qualifiers:**
plain, fine, actually, truly, deeply, really, certainly, definitely, essentially, fundamentally, basically

**Weakening Adverbs:**
even, just, simply, merely, quite, rather, somewhat

**Flourish Patterns:**
- "from X to Y" patterns
- Rule-of-three padding
- "not only...but also..."

### Meta Commentary to Avoid

- "Let's walk through..."
- "Below is..."
- "In this section we will..."
- "As mentioned above..."

### Structure Rules

- State facts. Move on.
- No disclaimers or hedging unless requested
- No overexplaining or restating the obvious
- No moralizing or "wisdom" lines

### Editing Priorities

1. Remove padding
2. Remove vague fillers
3. Keep meaning intact while tightening wording
4. Maintain professional but human voice

### Example Transformations

Bad:
> In this section, we will delve into the intricacies of the configuration system, which plays a pivotal role in ensuring seamless integration.

Good:
> The configuration system controls how components connect.

Bad:
> It's actually quite important to understand that the system truly leverages robust patterns.

Good:
> The system uses established patterns.

## Step 4: Add Figures

Create or include figures following the design system.

### Design System Colors

#### Primary Colors

| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| Deep Blue | #05289E | 5, 40, 158 | Primary actions, headers, links, charts, emphasis text |
| Lime Green | #CBFF9E | 203, 255, 158 | Success states, CTAs, accent backgrounds, highlights |
| Navy | #0F1729 | 15, 23, 41 | Primary text, dark surfaces, tooltips, hero backgrounds |
| Coral | #FC7246 | 252, 114, 70 | Warnings, warm highlights (use sparingly) |

#### Extended Green Scale

| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| Forest | #0d2818 | 13, 40, 24 | Deep hero backgrounds, premium feel |
| Dark Green | #1a3a2f | 26, 58, 47 | Hero sections, dark cards, headers |
| Sage | #2d5a47 | 45, 90, 71 | Secondary buttons on dark, hover states |
| Mint | #e8f5e9 | 232, 245, 233 | Light environmental accents |

#### Neutral Colors

| Color | Hex | Usage |
|-------|-----|-------|
| White | #FFFFFF | Primary background surface |
| Light Gray | #F8FAFC | Cards, secondary surfaces, sidebar |
| Border | #E2E8F0 | Dividers, borders, separators |
| Light Blue | #E8EBFF | Info backgrounds, hover states, selected items |
| Text Primary | #0F1729 | Main body text |
| Text Secondary | #64748B | Captions, labels, secondary text |
| Text Tertiary | #94A3B8 | Placeholder text, disabled states |

#### Chart Color Sequence

Use colors in this order for data visualizations (max 4 colors per chart):
1. #05289E (Deep Blue) — Primary data
2. #CBFF9E (Lime Green) — Accent/highlight
3. #1a3a2f (Dark Green) — Secondary data
4. #FC7246 (Coral) — Warning/attention
5. #E8EBFF (Light Blue) — Tertiary data

#### Color Rules

**Do:**
- Always use white backgrounds as primary surface
- Use #05289E for emphasis text on white backgrounds
- Use solid colors only (no gradients except hero sections)
- Maintain 4.5:1 contrast ratio for text (WCAG AA)
- Use red (#EF4444) only for error states
- Combine dark green with lime green for energy themes

**Don't:**
- Never use lime green (#CBFF9E) as text on white — unreadable (1.5:1 contrast)
- Never use red as a brand color
- Never use more than 4 colors per visualization
- Never use heavy shadows (max: 0 8px 24px rgba(0,0,0,0.08))
- Never mix forest green with coral in the same element

### Figure Location

- Store in `_design/figures/` (same level as overview.adoc)
- Output SVGs go to `<project-root>/meta/assets/figures/<package>/`

### Supported Figure Formats

| Extension | Tool | Best For |
|-----------|------|----------|
| .mmd | Mermaid | Flowcharts, sequence, class, state, ER, Gantt, pie |
| .blockdiag | BlockDiag | Simple block diagrams, network diagrams |
| .nomnoml | Nomnoml | UML-style class diagrams, simple and clean |
| .bytefield | Bytefield | Binary protocol layouts, packet structures |
| .drawio | diagrams.net | Complex diagrams, UI mockups, network topologies |
| .excalidraw | Excalidraw | Hand-drawn style, architecture sketches, whiteboards |

Prefer simple ASCII-based formats (mermaid, blockdiag, nomnoml). Use excalidraw or drawio for complex visuals.

### Image Macro Format

```asciidoc
.The Event Processing Flow
image::figures/<package>/<name>.svg[width=100%,height=100%, opts=inline]
```

Required attributes:
- `width=100%` — scales to container width
- `height=100%` — maintains aspect ratio
- `opts=inline` — embeds SVG for proper rendering

Example:

```asciidoc
.The Event Processing Flow
image::figures/cbanalytics/event-processing-flow.svg[width=100%,height=100%, opts=inline]
```

Generate SVGs with `make docs-generate` in the `_design` folder.

## Step 5: Include Code

Use tags for code inclusion, never generate inline Go code.

### Tag Format in Go Files

```go
// tag::example[]
func Example() {
    // code here
}
// end::example[]
```

### Include in AsciiDoc

```asciidoc
[source,go]
----
include::path/to/file.go[tag=example]
----
```

### Code Blocks with Callouts

```asciidoc
[source,go]
----
func Process(ctx context.Context, msg Message) error {
    if err := validate(msg); err != nil { // <1>
        return err
    }
    return handle(ctx, msg) // <2>
}
----
<1> Validate input before processing.
<2> Delegate to handler after validation.
```

### Rules

- Never generate Go code inline in .adoc files
- Always include from actual source files
- JSON, XML, and YAML may be inline
- If code is missing, create it in tests/xyz_example_test.go, tag it, then include

## Step 6: Add Icons

Use icons for visual grouping and to underline functionality.

### Icon Legend

| Icon | Meaning | Usage |
|------|---------|-------|
| 💡 | Idea/Suggestion | Ideas, feature proposals, feedback |
| 💭 | Thought/Collection | Idea sources, collection phase |
| 📥 | Incoming | Incoming requests, submissions |
| 📋 | Backlog/List | Backlogs, GitHub issues, task lists |
| 🔍 | Search/Investigation | Duplicate detection, pre-study, investigation |
| 📊 | Analytics/Data | Product Owner, roadmap, metrics |
| 🎨 | Design | Design phase, UI/UX |
| ✅ | Complete/Ready | Qualification, done states, approvals |
| ⚙️ | Engineering | In progress, development, technical work |
| 🧪 | Testing | QA, test environments, staging |
| 📦 | Package/Release | Ready for release |
| 🚀 | Deploy/Launch | Released, deployment |
| 🔄 | Cycle/Sync | Sprints, CI/CD, sync operations |
| 👤 | Person/Role | Individual roles, owners |
| 👥 | Group/Team | Stakeholders, teams |
| 🎫 | Ticket/Support | Support L1, tickets |
| 🔧 | Technical/L2 | Support L2, installers, technical |
| 📚 | Knowledge | Knowledge base, documentation |
| 🐛 | Bug | Bug reports, defects |
| 🚦 | Feature Flags | Gradual rollout, flags |
| ☁️ | Cloud | GCP, infrastructure |
| 📤 | Send/Report | Report back, notifications |
| ⬆️ | Escalate | Escalation paths |
| 👀 | Review | Code review, PR review, validation |
| 📅 | Schedule/Planning | Sprint planning, calendar events |
| ☀️ | Daily/Morning | Daily standup, recurring meetings |
| 🎬 | Demo/Presentation | Sprint review, demos, presentations |
| ⚖️ | Balance/Allocation | Capacity allocation, trade-offs |
| 🏷️ | Labels/Tags | Item types, categories, labels |
| 🧩 | Feature/Component | Feature items, puzzle pieces |
| 🔬 | Research | Investigation, spikes, proof of concept |
| 📄 | Document | Documentation items, files |
| 🌐 | Global/Live | Feature live, all users, worldwide |
| 🧹 | Cleanup | Tech debt cleanup, flag removal |
| 💻 | Coding | Implementation, development work |
| 📈 | Growth/Metrics | Metrics check, improvement trends |
| ⏪ | Rollback | Rollback, revert, undo |
| ▶️ | Start | Start state, begin process |
| 🔗 | Integration | Integration points, connections |

## Step 7: Target Audiences

Use ifdef/endif to scope content to specific audiences.

### Available Targets

| Keyword | Description | When to Use |
|---------|-------------|-------------|
| target-architect | Architect | System design, component relationships, patterns |
| target-developer | Developer | Implementation details, APIs, code examples |
| target-operations | DevOps/Operations | Deployment, monitoring, configuration |
| target-system | System Design | Cross-cutting concerns, integration points |
| target-business | Business | Business logic, requirements, workflows |
| target-provider | Provider | Provider implementations in /go-services/providers/ |
| target-test | Tester | Test strategies, fixtures, coverage |

### Usage Examples

Single target:

```asciidoc
ifdef::target-architect[]
== Architecture Overview
This section covers...
endif::target-architect[]
```

Multiple targets:

```asciidoc
ifdef::target-architect,target-operations[]
== Deployment Architecture
...
endif::target-architect,target-operations[]
```

Nested:

```asciidoc
ifdef::target-architect,target-developer[]
ifdef::target-developer[]
== API Reference
endif::target-developer[]

ifdef::target-architect[]
=== Design Rationale
...
endif::target-architect[]
ifdef::target-developer[]
== Other Dev Info
endif::target-developer[]

endif::target-architect,target-developer[]
```

When nested, all audiences that are nested must be included in the outer scope.

### Makefile Usage

```makefile
@${ASCIIDOCTOR} ${ASCIIDOC_PRE} \
    -a target-architect \
    -a target-developer \
    ./overview.adoc \
    -o ${DOCS}/package.html
```

## Step 8: Document Organization

### Location and Naming

- Package documentation lives in `_design/` subfolder
- Main document: `overview.adoc` — contains package overview chapter and includes sub-documents
- Sub-documents included with `include::sub-doc.adoc[leveloffset=+1]`

### Makefile

Place in `_design/` folder:

```makefile
# Include document generation targets
# docs-generate:
include ../../../docs_meta.mk

docs:
	@mkdir -p ${DOCS}
	@echo "build <package>"
	@${ASCIIDOCTOR} ${ASCIIDOC_PRE} \
		-a <target1> \
		-a <target2> \
		./overview.adoc \
		-o ${DOCS}/<package>.html
```

Replace `<package>` with actual package name (e.g., `cbanalytics`). The -a flags specify target audiences. Do not change the first two lines.

### Includes

- No `xref` or `link` macros. Use `include::` with `[leveloffset=+1]` instead.
- Look for tag markers in source files for code inclusion.

### Admonitions

Use `NOTE:`, `TIP:`, `CAUTION:`, `WARNING:`, `IMPORTANT:` where appropriate.

## Step 9: Validate

Invoke -doc-reviewer to validate the documentation.

### Action

Use -doc-reviewer to check:
- Voice compliance (no AI-ish vocabulary)
- Structure (no meta commentary)
- Format (proper AsciiDoc syntax)
- Figures (design system colors)
- Code blocks (uses includes)

Address any issues identified.

## Step 10: File Size Check

Ensure documentation files stay manageable.

### Rules

- Maximum 500 lines per file
- Check with `wc -l <file>.adoc`
- Split large files using `include::` directives

## Typography Reference

Use Inter font as the primary typeface. Fallback to system fonts.

### Type Scale

| Style | Size | Weight | Line Height | Color | Usage |
|-------|------|--------|-------------|-------|-------|
| Section Label | 11px | 600 | 1.4 | #05289E | Uppercase, letter-spacing: 1.5px |
| Hero Headline | 36-52px | 700 | 1.1 | #0F1729 or white | Page headers |
| Section Title | 24-32px | 700 | 1.2 | #0F1729 | Section headers |
| Card Title | 18px | 600 | 1.3 | #0F1729 | Card headers |
| Body Text | 14-16px | 400 | 1.6-1.7 | #0F1729 or #64748B | Paragraphs |
| Caption | 12-13px | 400 | 1.5 | #64748B | Labels, metadata |
| Big Numbers/KPIs | 32-96px | 700 | 1.0 | #05289E | Metrics display |

## Data Visualization Guidelines

### Bar Charts

- Bar Fill: #05289E (primary), #CBFF9E (highlight), #1a3a2f (secondary)
- Corner Radius: 4px top corners only
- Grid Lines: #E2E8F0 dashed 1px, horizontal only
- Axis Labels: 11px #64748B
- Bar Gap: Proportional to bar width (8-16px)

### Line & Area Charts

- Line Stroke: #05289E 2px, smooth curves
- Area Fill: rgba(5, 40, 158, 0.1) (10% opacity)
- Data Points: #05289E 4px radius circles
- Secondary Lines: Use chart color sequence

### Pie & Donut Charts

- Donut Inner Radius: 0.618 ratio (golden ratio)
- Angular Inset: 1px gap between segments
- Max Segments: 4 (group smaller values as "Other")
- Stroke Width: 24px for donut

### Gauges & Progress Bars

- Track Color: #E2E8F0
- Progress Stroke Width: 8-14px
- Stroke Linecap: round
- Value Typography: 32px bold #0F1729
- Label Typography: 12px #64748B

### Chart Tooltips

- Background: #0F1729
- Text: White
- Border Radius: 6px
- Padding: 8px 12px (compact), 12px 16px (detailed)
- Box Shadow: 0 4px 12px rgba(0,0,0,0.15)

## Accessibility Requirements

### Contrast Requirements (WCAG AA)

- Normal text: minimum 4.5:1
- Large text (18px+ or 14px bold): minimum 3:1
- UI components: minimum 3:1

### Contrast Examples

| Combination | Ratio | Status |
|-------------|-------|--------|
| Blue on White | 8.5:1 | Pass |
| Navy on White | 16.7:1 | Pass |
| Forest on White | 12.3:1 | Pass |
| Navy on Green | 12.1:1 | Pass |
| Green on White | 1.5:1 | Fail |

### Accessibility Rules

- Never rely on color alone to convey information
- All form inputs must have visible, associated labels
- Provide visible focus indicators for keyboard navigation
- Support screen readers with proper ARIA labels

## Verification Checklist

- [ ] Document header set correctly
- [ ] Voice guidelines followed
- [ ] No AI-ish vocabulary detected
- [ ] Figures use design system colors
- [ ] Figures have proper image macro format
- [ ] Code uses include with tags (no inline Go)
- [ ] Icons used appropriately
- [ ] File under 500 lines
- [ ] Target audiences properly scoped
- [ ] Reviewer validation passed
