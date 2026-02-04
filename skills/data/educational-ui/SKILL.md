---
name: educational-ui
description: Creates educational UI components following learning science principles. Use for classroom, student, or teacher interfaces.
allowed-tools: Read, Write, Edit, Glob
model: sonnet
context: fork
---

# Educational UI Design Skill

## When to Use

Use this skill when creating:

- Student-facing interfaces
- Teacher dashboards
- Learning activities
- Assessment components
- Progress tracking UI

## Core Principles

### 1. Learning Science

- **Clear objectives**: Always show what students will learn
- **Progress visibility**: Show advancement toward goals
- **Immediate feedback**: Respond to interactions instantly
- **Scaffolding**: Break complex tasks into steps
- **Spaced retrieval**: Support review and practice

### 2. Accessibility (WCAG 2.1 AA)

- Minimum 4.5:1 contrast for text
- Keyboard navigable
- Screen reader compatible
- Focus indicators visible
- Form labels and error messages

### 3. Mobile-First

- Touch targets ≥44px
- Readable without zoom
- Thumb-friendly placement
- Responsive breakpoints

## Elon Brand Tokens

```typescript
// ALWAYS use design tokens, NEVER hex codes
className="bg-maroon text-white"     // Primary brand
className="bg-gold text-black"       // Secondary accent
className="bg-surface-dark"          // Dark backgrounds
className="text-muted-foreground"    // Subdued text

// In SVG/Charts
fill="var(--color-maroon)"
stroke="var(--color-gold)"
```

## Component Patterns

### Progress Indicator

```typescript
import { Progress } from '@/components/ui/progress';

function LessonProgress({ completed, total }: { completed: number; total: number }) {
  const percentage = Math.round((completed / total) * 100);

  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span className="text-muted-foreground">Progress</span>
        <span className="font-medium">{percentage}%</span>
      </div>
      <Progress value={percentage} className="h-2" />
      <p className="text-xs text-muted-foreground">
        {completed} of {total} activities completed
      </p>
    </div>
  );
}
```

### Learning Objective Card

```typescript
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Target } from 'lucide-react';

function LearningObjective({ objective }: { objective: string }) {
  return (
    <Card className="border-l-4 border-l-maroon">
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center gap-2 text-base">
          <Target className="h-4 w-4 text-maroon" />
          Learning Objective
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground">{objective}</p>
      </CardContent>
    </Card>
  );
}
```

### Feedback Message

```typescript
import { CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

type FeedbackType = 'success' | 'error' | 'hint';

function Feedback({ type, message }: { type: FeedbackType; message: string }) {
  const config = {
    success: { icon: CheckCircle, className: 'bg-green-50 border-green-200 text-green-800' },
    error: { icon: XCircle, className: 'bg-red-50 border-red-200 text-red-800' },
    hint: { icon: AlertCircle, className: 'bg-amber-50 border-amber-200 text-amber-800' },
  };

  const { icon: Icon, className } = config[type];

  return (
    <div className={cn('flex items-start gap-2 p-4 rounded-lg border', className)}>
      <Icon className="h-5 w-5 flex-shrink-0 mt-0.5" />
      <p className="text-sm">{message}</p>
    </div>
  );
}
```

### Streamed AI Response

```typescript
'use client';

import { useChat } from 'ai/react';
import { StreamdownContent } from '@/components/streamdown-content';

function AITutor({ assistantId }: { assistantId: string }) {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',
    body: { assistantId },
  });

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((m) => (
          <div key={m.id} className={cn(
            'rounded-lg p-4',
            m.role === 'user' ? 'bg-muted ml-8' : 'bg-card mr-8 border'
          )}>
            {m.role === 'assistant' ? (
              <StreamdownContent content={m.content} />
            ) : (
              <p>{m.content}</p>
            )}
          </div>
        ))}
      </div>
      {/* Input area */}
    </div>
  );
}
```

## Chart Styling (Tremor/Recharts)

```typescript
// Always use CSS variables for Elon brand colors
const chartColors = {
  primary: 'var(--color-maroon)',
  secondary: 'var(--color-gold)',
  tertiary: 'hsl(var(--muted))',
};

// Example with Tremor
<BarChart
  data={data}
  index="name"
  categories={['value']}
  colors={['rose']} // Maps to maroon
  valueFormatter={(v) => `${v}%`}
/>
```

## Checklist

- [ ] Learning objective visible
- [ ] Progress indicator present
- [ ] Immediate feedback implemented
- [ ] Uses shadcn/ui components
- [ ] Color tokens (no hex codes)
- [ ] WCAG AA compliant
- [ ] Mobile responsive
- [ ] Keyboard navigable
- [ ] Screen reader labels
- [ ] Loading states with Suspense
