---
name: create-documentation
description: Document a new or existing design system component
---

# Create Documentation

After creating a component in the "ui" package, always create a corresponding docs MDX file with the following structure. Comments in this example are instructions for you to fill in information.

````md
## Overview

<!-- Provide a brief description about what the component is and where it might be used. -->

## Usage

Import the component:

```ts
import { COMPONENTNAME } from '@eqtylab/equality';
```
````

Basic usage with required properties:

```ts
// Give a minimal example of the component's usage with all required properties
```

## Variants

<!-- Display the component and its variants in the best possible way given its various properties. The goal is not always to display EVERY combination of properties, rather to give developers a good overview of what is available. Display a code example either below each variant (if there are many) or as a single code block with the subheading "Usage". -->

### Variant Subheadings

<!-- Use subheading sections here when required to expose specific properties that change the component's use dramatically. For example the badge component has some stylistic variants, but a distinct subsection is used to explain that it can be made closable. -->

## Slots

<!-- If relevant, use this section to display a table explaining which slots developers should use to display content using the component. -->

| Name | Description |
| ---- | ----------- |

## Props

<!-- Display a single table of top level component properties. Always use these headings in the following example. Some elements have className properties that allow developers to override things. Don't bother listing these in the table.-->

| Name          | Description                  | Type                                   | Default   | Required |
| ------------- | ---------------------------- | -------------------------------------- | --------- | -------- |
| `propname`    | Concise one line description | `boolean`                              | True      | ✅       |
| `enumexample` | If a prop is an enum         | `neutral`, `primary`, `success`, `etc` | `neutral` | ❌       |

```

```
