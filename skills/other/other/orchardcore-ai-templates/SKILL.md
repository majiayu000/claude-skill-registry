---
name: orchardcore-ai-templates
description: Skill for creating and managing AI Templates in Orchard Core. Covers template creation via admin UI, markdown files, recipes, deployment steps, template sources (SystemMessage, Profile), and applying templates when creating AI Profiles.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core AI Templates

## Overview

AI Templates are reusable configurations that can serve as profile templates or system message templates. They can include system messages, model parameters, connection settings, tools, agents, data sources, documents, and more.

### Template Sources

| Source | Description |
|--------|-------------|
| `Profile` | Pre-fills AI Profile settings when creating new profiles. Users can select from a dropdown and click "Apply". |
| `SystemMessage` | Provides reusable system message prompts that can be rendered using the `render_ai_template` Liquid tag. |

Templates can be defined in two ways:
1. **Admin UI (runtime)** — stored in the database, full CRUD support
2. **Markdown files (code)** — placed in `AITemplates/Profiles/` or `AITemplates/SystemMessages/` folders within modules, read-only at runtime

### Guidelines

- AI Templates extend `CatalogItem` and use the `INamedCatalogManager<AIProfileTemplate>` pattern.
- Templates are source-independent — the same template works with any AI provider.
- Database templates take precedence over file-based templates with the same name.
- Template properties are stored using `Entity.As<T>()/Put<T>()` (not `GetSettings/AlterSettings`).
- Profile-type templates: when applied, `Properties` are copied to both `profile.Properties` and `profile.Settings`.
- SystemMessage templates: rendered at runtime using `render_ai_template` Liquid tag.
- Profile types supported: `Chat`, `Utility`, `TemplatePrompt`, `Agent`.
- Agent templates must include `Description` and `AgentMetadata` with availability setting.

### Enabling AI Templates

The AI Templates feature is included with the core AI module:

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "CrestApps.OrchardCore.AI"
      ]
    }
  ]
}
```

## Creating Templates via Markdown Files

### Profile Templates

Place `.md` files in your module's `AITemplates/Profiles/` directory. The file name (without extension) becomes the template's technical name.

### SystemMessage Templates

Place `.md` files in your module's `AITemplates/SystemMessages/` directory. These are rendered using the `render_ai_template` Liquid tag.

### Markdown Template Format (Profile Source)

```markdown
---
Title: Customer Support Bot
Description: Template for customer support chatbots
Category: Customer Service
IsListable: true
ProfileType: Chat
ConnectionName: openai-main
OrchestratorName: default
WelcomeMessage: Hello! How can I help you today?
TitleType: Generated
Temperature: 0.7
TopP: 0.9
FrequencyPenalty: 0.0
PresencePenalty: 0.0
MaxOutputTokens: 800
PastMessagesCount: 10
ToolNames: web-search, knowledge-base
AgentNames: research-agent
---

You are a professional customer support agent.
Your goal is to help customers resolve issues efficiently.
Always be polite and empathetic.
```

The body after the front matter becomes the `SystemMessage`.

### Markdown Template Format (SystemMessage Source)

```markdown
---
Title: Agent Availability Info
Description: Provides the LLM with information about available agents
Category: System
IsListable: false
---

The following agents are available to assist you:
{% for agent in tools %}
{% if agent.Source == "Agent" %}
- **{{ agent.Name }}**: {{ agent.Description }}
{% endif %}
{% endfor %}
```

### Front Matter Properties

| Property | Type | Description |
|----------|------|-------------|
| `Title` | string | Display name for the template |
| `Description` | string | Description of what the template does |
| `Category` | string | Grouping category for the dropdown |
| `IsListable` | bool | Whether the template appears in the selection dropdown |
| `ProfileType` | string | `Chat`, `Utility`, `TemplatePrompt`, or `Agent` |
| `ConnectionName` | string | AI provider connection name (optional) |
| `OrchestratorName` | string | Orchestrator name (default: `default`) |
| `WelcomeMessage` | string | Initial greeting shown to users (Chat profiles only) |
| `TitleType` | string | `InitialPrompt` or `Generated` |
| `PromptTemplate` | string | Liquid template for TemplatePrompt profiles |
| `PromptSubject` | string | Subject for the prompt |
| `Temperature` | float | Controls randomness (0.0 to 2.0) |
| `TopP` | float | Nucleus sampling threshold |
| `FrequencyPenalty` | float | Reduces frequent token repetition |
| `PresencePenalty` | float | Encourages topic diversity |
| `MaxOutputTokens` | int | Maximum tokens in response |
| `PastMessagesCount` | int | Number of history messages to include |
| `ToolNames` | string | Comma-separated list of AI tool names |
| `AgentNames` | string | Comma-separated list of agent profile names |

### Using render_ai_template Liquid Tag

The `render_ai_template` tag renders a SystemMessage template by ID, optionally passing variables:

```liquid
{% render_ai_template "template-id" %}
```

With variables:

```liquid
{% render_ai_template "agent-availability" tools %}
```

This passes the `tools` variable from the current scope to the rendered template. Variables are inherited from the parent scope.

### Example: Composing Templates

```liquid
You are an AI assistant with access to various tools and agents.

