---
name: probe-estimation
description: Use to apply PROBE (PROxy-Based Estimation) method for story sizing. Uses historical data for accurate effort estimation.
version: 1.0.0
---
<!-- Powered by PRISMâ„¢ Core -->

# PROBE Estimation Task

## When to Use

- When estimating effort for a new story
- During sprint planning for sizing stories
- When comparing story complexity to historical work
- When calibrating estimation accuracy over time

## Quick Start

1. Load historical story data (if available)
2. Map story to size category (VS, S, M, L, VL)
3. Compare against proxy stories
4. Calculate estimated hours
5. Document estimation rationale

## Purpose

Apply the PROBE (PROxy-Based Estimation) method from PSP to estimate story size and effort using historical data and relative size comparison. This integrates with story creation to build estimation accuracy over time.

## Background

PROBE uses relative size categories and historical performance to create statistically-grounded estimates without requiring LOC counting. It tracks actual vs estimated to continuously improve estimation accuracy.

## SEQUENTIAL Task Execution

### 1. Gather Historical Data (if available)

Check for previous stories in `devStoryLocation` and extract:
- Story complexity ratings (VS, S, M, L, VL)  
- Estimated hours from story files
- Actual completion time (from Status timestamps)
- Story points if available

If no historical data exists, use these initial proxy values:
```yaml
initial_proxies:
  very_small: 2 hours
  small: 4 hours
  medium: 8 hours
  large: 16 hours
  very_large: 32 hours
```

### 2. Map Story Points to Size Category

Convert existing story points to PROBE size categories:

```yaml
story_point_mapping:
  1: very_small
  2: small
  3: medium
  5: large
  8: very_large
  
size_categories:
  very_small:
    story_points: 1
    description: "Simple config change or single-file update"
    typical_tasks: 1-2
    complexity: "Trivial logic, no dependencies"
    
  small:
    story_points: 2
    description: "Single feature or bug fix"
    typical_tasks: 3-5
    complexity: "Simple logic, minimal dependencies"
    
  medium:
    story_points: 3
    description: "Multi-component feature"
    typical_tasks: 6-10
    complexity: "Moderate logic, some integration"
    
  large:
    story_points: 5
    description: "Cross-system feature"
    typical_tasks: 11-20
    complexity: "Complex logic, significant integration"
    
  very_large:
    story_points: 8
    description: "Architectural change or major feature"
    typical_tasks: 20+
    complexity: "Very complex, multiple systems"
```

If story already has points assigned (from sprint planning or dev-task-tmpl), use the mapping.
Otherwise, analyze the story characteristics to assign appropriate points and size.

### 3. Find Similar Stories (Proxy Selection)

Search historical stories for similar characteristics:
- Similar technical components (frontend/backend/database)
- Similar task count
- Similar acceptance criteria count
- Similar risk profile

If found, use their actual completion times as proxies.

### 4. Calculate Estimate

Using PROBE calculation:

```yaml
probe_calculation:
  # If historical data exists
  with_history:
    beta0: regression_intercept  # From historical data
    beta1: regression_slope      # From historical data
    estimate: beta0 + (beta1 * proxy_size)
    range:
      optimistic: estimate * 0.7
      likely: estimate
      pessimistic: estimate * 1.5
  
  # Without historical data
  without_history:
    estimate: selected_proxy_value
    range:
      optimistic: estimate * 0.5
      likely: estimate
      pessimistic: estimate * 2.0
```

### 5. Add Estimation Data to Story

Append to story file in Dev Notes section:

```yaml
psp_estimation:
  method: "PROBE"
  story_points: {1|2|3|5|8}  # From sprint planning
  size_category: "{very_small|small|medium|large|very_large}"  # Mapped from points
  proxy_stories: 
    - "{epic.story} - {actual_hours}h"
  estimated_hours:
    optimistic: X
    likely: Y
    pessimistic: Z
  confidence: "{high|medium|low}"
  estimation_date: "YYYY-MM-DD"
  start_date: null  # Set when story starts
  end_date: null    # Set when story completes
  actual_hours: null # Calculate from dates
```

**Automatic Mapping:**
- Story Points (1,2,3,5,8) â†’ Size Categories (VS,S,M,L,VL)
- Preserves agile story points while adding PSP size tracking
- Both metrics tracked for correlation analysis

### 6. Track Actuals for Future Estimates

When story is marked complete, update the estimation section:
- Set end_date
- Calculate actual_hours from start/end dates
- Add to historical database (append to story file)

```yaml
estimation_accuracy:
  estimated: Y hours
  actual: A hours
  variance: (A-Y)/Y * 100%
  size_was_accurate: true/false
```

### 7. Continuous Improvement

After every 5 completed stories:
- Calculate estimation accuracy metrics
- Adjust proxy values based on actuals
- Update regression parameters if applicable
- Note patterns in estimation errors

Store in `../data/estimation-history.yaml` (relative to tasks folder):

```yaml
estimation_metrics:
  total_stories: N
  average_accuracy: X%
  size_distribution:
    very_small: { count: N, avg_hours: H, std_dev: S }
    small: { count: N, avg_hours: H, std_dev: S }
    medium: { count: N, avg_hours: H, std_dev: S }
    large: { count: N, avg_hours: H, std_dev: S }
    very_large: { count: N, avg_hours: H, std_dev: S }
  improvement_trend: "improving|stable|degrading"
```

## Integration Points

### With create-next-story Task

Add Step 2.5: "Execute PROBE Estimation"
- Run this task after gathering requirements
- Before populating story template
- Include estimation in Dev Notes

### With Story Template

The estimation data becomes part of the story record, enabling:
- Velocity tracking
- Capacity planning  
- Continuous estimation improvement
- Team performance metrics

### With Dev Agent

When dev agent starts a story:
- Set start_date in psp_estimation
- When completing, set end_date
- Calculate actual_hours

## Output Format

For story file Dev Notes section:

```markdown
### PSP Estimation (PROBE Method)

- **Size Category**: Medium
- **Similar Stories Used**: 
  - 1.2 User Auth (12h actual)
  - 1.5 API Integration (14h actual)
- **Estimate**: 8-13-20 hours (optimistic-likely-pessimistic)
- **Confidence**: Medium
- **Estimated**: 2024-01-15

**Tracking**:
- Started: [To be set when work begins]
- Completed: [To be set when work ends]
- Actual Hours: [To be calculated]
```

## Success Criteria

- [ ] Story has size category assigned
- [ ] Estimation includes range (O/L/P)
- [ ] Historical data referenced if available
- [ ] Tracking fields ready for actuals
- [ ] No new documents created (embedded in story)

## Benefits

1. **PSP Compliance**: Implements PROBE method from Chapter 6
2. **Minimal Overhead**: No new documents, uses existing story files
3. **Continuous Improvement**: Builds historical database automatically
4. **Team Metrics**: Enables velocity and capacity planning
5. **Objective Estimation**: Data-driven vs gut feel
