---
name: plan-article
description: "Create a detailed article outline with section structure, diagram specifications, and teaching flow. Use after research is complete, when planning a blog post structure. Requires research notes to exist."
allowed-tools: Read, Grep, Glob
---

# Article Planning Skill

## Input
$ARGUMENTS = topic name (must have research/<topic-slug>.md already)

## Process

### Step 1: Read Research Notes
Read research/<topic-slug>.md thoroughly.
Identify the core concepts, their dependencies, and the teaching order.

### Step 2: Define the Teaching Flow
Follow this exact pedagogical structure from the DeepSeek chapters:

```
A. Opening
   - Title (descriptive, not clickbait)
   - "This article covers" + 3-5 bullet points
   - Bridge from prerequisite knowledge
   - Roadmap figure showing where this fits

B. Intuition Section (Head 1)
   - The problem being solved
   - The core idea (no math yet)
   - A simple analogy or everyday comparison
   - First architectural diagram

C. Visual Walkthrough Section (Head 1)
   - Step-by-step with figures at every step
   - Running example with concrete numbers
   - Matrix shapes shown at every transformation
   - Multiple Head 2 subsections, one per component

D. Mathematical Foundation Section (Head 1)
   - Formal definitions (building on intuition)
   - Step-by-step derivation with figures
   - Key tricks or insights named explicitly
     (e.g., "The Absorption Trick")
   - Quantify the gains with exact numbers

E. Implementation Section (Head 1) [if applicable]
   - Code walkthrough
   - Annotated listings

F. Summary
   - Bullet points, each 2-3 sentences
```

### Step 3: Specify Every Diagram
For each section, list EVERY diagram needed.
Aim for 25 to 35 total.

For each diagram, specify:
```
- ID: fig_<descriptive_name>
- Section: which section it belongs to
- Type: architecture / flowchart / comparison / matrix-op / step-by-step / chart
- Description: exactly what it must show (2-4 sentences)
- Key elements: list the components, labels, colors, and flow direction
- Dimensions shown: what matrix shapes or numbers to display
- Caption: the full figure caption text
```

### Step 4: Define the Running Example
Choose a simple, consistent example:
- Input tokens (e.g., "The", "next", "day", "is")
- Embedding dimension (e.g., 8)
- Other relevant dimensions kept small (e.g., 4)
- Trace concrete values where possible

### Step 5: Write Section-by-Section Outline
For each Head 1 and Head 2 section:
- Title
- Key points to cover (3-5 bullets)
- Figures used (by ID)
- Transition sentence to next section

### Step 6: Save the Plan
Save to: plan/<topic-slug>_outline.md

Structure:
```
# Article Plan: <Topic>

## Title
<The article title>

## This Article Covers
- Point 1
- Point 2
- Point 3

## Running Example
<Define the example used throughout>

## Diagram Master List
| # | ID | Section | Type | Caption |
|---|-----|---------|------|---------|
| 1 | fig_roadmap | Opening | architecture | Figure X.1 ... |
| 2 | fig_... | ... | ... | ... |

## Section Outline

### Section 1: <Title> (Head 1)
**Key Points:**
- ...
**Figures:** fig_xxx, fig_yyy
**Transition:** "Now that we understand X, let's see how..."

#### Subsection 1.1: <Title> (Head 2)
**Key Points:**
- ...
**Figures:** fig_zzz
```

## Output
Save to plan/<topic-slug>_outline.md
Show the user the complete outline and ask for approval before proceeding.
Report the total number of diagrams planned.
