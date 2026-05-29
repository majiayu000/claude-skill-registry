---
name: new-feature
description: Create a new feature file for ATDD workflow - must be done BEFORE any implementation
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill: Create New Feature

Create a new feature file for ATDD workflow. This must be done BEFORE any implementation.

## Usage

```
/new-feature <FeatureName>
```

## Process

1. Create the feature file at `features/{category}/{feature-name}.feature`
2. Write Gherkin scenarios describing the expected behavior
3. **STOP and present the feature file for review**
4. Only proceed to implementation after user approval

## Feature File Template

```gherkin
Feature: {Feature Name}
  As a {role}
  I want {capability}
  So that {benefit}

  Background:
    Given {common preconditions}

  Scenario: {Primary happy path}
    Given {initial context}
    When {action taken}
    Then {expected outcome}

  Scenario: {Alternative path or edge case}
    Given {initial context}
    When {different action}
    Then {different outcome}

  Scenario Outline: {Parameterized scenario}
    Given {context with <parameter>}
    When {action with <input>}
    Then {outcome with <expected>}

    Examples:
      | parameter | input | expected |
      | value1    | in1   | out1     |
      | value2    | in2   | out2     |
```

## VSM-Specific Scenarios

When writing features for VSM Workshop, consider these common patterns:

### Builder Features
```gherkin
Scenario: Add a process step to the value stream
  Given I have an empty value stream map
  When I add a step named "Development" with process time 60 minutes
  Then the map should contain 1 step
  And the step should display "Development"
```

### Metrics Features
```gherkin
Scenario: Calculate flow efficiency
  Given a value stream with total process time of 120 minutes
  And total lead time of 480 minutes
  When I view the metrics dashboard
  Then the flow efficiency should show "25%"
```

### Simulation Features
```gherkin
Scenario: Simulate work flowing through the stream
  Given a value stream with 3 steps
  And 10 work items in the queue
  When I run the simulation for 100 ticks
  Then I should see work items moving through each step
```

## Review Checklist

Before presenting for review, verify:
- [ ] Feature title is clear and descriptive
- [ ] User story (As a/I want/So that) captures the value
- [ ] Scenarios cover happy path
- [ ] Scenarios cover key edge cases
- [ ] Given/When/Then steps are atomic and clear
- [ ] No implementation details in scenarios
- [ ] Language is from user's perspective
