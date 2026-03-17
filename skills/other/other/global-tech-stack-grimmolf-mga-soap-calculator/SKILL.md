---
name: Global Tech Stack
description: Maintain approved technology stack including TypeScript/Python languages, React/Tailwind frontend, Node.js/FastAPI backend, PostgreSQL/Redis persistence, and Ansible infrastructure automation with enforced quality gates. Use this skill when selecting technologies, adding dependencies, configuring tooling, or ensuring infrastructure-as-code practices. Applies to package.json, requirements.txt, CI/CD pipelines, Ansible playbooks, linters, formatters, testing frameworks, and all technology choices requiring documented approval and migration strategies.
---

# Global Tech Stack

## When to use this skill

- When choosing programming languages (TypeScript for Node/Frontend, Python for automation/data tooling)
- When selecting frontend frameworks or libraries (React, Next.js, Tailwind CSS, component libraries)
- When setting up backend frameworks (Node.js with NestJS/Express, Python with FastAPI)
- When choosing databases or persistence layers (PostgreSQL, Redis, S3-compatible storage)
- When configuring testing tools (Jest, Vitest, pytest) and code coverage thresholds
- When setting up quality gates (ESLint, Prettier, Ruff, Black) that run in CI and locally
- When creating or modifying infrastructure code in Ansible playbooks under `infra/ansible/`
- When defining CI/CD workflows in GitHub Actions or similar pipeline configurations
- When adding observability with OpenTelemetry, Prometheus/Grafana, or Sentry error tracking
- When managing secrets through 1Password Connect, AWS SSM Parameter Store, or environment-specific stores
- When documenting technology decisions in ADRs or `tech-stack.md` with upgrade strategies
- When evaluating new libraries or tools that require written approval and migration plans
- When ensuring all infrastructure changes flow through Ansible instead of manual SSH commands

# Global Tech Stack

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle global tech stack.

## Instructions

For details, refer to the information provided in this file:
[global tech stack](../../../agent-os/standards/global/tech-stack.md)
