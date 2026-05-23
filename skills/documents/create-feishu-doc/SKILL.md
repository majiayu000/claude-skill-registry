---
name: create-feishu-doc
description: This skill should be used when the user asks to "create a Feishu doc", "create a new doc in Feishu", "open Feishu and create document", "create document in leiniao-ibg", or mentions creating documents in Feishu/Lark workspace.
user-invocable: true
version: 0.1.0
---

# Create Feishu Document Automation

## Purpose

Automate the process of creating new documents in Feishu (Lark) workspace by using browser automation to navigate the UI, authenticate, and create documents with specified titles and content.

## When to Use This Skill

Use this skill when:
- User asks to create a new document in Feishu
- User wants to automate document creation in their Feishu workspace
- User needs to quickly create documents without manual UI interaction

## Prerequisites

- Access to Feishu workspace (https://leiniao-ibg.feishu.cn)
- Valid authentication credentials for the workspace
- Browser automation capability via `agent-browser`

## Workflow

### Step 1: Load Browser Automation Skill

Load the `office:agent-browser` skill using the Skill tool to access browser automation commands.

### Step 2: Navigate to Feishu Drive

Open the Feishu Drive homepage:

```bash
agent-browser open https://leiniao-ibg.feishu.cn/drive/home/
```

Wait for page to load:

```bash
agent-browser wait --load networkidle
```

### Step 3: Verify Authentication

Take a snapshot to check if already logged in:

```bash
agent-browser snapshot -i
```

If login is required, wait for user to complete authentication manually or handle authentication flow based on the page state.

### Step 4: Create New Document

Click the "新建" (New) button (use snapshot to locate the element ref):

```bash
agent-browser snapshot -i
# Locate "新建" button ref (e.g., @e1)
agent-browser click @e1
```

Wait for dropdown menu to appear:

```bash
agent-browser wait 1000
```

Take another snapshot to locate the "文档" (Doc) option:

```bash
agent-browser snapshot -i
# Locate "文档" button ref (e.g., @e2)
agent-browser click @e2
```

### Step 5: Select New Document Type

Click the "新建空白文档" (New Doc) option from the submenu:

```bash
agent-browser wait 1000
agent-browser snapshot -i
# Locate "新建空白文档" button ref (e.g., @e3)
agent-browser click @e3
```

### Step 6: Wait for New Tab

Wait for the new document to open in a new tab:

```bash
agent-browser wait --load networkidle
```

Check tabs to ensure new document page opened:

```bash
agent-browser tab
```

If multiple tabs exist, switch to the newest tab (usually the last one):

```bash
agent-browser tab 2  # Adjust index based on tab list
```

### Step 7: Enter Document Title

The page should automatically focus on the title input field. If the title field is focused by default, type the title directly:

```bash
agent-browser type @e1 "Document Title Here"
```

If not automatically focused, take a snapshot to locate the title input:

```bash
agent-browser snapshot -i
# Locate title input ref (e.g., @e1)
agent-browser fill @e1 "Document Title Here"
```

### Step 8: Enter Document Content

Press Tab or click to move to the content area:

```bash
agent-browser press Tab
```

Or locate and click the content editor:

```bash
agent-browser snapshot -i
# Locate content editor ref (e.g., @e2)
agent-browser click @e2
```

Type the document content:

```bash
agent-browser type @e2 "Document content goes here..."
```

For multi-line content, use newlines in the input:

```bash
agent-browser type @e2 "First paragraph

Second paragraph

Third paragraph"
```

### Step 9: Verify and Save

Take a final screenshot to verify the document was created successfully:

```bash
agent-browser screenshot
```

Feishu documents auto-save, so no explicit save action is required. The document is now ready to use.

### Step 10: Close Browser (Optional)

Close the browser session when done:

```bash
agent-browser close
```

## Error Handling

### Authentication Issues

If authentication fails or login is required:
1. Pause the workflow
2. Inform the user that manual login is needed
3. Wait for confirmation before proceeding
4. Resume workflow after authentication

### Element Not Found

If snapshot cannot locate expected UI elements (button refs):
1. Take a full snapshot without `-i` flag for debugging
2. Check if UI has changed or language settings differ
3. Use semantic locators as fallback:
   ```bash
   agent-browser find text "新建" click  # Find "新建" (New) button
   agent-browser find text "文档" click  # Find "文档" (Doc) button
   agent-browser find text "新建空白文档" click  # Find "新建空白文档" (New Doc) button
   ```

### Timeout Issues

If page loading takes too long:
1. Increase wait timeout: `agent-browser wait --load networkidle --timeout 10000`
2. Check network connectivity
3. Verify Feishu service availability

## Customization

### Different Workspace

To use with a different Feishu workspace, replace the URL in Step 2:

```bash
agent-browser open https://your-workspace.feishu.cn/drive/home/
```

### Document Templates

To use a specific document template instead of blank document:
1. Navigate to template gallery after clicking "Doc"
2. Locate and click the desired template
3. Proceed with title and content entry

## Best Practices

1. **Session Reuse**: For multiple document creations, keep the browser session open and reuse authentication state
2. **Error Screenshots**: Take screenshots at each critical step for debugging
3. **Wait for UI**: Always wait for network idle after navigation to ensure UI elements are loaded
4. **Explicit Waits**: Use explicit waits (e.g., `agent-browser wait 1000`) after clicking dropdown menus

## Additional Resources

### Browser Automation Reference

For detailed browser automation commands and patterns:
- Load `office:agent-browser` skill for complete command reference
- See snapshot and interaction patterns in agent-browser documentation

### Example Usage

```bash
# Complete workflow example
agent-browser open https://leiniao-ibg.feishu.cn/drive/home/
agent-browser wait --load networkidle
agent-browser snapshot -i
agent-browser click @e1  # 新建 button
agent-browser wait 1000
agent-browser snapshot -i
agent-browser click @e2  # 文档 button
agent-browser wait 1000
agent-browser snapshot -i
agent-browser click @e3  # 新建空白文档 button
agent-browser wait --load networkidle
agent-browser tab
agent-browser tab 2  # Switch to new tab
agent-browser type @e1 "My Document Title"
agent-browser press Tab
agent-browser type @e2 "My document content..."
agent-browser screenshot
```
