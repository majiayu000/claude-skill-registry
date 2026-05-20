---
name: frontend-patterns
description: |
  Frontend development patterns for LivestockAI. Use when implementing React components,
  TanStack Router routes, UI components, or working with the offline-first PWA architecture.
---

# Frontend Development Patterns

You are a frontend specialist for LivestockAI, expert in React 19, TanStack Router, and Tailwind CSS.

## Route Loader Pattern (Not useEffect!)

**Always use loaders for data fetching**:

```typescript
// ✅ CORRECT - SSR, prefetching, loading states
export const Route = createFileRoute('/_auth/batches/')({
  validateSearch: validateBatchSearch,

  loaderDeps: ({ search }) => ({
    farmId: search.farmId,
    page: search.page,
    status: search.status,
  }),

  loader: async ({ deps }) => {
    return getBatchesForFarmFn({ data: deps })
  },

  pendingComponent: BatchesSkeleton,

  errorComponent: ({ error }) => (
    <div className="p-4 text-red-600">Error: {error.message}</div>
  ),

  component: BatchesPage,
})

function BatchesPage() {
  const data = Route.useLoaderData()
  // ... render
}
```

```typescript
// ❌ WRONG - No SSR, no prefetching
function BatchesPage() {
  const [data, setData] = useState(null)
  useEffect(() => {
    getBatchesForFarmFn({ data: {} }).then(setData)
  }, [])
}
```

## Skeleton Components

Create skeleton components for `pendingComponent`:

```typescript
export function BatchesSkeleton() {
  return (
    <div className="space-y-4">
      <div className="grid gap-4 md:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-32 w-full" />
        ))}
      </div>
      <Skeleton className="h-64 w-full" />
    </div>
  )
}
```

## Custom Hooks (Mutations Only)

Hooks should handle mutations and UI state, NOT data fetching:

```typescript
export function useBatchPage() {
  const queryClient = useQueryClient()

  const createBatch = useMutation({
    mutationFn: (data: CreateBatchData) =>
      createBatchFn({ data: { batch: data } }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['batches'] })
      toast.success('Batch created')
    },
  })

  const [isDialogOpen, setIsDialogOpen] = useState(false)

  return { createBatch, isDialogOpen, setIsDialogOpen }
}
```

## UI Standards (Rugged Utility)

### Touch Targets

- Buttons: `h-12` (48px) minimum
- Action Grid: `w-16 h-16` (64px) minimum
- Form inputs: `h-11` (44px)
- List items: `h-12` (48px)

### Signal Colors

```typescript
// Use semantic colors
<Badge variant="success">Healthy</Badge>      // Green
<Badge variant="warning">Attention</Badge>    // Amber
<Badge variant="destructive">Critical</Badge> // Red
```

### Spacing

```typescript
// Consistent spacing scale
<div className="p-2">Tight (8px)</div>
<div className="p-3">Default (12px)</div>
<div className="p-4">Card padding (16px)</div>
<div className="p-6">Page sections (24px)</div>
```

## Form Patterns

```typescript
// Use react-hook-form with Zod
const form = useForm<FormData>({
  resolver: zodResolver(schema),
  defaultValues: { ... },
})

// Form submission
const onSubmit = async (data: FormData) => {
  try {
    await createBatch.mutateAsync(data)
    form.reset()
    onClose()
  } catch (error) {
    toast.error('Failed to create batch')
  }
}
```

## Dialog Pattern

```typescript
<Dialog open={isOpen} onOpenChange={setIsOpen}>
  <DialogContent className="sm:max-w-md">
    <DialogHeader>
      <DialogTitle>Create Batch</DialogTitle>
      <DialogDescription>Add a new livestock batch</DialogDescription>
    </DialogHeader>
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        {/* Form fields */}
        <DialogFooter>
          <Button type="button" variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" disabled={isLoading}>
            {isLoading ? 'Creating...' : 'Create'}
          </Button>
        </DialogFooter>
      </form>
    </Form>
  </DialogContent>
</Dialog>
```

## Navigation (No window.location.reload!)

```typescript
// ✅ CORRECT - Use router
const router = useRouter()
router.invalidate() // Refresh data
router.navigate({ to: '/batches' })

// ❌ WRONG - Breaks SPA
window.location.reload()
window.location.href = '/batches'
```
