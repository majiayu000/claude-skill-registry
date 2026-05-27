---
name: component-naming
description: Enforce consistent React component naming conventions using domain + role patterns. Use when creating, reviewing, or refactoring components.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Component Naming Conventions Skill

This skill helps you enforce consistent React component naming conventions across the codebase.

## When to Use This Skill

- Creating new React components
- Reviewing component names in PRs
- Refactoring existing components
- Ensuring codebase consistency

## Naming Rules

### 1. PascalCase

All React components use PascalCase:

```typescript
// ✅ Good
export const TrendChart = () => {};
export const HeroPost = () => {};

// ❌ Bad
export const trendChart = () => {};
export const trend_chart = () => {};
```

### 2. Domain + Role Pattern

Combine domain context with component role for clarity:

```typescript
// ✅ Good - Clear domain and role
export const TrendChart = () => {};       // Trend (domain) + Chart (role)
export const HeroPost = () => {};         // Hero (domain) + Post (role)
export const MetricCard = () => {};       // Metric (domain) + Card (role)
export const LatestCoePremium = () => {}; // LatestCoe (domain) + Premium (role)

// ❌ Bad - Too generic or unclear
export const Chart = () => {};            // No domain context
export const Data = () => {};             // Meaningless
export const Item = () => {};             // No specificity
```

### 3. Compound Components for Subparts

Use dot notation for related subcomponents:

```typescript
// ✅ Good - Compound component pattern
export const HeroPost = () => {};
HeroPost.Image = () => {};
HeroPost.Title = () => {};
HeroPost.Meta = () => {};

// Usage
<HeroPost>
  <HeroPost.Image src={...} />
  <HeroPost.Title>...</HeroPost.Title>
  <HeroPost.Meta date={...} />
</HeroPost>

// ❌ Bad - Flat naming for related components
export const HeroPostImage = () => {};
export const HeroPostTitle = () => {};
export const HeroPostMeta = () => {};
```

### 4. Avoid Problematic Suffixes

Never use these suffixes:

```typescript
// ❌ Avoid these suffixes
export const MetricCardContainer = () => {};  // -Container
export const ChartWrapper = () => {};         // -Wrapper
export const DataComponent = () => {};        // -Component
export const ListElement = () => {};          // -Element

// ✅ Use clear domain + role instead
export const MetricCard = () => {};
export const TrendChart = () => {};
export const RegistrationList = () => {};
```

### 5. Avoid Layout/Styling Descriptions

Names should describe purpose, not appearance:

```typescript
// ❌ Bad - Describes layout/styling
export const LeftSidebar = () => {};
export const BigHeader = () => {};
export const RedButton = () => {};
export const TwoColumnLayout = () => {};

// ✅ Good - Describes purpose
export const NavigationSidebar = () => {};
export const PageHeader = () => {};
export const DangerButton = () => {};
export const ComparisonLayout = () => {};
```

## File Naming Convention

Files use kebab-case matching the component name:

| Component | File Name |
|-----------|-----------|
| `TrendChart` | `trend-chart.tsx` |
| `HeroPost` | `hero-post.tsx` |
| `MetricCard` | `metric-card.tsx` |
| `LatestCoePremium` | `latest-coe-premium.tsx` |

## Validation Checklist

When reviewing component names:

- [ ] Uses PascalCase
- [ ] Has clear domain context (not just "Card", "List", "Item")
- [ ] Has clear role (Chart, Card, List, Banner, etc.)
- [ ] No -Container, -Wrapper, -Component suffixes
- [ ] No layout/styling descriptions (Left, Big, Red, TwoColumn)
- [ ] File name matches component in kebab-case
- [ ] Related subcomponents use compound pattern

## Examples from Codebase

**Good patterns found:**

- `TrendAreaChart` - Trends domain + Area Chart role
- `MarketShareDonut` - Market Share domain + Donut role
- `TopMakesChart` - Top Makes domain + Chart role
- `PremiumBanner` - Premium domain + Banner role
- `MetricCard` - Metric domain + Card role
- `LatestCoePremium` - Latest COE domain + Premium role

**Anti-patterns to avoid:**

- Generic names: `Chart`, `Card`, `List`, `Data`
- Layout names: `LeftPanel`, `MainContent`, `TopSection`
- Suffix pollution: `CardContainer`, `ListWrapper`, `ItemComponent`

## Related Files

- `apps/web/CLAUDE.md` - Web app component conventions
- `apps/web/src/components/` - Web app components
- `apps/web/src/app/admin/components/` - Admin interface components
