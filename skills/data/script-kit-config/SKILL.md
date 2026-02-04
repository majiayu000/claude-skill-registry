---
name: script-kit-config
description: Configuration management for script-kit-gpui
---

# script-kit-config

The configuration system for Script Kit GPUI manages user preferences, hotkeys, built-in feature flags, process limits, and AI provider settings. Configuration is loaded from a TypeScript file at startup and provides sensible defaults for all settings.

## Config Files

### Primary Config File
- **Location**: `~/.scriptkit/kit/config.ts`
- **Format**: TypeScript with default export
- **Type**: Uses `Config` interface from `@scriptkit/sdk`

### Config Loading Process
1. Check if `~/.scriptkit/kit/config.ts` exists
2. Transpile TypeScript to JavaScript using `bun build`
3. Execute the JS to extract the default export as JSON
4. Parse JSON into `Config` struct
5. Fall back to `Config::default()` if any step fails

### Example config.ts
```typescript
import type { Config } from "@scriptkit/sdk";

export default {
  hotkey: {
    modifiers: ["meta"],
    key: "Semicolon"
  },
  editor: "code",
  editorFontSize: 16,
  terminalFontSize: 14,
  uiScale: 1.0,
  builtIns: {
    clipboardHistory: true,
    appLauncher: true,
    windowSwitcher: true
  }
} satisfies Config;
```

## Key Configuration Options

### HotkeyConfig (Required)
The main hotkey to open Script Kit:
```typescript
hotkey: {
  modifiers: ["meta"],        // "meta", "ctrl", "alt", "shift"
  key: "Semicolon"            // "KeyK", "Digit0", "Space", etc.
}
```

### UI Settings
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `editorFontSize` | `f32` | `16.0` | Font size for editor prompts (pixels) |
| `terminalFontSize` | `f32` | `14.0` | Font size for terminal prompts (pixels) |
| `uiScale` | `f32` | `1.0` | UI scale factor (1.0 = 100%) |
| `padding` | `ContentPadding` | `{top: 8, left: 12, right: 12}` | Content area padding |

### Built-in Features (`builtIns`)
```typescript
builtIns: {
  clipboardHistory: true,    // Enable clipboard history (default: true)
  appLauncher: true,         // Enable app launcher (default: true)
  windowSwitcher: true       // Enable window switcher (default: true)
}
```

### Suggested Section (`suggested`)
Frecency-based ranking configuration:
```typescript
suggested: {
  enabled: true,              // Show Suggested section (default: true)
  maxItems: 10,               // Max items to show (default: 10)
  minScore: 0.1,              // Min score threshold (default: 0.1)
  halfLifeDays: 7.0,          // Score decay half-life (default: 7.0)
  trackUsage: true,           // Track script usage (default: true)
  excludedCommands: ["builtin-quit-script-kit"]  // Commands to exclude
}
```

### Process Limits (`processLimits`)
```typescript
processLimits: {
  maxMemoryMb: 512,           // Max memory in MB (optional)
  maxRuntimeSeconds: 300,     // Max runtime in seconds (optional)
  healthCheckIntervalMs: 5000 // Health check interval (default: 5000)
}
```

### Special Hotkeys
```typescript
notesHotkey: {
  modifiers: ["meta", "shift"],
  key: "KeyN"                 // Cmd+Shift+N for Notes
},
aiHotkey: {
  modifiers: ["meta", "shift"],
  key: "Space"                // Cmd+Shift+Space for AI Chat
}
```

### Per-Command Configuration (`commands`)
Override shortcuts, visibility, and confirmation for specific commands:
```typescript
commands: {
  "builtin/clipboard-history": {
    shortcut: {
      modifiers: ["meta", "shift"],
      key: "KeyV"
    },
    hidden: false,
    confirmationRequired: false
  },
  "script/my-dangerous-script": {
    confirmationRequired: true
  }
}
```

**Command ID Formats:**
- `builtin/` - Built-in Script Kit features
- `app/` - macOS applications (by bundle identifier)
- `script/` - User scripts (by filename)
- `scriptlet/` - Inline scriptlets (by UUID or name)

### Other Settings
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `editor` | `string?` | `$EDITOR` or `"code"` | External editor command |
| `bun_path` | `string?` | System PATH | Custom path to bun binary |
| `clipboardHistoryMaxTextLength` | `usize` | `100000` | Max bytes for clipboard text (0 = no limit) |

## Environment Variables

### AI Provider API Keys
All AI API keys use the `SCRIPT_KIT_*_API_KEY` prefix for security:

