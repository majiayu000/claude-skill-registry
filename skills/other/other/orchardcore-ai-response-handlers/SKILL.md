---
name: orchardcore-ai-response-handlers
description: Skill for implementing custom Chat Response Handlers in Orchard Core. Covers IChatResponseHandler, deferred and streaming handlers, webhook endpoints, live agent handoff, mid-conversation transfer via AI functions, UI notifications, protocol-agnostic relay infrastructure, and handler registration.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "2.0"
---

# Orchard Core Chat Response Handlers - Prompt Templates

## Implement Custom Chat Response Handlers

You are an Orchard Core expert. Generate code for implementing custom chat response handlers that route chat prompts to external systems (live agent platforms, custom backends) instead of AI. Support both webhook-based and protocol-agnostic relay approaches.

### Guidelines

- The `IChatResponseHandler` interface processes chat prompts and returns either a **streaming** result (immediate response) or a **deferred** result (response arrives later via webhook or relay).
- Handlers are registered in `Startup.cs` using `services.TryAddEnumerable(ServiceDescriptor.Scoped<IChatResponseHandler, YourHandler>())`.
- When a session's `ResponseHandlerName` is `null` or empty, the built-in AI handler processes prompts.
- Custom response handlers are NOT supported in Conversation mode (`ChatMode.Conversation`). The resolver always returns the AI handler in Conversation mode.
- Deferred handlers return `ChatResponseHandlerResult.Deferred()` — the hub saves the user prompt and completes without an assistant message. The external system responds later via webhook or relay.
- For deferred responses, create a webhook endpoint that writes the response to chat history and sends it to the client via SignalR. Or use the protocol-agnostic relay infrastructure for persistent connections.
- Reference `CrestApps.OrchardCore.AI.Chat.Core` (not the module projects) when resolving `IHubContext<AIChatHub>` or `IHubContext<ChatInteractionHub>`.
- Use `AIChatHub.GetSessionGroupName(sessionId)` and `ChatInteractionHub.GetInteractionGroupName(itemId)` for SignalR group names.
- For AI-function-based transfers, use `AIInvocationScope.Current` to access the active session or interaction.
- The hub automatically saves the session after AI response completes — do NOT call `SaveAsync` manually in transfer functions.
- Use `IChatNotificationSender` to send UI feedback (typing indicators, transfer status, session endings) — no JavaScript required.
- Create `ChatNotification` objects directly using constructor: `new ChatNotification("type")`. The `Type` setter is private — type must be passed via constructor.
- Use `ChatNotificationTypes` for well-known notification types (Typing, Transfer, AgentConnected, etc.).
- Use `ChatNotificationActionNames` for well-known action names (CancelTransfer, EndSession).
- **Do NOT use extension methods** — `ChatNotificationSenderExtensions` has been removed. Build notifications directly with `new ChatNotification("type") { ... }` and call `sender.SendAsync`, `sender.UpdateAsync`, or `sender.RemoveAsync`.
- Register notification action handlers as keyed services: `services.AddKeyedScoped<IChatNotificationActionHandler, YourHandler>("your-action-name")`.
- Seal all service classes. Use `internal sealed` for implementations in modules.
- Always name `IStringLocalizer` variables `T` (not `localizer`). This is required for Orchard Core's language extraction tooling.
- Never concatenate localized strings. Use a single combined phrase for translation.

### Two Approaches: Webhook vs. Protocol-Agnostic Relay

| Approach | When to Use | Key Interfaces |
|----------|------------|----------------|
| **Webhook** | External system pushes events via HTTP callbacks | `IChatNotificationSender`, `IHubContext<T>` |
| **Protocol-Agnostic Relay** | Persistent connections (WebSocket, SSE, gRPC, message queues) | `IExternalChatRelay`, `IExternalChatRelayManager`, `IExternalChatRelayEventHandler` |

### Handler Types

| Type | When to Use | Result |
|------|------------|--------|
| Streaming | External system returns response immediately | `ChatResponseHandlerResult.Stream(asyncEnumerable)` |
| Deferred | External system responds later via webhook or relay | `ChatResponseHandlerResult.Deferred()` |

