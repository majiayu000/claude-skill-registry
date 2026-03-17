---
name: orchardcore-ai-chat
description: Skill for configuring AI Chat in Orchard Core using the CrestApps AI Chat module. Covers chat profiles, admin chat UI, frontend chat widgets, provider connections, and the AI Agent module for task automation.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core AI Chat - Prompt Templates

## Configure AI Chat

You are an Orchard Core expert. Generate code, configuration, and recipes for adding AI chat capabilities to an Orchard Core application using CrestApps modules.

### Guidelines

- The CrestApps AI Chat module (`CrestApps.OrchardCore.AI.Chat`) builds on the core AI Services feature to provide chat interfaces.
- You must enable at least one AI completion provider (OpenAI, Azure OpenAI, Azure AI Inference, Ollama, DeepSeek) alongside the chat feature.
- Chat-type AI profiles with the "Show On Admin Menu" option appear under the **Artificial Intelligence** section in the admin menu.
- When the Widgets feature is enabled, an AI Chat widget can be embedded in frontend content.
- The AI Agent module (`CrestApps.OrchardCore.AI.Agent`) extends AI profiles with capabilities for content management, user management, feature management, and more.
- Always secure API keys using user secrets or environment variables; never hardcode them.
- Install CrestApps packages in the web/startup project.

### Available AI Completion Providers

| Provider | Feature ID | Description |
|----------|-----------|-------------|
| OpenAI | `CrestApps.OrchardCore.OpenAI` | Connect to OpenAI or any OpenAI-compatible endpoint (DeepSeek, Gemini, Together AI, LM Studio, etc.) |
| Azure OpenAI | `CrestApps.OrchardCore.OpenAI.Azure.Standard` | Azure OpenAI service |
| Azure OpenAI with Data | `CrestApps.OrchardCore.OpenAI.Azure.AISearch` | Azure OpenAI with Azure AI Search data |
| Azure AI Inference | `CrestApps.OrchardCore.AzureAIInference` | Azure AI Inference (GitHub Models) |
| Ollama | `CrestApps.OrchardCore.Ollama` | Local Ollama models |

### Enabling AI Chat Features

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "CrestApps.OrchardCore.AI",
        "CrestApps.OrchardCore.AI.Chat",
        "CrestApps.OrchardCore.OpenAI"
      ],
      "disable": []
    }
  ]
}
```

### Setting Up a Provider Connection via Recipe

```json
{
  "steps": [
    {
      "name": "AIProviderConnections",
      "connections": [
        {
          "Source": "OpenAI",
          "Name": "default",
          "IsDefault": true,
          "DefaultDeploymentName": "gpt-4o",
          "DisplayText": "OpenAI",
          "Properties": {
            "OpenAIConnectionMetadata": {
              "Endpoint": "https://api.openai.com/v1",
              "ApiKey": "{{YourApiKey}}"
            }
          }
        }
      ]
    }
  ]
}
```

### Creating a Chat Profile via Recipe

```json
{
  "steps": [
    {
      "name": "AIProfile",
      "profiles": [
        {
          "Source": "OpenAI",
          "Name": "customer-support-chat",
          "DisplayText": "Customer Support Chat",
          "WelcomeMessage": "Hello! How can I help you today?",
          "FunctionNames": [],
          "Type": "Chat",
          "TitleType": "InitialPrompt",
          "PromptTemplate": null,
          "ConnectionName": "",
          "DeploymentId": "",
          "Properties": {
            "AIProfileMetadata": {
              "SystemMessage": "You are a helpful customer support assistant. Answer questions about our products and services. Be friendly and concise.",
              "Temperature": 0.3,
              "TopP": null,
              "FrequencyPenalty": null,
              "PresencePenalty": null,
              "MaxTokens": 2048,
              "PastMessagesCount": 10
            }
          }
        }
      ]
    }
  ]
}
```

### Making a Chat Profile Visible on the Admin Menu

When creating or editing a profile, enable the "Show On Admin Menu" option. Profiles with this setting appear under **Artificial Intelligence** in the admin sidebar.

### Defining a Chat Profile in Code with DataMigration

```csharp
public sealed class AIChatProfileMigrations : DataMigration
{
    private readonly IAIProfileManager _profileManager;

    public AIChatProfileMigrations(IAIProfileManager profileManager)
    {
        _profileManager = profileManager;
    }

    public async Task<int> CreateAsync()
    {
        var profile = await _profileManager.NewAsync("OpenAI");

        profile.Name = "site-assistant";
        profile.DisplayText = "Site Assistant";
        profile.Type = AIProfileType.Chat;

        profile.WithSettings(new AIProfileSettings
        {
            LockSystemMessage = true,
            IsRemovable = false,
            IsListable = true,
        });

        profile.WithSettings(new AIChatProfileSettings
        {
            IsOnAdminMenu = true,
        });

        profile.Put(new AIProfileMetadata
        {
            SystemMessage = "You are a site assistant. Help users navigate the site and answer questions.",
            Temperature = 0.3f,
            MaxTokens = 4096,
            PastMessagesCount = 10,
        });

        await _profileManager.SaveAsync(profile);

        return 1;
    }
}
```

### Enabling the AI Agent Module

The AI Agent module provides tools that allow AI profiles to perform tasks on the Orchard Core site (content management, feature management, user management, etc.).

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "CrestApps.OrchardCore.AI",
        "CrestApps.OrchardCore.AI.Chat",
        "CrestApps.OrchardCore.AI.Agent",
        "CrestApps.OrchardCore.OpenAI"
      ],
      "disable": []
    }
  ]
}
```

Once enabled, navigate to your AI profile and assign capabilities under the **Capabilities** tab.

### Adding an AI Chat Widget to Frontend Content

When the Widgets feature is enabled, you can add an AI Chat widget to zones. Create a widget layer and add the AI Chat widget to display the chat interface on your frontend pages.

### Creating a Custom AI Tool for Chat

```csharp
public sealed class LookupOrderFunction : AIFunction
{
    public const string TheName = "lookup_order";

    private static readonly JsonElement _jsonSchema = JsonSerializer.Deserialize<JsonElement>(
    """
     {
       "type": "object",
       "properties": {
         "OrderId": {
           "type": "string",
           "description": "The order ID to look up."
         }
       },
       "additionalProperties": false,
       "required": ["OrderId"]
     }
    """);

    public override string Name => TheName;

    public override string Description => "Looks up order details by order ID.";

    public override JsonElement JsonSchema => _jsonSchema;

    protected override async ValueTask<object> InvokeCoreAsync(
        AIFunctionArguments arguments,
        CancellationToken cancellationToken)
    {
        if (!arguments.TryGetValue("OrderId", out var value) || value is null)
        {
            return "OrderId is required.";
        }

        var orderId = value is JsonElement jsonElement
            ? jsonElement.GetString()
            : value?.ToString();

        // Replace with actual order lookup logic.
        return $"Order {orderId}: Status=Shipped, ETA=2 days.";
    }
}
```

Register the tool and assign it to a profile:

```csharp
services.AddAITool<LookupOrderFunction>(LookupOrderFunction.TheName, options =>
{
    options.Title = "Order Lookup";
    options.Description = "Looks up order details by order ID.";
    options.Category = "Commerce";
});
```

### Security Best Practices

- Store API keys using `dotnet user-secrets` during development.
- Use environment variables or Azure Key Vault in production.
- Restrict AI profile access with Orchard Core permissions.
- Set appropriate token limits to control costs.
- Lock system messages on production profiles to prevent prompt injection.
