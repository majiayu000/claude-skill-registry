## Persistent Scheduling via launchd

To run stock checks when Claude Code is not open, create a launchd plist.

Save as `~/Library/LaunchAgents/com.claude.stock-monitor.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.claude.stock-monitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/tomdimino/.claude/skills/stock-monitor/scripts/stock_check.py</string>
    </array>
    <key>StartInterval</key>
    <integer>1800</integer>
    <key>StandardOutPath</key>
    <string>/tmp/stock-monitor.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/stock-monitor.err</string>
</dict>
</plist>
```

Load: `launchctl load ~/Library/LaunchAgents/com.claude.stock-monitor.plist`
Unload: `launchctl unload ~/Library/LaunchAgents/com.claude.stock-monitor.plist`
