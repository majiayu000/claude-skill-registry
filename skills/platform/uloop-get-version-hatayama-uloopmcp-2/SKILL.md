---
name: uloop-get-version
description: "Get Unity and project information via uloop CLI. Use when you need to verify Unity version, check project settings (ProductName, CompanyName, Version), or troubleshoot environment issues."
internal: true
---

# uloop get-version

Get Unity version and project information.

## Usage

```bash
uloop get-version
```

## Parameters

None.

## Output

Returns JSON with:
- `UnityVersion`: Unity Editor version
- `Platform`: Current platform
- `DataPath`: Assets folder path
- `PersistentDataPath`: Persistent data path
- `TemporaryCachePath`: Temporary cache path
- `IsEditor`: Whether running in editor
- `ProductName`: Application product name
- `CompanyName`: Company name
- `Version`: Application version
- `Ver`: uLoopMCP package version

## Notes

This is a sample custom tool demonstrating how to create MCP tools.
