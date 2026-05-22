---
name: shopify-polaris-icons
description: Guide for using Shopify Polaris Icons in Shopify Apps. Covers icon usage patterns, accessibility, tone variants, and common icon categories for commerce applications.
---

# Shopify Polaris Icons Skill

Polaris Icons is Shopify's official icon library with **400+ carefully designed icons** focused on commerce and entrepreneurship. These icons are designed to work seamlessly with the Polaris Design System.

## Installation

```bash
npm install @shopify/polaris-icons
# or
yarn add @shopify/polaris-icons
```

> [!NOTE]
> The `@shopify/polaris-icons` package is typically installed alongside `@shopify/polaris`. If you're using Polaris, you likely already have access to these icons.

## Basic Usage

### With Polaris Icon Component (Recommended)

```jsx
import { Icon } from '@shopify/polaris';
import { PlusCircleIcon } from '@shopify/polaris-icons';

function MyComponent() {
  return <Icon source={PlusCircleIcon} />;
}
```

### With Accessibility Label

When an icon appears without accompanying text, **always** provide an accessibility label:

```jsx
import { Icon } from '@shopify/polaris';
import { DeleteIcon } from '@shopify/polaris-icons';

function DeleteButton() {
  return (
    <button>
      <Icon source={DeleteIcon} accessibilityLabel="Delete item" />
    </button>
  );
}
```

### Icon Tones

Use the `tone` prop to set the icon color semantically:

```jsx
import { Icon } from '@shopify/polaris';
import { AlertCircleIcon, CheckCircleIcon, InfoIcon } from '@shopify/polaris-icons';

// Available tones
<Icon source={CheckCircleIcon} tone="success" />    // Green - positive actions
<Icon source={AlertCircleIcon} tone="critical" />   // Red - errors, destructive
<Icon source={AlertCircleIcon} tone="warning" />    // Yellow - warnings
<Icon source={AlertCircleIcon} tone="caution" />    // Orange - caution
<Icon source={InfoIcon} tone="info" />              // Blue - information
<Icon source={InfoIcon} tone="base" />              // Default text color
<Icon source={InfoIcon} tone="subdued" />           // Muted/secondary
<Icon source={InfoIcon} tone="interactive" />       // Link/action color
<Icon source={InfoIcon} tone="inherit" />           // Inherit from parent
<Icon source={InfoIcon} tone="magic" />             // AI/Magic features
<Icon source={InfoIcon} tone="emphasis" />          // Emphasized content
<Icon source={InfoIcon} tone="primary" />           // Primary brand color
```

## Icon Naming Convention

All icons follow a consistent naming pattern: `{Name}Icon`

```jsx
// Examples
import {
  HomeIcon,           // Navigation
  ProductIcon,        // Commerce
  OrderIcon,          // Orders
  CustomerIcon,       // Customers
  SettingsIcon,       // Settings
  PlusIcon,           // Actions
  EditIcon,           // Actions
  DeleteIcon,         // Actions
  SearchIcon,         // Search
  FilterIcon,         // Filtering
} from '@shopify/polaris-icons';
```

## Common Icon Categories

### Navigation & Layout
```jsx
import {
  HomeIcon,
  MenuIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  ChevronUpIcon,
  ChevronDownIcon,
  ArrowLeftIcon,
  ArrowRightIcon,
  ExternalIcon,
  MaximizeIcon,
  MinimizeIcon,
} from '@shopify/polaris-icons';
```

### Commerce & Products
```jsx
import {
  ProductIcon,
  CollectionIcon,
  InventoryIcon,
  PriceTagIcon,          // Renamed from TagIcon
  GiftCardIcon,
  DiscountIcon,
  CartIcon,
  CartAbandonedIcon,
  StorefrontIcon,
} from '@shopify/polaris-icons';
```

### Orders & Fulfillment
```jsx
import {
  OrderIcon,
  OrderDraftIcon,
  OrderFulfilledIcon,
  DeliveryIcon,
  ShippingLabelIcon,
  PackageIcon,
  ReturnIcon,
  RefundIcon,
} from '@shopify/polaris-icons';
```

### Customers & Users
```jsx
import {
  CustomerIcon,
  CustomerPlusIcon,
  PersonIcon,
  PersonAddIcon,
  TeamIcon,
  ProfileIcon,
} from '@shopify/polaris-icons';
```

### Actions
```jsx
import {
  PlusIcon,
  PlusCircleIcon,
  MinusIcon,
  MinusCircleIcon,
  EditIcon,
  DeleteIcon,
  DuplicateIcon,
  ArchiveIcon,
  SaveIcon,
  UndoIcon,
  RedoIcon,
  RefreshIcon,
  ImportIcon,
  ExportIcon,
  UploadIcon,
  DownloadIcon,
} from '@shopify/polaris-icons';
```

