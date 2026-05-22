---
name: shopify-polaris-design
description: Design and implement Shopify Admin interfaces using the Polaris Design System. Use this skill when building Shopify Apps, Admin extensions, or any interface that needs to feel native to Shopify.
---

This skill ensures that interfaces are built using Shopify's Polaris Design System (React implementation v13.x), guaranteeing a native, accessible, and professional look and feel for Shopify Merchants.

> **Note (2025-2026)**: Polaris React (`@shopify/polaris`) is in **maintenance mode**. Shopify has introduced Polaris Web Components for new development. However, Polaris React remains fully functional and supported for existing applications. This guide covers the React implementation.

## Core Principles

1.  **Merchant-Focused**: Design for efficiency and clarity. Merchants use these tools to run their business.
2.  **Native Feel**: The app should feel like a natural extension of the Shopify Admin. Do not introduce foreign design patterns (e.g. Material Design shadows, distinct bootstappy buttons) unless absolutely necessary.
3.  **Accessibility**: Polaris is built with accessibility in mind. Maintain this by using semantic components (e.g., `Button`, `Link`, `TextField`) rather than custom `div` implementations.
4.  **Predictability**: Follow standard Shopify patterns. Save buttons go in the App Bridge Save Bar. Page actions go in the top right. Primary content is centered.

## Technical Implementation

### Dependencies (v13.x - 2025-2026)

```json
{
  "@shopify/polaris": "^13.9.0",
  "@shopify/polaris-icons": "^9.x",
  "@shopify/app-bridge-react": "^4.x"
}
```

### App Bridge Integration (Critical for v13.x)

Many UI components are now handled by **App Bridge** instead of Polaris React:

| Deprecated Polaris Component | Use App Bridge Instead |
|------------------------------|------------------------|
| `Modal` | `@shopify/app-bridge-react` Modal API |
| `Navigation` | App Bridge Navigation Menu API |
| `Toast` | App Bridge Toast API |
| `ContextualSaveBar` | App Bridge `useSaveBar()` hook |
| `TopBar` | App Bridge Title Bar API |
| `Loading` | App Bridge Loading API |

```jsx
// Example: Using App Bridge for Modal (instead of deprecated Polaris Modal)
import { Modal, TitleBar } from '@shopify/app-bridge-react';

function MyComponent() {
  return (
    <Modal id="my-modal">
      <TitleBar title="Confirm Action">
        <button variant="primary" onClick={handleConfirm}>Confirm</button>
        <button onClick={handleCancel}>Cancel</button>
      </TitleBar>
      <p>Are you sure you want to proceed?</p>
    </Modal>
  );
}

// Example: Using App Bridge for Toast
import { useAppBridge } from '@shopify/app-bridge-react';

function showToast() {
  shopify.toast.show('Product saved successfully');
}

// Example: Using App Bridge Save Bar
import { useSaveBar } from '@shopify/app-bridge-react';

function SettingsForm() {
  const saveBar = useSaveBar();

  useEffect(() => {
    if (hasChanges) {
      saveBar.show();
    } else {
      saveBar.hide();
    }
  }, [hasChanges]);
}
```

### Fundamental Components

- **AppProvider**: All Polaris apps must be wrapped in `<AppProvider i18n={enTranslations}>`.
- **Page**: The top-level container for a route. Always set `title` and `primaryAction` (if applicable).
  ```jsx
  <Page
    title="Products"
    primaryAction={{content: 'Add product', onAction: handleAdd}}
    backAction={{content: 'Settings', url: '/settings'}}
  >
  ```
  > **v13.x Note**: `backAction` prop in `Page.Header` is deprecated. Use App Bridge navigation instead for complex navigation patterns.

- **Layout**: Use `Layout` and `Layout.Section` to structure content.
    - `Layout.AnnotatedSection`: For settings pages (Title/Description on left, Card on right).
    - `Layout.Section`: Standard Full (default), 1/2 (`variant="oneHalf"`), or 1/3 (`variant="oneThird"`) width columns.
