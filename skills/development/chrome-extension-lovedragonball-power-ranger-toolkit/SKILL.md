---
name: chrome-extension
description: Build Chrome Extensions with Manifest V3, background service workers, content scripts, and message passing. Use when developing TikTok Uploader extension or any browser extensions.
---

# 🔌 Chrome Extension Skill

## Use Cases
- TikTok auto-uploader
- Web automation tools
- Content modification
- Data extraction

---

## Manifest V3 Structure

```json
{
  "manifest_version": 3,
  "name": "Extension Name",
  "version": "1.0.0",
  "permissions": ["activeTab", "storage", "tabs"],
  "host_permissions": ["https://*.tiktok.com/*"],
  "background": {
    "service_worker": "background.js"
  },
  "content_scripts": [{
    "matches": ["https://*.tiktok.com/*"],
    "js": ["content.js"]
  }],
  "action": {
    "default_popup": "popup.html"
  },
  "side_panel": {
    "default_path": "sidepanel.html"
  }
}
```

---

## Message Passing

### Content → Background
```javascript
// content.js
chrome.runtime.sendMessage({ type: 'UPLOAD_COMPLETE', data: result });

// background.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'UPLOAD_COMPLETE') {
    console.log('Upload done:', message.data);
    sendResponse({ success: true });
  }
  return true; // Keep channel open for async
});
```

### Background → Content
```javascript
// background.js
chrome.tabs.sendMessage(tabId, { type: 'START_UPLOAD', file: fileData });

// content.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'START_UPLOAD') {
    handleUpload(message.file);
  }
});
```

---

## Storage Patterns

### Local Storage
```javascript
// Save
await chrome.storage.local.set({ uploadQueue: files });

// Load
const { uploadQueue } = await chrome.storage.local.get('uploadQueue');

// Listen for changes
chrome.storage.onChanged.addListener((changes, area) => {
  if (area === 'local' && changes.uploadQueue) {
    console.log('Queue updated:', changes.uploadQueue.newValue);
  }
});
```

---

## Side Panel

### Enable in manifest
```json
"side_panel": {
  "default_path": "sidepanel.html"
}
```

### Open programmatically
```javascript
chrome.sidePanel.open({ windowId: window.id });
```

---

## Trusted Types (CSP Fix)

```javascript
// Create policy
const trustedPolicy = trustedTypes.createPolicy('my-policy', {
  createHTML: (input) => input
});

// Use for innerHTML
element.innerHTML = trustedPolicy.createHTML(htmlString);
```

---

## Service Worker Persistence

```javascript
// Keep alive with alarm
chrome.alarms.create('keepAlive', { periodInMinutes: 1 });

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'keepAlive') {
    // Do minimal work to stay alive
  }
});
```

---

## Decision Tree

```
Extension task?
├── Background work? → Service Worker
├── Page modification? → Content Script
├── User UI? → Popup or Side Panel
├── Cross-script data? → Message passing
└── Persist data? → chrome.storage
```

---

## TikTok Uploader Patterns

### 1. Round-Robin Folders
```javascript
async function getNextFile() {
  const { folders, lastIndex } = await chrome.storage.local.get();
  const nextIndex = (lastIndex + 1) % folders.length;
  const folder = folders[nextIndex];
  
  const files = await fetchFilesFromFolder(folder);
  await chrome.storage.local.set({ lastIndex: nextIndex });
  
  return files[0];
}
```

### 2. Upload Queue Management
```javascript
// Add to queue
await addToQueue(file);

// Process queue
async function processQueue() {
  const { queue } = await chrome.storage.local.get('queue');
  if (queue.length > 0) {
    const file = queue.shift();
    await uploadFile(file);
    await chrome.storage.local.set({ queue });
    processQueue(); // Continue
  }
}
```

---

## Common Issues

| ปัญหา | สาเหตุ | แก้ไข |
|-------|--------|-------|
| Service worker dies | Idle timeout | Use alarms to keep alive |
| CSP error | innerHTML blocked | Use Trusted Types |
| Message not received | Channel closed | Return true in listener |
| Content script not running | Wrong match pattern | Check host_permissions |
