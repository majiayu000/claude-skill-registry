---
name: portfolio-context
description: 'Auto-loaded context for Portfolio Buddy 2 development. Use for ANY task
  involving: React 19 development, TypeScript, portfolio analysis features, metrics
  calculations, trading strategy comparison, or'
---

---
name: portfolio-context
description: Auto-loaded context for Portfolio Buddy 2 development. Use for ANY task involving: React 19 development, TypeScript, portfolio analysis features, metrics calculations, trading strategy comparison, or working with the Portfolio Buddy 2 codebase. Contains tech stack, known issues, and architectural constraints.
---

# Portfolio Buddy 2 - Project Context

## Tech Stack
- **Frontend**: React 19, TypeScript, Vite
- **UI**: Tailwind CSS, shadcn/ui (color system only)
- **Charts**: Chart.js, react-chartjs-2, chartjs plugins (zoom, annotation, date adapter)
- **State**: Plain React (useState, useMemo, useCallback)
- **Data Utils**: date-fns for date manipulation
- **Backend**: Supabase (PostgreSQL)
- **Deployment**: Cloudflare Pages

## Project Purpose
Portfolio analysis tool for investors and futures traders to:
- Compare trading strategies vs benchmark assets (SPY, GLD)
- Calculate correlation matrices between assets (Spearman & Pearson)
- Analyze risk metrics and performance (Sharpe, Sortino, Max DD, etc.)
- Upload trade data via CSV and visualize results
- Apply contract multipliers to adjust metrics for futures trading
- Filter data by date range for period-specific analysis

## Known Issues & Tech Debt

### Current Tech Debt
1. **Unused Dependency**: Recharts (11.5KB) installed but never imported
   - Should be removed from package.json
   - Currently using Chart.js instead

2. **Oversized Components**: Violate 200-line standard
   - PortfolioSection.tsx (591 lines) → needs refactoring into subcomponents
   - App.tsx (351 lines) → extract sections into components
   - MetricsTable.tsx (242 lines) → improved but still over limit

3. **TypeScript Violations**: 15 instances of `any` type
   - usePortfolio.ts: 11 occurrences in trade/metrics types
   - useMetrics.ts: 4 occurrences in sort comparisons
   - dataUtils.ts: 1 occurrence in Metrics interface

### Known Bugs
1. **Supabase Upload Errors**: Intermittent 500 errors on large uploads
   - Enhanced error handling added in commit 9fb7fdb
   - Check error handling in upload hooks
   - Verify row limits aren't exceeded on free tier

## Recent Features Added
- **Sortino Ratio Calculation** (commits 258ba3a, 9f25040)
  - **Location**: Implemented inline in PortfolioSection.tsx (lines 133-158)
  - Risk-free rate input state for user-specified risk-free rate
  - Annualized downside deviation using sqrt(365) factor
  - Corrected variance calculation (divides by total returns, not just negative)
  - Displayed in portfolio stats section (line 535)
  - **Note**: NOT in dataUtils.ts - kept in component due to portfolio-level context
- **Date Range Filtering** (commit 258ba3a)
  - Filter portfolio data by start/end date
  - Implemented in usePortfolio hook
- **Advanced Multi-Column Sorting** (useSorting hook)
  - Sort by multiple columns with priority
  - Custom comparison logic per column

## Architectural Constraints
- **Component Limit**: Max 200 lines per component (currently violated by 3 components)
- **Hook Pattern**: Custom hooks in `/src/hooks/`
- **Utils Pattern**: Pure functions in `/src/utils/`
- **Type Safety**: Strict TypeScript, no `any` types (15 violations exist as tech debt)
- **State Management**: Plain React hooks only - no Zustand or TanStack Query

## Key Components Structure
```
src/
├── components/
│   ├── AnalyticsControls.tsx     (toggle Metrics/Portfolio/Correlation views)
│   ├── ContractInput.tsx         (contract multiplier inputs)
│   ├── CorrelationHeatmap.tsx    (correlation visualization)
│   ├── CorrelationSection.tsx    (correlation analysis wrapper)
│   ├── CustomTooltip.tsx         (chart tooltips)
│   ├── ErrorList.tsx             (error display)
│   ├── Header.tsx                (app header)
│   ├── MasterContractControl.tsx (apply contract value to all)
│   ├── MetricsTable.tsx          (metrics display & selection)
│   ├── PortfolioSection.tsx      (portfolio charts & analysis - 591 lines!)
│   ├── SessionComplete.tsx       (completion UI)
│   ├── SortableHeader.tsx        (table header with sort indicators)
│   ├── UploadedFilesList.tsx     (list of uploaded files)
│   └── UploadSection.tsx         (file upload to Supabase)
├── hooks/
│   ├── useContractMultipliers.ts (manage contract multipliers)
│   ├── useMetrics.ts             (calculate trading metrics)
│   ├── usePortfolio.ts           (portfolio data & date filtering)
│   └── useSorting.ts             (advanced multi-column sorting)
└── utils/
    └── dataUtils.ts              (metric calculations, CSV parsing, correlations)
```

## Migration Context
Migrating 40 features from old app (35/40 completed). See `migration-tracker` skill for details.