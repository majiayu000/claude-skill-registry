---
name: script-kit-scripts
description: Script Kit scripts and scriptlets module architecture. Covers script loading from ~/.scriptkit/kit/*/scripts/, scriptlet parsing from markdown files in extensions/, scriptlet caching with change detection, metadata extraction (comments and codefence JSON), fuzzy search, result grouping, and scheduling. Use when working with Script, Scriptlet, ScriptletCache types, or any scripts/ module code.
---

# Script Kit Scripts Module

## Architecture Overview

```
src/
├── scripts/                    # Main scripts module
│   ├── mod.rs                  # Module exports and re-exports
│   ├── types.rs                # Core types: Script, Scriptlet, SearchResult
│   ├── loader.rs               # Script loading from filesystem
│   ├── scriptlet_loader.rs     # Scriptlet loading and parsing
│   ├── metadata.rs             # Metadata extraction from comments
│   ├── search.rs               # Fuzzy search with nucleo
│   ├── grouping.rs             # SUGGESTED/MAIN result grouping
│   ├── scheduling.rs           # Cron/schedule registration
│   └── input_detection.rs      # URL/path/math/code detection
├── scriptlets.rs               # Markdown scriptlet parser
├── scriptlet_cache.rs          # Per-file caching with diff detection
└── scriptlet_metadata.rs       # Codefence metadata/schema parser
```

## Core Types

### Script (`scripts/types.rs`)
```rust
pub struct Script {
    pub name: String,
    pub path: PathBuf,
    pub extension: String,                    // "ts" or "js"
    pub description: Option<String>,
    pub icon: Option<String>,
    pub alias: Option<String>,                // Quick trigger (e.g., "gc")
    pub shortcut: Option<String>,             // Keyboard shortcut
    pub typed_metadata: Option<TypedMetadata>, // From `metadata = {...}`
    pub schema: Option<Schema>,               // From `schema = {...}`
}
```

### Scriptlet (`scripts/types.rs`)
```rust
pub struct Scriptlet {
    pub name: String,
    pub description: Option<String>,
    pub code: String,
    pub tool: String,                 // "ts", "bash", "paste", etc.
    pub shortcut: Option<String>,
    pub expand: Option<String>,       // Text expansion trigger
    pub group: Option<String>,        // H1 header group name
    pub file_path: Option<String>,    // "/path/to/file.md#slug"
    pub command: Option<String>,      // Kebab-case slug
    pub alias: Option<String>,
}
```

### SearchResult (`scripts/types.rs`)
```rust
pub enum SearchResult {
    Script(ScriptMatch),
    Scriptlet(ScriptletMatch),
    BuiltIn(BuiltInMatch),
    App(AppMatch),
    Window(WindowMatch),
    Agent(AgentMatch),
    Fallback(FallbackMatch),
}
```

## Script Loading

### Loading Scripts (`scripts/loader.rs`)
```rust
// Glob pattern: ~/.scriptkit/kit/*/scripts/*.{ts,js}
pub fn read_scripts() -> Vec<Arc<Script>>

// Extracts metadata from file, returns Arc<Script> for cheap cloning
```

### Loading Scriptlets (`scripts/scriptlet_loader.rs`)
```rust
// Primary entry point - uses comprehensive parser
pub fn load_scriptlets() -> Vec<Arc<Scriptlet>>

// Load from specific file (for incremental updates)
pub fn read_scriptlets_from_file(path: &Path) -> Vec<Arc<Scriptlet>>

// Glob pattern: ~/.scriptkit/kit/*/extensions/*.md
```

## Scriptlet Parsing (`scriptlets.rs`)

### Markdown Format
```markdown
---
name: My Bundle
icon: Star
---

# Group Name

```ts
// Global prepend code for all scriptlets in group
```

## Scriptlet Name

<!-- shortcut: cmd shift k
     description: My description
     expand: snip,, -->

```ts
const result = await arg("Pick one");
```
```

### Key Functions
```rust
// Main parser - returns Vec<Scriptlet>
pub fn parse_markdown_as_scriptlets(content: &str, source_path: Option<&str>) -> Vec<Scriptlet>

// With validation - returns valid scriptlets + errors
pub fn parse_scriptlets_with_validation(content: &str, source_path: Option<&str>) -> ScriptletParseResult

// Variable substitution
pub fn format_scriptlet(content: &str, inputs: &HashMap<String, String>, positional_args: &[String], windows: bool) -> String

// Conditional processing: {{#if flag}}...{{else}}...{{/if}}
pub fn process_conditionals(content: &str, flags: &HashMap<String, bool>) -> String
```

### Valid Tool Types
```rust
pub const VALID_TOOLS: &[&str] = &[
    "bash", "python", "kit", "ts", "js", "transform", "template",
    "open", "edit", "paste", "type", "submit", "applescript",
    "ruby", "perl", "php", "node", "deno", "bun",
    "zsh", "sh", "fish", "cmd", "powershell", "pwsh",
];
```

## Codefence Metadata (`scriptlet_metadata.rs`)

### New Format (JSON in codefences)
````markdown
## Scriptlet Name

```metadata
{ "name": "Quick Todo", "description": "Add a todo item", "icon": "CheckSquare" }
```

```schema
{ "input": { "item": { "type": "string", "required": true } } }
```

```ts
const { item } = await input();
```
````

### Parser
```rust
pub fn parse_codefence_metadata(content: &str) -> CodefenceParseResult

pub struct CodefenceParseResult {
    pub metadata: Option<TypedMetadata>,
    pub schema: Option<Schema>,
    pub code: Option<CodeBlock>,
    pub errors: Vec<String>,
}
```

## Scriptlet Caching (`scriptlet_cache.rs`)

### Cache Structure
```rust
pub struct ScriptletCache {
    files: HashMap<PathBuf, CachedScriptletFile>,
}

pub struct CachedScriptletFile {
    pub path: PathBuf,
    pub mtime: SystemTime,
    pub fingerprint: Option<FileFingerprint>,  // mtime + size
    pub scriptlets: Vec<CachedScriptlet>,
}

pub struct CachedScriptlet {
    pub name: String,
    pub shortcut: Option<String>,
    pub expand: Option<String>,
    pub alias: Option<String>,
    pub file_path: String,  // "/path/to/file.md#slug"
}
```

### Change Detection
```rust
// Atomic upsert with diff
pub fn upsert_file(&mut self, path: PathBuf, fingerprint: FileFingerprint, scriptlets: Vec<CachedScriptlet>) -> ScriptletDiff

pub struct ScriptletDiff {
    pub added: Vec<CachedScriptlet>,
    pub removed: Vec<CachedScriptlet>,
    pub shortcut_changes: Vec<ShortcutChange>,
    pub expand_changes: Vec<ExpandChange>,
    pub alias_changes: Vec<AliasChange>,
    pub file_path_changes: Vec<FilePathChange>,
}

// Compute diff between old and new scriptlets
pub fn diff_scriptlets(old: &[CachedScriptlet], new: &[CachedScriptlet]) -> ScriptletDiff
```

### Usage Pattern
```rust
let mut cache = ScriptletCache::new();
let fingerprint = FileFingerprint::from_path(&path)?;

if cache.is_stale_fingerprint(&path, fingerprint) {
    let content = fs::read_to_string(&path)?;
    let result = load_scriptlets_with_validation(&content, &path);
    
    // Convert to cached format
    let cached: Vec<CachedScriptlet> = result.scriptlets.iter()
        .map(|s| scriptlet_to_cached(s, &path))
        .collect();
    
    // Atomic upsert returns diff for hotkey registration updates
    let diff = cache.upsert_file(path, fingerprint, cached);
    
    // Apply diff to hotkey/expand managers...
}
```

## Fuzzy Search (`scripts/search.rs`)

### Nucleo-based Scoring
```rust
// Context for reusing allocations across searches
struct NucleoCtx {
    pattern: Pattern,
    matcher: Matcher,
    buf: Vec<char>,
}

// Search functions (all return sorted by score desc)
pub fn fuzzy_search_scripts(scripts: &[Arc<Script>], query: &str) -> Vec<ScriptMatch>
pub fn fuzzy_search_scriptlets(scriptlets: &[Arc<Scriptlet>], query: &str) -> Vec<ScriptletMatch>
pub fn fuzzy_search_builtins(entries: &[BuiltInEntry], query: &str) -> Vec<BuiltInMatch>
pub fn fuzzy_search_apps(apps: &[AppInfo], query: &str) -> Vec<AppMatch>
pub fn fuzzy_search_windows(windows: &[WindowInfo], query: &str) -> Vec<WindowMatch>

// Unified search across all types
pub fn fuzzy_search_unified_all(scripts, scriptlets, builtins, apps, query) -> Vec<SearchResult>
```

### Score Weights
| Match Type | Points |
|------------|--------|
| Name prefix match | 100 |
| Name substring | 75 |
| Name fuzzy (nucleo) | 50 + scaled |
| Filename prefix | 60 |
| Filename substring | 45 |
| Description match | 25 |
| Path match | 10 |
| Code match (4+ chars) | 5 |

## Result Grouping (`scripts/grouping.rs`, `list_item.rs`)

### Grouped View (empty filter)
```rust
// Function in scripts/grouping.rs
pub fn get_grouped_results(...) -> (Vec<GroupedListItem>, Vec<SearchResult>)

// Type definition in list_item.rs
pub enum GroupedListItem {
    SectionHeader(String),  // "SUGGESTED", "SCRIPTS", etc.
    Item(usize),            // Index into results vec
}
```

**Sections**: SUGGESTED (frecency-based), SCRIPTS, SCRIPTLETS, COMMANDS, APPS, AGENTS

### Search Mode (non-empty filter)
- Flat list of matching items
- Menu bar actions section (limited to 5, min score 25)
- Fallback commands section ("Use {query} with...")

## Scheduling (`scripts/scheduling.rs`)

```rust
// Scan scripts with // Cron: or // Schedule: metadata
pub fn register_scheduled_scripts(scheduler: &Scheduler) -> usize
```

## Metadata Extraction (`scripts/metadata.rs`)

### Comment-based (Legacy)
```typescript
// Name: My Script
// Description: Does something
// Icon: Terminal
// Alias: ms
// Shortcut: cmd shift m
// Cron: */5 * * * *
// Schedule: every tuesday at 2pm
```

### Typed Metadata (New)
```typescript
metadata = {
    name: "My Script",
    description: "Does something",
    enter: "Run Script",
    fallback: true,
    fallback_label: "Search {input}"
}

schema = {
    input: { query: { type: "string", required: true } },
    output: { result: { type: "string" } }
}
```

## Input Detection (`scripts/input_detection.rs`)

```rust
pub enum InputType { Url, FilePath, MathExpression, CodeSnippet, PlainText }

pub fn detect_input_type(input: &str) -> InputType
pub fn is_url(input: &str) -> bool       // http://, https://, file://
pub fn is_file_path(input: &str) -> bool // /, ~/, ./, C:\
pub fn is_math_expression(input: &str) -> bool // 2+2, (10+5)/3
pub fn is_code_snippet(input: &str) -> bool // function, const, =>
```

## Performance Optimizations

1. **Arc wrapping** - `Arc<Script>`, `Arc<Scriptlet>` for cheap clones during filtering
2. **Nucleo context reuse** - Single allocation for pattern matching
3. **ASCII fast-path** - Byte-level comparison for ASCII strings
4. **Lazy match indices** - Only computed for visible rows
5. **Fingerprint caching** - mtime + size for robust staleness detection
6. **Truncated code search** - Only search code for queries 4+ chars when no other matches
