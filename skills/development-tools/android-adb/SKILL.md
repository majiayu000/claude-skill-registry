---
name: android-adb
description: Automate ADB commands for device management, app installation, and log analysis. Use when listing devices, installing APKs, viewing logs, debugging app issues, or capturing screenshots.
license: MIT
version: 1.0.0
---

# Android ADB Skill

Automate ADB commands for device management, app installation, and log analysis.

## When to Use

- Listing connected devices
- Installing/uninstalling APKs
- Viewing application logs
- Debugging app issues
- Capturing screenshots/screen recordings

## Commands

### Device Management

| Command | Description | ADB Command |
|---------|-------------|-------------|
| `devices` | List connected devices | `adb devices -l` |
| `restart` | Restart ADB server | `adb kill-server && adb start-server` |

### App Management

| Command | Description | ADB Command |
|---------|-------------|-------------|
| `install` | Install APK | `adb install -r app.apk` |
| `uninstall` | Remove app | `adb uninstall com.package.name` |
| `clear` | Clear app data | `adb shell pm clear com.package.name` |
| `start` | Launch app | `adb shell am start -n pkg/.Activity` |
| `stop` | Force stop app | `adb shell am force-stop com.package.name` |

### Logcat Commands

| Command | Description | ADB Command |
|---------|-------------|-------------|
| `log` | View all logs | `adb logcat -v threadtime` |
| `log:app` | App logs only | `adb logcat --pid=$(adb shell pidof pkg)` |
| `log:tag` | Filter by tag | `adb logcat -s TAG_NAME` |
| `log:error` | Errors only | `adb logcat *:E` |
| `log:clear` | Clear log buffer | `adb logcat -c` |

### Debug Commands

| Command | Description | ADB Command |
|---------|-------------|-------------|
| `screenshot` | Capture screen | `adb exec-out screencap -p > screen.png` |
| `screenrecord` | Record screen | `adb shell screenrecord /sdcard/video.mp4` |
| `anr` | Check ANR traces | `adb pull /data/anr/traces.txt` |
| `crash` | Get crash logs | `adb logcat -b crash` |

## Logcat Patterns

```bash
# Filter by specific tags (common managers)
adb logcat -s GameManagerImpl AuthService SyncManager

# Compose errors
adb logcat | grep -i "compose\|recomposition"

# Coroutine exceptions
adb logcat | grep "CoroutineException\|JobCancellationException"

# ANR detection
adb logcat | grep -i "ANR\|Application Not Responding"

# Timber logs (class name as tag)
adb logcat | grep -E "(GameManager|UserManager|AuthService)"
```

## Usage Examples

```bash
# Install and launch debug build
adb install -r app/build/outputs/apk/debug/app-debug.apk
adb shell am start -n com.creative.aiquiz/.LauncherActivity

# Clear app data and restart
adb shell pm clear com.creative.aiquiz
adb shell am start -n com.creative.aiquiz/.LauncherActivity

# Monitor specific logs
adb logcat -s GameManagerImpl:V

# Capture crash on error
adb logcat *:E -d > crash_log.txt

# Take screenshot for bug report
adb exec-out screencap -p > screenshot.png
```

## Error Handling

```bash
# Check device connection
adb devices -l || (adb kill-server && adb start-server && adb devices -l)

# Handle installation errors
adb install -r app.apk 2>&1 | grep -q "INSTALL_FAILED" && {
    echo "Installation failed - checking signature..."
    adb uninstall com.package.name
    adb install app.apk
}

# Parse crash from logcat
adb logcat -b crash -d | grep -A 20 "FATAL EXCEPTION"
```

**Common Errors:**
- **Device not found**: Enable USB debugging in Developer Options
- **Installation failed**: Uninstall conflicting version first
- **Permission denied**: Device needs root or debugging enabled
- **Unauthorized**: Approve computer on device prompt

## Troubleshooting

| Issue | Command |
|-------|---------|
| Device offline | `adb kill-server && adb start-server` |
| Multiple devices | `adb -s SERIAL_NUMBER shell` |
| App not starting | `adb shell am start -D -n pkg/.Activity` |
| Screen frozen | `adb shell input keyevent 26` |
| Storage full | `adb shell df -h` |

## Command Workflows

```bash
# Full debug cycle
adb logcat -c && \
./gradlew installDebug && \
adb shell am start -n com.pkg/.MainActivity && \
adb logcat -s MainActivity:V

# Capture crash report
adb logcat -b crash -d > crash.txt && \
adb bugreport > bugreport.zip

# Monitor specific feature
adb logcat -c && adb logcat -s GameManager AuthService SyncManager
```

## CI/CD Integration

```yaml
# Firebase Test Lab
- name: Run Instrumented Tests
  run: |
    gcloud firebase test android run \
      --type instrumentation \
      --app app-debug.apk \
      --test app-debug-androidTest.apk
```

## Best Practices

- Prefer filtered logs to avoid overwhelming output
- Use `-d` flag to dump existing logs and exit
- Clear logcat before reproducing issues
- Use Timber tags consistently (class name)

## References

- [ADB Documentation](https://developer.android.com/tools/adb)
- [Logcat Guide](https://developer.android.com/tools/logcat)
- [Debug Your App](https://developer.android.com/studio/debug)
