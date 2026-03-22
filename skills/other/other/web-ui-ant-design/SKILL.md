---
name: web-ui-ant-design
description: Ant Design enterprise UI library for React
---

# Ant Design Patterns

> **Quick Guide:** Ant Design is an enterprise-grade React UI library providing a complete set of high-quality components. Use ConfigProvider with design tokens for theming, the three-layer token system (Seed, Map, Alias) for customization, and the App component for context-aware feedback methods. **Current: v6.x** (pure CSS variables by default, zero-runtime mode, React 18+ required). v5.x is in maintenance. All patterns in this skill apply to both v5 and v6 unless noted.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST wrap your app with ConfigProvider for theming and locale - never override component styles with global CSS)**

**(You MUST use the App component and useApp() hook for message/notification/modal - never use static methods directly as they cannot consume ConfigProvider context)**

**(You MUST use Form.useForm() with TypeScript generics for type-safe form handling - never use untyped form instances)**

**(You MUST use CSS variables mode (cssVar: true) for optimal theme-switching performance in production)**

</critical_requirements>

---

**Auto-detection:** Ant Design, antd, ConfigProvider, theme.defaultAlgorithm, theme.darkAlgorithm, theme.compactAlgorithm, useToken, Form.useForm, Form.List, Form.useWatch, ProTable, ProForm, ProLayout, @ant-design/icons, @ant-design/pro-components, AntdRegistry, Table columns, message.success, notification.open, Modal.confirm

**When to use:**

- Building enterprise admin panels, dashboards, and data-heavy applications
- Need a comprehensive component library with consistent design language out of the box
- Working with complex data tables, forms with validation, and multi-step workflows
- Requiring built-in internationalization, dark mode, and theme customization

**When NOT to use:**

- Building a custom design system from scratch (use Radix UI or headless primitives)
- Need minimal bundle size for a simple marketing site (Ant Design is large)
- Want full control over styling without design opinions (use unstyled primitives)
- Building non-React applications (Ant Design is React-specific)

**Key patterns covered:**

- ConfigProvider theming with design tokens (Seed, Map, Alias, Component tokens)
- Table with sorting, filtering, virtual scrolling, and custom rendering
- Form with validation, dynamic fields (Form.List), and TypeScript generics
- Layout system (Layout, Grid, Space, Flex)
- Feedback patterns (Modal, Message, Notification via App/useApp)
- Dark mode and theme switching with algorithms
- Next.js SSR with AntdRegistry
- Pro Components (ProTable, ProForm, ProLayout)

---

## Examples

- [Core Setup & Theming](examples/core.md) -- ConfigProvider, App wrapper, design tokens, dark mode, nested themes, useToken
- [Forms & Validation](examples/form.md) -- Form, Form.Item, validation rules, useForm, Form.List, Form.useWatch, modal form
- [Tables](examples/table.md) -- Table, columns, sorting, filtering, pagination, row selection, virtual scrolling, expandable rows
- [Layout](examples/layout.md) -- Layout, Sider, Header, Content, Grid (Row/Col), Space, Flex
- [Feedback Components](examples/feedback.md) -- Modal, Drawer, message, notification, useApp
- [Data Display](examples/data-display.md) -- Card, Descriptions, Statistic, Tag, Badge
- [Navigation & Icons](examples/navigation.md) -- Menu, Breadcrumb, icon tree-shaking, custom icons
- [Pro Components](examples/pro-components.md) -- ProLayout, ProTable, ProForm, StepsForm
- [Next.js Integration](examples/nextjs.md) -- AntdRegistry, SSR, client components, App Router
- [Internationalization](examples/i18n.md) -- ConfigProvider locale, dayjs locale sync

For quick reference and component checklists, see [reference.md](reference.md).

---

<philosophy>

## Philosophy

Ant Design follows the principles of **Natural**, **Certain**, **Meaningful**, and **Growing** to provide an enterprise-grade design system. It solves UI consistency across large teams by providing:

