---
name: streaming-llm-responses
description: |
  Implement real-time streaming UI patterns for AI chat applications. Use when adding response
  lifecycle handlers, progress indicators, client effects, or thread state synchronization.
  Covers onResponseStart/End, onEffect, ProgressUpdateEvent, and client tools.
  NOT when building basic chat without real-time feedback.
---

# Streaming LLM Responses

Build responsive, real-time chat interfaces with streaming feedback.

## Quick Start

```typescript
import { useChatKit } from "@openai/chatkit-react";

const chatkit = useChatKit({
  api: { url: API_URL, domainKey: DOMAIN_KEY },

  onResponseStart: () => setIsResponding(true),
  onResponseEnd: () => setIsResponding(false),

  onEffect: ({ name, data }) => {
    if (name === "update_status") updateUI(data);
  },
});
```

---

## Response Lifecycle

```
User sends message
    ↓
onResponseStart() fires
    ↓
[Streaming: tokens arrive, ProgressUpdateEvents shown]
    ↓
onResponseEnd() fires
    ↓
UI unlocks, ready for next interaction
```

---

## Core Patterns

### 1. Response Lifecycle Handlers

Lock UI during AI response to prevent race conditions:

```typescript
function ChatWithLifecycle() {
  const [isResponding, setIsResponding] = useState(false);
  const lockInteraction = useAppStore((s) => s.lockInteraction);
  const unlockInteraction = useAppStore((s) => s.unlockInteraction);

  const chatkit = useChatKit({
    api: { url: API_URL, domainKey: DOMAIN_KEY },

    onResponseStart: () => {
      setIsResponding(true);
      lockInteraction(); // Disable map/canvas/form interactions
    },

    onResponseEnd: () => {
      setIsResponding(false);
      unlockInteraction();
    },

    onError: ({ error }) => {
      console.error("ChatKit error:", error);
      setIsResponding(false);
      unlockInteraction();
    },
  });

  return (
    <div>
      {isResponding && <LoadingOverlay />}
      <ChatKit control={chatkit.control} />
    </div>
  );
}
```

### 2. Client Effects (Fire-and-Forget)

Server sends effects to update client UI without expecting a response:

**Backend - Streaming Effects:**

```python
from chatkit.types import ClientEffectEvent

async def respond(self, thread, item, context):
    # ... agent processing ...

    # Fire client effect to update UI
    yield ClientEffectEvent(
        name="update_status",
        data={
            "state": {"energy": 80, "happiness": 90},
            "flash": "Status updated!"
        }
    )

    # Another effect
    yield ClientEffectEvent(
        name="show_notification",
        data={"message": "Task completed!"}
    )
```

**Frontend - Handling Effects:**

```typescript
const chatkit = useChatKit({
  api: { url: API_URL, domainKey: DOMAIN_KEY },

  onEffect: ({ name, data }) => {
    switch (name) {
      case "update_status":
        applyStatusUpdate(data.state);
        if (data.flash) setFlashMessage(data.flash);
        break;

      case "add_marker":
        addMapMarker(data);
        break;

      case "select_mode":
        setSelectionMode(data.mode);
        break;
    }
  },
});
```

### 3. Progress Updates

Show "Searching...", "Loading...", "Analyzing..." during long operations:

```python
from chatkit.types import ProgressUpdateEvent

@function_tool
async def search_articles(ctx: AgentContext, query: str) -> str:
    """Search for articles matching the query."""

    yield ProgressUpdateEvent(message="Searching articles...")

    results = await article_store.search(query)

    yield ProgressUpdateEvent(message=f"Found {len(results)} articles...")

    for i, article in enumerate(results):
        if i % 5 == 0:
            yield ProgressUpdateEvent(
                message=f"Processing article {i+1}/{len(results)}..."
            )

    return format_results(results)
```

### 4. Thread Lifecycle Events

Track thread changes for persistence and UI updates:

