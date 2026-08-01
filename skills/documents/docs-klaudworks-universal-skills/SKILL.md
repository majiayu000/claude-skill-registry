---
name: docs-klaudworks-universal-skills
description: A short, actionable guide to how I use skills.
---

A short, actionable guide to how I use skills.

High-level:

1. Work on a problem.
2. Recognize grunt work.
3. Load the Skill Creator meta-skill to create a new skill.
4. Write a skill to (semi-)automate your problem.
5. Profit.

Example: Publishing an npm package

I’ll walk you through the process I used to create the simple npm publisher skill in [.agent/skills/npm-publisher/SKILL.md](../.agent/skills/npm-publisher/SKILL.md).

### Prerequisites

Install Anthropic’s Skill Creator skill. It’s a skill that helps you create new skills.

```bash
npx universal-skills install --repo https://github.com/anthropics/skills --repo-dir skill-creator/ --local-dir ~/.agent/skills
```

I recommend installing the skill-creator skill into `~/.agent/skills`. If you also want to work with Claude Code’s native skills feature, store the skill in `~/.claude/skills`.

### Identify a problem and solve it once

I don’t usually publish npm packages. However, TypeScript provides the best MCP implementation, so I chose it for this project. To publish my first npm package, I prompted my coding agent and provided it with external docs. After completing this task the first time, my agent’s session contained all the knowledge needed to publish npm packages. A few examples of knowledge I want my agent to have when I repeat the process:

- The overall steps involved to publish an npm package.
- The agent should not actually publish the package; that’s done by a GitHub workflow.
- The agent should run npm version patch/minor/major to bump the version.
- The agent should not add annoying attributions for my AI agent to my commit messages.

### Profit

From now on, I can use the npm-publisher skill. Its metadata is automatically loaded into my context. Unlike MCP servers, a skill usually takes fewer than 100 tokens, which is negligible compared to the GitHub MCP server using ~10k tokens.

---

```yaml
---
name: npm-publisher
description: >
  Use this skill when the user wants to publish, release, or deploy an npm package.
  It handles the complete release workflow, including staging changes, committing,
  version bumping, tagging, and pushing to trigger automated CI/CD publishing.
---
```

Whenever I write something like:

- “Publish the npm package”
- “Release a new version”
- “Deploy to npm”
- “Create a new release”
- “Bump the version and publish”

The agent can infer, based on the description in its context, that it should load the entire skill. At this point, my session contains all the knowledge needed to publish an npm package.

### Evolve the skill

1. Manually review the first draft of the skill and fix it where necessary.
2. Mostly, I just use it. When I want to improve the skill, I tell the agent what to do differently and ask it to update .agent/skills/SKILL.md with that knowledge. This way, I only have to intervene once to improve the automation.
