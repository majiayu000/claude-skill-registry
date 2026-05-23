---
name: biomechanics-validation
description: Validates jump metrics against physiological norms. Use when analyzing CMJ or drop jump results, discussing RSI values, jump heights, ground contact times, or when metrics seem unusual.
---

# Biomechanics Validation

When reviewing jump metrics, validate against these norms:

## RSI (Reactive Strength Index)

| Population   | RSI Range |
| ------------ | --------- |
| Recreational | 0.5-1.5   |
| Trained      | 1.5-2.5   |
| Elite        | 2.5-3.5   |

**Flag values > 3.5** as potentially erroneous (measurement or technique issue).

## CMJ Jump Height

| Population   | Male (cm) | Female (cm) |
| ------------ | --------- | ----------- |
| Recreational | 25-40     | 20-35       |
| Trained      | 40-55     | 35-45       |
| Elite        | 55-70+    | 45-55+      |

## Ground Contact Time (Drop Jump)

| Range      | Interpretation                             |
| ---------- | ------------------------------------------ |
| < 100 ms   | Likely sensor/detection error              |
| 150-250 ms | Optimal reactive strength                  |
| 250-350 ms | Acceptable, technique improvement possible |
| > 400 ms   | Technique issue or fatigue                 |

## Flight Time

| Jump Type | Typical Range | Flag If  |
| --------- | ------------- | -------- |
| CMJ       | 400-600 ms    | > 800 ms |
| Drop Jump | 350-550 ms    | > 700 ms |

## Triple Extension (CMJ)

All three joints should approach full extension at takeoff:

- Hip: > 160° (optimal: 170-180°)
- Knee: > 160° (optimal: 170-180°)
- Ankle: > 130° (plantar flexion)

## Countermovement Depth (CMJ)

| Depth    | Interpretation                       |
| -------- | ------------------------------------ |
| < 20 cm  | Shallow - may limit power generation |
| 20-40 cm | Optimal range                        |
| > 50 cm  | Deep - may indicate technique issue  |

## Validation Response Format

When validating metrics, provide:

1. **Status**: Normal / Warning / Error
2. **Value**: The actual metric value
3. **Expected Range**: Population-appropriate range
4. **Interpretation**: Coaching-friendly explanation
5. **Recommendation**: If outside norms, suggest next steps

## Example Validation

```
RSI: 2.8
Status: Normal (Elite range)
Expected: 2.5-3.5 for elite athletes
Interpretation: Excellent reactive strength capability
```

```
Ground Contact Time: 85 ms
Status: Warning
Expected: 150-250 ms optimal
Interpretation: Unusually short - likely detection error
Recommendation: Review debug video for takeoff/landing detection accuracy
```
