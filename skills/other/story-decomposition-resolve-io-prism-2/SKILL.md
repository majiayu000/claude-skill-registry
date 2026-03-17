---
name: story-decomposition
description: Use to break down large stories into optimally-sized stories (1-3 days). Applies PSP measurement discipline.
---
<!-- Powered by PRISMâ„¢ Core -->

# Story Decomposition Task

## When to Use

- When a story estimate exceeds 3 days
- When story complexity requires breakdown
- During sprint planning for story right-sizing
- When applying PSP measurement discipline to large stories

## Quick Start

1. Load story context and historical sizing data
2. Analyze story components using decomposition patterns
3. Create sub-stories with independent value
4. Validate each sub-story is 1-3 days
5. Apply PROBE estimation to confirm sizing

## Purpose

Break down stories into optimally-sized stories using PSP measurement discipline:
- Target 1-3 day stories based on historical data
- Maintain architectural alignment in decomposition
- Ensure each story is independently valuable
- Apply PROBE estimation to validate sizing
- Create continuous flow of ready stories

## SEQUENTIAL Task Execution

### 1. Load Story and Context

**Gather Story Information:**
```yaml
story_context:
  story_number: X
  story_title: "{title}"
  business_goal: "{goal}"
  acceptance_criteria: 
    - AC1: "{criterion}"
    - AC2: "{criterion}"
  architectural_components:
    - frontend: ["components"]
    - backend: ["services"]
    - database: ["models"]
  dependencies:
    external: ["third-party APIs"]
    internal: ["other stories/stories"]
```

### 2. Analyze Historical Sizing Data

**Load from estimation-history.yaml:**
```yaml
size_calibration:
  very_small:
    typical_hours: X (from actuals)
    examples: ["Login form", "Config update"]
    complexity: "Single file, no integration"
    
  small:
    typical_hours: Y (from actuals)
    examples: ["CRUD endpoint", "Simple UI component"]
    complexity: "2-3 files, minimal integration"
    
  medium:
    typical_hours: Z (from actuals)
    examples: ["Feature with UI+API", "Data migration"]
    complexity: "Multiple components, some integration"
    
  target_range:
    minimum: 4 hours (0.5 days)
    sweet_spot: 8-16 hours (1-2 days)
    maximum: 24 hours (3 days)
    
  avoid:
    too_small: <4 hours (overhead exceeds value)
    too_large: >24 hours (needs further decomposition)
```

### 3. Identify Natural Boundaries

**Decomposition Strategies:**

```yaml
architectural_boundaries:
  vertical_slice:
    - "User-facing feature through all layers"
    - "Complete workflow from UI to database"
    - "End-to-end functionality"
    
  horizontal_layer:
    - "All API endpoints for feature"
    - "Complete UI components for screen"
    - "Database schema and migrations"
    
  functional_boundary:
    - "CRUD operations separately"
    - "Happy path vs error handling"
    - "Core feature vs enhancements"
    
  technical_boundary:
    - "Infrastructure setup"
    - "Third-party integration"
    - "Performance optimization"
```

### 4. Create Story Candidates

For each identified boundary:

```yaml
story_candidate:
  sequence: X.Y
  title: "{descriptive_title}"
  
  scope:
    includes: ["specific functionality"]
    excludes: ["what's not in this story"]
    
  value_statement:
    user_value: "What user can do"
    technical_value: "What it enables"
    
  testability:
    acceptance_criteria: ["specific ACs from story"]
    independent_testing: true/false
    
  initial_sizing:
    estimated_tasks: N
    complexity_assessment: "low|medium|high"
    predicted_size: "VS|S|M|L|VL"
    
  dependencies:
    blocks: ["stories that depend on this"]
    blocked_by: ["stories this depends on"]
```

### 5. Apply PROBE Estimation

For each candidate story:

```yaml
probe_analysis:
  size_category: "{VS|S|M|L|VL}"
  
  similar_stories:
    - "Story A.B - {actual_hours}h - {similarity_score}%"
    - "Story C.D - {actual_hours}h - {similarity_score}%"
    
  hour_estimate:
    optimistic: X (best case)
    likely: Y (expected)
    pessimistic: Z (with complications)
    
  confidence_check:
    within_target: true/false (4-24 hours)
    splitting_needed: true/false
    combining_possible: true/false
```

