---
name: system-prompt-builder
description: System prompt assembly for blah.chat AI backend. Multi-layer prompt construction with priority ordering, parallel context loading, memory truncation, budget awareness. Use when working with "system prompt", "base prompt", "identity memories", "custom instructions", "knowledge bank", "budget state", prompt ordering, or message assembly in Convex generation actions.
---

# System Prompt Builder

Backend system for assembling multi-layer AI system prompts with order-dependent priority. Located in `packages/backend/convex/lib/prompts/`.

## Priority Order (Critical)

**Later messages = higher priority** due to LLM recency bias.

Structure:
1. Base prompt (foundation)
2. Identity memories (10% context budget)
3. Contextual memories (prefetched for non-tool models)
4. Project context
5. Knowledge bank prompt
6. Budget awareness prompts
7. Document mode prompt
8. Conversation-level system prompt
9. **Custom instructions (HIGHEST - last)**

From `systemBuilder.ts`:

```typescript
// === 1. BASE IDENTITY (foundation) ===
systemMessages.push({
  role: "system",
  content: basePrompt,
});

// === 2. IDENTITY MEMORIES ===
systemMessages.push({
  role: "system",
  content: `## Identity & Preferences\n\n${memoryContentForTracking}`,
});

// ... 3-5 project/KB/budget prompts ...

// === 6. USER CUSTOM INSTRUCTIONS (HIGHEST PRIORITY - LAST) ===
const userPreferencesContent = `<user_preferences priority="highest">
## User Personalization Settings
**IMPORTANT**: These take absolute priority over default behavior.

${sections.join("\n\n")}
</user_preferences>`;

systemMessages.push({
  role: "system",
  content: userPreferencesContent,
});
```

## Parallel Context Loading

Load user, conversation, project data in parallel to minimize latency.

From `systemBuilder.ts`:

```typescript
// Parallelize context queries
const [user, conversation] = (await Promise.all([
  ctx.runQuery(internal.lib.helpers.getCurrentUser, {}),
  ctx.runQuery(internal.lib.helpers.getConversation, {
    id: args.conversationId,
  }),
])) as [Doc<"users"> | null, Doc<"conversations"> | null];
```

Do NOT load sequentially - use `Promise.all()`.

## Base Prompt Structure

Base prompt adapts based on:
- Model capabilities (vision, thinking, extended-thinking)
- Function calling support
- Custom instructions presence

From `base.ts`:

```typescript
export function getBasePrompt(options: BasePromptOptions): string {
  // Check if user has custom tone that should override defaults
  const hasCustomTone =
    customInstructions?.enabled &&
    customInstructions?.baseStyleAndTone &&
    customInstructions.baseStyleAndTone !== "default";

  // Build capabilities list
  const capabilities = buildCapabilities(modelConfig, hasFunctionCalling);

  // Build memory system section
  const memorySection = buildMemorySection(
    hasFunctionCalling,
    prefetchedMemories,
    memoryExtractionLevel,
  );

  return `<system>
  <identity>
    <name>blah.chat</name>
    <description>A personal AI assistant for thoughtful conversations.</description>
    ...
  </identity>

  <context>
    <model>${modelConfig.name}</model>
    <knowledge_cutoff>${knowledgeCutoff}</knowledge_cutoff>
    <current_date>${currentDate}</current_date>
  </context>

  <capabilities>
${capabilities}
  </capabilities>

${memorySection}

  <response_style>
${toneSection}
    ...
  </response_style>
</system>`;
}
```

### Conditional Tone Section

When user has custom tone, base prompt defers to their preferences:

```typescript
function buildToneSection(hasCustomTone: boolean): string {
  if (hasCustomTone) {
    return `    <tone>
      <!-- User has custom tone/style preferences -->
      - Adapt to user's explicitly configured style and tone preferences
      - User's custom instructions take absolute priority
    </tone>`;
  }

  // Default tone for users without custom preferences
  return `    <tone>
      - Conversational, genuine, direct
      - Adapt to user's style and energy
      - Avoid corporate/HR-speak ("I'd be happy to help!")
      ...
    </tone>`;
}
```

## Identity Memories

Load top 20 identity memories, truncate to 10% context budget.

From `systemBuilder.ts`:

```typescript
const identityMemories: Doc<"memories">[] = await ctx.runQuery(
  internal.memories.search.getIdentityMemories,
  {
    userId: args.userId,
    limit: 20,
  },
);

