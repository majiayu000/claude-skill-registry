---
name: custom-node-definition
description: Create custom node definitions with renderers, ports, external data, and constraints. Use when implementing new node types, custom node appearances, or node-specific behaviors.
---

# Custom Node Definition

This skill covers creating custom node definitions in react-wireflow.

## Basic NodeDefinition Structure

```typescript
import type { NodeDefinition } from "react-wireflow";

const MyNodeDefinition: NodeDefinition = {
  type: "my-node",           // Unique identifier
  displayName: "My Node",    // Display name in UI
  description: "Description for palette",
  category: "My Category",   // For grouping in palette

  // Default values for new nodes
  defaultData: { title: "New Node" },
  defaultSize: { width: 200, height: 100 },
  defaultResizable: true,

  // Port definitions
  ports: [
    { id: "input", type: "input", position: "left", label: "Input" },
    { id: "output", type: "output", position: "right", label: "Output" },
  ],
};
```

## Custom Node Renderer

Use `renderNode` for custom node appearance:

```typescript
import type { NodeDefinition, NodeRendererProps } from "react-wireflow";
import { NodeResizer } from "react-wireflow";

type TaskData = {
  title: string;
  status: "todo" | "done";
};

const TaskNodeRenderer = ({
  node,
  isSelected,
  isDragging,
  isResizing,
  isEditing,
  onStartEdit,
  onUpdateNode,
}: NodeRendererProps<TaskData>) => {
  const data = node.data;

  return (
    <NodeResizer node={node} defaultWidth={200} defaultHeight={100}>
      {() => (
        <div
          className="task-node"
          data-selected={isSelected}
          data-status={data.status}
          onDoubleClick={onStartEdit}
        >
          <h3>{data.title}</h3>
          <span>{data.status}</span>
        </div>
      )}
    </NodeResizer>
  );
};

const TaskNodeDefinition: NodeDefinition<TaskData> = {
  type: "task",
  displayName: "Task",
  defaultData: { title: "New Task", status: "todo" },
  ports: [...],
  renderNode: TaskNodeRenderer,
};
```

## NodeRendererProps Reference

```typescript
type NodeRendererProps<TData> = {
  node: Node & { data: TData };
  isSelected: boolean;
  isDragging: boolean;
  isResizing: boolean;
  isEditing: boolean;
  externalData: unknown;
  isLoadingExternalData: boolean;
  externalDataError: Error | null;
  onStartEdit: () => void;
  onUpdateNode: (updates: Partial<Node>) => void;
};
```

## Port Configuration

### Basic Ports

```typescript
ports: [
  { id: "in", type: "input", position: "left", label: "Input" },
  { id: "out", type: "output", position: "right", label: "Output" },
]
```

### Port with Data Type

```typescript
{
  id: "number-out",
  type: "output",
  position: "right",
  label: "Number",
  dataType: "number",           // Single type
  // or
  dataTypes: ["number", "int"], // Multiple compatible types
}
```

### Port with Connection Limits

```typescript
{
  id: "multi-input",
  type: "input",
  position: "left",
  label: "Multi",
  maxConnections: 5,            // or "unlimited"
}
```

### Port with Custom Validation

```typescript
{
  id: "exclusive",
  type: "output",
  position: "right",
  label: "Exclusive",
  canConnect: (context) => {
    // Only connect to specific node types
    return context.toNode?.type === "receiver";
  },
}
```

### Dynamic Ports

```typescript
{
  id: "item",
  type: "input",
  position: "left",
  label: "Item",
  instances: (context) => context.node.data.itemCount ?? 1,
  createPortId: (ctx) => `item-${ctx.index}`,
  createPortLabel: (ctx) => `Item ${ctx.index + 1}`,
}
```

### Absolute Port Position

```typescript
{
  id: "center",
  type: "output",
  label: "Center",
  position: {
    mode: "absolute",
    x: 0.5,  // 50% from left
    y: 0.5,  // 50% from top
    unit: "fraction",
  },
}
```

## External Data Integration

For nodes that load data from external sources:

