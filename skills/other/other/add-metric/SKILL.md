---
name: add-metric
description: Add a new calculated metric to the VSM dashboard with test-first development
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Skill: Add New Metric

Add a new calculated metric to the VSM dashboard.

## Usage

```
/add-metric <MetricName>
```

## Prerequisites

Create a feature file first using `/new-feature` that describes:
- What the metric measures
- How it's calculated (from user perspective)
- What values indicate good/warning/critical status

## Process

1. **Feature file** - Define metric behavior in Gherkin
2. **Review** - Get approval on the metric definition
3. **Step definitions** - Write failing acceptance tests
4. **Implementation** - Build the metric

## Example Feature File

```gherkin
Feature: Flow Efficiency Metric
  As a team lead
  I want to see flow efficiency percentage
  So that I understand how much time is spent on actual work vs waiting

  Scenario: Display flow efficiency for a value stream
    Given a value stream with the following steps:
      | name        | processTime | leadTime |
      | Development | 60          | 240      |
      | Testing     | 30          | 120      |
      | Deployment  | 10          | 40       |
    When I view the metrics dashboard
    Then I should see flow efficiency of "25%"

  Scenario: Flag low flow efficiency as warning
    Given a value stream with flow efficiency below 15%
    When I view the metrics dashboard
    Then the flow efficiency card should show warning status

  Scenario: Handle empty value stream
    Given an empty value stream map
    When I view the metrics dashboard
    Then flow efficiency should show "N/A"
```

## Implementation Steps

1. Implement calculation logic in `src/utils/calculations/{metric}.js`
2. Add to the metrics store selector in `src/stores/metricsStore.js`
3. Create dashboard card in `src/components/metrics/{MetricName}Card.jsx`
4. Add educational tooltip explaining the metric
5. Write unit tests for the calculation

## Calculation Pattern

```javascript
// src/utils/calculations/{metric}.js

/**
 * Calculate {MetricName} for a value stream map
 * @param {Object} vsm - The value stream map
 * @returns {Object} - The metric result
 */
export function calculate{MetricName}(vsm) {
  if (!vsm.steps || vsm.steps.length === 0) {
    return {
      value: null,
      unit: '%',
      status: 'neutral',
      displayValue: 'N/A'
    };
  }

  // Perform calculation
  const value = /* calculation */;

  // Determine status based on thresholds
  let status;
  if (value > 0.25) {
    status = 'good';
  } else if (value > 0.15) {
    status = 'warning';
  } else {
    status = 'critical';
  }

  return {
    value,
    unit: '%',
    status,
    displayValue: `${(value * 100).toFixed(0)}%`
  };
}
```

## Dashboard Card Pattern

```jsx
// src/components/metrics/{MetricName}Card.jsx

import PropTypes from 'prop-types';
import { useMetricsStore } from '../../stores/metricsStore';
import MetricTooltip from '../ui/MetricTooltip';

function {MetricName}Card() {
  const metric = useMetricsStore((state) => state.{metricName});

  const statusClasses = {
    good: 'bg-green-50 border-green-200 text-green-800',
    warning: 'bg-amber-50 border-amber-200 text-amber-800',
    critical: 'bg-red-50 border-red-200 text-red-800',
    neutral: 'bg-gray-50 border-gray-200 text-gray-800'
  };

  return (
    <div
      className={`metric-card border rounded-lg p-4 ${statusClasses[metric.status]}`}
      data-testid="{metric-name}-card"
      data-status={metric.status}
    >
      <MetricTooltip term="{MetricName}">
        <h3 className="metric-card__title text-sm font-medium">
          {MetricName}
        </h3>
      </MetricTooltip>
      <div className="metric-card__value text-2xl font-bold">
        {metric.displayValue}
      </div>
    </div>
  );
}

export default {MetricName}Card;
```

## Common VSM Metrics

- **Flow Efficiency**: Process Time / Lead Time
- **Throughput**: Items completed per time period
- **Cycle Time**: End-to-end time for one item
- **WIP**: Current work in progress count
- **Queue Time**: Time spent waiting
- **Rework Rate**: Percentage of items requiring rework
- **First Pass Yield**: Items passing without rework
