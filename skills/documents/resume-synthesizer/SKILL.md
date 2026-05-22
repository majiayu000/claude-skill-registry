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
> Senior Software Engineer with 6+ years building scalable AI/ML systems. Led backend migrations improving query performance by 40%, deployed real-time streaming systems processing 10K+ events/sec, and architected cloud infrastructure serving 100K+ users. Deep expertise in Python, Go, distributed systems, and MLOps, with proven ability to translate complex technical challenges into business value.

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

### Senior Software Engineer | Current Company | 2020 - Present

**2024**
- Led backend migration from PostgreSQL to MongoDB, reducing query latency by 40% and improving system scalability
- Architected real-time streaming mosaic processing system handling 10K+ concurrent CCTV streams
- Mentored 3 junior engineers on distributed systems design patterns learned through production challenges

**2023**
- Designed and deployed Naver Cloud tagging system processing 100K+ resources with 99.9% uptime
- Reduced infrastructure costs by 25% through automated resource optimization and monitoring
- Developed expertise in cloud-native architectures and multi-cloud deployment strategies
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
`what_i_did_2024.md`: "Led backend migration to MongoDB"
`performance_2024.md`: "Query latency reduced by 40%, handled 10K QPS"
`my_thoughts_2024.md`: "Learned NoSQL data modeling, understood trade-offs"

### Synthesized Output:
```markdown
- Architected and led critical backend migration from PostgreSQL to MongoDB, applying NoSQL data modeling principles to achieve 40% latency reduction while scaling to 10K+ queries per second
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
