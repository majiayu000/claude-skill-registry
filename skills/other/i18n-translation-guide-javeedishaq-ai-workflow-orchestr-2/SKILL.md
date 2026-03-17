---
name: "i18n-translation-guide"
description: "Implement internationalization (i18n) in Ballee using react-i18next with Trans component and useTranslation hook; use when adding user-facing text, translating components, implementing toast messages, or organizing translation files"
version: "1.0.0"
last_updated: "2025-12-03"
---

# i18n Translation Guide

**Purpose**: Comprehensive guide for implementing internationalization (i18n) in Ballee using react-i18next

**When to Use**: When adding user-facing text, creating UI components, implementing toast messages, or translating existing hardcoded text

---

## Overview

Ballee uses **react-i18next** with the **Trans component** from `@kit/ui/trans` for all internationalization. This skill provides battle-tested patterns from translating 100+ strings across marketing pages and admin dialogs.

### Framework Stack
- **Library**: react-i18next + i18next
- **Component**: `<Trans>` from `@kit/ui/trans`
- **Hook**: `useTranslation()` from `react-i18next`
- **Translation Files**: `apps/web/public/locales/en/*.json`

---

## Core Patterns

### Pattern 1: UI Components (JSX)

Use `<Trans>` component for all JSX elements (titles, labels, buttons, etc.)

```tsx
import { Trans } from '@kit/ui/trans';

// Simple text
<h1><Trans i18nKey="marketing:home.hero.headline" /></h1>

// With variable interpolation
<Trans
  i18nKey="admin:clients.confirmDialog.delete.description"
  values={{ name: clientName }}
/>

// Translation: "Are you sure you want to delete "{{name}}"?"
```

**When to Use**:
- ✅ Dialog titles/descriptions
- ✅ Form labels
- ✅ Button text
- ✅ Page headings
- ✅ Empty state messages
- ✅ Table column headers

### Pattern 2: Toast Messages (Strings)

⚠️ **CRITICAL**: Toast messages require the `useTranslation` hook because they expect strings, not JSX.

```tsx
import { useTranslation } from 'react-i18next';
import { toast } from '@kit/ui/sonner';

function MyComponent() {
  const { t } = useTranslation();

  const handleAction = async () => {
    // ❌ WRONG - Toast doesn't accept JSX
    toast.success(<Trans i18nKey="admin:clients.toast.created" />);

    // ✅ CORRECT - Use t() function
    toast.success(t('admin:clients.toast.created'));

    // With interpolation
    toast.loading(t('admin:clients.toast.switchingTo', { name: clientName }));
  };
}
```

**When to Use `t()` instead of `<Trans>`**:
- ✅ Toast messages (success, error, loading)
- ✅ Input placeholders (`placeholder={t('...')}`)
- ✅ Accessibility attributes (`aria-label={t('...')}`)
- ✅ Any prop that expects a string, not JSX

### Pattern 3: Server Components

For Next.js server components, use `withI18n` HOC wrapper:

```tsx
import { withI18n } from '~/lib/i18n/with-i18n';
import { Trans } from '@kit/ui/trans';

function ServerPage() {
  return (
    <div>
      <Trans i18nKey="marketing:home.hero.headline" />
    </div>
  );
}

export default withI18n(ServerPage);
```

---

## Translation File Organization

### Namespace Structure

Follow hierarchical naming: `namespace:category.subcategory.key`

```json
// apps/web/public/locales/en/admin.json
{
  "clients": {
    "title": "Clients",
    "createDialog": {
      "title": "Create Client",
      "description": "Add a new client account..."
    },
    "form": {
      "name": "Name",
      "slug": "Slug",
      "email": "Email"
    },
    "buttons": {
      "create": "Create Client",
      "creating": "Creating...",
      "save": "Save Changes",
      "saving": "Saving..."
    },
    "toast": {
      "created": "Client created successfully",
      "createFailed": "Failed to create client",
      "switchingTo": "Switching to {{name}}...",
      "switchedTo": "Switched to {{name}}"
    },
    "table": {
      "name": "Name",
      "slug": "Slug",
      "email": "Email",
      "actions": "Actions",
      "searchPlaceholder": "Search clients..."
    },
    "actions": {
      "edit": "Edit",
      "delete": "Delete",
      "openMenu": "Open menu"
    },
    "empty": {
      "title": "No clients yet",
      "description": "Create your first client to get started"
    },
    "confirmDialog": {
      "delete": {
        "title": "Delete Client",
        "description": "Are you sure you want to delete \"{{name}}\"?..."
      }
    }
  }
}
```

