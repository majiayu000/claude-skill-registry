---
name: macos-automation
cluster: macos
description: "AppleScript, JXA, Shortcuts, Automator, osascript, System Events, accessibility API"
tags: ["automation","applescript","shortcuts","macos"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "automation applescript shortcuts automator macos scripting jxa"
---

# macos-automation

## Purpose
This skill automates tasks on macOS using tools like AppleScript, JXA, Shortcuts, Automator, osascript, System Events, and the accessibility API, enabling script-based control of apps and system functions.

## When to Use
- Automate repetitive workflows, such as file management or app interactions.
- Integrate with macOS apps for custom behaviors, like triggering actions via keyboard shortcuts.
- Script complex sequences involving multiple apps, e.g., when Shortcuts alone isn't sufficient.
- Handle accessibility tasks, like UI element manipulation, when apps don't expose direct APIs.
- Use for rapid prototyping of automations in environments like shell scripts or IDEs.

## Key Capabilities
- Execute AppleScript via osascript for app control, e.g., manipulating Finder or Safari.
- Run JXA (JavaScript for Automation) to interact with macOS APIs, supporting modern JavaScript syntax.
- Create and invoke Shortcuts programmatically for quick actions, like sharing files.
- Use Automator workflows as scripts, convertible to applications or services.
- Leverage System Events for UI automation, including keyboard/mouse simulation via accessibility API.
- Access macOS-specific APIs like NSAppleScript for embedding in Objective-C/Swift code.

## Usage Patterns
- Run scripts from the command line using osascript; for example, pipe AppleScript code directly.
- Embed JXA in Node.js environments by loading the JXA module and executing via `Application('Finder').activate()`.
- Chain Shortcuts with other tools by exporting as URLs and invoking via `open` command.
- Use Automator to build workflows, then save as .applescript files for osascript execution.
- For accessibility, ensure "Accessibility" is enabled in System Preferences > Security & Privacy, then use System Events to target UI elements like `tell application "System Events" to click button "OK" of window "Main"`.
- Always check for required permissions, such as Full Disk Access, before running scripts that access files.

## Common Commands/API
- **osascript CLI**: Use `osascript -e 'tell application "Finder" to make new folder at desktop'` to create a folder; handle errors by checking the exit code.
- **JXA Example**: In a JavaScript file, use `const app = Application('Safari'); app.activate(); app.documents[0].url = 'https://example.com';` to open and navigate a URL.
- **Shortcuts Integration**: Run a shortcut via `shortcuts run "My Shortcut" -i '{"input": "text"}'`; pass inputs as JSON for parameterized execution.
- **Automator API**: Convert workflows to AppleScript with `tell application "Automator" to run workflow "path/to/workflow"`.
- **System Events API**: For UI automation, use `osascript -e 'tell application "System Events" to keystroke "a" using {command down}'` to simulate Command+A.
- **Config Formats**: Store scripts in plain text files (.applescript) and invoke with `osascript path/to/script.applescript`; for JXA, use ES6 modules in .js files.

## Integration Notes
- Integrate with other tools by wrapping osascript calls in shell scripts; e.g., use `$ export APPLESCRIPT_PATH='/path/to/script'` and run via `osascript $APPLESCRIPT_PATH`.
- For JXA, require the OSA module in Node.js: `npm install osa` and use `const OSA = require('osa'); OSA.runAppleScript('...')`.
- If accessibility features are needed, set the env var `$ACCESSIBILITY_ENABLED=1` after granting permissions in System Preferences.
- Auth/keys: For scripts accessing protected resources, use env vars like `$osascript_API_KEY` (though rare); more commonly, handle macOS permissions via `tccutil` CLI, e.g., `tccutil reset AppleEvents com.example.app` to reset access.
- Embed in larger apps by compiling AppleScript into bundles or using JXA in Electron apps for cross-tool integration.

## Error Handling
- Check osascript exit codes: If a script fails, capture with `osascript -e 'script' 2>&1` and parse stderr for messages like "Execution error: ...".
- In JXA, wrap code in try-catch: `try { Application('Finder').activate(); } catch (e) { console.error(e.message); }` to handle app not found errors.
- For Shortcuts, verify with `shortcuts run "Name" --wait-for-result` and check output for failures.
- Use Automator's built-in logging by enabling in workflow settings, then review logs via Console app.
- General pattern: Always run scripts with elevated privileges if needed, e.g., via `sudo osascript -e '...'`, and handle permission errors by prompting users to adjust settings.

## Concrete Usage Examples
1. **Automate App Launch and Action**: Use osascript to open Safari and load a page: `osascript -e 'tell application "Safari" to open location "https://example.com"' followed by 'tell application "Safari" to activate'`. This is useful for daily workflows; extend by adding error checks.
2. **UI Automation with Shortcuts**: Create a Shortcut to resize windows, then invoke via CLI: `shortcuts run "Resize Window" -i '{"app": "Finder", "width": 800}'`. Combine with JXA for dynamic inputs, e.g., in a script: `Application('Shortcuts').run('Resize Window', {input: JSON.stringify({app: 'Finder'})})`.

## Graph Relationships
- Related to: macos cluster (direct parent), applescript skill (sub-skill for scripting), shortcuts skill (integrated tool), automation cluster (broader category).
- Dependencies: Requires macos-os (base system), interacts with accessibility-api skill for UI tasks.
