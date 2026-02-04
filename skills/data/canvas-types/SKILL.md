---
name: canvas-types
description: Foundational Canvas type definitions and language support patterns. Use when working with Canvas types, schemas, or language configuration.
allowed-tools: Read, Write, Edit, Glob
context: fork
---

# Canvas Types & Patterns Skill

## When to Use

Use this skill when:

- Defining new Canvas types
- Working with Zod schemas
- Adding language support
- Creating utility functions for Canvas

## Core Type Definitions

### Canvas Types

```typescript
// From lib/canvas/types.ts

export const CANVAS_TYPES = [
  'code',           // Executable code with Monaco editor
  'document',       // Markdown/rich text editor
  'visualization',  // D3/Chart.js interactive visualizations
  'quiz',           // Interactive assessment
  'flashcards',     // Study cards with flip interaction
  'diagram',        // Mermaid/PlantUML diagrams
  'math',           // LaTeX mathematical expressions
  'react',          // React component preview
] as const;

export type CanvasType = (typeof CANVAS_TYPES)[number];
```

### View Modes

```typescript
export type ViewMode = 'code' | 'preview' | 'split';
```

### Canvas State

```typescript
export interface CanvasState {
  // Core state
  isOpen: boolean;
  content: string;
  type: CanvasType;
  title: string;
  language: string;
  viewMode: ViewMode;

  // History for undo/redo
  history: string[];
  historyIndex: number;

  // Generation state
  generationPrompt: string;
  isGenerating: boolean;
}
```

## Zod Schemas

### Canvas Configuration Schema

```typescript
import { z } from 'zod';

export const CanvasConfigSchema = z.object({
  type: z.enum(CANVAS_TYPES),
  title: z.string().max(100),
  language: z.string().optional(),
  initialContent: z.string().optional().default(''),
  generationPrompt: z.string().optional(),
  educationalContext: z.object({
    topic: z.string().optional(),
    difficulty: z.enum(['beginner', 'intermediate', 'advanced']).optional(),
    learningObjective: z.string().optional(),
  }).optional(),
  // Artifact persistence tracking
  artifactId: z.string().uuid().optional(),
  conversationId: z.string().uuid().optional(),
  messageId: z.string().uuid().optional(),
  toolInvocationId: z.string().optional(),
});

export type CanvasConfig = z.infer<typeof CanvasConfigSchema>;
```

### Content Validation

```typescript
/**
 * Maximum canvas content size (1MB)
 * Prevents memory abuse while allowing substantial code examples
 */
export const CANVAS_MAX_CONTENT_SIZE = 1_048_576;

export const CanvasContentSchema = z.object({
  type: z.enum(CANVAS_TYPES),
  title: z.string().max(100),
  content: z.string().max(CANVAS_MAX_CONTENT_SIZE),
  language: z.string().optional(),
  metadata: z.object({
    educationalObjective: z.string().optional(),
    difficulty: z.enum(['beginner', 'intermediate', 'advanced']).optional(),
    estimatedTime: z.number().optional(),
    prerequisites: z.array(z.string()).optional(),
  }).optional(),
});

export type CanvasContent = z.infer<typeof CanvasContentSchema>;
```

## Language Support

### Tiered Language Support

```typescript
export const SUPPORTED_LANGUAGES = {
  // P0 - Must have (curriculum analysis)
  tier1: [
    { id: 'python', name: 'Python', extensions: ['.py'], monacoId: 'python' },
    { id: 'javascript', name: 'JavaScript', extensions: ['.js'], monacoId: 'javascript' },
    { id: 'html', name: 'HTML', extensions: ['.html'], monacoId: 'html' },
    { id: 'css', name: 'CSS', extensions: ['.css'], monacoId: 'css' },
    { id: 'sql', name: 'SQL', extensions: ['.sql'], monacoId: 'sql' },
    { id: 'markdown', name: 'Markdown', extensions: ['.md'], monacoId: 'markdown' },
  ],
  // P1 - High priority
  tier2: [
    { id: 'typescript', name: 'TypeScript', extensions: ['.ts', '.tsx'], monacoId: 'typescript' },
    { id: 'java', name: 'Java', extensions: ['.java'], monacoId: 'java' },
    { id: 'r', name: 'R', extensions: ['.r'], monacoId: 'r' },
    { id: 'latex', name: 'LaTeX', extensions: ['.tex'], monacoId: 'latex' },
  ],
  // P2 - Secondary
  tier3: [
    { id: 'c', name: 'C', extensions: ['.c', '.h'], monacoId: 'c' },
    { id: 'cpp', name: 'C++', extensions: ['.cpp', '.hpp'], monacoId: 'cpp' },
  ],
} as const;
```

### Execution Support Matrix

```typescript
export const EXECUTION_SUPPORT: Record<string, 'pyodide' | 'iframe' | 'none'> = {
  python: 'pyodide',
  javascript: 'iframe',
  html: 'iframe',
  typescript: 'iframe',  // Transpiled to JS
  react: 'iframe',
  css: 'iframe',
  sql: 'none',
  java: 'none',
  c: 'none',
  cpp: 'none',
  r: 'none',
  latex: 'none',
  markdown: 'none',
  mermaid: 'none',
};
```

