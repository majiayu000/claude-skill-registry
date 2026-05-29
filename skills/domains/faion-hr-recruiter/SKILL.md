---
name: faion-hr-recruiter
description: "HR recruiting: talent acquisition, employer branding, interviews, onboarding, DEI."
user-invocable: false
allowed-tools: Read, Write, Edit, Task, WebSearch, AskUserQuestion, TodoWrite, Glob
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# HR Recruiter Domain Skill

**Communication: User's language. Job descriptions and HR documents: target audience language.**

## Purpose

Orchestrates all HR and recruiting activities from talent acquisition strategy to employee retention. Covers employer branding, structured hiring, interviewing, onboarding, HR tech stack optimization, and compliance.

---

## Context Discovery

### Auto-Investigation

| Signal | Check For | Why |
|--------|-----------|-----|
| `job-descriptions/` | JD templates, competency frameworks | Recruiting standards |
| `interview-guides/` | STAR questions, scorecards | Structured interviewing |
| `onboarding/` | 30-60-90 plans, checklists | Onboarding process |
| `employer-brand/` | EVP statement, careers page content | Branding efforts |
| HRIS/ATS config | Recruitment funnel metrics | Hiring analytics |

### Discovery Questions

```yaml
questions:
  - question: "What's your hiring stage?"
    options:
      - label: "Defining role/writing JD"
        description: "Use recruitment-funnel-optimization"
      - label: "Interviewing candidates"
        description: "Use structured-interview-design, star-interview-method"
      - label: "Onboarding new hire"
        description: "Use onboarding-30-day, onboarding-60-90-day"
      - label: "Building employer brand"
        description: "Use employee-value-proposition, employer-branding"

  - question: "What's your interview approach?"
    options:
      - label: "Structured/standardized"
        description: "Continue with structured-interview-design"
      - label: "Ad-hoc/inconsistent"
        description: "Implement structured-interview-design, scorecards"
      - label: "No process yet"
        description: "Start with star-interview-framework"

  - question: "How long is your onboarding?"
    options:
      - label: "Less than 30 days"
        description: "Extend to 30-60-90 day plan"
      - label: "30-90 days"
        description: "Use existing onboarding methodologies"
      - label: "No formal onboarding"
        description: "Create onboarding-30-day plan"
```

---

## Quick Reference

| If you need... | Use | File |
|----------------|-----|------|
| Optimize hiring funnel | recruitment-funnel-optimization | [recruiting-process.md](recruiting-process.md) |
| Write job description | Best practices from funnel optimization | [recruiting-process.md](recruiting-process.md) |
| Design interview process | structured-interview-design | [interview-methods.md](interview-methods.md) |
| Ask behavioral questions | star-interview-method | [star-interview-framework.md](star-interview-framework.md) |
| Create onboarding plan (days 1-30) | onboarding-30-day | [onboarding.md](onboarding.md) |
| Create onboarding plan (days 31-90) | onboarding-60-90-day | [onboarding.md](onboarding.md) |
| Define employer brand | employee-value-proposition | [employer-branding.md](employer-branding.md) |
| Analyze turnover | Exit/stay interviews + metrics | [retention-compliance.md](retention-compliance.md) |

### STAR Framework

| Component | Question |
|-----------|----------|
| **S**ituation | "Set the scene. What was the context?" |
| **T**ask | "What was your responsibility?" |
| **A**ction | "What did YOU specifically do?" |
| **R**esult | "What was the outcome? What did you learn?" |

### Onboarding Phases

| Phase | Focus | Key Activities |
|-------|-------|----------------|
| Days 1-30 | **LEARN** | Orientation, meet team, understand product, first small wins |
| Days 31-60 | **CONTRIBUTE** | Own small projects, build relationships, regular 1:1s |
| Days 61-90 | **IMPACT** | Lead initiatives, measurable results, 90-day review |

### Common Workflows

| Workflow | Steps |
|----------|-------|
| **New Hire** | recruitment-funnel-optimization → structured-interview-design → star-interview-method → onboarding-30-day → onboarding-60-90-day |
| **Improve Hiring** | recruitment-funnel-optimization → structured-interview-design → employee-value-proposition |

---

## Agents

| Agent | Purpose | Modes/Skills |
|-------|---------|--------------|
| faion-recruiter-agent | Full-cycle recruiting | sourcing, screening, interviewing |
| faion-onboarding-agent | Employee onboarding | 30-60-90 plans, orientation |
| faion-employer-brand-agent | Employer branding & EVP | content, careers page |

---

## References

Methodology documentation organized by domain:

| Reference | Content | Tokens |
|-----------|---------|--------|
| [recruiting-process.md](recruiting-process.md) | Talent acquisition, sourcing, offers | ~1400 |
| [interview-methods.md](interview-methods.md) | Structured interviews, STAR, scorecards | ~1100 |
| [onboarding.md](onboarding.md) | 30-60-90 plans, preboarding, buddy program | ~1200 |
| [employer-branding.md](employer-branding.md) | EVP, careers page, Glassdoor, testimonials | ~1000 |
| [retention-compliance.md](retention-compliance.md) | Stay interviews, DEI, hiring compliance | ~1000 |

