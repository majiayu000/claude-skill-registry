---
name: new-process-step
description: Add a new type of process step to the VSM builder with custom visualization
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Skill: Add New Process Step Type

Add a new type of process step to the VSM builder.

## Usage

```
/new-process-step <StepTypeName>
```

## Prerequisites

Create a feature file first using `/new-feature` that describes:
- How users select this step type
- What unique properties it has
- How it displays on the canvas

## Process

1. **Feature file** - Define behavior in Gherkin (must be approved)
2. **Step definitions** - Write failing acceptance tests
3. **Implementation** - Build the step type

## Implementation Steps

1. Add the step type constant to `src/data/stepTypes.js`
2. Create the custom React Flow node at `src/components/canvas/nodes/{StepTypeName}Node.jsx`
3. Register the node type in `src/components/canvas/nodeTypes.js`
4. Add default values for the step type in `src/data/stepDefaults.js`
5. Update the step creation UI in `src/components/builder/StepSelector.jsx`

## Required Properties

Every process step must include:
- `id`: Unique identifier
- `name`: Display name
- `type`: Step type constant
- `processTime`: Time for actual work (in minutes)
- `leadTime`: Total elapsed time including wait (in minutes)
- `percentCompleteAccurate`: Quality metric (0-100)
- `queueSize`: Number of items waiting
- `batchSize`: Items processed together

## Step Types Constants

```javascript
// src/data/stepTypes.js

export const STEP_TYPES = {
  PLANNING: 'planning',
  DEVELOPMENT: 'development',
  CODE_REVIEW: 'code_review',
  TESTING: 'testing',
  QA: 'qa',
  STAGING: 'staging',
  DEPLOYMENT: 'deployment',
  MONITORING: 'monitoring',
  CUSTOM: 'custom'
};
```

## Node Component Template

```jsx
// src/components/canvas/nodes/{StepTypeName}Node.jsx

import { Handle, Position } from 'reactflow';
import PropTypes from 'prop-types';

function {StepTypeName}Node({ data }) {
  return (
    <div
      className="vsm-node vsm-node--{step-type}"
      data-testid="vsm-node-{step-type}"
    >
      <Handle type="target" position={Position.Left} />
      <div className="vsm-node__header">
        <span className="vsm-node__icon">{/* Icon */}</span>
        <span className="vsm-node__name">{data.name}</span>
      </div>
      <div className="vsm-node__metrics">
        <div>PT: {data.processTime}m</div>
        <div>LT: {data.leadTime}m</div>
        <div>%C&amp;A: {data.percentCompleteAccurate}%</div>
      </div>
      <Handle type="source" position={Position.Right} />
    </div>
  );
}

{StepTypeName}Node.propTypes = {
  data: PropTypes.shape({
    name: PropTypes.string.isRequired,
    processTime: PropTypes.number.isRequired,
    leadTime: PropTypes.number.isRequired,
    percentCompleteAccurate: PropTypes.number.isRequired
  }).isRequired
};

export default {StepTypeName}Node;
```

## Example Feature File

```gherkin
Feature: Development Step Type
  As a team mapping their value stream
  I want to add development steps
  So that I can capture coding work in my process

  Scenario: Add a development step
    Given I am editing a value stream map
    When I select "Development" from the step type menu
    And I enter "Backend API" as the step name
    Then a development step should appear on the canvas
    And it should have a code icon
```
