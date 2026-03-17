---
name: Livestock - Apiculture
description: Beekeeping domain knowledge for honey production in LivestockAI
---

# Livestock - Apiculture

LivestockAI supports beekeeping (apiculture) for honey and bee product production.

## Tracking Units

Unlike other livestock, bees are tracked by:

- **Colonies/Hives** (not individual bees)
- **Frames** within hives

## Products

| Product     | Harvest Frequency  |
| ----------- | ------------------ |
| Honey       | 2-3 times/year     |
| Beeswax     | With honey harvest |
| Propolis    | Periodic           |
| Royal jelly | Specialized        |

## Key Metrics

- Colony strength (frames of bees)
- Queen status (present, laying, superseded)
- Honey yield per hive
- Swarm events

## Source Sizes

```typescript
const beeSourceSizes = [
  { value: 'nucleus', label: 'Nucleus Colony (Nuc)' },
  { value: 'package', label: 'Package Bees' },
  { value: 'established', label: 'Established Hive' },
  { value: 'swarm', label: 'Captured Swarm' },
]
```

## Seasonal Calendar

| Season | Activities                          |
| ------ | ----------------------------------- |
| Spring | Colony inspection, swarm prevention |
| Summer | Honey harvest, expansion            |
| Fall   | Winter preparation, feeding         |
| Winter | Minimal disturbance, monitoring     |

## Batch Lifecycle

1. **Establishment**: New colony setup
2. **Building**: Colony growth and comb building
3. **Production**: Honey flow and harvest
4. **Maintenance**: Disease prevention, feeding

## Related Skills

- `batch-centric-design` - UI patterns for batch management
- `financial-calculations` - Cost and revenue tracking
