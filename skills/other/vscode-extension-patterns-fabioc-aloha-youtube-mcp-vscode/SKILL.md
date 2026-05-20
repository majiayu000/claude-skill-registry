---
name: "vscode-extension-patterns"
description: "Reusable patterns for VS Code extension development."
user-invokable: false
---

# VS Code Extension Patterns Skill

> Reusable patterns for VS Code extension development.

## ⚠️ Staleness Warning

VS Code APIs evolve with each monthly release. Patterns may become outdated or better alternatives may emerge.

**Refresh triggers:**

- VS Code major/minor releases
- New proposed APIs becoming stable
- Extension API deprecations
- Webview security policy changes

**Last validated:** February 2026 (VS Code 1.109+)

**Check current state:** [VS Code API](https://code.visualstudio.com/api), [Release Notes](https://code.visualstudio.com/updates)

---

## Webview Dashboard

```typescript
// Gather data in parallel, build HTML with async
const [health, knowledge, sync] = await Promise.all([
    checkHealth(true), getKnowledgeSummary(), getSyncStatus()
]);
panel.webview.html = await getWebviewContent(health, knowledge, sync);
```

**Key**: Make `getWebviewContent` async if it needs directory scanning or other async ops.

## TreeDataProvider for Sidebar

```typescript
class WelcomeViewProvider implements vscode.WebviewViewProvider {
    resolveWebviewView(webviewView: vscode.WebviewView) {
        webviewView.webview.options = { enableScripts: true };
        webviewView.webview.html = this.getHtmlContent();
        webviewView.webview.onDidReceiveMessage(async (message) => {
            switch (message.command) {
                case 'refresh': await this.refresh(); break;
            }
        });
    }
}

// Register in extension.ts
vscode.window.registerWebviewViewProvider('alex.welcomeView', new WelcomeViewProvider());
```

## CSP-Compliant Webview Event Handling

**Problem**: Inline event handlers (`onclick="..."`) violate Content Security Policy and can be blocked.

**Solution**: Use `data-cmd` attributes with delegated event listeners:

```html
<!-- ❌ WRONG: Inline handlers (CSP violation) -->
<button onclick="handleClick()">Click</button>

<!-- ✅ CORRECT: data-cmd pattern -->
<button data-cmd="play">Play</button>
<button data-cmd="stop">Stop</button>
```

```javascript
// Single delegated listener for all commands
document.addEventListener('click', (e) => {
    const target = e.target.closest('[data-cmd]');
    if (!target) return;
    
    const cmd = target.getAttribute('data-cmd');
    switch (cmd) {
        case 'play': audio.play(); break;
        case 'stop': audio.pause(); audio.currentTime = 0; break;
    }
});
```

**Benefits**:
- CSP-compliant (no inline scripts)
- Single event listener (better performance)
- Easy to add new commands
- Consistent pattern across webviews

## Safe Configuration Pattern

**Tiered settings**: Essential (🔴) → Recommended (🟡) → Auto-Approval (🟠) → Extended Thinking (🧠) → Enterprise (🔵)

**Safety rules**:

- Additive only — never modify/remove existing
- Check `config.inspect(key)?.globalValue` before applying
- Preview JSON before changes
- User chooses categories
- Preserve higher user values when applying recommendations

```typescript
async function applySettings(settings: Record<string, unknown>) {
    const config = vscode.workspace.getConfiguration();
    for (const [key, value] of Object.entries(settings)) {
        if (config.inspect(key)?.globalValue === undefined) {
            await config.update(key, value, vscode.ConfigurationTarget.Global);
        }
    }
}
```

## Comprehensive Settings Management Pattern

**Pattern**: Documentation-first approach for complex settings ecosystems (VS Code 1.109+ chat settings).

**Steps**:

1. **Research Phase** — Comprehensive discovery
   - Grep search for all related settings in codebase
   - Read MS documentation for official settings
   - Identify experimental/unstable features
   - Document current user configuration

2. **Documentation Phase** — Create reference materials before implementation
   - **GUIDE**: Comprehensive reference (all settings, categories, use cases, warnings)
   - **SUMMARY**: Current state snapshot (what user has, what's missing, recommendations)
   - **APPLIED**: Change log document (what was applied, why, how to rollback)
   - **JSON Template**: Copy-paste ready configuration file

3. **Implementation Phase** — Safe automated application
   - Create PowerShell/shell script for automation (platform-specific)
   - **Always backup** before modifications (`settings.json.backup-{timestamp}`)
   - Compare new vs existing, report changes (new, updated, skipped, preserved)
   - **Preserve higher values** (user has 150, recommending 100? Keep 150)
   - **Exclude unstable features** explicitly documented

4. **Extension Integration** — Make it permanent
   - Update `setupEnvironment.ts` ESSENTIAL_SETTINGS, RECOMMENDED_SETTINGS, etc.
   - Add new categories if pattern discovered (e.g., AUTO_APPROVAL_SETTINGS)
   - Integrate into Initialize/Upgrade commands (`offerEnvironmentSetup()`)
   - Update Welcome sidebar with accurate counts

5. **Validation Phase**
   - Test script execution (fix syntax errors iteratively)
   - Verify settings applied (check VS Code settings.json)
   - Document excluded settings with reasons (hooks not stable, platform-specific)
   - Commit documentation files to git

**Key insights from Feb 2026 implementation**:

- VS Code 1.109+ has 47+ chat-related settings across 6 categories
- Hooks (`chat.hooks.enabled`) marked experimental but not stable yet
- Auto-approval settings reduce friction (5 settings: autoRun, fileSystem.autoApprove, terminal.*)
- Initialize/Upgrade should apply Essential + Recommended + Auto-Approval (36 total)
- PowerShell inline commands unreliable — use `.ps1` file for complex scripts
- Settings categories prevent overwhelming users (show 5 categories vs 47 individual settings)

**When to use this pattern**:

- Complex settings ecosystems (10+ related settings)
- Rapidly evolving features (experimental → stable transitions)
- User education needed (settings have non-obvious interdependencies)
- Safety-critical configuration (wrong settings break functionality)

**Template structure**:

```
docs/guides/
├── FEATURE-SETTINGS-GUIDE.md         # Comprehensive reference
├── FEATURE-SETTINGS-SUMMARY.md       # Current state snapshot  
└── FEATURE-SETTINGS-APPLIED.md       # Change log (gitignore if sensitive)

.vscode/
└── recommended-feature-settings.jsonc # Template (gitignore)

src/commands/
└── setupEnvironment.ts                # Settings constants + apply logic
```

**Benefits**:

- Users understand full capability before committing
- Documentation serves as reference post-application
- Safe rollback via timestamped backups
- Extension automatically applies for new users
- Audit trail of what was applied and why

## Auto-Detection with Confidence

```typescript
const PATTERNS = [
    { pattern: /learned|discovered|realized/i, confidence: 0.8 },
    { pattern: /key insight|the trick is/i, confidence: 0.85 },
];
```

Use confidence thresholds for auto-actions. Higher threshold = fewer false positives.

## Duplicate Detection

```typescript
function isDuplicate(newText: string, existing: string[]): boolean {
    const normalize = (s: string) => s.toLowerCase().replace(/[^\w\s]/g, '');
    return existing.some(e => calculateSimilarity(normalize(newText), normalize(e)) > 0.8);
}
```

## Portability Rules

Extensions must work on any machine:

```typescript
// ✅ CORRECT: Dynamic paths
const rootPath = vscode.workspace.workspaceFolders?.[0].uri.fsPath;
const globalPath = path.join(os.homedir(), '.alex');

// ❌ WRONG: Hardcoded paths
const rootPath = 'c:\\Development\\MyProject';  // Never!
```

**Key utilities**:

- `vscode.workspace.workspaceFolders` — Current workspace
- `os.homedir()` — Platform-independent home
- `path.join()` — Cross-platform path building

## Publishing Workflow

```powershell
# Load PAT from .env
$env:VSCE_PAT = (Get-Content .env | Select-String "VSCE_PAT" | ForEach-Object { $_.Line.Split("=",2)[1] })
vsce publish
```

**Version collision**: Increment patch → update package.json, README badge, CHANGELOG → retry.

## Goals with Streak Tracking

```typescript
interface LearningGoal {
    id: string;
    title: string;
    category: 'coding' | 'reading' | 'practice' | 'review';
    targetCount: number;
    currentCount: number;
    type: 'daily' | 'weekly';
    expiresAt: string;
}

// Auto-increment on activity
async function autoIncrementGoals(activityType: 'session' | 'insight') {
    const data = await loadGoalsData();
    for (const goal of data.goals) {
        if (shouldIncrement(goal, activityType) && !isExpired(goal)) {
            goal.currentCount = Math.min(goal.currentCount + 1, goal.targetCount);
        }
    }
    await saveGoalsData(data);
}
```

## SecretStorage for Sensitive Tokens

**Never store secrets in settings** — use VS Code's SecretStorage API:

```typescript
// Module-level cache
let secretStorage: vscode.SecretStorage | null = null;
let cachedToken: string | null = null;

// Initialize during activation
export async function initSecrets(context: vscode.ExtensionContext): Promise<void> {
    secretStorage = context.secrets;
    cachedToken = await secretStorage.get('myExtension.apiToken') || null;
    
    // Migration: Move token from settings to secrets
    const config = vscode.workspace.getConfiguration('myExtension');
    const settingsToken = config.get<string>('apiToken')?.trim();
    if (settingsToken && !cachedToken) {
        await secretStorage.store('myExtension.apiToken', settingsToken);
        cachedToken = settingsToken;
        await config.update('apiToken', undefined, vscode.ConfigurationTarget.Global);
        vscode.window.showInformationMessage('Token migrated to secure storage.');
    }
}

// Synchronous access to cached value
function getToken(): string | null {
    return cachedToken;
}
```

**Key points:**
- `context.secrets.get()` / `store()` / `delete()` are async
- Cache at module level for sync access
- Migrate existing settings tokens on first run
- Mark old setting as deprecated in package.json

## Webview CSP Security

**Always add Content-Security-Policy** when `enableScripts: true`:

```typescript
import { getNonce } from './sanitize';

function getWebviewHtml(webview: vscode.Webview): string {
    const nonce = getNonce();
    return `<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Security-Policy" content="
        default-src 'none';
        style-src ${webview.cspSource} 'unsafe-inline';
        script-src 'nonce-${nonce}';
        img-src ${webview.cspSource} https: data:;
        font-src ${webview.cspSource};
    ">
</head>
<body>
    <script nonce="${nonce}">
        const vscode = acquireVsCodeApi();
        // ... your code
    </script>
</body>
</html>`;
}

// Nonce generator
function getNonce(): string {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    return Array.from({ length: 32 }, () => 
        chars.charAt(Math.floor(Math.random() * chars.length))
    ).join('');
}
```

## CSP Event Delegation (onclick → data-cmd)

**Problem**: After adding CSP with `script-src 'nonce-${nonce}'`, all inline event handlers (`onclick`, `onchange`) stop working because CSP blocks inline JavaScript.

**Solution**: Replace inline handlers with data attributes and event delegation:

```html
<!-- ❌ BLOCKED BY CSP -->
<button onclick="cmd('upgrade')">Upgrade</button>
<button onclick="cmd('launchSkill', {skill: 'code-review'})">Review</button>

<!-- ✅ CSP-COMPLIANT -->
<button data-cmd="upgrade">Upgrade</button>
<button data-cmd="launchSkill" data-skill="code-review">Review</button>

<script nonce="${nonce}">
    document.addEventListener('click', function(e) {
        const el = e.target.closest('[data-cmd]');
        if (el) {
            e.preventDefault();
            const command = el.getAttribute('data-cmd');
            const skill = el.getAttribute('data-skill');
            vscode.postMessage(skill ? { command, skill } : { command });
        }
    });
</script>
```

**Benefits**:
- Security — CSP blocks all inline scripts
- Performance — Single event listener vs many handlers
- Maintainability — Commands defined as data, not code

## Webview Sandbox: postMessage Required

**Problem**: `window.open()`, `location.reload()`, and direct external links silently fail in sandboxed webviews.

**Solution**: WebView sends message to extension host; extension performs privileged action:

```typescript
// In webview HTML
vscode.postMessage({ type: 'openExternal', url: 'https://example.com' });

// In extension host
panel.webview.onDidReceiveMessage(async (message) => {
    if (message.type === 'openExternal') {
        await vscode.env.openExternal(vscode.Uri.parse(message.url));
    }
});
```

**Key insight**: WebView ↔ Extension Host communication mirrors browser Content Script ↔ Background Script patterns.

## Telemetry Opt-Out Compliance

**Always respect VS Code's telemetry settings:**

```typescript
function isTelemetryEnabled(): boolean {
    // Check VS Code global setting first
    if (!vscode.env.isTelemetryEnabled) {
        return false;
    }
    // Then check extension-specific setting
    const config = vscode.workspace.getConfiguration('myExtension');
    return config.get<boolean>('telemetry.enabled', true);
}

function log(event: string, data?: Record<string, unknown>): void {
    if (!isTelemetryEnabled()) {
        return;
    }
    // Send telemetry...
}
```

## Configuration Change Listeners

**React to settings changes at runtime:**

```typescript
export function activate(context: vscode.ExtensionContext) {
    // Listen for configuration changes
    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration(e => {
            if (e.affectsConfiguration('myExtension.featureA')) {
                // Refresh feature A
                refreshFeatureA();
            }
            if (e.affectsConfiguration('myExtension.telemetry')) {
                // Update telemetry state
            }
        })
    );
}
```

**Key points:**
- Use `affectsConfiguration()` to filter relevant changes
- Push listener to `context.subscriptions` for cleanup
- Re-read config values, don't cache indefinitely

## VS Code 1.109+ Agent Platform Capabilities

VS Code 1.109 introduces a native agent platform that extensions can leverage:

### Agent Files (`AGENTS.md`)

Extensions can ship agent definitions that VS Code auto-discovers:

```markdown
<!-- .github/agents/my-agent.agent.md -->
---
name: "MyAgent"
description: "Specialized agent for domain X"
---

# MyAgent Instructions

Agent-specific instructions and knowledge go here.
```

**Setting**: `chat.useAgentsMdFile: true` enables automatic loading.

### Skills Loading

Extensions can define skills in `.github/skills/` that are auto-loaded into chat:

**Setting**: `chat.agentSkillsLocations: [".github/skills"]`

Each skill folder contains a `SKILL.md` (knowledge) and optional `synapses.json` (connections).

### Chat Participant API

Register custom chat participants that users can `@mention`:

```typescript
const participant = vscode.chat.createChatParticipant('myext.agent', async (request, context, stream, token) => {
  // Access to request.prompt, request.command
  // Stream responses with stream.markdown(), stream.button(), stream.reference()
  stream.markdown('Hello from my agent!');
});

participant.iconPath = vscode.Uri.joinPath(context.extensionUri, 'icon.png');
context.subscriptions.push(participant);
```

### Tool Registration

Register tools that any chat participant can invoke:

```typescript
const tool = vscode.lm.registerTool('myext-searchDocs', {
  async invoke(options, token) {
    const query = options.input.query;
    // Perform tool action
    return new vscode.LanguageModelToolResult([
      new vscode.LanguageModelTextPart(JSON.stringify(results))
    ]);
  }
});
context.subscriptions.push(tool);
```

**Declare in package.json**:

```json
{
  "contributes": {
    "languageModelTools": [{
      "name": "myext-searchDocs",
      "displayName": "Search Documentation",
      "modelDescription": "Searches project documentation for relevant content",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": { "type": "string", "description": "Search query" }
        },
        "required": ["query"]
      }
    }]
  }
}
```

### Extended Thinking

Models supporting extended thinking can be configured per-model:

```json
{
  "claude-opus-4-*.extendedThinkingEnabled": true,
  "claude-opus-4-*.thinkingBudget": 16384
}
```

### MCP Integration

VS Code 1.109+ supports Model Context Protocol servers:

**Setting**: `chat.mcp.gallery.enabled: true`

MCP servers extend AI capabilities with external tools (Azure, GitHub, databases).

### Key 1.109 Settings Summary

| Setting | Value | Purpose |
|---------|-------|---------|
| `chat.agent.enabled` | `true` | Enable custom agents |
| `chat.agentSkillsLocations` | `[".github/skills"]` | Auto-load skills |
| `chat.useAgentsMdFile` | `true` | Use AGENTS.md |
| `chat.mcp.gallery.enabled` | `true` | MCP tool access |

## Integration Audit Checklist

**10-category audit scoring system** (5 points each, 50 total):

| # | Category | What to Check |
|---|----------|---------------|
| 1 | Activation Events | package.json activationEvents match actual needs |
| 2 | Extension Context | context.subscriptions, secrets, globalState usage |
| 3 | Disposable Management | All disposables pushed to subscriptions |
| 4 | Command Registration | Commands in package.json match registerCommand |
| 5 | Configuration Access | getConfiguration usage, onDidChangeConfiguration |
| 6 | Webview Security | CSP policies, nonce usage, enableScripts |
| 7 | Language Model/Chat | vscode.lm patterns, tool registration |
| 8 | Telemetry | vscode.env.isTelemetryEnabled respected |
| 9 | Error Handling | try/catch patterns, error type handling |
| 10 | File System | vscode.workspace.fs vs Node.js fs |

**Quick wins** (high impact, low effort):
- Telemetry opt-out: Check `vscode.env.isTelemetryEnabled`
- CSP on webviews: Add Content-Security-Policy with nonce
- Config listeners: Add `onDidChangeConfiguration` for runtime updates
- Secret storage: Use `context.secrets` instead of settings for tokens

**Scoring**:
- 45-50: Excellent — Ready for publish
- 40-44: Good — Minor fixes
- 35-39: Fair — Address before publish
- <35: Needs Work — Major refactoring

**When to apply**: Before marketplace publishing, after major features, quarterly reviews.

## Synapses

See [synapses.json](synapses.json) for connections.
