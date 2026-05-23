---
name: Livestock - Aquaculture
description: Fish farming domain knowledge for catfish and tilapia in LivestockAI
---

# Livestock - Aquaculture

LivestockAI supports aquaculture with specialized tracking for catfish and tilapia.

## Supported Species

| Species | Purpose         | Typical Cycle |
| ------- | --------------- | ------------- |
| Catfish | Meat production | 4-6 months    |
| Tilapia | Meat production | 6-8 months    |

## Source Sizes

```typescript
const fishSourceSizes = [
  { value: 'fingerling', label: 'Fingerling (3-5cm)' },
  { value: 'juvenile', label: 'Juvenile (5-10cm)' },
  { value: 'post-fingerling', label: 'Post-Fingerling' },
  { value: 'table-size', label: 'Table Size' },
]
```

## Key Metrics

### Catfish

- **FCR**: Target 1.2-1.5
- **Survival Rate**: Target >90%
- **Stocking Density**: 50-100 fish/m³
- **Target Weight**: 1.0-1.5kg at harvest

### Tilapia

- **FCR**: Target 1.5-1.8
- **Survival Rate**: Target >85%
- **Stocking Density**: 20-50 fish/m³
- **Target Weight**: 400-600g at harvest

## Water Quality Tracking

Critical parameters monitored:

| Parameter        | Optimal Range |
| ---------------- | ------------- |
| Temperature      | 26-30°C       |
| pH               | 6.5-8.5       |
| Dissolved Oxygen | >5 mg/L       |
| Ammonia          | <0.02 mg/L    |
| Nitrite          | <0.1 mg/L     |

## Batch Lifecycle

1. **Stocking**: Fingerlings introduced to pond/tank
2. **Nursery** (Week 1-4): High protein feed, frequent feeding
3. **Grow-out** (Month 2-5): Standard feed, monitoring
4. **Harvest**: Partial or complete harvest

## Related Skills

- `batch-centric-design` - UI patterns for batch management
- `financial-calculations` - Cost and revenue tracking
