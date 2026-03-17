---
name: resize-story
version: 1.0.0
description: Use when a story needs to be resized based on new information. Adjusts estimates and splits/combines stories as needed.
---
<!-- Powered by PRISMâ„¢ Core -->

# Resize Story Task

## When to Use

- When story estimation exceeds 3 days (split needed)
- When story estimation is under 0.5 days (combine candidate)
- When new information changes story complexity
- During sprint planning when stories need right-sizing

## Quick Start

1. Analyze current story estimation and complexity
2. Determine if too large (>24h) or too small (<4h)
3. For large stories: identify split points at natural boundaries
4. For small stories: identify candidates to combine
5. Update estimations using PROBE method

## Purpose

Analyze and resize stories that are too large (>3 days) or too small (<0.5 days) using PSP data:
- Split large stories while maintaining value
- Combine small stories where logical
- Maintain architectural boundaries
- Update estimations using PROBE
- Ensure continuous flow efficiency

## SEQUENTIAL Task Execution

### 1. Analyze Current Story

Load story and assess size:

```yaml
story_analysis:
  id: "{story}.{story}"
  current_estimation:
    story_points: X
    size_category: "{VS|S|M|L|VL}"
    hours_estimated: Y
    confidence: "{high|medium|low}"
    
  size_assessment:
    too_large: hours > 24 (3 days)
    too_small: hours < 4 (0.5 days)
    just_right: 4 <= hours <= 24
    
  complexity_factors:
    technical_components: N
    integration_points: M
    acceptance_criteria: P
    risk_factors: ["list"]
```

### 2. Identify Split Points (If Too Large)

**Find Natural Boundaries:**

```yaml
split_analysis:
  functional_splits:
    - "Create vs Read vs Update vs Delete"
    - "Happy path vs error handling"
    - "Core feature vs enhancements"
    - "Basic vs advanced functionality"
    
  technical_splits:
    - "Frontend vs Backend vs Database"
    - "API vs UI vs Business Logic"
    - "Setup vs Implementation vs Testing"
    
  temporal_splits:
    - "Now vs Later features"
    - "MVP vs Nice-to-have"
    - "Phase 1 vs Phase 2"
    
  risk_based_splits:
    - "Known vs Unknown"
    - "Simple vs Complex"
    - "Stable vs Experimental"
```

### 3. Create Split Stories

For each split:

```yaml
split_story:
  original: "X.Y - User Management (VL, 40h)"
  
  splits:
    - id: "X.Y.1"
      title: "User Registration Flow"
      scope:
        includes: ["Registration form", "Validation", "Account creation"]
        excludes: ["Email verification", "Profile setup"]
      acceptance_criteria: [AC1, AC2, AC3]
      estimation:
        points: 3
        category: "M"
        hours: 12
      dependencies: none
      
    - id: "X.Y.2"
      title: "User Authentication"
      scope:
        includes: ["Login", "Logout", "Session management"]
        excludes: ["Password reset", "2FA"]
      acceptance_criteria: [AC4, AC5]
      estimation:
        points: 3
        category: "M"
        hours: 14
      dependencies: ["X.Y.1 for user exists"]
      
    - id: "X.Y.3"
      title: "User Profile Management"
      scope:
        includes: ["View profile", "Edit profile", "Avatar upload"]
        excludes: ["Social connections", "Preferences"]
      acceptance_criteria: [AC6, AC7, AC8]
      estimation:
        points: 2
        category: "S"
        hours: 10
      dependencies: ["X.Y.1", "X.Y.2"]
```

### 4. Validate Splits

**Check Each Split Story:**

```yaml
split_validation:
  independence:
    can_be_developed_alone: true/false
    can_be_tested_alone: true/false
    delivers_value: true/false
    
  size_check:
    within_target_range: true/false (4-24 hours)
    needs_further_split: true/false
    
  completeness:
    all_acs_covered: true/false
    no_scope_gaps: true/false
    dependencies_clear: true/false
    
  architectural:
    respects_boundaries: true/false
    maintains_cohesion: true/false
```

### 5. Combine Small Stories (If Needed)

**Find Combination Candidates:**

```yaml
combination_analysis:
  candidates:
    - stories: ["X.A (2h)", "X.B (3h)"]
      rationale: "Same component, related functionality"
      combined_hours: 5
      
    - stories: ["X.C (3h)", "X.D (2h)", "X.E (3h)"]
      rationale: "All config changes, same file"
      combined_hours: 8
      
  combination_rules:
    - "Must be related functionality"
    - "Should touch same components"
    - "Combined size still in target range"
    - "Maintains single responsibility"
    - "Dependencies align"
```

### 6. Update PROBE Estimations

For each resized story:

```yaml
re_estimation:
  story: "X.Y.1"
  
  probe_inputs:
    similar_stories:
      - "A.B - Registration (12h actual)"
      - "C.D - Form handling (10h actual)"
    
    size_factors:
      base_complexity: "medium"
      integration_points: 2
      new_technology: false
      
  new_estimate:
    optimistic: 10
    likely: 12
    pessimistic: 16
    confidence: "high"
    
  historical_update:
    add_to_proxies: true
    category: "user_management"
```

### 7. Update Dependencies

**Resequence if needed:**

```yaml
dependency_updates:
  original_sequence:
    - X.Y blocks [X.Z, X.W]
    
  new_sequence:
    - X.Y.1 blocks [X.Y.2, X.Y.3]
    - X.Y.2 blocks [X.Z]
    - X.Y.3 blocks [X.W]
    
  impact_analysis:
    delayed_stories: []
    accelerated_stories: ["X.Z can start after X.Y.2"]
    risk_changes: "Reduced risk with smaller chunks"
```

### 8. Generate Resize Report

```markdown
# Story Resize Report

## Original Story
- ID: X.Y
- Size: VL (40 hours)
- Issue: Too large for continuous flow

## Resize Action
- Action: Split into 3 stories
- Total Hours: 36 (saved 4 hours overlap)

## New Stories

### X.Y.1 - User Registration Flow
- Size: M (12 hours)
- Confidence: High
- Ready: Immediately

### X.Y.2 - User Authentication  
- Size: M (14 hours)
- Confidence: High
- Ready: After X.Y.1

### X.Y.3 - User Profile Management
- Size: S (10 hours)
- Confidence: Medium
- Ready: After X.Y.2

## Benefits
- Faster feedback cycles
- Reduced risk per story
- Parallel development possible
- Clearer scope per story

## Recommendations
- Start X.Y.1 immediately
- Consider parallel work on X.Y.2 UI while X.Y.1 backend in progress
- X.Y.3 could be deferred if needed
```

## Success Criteria

- [ ] No stories larger than 24 hours
- [ ] Minimal stories smaller than 4 hours
- [ ] Each story independently valuable
- [ ] Dependencies properly mapped
- [ ] PROBE estimates updated
- [ ] Architecture boundaries respected
- [ ] Original scope fully covered

## Output

- Updated story files (split or combined)
- Resize report with rationale
- Updated dependency map
- New PROBE estimations
- Recommendations for execution order
