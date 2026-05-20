---
name: Livestock - Poultry
description: Poultry farming domain knowledge for broilers and layers in LivestockAI
---

# Livestock - Poultry

LivestockAI supports poultry farming with specialized tracking for broilers and layers.

## Supported Species

| Species  | Purpose              | Typical Cycle |
| -------- | -------------------- | ------------- |
| Broiler  | Meat production      | 6-8 weeks     |
| Layer    | Egg production       | 72-78 weeks   |
| Cockerel | Meat (slower growth) | 12-16 weeks   |
| Turkey   | Meat production      | 12-20 weeks   |

## Source Sizes

```typescript
const poultrySourceSizes = [
  { value: 'day-old', label: 'Day Old Chicks (DOC)' },
  { value: 'week-old', label: 'Week Old' },
  { value: 'point-of-lay', label: 'Point of Lay (POL)' },
  { value: 'grower', label: 'Grower' },
]
```

## Key Metrics

### Broilers

- **FCR** (Feed Conversion Ratio): Target 1.6-1.8
- **Mortality Rate**: Target <5%
- **Average Daily Gain**: 50-60g/day
- **Target Weight**: 2.0-2.5kg at 6 weeks

### Layers

- **Hen-Day Production**: Eggs per hen per day
- **Peak Production**: 90-95% at 26-30 weeks
- **Feed per Dozen Eggs**: 1.4-1.6kg

## Growth Curve

Broiler growth follows a sigmoid curve:

```typescript
// Simplified growth model
function estimateWeight(ageInDays: number): number {
  // Gompertz growth curve parameters for broilers
  const maxWeight = 3000 // grams
  const growthRate = 0.05
  const inflectionPoint = 35 // days

  return (
    maxWeight * Math.exp(-Math.exp(-growthRate * (ageInDays - inflectionPoint)))
  )
}
```

## Batch Lifecycle

1. **Brooding** (Week 1-2): Temperature control, starter feed
2. **Growing** (Week 3-5): Grower feed, weight monitoring
3. **Finishing** (Week 6-8): Finisher feed, market preparation
4. **Harvest**: Sale or processing

## Related Skills

- `batch-centric-design` - UI patterns for batch management
- `financial-calculations` - Cost and revenue tracking
