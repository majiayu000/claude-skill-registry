---
name: migration-tracker
description: 'Context for ongoing migration from old Portfolio Buddy app. Use when:
  fixing bugs, adding migrated features, checking feature parity, or understanding
  why certain code exists. Contains list of 40 feat'
---

---
name: migration-tracker
description: Context for ongoing migration from old Portfolio Buddy app. Use when: fixing bugs, adding migrated features, checking feature parity, or understanding why certain code exists. Contains list of 40 features being migrated and known issues.
---

# Portfolio Buddy 2 - Migration Tracker

## Migration Status: 40 Features

### ✅ Completed (36/40 - 90%)
Core features migrated and working:
- CSV upload and parsing with PapaParse
- Supabase storage integration
- Basic metrics calculation (Sharpe, Max DD, CAGR, Win Rate, etc.)
- **Sortino Ratio** (completed commits 258ba3a, 9f25040)
- **Risk-free rate input** (completed commit 258ba3a)
- Asset correlation matrix (Spearman & Pearson)
- Portfolio comparison charts (Chart.js)
- Equity curve visualization
- Responsive UI with Tailwind CSS
- shadcn/ui color system integration
- **Date range filtering** (completed commit 258ba3a)
- **Contract multipliers for futures** (useContractMultipliers hook)
- **Advanced multi-column sorting** (useSorting hook)
- Error handling and validation
- File upload progress tracking
- Multiple file management

- **Database Integration** (Nov 16, 2025) - PRODUCTION READY ✓
  - Python script uploads trades automatically ✓
  - New database schema (portfolios, strategies, trades) ✓
  - Frontend database fetch ✓ (commits c4fa57c through ee7cec8)
  - Dual CSV/Database support ✓
  - Format auto-detection (1-row vs 2-row) ✓
  - User tested and verified ✓
  - Merged to main and deployed ✓
  - **See:** `dev-docs/supabase-migration-plan.md`

### 🚧 In Progress (3/40)
1. **Advanced filtering** - Partial implementation
   - Date filtering complete ✓
   - Symbol filtering needed
   - Strategy filtering needed
2. **Export functionality** - CSV export only
   - Excel export pending
   - PDF reports pending
3. **Historical comparison** - Backend ready, UI pending
   - Need UI for comparing multiple time periods

### ❌ Not Started (2/40)
1. **Multi-period analysis** - Complex, low priority
   - Compare performance across different time windows
   - Requires significant UI work
2. **Risk scenario modeling** - Requires new backend logic
   - Monte Carlo simulations
   - Stress testing

## Recent Completed Features

