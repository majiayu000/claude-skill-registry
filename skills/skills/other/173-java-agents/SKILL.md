---
name: 173-java-agents
description: Use when you need to generate an AGENTS.md file for a Java repository — covering project conventions, tech stack, file structure, commands, Git workflow, and contributor boundaries — through a modular, step-based interactive process that adapts to your specific project needs. Part of the skills-for-java project
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# AGENTS.md Generator for Java repositories

Generate a comprehensive AGENTS.md file for Java repositories through a modular, step-based interactive process that covers role definition, tech stack, file structure, commands, Git workflow, and contributor boundaries.

**Core areas:** AGENTS.md generation for Java repositories of any complexity, role and expertise definition for AI agents and contributors, tech stack documentation (language, build tool, frameworks, pipelines), file structure mapping with read/write boundaries, command catalogue for build/test/deploy/run workflows, Git workflow conventions (branching strategy, commit message format), and contributor boundaries using ✅ Always do / ⚠️ Ask first / 🚫 Never do formatting.

**Prerequisites:** No Maven validation is required before generating AGENTS.md. However, review the project structure and existing documentation before starting to provide accurate answers during Step 1.

**Multi-step scope:** Step 1 assesses project requirements through 6 targeted questions covering role/expertise, tech stack, directory layout, key commands, Git workflow, and contributor boundaries — all questions must be answered in strict order before proceeding. Step 2 generates the AGENTS.md file in the project root by mapping each answer to the corresponding section, handles existing files via overwrite/merge/backup strategies, validates that all 6 sections are present and correctly formatted, and confirms that boundaries use the required ✅ / ⚠️ / 🚫 icons.

**Before applying changes:** Read the reference for detailed good/bad examples, constraints, and safeguards for each AGENTS.md generation pattern.

## Reference

For detailed guidance, examples, and constraints, see [references/173-java-agents.md](references/173-java-agents.md).