### Namespace Guidelines

**common.json** - Shared UI elements across the app
```json
{
  "buttons": {
    "create": "Create", "creating": "Creating...",
    "save": "Save", "saving": "Saving...",
    "delete": "Delete", "deleting": "Deleting...",
    "cancel": "Cancel", "confirm": "Confirm",
    "retry": "Retry", "close": "Close"
  },
  "form": {
    "name": "Name", "email": "Email",
    "notes": "Notes", "notesOptional": "Notes (optional)",
    "description": "Description"
  },
  "dialog": {
    "confirm": "Are you sure?",
    "warning": "This action cannot be undone"
  },
  "toast": {
    "deleteSuccess": "Deleted successfully",
    "updateSuccess": "Updated successfully"
  },
  "empty": {
    "noItems": "No items found",
    "noResults": "No results found"
  },
  "loading": {
    "default": "Loading...",
    "data": "Loading data..."
  },
  "accessibility": {
    "closeDialog": "Close dialog",
    "openMenu": "Open menu"
  }
}
```

**marketing.json** - Public marketing pages
```json
{
  "home": { "hero": {...}, "features": {...} },
  "contact": { "hero": {...}, "methods": {...}, "form": {...} },
  "about": { "hero": {...}, "story": {...}, "values": {...} },
  "services": { "hero": {...}, "list": {...}, "whyChooseUs": {...} }
}
```

**admin.json** - Admin section (super admin)
```json
{
  "common": { "buttons": {...}, "dialog": {...} },
  "clients": { "createDialog": {...}, "table": {...}, "toast": {...} },
  "events": { "cast": {...}, "table": {...}, "toast": {...} },
  "productions": { "form": {...}, "detail": {...} }
}
```

**user.json** - Dancer/user section
```json
{
  "events": { "participation": {...}, "detail": {...} },
  "assignments": { "contract": {...} },
  "reimbursements": { "detail": {...}, "dialog": {...} }
}
```

---

## Common UI Patterns

### Empty States

```tsx
// Pattern: Icon + Title + Description
<div className="py-8 text-center">
  <Building2 className="text-muted-foreground mx-auto mb-4 h-12 w-12" />
  <h3 className="text-muted-foreground text-lg font-medium">
    <Trans i18nKey="admin:clients.empty.title" />
  </h3>
  <p className="text-muted-foreground mt-2 text-sm">
    <Trans i18nKey="admin:clients.empty.description" />
  </p>
</div>
```

### Form Fields

```tsx
<FormField
  control={form.control}
  name="name"
  render={({ field }) => (
    <FormItem>
      <FormLabel>
        <Trans i18nKey="admin:clients.form.name" />
      </FormLabel>
      <FormControl>
        <Input
          placeholder="Fever" // ⚠️ Consider: translate or leave hardcoded?
          {...field}
        />
      </FormControl>
      <FormDescription>
        The display name of the client  {/* ⚠️ Consider: translate or leave? */}
      </FormDescription>
      <FormMessage />
    </FormItem>
  )}
/>
```

**Form Field Translation Considerations**:
- **Labels**: Always translate (`<Trans i18nKey="..." />`)
- **Placeholders**: Optional - depends on whether they're example data or instructional
  - Example data (e.g., "Fever", "john@example.com"): Leave hardcoded
  - Instructions (e.g., "Enter your email"): Translate
- **FormDescription**: Optional - translate if it's important user guidance

### Conditional Button States

```tsx
<Button type="submit" disabled={isSubmitting}>
  {isSubmitting ? (
    <Trans i18nKey="admin:clients.buttons.creating" />
  ) : (
    <Trans i18nKey="admin:clients.buttons.create" />
  )}
</Button>
```

### Table Columns with Translation

When defining table columns, pass the `t` function as a parameter:

