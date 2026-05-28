---
name: PromptWar̊e ØS Agent Skill Specification
description: Learn how to use SKILL by following this SKILL specification.
---

# The SKILL.md Specification for PromptWar̊e ØS

PromptWar̊e ØS Agent Skills are based on the Anthropic Claude Agent Skills Spec, with below modifications and enhancements:

1. all `scripts`/`tools` MUST written in TypeScript with Deno as runtime. No exceptions. 
2. all `scripts`/`tools` MUST support standand CLI `--help` command and output the detailed usage description.
3. all `scripts`/`tools` will be executed with a remote-first way, no download needed. (use `deno https://url` to execute it directly)

## References

**UnDoc** is our ultimate documentation source of the truth.

- Learn full anthropic claude agent skills specification at <https://shipfail.github.io/undoc/un/claude-agent-skills-spec.md>
