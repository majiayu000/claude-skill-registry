---
name: inspector-customization
description: Create and customize inspector panels for node editors. Use when implementing custom inspector tabs, settings panels, node-specific inspectors, or using inspector UI components.
---

# Inspector Customization

This skill covers creating and customizing inspector panels in react-wireflow.

## Three Customization Patterns

### Pattern 1: Node-Level `renderInspector`

Define custom inspector content per node type in the NodeDefinition:

```typescript
import type { NodeDefinition, InspectorRenderProps } from "react-wireflow";
import {
  PropertySection,
  InspectorDefinitionList,
  InspectorDefinitionItem,
  InspectorInput,
  InspectorSelect,
} from "react-wireflow";

type PersonNodeData = {
  name: string;
  email: string;
  role: "developer" | "designer" | "manager";
};

function PersonInspectorRenderer({
  node,
  onUpdateNode,
}: InspectorRenderProps<PersonNodeData>): React.ReactElement {
  const data = node.data ?? ({} as PersonNodeData);

  const handleChange = <K extends keyof PersonNodeData>(
    key: K,
    value: PersonNodeData[K]
  ) => {
    onUpdateNode({ data: { ...data, [key]: value } });
  };

  return (
    <PropertySection title="Person Details">
      <InspectorDefinitionList>
        <InspectorDefinitionItem label="Name">
          <InspectorInput
            value={data.name ?? ""}
            onChange={(e) => handleChange("name", e.target.value)}
            placeholder="Enter name"
          />
        </InspectorDefinitionItem>
        <InspectorDefinitionItem label="Role">
          <InspectorSelect
            value={data.role ?? "developer"}
            onChange={(e) =>
              handleChange("role", e.target.value as PersonNodeData["role"])
            }
          >
            <option value="developer">Developer</option>
            <option value="designer">Designer</option>
            <option value="manager">Manager</option>
          </InspectorSelect>
        </InspectorDefinitionItem>
      </InspectorDefinitionList>
    </PropertySection>
  );
}

const PersonNodeDefinition: NodeDefinition<PersonNodeData> = {
  type: "person",
  displayName: "Person",
  ports: [...],
  renderInspector: PersonInspectorRenderer,
};
```

### Pattern 2: Custom Tabs via `InspectorPanel`

Add custom tabs to the inspector panel:

```typescript
import {
  InspectorPanel,
  InspectorLayersTab,
  InspectorPropertiesTab,
  InspectorSettingsTab,
  InspectorSection,
  PropertySection,
  type InspectorPanelTabConfig,
} from "react-wireflow";

const StatisticsTab: React.FC = () => (
  <InspectorSection>
    <PropertySection title="Editor Statistics">
      <InspectorDefinitionList>
        <InspectorDefinitionItem label="Total Nodes">
          <ReadOnlyField>5</ReadOnlyField>
        </InspectorDefinitionItem>
      </InspectorDefinitionList>
    </PropertySection>
  </InspectorSection>
);

const CustomInspectorPanel: React.FC = () => {
  const tabs: InspectorPanelTabConfig[] = React.useMemo(
    () => [
      {
        id: "layers",
        label: "Layers",
        render: () => <InspectorLayersTab />,
      },
      {
        id: "properties",
        label: "Properties",
        render: () => <InspectorPropertiesTab />,
      },
      {
        id: "statistics",
        label: "Stats",
        render: () => <StatisticsTab />,
      },
      {
        id: "settings",
        label: "Settings",
        render: () => <InspectorSettingsTab />,
      },
    ],
    []
  );

  return <InspectorPanel tabs={tabs} />;
};
```

### Pattern 3: Custom Settings Panels

Add custom panels to the Settings tab:

```typescript
import {
  InspectorSettingsTab,
  InspectorDefinitionList,
  InspectorDefinitionItem,
  InspectorSelect,
  InspectorButton,
  type InspectorSettingsPanelConfig,
} from "react-wireflow";

const ExportSettingsPanel: React.FC = () => {
  const [format, setFormat] = React.useState<"json" | "yaml">("json");

  return (
    <InspectorDefinitionList>
      <InspectorDefinitionItem label="Format">
        <InspectorSelect
          value={format}
          onChange={(e) => setFormat(e.target.value as "json" | "yaml")}
        >
          <option value="json">JSON</option>
          <option value="yaml">YAML</option>
        </InspectorSelect>
      </InspectorDefinitionItem>
      <InspectorDefinitionItem label="">
        <InspectorButton variant="primary" size="small">
          Export Data
        </InspectorButton>
      </InspectorDefinitionItem>
    </InspectorDefinitionList>
  );
};

const settingsPanels: InspectorSettingsPanelConfig[] = [
  {
    title: "Export Options",
    component: ExportSettingsPanel,
  },
];

// Use in tabs:
{
  id: "settings",
  label: "Settings",
  render: () => <InspectorSettingsTab panels={settingsPanels} />,
}
```

## Available Inspector Components

### Panel Components

| Component | Description |
|-----------|-------------|
| `InspectorPanel` | Main container with tab support |
| `InspectorLayersTab` | Built-in layers/tree tab |
| `InspectorPropertiesTab` | Built-in properties tab (uses node's `renderInspector`) |
| `InspectorSettingsTab` | Built-in settings tab with extensible panels |
| `InspectorHistoryTab` | Built-in undo/redo history tab |

### Layout Components

| Component | Description |
|-----------|-------------|
| `InspectorSection` | Basic section wrapper |
| `PropertySection` | Collapsible section with title |
| `InspectorField` | Vertical field layout (label above input) |
| `InspectorFieldRow` | Horizontal field layout |
| `InspectorDefinitionList` | Definition list container |
| `InspectorDefinitionItem` | Label-value pair in definition list |
| `PositionInputsGrid` | Grid for X/Y coordinate inputs |
| `InspectorSectionTitle` | Standalone section title |
| `InspectorTabbedContainer` | Nested tabs within inspector |

### Input Components

| Component | Description |
|-----------|-------------|
| `InspectorInput` | Text input field |
| `InspectorNumberInput` | Number input with label |
| `InspectorTextarea` | Multi-line text input |
| `InspectorSelect` | Dropdown select |
| `InspectorButton` | Button (variants: primary, danger, default) |
| `InspectorIconButton` | Icon-only button |
| `InspectorButtonGroup` | Segmented button group (radio-style) |
| `InspectorToggleGroup` | Toggle button group (checkbox-style) |
| `InspectorLabel` | Form label |
| `ReadOnlyField` | Non-editable display field |

## InspectorRenderProps Reference

```typescript
type InspectorRenderProps<TData> = {
  node: Node & { data: TData };
  externalData: unknown;
  isLoadingExternalData: boolean;
  externalDataError: Error | null;
  onUpdateNode: (updates: Partial<Node>) => void;
  onUpdateExternalData: (data: unknown) => Promise<void>;
  onDeleteNode: () => void;
};
```

## Best Practices

1. **Always use inspector components** for consistent theming across light/dark modes
2. **Use `PropertySection`** for collapsible groups of related fields
3. **Use `InspectorDefinitionList`** for label-value pairs
4. **Use `InspectorButtonGroup`** for mutually exclusive options
5. **Keep inspector content scrollable** - avoid fixed heights

## Example File

See complete example at:
`src/examples/demos/custom/inspector/custom-inspector/CustomInspectorExample.tsx`
