---
name: uloop-get-project-info
description: "Get Unity project information via uloop CLI. Use when you need to check project settings, Unity version, platform, or other project metadata."
internal: true
---

# uloop get-project-info

Get detailed Unity project information.

## Usage

```bash
uloop get-project-info
```

## Parameters

None.

## Output

Returns JSON with:
- `ProjectName`: Application product name
- `CompanyName`: Company name
- `Version`: Application version
- `UnityVersion`: Unity Editor version
- `Platform`: Current platform
- `DataPath`: Assets folder path
- `IsEditor`: Whether running in editor
- `IsPlaying`: Whether in play mode
- `DeviceType`: Device type
- `OperatingSystem`: OS information
- `ProcessorType`: CPU type
- `SystemMemorySize`: RAM size in MB
- `GraphicsDeviceName`: GPU name

## Notes

This is a sample custom tool demonstrating how to create MCP tools.
