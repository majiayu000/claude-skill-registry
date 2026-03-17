---
name: tauri
description: Tauri framework for building cross-platform desktop and mobile apps. Use for desktop app development, native integrations, Rust backend, and web-based UIs.
---

# Tauri Skill

Comprehensive assistance with Tauri development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Building cross-platform desktop applications with Rust + WebView
- Implementing native system integrations (file system, notifications, system tray)
- Setting up Tauri project structure and configuration
- Debugging Tauri applications in VS Code or Neovim
- Configuring Windows/macOS/Linux code signing for distribution
- Developing mobile apps with Tauri (Android/iOS)
- Creating Tauri plugins for custom native functionality
- Implementing IPC (Inter-Process Communication) between frontend and backend
- Optimizing Tauri app security and permissions
- Setting up CI/CD pipelines for Tauri app releases

## Key Concepts

### Multi-Process Architecture
Tauri uses a **Core Process** (Rust) and **WebView Process** (HTML/CSS/JS) architecture:
- **Core Process**: Manages windows, system tray, IPC routing, and has full OS access
- **WebView Process**: Renders UI using system WebViews (no bundled browser!)
- **Principle of Least Privilege**: Each process has minimal required permissions

### Inter-Process Communication (IPC)
Two IPC primitives:
- **Events**: Fire-and-forget, one-way messages (both Core → WebView and WebView → Core)
- **Commands**: Request-response pattern using `invoke()` API (WebView → Core only)

### Why Tauri?
- **Small binaries**: Uses OS WebViews (Microsoft Edge WebView2/WKWebView/webkitgtk)
- **Security-first**: Message passing architecture prevents direct function access
- **Multi-platform**: Desktop (Windows/macOS/Linux) + Mobile (Android/iOS)

## Quick Reference

### 1. Project Setup - Cargo.toml

```toml
[build-dependencies]
tauri-build = "2.0.0"

[dependencies]
tauri = { version = "2.0.0" }
```

### 2. Windows Code Signing Configuration

```json
{
  "tauri": {
    "bundle": {
      "windows": {
        "certificateThumbprint": "A1B1A2B2A3B3A4B4A5B5A6B6A7B7A8B8A9B9A0B0",
        "digestAlgorithm": "sha256",
        "timestampUrl": "http://timestamp.comodoca.com"
      }
    }
  }
}
```

### 3. VS Code Debugging - launch.json

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "lldb",
      "request": "launch",
      "name": "Tauri Development Debug",
      "cargo": {
        "args": [
          "build",
          "--manifest-path=./src-tauri/Cargo.toml",
          "--no-default-features"
        ]
      },
      "preLaunchTask": "ui:dev"
    }
  ]
}
```

### 4. Rust State Management

```rust
let data = app.state::<AppData>();
```

### 5. GitHub Actions - Publish Workflow

```yaml
name: 'publish'

on:
  push:
    tags:
      - 'app-v*'
```

### 6. Trunk Configuration (Rust Frontend)

```toml
# Trunk.toml
[watch]
ignore = ["./src-tauri"]

[serve]
ws_protocol = "ws"
```

### 7. Azure Key Vault Signing (relic.conf)

```toml
[server.azurekv]
url = "https://<KEY_VAULT_NAME>.vault.azure.net/certificates/<CERTIFICATE_NAME>"
```

### 8. Custom Sign Command (tauri.conf.json)

```json
{
  "tauri": {
    "bundle": {
      "windows": {
        "signCommand": "relic sign -c relic.conf -f -o \"%1\""
      }
    }
  }
}
```

### 9. Opening DevTools Programmatically

```rust
use tauri::Manager;

