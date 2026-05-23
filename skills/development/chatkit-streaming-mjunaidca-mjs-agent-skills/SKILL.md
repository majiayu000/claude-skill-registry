---
name: chatkit-streaming
description: Implements real-time streaming UI patterns for ChatKit applications. This skill should be used when adding response lifecycle management, progress indicators, client effects, and thread state synchronization. Covers onResponseStart/End, onEffect, ProgressUpdateEvent, and thread lifecycle events.
---

# ChatKit Streaming Skill

## Overview

This skill provides patterns for building responsive, real-time ChatKit interfaces. It covers the streaming layer between basic integration and full interactive widgets - making the UI feel alive during AI responses.

## Core Concepts

### Response Lifecycle

ChatKit streams responses in real-time. The lifecycle:

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

### Client Effects vs Client Tools

| Type | Direction | Response Required | Use Case |
|------|-----------|-------------------|----------|
| **Client Effect** | Server → Client | No (fire-and-forget) | Update UI state, show notifications |
| **Client Tool** | Server → Client → Server | Yes (return value) | Get client state for AI decision |

## Implementation Patterns

### Pattern 1: Response Lifecycle Handlers

**When**: Lock UI during AI response, show loading states, prevent race conditions

**Frontend Implementation**:
```typescript
import { useChatKit } from "@openai/chatkit-react";

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

    onReady: () => {
      console.log("ChatKit initialized");
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

**Evidence**: `metro-map/frontend/src/components/ChatKitPanel.tsx:205-210`

### Pattern 2: Client Effects (Fire-and-Forget)

**When**: Server needs to update client UI without expecting a response

**Backend - Streaming Effects**:
```python
from chatkit.types import ClientEffectEvent

async def respond(self, thread, item, context):
    # ... agent processing ...

    # Fire client effect to update UI
    yield ClientEffectEvent(
        name="update_cat_status",
        data={
            "state": {"energy": 80, "happiness": 90},
            "flash": "Cat is now happy!"
        }
    )

    # Another effect - speech bubble
    yield ClientEffectEvent(
        name="cat_say",
        data={"message": "Meow!"}
    )
```

**Frontend - Handling Effects**:
```typescript
const chatkit = useChatKit({
  api: { url: API_URL, domainKey: DOMAIN_KEY },

  onEffect: ({ name, data }) => {
    switch (name) {
      case "update_cat_status":
        const catState = data.state as CatStatePayload;
        applyCatUpdate(catState);
        if (data.flash) {
          setFlashMessage(data.flash as string);
        }
        break;

      case "cat_say":
        setSpeech({ message: String(data.message) });
        break;

      case "location_select_mode":
        setLocationSelectLineId(data.lineId as string);
        break;

      case "add_station":
        clearLocationSelectMode();
        if (data.map) setMap(data.map as MetroMap);
        if (data.stationId) {
          requestAnimationFrame(() => focusStation(data.stationId));
        }
        break;
    }
  },
});
```

**Evidence**:
- `cat-lounge/backend/app/cat_agent.py` (server-side effects)
- `cat-lounge/frontend/src/components/ChatKitPanel.tsx:86-103` (frontend handler)
- `metro-map/frontend/src/components/ChatKitPanel.tsx:130-153`

### Pattern 3: Progress Updates

**When**: Show "Searching...", "Loading...", "Analyzing..." during long operations

**Backend - Streaming Progress**:
```python
from chatkit.types import ProgressUpdateEvent

@function_tool
async def search_articles(ctx: AgentContext, query: str) -> str:
    """Search for articles matching the query."""

    # Show progress to user
    yield ProgressUpdateEvent(message="Searching articles...")

    results = await article_store.search(query)

    yield ProgressUpdateEvent(message=f"Found {len(results)} articles...")

    # Process results
    for i, article in enumerate(results):
        if i % 5 == 0:
            yield ProgressUpdateEvent(
                message=f"Processing article {i+1}/{len(results)}..."
            )
        # ... process article

    return format_results(results)
