---
name: ui-patterns
description: Ready-to-use UI patterns library for common scenarios - stats dashboards, data tables, forms, modals, and feedback states
user-invocable: false
---

# Pierre UI Patterns Library

Ready-to-use UI patterns for common scenarios. Copy and adapt these patterns when building features.

## Data Display Patterns

### Stats Dashboard
```tsx
<div className="grid grid-cols-1 md:grid-cols-3 gap-6">
  <Card variant="stat">
    <div className="text-3xl font-bold text-pierre-gray-900">1,234</div>
    <div className="text-sm text-pierre-gray-500 mt-1">Total Requests</div>
    <div className="text-xs text-pierre-green-600 mt-2">+12% from last week</div>
  </Card>
  <Card variant="stat">
    <div className="text-3xl font-bold text-pierre-activity">98.5%</div>
    <div className="text-sm text-pierre-gray-500 mt-1">Uptime</div>
  </Card>
  <Card variant="stat">
    <div className="text-3xl font-bold text-pierre-violet">42ms</div>
    <div className="text-sm text-pierre-gray-500 mt-1">Avg Response</div>
  </Card>
</div>
```

### Data Table with Actions
```tsx
<Card>
  <CardHeader title="API Keys" subtitle="Manage your API keys" />
  <div className="overflow-x-auto">
    <table className="w-full">
      <thead>
        <tr className="border-b border-pierre-gray-200">
          <th className="text-left py-3 px-4 text-sm font-medium text-pierre-gray-700">Name</th>
          <th className="text-left py-3 px-4 text-sm font-medium text-pierre-gray-700">Status</th>
          <th className="text-right py-3 px-4 text-sm font-medium text-pierre-gray-700">Actions</th>
        </tr>
      </thead>
      <tbody>
        {items.map((item) => (
          <tr key={item.id} className="border-b border-pierre-gray-100 hover:bg-pierre-gray-50">
            <td className="py-3 px-4">
              <div className="font-medium text-pierre-gray-900">{item.name}</div>
              <div className="text-sm text-pierre-gray-500">{item.description}</div>
            </td>
            <td className="py-3 px-4">
              <Badge variant={item.active ? 'success' : 'secondary'}>
                {item.active ? 'Active' : 'Inactive'}
              </Badge>
            </td>
            <td className="py-3 px-4 text-right">
              <Button variant="secondary" size="sm">Edit</Button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
</Card>
```

## Form Patterns

### Standard Form
```tsx
<Card>
  <CardHeader title="Create New Key" />
  <form onSubmit={handleSubmit} className="space-y-4">
    <div>
      <label className="label">Key Name</label>
      <input
        type="text"
        className="input-field"
        placeholder="Enter key name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      {errors.name && <span className="error-text">{errors.name}</span>}
    </div>

    <div>
      <label className="label">Description</label>
      <textarea
        className="input-field min-h-[100px]"
        placeholder="Optional description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <span className="help-text">Describe what this key is used for</span>
    </div>

    <div className="flex justify-end gap-2 pt-4">
      <Button variant="secondary" type="button" onClick={onCancel}>
        Cancel
      </Button>
      <Button variant="primary" type="submit" loading={isSubmitting}>
        {isSubmitting ? 'Creating...' : 'Create Key'}
      </Button>
    </div>
  </form>
</Card>
```

### Filter Bar
```tsx
<div className="flex items-center justify-between mb-6">
  <div className="flex items-center gap-4">
    <input
      type="text"
      className="input-field w-64"
      placeholder="Search..."
      value={search}
      onChange={(e) => setSearch(e.target.value)}
    />
    <select className="input-field w-40">
      <option value="">All Status</option>
      <option value="active">Active</option>
      <option value="inactive">Inactive</option>
    </select>
  </div>
  <Button variant="primary">Add New</Button>
</div>
```

## Feedback Patterns

### Success State
```tsx
<div className="bg-pierre-green-50 border border-pierre-green-200 rounded-lg p-4">
  <div className="flex items-center gap-3">
    <svg className="w-5 h-5 text-pierre-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
    </svg>
    <div>
      <p className="font-medium text-pierre-green-800">Success!</p>
      <p className="text-sm text-pierre-green-700">Your changes have been saved.</p>
    </div>
  </div>
</div>
```