if (identityMemories.length > 0) {
  // Calculate 10% budget for identity memories
  const maxMemoryTokens = Math.floor(
    args.modelConfig.contextWindow * 0.1,
  );

  // Truncate by priority
  const truncated = truncateMemories(identityMemories, maxMemoryTokens);

  memoryContentForTracking = formatMemoriesByCategory(truncated);

  if (memoryContentForTracking) {
    systemMessages.push({
      role: "system",
      content: `## Identity & Preferences\n\n${memoryContentForTracking}`,
    });
  }
}
```

Skip for incognito blank slate mode:

```typescript
const isBlankSlate =
  conversation?.isIncognito &&
  conversation?.incognitoSettings?.applyCustomInstructions === false;

if (!isBlankSlate) {
  // Load identity memories
}
```

## Memory Truncation

Truncate memories by category priority to fit budget.

Priority order: `relationship` > `preference` > `identity` > `project` > `context`

From `formatting.ts`:

```typescript
export function truncateMemories(
  memories: Array<Doc<"memories">>,
  maxTokens: number,
): Array<Doc<"memories">> {
  const priorityOrder: MemoryCategory[] = [
    "relationship",
    "preference",
    "identity",
    "project",
    "context",
  ];

  const categorized = new Map<MemoryCategory, Array<Doc<"memories">>>();
  for (const mem of memories) {
    const cat = (mem.metadata?.category as MemoryCategory) || "context";
    if (!categorized.has(cat)) categorized.set(cat, []);
    categorized.get(cat)?.push(mem);
  }

  const result: Array<Doc<"memories">> = [];
  let estimatedTokens = 0;

  for (const category of priorityOrder) {
    const mems = categorized.get(category) || [];
    for (const mem of mems) {
      const tokens = estimateTokens(mem.content);
      if (estimatedTokens + tokens > maxTokens) break;
      result.push(mem);
      estimatedTokens += tokens;
    }
  }

  return result;
}
```

Format by category:

```typescript
export function formatMemoriesByCategory(
  memories: Array<Doc<"memories">>,
): string {
  const categorized: Record<MemoryCategory, string[]> = {
    relationship: [],
    preference: [],
    identity: [],
    project: [],
    context: [],
  };

  for (const mem of memories) {
    const cat = (mem.metadata?.category as MemoryCategory) || "context";
    categorized[cat].push(mem.content);
  }

  const sections: string[] = [];

  if (categorized.relationship.length) {
    sections.push(
      `### Relationships\n${categorized.relationship.map((m) => `- ${m}`).join("\n")}`,
    );
  }
  // ... other categories ...

  return `## Relevant Memories\n\n${sections.join("\n\n")}`;
}
```

## Custom Instructions Override

User custom instructions placed LAST for maximum priority.

From `systemBuilder.ts`:

```typescript
if (customInstructions?.enabled && !isBlankSlate) {
  const {
    aboutUser,
    responseStyle,
    baseStyleAndTone,
    nickname,
    occupation,
    moreAboutYou,
  } = customInstructions;

  const sections: string[] = [];

  // User identity
  const identityParts: string[] = [];
  if (nickname) identityParts.push(`Name: ${nickname}`);
  if (occupation) identityParts.push(`Role: ${occupation}`);
  if (identityParts.length > 0) {
    sections.push(`### User Identity\n${identityParts.join("\n")}`);
  }

  // About the user
  if (aboutUser || moreAboutYou) {
    const aboutSections: string[] = [];
    if (aboutUser) aboutSections.push(aboutUser);
    if (moreAboutYou) aboutSections.push(moreAboutYou);
    sections.push(`### About the User\n${aboutSections.join("\n\n")}`);
  }

  // Response style
  if (responseStyle) {
    sections.push(`### Response Style Instructions\n${responseStyle}`);
  }

  // Tone directive
  if (baseStyleAndTone && baseStyleAndTone !== "default") {
    const toneDescriptions: Record<string, string> = {
      professional: "Be polished and precise. Use formal language.",
      friendly: "Be warm and chatty. Use casual language.",
      // ... other tones
    };
    const toneDirective = toneDescriptions[baseStyleAndTone];
    if (toneDirective) {
      sections.push(`### Tone Directive\n${toneDirective}`);
    }
  }

  if (sections.length > 0) {
    const userPreferencesContent = `<user_preferences priority="highest">
## User Personalization Settings
**IMPORTANT**: These take absolute priority over default behavior.

${sections.join("\n\n")}

**Reminder**: Always honor these preferences.
</user_preferences>`;

    systemMessages.push({
      role: "system",
      content: userPreferencesContent,
    });
  }
}
```

## Knowledge Bank Prompt

Inject KB instructions for models with function calling.

From `systemBuilder.ts`:

```typescript
if (!isBlankSlate && args.hasFunctionCalling) {
  try {
    const hasKnowledge = (await (ctx.runQuery as any)(
      internal.knowledgeBank.index.hasKnowledge,
      { userId: args.userId },
    )) as boolean;

    const kbPrompt = getKnowledgeBankSystemPrompt(hasKnowledge);
    if (kbPrompt) {
      systemMessages.push({
        role: "system",
        content: kbPrompt,
      });
    }
  } catch (error) {
    logger.error("Failed to check knowledge bank", {
      tag: "KnowledgeBank",
      userId: args.userId,
      error: String(error),
    });
    // Continue without KB prompt (graceful degradation)
  }
}
```

## Budget State Awareness

Inject budget warnings when context is getting full.

From `systemBuilder.ts`:

```typescript
// === 4.3. BUDGET AWARENESS (Phase 3) ===
if (args.budgetState && isContextGettingFull(args.budgetState)) {
  systemMessages.push({
    role: "system",
    content: formatStatus(args.budgetState),
  });
}