```typescript
const chatkit = useChatKit({
  api: { url: API_URL, domainKey: DOMAIN_KEY },

  onThreadChange: ({ threadId }) => {
    setThreadId(threadId);
    if (threadId) localStorage.setItem("lastThreadId", threadId);
    clearSelections();
  },

  onThreadLoadStart: ({ threadId }) => {
    setIsLoadingThread(true);
  },

  onThreadLoadEnd: ({ threadId }) => {
    setIsLoadingThread(false);
  },
});
```

### 5. Client Tools (State Query)

AI needs to read client-side state to make decisions:

**Backend - Defining Client Tool:**

```python
@function_tool(name_override="get_selected_items")
async def get_selected_items(ctx: AgentContext) -> dict:
    """Get the items currently selected on the canvas.

    This is a CLIENT TOOL - executed in browser, result comes back.
    """
    yield ProgressUpdateEvent(message="Reading selection...")
    pass  # Actual execution happens on client
```

**Frontend - Handling Client Tools:**

```typescript
const chatkit = useChatKit({
  api: { url: API_URL, domainKey: DOMAIN_KEY },

  onClientTool: ({ name, params }) => {
    switch (name) {
      case "get_selected_items":
        return { itemIds: selectedItemIds };

      case "get_current_viewport":
        return {
          center: mapRef.current.getCenter(),
          zoom: mapRef.current.getZoom(),
        };

      case "get_form_data":
        return { values: formRef.current.getValues() };

      default:
        throw new Error(`Unknown client tool: ${name}`);
    }
  },
});
```

---

## Client Effects vs Client Tools

| Type | Direction | Response Required | Use Case |
|------|-----------|-------------------|----------|
| **Client Effect** | Server → Client | No (fire-and-forget) | Update UI, show notifications |
| **Client Tool** | Server → Client → Server | Yes (return value) | Get client state for AI decision |

---

## Common Patterns by Use Case

### Interactive Map/Canvas

```typescript
onResponseStart: () => lockCanvas(),
onResponseEnd: () => unlockCanvas(),
onEffect: ({ name, data }) => {
  if (name === "add_marker") addMarker(data);
  if (name === "pan_to") panTo(data.location);
},
onClientTool: ({ name }) => {
  if (name === "get_selection") return getSelectedItems();
},
```

### Form-Based UI

```typescript
onResponseStart: () => setFormDisabled(true),
onResponseEnd: () => setFormDisabled(false),
onClientTool: ({ name }) => {
  if (name === "get_form_values") return form.getValues();
},
```

### Game/Simulation

```typescript
onResponseStart: () => pauseSimulation(),
onResponseEnd: () => resumeSimulation(),
onEffect: ({ name, data }) => {
  if (name === "update_entity") updateEntity(data);
  if (name === "show_notification") showToast(data.message);
},
```

---

## Thread Title Generation

Dynamically update thread title based on conversation:

```python
class TitleAgent:
    async def generate_title(self, first_message: str) -> str:
        result = await Runner.run(
            Agent(
                name="TitleGenerator",
                instructions="Generate a 3-5 word title.",
                model="gpt-4o-mini",  # Fast model
            ),
            input=f"First message: {first_message}",
        )
        return result.final_output

# In ChatKitServer
async def respond(self, thread, item, context):
    if not thread.title and item:
        title = await self.title_agent.generate_title(item.content)
        thread.title = title
        await self.store.save_thread(thread, context)
```

---

## Anti-Patterns

1. **Not locking UI during response** - Leads to race conditions
2. **Blocking in effects** - Effects should be fire-and-forget
3. **Heavy computation in onEffect** - Use requestAnimationFrame for DOM updates
4. **Missing error handling** - Always handle onError to unlock UI
5. **Not persisting thread state** - Use onThreadChange to save context

---

## Verification

Run: `python3 scripts/verify.py`

Expected: `✓ streaming-llm-responses skill ready`

## If Verification Fails

1. Check: references/ folder has streaming-patterns.md
2. **Stop and report** if still failing

## References

- [references/streaming-patterns.md](references/streaming-patterns.md) - Complete streaming configuration