### Error State
```tsx
<div className="bg-pierre-red-50 border border-pierre-red-200 rounded-lg p-4">
  <div className="flex items-center gap-3">
    <svg className="w-5 h-5 text-pierre-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
    <div>
      <p className="font-medium text-pierre-red-800">Error</p>
      <p className="text-sm text-pierre-red-700">{error.message}</p>
    </div>
  </div>
</div>
```

### Empty State
```tsx
<div className="text-center py-12">
  <svg className="w-12 h-12 text-pierre-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
  </svg>
  <p className="text-lg font-medium text-pierre-gray-900 mb-1">No items yet</p>
  <p className="text-sm text-pierre-gray-500 mb-4">Get started by creating your first item.</p>
  <Button variant="primary">Create Item</Button>
</div>
```

### Loading State
```tsx
// Full page loading
<div className="flex items-center justify-center h-64">
  <div className="pierre-spinner w-8 h-8" />
</div>

// Inline loading
<Button variant="primary" loading={true}>
  <div className="pierre-spinner mr-2" />
  Loading...
</Button>

// Skeleton loading
<div className="space-y-4">
  <div className="h-4 bg-pierre-gray-200 rounded animate-pulse w-3/4" />
  <div className="h-4 bg-pierre-gray-200 rounded animate-pulse w-1/2" />
  <div className="h-4 bg-pierre-gray-200 rounded animate-pulse w-5/6" />
</div>
```

## Navigation Patterns

### Tabs
```tsx
<div className="border-b border-pierre-gray-200">
  <nav className="flex gap-8">
    <button
      className={clsx('tab', activeTab === 'overview' && 'tab-active')}
      onClick={() => setActiveTab('overview')}
    >
      Overview
    </button>
    <button
      className={clsx('tab', activeTab === 'settings' && 'tab-active')}
      onClick={() => setActiveTab('settings')}
    >
      Settings
    </button>
  </nav>
</div>
```

### Breadcrumbs
```tsx
<nav className="flex items-center gap-2 text-sm text-pierre-gray-500 mb-6">
  <a href="/dashboard" className="hover:text-pierre-violet">Dashboard</a>
  <span>/</span>
  <a href="/settings" className="hover:text-pierre-violet">Settings</a>
  <span>/</span>
  <span className="text-pierre-gray-900">API Keys</span>
</nav>
```

## Modal Patterns

### Confirmation Modal
```tsx
<ConfirmDialog
  isOpen={showDelete}
  onClose={() => setShowDelete(false)}
  onConfirm={handleDelete}
  title="Delete API Key"
  message="Are you sure you want to delete this API key? This action cannot be undone."
  variant="danger"
  confirmText="Delete"
  cancelText="Cancel"
/>
```

### Form Modal
```tsx
<Modal
  isOpen={showCreate}
  onClose={() => setShowCreate(false)}
  title="Create New Item"
>
  <form onSubmit={handleSubmit} className="space-y-4">
    <div>
      <label className="label">Name</label>
      <input type="text" className="input-field" />
    </div>
    <ModalActions>
      <Button variant="secondary" onClick={() => setShowCreate(false)}>
        Cancel
      </Button>
      <Button variant="primary" type="submit">
        Create
      </Button>
    </ModalActions>
  </form>
</Modal>
```

## Three Pillars Usage

Use pillar colors semantically for fitness-related features:

```tsx
// Activity (emerald) - fitness, workouts, movement
<Badge className="bg-pierre-activity text-white">Running</Badge>
<div className="bg-gradient-activity text-white p-4 rounded-lg">
  Activity Summary
</div>

// Nutrition (amber) - food, meals, hydration
<Badge className="bg-pierre-nutrition text-white">Meal Logged</Badge>
<div className="bg-gradient-nutrition text-white p-4 rounded-lg">
  Nutrition Overview
</div>

// Recovery (indigo) - sleep, rest, wellness
<Badge className="bg-pierre-recovery text-white">Sleep Score</Badge>
<div className="bg-gradient-recovery text-white p-4 rounded-lg">
  Recovery Status
</div>
```
