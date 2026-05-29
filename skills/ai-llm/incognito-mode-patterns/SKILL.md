---
name: incognito-mode-patterns
description: Incognito mode patterns for ephemeral conversations with blank slate option. Controls tool access (write tools always disabled, read tools configurable), custom instruction application, and inactivity auto-cleanup. Triggers on "incognito", "ephemeral", "blank slate", "private mode", "no memory", "read tools", "write tools", "custom instructions", "incognito settings", "inactivity timeout".
---

# Incognito Mode Patterns

Incognito conversations provide ephemeral, privacy-focused chat sessions with configurable tool access and optional blank slate mode (skips memories and custom instructions).

## Core Behavior

**Always disabled in incognito:**
- Write tools: saveMemory, deleteMemory, manageTasks
- Canvas/Document mode tools

**Configurable in incognito:**
- Read tools: search (files, notes, tasks, history, memories, knowledge bank)
- Custom instructions application
- Memory injection

## Schema Structure

### Conversation Table Fields

```typescript
// From conversations.ts:30-36
isIncognito: v.optional(v.boolean()),
incognitoSettings: v.optional(
  v.object({
    enableReadTools: v.optional(v.boolean()),
    applyCustomInstructions: v.optional(v.boolean()),
    inactivityTimeoutMinutes: v.optional(v.number()),
  }),
),
```

### Creation Pattern

```typescript
// From conversations.ts:57-67
...(args.isIncognito && {
  isIncognito: true,
  incognitoSettings: {
    enableReadTools: args.incognitoSettings?.enableReadTools ?? true,
    applyCustomInstructions:
      args.incognitoSettings?.applyCustomInstructions ?? true,
    inactivityTimeoutMinutes:
      args.incognitoSettings?.inactivityTimeoutMinutes,
    lastActivityAt: now,
  },
}),
```

**Default behavior**: Read tools enabled, custom instructions applied unless explicitly disabled.

## Tool Filtering Logic

### Write Tools: Always Disabled

```typescript
// From tools.ts:167-210
// Write tools: DISABLED for incognito
if (!isIncognito) {
  // Memory write tools
  if (enableMemoryWriteTools) {
    tools.saveMemory = createMemorySaveTool(ctx, userId);
    if (memoryExtractionLevel !== "passive") {
      tools.deleteMemory = createMemoryDeleteTool(ctx, userId);
    }
  }

  // Task manager
  tools.manageTasks = createTaskManagerTool(ctx, userId, conversation?.projectId);

  // Document mode tools
  tools.enterDocumentMode = createEnterDocumentModeTool(ctx, conversationId);
  if (isDocumentMode) {
    tools.exitDocumentMode = createExitDocumentModeTool(ctx, conversationId);
    tools.createDocument = createDocumentTool(ctx, userId, conversationId);
    tools.updateDocument = createUpdateDocumentTool(ctx, userId, conversationId);
    tools.readDocument = createReadDocumentTool(ctx, userId, conversationId);
    tools.resolveConflict = createResolveConflictTool(ctx, userId, conversationId);
  }
}
```

### Read Tools: Configurable

```typescript
// From tools.ts:86-97
const isIncognito = conversation?.isIncognito ?? false;
const incognitoSettings = conversation?.incognitoSettings;
const enableReadTools = !isIncognito || incognitoSettings?.enableReadTools !== false;

// Memory tool settings based on extraction level
const enableMemoryWriteTools = !isIncognito && memoryExtractionLevel !== "none";
const enableMemoryReadTools = enableReadTools && memoryExtractionLevel !== "none";
```

```typescript
// From tools.ts:212-238
// Read tools: Configurable for incognito (search user data)
if (enableReadTools) {
  // Memory search: respects extraction level
  if (enableMemoryReadTools) {
    tools.searchMemories = createMemorySearchTool(ctx, userId);
  }

  // Other search tools
  tools.searchFiles = createSearchFilesTool(ctx, userId);
  tools.searchNotes = createSearchNotesTool(ctx, userId);
  tools.searchTasks = createSearchTasksTool(ctx, userId);
  tools.queryHistory = createQueryHistoryTool(ctx, userId, conversationId);
  tools.searchAll = createSearchAllTool(ctx, userId, conversationId, searchCache, budgetState);
  tools.searchKnowledgeBank = createSearchKnowledgeBankTool(ctx, userId, conversation?.projectId);
}
```

**Logic**: `enableReadTools` defaults to `true` unless explicitly set to `false` via `incognitoSettings.enableReadTools`.

### Capability Tools: Always Available

Stateless tools (calculator, datetime, web search, URL reader, code execution, weather, YouTube, file docs) are always enabled regardless of incognito mode.

