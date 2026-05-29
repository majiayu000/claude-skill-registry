---
name: managing-complex-forms
description: Best practices for handling long forms using React Hook Form and Zod. Use for booking, profile updates, or tour creation.
---

# Complex Form Management

## When to use this skill
- Multi-step booking forms.
- User profile editing.
- Admin tour creation dashboard.

## Tools
- **React Hook Form**: For state and performance.
- **Zod**: For schema validation.
- **Shadcn Form**: For UI integration.

## Workflow
- [ ] Define Zod schema.
- [ ] Initialize `useForm` with resolver.
- [ ] Wrap components in `<Form>`.
- [ ] Handle submission with Loading state.

## Instructions
- **Inline Validation**: Show errors immediately on blur or change.
- **UX**: Use stepper for very long forms.
