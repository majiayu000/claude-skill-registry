---
name: linkedin_job_resume_optimizer
description: |
  Automates end-to-end job search workflow: searches LinkedIn for AI-related remote jobs,
  extracts job descriptions, reads base resume, generates ATS-optimized tailored resumes,
  performs skill gap analysis, suggests interview prep questions, and provides LinkedIn
  profile optimization recommendations. Use when: (1) User needs job-specific resume
  tailoring, (2) Preparing for job applications with targeted optimization, (3) Requires
  skill gap analysis between resume and job requirements, (4) Needs interview preparation
  questions based on skill gaps.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
model: claude-sonnet-4-5
---

# LinkedIn Job Resume Optimizer

Comprehensive job search automation with resume tailoring and interview preparation.

## Overview

This skill orchestrates a complete job application workflow:
1. Search LinkedIn for relevant remote AI jobs
2. Extract full job descriptions and requirements
3. Analyze base resume to extract skills and experience
4. Generate ATS-optimized, job-tailored resumes
5. Perform skill gap analysis
6. Generate targeted interview preparation questions
7. Suggest LinkedIn profile optimizations

## Workflow Diagram

```
User Request
    ↓
Workflow Orchestrator
    ↓
┌─────────────────┬──────────────────┬─────────────────┐
│ LinkedIn        │ Resume           │ ATS             │
│ Scraper         │ Analyzer         │ Optimizer       │
│ (Playwright)    │ (Pandoc+Docx)    │ (NLP)           │
└─────────────────┴──────────────────┴─────────────────┘
    ↓
Gap Analyzer (Compare skills)
    ↓
Question Generator (Interview prep)
    ↓
Final Report (Summary + File locations)
```

## Prerequisites

### 1. Playwright MCP Server (for LinkedIn automation)

Start the server before running this skill:
```bash
bash /mnt/d/Ali_Home/Learning/AgenticAI/AI-P009/Assignments/ProjectA1/resume_optimizer/.claude/skills/browsing-with-playwright/scripts/start-server.sh
```

### 2. Base Resume

Ensure resume exists at configured path (default: `/mnt/d/Ali_Home/Learning/AgenticAI/AI-P009/Assignments/ProjectA1/resume_optimizer/resume/resume06012026.docx`)

### 3. System Dependencies

```bash
# Core tools
sudo apt-get install pandoc python3 python3-pip nodejs npm

# Optional (for PDF export)
sudo apt-get install libreoffice poppler-utils
```

### 4. Python Packages

```bash
pip install python-docx spacy nltk pandas requests
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt stopwords
```

### 5. Node Packages

```bash
npm install -g @playwright/mcp
```

## Quick Start

### Basic Usage

```bash
python3 scripts/workflow_orchestrator.py \
  --job-keywords "AI Engineer remote" \
  --job-count 2
```

### With Custom Resume Path

```bash
python3 scripts/workflow_orchestrator.py \
  --resume-path "/path/to/your/resume.docx" \
  --job-keywords "Machine Learning Engineer" \
  --job-count 2 \
  --output-dir "./custom_output"
```

## Step-by-Step Workflow

### Phase 1: Initialize Playwright Server

```bash
bash /mnt/d/Ali_Home/Learning/AgenticAI/AI-P009/Assignments/ProjectA1/resume_optimizer/.claude/skills/browsing-with-playwright/scripts/start-server.sh
```

Verify server is running:
```bash
curl http://localhost:8808
```

### Phase 2: Search LinkedIn Jobs

```bash
python3 scripts/linkedin_scraper.py \
  --keywords "AI Engineer remote" \
  --count 2 \
  --output jobs.json
```

**Output**: `jobs.json` containing:
```json
[
  {
    "title": "Senior AI Engineer",
    "company": "TechCorp",
    "url": "https://linkedin.com/jobs/view/12345",
    "description": "Full job description...",
    "required_skills": ["Python", "TensorFlow", "MLOps"],
    "preferred_skills": ["Kubernetes", "AWS"]
  }
]
```

### Phase 3: Extract Base Resume Skills

```bash
# Convert DOCX to markdown
pandoc --track-changes=accept /mnt/d/Ali_Home/Learning/AgenticAI/AI-P009/Assignments/ProjectA1/resume_optimizer/resume/resume06012026.docx -o resume.md

# Extract skills
python3 scripts/resume_analyzer.py --resume-md resume.md --output base_skills.json
```

**Output**: `base_skills.json` with skills inventory

### Phase 4: Generate Tailored Resumes

For each job, generate ATS-optimized resume:
```bash
python3 scripts/ats_optimizer.py \
  --base-resume /mnt/d/Ali_Home/Learning/AgenticAI/AI-P009/Assignments/ProjectA1/resume_optimizer/resume/resume06012026.docx \
  --job-description jobs.json \
  --job-index 0 \
  --output "resume_tailored_Senior_AI_Engineer.docx"
```

### Phase 5: Perform Gap Analysis

