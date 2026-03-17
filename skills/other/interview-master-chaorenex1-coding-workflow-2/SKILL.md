---
name: interview-master
description: This skill should be used when the user asks to "generate interview questions", "prepare for interview", "optimize resume", "conduct mock interview", "analyze git commits for resume", "generate resume from code", "review my resume", or mentions interview preparation, career assistance, or extracting project experience from git history. Provides comprehensive interview and career development guidance for both job seekers and interviewers.
version: 0.1.0
---

# Interview Master - Comprehensive Career & Interview Assistant

## Purpose

Interview Master is a specialized skill that provides end-to-end support for technical interview preparation and career development. It serves both job seekers preparing for interviews and interviewers designing effective assessments. The skill's unique capability is generating professional resumes by analyzing git commit history to extract technical skills, project impact, and contributions.

## When to Use This Skill

Use this skill when:

- Generating interview questions for specific roles or seniority levels
- Preparing for technical interviews (algorithms, system design, behavioral)
- Optimizing or reviewing resume content
- Conducting mock interviews with realistic scenarios
- Analyzing git repositories to generate resume content
- Extracting technical expertise and project contributions from code history
- Creating interview preparation roadmaps
- Evaluating candidate technical skills through code analysis

## Core Capabilities

### 1. Interview Question Generation

Generate role-specific interview questions tailored to position requirements, seniority level, and technical stack.

**Process:**
1. Identify target role, seniority (junior/mid/senior/staff), and tech stack
2. Consult `references/interview-questions-bank.md` for question patterns
3. Generate questions across categories:
   - Technical fundamentals
   - Problem-solving and algorithms
   - System design (for senior+ roles)
   - Behavioral and situational
   - Role-specific deep dives
4. Include follow-up questions and evaluation criteria
5. Provide answer guidelines for interviewers

Typical output includes 10-15 questions with difficulty ratings, estimated time, and evaluation rubrics.

### 2. Resume Optimization

Analyze and improve resume content for technical roles with actionable feedback.

**Process:**
1. Review resume structure, formatting, and content
2. Reference `references/resume-best-practices.md` for industry standards
3. Evaluate:
   - Technical skills presentation
   - Project descriptions and impact metrics
   - Achievement quantification
   - ATS (Applicant Tracking System) compatibility
   - Keyword optimization for target roles
4. Provide specific improvement suggestions with before/after examples
5. Check for common mistakes (typos, inconsistent formatting, vague descriptions)

Consult `examples/good-resume-examples.md` for reference patterns.

### 3. Mock Interview Simulation

Conduct realistic mock interviews with real-time feedback and performance evaluation.

**Process:**
1. Establish interview context (role, company type, interview stage)
2. Reference `references/interview-flow.md` for realistic pacing
3. Ask questions progressively, adapting difficulty based on responses
4. Provide hints if candidate struggles
5. Evaluate responses on:
   - Technical accuracy
   - Communication clarity
   - Problem-solving approach
   - Time management
6. Deliver constructive feedback with improvement areas

See `examples/mock-interview-dialogue.md` for interaction patterns.

### 4. Git-Based Resume Generation (Signature Feature)

Analyze git commit history to automatically generate resume content highlighting technical contributions and project impact.

**Workflow:**

**Step 1: Collect Repository Information**
- Identify target repository path
- Determine author name/email to analyze
- Specify time range (optional, default: all history)

**Step 2: Execute Analysis Scripts**

Use the following scripts in sequence:

1. **`scripts/analyze-commits.sh`** - Extract commit history
   ```bash
   ./scripts/analyze-commits.sh <author> <repo-path> [start-date] [end-date]
   ```
   Output: Commit count, frequency, file change patterns

2. **`scripts/extract-tech-stack.sh`** - Identify technologies
   ```bash
   ./scripts/extract-tech-stack.sh <repo-path> <author>
   ```
   Output: Programming languages, frameworks, tools detected from code changes
   Reference: `references/tech-stack-keywords.md` for keyword matching

3. **`scripts/calculate-impact.py`** - Quantify contributions
   ```bash
   python scripts/calculate-impact.py <repo-path> <author>
   ```
   Output: Lines added/removed, files modified, feature-critical commits
   Reference: `references/project-impact-metrics.md` for impact calculation

4. **`scripts/generate-resume-data.sh`** - Aggregate results
   ```bash
   ./scripts/generate-resume-data.sh <author> <repo-path>
   ```
   Output: Structured JSON with resume-ready content

**Step 3: Generate Resume Content**

Transform analysis into professional resume sections:

1. **Technical Skills Section**
   - Group technologies by category (languages, frameworks, tools, databases)
   - Prioritize by usage frequency and recency

2. **Project Experience Section**
   - Identify major features/modules from commit messages
   - Quantify impact (e.g., "Developed authentication system handling 10K+ daily users")
   - Highlight technical challenges solved
   - Use action verbs: "Architected", "Implemented", "Optimized", "Refactored"

3. **Key Achievements**
   - Extract notable contributions (large refactors, performance improvements, critical bug fixes)
   - Convert git data to business impact when possible
   - Include metrics from `references/project-impact-metrics.md`

**Step 4: Format and Review**