## Utility Functions

### Default Language by Canvas Type

```typescript
export function getDefaultLanguage(type: CanvasType): string {
  const defaults: Record<CanvasType, string> = {
    code: 'python',
    visualization: 'html',
    react: 'typescript',
    document: 'markdown',
    diagram: 'mermaid',
    math: 'latex',
    quiz: 'json',
    flashcards: 'json',
  };
  return defaults[type] || 'plaintext';
}
```

### Monaco Language Mapping

```typescript
export function getMonacoLanguage(language: string): string {
  const mapping: Record<string, string> = {
    python: 'python',
    javascript: 'javascript',
    typescript: 'typescript',
    tsx: 'typescript',
    jsx: 'javascript',
    html: 'html',
    css: 'css',
    markdown: 'markdown',
    json: 'json',
    sql: 'sql',
    java: 'java',
    c: 'c',
    cpp: 'cpp',
    csharp: 'csharp',
    go: 'go',
    rust: 'rust',
    latex: 'latex',
    mermaid: 'markdown', // No native mermaid support
  };
  return mapping[language] || 'plaintext';
}
```

### Execution Check

```typescript
export function canExecute(language: string): boolean {
  return (
    EXECUTION_SUPPORT[language] !== 'none' &&
    EXECUTION_SUPPORT[language] !== undefined
  );
}
```

### File Extension Mapping

```typescript
export function getFileExtension(language: string): string {
  const extensions: Record<string, string> = {
    python: '.py',
    javascript: '.js',
    typescript: '.ts',
    html: '.html',
    css: '.css',
    markdown: '.md',
    json: '.json',
    sql: '.sql',
    java: '.java',
    c: '.c',
    cpp: '.cpp',
  };
  return extensions[language] || '.txt';
}
```

## Tool Result Types

### Canvas Actions

```typescript
export interface OpenCanvasResult {
  action: 'open_canvas';
  canvasConfig: {
    type: CanvasType;
    title: string;
    language: string;
    initialContent: string;
    generationPrompt: string;
    educationalContext?: {
      topic?: string;
      difficulty?: 'beginner' | 'intermediate' | 'advanced';
      learningObjective?: string;
    };
  };
}

export interface UpdateCanvasResult {
  action: 'update_canvas';
  updates: {
    content?: string;
    title?: string;
    language?: string;
  };
}
```

## Adding New Canvas Types

### Step 1: Add to Types

```typescript
// In types.ts
export const CANVAS_TYPES = [
  // ... existing
  'new_type',  // Add here
] as const;
```

### Step 2: Set Default Language

```typescript
// In getDefaultLanguage()
const defaults: Record<CanvasType, string> = {
  // ... existing
  new_type: 'json',  // Add default
};
```

### Step 3: Update GenUI Components

```tsx
// In genui renderer
switch (canvasType) {
  // ... existing cases
  case 'new_type':
    return <NewTypeCanvas {...props} />;
}
```

## Adding New Languages

### Step 1: Add to Tier

```typescript
// In SUPPORTED_LANGUAGES
tier2: [
  // ... existing
  { id: 'rust', name: 'Rust', extensions: ['.rs'], monacoId: 'rust' },
],
```

### Step 2: Set Execution Support

```typescript
// In EXECUTION_SUPPORT
rust: 'none',  // Or 'iframe' if you implement WASM execution
```

### Step 3: Add Monaco Mapping

```typescript
// In getMonacoLanguage()
rust: 'rust',
```

### Step 4: Add File Extension

```typescript
// In getFileExtension()
rust: '.rs',
```

## Type Guards

### Canvas Type Guard

```typescript
export function isCanvasType(value: unknown): value is CanvasType {
  return typeof value === 'string' && CANVAS_TYPES.includes(value as CanvasType);
}
```

### Execution Support Guard

```typescript
export function supportsExecution(language: string): language is 'python' | 'javascript' | 'typescript' | 'html' | 'react' | 'css' {
  return EXECUTION_SUPPORT[language] !== 'none' && EXECUTION_SUPPORT[language] !== undefined;
}
```

## Validation Patterns

### Safe Parsing

```typescript
import { CanvasConfigSchema } from '@/lib/canvas/types';

function parseCanvasConfig(input: unknown) {
  const result = CanvasConfigSchema.safeParse(input);

  if (!result.success) {
    console.error('Invalid canvas config:', result.error.errors);
    return null;
  }

  return result.data;
}
```

### Content Size Check

```typescript
function isContentValid(content: string): boolean {
  const byteSize = new TextEncoder().encode(content).length;
  return byteSize <= CANVAS_MAX_CONTENT_SIZE;
}
```

## Testing Checklist

- [ ] All Canvas types have default languages
- [ ] All languages have Monaco mappings
- [ ] All languages have file extensions
- [ ] Execution support is correctly marked
- [ ] Zod schemas validate correctly
- [ ] Type guards work as expected
- [ ] Max content size is enforced
