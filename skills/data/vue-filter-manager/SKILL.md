---
name: vue-filter-manager
description: COMPREHENSIVE Vue.js filter management system that eliminates duplicate filters, standardizes filter architecture, and ensures cross-view consistency. This skill combines the capabilities of vue-filter-consistency-fixer, vue-filter-architecture-standardizer, and vue-duplicate-filter-remover to provide unified filter management.
keywords: vue, filter, management, architecture, consistency, duplication, cross-view, standardization
category: development
triggers: filter duplication, inconsistent filters, cross-view filter issues, architecture standardization
---

# Vue Filter Manager Skill

**Purpose**: Comprehensive Vue.js filter management system that provides unified filter architecture, eliminates duplication, and ensures consistency across all views.

## Problem Solved

Pomo-Flow has a sophisticated filtering system but suffers from multiple issues:
- **Duplicate Filter Controls**: Multiple views implement their own inline filters alongside FilterControls
- **Inconsistent Implementation**: Mixed patterns across BoardView, CalendarView, and CanvasView
- **Cross-View Synchronization**: No unified filter state management across views
- **Architecture Fragmentation**: No standardized approach to filter implementation

## Combined Capabilities

This skill merges three specialized filter skills:

### From vue-filter-consistency-fixer:
- Filter analysis and inconsistency detection
- Cross-view filter state synchronization
- Reactivity problem solving

### From vue-filter-architecture-standardizer:
- Removal of inline filter implementations
- Enhanced FilterControls component
- Centralized filter state management

### From vue-duplicate-filter-remover:
- Route-based conditional rendering
- Automatic duplicate detection
- Clean deduplication implementation

## Features

### 🎯 **Filter Analysis & Detection**
- Scans all Vue components for filter usage patterns
- Identifies missing filter types in each view
- Detects duplicate filter implementations
- Analyzes filter state management patterns

### 🏗️ **Architecture Standardization**
- Removes all inline filter implementations
- Creates unified FilterControls component system
- Implements centralized state management
- Establishes consistent patterns across views

### 🔄 **Cross-View Synchronization**
- Implements Pinia-based filter state management
- Ensures consistent filter behavior across all views
- Maintains filter state during navigation
- Provides reactive filter updates

### 🚫 **Duplicate Elimination**
- Route-based conditional rendering
- Automatic duplicate detection
- Clean removal of redundant filters
- Preserves primary filter functionality

### ✅ **Validation & Testing**
- Comprehensive filter consistency testing
- Visual validation with Playwright
- Cross-view functionality testing
- Performance impact assessment

## Usage

```bash
# Run comprehensive filter management
claude skill vue-filter-manager

# The skill will:
# 1. Analyze current filter implementation
# 2. Detect duplicates and inconsistencies
# 3. Standardize architecture across views
# 4. Implement cross-view synchronization
# 5. Validate all changes with testing
```

## Technical Approach

### Phase 1: Analysis & Detection
1. **Static Analysis**: Parse Vue components to identify filter usage
2. **Pattern Detection**: Compare against established patterns
3. **Duplicate Identification**: Find overlapping filter implementations
4. **Inconsistency Mapping**: Document variations across views

### Phase 2: Architecture Standardization
1. **Inline Removal**: Remove all inline filter implementations
2. **Component Enhancement**: Enhance FilterControls with missing features
3. **State Centralization**: Move filter logic to Pinia store
4. **Route Integration**: Implement conditional rendering based on routes

### Phase 3: Implementation
1. **Code Generation**: Create standardized filter components
2. **State Management**: Implement centralized filter state
3. **Route Logic**: Add view-specific filter behavior
4. **Integration**: Ensure seamless integration with existing code

### Phase 4: Validation
1. **Functionality Testing**: Test all filter combinations
2. **Cross-View Testing**: Verify consistency across views
3. **Performance Testing**: Ensure no performance degradation
4. **Visual Testing**: Playwright validation of filter behavior

## Implementation Pattern

