# Real Case Example: GummySearch

Based on the public Before You Build case:
https://beforeyoubuild.fyi/en/cases/gummysearch

This example does not reproduce the full case. It turns the public case into a skill usage scenario.

## Prompt

```text
before you build: I want to build a Reddit-based audience research tool for founders. It will scan communities, summarize pain points, and surface startup ideas. Is this worth building?
```

## Public Case Background

The public GummySearch case is useful because it is not a simple "bad idea" example. The problem is real: founders and marketers want to understand communities and find demand signals.

The risk is more subtle. The product depends heavily on a third-party platform, data access, and the user's ability to turn research into a repeated workflow.

## What The Skill Should Notice

- The demand may be real, but the product could be exposed to Reddit API, policy, and data-access changes.
- Users may treat the tool as one-time research instead of a recurring product.
- The value is not just summarization; it is whether users make better decisions from the output.
- The target user should be narrowed: indie founders, agencies, marketers, product teams, or researchers have different budgets and workflows.
- Distribution may be harder than the build because many founder tools compete for the same audience.

## Good Output Shape

```markdown
## Quick Reality Check

What you want to build:
- A Reddit audience research tool that helps founders discover pain points and startup ideas.

Biggest risk:
- The idea depends on both platform access and repeated research behavior. Either one can break the business.

Most likely failure patterns:
- Platform dependency
- Research tool without workflow
- Founder-tool distribution crowding
- One-time use instead of recurring need

Validate before building:
1. Choose one buyer segment and one repeated job, such as agencies doing weekly niche research for clients.
2. Manually produce 5 research reports from Reddit communities and charge for them before building automation.
3. Ask users what decision they made from the report, not whether the report looked interesting.
4. Check what happens if Reddit data access becomes slower, more expensive, or less complete.

Recommendation:
Validate first
```

## Why This Example Helps

It shows that the skill should not always say "do not build." Sometimes the right answer is to validate the workflow, dependency, and repeated-use path before turning a real problem into software.