### Creating a Deferred Response Handler

```csharp
using CrestApps.OrchardCore.AI;
using CrestApps.OrchardCore.AI.Models;

public sealed class GenesysResponseHandler : IChatResponseHandler
{
    public string Name => "Genesys";

    public async Task<ChatResponseHandlerResult> HandleAsync(
        ChatResponseHandlerContext context,
        CancellationToken cancellationToken = default)
    {
        var genesysClient = context.Services.GetRequiredService<IGenesysClient>();

        await genesysClient.SendMessageAsync(new GenesysMessage
        {
            SessionId = context.SessionId,
            ConnectionId = context.ConnectionId,
            ChatType = context.ChatType.ToString(),
            Text = context.Prompt,
        });

        return ChatResponseHandlerResult.Deferred();
    }
}
```

### Registering a Handler

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using OrchardCore.Modules;

public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.TryAddEnumerable(
            ServiceDescriptor.Scoped<IChatResponseHandler, GenesysResponseHandler>());
    }
}
```

### Webhook for Deferred Responses (AI Chat Session)

```csharp
using CrestApps.OrchardCore.AI.Chat.Hubs;
using CrestApps.OrchardCore.AI.Models;
using CrestApps.Support;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Routing;
using Microsoft.AspNetCore.SignalR;
using Microsoft.Extensions.AI;

internal static class WebhookEndpoint
{
    public static IEndpointRouteBuilder MapWebhookEndpoint(this IEndpointRouteBuilder builder)
    {
        builder.MapPost("api/agent/webhook", HandleAsync).AllowAnonymous().DisableAntiforgery();
        return builder;
    }

    private static async Task<IResult> HandleAsync(
        HttpRequest request,
        AgentWebhookPayload payload,
        IAIChatSessionManager sessionManager,
        IAIChatSessionPromptStore promptStore,
        IHubContext<AIChatHub> chatHubContext)
    {
        var session = await sessionManager.FindByIdAsync(payload.SessionId);

        if (session is null)
        {
            return TypedResults.NotFound();
        }

        var prompt = new AIChatSessionPrompt
        {
            ItemId = IdGenerator.GenerateId(),
            SessionId = session.SessionId,
            Role = ChatRole.Assistant,
            Content = payload.AgentMessage,
        };
        await promptStore.CreateAsync(prompt);

        var groupName = AIChatHub.GetSessionGroupName(session.SessionId);
        await chatHubContext.Clients.Group(groupName).SendAsync("ReceiveMessage", new
        {
            sessionId = session.SessionId,
            messageId = prompt.ItemId,
            content = payload.AgentMessage,
            role = "assistant",
        });

        return TypedResults.Ok();
    }
}
```

### Mid-Conversation Transfer via AI Function

```csharp
using System.Text.Json;
using CrestApps.OrchardCore.AI.Models;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.DependencyInjection;

public sealed class TransferToAgentFunction : AIFunction
{
    public const string TheName = "transfer_to_live_agent";

    private static readonly JsonElement _jsonSchema = JsonSerializer.Deserialize<JsonElement>(
        """
        {
          "type": "object",
          "properties": {
            "queue_name": { "type": "string", "description": "The agent queue name." },
            "reason": { "type": "string", "description": "Why the user is being transferred." }
          },
          "required": ["queue_name"],
          "additionalProperties": false
        }
        """);

    public override string Name => TheName;
    public override string Description => "Transfers the user to a live support agent.";
    public override JsonElement JsonSchema => _jsonSchema;