### Before (Multiple Approaches):
```vue
<!-- BoardView.vue - Inline filters -->
<div class="board-filters">
  <select v-model="density">Density</select>
  <button @click="toggleHideDone">Hide Done</button>
  <div class="status-filters">...</div>
</div>
<FilterControls />

<!-- TaskManagerSidebar.vue - Duplicate filters -->
<div class="sidebar-filters">
  <div class="status-filters">...</div>
</div>

<!-- CalendarView.vue - Another approach -->
<div class="calendar-filters">
  <button @click="toggleHideDone">Hide Done</button>
  <select v-model="projectFilter">Project</select>
</div>
```

### After (Unified Approach):
```vue
<!-- All views - Single FilterControls component -->
<FilterControls
  :showDensity="viewContext === 'board'"
  :showToday="viewContext === 'board'"
  :showProject="viewContext === 'calendar'"
  :showStatus="true"
  :context="viewContext"
/>
```

## Supported Views

### BoardView
- Density selector (comfortable, compact, spacious)
- Today filter toggle
- Hide completed tasks toggle
- Status filters (Backlog, Ready, Working, Done)
- Project filters

### CalendarView
- Hide completed tasks toggle
- Status filters
- Project filters
- Date-based filtering

### CanvasView
- Status filters
- Project filters
- Hide completed tasks toggle
- Smart view filters

## Success Criteria

### ✅ **Architecture Standardization**
- All views use FilterControls component exclusively
- No inline filter implementations remain
- Consistent filter API across all views
- Centralized state management implemented

### ✅ **Duplicate Elimination**
- No visual duplicate filters anywhere
- Route-based conditional rendering working
- Clean, maintainable code structure
- Preserved functionality

### ✅ **Cross-View Consistency**
- Filter state synchronized across views
- Consistent behavior regardless of active view
- Seamless filter state persistence
- Reactive updates working correctly

### ✅ **Quality Assurance**
- All filter combinations tested
- Playwright validation complete
- No performance regression
- User experience enhanced

## Configuration Options

```typescript
interface FilterManagerConfig {
  // View-specific filter settings
  boardView: {
    showDensity: true;
    showToday: true;
    showProject: true;
    showStatus: true;
  };
  calendarView: {
    showDensity: false;
    showToday: false;
    showProject: true;
    showStatus: true;
  };
  canvasView: {
    showDensity: false;
    showToday: false;
    showProject: true;
    showStatus: true;
  };

  // Global settings
  persistFilters: true;
  syncAcrossViews: true;
  enableAnimations: true;
}
```

## Compatibility

- **Vue 3** with Composition API
- **Vue Router 4+** for route-based conditional rendering
- **Pinia** for centralized state management
- **TypeScript** support with full type safety
- **Vite** development environment
- **Playwright** for automated testing

## Performance Considerations

- **Optimized Rendering**: Conditional rendering prevents unnecessary DOM nodes
- **Efficient State Management**: Centralized Pinia store prevents prop drilling
- **Lazy Loading**: Filter components load only when needed
- **Memory Efficient**: No duplicate state or event listeners

## Migration Guide

When migrating from individual filter skills:

1. **Remove Dependencies**: Uninstall or disable individual filter skills
2. **Update Imports**: Replace individual skill imports with vue-filter-manager
3. **Configuration**: Migrate any custom configurations to unified format
4. **Testing**: Validate all filter functionality works as expected

## Troubleshooting

### Common Issues:

**Filters not appearing in certain views:**
- Check view context configuration
- Verify route-based conditional rendering
- Ensure FilterControls props are correctly set

**Duplicate filters still showing:**
- Check for remaining inline filter implementations
- Verify component cleanup
- Test conditional rendering logic

**Cross-view synchronization not working:**
- Verify Pinia store configuration
- Check reactive state bindings
- Test filter state persistence

## Future Enhancements

- Advanced filter combinations and presets
- Filter usage analytics and optimization
- AI-powered filter suggestions
- Performance monitoring and optimization
- Enhanced accessibility features

---

**Result**: A unified, consistent, and maintainable filter system that eliminates duplication, standardizes architecture, and provides seamless cross-view filter synchronization for Vue.js applications.

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