- **Card**: The primary container for content pieces. Group related information in a Card.
    - Use `BlockStack` (vertical) or `InlineStack` (horizontal) for internal layout within a Card.
    - **Do not** use `LegacyCard` - it is deprecated. Use `Card` with layout primitives.

### Layout Primitives (Modern Pattern)

```jsx
import { Box, BlockStack, InlineStack, InlineGrid, Bleed, Divider } from '@shopify/polaris';

// Box - Low-level layout primitive with full token access
<Box padding="400" background="bg-surface-secondary" borderRadius="200">
  Content here
</Box>

// BlockStack - Vertical stacking with gap
<BlockStack gap="400">
  <Item1 />
  <Item2 />
</BlockStack>

// InlineStack - Horizontal layout with alignment
<InlineStack gap="200" align="center" blockAlign="center">
  <Icon />
  <Text>Label</Text>
</InlineStack>

// InlineGrid - Responsive grid layout
<InlineGrid columns={{xs: 1, sm: 2, md: 3}} gap="400">
  <Card>...</Card>
  <Card>...</Card>
  <Card>...</Card>
</InlineGrid>

// Bleed - Negative margin for edge-to-edge content
<Card>
  <Bleed marginInline="400">
    <img src="banner.jpg" style={{width: '100%'}} />
  </Bleed>
</Card>
```

### Data Display

- **IndexTable**: For lists of objects (Products, Orders) with bulk actions and filtering.
  ```jsx
  import { IndexTable, Card, Text, Badge, useIndexResourceState } from '@shopify/polaris';

  function ProductList({ products }) {
    const { selectedResources, allResourcesSelected, handleSelectionChange } =
      useIndexResourceState(products);

    const rowMarkup = products.map((product, index) => (
      <IndexTable.Row
        id={product.id}
        key={product.id}
        selected={selectedResources.includes(product.id)}
        position={index}
      >
        <IndexTable.Cell>
          <Text variant="bodyMd" fontWeight="bold">{product.name}</Text>
        </IndexTable.Cell>
        <IndexTable.Cell>{product.sku}</IndexTable.Cell>
        <IndexTable.Cell>
          <Badge tone={product.status === 'active' ? 'success' : 'info'}>
            {product.status}
          </Badge>
        </IndexTable.Cell>
      </IndexTable.Row>
    ));

    return (
      <Card padding="0">
        <IndexTable
          resourceName={{singular: 'product', plural: 'products'}}
          itemCount={products.length}
          selectedItemsCount={allResourcesSelected ? 'All' : selectedResources.length}
          onSelectionChange={handleSelectionChange}
          headings={[
            {title: 'Name'},
            {title: 'SKU'},
            {title: 'Status'},
          ]}
        >
          {rowMarkup}
        </IndexTable>
      </Card>
    );
  }
  ```

- **DataTable**: For simple, non-interactive data grids (e.g., analytics data).
- **ResourceList**: For simpler lists without table structure (use `ResourceItem` for each item).

### Form Design

```jsx
import {
  Form, FormLayout, TextField, Select, Checkbox,
  ChoiceList, RadioButton, RangeSlider, ColorPicker,
  DropZone, Tag, Autocomplete
} from '@shopify/polaris';

function ProductForm() {
  const [formState, setFormState] = useState({
    title: '',
    description: '',
    status: 'draft',
    tags: [],
  });
  const [errors, setErrors] = useState({});

  return (
    <Form onSubmit={handleSubmit}>
      <FormLayout>
        <TextField
          label="Product title"
          value={formState.title}
          onChange={(value) => setFormState({...formState, title: value})}
          error={errors.title}
          autoComplete="off"
          helpText="This will be displayed to customers"
        />

        <TextField
          label="Description"
          value={formState.description}
          onChange={(value) => setFormState({...formState, description: value})}
          multiline={4}
          autoComplete="off"
        />

        <Select
          label="Status"
          options={[
            {label: 'Draft', value: 'draft'},
            {label: 'Active', value: 'active'},
            {label: 'Archived', value: 'archived'},
          ]}
          value={formState.status}
          onChange={(value) => setFormState({...formState, status: value})}
        />

        <FormLayout.Group>
          <TextField label="Price" type="number" prefix="$" />
          <TextField label="Compare at price" type="number" prefix="$" />
        </FormLayout.Group>

        <ChoiceList
          title="Availability"
          choices={[
            {label: 'Online Store', value: 'online'},
            {label: 'Point of Sale', value: 'pos'},
            {label: 'Buy Button', value: 'buy_button'},
          ]}
          selected={formState.channels}
          onChange={(value) => setFormState({...formState, channels: value})}
          allowMultiple
        />
      </FormLayout>
    </Form>
  );
}
```

