---
name: canvas-ai-tools
description: Implements AI tools for Canvas generation and updates. Use when creating GenUI tools for code generation, document editing, or Canvas interactions.
allowed-tools: Read, Write, Edit, Glob
context: fork
---

# Canvas AI Tools Skill

## When to Use

Use this skill when:

- Creating AI tools that generate Canvas content
- Implementing code generation/editing tools
- Building GenUI tools for Canvas interaction
- Adding AI-powered features to Canvas

## GenUI Tool Architecture

```
lib/ai/tools/           # Tool definitions
├── canvas-tools.ts     # open_canvas, update_canvas, etc.
├── code-tools.ts       # run_code, explain_code
└── index.ts            # Registry

lib/ai/genui/           # UI components for tools
├── canvas-genui.tsx    # Canvas generation UI
└── code-result.tsx     # Code execution results
```

## Canvas Tool Definitions

### open_canvas Tool

```typescript
import { z } from 'zod';
import { tool } from 'ai';
import { CANVAS_TYPES, CanvasConfigSchema } from '@/lib/canvas/types';

export const openCanvasTool = tool({
  description: `Opens an interactive canvas for code editing, visualization, or document creation.

  Use this when the student needs to:
  - Write, edit, or run code
  - Create visualizations
  - Work on documents
  - Practice with interactive exercises

  The canvas provides a Monaco editor with syntax highlighting and execution support.`,

  parameters: z.object({
    type: z.enum(CANVAS_TYPES).describe('Type of canvas to open'),
    title: z.string().max(100).describe('Title for the canvas'),
    language: z.string().optional().describe('Programming language (for code type)'),
    initialContent: z.string().optional().describe('Starting content'),
    generationPrompt: z.string().optional().describe('Internal prompt for generation'),
    educationalContext: z.object({
      topic: z.string().optional(),
      difficulty: z.enum(['beginner', 'intermediate', 'advanced']).optional(),
      learningObjective: z.string().optional(),
    }).optional(),
  }),

  execute: async (args) => {
    // Validate with full schema
    const config = CanvasConfigSchema.parse(args);

    return {
      action: 'open_canvas' as const,
      canvasConfig: config,
    };
  },
});
```

### update_canvas Tool

```typescript
export const updateCanvasTool = tool({
  description: `Updates the content of the currently open canvas.

  Use this when:
  - Fixing errors in student code
  - Adding examples or explanations
  - Modifying existing content based on student request

  Only updates specified fields, preserving others.`,

  parameters: z.object({
    content: z.string().optional().describe('New content for the canvas'),
    title: z.string().max(100).optional().describe('New title'),
    language: z.string().optional().describe('Change programming language'),
  }),

  execute: async (args) => {
    return {
      action: 'update_canvas' as const,
      updates: args,
    };
  },
});
```

### run_code Tool

```typescript
export const runCodeTool = tool({
  description: `Executes the current code in the canvas and returns the result.

  Supports:
  - Python (via Pyodide)
  - JavaScript/TypeScript (via iframe sandbox)
  - HTML/CSS (preview)

  Returns output, errors, and execution time.`,

  parameters: z.object({
    includeVariables: z.boolean().optional().describe('Include final variable values'),
  }),

  execute: async (args) => {
    return {
      action: 'run_code' as const,
      options: args,
    };
  },
});
```

## Tool Registry Pattern

### Registering Canvas Tools

```typescript
// lib/ai/tools/registry.ts
import { openCanvasTool, updateCanvasTool, runCodeTool } from './canvas-tools';

export const CANVAS_TOOLS = {
  open_canvas: openCanvasTool,
  update_canvas: updateCanvasTool,
  run_code: runCodeTool,
} as const;

// For AI SDK
export const canvasToolsArray = Object.values(CANVAS_TOOLS);
```

### Using in Chat

```typescript
import { streamText } from 'ai';
import { CANVAS_TOOLS } from '@/lib/ai/tools/registry';

const result = await streamText({
  model,
  messages,
  tools: CANVAS_TOOLS,
  maxToolRoundtrips: 3,
});
```

## GenUI Component Pattern

### Tool Result Rendering

```tsx
// lib/ai/genui/canvas-genui.tsx
'use client';

import { useEffect } from 'react';
import { useCanvasStore } from '@/stores/canvas-store';
import type { OpenCanvasResult, UpdateCanvasResult } from '@/lib/canvas/types';

interface CanvasGenUIProps {
  toolResult: OpenCanvasResult | UpdateCanvasResult;
}

export function CanvasGenUI({ toolResult }: CanvasGenUIProps) {
  const { openCanvas, updateCanvas } = useCanvasStore();

  useEffect(() => {
    if (toolResult.action === 'open_canvas') {
      openCanvas(toolResult.canvasConfig);
    } else if (toolResult.action === 'update_canvas') {
      updateCanvas(toolResult.updates);
    }
  }, [toolResult, openCanvas, updateCanvas]);

  // Return minimal UI - canvas opens in side panel
  return (
    <div className="flex items-center gap-2 text-sm text-muted-foreground">
      <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
      {toolResult.action === 'open_canvas'
        ? `Opening canvas: ${toolResult.canvasConfig.title}`
        : 'Updating canvas...'}
    </div>
  );
}
```

### Code Execution Result

