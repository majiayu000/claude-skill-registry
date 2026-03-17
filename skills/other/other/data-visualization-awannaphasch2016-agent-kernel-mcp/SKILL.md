---
name: data-visualization
description: Build mathematically correct, visually prominent data visualizations for time-series charts. Use this skill when creating charts with mathematical overlays (trendlines, patterns, indicators), fixing visual artifacts (wavy lines, domain mismatches), or validating chart correctness. Focuses on technical correctness and progressive validation, not aesthetic design.
license: Project-specific skill
---

# Data Visualization Skill

**Focus**: Mathematical correctness and visual prominence for time-series charts with overlays (trendlines, patterns, indicators).

**When to use this skill**:
- Building charts with mathematical overlays (trendlines, moving averages, regressions)
- Fixing visual artifacts (wavy lines at gaps, domain mismatches)
- Validating chart correctness (progressive evidence)
- Implementing pattern overlays (flags, wedges, triangles, H&S)
- Working with Chart.js, D3.js, Recharts, or similar frameworks

**When NOT to use this skill**:
- Aesthetic UI design (use `frontend-design` skill)
- Telegram-specific UI patterns (use `telegram-uiux` skill)
- General React/TypeScript patterns (use `telegram-uiux` skill)

---

## Quick Reference

**Problem**: Trendlines appear wavy at weekend gaps
**Solution**: Use timestamp-based regression (not index-based) → [MATHEMATICAL-CORRECTNESS.md](MATHEMATICAL-CORRECTNESS.md#domain-compatibility)

**Problem**: Pattern overlays hard to see on chart
**Solution**: Use shaded regions + bold lines + layer ordering → [VISUAL-HIERARCHY.md](VISUAL-HIERARCHY.md#visual-prominence-through-layering)

**Problem**: Custom polygon fill doesn't render in Chart.js
**Solution**: Use framework's dataset-to-dataset fill feature → [FRAMEWORK-PATTERNS.md](FRAMEWORK-PATTERNS.md#framework-native-over-custom)

**Problem**: Chart works with perfect data but crashes on real data
**Solution**: Test with edge cases (gaps, nulls, holidays) → [VALIDATION.md](VALIDATION.md#edge-cases-reveal-bugs)

---

## Decision Tree

```
User request involves data visualization?
├─ YES → Continue
└─ NO → Use different skill

Mathematical overlays (trendlines, patterns)?
├─ YES → Use this skill
└─ NO → Consider frontend-design (if aesthetic focus)

Problem type?
├─ Visual artifacts (wavy lines, curvature)
│  └─ Check: Domain compatibility [MATHEMATICAL-CORRECTNESS.md]
├─ Low visibility (patterns hard to see)
│  └─ Check: Visual hierarchy [VISUAL-HIERARCHY.md]
├─ Framework issues (custom code not working)
│  └─ Check: Framework patterns [FRAMEWORK-PATTERNS.md]
├─ Correctness validation (how to verify?)
│  └─ Check: Progressive validation [VALIDATION.md]
└─ General implementation
   └─ Read all sections for comprehensive approach
```

---

## Core Principles

### 1. Visual Prominence Through Layering
**Pattern**: Shaded regions (fills) + bold trendlines + layer ordering

**Why**: Simple lines blend into busy charts; shaded areas create immediate recognition

**See**: [VISUAL-HIERARCHY.md](VISUAL-HIERARCHY.md) for opacity guidelines, layering strategy, Chart.js implementation

---

### 2. Domain Compatibility for Mathematical Correctness
**Pattern**: Regression domain must match visualization axis domain

**Why**: Domain mismatch creates visual artifacts (wavy lines at irregular spacing)

**See**: [MATHEMATICAL-CORRECTNESS.md](MATHEMATICAL-CORRECTNESS.md) for timestamp vs index, testing strategy, common mismatches

---

### 3. Framework-Native Over Custom Solutions
**Pattern**: Use framework's built-in features instead of custom implementations

**Why**: Native features are tested, documented, maintained; custom solutions fragile

**See**: [FRAMEWORK-PATTERNS.md](FRAMEWORK-PATTERNS.md) for Chart.js patterns, research workflow, when custom is acceptable

---

### 4. Edge Cases Reveal Mathematical Bugs
**Pattern**: Test with irregular data (weekend gaps, holidays, nulls)

**Why**: Regular spacing hides domain mismatches; irregular spacing reveals bugs

**See**: [VALIDATION.md](VALIDATION.md#edge-cases-reveal-bugs) for edge case examples, testing checklist, validation workflow

---

### 5. Progressive Evidence for UI Validation
**Pattern**: Validate through layers: visual → code → edge cases → mathematical

**Why**: Visual appearance alone doesn't prove correctness; need multiple validation levels

**See**: [VALIDATION.md](VALIDATION.md#progressive-evidence) for 4-layer validation, evidence hierarchy, validation matrix

---

## Workflow

### Phase 1: Plan Implementation
1. **Understand requirements**: What visualization? What overlays?
2. **Research framework**: Does Chart.js/D3 have built-in feature?
3. **Choose approach**: Native feature vs custom (prefer native)
4. **Identify domain**: What's the X-axis? (time, categories, continuous)

### Phase 2: Implement Visualization
1. **Start with data layer**: Render base chart (candlesticks, line, etc.)
2. **Add mathematical overlays**: Trendlines, patterns, indicators
3. **Apply visual hierarchy**: Layer ordering (fills behind, lines front)
4. **Tune prominence**: Adjust opacity (25-30% for web), line width (3px)

### Phase 3: Validate Correctness
1. **Layer 1 (Visual)**: Does it look right? Take screenshots
2. **Layer 2 (Code)**: Using framework correctly? Review patterns
3. **Layer 3 (Edge)**: Test with weekend gaps, holidays, nulls
4. **Layer 4 (Math)**: Verify algorithm correctness (domain match?)

### Phase 4: Debug Issues
**If wavy lines**:
- Check domain compatibility (timestamp vs index regression)
- Test with weekend gap data
- Verify Chart.js axis type (`type: 'time'`)

**If low visibility**:
- Add shaded fill regions (25-30% opacity)
- Increase line width (3px)
- Apply layer ordering (order: 1,2,3)

**If framework issues**:
- Research native features (dataset-to-dataset fill)
- Check documentation examples
- Prefer configuration over code

---

## Common Patterns

### Pattern: Timestamp-Based Regression
**Use when**: Continuous time axis (Chart.js `type: 'time'`)

```javascript
function fitLinearTrendline(points) {
    const n = points.length;

    // Use timestamps (p.x), not indices (i)
    const sumX = points.reduce((sum, p) => sum + p.x, 0);
    const sumXY = points.reduce((sum, p) => sum + p.x * p.y, 0);
    const sumX2 = points.reduce((sum, p) => sum + p.x * p.x, 0);

    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;

    return points.map(p => ({
        x: p.x,
        y: slope * p.x + intercept  // Timestamp-based
    }));
}
```

**See**: [MATHEMATICAL-CORRECTNESS.md](MATHEMATICAL-CORRECTNESS.md#timestamp-based-regression)

---

### Pattern: Shaded Region with Layering
**Use when**: Overlaying patterns on busy charts

```javascript
const datasets = [];

// Layer 3: Fill area (behind)
datasets.push({
    label: 'Pattern Area',
    data: polygonPoints,
    backgroundColor: 'rgba(38, 166, 154, 0.25)',  // 25% opacity
    fill: true,
    borderColor: 'transparent',
    order: 3,  // Behind
    pointRadius: 0
});

// Layer 2: Trendline (front)
datasets.push({
    label: 'Trendline',
    data: trendlinePoints,
    borderColor: '#26A69A',
    borderWidth: 3,  // Bold
    fill: false,
    order: 2,  // Front
    pointRadius: 0
});

// Layer 1: Data (highest priority)
datasets.push({
    type: 'candlestick',
    data: ohlcData,
    order: 1  // Front-most
});
```

**See**: [VISUAL-HIERARCHY.md](VISUAL-HIERARCHY.md#shaded-regions)

---

### Pattern: Dataset-to-Dataset Fill (Chart.js)
**Use when**: Filling area between two lines

```javascript
const datasets = [];

// Draw lower boundary first
const lowerIndex = datasets.length;
datasets.push({
    label: 'Support',
    data: lowerLine,
    borderColor: '#26A69A',
    fill: false,
    order: 2
});

// Draw upper boundary with fill TO lower
datasets.push({
    label: 'Resistance',
    data: upperLine,
    borderColor: '#26A69A',
    backgroundColor: 'rgba(38, 166, 154, 0.25)',
    fill: lowerIndex,  // Fill to support dataset (Chart.js native)
    order: 2
});
```

**See**: [FRAMEWORK-PATTERNS.md](FRAMEWORK-PATTERNS.md#dataset-to-dataset-fill)

---

### Pattern: Edge Case Testing
**Use when**: Validating mathematical correctness

```javascript
// Test data with weekend gap
const testData = [
    { x: Date.parse('2024-01-01'), y: 100 },  // Mon
    { x: Date.parse('2024-01-02'), y: 102 },  // Tue
    { x: Date.parse('2024-01-03'), y: 104 },  // Wed
    // Weekend gap (Thu-Sun missing)
    { x: Date.parse('2024-01-08'), y: 106 },  // Mon (5 days later!)
    { x: Date.parse('2024-01-09'), y: 108 },  // Tue
];

const trendline = fitLinearTrendline(testData);

// Validation: Line should stay straight
// If wavy → domain mismatch bug
```

**See**: [VALIDATION.md](VALIDATION.md#edge-case-testing)

---

## Anti-Patterns

### ❌ Index-Based Regression on Time Axis
```javascript
// BAD: Using array indices on continuous time axis
const sumX = points.reduce((sum, p, i) => sum + i, 0);
return { x: p.x, y: slope * i + intercept };
// Result: Wavy lines at weekend gaps
```

**Fix**: Use timestamp-based regression → [MATHEMATICAL-CORRECTNESS.md](MATHEMATICAL-CORRECTNESS.md#domain-mismatch)

---

### ❌ Custom Polygon Fill (Chart.js)
```javascript
// BAD: Concatenating reversed arrays
const polygon = [...upperLine, ...lowerLine.reverse()];
datasets.push({ data: polygon, fill: true });
// Result: Doesn't render correctly in Chart.js
```

**Fix**: Use dataset-to-dataset fill → [FRAMEWORK-PATTERNS.md](FRAMEWORK-PATTERNS.md#polygon-vs-dataset-fill)

---

### ❌ Visual-Only Validation
```javascript
// BAD: Stopping at "looks good"
console.log('Screenshot looks good! Ship it!');
// Missing: Code review, edge cases, math verification
```

**Fix**: Progressive validation (4 layers) → [VALIDATION.md](VALIDATION.md#progressive-evidence)

---

### ❌ Same Layer Order for All Elements
```javascript
// BAD: Random rendering order
datasets.push({ order: 1 });  // Fill
datasets.push({ order: 1 });  // Line
datasets.push({ order: 1 });  // Data
// Result: Unpredictable z-index
```

**Fix**: Explicit layering (1=data, 2=lines, 3=fills) → [VISUAL-HIERARCHY.md](VISUAL-HIERARCHY.md#layer-ordering)

---

## Integration with Other Skills

**Complements**:
- `frontend-design`: Aesthetic UI design (this skill: technical correctness)
- `telegram-uiux`: Telegram-specific patterns (this skill: general data viz)
- `testing-workflow`: General testing (this skill: visualization-specific validation)

**References**:
- See `docs/frontend/UI_PRINCIPLES.md` for comprehensive principles
- See `.claude/implementations/2026-01-05-shaded-pattern-visualization.md` for implementation case study
- See `.claude/implementations/2026-01-05-proper-pattern-trendlines-all-types.md` for pattern-specific details

---

## Real-World Example

**Problem**: Chart pattern trendlines appeared wavy at weekends, user feedback "I don't like the look"

**Root causes**:
1. Visual: Simple thin lines blended into chart (low contrast)
2. Mathematical: Index-based regression on continuous time axis (domain mismatch)

**Solutions applied**:
1. Visual: Shaded regions (25% opacity) + bold lines (3px) + layer ordering
2. Mathematical: Timestamp-based regression (domain match)
3. Validation: Tested with weekend gap data (edge cases)

**Outcome**: ✅ Patterns 3-5x more visible, ✅ Straight lines across gaps, ✅ Professional appearance

**See**: `.claude/evolution/2026-01-05-data-visualization-principles.md` for full case study

---

## Quick Checklist

**Before implementation**:
- [ ] Research framework features (Chart.js docs, examples)
- [ ] Identify axis domain (time, categories, continuous)
- [ ] Plan layer ordering (data=1, lines=2, fills=3)

**During implementation**:
- [ ] Use framework-native features (dataset-to-dataset fill)
- [ ] Match regression domain to axis domain (timestamps for time axis)
- [ ] Apply visual hierarchy (shaded regions, bold lines)

**After implementation**:
- [ ] Visual validation (screenshot, looks right?)
- [ ] Code review (framework patterns correct?)
- [ ] Edge case testing (weekend gaps, nulls, holidays)
- [ ] Mathematical verification (domain match, formula correct?)

---

**See detailed documentation**:
- [VISUAL-HIERARCHY.md](VISUAL-HIERARCHY.md) - Layering, prominence, opacity
- [MATHEMATICAL-CORRECTNESS.md](MATHEMATICAL-CORRECTNESS.md) - Domain compatibility, regression, edge cases
- [FRAMEWORK-PATTERNS.md](FRAMEWORK-PATTERNS.md) - Chart.js patterns, native features
- [VALIDATION.md](VALIDATION.md) - Progressive validation, 4-layer evidence

---

**Last Updated**: 2026-01-05
**Version**: 1.0.0
**Source**: Distilled from candlestick chart pattern visualization work