### Filters & Search (IndexFilters)

```jsx
import {
  IndexFilters, useSetIndexFiltersMode, IndexFiltersMode,
  ChoiceList, RangeSlider, TextField
} from '@shopify/polaris';

function FilteredList() {
  const [queryValue, setQueryValue] = useState('');
  const [status, setStatus] = useState([]);
  const { mode, setMode } = useSetIndexFiltersMode(IndexFiltersMode.Filtering);

  const filters = [
    {
      key: 'status',
      label: 'Status',
      filter: (
        <ChoiceList
          title="Status"
          titleHidden
          choices={[
            {label: 'Active', value: 'active'},
            {label: 'Draft', value: 'draft'},
            {label: 'Archived', value: 'archived'},
          ]}
          selected={status}
          onChange={setStatus}
          allowMultiple
        />
      ),
      shortcut: true,
    },
  ];

  const appliedFilters = status.length > 0
    ? [{key: 'status', label: `Status: ${status.join(', ')}`}]
    : [];

  return (
    <IndexFilters
      queryValue={queryValue}
      queryPlaceholder="Search products"
      onQueryChange={setQueryValue}
      onQueryClear={() => setQueryValue('')}
      filters={filters}
      appliedFilters={appliedFilters}
      onClearAll={() => setStatus([])}
      mode={mode}
      setMode={setMode}
      tabs={[
        {content: 'All', id: 'all'},
        {content: 'Active', id: 'active'},
        {content: 'Draft', id: 'draft'},
      ]}
      selected={0}
    />
  );
}
```

## Design Tokens & CSS (v13.x)

- **Avoid Custom CSS**: 95% of styling should be handled by Polaris props (`gap`, `padding`, `align`, `justify`).
- **Design Tokens**: If you MUST use custom CSS, use Polaris CSS Custom Properties (Tokens).

### Spacing Tokens (4px base)

| Token | Value | Usage |
|-------|-------|-------|
| `--p-space-050` | 2px | Minimal spacing |
| `--p-space-100` | 4px | Tight spacing |
| `--p-space-200` | 8px | Compact spacing |
| `--p-space-300` | 12px | Default small |
| `--p-space-400` | 16px | **Default standard** |
| `--p-space-500` | 20px | Medium spacing |
| `--p-space-600` | 24px | Large spacing |
| `--p-space-800` | 32px | Section spacing |
| `--p-space-1000` | 40px | Page spacing |
| `--p-space-1200` | 48px | Extra large |

### Color Tokens

```css
/* Backgrounds */
--p-color-bg                     /* Default page background */
--p-color-bg-surface             /* Card/surface background */
--p-color-bg-surface-secondary   /* Secondary surface */
--p-color-bg-surface-hover       /* Hover state */
--p-color-bg-surface-selected    /* Selected state */
--p-color-bg-fill-brand          /* Primary brand fill */
--p-color-bg-fill-success        /* Success background */
--p-color-bg-fill-warning        /* Warning background */
--p-color-bg-fill-critical       /* Critical/error background */

/* Text */
--p-color-text                   /* Default text */
--p-color-text-secondary         /* Subdued text */
--p-color-text-disabled          /* Disabled text */
--p-color-text-brand             /* Brand colored text */
--p-color-text-success           /* Success text */
--p-color-text-warning           /* Warning text */
--p-color-text-critical          /* Error text */

/* Borders */
--p-color-border                 /* Default border */
--p-color-border-hover           /* Hover border */
--p-color-border-focus           /* Focus ring */
--p-color-border-brand           /* Brand border */
```