```tsx
import { useTranslation } from 'react-i18next';

function MyTable() {
  const { t } = useTranslation();

  const columns = getColumns(t, ...otherParams);

  return <DataTable columns={columns} data={data} />;
}

function getColumns(
  t: (key: string) => string,
  // ...other params
): ColumnDef<MyType>[] {
  return [
    {
      id: 'name',
      header: t('admin:clients.table.name'),
      cell: ({ row }) => (
        <div>
          {row.original.name}
          {isActive && (
            <Badge>
              {t('admin:clients.table.active')}
            </Badge>
          )}
        </div>
      ),
    },
    {
      id: 'actions',
      header: t('admin:clients.table.actions'),
      cell: ({ row }) => (
        <DropdownMenu>
          <DropdownMenuTrigger>
            <span className="sr-only">{t('admin:clients.actions.openMenu')}</span>
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            <DropdownMenuItem>{t('admin:clients.actions.edit')}</DropdownMenuItem>
            <DropdownMenuItem>{t('admin:clients.actions.delete')}</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      ),
    },
  ];
}
```

### Dialog Patterns

```tsx
<Dialog open={open} onOpenChange={setOpen}>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>
        <Trans i18nKey="admin:clients.createDialog.title" />
      </DialogTitle>
      <DialogDescription>
        <Trans i18nKey="admin:clients.createDialog.description" />
      </DialogDescription>
    </DialogHeader>

    {/* Form content */}

    <DialogFooter>
      <Button variant="outline" onClick={() => setOpen(false)}>
        <Trans i18nKey="common:buttons.cancel" />
      </Button>
      <Button type="submit" disabled={isSubmitting}>
        {isSubmitting ? (
          <Trans i18nKey="admin:clients.buttons.saving" />
        ) : (
          <Trans i18nKey="admin:clients.buttons.save" />
        )}
      </Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Confirmation Dialogs

```tsx
<AlertDialog open={!!itemToDelete} onOpenChange={...}>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>
        <Trans i18nKey="admin:clients.confirmDialog.delete.title" />
      </AlertDialogTitle>
      <AlertDialogDescription>
        <Trans
          i18nKey="admin:clients.confirmDialog.delete.description"
          values={{ name: itemToDelete?.name }}
        />
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel disabled={isDeleting}>
        <Trans i18nKey="common:buttons.cancel" />
      </AlertDialogCancel>
      <AlertDialogAction
        onClick={handleDelete}
        disabled={isDeleting}
        className="bg-destructive text-destructive-foreground"
      >
        {isDeleting ? (
          <Trans i18nKey="common:buttons.deleting" />
        ) : (
          <Trans i18nKey="common:buttons.delete" />
        )}
      </AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

---

## Accessibility Text

Always translate sr-only text for screen readers:

```tsx
<Button variant="ghost" size="sm">
  <MoreHorizontal className="h-4 w-4" />
  <span className="sr-only">{t('admin:clients.actions.openMenu')}</span>
</Button>
```

---

## Search Input Placeholders

Use the `t()` function for placeholders:

```tsx
import { useTranslation } from 'react-i18next';

function MyTable() {
  const { t } = useTranslation();

  return (
    <TableSearchInput
      defaultValue={filters.search}
      placeholder={t('admin:clients.table.searchPlaceholder')}
      className="w-64"
    />
  );
}
```

---

## Variable Interpolation

### Simple Variables

```tsx
<Trans
  i18nKey="admin:clients.toast.switchedTo"
  values={{ name: clientName }}
/>

// Translation: "Switched to {{name}}"
// Output: "Switched to Fever"
```

### Multiple Variables

```tsx
<Trans
  i18nKey="admin:events.detail.info"
  values={{ date: eventDate, location: venueName }}
/>

// Translation: "Event on {{date}} at {{location}}"
// Output: "Event on 2025-11-23 at Opera House"
```

### With t() Function

```tsx
const { t } = useTranslation();

toast.success(t('admin:clients.toast.switchedTo', { name: clientName }));
```

---

## Migration Checklist

When translating existing components:

### Step 1: Identify Hardcoded Text
- [ ] Dialog titles/descriptions
- [ ] Form labels
- [ ] Button text (including conditional states: "Creating...", "Create")
- [ ] Toast messages
- [ ] Table column headers
- [ ] Empty state messages
- [ ] Search placeholders
- [ ] Accessibility text (sr-only)
- [ ] Action menu items

### Step 2: Add Imports

```tsx
// For UI components
import { Trans } from '@kit/ui/trans';

// For toast messages, placeholders, table columns
import { useTranslation } from 'react-i18next';
```

### Step 3: Add Translations to JSON Files

