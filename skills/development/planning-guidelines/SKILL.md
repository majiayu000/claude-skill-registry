---
name: planning-guidelines
description: 'Core planning principles for Portfolio Buddy 2 development. Use when:
  planning any feature implementation, modification, or refactoring. Ensures code
  preservation, mobile/desktop optimization, and tho'
---

---
name: planning-guidelines
description: Core planning principles for Portfolio Buddy 2 development. Use when: planning any feature implementation, modification, or refactoring. Ensures code preservation, mobile/desktop optimization, and thorough requirement gathering.
---

# Planning Guidelines for Portfolio Buddy 2

## Core Principles

When planning and implementing features for Portfolio Buddy 2, always follow these fundamental principles:

1. **Preserve Existing Code** - Default to extending rather than replacing
2. **Optimize for Mobile & Desktop** - Every feature must work well on both
3. **Ask Clarifying Questions** - Gather complete context before execution
4. **Integrate Seamlessly** - New code should feel native to the existing codebase

---

## Code Preservation Strategy

### Default Behavior: Always Preserve

**Rule:** Preserve existing code unless explicitly instructed to refactor or rewrite.

When implementing new features or fixes:
- ✅ Extend existing components
- ✅ Add new functions alongside existing ones
- ✅ Preserve existing patterns and conventions
- ✅ Maintain backward compatibility
- ❌ Don't refactor working code "just because"
- ❌ Don't introduce new patterns without justification

### Exception: Massively Better Options

You MAY propose improvements to existing code **ONLY** when ALL conditions are met:

1. **Very Low Risk** - Change is isolated, well-understood, easily reversible
2. **Massive Upside** - Significant benefit (correctness, performance, maintainability)
3. **No Unnecessary Complexity** - Solution is simpler or equal complexity
4. **Clear Justification** - Can explain why exception applies

**When exception applies, you MUST:**
- Explain the problem with current implementation
- Show the proposed improvement
- Demonstrate why it meets all three criteria
- Get user approval before implementing

### Real Example: Annual Growth Rate Fix

**Situation:** During implementation of Trading Days update, discovered Annual Growth Rate calculation was mathematically incorrect.

**Current (incorrect) code:**
```typescript
const tradingPeriodDays = uniqueTradingDates.size || 1;  // 150 days
const annualGrowthRate = (totalPnl / startingCapital / tradingPeriodDays) * 365 * 100;
// Result: Inflated by mixing trading days (denominator) with calendar day annualization (365)
```

**Why exception applied:**
1. **Very Low Risk** ✅
   - Isolated calculation (one line)
   - Easy to understand (calendar days vs trading days)
   - Easily reversible if wrong

2. **Massive Upside** ✅
   - Fixes incorrect financial metric (accuracy critical)
   - Returns were inflated by ~2.4x
   - Aligns with financial industry standards

3. **No Unnecessary Complexity** ✅
   - Added 9 lines (calendar day calculation)
   - Clearer, more correct logic
   - No new dependencies

**Result:** User approved fix immediately because exception criteria were clearly met.

---

## Mobile & Desktop Optimization

Every feature must be optimized for both mobile and desktop experiences.

### Quick Reference Checklist

✅ **Use Responsive Tailwind Classes**
- Base styles for mobile (no prefix)
- `sm:` for small screens (640px+)
- `md:` for medium screens (768px+)
- `lg:` for large screens (1024px+)

✅ **Touch Targets**
- Minimum 44x44 pixels for all interactive elements
- Use `touch-manipulation` CSS class for better touch response

✅ **Test Both Viewports**
- Verify layout works on mobile and desktop before completion
- Check that text is readable on small screens
- Ensure buttons/inputs are appropriately sized

### Existing Patterns to Follow

Portfolio Buddy 2 already has excellent responsive patterns. Reference these:

**Example 1: Responsive Text Sizing**
```tsx
className="text-xs sm:text-sm"        // Smaller on mobile
className="text-base sm:text-lg"      // Larger on desktop
```