#[tauri::command]
fn open_devtools(window: tauri::Window) {
    window.open_devtools();
}
```

### 10. Mobile Plugin - Android Command

```kotlin
@Command
fun download(invoke: Invoke) {
    val args = invoke.parseArgs(DownloadArgs::class.java)
    // Command implementation
    invoke.resolve()
}
```

## Reference Files

This skill includes comprehensive documentation organized into 9 categories:

### core_concepts.md
**Contains:** 7 pages covering foundational architecture
- **Process Model**: Multi-process architecture, Core vs WebView processes, security principles
- **Inter-Process Communication**: Events and Commands patterns, message passing
- **Debug in VS Code**: Setting up `vscode-lldb`, launch.json configuration, Windows debugger
- **Tauri Architecture**: Ecosystem overview (tauri-runtime, tauri-macros, tauri-utils, WRY, TAO)

**When to use**: Understanding Tauri's design philosophy, debugging setup, architecture decisions

### development.md
**Contains:** 13 pages on development workflows
- **Debug in Neovim**: nvim-dap setup, codelldb configuration, overseer plugin for dev servers
- **CrabNebula DevTools**: Real-time log inspection, performance tracking, event monitoring
- **Debug**: Development-only code patterns, console logging, WebView inspector, production debugging
- **Mobile Plugin Development**: Android (Kotlin) and iOS (Swift) plugin creation, lifecycle events

**When to use**: Setting up development environment, debugging strategies, mobile development

### distribution.md
**Contains:** 8 pages on app distribution
- **Windows Code Signing**: OV certificates, Azure Key Vault, custom sign commands, GitHub Actions
- **Azure Code Signing**: trusted-signing-cli setup, environment variables, signing workflows
- **Code Signing Best Practices**: EV vs OV certificates, SmartScreen reputation, Microsoft Store

**When to use**: Preparing apps for release, code signing, CI/CD pipelines, production builds

### getting_started.md
**Contains:** Quick start guides and initial setup instructions
- Project initialization
- First Tauri app tutorials
- Configuration basics

**When to use**: Starting new Tauri projects, onboarding new developers

### plugins.md
**Contains:** Plugin development and integration guides
- Creating custom plugins
- Mobile plugin patterns (Android/iOS)
- Plugin configuration
- Lifecycle events (load, onNewIntent)
- Command arguments and parsing

**When to use**: Extending Tauri with native functionality, integrating third-party libraries

### reference.md
**Contains:** API references and configuration schemas
- tauri.conf.json structure
- Command-line interface options
- Configuration options reference

**When to use**: Looking up specific API methods, configuration properties, CLI flags

### security.md
**Contains:** Security best practices and patterns
- Content Security Policy (CSP)
- Secure IPC patterns
- Permission management
- WebView security

**When to use**: Hardening applications, security audits, implementing secure features

### tutorials.md
**Contains:** Step-by-step implementation guides
- Building specific features
- Integration examples
- Real-world use cases

**When to use**: Learning by example, implementing common patterns

### other.md
**Contains:** Miscellaneous documentation not categorized above
- Advanced topics
- Edge cases
- Platform-specific notes

**When to use**: Troubleshooting unusual issues, platform-specific implementations

## Working with This Skill

### For Beginners
1. **Start with**: `getting_started.md` for project setup and basic concepts
2. **Then read**: `core_concepts.md` → Process Model and IPC sections
3. **Practice**: Set up debugging with `development.md` → Debug in VS Code
4. **Build**: Follow tutorials in `tutorials.md`

**Common beginner questions:**
- "How do I create a Tauri app?" → `getting_started.md`
- "What is the Core Process?" → `core_concepts.md` → Process Model
- "How do I call Rust from JavaScript?" → `core_concepts.md` → IPC → Commands

### For Intermediate Developers
1. **Focus on**: `plugins.md` for custom native functionality
2. **Master**: `development.md` for debugging and DevTools
3. **Explore**: `reference.md` for API details
4. **Implement**: Custom IPC patterns from `core_concepts.md`

**Common intermediate questions:**
- "How do I create a custom plugin?" → `plugins.md` → Plugin Development
- "How do I debug performance issues?" → `development.md` → CrabNebula DevTools
- "What configuration options are available?" → `reference.md`

### For Advanced Users
1. **Deep dive**: `security.md` for production-ready security
2. **Optimize**: Mobile development patterns in `plugins.md`
3. **Automate**: Distribution workflows in `distribution.md`
4. **Customize**: Advanced patterns in `other.md`

**Common advanced questions:**
- "How do I set up code signing for Windows?" → `distribution.md` → Windows Code Signing
- "How do I create mobile plugins?" → `development.md` → Mobile Plugin Development
- "What are the security best practices?" → `security.md`

### Navigation Tips
- **Search by topic**: Each reference file has a table of contents
- **Code examples**: All code blocks include language annotations
- **Original docs**: Reference files include URLs to source documentation
- **Quick patterns**: Check the Quick Reference section above first

### Using with Claude
When asking Claude for help with Tauri:
1. **Be specific**: Mention the platform (Windows/macOS/Linux/Android/iOS)
2. **Provide context**: Share your `tauri.conf.json` if relevant
3. **Reference categories**: "Check the distribution.md file for signing info"
4. **Share errors**: Include full error messages and stack traces

## Resources

### references/
Organized documentation extracted from official Tauri sources (https://tauri.app/). These files contain:
- **Detailed explanations**: Architecture, patterns, best practices
- **Code examples**: Language-annotated (rust, json, toml, kotlin, swift)
- **Links to sources**: Original documentation URLs for deeper reading
- **Table of contents**: Quick navigation within each file

### scripts/
Helper scripts for common automation tasks:
- Build scripts
- Testing utilities
- Deployment helpers

*Add your custom scripts here for project-specific automation*

### assets/
Templates, boilerplate, and example projects:
- Project templates
- Configuration examples
- Sample applications

*Add your templates and boilerplate code here*

## Common Patterns

### Creating a Tauri Command
```rust
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