### 6. Optimize Story Sizes

**Split Large Stories (>24 hours):**

```yaml
splitting_strategy:
  original_story: "X.Y - {30 hours}"
  
  split_into:
    - story: "X.Y.1"
      scope: "Core functionality"
      hours: 12
      
    - story: "X.Y.2"
      scope: "Enhanced features"
      hours: 10
      
    - story: "X.Y.3"
      scope: "Error handling & edge cases"
      hours: 8
      
  maintains:
    - "Each piece independently valuable"
    - "Clear boundaries between pieces"
    - "Testable in isolation"
```

**Combine Small Stories (<4 hours):**

```yaml
combining_strategy:
  original_stories:
    - "X.A - 2 hours"
    - "X.B - 3 hours"
    
  combined_into:
    story: "X.AB"
    scope: "Combined related functionality"
    hours: 5
    rationale: "Natural cohesion, same component"
```

### 7. Sequence Stories

**Order by Dependencies and Value:**

```yaml
story_sequence:
  phase_1_foundation: # Must do first
    - X.1: "Database schema" (S, 8h)
    - X.2: "Core API endpoints" (M, 16h)
    
  phase_2_features: # Build on foundation
    - X.3: "Basic UI" (M, 12h)
    - X.4: "User workflows" (L, 20h)
    
  phase_3_enhancement: # Optional/later
    - X.5: "Advanced features" (M, 16h)
    - X.6: "Performance optimization" (S, 8h)
    
  continuous_flow:
    ready_now: [X.1, X.2]
    ready_when_1_done: [X.3]
    ready_when_2_done: [X.4]
```

### 8. Validate Decomposition

**Quality Checks:**

```yaml
validation:
  coverage:
    all_acs_covered: true/false
    story_goal_achievable: true/false
    
  sizing:
    all_within_target: X/Y stories
    average_size: Z hours
    size_distribution:
      VS: N stories
      S: N stories  
      M: N stories
      L: N stories
      VL: N stories (flag if >0)
      
  dependencies:
    circular: false
    external_identified: true
    sequence_logical: true
    
  testability:
    all_independently_testable: true/false
    clear_acceptance_criteria: true/false
    
  architectural:
    boundaries_respected: true/false
    components_aligned: true/false
```

### 9. Create Story Files

For each story, generate story file with:
- Complete story definition
- PROBE estimation included
- Dependencies documented
- Architectural alignment noted
- Ready for development marker

### 10. Generate Decomposition Report

```markdown
# Story X Decomposition Report

## Summary
- Story: {title}
- Total Stories: N
- Total Estimated Hours: X
- Average Story Size: Y hours
- Confidence: High/Medium/Low

## Story Map
[Visual representation of story sequence and dependencies]

## Size Distribution
- Target (4-24h): N stories (X%)
- Too Small (<4h): N stories  
- Too Large (>24h): N stories

## Story Sequence
1. X.1 - {title} - {size} - {hours}h
2. X.2 - {title} - {size} - {hours}h
...

## Architectural Alignment
- Frontend: Stories X.A, X.B
- Backend: Stories X.C, X.D
- Database: Stories X.E, X.F

## Risk Factors
- Large stories needing monitoring
- Complex dependencies
- External blockers

## Recommendations
- Start with stories: [X.1, X.2]
- Monitor for splitting: [X.7]
- Consider combining: [X.8, X.9]
```

## Success Criteria

- [ ] All story ACs covered by stories
- [ ] No story larger than 3 days (24 hours)
- [ ] Few stories smaller than 0.5 days (4 hours)
- [ ] Each story independently valuable
- [ ] Dependencies clearly mapped
- [ ] Architectural boundaries respected
- [ ] PROBE estimates for all stories
- [ ] Continuous flow sequence defined

## Output

- Individual story files created
- Story decomposition report
- Updated estimation history
- Story dependency map
- Ready for continuous development flow
