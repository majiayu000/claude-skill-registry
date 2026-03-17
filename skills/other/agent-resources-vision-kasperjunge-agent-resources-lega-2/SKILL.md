---
name: agent-resources-vision
description: "North star guidance for the agent-resources project. Use this skill to understand project context, get inspiration for development decisions, and resolve uncertainty about feature priorities or design choices. Reference when asking 'why does this project exist?' or 'what should we optimize for?'"
---

# Agent Resources - Project Vision

This document defines the ideal outcomes we're building toward. Use it to guide development decisions and maintain alignment with the project's purpose.

## For Individual Users

**Build Your Personal Agent Toolkit**
- Curate a personal collection of your best skills, commands, and agents in your own GitHub repo
- Your toolkit travels with you across machines, projects, and jobs
- Iterate and refine your resources over time as you discover what works
- Version control your AI workflow improvements

**Instant Capability Extension**
- Add new capabilities to Claude Code with a single command
- No manual downloading, copying, or configuration
- Zero installation friction via `uvx` - just run and go
- Works immediately without restarting or setup steps

**Leverage Community Knowledge**
- Access a growing ecosystem of resources built by others
- Skip the learning curve by using battle-tested configurations
- Find domain-specific setups (security, data science, DevOps, etc.)
- Learn from how others structure effective prompts and workflows

---

## For the Community

**Frictionless Sharing**
- Share resources as easily as sharing a link: "try `uvx skill-add yourname/cool-skill`"
- Drop recommendations in Slack, Discord, Twitter, or READMEs
- No publishing step, no registry approval - push to GitHub and it's available

**Social Discovery**
- GitHub username IS your namespace - identity-linked sharing
- Follow interesting developers to see what resources they create
- Star and fork repos to track and remix useful collections
- The existing GitHub social graph becomes the discovery mechanism

**Network Effects**
- The more people share, the more valuable the ecosystem becomes
- Popular resources get visibility through GitHub's existing mechanisms
- Specialization emerges - people become known for specific domains
- Remixing and building on others' work accelerates innovation

**Low Barrier to Contribution**
- Anyone with a GitHub account can be a creator
- No infrastructure to maintain - GitHub handles hosting and distribution
- Start by sharing one useful skill; grow from there
- Democratizes access to high-quality AI workflows

---

## The Big Picture

**From Tool to Platform**
- Transforms Claude Code from a personal tool into a community-extensible platform
- Creates a marketplace effect without the marketplace overhead
- Enables specialization and division of labor in AI workflow development

**Multiplied Productivity**
- Individual improvements benefit everyone who uses them
- Standing on the shoulders of the community's collective experimentation
- Time invested in creating good resources pays dividends across the ecosystem

**Dotfiles for the AI Era**
- Like dotfiles repos, but for AI agent configurations
- Personal, shareable, forkable, remixable
- A new primitive for how developers customize and share their AI-augmented workflows

---

## The Growth Flywheel

```
                    ┌─────────────────────┐
                    │   USER TRIES A      │
                    │   RESOURCE          │
                    │   uvx add-skill ... │
                    └──────────┬──────────┘
                               │
                               ▼
         ┌─────────────────────────────────────────┐
         │                                         │
         │         EXPERIENCES VALUE               │
         │         "This actually helps me"        │
         │                                         │
         └──────────┬─────────────────────┬────────┘
                    │                     │
        ┌───────────▼───────────┐   ┌─────▼─────────────┐
        │                       │   │                   │
        │   SHARES WITH OTHERS  │   │  BECOMES CREATOR  │
        │   "Try uvx add-skill  │   │  "I could make    │
        │    username/skill"    │   │   one of these"   │
        │                       │   │                   │
        └───────────┬───────────┘   └─────┬─────────────┘
                    │                     │
                    │                     ▼
                    │         ┌───────────────────────┐
                    │         │  CREATES & PUBLISHES  │
                    │         │  uvx create-agent-    │
                    │         │  resources-repo       │
                    │         │  --github             │
                    │         └───────────┬───────────┘
                    │                     │
                    │                     │ shares their creation
                    │                     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   MORE PEOPLE       │
                    │   DISCOVER          │◄───── loop continues
                    └─────────────────────┘
```

### What Makes It Spin

**Zero-Friction Entry Points**
- **Try**: `uvx add-skill username/skill` — no install, no signup, no docs
- **Create**: `uvx create-agent-resources-repo --github` — repo live in 30 seconds
- **Share**: One sentence contains complete onboarding

**Every User Is a Distribution Channel**
- Sharing a resource = sharing the ecosystem
- "Try `uvx add-skill me/cool-skill`" teaches the pattern
- No learning curve for recipients

**Creators Have Skin in the Game**
- Creators want their resources used → they evangelize
- Every creator brings their network
- Pride of authorship drives quality

**Compounding Value**
- More resources → higher chance someone finds what they need
- More diverse creators → more use cases covered
- Community quality rises as patterns emerge

### Acceleration Levers

| Lever | Effect |
|-------|--------|
| **Featured resources** | Curated list shows what's possible |
| **Social proof** | "X people installed this" |
| **Creator spotlights** | Recognition motivates contribution |
| **Templates** | Lower barrier to high-quality resources |
| **Discoverability** | Community index makes finding easy |

### The Virtuous Cycle

```
More Resources → More Value → More Users → More Sharing → More Creators → More Resources
```

**Critical insight**: The one-liner install command is both the product AND the marketing. Every share teaches the pattern while delivering value.

---

## Decision-Making Guide

When uncertain about a feature or design choice, ask:

1. **Does it reduce friction?** - Fewer steps to share/install = better
2. **Does it leverage existing infrastructure?** - GitHub-native > custom registry
3. **Does it enable the social layer?** - Personal identity + sharing = network effects
4. **Does it serve both user segments?** - Individual AND community value
5. **Is it simple enough to just work?** - `uvx` one-liner is the gold standard
