---
name: orchardcore-ai-a2a-host
description: Skill for configuring the CrestApps A2A Host feature in Orchard Core. Covers exposing Agent AI Profiles as A2A agents, host authentication, agent cards, endpoints, and host settings.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core A2A Host - Prompt Templates

## Configure an A2A Host

You are an Orchard Core expert. Generate configuration and guidance for exposing Orchard Core Agent AI Profiles through the CrestApps A2A Host feature.

### Guidelines

- Use the A2A Host feature ID `CrestApps.OrchardCore.AI.A2A.Host`.
- The host exposes AI Profiles whose `Type` is `Agent`.
- Agent cards are served from `/.well-known/agent-card.json`.
- By default, the well-known endpoint returns a JSON array of agent cards, one per Agent AI Profile.
- Each card points to `/a2a?agent={agentName}` through its `url` property.
- When `ExposeAgentsAsSkill` is enabled, the host returns a single combined agent card and routes requests using the `agentName` metadata field.
- Keep agent `Description` accurate because it becomes part of the external agent or skill description.
- Prefer authenticated host access in shared or production environments.

### Feature Overview

| Feature | Feature ID | Description |
|---------|-----------|-------------|
| A2A Host | `CrestApps.OrchardCore.AI.A2A.Host` | Expose Agent AI Profiles via the Agent-to-Agent protocol |

### Enable the Host Feature

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "CrestApps.OrchardCore.AI",
        "CrestApps.OrchardCore.AI.A2A.Host"
      ],
      "disable": []
    }
  ]
}
```

### Prerequisite: Create Agent Profiles

Only AI Profiles of type `Agent` are exposed by the host.

```json
{
  "steps": [
    {
      "name": "AIProfile",
      "profiles": [
        {
          "Source": "OpenAI",
          "Name": "research-agent",
          "DisplayText": "Research Agent",
          "Description": "Researches topics and returns sourced summaries.",
          "Type": "Agent",
          "ChatDeploymentId": "research-chat-deployment",
          "UtilityDeploymentId": "research-utility-deployment",
          "Properties": {
            "AIProfileMetadata": {
              "SystemMessage": "You are a research assistant.",
              "Temperature": 0.2,
              "MaxTokens": 4096
            },
            "AgentMetadata": {
              "Availability": "OnDemand"
            }
          }
        }
      ]
    }
  ]
}
```

### Host Settings in Configuration

```json
{
  "OrchardCore": {
    "CrestApps_AI": {
      "A2AHost": {
        "AuthenticationType": "None",
        "ApiKey": "your-api-key-here",
        "RequireAccessPermission": false,
        "ExposeAgentsAsSkill": false
      }
    }
  }
}
```

### Agent Exposure Modes

#### Multi-Agent Mode (Default)

Use `ExposeAgentsAsSkill: false` when you want one agent card per Agent profile.

- `/.well-known/agent-card.json` returns a JSON array of cards.
- Each card advertises a single agent.
- Each card points clients to `/a2a?agent={agentName}`.

#### Skill Mode

Use `ExposeAgentsAsSkill: true` when you want a single combined agent card.

- The well-known endpoint returns one combined card.
- Each Agent AI Profile is represented as a skill.
- Requests are routed using the `agentName` metadata field.

### Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/.well-known/agent-card.json` | Agent discovery endpoint |
| `/a2a?agent={agentName}` | Sends messages to a specific exposed agent |

### Authentication Guidance

The host configuration supports authentication settings through `AuthenticationType` and related options in `OrchardCore:CrestApps_AI:A2AHost`.

Use these settings as your starting point:

- `AuthenticationType: "None"` for local development only.
- Set `ApiKey` when using API-key-based access.
- Use `RequireAccessPermission: true` when you want Orchard permission checks enforced for host access.

### Example Host Configuration for a Shared Environment

```json
{
  "OrchardCore": {
    "CrestApps_AI": {
      "A2AHost": {
        "AuthenticationType": "ApiKey",
        "ApiKey": "{{A2AHostApiKey}}",
        "RequireAccessPermission": true,
        "ExposeAgentsAsSkill": true
      }
    }
  }
}
```

### Best Practices

- Use Agent profiles, not Chat profiles, for A2A host exposure.
- Write strong profile descriptions so remote clients can pick the right agent.
- Keep `ExposeAgentsAsSkill` disabled when clients should select named agents directly.
- Enable `ExposeAgentsAsSkill` when clients prefer one consolidated card with multiple skills.
- Avoid `AuthenticationType: "None"` outside local development.
