---
name: css-design-token-enforcer
description: Systematically find and replace ALL hardcoded hex values with proper CSS design tokens to ensure complete color consistency across the Pomo-Flow application. This skill addresses the critical issue of yellow vs orange medium priority colors by enforcing a unified design token system based on industry best practices from Atlassian, Salesforce, and enterprise design systems.
---

# CSS Design Token Enforcer

This skill provides a comprehensive workflow for eliminating hardcoded hex values and enforcing consistent CSS design token usage across the entire Pomo-Flow codebase. It addresses the critical color inconsistency issues where medium priority tasks display different colors (yellow vs orange) across different views.

## When to Use This Skill

Use this skill when you encounter:
- **Color inconsistency**: Different shades of the same color across views (yellow vs orange medium priority)
- **Hardcoded values**: Hex values or rgba() functions in CSS that should use design tokens
- **Visual inconsistency**: Priority indicators, badges, or UI elements showing different colors
- **Design system compliance**: Need to ensure all components follow the established design token system
- **Codebase cleanup**: Systematic replacement of outdated hardcoded values

## Workflow Overview

### Phase 1: Discovery and Analysis
Run comprehensive scanning to identify all hardcoded color values and their usage patterns.

### Phase 2: Strategic Replacement
Execute automated replacement with intelligent mapping based on context, opacity levels, and component types.

### Phase 3: Validation and Testing
Verify that replacements were successful and that visual consistency is achieved across all views.

## Step-by-Step Implementation

### Step 1: Scan for Hardcoded Values
Execute the hex value finder to create a comprehensive inventory of all hardcoded colors:

```bash
python scripts/find_hardcoded_hex.py --verbose
```

**Expected Output:**
- Complete list of all hardcoded hex values
- File locations and line numbers
- Categorization by color type and priority
- Identification of critical issues (yellow vs orange discrepancy)

### Step 2: Review the Analysis Report
Examine the generated `hex_value_report.json` to understand:
- Total files with hardcoded values
- Color frequency analysis
- Priority issues requiring immediate attention
- Component-specific patterns

### Step 3: Preview Replacements (Dry Run)
Preview what changes will be made without modifying files:

```bash
python scripts/replace_with_tokens.py --dry-run --verbose
```

**Review the dry run results to confirm:**
- Correct token mappings for each hex value
- Appropriate alpha level handling
- Context-aware replacements

### Step 4: Execute Automated Replacements
Run the replacement script to systematically update all files:

```bash
python scripts/replace_with_tokens.py
```

**The script will:**
- Create automatic backups before making changes
- Apply intelligent replacements based on context
- Handle alpha values and opacity correctly
- Generate detailed modification reports

### Step 5: Validate Consistency
Run comprehensive validation to ensure success:

```bash
python scripts/validate_consistency.py
```

**Validation checks:**
- No remaining hardcoded priority colors
- Consistent color usage across all components
- Proper token naming conventions
- Visual consistency verification

### Step 6: Visual Testing
Test the application manually to confirm:
- Medium priority colors are identical across all views (Board, Calendar, Canvas, Table)
- No yellow vs orange discrepancy remains
- All UI elements display expected colors
- Hover states and interactions work correctly

## Included Tools and Resources

### Scripts Directory
- **`find_hardcoded_hex.py`**: Comprehensive scanner for hardcoded hex values with intelligent categorization
- **`replace_with_tokens.py`**: Automated replacement engine with context-aware mapping and backup creation
- **`validate_consistency.py`**: Post-replacement validation and consistency checking

### References Directory
- **`design_token_best_practices.md`**: Industry best practices from Atlassian, Salesforce, and enterprise design systems
- **`color_token_mapping.md`**: Complete mapping between hex values and appropriate CSS tokens
- **`replacement_patterns.md`**: Common patterns and edge cases for color replacement

### Assets Directory
- **`replacement_rules.json`**: Configuration file defining all replacement rules and priorities
- **`token_definitions.json`**: Complete design token definitions with usage guidelines

## Intelligent Replacement Logic

### Priority Color Mapping
The skill uses intelligent mapping based on context:

**Direct Color Replacements:**
- `#f59e0b` → `var(--color-priority-medium)` (main color)
- `#feca57` → `var(--color-priority-medium)` (yellow variant elimination)
- `#ef4444` → `var(--color-priority-high)` (high priority)
- `#3b82f6` → `var(--color-priority-low)` (low priority)

**Alpha-Aware Replacements:**
- `rgba(245, 158, 11, 0.3)` → `var(--color-priority-medium-bg)` (30% opacity)
- `rgba(245, 158, 11, 0.1)` → `var(--color-warning-alpha-10)` (10% opacity)
- `rgba(245, 158, 11, 0.2)` → `var(--color-priority-medium-border-medium)` (border context)

**Gradient Elimination:**
- `linear-gradient(180deg, var(--color-priority-medium) 0%, #feca57 100%)` → `var(--color-priority-medium)`

### Context-Aware Processing
The replacement engine considers:
- **CSS property type** (background, color, border, shadow)
- **Component context** (TaskCard, CalendarView, mobile components)
- **Alpha levels** and appropriate token variants
- **File-specific patterns** and known issues

