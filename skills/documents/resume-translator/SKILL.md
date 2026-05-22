---
name: resume-translator
description: Translate and adapt resumes for different formats, languages, and audiences. Use when converting resumes to PDF/HTML, translating to other languages, or tailoring for specific roles.
allowed-tools: Read, Write, Edit, Bash
context: fork
---

# Resume Translator Skill

## Purpose
Transform a resume into **different versions** optimized for specific formats, languages, or target audiences using intelligent LLM-powered adaptation.

## Task
Given `RESUME.md` (or other resume file), produce:
- **Format translations**: PDF, HTML, DOCX, JSON, plain text
- **Language translations**: English, Korean, Japanese, etc.
- **Audience adaptations**: Technical IC, Engineering Manager, Executive, Startup

## Instructions

### Step 1: Read Source Resume
- Locate and read the source resume file (typically `RESUME.md`)
- Understand the structure, content, and tone
- Identify key sections and achievements

### Step 2: Determine Translation Type

Ask yourself (or user): What kind of translation is needed?

#### A. Format Translation
Convert to different file formats while preserving content:

**PDF** (via pandoc or weasyprint):
```bash
pandoc RESUME.md -o RESUME.pdf --pdf-engine=xelatex -V mainfont="Arial"
```

**HTML**:
- Generate semantic, clean HTML
- Include minimal CSS for professional styling
- Ensure print-friendly layout

**DOCX** (via pandoc):
```bash
pandoc RESUME.md -o RESUME.docx
```

**Plain Text**:
- Remove markdown formatting
- Preserve structure with ASCII characters
- 80-character line width for ATS compatibility

**JSON** (for ATS/APIs):
```json
{
  "name": "...",
  "contact": {...},
  "summary": "...",
  "experience": [
    {
      "company": "...",
      "role": "...",
      "dates": "...",
      "achievements": [...]
    }
  ],
  "skills": [...]
}
```

#### B. Language Translation
Translate content while maintaining:
- Professional terminology
- Industry-standard terms (keep in English if appropriate)
- Quantifiable metrics (preserve numbers)
- Tone and formality level

**Example: Korean → English**
```markdown
Before (Korean):
백엔드 시스템 마이그레이션을 주도하여 쿼리 성능을 40% 개선

After (English):
Led backend system migration, improving query performance by 40%
```

**Considerations**:
- English: Active voice, concise bullets
- Korean: More context, polite professional tone
- Japanese: Humble language (謙譲語) for own achievements

#### C. Audience Adaptation
Tailor content for specific target roles:

**Technical IC (Individual Contributor)**:
- Emphasize: Technical depth, specific technologies, architecture decisions
- Highlight: Code contributions, system design, performance optimizations
- Include: GitHub, technical blog, open-source contributions
- Language: Technical jargon appropriate, detailed metrics

**Engineering Manager**:
- Emphasize: Team leadership, mentoring, process improvements
- Highlight: Team size, hiring, performance management, cross-team collaboration
- Include: "Managed team of X engineers", "Improved team velocity by Y%"
- Language: Balance technical and people leadership

**Executive / Director**:
- Emphasize: Business impact, strategic vision, organizational influence
- Highlight: Revenue impact, cost savings, major initiatives, stakeholder management
- Include: Budget responsibility, headcount growth, P&L ownership
- Language: High-level, business outcomes over technical details

**Startup Role**:
- Emphasize: Versatility, scrappiness, 0-to-1 building, rapid iteration
- Highlight: Full-stack work, wearing multiple hats, fast shipping
- Include: Early-stage experience, ambiguity tolerance, lean methodologies
- Language: Energetic, entrepreneurial tone

**Academic/Research**:
- Emphasize: Publications, research contributions, theoretical knowledge
- Highlight: Papers, patents, conference talks, collaborations
- Include: Citations, h-index, research interests
- Language: Formal, scholarly tone

### Step 3: Execute Translation with LLM Intelligence

