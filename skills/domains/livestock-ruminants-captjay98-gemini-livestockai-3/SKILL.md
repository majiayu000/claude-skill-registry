---
name: Livestock - Ruminants
description: Cattle, goats, and sheep farming domain knowledge in LivestockAI
---

# Livestock - Ruminants

LivestockAI supports ruminant farming including cattle, goats, and sheep.

## Supported Species

### Cattle

| Type         | Purpose         | Typical Cycle |
| ------------ | --------------- | ------------- |
| Beef cattle  | Meat production | 18-24 months  |
| Dairy cattle | Milk production | Ongoing       |

### Goats

| Type        | Purpose         | Typical Cycle |
| ----------- | --------------- | ------------- |
| Meat goats  | Meat production | 6-12 months   |
| Dairy goats | Milk production | Ongoing       |

### Sheep

| Type       | Purpose         | Typical Cycle |
| ---------- | --------------- | ------------- |
| Meat sheep | Meat production | 6-12 months   |
| Wool sheep | Wool production | Ongoing       |

## Source Sizes

```typescript
const ruminantSourceSizes = [
  { value: 'calf', label: 'Calf/Kid/Lamb' },
  { value: 'weaner', label: 'Weaner' },
  { value: 'yearling', label: 'Yearling' },
  { value: 'adult', label: 'Adult' },
]
```

## Key Metrics

### Cattle

- **Average Daily Gain**: 0.8-1.5 kg/day (beef)
- **Feed Efficiency**: 6-8 kg feed per kg gain
- **Target Weight**: 450-600 kg at slaughter

### Goats

- **Average Daily Gain**: 100-200 g/day
- **Kidding Rate**: 1.5-2.0 kids per doe
- **Target Weight**: 25-40 kg at slaughter

### Sheep

- **Average Daily Gain**: 150-300 g/day
- **Lambing Rate**: 1.2-1.8 lambs per ewe
- **Target Weight**: 35-50 kg at slaughter

## Batch Lifecycle

1. **Acquisition**: Purchase or birth
2. **Growing**: Pasture + supplemental feeding
3. **Finishing**: Intensive feeding before sale
4. **Sale/Breeding**: Market or retained for breeding

## Related Skills

- `batch-centric-design` - UI patterns for batch management
- `financial-calculations` - Cost and revenue tracking
