---
name: browser-extension-developer
description: Chrome Manifest v3 extension development for Vigil Guard v2.0.0. Use for plugin development, content scripts, service workers, webhook integration with 3-branch detection, browser fingerprinting, and extension debugging.
version: 2.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Browser Extension Developer (v2.0.0)

## Overview

Chrome Manifest v3 browser extension for Vigil Guard providing client-side prompt injection protection through webhook proxy integration with 3-branch parallel detection architecture and browser fingerprinting.

## When to Use This Skill

- Developing Chrome extension (plugin/)
- Implementing Manifest v3 features
- Working with content scripts and background workers
- Managing webhook integration with 3-branch detection
- Implementing browser fingerprinting
- Debugging extension issues

## Tech Stack

- Manifest v3 (Chrome Extensions API)
- JavaScript ES6+ (no build step)
- Service Worker (background.js)
- Content Scripts (content.js)
- Popup UI (HTML/CSS)

## Project Structure

```
plugin/
├── manifest.json           # Extension manifest (Manifest v3)
├── background.js           # Service Worker (webhook proxy)
├── content.js              # Content script (ChatGPT integration)
├── popup.html             # Extension popup UI
├── popup.js               # Popup logic
├── config.js              # Shared configuration
├── icons/                 # Extension icons
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
└── README.md              # Installation guide
```

## v2.0.0 Response Structure

### Webhook Response Format (3-Branch Detection)

```json
{
  "status": "BLOCKED",
  "arbiter_decision": "BLOCK",
  "threat_score": 85,
  "branch_a_score": 72,
  "branch_b_score": 88,
  "branch_c_score": 91,
  "branch_a_timing_ms": 45,
  "branch_b_timing_ms": 120,
  "branch_c_timing_ms": 250,
  "detected_categories": ["PROMPT_INJECTION", "JAILBREAK"],
  "sanitized_input": null,
  "pii_detected": false,
  "pipeline_version": "2.0.0"
}
```

### Decision Mapping

```javascript
// v2.0.0 arbiter decisions
const DECISION_MAP = {
  'BLOCK': { allow: false, sanitize: false },
  'SANITIZE': { allow: true, sanitize: true },
  'ALLOW': { allow: true, sanitize: false }
};
```

## Manifest v3 Structure

```json
{
  "manifest_version": 3,
  "name": "Vigil Guard Browser Extension",
  "version": "2.0.0",
  "description": "Client-side prompt injection protection with 3-branch detection",

  "permissions": [
    "storage",
    "activeTab"
  ],

  "host_permissions": [
    "https://chat.openai.com/*",
    "http://localhost:5678/*"
  ],

  "background": {
    "service_worker": "background.js",
    "type": "module"
  },

  "content_scripts": [{
    "matches": ["https://chat.openai.com/*"],
    "js": ["content.js"],
    "run_at": "document_idle"
  }],

  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icons/icon16.png",
      "48": "icons/icon48.png",
      "128": "icons/icon128.png"
    }
  }
}
```

## Common Tasks

### Task 1: Content Script (v2.0.0 Integration)

```javascript
// content.js - Updated for v2.0.0 response format
(function() {
  'use strict';

  // Generate unique client ID
  let clientId = localStorage.getItem('vigil_client_id');
  if (!clientId) {
    clientId = 'client_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('vigil_client_id', clientId);
  }

  // Intercept form submission
  function interceptChatSubmit() {
    const form = document.querySelector('form[class*="composer"]');
    if (!form) return;

    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      e.stopPropagation();

      const textarea = form.querySelector('textarea');
      const userInput = textarea.value.trim();

      if (!userInput) return;

      // Get browser metadata
      const browserMetadata = {
        userAgent: navigator.userAgent,
        language: navigator.language,
        platform: navigator.platform,
        screenResolution: `${screen.width}x${screen.height}`,
        timestamp: new Date().toISOString()
      };

      // Send to Vigil Guard via background script
      chrome.runtime.sendMessage({
        type: 'ANALYZE_PROMPT',
        data: {
          chatInput: userInput,
          clientId: clientId,
          browser_metadata: browserMetadata
        }
      }, response => {
        // v2.0.0: Check arbiter_decision instead of status
        const decision = response.arbiter_decision || response.status;

        if (decision === 'ALLOW') {
          form.submit();
        } else if (decision === 'SANITIZE') {
          // Use sanitized input if available
          if (response.sanitized_input) {
            textarea.value = response.sanitized_input;
          }
          form.submit();
        } else if (decision === 'BLOCK') {
          // v2.0.0: Show detailed branch scores
          const branchInfo = response.branch_a_score !== undefined
            ? `\n\nBranch Scores:\n• Heuristics: ${response.branch_a_score}\n• Semantic: ${response.branch_b_score}\n• LLM Guard: ${response.branch_c_score}`
            : '';

          alert(`⚠️ Vigil Guard: Potential prompt injection detected!\n\nThreat Score: ${response.threat_score}\nCategories: ${(response.detected_categories || []).join(', ')}${branchInfo}`);
        }
      });
    }, true);
  }

  // Initialize when DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', interceptChatSubmit);
  } else {
    interceptChatSubmit();
  }
})();
```

