---
name: wix-site-widget
description: Creates custom element widgets (site widgets) for Wix sites with React components and built-in settings panels. Generates interactive widgets that site owners can add to pages via the Wix Editor, with configurable properties managed through a settings panel. Use when building interactive widgets (countdown timers, progress bars, calculators), custom data displays (product showcases, testimonials, galleries), configurable components with visual customization, reusable components, or widgets displaying data from Wix Data collections. Triggers: widget, custom element, site widget, interactive component, countdown, timer, calculator, display, showcase, gallery, form widget, interactive, configurable, settings panel, editor component, web component.
license: MIT
compatibility: Requires Wix CLI project with custom element extension support
metadata:
  author: wix
  version: "1.0.0"
  category: wix-extensions
---

# Wix Site Widget Builder

Creates custom element widget extensions for Wix CLI applications. Site widgets are React components converted to web components that appear in the Wix Editor, allowing site owners to add interactive, configurable widgets to their pages with a built-in settings panel.

## Non-Matching Intents

Do NOT use this skill for:

- **Dashboard admin interfaces** → Use `wix-dashboard-page`
- **Embedded scripts** (HTML/JavaScript injection) → Use `wix-embedded-script`
- **Backend API endpoints** → Use `wix-backend-api`
- **Service plugins** (eCommerce SPIs) → Use `wix-service-plugin`
- **Site components** (React-only, no settings panel) → Use `wix-site-component`

## Architecture

Site widgets consist of **two required files**:

### 1. Widget Component (`widget.tsx`)

React component converted to a web component using `react-to-webcomponent`:

- Define Props interface with configurable properties (camelCase)
- Create a React functional component that renders the widget UI
- Convert to web component with props mapping
- Use inline styles (no CSS imports)
- Handle Wix Editor environment when using Wix Data API

### 2. Settings Panel (`panel.tsx`)

Settings panel shown in the Wix Editor sidebar:

- Uses Wix Design System components (see [references/WDS-COMPONENTS.md](references/WDS-COMPONENTS.md))
- Manages widget properties via `@wix/editor` widget API
- Loads initial values with `widget.getProp('kebab-case-name')`
- Updates properties with `widget.setProp('kebab-case-name', value)`
- Wrapped in `WixDesignSystemProvider > SidePanel > SidePanel.Content`

## Widget Component Pattern

```typescript
import React, { type FC, useState, useEffect } from "react";
import ReactDOM from "react-dom";
import reactToWebComponent from "react-to-webcomponent";

interface WidgetProps {
  title?: string;
  targetDate?: string;
  bgColor?: string;
  textColor?: string;
  font?: string;
}

const CustomElement: FC<WidgetProps> = ({
  title = "Default Title",
  targetDate = "",
  bgColor = "#ffffff",
  textColor = "#333333",
  font = "{}",
}) => {
  // Parse font if needed
  const { font: textFont, textDecoration } = JSON.parse(font);

  // Component logic and state
  const [data, setData] = useState(null);

  // Use inline styles
  const styles = {
    wrapper: {
      display: "flex",
      flexDirection: "column",
      padding: "20px",
      backgroundColor: bgColor,
      color: textColor,
      fontFamily: textFont || "inherit",
    },
  };

  return (
    <div style={styles.wrapper}>
      {title && <h2 style={{ margin: 0 }}>{title}</h2>}
      {/* Widget content */}
    </div>
  );
};

// Convert to web component
const customElement = reactToWebComponent(CustomElement, React, ReactDOM, {
  props: {
    title: "string",
    targetDate: "string",
    bgColor: "string",
    textColor: "string",
    font: "string",
  },
});

export default customElement;
```

**Key Points:**

- Props interface uses **camelCase** (e.g., `targetDate`, `bgColor`)
- `reactToWebComponent` config uses camelCase keys with `'string'` type
- All props are passed as strings from the web component
- Use inline styles, not CSS imports
- Parse complex props (like `font`) from JSON strings if needed

## Settings Panel Pattern