```bash
python3 scripts/gap_analyzer.py \
  --base-skills base_skills.json \
  --job-requirements jobs.json \
  --output gap_analysis.json
```

**Output**: `gap_analysis.json`
```json
[
  {
    "job_title": "Senior AI Engineer",
    "skill_gaps": [
      {
        "skill": "Kubernetes",
        "gap_type": "missing",
        "importance": "high",
        "related_experience": ["Docker experience in current role"]
      }
    ],
    "interview_questions": [
      "Explain your understanding of Kubernetes orchestration...",
      "How would you design a Kubernetes deployment for ML models?",
      "..."
    ],
    "linkedin_updates": {
      "about_section": "Add: 'Experienced in containerization with Docker, transitioning to Kubernetes for production ML deployments'",
      "skills_to_add": ["Kubernetes", "Container Orchestration", "MLOps"]
    }
  }
]
```

### Phase 6: Generate Interview Questions

```bash
python3 scripts/question_generator.py \
  --gap-analysis gap_analysis.json \
  --questions-per-gap 10 \
  --output interview_prep.md
```

### Phase 7: Cleanup

```bash
bash /mnt/d/Ali_Home/Learning/AgenticAI/AI-P009/Assignments/ProjectA1/resume_optimizer/.claude/skills/browsing-with-playwright/scripts/stop-server.sh
```

## Configuration

Edit `config.json` in skill directory:

```json
{
  "resume_path": "/mnt/d/Ali_Home/Learning/AgenticAI/AI-P009/Assignments/ProjectA1/resume_optimizer/resume/resume06012026.docx",
  "output_directory": "./resume_optimizer/output",
  "playwright_port": 8808,
  "job_search": {
    "default_keywords": "AI Engineer remote",
    "default_count": 2,
    "location": "Remote"
  },
  "ats_optimization": {
    "keyword_density_target": 0.75,
    "exact_match_priority": true,
    "preserve_formatting": true
  },
  "interview_prep": {
    "questions_per_gap": 10,
    "include_behavioral": true,
    "include_technical": true
  }
}
```

## ATS Optimization Strategies

See [references/ats-optimization-guide.md](references/ats-optimization-guide.md) for detailed strategies including:

### Keyword Density
- **Required Skills**: 70-80% coverage
- **Preferred Skills**: 40-50% coverage
- **Exact Match**: Use exact phrases from job description
- **Context Integration**: Weave keywords naturally into experience descriptions

### Keyword Placement Priority
1. **Professional Summary** (highest ATS weight)
   - Include job title keyword
   - Top 3-5 required skills
   - Industry-specific terminology

2. **Skills Section** (exact match critical)
   - Mirror job posting's skills terminology exactly
   - Group by category if job posting does

3. **Experience Descriptions** (context + keywords)
   - Integrate keywords into achievement statements
   - Use action verbs + keyword + quantifiable result

### Natural Integration Techniques

**Action Verb + Keyword + Result**:
```
Before: "Worked on machine learning projects"
After: "Developed TensorFlow-based ML models, reducing inference time by 30%"
```

**Technology Stack Enumeration**:
```
Before: "Built backend systems"
After: "Built scalable backend systems using Python, Docker, and Kubernetes on AWS infrastructure"
```

## LinkedIn Automation

See [references/linkedin-automation.md](references/linkedin-automation.md) for:

- Navigation patterns for LinkedIn job search
- Element selectors and snapshot references
- Rate limiting and anti-bot detection strategies
- Fallback strategies if elements change

**Key Points**:
- Implement random delays (1-3 seconds between actions)
- Use `--shared-browser-context` flag for Playwright MCP
- Handle rate limiting with exponential backoff
- Parse snapshots for job card refs

## Interview Question Generation

See [references/interview-prep-patterns.md](references/interview-prep-patterns.md) for:

- STAR method question templates
- Technical depth assessment questions
- Behavioral questions for skill gaps
- System design scenarios

**Question Distribution**:
- **Missing Skills**: 40% fundamentals, 30% transferable experience, 30% scenarios
- **Weak Skills**: 40% depth assessment, 30% practical application, 30% troubleshooting

## Error Handling

### No Jobs Found
```python
if len(jobs) == 0:
    print("No jobs found matching criteria. Suggestions:")
    print("- Broaden search keywords")
    print("- Remove 'remote' filter")
    print("- Try alternative job titles")
    sys.exit(1)
```

### Resume Read Errors
```python
try:
    resume_text = extract_resume(resume_path)
except FileNotFoundError:
    print(f"Resume not found at {resume_path}")
    print("Please provide valid resume path with --resume-path")
    sys.exit(1)
except Exception as e:
    print(f"Error reading resume: {e}")
    print("Ensure resume is valid .docx format")
    sys.exit(1)
```

### LinkedIn Rate Limiting
```python
# Implement exponential backoff
for attempt in range(3):
    try:
        job_data = scrape_job(url)
        break
    except RateLimitError:
        wait_time = 2 ** attempt * 5  # 5s, 10s, 20s
        time.sleep(wait_time)
```

