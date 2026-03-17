---
name: new-component
description: Create a new React component following project conventions with PropTypes and test attributes
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill: Create New Component

Create a new React component following project conventions.

## Usage

```
/new-component <ComponentName> [directory]
```

## Prerequisites

This should typically be done as part of implementing a feature. Ensure:
- A feature file exists that requires this component
- Step definitions reference the component's behavior

## Steps

1. Create the component file at `src/components/{directory}/{ComponentName}.jsx`
2. Use functional component with hooks
3. Define PropTypes for type checking
4. Export the component as default
5. Add data-testid attributes for acceptance testing

## Template

```jsx
// src/components/{directory}/{ComponentName}.jsx

import { useState } from 'react';
import PropTypes from 'prop-types';

function {ComponentName}({ prop1, prop2 }) {
  // Component logic here

  return (
    <div data-testid="{component-name}">
      {/* Component content */}
    </div>
  );
}

{ComponentName}.propTypes = {
  prop1: PropTypes.string.isRequired,
  prop2: PropTypes.number
};

{ComponentName}.defaultProps = {
  prop2: 0
};

export default {ComponentName};
```

## Naming Conventions

- Component files: PascalCase (`StepEditor.jsx`)
- Test IDs: kebab-case (`data-testid="step-editor"`)
- CSS classes: kebab-case with BEM (`step-editor__input`)

## Test ID Guidelines

Add `data-testid` attributes for elements that acceptance tests need to interact with:

```jsx
<button data-testid="add-step-button">Add Step</button>
<input data-testid="step-name-input" />
<div data-testid="metrics-dashboard">...</div>
```

## Integration with Acceptance Tests

Components should be designed to support acceptance testing:

```javascript
// In step definitions
When('I click the add step button', async function () {
  const button = await this.page.$('[data-testid="add-step-button"]');
  await button.click();
});

Then('I should see the step editor', async function () {
  const editor = await this.page.$('[data-testid="step-editor"]');
  expect(editor).to.exist;
});
```
