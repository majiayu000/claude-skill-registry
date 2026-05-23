---
name: unity-headless
description: Install Unity Hub/Editor, activate licenses, run headless builds and tests
---

# Unity Headless Skill

Install Unity components, manage licenses, and run headless builds/tests.

> **See also**: [Shared Conventions](../shared/CONVENTIONS.md) | [Safety Guidelines](../shared/SAFETY.md)

## Purpose

Set up Unity for CI/CD and run builds without a GUI.

## Background Knowledge

### Unity Hub CLI

Unity Hub supports headless operation via CLI:
```bash
unityhub --headless <command>
```

### Licensing Models

1. **Serial-based activation** - Requires serial key, can be done headless
2. **Account-based activation** - Requires Unity account login, interactive

### Build Server Concept

Unity supports "Build Server" licensing for headless builds only (batchmode). This is ideal for CI/CD pipelines.

## Installation Paths

Unity can be installed to:
- `/opt/unity/` - System-wide
- `$HOME/.local/share/Unity/` - User-local
- Hub default paths

## Commands

### Hub Installation

```bash
# Download and install Hub (Ubuntu/Debian)
wget -qO - https://hub.unity3d.com/linux/keys/public | sudo apt-key add -
sudo sh -c 'echo "deb https://hub.unity3d.com/linux/repos/deb stable main" > /etc/apt/sources.list.d/unityhub.list'
sudo apt update && sudo apt install unityhub
```

### Editor Installation

```bash
# List available versions
unityhub --headless editors --releases

# Install specific version with modules
unityhub --headless install --version 2022.3.0f1 --module linux-il2cpp --module linux-server
```

### License Activation

```bash
# Serial-based activation
unity -quit -batchmode -serial <serial> -username <email> -password <password>

# Return license
unity -quit -batchmode -returnlicense
```

### Headless Build

```bash
unity -quit -batchmode -nographics \
  -projectPath /path/to/project \
  -executeMethod BuildScript.PerformBuild \
  -logFile build.log
```

### Headless Tests

```bash
unity -quit -batchmode -nographics \
  -projectPath /path/to/project \
  -runTests \
  -testResults results.xml \
  -logFile test.log
```

## Helper Scripts

- `scripts/unity_install.sh` - Install Hub + Editor + modules
- `scripts/unity_build.sh` - Run batchmode build with logging
- `scripts/unity_logs.sh` - Parse logs for errors

## Workflow: Set Up Build Environment

```bash
# 1. Install Hub
./scripts/unity_install.sh hub

# 2. Install Editor (version from ProjectSettings/ProjectVersion.txt)
./scripts/unity_install.sh editor 2022.3.0f1 linux-il2cpp,linux-server

# 3. Activate license
./scripts/unity_install.sh license <serial>
```

## Workflow: Run a Build

```bash
# Build with logging and error checking
./scripts/unity_build.sh \
  ~/workspace/my-game \
  BuildScript.PerformBuild \
  ~/workspace/_artifacts/build.log

# Check exit code
echo "Exit code: $?"
```

## Artifacts

Write all build outputs and logs to:
```
~/workspace/_artifacts/
```

## Safety Rails

- **Always use `-logFile`** - Never run a build without capturing logs
- **Always capture exit code** - Check `$?` after builds
- **License activation failure** - Stop and report required inputs (serial vs account)
- **Never run builds without `-quit`** - Ensures Unity exits after completion

## Common Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Build failed |
| 2 | Invalid arguments |
| 3 | License error |

## Troubleshooting

If license activation fails:
1. Check if machine already has a license (`~/.local/share/unity3d/Unity/Unity_lic.ulf`)
2. Verify serial is valid for this license type
3. Check if Build Server license is appropriate (headless only)
4. Report to user with specific error from log