### Database Fetch Implementation (Nov 16, 2025) ✅ COMPLETED
**Status**: Production ready - Tested and deployed
**Commits**: c4fa57c, a5ce0ec, 676de06, eba4c8d, ee7cec8, ae9202d
**Merged to main**: d56497a (PR #1)

**Implementation Journey** (6 commits):

1. **Initial Implementation** (c4fa57c)
   - Added `calculateMetricsFromDatabase()` and `buildFilenameFromMetadata()` to dataUtils.ts
   - Rewrote `fetchFromSupabase()` in App.tsx
   - Changed from old `csv_files` table to new `strategies` + `trades` schema
   - Added TypeScript interfaces: DatabaseTrade, StrategyMetadata

2. **Fix Query Syntax** (a5ce0ec)
   - Fixed Supabase order clause syntax error
   - Changed `order('trades.trade_date')` to `order('trade_date')` with foreignTable parameter
   - Error: "failed to parse order (trades.trade_date.asc)"

3. **Fix Trade Count Limit** (676de06)
   - Discovered Supabase embedded resource limit (~60 rows)
   - Separated queries: fetch strategies first, then fetch trades separately
   - Added explicit `.limit(10000)` to get all trades
   - Fixed: 59 trades → 119 trades ✅

4. **Fix TypeScript Build Errors** (eba4c8d)
   - Added StrategyFromDB interface with optional `trades?` property
   - Added DatabaseTrade interface to App.tsx
   - Fixed: "Property 'trades' does not exist" errors

5. **Fix Metrics Calculation** (ee7cec8) ⭐ **CRITICAL FIX**
   - Auto-detect format: 2-row (Entry/Exit) vs 1-row (database)
   - Modified `calculateMetrics()` to check for "Entry/Exit" column
   - If present → loop by 2 (old CSV format)
   - If absent → loop by 1 (new database format)
   - Fixed: Metrics now calculated correctly for all 119 trades ✅

6. **Update Documentation** (ae9202d)
   - Updated migration-tracker skill with implementation details
   - Documented all changes and line numbers

**Final Results**:
- ✅ 119 trades loaded from database (not 59)
- ✅ All metrics calculated correctly (win rate, profit factor, etc.)
- ✅ CSV upload backward compatibility preserved
- ✅ Dual-mode support: both CSV and database work simultaneously
- ✅ Format auto-detection works seamlessly
- ✅ User tested and verified working
- ✅ Deployed to production

**Files Modified**:
- `src/utils/dataUtils.ts`: +235 lines (functions, interfaces, auto-detection)
- `src/App.tsx`: +145 lines (database fetch, TypeScript types)
- `.claude/skills/migration-tracker/SKILL.md`: Documentation updates

**How It Works**:
1. User clicks "Load Data" button
2. App fetches strategies from Supabase
3. For each strategy, fetches ALL trades separately (no 60-row limit)
4. Builds filename from metadata (e.g., SI_Long_Test_TestStrategy1.csv)
5. Transforms to cleanedData format with 3 columns (no Entry/Exit column)
6. `calculateMetrics()` auto-detects format and processes correctly
7. Pre-populates contract multipliers from database
8. Auto-selects strategies and displays metrics/charts

**Backward Compatibility**:
- ✅ CSV upload with 4 columns (includes Entry/Exit) → 2-row processing
- ✅ Database with 3 columns (no Entry/Exit) → 1-row processing
- ✅ Both formats work simultaneously
- ✅ All existing components, hooks, charts unchanged

### Database Integration Planning (Nov 16, 2025)
**Status**: Planning complete, ready for implementation
**What Changed**:
- Created comprehensive migration plan (`dev-docs/supabase-migration-plan.md`)
- Analyzed new Supabase database schema (portfolios, strategies, trades tables)
- Designed dual-mode support (CSV upload + database fetch)
- Planned data transformation strategy (single-row trades vs entry/exit pairs)

**New Database Schema**:
- `portfolios`: Portfolio definitions with is_master flag
- `strategies`: Strategy metadata (market, direction, contract_multiplier, etc.)
- `trades`: Individual trade records (trade_date, trade_time, profit)
- `portfolio_strategies`: Links portfolios to strategies

**Implementation Plan**:
1. Add `calculateMetricsFromDatabase()` function in dataUtils.ts (~80 lines)
2. Update `fetchFromSupabase()` query in App.tsx (~60 lines changed)
3. Transform database data to match cleanedData format
4. Pre-populate contract multipliers from database
5. Test with 119 existing trades

**Current State**:
- Python script on Windows VPS uploads trades automatically ✓
- Database contains 1 strategy with 119 trades ✓
- Frontend still queries old `csv_files` table (needs update)

**Next Steps**:
- Implement Phase 1: New calculation function
- Implement Phase 2: Update Supabase query
- Test dual CSV/Database support
- Deploy to production

### Strategy Delete Feature (Nov 19, 2025) ✅
**Commit:** c372ab7a92d267eda3e540b298872484ef09e38d
**Files:** App.tsx (+47), MetricsTable.tsx (+18), PortfolioSection.tsx (+8)

**What it does:**
- Delete database strategies permanently (red trash icon with confirmation)
- Remove CSV strategies from view (gray trash icon, immediate)
- strategyIdMap tracks DB vs CSV (App.tsx line 67)
- handleDeleteStrategy with Supabase deletion (App.tsx lines 423-458)
- Trash2 icon in Actions column (MetricsTable.tsx lines 1, 239-246)

### Git Forensic Recovery (Dec 2, 2025) ✅
**Problem:** Delete feature was "lost" (local repo behind origin/main)

**Solution:**
```bash
git fetch origin
git merge origin/main  # Fast-forward to c372ab7
```

**Key lesson:** Always check `git log origin/main` when work seems missing

### Sortino Ratio (Oct 2025)
**Commits**: 258ba3a, 9f25040
**What Changed**:
- Added risk-free rate input field in PortfolioSection (line 131: `useState<number>(0)`)
- Implemented inline Sortino calculation in PortfolioSection (lines 133-158)
- Fixed downside deviation calculation (now properly annualized using sqrt(365))
- Corrected variance calculation (divides by total returns, not just negative returns)
- Displays in portfolio stats section (line 535)

**Files Modified**:
- `PortfolioSection.tsx`: Added riskFreeRate state, downside deviation calculation, and display

**Implementation Details**:
- **NOT in dataUtils.ts** - Sortino is calculated inline in PortfolioSection using `useMemo`
- **NOT in MetricsTable** - Only displayed in portfolio stats area
- Kept in component due to portfolio-level context requirements:
  - Needs user input (risk-free rate)
  - Operates on portfolio daily returns (not trade-level metrics)
  - Different calculation scope than win rate, profit factor, etc.

### Date Range Filtering (Oct 2025)
**Commit**: 258ba3a
**What Changed**:
- usePortfolio hook now accepts date range params
- Filters trades by start/end date
- Recalculates metrics for filtered period only
- UI controls in PortfolioSection

**Files Modified**:
- `usePortfolio.ts`: Added date filtering logic
- `PortfolioSection.tsx`: Added date picker controls

### Enhanced Error Handling (Sept 2025)
**Commit**: 9fb7fdb
**What Changed**:
- Better Supabase error messages
- Client validation before upload
- Error list component shows all errors
- Toast notifications for user feedback

**Files Modified**:
- `UploadSection.tsx`: Enhanced error handling
- `ErrorList.tsx`: New component for error display
- `usePortfolio.ts`: Better error propagation

## Current Tech Debt

### High Priority
1. **PortfolioSection.tsx is 591 lines** (3x the 200-line limit)
   - Needs refactoring into:
     - `EquityChartSection.tsx`
     - `PortfolioStats.tsx`
     - `ContractControls.tsx`
   - Estimated effort: 4-6 hours

2. **Remove unused Recharts dependency** (11.5KB waste)
   - Currently using Chart.js
   - Recharts never imported anywhere
   - Run: `npm uninstall recharts`

3. **Fix 15 TypeScript `any` violations**
   - usePortfolio.ts: 11 instances
   - useMetrics.ts: 4 instances
   - dataUtils.ts: 1 instance
   - Need proper interfaces for Trade and Metric types

### Medium Priority
4. **App.tsx is 351 lines** (175% of limit)
   - Extract sections into components
   - Estimated effort: 2-3 hours

5. **MetricsTable.tsx is 242 lines** (121% of limit)
   - Improved from 350 lines
   - Still over limit, could extract more

6. **No error boundaries implemented**
   - Should wrap risky components
   - Prevents full app crashes

### Low Priority
7. **No testing setup**
   - Should test critical calculations
   - Vitest recommended for Vite projects

8. **No CI/CD pipeline**
   - Manual Cloudflare deployments
   - Could automate with GitHub Actions

## Known Issues

### Issue 1: Supabase 500 Errors
**Status**: Partially fixed (commit 9fb7fdb)
**Root cause**: Row limit exceeded on free tier
**Current workaround**:
- Enhanced error handling shows user-friendly messages
- Batch uploads in smaller chunks recommended
**Long-term fix**: Implement data aggregation before storage

### Issue 2: Large Component Files
**Status**: Documented but not fixed
**Problem**: Components grew during migration
**Affected**:
- PortfolioSection.tsx: 591 lines (was 280, now worse!)
- App.tsx: 351 lines
- MetricsTable.tsx: 242 lines (improved from 350)
**Fix needed**: Systematic refactoring into smaller components

### Issue 3: No Select All Button
**Status**: Feature doesn't exist
**Note**: Previous skill version documented a "Select All bug" but this feature was either removed or never implemented. MetricsTable has individual selection but no "Select All" functionality.

### Issue 4: Lost/Missing Code
**Status**: Recoverable via git forensics
**Problem**: Can't find recently added features or code seems to have disappeared
**Solution**:
1. Check remote: `git log origin/main --oneline -10`
2. Search commits: `git log --all --grep="keyword"`
3. Fast-forward if behind: `git merge origin/main`
4. Use reflog to see recent HEAD positions: `git reflog`
**Example**: On Dec 2, 2025, the delete feature was recovered by fast-forwarding from f4e752a to c372ab7

## Migration Priorities (ICE Scored)

| Feature | Impact | Confidence | Ease | ICE Score | Status |
|---------|--------|------------|------|-----------|--------|
| Refactor PortfolioSection | 6 | 8 | 4 | 19.2 | ❌ |
| Remove Recharts | 3 | 10 | 10 | 30 | ❌ |
| Fix TypeScript `any` | 5 | 9 | 6 | 27 | ❌ |
| Export to Excel | 8 | 8 | 7 | 44.8 | 🚧 |
| Advanced filters | 7 | 6 | 5 | 21 | 🚧 |
| Historical comparison UI | 6 | 7 | 4 | 16.8 | 🚧 |
| Error boundaries | 7 | 9 | 8 | 50.4 | ❌ |
| Testing setup | 6 | 8 | 5 | 24 | ❌ |
| Risk scenarios | 5 | 4 | 2 | 4 | ❌ |

**Top Priorities by ICE Score**:
1. Error boundaries (50.4) - High impact, easy to implement
2. Export to Excel (44.8) - User-requested feature
3. Remove Recharts (30) - Quick win, technical cleanup
4. Fix TypeScript violations (27) - Code quality
5. Testing setup (24) - Long-term maintainability

## What Changed from Old App

### Tech Stack Evolution
| Component | Old App | New App | Reason |
|-----------|---------|---------|--------|
| React | 16.x | 19.x | Latest features, better performance |
| Language | JavaScript | TypeScript | Type safety, better DX |
| Build Tool | Create React App | Vite | 10x faster builds, modern |
| Styling | Material-UI v4 | Tailwind + shadcn | More flexible, lighter |
| Charts | Recharts | Chart.js | Better performance, more features |
| State | Redux | Plain React hooks | Simpler, less boilerplate |
| Backend | Custom Node.js | Supabase | Faster development, PostgreSQL |

### State Management Migration
- **Old**: Redux with actions, reducers, middleware (complex)
- **New**: Plain React hooks (useState, useMemo, useCallback)
- **Result**: 70% less boilerplate, easier to understand

**Note**: Skills previously claimed migration to TanStack Query + Zustand, but actual implementation uses plain React hooks only.

### Why No Global State Library?
Portfolio Buddy 2 is simple enough to use React's built-in state:
- Small component tree (14 components)
- State rarely shared across distant components
- Custom hooks encapsulate shared logic effectively
- No complex async state management needed

## Migration Lessons Learned

### What Went Well
1. **Vite adoption** - Build times dropped from 30s to 2s
2. **TypeScript migration** - Caught many bugs early
3. **Chart.js over Recharts** - Better performance with large datasets
4. **Simplified state** - No Redux complexity
5. **Supabase integration** - Fast backend setup

### What Could Be Better
1. **Component size discipline** - Let components grow too large
2. **TypeScript strictness** - Too many `any` escapes
3. **Testing from start** - No tests written yet (tech debt)
4. **Code reviews** - Need refactoring before more features
5. **Documentation** - Should have updated skills continuously

### Migration Velocity
- **Weeks 1-4**: Core features (upload, parsing, basic metrics)
- **Weeks 5-8**: Charts, correlation, UI polish
- **Weeks 9-12**: Advanced features (Sortino, date filtering, sorting)
- **Current**: Maintenance, refactoring, optimization

## Next Steps

### Immediate (This Sprint)
1. Remove Recharts dependency
2. Add error boundaries to risky components
3. Fix highest-impact TypeScript `any` violations

### Short Term (Next 2 Sprints)
1. Refactor PortfolioSection into smaller components
2. Implement Excel export
3. Complete symbol/strategy filtering

### Long Term (Next Quarter)
1. Set up Vitest testing framework
2. Add CI/CD with GitHub Actions
3. Multi-period analysis UI
4. Risk scenario modeling

## Feature Parity Checklist

Comparing to old Portfolio Buddy v1:

| Feature | Old App | New App | Notes |
|---------|---------|---------|-------|
| CSV Upload | ✅ | ✅ | Improved error handling |
| Sharpe Ratio | ✅ | ✅ | Same calculation |
| Sortino Ratio | ✅ | ✅ | **Fixed** calculation (9f25040) |
| Max Drawdown | ✅ | ✅ | Same calculation |
| CAGR | ✅ | ✅ | Same calculation |
| Correlation Matrix | ✅ | ✅ | Added Pearson + Spearman |
| Equity Curves | ✅ | ✅ | Better charts with zoom/pan |
| Contract Multipliers | ❌ | ✅ | **New feature** |
| Date Filtering | ❌ | ✅ | **New feature** |
| Multi-column Sort | ✅ | ✅ | **Improved** with useSorting |
| Export to CSV | ✅ | ✅ | Same functionality |
| Export to Excel | ✅ | ❌ | **Regression** - needs reimplementation |
| Export to PDF | ✅ | ❌ | **Regression** - low priority |
| Symbol Filtering | ✅ | ❌ | **Regression** - in progress |
| Historical Compare | ✅ | ❌ | **Regression** - backend ready |

**Parity Status**: 85% (11/13 core features complete)