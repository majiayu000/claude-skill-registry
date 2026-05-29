---
name: activate-lightning-page
description: Activates a newly deployed Lightning App Page so it appears in the App Launcher. Use when you've deployed a new flexipage and need to make it accessible to users.
allowed-tools: Bash, Read, mcp__python-kernel__execute_python
---

# Activate Lightning App Page

Activates a newly deployed Lightning App Page via browser automation so it appears in the App Launcher.

## Prerequisites

- Browser session already established via Playwright (see CLAUDE.md)
- Page already deployed to org
- User logged into Salesforce

## Steps

### 1. Navigate to Lightning App Builder

```python
await page.goto("https://chbd12461--partial.sandbox.lightning.force.com/lightning/setup/FlexiPageList/home")
await asyncio.sleep(3)
```

### 2. Access iframe content

Setup pages render in an iframe:

```python
iframe = await page.query_selector("iframe")
frame = await iframe.content_frame()
```

### 3. Find and click on the page

Replace `$ARGUMENTS` with the page name:

```python
page_link = await frame.query_selector("a:has-text('$ARGUMENTS')")
await page_link.click()
await asyncio.sleep(3)
```

### 4. Click Edit button

Note the spaces in the value attribute:

```python
edit_btn = await frame.query_selector("input[value=' Edit ']")
await edit_btn.click()
await asyncio.sleep(5)
```

### 5. Click Activation

Now in main page context, not iframe:

```python
activation_btn = await page.wait_for_selector("button:has-text('Activation')")
await activation_btn.click()
await asyncio.sleep(3)
```

### 6. Save activation

Use the last Save button (the one in the dialog):

```python
save_buttons = await page.query_selector_all("button:has-text('Save')")
await save_buttons[-1].click()
await asyncio.sleep(3)
```

### 7. Skip navigation menu prompt

```python
skip_btn = await page.wait_for_selector("button:has-text('Skip and Save')")
await skip_btn.click()
await asyncio.sleep(2)
```

### 8. Verify

Take screenshot or look for "Activation successful" message:

```python
await page.screenshot(path="/tmp/activation_result.png")
```

## Result

- Page is now searchable in App Launcher
- Direct URL: `/lightning/n/Page_Name`
