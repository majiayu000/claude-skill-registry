---
name: serde-patterns
description: Serialization patterns with serde and serde_json
---

# serde-patterns

Serde is Rust's framework for **ser**ializing and **de**serializing data structures. Script-kit-gpui uses it extensively for:

- **Config files**: `~/.scriptkit/kit/config.json`, `theme.json`
- **IPC protocol**: JSON messages between SDK and app
- **Script metadata**: Typed metadata in script files
- **Persistence**: Window state, shortcuts, frecency data

## Derive Macros

The most common pattern - derive `Serialize` and `Deserialize`:

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Config {
    pub hotkey: HotkeyConfig,
    pub editor: Option<String>,
}
```

For deserialization only (common for incoming protocol messages):

```rust
#[derive(Debug, Clone, serde::Deserialize)]
#[serde(tag = "type", rename_all = "camelCase")]
pub enum ExternalCommand {
    Run { path: String },
    Show { request_id: Option<String> },
}
```

## Common Attributes

### Field Renaming

```rust
// Rename all fields to camelCase (JavaScript convention)
#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct BuiltInConfig {
    pub clipboard_history: bool,  // serializes as "clipboardHistory"
    pub app_launcher: bool,       // serializes as "appLauncher"
}

// Rename individual field
#[serde(rename = "requestId")]
pub request_id: String,

// Rename for both ser/de or separately
#[serde(rename(serialize = "Foo", deserialize = "foo"))]
```

### Default Values

```rust
// Use Default::default() for missing fields
#[serde(default)]
pub tags: Vec<String>,

// Use a custom function for default
#[serde(default = "default_grid_size")]
pub grid_size: u32,

fn default_grid_size() -> u32 {
    8
}

// Default for nested structs
#[serde(default)]
pub terminal: TerminalColors,  // uses TerminalColors::default()
```

### Skip Serialization

```rust
// Skip if None
#[serde(skip_serializing_if = "Option::is_none")]
pub editor: Option<String>,

// Skip if empty vector
#[serde(default, skip_serializing_if = "Vec::is_empty")]
pub suggestions: Vec<String>,

// Skip always (computed field)
#[serde(skip)]
pub cached_value: Option<i32>,

// Common pattern: default + skip combo
#[serde(default, skip_serializing_if = "Option::is_none")]
pub actions: Option<Vec<ProtocolAction>>,
```

### Tagged Enums

```rust
// Externally tagged (default): {"Run": {"path": "..."}}
#[derive(Deserialize)]
enum Message {
    Run { path: String },
}

// Internally tagged: {"type": "run", "path": "..."}
#[derive(Deserialize)]
#[serde(tag = "type", rename_all = "camelCase")]
enum ExternalCommand {
    Run { path: String },
    Show { request_id: Option<String> },
}

// Custom tag name with rename
#[serde(tag = "type")]
enum Message {
    #[serde(rename = "arg")]
    Arg { id: String, placeholder: String },
    #[serde(rename = "submit")]
    Submit { id: String, value: Option<String> },
}
```

### Flatten

```rust
// Merge fields into parent
#[derive(Serialize, Deserialize)]
struct LayoutInfoResult {
    request_id: String,
    #[serde(flatten)]
    info: LayoutInfo,  // LayoutInfo fields appear at top level
}

// Capture unknown fields
#[derive(Deserialize)]
struct TypedMetadata {
    pub name: Option<String>,
    #[serde(flatten)]
    pub extra: HashMap<String, serde_json::Value>,
}
```

## Usage in script-kit-gpui

### Config Loading (`src/config/types.rs`)

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Config {
    pub hotkey: HotkeyConfig,
    
    #[serde(skip_serializing_if = "Option::is_none")]
    pub bun_path: Option<String>,
    
    #[serde(default, skip_serializing_if = "Option::is_none", rename = "editorFontSize")]
    pub editor_font_size: Option<f32>,
    
    #[serde(default, skip_serializing_if = "Option::is_none", rename = "builtIns")]
    pub built_ins: Option<BuiltInConfig>,
}
```

### IPC Protocol Messages (`src/protocol/message.rs`)

