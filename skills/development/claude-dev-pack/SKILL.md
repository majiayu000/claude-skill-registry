---
name: claude-dev-pack
description: "Developer toolkit: build, test, deploy, and debug with curated skills."
version: 0.1.0
skillset: true
dependencies:
  # Official: https://github.com/anthropics/skills
  - anthropics/skills/skills/webapp-testing
  - anthropics/skills/skills/web-artifacts-builder
  - anthropics/skills/skills/mcp-builder

  # Vercel engineering: https://github.com/vercel-labs/agent-skills
  - https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices
  - https://github.com/vercel-labs/agent-skills/tree/main/skills/claude.ai/vercel-deploy-claimable

  # Community (from awesome-claude-skills): https://github.com/VoltAgent/awesome-claude-skills
  - lackeyjb/playwright-skill/skills/playwright-skill
  - jthack/ffuf_claude_skill/ffuf-skill
  - zxkane/aws-skills/plugins/aws-cdk/skills/aws-cdk-development
  - scarletkc/vexor/plugins/vexor/skills/vexor-cli
  - https://github.com/sanjay3290/ai-skills/tree/main/skills/postgres
---

# claude-dev-pack

Install:

```bash
skild install ./skillsets/claude-dev-pack
```
