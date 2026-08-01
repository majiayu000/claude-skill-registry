---
name: planning-framework
description: 'Apply structured thinking before coding. Use when: starting new features,
  making architectural decisions, refactoring large components, or evaluating implementation
  approaches. Includes Musk''s 5-step'
---

---
name: planning-framework
description: Apply structured thinking before coding. Use when: starting new features, making architectural decisions, refactoring large components, or evaluating implementation approaches. Includes Musk's 5-step algorithm and ICE scoring framework.
---

# Planning Framework

## When to Use
Before starting ANY significant coding task:
- New features (> 50 lines of code)
- Refactoring existing components
- Architectural changes
- Debugging complex issues

## Musk's 5-Step Algorithm

### Step 1: Make Requirements Less Dumb
**Question everything:**
- Who requested this feature? Why?
- What problem does it actually solve?
- Is there a simpler way to achieve the same outcome?
- What happens if we don't build this?

**Portfolio Buddy 2 Example**:
> **Request**: "Add sortable columns to metrics table"
>
> **Questions**:
> - Why? Users want to find best/worst performing strategies quickly
> - Simpler solution? Just default sort by Sharpe Ratio (most important metric)
> - Alternative? Add "Top 3" and "Bottom 3" highlight sections
>
> **Decision**: Implemented full multi-column sorting via `useSorting` hook because:
> - Different users care about different metrics (Sharpe vs Sortino vs Max DD)
> - Sorting is O(n log n) - negligible for <100 strategies
> - Reusable hook can be used in future tables

### Step 2: Delete the Part or Process
**What can we eliminate?**
- Remove features that serve no clear purpose
- Cut unnecessary steps in workflows
- Simplify data structures
- Delete unused dependencies

**Rule**: If you don't add back 10% of what you deleted, you didn't delete enough.

**Portfolio Buddy 2 Example**:
> **Discovery**: Recharts library (11.5KB) installed but never imported
>
> **Questions**:
> - Is it used anywhere? NO - search reveals zero imports
> - Why was it installed? Probably initial plan, switched to Chart.js
> - Can we delete it? YES - nothing depends on it
>
> **Action**: `npm uninstall recharts` (saves 11.5KB in bundle)
>
> **Result**: Cleaner dependency tree, faster installs, smaller bundle

### Step 3: Simplify or Optimize
**Only after deleting:**
- Simplify remaining code
- Extract reusable functions
- Improve type safety
- Reduce complexity

**Portfolio Buddy 2 Example**:
> **Problem**: PortfolioSection.tsx is 591 lines (3x the 200-line limit)
>
> **Before Optimization**:
> ```typescript
> function PortfolioSection() {
>   // 50 lines of contract multiplier logic
>   // 40 lines of date filtering logic
>   // 100 lines of Chart.js configuration
>   // 80 lines of statistics calculations
>   // 300+ lines of JSX rendering
> }
> ```
>
> **After Simplification**:
> ```typescript
> // Extract hooks
> const portfolio = usePortfolio(files, dateRange)
> const contracts = useContractMultipliers(strategies)
>
> // Extract components
> <ContractControls {...contracts} />
> <EquityChartSection data={portfolio.equity} />
> <PortfolioStats metrics={portfolio.metrics} />
> ```
>
> **Result**: Main component < 100 lines, logic encapsulated, reusable

### Step 4: Accelerate Cycle Time
- Reduce build/test time
- Improve developer experience
- Add helpful error messages
- Optimize feedback loops

**Portfolio Buddy 2 Example**:
> **Before**: Create React App build time: ~30 seconds
>
> **Action**: Migrated to Vite
>
> **After**: Vite build time: ~2 seconds (15x faster)
>
> **Impact**: Developer can iterate 15x more per hour

### Step 5: Automate
Last step only - automate what's proven necessary.

**Portfolio Buddy 2 Example**:
> **Don't automate yet**: CI/CD pipeline
> - Manual Cloudflare deployments work fine for now
> - Only deploying 2-3x per month
> - Setting up GitHub Actions would take 2-4 hours
> - Wait until deployment frequency increases
>
> **Should automate**: TypeScript checking on commit
> - Would catch `any` type violations before merge
> - Git pre-commit hook: `tsc --noEmit`
> - Saves debugging time later

## ICE Scoring Framework

Evaluate solutions using:
- **Impact**: How much does this move the needle? (1-10)
- **Confidence**: How certain are we this will work? (1-10)
- **Ease**: How simple to implement? (1-10)

**ICE Score = (Impact × Confidence × Ease) / 10**

