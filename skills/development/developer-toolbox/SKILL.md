---
name: developer-toolbox
description: |
  Essential development workflow agents for code review, debugging, testing, documentation, and git operations.
  Includes 7 specialized agents with strong auto-discovery triggers.

  Use when: setting up development workflows, code reviews, debugging errors, writing tests,
  generating documentation, creating commits, or verifying builds.
license: MIT
metadata:
  version: "1.0.0"
  last_verified: "2025-01-20"
  author: "Jezweb"
---

# Developer Toolbox

A collection of essential development workflow agents that integrate seamlessly with Claude Code.

## What's Included

### Agents (7)

| Agent | Purpose | Triggers On |
|-------|---------|-------------|
| **commit-helper** | Generate conventional commit messages | "commit message", "staged changes" |
| **build-verifier** | Verify dist/ matches source after builds | "changes not appearing", "verify build" |
| **code-reviewer** | Security audits and code quality reviews | "code review", "security audit", "OWASP" |
| **debugger** | Systematic debugging with root cause analysis | "error", "TypeError", "stack trace", "bug" |
| **test-runner** | TDD workflow and test creation | "write tests", "TDD", "coverage", "jest" |
| **orchestrator** | Coordinate complex multi-step projects | "coordinate", "multi-step", "complex feature" |
| **documentation-expert** | README, API docs, architecture diagrams | "document", "README", "API docs" |

### Rules (1)

| Rule | Purpose |
|------|---------|
| **agent-first-thinking** | Behavioral interrupt - consider agents before manual work |

## Installation

```bash
# Via marketplace
/plugin install developer-toolbox

# Or local development
/plugin install ./skills/developer-toolbox
```

After installation, restart Claude Code to load the agents.

## Usage Examples

### Commit Helper
```
"Help me write a commit message for these staged changes"
```

### Build Verifier
```
"My changes aren't appearing in production, verify the build output"
```

### Code Reviewer
```
"Review this authentication code for security vulnerabilities"
```

### Debugger
```
"I'm getting TypeError: Cannot read property 'map' of undefined"
```

### Test Runner
```
"Use TDD to implement this user validation function"
```

### Orchestrator
```
"Coordinate a refactor of the authentication system across 5 services"
```

### Documentation Expert
```
"Create comprehensive API documentation for this REST endpoint"
```

## Agent Design Philosophy

All agents follow the **"MUST BE USED when"** pattern for reliable auto-discovery:

```yaml
description: |
  [Role] specialist. MUST BE USED when: [trigger 1], [trigger 2], [trigger 3].
  Use PROACTIVELY for [broad task category].

  Keywords: keyword1, keyword2, error-message-fragment
```

This ensures Claude Code discovers and proposes the right agent automatically based on user requests.

## Agent-First Thinking Rule

The included `agent-first-thinking.md` rule encourages using agents by default:

**The Inversion:**
- Wrong: "I'll do this manually unless it's big enough for agents"
- Right: "I'll use agents unless there's a reason not to"

**Triggers:**
| If about to... | Use instead... |
|----------------|----------------|
| grep/glob 3+ times | Explore agent |
| Read 5+ files | Explore agent |
| Same edit across files | Parallel agents |
| Audit multiple items | Parallel swarm |

## Customization

Each agent can be extended by editing its markdown file after installation:

```bash
# Find installed agents
ls ~/.claude/plugins/cache/*/developer-toolbox/*/agents/

# Or copy to user-level for customization
cp [plugin-path]/agents/code-reviewer.md ~/.claude/agents/
```

## Combining Agents

Agents work well together:

```
"Review this code for security issues, then write tests for the critical paths"
# → code-reviewer first, then test-runner
```

```
"Debug this failing test, document the root cause, and commit the fix"
# → debugger → documentation-expert → commit-helper
```

## Version History

- **1.0.0** (2025-01-20): Initial release with 7 agents and 1 rule
