---
name: orchardcore-ai
description: Skill for configuring AI integrations in Orchard Core. Covers AI service registration, MCP enablement, prompt configuration, and agent framework integration.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core AI - Prompt Templates

## Configure AI Integration

You are an Orchard Core expert. Generate code and configuration for AI integrations in Orchard Core.

### Guidelines

- Orchard Core supports AI integrations through the CrestApps AI module ecosystem.
- Supported AI providers: OpenAI, Azure, AzureAIInference, and Ollama.
- Configure AI services through `appsettings.json` or the admin UI.
- Use dependency injection to access AI services in modules.
- Always secure API keys using user secrets or environment variables, never hardcode them.
- AI profiles define how the AI system interacts with users, including system messages and response behavior.
- Profile types include `Chat`, `Utility`, and `TemplatePrompt`.

### Enabling AI Features

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "CrestApps.OrchardCore.AI"
      ],
      "disable": []
    }
  ]
}
```

### AI Configuration in appsettings.json

```json
{
  "OrchardCore": {
    "CrestApps_AI": {
      "DefaultParameters": {
        "Temperature": 0,
        "MaxOutputTokens": 800,
        "TopP": 1,
        "FrequencyPenalty": 0,
        "PresencePenalty": 0,
        "PastMessagesCount": 10,
        "MaximumIterationsPerRequest": 1,
        "EnableOpenTelemetry": false,
        "EnableDistributedCaching": true
      },
      "Providers": {
        "OpenAI": {
          "DefaultConnectionName": "default",
          "DefaultDeploymentName": "gpt-4o",
          "DefaultIntentDeploymentName": "gpt-4o-mini",
          "DefaultEmbeddingDeploymentName": "",
          "DefaultImagesDeploymentName": "",
          "Connections": {
            "default": {
              "DefaultDeploymentName": "gpt-4o",
              "DefaultIntentDeploymentName": "gpt-4o-mini"
            }
          }
        }
      }
    }
  }
}
```

### Deployment Name Settings

| Setting | Description | Required |
|---------|-------------|----------|
| `DefaultDeploymentName` | The default model for chat completions | Yes |
| `DefaultEmbeddingDeploymentName` | The model for generating embeddings (for RAG/vector search) | No |
| `DefaultIntentDeploymentName` | A lightweight model for intent classification (e.g., `gpt-4o-mini`) | No |
| `DefaultImagesDeploymentName` | The model for image generation (e.g., `dall-e-3`) | No |

### Adding AI Provider Connection via Recipe

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

### Creating AI Profiles via Recipe

```json
{
  "steps": [
    {
      "name": "AIProfile",
      "profiles": [
        {
          "Source": "OpenAI",
          "Name": "{{ProfileName}}",
          "DisplayText": "{{DisplayName}}",
          "WelcomeMessage": "{{WelcomeMessage}}",
          "FunctionNames": [],
          "Type": "Chat",
          "TitleType": "InitialPrompt",
          "PromptTemplate": null,
          "ConnectionName": "",
          "DeploymentId": "",
          "Properties": {
            "AIProfileMetadata": {
              "SystemMessage": "{{SystemMessage}}",
              "Temperature": null,
              "TopP": null,
              "FrequencyPenalty": null,
              "PresencePenalty": null,
              "MaxTokens": null,
              "PastMessagesCount": null
            }
          }
        }
      ]
    }
  ]
}
```

### Defining Chat Profiles Using Code

```csharp
public sealed class SystemDefinedAIProfileMigrations : DataMigration
{
    private readonly IAIProfileManager _profileManager;

    public SystemDefinedAIProfileMigrations(IAIProfileManager profileManager)
    {
        _profileManager = profileManager;
    }

    public async Task<int> CreateAsync()
    {
        var profile = await _profileManager.NewAsync("OpenAI");

        profile.Name = "UniqueTechnicalName";
        profile.DisplayText = "A Display name for the profile";
        profile.Type = AIProfileType.Chat;

        profile.WithSettings(new AIProfileSettings
        {
            LockSystemMessage = true,
            IsRemovable = false,
            IsListable = false,
        });

        profile.WithSettings(new AIChatProfileSettings
        {
            IsOnAdminMenu = true,
        });

        profile.Put(new AIProfileMetadata
        {
            SystemMessage = "some system message",
            Temperature = 0.3f,
            MaxTokens = 4096,
        });

        await _profileManager.SaveAsync(profile);

        return 1;
    }
}
```

### Extending AI Chat with Custom Functions

```csharp
public sealed class GetWeatherFunction : AIFunction
{
    public const string TheName = "get_weather";

    private static readonly JsonElement _jsonSchema = JsonSerializer.Deserialize<JsonElement>(
    """
     {
       "type": "object",
       "properties": {
         "Location": {
           "type": "string",
           "description": "The geographic location for which the weather information is requested."
         }
       },
       "additionalProperties": false,
       "required": ["Location"]
     }
    """);

    public override string Name => TheName;

    public override string Description => "Retrieves weather information for a specified location.";

    public override JsonElement JsonSchema => _jsonSchema;

    protected override ValueTask<object> InvokeCoreAsync(AIFunctionArguments arguments, CancellationToken cancellationToken)
    {
        if (!arguments.TryGetValue("Location", out var prompt) || prompt is null)
        {
            return ValueTask.FromResult<object>("Location is required.");
        }

        var location = prompt is JsonElement jsonElement
            ? jsonElement.GetString()
            : prompt?.ToString();

        var weather = Random.Shared.NextDouble() > 0.5
            ? $"It's sunny in {location}."
            : $"It's raining in {location}.";

        return ValueTask.FromResult<object>(weather);
    }
}
```

### Registering Custom AI Tools

```csharp
services.AddAITool<GetWeatherFunction>(GetWeatherFunction.TheName);
```

Or with configuration options:

```csharp
services.AddAITool<GetWeatherFunction>(GetWeatherFunction.TheName, options =>
{
    options.Title = "Weather Getter";
    options.Description = "Retrieves weather information for a specified location.";
    options.Category = "Service";
});
```

### Security Best Practices

- Store API keys in user secrets during development: `dotnet user-secrets set "OrchardCore:CrestApps_AI:Providers:OpenAI:Connections:default:ApiKey" "your-key"`
- Use environment variables in production.
- Apply appropriate permissions to restrict AI feature access.
- Monitor token usage and set rate limits for production deployments.
