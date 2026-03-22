---
name: chat-deepseek
alias:
  - deepseek
  - deepseek-it
  - ask-deepseek
  - open-deepseek
  - browse-deepseek
  - deepseek-search
  - deepseeking

description: openclaw browser open https://chat.deepseek.com and login it, then input questions from user's messages, extract response of deepseek chat to reply user.
allowed-tools: Bash(npm:*) Bash(npx:*) Bash(openclaw:*) Bash(curl:*) Read Write WebFetch
---

# DeepSeek Chat Automation Skill

Automate login with scanning qr code snapshot, input questions got from user messages, and extract responses from DeepSeek chat, and then reply to user.

**Key Feature:** Pure browser automation + DOM extraction. **No LLM requests or processing** - just raw text from the rendered page.

## When to Use

✅ **USE this skill when:**
- ask somthing to DeepSeek
- Sending messages to DeepSeek chat
- Extracting AI responses as raw text (no LLM processing)
- Browser automation workflows
- Batch processing chat queries with direct output

❌ **DON'T use this skill when:**
- Need real-time SSE stream capture (use curl/WebSocket directly)
- Page uses heavy anti-bot protection
- Requires complex CAPTCHA solving
- Need LLM-powered text processing (use Claude API directly)

## Requirements

- check browser extention with `openclaw browser status`, and get `enabled: true`
- Browser tool with `profile: "openclaw"`
- **No API keys or LLM credits needed**

## Workflow Overview (5 Steps)

```
┌─────────────────────────────────────────────────────────────────┐
│  1. Open chat.deepseek.com OR check existing tab                │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. Check login status - QR Code needed?                         │
│     - If login form → Manual QR Code scan required               │
│     - If chat interface → Already logged in                      │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. Input text in textarea/box                                   │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. Keep focus on input, press Enter key                         │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. Extract response from DOM (page body)                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Open or Reuse Tab

```javascript
// Try to find existing DeepSeek tab first
const existingTabs = await sessions_list({ /* filter for chat.deepseek.com */ });

if (existingTabs.length > 0) {
  console.log("✅ Reusing existing DeepSeek tab:", existingTabs[0]);
  tabId = existingTabs[0];
} else {
  // Open new tab
  const result = await browser({
    action: "open",
    profile: "openclaw",
    targetUrl: "https://chat.deepseek.com/"
  });
  tabId = result.targetId;
  console.log("✅ Opened new DeepSeek tab:", tabId);
}

// Wait for page to load
await new Promise(r => setTimeout(r, 2000));
```

---

## Step 2: Check Login Status (QR Code Needed?)

```javascript
// Check if login required (QR Code scan) or already logged in
await browser({
  action: "act",
  kind: "evaluate",
  profile: "openclaw",
  targetId: tabId,
  fn: `{ 
    // Check for login form (QR Code or phone input)
    const loginForm = document.querySelector('input[type="tel"], input[placeholder*="Phone"]');
    const qrCode = document.querySelector('iframe[src*="wechat"], img[alt*="WeChat"]');
    const chatInput = document.querySelector('textarea[placeholder*="Message DeepSeek"]');
    const userAvatar = document.querySelector('[class*="avatar"], [class*="user"]');
    
    JSON.stringify({ 
      needLogin: !!(loginForm || qrCode),
      hasChatInput: !!chatInput,
      hasUser: !!userAvatar,
      hasLoginForm: !!loginForm,
      hasQrCode: !!qrCode
    });
  }`,
  returnByValue: true
});
```

### Login Status Indicators

| Status | Check | Action Required |
|--------|-------|-----------------|
| ✅ Already Logged In | Chat input visible + user avatar | Proceed to Step 3 |
| ❌ Need Login | QR Code or login form visible | **Manual QR Code scan required** |

### QR Code Login Flow

```javascript
// If QR Code is needed, notify user to scan
const status = JSON.parse(result);