```tsx
// lib/ai/genui/code-result.tsx
import { CheckCircle, XCircle, Clock } from 'lucide-react';
import { cn } from '@/lib/utils';

interface CodeResultProps {
  result: {
    success: boolean;
    output: string;
    error: string | null;
    durationMs: number;
  };
}

export function CodeResultGenUI({ result }: CodeResultProps) {
  return (
    <div className={cn(
      'rounded-lg border p-4',
      result.success ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
    )}>
      <div className="flex items-center gap-2 mb-2">
        {result.success ? (
          <CheckCircle className="h-4 w-4 text-green-600" />
        ) : (
          <XCircle className="h-4 w-4 text-red-600" />
        )}
        <span className="font-medium">
          {result.success ? 'Execution Successful' : 'Execution Failed'}
        </span>
        <span className="text-xs text-muted-foreground ml-auto flex items-center gap-1">
          <Clock className="h-3 w-3" />
          {result.durationMs}ms
        </span>
      </div>

      {result.output && (
        <pre className="text-sm bg-white/50 rounded p-2 overflow-x-auto">
          {result.output}
        </pre>
      )}

      {result.error && (
        <pre className="text-sm text-red-700 bg-white/50 rounded p-2 overflow-x-auto">
          {result.error}
        </pre>
      )}
    </div>
  );
}
```

## AI Tool Message Handling

### Processing Tool Calls

```tsx
// In chat message handler
import { useChat } from 'ai/react';
import { CanvasGenUI } from '@/lib/ai/genui/canvas-genui';

function ChatMessages() {
  const { messages } = useChat();

  return (
    <>
      {messages.map((message) => (
        <div key={message.id}>
          {/* Regular content */}
          {message.content}

          {/* Tool invocations */}
          {message.toolInvocations?.map((tool) => {
            if (tool.toolName === 'open_canvas' || tool.toolName === 'update_canvas') {
              return (
                <CanvasGenUI
                  key={tool.toolCallId}
                  toolResult={tool.result}
                />
              );
            }
            // Handle other tools...
          })}
        </div>
      ))}
    </>
  );
}
```

## Code Generation Best Practices

### Prompt Engineering for Code

```typescript
const codeGenerationPrompt = `
Generate {language} code that:
1. Is educational and well-commented
2. Follows best practices for {language}
3. Is appropriate for {difficulty} level students
4. Demonstrates the concept: {concept}

Include:
- Clear variable names
- Step-by-step comments
- Example output as comments

Educational context:
- Topic: {topic}
- Learning objective: {learningObjective}
`;
```

### Response Format

```typescript
// AI should return structured code blocks
interface CodeGenerationResult {
  code: string;
  explanation: string;
  examples: string[];
  nextSteps: string[];
}
```

## Tool Invocation Tracking

### Artifact Persistence

```typescript
// Track tool invocations for artifact persistence
interface CanvasArtifact {
  artifactId: string;
  conversationId: string;
  messageId: string;
  toolInvocationId: string;
  type: CanvasType;
  content: string;
  createdAt: Date;
  updatedAt: Date;
}

// Save artifact when canvas content changes
async function saveCanvasArtifact(
  conversationId: string,
  messageId: string,
  toolInvocationId: string,
  content: string
) {
  await db.insert(canvasArtifacts).values({
    id: nanoid(),
    conversationId,
    messageId,
    toolInvocationId,
    content,
    // ...
  });
}
```

## Error Handling in Tools

### Tool Error Response

```typescript
export const openCanvasTool = tool({
  // ...
  execute: async (args, { abortSignal }) => {
    try {
      // Check signal for cancellation
      if (abortSignal?.aborted) {
        return { action: 'cancelled' };
      }

      const config = CanvasConfigSchema.parse(args);
      return {
        action: 'open_canvas' as const,
        canvasConfig: config,
      };
    } catch (error) {
      if (error instanceof z.ZodError) {
        return {
          action: 'error',
          error: 'Invalid canvas configuration',
          details: error.errors,
        };
      }
      throw error; // Re-throw unexpected errors
    }
  },
});
```

### UI Error Display

```tsx
function ToolErrorDisplay({ error }: { error: { message: string; details?: unknown } }) {
  return (
    <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-3">
      <p className="text-sm text-destructive font-medium">{error.message}</p>
      {error.details && (
        <pre className="text-xs mt-2 text-muted-foreground">
          {JSON.stringify(error.details, null, 2)}
        </pre>
      )}
    </div>
  );
}
```

## Model-Specific Considerations

### Tuning for Different Models

```typescript
// lib/ai/config/model-canvas.ts

export const CANVAS_MODEL_CONFIG = {
  'gemini-3-flash': {
    // Gemini tends to be less verbose
    toolCallBehavior: 'lenient',
    promptSuffix: 'When using tools, provide complete implementations.',
  },
  'grok-4.1-fast': {
    // Grok excels at agentic tool calling
    toolCallBehavior: 'strict',
    maxToolRoundtrips: 5,
  },
  'claude-4.5': {
    toolCallBehavior: 'balanced',
    maxToolRoundtrips: 3,
  },
} as const;
```

## Testing Checklist

- [ ] open_canvas creates correct configuration
- [ ] update_canvas merges properly
- [ ] run_code returns structured results
- [ ] GenUI components render correctly
- [ ] Tool errors display user-friendly messages
- [ ] Artifact tracking persists data
- [ ] Tool cancellation works
- [ ] Model-specific tuning applied