```typescript
import React, { type FC, useState, useEffect, useCallback } from "react";
import { widget } from "@wix/editor";
import {
  SidePanel,
  WixDesignSystemProvider,
  Input,
  FormField,
  Box,
} from "@wix/design-system";
import "@wix/design-system/styles.global.css";

const Panel: FC = () => {
  const [title, setTitle] = useState<string>("");
  const [targetDate, setTargetDate] = useState<string>("");
  const [bgColor, setBgColor] = useState<string>("#ffffff");

  // Load initial values (kebab-case prop names)
  useEffect(() => {
    Promise.all([
      widget.getProp("title"),
      widget.getProp("target-date"),
      widget.getProp("bg-color"),
    ])
      .then(([titleVal, dateVal, bgColorVal]) => {
        setTitle(titleVal || "");
        setTargetDate(dateVal || "");
        setBgColor(bgColorVal || "#ffffff");
      })
      .catch((error) =>
        console.error("Failed to fetch widget properties:", error)
      );
  }, []);

  // Update both local state and widget prop (kebab-case)
  const handleTitleChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const newTitle = event.target.value;
      setTitle(newTitle);
      widget.setProp("title", newTitle);
    },
    []
  );

  const handleDateChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const newDate = event.target.value;
      setTargetDate(newDate);
      widget.setProp("target-date", newDate);
    },
    []
  );

  return (
    <WixDesignSystemProvider>
      <SidePanel width="300" height="100vh">
        <SidePanel.Header title="Widget Settings" />
        <SidePanel.Content noPadding stretchVertically>
          <Box direction="vertical" gap="24px">
            <SidePanel.Field>
              <FormField label="Title">
                <Input
                  type="text"
                  value={title}
                  onChange={handleTitleChange}
                  placeholder="Enter title"
                />
              </FormField>
            </SidePanel.Field>

            <SidePanel.Field>
              <FormField label="Target Date">
                <Input
                  type="date"
                  value={targetDate}
                  onChange={handleDateChange}
                />
              </FormField>
            </SidePanel.Field>
          </Box>
        </SidePanel.Content>
      </SidePanel>
    </WixDesignSystemProvider>
  );
};

export default Panel;
```

**Key Points:**

- Prop names in `widget.getProp()` and `widget.setProp()` use **kebab-case** (e.g., `"target-date"`, `"bg-color"`)
- Always update both local state AND widget prop in onChange handlers
- Wrap content in `WixDesignSystemProvider > SidePanel > SidePanel.Content`
- Use WDS components from `@wix/design-system` (see [references/WDS-COMPONENTS.md](references/WDS-COMPONENTS.md))
- Import `@wix/design-system/styles.global.css` for styles

### Querying WDS Component Details

For detailed information about WDS components (descriptions, usage guidelines, feature examples, code snippets), use the shared query script:

```bash
node ./scripts/query-wds-components.js <component-name> [<component-name> ...]

# Examples:
node ./scripts/query-wds-components.js FormField Input
node ./scripts/query-wds-components.js SidePanel SidePanel.Header
node ./scripts/query-wds-components.js ToggleSwitch DatePicker
```

The script reads from `assets/wds-storybook.json` and outputs formatted component information. This is useful when you need specific prop usage examples, best practices, or feature-specific code examples beyond what's documented in [WDS-COMPONENTS.md](references/WDS-COMPONENTS.md).

## Props Naming Convention

**Critical:** Props use different naming conventions in each file:

| File                           | Convention | Example                                       |
| ------------------------------ | ---------- | --------------------------------------------- |
| `widget.tsx` (Props interface) | camelCase  | `targetDate`, `bgColor`, `textColor`          |
| `panel.tsx` (widget API)       | kebab-case | `"target-date"`, `"bg-color"`, `"text-color"` |
| `reactToWebComponent` config   | camelCase  | `targetDate: 'string'`                        |

The web component automatically converts between camelCase (React props) and kebab-case (HTML attributes).

## Wix Data API Integration

When using Wix Data API in widgets, you **must** handle the Wix Editor environment gracefully:

```typescript
import { items } from "@wix/data";
import { window as wixWindow } from "@wix/site-window";

const CustomElement: FC<WidgetProps> = ({ collectionId }) => {
  const [data, setData] = useState(null);
  const [isEditor, setIsEditor] = useState(false);

  useEffect(() => {
    const loadData = async () => {
      const currentViewMode = await wixWindow.viewMode();

      if (currentViewMode === "Editor") {
        // Don't fetch data in editor - show placeholder
        setIsEditor(true);
        return;
      }

      // Fetch real data only on live site
      try {
        const results = await items.query(collectionId).limit(10).find();
        setData(results.items);
      } catch (error) {
        console.error("Failed to load data:", error);
      }
    };

    loadData();
  }, [collectionId]);

  if (isEditor) {
    return (
      <div style={{ padding: "20px", border: "2px dashed #ccc" }}>
        <p>Widget will display data on the live site</p>
        <p>Collection: {collectionId}</p>
      </div>
    );
  }

  // Render widget with real data
  return (
    <div>
      {data?.map((item) => (
        <div key={item._id}>{item.title}</div>
      ))}
    </div>
  );
};
```

**Requirements:**

- Import `{ window as wixWindow }` from `"@wix/site-window"`
- Check `await wixWindow.viewMode()` before fetching data
- If `viewMode === 'Editor'`, show a placeholder UI instead
- Only fetch and render real data when NOT in editor mode

## Font Selection

For font selection in settings panels, use `FontPickerField` component with `inputs.selectFont()`:

