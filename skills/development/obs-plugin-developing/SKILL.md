---
name: obs-plugin-developing
description: Entry point for OBS Studio plugin development. Routes to specialized skills for audio plugins, video plugins, outputs, encoders, and services. Covers plugin types overview, build system setup, and module registration basics. Use when starting OBS plugin development or unsure which skill to use.
version: 1.0.0
---

# OBS Plugin Development

## Purpose

Entry point skill for the OBS Studio plugin development ecosystem. Routes to specialized skills based on plugin type and guides initial project setup.

## When NOT to Use

- Developing audio plugins → Use **obs-audio-plugin-writing**
- Reviewing existing plugin code → Use **obs-plugin-reviewing**
- Need comprehensive guidance → Use **obs-plugin-expert** agent

## Skill Routing

| Task                     | Use Skill                    |
| ------------------------ | ---------------------------- |
| Create audio filter      | `obs-audio-plugin-writing`   |
| Create audio source      | `obs-audio-plugin-writing`   |
| Review plugin code       | `obs-plugin-reviewing`       |
| Video plugins (future)   | Check this skill for updates |
| Output plugins (future)  | Check this skill for updates |
| Encoder plugins (future) | Check this skill for updates |

## OBS Plugin Types Overview

### Sources (obs_source_info)

Sources render video and/or audio content. Three main types:

| Type           | Flag                         | Purpose                         |
| -------------- | ---------------------------- | ------------------------------- |
| **INPUT**      | `OBS_SOURCE_TYPE_INPUT`      | Capture devices, generators     |
| **FILTER**     | `OBS_SOURCE_TYPE_FILTER`     | Process video/audio from parent |
| **TRANSITION** | `OBS_SOURCE_TYPE_TRANSITION` | Animate between sources         |

**Output capability flags:**

- `OBS_SOURCE_VIDEO` - Renders video
- `OBS_SOURCE_AUDIO` - Outputs audio
- `OBS_SOURCE_ASYNC_VIDEO` - Provides raw frames (RAM-based)
- `OBS_SOURCE_COMPOSITE` - Contains child sources

### Outputs (obs_output_info)

Handle streaming and recording by receiving raw or encoded data.

**Examples:** RTMP streaming, file recording, FFmpeg muxing

### Encoders (obs_encoder_info)

Wrap codec implementations for video/audio compression.

**Examples:** x264, NVENC, QuickSync, AAC

### Services (obs_service_info)

Integrate with streaming platforms.

**Examples:** Twitch, YouTube, custom RTMP

## Module Registration (Required)

Every OBS plugin requires this boilerplate:

```c
#include <obs-module.h>

/* Required: Exports common module functions */
OBS_DECLARE_MODULE()

/* Optional: Load locale from data/locale/ */
OBS_MODULE_USE_DEFAULT_LOCALE("my-plugin", "en-US")

bool obs_module_load(void)
{
    /* Register your plugin components here */
    obs_register_source(&my_source);
    // obs_register_output(&my_output);
    // obs_register_encoder(&my_encoder);
    // obs_register_service(&my_service);

    return true;  /* Must return true on success */
}

void obs_module_unload(void)
{
    /* Optional: Cleanup on unload */
}
```

## Build System Setup

### Using obs-plugintemplate (Recommended)

Clone and customize the official template:

```bash
# Clone template
git clone https://github.com/obsproject/obs-plugintemplate my-plugin
cd my-plugin

# Edit buildspec.json with your plugin info
# Edit src/plugin-main.c with your implementation
```

### buildspec.json Configuration

```json
{
  "name": "my-plugin",
  "displayName": "My Plugin",
  "version": "1.0.0",
  "author": "Your Name",
  "website": "https://example.com",
  "email": "you@example.com"
}
```

### CMakeLists.txt Structure

```cmake
cmake_minimum_required(VERSION 3.28...3.30)

project(my-plugin VERSION 1.0.0)

add_library(${CMAKE_PROJECT_NAME} MODULE)

find_package(libobs REQUIRED)
target_link_libraries(${CMAKE_PROJECT_NAME} PRIVATE OBS::libobs)

target_sources(${CMAKE_PROJECT_NAME} PRIVATE src/plugin-main.c)
```

### Build Commands

```bash
# Configure
cmake -B build -S .

# Build
cmake --build build

# Install (to OBS plugins directory)
cmake --install build
```

## Project Structure

```
my-plugin/
├── CMakeLists.txt
├── buildspec.json
├── src/
│   ├── plugin-main.c     # Module registration
│   ├── my-source.c       # Source implementation
│   └── plugin-support.h  # Helper macros
└── data/
    └── locale/
        └── en-US.ini     # Localization strings
```

## External Documentation

### Context7 (Real-time docs)

```
mcp__context7__get-library-docs
context7CompatibleLibraryID: "/obsproject/obs-studio"
topic: "plugin development"
```

### Official Documentation

- **Plugin Guide**: https://docs.obsproject.com/plugins
- **Plugin Template**: https://github.com/obsproject/obs-plugintemplate
- **Module Reference**: https://docs.obsproject.com/reference-modules
- **Source Reference**: https://docs.obsproject.com/reference-sources

## Related Skills

- **obs-audio-plugin-writing** - Audio sources and filters (primary focus)
- **obs-plugin-reviewing** - Code review and quality audit

## Related Agent

Use **obs-plugin-expert** agent for:

- Coordinated guidance across all OBS plugin skills
- Complex plugin development workflows
- When unsure which skill to apply