## Blank Slate Mode

Skip memories and custom instructions when `applyCustomInstructions: false`.

```typescript
// From systemBuilder.ts:59-62
const isBlankSlate =
  conversation?.isIncognito &&
  conversation?.incognitoSettings?.applyCustomInstructions === false;
```

### Skipped Sections

```typescript
// From systemBuilder.ts:95-133
// === 2. IDENTITY MEMORIES ===
// Skip for incognito blank slate mode
if (!isBlankSlate) {
  const identityMemories = await ctx.runQuery(
    internal.memories.search.getIdentityMemories,
    { userId: args.userId, limit: 20 }
  );
  // ... format and inject
}
```

```typescript
// From systemBuilder.ts:135-142
// === 3. CONTEXTUAL MEMORIES ===
// Skip for incognito blank slate mode
if (args.prefetchedMemories && !isBlankSlate) {
  systemMessages.push({
    role: "system",
    content: `## Contextual Memories\n\n${args.prefetchedMemories}`,
  });
}
```

```typescript
// From systemBuilder.ts:160-186
// === 4.25. KNOWLEDGE BANK ===
// Skip for incognito blank slate mode
if (!isBlankSlate && args.hasFunctionCalling) {
  const hasKnowledge = await ctx.runQuery(
    internal.knowledgeBank.index.hasKnowledge,
    { userId: args.userId }
  );
  const kbPrompt = getKnowledgeBankSystemPrompt(hasKnowledge);
  if (kbPrompt) {
    systemMessages.push({ role: "system", content: kbPrompt });
  }
}
```

```typescript
// From systemBuilder.ts:227-304
// === 6. USER CUSTOM INSTRUCTIONS ===
// Skip for incognito blank slate mode
if (customInstructions?.enabled && !isBlankSlate) {
  // ... build and inject user preferences
}
```

**Effect**: Blank slate mode provides completely fresh AI behavior without personalization or history context.

## Inactivity Timeout

Optional auto-cleanup for incognito conversations.

### Field Structure

```typescript
incognitoSettings: {
  inactivityTimeoutMinutes?: number;  // Optional timeout in minutes
  lastActivityAt: number;             // Timestamp of last activity
}
```

**Implementation**: Set during creation, updated on message activity. Cleanup logic runs via scheduled job (not shown in provided files but referenced in schema).

## Usage Patterns

### Standard Incognito (Read Tools Enabled)

```typescript
await ctx.runMutation(api.conversations.create, {
  model: "openai:gpt-5-mini",
  isIncognito: true,
  incognitoSettings: {
    enableReadTools: true,          // Can search files/notes/tasks
    applyCustomInstructions: true,  // Apply user preferences
  },
});
```

**Tools**: Web search, URL reader, code execution + file/note/task/history search. No writes.

### Strict Incognito (Read Tools Disabled)

```typescript
await ctx.runMutation(api.conversations.create, {
  model: "openai:gpt-5-mini",
  isIncognito: true,
  incognitoSettings: {
    enableReadTools: false,         // No data access
    applyCustomInstructions: true,  // Still apply preferences
  },
});
```

**Tools**: Only capability tools (web search, calculator, datetime, URL reader, code execution). No data access.

### Blank Slate Mode

```typescript
await ctx.runMutation(api.conversations.create, {
  model: "openai:gpt-5-mini",
  isIncognito: true,
  incognitoSettings: {
    enableReadTools: false,              // No data access
    applyCustomInstructions: false,      // Skip memories + custom instructions
    inactivityTimeoutMinutes: 60,        // Auto-delete after 1 hour of inactivity
  },
});
```

**Tools**: Only capability tools. **System prompt**: Skips identity memories, contextual memories, knowledge bank, and custom instructions. Fully anonymous.

## Key Files

- `packages/backend/convex/conversations.ts` - Schema + creation mutation (lines 30-112)
- `packages/backend/convex/generation/tools.ts` - Tool filtering logic (lines 42-241)
- `packages/backend/convex/lib/prompts/systemBuilder.ts` - Blank slate prompt filtering (lines 59-304)

## Anti-Patterns

**Don't assume incognito = no read tools**. Default is `enableReadTools: true`. Must explicitly set to `false` for strict privacy.

**Don't confuse blank slate with incognito**. Incognito only controls tool access. Blank slate (`applyCustomInstructions: false`) controls system prompt personalization.

**Don't use incognito for temporary chats**. Use `inactivityTimeoutMinutes` for auto-cleanup. Otherwise incognito conversations persist like normal ones.

**Don't expose write tools in incognito UI**. Backend enforces this but frontend must not offer task creation, memory saving, or canvas tools when `isIncognito: true`.