Choose the appropriate namespace:
- `common.json` - Shared UI (buttons, forms, dialogs)
- `admin.json` - Admin-specific features
- `marketing.json` - Public marketing pages
- `user.json` - Dancer/user features

### Step 4: Replace Hardcoded Text

```tsx
// Before
<DialogTitle>Create Client</DialogTitle>
<Button>{isSubmitting ? 'Creating...' : 'Create Client'}</Button>
toast.success('Client created successfully');

// After
<DialogTitle><Trans i18nKey="admin:clients.createDialog.title" /></DialogTitle>
<Button>
  {isSubmitting ? (
    <Trans i18nKey="admin:clients.buttons.creating" />
  ) : (
    <Trans i18nKey="admin:clients.buttons.create" />
  )}
</Button>

const { t } = useTranslation();
toast.success(t('admin:clients.toast.created'));
```

### Step 5: Validate JSON

```bash
# Validate JSON syntax
node -e "JSON.parse(require('fs').readFileSync('apps/web/public/locales/en/admin.json', 'utf8'))"
```

### Step 6: Test Build

```bash
pnpm build  # Ensure no translation errors
```

---

## Anti-Patterns (Don't Do This)

### ❌ Using Trans for Toast Messages

```tsx
// ❌ WRONG - Toast expects strings, not JSX
toast.success(<Trans i18nKey="admin:clients.toast.created" />);

// ✅ CORRECT
const { t } = useTranslation();
toast.success(t('admin:clients.toast.created'));
```

### ❌ Hardcoding Text in Shared Components

```tsx
// ❌ WRONG
<Button>Cancel</Button>
<Button>Delete</Button>

// ✅ CORRECT - Use common namespace
<Button><Trans i18nKey="common:buttons.cancel" /></Button>
<Button><Trans i18nKey="common:buttons.delete" /></Button>
```

### ❌ Duplicating Translations

```tsx
// ❌ WRONG - Duplicate "Cancel" across namespaces
// admin.json: { "buttons": { "cancel": "Cancel" } }
// user.json: { "buttons": { "cancel": "Cancel" } }

// ✅ CORRECT - Share common translations
<Trans i18nKey="common:buttons.cancel" />
```

### ❌ Not Translating Accessibility Text

```tsx
// ❌ WRONG
<span className="sr-only">Open menu</span>

// ✅ CORRECT
<span className="sr-only">{t('admin:clients.actions.openMenu')}</span>
```

### ❌ Using Defaults Instead of JSON Files

```tsx
// ❌ WRONG - Defaults bypass translation system
<Trans i18nKey="admin:clients.title" defaults="Clients" />

// ✅ CORRECT - Add to JSON file, no defaults
<Trans i18nKey="admin:clients.title" />

// admin.json: { "clients": { "title": "Clients" } }
```

---

## Quick Reference

| Use Case | Pattern | Example |
|----------|---------|---------|
| UI Text | `<Trans>` | `<Trans i18nKey="admin:clients.title" />` |
| Toast Messages | `t()` | `toast.success(t('admin:clients.toast.created'))` |
| Button States | Conditional `<Trans>` | `{isLoading ? <Trans i18nKey="..." /> : <Trans i18nKey="..." />}` |
| Table Headers | `t()` in column def | `header: t('admin:clients.table.name')` |
| Placeholders | `t()` in prop | `placeholder={t('...')}` |
| Accessibility | `t()` in sr-only | `<span className="sr-only">{t('...')}</span>` |
| Variables | `values` prop | `<Trans i18nKey="..." values={{ name }} />` |

---

## Examples from Production

### Marketing Page (Homepage)

```tsx
import { Trans } from '@kit/ui/trans';
import { withI18n } from '~/lib/i18n/with-i18n';

function HomePage() {
  return (
    <PrimaryHero
      eyebrow={<Trans i18nKey="marketing:home.hero.eyebrow" />}
      headline={<Trans i18nKey="marketing:home.hero.headline" />}
      subheadline={<Trans i18nKey="marketing:home.hero.subheadline" />}
    />
  );
}

export default withI18n(HomePage);
```

### Admin Dialog (Client Creation)