| Variable | Provider |
|----------|----------|
| `SCRIPT_KIT_OPENAI_API_KEY` | OpenAI (GPT models) |
| `SCRIPT_KIT_ANTHROPIC_API_KEY` | Anthropic (Claude models) |
| `SCRIPT_KIT_GOOGLE_API_KEY` | Google (Gemini models) |
| `SCRIPT_KIT_GROQ_API_KEY` | Groq (fast inference) |
| `SCRIPT_KIT_OPENROUTER_API_KEY` | OpenRouter (multi-provider) |
| `SCRIPT_KIT_VERCEL_API_KEY` | Vercel AI |

### Debug Environment Variables
| Variable | Purpose |
|----------|---------|
| `SCRIPT_KIT_DEBUG_GRID` | Enable grid overlay for debugging |
| `SCRIPT_KIT_AI_LOG=1` | Enable ultra-compact AI log format |
| `SCRIPT_KIT_FIELD_DEBUG` | Enable form field debugging |
| `SCRIPT_KIT_TEST_NOTES_HOVERED` | Test notes hover state |
| `SCRIPT_KIT_TEST_NOTES_ACTIONS_PANEL` | Test notes actions panel |

### Standard Environment Variables
| Variable | Purpose |
|----------|---------|
| `EDITOR` | Fallback editor if not in config |

## Loading and Persistence

### Config Loading (`load_config()`)
Located in `src/config/loader.rs`:
```rust
pub fn load_config() -> Config {
    let config_path = PathBuf::from(shellexpand::tilde("~/.scriptkit/kit/config.ts").as_ref());
    
    if !config_path.exists() {
        return Config::default();
    }
    
    // 1. Transpile with bun build
    // 2. Execute and extract JSON
    // 3. Parse into Config struct
    // Falls back to Config::default() on any error
}
```

### Getter Methods
All optional config fields have corresponding getter methods that provide defaults:
- `config.get_editor()` - Returns configured editor, `$EDITOR`, or `"code"`
- `config.get_padding()` - Returns `ContentPadding::default()` if not set
- `config.get_builtins()` - Returns `BuiltInConfig::default()` if not set
- `config.get_suggested()` - Returns `SuggestedConfig::default()` if not set
- `config.get_process_limits()` - Returns `ProcessLimits::default()` if not set
- `config.requires_confirmation(command_id)` - Checks confirmation requirements

### Clipboard History Config
Runtime-configurable via `src/clipboard_history/config.rs`:
```rust
set_retention_days(30);           // Set retention period
set_max_text_content_len(100000); // Set max text length (0 = no limit)
```

### JSON Serialization
- Uses `serde` with `#[serde(rename_all = "camelCase")]`
- Optional fields use `#[serde(skip_serializing_if = "Option::is_none")]`
- TypeScript config uses camelCase (e.g., `editorFontSize`, `builtIns`)

## Default Values

All defaults are defined in `src/config/defaults.rs`:

```rust
// Padding
pub const DEFAULT_PADDING_TOP: f32 = 8.0;
pub const DEFAULT_PADDING_LEFT: f32 = 12.0;
pub const DEFAULT_PADDING_RIGHT: f32 = 12.0;

// Font sizes
pub const DEFAULT_EDITOR_FONT_SIZE: f32 = 16.0;
pub const DEFAULT_TERMINAL_FONT_SIZE: f32 = 14.0;

// UI scale
pub const DEFAULT_UI_SCALE: f32 = 1.0;

// Built-in features (all enabled by default)
pub const DEFAULT_CLIPBOARD_HISTORY: bool = true;
pub const DEFAULT_APP_LAUNCHER: bool = true;
pub const DEFAULT_WINDOW_SWITCHER: bool = true;

// Clipboard history
pub const DEFAULT_CLIPBOARD_HISTORY_MAX_TEXT_LENGTH: usize = 100_000;

// Process limits
pub const DEFAULT_HEALTH_CHECK_INTERVAL_MS: u64 = 5000;

// Suggested section
pub const DEFAULT_SUGGESTED_ENABLED: bool = true;
pub const DEFAULT_SUGGESTED_MAX_ITEMS: usize = 10;
pub const DEFAULT_SUGGESTED_MIN_SCORE: f64 = 0.1;
pub const DEFAULT_SUGGESTED_HALF_LIFE_DAYS: f64 = 7.0;
pub const DEFAULT_SUGGESTED_TRACK_USAGE: bool = true;

// Commands requiring confirmation by default
pub const DEFAULT_CONFIRMATION_COMMANDS: &[&str] = &[
    "builtin-shut-down",
    "builtin-restart",
    "builtin-log-out",
    "builtin-empty-trash",
    "builtin-sleep",
    "builtin-quit-script-kit",
    "builtin-test-confirmation", // Dev test item
];

// Commands excluded from frecency tracking
pub const DEFAULT_FRECENCY_EXCLUDED_COMMANDS: &[&str] = &["builtin-quit-script-kit"];
```

