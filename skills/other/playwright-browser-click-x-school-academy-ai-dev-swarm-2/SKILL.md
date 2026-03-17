---
name: playwright-browser-click
description: "To click a page element in the browser, perform a click on buttons, links, or controls during Playwright automation."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"playwright","tool_name":"browser_click","arguments":{}}
```

## Tool Description
Perform click on a web page

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "element": {
      "description": "Human-readable element description used to obtain permission to interact with the element",
      "type": "string"
    },
    "ref": {
      "type": "string",
      "description": "Exact target element reference from the page snapshot"
    },
    "doubleClick": {
      "description": "Whether to perform a double click instead of a single click",
      "type": "boolean"
    },
    "button": {
      "description": "Button to click, defaults to left",
      "type": "string",
      "enum": [
        "left",
        "right",
        "middle"
      ]
    },
    "modifiers": {
      "description": "Modifier keys to press",
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "Alt",
          "Control",
          "ControlOrMeta",
          "Meta",
          "Shift"
        ]
      }
    }
  },
  "required": [
    "ref"
  ],
  "additionalProperties": false
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"playwright","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