```rust
#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(tag = "type")]
pub enum Message {
    #[serde(rename = "arg")]
    Arg {
        id: String,
        placeholder: String,
        choices: Vec<Choice>,
        #[serde(default, skip_serializing_if = "Option::is_none")]
        actions: Option<Vec<ProtocolAction>>,
    },
    
    #[serde(rename = "div")]
    Div {
        id: String,
        html: String,
        #[serde(rename = "containerClasses", skip_serializing_if = "Option::is_none")]
        container_classes: Option<String>,
        #[serde(rename = "containerPadding", skip_serializing_if = "Option::is_none")]
        container_padding: Option<serde_json::Value>,
    },
}
```

### Theme Colors with Custom Serialization (`src/theme/hex_color.rs`)

```rust
pub type HexColor = u32;

// Custom module for special serialization
pub mod hex_color_serde {
    use super::*;
    use serde::de::{self, Visitor};
    
    pub fn serialize<S>(color: &HexColor, serializer: S) -> Result<S::Ok, S::Error>
    where S: Serializer {
        serializer.serialize_str(&format!("#{:06X}", color))
    }
    
    pub fn deserialize<'de, D>(deserializer: D) -> Result<HexColor, D::Error>
    where D: Deserializer<'de> {
        struct HexColorVisitor;
        
        impl<'de> Visitor<'de> for HexColorVisitor {
            type Value = HexColor;
            
            fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
                formatter.write_str("a number, hex string, or rgba()")
            }
            
            fn visit_u64<E>(self, value: u64) -> Result<HexColor, E> {
                Ok(value as HexColor)
            }
            
            fn visit_str<E>(self, value: &str) -> Result<HexColor, E>
            where E: de::Error {
                parse_color_string(value).map_err(de::Error::custom)
            }
        }
        
        deserializer.deserialize_any(HexColorVisitor)
    }
}

// Usage in structs
#[derive(Serialize, Deserialize)]
pub struct BackgroundColors {
    #[serde(with = "hex_color_serde")]
    pub main: HexColor,  // Accepts: "#1E1E1E", "rgb(30,30,30)", 1973790
}
```

### Script Metadata (`src/metadata_parser.rs`)

```rust
#[derive(Clone, Debug, Default, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "camelCase")]
pub struct TypedMetadata {
    pub name: Option<String>,
    pub description: Option<String>,
    
    #[serde(default)]
    pub tags: Vec<String>,
    
    #[serde(default)]
    pub hidden: bool,
    
    // Capture any extra fields
    #[serde(flatten)]
    pub extra: HashMap<String, serde_json::Value>,
}
```

## Custom Serialization

### Using `serialize_with` / `deserialize_with`

```rust
#[derive(Serialize, Deserialize)]
pub struct DropShadow {
    #[serde(with = "hex_color_serde")]
    pub color: HexColor,
}

// For Option<T> with custom serde
pub mod hex_color_option_serde {
    pub fn serialize<S>(color: &Option<HexColor>, serializer: S) -> Result<S::Ok, S::Error> {
        match color {
            Some(c) => serializer.serialize_str(&format!("#{:06X}", c)),
            None => serializer.serialize_none(),
        }
    }
    
    pub fn deserialize<'de, D>(deserializer: D) -> Result<Option<HexColor>, D::Error> {
        // Custom visitor implementation
    }
}
```

### Implementing Visitor Pattern

```rust
struct HexColorVisitor;

impl<'de> Visitor<'de> for HexColorVisitor {
    type Value = HexColor;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        formatter.write_str("a number, hex string (#RRGGBB), or rgba(r, g, b, a)")
    }

    fn visit_u64<E>(self, value: u64) -> Result<HexColor, E>
    where E: de::Error {
        Ok(value as HexColor)
    }

    fn visit_i64<E>(self, value: i64) -> Result<HexColor, E>
    where E: de::Error {
        Ok(value as HexColor)
    }

    fn visit_str<E>(self, value: &str) -> Result<HexColor, E>
    where E: de::Error {
        parse_color_string(value).map_err(de::Error::custom)
    }
}
```

## Handling Unknown Fields

### Strict Mode (Reject Unknown)

```rust
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
pub struct StrictConfig {
    pub name: String,
}
```

### Capture Unknown Fields

