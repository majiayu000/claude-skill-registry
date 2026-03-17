---
name: admin-crud
description: Generate admin dashboard pages with data tables, filters, bulk actions, dialogs, and forms. Use when building admin interfaces, management pages, or dashboard components.
---

# Admin CRUD Generator

Create admin dashboard pages following this project's established patterns.

## Admin Page Structure

```
src/
├── routes/admin/
│   └── resources/
│       ├── index.tsx          # List page
│       └── $resourceId.tsx    # Detail/edit page
└── components/admin/
    └── resources/
        ├── ResourcesList.tsx        # List container
        ├── ResourceForm.tsx         # Create/edit form
        └── components/
            ├── ResourceTable.tsx    # Data table
            ├── StatusBadge.tsx      # Status indicator
            ├── BulkActionsBar.tsx   # Bulk operations
            └── ResourceActions.tsx  # Row actions
```

## List Page Template

```typescript
// src/routes/admin/resources/index.tsx
import { createFileRoute } from '@tanstack/react-router'
import { ResourcesList } from '@/components/admin/resources/ResourcesList'

export const Route = createFileRoute('/admin/resources/')({
  component: ResourcesPage,
})

function ResourcesPage() {
  return <ResourcesList />
}
```

## List Component with Data Table

```typescript
// src/components/admin/resources/ResourcesList.tsx
import { useQuery } from '@tanstack/react-query'
import { useTranslation } from 'react-i18next'
import { Plus } from 'lucide-react'
import { Link } from '@tanstack/react-router'

import { Button } from '@/components/ui/button'
import { ResourceTable } from './components/ResourceTable'

export function ResourcesList() {
  const { t } = useTranslation()

  const { data, isLoading, error } = useQuery({
    queryKey: ['resources'],
    queryFn: async () => {
      const res = await fetch('/api/resources', { credentials: 'include' })
      const json = await res.json()
      if (!json.success) throw new Error(json.error)
      return json
    },
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div
          className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-pink-500"
          role="status"
          aria-label="Loading"
        />
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-500">{t('Failed to load')}</p>
      </div>
    )
  }

  const { items, total } = data

  if (items.length === 0) {
    return (
      <div className="text-center py-12">
        <Package className="mx-auto h-12 w-12 text-muted-foreground" />
        <h3 className="mt-2 text-sm font-semibold">{t('No resources')}</h3>
        <p className="mt-1 text-sm text-muted-foreground">
          {t('Get started by creating a new resource.')}
        </p>
        <div className="mt-6">
          <Button asChild>
            <Link to="/admin/resources/new">
              <Plus className="mr-2 h-4 w-4" />
              {t('Add Resource')}
            </Link>
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">{t('Resources')}</h1>
        <Button asChild>
          <Link to="/admin/resources/new">
            <Plus className="mr-2 h-4 w-4" />
            {t('Add Resource')}
          </Link>
        </Button>
      </div>

      <ResourceTable resources={items} />

      <div className="text-sm text-muted-foreground">
        {t('{{count}} total', { count: total })}
      </div>
    </div>
  )
}
```

## Data Table Component