### Border Radius Tokens

```css
--p-border-radius-100    /* 4px - Small elements */
--p-border-radius-200    /* 8px - Cards, buttons */
--p-border-radius-300    /* 12px - Large cards */
--p-border-radius-full   /* 9999px - Pills, avatars */
```

### Shadow Tokens

```css
--p-shadow-100   /* Subtle shadow */
--p-shadow-200   /* Card shadow */
--p-shadow-300   /* Elevated shadow */
--p-shadow-400   /* Modal shadow */
```

### Typography

```jsx
// Use Text component with variants instead of HTML tags
<Text variant="headingXl">Page Title</Text>      // 28px bold
<Text variant="headingLg">Section Title</Text>   // 24px bold
<Text variant="headingMd">Card Title</Text>      // 20px semibold
<Text variant="headingSm">Subsection</Text>      // 16px semibold
<Text variant="headingXs">Small Header</Text>    // 14px semibold
<Text variant="bodyLg">Large body</Text>         // 16px regular
<Text variant="bodyMd">Default body</Text>       // 14px regular
<Text variant="bodySm">Small text</Text>         // 12px regular

// Tones for semantic meaning
<Text tone="subdued">Secondary information</Text>
<Text tone="success">Success message</Text>
<Text tone="critical">Error message</Text>
<Text tone="caution">Warning message</Text>
```

## Deprecated Components (v13.x) - DO NOT USE

These components will be removed in future versions:

| Deprecated | Use Instead |
|------------|-------------|
| `LegacyCard` | `Card` + `BlockStack` |
| `LegacyStack` | `BlockStack` / `InlineStack` |
| `LegacyFilters` | `IndexFilters` |
| `LegacyTabs` | `Tabs` |
| `Modal` | App Bridge Modal API |
| `Navigation` | App Bridge Navigation Menu |
| `Toast` | App Bridge Toast API |
| `ContextualSaveBar` | App Bridge `useSaveBar()` |
| `TopBar` | App Bridge Title Bar |
| `Loading` | App Bridge Loading API |
| `Frame` | App Bridge handles this |
| `Sheet` | App Bridge Modal or custom |
| `DisplayText` | `Text` with `variant="heading*"` |
| `Heading` | `Text` with `variant="heading*"` |
| `Subheading` | `Text` with `variant="headingSm"` |
| `Caption` | `Text` with `variant="bodySm"` |
| `TextStyle` | `Text` with `tone` prop |
| `TextContainer` | `BlockStack` with gap |
| `SettingToggle` | Custom with `Card` + `InlineStack` + `Button` |
| `PageActions` | `Page` `primaryAction`/`secondaryActions` props |
| `VisuallyHidden` | Use `visuallyHidden` prop on Text |

## Code Style Example (v13.x Best Practices)