### Task 2: Background Service Worker (v2.0.0)

```javascript
// background.js - Updated for v2.0.0
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'ANALYZE_PROMPT') {
    chrome.storage.sync.get(['webhookUrl'], async (items) => {
      const webhookUrl = items.webhookUrl || 'http://localhost:5678/webhook/default';

      try {
        const response = await fetch(webhookUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            ...request.data,
            sessionId: `ext_${Date.now()}`
          })
        });

        const result = await response.json();

        // v2.0.0: Normalize response for backward compatibility
        const normalizedResult = {
          ...result,
          // Map arbiter_decision to status if not present
          status: result.status || result.arbiter_decision,
          // Include branch scores if available
          branch_a_score: result.branch_a_score,
          branch_b_score: result.branch_b_score,
          branch_c_score: result.branch_c_score,
          // Map detected categories
          detected_categories: result.detected_categories || result.detectedCategories || []
        };

        sendResponse(normalizedResult);

      } catch (error) {
        console.error('Vigil Guard error:', error);
        sendResponse({
          status: 'ALLOW',
          arbiter_decision: 'ALLOW',  // v2.0.0 field
          error: error.message
        });
      }
    });

    return true;
  }
});
```

### Task 3: Popup Configuration UI (v2.0.0)

```html
<!-- popup.html - Updated for v2.0.0 -->
<!DOCTYPE html>
<html>
<head>
  <title>Vigil Guard v2.0.0 Settings</title>
  <style>
    body { width: 320px; padding: 12px; font-family: Arial, sans-serif; }
    h3 { margin: 0 0 10px 0; }
    input { width: 100%; padding: 8px; margin: 5px 0; box-sizing: border-box; }
    button { width: 100%; padding: 10px; margin: 5px 0; cursor: pointer; }
    .primary { background: #4CAF50; color: white; border: none; }
    .secondary { background: #2196F3; color: white; border: none; }
    .status { margin-top: 10px; padding: 8px; border-radius: 4px; font-size: 12px; }
    .success { background: #d4edda; color: #155724; }
    .error { background: #f8d7da; color: #721c24; }
    .info { background: #cce5ff; color: #004085; }
    .branch-status { font-size: 11px; margin-top: 8px; }
    .branch-status div { margin: 2px 0; }
    .healthy { color: #155724; }
    .unhealthy { color: #721c24; }
  </style>
</head>
<body>
  <h3>Vigil Guard v2.0.0</h3>

  <label>Webhook URL:</label>
  <input type="text" id="webhookUrl" placeholder="http://localhost:5678/webhook/xxx">

  <button id="save" class="primary">Save Configuration</button>
  <button id="test" class="secondary">Test Connection</button>
  <button id="healthCheck" class="secondary">Check Branch Health</button>

  <div id="status"></div>
  <div id="branchStatus" class="branch-status"></div>

  <script src="popup.js"></script>
</body>
</html>
```

```javascript
// popup.js - Updated for v2.0.0
document.getElementById('save').addEventListener('click', () => {
  const webhookUrl = document.getElementById('webhookUrl').value;
  chrome.storage.sync.set({ webhookUrl }, () => {
    showStatus('Configuration saved!', 'success');
  });
});

document.getElementById('test').addEventListener('click', async () => {
  const webhookUrl = document.getElementById('webhookUrl').value;

  try {
    const response = await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chatInput: 'test connection',
        sessionId: 'extension_test'
      })
    });

    if (response.ok) {
      const result = await response.json();
      // v2.0.0: Check for arbiter_decision
      if (result.arbiter_decision) {
        showStatus(`✅ Connected (v2.0.0) - Arbiter: ${result.arbiter_decision}`, 'success');
      } else {
        showStatus('✅ Connected (legacy mode)', 'success');
      }
    } else {
      showStatus(`❌ Error: ${response.status}`, 'error');
    }
  } catch (error) {
    showStatus(`❌ Connection failed: ${error.message}`, 'error');
  }
});

// v2.0.0: Branch health check
document.getElementById('healthCheck').addEventListener('click', async () => {
  const webhookUrl = document.getElementById('webhookUrl').value;
  const baseUrl = new URL(webhookUrl).origin;

  try {
    // Note: This requires backend proxy endpoint
    const response = await fetch(`${baseUrl}/api/health/branches`);

    if (response.ok) {
      const branches = await response.json();
      showBranchStatus(branches);
    } else {
      showStatus('❌ Health check unavailable', 'error');
    }
  } catch (error) {
    showStatus('❌ Cannot reach health endpoint', 'error');
  }
});

function showStatus(message, type) {
  const status = document.getElementById('status');
  status.textContent = message;
  status.className = `status ${type}`;
}

function showBranchStatus(branches) {
  const container = document.getElementById('branchStatus');
  container.innerHTML = `
    <div class="${branches.branch_a?.healthy ? 'healthy' : 'unhealthy'}">
      Branch A (Heuristics): ${branches.branch_a?.healthy ? '✅' : '❌'}
    </div>
    <div class="${branches.branch_b?.healthy ? 'healthy' : 'unhealthy'}">
      Branch B (Semantic): ${branches.branch_b?.healthy ? '✅' : '❌'}
    </div>
    <div class="${branches.branch_c?.healthy ? 'healthy' : 'unhealthy'}">
      Branch C (LLM Guard): ${branches.branch_c?.healthy ? '✅' : '❌'}
    </div>
  `;
  showStatus('Branch status updated', 'info');
}

// Load saved configuration
chrome.storage.sync.get(['webhookUrl'], (items) => {
  if (items.webhookUrl) {
    document.getElementById('webhookUrl').value = items.webhookUrl;
  }
});
```