```rust
#[derive(Deserialize)]
pub struct FlexibleConfig {
    pub name: String,
    #[serde(flatten)]
    pub extra: HashMap<String, serde_json::Value>,
}
```

## JSON Patterns

### Parsing JSON

```rust
// From string
let config: Config = serde_json::from_str(&content)?;

// From reader (file)
let config: Config = serde_json::from_reader(file)?;

// From bytes
let config: Config = serde_json::from_slice(&bytes)?;
```

### Serializing to JSON

```rust
// To string
let json = serde_json::to_string(&config)?;

// To pretty string (for config files)
let json = serde_json::to_string_pretty(&config)?;

// To writer
serde_json::to_writer(file, &config)?;

// To Value
let value: serde_json::Value = serde_json::to_value(&config)?;
```

### Working with Dynamic JSON (`serde_json::Value`)

```rust
use serde_json::{json, Value};

// Create JSON dynamically
let value = json!({
    "name": "John Doe",
    "age": 43,
    "phones": ["+44 1234567"]
});

// Access fields
if let Some(name) = value["name"].as_str() {
    println!("Name: {}", name);
}

// Modify
if let Some(obj) = value.as_object_mut() {
    obj.insert("email".to_string(), json!("john@example.com"));
}

// Convert Value to typed struct
let person: Person = serde_json::from_value(value)?;
```

### The `json!` Macro

```rust
use serde_json::json;

// Build complex JSON with interpolation
let name = "Script Kit";
let version = 1;

let metadata = json!({
    "name": name,
    "version": version,
    "features": ["arg", "div", "editor"],
    "config": {
        "enabled": true,
        "timeout": null
    }
});
```

## Anti-patterns

### 1. Missing `#[serde(default)]` for Optional Collections

```rust
// BAD: Fails if "tags" is missing from JSON
pub tags: Vec<String>,

// GOOD: Uses empty vec if missing
#[serde(default)]
pub tags: Vec<String>,
```

### 2. Inconsistent Naming Without `rename_all`

```rust
// BAD: Rust fields don't match JSON camelCase
pub struct Config {
    pub editor_font_size: f32,  // JSON has "editorFontSize"
}

// GOOD: Automatic conversion
#[serde(rename_all = "camelCase")]
pub struct Config {
    pub editor_font_size: f32,
}
```

### 3. Not Using `skip_serializing_if` for Optional Fields

```rust
// BAD: Serializes as {"value": null}
pub value: Option<String>,

// GOOD: Omits field when None
#[serde(skip_serializing_if = "Option::is_none")]
pub value: Option<String>,
```

### 4. Forgetting `#[serde(default)]` with `skip_serializing_if`

```rust
// BAD: Can serialize but not deserialize if field missing
#[serde(skip_serializing_if = "Option::is_none")]
pub value: Option<String>,

// GOOD: Handles both directions
#[serde(default, skip_serializing_if = "Option::is_none")]
pub value: Option<String>,
```

### 5. Using `String` for Enums in JSON

```rust
// BAD: Serializes as string, lossy
pub action: String,  // "copy" or "paste"

// GOOD: Type-safe enum
#[derive(Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ClipboardAction {
    Copy,
    Paste,
    Read,
}
```

### 6. Ignoring Errors in Config Loading

```rust
// BAD: Silent failures
let config = serde_json::from_str(&content).unwrap_or_default();

// GOOD: Log errors, use defaults gracefully
match serde_json::from_str::<Config>(&content) {
    Ok(config) => config,
    Err(e) => {
        tracing::warn!(error = %e, "Failed to parse config, using defaults");
        Config::default()
    }
}
```

## Best Practices

1. **Always derive both `Serialize` and `Deserialize`** unless you only need one direction
2. **Use `#[serde(rename_all = "camelCase")]`** for JavaScript/TypeScript interop
3. **Combine `default` with `skip_serializing_if`** for optional fields
4. **Use custom modules (`with = "...")` for complex types** like colors, dates
5. **Prefer typed enums over strings** for discriminated unions
6. **Use `#[serde(flatten)]`** to capture unknown fields or compose structs
7. **Add `#[serde(default)]`** to `Vec<T>` fields that might be missing
