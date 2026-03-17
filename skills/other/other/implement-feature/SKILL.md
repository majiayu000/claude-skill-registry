---
name: implement-feature
description: Implement an approved feature file using ATDD workflow with test-first development
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Skill: Implement Feature

Implement an approved feature using ATDD workflow.

## Usage

```
/implement-feature <feature-file-path>
```

## Prerequisites

- Feature file must exist and be approved
- Do NOT use this skill without an approved feature file

## Process

1. Read the approved feature file
2. Create step definitions in `features/step-definitions/`
3. Run acceptance tests (should fail)
4. Implement minimum code to pass first scenario
5. Refactor while keeping tests green
6. Repeat for remaining scenarios

## Step Definition Template

```javascript
// features/step-definitions/{feature}.steps.js

import { Given, When, Then } from '@cucumber/cucumber'
import { expect } from 'chai'

Given('I have an empty value stream map', function () {
  this.vsm = { steps: [], connections: [] }
})

When('I add a step named {string} with process time {int} minutes', function (name, processTime) {
  const step = {
    id: crypto.randomUUID(),
    name,
    processTime,
    leadTime: processTime,
    percentCompleteAccurate: 100,
    queueSize: 0,
    batchSize: 1,
  }
  this.vsm.steps.push(step)
})

Then('the map should contain {int} step(s)', function (count) {
  expect(this.vsm.steps).to.have.lengthOf(count)
})

Then('the step should display {string}', function (name) {
  const step = this.vsm.steps.find(s => s.name === name)
  expect(step).to.exist
})
```

## Implementation Order

1. **Step definitions first** - Make them fail meaningfully
2. **Data layer** - Stores, state management
3. **Business logic** - Calculations, validations
4. **UI components** - React components
5. **Integration** - Wire everything together

## Component Implementation Pattern

```jsx
// src/components/builder/StepEditor.jsx

import { useState } from 'react'
import PropTypes from 'prop-types'

function StepEditor({ step, onUpdate }) {
  const [name, setName] = useState(step?.name || '')
  const [processTime, setProcessTime] = useState(step?.processTime || 0)

  const handleSubmit = (e) => {
    e.preventDefault()
    onUpdate({ ...step, name, processTime })
  }

  return (
    <form onSubmit={handleSubmit} data-testid="step-editor">
      <label>
        Step Name
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          data-testid="step-name-input"
        />
      </label>
      <label>
        Process Time (minutes)
        <input
          type="number"
          value={processTime}
          onChange={(e) => setProcessTime(Number(e.target.value))}
          data-testid="process-time-input"
        />
      </label>
      <button type="submit">Save</button>
    </form>
  )
}

StepEditor.propTypes = {
  step: PropTypes.shape({
    id: PropTypes.string,
    name: PropTypes.string,
    processTime: PropTypes.number,
  }),
  onUpdate: PropTypes.func.isRequired,
}

export default StepEditor
```

## Testing Commands

```bash
# Run acceptance tests for specific feature
pnpm test:acceptance -- features/builder/add-step.feature

# Run in watch mode during implementation
pnpm test:acceptance --watch

# Run all acceptance tests
pnpm test:acceptance
```

## Done Criteria

- [ ] All scenarios in the feature file pass
- [ ] No skipped or pending steps
- [ ] Code is refactored and clean
- [ ] Unit tests added for complex logic