```jsx
import {
  Page, Layout, Card, BlockStack, InlineStack,
  Text, Button, Badge, Box, Divider, Banner,
  IndexTable, useIndexResourceState
} from '@shopify/polaris';
import { ExportIcon, PlusIcon } from '@shopify/polaris-icons';

export default function Dashboard({ products }) {
  const { selectedResources, allResourcesSelected, handleSelectionChange } =
    useIndexResourceState(products);

  const promotedBulkActions = [
    { content: 'Export selected', icon: ExportIcon },
  ];

  const rowMarkup = products.map((product, index) => (
    <IndexTable.Row
      id={product.id}
      key={product.id}
      selected={selectedResources.includes(product.id)}
      position={index}
    >
      <IndexTable.Cell>
        <Text variant="bodyMd" fontWeight="bold">{product.title}</Text>
      </IndexTable.Cell>
      <IndexTable.Cell>
        <Badge tone={product.status === 'active' ? 'success' : 'info'}>
          {product.status}
        </Badge>
      </IndexTable.Cell>
      <IndexTable.Cell>${product.price}</IndexTable.Cell>
    </IndexTable.Row>
  ));

  return (
    <Page
      title="Dashboard"
      primaryAction={{
        content: 'Add product',
        icon: PlusIcon,
        onAction: () => {}
      }}
      secondaryActions={[
        {content: 'Export', icon: ExportIcon, onAction: () => {}}
      ]}
    >
      <Layout>
        <Layout.Section>
          <Banner tone="info" onDismiss={() => {}}>
            <p>New: Try our improved bulk editing features.</p>
          </Banner>
        </Layout.Section>

        <Layout.Section>
          <Card padding="0">
            <IndexTable
              resourceName={{singular: 'product', plural: 'products'}}
              itemCount={products.length}
              selectedItemsCount={allResourcesSelected ? 'All' : selectedResources.length}
              onSelectionChange={handleSelectionChange}
              headings={[
                {title: 'Product'},
                {title: 'Status'},
                {title: 'Price', alignment: 'end'},
              ]}
              promotedBulkActions={promotedBulkActions}
            >
              {rowMarkup}
            </IndexTable>
          </Card>
        </Layout.Section>

        <Layout.Section variant="oneThird">
          <Card>
            <BlockStack gap="400">
              <Text as="h2" variant="headingMd">Quick Stats</Text>
              <Divider />
              <BlockStack gap="200">
                <InlineStack align="space-between">
                  <Text tone="subdued">Total products</Text>
                  <Text fontWeight="semibold">{products.length}</Text>
                </InlineStack>
                <InlineStack align="space-between">
                  <Text tone="subdued">Active</Text>
                  <Text fontWeight="semibold">
                    {products.filter(p => p.status === 'active').length}
                  </Text>
                </InlineStack>
              </BlockStack>
            </BlockStack>
          </Card>

          <Box paddingBlockStart="400">
            <Card>
              <BlockStack gap="300">
                <Text as="h3" variant="headingSm">Quick Actions</Text>
                <Button variant="plain" url="/settings">
                  View all settings
                </Button>
              </BlockStack>
            </Card>
          </Box>
        </Layout.Section>
      </Layout>
    </Page>
  );
}
```

## Anti-Patterns to AVOID

- **DO NOT** use deprecated components (`LegacyCard`, `Modal`, `Toast`, etc.).
- **DO NOT** use Shadows or Borders manually. Cards handle this.
- **DO NOT** use `style={{ margin: 10 }}`. Use `<Box padding="400">` or `<BlockStack gap="400">`.
- **DO NOT** create a "Save" button at the bottom of a form. Use App Bridge Save Bar.
- **DO NOT** use generic loading spinners. Use `<SkeletonPage>` or `<SkeletonBodyText>` for loading states.
- **DO NOT** use `<h1>`, `<h2>`, etc. directly. Use `<Text as="h2" variant="headingMd">`.
- **DO NOT** use inline styles. Use Box/BlockStack props or design tokens.
- **DO NOT** import from `@shopify/polaris/build/esm/...`. Use named exports from `@shopify/polaris`.

## Internationalization Support (v13.10+)

Polaris v13.10 added translations for 8 new languages: Hindi, Lithuanian, Bulgarian, Hungarian, Romanian, Russian, Indonesian, and Greek.

```jsx
import enTranslations from '@shopify/polaris/locales/en.json';
import viTranslations from '@shopify/polaris/locales/vi.json';

// Use the appropriate translations based on merchant locale
<AppProvider i18n={merchantLocale === 'vi' ? viTranslations : enTranslations}>
  <App />
</AppProvider>
```

## Resources

- [Polaris React Components](https://polaris-react.shopify.com/components)
- [Polaris Icons](https://polaris.shopify.com/icons)
- [Polaris Design Tokens](https://polaris.shopify.com/tokens)
- [App Bridge React](https://shopify.dev/docs/api/app-bridge-library)
