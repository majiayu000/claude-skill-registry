---
name: generate-card
description: Generate dashboard card component with shadcn Card structure, TypeScript props, and optional sub-components. Use when creating new dashboard widgets or stat cards.
allowed-tools: Read, Write, Glob, Grep
---

# Generate Card

Generate a dashboard card component following Health Tracker 9000 patterns.

## Usage

When user requests to create a card component, ask for:

1. **Card name** (e.g., "WaterIntakeCard", "SleepScoreCard")
2. **Data type** the card displays (statistic, progress, chart, list, etc.)
3. **Icon name** from Lucide React
4. **Whether it includes a sub-component** (list items, chart, etc.)

## Implementation Pattern

Based on `src/components/dashboard/HealthScoreCard.tsx` pattern.

### File Structure

Create file: `src/components/dashboard/{CardName}.tsx`

```typescript
'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { cn } from '@/lib/utils';
import { Activity } from 'lucide-react';

interface CardNameProps {
  score: number;
  data: {
    field1: number;
    field2: number;
  };
}

export function CardName({ score, data }: CardNameProps) {
  const getScoreColor = (value: number) => {
    if (value >= 80) return 'text-green-500';
    if (value >= 60) return 'text-yellow-500';
    return 'text-red-500';
  };

  const getProgressColor = (value: number) => {
    if (value >= 80) return 'bg-green-500';
    if (value >= 60) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <Card className="overflow-hidden">
      <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
        <CardTitle className="text-sm font-medium">Card Title</CardTitle>
        <Activity className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="flex flex-col items-center justify-center py-4">
          <div className={cn('text-5xl font-bold mb-2', getScoreColor(score))}>
            {score}
          </div>
          <p className="text-xs text-muted-foreground">Subtitle</p>
        </div>

        <div className="space-y-3 mt-4">
          <ItemComponent
            label="Item 1"
            value={data.field1}
            description="Description of what this measures"
          />
          <ItemComponent
            label="Item 2"
            value={data.field2}
            description="Description of what this measures"
          />
        </div>
      </CardContent>
    </Card>
  );
}

interface ItemComponentProps {
  label: string;
  value: number;
  description: string;
}

function ItemComponent({ label, value, description }: ItemComponentProps) {
  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-xs">
        <div className="flex items-center gap-1 text-muted-foreground">
          {label}
        </div>
        <span className="font-medium">{value}%</span>
      </div>
      <Progress value={value} className="h-1" />
    </div>
  );
}
```

### With Chart Integration (Optional)

For cards with charts, add Recharts:

```typescript
'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp } from 'lucide-react';

interface ChartCardProps {
  data: Array<{ label: string; value: number }>;
  title: string;
}

export function ChartCard({ data, title }: ChartCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <TrendingUp className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="label" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
```

## Key Conventions

- Use `'use client'` directive at top
- Import Card components from `@/components/ui/card`
- Props interface should be `{ComponentName}Props`
- Use Lucide React icons for visual elements
- Tailwind for styling with shadcn color utilities
- Optional: sub-components for list items, chart items, etc.
- Optional: `React.memo()` wrapper for performance optimization
- Color functions for responsive visual feedback (green/yellow/red)

## Steps

1. Ask user for card name, data type, icon, and optional sub-component
2. Create file: `src/components/dashboard/{CardName}.tsx`
3. Generate component with Card wrapper from shadcn/ui
4. Add icon from lucide-react
5. Add props interface with TypeScript
6. Add helper functions for colors/formatting if needed
7. Add optional sub-component if requested
8. Format with Prettier

## Implementation Checklist

- [ ] Component exports correctly
- [ ] Props interface defined and typed
- [ ] Icon imported from lucide-react
- [ ] 'use client' directive present
- [ ] Uses shadcn/ui Card components
- [ ] Color functions for visual feedback
- [ ] Sub-component created (if applicable)
- [ ] Responsive design with Tailwind
