---
name: canvas-component
description: Creates and extends Canvas UI components with Monaco editor, split views, and educational context. Use when building Canvas panel, editor, or preview features.
allowed-tools: Read, Write, Edit, Glob
context: fork
---

# Canvas Component Development Skill

## When to Use

Use this skill when:

- Creating Canvas panel or container components
- Adding Monaco editor features
- Building code preview/execution UI
- Implementing split-view layouts
- Adding toolbar actions (run, download, share)

## Component Architecture

```
components/canvas/
├── canvas-container.tsx          # Root container with state
├── canvas-panel.tsx              # Full panel with editor + preview
├── canvas-editor.tsx             # Monaco wrapper
├── canvas-preview.tsx            # Execution preview
├── canvas-toolbar.tsx            # Actions toolbar
├── canvas-editor-error-boundary.tsx  # Error recovery
└── index.ts                      # Barrel exports
```

## State Management (Zustand)

### Canvas Store Pattern

```typescript
import { create } from 'zustand';
import type { CanvasState, CanvasType, ViewMode } from '@/lib/canvas/types';

interface CanvasStore extends CanvasState {
  // Actions
  openCanvas: (config: CanvasConfig) => void;
  closeCanvas: () => void;
  updateContent: (content: string) => void;
  setViewMode: (mode: ViewMode) => void;
  undo: () => void;
  redo: () => void;

  // Generation
  startGeneration: (prompt: string) => void;
  completeGeneration: (content: string) => void;
}

export const useCanvasStore = create<CanvasStore>((set, get) => ({
  // Initial state
  isOpen: false,
  content: '',
  type: 'code',
  title: 'Untitled',
  language: 'python',
  viewMode: 'split',
  history: [],
  historyIndex: -1,
  generationPrompt: '',
  isGenerating: false,

  openCanvas: (config) => set({
    isOpen: true,
    type: config.type,
    title: config.title,
    language: config.language || getDefaultLanguage(config.type),
    content: config.initialContent || '',
    generationPrompt: config.generationPrompt || '',
    viewMode: 'split',
    history: [config.initialContent || ''],
    historyIndex: 0,
  }),

  updateContent: (content) => {
    const { history, historyIndex } = get();
    const newHistory = [...history.slice(0, historyIndex + 1), content];
    set({
      content,
      history: newHistory,
      historyIndex: newHistory.length - 1,
    });
  },
  // ...
}));
```

## Monaco Editor Wrapper

### Basic Setup

```tsx
'use client';

import { useRef, useCallback } from 'react';
import MonacoEditor, { OnMount, OnChange } from '@monaco-editor/react';
import { getMonacoLanguage } from '@/lib/canvas/types';
import { CanvasEditorErrorBoundary } from './canvas-editor-error-boundary';

interface CanvasEditorProps {
  content: string;
  language: string;
  onChange: (value: string) => void;
  readOnly?: boolean;
  height?: string;
}

export function CanvasEditor({
  content,
  language,
  onChange,
  readOnly = false,
  height = '100%',
}: CanvasEditorProps) {
  const editorRef = useRef<any>(null);

  const handleMount: OnMount = (editor, monaco) => {
    editorRef.current = editor;

    // Configure Monaco for educational use
    monaco.editor.defineTheme('canvas-theme', {
      base: 'vs-dark',
      inherit: true,
      rules: [],
      colors: {
        'editor.background': '#1a1a1a',
      },
    });

    editor.updateOptions({
      fontSize: 14,
      lineHeight: 22,
      minimap: { enabled: false },
      scrollBeyondLastLine: false,
      wordWrap: 'on',
      tabSize: 4,
      insertSpaces: true,
    });
  };

  const handleChange: OnChange = (value) => {
    onChange(value || '');
  };

  return (
    <CanvasEditorErrorBoundary>
      <MonacoEditor
        height={height}
        language={getMonacoLanguage(language)}
        value={content}
        onChange={handleChange}
        onMount={handleMount}
        theme="canvas-theme"
        options={{
          readOnly,
          automaticLayout: true,
        }}
        loading={<EditorSkeleton />}
      />
    </CanvasEditorErrorBoundary>
  );
}
```

### Error Boundary