### Status & Feedback
```jsx
import {
  CheckIcon,
  CheckCircleIcon,
  XIcon,
  XCircleIcon,
  AlertCircleIcon,
  AlertTriangleIcon,
  InfoIcon,
  QuestionCircleIcon,
  ClockIcon,
  CalendarIcon,
} from '@shopify/polaris-icons';
```

### Communication
```jsx
import {
  EmailIcon,
  ChatIcon,
  NotificationIcon,
  BellIcon,
  PhoneIcon,
  SendIcon,
  NoteIcon,
} from '@shopify/polaris-icons';
```

### Settings & Tools
```jsx
import {
  SettingsIcon,
  ToolsIcon,
  KeyIcon,
  LockIcon,
  UnlockIcon,
  EyeIcon,
  HideIcon,
  FilterIcon,
  SortIcon,
  SearchIcon,
  CodeIcon,
  ApiIcon,
} from '@shopify/polaris-icons';
```

### Analytics & Reports
```jsx
import {
  AnalyticsIcon,
  ChartVerticalIcon,
  ChartHorizontalIcon,
  ReportIcon,
  TrendingUpIcon,
  TrendingDownIcon,
} from '@shopify/polaris-icons';
```

### Media
```jsx
import {
  ImageIcon,
  ImageAltIcon,
  VideoIcon,
  FileIcon,
  FolderIcon,
  AttachmentIcon,
  LinkIcon,
} from '@shopify/polaris-icons';
```

### AI & Magic (Shopify Magic)
```jsx
import {
  MagicIcon,
  SparklesIcon,        // AI-generated content
  WandIcon,
} from '@shopify/polaris-icons';
```

## Usage in Polaris Components

### Button with Icon

```jsx
import { Button } from '@shopify/polaris';
import { PlusIcon, DeleteIcon } from '@shopify/polaris-icons';

// Icon before text
<Button icon={PlusIcon}>Add product</Button>

// Destructive action
<Button icon={DeleteIcon} variant="primary" tone="critical">
  Delete
</Button>

// Icon-only button (requires accessibilityLabel)
<Button icon={EditIcon} accessibilityLabel="Edit product" />
```

### TextField with Icon

```jsx
import { TextField } from '@shopify/polaris';
import { SearchIcon } from '@shopify/polaris-icons';

<TextField
  label="Search"
  prefix={<Icon source={SearchIcon} />}
  placeholder="Search products..."
/>
```

### Banner with Icon

```jsx
import { Banner, Icon } from '@shopify/polaris';
import { AlertCircleIcon } from '@shopify/polaris-icons';

<Banner
  title="Warning"
  tone="warning"
  icon={AlertCircleIcon}
>
  Please review your settings.
</Banner>
```

### Navigation Item

```jsx
import { Navigation } from '@shopify/polaris';
import { HomeIcon, OrderIcon, ProductIcon } from '@shopify/polaris-icons';

<Navigation location="/">
  <Navigation.Section
    items={[
      { label: 'Home', icon: HomeIcon, url: '/' },
      { label: 'Orders', icon: OrderIcon, url: '/orders' },
      { label: 'Products', icon: ProductIcon, url: '/products' },
    ]}
  />
</Navigation>
```

## Accessibility Best Practices

1. **Decorative Icons**: When an icon accompanies text that already describes the action, the icon is decorative and doesn't need a label:
   ```jsx
   <Button icon={PlusIcon}>Add product</Button>
   // No accessibilityLabel needed - "Add product" describes the action
   ```

2. **Standalone Icons**: When an icon appears without text, always provide an `accessibilityLabel`:
   ```jsx
   <Button icon={EditIcon} accessibilityLabel="Edit product" />
   ```

3. **Status Icons**: For icons that convey important status information:
   ```jsx
   <Icon source={CheckCircleIcon} tone="success" accessibilityLabel="Completed" />
   ```

## Anti-Patterns to Avoid

- **DO NOT** use icons without context. Pair with text or provide accessibility labels.
- **DO NOT** use non-Polaris icons in a Polaris app. This breaks visual consistency.
- **DO NOT** manually set icon colors with CSS. Use the `tone` prop instead.
- **DO NOT** resize icons using CSS. Polaris icons are designed for a 20x20 viewport.
- **DO NOT** use icons for decoration only. Each icon should have semantic meaning.

## References

- [Icon Categories](./references/icon-categories.md) - Complete categorized list of all Polaris icons
- [Migration Guide](./references/migration-guide.md) - Guide for migrating from older icon versions

## External Resources

- [Polaris Icons Browser](https://polaris.shopify.com/icons) - Search and browse all icons
- [Icon Component Docs](https://polaris.shopify.com/components/images-and-icons/icon) - Official component documentation
- [NPM Package](https://www.npmjs.com/package/@shopify/polaris-icons) - Package information and changelog