**Example 2: Responsive Spacing**
```tsx
className="gap-1 sm:gap-2"           // Tighter gaps on mobile
className="px-2 sm:px-4 py-2 sm:py-3" // Smaller padding on mobile
```

**Example 3: Responsive Layout**
```tsx
className="flex flex-col sm:flex-row"  // Stack on mobile, row on desktop
```

**Example 4: Responsive Visibility**
```tsx
<span className="hidden sm:inline">Total Margin</span>  // Hide text on mobile, show on desktop
```

**See:** [src/components/PortfolioSection.tsx](src/components/PortfolioSection.tsx) for comprehensive examples of responsive patterns throughout the application.

---

## Clarifying Questions Framework

### When to Ask Questions

Ask clarifying questions **BEFORE** executing when:
- Requirements are ambiguous
- Multiple valid approaches exist
- Decision affects architecture or user experience
- User's request could be interpreted multiple ways
- You need context about business logic or domain knowledge

### Question Format Template

Use this structure for ALL clarifying questions:

```
## Clarifying Question: [Topic]

[Brief context about why you need to ask]

**Option A: [Approach Name]** ✅ (Recommended)
- [Detail about approach]
- [Key characteristics]
- **Pros:** [Benefits]
- **Cons:** [Trade-offs]
- **Why experts prefer this:** [Technical reasoning from domain expert perspective]

**Option B: [Alternative Approach]**
- [Detail about approach]
- [Key characteristics]
- **Pros:** [Benefits]
- **Cons:** [Trade-offs]
- **Trade-offs:** [Why this isn't the top choice]

**Option C: [Another Alternative]** (if applicable)
- [Detail about approach]
- [Key characteristics]
- **Pros:** [Benefits]
- **Cons:** [Trade-offs]
- **Trade-offs:** [Why this isn't the top choice]
```

### Key Requirements

1. **Mark Best Option** - Use ✅ to indicate expert-recommended choice
2. **Explain Reasoning** - "Why experts prefer this" section required
3. **Unbiased Options** - Present all options fairly, let marking indicate preference
4. **Complete Context** - User should understand trade-offs without additional research

### Real Example: Trading Days Calculation

From today's conversation about how to calculate Trading Days:

```
## Clarifying Question 2: Trading Days Calculation with Date Filters

When the user sets a custom date range (Start Date/End Date), should Trading Days represent:

**Option A: The number of calendar days in the selected date range** ✅ (Recommended)
- Example: Jan 1 to Jan 31 = 31 days
- **Pros:** Simple, matches user's mental model of "days in range"
- **Cons:** Doesn't account for non-trading days
- **Why experts prefer this:** For portfolio analysis, calendar days provide accurate time-based performance metrics and match financial industry standards for annualized returns.

**Option B: The number of actual trading days (days with trades) within the date range**
- Example: Jan 1 to Jan 31 = only count days where trades occurred (e.g., 18 days)
- **Pros:** Reflects actual market activity
- **Cons:** Can be misleading - a strategy might not trade every day by design
- **Trade-offs:** Better for measuring trading frequency, not time-based performance
```

**Outcome:** User chose Option B, demonstrating how clear options enable informed decisions.

---

## Decision Criteria

### When to Preserve vs Improve

Use this decision tree:

```
Is the code broken or incorrect?
├─ YES → Fix it (with explanation)
└─ NO → Is there a massively better option?
    ├─ YES → Does it meet ALL exception criteria?
    │   ├─ YES → Propose improvement (get approval)
    │   └─ NO → Preserve existing code
    └─ NO → Preserve existing code
```

### Risk Assessment Checklist

Before proposing any change to existing code, verify:

- [ ] Change is isolated to specific files/functions
- [ ] No ripple effects on other features
- [ ] TypeScript compilation succeeds
- [ ] No breaking changes to interfaces
- [ ] Existing tests still pass (if tests exist)
- [ ] Can be reverted with single git revert

### Complexity Evaluation

