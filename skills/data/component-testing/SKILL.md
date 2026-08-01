---
name: component-testing
description: Archived skill guidance for component-testing.
---

---
name: component-testing
description: Use this skill to create or modify tests for a component.
----

## Component testing

Use this skill to create or modify component tests for the application.

## Creating stories

- Create a separate story for each state of the component.
- Add tests to verify event handling logic included in the component.
- Stories must be added next to the component.
- If the component file is `button.tsx` then the stories file is `button.stories.tsx`

## Template for a component story

```jsx
import { GitHubSignInButton } from "./github-signin-button"; // The module exporting the component
import { Meta, StoryObj } from "@storybook/nextjs-vite"; // Required framework components

const meta = {
    component: GitHubSignInButton,               // The exported component
    title: "Components/Auth/GitHubSignInButton", // The logical path to the component.
}

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
    args: {},
};
```