Use your language model capabilities to:
- **Understand context**: What aspects should be emphasized?
- **Adapt tone**: Match the target audience's expectations
- **Rewrite strategically**: Don't just translate word-for-word
- **Preserve truth**: Never exaggerate or fabricate
- **Optimize format**: Structure for the medium (PDF vs web vs ATS)

### Step 4: Quality Assurance

Before writing output:
- ✅ Target format/language/audience achieved
- ✅ All key achievements preserved
- ✅ Metrics and dates accurate
- ✅ Appropriate tone and terminology
- ✅ No information loss
- ✅ Proper formatting for medium

### Step 5: Write Output

Name output files clearly:
- `RESUME_EN.md` (English version)
- `RESUME_technical.md` (Technical IC version)
- `RESUME_manager.md` (EM version)
- `RESUME.pdf` (PDF format)
- `RESUME.html` (Web format)

## Translation Examples

### Example 1: Technical IC Adaptation

**Original (General)**:
```markdown
- Led backend migration from PostgreSQL to MongoDB
```

**Adapted (Technical IC)**:
```markdown
- Architected and executed zero-downtime backend migration from PostgreSQL to MongoDB using dual-write pattern, implementing custom data consistency validation framework in Python to ensure 100% data integrity across 500GB dataset
```

Notice: Added technical details, specific patterns, tools, scale.

### Example 2: EM Adaptation

**Original (General)**:
```markdown
- Led backend migration from PostgreSQL to MongoDB
```

**Adapted (Engineering Manager)**:
```markdown
- Led cross-functional team of 5 engineers through critical backend migration, establishing clear milestones and risk mitigation strategies that delivered the project 2 weeks ahead of schedule with zero customer-facing incidents
```

Notice: Added team leadership, project management, stakeholder outcomes.

### Example 3: Language Translation (Korean → English)

**Original (Korean)**:
```markdown
실시간 스트리밍 모자이크 처리 시스템을 설계 및 구축하여 10,000개 이상의 동시 CCTV 스트림을 99.9% 가동률로 처리
```

**Translated (English)**:
```markdown
Designed and deployed real-time streaming mosaic processing system handling 10K+ concurrent CCTV streams with 99.9% uptime
```

Notice: Natural English phrasing, preserved metrics, professional tone.

### Example 4: Format Translation (Markdown → HTML)

**Original (Markdown)**:
```markdown
## Work Experience

### Senior Software Engineer | Company | 2020-Present

- Led backend migration
```

**Translated (HTML)**:
```html
<section id="experience">
  <h2>Work Experience</h2>
  <article class="job">
    <h3>Senior Software Engineer</h3>
    <p class="company-dates">
      <span class="company">Company</span> |
      <span class="dates">2020-Present</span>
    </p>
    <ul class="achievements">
      <li>Led backend migration</li>
    </ul>
  </article>
</section>
```

With accompanying CSS for professional styling.

## Advanced Translation Strategies

### Multi-Dimensional Translation
Combine multiple translation types:
- "Korean → English + Technical IC focus + PDF format"
- "Shorten to 1-page + Executive audience + HTML"

### Conditional Emphasis
Based on target audience, selectively emphasize:
- **For Google/Meta**: Distributed systems, scale
- **For startups**: Breadth, rapid shipping
- **For finance**: Reliability, security, compliance
- **For AI companies**: ML/AI projects, research

### Feedback Integration
If user provides feedback:
- "Make it more concise" → Reduce bullet points, tighter language
- "Highlight leadership" → Rewrite to emphasize team/people aspects
- "Add more technical depth" → Include architecture decisions, patterns

## Error Handling

- **Missing dependencies** (pandoc, weasyprint): Inform user, provide installation instructions
- **Unsupported language**: Attempt best-effort translation or inform limitations
- **Format incompatibility**: Suggest alternative formats
- **Content too long for target**: Ask user for prioritization guidance

## Success Criteria
- Output file created in requested format/language/style
- Content accurately represents source resume
- Appropriate for target audience
- Professional quality
- No information loss or exaggeration