```typescript
// src/components/admin/resources/components/ResourceTable.tsx
import { useState } from 'react'
import { Link } from '@tanstack/react-router'
import { MoreHorizontal, ArrowUpDown, ArrowUp, ArrowDown } from 'lucide-react'
import { useTranslation } from 'react-i18next'

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { StatusBadge } from './StatusBadge'

interface Resource {
  id: string
  name: { en: string }
  status: 'active' | 'draft' | 'archived'
  createdAt: string
}

interface Props {
  resources: Resource[]
}

export function ResourceTable({ resources }: Props) {
  const { t } = useTranslation()
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set())
  const [sortKey, setSortKey] = useState<string>('createdAt')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc')

  const toggleSelect = (id: string) => {
    const next = new Set(selectedIds)
    if (next.has(id)) {
      next.delete(id)
    } else {
      next.add(id)
    }
    setSelectedIds(next)
  }

  const toggleSelectAll = () => {
    if (selectedIds.size === resources.length) {
      setSelectedIds(new Set())
    } else {
      setSelectedIds(new Set(resources.map((r) => r.id)))
    }
  }

  const isAllSelected = selectedIds.size === resources.length
  const isSomeSelected = selectedIds.size > 0 && selectedIds.size < resources.length

  const handleSort = (key: string) => {
    if (sortKey === key) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
    } else {
      setSortKey(key)
      setSortOrder('desc')
    }
  }

  const SortIcon = ({ columnKey }: { columnKey: string }) => {
    if (sortKey !== columnKey) return <ArrowUpDown className="ml-2 h-4 w-4" />
    return sortOrder === 'asc'
      ? <ArrowUp className="ml-2 h-4 w-4" />
      : <ArrowDown className="ml-2 h-4 w-4" />
  }

  return (
    <>
      {selectedIds.size > 0 && (
        <BulkActionsBar
          selectedCount={selectedIds.size}
          onClearSelection={() => setSelectedIds(new Set())}
        />
      )}

      <div className="rounded-md border">
        <table className="w-full">
          <thead>
            <tr className="border-b bg-muted/50">
              <th className="w-12 p-4">
                <Checkbox
                  checked={isAllSelected}
                  indeterminate={isSomeSelected}
                  onCheckedChange={toggleSelectAll}
                />
              </th>
              <th className="p-4 text-left">
                <button
                  className="flex items-center font-medium"
                  onClick={() => handleSort('name')}
                >
                  {t('Name')}
                  <SortIcon columnKey="name" />
                </button>
              </th>
              <th className="p-4 text-left">{t('Status')}</th>
              <th className="p-4 text-left">
                <button
                  className="flex items-center font-medium"
                  onClick={() => handleSort('createdAt')}
                >
                  {t('Created')}
                  <SortIcon columnKey="createdAt" />
                </button>
              </th>
              <th className="w-12 p-4"></th>
            </tr>
          </thead>
          <tbody>
            {resources.map((resource) => (
              <tr
                key={resource.id}
                className={`border-b hover:bg-muted/50 group ${
                  selectedIds.has(resource.id) ? 'bg-pink-500/5' : ''
                }`}
              >
                <td className="p-4">
                  <Checkbox
                    checked={selectedIds.has(resource.id)}
                    onCheckedChange={() => toggleSelect(resource.id)}
                  />
                </td>
                <td className="p-4">
                  <Link
                    to="/admin/resources/$resourceId"
                    params={{ resourceId: resource.id }}
                    className="font-medium hover:underline"
                  >
                    {resource.name.en}
                  </Link>
                </td>
                <td className="p-4">
                  <StatusBadge status={resource.status} />
                </td>
                <td className="p-4 text-muted-foreground">
                  {new Date(resource.createdAt).toLocaleDateString()}
                </td>
                <td className="p-4">
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="icon">
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem asChild>
                        <Link
                          to="/admin/resources/$resourceId"
                          params={{ resourceId: resource.id }}
                        >
                          {t('Edit')}
                        </Link>
                      </DropdownMenuItem>
                      <DropdownMenuItem className="text-destructive">
                        {t('Delete')}
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  )
}
```

## Status Badge

```typescript
// src/components/admin/resources/components/StatusBadge.tsx
import { cn } from '@/lib/utils'

const statusStyles = {
  active: 'bg-emerald-500/10 text-emerald-500',
  draft: 'bg-amber-500/10 text-amber-500',
  archived: 'bg-muted text-muted-foreground',
  pending: 'bg-blue-500/10 text-blue-500',
  processing: 'bg-purple-500/10 text-purple-500',
  shipped: 'bg-cyan-500/10 text-cyan-500',
  delivered: 'bg-emerald-500/10 text-emerald-500',
  cancelled: 'bg-red-500/10 text-red-500',
  paid: 'bg-emerald-500/10 text-emerald-500',
  failed: 'bg-red-500/10 text-red-500',
  refunded: 'bg-amber-500/10 text-amber-500',
}

interface Props {
  status: keyof typeof statusStyles
}

export function StatusBadge({ status }: Props) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-full px-2 py-1 text-xs font-medium uppercase',
        statusStyles[status] || statusStyles.draft
      )}
    >
      <span className="h-1.5 w-1.5 rounded-full bg-current" />
      {status}
    </span>
  )
}
```

## Bulk Actions Bar