    protected override async ValueTask<object> InvokeCoreAsync(
        AIFunctionArguments arguments,
        CancellationToken cancellationToken)
    {
        if (!arguments.TryGetFirstString("queue_name", out var queueName))
        {
            return "Unable to find a 'queue_name' argument.";
        }

        var invocationScope = AIInvocationScope.Current;

        if (invocationScope?.Items.TryGetValue(nameof(AIChatSession), out var sessionObj) == true
            && sessionObj is AIChatSession chatSession)
        {
            // Check Conversation mode — custom handlers not supported.
            var profileManager = arguments.Services.GetRequiredService<IAIProfileManager>();
            var profile = await profileManager.FindByIdAsync(chatSession.ProfileId);

            if (profile != null
                && profile.TryGetSettings<ChatModeProfileSettings>(out var settings)
                && settings.ChatMode == ChatMode.Conversation)
            {
                return "Transfer not available in Conversation mode.";
            }

            chatSession.ResponseHandlerName = "Genesys";
        }
        else if (invocationScope?.ToolExecutionContext?.Resource is ChatInteraction interaction)
        {
            interaction.ResponseHandlerName = "Genesys";
        }
        else
        {
            return "No active chat session found.";
        }

        return $"Transferring to '{queueName}' queue. Please wait...";
    }
}
```

Register the transfer function:

```csharp
using CrestApps.OrchardCore.AI.Core.Extensions;

public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddAITool<TransferToAgentFunction>(TransferToAgentFunction.TheName);
    }
}
```

### Sending UI Notifications from Webhooks

Use `IChatNotificationSender` to send typing indicators, transfer status, and session endings from webhooks. Create `ChatNotification` objects directly and use well-known constants from `ChatNotificationTypes` and `ChatNotificationActionNames`:

```csharp
using CrestApps.OrchardCore.AI;
using CrestApps.OrchardCore.AI.Models;
using Microsoft.Extensions.Localization;

internal static class AgentEventEndpoints
{
    public static IEndpointRouteBuilder MapAgentEventEndpoints(this IEndpointRouteBuilder builder)
    {
        builder.MapPost("api/agent/typing", OnAgentTyping).AllowAnonymous().DisableAntiforgery();
        builder.MapPost("api/agent/transfer-started", OnTransferStarted).AllowAnonymous().DisableAntiforgery();
        builder.MapPost("api/agent/transfer-completed", OnTransferCompleted).AllowAnonymous().DisableAntiforgery();
        builder.MapPost("api/agent/session-ended", OnSessionEnded).AllowAnonymous().DisableAntiforgery();
        return builder;
    }

    private static async Task<IResult> OnAgentTyping(
        AgentTypingPayload payload,
        IChatNotificationSender notifications,
        IStringLocalizer<AgentEventEndpoints> T)
    {
        if (payload.IsTyping)
        {
            await notifications.SendAsync(
                payload.SessionId,
                ChatContextType.AIChatSession,
                new ChatNotification(ChatNotificationTypes.Typing)
                {
                    Content = string.IsNullOrEmpty(payload.AgentName)
                        ? T["Agent is typing"].Value
                        : T["{0} is typing", payload.AgentName].Value,
                    Icon = "fa-solid fa-ellipsis",
                });
        }
        else
        {
            await notifications.RemoveAsync(
                payload.SessionId,
                ChatContextType.AIChatSession,
                ChatNotificationTypes.Typing);
        }

        return TypedResults.Ok();
    }

    private static async Task<IResult> OnTransferStarted(
        TransferPayload payload,
        IChatNotificationSender notifications,
        IStringLocalizer<AgentEventEndpoints> T)
    {
        await notifications.SendAsync(
            payload.SessionId,
            ChatContextType.AIChatSession,
            new ChatNotification(ChatNotificationTypes.Transfer)
            {
                Content = !string.IsNullOrEmpty(payload.EstimatedWait)
                    ? T["Transferring you to a live agent... Estimated wait: {0}.", payload.EstimatedWait].Value
                    : T["Transferring you to a live agent..."].Value,
                Icon = "fa-solid fa-headset",
                Actions =
                [
                    new ChatNotificationAction
                    {
                        Name = ChatNotificationActionNames.CancelTransfer,
                        Label = T["Cancel Transfer"].Value,
                        CssClass = "btn-outline-danger",
                        Icon = "fa-solid fa-xmark",
                    },
                ],
            });

        return TypedResults.Ok();
    }

