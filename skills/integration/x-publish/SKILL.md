---
name: x-publish
description: Publish tweets and threads to X (Twitter) draft using browser automation. Use when user wants to publish content to X, save to drafts, or mentions "publish to X", "post tweet", "x-publish", "发布推文". Supports short tweets and threads. NEVER auto-publish, always saves to draft.
---

# X Publish

Publish tweets and threads to X draft using Playwright browser automation.

## Prerequisites

- Playwright MCP for browser automation
- User logged into X (Twitter)
- Python 3.9+ with dependencies:
  - macOS: `pip install Pillow pyobjc-framework-Cocoa`
  - Windows: `pip install Pillow pywin32`

## Critical Rules

1. **NEVER auto-publish** - Only save to draft
2. **User must be logged in** - Prompt to login if not
3. **Verify content before saving** - Double-check tweet text

## Content Types

### Short Tweet
Single tweet ≤280 characters

### Thread
Multiple tweets connected (3-10 tweets)

## Scripts

### copy_to_clipboard.py
Copy text to system clipboard for paste operation:
```bash
# Copy text to clipboard
python scripts/copy_to_clipboard.py text "Tweet content here"

# Copy from file
python scripts/copy_to_clipboard.py text --file /tmp/tweet.txt
```

## Workflow

### Short Tweet

**Step 1: Prepare Content**
```bash
# Save tweet to temp file
echo "Tweet content" > /tmp/tweet.txt

# Copy to clipboard
python scripts/copy_to_clipboard.py text --file /tmp/tweet.txt
```

**Step 2: Open Compose**
```
browser_navigate: https://x.com/compose/post
```

**Step 3: Paste Content**
```
browser_snapshot → Find tweet textbox
browser_click: textbox
browser_press_key: Meta+v
```

**Step 4: Save Draft**
```
browser_click: X (close button)
browser_click: "Save" or "保存" in dialog
```

**Step 5: Verify**
```
Report: "Draft saved. Please review at https://x.com/compose/drafts"
```

### Thread

**Step 1: Prepare Content**
Parse thread into individual tweets:
```
### 1/5
First tweet content...

### 2/5
Second tweet content...
```

**Step 2: Open Compose**
```
browser_navigate: https://x.com/compose/post
```

**Step 3: Add First Tweet**
```bash
python scripts/copy_to_clipboard.py text "First tweet content"
```
```
browser_click: textbox
browser_press_key: Meta+v
```

**Step 4: Add More Tweets**
For each additional tweet:
```
browser_click: "Add another post" / "添加" button
browser_press_key: Meta+v (after copying next tweet)
```

**Step 5: Save Draft**
```
browser_click: X (close button)
browser_click: "Save" in dialog
```

**Step 6: Verify**
```
Report: "Thread draft saved ({n} tweets). Review at https://x.com/compose/drafts"
```

## Efficiency Guidelines

### Avoid Unnecessary Waits
```
❌ browser_snapshot after every action
✅ Use action return values for next step
```

### Parallel Preparation
```
✅ Prepare all tweet content before browser operations
✅ Copy to clipboard while navigating
```

### Sequential Execution
```
Navigate → Paste first tweet → Add tweet → Paste → ... → Save
```

## Element References

Common elements in X compose:

| Element | Description | Typical ref pattern |
|---------|-------------|-------------------|
| Tweet textbox | Main input area | textbox with "What's happening" |
| Add tweet button | "+" or "添加" | button near compose area |
| Close button | X icon | button top-left |
| Save draft | In close dialog | "Save" / "保存" button |
| Drafts link | View saved drafts | link to /compose/drafts |

## Example Flows

### Short Tweet Example

User: `/x-publish "Claude 4.5发布了，extended thinking是真正的游戏规则改变者。"`

```bash
# 1. Copy to clipboard
python scripts/copy_to_clipboard.py text "Claude 4.5发布了，extended thinking是真正的游戏规则改变者。"
```

```
# 2. Navigate and paste
browser_navigate: https://x.com/compose/post
browser_snapshot → find textbox
browser_click: textbox
browser_press_key: Meta+v

# 3. Close and save
browser_click: close button (X)
browser_click: "Save" button

# 4. Report
"Draft saved! Review at: https://x.com/compose/drafts"
```

### Thread Example

User: `/x-publish` (with thread content from x-create)

```
Thread:
### 1/3
First point about AI...

### 2/3
Second point...

### 3/3
Conclusion...
```

Execution:
```bash
# Prepare all tweets
tweet1="First point about AI..."
tweet2="Second point..."
tweet3="Conclusion..."
```

```
# Navigate
browser_navigate: https://x.com/compose/post

# Tweet 1
python copy_to_clipboard.py text "$tweet1"
browser_click: textbox
browser_press_key: Meta+v

# Tweet 2
python copy_to_clipboard.py text "$tweet2"
browser_click: "Add another post" button
browser_press_key: Meta+v

# Tweet 3
python copy_to_clipboard.py text "$tweet3"
browser_click: "Add another post" button
browser_press_key: Meta+v

# Save
browser_click: close button
browser_click: "Save"

# Report
"Thread draft saved (3 tweets). Review at: https://x.com/compose/drafts"
```

## Error Handling

### Not Logged In
```
If login page detected:
→ "Please log in to X first, then run /x-publish again"
```

### Character Limit
```
If tweet > 280 chars:
→ Split into thread or truncate with warning
```

### Network Error
```
If page fails to load:
→ Retry once, then report error
```

## Integration

After publishing:
```
推文已保存到草稿箱！

- 类型: {short/thread}
- 条数: {n}
- 草稿链接: https://x.com/compose/drafts

请手动审核后发布。
```