if (status.needLogin) {
  console.log("⚠️ QR Code login required!");
  
  // For QR Code login:
  // 1. Navigate to login page if not already there
  // 2. Take screenshot of QR Code
  // 3. Send to user via imsg and other enabled and running channels
  // 4. User scans with WeChat
  // 5. After scan, chat interface should appear
  
  await browser({
    action: "navigate",
    profile: "openclaw",
    targetId: tabId,
    targetUrl: "https://chat.deepseek.com/sign_in"
  });
  
  // Take screenshot of QR Code
  await browser({
    action: "screenshot",
    profile: "openclaw",
    targetId: tabId
  });
  
  // Send QR Code to user's running channel for scanning
  // Channel example #1: imessage (<account_id> got fron imessage channel)
  await exec({
    command: 'imsg send --to "<account_id>" --text "DeepSeek QR Code Login - Please scan with WeChat" --file "/path/to/screenshot.jpg"'
  });
  // Channel example #2: whatsapp (<account_id> got fron whatsapp channel)
  await exec({
    command: 'openclaw message send --channel whatsapp --target <account_id> -m "DeepSeek QR Code Login - Please scan with WeChat" --media "<your-workspace>/snapshot/screenshot.jpg"'
  });
  // Channel example #3: signal (<account_id> got fron signal channel)
  await exec({
    command: 'openclaw message send --channel signal --target <account_id> -m "DeepSeek QR Code Login - Please scan with WeChat" --file "/path/to/screenshot.jpg"'
  });
  
  console.log("📱 QR Code sent. Waiting for scan...");
  
  // Poll for login success (every 5 seconds, max 60 attempts)
  let attempts = 0;
  while (attempts < 60) {
    await new Promise(r => setTimeout(r, 5000));
    const loginCheck = await browser({
      action: "act",
      kind: "evaluate",
      profile: "openclaw",
      targetId: tabId,
      fn: `{
        const chatInput = document.querySelector('textarea[placeholder*="Message DeepSeek"]');
        !!chatInput;
      }`,
      returnByValue: true
    });
    
    if (loginCheck === 'true') {
      console.log("✅ QR Code scan successful!");
      break;
    }
    attempts++;
  }
}
```

---

## Step 3: Input Text in Textarea

```javascript
// Ensure we're on chat page
await browser({
  action: "navigate",
  profile: "openclaw",
  targetId: tabId,
  targetUrl: "https://chat.deepseek.com/"
});

// Take snapshot to a snapshot dir in workspace (if none, makedir it), and get fresh refs
await browser({
  action: "snapshot",
  profile: "openclaw",
  out: "<your-workspace>/snapshot/snapshot.jpg"
  targetId: tabId
});

// Type message into input box
await browser({
  action: "act",
  kind: "type",
  profile: "openclaw",
  targetId: tabId,
  ref: "e94", // Get from snapshot - textarea ref
  text: "Your message here"
});

console.log("✅ Text typed into input box");
```

---

## Step 4: Keep Focus, Press Enter Key

```javascript
// Ensure input stays focused and dispatch Enter key events
await browser({
  action: "act",
  kind: "evaluate",
  profile: "openclaw",
  targetId: tabId,
  fn: `{
    // Get the textarea element
    const input = document.querySelector('textarea[placeholder*="Message DeepSeek"]');
    
    if (input) {
      // Ensure input is focused
      input.focus();
      input.scrollIntoView({ behavior: 'smooth', block: 'center' });
      
      // Dispatch Enter key events directly on the input element
      // Use createEvent for better browser compatibility
      const enterEvent = new KeyboardEvent('keydown', {
        key: 'Enter',
        code: 'Enter',
        keyCode: 13,
        which: 13,
        bubbles: true,
        cancelable: true
      });
      input.dispatchEvent(enterEvent);
      
      // Also dispatch keypress and keyup for completeness
      const keypressEvent = new KeyboardEvent('keypress', {
        key: 'Enter',
        code: 'Enter',
        keyCode: 13,
        bubbles: true
      });
      input.dispatchEvent(keypressEvent);
      
      const keyupEvent = new KeyboardEvent('keyup', {
        key: 'Enter',
        code: 'Enter',
        keyCode: 13,
        bubbles: true
      });
      input.dispatchEvent(keyupEvent);
      
      'Enter key dispatched on focused input';
    } else {
      'Input element not found';
    }
  }`,
  returnByValue: true
});

// Wait for response (5-10 seconds for complex queries)
await new Promise(r => setTimeout(r, 8000));

console.log("✅ Enter key pressed, waiting for response...");
```

---

## Step 5: Extract Response from DOM (Page Body)

```javascript
// Extract assistant response from page body
// Returns raw text, no LLM processing
await browser({
  action: "act",
  kind: "evaluate",
  profile: "openclaw",
  targetId: tabId,
  fn: `{
    // Get all paragraph elements from the entire page body
    const body = document.body;
    const paras = Array.from(body.querySelectorAll('p'));
    
    // Filter to find assistant messages (not user messages, not system text)
    const assistantMsgs = paras.filter(p => {
      const text = p.innerText || '';
      const parent = p.parentElement;
      
      // Exclude system messages and user messages
      return text.length > 15 && 
             !text.includes('AI-generated') &&
             !text.includes('Upload docs') &&
             !text.includes('How can I help') &&
             !text.includes('⌘') &&
             parent && !parent.closest('header') &&
             parent && !parent.closest('footer');
    });
    
    // Get the most recent assistant message
    const lastResponse = assistantMsgs.length > 0 
      ? assistantMsgs[assistantMsgs.length - 1].innerText 
      : 'No response found';
    
    // Clean up the response
    lastResponse.trim();
  }`,
  returnByValue: true
});