    private static async Task<IResult> OnTransferCompleted(
        TransferPayload payload,
        IChatNotificationSender notifications,
        IStringLocalizer<AgentEventEndpoints> T)
    {
        await notifications.RemoveAsync(
            payload.SessionId,
            ChatContextType.AIChatSession,
            ChatNotificationTypes.Transfer);

        await notifications.SendAsync(
            payload.SessionId,
            ChatContextType.AIChatSession,
            new ChatNotification(ChatNotificationTypes.AgentConnected)
            {
                Content = string.IsNullOrEmpty(payload.AgentName)
                    ? T["You are now connected to a live agent."].Value
                    : T["You are now connected to {0}.", payload.AgentName].Value,
                Icon = "fa-solid fa-user-check",
                Dismissible = true,
            });

        return TypedResults.Ok();
    }

    private static async Task<IResult> OnSessionEnded(
        SessionEndPayload payload,
        IChatNotificationSender notifications,
        IStringLocalizer<AgentEventEndpoints> T)
    {
        await notifications.SendAsync(
            payload.SessionId,
            ChatContextType.AIChatSession,
            new ChatNotification(ChatNotificationTypes.SessionEnded)
            {
                Content = T["This chat session has ended."].Value,
                Icon = "fa-solid fa-circle-check",
                Dismissible = true,
            });

        return TypedResults.Ok();
    }
}
```

### Protocol-Agnostic Relay Infrastructure

For persistent connections (WebSocket, SSE, gRPC, message queues), implement `IExternalChatRelay` instead of webhooks. The relay infrastructure provides:

- **`IExternalChatRelay`** — protocol-agnostic interface for bidirectional communication. Supports any transport.
- **`IExternalChatRelayManager`** — singleton that manages relay lifecycle (connect, disconnect, retrieve by session).
- **`IExternalChatRelayEventHandler`** — routes relay events through keyed `IExternalChatRelayNotificationBuilder` services.
- **`ExternalChatRelayEventTypes`** — string constants for built-in event types (agent-typing, agent-connected, etc.).

#### Implementing a WebSocket Relay

```csharp
using CrestApps.OrchardCore.AI;
using CrestApps.OrchardCore.AI.Models;
using Microsoft.Extensions.DependencyInjection;

internal sealed class GenesysWebSocketRelay : IExternalChatRelay
{
    private readonly IServiceScopeFactory _scopeFactory;
    private ClientWebSocket? _webSocket;

    public GenesysWebSocketRelay(IServiceScopeFactory scopeFactory)
    {
        _scopeFactory = scopeFactory;
    }

    public string SessionId { get; set; } = string.Empty;
    public ChatContextType ChatType { get; set; }

    public Task<bool> IsConnectedAsync(CancellationToken cancellationToken = default)
        => Task.FromResult(_webSocket?.State == WebSocketState.Open);

    public async Task ConnectAsync(CancellationToken cancellationToken = default)
    {
        _webSocket = new ClientWebSocket();
        await _webSocket.ConnectAsync(new Uri("wss://genesys.example.com/ws"), cancellationToken);

        // Start background listener that dispatches events.
        _ = Task.Run(() => ListenForEventsAsync(cancellationToken), cancellationToken);
    }

    public async Task SendPromptAsync(string prompt, CancellationToken cancellationToken = default)
    {
        var bytes = Encoding.UTF8.GetBytes(prompt);
        await _webSocket!.SendAsync(bytes, WebSocketMessageType.Text, true, cancellationToken);
    }

    public Task SendSignalAsync(string signal, CancellationToken cancellationToken = default)
        => Task.CompletedTask;