// === 4.4. ASK USER SUGGESTION (Phase 3) ===
// Nudge AI to ask for clarification when stuck
if (args.budgetState && shouldSuggestAskUser(args.budgetState)) {
  const { searchHistory } = args.budgetState;
  const lowQualityCount = searchHistory.filter(
    (h) => h.topScore < LOW_QUALITY_SCORE_THRESHOLD,
  ).length;
  systemMessages.push({
    role: "system",
    content: `[Stuck Detection: ${lowQualityCount} low-quality searches. Use askForClarification tool to get user input instead of continuing to search.]`,
  });
}
```

## Document Mode (Canvas)

Special prompt for document editing mode.

From `systemBuilder.ts`:

```typescript
if (conversation?.mode === "document") {
  const { DOCUMENT_MODE_PROMPT } = await import("./index");
  systemMessages.push({
    role: "system",
    content: DOCUMENT_MODE_PROMPT,
  });
}
```

## Key Files

- `packages/backend/convex/lib/prompts/systemBuilder.ts` - Main assembly logic
- `packages/backend/convex/lib/prompts/base.ts` - Base prompt generation
- `packages/backend/convex/lib/prompts/formatting.ts` - Memory formatting/truncation
- `packages/backend/convex/lib/budgetTracker.ts` - Budget state helpers
- `packages/backend/convex/knowledgeBank/tool.ts` - KB prompt generation

## Anti-Patterns

**DON'T** load context sequentially - use `Promise.all()` for parallel loading.

**DON'T** place custom instructions early - they go LAST for highest priority.

**DON'T** skip incognito blank slate checks - respect user privacy settings.

**DON'T** exceed memory budget - always truncate to 10% context window.

**DON'T** forget graceful degradation - catch errors, continue without optional context.
