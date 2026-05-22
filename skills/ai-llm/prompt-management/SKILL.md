---
name: prompt-management
description: Centralized prompt management for LLM operations. All prompts in lib/prompts/ as named exports. Multi-level extraction, system builder, parameter injection. Triggers on "prompt", "LLM", "system prompt", "extraction", "operational prompt".
---

# Prompt Management

All LLM prompts centralized in `packages/backend/convex/lib/prompts/`. Never hardcode prompts in actions/routes. Always import from this directory.

## Directory Structure

```
convex/lib/prompts/
├── index.ts                    # Central export point
├── base.ts                     # Base system prompt
├── systemBuilder.ts            # Builds system message array
├── formatting.ts               # Memory formatting utilities
├── operational/                # Task-specific prompts
│   ├── memoryExtraction.ts     # Extract facts from conversations
│   ├── titleGeneration.ts      # Generate titles
│   ├── summarization.ts        # Summarize text
│   ├── tagExtraction.ts        # Auto-tag notes/tasks
│   ├── documentMode.ts         # Canvas mode prompt
│   └── ...
└── templates/                  # User-facing templates
    └── builtIn.ts
```

## Named Export Pattern

Every prompt MUST be a named export. Never inline strings.

```typescript
// From operational/titleGeneration.ts
export const CONVERSATION_TITLE_PROMPT = `Generate a 3-6 word title capturing the main topic of this conversation.

Rules:
- Focus on the core subject, not the request type
- Use natural language, avoid technical jargon unless central to the topic
- No quotes, periods, or special punctuation
- Title case (capitalize first letter of major words)

Return only the title text.`;

// From operational/summarization.ts
export const SUMMARIZATION_SYSTEM_PROMPT = `Summarize the provided text in 1-2 sentences. Focus on the key points. Be concise and direct.`;
```

**Usage in actions**:
```typescript
import { CONVERSATION_TITLE_PROMPT } from "../lib/prompts";

const result = await generateText({
  model,
  system: CONVERSATION_TITLE_PROMPT,
  prompt: conversationText,
});
```

## Builder Functions for Dynamic Prompts

When prompts need parameters, use builder functions:

```typescript
// From operational/tagExtraction.ts
export function buildAutoTagPrompt(
  content: string,
  existingTags: Array<{ displayName: string; usageCount: number }>,
): string {
  const tagsContext =
    existingTags.length > 0
      ? `YOUR EXISTING TAGS (${existingTags.length} total):
${existingTags.map((t) => `- ${t.displayName} (${t.usageCount}×)`).join("\n")}`
      : "No existing tags yet - create appropriate ones.";

  return `Auto-tag this content with 1-3 tags.

${tagsContext}

DECISION PROCESS:
1. First, check if ANY existing tag fits the content well
2. Prefer existing tags even if not a perfect match (80%+ fit = use it)
...

Return JSON: {"tags": ["tag1", "tag2"]}`;
}
```

**Pattern**: Accept all variable inputs as parameters, inject into template strings.

## Memory Extraction Levels

Four-level extraction system with thresholds:

```typescript
// From operational/memoryExtraction.ts
export type MemoryExtractionLevel =
  | "none"      // No extraction
  | "passive"   // Only explicit requests ("remember this")
  | "minimal"   // Core identity only (importance >= 8, confidence >= 0.8)
  | "moderate"  // Lasting traits (importance >= 7, confidence >= 0.7) [DEFAULT]
  | "active";   // Proactive inference (importance >= 5, confidence >= 0.6)

export const EXTRACTION_THRESHOLDS: Record<
  Exclude<MemoryExtractionLevel, "none">,
  { importance: number; confidence: number }
> = {
  passive: { importance: 9, confidence: 0.9 },
  minimal: { importance: 8, confidence: 0.8 },
  moderate: { importance: 7, confidence: 0.7 },
  active: { importance: 5, confidence: 0.6 },
};
```

**Usage**:
```typescript
export function buildMemoryExtractionPrompt(
  existingMemoriesText: string,
  conversationText: string,
  level: MemoryExtractionLevel = "moderate",
): string {
  if (level === "none") return "";

  const thresholds = EXTRACTION_THRESHOLDS[level];
  const basePrompt = buildBasePrompt(level, thresholds);

  return `${basePrompt}

