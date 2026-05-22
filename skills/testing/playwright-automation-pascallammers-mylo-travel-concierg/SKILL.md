---
name: playwright-automation
description: Automate browser testing, web scraping, and user workflow testing with Playwright across multiple browsers. Use when writing end-to-end tests for web applications, automating repetitive browser tasks, scraping data from websites, testing across Chrome/Firefox/Safari, taking screenshots for visual regression testing, testing authentication flows, filling and submitting forms programmatically, testing responsive designs across viewports, or any browser automation requiring reliable, cross-browser testing capabilities.
---

# Playwright Automation - Browser Testing

## When to use this skill

- Writing end-to-end tests for web applications
- Automating repetitive browser tasks and workflows
- Scraping data from websites programmatically
- Testing across Chrome, Firefox, Safari, and Edge browsers
- Taking screenshots for visual regression testing
- Testing authentication and login flows
- Filling and submitting forms automatically
- Testing responsive designs across different viewports
- Simulating user interactions (clicks, typing, navigation)
- Testing file uploads and downloads
- Capturing network requests and responses
- Testing Single Page Applications (SPAs)
- Any browser automation requiring reliable cross-browser support

## When to use this skill

- E2E testing, browser automation, web scraping.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: E2E testing, browser automation, web scraping.

## Basic Test
\`\`\`typescript
import { test, expect } from '@playwright/test';

test('homepage', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading')).toBeVisible();
});
\`\`\`

## Resources
- [Playwright](https://playwright.dev/)