// In main.rs
fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Calling Commands from Frontend
```javascript
import { invoke } from '@tauri-apps/api/core';

const greeting = await invoke('greet', { name: 'World' });
console.log(greeting); // "Hello, World!"
```

### Emitting Events
```rust
// From Rust
app.emit_all("event-name", Payload { message: "Hello".into() }).unwrap();

// Listening in JavaScript
import { listen } from '@tauri-apps/api/event';

const unlisten = await listen('event-name', (event) => {
    console.log(event.payload.message);
});
```

## Debugging Quick Tips

### Enable Rust Backtraces
```bash
# Linux/macOS
RUST_BACKTRACE=1 tauri dev

# Windows (PowerShell)
$env:RUST_BACKTRACE=1; tauri dev
```

### Create Debug Build
```bash
npm run tauri build -- --debug
```

### Open DevTools Programmatically
```rust
use tauri::Manager;
window.open_devtools();
window.close_devtools();
```

## Platform-Specific Notes

### Windows
- Uses **Microsoft Edge WebView2** (automatically installed on Windows 11)
- Code signing required for SmartScreen reputation
- EV certificates get immediate trust; OV certificates build reputation over time

### macOS
- Uses **WKWebView** (native to macOS)
- DevTools API is private (using in production prevents App Store acceptance)
- Code signing with Apple Developer certificate

### Linux
- Uses **webkitgtk** (must be installed separately)
- Package formats: .deb, .rpm, .AppImage

### Android
- Kotlin-based plugins
- Activity lifecycle integration
- Requires Android Studio

### iOS
- Swift-based plugins
- Swift Package Manager for dependencies
- Requires Xcode

## Notes

- This skill was automatically generated from official Tauri documentation
- All code examples are extracted from official sources
- Reference files preserve structure and links to original docs
- Quick reference patterns represent real-world usage
- Last updated: October 2025

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with `configs/tauri.json`
2. The skill will be rebuilt with the latest information
3. Enhancement will preserve custom additions in `scripts/` and `assets/`
