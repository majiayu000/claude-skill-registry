# Dashboard Components Skill

> React component patterns for cl-n8n-mcp dashboard.

---

## Theme (Orange Accent)

```typescript
colors: {
  'n2f-bg': '#0a0a0f',
  'n2f-surface': '#12121a',
  'n2f-elevated': '#1a1a24',
  'n2f-border': '#2a2a3a',
  'n2f-text': '#f0f0f5',
  'n2f-accent': '#f97316',
}
```

## Button Variants

```tsx
const variants = {
  primary: 'bg-n2f-accent hover:bg-n2f-accent-hover text-white',
  secondary: 'bg-n2f-elevated text-n2f-text border border-n2f-border',
  danger: 'bg-red-600 hover:bg-red-700 text-white',
};
```

## Card Pattern

```tsx
<Card className="bg-n2f-surface border-n2f-border">
  <CardHeader>
    <CardTitle className="text-n2f-text">Title</CardTitle>
  </CardHeader>
  <CardContent>
    {/* content */}
  </CardContent>
</Card>
```

## Input Pattern

```tsx
<input
  className="w-full px-4 py-2 bg-n2f-elevated border border-n2f-border rounded-lg text-n2f-text focus:border-n2f-accent focus:ring-1 focus:ring-n2f-accent"
/>
```
