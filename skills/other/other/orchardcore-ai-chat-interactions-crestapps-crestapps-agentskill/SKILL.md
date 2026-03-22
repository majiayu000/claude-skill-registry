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
- Users can select agents from the Capabilities tab to enhance interaction capabilities. Agent selection is saved via the SignalR hub.
- The Capabilities tab is organized: MCP Connections first, then Agents, then Tools.
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

To enable image generation, add a deployment with `Type: Image` in the `Deployments` array on your provider connection, or create an Image deployment through the admin UI.

**Via Admin UI:** Navigate to **Artificial Intelligence → Provider Connections**, edit your connection, and add an Image deployment (e.g., `dall-e-3`).

**Via appsettings.json:**

```json
{
  "OrchardCore": {
    "CrestApps_AI": {
      "Providers": {
        "OpenAI": {
          "Connections": {
            "default": {
              "Deployments": [
                { "Name": "gpt-4o", "Type": "Chat", "IsDefault": true },
                { "Name": "dall-e-3", "Type": "Image", "IsDefault": true }
              ]
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
              "Deployments": [
                { "Name": "gpt-4o", "Type": "Chat", "IsDefault": true },
                { "Name": "gpt-4o-mini", "Type": "Utility", "IsDefault": true },
                { "Name": "dall-e-3", "Type": "Image", "IsDefault": true }
              ]
            }
          }
        }
      }
    }
  }
}
```

If no Utility deployment is configured, the system falls back to the Chat deployment or keyword-based intent detection.

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

Documents require an embedding model for RAG. Add a deployment with `Type: Embedding` in the `Deployments` array on your provider connection, or create an Embedding deployment through the admin UI:

```json
{
  "OrchardCore": {
    "CrestApps_AI": {
      "Providers": {
        "OpenAI": {
          "Connections": {
            "default": {
              "Deployments": [
                { "Name": "gpt-4o", "Type": "Chat", "IsDefault": true },
                { "Name": "text-embedding-3-small", "Type": "Embedding", "IsDefault": true },
                { "Name": "gpt-4o-mini", "Type": "Utility", "IsDefault": true },
                { "Name": "dall-e-3", "Type": "Image", "IsDefault": true }
              ]
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

### Chat Mode in Chat Interactions

Chat interactions support the same `ChatMode` options as AI profiles, but configured at the site level via `ChatInteractionChatModeSettings` (under **Settings → AI Settings → Chat Interactions**):

| Mode | Description | Requirements |
|------|-------------|--------------|
| `TextOnly` | Standard text-only chat (default) | None |
| `AudioInput` | Adds microphone button for speech-to-text dictation | `DefaultSpeechToTextDeploymentId` configured |
| `Conversation` | Two-way voice conversation | Both `DefaultSpeechToTextDeploymentId` and `DefaultTextToSpeechDeploymentId` configured |

Unlike AI profiles (configured per profile), chat interactions use a **single site-wide setting** that applies to all chat interaction sessions.

### SignalR Hub Methods (ChatInteractionHub)

| Method | Description |
|--------|-------------|
| `SendMessage` | Sends a text message |
| `SendAudioStream` | Streams audio chunks for speech-to-text transcription |
| `StartConversation` | Starts a full two-way voice conversation |
| `SynthesizeSpeech` | Converts text to speech audio |
| `UpdateAgents` | Updates agent selection for a session |
| `ClearHistory` | Clears chat history for a session |

### Voice Configuration

When conversation mode is enabled, voices are populated from the configured TTS deployment. Voices are grouped by language in dropdown menus and sorted alphabetically. Each `SpeechVoice` includes `Id`, `Name`, `Language`, `Gender`, and `VoiceSampleUrl`.

### Conversation Mode Behavior

In conversation mode:
1. User clicks the headset button → persistent audio stream opens
2. Microphone, send button, and textarea are hidden/disabled
3. User speaks → audio streams to server via SignalR → STT transcribes → text appears as user message
4. Transcript is automatically sent to AI orchestrator → AI response text streams to message list AND audio streams back
5. User can interrupt by speaking → cancels current AI response → processes new prompt
6. User clicks headset again → ends conversation, restores normal UI
