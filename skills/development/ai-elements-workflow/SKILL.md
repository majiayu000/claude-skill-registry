---
name: ai-elements-workflow
description: This skill provides guidance for building workflow visualizations using Vercel AI Elements and React Flow. It should be used when implementing interactive node-based interfaces, workflow diagrams, or process flow visualizations in Next.js applications. Covers Canvas, Node, Edge, Connection, Controls, Panel, and Toolbar components.
---

# AI Elements Workflow

This skill provides comprehensive guidance for building workflow visualizations using Vercel AI Elements with React Flow.

## When to Use

- Building interactive node-based workflow interfaces
- Creating process flow visualizations
- Implementing diagram editors with custom nodes and edges
- Adding workflow visualization to AI applications

## Setup

### 1. Create Next.js Project

```bash
npx create-next-app@latest ai-workflow && cd ai-workflow
```

Choose to use Tailwind in the project setup.

### 2. Install AI Elements

```bash
npx ai-elements@latest
```

This also sets up shadcn/ui if not configured.

### 3. Install React Flow

```bash
npm i @xyflow/react
```

### 4. Add Components

Install the workflow components as needed:

```bash
npx ai-elements@latest add canvas
npx ai-elements@latest add node
npx ai-elements@latest add edge
npx ai-elements@latest add connection
npx ai-elements@latest add controls
npx ai-elements@latest add panel
npx ai-elements@latest add toolbar
```

## Building a Workflow

### Import Components

```tsx
'use client';
import { Canvas } from '@/components/ai-elements/canvas';
import { Connection } from '@/components/ai-elements/connection';
import { Controls } from '@/components/ai-elements/controls';
import { Edge } from '@/components/ai-elements/edge';
import {
  Node,
  NodeContent,
  NodeDescription,
  NodeFooter,
  NodeHeader,
  NodeTitle,
} from '@/components/ai-elements/node';
import { Panel } from '@/components/ai-elements/panel';
import { Toolbar } from '@/components/ai-elements/toolbar';
import { Button } from '@/components/ui/button';
```

### Define Node IDs

```tsx
const nodeIds = {
  start: 'start',
  process1: 'process1',
  decision: 'decision',
  output1: 'output1',
  output2: 'output2',
  complete: 'complete',
};
```

### Create Nodes

```tsx
const nodes = [
  {
    id: nodeIds.start,
    type: 'workflow',
    position: { x: 0, y: 0 },
    data: {
      label: 'Start',
      description: 'Initialize workflow',
      handles: { target: false, source: true },
      content: 'Triggered by user action',
      footer: 'Status: Ready',
    },
  },
  // Add more nodes...
];
```

### Create Edges

Use `animated` for active paths and `temporary` for conditional/error paths:

```tsx
const edges = [
  {
    id: 'edge1',
    source: nodeIds.start,
    target: nodeIds.process1,
    type: 'animated',
  },
  {
    id: 'edge2',
    source: nodeIds.decision,
    target: nodeIds.output2,
    type: 'temporary', // For error/conditional paths
  },
];
```

### Define Node Types

```tsx
const nodeTypes = {
  workflow: ({
    data,
  }: {
    data: {
      label: string;
      description: string;
      handles: { target: boolean; source: boolean };
      content: string;
      footer: string;
    };
  }) => (
    <Node handles={data.handles}>
      <NodeHeader>
        <NodeTitle>{data.label}</NodeTitle>
        <NodeDescription>{data.description}</NodeDescription>
      </NodeHeader>
      <NodeContent>
        <p className="text-sm">{data.content}</p>
      </NodeContent>
      <NodeFooter>
        <p className="text-muted-foreground text-xs">{data.footer}</p>
      </NodeFooter>
      <Toolbar>
        <Button size="sm" variant="ghost">Edit</Button>
        <Button size="sm" variant="ghost">Delete</Button>
      </Toolbar>
    </Node>
  ),
};
```

### Define Edge Types

```tsx
const edgeTypes = {
  animated: Edge.Animated,
  temporary: Edge.Temporary,
};
```

### Render the Canvas

```tsx
const App = () => (
  <Canvas
    edges={edges}
    edgeTypes={edgeTypes}
    fitView
    nodes={nodes}
    nodeTypes={nodeTypes}
    connectionLineComponent={Connection}
  >
    <Controls />
    <Panel position="top-left">
      <Button size="sm" variant="secondary">Export</Button>
    </Panel>
  </Canvas>
);

export default App;
```

## Key Features

| Feature | Description |
|---------|-------------|
| Custom Node Components | Use NodeHeader, NodeTitle, NodeDescription, NodeContent, NodeFooter for structured layouts |
| Node Toolbars | Attach contextual actions to nodes via Toolbar component |
| Handle Configuration | Control connections with `handles: { target: boolean, source: boolean }` |
| Edge Types | `Edge.Animated` for active flow, `Edge.Temporary` for conditional paths |
| Connection Lines | Styled bezier curves when dragging new connections |
| Controls | Zoom in/out and fit view buttons |
| Panels | Position custom UI anywhere on the canvas |

## Component Reference

For detailed props and API documentation for each component, see `references/components.md`.