    public async Task DisconnectAsync(CancellationToken cancellationToken = default)
    {
        if (_webSocket?.State == WebSocketState.Open)
        {
            await _webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, null, cancellationToken);
        }
    }

    public async ValueTask DisposeAsync()
    {
        _webSocket?.Dispose();
    }

    private async Task ListenForEventsAsync(CancellationToken cancellationToken)
    {
        var buffer = new byte[4096];
        while (_webSocket?.State == WebSocketState.Open && !cancellationToken.IsCancellationRequested)
        {
            var result = await _webSocket.ReceiveAsync(buffer, cancellationToken);
            var json = Encoding.UTF8.GetString(buffer, 0, result.Count);
            var relayEvent = ParseEvent(json);

            // Create a new scope per event for DI.
            await using var scope = _scopeFactory.CreateAsyncScope();
            var eventHandler = scope.ServiceProvider.GetRequiredService<IExternalChatRelayEventHandler>();
            var context = new ExternalChatRelayContext
            {
                SessionId = SessionId,
                ChatType = ChatType,
            };
            await eventHandler.HandleAsync(context, relayEvent, cancellationToken);
        }
    }

    private static ExternalChatRelayEvent ParseEvent(string json)
    {
        // Parse JSON from your external platform into ExternalChatRelayEvent.
        // Map platform event types to ExternalChatRelayEventTypes constants.
        return new ExternalChatRelayEvent
        {
            EventType = ExternalChatRelayEventTypes.AgentTyping,
        };
    }
}
```

#### Registering a Relay in Startup

```csharp
public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        // Register your relay implementation.
        services.AddScoped<GenesysWebSocketRelay>();

        // Register the response handler.
        services.TryAddEnumerable(
            ServiceDescriptor.Scoped<IChatResponseHandler, GenesysResponseHandler>());
    }
}
```

#### Using the Relay in a Response Handler

```csharp
internal sealed class GenesysResponseHandler : IChatResponseHandler
{
    public string Name => "Genesys";

    public async Task<ChatResponseHandlerResult> HandleAsync(
        ChatResponseHandlerContext context,
        CancellationToken cancellationToken = default)
    {
        var relay = context.Services.GetRequiredService<GenesysWebSocketRelay>();
        relay.SessionId = context.SessionId;
        relay.ChatType = context.ChatType;

        var relayManager = context.Services.GetRequiredService<IExternalChatRelayManager>();
        await relayManager.ConnectAsync(relay, cancellationToken);

        // Forward the prompt to the external platform.
        await relay.SendPromptAsync(context.Prompt, cancellationToken);

        return ChatResponseHandlerResult.Deferred();
    }
}
```

#### Adding Custom Relay Event Types

Register a keyed `IExternalChatRelayNotificationBuilder` for custom event types:

```csharp
// In Startup.cs:
services.AddKeyedScoped<IExternalChatRelayNotificationBuilder, SupervisorJoinedBuilder>("supervisor-joined");
```

Implement the builder:

```csharp
internal sealed class SupervisorJoinedBuilder : IExternalChatRelayNotificationBuilder
{
    // Declares the notification type — used to create ChatNotification("info").
    public string? NotificationType => "info";

    public void Build(
        ExternalChatRelayEvent relayEvent,
        ChatNotification notification,
        ExternalChatRelayNotificationResult result,
        IStringLocalizer T)
    {
        var name = relayEvent.Data?.TryGetValue("supervisor_name", out var n) == true ? n : null;
        notification.Content = string.IsNullOrEmpty(name)
            ? T["A supervisor has joined the conversation."].Value
            : T["{0} (supervisor) has joined.", name].Value;
        notification.Icon = "fa-solid fa-user-shield";
        notification.Dismissible = true;
    }
}
```

Built-in event types with registered builders:

| Event Type | Builder Behavior |
|------------|-----------------|
| `ExternalChatRelayEventTypes.AgentTyping` | Sends typing indicator notification |
| `ExternalChatRelayEventTypes.AgentStoppedTyping` | Removes typing indicator (no notification) |
| `ExternalChatRelayEventTypes.AgentConnected` | Sends agent-connected info + removes transfer |
| `ExternalChatRelayEventTypes.AgentDisconnected` | Removes agent-connected notification (no notification) |
| `ExternalChatRelayEventTypes.AgentReconnecting` | Sends reconnecting warning notification |
| `ExternalChatRelayEventTypes.ConnectionLost` | Sends connection-lost error notification |
| `ExternalChatRelayEventTypes.ConnectionRestored` | Removes connection-lost notification (no notification) |
| `ExternalChatRelayEventTypes.WaitTimeUpdated` | Updates transfer notification (`IsUpdate = true`) |
| `ExternalChatRelayEventTypes.SessionEnded` | Sends session-ended notification |

### Custom Notification Action Handler

Handle user-initiated actions on notification system messages (e.g., feedback buttons):

```csharp
using CrestApps.OrchardCore.AI;
using CrestApps.OrchardCore.AI.Models;

