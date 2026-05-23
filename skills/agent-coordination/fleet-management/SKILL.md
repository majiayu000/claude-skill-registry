---
name: letta-fleet-management
description: Manage Letta AI agent fleets declaratively with kubectl-style CLI. Use when creating, updating, or managing multiple Letta agents with shared configurations, memory blocks, tools, and folders.
license: MIT
---

# lettactl

kubectl-style CLI for managing Letta AI agent fleets declaratively.

## When to Use

- Deploying multiple agents with shared configurations
- Managing agent memory blocks, tools, and folders
- Applying templates to existing agents
- Programmatic fleet management via SDK

## Core Workflow

1. Define agents in `fleet.yaml`
2. Apply with `lettactl apply -f fleet.yaml`
3. Verify with `lettactl get agents` and `lettactl describe agent <name>`

## Fleet YAML Structure

```yaml
shared_blocks:
  - name: company-context
    description: Shared company knowledge
    limit: 5000
    from_file: ./context/company.md

agents:
  - name: support-agent
    description: Customer support assistant
    system_prompt:
      from_file: ./prompts/support.md
    llm_config:
      model: gpt-4o
      context_window: 128000
    memory_blocks:
      - name: persona
        description: Agent personality
        limit: 2000
        value: "You are a helpful support agent."
    shared_blocks:
      - company-context
    tools:
      - send_email
      - search_docs
```

See `reference/fleet-config.md` for full schema.

## CLI Commands

### Apply Configuration
```bash
lettactl apply -f fleet.yaml              # Create/update agents
lettactl apply -f fleet.yaml --dry-run    # Preview changes
lettactl apply -f fleet.yaml --match "*-draper"  # Template mode
```

### Inspect Resources
```bash
lettactl get agents                    # List all agents
lettactl get agents -o wide            # With details
lettactl get blocks --shared           # Shared blocks only
lettactl get tools --orphaned          # Unused tools
lettactl describe agent <name>         # Full agent details
```

### Messaging
```bash
lettactl send <agent> "Hello"          # Send message
lettactl send <agent> "Hi" --stream    # Stream response
lettactl messages list <agent>         # View history
lettactl messages reset <agent>        # Clear history
```

See `reference/cli-commands.md` for all options.

## Template Mode

Apply configuration to existing agents matching a pattern:

```bash
lettactl apply -f template.yaml --match "*-draper"
```

Uses three-way merge: preserves user-added resources while updating managed ones. See `reference/template-mode.md`.

## SDK Usage

```typescript
import { LettaCtl } from 'lettactl';

const ctl = new LettaCtl({ lettaBaseUrl: 'http://localhost:8283' });

await ctl.deployFromYaml('./fleet.yaml');
await ctl.deployFromYaml('./template.yaml', { match: '*-prod' });
```

See `reference/sdk-usage.md` for full API and `reference/cli-commands.md` for environment variables.
