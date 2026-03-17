---
name: orchardcore-ai-chat-interactions
description: Skill for configuring AI Chat Interactions in Orchard Core using the CrestApps module. Covers ad-hoc chat sessions, prompt routing with intent detection, document upload with RAG support, image and chart generation, and custom processing strategies.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core AI Chat Interactions - Prompt Templates

## Configure AI Chat Interactions

You are an Orchard Core expert. Generate code, configuration, and recipes for adding ad-hoc AI chat interactions with document upload, RAG, and intent-based prompt routing to an Orchard Core application using CrestApps modules.

### Guidelines

- The AI Chat Interactions module (`CrestApps.OrchardCore.AI.Chat.Interactions`) provides ad-hoc chat without predefined AI profiles.
- Users can configure temperature, TopP, max tokens, frequency/presence penalties, and past messages count per session.
- All chat messages are persisted and sessions can be resumed later.
- Prompt routing uses intent detection to classify user prompts and route them to specialized processing strategies.
- Intent detection can use a dedicated lightweight AI model or fall back to keyword-based detection.
- The Documents extension adds document upload with RAG (Retrieval Augmented Generation) support.
- Document indexing requires Elasticsearch or Azure AI Search as the embedding/search provider.
- Install CrestApps packages in the web/startup project.
- Always secure API keys using user secrets or environment variables.

### Enabling AI Chat Interactions

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "CrestApps.OrchardCore.AI",
        "CrestApps.OrchardCore.AI.Chat.Interactions",
        "CrestApps.OrchardCore.OpenAI"
      ],
      "disable": []
    }
  ]
}
```

### Getting Started

1. Enable the `AI Chat Interactions` feature in the Orchard Core admin under **Configuration → Features**.
2. Navigate to **Artificial Intelligence → Chat Interactions**.
3. Click **+ New Chat** and select an AI provider connection.
4. Configure chat settings (model, temperature, tools) and start chatting.

### Built-in Intents

The AI Chat Interactions module ships with default intents for image and chart generation:

| Intent | Description | Example Prompts |
|--------|-------------|-----------------|
| `GenerateImage` | Generate an image from a text description | "Generate an image of a sunset", "Create a picture of a cat" |
| `GenerateImageWithHistory` | Generate an image using conversation context | "Based on the above, draw a diagram" |
| `GenerateChart` | Generate a chart or graph specification | "Create a bar chart of sales data", "Draw a pie chart" |

### Configuring Image Generation

To enable image generation, set the `DefaultImagesDeploymentName` in your provider connection.

**Via Admin UI:** Navigate to **Artificial Intelligence → Provider Connections**, edit your connection, and set the **Images deployment name** (e.g., `dall-e-3`).

**Via appsettings.json:**

```json
{
  "OrchardCore": {
    "CrestApps_AI": {
      "Providers": {
        "OpenAI": {
          "Connections": {
            "default": {
              "DefaultDeploymentName": "gpt-4o",
              "DefaultImagesDeploymentName": "dall-e-3"
            }
          }
        }
      }
    }
  }
}
```

### Configuring Intent Detection Model

Use a lightweight model for intent classification to optimize costs:

```json
{
  "OrchardCore": {
    "CrestApps_AI": {
      "Providers": {
        "OpenAI": {
          "Connections": {
            "default": {
              "DefaultDeploymentName": "gpt-4o",
              "DefaultIntentDeploymentName": "gpt-4o-mini",
              "DefaultImagesDeploymentName": "dall-e-3"
            }
          }
        }
      }
    }
  }
}
```

If `DefaultIntentDeploymentName` is not configured, the system falls back to the `DefaultDeploymentName` (chat model) or keyword-based intent detection.

### Enabling Document Upload and RAG

The Documents extension (`CrestApps.OrchardCore.AI.Chat.Interactions.Documents`) adds document upload and document-aware prompt processing. It requires a search/indexing provider.

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "CrestApps.OrchardCore.AI",
        "CrestApps.OrchardCore.AI.Chat.Interactions",
        "CrestApps.OrchardCore.AI.Chat.Interactions.Documents.AzureAI",
        "OrchardCore.Search.AzureAI",
        "CrestApps.OrchardCore.OpenAI"
      ],
      "disable": []
    }
  ]
}
```