- **Complete component set**: 60+ components covering layout, data display, data entry, navigation, and feedback
- **Design token system**: Three-layer architecture (Seed > Map > Alias) enabling systematic customization without CSS overrides
- **Enterprise patterns**: Built-in pagination, filtering, form validation, internationalization, and accessibility

**Architecture (CSS-in-JS with CSS Variables):** Ant Design uses a CSS-in-JS engine (`@ant-design/cssinjs`) with design tokens. v6 defaults to pure CSS Variables mode for reduced bundle size and instant theme switching. v6 also supports zero-runtime mode (`zeroRuntime: true`) where styles are pre-extracted to static CSS. Tree-shaking is built-in -- no `babel-plugin-import` needed.

**When to use Ant Design:**

- Enterprise admin interfaces with data tables, forms, and dashboards
- Internal tools where development speed matters more than unique design
- Projects needing i18n, RTL, and accessibility out of the box
- Teams wanting a comprehensive, well-documented component library

**When NOT to use:**

- Consumer-facing products needing distinctive brand design (too opinionated)
- Performance-critical SPAs where bundle size must be minimal
- Projects using a utility-class-first styling paradigm

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: App Root Setup

The minimal app setup wraps everything in ConfigProvider + App:

```tsx
import { ConfigProvider, App as AntApp } from "antd";
import type { ThemeConfig } from "antd";
import enUS from "antd/locale/en_US";

const THEME_CONFIG: ThemeConfig = {
  cssVar: true,
  token: { colorPrimary: "#1677ff", borderRadius: 6 },
};

function App() {
  return (
    <ConfigProvider theme={THEME_CONFIG} locale={enUS}>
      <AntApp>
        <MainContent />
      </AntApp>
    </ConfigProvider>
  );
}
export { App };
```

**Why this structure:** ConfigProvider provides theme tokens and locale to all children. App component enables context-aware message/notification/modal APIs. cssVar mode optimizes theme switching performance.

See [examples/core.md](examples/core.md) for enterprise theme, dark mode toggle, nested themes, and useToken patterns.

---

### Pattern 2: Design Tokens and Theming

Ant Design uses a three-layer token system:

- **Seed Tokens**: Foundational values (`colorPrimary`, `fontSize`, `borderRadius`) that derive all other tokens
- **Map Tokens**: Derived from seed tokens via algorithms (`colorPrimaryBg`, `colorPrimaryHover`)
- **Alias Tokens**: Semantic tokens mapping to use cases (`colorBgContainer`, `colorTextHeading`)
- **Component Tokens**: Per-component overrides (`Button.primaryShadow`, `Table.headerBg`)

```tsx
// Access tokens programmatically for custom components
import { theme } from "antd";
const { useToken } = theme;

function CustomCard() {
  const { token } = useToken();
  return (
    <div
      style={{ background: token.colorBgContainer, padding: token.paddingLG }}
    >
      Styled with design tokens
    </div>
  );
}
```

See [examples/core.md](examples/core.md) for full theme configuration, nested themes, and StatusCard using useToken.

---

### Pattern 3: Dark Mode and Theme Switching

```tsx
import { ConfigProvider, theme as antTheme } from "antd";

// Switch between algorithms for dark/light/compact modes
const themeConfig = {
  cssVar: true,
  algorithm: isDark ? antTheme.darkAlgorithm : antTheme.defaultAlgorithm,
  token: { colorPrimary: "#1677ff" },
};

// Combine algorithms: dark + compact
const combined = {
  algorithm: [antTheme.darkAlgorithm, antTheme.compactAlgorithm],
};
```

See [examples/core.md](examples/core.md) for dark mode toggle with persistence and algorithm combining.

---

### Pattern 4: Layout System

Use Layout for page-level structure, Grid (Row/Col) for responsive content areas, Flex for inline element alignment, Space for uniform gaps between small elements.