## Existing Memories (Do NOT Duplicate)

${existingMemoriesText}

## Conversation

${conversationText}

Return JSON: {"facts": [{"content": "...", "category": "identity|preference|project|context|relationship", "importance": ${thresholds.importance}-10, "reasoning": "...", "confidence": ${thresholds.confidence}-1.0, "expirationHint": "contextual|preference|deadline|temporary"}]}

If nothing meets these criteria, return {"facts": []}.`;
}
```

Each level has different extraction criteria built by `buildPassivePrompt()`, `buildMinimalPrompt()`, `buildModeratePrompt()`, `buildActivePrompt()`.

## System Prompt Building

Multi-source system prompt builder with priority order:

```typescript
// From systemBuilder.ts
export async function buildSystemPrompts(
  ctx: ActionCtx,
  args: BuildSystemPromptsArgs,
): Promise<BuildSystemPromptsResult> {
  const systemMessages: ModelMessage[] = [];

  // 1. BASE IDENTITY (foundation)
  systemMessages.push({
    role: "system",
    content: getBasePrompt(basePromptOptions),
  });

  // 2. IDENTITY MEMORIES
  if (!isBlankSlate) {
    const identityMemories = await ctx.runQuery(
      internal.memories.search.getIdentityMemories,
      { userId, limit: 20 }
    );
    if (identityMemories.length > 0) {
      systemMessages.push({
        role: "system",
        content: `## Identity & Preferences\n\n${formatMemoriesByCategory(truncated)}`,
      });
    }
  }

  // 3. CONTEXTUAL MEMORIES (prefetched)
  if (prefetchedMemories && !isBlankSlate) {
    systemMessages.push({
      role: "system",
      content: `## Contextual Memories\n\n${prefetchedMemories}`,
    });
  }

  // 4. PROJECT CONTEXT
  if (conversation?.projectId && project?.systemPrompt) {
    systemMessages.push({
      role: "system",
      content: `## Project Context\n${project.systemPrompt}`,
    });
  }

  // 5. CONVERSATION-LEVEL SYSTEM PROMPT
  if (conversation?.systemPrompt) {
    systemMessages.push({
      role: "system",
      content: `## Conversation Instructions\n${conversation.systemPrompt}`,
    });
  }

  // 6. USER CUSTOM INSTRUCTIONS (HIGHEST PRIORITY - LAST)
  if (customInstructions?.enabled && !isBlankSlate) {
    systemMessages.push({
      role: "system",
      content: userPreferencesContent,
    });
  }

  return { messages: systemMessages, memoryContent };
}
```

**Key insight**: Later messages have higher priority (LLM recency bias). User preferences always last.

## Base System Prompt Pattern

Conditional sections based on model capabilities and user settings:

```typescript
// From base.ts
export function getBasePrompt(options: BasePromptOptions): string {
  const { modelConfig, hasFunctionCalling, customInstructions, memoryExtractionLevel } = options;

  // Check if user has custom tone
  const hasCustomTone =
    customInstructions?.enabled &&
    customInstructions?.baseStyleAndTone &&
    customInstructions.baseStyleAndTone !== "default";

  const capabilities = buildCapabilities(modelConfig, hasFunctionCalling);
  const memorySection = buildMemorySection(hasFunctionCalling, prefetchedMemories, memoryExtractionLevel);
  const toneSection = buildToneSection(!!hasCustomTone);
  const providerSection = getProviderOptimizations(modelConfig);

  return `<system>
  <identity>
    <name>blah.chat</name>
    ...
  </identity>

  <context>
    <model>${modelConfig.name}</model>
    <knowledge_cutoff>${knowledgeCutoff}</knowledge_cutoff>
    ...
  </context>

  <capabilities>
${capabilities}
  </capabilities>

${memorySection}

  <response_style>
${toneSection}
    ...
  </response_style>

${providerSection}
</system>`;
}
```

**Pattern**: Build sections conditionally, compose into single string.

## Prompt Categories

| Category | File | Purpose |
|----------|------|---------|
| Extraction | `operational/memoryExtraction.ts` | Extract facts (multi-level) |
| Generation | `operational/titleGeneration.ts` | Generate titles (conversation/note) |
| Formatting | `operational/summarization.ts` | Summarize text |
| Tagging | `operational/tagExtraction.ts` | Auto-tag with reuse priority |
| Mode-specific | `operational/documentMode.ts` | Canvas mode behavior |

## Central Export Pattern

Always export from `index.ts` for clean imports:

```typescript
// From index.ts
export { getBasePrompt } from "./base";
export { buildSystemPrompts } from "./systemBuilder";
export {
  CONVERSATION_TITLE_PROMPT,
  NOTE_TITLE_PROMPT
} from "./operational/titleGeneration";
export { buildMemoryExtractionPrompt } from "./operational/memoryExtraction";
export { buildAutoTagPrompt } from "./operational/tagExtraction";
```

**Usage**:
```typescript
// Clean import - single source
import {
  CONVERSATION_TITLE_PROMPT,
  buildMemoryExtractionPrompt,
  buildSystemPrompts
} from "../lib/prompts";
```

## Parameter Injection Patterns

### Simple Constant Injection
```typescript
export const NOTE_TITLE_PROMPT = `Generate a 3-8 word title capturing the main topic or purpose of this note.

Rules:
- Focus on what the note is about, not how it's written
- Use natural language
- No quotes, periods, or markdown formatting
- Title case

Return only the title text.`;
```

### Dynamic List Injection
```typescript
const tagsContext =
  existingTags.length > 0
    ? `YOUR EXISTING TAGS (${existingTags.length} total):
${existingTags.map((t) => `- ${t.displayName} (${t.usageCount}×)`).join("\n")}`
    : "No existing tags yet - create appropriate ones.";
