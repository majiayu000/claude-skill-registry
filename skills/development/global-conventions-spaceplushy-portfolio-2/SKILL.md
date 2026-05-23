---
name: Global Conventions
description: Follow project structure standards, environment variable management, Content Collections setup, version control practices, and build/deployment conventions. Use this skill when setting up project structure, managing configuration files, organizing dependencies, or establishing development workflows. When working on project directory structure and organization, environment variable files (.env, .env.local, .env.production), Content Collections configuration (src/content/config.ts), package.json and dependency management, git commit messages and branching strategy, configuration files (astro.config.mjs, tsconfig.json), build and deployment setups, or documentation files (README.md, ADRs).
---

# Global Conventions

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle global conventions.

## When to use this skill

- When organizing project directory structure (src/, public/, components/, pages/, etc.)
- When managing environment variables (.env files, PUBLIC\_ prefix for client-exposed vars)
- When setting up Content Collections with Zod schemas in src/content/config.ts
- When writing git commit messages using conventional commits format (feat:, fix:, docs:)
- When managing dependencies in package.json and lock files
- When configuring Astro integrations or adapters in astro.config.mjs
- When establishing code review processes and pull request templates
- When setting up build modes (SSG, hybrid, SSR) and deployment strategies
- When creating project documentation (README.md, Architecture Decision Records)
- When implementing performance standards (Lighthouse scores, bundle size budgets)
- When organizing files by feature or colocation patterns

## Instructions

For details, refer to the information provided in this file:
[global conventions](../../../agent-os/standards/global/conventions.md)