```tsx
// Page shell: Layout + Sider + Header + Content
<Layout style={{ minHeight: "100vh" }}>
  <Sider width={200} collapsible>
    <Menu theme="dark" mode="inline" items={MENU_ITEMS} />
  </Sider>
  <Layout>
    <Header />
    <Content>{children}</Content>
  </Layout>
</Layout>

// Responsive grid: Row + Col (24-column)
<Row gutter={[16, 16]}>
  <Col xs={24} md={8}><Card /></Col>
  <Col xs={24} md={8}><Card /></Col>
</Row>

// Flex alignment (v5.10+)
<Flex gap={8} justify="space-between" align="center" wrap>
  <Button type="primary">Save</Button>
  <Button>Cancel</Button>
</Flex>
```

See [examples/layout.md](examples/layout.md) for full layout, grid, and flex examples.

---

### Pattern 5: Table

Key requirements: TypeScript generics on `Table<T>` and `ColumnsType<T>`, `rowKey` prop always set, typed `onChange` handler.

```tsx
import { Table } from "antd";
import type { ColumnsType } from "antd/es/table";

// Virtual scrolling (10,000+ rows): requires both scroll.x and scroll.y as numbers
<Table<DataRecord>
  virtual
  scroll={{ x: 1200, y: 500 }}
  columns={columns} // All columns need explicit width
  pagination={false}
/>;
```

See [examples/table.md](examples/table.md) for server-side table, expandable rows, summary rows, and virtual scrolling.

---

### Pattern 6: Form with Validation and Dynamic Fields

Key requirements: `Form.useForm<T>()` with TypeScript generic, `initialValues` on Form (not Form.Item), `htmlType="submit"` on submit button, `destroyOnClose` on Modal/Drawer containing Form.

```tsx
const [form] = Form.useForm<MyFormValues>();
const watchedValue = Form.useWatch("fieldName", form);

<Form<MyFormValues>
  form={form}
  layout="vertical"
  onFinish={handleSubmit}
  initialValues={{ role: "viewer" }}
>
  <Form.Item name="email" rules={[{ required: true, type: "email" }]}>
    <Input />
  </Form.Item>
</Form>;
```

See [examples/form.md](examples/form.md) for complex validation, Form.List dynamic fields, Form.useWatch, and modal form patterns.

---

### Pattern 7: Feedback Components (Modal, Message, Notification)

Always use `App.useApp()` for feedback -- never static methods:

```tsx
function MyComponent() {
  const { message, notification, modal } = App.useApp();

  // These respect ConfigProvider theme and locale
  message.success("Saved!");
  notification.open({ message: "Update", description: "..." });
  modal.confirm({
    title: "Delete?",
    onOk: async () => {
      /* ... */
    },
  });
}
```

See [examples/feedback.md](examples/feedback.md) for declarative Modal, Drawer, and Popconfirm patterns.

---

### Pattern 8: Data Display Components

```tsx
// Descriptions for detail views
<Descriptions bordered column={{ xs: 1, sm: 2, md: 3 }} items={details} />

// Statistic cards for dashboards
<Statistic title="Revenue" value={112893} prefix="$" precision={2} />
```

See [examples/data-display.md](examples/data-display.md) for Descriptions, Statistic, Card grid, Tag, and Badge patterns.

---

### Pattern 9: Navigation and Icons

```tsx
// Use items API (v4.20+) - not JSX children
<Menu mode="inline" items={MENU_ITEMS} onClick={({ key }) => navigate(key)} />;

// Icons: always import individually for tree-shaking
import { UserOutlined } from "@ant-design/icons";
// NEVER: import * as Icons from "@ant-design/icons" (500KB+)
```

See [examples/navigation.md](examples/navigation.md) for Menu, Breadcrumb, icon tree-shaking, and custom SVG icons.

---

### Pattern 10: Next.js App Router Integration

```tsx
// app/layout.tsx - wrapping order matters: AntdRegistry > ConfigProvider > App
<AntdRegistry>
  <ConfigProvider theme={THEME} locale={enUS}>
    <AntApp>{children}</AntApp>
  </ConfigProvider>
</AntdRegistry>
```