```typescript
import type { ExternalDataReference } from "react-wireflow";

const TaskNodeDefinition: NodeDefinition = {
  type: "task",
  displayName: "Task",
  ports: [...],

  loadExternalData: async (ref: ExternalDataReference) => {
    const response = await fetch(`/api/tasks/${ref.id}`);
    return response.json();
  },

  updateExternalData: async (ref: ExternalDataReference, data: unknown) => {
    await fetch(`/api/tasks/${ref.id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  },

  renderNode: TaskNodeRenderer,
  renderInspector: TaskInspectorRenderer,
};

// Provide external data refs to NodeEditor:
<NodeEditor
  initialData={data}
  nodeDefinitions={[TaskNodeDefinition]}
  externalDataRefs={{
    "node-1": { id: "task-123", type: "task" },
    "node-2": { id: "task-456", type: "task" },
  }}
/>
```

## Node-Level Connection Validation

```typescript
const HubNodeDefinition: NodeDefinition = {
  type: "hub",
  displayName: "Hub",
  ports: [...],

  validateConnection: (fromPort, toPort) => {
    // Custom validation logic
    // fromPort is always OUTPUT, toPort is always INPUT
    console.log(`Validating: ${fromPort.nodeId} -> ${toPort.nodeId}`);
    return true; // or false to reject
  },
};
```

## Node Constraints

```typescript
import type { NodeConstraint, ConstraintContext } from "react-wireflow";

const maxNodesConstraint: NodeConstraint = {
  id: "max-nodes",
  name: "Maximum Nodes",
  description: "Limit total nodes of this type",
  blocking: true,
  appliesTo: ["create"],
  validate: (context: ConstraintContext) => {
    const count = Object.values(context.allNodes)
      .filter(n => n.type === context.node.type).length;

    if (count >= 5) {
      return {
        isValid: false,
        violations: [{
          type: "max-nodes",
          message: "Maximum 5 nodes allowed",
          severity: "error",
        }],
      };
    }
    return { isValid: true, violations: [] };
  },
};

const LimitedNodeDefinition: NodeDefinition = {
  type: "limited",
  displayName: "Limited Node",
  constraints: [maxNodesConstraint],
  maxPerFlow: 5,  // Built-in limit option
};
```

## Custom Port Positions

Override default port positioning:

```typescript
const CustomLayoutNode: NodeDefinition = {
  type: "custom-layout",
  displayName: "Custom Layout",
  ports: [...],

  computePortPositions: (context) => {
    const { node, ports, nodeSize, defaultCompute } = context;

    // Use default for most ports
    const positions = defaultCompute(ports);

    // Override specific port
    const specialPort = ports.find(p => p.id === "special");
    if (specialPort) {
      positions.set("special", {
        renderPosition: { x: nodeSize.width / 2, y: 0 },
        connectionPoint: {
          x: node.position.x + nodeSize.width / 2,
          y: node.position.y,
        },
      });
    }

    return positions;
  },
};
```

## Node Behaviors

```typescript
const GroupNodeDefinition: NodeDefinition = {
  type: "group",
  displayName: "Group",
  behaviors: ["group"],  // Enables group container behavior
};

const AppearanceNodeDefinition: NodeDefinition = {
  type: "styled",
  displayName: "Styled Node",
  behaviors: ["appearance", "node"],  // Custom appearance + standard node
  disableOutline: true,  // Disable default selection styling
};
```

## Visual State

```typescript
const ErrorNodeDefinition: NodeDefinition = {
  type: "error",
  displayName: "Error Node",
  visualState: "error",  // "info" | "success" | "warning" | "error" | "disabled"
};
```

## Categories

```typescript
// Single category
category: "Math"

// Multiple categories
category: ["Math", "Utilities"]

// Hierarchical category
category: "custom/ui/buttons"
```

## Type-Safe Helper

```typescript
import { createNodeDefinition, asNodeDefinition } from "react-wireflow";

// Type-safe creation
const TypedNode = createNodeDefinition<MyDataType>({
  type: "typed",
  displayName: "Typed Node",
  defaultData: { value: 0 },
  ports: [],
});

// Convert to base type for arrays
const definitions: NodeDefinition[] = [
  asNodeDefinition(TypedNode),
];
```

## Example Files

- Basic custom node: `src/examples/demos/custom/nodes/custom-node/CustomNodeExample.tsx`
- Advanced nodes: `src/examples/demos/advanced/advanced-node/`
- Connection rules: `src/examples/demos/custom/connections/connection-rules/`
- Constrained nodes: `src/examples/demos/basic/constrained-nodes/`