## Anti-patterns

### Missing Required `hotkey` Field
```typescript
// BAD - will fail to parse
export default {
  editor: "vim"
};

// GOOD - always include hotkey
export default {
  hotkey: {
    modifiers: ["meta"],
    key: "Semicolon"
  },
  editor: "vim"
};
```

### Using snake_case in TypeScript
```typescript
// BAD - Rust uses camelCase for JSON
export default {
  hotkey: { modifiers: ["meta"], key: "Semicolon" },
  editor_font_size: 16,  // Wrong!
  built_ins: {}          // Wrong!
};

// GOOD - Use camelCase
export default {
  hotkey: { modifiers: ["meta"], key: "Semicolon" },
  editorFontSize: 16,
  builtIns: {}
};
```

### Incorrect Hotkey Format
```typescript
// BAD - key should be a JavaScript key code
hotkey: {
  modifiers: ["cmd"],     // Use "meta" not "cmd"
  key: ";"                // Use "Semicolon" not ";"
}

// GOOD - Use correct key codes
hotkey: {
  modifiers: ["meta"],    // "meta", "ctrl", "alt", "shift"
  key: "Semicolon"        // "KeyA", "Digit0", "Space", "Semicolon"
}
```

### Exposing API Keys in Config
```typescript
// BAD - Don't put API keys in config.ts
export default {
  hotkey: { modifiers: ["meta"], key: "Semicolon" },
  openaiKey: "sk-..." // NEVER do this!
};

// GOOD - Use environment variables
// Set in ~/.zshrc or ~/.scriptkit/.env:
// export SCRIPT_KIT_OPENAI_API_KEY="sk-..."
```

### Forgetting Default Fallbacks
```rust
// BAD - Direct field access may panic or return None
let font_size = config.editor_font_size.unwrap();

// GOOD - Use getter methods that provide defaults
let font_size = config.get_editor_font_size();
```

### Not Handling Config Load Failures
The `load_config()` function always returns a valid `Config` (defaults on error), but logging should capture failures:
```rust
// Config loading is designed to be resilient
// It logs warnings on failure and returns defaults
// Never panics on invalid config
```

## Module Structure

```
src/config/
  mod.rs         - Public API, re-exports
  types.rs       - Struct definitions (Config, HotkeyConfig, BuiltInConfig, etc.)
  defaults.rs    - Default constant values (DEFAULT_* constants)
  loader.rs      - File system loading and parsing (load_config())
  config_tests.rs - Unit tests
```

Note: AI provider configuration uses environment variables (see Environment Variables section), not a separate config module.

## Key Types

```rust
pub struct Config {
    pub hotkey: HotkeyConfig,
    pub bun_path: Option<String>,
    pub editor: Option<String>,
    pub padding: Option<ContentPadding>,
    pub editor_font_size: Option<f32>,
    pub terminal_font_size: Option<f32>,
    pub ui_scale: Option<f32>,
    pub built_ins: Option<BuiltInConfig>,
    pub process_limits: Option<ProcessLimits>,
    pub clipboard_history_max_text_length: Option<usize>,
    pub suggested: Option<SuggestedConfig>,
    pub notes_hotkey: Option<HotkeyConfig>,
    pub ai_hotkey: Option<HotkeyConfig>,
    pub commands: Option<HashMap<String, CommandConfig>>,
}

pub struct HotkeyConfig {
    pub modifiers: Vec<String>,  // "meta", "ctrl", "alt", "shift"
    pub key: String,             // JavaScript key code
}

pub struct BuiltInConfig {
    pub clipboard_history: bool,
    pub app_launcher: bool,
    pub window_switcher: bool,
}

pub struct SuggestedConfig {
    pub enabled: bool,
    pub max_items: usize,
    pub min_score: f64,
    pub half_life_days: f64,
    pub track_usage: bool,
    pub excluded_commands: Vec<String>,
}

pub struct ProcessLimits {
    pub max_memory_mb: Option<u64>,
    pub max_runtime_seconds: Option<u64>,
    pub health_check_interval_ms: u64,
}

pub struct CommandConfig {
    pub shortcut: Option<HotkeyConfig>,
    pub hidden: Option<bool>,
    pub confirmation_required: Option<bool>,
}
```