Avoid unnecessary complexity:

- ❌ Adding new libraries when existing ones suffice
- ❌ Introducing new patterns when existing patterns work
- ❌ Over-engineering simple features
- ❌ Premature optimization
- ✅ Using existing utilities and components
- ✅ Following established patterns
- ✅ Simple, readable solutions

---

## Integration with Other Skills

This skill works alongside other Portfolio Buddy 2 skills:

- **Use with `planning-framework`** - Apply Musk's 5-step algorithm and ICE scoring for feature planning
- **Reference `coding-standards`** - Follow React 19 and TypeScript standards during implementation
- **Check `architecture-reference`** - Understand component hierarchy and existing patterns before adding code
- **Consult `migration-tracker`** - Verify feature parity and check for known issues before starting
- **Load `portfolio-context`** - Get tech stack and architectural constraints context

**Workflow:**
1. Load `planning-guidelines` (this skill) → Understand principles
2. Load `planning-framework` → Plan the feature approach
3. Check `architecture-reference` → Find where code goes
4. Apply `coding-standards` → Write the code correctly
5. Update `migration-tracker` → Document what was added

---

## Real Portfolio Buddy 2 Examples

### Example 1: Risk-Free Rate Default (Code Preservation)

**Task:** Set Risk-Free Rate default to 4%

**Approach:** Pure preservation
- Found existing code: `useState<number>(0)`
- Changed ONLY the default value: `useState<number>(4)`
- Preserved everything else: input field, validation, usage in Sortino Ratio
- **Result:** One line changed, zero risk

### Example 2: Trading Days Update (Code Preservation)

**Task:** Make Trading Days recalculate when date range changes

**Approach:** Extend existing calculation
- Kept existing `tradingPeriodDays` variable and display
- Added new logic to count unique dates from filtered trades
- Preserved all downstream usage (Annual Growth Rate, etc.)
- **Result:** Extended, didn't replace

### Example 3: Total Margin Button (Seamless Integration)

**Task:** Add "Set to Total Margin" button for Starting Capital

**Approach:** Mobile/desktop optimized integration
- Added button next to existing Starting Capital input
- Used existing Portfolio Buddy 2 responsive patterns:
  - `className="flex items-center gap-1 sm:gap-2"` (responsive spacing)
  - `<span className="hidden sm:inline">Total Margin</span>` (hide text on mobile)
  - `className="h-3 w-3 sm:h-3.5 sm:w-3.5"` (smaller icon on mobile)
  - `touch-manipulation` class for better mobile interaction
- Matched existing blue theme and styling
- Only appears when `portfolioData` exists (conditional rendering)
- **Result:** Feels native, works on both viewports

### Example 4: Annual Growth Rate Fix (Exception Case)

**Task:** Originally just fixing Trading Days calculation

**Discovery:** Found Annual Growth Rate calculation was mathematically incorrect

**Exception Applied:**
- **Very Low Risk:** Isolated calculation, 9 lines added, clear logic
- **Massive Upside:** Fixed inflated returns (was ~2.4x too high), critical for financial accuracy
- **No Complexity:** Simpler logic (calendar days vs trading days), more maintainable

**Approach:**
1. Explained the problem clearly
2. Showed incorrect vs correct formula with examples
3. Demonstrated exception criteria were met
4. Got user approval
5. Implemented fix

**Result:** User approved immediately because criteria were objective and clearly met.

---

## Summary

**Always:**
- Preserve existing code by default
- Optimize for mobile AND desktop
- Ask clarifying questions with ✅ marked recommendations
- Integrate seamlessly with existing patterns

**Only when ALL criteria met:**
- Propose improvements (low risk + massive upside + no added complexity)
- Get user approval before implementing

**Never:**
- Refactor working code without justification
- Add complexity unnecessarily
- Guess at requirements when you could ask
- Ignore mobile or desktop experience

---

**This skill ensures Portfolio Buddy 2 remains maintainable, consistent, and user-friendly across all devices while preserving the stability of working code.**