See [examples/nextjs.md](examples/nextjs.md) for SSR setup, client components, and sub-component workarounds.

---

### Pattern 11: Internationalization

ConfigProvider locale handles antd component text. Set dayjs locale separately for date/time formatting.

See [examples/i18n.md](examples/i18n.md) for locale switching with dayjs sync.

---

### Pattern 12: Pro Components

ProTable, ProForm, and ProLayout provide page-level enterprise abstractions with auto-generated search forms, step wizards, and route-based menus.

See [examples/pro-components.md](examples/pro-components.md) for ProLayout, ProTable CRUD, and StepsForm patterns.

</patterns>

---

<performance>

## Performance Optimization

### CSS Variables Mode

```tsx
// v6: CSS variables are default. v5: opt in with cssVar: true
const THEME: ThemeConfig = {
  cssVar: true,
  hashed: false, // Disable hash when only one antd version in the app
};

// v6 zero-runtime mode: no runtime style generation
// Import 'antd/dist/antd.css' for default styles, or use
// @ant-design/static-style-extract for custom themes
const ZERO_RUNTIME_THEME: ThemeConfig = {
  zeroRuntime: true,
};
```

CSS variables mode eliminates runtime style recalculation when switching themes. `hashed: false` is safe when only one antd version exists. Zero-runtime mode (v6) completely removes runtime style generation for maximum performance.

### Tree-Shaking

Tree-shaking works natively -- no `babel-plugin-import` needed. Icons must always be imported individually (`import { UserOutlined } from "@ant-design/icons"`) or via path imports.

### Virtual Scrolling

```tsx
// Table: virtual requires both scroll.x and scroll.y as numbers
<Table virtual scroll={{ x: 1200, y: 500 }} />

// Select: virtual prop for large option lists
<Select virtual options={largeOptionsList} />

// Tree/TreeSelect: virtual prop
<Tree virtual treeData={largeTreeData} />
```

</performance>

---

<decision_framework>

## Decision Framework

### Choosing Feedback Components

```
Need to show user feedback?
├─ Brief status update (success/error/loading) -> message via useApp()
├─ Detailed notification with title + description -> notification via useApp()
├─ Requires user decision -> modal.confirm() via useApp()
├─ Complex form or content -> Modal component (declarative, with open prop)
└─ Side panel with content -> Drawer component
```

### Table vs ProTable

```
Building a data table?
├─ Simple display with basic sort/filter -> Table
├─ Need auto-generated search form -> ProTable
├─ Need server-side pagination + filtering -> ProTable (request API)
├─ Custom complex UI around table -> Table (more control)
└─ CRUD page with toolbar actions -> ProTable (toolBarRender)
```

### Form vs ProForm

```
Building a form?
├─ Simple single-page form -> Form
├─ Multi-step wizard -> StepsForm (from ProForm)
├─ Form in modal -> ModalForm (from ProForm)
├─ Form in drawer -> DrawerForm (from ProForm)
├─ Search/filter form -> QueryFilter or LightFilter (from ProForm)
└─ Need full layout control -> Form (more flexible)
```

### Layout Approach

```
How to lay out content?
├─ Page-level shell (sidebar + header + content) -> Layout
├─ Responsive grid of cards/panels -> Row + Col (24-column grid)
├─ Flex alignment of inline elements -> Flex (v5.10+)
├─ Uniform spacing between small elements -> Space
├─ Enterprise admin with route-based menu -> ProLayout
└─ Responsive breakpoints needed -> Row + Col with xs/sm/md/lg/xl props
```

### Theming Approach

```
How to customize appearance?
├─ Brand colors only -> Seed tokens (colorPrimary, etc.)
├─ Specific component tweaks -> Component tokens (Button.colorPrimary)
├─ Dark mode -> algorithm: theme.darkAlgorithm
├─ Compact spacing -> algorithm: theme.compactAlgorithm
├─ Section-specific theme -> Nested ConfigProvider
├─ Access tokens in custom components -> useToken() hook
└─ Dynamic theme switching -> cssVar: true + state-driven algorithm
```

