---
name: message-consolidation
description: Message consolidation and conversation compaction for blah.chat. Covers comparison consolidation (merging multi-model responses) and conversation compaction (summarizing long chats). Triggers on "consolidation", "consolidate", "merge messages", "compaction", "compact conversation", "comparison group", "context window".
---

# Message Consolidation

Two distinct features for managing message context:

1. **Comparison consolidation** - merge multiple model responses into one comprehensive response
2. **Conversation compaction** - summarize long conversations to create a new conversation with context

## Comparison Consolidation

Merge multiple assistant responses from model comparison into single consolidated response.

### Schema Fields

Messages table uses these fields:

```typescript
// From packages/backend/convex/schema/messages.ts
comparisonGroupId: v.optional(v.string()),
consolidatedMessageId: v.optional(v.id("messages")),
isConsolidation: v.optional(v.boolean()),
```

When consolidation happens:
- Original responses get `consolidatedMessageId` pointing to merged message
- New message gets `isConsolidation: true`
- Original messages remain in DB but hidden from UI

### Consolidation Flow

Two mutation patterns in `packages/backend/convex/conversations/consolidation.ts`:

**Pattern 1: New conversation**

```typescript
// createConsolidationConversation - creates separate conversation with consolidated response
export const createConsolidationConversation = mutation({
  args: {
    comparisonGroupId: v.string(),
    consolidationModel: v.string(),
  },
  handler: async (ctx, args) => {
    // 1. Fetch all messages in comparison group
    const allMessages = await ctx.db
      .query("messages")
      .withIndex("by_comparison_group", (q) =>
        q.eq("comparisonGroupId", args.comparisonGroupId)
      )
      .collect();

    // 2. Separate user message and assistant responses
    const userMessage = allMessages.find((m) => m.role === "user");
    const responses = allMessages.filter((m) => m.role === "assistant");

    // 3. Build consolidation prompt
    const modelList = responses.map((r) => r.model || "unknown").join(", ");
    let consolidationPrompt = `Here are ${responses.length} responses from ${modelList} about:\n\n`;
    consolidationPrompt += `**Original prompt:** "${userMessage.content}"\n\n`;

    for (const r of responses) {
      consolidationPrompt += `**Response from ${r.model || "unknown"}:**\n${r.content}\n\n`;
    }

    consolidationPrompt += "Can you consolidate all of this information...";

    // 4. Create new conversation with consolidated prompt as user message
    // 5. Schedule generation action
  }
});
```

**Pattern 2: Same conversation**

```typescript
// consolidateInSameChat - adds consolidated message to existing conversation
export const consolidateInSameChat = mutation({
  args: {
    conversationId: v.id("conversations"),
    comparisonGroupId: v.string(),
    consolidationModel: v.string(),
  },
  handler: async (ctx, args) => {
    // Same message fetching + prompt building as Pattern 1

    // Insert pending consolidated assistant message (NO comparisonGroupId)
    const consolidatedMessageId = await ctx.db.insert("messages", {
      conversationId: args.conversationId,
      userId: user._id,
      role: "assistant",
      content: "",
      status: "pending",
      model: args.consolidationModel,
      isConsolidation: true, // Mark as consolidated
      createdAt: Date.now(),
      updatedAt: Date.now(),
    });

    // Link comparison messages to consolidated message
    for (const response of responses) {
      await ctx.db.patch(response._id, {
        consolidatedMessageId, // Hides original from UI
      });
    }

    // Schedule generation with consolidation prompt as systemPromptOverride
    await ctx.scheduler.runAfter(0, internal.generation.generateResponse, {
      conversationId: args.conversationId,
      existingMessageId: consolidatedMessageId,
      modelId: args.consolidationModel,
      userId: user._id,
      systemPromptOverride: consolidationPrompt, // Key difference
    });
  }
});
```

### Prompt Building

Reusable helper in `apps/web/src/lib/consolidation.ts`:

```typescript
export function buildConsolidationPrompt(
  originalPrompt: string,
  responses: Array<{ model: string; content: string }>,
): string {
  const modelList = responses.map((r) => r.model).join(", ");

  let prompt = `Here are ${responses.length} responses from ${modelList} about:\n\n`;
  prompt += `**Original prompt:** "${originalPrompt}"\n\n`;

  for (const r of responses) {
    prompt += `**Response from ${r.model}:**\n${r.content}\n\n`;
  }

  prompt += "Can you consolidate all of this information into one comprehensive, well-organized response? Identify common themes, reconcile any differences, and synthesize the best insights from each response.";

  return prompt;
}
```

### UI Filtering

`apps/web/src/hooks/useMessageGrouping.ts` filters consolidated messages from display:

```typescript
export function useMessageGrouping(messages: MessageWithUser[]): GroupedItem[] {
  const visibleMessages = messages.filter(
    (m) => !(m.role === "assistant" && m.consolidatedMessageId)
  );

  // Group by comparisonGroupId for comparison UI
  // Return consolidated message or individual messages
}
```

## Conversation Compaction

Summarize long conversation to create new conversation with recap. Reduces context window usage.

### Minimum Message Threshold

From `packages/backend/convex/constants.ts`:

```typescript
/**
 * Minimum number of messages required before a conversation can be compacted.
 * Used to prevent compacting conversations that are too short to benefit.
 */
export const MIN_MESSAGES_FOR_COMPACTION = 3;
```

