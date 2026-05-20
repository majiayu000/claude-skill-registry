---
name: browser-operator
description: Visual web automation and data extraction using Playwright. Allows Epsilon Prime to navigate websites, interact with UI elements, and extract structured data from gated or complex web pages.
version: 1.0.0
tier: 4
metadata:
  author: Epsilon Prime
  capability: Web Automation / Scraper
---

# 🌐 Browser Operator
**Mission:** To provide Epsilon Prime with "eyes" and "hands" on the live web. This skill enables the navigation of complex, JavaScript-heavy, or gated websites that standard HTTP scrapers cannot handle.

## 🛠️ Operational Mandates
1.  **Stealth Mode:** Mimic human interaction patterns to avoid being blocked by anti-bot measures.
2.  **Structured Output:** Always convert extracted web data into clean Markdown or JSON for RAG ingestion.
3.  **Efficiency:** Close browser contexts immediately after the task is complete to conserve system memory.

## 🔄 Standard Workflows

### 1. Web Navigation & Scraping
1.  **Launch:** Open a headless Chromium instance.
2.  **Navigate:** Go to the target URL and wait for the network to be idle.
3.  **Extract:** Select specific CSS elements or the entire page body.
4.  **Format:** Convert HTML to Markdown.

### 2. UI Interaction
1.  **Search:** Locate input fields and buttons using CSS selectors.
2.  **Act:** Fill forms, click buttons, or scroll through feeds.
3.  **Capture:** Take screenshots or log terminal outputs for verification.

## 🧰 Authorized Tools
- `tools/browser_operator.py` (Playwright Wrapper)
- `playwright` (Open Source Library)
