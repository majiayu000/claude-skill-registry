---
name: frontend-component
description: Create React components following project standards.
---

# Component Creation

## Use Generator Scripts

```bash
./scripts/generate-component.sh MyButton              # → shared/
./scripts/generate-component.sh ClusterCard clustering # → clustering/
./scripts/generate-hook.sh useTheme
```

## Location Rules

| Type | Path |
|------|------|
| Reusable | `components/shared/` |
| Feature-specific | `components/[feature]/` |
| Sub-components | `components/[feature]/components/` |

## Standards

- Tailwind CSS with **slate** (bg/text) + **sky** (accents)
- Icons from `lucide-react`
- Wrap in `memo()` for lists/visualizations
- Always accept `className` prop
- Use `@/` alias for imports