**Check before offering compaction**:

```typescript
// In ConversationHeaderMenu.tsx
const messages = useQuery(api.messages.list, { conversationId });

const canCompact =
  messages &&
  messages.length >= MIN_MESSAGES_FOR_COMPACTION;
```

### Compaction Action

From `packages/backend/convex/conversations/compact.ts`:

```typescript
export const compact = action({
  args: {
    conversationId: v.id("conversations"),
    targetModel: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const messages = await ctx.runQuery(internal.messages.listInternal, {
      conversationId: args.conversationId,
    });

    if (messages.length < MIN_MESSAGES_FOR_COMPACTION) {
      throw new Error("Conversation too short to compact");
    }

    // Filter to only complete messages
    const completeMessages = messages.filter((m) => m.status === "complete");

    // Build transcript (max 16000 chars)
    const transcript = completeMessages
      .map((m) => `${m.role === "user" ? "User" : "Assistant"}: ${m.content}`)
      .join("\n\n");

    const truncatedTranscript = transcript.slice(0, 16000);

    // Generate summary using operational model
    const result = await generateText({
      model: getModel(SUMMARIZATION_MODEL.id),
      system: CONVERSATION_COMPACTION_PROMPT,
      prompt: buildCompactionPrompt(truncatedTranscript),
      temperature: 0.7,
    });

    // Create new conversation
    const newConversationId = await ctx.runMutation(
      internal.conversations.createInternal,
      {
        userId: user._id,
        model: args.targetModel || conversation.model,
        title: `${conversation.title} (continued)`,
      }
    );

    // Insert summary as first assistant message
    await ctx.runMutation(internal.messages.create, {
      conversationId: newConversationId,
      role: "assistant",
      content: `**Recap from previous conversation:**\n\n${summary}`,
      status: "complete",
      model: args.targetModel || conversation.model,
    });

    return { conversationId: newConversationId };
  },
});
```

### Compaction Prompt

From `packages/backend/convex/lib/prompts/operational/conversationCompaction.ts`:

```typescript
export const CONVERSATION_COMPACTION_PROMPT = `Summarize this conversation for context continuity. Your summary will be used as the starting point for a new conversation, so preserve all important context.

Include:
- Key topics discussed and their outcomes
- Important decisions made or conclusions reached
- Unresolved questions or pending items
- Critical facts, names, and entities mentioned
- User preferences or requirements expressed

Format as a clear, organized recap. Be comprehensive but concise.`;

export function buildCompactionPrompt(transcript: string): string {
  return `Summarize this conversation:\n\n${transcript}`;
}
```

### Model Used

Always use operational model (cheap, fast):

```typescript
// From packages/backend/convex/lib/ai/operational-models.ts
import { SUMMARIZATION_MODEL } from "@/lib/ai/operational-models";

const result = await generateText({
  model: getModel(SUMMARIZATION_MODEL.id), // gpt-4o-mini
  // ...
});
```

Track usage for compaction operation separately from chat generation.

### UI Integration

From `apps/web/src/components/chat/ConversationHeaderMenu.tsx`:

```typescript
const compactConversation = useAction(api.conversations.compact.compact);
const messages = useQuery(api.messages.list, { conversationId });

const handleCompactConversation = async () => {
  setIsCompacting(true);
  try {
    const { conversationId } = await compactConversation({
      conversationId: conversation._id,
      targetModel: conversation.model,
    });
    toast.success("Conversation compacted!");
    router.push(`/chat/${conversationId}`); // Navigate to new conversation
  } catch (_error) {
    toast.error("Failed to compact conversation");
  } finally {
    setIsCompacting(false);
  }
};

// In menu
<DropdownMenuItem
  onClick={handleCompactConversation}
  disabled={!messages || messages.length < MIN_MESSAGES_FOR_COMPACTION || isCompacting}
>
  <Shrink className="mr-2 h-4 w-4" />
  {isCompacting ? "Compacting..." : "Compact conversation"}
</DropdownMenuItem>
```

## Key Files

- `packages/backend/convex/conversations/consolidation.ts` - Comparison consolidation mutations
- `packages/backend/convex/conversations/compact.ts` - Conversation compaction action
- `packages/backend/convex/lib/prompts/operational/conversationCompaction.ts` - Compaction prompts
- `apps/web/src/lib/consolidation.ts` - Consolidation prompt builder
- `apps/web/src/hooks/useMessageGrouping.ts` - Filters consolidated messages from UI
- `packages/backend/convex/schema/messages.ts` - Schema with consolidation fields
- `packages/backend/convex/constants.ts` - MIN_MESSAGES_FOR_COMPACTION constant
- `apps/web/src/components/chat/ConversationHeaderMenu.tsx` - Compaction UI

## Important Distinctions

**Comparison consolidation**:
- Merges multiple responses from SAME user prompt
- Uses comparison group ID to link messages
- Original messages hidden via `consolidatedMessageId` field
- LLM synthesizes responses into comprehensive answer
- Happens in same or new conversation

**Conversation compaction**:
- Summarizes ENTIRE conversation history
- Creates NEW conversation with recap as first message
- Original conversation unchanged
- LLM produces context-preserving summary
- Always creates new conversation (user navigates to it)

**Never confuse the two** - they solve different problems (model comparison vs context window management).