public sealed class FeedbackActionHandler : IChatNotificationActionHandler
{
    public async Task HandleAsync(
        ChatNotificationActionContext context,
        CancellationToken cancellationToken = default)
    {
        var feedbackService = context.Services.GetRequiredService<IFeedbackService>();
        await feedbackService.RecordAsync(context.SessionId, positive: true);

        var notifications = context.Services.GetRequiredService<IChatNotificationSender>();
        await notifications.RemoveAsync(context.SessionId, context.ChatType, context.NotificationType);
    }
}
```

### Custom Notification with Action Buttons

```csharp
await notifications.SendAsync(sessionId, ChatContextType.AIChatSession, new ChatNotification("feedback-request")
{
    Content = "Was this helpful?",
    Icon = "fa-solid fa-star",
    Dismissible = true,
    Actions =
    [
        new ChatNotificationAction
        {
            Name = "feedback-positive",
            Label = "Yes!",
            CssClass = "btn-outline-success",
            Icon = "fa-solid fa-thumbs-up",
        },
        new ChatNotificationAction
        {
            Name = "feedback-negative",
            Label = "No",
            CssClass = "btn-outline-secondary",
            Icon = "fa-solid fa-thumbs-down",
        },
    ],
});
```

### Handler Context Properties

| Property | Type | Description |
|----------|------|-------------|
| `Prompt` | `string` | The user's message text |
| `ConnectionId` | `string` | The SignalR connection ID |
| `SessionId` | `string` | The session or interaction ID |
| `ChatType` | `ChatContextType` | `AIChatSession` or `ChatInteraction` |
| `ConversationHistory` | `IList<ChatMessage>` | Previous messages in the conversation |
| `Services` | `IServiceProvider` | Scoped service provider |
| `Profile` | `AIProfile` | The AI profile (for AI Chat Sessions) |
| `ChatSession` | `AIChatSession` | The chat session (for AI Chat Sessions) |
| `Interaction` | `ChatInteraction` | The interaction (for Chat Interactions) |

### Well-Known Constants

**Notification Types** (`ChatNotificationTypes`):

| Constant | Value | Description |
|----------|-------|-------------|
| `Typing` | `"typing"` | Typing indicator |
| `Transfer` | `"transfer"` | Transfer status notification |
| `AgentConnected` | `"agent-connected"` | Agent connected notification |
| `AgentReconnecting` | `"agent-reconnecting"` | Agent reconnecting warning |
| `ConnectionLost` | `"connection-lost"` | Connection lost error |
| `ConversationEnded` | `"conversation-ended"` | Conversation ended notification |
| `SessionEnded` | `"session-ended"` | Session ended notification |

**Action Names** (`ChatNotificationActionNames`):

| Constant | Value | Description |
|----------|-------|-------------|
| `CancelTransfer` | `"cancel-transfer"` | Cancel transfer action |
| `EndSession` | `"end-session"` | End session action |

### Built-In Notification Action Handlers

| Action Name | Behavior |
|-------------|----------|
| `cancel-transfer` | Resets `ResponseHandlerName` to `null` (back to AI), removes transfer notification |
| `end-session` | Closes session (`Status = Closed`), shows session ended notification |

### Configuring Initial Response Handler

Via AI Profile settings:
```csharp
profile.AlterSettings<ResponseHandlerProfileSettings>(settings =>
{
    settings.InitialResponseHandlerName = "Genesys";
});
```

### SignalR Group Names

| Chat Type | Group Name Pattern |
|-----------|-------------------|
| AI Chat Session | `aichat-session-{sessionId}` |
| Chat Interaction | `chat-interaction-{itemId}` |
