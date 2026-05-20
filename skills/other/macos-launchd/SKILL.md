---
name: macos-launchd
cluster: macos
description: "LaunchDaemons/LaunchAgents, plist, launchctl, login items, OpenClaw gateway service"
tags: ["launchd","plist","services","macos"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "launchd plist launchctl service daemon agent macos openclaw"
---

# macos-launchd

## Purpose
This skill manages macOS launchd services, including LaunchDaemons and LaunchAgents, for tasks like running background processes, handling login items, and setting up the OpenClaw gateway service. It focuses on creating, loading, and controlling services via plist files and launchctl.

## When to Use
Use this skill when you need to automate macOS services, such as starting a script on system boot (LaunchDaemon), running an app on user login (LaunchAgent), or ensuring the OpenClaw gateway service persists across reboots. Apply it for system-level tasks requiring persistence or for integrating OpenClaw with macOS environments.

## Key Capabilities
- Create and edit plist files for LaunchDaemons/Agents, specifying keys like Label, ProgramArguments, and RunAtLoad.
- Load/unload services using launchctl to control execution.
- Manage login items via System Events in AppleScript or launchctl equivalents.
- Integrate with OpenClaw by configuring a service that runs the gateway, using environment variables for authentication like $OPENCLAW_API_KEY.
- Handle service states, such as enabling/disabling, and monitor logs via Console.app.

## Usage Patterns
To accomplish tasks, first create a plist file in /Library/LaunchDaemons (for system-wide) or ~/Library/LaunchAgents (for user-specific). Use launchctl commands to manage it. For OpenClaw integration, embed the gateway command in the plist and reference env vars. Always validate plist syntax before loading. For programmatic access, use AppleScript to add login items, e.g., via osascript.

## Common Commands/API
- Use `launchctl load [-w] /path/to/com.example.plist` to load a service; the -w flag writes to persistent storage.
- Unload with `launchctl unload [-w] /path/to/com.example.plist`.
- Start/stop services: `launchctl start com.example.label` or `launchctl stop com.example.label`.
- Plist format example (in XML):
  ```
  <?xml version="1.0" encoding="UTF-8"?>
  <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
  <plist version="1.0">
    <dict>
      <key>Label</key><string>com.example.service</string>
      <key>ProgramArguments</key><array><string>/usr/bin/python3</string><string>/path/to/script.py</string></array>
      <key>RunAtLoad</key><true/>
    </dict>
  </plist>
  ```
- For OpenClaw gateway, use `launchctl list | grep openclaw` to check status.
- API note: No direct API; interact via launchctl CLI or SystemConfiguration framework in Swift, e.g., `SCDynamicStoreCopyConsoleUser()` for user context.

## Integration Notes
When integrating with OpenClaw, place the gateway service in a plist under ProgramArguments, e.g., `<string>/path/to/openclaw-gateway --key $OPENCLAW_API_KEY</string>`. Set the env var in the plist using <key>EnvironmentVariables</key><dict><key>OPENCLAW_API_KEY</key><string>your_key</string></dict>. Ensure the service runs as the correct user by adding <key>UserName</key><string>yourusername</string>. For cross-skill integration, reference the macos cluster; export paths like export PATH=$PATH:/usr/bin for launchctl access.

## Error Handling
Check launchctl exit codes: 0 for success, non-zero for errors (e.g., 78 for invalid plist). Parse errors with `plutil -lint /path/to/com.example.plist` to validate before loading. If a service fails, use `launchctl error <label>` or check system logs with `log show --predicate 'subsystem == "com.apple.launchd"'`. For OpenClaw, if authentication fails, ensure $OPENCLAW_API_KEY is set and not expired; handle by restarting the service with `launchctl kickstart -k com.openclaw.gateway`. Always unload and reload services after edits to avoid conflicts.

## Usage Examples
1. Create a LaunchAgent to run a script on login: First, write a plist file at ~/Library/LaunchAgents/com.example.login.plist with the above format, then run `launchctl load -w ~/Library/LaunchAgents/com.example.login.plist`. To verify, use `launchctl list | grep com.example`.
2. Set up OpenClaw gateway as a LaunchDaemon: Create /Library/LaunchDaemons/com.openclaw.gateway.plist with <key>ProgramArguments</key><array><string>/path/to/openclaw-gateway</string><string>--key</string><string>$OPENCLAW_API_KEY</string></array>, then execute `sudo launchctl load -w /Library/LaunchDaemons/com.openclaw.gateway.plist`. Monitor with `launchctl list com.openclaw.gateway`.

## Graph Relationships
- Related to: macos (cluster), as it shares tags like "macos" and "services".
- Links to: launchd (tag), for dependent skills like system management; openclaw (embedding hint), for gateway-specific integrations.
- Connected via: plist (tag), potentially linking to file management skills; launchctl (description), for command-line utilities in macos cluster.
