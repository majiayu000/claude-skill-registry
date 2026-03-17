---
name: rspress-components
description: Use RSPress built-in components and MDX features in documentation. Use when adding interactive elements like tabs, badges, steps, callouts, or code groups to documentation pages.
allowed-tools: Read, Write, Edit, Glob
agent: rspress-doc-agent
---

# RSPress Components Skill

Guide for using RSPress built-in components and MDX features in documentation.

## Importing Components

Import built-in components from `rspress/theme`:

```tsx
import { Badge, Tabs, Tab } from 'rspress/theme';
```

## Common Components

### Badge

Display inline status badges:

```tsx
<Badge type="info" text="Info" />
<Badge type="tip" text="Tip" />
<Badge type="warning" text="Warning" />
<Badge type="danger" text="Danger" />
```

### Tabs

Create tabbed content sections:

```tsx
import { Tabs, Tab } from 'rspress/theme';

<Tabs>
  <Tab label="JavaScript">
    ```javascript
    console.log('Hello');
    ```
  </Tab>
  <Tab label="TypeScript">
    ```typescript
    console.log('Hello');
    ```
  </Tab>
</Tabs>
```

### PackageManagerTabs

Special tabs for package manager commands:

```tsx
import { PackageManagerTabs } from 'rspress/theme';

<PackageManagerTabs command="install react" />
<PackageManagerTabs command="add -D typescript" />
```

### Steps

Create numbered step-by-step instructions:

```tsx
import { Steps } from 'rspress/theme';

<Steps>
### Step 1

First instruction.

### Step 2

Second instruction.
</Steps>
```

### NoSSR

Prevent server-side rendering for client-only components:

```tsx
import { NoSSR } from 'rspress/theme';

<NoSSR>
  <ClientOnlyComponent />
</NoSSR>
```

## Code Block Features

### Syntax Highlighting

Specify language for automatic syntax highlighting:

````markdown
```typescript
const example: string = "code";
```
````

### Line Highlighting

Highlight specific lines with `{line-numbers}`:

````markdown
```typescript{2,4-6}
const a = 1;
const b = 2; // highlighted
const c = 3;
const d = 4; // highlighted
const e = 5; // highlighted
const f = 6; // highlighted
```
````

### Diff Highlighting

Show additions and deletions with `// [!code ++]` and `// [!code --]`:

````markdown
```typescript
const old = 'remove'; // [!code --]
const new = 'add'; // [!code ++]
```
````

## Container Blocks

### Callouts

Create styled callout boxes:

```markdown
:::tip
Helpful tip content
:::

:::info
Informational content
:::

:::warning
Warning content
:::

:::danger
Danger/error content
:::
```

### Details (Collapsible)

Create collapsible sections:

```markdown
:::details Summary text
Hidden content that can be expanded
:::
```

## MDX Features

### Importing Custom Components

```tsx
import CustomComponent from '../components/CustomComponent';

<CustomComponent prop="value" />
```

### Inline Expressions

Use JavaScript expressions inline:

```tsx
export const version = '1.0.0';

Current version: {version}
```

### Mixing Markdown and JSX

```tsx
<div className="custom-wrapper">

## Markdown heading

Regular markdown content works inside JSX.

</div>
```

## Best Practices

* Use `PackageManagerTabs` for install commands to support all package managers
* Add language identifiers to all code blocks for proper syntax highlighting
* Use appropriate callout types (tip/info/warning/danger) for context
* Import only the components you need to minimize bundle size
* Use `NoSSR` sparingly, only when necessary for client-only features