```

### Threshold Injection
```typescript
// Inject threshold values directly into prompt
return `...
importance: ${thresholds.importance}-10
confidence: ${thresholds.confidence}-1.0
...`;
```

### Conditional Sections
```typescript
function buildToneSection(hasCustomTone: boolean): string {
  if (hasCustomTone) {
    return `    <tone>
      <!-- User has custom tone/style preferences - see user_preferences section below -->
      - Adapt to the user's explicitly configured style and tone preferences
    </tone>`;
  }

  return `    <tone>
      - Conversational, genuine, direct
      - Adapt to the user's style and energy
      ...
    </tone>`;
}
```

## Key Files

- `convex/lib/prompts/base.ts` - Base system prompt with capabilities
- `convex/lib/prompts/systemBuilder.ts` - Multi-source system prompt composition
- `convex/lib/prompts/operational/memoryExtraction.ts` - Four-level extraction
- `convex/lib/prompts/operational/titleGeneration.ts` - Simple constant exports
- `convex/lib/prompts/operational/tagExtraction.ts` - Parameter injection example
- `convex/lib/prompts/index.ts` - Central export point

## Anti-Patterns

**Never hardcode prompts in actions**:
```typescript
// ❌ BAD
const result = await generateText({
  model,
  system: "Generate a 3-6 word title...",
  prompt: text,
});

// ✅ GOOD
import { CONVERSATION_TITLE_PROMPT } from "../lib/prompts";

const result = await generateText({
  model,
  system: CONVERSATION_TITLE_PROMPT,
  prompt: text,
});
```

**Never inline builder logic**:
```typescript
// ❌ BAD
const prompt = `Extract facts...
${existingMemories.map(m => m.content).join("\n")}
...`;

// ✅ GOOD
import { buildMemoryExtractionPrompt } from "../lib/prompts";

const prompt = buildMemoryExtractionPrompt(
  existingMemoriesText,
  conversationText,
  "moderate"
);
```

**Never skip the index export**:
```typescript
// ❌ BAD - direct import from operational/
import { CONVERSATION_TITLE_PROMPT } from "../lib/prompts/operational/titleGeneration";

// ✅ GOOD - import from index
import { CONVERSATION_TITLE_PROMPT } from "../lib/prompts";
```