```typescript
// src/components/admin/resources/components/BulkActionsBar.tsx
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useTranslation } from 'react-i18next'
import { toast } from 'sonner'

import { Button } from '@/components/ui/button'

interface Props {
  selectedCount: number
  selectedIds: string[]
  onClearSelection: () => void
}

export function BulkActionsBar({ selectedCount, selectedIds, onClearSelection }: Props) {
  const { t } = useTranslation()
  const queryClient = useQueryClient()

  const bulkUpdate = useMutation({
    mutationFn: async (action: 'activate' | 'archive' | 'delete') => {
      const res = await fetch('/api/resources/bulk', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ ids: selectedIds, action }),
      })
      const json = await res.json()
      if (!json.success) throw new Error(json.error)
      return json
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['resources'] })
      onClearSelection()
      toast.success(t('Updated successfully'))
    },
    onError: (error) => {
      toast.error(error.message)
    },
  })

  return (
    <div className="flex items-center gap-4 rounded-lg border bg-muted/50 p-4">
      <span className="text-sm font-medium">
        {t('{{count}} selected', { count: selectedCount })}
      </span>
      <div className="flex gap-2">
        <Button
          size="sm"
          variant="outline"
          onClick={() => bulkUpdate.mutate('activate')}
          disabled={bulkUpdate.isPending}
        >
          {t('Activate')}
        </Button>
        <Button
          size="sm"
          variant="outline"
          onClick={() => bulkUpdate.mutate('archive')}
          disabled={bulkUpdate.isPending}
        >
          {t('Archive')}
        </Button>
        <Button
          size="sm"
          variant="destructive"
          onClick={() => bulkUpdate.mutate('delete')}
          disabled={bulkUpdate.isPending}
        >
          {t('Delete')}
        </Button>
      </div>
      <Button
        size="sm"
        variant="ghost"
        onClick={onClearSelection}
        className="ml-auto"
      >
        {t('Clear selection')}
      </Button>
    </div>
  )
}
```

## Card-Based Form Layout

```typescript
// Product form pattern with gradient accent cards
<div className="grid lg:grid-cols-3 gap-6">
  {/* Main content - 2 columns */}
  <div className="lg:col-span-2 space-y-6">
    {/* Details Card */}
    <Card className="border-border/50 shadow-xl shadow-foreground/5 bg-card/50 backdrop-blur-sm overflow-hidden">
      <div className="h-1 bg-gradient-to-r from-pink-500 to-purple-500" />
      <CardHeader>
        <CardTitle>{t('Details')}</CardTitle>
      </CardHeader>
      <CardContent>
        {/* Form fields */}
      </CardContent>
    </Card>

    {/* Media Card */}
    <Card className="overflow-hidden">
      <div className="h-1 bg-gradient-to-r from-violet-500 to-fuchsia-500" />
      <CardHeader>
        <CardTitle>{t('Media')}</CardTitle>
      </CardHeader>
      <CardContent>
        {/* Image uploader */}
      </CardContent>
    </Card>
  </div>

  {/* Sidebar - 1 column, sticky */}
  <div className="space-y-6">
    <div className="lg:sticky lg:top-4">
      {/* Status Card */}
      <Card>
        <div className="h-1 bg-gradient-to-r from-emerald-500 to-teal-500" />
        <CardHeader>
          <CardTitle>{t('Status')}</CardTitle>
        </CardHeader>
        <CardContent>
          {/* Status select */}
        </CardContent>
      </Card>
    </div>
  </div>
</div>
```

## Gradient Accent Colors

| Section  | Gradient                         |
| -------- | -------------------------------- |
| Details  | `from-pink-500 to-purple-500`    |
| Media    | `from-violet-500 to-fuchsia-500` |
| Options  | `from-blue-500 to-cyan-500`      |
| Variants | `from-emerald-500 to-teal-500`   |
| SEO      | `from-amber-500 to-orange-500`   |

## Confirmation Dialog

```typescript
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'

function DeleteConfirmDialog({ open, onOpenChange, onConfirm, resourceName }) {
  const { t } = useTranslation()

  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>{t('Delete Resource')}</AlertDialogTitle>
          <AlertDialogDescription>
            {t('Are you sure you want to delete "{{name}}"? This action cannot be undone.', {
              name: resourceName,
            })}
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>{t('Cancel')}</AlertDialogCancel>
          <AlertDialogAction
            onClick={onConfirm}
            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
          >
            {t('Delete')}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}
```

## See Also

- `src/components/admin/products/` - Full product CRUD example
- `src/components/admin/orders/` - Order management
- `src/hooks/useDataTable.ts` - Table state management
- `forms` skill - Form patterns with FNForm
