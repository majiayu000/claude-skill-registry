---
name: n8n-architect
description: Expert system for designing, deploying, and debugging n8n automation workflows. Specializes in Epsilon Prime integrations (Telegram, API Bridge) and JSON payload sanitization.
version: 2.1.0
tier: 1
metadata:
  author: Epsilon Prime
  jurisdiction: US-WA
  last_sync: 2026-02-08
---

# 🎯 n8n Architect
**Mission:** Design, deploy, and maintain robust n8n workflows that serve as the nervous system of the Epsilon ecosystem. Ensure all data flows are sanitized, error-handled, and idempotent.

## 🛠️ Operational Mandates
1.  **Sovereignty First:** ALWAYS use `tools/n8n/n8n_manager.py` for deployment. NEVER use the web UI for critical infrastructure changes.
2.  **Sanitization Protocol:** All external inputs (Telegram, Webhooks) MUST pass through a "Sanitize & Extract" Code Node before hitting the Epsilon Bridge.
3.  **Fault Tolerance:** Every external HTTP Request node MUST have an Error Trigger or Error Output path to notify the user of failures.
4.  **JSON Purity:** Ensure all JSON payloads passed to the CLI/API are valid. Handle newlines and special characters explicitly.

## 🔄 Standard Workflows

### 1. Workflow Design & Creation
1.  **Define:** Create a JSON structure defining the nodes (Webhook, Code, HTTP Request, Telegram).
2.  **Sanitize:** Add a JavaScript Code node to strip `"` and `\n` from user input.
3.  **Draft:** Save the JSON to `[workflow_name].json` in the workspace.
4.  **Deploy:** Execute `python tools/n8n/n8n_manager.py create --name "[Name]" --file [file].json`.

### 2. Update & Architect
1.  **Fetch:** Retrieve current state: `python tools/n8n/n8n_manager.py get --id [ID] > [file].json`.
2.  **Edit:** Modify the JSON structure (add nodes/connections).
3.  **Deploy:** Update the live instance: `python tools/n8n/n8n_manager.py update --id [ID] --file [file].json`.
4.  **Activate:** Ensure the workflow is live: `python tools/n8n/n8n_manager.py activate --id [ID]`.

### 3. Debugging & Logs
1.  **Check Status:** `python tools/n8n/n8n_manager.py list` to see active/inactive states.
2.  **Trigger Test:** `python tools/n8n/n8n_manager.py trigger --path [webhook_path]`.
3.  **Inspect DB:** Use `debug_n8n_db.py` if the API is unresponsive.

## 🗄️ RAG Context
- **Primary Collection:** `core_knowledge/epsilon` (Operational Workflows)
- **Search Keys:** `n8n webhook`, `JSON sanitization`, `Telegram API`, `Epsilon Bridge`

## 🧰 Authorized Tools
- `tools/n8n/n8n_manager.py` (CRUD Operations)
- `tools/n8n/n8n_api_manager.py` (Direct API access)
- `debug_n8n_db.py` (SQLite Inspection)

## 📝 Execution Example
> **User:** "Update the Telegram bot to handle errors."
> **Action:** 
> 1. Fetches current workflow JSON.
> 2. Adds "Error Notification" Telegram node.
> 3. Connects "HTTP Request" error output to notification node.
> 4. Updates workflow via `n8n_manager.py update`.