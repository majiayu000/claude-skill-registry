---
name: resume-synthesizer
description: Synthesize structured career components (what_i_did, my_thoughts, performance files) into a cohesive professional resume. Use when generating resumes from extracted yearly data.
allowed-tools: Read, Write, Glob, Grep
context: fork
---

# Resume Synthesizer Skill

## Purpose
Create a **polished, professional resume** by intelligently combining structured career data from multiple years into a coherent narrative.

## Task
Generate `RESUME.md` by synthesizing:
- `what_i_did_*.md` files (all years)
- `my_thoughts_*.md` files (all years)
- `performance_*.md` files (all years)
- `basic_info.md` (static info: name, contact, education, military, certs)

## Instructions

### Step 1: Discover and Read All Components
- Use Glob to find all `what_i_did_*.md`, `my_thoughts_*.md`, `performance_*.md` files
- Read `basic_info.md` for static info (name, contact, education, military, certs, career)
- Sort by year (most recent first)

### Step 2: Analyze Content with LLM Intelligence
For each year's data:
- **Identify themes**: What were the major accomplishments?
- **Find patterns**: Career progression, skill evolution, increasing impact
- **Extract highlights**: Most impressive projects, biggest wins
- **Connect dots**: How do learnings translate to results?

### Step 3: Synthesize Resume Structure

#### Header
- Name, title, contact info (from basic_info.md)
- One-line value proposition (synthesized from overall career arc)

#### Professional Summary (3-4 sentences)
Synthesize from **all years**:
- Years of experience
- Core expertise areas (from what_i_did files)
- Key strengths (from my_thoughts files)
- Signature achievements (from performance files)

**Example**:
> [Role] with [X]+ years building [domain] systems. Led [project type] improving [metric] by [X]%, deployed [system type] processing [X]+ [unit], and architected [infrastructure] serving [X]+ users. Deep expertise in [tech stack], with proven ability to translate complex technical challenges into business value.

#### Technical Skills
Aggregate from all `what_i_did_*.md` files:
- **Languages**: Python, Go, JavaScript, etc.
- **Frameworks**: Django, FastAPI, React, etc.
- **AI/ML**: TensorFlow, PyTorch, LangChain, etc.
- **Infrastructure**: Docker, Kubernetes, AWS, etc.
- **Databases**: PostgreSQL, MongoDB, Redis, etc.

Group logically, prioritize by recency and proficiency.

#### Work Experience
Synthesize from all three file types:
- **Format**: Company | Role | Dates
- **Content**: For each role/year:
  - 3-5 bullet points per year
  - Start with impact (performance) → action (what_i_did) → context (my_thoughts)
  - Use strong action verbs (Led, Architected, Delivered, Optimized)
  - **Quantify everything** from performance files

**Example**:
```markdown
## Work Experience

### [Role] | [Company] | [Start Year] - [End Year/Present]

**[Year 2]**
- Led [project name] from [old tech] to [new tech], reducing [metric] by [X]% and improving [outcome]
- Architected [system type] handling [X]+ [units] with [performance metric]
- Mentored [X] [junior/mid-level] engineers on [technical area] learned through [experience]

**[Year 1]**
- Designed and deployed [system name] processing [X]+ [units] with [X]% uptime
- Reduced [cost/time/resource] by [X]% through [method] and [technique]
- Developed expertise in [technical domain] and [related skill]
```

#### Key Projects (Optional section)
If there are standout projects that deserve spotlight:
- Select top 3-5 most impressive projects across all years
- Provide brief description + impact metrics
- Use when projects are more notable than chronological experience

#### Education & Certifications
From basic_info.md - keep concise.

### Step 4: Apply Professional Polish

**Tone**:
- Confident, results-oriented
- Active voice, strong verbs
- Professional but not stiff

**Language**:
- Korean for narrative (if Profile is in Korean)
- English for technical terms
- Consistent terminology

**Formatting**:
- Clean markdown with clear hierarchy
- Consistent bullet point style
- Proper spacing and readability

### Step 5: Quality Checks

Before writing output:
- ✅ All metrics from performance files included
- ✅ No redundancy or repetition
- ✅ Chronological order (recent first)
- ✅ Learnings from my_thoughts integrated naturally
- ✅ Projects from what_i_did accurately represented
- ✅ No grammatical errors
- ✅ Consistent formatting

### Step 6: Write Output
Write to `RESUME.md` in the base directory.

## Synthesis Principles

### DO:
- **Tell a story**: Career progression should be clear
- **Show impact**: Every bullet point should demonstrate value
- **Be specific**: "Improved performance by 40%" not "Made system faster"
- **Connect learnings to results**: "Applied distributed systems patterns learned in Q1 to architect..."
- **Highlight growth**: Show increasing responsibility and impact over time

### DON'T:
- Copy-paste from source files verbatim
- Include every single detail (be selective)
- Use generic phrases ("Worked on various projects")
- Forget to quantify achievements
- Lose the human element (learnings and growth)

## Example Synthesis

### Input Files:
`what_i_did_YYYY.md`: "Led [system] migration to [new tech]"
`performance_YYYY.md`: "[Metric] reduced by [X]%, handled [X] [unit]"
`my_thoughts_YYYY.md`: "Learned [concept], understood [principles]"

### Synthesized Output:
```markdown
- Architected and led critical [system] migration from [old tech] to [new tech], applying [technical principles] to achieve [X]% [metric] reduction while scaling to [X]+ [unit]
```

Notice how it:
- Combines all three sources
- Leads with action and impact
- Weaves in learnings naturally
- Quantifies results
- Shows technical depth

## Customization Options

You may receive additional instructions like:
- "Focus on leadership aspects" → Emphasize mentoring, architecture decisions
- "Technical depth preferred" → Include more technology details, design patterns
- "One-page format" → Be more selective, condensed bullets
- "For startup role" → Emphasize rapid iteration, scrappiness, breadth

Adapt synthesis strategy accordingly using your LLM judgment.

## Success Criteria
- Resume is coherent and reads like a unified narrative
- All key achievements from performance files are highlighted
- Career growth is evident
- Technical skills are accurately represented
- Professional, polished, ready to send
