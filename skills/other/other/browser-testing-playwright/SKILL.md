---
name: browser-testing-playwright
description: >-
  A skill for setting up and running end-to-end browser tests using Playwright. It includes guidance on project setup, the Page Object Model, user flow testing, visual regression, cross-browser configuration, and CI integration. Use this when a user wants to implement browser-based E2E testing.

---

# End-to-End Browser Testing with Playwright

This skill provides a structured workflow for creating a robust end-to-end testing suite using Playwright.

## Core Workflow

1.  **Setup and Configuration**: Start by setting up the Playwright configuration. See `references/playwright_setup.md` for a detailed guide and a commented `playwright.config.ts`.
2.  **Structure with Page Object Model (POM)**: Organize your test code by creating Page Object classes for each page or component. This pattern makes tests more readable and maintainable. For a detailed explanation and examples, read `references/page_object_model.md`.
3.  **Write User Flow Tests**: With POMs in place, write end-to-end tests that simulate user journeys. A complete example for a `signup -> login -> create task` flow is in `references/user_flow_testing.md`.
4.  **Implement Visual Regression Testing**: Catch unintended visual changes by adding screenshot assertions. Guidance on this is available in `references/visual_regression.md`.
5.  **Configure Cross-Browser Testing**: Ensure your application works across different browsers by configuring projects in Playwright. See `references/cross_browser_testing.md` for how to set up Chromium, Firefox, and WebKit.
6.  **Integrate with CI**: Automate your tests to run on every code change. A sample GitHub Actions workflow and setup instructions are in `references/ci_integration.md`.
7.  **Manage Test Data**: Learn strategies for setting up and tearing down test data to ensure reliable and independent tests. See `references/test_data_management.md`.

## Bundled Resources

This skill includes reference files to guide you through each step. When you need to implement a part of the workflow, read the corresponding reference file.

- `references/playwright_setup.md`
- `references/page_object_model.md`
- `references/user_flow_testing.md`
- `references/visual_regression.md`
- `references/cross_browser_testing.md`
- `references/ci_integration.md`
- `references/test_data_management.md`