### Task 4: Browser Fingerprinting

```javascript
// config.js
function getBrowserFingerprint() {
  return {
    userAgent: navigator.userAgent,
    language: navigator.language,
    languages: navigator.languages.join(','),
    platform: navigator.platform,
    hardwareConcurrency: navigator.hardwareConcurrency,
    deviceMemory: navigator.deviceMemory,
    screenResolution: `${screen.width}x${screen.height}`,
    colorDepth: screen.colorDepth,
    pixelRatio: window.devicePixelRatio,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    plugins: Array.from(navigator.plugins).map(p => p.name).join(','),
    touchSupport: 'ontouchstart' in window,
    webGL: getWebGLInfo(),
    canvas: getCanvasFingerprint()
  };
}

function getWebGLInfo() {
  const canvas = document.createElement('canvas');
  const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
  if (!gl) return 'not supported';

  const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
  return debugInfo ? {
    vendor: gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL),
    renderer: gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL)
  } : 'no debug info';
}

function getCanvasFingerprint() {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  ctx.textBaseline = 'top';
  ctx.font = '14px Arial';
  ctx.fillText('Vigil Guard Fingerprint', 2, 2);
  return canvas.toDataURL().substring(0, 50);
}
```

## Integration Points

### With n8n-vigil-workflow (v2.0.0):
```yaml
when: Extension sends request
action:
  1. Workflow receives browser_metadata + clientId
  2. 3-branch parallel detection executes
  3. Arbiter v2 makes decision
  4. Response includes branch scores
  5. Log to ClickHouse with branch columns
```

### With clickhouse-grafana-monitoring (v2.0.0):
```sql
-- Query extension usage with branch data
SELECT
  client_id,
  count() as requests,
  avg(branch_a_score) as avg_heuristics,
  avg(branch_b_score) as avg_semantic,
  avg(branch_c_score) as avg_llm_guard,
  countIf(arbiter_decision = 'BLOCK') as blocked
FROM n8n_logs.events_processed
WHERE client_id LIKE 'client_%'
GROUP BY client_id
ORDER BY requests DESC
```

## Testing & Development

### Local Testing
```bash
# 1. Load extension in Chrome
chrome://extensions/ → Enable Developer Mode → Load unpacked → Select plugin/

# 2. Test on ChatGPT
open https://chat.openai.com/

# 3. Check console for v2.0.0 response
F12 → Console → Look for "Vigil Guard" messages with branch scores

# 4. Verify webhook (check for arbiter_decision)
docker logs vigil-n8n | grep "arbiter_decision"
```

### Debugging
```javascript
// background.js - Add v2.0.0 logging
console.log('[Vigil Guard v2.0.0] Analyzing prompt:', request.data);
console.log('[Vigil Guard v2.0.0] Response:', {
  arbiter_decision: response.arbiter_decision,
  branch_a: response.branch_a_score,
  branch_b: response.branch_b_score,
  branch_c: response.branch_c_score
});
```

## Troubleshooting

**v2.0.0 response not recognized:**
```javascript
// Check for both old and new response formats
const decision = response.arbiter_decision || response.status;
const categories = response.detected_categories || response.detectedCategories || [];
```

**Branch scores undefined:**
```javascript
// Branch C may timeout - handle gracefully
const branchInfo = response.branch_a_score !== undefined
  ? `Scores: A=${response.branch_a_score}, B=${response.branch_b_score}, C=${response.branch_c_score || 'N/A'}`
  : 'Branch scores unavailable';
```

## Quick Reference

```bash
# Package extension
cd plugin && zip -r vigil-guard-extension-v2.0.0.zip *

# Install in Chrome
chrome://extensions/ → Load unpacked → Select plugin/

# View console
F12 → Console

# Check v2.0.0 backend
curl http://localhost:5678/webhook/default \
  -H "Content-Type: application/json" \
  -d '{"chatInput":"test","sessionId":"ext_test"}' | jq '.arbiter_decision'
```

---

**Current Version:** v2.0.0
**Manifest:** v3
**Supported Sites:** ChatGPT (chat.openai.com)
**Backend:** 3-Branch Parallel Detection (24 nodes)
**Response Format:** arbiter_decision + branch scores
