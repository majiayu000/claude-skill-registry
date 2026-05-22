---
name: code-cleanup-agent
description: Code cleanup agent that organizes codebase by moving inline CSS to external files, extracting functions to proper locations, and removing unused code. Use when refactoring, cleaning up technical debt, or improving code organization.
---

# Code Cleanup Agent

This skill provides automated code cleanup and organization for the Advisor project, ensuring CSS is properly externalized, functions are organized in the correct directories, and unused code is removed.

## Core Principles

**"Clean code is not written by following a set of rules. You don't become a software craftsman by learning a list of what to do and what not to do. Professionalism and craftsmanship come from discipline and practice."** - Robert C. Martin

The cleanup agent follows these principles:
1. **Separation of Concerns**: HTML, CSS, and PHP logic should be in separate files
2. **DRY (Don't Repeat Yourself)**: Eliminate code duplication
3. **Single Responsibility**: Each file/function should have one clear purpose
4. **Clean Architecture**: Follow the project's established directory structure

## Project Structure Standards

```
advisor/
├── index.php              # Main entry point (minimal inline styles)
├── login.php              # Login page (minimal inline styles)
├── _css/                  # All CSS files
│   ├── style.css          # Main stylesheet (already exists)
│   ├── login.css          # Login-specific styles (to be created)
│   └── dashboard.css      # Dashboard-specific styles (to be created)
├── _fun/                  # Reusable functions
│   ├── function_logs.php      # Logging functions
│   ├── function_analytics.php # Analytics functions
│   ├── function_auth.php      # Authentication helpers
│   └── function_ui.php        # UI helper functions
├── _inc/                  # Include files
│   └── include_log.php    # Activity logging include
└── _logs/                 # Log files
```

## Cleanup Workflow

### Phase 1: CSS Extraction
**Goal**: Move all inline `<style>` blocks to external CSS files

**Process**:
1. Scan all PHP files for `<style>` tags
2. Identify page-specific vs. global styles
3. Create dedicated CSS files for each page if needed
4. Move styles to appropriate files
5. Replace `<style>` blocks with `<link>` tags
6. Preserve any CSS variables and ensure consistency

**Example Transformation**:

**Before** ([login.php](login.php)):
```php
<head>
    <style>
        body { display: flex; }
        .login-card { background: #FEFBF3; }
    </style>
</head>
```

**After**:
```php
<head>
    <link rel="stylesheet" href="_css/style.css">
    <link rel="stylesheet" href="_css/login.css">
</head>
```

**New File** ([_css/login.css](_css/login.css)):
```css
/* Login Page Specific Styles */
body {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}

.login-card {
    background: #FEFBF3;
    /* ... rest of styles */
}
```

### Phase 2: Function Extraction
**Goal**: Move PHP functions to appropriate files in `_fun/` directory

**Process**:
1. Identify standalone functions in PHP files
2. Categorize functions by purpose:
   - **Authentication**: `function_auth.php`
   - **Logging**: `function_logs.php`
   - **Analytics**: `function_analytics.php`
   - **UI Helpers**: `function_ui.php`
3. Move functions to appropriate files
4. Add proper function documentation
5. Include function files where needed using `require_once`

**Function Categories**:

**Authentication Functions** ([_fun/function_auth.php](_fun/function_auth.php)):
- `checkUserLogin()` - Verify user session
- `handleGoogleOAuth()` - Process OAuth callback
- `logoutUser()` - Destroy session and logout
- `sanitizeUserInput()` - Clean user input

**Logging Functions** ([_fun/function_logs.php](_fun/function_logs.php)):
- `logUserActivity()` - Log user actions
- `writeLog()` - Write to log files
- `getActivityLogs()` - Retrieve user activity

**Analytics Functions** ([_fun/function_analytics.php](_fun/function_analytics.php)):
- `trackPageView()` - Track page visits
- `recordUserAction()` - Record specific actions
- `getAnalytics()` - Retrieve analytics data

**UI Helper Functions** ([_fun/function_ui.php](_fun/function_ui.php)):
- `renderCard()` - Generate card HTML
- `renderMentorItem()` - Generate mentor list item
- `escapeOutput()` - Safely escape output (wrapper for htmlspecialchars)

### Phase 3: Unused Code Detection
**Goal**: Identify and remove unused code, variables, and functions

**Detection Methods**:
1. **Unused Variables**: Variables assigned but never read
2. **Duplicate CSS**: Same styles defined multiple times
3. **Dead Code**: Unreachable code or commented-out blocks
4. **Unused Imports/Includes**: Files included but never used
5. **Orphaned Functions**: Functions defined but never called

**Analysis Checklist**:
- [ ] Scan for TODO comments and placeholders
- [ ] Find duplicate CSS rules
- [ ] Identify unused PHP variables
- [ ] Locate commented-out code blocks
- [ ] Check for unused function definitions
- [ ] Find redundant includes/requires

### Phase 4: Code Consistency
**Goal**: Ensure consistent coding standards across the project

**Standards**:

**PHP Standards**:
```php
<?php
// File header comment
/**
 * Brief description of file purpose
 * @author Advisor Team
 */

// Proper spacing
session_start();

// Function documentation
/**
 * Check if user is logged in
 * @return bool True if logged in, false otherwise
 */
function checkUserLogin() {
    return isset($_SESSION['user_id']);
}

// Consistent naming: camelCase for functions
// Consistent indentation: 4 spaces
?>
```

**CSS Standards**:
```css
/* Section headers with clear boundaries */
/* ============================================
   SECTION NAME
   ============================================ */

/* Use CSS variables from style.css */
.element {
    padding: var(--spacing-md);
    color: var(--color-charcoal);
}

/* Consistent spacing and organization */
```

**HTML Standards**:
```html
<!-- Clear indentation (4 spaces) -->
<!-- Semantic HTML5 elements -->
<!-- Proper attribute ordering: class, id, data-*, other -->
<div class="card" id="welcome-card" data-section="dashboard">
    <h2>Welcome</h2>
</div>
```

## Cleanup Commands

### Full Cleanup
**Command**: "Run full code cleanup"

**Actions**:
1. Extract all inline CSS to external files
2. Move all functions to appropriate `_fun/` files
3. Remove unused code
4. Standardize code formatting
5. Update all file references
6. Generate cleanup report

### CSS Only Cleanup
**Command**: "Clean up CSS only"

**Actions**:
1. Extract inline styles from all PHP files
2. Organize into page-specific CSS files
3. Remove duplicate CSS rules
4. Ensure CSS variables are used consistently
5. Add proper CSS comments

### Function Organization
**Command**: "Organize PHP functions"

**Actions**:
1. Scan for loose functions in PHP files
2. Move to appropriate `_fun/` files
3. Add function documentation
4. Update includes/requires
5. Remove duplicate functions

### Dead Code Removal
**Command**: "Remove unused code"

**Actions**:
1. Identify unused variables
2. Find commented-out code
3. Locate unreferenced functions
4. Remove or flag for review
5. Generate report of removed code

## Cleanup Report Format

After cleanup, generate a detailed report:

```markdown
# Code Cleanup Report
Date: [YYYY-MM-DD]

## Summary
- Files processed: X
- CSS lines extracted: X
- Functions moved: X
- Dead code removed: X lines
- Duplicate code eliminated: X instances

## CSS Extraction
### Files Created
- `_css/login.css` (245 lines) - Login page styles
- `_css/dashboard.css` (320 lines) - Dashboard styles

### Files Modified
- `login.php` - Removed 307 lines of inline CSS
- `index.php` - Removed 322 lines of inline CSS

## Function Organization
### Functions Moved
- `checkUserLogin()` → `_fun/function_auth.php`
- `logUserActivity()` → `_fun/function_logs.php`

### New Files Created
- `_fun/function_auth.php` (4 functions)
- `_fun/function_ui.php` (6 functions)

## Code Removed
### Unused Variables
- `$unused_var` in login.php:45 (never used)

### Commented Code
- login.php:60-75 (15 lines of old OAuth code)

### Duplicate CSS
- `.container` definition (appeared 3 times, consolidated)

## Recommendations
- [ ] Review TODO comments at login.php:16
- [ ] Consider creating `_fun/function_validation.php` for input validation
- [ ] Add PHPDoc comments to all functions
- [ ] Consider implementing autoloader for function files

## Files Changed
1. login.php (−307 lines CSS, +2 lines link tags)
2. index.php (−322 lines CSS, +2 lines link tags)
3. _css/login.css (CREATED, +307 lines)
4. _css/dashboard.css (CREATED, +322 lines)
5. _fun/function_auth.php (CREATED, +45 lines)
6. _fun/function_ui.php (CREATED, +78 lines)

## Next Steps
1. Test all pages to ensure styles load correctly
2. Verify all functions work after extraction
3. Update CLAUDE.md with new file structure
4. Run through manual QA checklist
```

## Safety Protocols

### Before Cleanup
1. **Backup Check**: Ensure git repository is clean or create backup
2. **Dependency Analysis**: Map all file dependencies
3. **Function Usage**: Track where each function is called
4. **Style Scope**: Identify global vs. page-specific styles

### During Cleanup
1. **Incremental Changes**: Make changes in small, testable chunks
2. **Preserve Functionality**: Never break working features
3. **Comment Preservation**: Keep meaningful comments
4. **Version Notes**: Document what was changed and why

### After Cleanup
1. **Functionality Test**: Verify all pages still work
2. **Style Verification**: Ensure all styles load correctly
3. **Cross-browser Check**: Test in multiple browsers
4. **Performance Audit**: Verify no performance regression

## Common Cleanup Patterns

### Pattern 1: Login Page CSS
**Issue**: 268 lines of inline CSS in login.php

**Solution**:
1. Create `_css/login.css`
2. Move page-specific styles (body flex, login-card, etc.)
3. Keep global styles in `_css/style.css`
4. Link both files in `<head>`

### Pattern 2: Duplicate Styles
**Issue**: Same styles in multiple files

**Solution**:
1. Extract common styles to `_css/style.css`
2. Use CSS classes instead of inline styles
3. Utilize CSS variables for consistency

### Pattern 3: Inline PHP Logic
**Issue**: Business logic mixed with HTML

**Solution**:
1. Extract logic to separate functions
2. Move functions to appropriate `_fun/` files
3. Keep PHP in templates minimal (display only)

### Pattern 4: Hardcoded Values
**Issue**: Colors, sizes, URLs hardcoded throughout

**Solution**:
1. Use CSS variables for design tokens
2. Create constants file for PHP values
3. Centralize configuration

## Integration with Existing Structure

The cleanup agent respects the existing project structure defined in CLAUDE.md:

```
advisor/
├── _css/           # ← All CSS goes here (cleanup target)
├── _fun/           # ← All functions go here (cleanup target)
├── _inc/           # ← Include files (check for optimization)
├── _logs/          # ← Logs (check file permissions)
├── index.php       # ← Cleanup inline styles/functions
└── login.php       # ← Cleanup inline styles/functions
```

## Usage Examples

### Example 1: Full Project Cleanup
**User**: "Run full code cleanup on the project"

**Agent Process**:
1. Scan all PHP files for inline CSS
2. Create `_css/login.css` and `_css/dashboard.css`
3. Move all inline styles to appropriate CSS files
4. Update PHP files with `<link>` tags
5. Scan for loose functions
6. Create/update function files in `_fun/`
7. Remove commented-out code
8. Generate cleanup report
9. Ask user to review before committing

### Example 2: CSS-Only Cleanup
**User**: "Extract all CSS to external files"

**Agent Process**:
1. Analyze inline `<style>` blocks in all PHP files
2. Categorize styles (global vs. page-specific)
3. Create page-specific CSS files
4. Move styles preserving structure
5. Update HTML with links
6. Test that styles still apply
7. Generate CSS extraction report

### Example 3: Function Organization
**User**: "Organize all PHP functions into _fun/ directory"

**Agent Process**:
1. Scan PHP files for function definitions
2. Categorize by purpose (auth, logging, UI, analytics)
3. Create necessary function files
4. Move functions with documentation
5. Add `require_once` statements
6. Test function calls still work
7. Report moved functions

## Best Practices

### DO:
✅ Make incremental changes
✅ Test after each major change
✅ Preserve meaningful comments
✅ Use CSS variables from style.css
✅ Follow established naming conventions
✅ Document all functions with PHPDoc
✅ Group related styles together
✅ Maintain alphabetical ordering in CSS
✅ Keep backups before major refactoring

### DON'T:
❌ Delete code without analyzing usage
❌ Break existing functionality
❌ Mix page-specific and global styles
❌ Remove TODO comments without asking
❌ Change functionality during cleanup
❌ Ignore project structure conventions
❌ Skip testing after changes
❌ Commit without review

## Quality Checklist

After cleanup, verify:

### CSS Quality
- [ ] No inline `<style>` tags remain (except critical path CSS if needed)
- [ ] All page-specific CSS in dedicated files
- [ ] Global styles use CSS variables
- [ ] No duplicate CSS rules
- [ ] Proper CSS organization with section comments
- [ ] All `<link>` tags in `<head>` section
- [ ] Styles load in correct order (global → specific)

### PHP Quality
- [ ] All functions in `_fun/` directory
- [ ] Functions properly categorized
- [ ] All functions have PHPDoc comments
- [ ] No duplicate function definitions
- [ ] Proper `require_once` statements
- [ ] No unused variables
- [ ] Minimal inline logic in templates

### Code Quality
- [ ] Consistent indentation (4 spaces)
- [ ] Proper file headers
- [ ] No commented-out code blocks
- [ ] Clear separation of concerns
- [ ] Follow PSR standards where applicable
- [ ] Semantic HTML structure
- [ ] Accessible markup (ARIA labels, alt text)

### Testing
- [ ] All pages load without errors
- [ ] Styles render correctly
- [ ] Functions execute properly
- [ ] No console errors
- [ ] Cross-browser compatibility
- [ ] Mobile responsive design maintained
- [ ] Performance not degraded

## Advanced Cleanup Features

### Smart Deduplication
The agent identifies:
- Duplicate CSS rules (same selector, same properties)
- Similar functions with minor differences (suggest consolidation)
- Redundant includes (same file required multiple times)
- Repeated code blocks (suggest function extraction)

### Dependency Mapping
Before moving code:
- Map all function calls to their definitions
- Track CSS class usage across files
- Identify include file dependencies
- Detect circular dependencies

### Impact Analysis
Before changes:
- Predict which files will be affected
- Estimate lines added/removed
- Calculate complexity reduction
- Assess performance impact

## Maintenance Workflow

### Regular Cleanup Schedule
**Weekly**: Check for new inline styles in committed code
**Monthly**: Review `_fun/` directory for consolidation opportunities
**Quarterly**: Full codebase cleanup and organization

### Continuous Monitoring
Watch for:
- New files with inline CSS
- Functions not in `_fun/` directory
- Growing commented-out code sections
- Duplicate code patterns emerging

## Error Prevention

### Common Mistakes to Avoid

**Mistake 1: Breaking CSS Specificity**
```css
/* Wrong: Moving specific style to global file */
/* _css/style.css - Don't do this */
.login-card { background: #FEFBF3; }

/* Right: Keep in page-specific file */
/* _css/login.css */
.login-card { background: #FEFBF3; }
```

**Mistake 2: Losing CSS Variable Context**
```css
/* Wrong: Hardcoding values that exist as variables */
.card { padding: 42px; }

/* Right: Use existing CSS variables */
.card { padding: var(--spacing-lg); }
```

**Mistake 3: Moving Used Code**
```php
// Wrong: Moving function that's used in same file
// This breaks execution if not properly included

// Right: Ensure require_once is added before usage
require_once '_fun/function_auth.php';
```

## Output Format

When performing cleanup, provide:

1. **Analysis Summary**: What was found
2. **Proposed Changes**: What will be changed
3. **Impact Assessment**: What might break
4. **Action Plan**: Step-by-step changes
5. **Execution**: Perform the cleanup
6. **Verification**: Test results
7. **Report**: Detailed cleanup report

## Remember

- **Cleanup is not refactoring**: Don't change functionality, just organize
- **Safety first**: Always ensure changes are reversible
- **Test thoroughly**: Every change should be tested
- **Document changes**: Keep clear record of what was moved where
- **Incremental approach**: Small, safe changes are better than big risky ones
- **Respect conventions**: Follow existing project patterns
- **Communication**: Keep the user informed of progress

---

*"Clean code always looks like it was written by someone who cares."* - Robert C. Martin
