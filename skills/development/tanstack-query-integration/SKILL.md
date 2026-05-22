---
name: tanstack-query-integration
description: Integration patterns for TanStack Query with VeeValidate forms, TanStack Table, and ProVet patterns. Use when combining queries with forms or tables.
---

# TanStack Query Integration

## Forms + TanStack Query

### Load Initial Data

```typescript
const route = useRoute()

const { data: user } = useUserDetailQuery({ id: route.params.id })

const { resetForm } = useForm({
  validationSchema: toTypedSchema(schema),
})

watchEffect(() => {
  if (user.value) {
    resetForm({ values: user.value })
  }
})
```

### Submit with Mutation

```typescript
const { handleSubmit } = useForm()
const { mutate, isPending } = useUserUpdateMutation()

const onSubmit = handleSubmit((values) => {
  mutate(
    { id, ...values },
    {
      onSuccess: () => showToast({ variant: 'success' }),
      onError: (error) => showToast({ variant: 'error', title: error.detail }),
    },
  )
})
```

## Tables + TanStack Query

### Server-Side Pagination

```typescript
const pagination = ref({ pageIndex: 0, pageSize: 50 })

const { data } = useUsersListQuery({
  params: computed(() => toPaginationQueryParams(pagination.value)),
})

const table = useVueTable({
  get data() {
    return data.value?.data || []
  },
  columns,
  manualPagination: true,
  pageCount: data.value?.meta?.pages ?? 0,
  state: {
    get pagination() {
      return pagination.value
    },
  },
  onPaginationChange: (updater) => {
    pagination.value =
      typeof updater === 'function' ? updater(pagination.value) : updater
  },
})
```

### Server-Side Sorting

```typescript
const sorting = ref<SortingState>([])

const { data } = useUsersListQuery({
  params: computed(() => ({
    sort: sortingStateToQueryParam(sorting.value),
  })),
})

const table = useVueTable({
  get data() {
    return data.value?.data || []
  },
  columns,
  manualSorting: true,
  state: {
    get sorting() {
      return sorting.value
    },
  },
  onSortingChange: (updater) => {
    sorting.value =
      typeof updater === 'function' ? updater(sorting.value) : updater
  },
})
```

### Server-Side Filtering

```typescript
const filters = ref({ search: '', archived: false })

const { data } = useUsersListQuery({
  params: computed(() => ({
    'filter[search]': filters.value.search || undefined,
    'filter[archived]': filters.value.archived,
  })),
})
```

## Filters + TanStack Query

### URL State Persistence

```typescript
const filtersWithUrlState = useFiltersWithUrlState({
  search: '',
  archived: false,
})

const { data } = useUsersListQuery({
  params: computed(() => ({
    'filter[search]': filtersWithUrlState.search.value || undefined,
    'filter[archived]': filtersWithUrlState.archived.value,
  })),
})
```

## Mutations + Cache Updates

### Invalidate After Create

```typescript
const { mutate } = useMutation({
  mutationFn: createUser,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: userKeys.lists() })
  },
})
```

### Invalidate After Update

```typescript
const { mutate } = useMutation({
  mutationFn: ({ id, data }) => updateUser(id, data),
  onSuccess: (_, variables) => {
    queryClient.invalidateQueries({ queryKey: userKeys.detail(variables.id) })
    queryClient.invalidateQueries({ queryKey: userKeys.lists() })
  },
})
```

### Invalidate After Delete

```typescript
const { mutate } = useMutation({
  mutationFn: deleteUser,
  onSuccess: (_, id) => {
    queryClient.invalidateQueries({ queryKey: userKeys.lists() })
    queryClient.removeQueries({ queryKey: userKeys.detail(id) })
  },
})
```

## Form Autosave + Mutation

```typescript
const { values } = useForm()
const { mutate } = useUpdateMutation()

watch(
  values,
  (newValues) => {
    mutate(newValues)
  },
  { debounce: 500 },
)
```

## Loading States

```typescript
const { data, isLoading, isFetching } = useQuery()
const { mutate, isPending } = useMutation()
```

```vue
<nord-spinner v-if="isLoading" />
<nord-button :loading="isPending" @click="onSubmit">Save</nord-button>
```

## Error Display

```typescript
const { error, isError } = useQuery()
```

```vue
<nord-banner v-if="isError" variant="error">
  {{ error.message }}
</nord-banner>
```