Or for Elasticsearch:

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "CrestApps.OrchardCore.AI",
        "CrestApps.OrchardCore.AI.Chat.Interactions",
        "CrestApps.OrchardCore.AI.Chat.Interactions.Documents.Elasticsearch",
        "OrchardCore.Search.Elasticsearch",
        "CrestApps.OrchardCore.OpenAI"
      ],
      "disable": []
    }
  ]
}
```

### Setting Up Document Indexing

1. Enable a search provider feature (Elasticsearch or Azure AI Search).
2. Navigate to **Search → Indexing** and create a new index (e.g., "ChatDocuments").
3. Navigate to **Settings → Chat Interaction** and select the new index as the default document index.
4. Enable the `AI Chat Interactions - Documents` feature.

### Configuring Embedding Model for Documents

Documents require an embedding model for RAG. Configure `DefaultEmbeddingDeploymentName` in your provider connection:

```json
{
  "OrchardCore": {
    "CrestApps_AI": {
      "Providers": {
        "OpenAI": {
          "Connections": {
            "default": {
              "DefaultDeploymentName": "gpt-4o",
              "DefaultEmbeddingDeploymentName": "text-embedding-3-small",
              "DefaultIntentDeploymentName": "gpt-4o-mini",
              "DefaultImagesDeploymentName": "dall-e-3"
            }
          }
        }
      }
    }
  }
}
```

### Supported Document Formats

| Format | Extension | Required Feature |
|--------|-----------|------------------|
| PDF | .pdf | `CrestApps.OrchardCore.AI.Chat.Interactions.Pdf` |
| Word | .docx | `CrestApps.OrchardCore.AI.Chat.Interactions.OpenXml` |
| Excel | .xlsx | `CrestApps.OrchardCore.AI.Chat.Interactions.OpenXml` |
| PowerPoint | .pptx | `CrestApps.OrchardCore.AI.Chat.Interactions.OpenXml` |
| Text | .txt | Built-in |
| CSV | .csv | Built-in |
| Markdown | .md | Built-in |
| JSON | .json | Built-in |
| XML | .xml | Built-in |
| HTML | .html, .htm | Built-in |
| YAML | .yml, .yaml | Built-in |

Legacy Office formats (.doc, .xls, .ppt) are not supported. Convert them to newer formats.

### Document Intent Types

When documents are uploaded, the intent detector routes prompts to specialized strategies:

| Intent | Description | Example Prompts |
|--------|-------------|-----------------|
| `DocumentQnA` | Question answering using RAG | "What does this document say about X?" |
| `SummarizeDocument` | Document summarization | "Summarize this document" |
| `AnalyzeTabularData` | CSV/Excel data analysis | "Calculate the total sales" |
| `ExtractStructuredData` | Structured data extraction | "Extract all email addresses" |
| `CompareDocuments` | Multi-document comparison | "Compare these two documents" |
| `TransformFormat` | Content reformatting | "Convert to bullet points" |
| `GeneralChatWithReference` | General chat using document context | Default fallback |

### Adding a Custom Processing Strategy

Register a custom intent and strategy to extend prompt routing:

```csharp
public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddPromptProcessingIntent(
            "TranslateDocument",
            "The user wants to translate the document content to another language.");

        services.AddPromptProcessingStrategy<TranslateDocumentStrategy>();
    }
}
```

### Enabling PDF and Office Document Support

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "CrestApps.OrchardCore.AI.Chat.Interactions.Pdf",
        "CrestApps.OrchardCore.AI.Chat.Interactions.OpenXml"
      ],
      "disable": []
    }
  ]
}
```

### Document Upload API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ai/chat-interactions/upload-document` | POST | Upload one or more documents |
| `/ai/chat-interactions/remove-document` | POST | Remove a document |
