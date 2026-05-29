---
name: harness-ui
description: "Harnessダッシュボードを表示。現状を一目で把握できる司令塔。Use when user mentions '/harness-ui', dashboard, monitoring, or UI display. Do NOT load for: app UI implementation, dashboard component creation, admin panel features."
description-en: "Display Harness dashboard. Command center for status at a glance. Use when user mentions '/harness-ui', dashboard, monitoring, or UI display. Do NOT load for: app UI implementation, dashboard component creation, admin panel features."
description-ja: "Harnessダッシュボードを表示。現状を一目で把握できる司令塔。Use when user mentions '/harness-ui', dashboard, monitoring, or UI display. Do NOT load for: app UI implementation, dashboard component creation, admin panel features."
allowed-tools: ["Read", "Write", "Edit", "Bash", "WebFetch"]
argument-hint: "[LICENSE_KEY] [--force]"
user-invocable: false
---

# Harness UI Skill

Displays the Harness UI dashboard for monitoring sessions, tasks, and project status.

## Quick Reference

- "**UIを開きたい**" → `/harness-ui`
- "**ダッシュボードを見たい**" → `/harness-ui`
- "**ライセンスキーを設定**" → `/harness-ui YOUR-KEY`

## Usage

```bash
/harness-ui              # Open dashboard (auto-setup if needed)
/harness-ui YOUR-KEY     # Set license key and open
/harness-ui --force      # Force re-setup
```

## Accessibility Settings (CC 2.1.38+)

視覚的な快適性のための設定です。

### Reduced Motion 設定

Claude Code の設定ファイルでアニメーションを最小化できます:

```jsonc
// settings.json
{
  "reducedMotion": true  // アニメーションを最小化
}
```

**推奨設定**:

| 設定 | 用途 |
|------|------|
| `reducedMotion: true` | モーション酔い対策、集中力向上 |
| `reducedMotion: false` | デフォルト（アニメーションあり） |

**こんな方におすすめ**:
- 長時間作業で目が疲れやすい方
- アニメーションによる視覚的な刺激に敏感な方
- 集中して作業したい方

設定ファイルの場所:
- **macOS**: `~/Library/Application Support/Claude/settings.json`
- **Windows**: `%APPDATA%\Claude\settings.json`
- **Linux**: `~/.config/Claude/settings.json`

## Features

- Session monitoring
- Task progress visualization
- Plans.md status display
- SSOT file overview
- Real-time updates

## Execution Flow

### Step 1: Check License Key

```bash
SETTINGS_FILE=".claude/state/ui-settings.json"

if [ -f "$SETTINGS_FILE" ]; then
  LICENSE_KEY=$(jq -r '.licenseKey // ""' "$SETTINGS_FILE")
  if [ -n "$LICENSE_KEY" ]; then
    echo "License key found"
    # → Open dashboard
  fi
fi
```

### Step 2: Setup Mode (If No Key)

If license key is not configured:

> **Harness UI Setup**
>
> License key is required to use Harness UI.
>
> Get your key at: https://harness-ui.example.com/license
>
> Enter your license key:

**Wait for response**

### Step 3: Save Settings

```bash
mkdir -p .claude/state
cat > "$SETTINGS_FILE" << EOF
{
  "licenseKey": "$LICENSE_KEY",
  "configured_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
```

### Step 4: Open Dashboard

```bash
# Start UI server
cd "${CLAUDE_PLUGIN_ROOT}/harness-ui"
npm run dev &

# Open in browser
open http://localhost:3001
```

## Dashboard Components

| Component | Description |
|-----------|-------------|
| Session Panel | Active sessions and status |
| Tasks Panel | Plans.md tasks with progress |
| Files Panel | Changed files and SSOT status |
| Logs Panel | Recent activity log |

## Related Commands

- `/sync-status` - CLI-based status check
- `/session` - Session management