- Apply `assets/resume-template.md` structure
- Ensure ATS compatibility (plain text format, standard section headings)
- Cross-reference with `examples/good-resume-examples.md` for quality standards
- Validate technical terminology accuracy

**Example Usage:**
```
User: "Analyze my commits in this repository and generate resume content"
Assistant:
1. Runs analyze-commits.sh to get 247 commits over 18 months
2. Extracts tech stack: React, TypeScript, Node.js, PostgreSQL, Docker
3. Calculates impact: 15K lines added, 12 major features
4. Generates resume section:
   "Software Engineer | E-commerce Platform (Jan 2023 - Present)
   - Architected and implemented user authentication system using JWT and OAuth 2.0, serving 50K+ daily active users
   - Developed RESTful API with Node.js and Express, improving response time by 40% through query optimization
   - Built responsive admin dashboard with React and TypeScript, reducing content management time by 60%
   - Containerized application with Docker, enabling consistent deployment across 3 environments"
```

### 5. Interview Preparation Guidance

Create personalized preparation roadmaps for technical interviews.

**Process:**
1. Assess candidate current level and target role
2. Generate study plan covering:
   - Algorithm and data structures (reference: `references/algorithm-prep.md`)
   - System design concepts (reference: `references/system-design-prep.md`)
   - Behavioral interview techniques (reference: `references/behavioral-interview.md`)
3. Provide timeline-based milestones (2 weeks, 1 month, 3 months)
4. Include practice resources and mock interview schedules
5. Track preparation progress and adjust plan

## Workflow Integration

### For Job Seekers

1. **Resume Generation**: Run git analysis on personal projects → generate technical resume content
2. **Resume Optimization**: Review generated/existing resume → receive improvement suggestions
3. **Interview Prep**: Follow preparation roadmap → practice with mock interviews
4. **Mock Interview**: Conduct simulated interview → receive feedback → iterate

### For Interviewers

1. **Question Design**: Specify role requirements → generate tailored question set
2. **Evaluation Framework**: Use provided rubrics → standardize candidate assessment
3. **Interview Calibration**: Reference mock interview examples → align interview style

## Additional Resources

### Reference Files

Detailed guides and knowledge bases:
- **`references/interview-questions-bank.md`** - Comprehensive question library by role and category
- **`references/resume-best-practices.md`** - Industry-standard resume writing guidelines
- **`references/algorithm-prep.md`** - Algorithm interview preparation roadmap
- **`references/system-design-prep.md`** - System design concepts and practice problems
- **`references/behavioral-interview.md`** - STAR method and behavioral question patterns
- **`references/tech-stack-keywords.md`** - Technology keyword database for code analysis
- **`references/project-impact-metrics.md`** - Impact quantification standards

### Example Files

Working examples and templates:
- **`examples/good-resume-examples.md`** - High-quality resume samples for various roles
- **`examples/interview-questions-set.md`** - Complete interview question sets
- **`examples/mock-interview-dialogue.md`** - Realistic interview conversation flows
- **`examples/git-analysis-output.json`** - Sample git analysis results

### Script Utilities

Automation tools for git analysis:
- **`scripts/analyze-commits.sh`** - Extract commit history and patterns
- **`scripts/extract-tech-stack.sh`** - Identify technologies from codebase
- **`scripts/calculate-impact.py`** - Quantify code contributions and impact
- **`scripts/generate-resume-data.sh`** - Aggregate analysis into resume format

### Asset Templates

Ready-to-use templates:
- **`assets/resume-template.md`** - Markdown resume template
- **`assets/resume-template.json`** - Structured resume data schema

## Best Practices

1. **Resume Generation**: Always validate generated content for accuracy; git commits may contain technical jargon that needs business-friendly translation
2. **Interview Questions**: Adapt difficulty to candidate level; avoid questions beyond role requirements
3. **Mock Interviews**: Maintain realistic pacing; provide hints before revealing answers
4. **Feedback Delivery**: Be constructive and specific; focus on actionable improvements
5. **Privacy**: When analyzing git history, ensure proper authorization; anonymize sensitive project details if needed

## Common Use Cases

**Scenario 1: Junior Developer Seeking First Role**
- Generate resume from university project repositories
- Focus on technical skills and learning trajectory
- Provide entry-level interview prep roadmap

**Scenario 2: Senior Engineer Career Transition**
- Analyze contributions across multiple projects
- Highlight system design and architecture work
- Prepare for staff-level system design interviews

**Scenario 3: Hiring Manager Building Interview Process**
- Generate role-specific question bank
- Establish evaluation criteria
- Calibrate interview difficulty

**Scenario 4: Career Switcher with Limited Resume Content**
- Mine git history for hidden technical achievements
- Quantify impact of side projects
- Frame bootcamp/self-taught experience professionally

## Technical Requirements

- **Git access**: Scripts require read access to target repositories
- **Shell environment**: Bash 4.0+ for shell scripts
- **Python 3.8+**: For impact calculation script
- **Git command-line**: Version 2.20+ installed

## Limitations

- Git analysis quality depends on commit message clarity; vague messages yield less useful insights
- Cannot access private repositories without proper authentication
- Project impact quantification is heuristic-based; manual validation recommended
- Generated resume content requires human review for context and accuracy