```tsx
'use client';

import { Component, ReactNode } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { resetMonacoLoader } from '@/lib/canvas/monaco-loader';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class CanvasEditorErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  handleReset = () => {
    resetMonacoLoader();
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex flex-col items-center justify-center h-full gap-4 p-8 text-center">
          <AlertTriangle className="h-8 w-8 text-destructive" />
          <div>
            <h3 className="font-medium">Editor failed to load</h3>
            <p className="text-sm text-muted-foreground mt-1">
              This usually resolves after a page refresh.
            </p>
          </div>
          <Button onClick={this.handleReset} size="sm">
            <RefreshCw className="h-4 w-4 mr-2" />
            Try Again
          </Button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

## Split View Panel

### Resizable Layout

```tsx
'use client';

import { ResizablePanelGroup, ResizablePanel, ResizableHandle } from '@/components/ui/resizable';
import { CanvasEditor } from './canvas-editor';
import { CanvasPreview } from './canvas-preview';
import { CanvasToolbar } from './canvas-toolbar';
import type { ViewMode } from '@/lib/canvas/types';

interface CanvasPanelProps {
  content: string;
  language: string;
  viewMode: ViewMode;
  onContentChange: (content: string) => void;
  onViewModeChange: (mode: ViewMode) => void;
  onRun: () => void;
}

export function CanvasPanel({
  content,
  language,
  viewMode,
  onContentChange,
  onViewModeChange,
  onRun,
}: CanvasPanelProps) {
  return (
    <div className="flex flex-col h-full">
      <CanvasToolbar
        viewMode={viewMode}
        onViewModeChange={onViewModeChange}
        onRun={onRun}
        language={language}
      />

      <div className="flex-1 min-h-0">
        {viewMode === 'split' ? (
          <ResizablePanelGroup direction="horizontal">
            <ResizablePanel defaultSize={50} minSize={30}>
              <CanvasEditor
                content={content}
                language={language}
                onChange={onContentChange}
              />
            </ResizablePanel>
            <ResizableHandle withHandle />
            <ResizablePanel defaultSize={50} minSize={30}>
              <CanvasPreview
                content={content}
                language={language}
              />
            </ResizablePanel>
          </ResizablePanelGroup>
        ) : viewMode === 'code' ? (
          <CanvasEditor
            content={content}
            language={language}
            onChange={onContentChange}
          />
        ) : (
          <CanvasPreview
            content={content}
            language={language}
          />
        )}
      </div>
    </div>
  );
}
```

## Toolbar Actions

### Standard Toolbar

```tsx
'use client';

import { Play, Download, Copy, Code, Eye, Columns2, Undo, Redo } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';
import { canExecute, getFileExtension } from '@/lib/canvas/types';
import type { ViewMode } from '@/lib/canvas/types';

interface CanvasToolbarProps {
  viewMode: ViewMode;
  onViewModeChange: (mode: ViewMode) => void;
  onRun: () => void;
  onUndo?: () => void;
  onRedo?: () => void;
  canUndo?: boolean;
  canRedo?: boolean;
  language: string;
  content?: string;
  isRunning?: boolean;
}