---

## Workflows

### Workflow 1: Full-Cycle Recruiting

```
Job requisition → Job description → Sourcing → Screening → Interviews → Offer → Onboarding
```

**Reference:** [recruiting-process.md](recruiting-process.md)

### Workflow 2: Employer Branding

```
EVP audit → Employee research → Competitor analysis → EVP development → Content creation → Career page
```

**Reference:** [employer-branding.md](employer-branding.md)

### Workflow 3: Structured Hiring

```
Define competencies → Create scorecard → Design interview → Train interviewers → Execute → Debrief
```

**Reference:** [interview-methods.md](interview-methods.md)

### Workflow 4: Onboarding

```
Pre-boarding → Day 1 orientation → 30-day plan → 60-day check → 90-day review
```

**Reference:** [onboarding.md](onboarding.md)

---

## Core Methodologies

### recruitment-funnel-optimization

**Problem:** High candidate drop-off, long time-to-hire.

**Solution:** Analyze and optimize each funnel stage (awareness → application → screening → interview → offer → onboarding) using benchmarks.

**Reference:** [recruiting-process.md](recruiting-process.md)

**Agent:** faion-recruiter-agent

---

### star-interview-method

**Problem:** Vague, unhelpful interview answers.

**Solution:** Structured behavioral interviewing using Situation → Task → Action → Result framework with follow-up questions.

**Reference:** [star-interview-framework.md](star-interview-framework.md), [star-interview-examples.md](star-interview-examples.md)

**Agent:** faion-recruiter-agent

---

### onboarding-30-day

**Problem:** New hires flounder in first 30 days without direction.

**Solution:** Structured learning phase: Understand company, team, processes. Meet stakeholders, complete training.

**Reference:** [onboarding.md](onboarding.md)

**Agent:** faion-onboarding-agent

---

### onboarding-60-90-day

**Problem:** New hires need clear progression path days 31-90.

**Solution:** Days 31-60 (Contribute) → 61-90 (Execute independently). Small projects to full productivity.

**Reference:** [onboarding.md](onboarding.md)

**Agent:** faion-onboarding-agent

---

### employee-value-proposition

**Problem:** No clear reason for candidates to choose you.

**Solution:** Define EVP across compensation, benefits, career, culture, purpose. Create compelling EVP statement.

**Reference:** [employer-branding.md](employer-branding.md)

**Agent:** faion-employer-brand-agent

---

### structured-interview-design

**Problem:** Inconsistent, biased interviews.

**Solution:** Define 4-6 competencies, standardize questions, use scoring rubrics, conduct panel debriefs.

**Reference:** [interview-methods.md](interview-methods.md)

**Agent:** faion-recruiter-agent

---

## Extended Methodologies

Additional 40 methodologies organized by domain:

| Domain | Count | Reference |
|--------|-------|-----------|
| Talent Acquisition | 12 | [recruiting-process.md](recruiting-process.md) |
| Employer Branding | 8 | [employer-branding.md](employer-branding.md) |
| Interviewing & Selection | 10 | [interview-methods.md](interview-methods.md) |
| Onboarding | 8 | [onboarding.md](onboarding.md) |
| Retention & Compliance | 7 | [retention-compliance.md](retention-compliance.md) |

---

## Execution

### Full-Cycle Recruiting

```python
# Define hiring need
AskUserQuestion(
    questions=[
        {
            "question": "What type of role?",
            "options": [
                {"label": "Technical", "description": "Engineering, DevOps, Data"},
                {"label": "Non-technical", "description": "Sales, Marketing, Ops"},
                {"label": "Leadership", "description": "Manager, Director, VP"}
            ]
        },
        {
            "question": "Hiring urgency?",
            "options": [
                {"label": "Urgent", "description": "< 30 days"},
                {"label": "Normal", "description": "30-60 days"},
                {"label": "Pipeline", "description": "Future need"}
            ]
        }
    ]
)

# Generate job description
Task(subagent_type="faion-recruiter-agent",
     prompt=f"Write job description for {role} with skills: {skills}")

# Design interview process
Task(subagent_type="faion-recruiter-agent",
     prompt=f"Create structured interview plan with {num_rounds} rounds")
```

### Employer Branding

```python
Task(subagent_type="faion-employer-brand-agent",
     prompt=f"Audit current employer brand across {channels}")

Task(subagent_type="faion-employer-brand-agent",
     prompt=f"Develop EVP based on {employee_research}")

Task(subagent_type="faion-employer-brand-agent",
     prompt=f"Create careers page content for {company}")
```

### Onboarding

```python
Task(subagent_type="faion-onboarding-agent",
     prompt=f"Create 30-60-90 day plan for {role}")

Task(subagent_type="faion-onboarding-agent",
     prompt=f"Design onboarding checklist for {department}")
```

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| faion-communicator | Interview communication, stakeholder dialogue |
| faion-project-manager | Hiring project management |
| faion-marketing-manager | Employer brand content, careers page |

---

*Domain Skill v1.0 - HR Recruiter*
*45 Methodologies | 3 Agents*
*Based on: SHRM BASK, AIHR, Gartner HR research*
