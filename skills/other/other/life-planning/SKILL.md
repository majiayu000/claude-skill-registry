---
name: life-planning
description: Cross-repo life and project planning. Use when user wants to plan their week, prioritize projects, review progress across all areas, or make decisions about what to focus on. Triggers on "plan my week", "what should I work on", "prioritize", "weekly review", "life planning".
---

# Life Planning

Unified planning across personal life (my-vault), projects (ideas/), and learning.

## Data Sources

| Source | Location | Contains |
|--------|----------|----------|
| **About Taylor** | `.claude/memories/about-taylor.md` | Profile, context, current situation |
| **Journal** | `my-vault/02 Calendar/` | Daily activities, work, study |
| **Learning Plan** | `.claude/learning-sessions/learning-plan.json` | Study progress, queue, reviews due |
| **Projects** | `ideas/CLAUDE.md` | Project index with status |
| **Project Details** | `ideas/ideas/[project]/` | Briefs, specs, issues |
| **Memories** | `.claude/memories/` | Learned preferences and context |

## Workflows

| Command | Purpose |
|---------|---------|
| `/weekly-review` | Review past week, plan next week |
| `/whats-next` | Quick prioritization of what to work on |
| `/project-status` | Overview of all projects |

## Planning Principles

1. **Job search is priority** - Taylor is actively job hunting (since March 2025)
2. **Learning supports job search** - Jira DC on AWS for interview prep
3. **Side projects are secondary** - Unless they support job search (CareerBrain)
4. **Balance is important** - Personal life, health, social shouldn't be neglected

## Current Focus Areas

### Job Search (Primary)
- Interview prep (SAS went well 2026-01-11)
- AWS + Jira DC technical depth
- CareerBrain for tracking applications

### Learning (Supports Job Search)
- Queue: EFS, ASG, blue/green deployment, Secrets Manager rotation
- Spaced repetition reviews

### Side Projects (When Time Permits)
- Active: Coordinatr, ollama-agent-manager, leafspec, 49th-floor
- On hold: YourBench (until job secured)

## Integration Points

- `/good-morning` checks learning reviews due
- `/daily-review` covers all three journal sections
- Ideas repo has `/brief`, `/spec`, `/implement` for project work
- Learning system tracks study progress