## Critical Issues Addressed

### 1. Yellow vs Orange Discrepancy
**Root Cause**: Mixed use of `#f59e0b` (orange) and `#feca57` (yellow) for medium priority
**Solution**: Replace all instances with consistent `var(--color-priority-medium)`

### 2. Gradient Color Inconsistency
**Root Cause**: Gradients ending in different colors than they start
**Solution**: Replace gradients with solid color tokens

### 3. Hardcoded Alpha Values
**Root Cause**: Manual rgba() definitions with inconsistent opacity levels
**Solution**: Use predefined alpha variant tokens

### 4. Component-Specific Issues
**TaskCard.vue**: Multiple hardcoded rgba values
**CalendarView.vue**: Problematic gradient definitions
**BaseModal.vue**: Hardcoded shadow effects
**Mobile components**: Wrong color variables

## Quality Assurance

### Automated Validation
- **Forbidden hex detection**: Identifies remaining problematic values
- **Token compliance checking**: Ensures proper CSS variable usage
- **Consistency scoring**: Rates overall token usage compliance

### Visual Verification Checklist
- [ ] Medium priority colors identical across Board, Calendar, Canvas, and Table views
- [ ] No yellow vs orange discrepancy remains
- [ ] All hover states show consistent colors
- [ ] Mobile app colors match web application
- [ ] All focus states use appropriate glow effects

### Rollback Capability
The skill automatically creates timestamped backups before making changes:
```
.claude/css-token-backups/20231108_143022/
```

Restoration process:
1. Identify the backup directory timestamp
2. Copy specific files or entire directories back
3. Test the restoration

## Industry Best Practices Integration

This skill incorporates best practices from:

### Atlassian Design System
- Semantic naming conventions
- Consistent opacity levels
- Systematic token categorization

### Salesforce Lightning Design System
- Comprehensive token definitions
- Context-aware usage guidelines
- Validation frameworks

### Enterprise Design System Standards
- Automated enforcement strategies
- Migration best practices
- Quality assurance methodologies

## Expected Outcomes

### Primary Goal Achieved
**Complete Color Consistency**: All medium priority indicators display identical orange color (#f59e0b) across every view and component.

### Secondary Benefits
- **100% Design Token Compliance**: No hardcoded hex values remain in priority colors
- **Maintainable Codebase**: All color changes propagate automatically through token updates
- **Improved Developer Experience**: Clear, semantic token names replace cryptic hex values
- **Enhanced Design System**: Robust foundation for future color system evolution

### Quality Metrics
- **Consistency Score**: 100% (no color variations)
- **Token Usage Compliance**: 100% (all colors use CSS variables)
- **Code Quality**: Eliminated anti-patterns and inconsistencies
- **Visual Validation**: Approved across all application views

## Troubleshooting

### Common Issues and Solutions

**Issue**: Some colors still appear different after replacement
**Solution**: Check browser cache and ensure CSS variables are properly loaded

**Issue**: Replacement script skips some matches
**Solution**: Verify CSS context matches replacement rules in the configuration

**Issue**: Mobile app colors don't match web app
**Solution**: Check for additional hardcoded values in mobile-specific components

**Issue**: Validation reports false positives
**Solution**: Review replacement rules and adjust context patterns if needed

### Getting Help

1. Check the generated reports for detailed information
2. Review the reference documentation for best practices
3. Examine the configuration files for rule customization
4. Use the verbose flag for detailed output during execution

This skill provides a systematic, industry-standard approach to achieving perfect color consistency through automated design token enforcement.

---

## MANDATORY USER VERIFICATION REQUIREMENT

### Policy: No Fix Claims Without User Confirmation

**CRITICAL**: Before claiming ANY issue, bug, or problem is "fixed", "resolved", "working", or "complete", the following verification protocol is MANDATORY:

#### Step 1: Technical Verification
- Run all relevant tests (build, type-check, unit tests)
- Verify no console errors
- Take screenshots/evidence of the fix

#### Step 2: User Verification Request
**REQUIRED**: Use the `AskUserQuestion` tool to explicitly ask the user to verify the fix:

```
"I've implemented [description of fix]. Before I mark this as complete, please verify:
1. [Specific thing to check #1]
2. [Specific thing to check #2]
3. Does this fix the issue you were experiencing?

Please confirm the fix works as expected, or let me know what's still not working."
```

#### Step 3: Wait for User Confirmation
- **DO NOT** proceed with claims of success until user responds
- **DO NOT** mark tasks as "completed" without user confirmation
- **DO NOT** use phrases like "fixed", "resolved", "working" without user verification

#### Step 4: Handle User Feedback
- If user confirms: Document the fix and mark as complete
- If user reports issues: Continue debugging, repeat verification cycle

### Prohibited Actions (Without User Verification)
- Claiming a bug is "fixed"
- Stating functionality is "working"
- Marking issues as "resolved"
- Declaring features as "complete"
- Any success claims about fixes

### Required Evidence Before User Verification Request
1. Technical tests passing
2. Visual confirmation via Playwright/screenshots
3. Specific test scenarios executed
4. Clear description of what was changed

**Remember: The user is the final authority on whether something is fixed. No exceptions.**