</decision_framework>

---

<integration>

## Integration Guide

**Routing:** Layout, Menu, and Breadcrumb components accept `onClick` / `href` handlers -- wire them to your router's navigation. Menu `items` array maps naturally to route definitions.

**Data fetching:** Table and ProTable work with any data source. Pass fetched data via `dataSource` prop or use ProTable's `request` callback which expects `{ data, success, total }`.

**Date library:** dayjs is the default date library (replaces moment.js from v4). Date components use it internally -- set dayjs locale separately from ConfigProvider locale.

**Ant Design ecosystem packages:**

- `@ant-design/pro-components` -- enterprise patterns (ProTable, ProForm, ProLayout)
- `@ant-design/nextjs-registry` -- SSR style extraction for SSR frameworks
- `@ant-design/icons` -- icon library (import individually for tree-shaking)

**Styling coexistence:** Avoid overriding antd styles with global CSS -- use design tokens and component tokens instead. Antd's CSS-in-JS styles have their own specificity; mixing with utility-class frameworks requires careful management.

</integration>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using static `message.success()`, `notification.open()`, `Modal.confirm()` without App wrapper -- they bypass ConfigProvider context, leading to wrong theme and broken locale
- Overriding antd styles with global CSS (`.ant-btn { ... }`) -- breaks on theme changes and version upgrades, use component tokens instead
- Importing entire icon set (`import * as Icons from "@ant-design/icons"`) -- adds 500KB+ to bundle
- Using `value`/`defaultValue` on form controls inside `Form.Item` with `name` -- conflicts with Form's state management

**Medium Priority Issues:**

- Missing `rowKey` on Table -- causes React key warnings and update bugs
- Using `Form.Item initialValue` instead of `Form initialValues` -- inconsistent behavior with form reset
- Not wrapping app with `<App>` component when using feedback methods -- feedback renders outside theme context
- Missing `destroyOnClose` on Modal with Form inside -- stale form state persists across open/close

**Common Mistakes:**

- Forgetting to set dayjs locale alongside ConfigProvider locale (date components show wrong language)
- Using dot-notation sub-components in Next.js App Router server components (`<Select.Option>`)
- Not enabling `cssVar: true` for apps that switch themes (causes full style recalculation)
- Wrapping AntdRegistry inside ConfigProvider instead of outside in Next.js (breaks style extraction)

**Gotchas & Edge Cases:**

- `Form.useWatch` triggers component re-render -- use sparingly in performance-sensitive forms
- Table `onChange` fires for pagination, filters, AND sorting -- check the extra parameter to determine which changed
- `Modal.confirm()` returns a reference for updating/destroying -- store it if you need to close programmatically
- ConfigProvider `theme.components` tokens with `algorithm: true` derive from the component's `colorPrimary`, not the global one
- Virtual Table requires explicit column `width` values and both `scroll.x` and `scroll.y` as numbers -- without them, columns collapse or virtual mode fails
- ProTable `request` must return `{ data, success, total }` -- missing `success: true` causes infinite loading
- Nested ConfigProvider inherits unset tokens from parent -- set tokens explicitly if you want isolation
- `@ant-design/icons@6` is NOT compatible with `antd@5` -- always upgrade both packages together

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST wrap your app with ConfigProvider for theming and locale - never override component styles with global CSS)**

**(You MUST use the App component and useApp() hook for message/notification/modal - never use static methods directly as they cannot consume ConfigProvider context)**

**(You MUST use Form.useForm() with TypeScript generics for type-safe form handling - never use untyped form instances)**

**(You MUST use CSS variables mode (cssVar: true) for optimal theme-switching performance in production)**

**Failure to follow these rules will cause theme inconsistencies, broken internationalization, and degraded performance.**

</critical_reminders>