```typescript
import { inputs } from "@wix/editor";
import { FontPickerField } from "./components/FontPickerField";

const Panel: FC = () => {
  const [font, setFont] = useState({ font: "", textDecoration: "" });

  const handleFontChange = async () => {
    const selectedFont = await inputs.selectFont();
    if (selectedFont) {
      const fontValue = {
        font: selectedFont.fontFamily || "",
        textDecoration: selectedFont.textDecoration || "",
      };
      setFont(fontValue);
      widget.setProp("font", JSON.stringify(fontValue));
    }
  };

  return (
    <FontPickerField
      label="Text Font"
      value={font}
      onChange={handleFontChange}
    />
  );
};
```

**Important:** Use `inputs.selectFont()` from `@wix/editor`, NOT a text Input. This provides a rich font picker dialog with bold, italic, size, and typography features.

## Output Structure

```
src/site/widgets/custom-elements/
└── {widget-name}/
    ├── widget.tsx           # Main widget component
    ├── panel.tsx            # Settings panel component
    ├── extensions.ts         # Extension registration
    ├── components/          # Optional sub-components
    │   ├── ColorPickerField.tsx
    │   └── FontPickerField.tsx
    └── utils/               # Optional helper functions
        └── formatters.ts
```

## Examples

### Countdown Timer Widget

**Request:** "Create a countdown timer widget"

**Output:**

- Widget with configurable title, target date/time, colors, and font
- Settings panel with date picker, time input, color pickers, font picker
- Real-time countdown display with days, hours, minutes, seconds

### Product Showcase Widget

**Request:** "Create a widget that displays products from a collection"

**Output:**

- Widget that queries Wix Data collection
- Editor environment handling (shows placeholder in editor)
- Settings panel for collection selection, display options, styling
- Responsive grid layout with product cards

### Interactive Calculator Widget

**Request:** "Create a calculator widget with customizable colors"

**Output:**

- Functional calculator component
- Settings panel for color customization (background, buttons, text)
- Inline styles for all styling
- No external dependencies

## Frontend Aesthetics

Avoid generic "AI slop" aesthetics. Create distinctive, creative designs:

**Do:**

- Use unique, interesting fonts (avoid Inter, Roboto, Arial)
- Commit to cohesive color palettes with sharp accents
- Add CSS animations and transitions for micro-interactions
- Create atmospheric backgrounds with gradients or patterns
- Vary between light and dark themes
- Make context-specific design choices

**Don't:**

- Use overused font families (Inter, Roboto, Arial, system fonts)
- Use clichéd color schemes (purple gradients on white)
- Create predictable, cookie-cutter layouts
- Converge on common choices across generations

## Extension Registration

**Extension registration is MANDATORY and has TWO required steps.**

### Step 1: Create Widget-Specific Extension File

Each site widget requires an `extensions.ts` file in its folder:

```typescript
import { extensions } from "@wix/astro/builders";

export const sitewidgetMyWidget = extensions.customElement({
  id: "{{GENERATE_UUID}}",
  name: "My Widget",
  tagName: "my-widget",
  element: "./site/widgets/custom-elements/my-widget/widget.tsx",
  settings: "./site/widgets/custom-elements/my-widget/panel.tsx",
  installation: {
    autoAdd: true,
  },
  width: {
    defaultWidth: 500,
    allowStretch: true,
  },
  height: {
    defaultHeight: 500,
  },
});
```

**CRITICAL: UUID Generation**

The `id` must be a unique, static UUID v4 string. Generate a fresh UUID for each extension - do NOT use `randomUUID()` or copy UUIDs from examples. Replace `{{GENERATE_UUID}}` with a freshly generated UUID like `"a1b2c3d4-e5f6-7890-abcd-ef1234567890"`.

| Property       | Type   | Description                            |
| -------------- | ------ | -------------------------------------- |
| `id`           | string | Unique static UUID v4 (generate fresh) |
| `name`         | string | Display name in editor                 |
| `tagName`      | string | HTML custom element tag (kebab-case)   |
| `element`      | string | Path to widget React component         |
| `settings`     | string | Path to settings panel component       |
| `installation` | object | Auto-add behavior                      |
| `width`        | object | Default width and stretch settings     |
| `height`       | object | Default height settings                |

### Step 2: Register in Main Extensions File

**CRITICAL:** After creating the widget-specific extension file, you MUST read [../references/EXTENSIONS.md](../references/EXTENSIONS.md) and follow the "App Registration" section to update `src/extensions.ts`.

**Without completing Step 2, the site widget will not be available in the Wix Editor.**

## Code Quality Requirements

- Strict TypeScript (no `any`, explicit return types)
- Functional React components with hooks
- Proper error handling and loading states
- No `@ts-ignore` comments
- Inline styles only (no CSS imports)
- Handle Wix Editor environment when using Wix Data API
- Consistent prop naming (camelCase in widget, kebab-case in panel)
