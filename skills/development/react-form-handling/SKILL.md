---
name: react-form-handling
description: Provides robust patterns and reusable components for handling forms in React. Use this skill when building forms that require validation, error handling, multi-step flows, file uploads, or complex submission logic. It covers libraries like React Hook Form, Zod, and Yup, offering templates and best practices for creating performant and user-friendly forms.
---

# React Form Handling

This skill provides a comprehensive guide and reusable assets for building robust and user-friendly forms in React.

## Overview

Handling forms in React can be complex. This skill simplifies the process by providing battle-tested patterns and reusable components for common form-related tasks. It focuses on using `react-hook-form` for performance and developer experience, paired with schema validation libraries like `zod` or `yup`.

## Core Concepts

The core workflow for building a form with this skill is:

1.  **Define a validation schema**: Use Zod (recommended) or Yup to define the shape and validation rules for your form data.
2.  **Set up `react-hook-form`**: Initialize the form hook with your schema.
3.  **Build the UI**: Use the provided reusable form components (`TextInput`, `Select`, etc.) which are pre-wired to work with `react-hook-form`.
4.  **Handle submission**: Implement the `onSubmit` handler to process valid form data.

## Getting Started: Choosing a Validation Library

This skill supports multiple validation libraries. Here's a quick guide to help you choose:

-   **Zod (Recommended)**: Offers excellent type-safety and a modern API. It's a great choice for TypeScript projects. See `references/zod.md` for examples.
-   **Yup**: A mature and popular library. It's a solid choice if you're already familiar with it or working in a project that uses it. See `references/yup.md` for examples.
-   **React Hook Form (Built-in)**: For simple forms without complex validation, you can use the built-in validation. However, for most applications, a schema-based library is recommended for better maintainability.

## Key Patterns and Guides

This skill provides detailed guides on various form handling patterns in the `references/` directory.

-   **React Hook Form Setup**: For a complete setup template and best practices, see `references/react-hook-form.md`.
-   **Validation**: For advanced validation techniques like async validation (e.g., checking for username uniqueness), see `references/validation-patterns.md`.
-   **Error Handling**: For strategies on displaying clear and helpful error messages, see `references/error-handling.md`.
-   **Advanced Forms**: For complex scenarios like multi-step wizards or forms with file uploads, see `references/advanced-patterns.md`.

## Reusable Components

This skill includes a set of reusable, unstyled form components in `assets/components/`. These components are designed to be easily integrated into any React project and are pre-configured to work with `react-hook-form`.

-   `assets/components/TextInput.tsx`
-   `assets/components/Select.tsx`
-   `assets/components/Checkbox.tsx`
-   `assets/components/FileUpload.tsx`

To use them, copy them into your project's component directory.

## Templates

A complete project template for a basic React Hook Form setup can be found in `assets/templates/react-hook-form-setup/`. You can use this to quickly bootstrap a new form.