// Result: Raw text response from DeepSeek
```

### Response Extraction Strategy

| Element | Strategy |
|---------|----------|
| Container | `document.body` |
| Message type | `<p>` tags |
| Filter out | AI-generated, Upload docs, Help text, Keyboard shortcuts |
| Get | Last matching `<p>` from body |

---

## Example: Complete Workflow

```javascript
// ============ DEEPSEEK CHAT AUTOMATION ============

const profile = "openclaw";

// Step 1: Open or reuse tab
let tabId;
const tabsResult = await sessions_list({ /* filter */ });
if (tabsResult.length > 0) {
  tabId = tabsResult[0];
  console.log("Reusing existing tab:", tabId);
} else {
  const openResult = await browser({
    action: "open",
    profile: profile,
    targetUrl: "https://chat.deepseek.com/"
  });
  tabId = openResult.targetId;
}

// Step 2: Check login status
const loginCheck = await browser({
  action: "act",
  kind: "evaluate",
  profile: profile,
  targetId: tabId,
  fn: `{
    const loginForm = document.querySelector('input[type="tel"]');
    const chatInput = document.querySelector('textarea');
    const avatar = document.querySelector('[class*="avatar"]');
    { needLogin: !loginForm && !chatInput, hasChat: !!chatInput, hasUser: !!avatar };
  }`,
  returnByValue: true
});

// Step 3: Type message
await browser({
  action: "act",
  kind: "type",
  profile: profile,
  targetId: tabId,
  ref: "e94",
  text: "Tell me about Landon Railway history"
});

// Step 4: Press Enter
await browser({
  action: "act",
  kind: "evaluate",
  profile: profile,
  targetId: tabId,
  fn: `{
    const input = document.querySelector('textarea');
    input.focus();
    ['keydown', 'keypress', 'keyup'].forEach(type => {
      input.dispatchEvent(new KeyboardEvent(type, { key: 'Enter', bubbles: true, cancelable: true }));
    });
    'Enter sent';
  }`,
  returnByValue: true
});

await new Promise(r => setTimeout(r, 8000));

// Step 5: Extract response
const response = await browser({
  action: "act",
  kind: "evaluate",
  profile: profile,
  targetId: tabId,
  fn: `{
    const msgs = Array.from(document.body.querySelectorAll('p'))
      .filter(p => p.innerText.length > 15 && !p.innerText.includes('AI-generated'));
    msgs[msgs.length - 1]?.innerText || 'No response';
  }`,
  returnByValue: true
});

console.log("DeepSeek Response:", response);
// Send response to iMessage or other enabled and running channel
```

---

## Common Selectors

| Element | Selector |
|---------|----------|
| Chat input | `textarea[placeholder*="Message DeepSeek"]` |
| Send (Enter) | `input.dispatchEvent(KeyboardEvent('Enter'))` |
| QR Code | `iframe[src*="wechat"], img[alt*="WeChat"]` |
| Login form | `input[type="tel"], input[placeholder*="Phone"]` |
| User avatar | `[class*="avatar"], [class*="user"]` |
| Response content | Last `<p>` in `document.body` (filtered) |

---

## Limitations

- **Rate Limiting**: DeepSeek may block requests (429 errors)
- **Event Validation**: Some buttons need real user events
- **Login Verification**: QR Code scan requires user interaction
- **No API Access**: Direct API requires bypassing WAF
- **No Files Uploading**: DO NOT upload files to chat.deepseek.com, DO NOT click file button.
- **No LLM Processing**: Extract raw text only

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Input not found | Refresh page, take new snapshot |
| Enter not working | DeepSeek uses custom event handlers |
| File uploading pending | Cancel file uploading dialog |
| Response not found | Wait longer, check page rendering |
| QR Code timeout | User needs to scan with WeChat |
| Cookies expired | Manual re-login required |

---

## See Also

- `imsg` skill - Send results to iMessage
- `openclaw channels status` skill - Get enabled and running channels
- `openclaw message send --help` skill - Send results to enabled and running channels
- `openclaw browser status` skill - Get browser status `enabled: true`
- `browser` tool - OpenClaw browser control
- `curl` - Direct API access (if WAF bypass possible)