```tsx
import { useTranslation } from 'react-i18next';
import { Trans } from '@kit/ui/trans';

export function CreateClientDialog({ children }) {
  const { t } = useTranslation();

  const onSubmit = async (data) => {
    const result = await createClientAction(data);

    if (result.error) {
      toast.error(t('admin:clients.toast.createFailed'), {
        description: result.error,
      });
      return;
    }

    toast.success(t('admin:clients.toast.created'));
  };

  return (
    <Dialog>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>
            <Trans i18nKey="admin:clients.createDialog.title" />
          </DialogTitle>
          <DialogDescription>
            <Trans i18nKey="admin:clients.createDialog.description" />
          </DialogDescription>
        </DialogHeader>

        <Form onSubmit={onSubmit}>
          <FormField name="name">
            <FormLabel><Trans i18nKey="admin:clients.form.name" /></FormLabel>
            <Input placeholder="Fever" />
          </FormField>

          <DialogFooter>
            <Button variant="outline">
              <Trans i18nKey="common:buttons.cancel" />
            </Button>
            <Button type="submit">
              {isSubmitting ? (
                <Trans i18nKey="admin:clients.buttons.creating" />
              ) : (
                <Trans i18nKey="admin:clients.buttons.create" />
              )}
            </Button>
          </DialogFooter>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
```

### Data Table with Translations

```tsx
import { useTranslation } from 'react-i18next';
import { Trans } from '@kit/ui/trans';

export function ClientsTable({ clients }) {
  const { t } = useTranslation();

  const columns = getColumns(t, handleEdit, handleDelete);

  if (clients.length === 0) {
    return (
      <div className="text-center py-8">
        <h3><Trans i18nKey="admin:clients.empty.title" /></h3>
        <p><Trans i18nKey="admin:clients.empty.description" /></p>
      </div>
    );
  }

  return (
    <>
      <TableSearchInput
        placeholder={t('admin:clients.table.searchPlaceholder')}
      />
      <DataTable columns={columns} data={clients} />
    </>
  );
}

function getColumns(t, onEdit, onDelete) {
  return [
    {
      id: 'name',
      header: t('admin:clients.table.name'),
      cell: ({ row }) => row.original.name,
    },
    {
      id: 'actions',
      header: t('admin:clients.table.actions'),
      cell: ({ row }) => (
        <DropdownMenu>
          <DropdownMenuTrigger>
            <span className="sr-only">{t('admin:clients.actions.openMenu')}</span>
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            <DropdownMenuItem onClick={() => onEdit(row.original)}>
              {t('admin:clients.actions.edit')}
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => onDelete(row.original)}>
              {t('admin:clients.actions.delete')}
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      ),
    },
  ];
}
```

---

## Testing Translations

### Manual Testing
1. Check UI in browser - all text should render
2. Test toast messages - verify they show string content
3. Test empty states - verify messages display
4. Test table columns - verify headers show
5. Test button states - verify conditional text works

### Build Validation
```bash
pnpm build  # Ensure no missing translation errors
pnpm typecheck  # Ensure types are correct
```

### Translation Key Validation
```bash
# Check for unused translation keys
grep -r "i18nKey" apps/web/app | grep -o '"[^"]*"' | sort | uniq

# Check for missing translations
# (manual comparison with JSON files)
```

---

## Future Enhancements

1. **FormDescription Translation**: Decide whether to translate helper text under form fields
2. **Placeholder Translation**: Create guidelines for when to translate vs. leave hardcoded
3. **Dynamic Content**: Pattern for translating database-driven content
4. **Pluralization**: Handle singular/plural forms (e.g., "1 item" vs "5 items")
5. **Date/Number Formatting**: Locale-specific formatting patterns
6. **RTL Support**: Right-to-left language support guidelines

---

## Summary

**Quick Start**:
1. Import `<Trans>` for JSX, `useTranslation()` for strings
2. Add translations to appropriate namespace (`common`, `admin`, `marketing`, `user`)
3. Use `<Trans i18nKey="..." />` for UI components
4. Use `t('...')` for toast messages, placeholders, and string props
5. Always translate accessibility text
6. Test build and UI thoroughly

**Key Learnings**:
- Toast messages need `t()`, not `<Trans>`
- Table columns should use `t()` function passed as parameter
- Button states need conditional `<Trans>` components
- Shared UI elements belong in `common.json`
- Variable interpolation uses `values` prop

**Production Stats** (as of 2025-11-23):
- ✅ 100+ strings translated across marketing pages and admin dialogs
- ✅ Pattern validated across 8 TSX files
- ✅ 3 namespaces fully structured (common, marketing, admin)