{% if hasAgents %}
{% render_ai_template "agent-availability" tools %}
{% endif %}

Always follow the user's instructions carefully.
```

## Creating Agent Templates

Agent templates help users quickly create agent profiles:

```json
{
  "steps": [
    {
      "name": "AIProfileTemplate",
      "Templates": [
        {
          "Name": "research-agent",
          "DisplayText": "Research Agent",
          "Description": "Template for creating a research agent that can gather and summarize information.",
          "Category": "Agents",
          "IsListable": true,
          "ProfileType": "Agent",
          "SystemMessage": "You are a research assistant. Gather information from available tools, verify facts, and provide comprehensive answers with sources.",
          "Temperature": 0.3,
          "MaxOutputTokens": 4096,
          "ToolNames": ["web-search"],
          "AgentNames": [],
          "Properties": {
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

## Creating Templates via Recipes

### Profile Template Recipe

```json
{
  "steps": [
    {
      "name": "AIProfileTemplate",
      "Templates": [
        {
          "Name": "customer-support",
          "DisplayText": "Customer Support Bot",
          "Description": "Template for customer support chatbots",
          "Category": "Customer Service",
          "IsListable": true,
          "ProfileType": "Chat",
          "ConnectionName": "",
          "OrchestratorName": "default",
          "SystemMessage": "You are a professional customer support agent.",
          "WelcomeMessage": "Hello! How can I help you today?",
          "TitleType": "Generated",
          "Temperature": 0.7,
          "TopP": 0.9,
          "MaxOutputTokens": 800,
          "PastMessagesCount": 10,
          "ToolNames": ["web-search", "knowledge-base"],
          "AgentNames": ["research-agent"],
          "Properties": {}
        }
      ]
    }
  ]
}
```

### Recipe with Post-Session, Data Extraction & Conversion Goals

Templates store all settings in `Properties` (not `Settings`). Here is a full recipe with post-session tasks, data extraction entries, and conversion goals:

```json
{
  "steps": [
    {
      "name": "AIProfileTemplate",
      "Templates": [
        {
          "Name": "support-analytics",
          "DisplayText": "Support with Analytics",
          "Description": "Support template with full data processing and metrics.",
          "Category": "Customer Service",
          "ProfileType": "Chat",
          "SystemMessage": "You are a customer support agent.",
          "AgentNames": [],
          "Properties": {
            "AIProfilePostSessionSettings": {
              "EnablePostSessionProcessing": true,
              "ToolNames": [],
              "PostSessionTasks": [
                {
                  "Name": "sentiment",
                  "Type": "PredefinedOptions",
                  "Instructions": "Classify the overall sentiment of the conversation.",
                  "AllowMultipleValues": false,
                  "Options": [
                    { "Value": "positive", "Description": "Customer was happy." },
                    { "Value": "neutral", "Description": "No strong emotion." },
                    { "Value": "negative", "Description": "Customer was frustrated." }
                  ]
                },
                {
                  "Name": "summary",
                  "Type": "Semantic",
                  "Instructions": "Write a concise summary of the conversation.",
                  "AllowMultipleValues": false,
                  "Options": []
                }
              ]
            },
            "AIProfileDataExtractionSettings": {
              "EnableDataExtraction": true,
              "ExtractionCheckInterval": 1,
              "SessionInactivityTimeoutInMinutes": 30,
              "DataExtractionEntries": [
                {
                  "Name": "customer_name",
                  "Description": "The customer's full name.",
                  "AllowMultipleValues": false,
                  "IsUpdatable": true
                },
                {
                  "Name": "issue_category",
                  "Description": "The category of the issue.",
                  "AllowMultipleValues": false,
                  "IsUpdatable": true
                }
              ]
            },
            "AnalyticsMetadata": {
              "EnableSessionMetrics": true,
              "EnableAIResolutionDetection": true,
              "EnableConversionMetrics": true,
              "ConversionGoals": [
                {
                  "Name": "issue_resolved",
                  "Description": "The customer's issue was fully resolved.",
                  "MinScore": 0,
                  "MaxScore": 10
                },
                {
                  "Name": "customer_satisfaction",
                  "Description": "The customer expressed satisfaction.",
                  "MinScore": 0,
                  "MaxScore": 10
                }
              ]
            }
          }
        }
      ]
    }
  ]
}
```

### Named Entry Merge Behavior

When re-importing templates via recipe, named entries (PostSessionTasks, DataExtractionEntries, ConversionGoals) are merged by their `Name` field:

| Scenario | Result |
|----------|--------|
| Entry with same name exists | Updated with incoming values |
| Entry is new (name not found) | Added to the list |
| Existing entry not in import | Preserved (not deleted) |

Entry names must be unique within each list and contain only alphanumeric characters and underscores.

## Exporting Templates via Deployment

AI Templates can be exported using the deployment plan system. The deployment step `AIProfileTemplate` exports all or specific templates.

## Creating a Display Driver for AIProfileTemplate

To extend the template editor with custom tabs (like documents, capabilities, etc.), create a `DisplayDriver<AIProfileTemplate>`:

```csharp
public sealed class MyCustomTemplateDriver : DisplayDriver<AIProfileTemplate>
{
    public override IDisplayResult Edit(AIProfileTemplate template, BuildEditorContext context)
    {
        return Initialize<MyViewModel>("MyShape_Edit", model =>
        {
            var metadata = template.As<MyMetadata>();
            model.SomeSetting = metadata?.SomeSetting;
        }).Location("Content:10#MyTab;8");
    }

    public override async Task<IDisplayResult> UpdateAsync(
        AIProfileTemplate template,
        UpdateEditorContext context)
    {
        var model = new MyViewModel();

        await context.Updater.TryUpdateModelAsync(model, Prefix);

        template.Put(new MyMetadata
        {
            SomeSetting = model.SomeSetting,
        });

        return await EditAsync(template, context);
    }
}
```

Register the driver in Startup:

```csharp
services.AddDisplayDriver<AIProfileTemplate, MyCustomTemplateDriver>();
```

### Placement Format Reference

When specifying `.Location()` for display drivers, use the format:

```
Zone:ItemPosition#TabName;TabGroupPosition
```

- `:N` after zone = item order WITHIN the tab (lower number = first)
- `;N` after tab name = tab order among other tabs (lower number = first)
- **CRITICAL**: Use `;` (semicolon) after tab name, NOT `:` (colon). Using `:` makes the number part of the tab name.

Examples:
- `Content:3#Capabilities;8` — item at position 3 within the "Capabilities" tab, tab at position 8
- `Content:5#Data Processing & Metrics;10` — item at position 5 within the "Data Processing & Metrics" tab, tab at position 10

### Important Notes

- Template drivers use `template.As<T>()/Put<T>()` from `OrchardCore.Entities` (not `GetSettings/AlterSettings`).
- Template drivers can reuse the same ViewModels and shape names as AI Profile drivers.
- When applying a template, `Properties` are copied to both `profile.Properties` and `profile.Settings`.
- Templates support document uploads — documents are cloned when applying a template to a new profile.
- All template settings (post-session, data extraction, analytics) live in `template.Properties`.

### Where Template Settings Live vs AI Profile Settings

| Settings Type | On AIProfileTemplate | On AIProfile |
|---|---|---|
| `AIProfilePostSessionSettings` | `template.Properties` via `As<T>()/Put<T>()` | `profile.Settings` via `GetSettings/AlterSettings` |
| `AIProfileDataExtractionSettings` | `template.Properties` via `As<T>()/Put<T>()` | `profile.Settings` via `GetSettings/AlterSettings` |
| `AnalyticsMetadata` | `template.Properties` via `As<T>()/Put<T>()` | `profile.Properties` via `As<T>()/Put<T>()` |
| `AIProfileMetadata` | `template.Properties` via `As<T>()/Put<T>()` | `profile.Properties` via `As<T>()/Put<T>()` |
| `AgentMetadata` | `template.Properties` via `As<T>()/Put<T>()` | `profile.Properties` via `As<T>()/Put<T>()` |

## Security

- AI Template management requires the `ManageAIProfileTemplates` permission.
- Templates do not store API keys or sensitive connection details.
- Templates reference connections by name, not by credentials.