```

**Evidence**:
- `news-guide/backend/app/agents/news_agent.py` (search tools with progress)
- `metro-map/backend/app/agents/metro_map_agent.py` (get_map progress)

### Pattern 4: Thread Lifecycle Events

**When**: Track thread changes, persist thread state, update UI on thread switch

**Frontend Implementation**:
```typescript
const chatkit = useChatKit({
  api: { url: API_URL, domainKey: DOMAIN_KEY },

  onThreadChange: ({ threadId }) => {
    console.log("Thread changed to:", threadId);
    setThreadId(threadId);

    // Persist last active thread
    if (threadId) {
      localStorage.setItem("lastThreadId", threadId);
    }

    // Clear thread-specific UI state
    clearSelections();
  },

  onThreadLoadStart: ({ threadId }) => {
    console.log("Loading thread:", threadId);
    setIsLoadingThread(true);
  },

  onThreadLoadEnd: ({ threadId }) => {
    console.log("Thread loaded:", threadId);
    setIsLoadingThread(false);
  },
});
```

### Pattern 5: Client Tools (State Query)

**When**: AI needs to read client-side state to make decisions

**Backend - Defining Client Tool**:
```python
@function_tool(name_override="get_selected_stations")
async def get_selected_stations(ctx: AgentContext) -> dict:
    """Get the stations currently selected on the canvas.

    This is a CLIENT TOOL - it will be executed in the browser.
    The result comes back from the frontend.
    """
    # Progress while waiting for client response
    yield ProgressUpdateEvent(message="Reading selected stations...")

    # The actual execution happens on the client
    # Return type indicates expected response shape
    pass
```

**Frontend - Handling Client Tools**:
```typescript
const chatkit = useChatKit({
  api: { url: API_URL, domainKey: DOMAIN_KEY },

  onClientTool: ({ name, params }) => {
    switch (name) {
      case "get_selected_stations":
        // Return current selection to the AI
        return { stationIds: selectedStationIds };

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

**Evidence**: `metro-map/frontend/src/components/ChatKitPanel.tsx:119-128`

### Pattern 6: Streaming with Thread Title Updates

**When**: Dynamically update thread title based on conversation

**Backend - Title Agent Pattern**:
```python
from chatkit.types import ThreadMetadata

class TitleAgent:
    """Generates concise thread titles from conversation."""

    async def generate_title(
        self,
        first_message: str,
        context: str = ""
    ) -> str:
        # Use a fast model for title generation
        result = await Runner.run(
            Agent(
                name="TitleGenerator",
                instructions="Generate a 3-5 word title for this conversation.",
                model="gpt-4o-mini",
            ),
            input=f"Context: {context}\nFirst message: {first_message}",
        )
        return result.final_output

# In ChatKitServer
async def respond(self, thread: ThreadMetadata, item, context):
    # Generate title on first message
    if not thread.title and item:
        title = await self.title_agent.generate_title(item.content)
        thread.title = title
        await self.store.save_thread(thread, context)

    # ... rest of response handling
```

**Evidence**:
- `news-guide/backend/app/agents/title_agent.py`
- `metro-map/backend/app/agents/title_agent.py`

## Configuration Options

### Streaming-Related useChatKit Options

```typescript
const chatkit = useChatKit({
  api: { url, domainKey },

  // === Lifecycle Events ===
  onReady: () => void,                    // ChatKit initialized
  onError: ({ error }) => void,           // Error occurred
  onResponseStart: () => void,            // AI started responding
  onResponseEnd: () => void,              // AI finished responding

  // === Thread Events ===
  onThreadChange: ({ threadId }) => void, // Thread switched
  onThreadLoadStart: ({ threadId }) => void,
  onThreadLoadEnd: ({ threadId }) => void,

  // === Client Interaction ===
  onEffect: ({ name, data }) => void,     // Server sent effect
  onClientTool: ({ name, params }) => any, // AI requests client state

  // === Logging ===
  onLog: ({ name, data }) => void,        // Analytics events
});
```

## Common Patterns by Use Case

### Interactive Map/Canvas

```typescript
// Lock during response, handle effects for state sync
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
// Disable form during response, sync form state
onResponseStart: () => setFormDisabled(true),
onResponseEnd: () => setFormDisabled(false),
onClientTool: ({ name }) => {
  if (name === "get_form_values") return form.getValues();
},
```

### Game/Simulation

```typescript
// Pause game during response, handle state updates
onResponseStart: () => pauseSimulation(),
onResponseEnd: () => resumeSimulation(),
onEffect: ({ name, data }) => {
  if (name === "update_entity") updateEntity(data);
  if (name === "show_notification") showToast(data.message);
},
```

## Anti-Patterns to Avoid

1. **Not locking UI during response** - Leads to race conditions
2. **Blocking effects** - Effects should be fire-and-forget, not awaited
3. **Heavy computation in onEffect** - Use requestAnimationFrame for DOM updates
4. **Missing error handling** - Always handle onError to unlock UI
5. **Not persisting thread state** - Use onThreadChange to save context

## References

- `references/complete-frontend-config.tsx` - Complete useChatKit configuration with all streaming handlers
- `references/client-effects.md` - Effect catalog and examples
- `references/client-tools.md` - Client tool implementation patterns

## Evidence Sources

All patterns derived from OpenAI ChatKit advanced samples:
- `blueprints/openai-chatkit-advanced-samples-main/examples/cat-lounge/`
- `blueprints/openai-chatkit-advanced-samples-main/examples/metro-map/`
- `blueprints/openai-chatkit-advanced-samples-main/examples/news-guide/`
