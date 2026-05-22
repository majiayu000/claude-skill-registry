---
name: testing-automation-mcp
description: Autonomous E2E testing using Playwright Model Context Protocol (MCP).
category: quality-assurance
version: 4.1.0-fractal
layer: tool-skill
---

# 🧪 Testing Automation MCP

This skill empowers AI Agents to **autonomously write, execute, and debug E2E tests** using the official Playwright MCP Server. It transforms passive testing into an active, agentic workflow.

---

## 🚀 Capabilities

1.  **Browser Control**: Navigate URLs, click elements, fill forms, and handle dialogs via MCP.
2.  **Visual Verification**: Capture screenshots and trace files for debugging.
3.  **Self-Healing**: Analyze failure logs and rewrite selector logic automatically.
4.  **Cross-Browser**: Execute tests on Chromium, Firefox, and WebKit.

---

## 🛠️ MCP Toolset (Playwright)

| Tool | Description | Usage |
| :--- | :--- | :--- |
| `playwright_navigate` | Go to a specific URL. | `{"url": "http://localhost:3000"}` |
| `playwright_click` | Click an element by selector. | `{"selector": "button[type='submit']"}` |
| `playwright_fill` | Fill input fields. | `{"selector": "#email", "value": "test@example.com"}` |
| `playwright_screenshot` | Take a screenshot of the viewport. | `{"path": "debug/error.png"}` |
| `playwright_evaluate` | Run custom JS in the browser. | `{"script": "return document.title"}` |

---

## ♟️ Strategic Patterns

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [1. The "Observer" Pattern (Test Creation)](./sub-skills/1-the-observer-pattern-test-creation.md)
### 2. [2. The "Healer" Pattern (Test Recovery)](./sub-skills/2-the-healer-pattern-test-recovery.md)
### 3. [3. The "Simulator" Pattern (User Journey)](./sub-skills/3-the-simulator-pattern-user-journey.md)
