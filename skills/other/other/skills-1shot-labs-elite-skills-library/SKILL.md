---
name: elite-skills-library
description: Premium subscription-based skills library with 270+ professional-grade skills. Use when advanced domain expertise is needed. Skills are fetched from API based on user's subscription.
triggers:
  - "domain-driven design"
  - "microservices"
  - "system design"
  - "chaos engineering"
  - "functional programming"
  - "technical interview"
  - "any advanced software engineering topic"
---

# Elite Skills Library

This plugin provides access to the Elite Skills Library - a curated collection of 270+ professional-grade skills across multiple domains.

## How It Works

Skills are fetched dynamically from the Elite Skills API based on:
1. User's subscription status (Free or Professional)
2. Available monthly request quota
3. Specific skill requested by Claude

## Authentication

API key required. Configured via `/elite-skills:configure` command.

Stored in: `.claude/.elite-skills.local.md` (gitignored, project-scoped)

## Subscription Plans

- **Free:** 1 API key, 100 requests/month, access to all skills
- **Professional:** 5 API keys, unlimited requests, priority support

## API Integration

Skills are fetched from: `https://skills.1shotlabs.com/api/skills/{slug}`

Authentication: Bearer token in Authorization header

## Categories

The Elite Skills Library includes skills in:
- Software Architecture & System Design
- Cloud & Infrastructure
- Database & Data Engineering
- Security & DevOps
- AI/ML & Data Science
- Testing & Quality Assurance
- Programming Languages & Frameworks
- Business & Product
- And many more...

## Usage

Skills automatically load when Claude determines they're relevant. No manual invocation needed.

**Note:** This is a meta-skill that enables the plugin. Individual skills are fetched from the API based on context.