### Playwright Connection Failures
- Pre-flight check: Verify server running before job search
- Auto-restart server if connection fails
- Retry with exponential backoff (3 attempts)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Playwright not responding | Restart: `bash scripts/stop-server.sh && bash scripts/start-server.sh` |
| LinkedIn blocks automation | Add wait times, use headless:false, rotate user agents |
| Resume conversion fails | Verify pandoc installed: `pandoc --version` |
| ATS optimization weak | Review keyword extraction, increase density target in config.json |
| No skill gaps detected | Lower similarity threshold in gap_analyzer.py |
| Python packages missing | Run: `pip install python-docx spacy nltk pandas requests` |
| spaCy model not found | Run: `python -m spacy download en_core_web_sm` |

## Output Summary Format

After running the workflow, you'll receive a summary report:

```markdown
# Job Search Results Summary

## Jobs Found: 2

### Job 1: Senior AI Engineer - TechCorp
- **LinkedIn URL**: https://linkedin.com/jobs/view/12345
- **Tailored Resume**: ./resume_optimizer/output/resume_tailored_Senior_AI_Engineer.docx
- **Key Requirements**: Python, TensorFlow, MLOps, Kubernetes
- **Skill Gaps**: Kubernetes (High priority), AWS Sagemaker (Medium)
- **Interview Prep Questions**: 20 questions generated (see interview_prep.md)

### Job 2: Machine Learning Engineer - AI Startup
- **LinkedIn URL**: https://linkedin.com/jobs/view/67890
- **Tailored Resume**: ./resume_optimizer/output/resume_tailored_Machine_Learning_Engineer.docx
- **Key Requirements**: PyTorch, Docker, CI/CD, Model deployment
- **Skill Gaps**: PyTorch (High priority - similar TensorFlow experience)
- **Interview Prep Questions**: 15 questions generated (see interview_prep.md)

## LinkedIn Profile Recommendations

### About Section Updates
- Add: "Specialized in MLOps with focus on production-scale deployments"
- Emphasize: Kubernetes orchestration experience
- Highlight: Cross-functional collaboration in AI product development

### Skills to Add
1. Kubernetes (High priority - both jobs)
2. MLOps (Critical keyword)
3. Model Deployment
4. CI/CD for ML

## Next Steps
1. Review tailored resumes in ./resume_optimizer/output/
2. Study interview prep questions in interview_prep.md
3. Update LinkedIn profile per recommendations above
4. Apply to jobs with tailored resumes
```

## Integration with Existing Skills

This skill leverages:

### browsing-with-playwright
- LinkedIn job search automation
- Browser navigation and snapshot parsing
- Start server: `bash scripts/start-server.sh`
- Stop server: `bash scripts/stop-server.sh`

### docx
- Resume reading using pandoc
- Tailored resume generation
- Convert: `pandoc --track-changes=accept resume.docx -o resume.md`

## Advanced Usage

### Manual Job URLs (Skip LinkedIn Scraping)

If you prefer to provide job URLs manually:

1. Create `jobs_manual.json`:
```json
[
  {
    "title": "AI Engineer",
    "company": "CompanyName",
    "url": "https://linkedin.com/jobs/view/12345",
    "description": "Paste full job description here..."
  }
]
```

2. Run workflow with manual jobs:
```bash
python3 scripts/workflow_orchestrator.py \
  --manual-jobs jobs_manual.json \
  --skip-linkedin
```

### Custom Keyword Extraction

Override automatic skill extraction:

```bash
python3 scripts/ats_optimizer.py \
  --base-resume resume.docx \
  --job-description jobs.json \
  --job-index 0 \
  --custom-keywords "Python,TensorFlow,Kubernetes,AWS" \
  --output tailored_resume.docx
```

## Dependencies Summary

### Required
- Python 3.8+
- Node.js 14+
- pandoc
- browsing-with-playwright skill
- docx skill

### Python Packages
- python-docx
- spacy
- nltk
- pandas
- requests

### Node Packages
- @playwright/mcp

## Performance

- **LinkedIn Search**: 30-90 seconds (2 jobs)
- **Resume Analysis**: 10-20 seconds
- **Resume Tailoring**: 30-60 seconds per job
- **Gap Analysis**: 20-30 seconds
- **Interview Prep**: 40-60 seconds
- **Total Estimated Time**: 2-4 minutes for 2 jobs

## Limitations

1. **LinkedIn Access**: Requires LinkedIn to be accessible (may need login for some content)
2. **Job Count**: Recommended maximum 5 jobs per session to avoid rate limiting
3. **Resume Format**: Only supports .docx format (not .doc or PDF)
4. **Language**: Optimized for English resumes and job descriptions
5. **Technical Roles**: Best suited for technical roles (AI, ML, Engineering)

## Security & Privacy

- **Local Processing**: All resume processing happens locally
- **No Storage**: No resume data is stored remotely
- **Browser Automation**: Uses local Playwright instance
- **Data Privacy**: Job descriptions and resumes remain on your machine

## License

This skill is part of the Claude Code skills ecosystem.
