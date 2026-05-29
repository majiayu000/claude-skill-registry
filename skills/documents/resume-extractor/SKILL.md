---
name: resume-extractor
description: Extract and categorize yearly career data into structured components (what_i_did, my_thoughts, performance). Use when processing raw yearly markdown files into organized sections.
allowed-tools: Read, Write, Glob, Grep
context: fork
---

# Resume Extractor Skill

## Purpose
Transform raw yearly career documents into **three structured markdown files** that separate facts from reflections from metrics.

## Task
Given a year (e.g., 2024), process all related markdown files in that year's directory and extract:

1. **what_i_did_YYYY.md** - Factual accomplishments
   - Projects delivered
   - Technologies used
   - Systems built/maintained
   - Responsibilities held
   - Concrete deliverables

2. **my_thoughts_YYYY.md** - Personal growth & reflections
   - What I learned
   - Challenges faced and how I overcame them
   - Skills developed
   - Areas of growth
   - Key insights or "aha" moments

3. **performance_YYYY.md** - Quantifiable impact
   - KPIs and metrics
   - Business outcomes
   - Performance improvements (latency, throughput, revenue, etc.)
   - Team impact (people mentored, processes improved)
   - Recognition or achievements

## Instructions

### Step 1: Discover Source Files
- Use Glob to find all markdown files in the year directory (e.g., `./2024/*.md`)
- Read each file to understand the content structure
- Note: Files may be quarterly reviews, project timelines, retrospectives, or summaries

### Step 2: Intelligent Extraction
For each source file, use your LLM capabilities to:
- **Understand context**: Is this a quarterly review? A project description? A retrospective?
- **Categorize content**: Which sections belong to what_i_did vs my_thoughts vs performance?
- **Handle ambiguity**: Some content may fit multiple categories - use your judgment
- **Preserve specifics**: Keep dates, numbers, project names, technology names exact

### Step 3: Structure Output
Each output file should be well-organized with:
- Clear section headers (## Projects, ## Technologies, ## Learnings, etc.)
- Chronological ordering (Q1 → Q4)
- Consistent formatting
- Deduplication (if same achievement mentioned multiple times)

### Step 4: Validation
Before writing output files, verify:
- No information loss (all important details captured)
- No duplication across the three files
- Dates and metrics are accurate
- Proper markdown formatting

### Step 5: Write Output
Write the three files to the same directory as the source files:
- `YYYY/what_i_did_YYYY.md`
- `YYYY/my_thoughts_YYYY.md`
- `YYYY/performance_YYYY.md`

## Example Input/Output

### Input: `2024/1분기.md`
```markdown
# 2024 Q1 회고

이번 분기에는 백엔드 시스템 마이그레이션을 주도했다.
PostgreSQL에서 MongoDB로 전환하면서 쿼리 성능이 40% 개선되었다.
이 과정에서 NoSQL 데이터 모델링에 대해 깊이 배울 수 있었다.
```

### Output: `2024/what_i_did_2024.md`
```markdown
## Q1 - Projects
- Led backend system migration from PostgreSQL to MongoDB
- Redesigned data models for NoSQL architecture
```

### Output: `2024/performance_2024.md`
```markdown
## Q1 - Impact
- Query performance improved by 40% after migration
```

### Output: `2024/my_thoughts_2024.md`
```markdown
## Q1 - Learnings
- Gained deep understanding of NoSQL data modeling principles
- Learned trade-offs between relational and document databases
```

## Error Handling

If you encounter:
- **Missing files**: Report which year directory has no content
- **Ambiguous content**: Make best judgment and note uncertainty in comments
- **Invalid formats**: Parse what you can, skip malformed sections
- **Encoding issues**: Try UTF-8, then fallback to other encodings

## Success Criteria
- All three output files created
- Content properly categorized
- No information lost from source files
- Consistent formatting and structure