### Portfolio Buddy 2 Examples

#### Example 1: Error Boundaries (High Priority)
**Feature**: Add React error boundaries around risky components
- **Impact**: 7 (prevents full app crashes from component errors)
- **Confidence**: 9 (standard React pattern, well-documented)
- **Ease**: 8 (wrapper component + fallback UI, ~50 lines)
- **ICE Score**: (7 × 9 × 8) / 10 = **50.4** → **HIGH PRIORITY**

**Decision**: Should implement soon. Quick win, high impact.

#### Example 2: Export to Excel (Medium-High Priority)
**Feature**: Add Excel export button for metrics table
- **Impact**: 8 (users explicitly requested it)
- **Confidence**: 8 (libraries like xlsx exist, proven solution)
- **Ease**: 7 (format data, generate file, trigger download)
- **ICE Score**: (8 × 8 × 7) / 10 = **44.8** → **HIGH PRIORITY**

**Decision**: Worth implementing. Clear user value, reasonable effort.

#### Example 3: Refactor PortfolioSection (Medium Priority)
**Feature**: Split 591-line component into smaller pieces
- **Impact**: 6 (improves maintainability, no user-facing change)
- **Confidence**: 8 (clear extraction points identified)
- **Ease**: 4 (tedious, 4-6 hours, risk of breaking things)
- **ICE Score**: (6 × 8 × 4) / 10 = **19.2** → **MEDIUM PRIORITY**

**Decision**: Important for code health, but not urgent. Do after user-facing features.

#### Example 4: Real-time Price Updates via WebSocket (Low Priority)
**Feature**: Live market data updates in charts
- **Impact**: 6 (nice to have, but app analyzes historical data)
- **Confidence**: 5 (complex integration, data source needed)
- **Ease**: 3 (WebSocket setup, state management, error handling)
- **ICE Score**: (6 × 5 × 3) / 10 = **9** → **LOW PRIORITY**

**Decision**: Skip for now. Doesn't fit core use case (historical analysis).

#### Example 5: Remove Recharts Dependency (Quick Win)
**Feature**: Uninstall unused Recharts library
- **Impact**: 3 (small bundle size reduction, cleaner deps)
- **Confidence**: 10 (confirmed never imported anywhere)
- **Ease**: 10 (one command: `npm uninstall recharts`)
- **ICE Score**: (3 × 10 × 10) / 10 = **30** → **MEDIUM PRIORITY**

**Decision**: Easy quick win. Do it next time touching package.json.

#### Example 6: Sortino Ratio Calculation (Completed)
**Feature**: Add Sortino Ratio metric (already completed)
- **Impact**: 8 (important risk-adjusted metric for traders)
- **Confidence**: 9 (well-defined formula, similar to Sharpe)
- **Ease**: 7 (calculation + UI + risk-free rate input)
- **ICE Score**: (8 × 9 × 7) / 10 = **50.4** → **HIGH PRIORITY**

**Result**: Successfully implemented in commits 258ba3a & 9f25040.

### ICE Score Interpretation

| ICE Score Range | Priority | Action |
|-----------------|----------|--------|
| 40+ | High | Do soon, within 1-2 sprints |
| 25-39 | Medium-High | Plan for next 2-3 sprints |
| 15-24 | Medium | Backlog, do when capacity available |
| 10-14 | Low | Consider if very easy or strategic |
| < 10 | Very Low | Probably skip unless requirements change |

## Planning Checklist

Before coding:
- [ ] Applied Step 1: Questioned requirements thoroughly
- [ ] Applied Step 2: Identified what can be deleted/simplified
- [ ] Calculated ICE score (for features > 100 lines)
- [ ] Confirmed simpler solution doesn't exist
- [ ] Identified which components/hooks will be affected
- [ ] Checked for existing similar functionality in codebase
- [ ] Reviewed related code to understand context

After planning:
- [ ] Written approach in 3-5 bullet points
- [ ] Identified potential issues/edge cases
- [ ] Estimated time realistically (multiply initial guess by 2)
- [ ] Confirmed TypeScript types are planned (no `any`)
- [ ] Verified component won't exceed 200 lines

## Portfolio Buddy 2 Planning Examples

### Example: Adding Sortino Ratio (Completed Feature)

**Step 1 - Requirements**:
- Users need Sortino Ratio alongside Sharpe Ratio
- Sortino focuses on downside risk (more relevant for traders)
- Requires risk-free rate input

**Step 2 - Delete**:
- Don't need separate page for advanced metrics
- Don't need tutorial/help text (formula is standard)

