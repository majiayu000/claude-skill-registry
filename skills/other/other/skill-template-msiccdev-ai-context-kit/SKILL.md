---
name: "example-skill"
description: "Briefly describe what this skill does and when it should be used."
license: "Optional license identifier"
compatibility: "Optional environment/runtime requirements."
metadata:
  owner: "Optional owner"
  domain: "Optional domain"
# allowed-tools: [] # Optional and experimental. Keep disabled by default.
---

# Example Skill

## Purpose
Describe the capability this skill provides and the problem it solves.

## When To Use
- Use this skill when the task matches this domain.
- Do not use this skill for unrelated tasks.

## Required Inputs
- List required information the assistant needs before applying this skill.

## Workflow
1. Confirm the task fits the skill scope.
2. Gather only the inputs required for this workflow.
3. Execute steps in order and verify outputs.

## Output Expectations
- Define the expected output format and quality criteria.
- Include any acceptance checks.

## Resources
- `references/` for detailed docs loaded on demand.
- `scripts/` for optional automation or checks.
- `assets/` for reusable static artifacts.

## Constraints And Safety
- Keep instructions concise in this file; move large material to `references/`.
- Use relative paths for all skill-local references.
- Mention risky operations explicitly and require confirmation before running them.

## Frontmatter Rules
- `name` (required):
- 1-64 characters.
- Lowercase letters, numbers, and hyphens only.
- No leading/trailing hyphen.
- No consecutive hyphens.
- Must match the parent skill directory name.
- `description` (required):
- 1-1024 characters.
- Must state what the skill does and when to use it.
- `license` (optional): short license identifier.
- `compatibility` (optional):
- 1-500 characters.
- Use only for real environment constraints.
- `metadata` (optional): map of string keys to string values.
- `allowed-tools` (optional/experimental):
- Parseable if present.
- Keep disabled by default unless explicitly enabled by policy.
