---
name: policyengine-github-agent-skill
description: Guidance for working with the PolicyEngine GitHub agent bot
---

# PolicyEngine GitHub Agent Skill

## For Users 👥

The PolicyEngine GitHub agent is an automated bot that can be invoked on GitHub issues and pull requests using `@policyengine` mentions. It helps with code reviews, bug fixes, and implementing features across PolicyEngine repositories.

## For Contributors 💻

### Critical: Avoiding Doom Loops

**NEVER use '@policyengine' or '@policyengine-auto' in bot responses.** These mentions trigger the bot and create infinite loops where the bot repeatedly responds to itself.

#### Why This Matters

When the bot posts a comment containing `@policyengine`, GitHub notifies the bot account, which triggers another invocation. This creates a chain reaction of bot responses that can generate dozens or hundreds of comments before being stopped. See [PR #22](https://github.com/PolicyEngine/policyengine-github-agent/pull/22) for a real example of this issue.

#### Safe Alternatives

Instead of mentioning the bot directly:

❌ **Don't do this:**
- "Thanks @policyengine for the suggestion!"
- "I've addressed @policyengine's feedback"
- "cc @policyengine-auto"

✅ **Do this instead:**
- "I've implemented the suggested changes"
- "The feedback has been addressed"
- "Updated based on the review comments"
- Simply refer to "the bot" or "the agent" without the @ mention

### Bot Invocation

The bot can only be invoked by members of the [PolicyEngine/core-developers](https://github.com/orgs/PolicyEngine/teams/core-developers) team. Non-members will receive a permission error.

### Response Style

When the bot responds to issues or PRs:
- Keep responses concise and actionable
- Focus on the technical task at hand
- Avoid unnecessary pleasantries or acknowledgments
- Never include @ mentions of the bot usernames

## Resources

- [policyengine-github-agent repository](https://github.com/PolicyEngine/policyengine-github-agent)
- [PR #22: Stop doom loops](https://github.com/PolicyEngine/policyengine-github-agent/pull/22)