**Step 3 - Simplify**:
- Add single risk-free rate input (not per-strategy)
- Calculate in existing `calculateMetrics()` function
- Add column to existing MetricsTable

**ICE Score**: 50.4 (High Priority)

**Approach**:
1. Add `calculateSortino()` to dataUtils.ts
2. Include Sortino in metrics calculation
3. Add risk-free rate input to PortfolioSection
4. Add Sortino column to MetricsTable
5. Test with sample data

**Time Estimate**: 3-4 hours

**Result**: Completed successfully, but found calculation bug (commit 9f25040 fixed it).

**Implementation Note**: Sortino was implemented inline in PortfolioSection.tsx (lines 133-158) rather than in dataUtils.ts. This decision was made because:
- Sortino requires portfolio-level daily returns (not trade-level metrics)
- Needs user input state (risk-free rate)
- Different calculation context than win rate, profit factor, etc.
- Team should discuss whether to extract to dataUtils for consistency

### Example: Refactoring PortfolioSection (Future Work)

**Step 1 - Requirements**:
- Component is 591 lines (3x limit)
- Hard to maintain and understand
- Want to follow coding standards

**Step 2 - Delete**:
- Review for duplicate logic
- Remove commented-out code
- Consolidate similar state handlers

**Step 3 - Simplify**:
- Extract `ContractControls.tsx` (contract multiplier UI)
- Extract `EquityChartSection.tsx` (Chart.js config)
- Extract `PortfolioStats.tsx` (statistics display)
- Keep only orchestration in main component

**ICE Score**: 19.2 (Medium Priority)

**Approach**:
1. Create EquityChartSection component (150 lines)
2. Create PortfolioStats component (80 lines)
3. Create ContractControls component (100 lines)
4. Refactor main PortfolioSection to <100 lines
5. Test all functionality still works

**Time Estimate**: 4-6 hours (tedious but straightforward)

**Risks**:
- Breaking existing functionality
- Props drilling if not careful
- Testing all edge cases

**Decision**: Medium priority. Do after more urgent user-facing features.

### Example: Vitest Testing Setup (Future Work)

**Step 1 - Requirements**:
- No tests currently
- Critical calculations need testing (Sharpe, Sortino, correlation)
- Prevent regressions in metric calculations

**Step 2 - Delete**:
- Don't need 100% coverage
- Skip UI/component testing for now
- Focus only on calculation functions

**Step 3 - Simplify**:
- Test only dataUtils.ts functions
- Use Vitest (built-in with Vite)
- Mock data from real CSV files

**ICE Score**: 24 (Medium Priority)

**Approach**:
1. Install Vitest: `npm install -D vitest`
2. Add test script to package.json
3. Create `dataUtils.test.ts`
4. Write tests for critical calculations
5. Run tests in CI eventually

**Time Estimate**: 6-8 hours (learning curve + writing tests)

**Tests to Write**:
- `calculateSharpe()` with known data
- `calculateSortino()` with known data
- `calculateCorrelation()` edge cases
- `parseCSV()` error handling

## Red Flags to Watch For

### During Planning
- ❌ "This will only take 30 minutes" (usually takes 2-3 hours)
- ❌ "I'll just use `any` types for now" (technical debt accumulates)
- ❌ "We might need this later" (YAGNI - You Aren't Gonna Need It)
- ❌ "Everyone does it this way" (verify it fits your use case)

### During Implementation
- ❌ Component approaching 200 lines (refactor NOW, not later)
- ❌ Duplicating logic from another file (extract to shared utility)
- ❌ Adding dependency without checking size/alternatives
- ❌ No error handling ("will add later" = never happens)

### Portfolio Buddy 2 Lessons
- ✅ **Did well**: Questioned need for Redux, used plain React hooks instead
- ✅ **Did well**: Chose Chart.js over Recharts after testing both
- ❌ **Should improve**: Let PortfolioSection grow to 591 lines
- ❌ **Should improve**: Accumulated 14 `any` type violations

## Framework in Action

**When you're about to start coding, ask**:
1. What am I building? (clear requirement)
2. Why am I building it? (real problem to solve)
3. What can I delete? (remove unnecessary parts)
4. What's the simplest version? (MVP approach)
5. How confident am I? (ICE scoring)
6. What's the time estimate? (be realistic, multiply by 2)

**Then write your plan as**:
- 3-5 bullet point approach
- Time estimate
- Files that will change
- Potential issues

**Finally**:
- Get feedback if >4 hours of work
- Start with smallest testable increment
- Commit frequently