---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
license: Complete terms in LICENSE.txt
---

# WebApp Testing Guide

## Overview
This skill provides a comprehensive toolkit for testing and debugging web applications using Playwright.

## Core Operations

### Start a Dev Server
Before testing, ensure your web app is running.
```bash
npm run dev
```

### Run Playwright Tests
Execute automated tests to verify functionality.
```bash
npx playwright test
```

### Debugging with Browser
Use the browser tool to interact with the app manually and inspect state.

## Best Practices
- Use unique IDs for interactive elements to simplify selection.
- Clear browser logs and screenshots before each test run for clean results.
- Record videos of failed tests for easier debugging.