export function CanvasToolbar({
  viewMode,
  onViewModeChange,
  onRun,
  onUndo,
  onRedo,
  canUndo,
  canRedo,
  language,
  content,
  isRunning,
}: CanvasToolbarProps) {
  const showRunButton = canExecute(language);

  const handleDownload = () => {
    const blob = new Blob([content || ''], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `code${getFileExtension(language)}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleCopy = async () => {
    await navigator.clipboard.writeText(content || '');
    // Show toast
  };

  return (
    <div className="flex items-center justify-between px-2 py-1.5 border-b bg-muted/50">
      <div className="flex items-center gap-1">
        {/* View Mode Toggle */}
        <ToggleGroup
          type="single"
          value={viewMode}
          onValueChange={(v) => v && onViewModeChange(v as ViewMode)}
          size="sm"
        >
          <ToggleGroupItem value="code" aria-label="Code only">
            <Code className="h-4 w-4" />
          </ToggleGroupItem>
          <ToggleGroupItem value="split" aria-label="Split view">
            <Columns2 className="h-4 w-4" />
          </ToggleGroupItem>
          <ToggleGroupItem value="preview" aria-label="Preview only">
            <Eye className="h-4 w-4" />
          </ToggleGroupItem>
        </ToggleGroup>

        <div className="w-px h-4 bg-border mx-1" />

        {/* Undo/Redo */}
        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              variant="ghost"
              size="icon"
              className="h-7 w-7"
              onClick={onUndo}
              disabled={!canUndo}
            >
              <Undo className="h-4 w-4" />
            </Button>
          </TooltipTrigger>
          <TooltipContent>Undo (Ctrl+Z)</TooltipContent>
        </Tooltip>

        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              variant="ghost"
              size="icon"
              className="h-7 w-7"
              onClick={onRedo}
              disabled={!canRedo}
            >
              <Redo className="h-4 w-4" />
            </Button>
          </TooltipTrigger>
          <TooltipContent>Redo (Ctrl+Shift+Z)</TooltipContent>
        </Tooltip>
      </div>

      <div className="flex items-center gap-1">
        <Tooltip>
          <TooltipTrigger asChild>
            <Button variant="ghost" size="icon" className="h-7 w-7" onClick={handleCopy}>
              <Copy className="h-4 w-4" />
            </Button>
          </TooltipTrigger>
          <TooltipContent>Copy code</TooltipContent>
        </Tooltip>

        <Tooltip>
          <TooltipTrigger asChild>
            <Button variant="ghost" size="icon" className="h-7 w-7" onClick={handleDownload}>
              <Download className="h-4 w-4" />
            </Button>
          </TooltipTrigger>
          <TooltipContent>Download</TooltipContent>
        </Tooltip>

        {showRunButton && (
          <Button
            size="sm"
            className="ml-2 gap-1"
            onClick={onRun}
            disabled={isRunning}
          >
            <Play className="h-3 w-3" />
            {isRunning ? 'Running...' : 'Run'}
          </Button>
        )}
      </div>
    </div>
  );
}
```

## Keyboard Shortcuts

### Hook Implementation

```tsx
import { useHotkeys } from 'react-hotkeys-hook';

function CanvasWithShortcuts() {
  const { content, updateContent, undo, redo, canUndo, canRedo } = useCanvasStore();

  // Run code
  useHotkeys('mod+enter', () => handleRun(), { enableOnFormTags: true });

  // Undo/Redo (Monaco handles internal, this is for store)
  useHotkeys('mod+z', () => undo(), { enabled: canUndo });
  useHotkeys('mod+shift+z', () => redo(), { enabled: canRedo });

  // Toggle view modes
  useHotkeys('mod+1', () => setViewMode('code'));
  useHotkeys('mod+2', () => setViewMode('split'));
  useHotkeys('mod+3', () => setViewMode('preview'));
}
```

## Educational Context Display

### Learning Objective Header

```tsx
interface EducationalContextProps {
  context?: {
    topic?: string;
    difficulty?: 'beginner' | 'intermediate' | 'advanced';
    learningObjective?: string;
  };
}

function EducationalContextHeader({ context }: EducationalContextProps) {
  if (!context?.learningObjective) return null;

  const difficultyColors = {
    beginner: 'bg-green-100 text-green-800',
    intermediate: 'bg-amber-100 text-amber-800',
    advanced: 'bg-red-100 text-red-800',
  };

  return (
    <div className="px-4 py-2 border-b bg-muted/30">
      <div className="flex items-center gap-2 text-sm">
        {context.difficulty && (
          <span className={cn(
            'px-2 py-0.5 rounded-full text-xs font-medium',
            difficultyColors[context.difficulty]
          )}>
            {context.difficulty}
          </span>
        )}
        {context.topic && (
          <span className="text-muted-foreground">
            {context.topic}
          </span>
        )}
      </div>
      <p className="text-sm mt-1">{context.learningObjective}</p>
    </div>
  );
}
```

## Accessibility Requirements

### WCAG 2.1 AA Checklist

- [ ] Focus visible on all interactive elements
- [ ] Keyboard navigation for all actions
- [ ] Screen reader labels for icons
- [ ] Color contrast 4.5:1 minimum
- [ ] Announced status changes (execution results)
- [ ] Skip links for editor navigation

```tsx
// Example: Screen reader announcement
import { useEffect } from 'react';

function useAnnounce() {
  const announce = (message: string) => {
    const el = document.createElement('div');
    el.setAttribute('role', 'status');
    el.setAttribute('aria-live', 'polite');
    el.className = 'sr-only';
    el.textContent = message;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 1000);
  };
  return announce;
}

// Usage
const announce = useAnnounce();
announce('Code executed successfully');
```

## Testing Checklist

- [ ] Monaco loads without errors
- [ ] Split view resizing works
- [ ] View mode toggles correctly
- [ ] Keyboard shortcuts function
- [ ] Undo/redo maintains history
- [ ] Copy/download work
- [ ] Mobile responsive
- [ ] Error boundary catches Monaco failures
- [ ] Educational context displays
- [ ] Accessibility requirements met
