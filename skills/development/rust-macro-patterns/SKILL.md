---
name: rust-macro-patterns
description: Rust macro development patterns including procedural macros, derive macros, attribute macros, and declarative macros. Use when implementing code generation, custom derives, attribute syntax, or compile-time metaprogramming. Trigger phrases include "derive macro", "proc macro", "attribute macro", "macro_rules", "quote!", "syn", or "TokenStream".
---

# Rust Macro Patterns

## Overview

Rust macros enable compile-time code generation through two primary systems: **declarative macros** (`macro_rules!`) and **procedural macros** (derive, attribute, function-like). This skill covers canonical patterns, when to use macros vs generics, and integration with Tauri/Effect-RS ecosystems.

**Key capabilities:**
- Code generation without runtime overhead
- Custom derive implementations for traits
- Attribute-based syntax extensions
- Compile-time validation and error handling

## Canonical Sources

**Rust Language:**
- `std::macro` — Standard library macros
- `proc_macro` crate — Procedural macro infrastructure
- `syn` crate — Rust AST parsing (https://docs.rs/syn)
- `quote` crate — Token stream generation (https://docs.rs/quote)

**TMNL Ecosystem:**
- `submodules/frida-rust/` — Real-world macro usage examples
- `src-ava/` — AVA domain macros (thiserror, serde derives)
- Tauri command macros — `#[tauri::command]`

## Pattern 1: Declarative Macros (macro_rules!)

**Use when:** Simple pattern-based code generation, no AST introspection needed.

### Basic Pattern Matching

```rust
macro_rules! vec_of_strings {
    ($($x:expr),* $(,)?) => {
        vec![$($x.to_string()),*]
    };
}

// Usage
let names = vec_of_strings!["Alice", "Bob", "Charlie"];
```

**Key Features:**
- `$()` — Repetition group
- `*` — Zero or more repetitions
- `+` — One or more repetitions
- `?` — Optional element
- `$(,)?` — Optional trailing comma

### Internal Rules Pattern

```rust
macro_rules! hash_map {
    // Base case: empty
    (@single $($x:tt)*) => (());

    // Recursive case: key-value pairs
    (@count $($rest:expr),*) => (<[()]>::len(&[$(hash_map!(@single $rest)),*]));

    // Public interface
    ($($key:expr => $value:expr),* $(,)?) => {{
        let _cap = hash_map!(@count $($key),*);
        let mut _map = std::collections::HashMap::with_capacity(_cap);
        $(
            _map.insert($key, $value);
        )*
        _map
    }};
}

// Usage
let config = hash_map! {
    "host" => "localhost",
    "port" => "8080",
};
```

**Pattern:** Use `@internal` rules for helper logic, public rules for API.

### Hygiene and Variable Capture

```rust
macro_rules! log_expr {
    ($e:expr) => {{
        let result = $e;  // Hygienic: doesn't capture outer `result`
        println!("{} = {:?}", stringify!($e), result);
        result
    }};
}
```

**Anti-Pattern:**
```rust
// WRONG: Variable capture issues
macro_rules! bad_swap {
    ($a:expr, $b:expr) => {
        let temp = $a;  // Captures outer `temp` if it exists
        $a = $b;
        $b = temp;
    };
}
```

## Pattern 2: Derive Macros

**Use when:** Auto-implementing traits based on struct/enum shape.

### Basic Derive Macro Structure

```rust
// In Cargo.toml:
// [lib]
// proc-macro = true
//
// [dependencies]
// syn = { version = "2.0", features = ["full"] }
// quote = "1.0"
// proc-macro2 = "1.0"

use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, DeriveInput};

#[proc_macro_derive(Builder)]
pub fn derive_builder(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    let name = &input.ident;
    let builder_name = format!("{}Builder", name);
    let builder_ident = syn::Ident::new(&builder_name, name.span());

    // Extract fields from struct
    let fields = match &input.data {
        syn::Data::Struct(data) => match &data.fields {
            syn::Fields::Named(fields) => &fields.named,
            _ => panic!("Builder only supports named fields"),
        },
        _ => panic!("Builder only supports structs"),
    };

    // Generate builder fields (all Option<T>)
    let builder_fields = fields.iter().map(|f| {
        let name = &f.ident;
        let ty = &f.ty;
        quote! { #name: Option<#ty> }
    });

    // Generate setter methods
    let setters = fields.iter().map(|f| {
        let name = &f.ident;
        let ty = &f.ty;
        quote! {
            pub fn #name(mut self, #name: #ty) -> Self {
                self.#name = Some(#name);
                self
            }
        }
    });

    // Generate build method
    let build_fields = fields.iter().map(|f| {
        let name = &f.ident;
        quote! {
            #name: self.#name.ok_or(concat!("Field ", stringify!(#name), " not set"))?
        }
    });

    let expanded = quote! {
        impl #name {
            pub fn builder() -> #builder_ident {
                #builder_ident::default()
            }
        }

        #[derive(Default)]
        pub struct #builder_ident {
            #(#builder_fields),*
        }

        impl #builder_ident {
            #(#setters)*

            pub fn build(self) -> Result<#name, &'static str> {
                Ok(#name {
                    #(#build_fields),*
                })
            }
        }
    };

    TokenStream::from(expanded)
}
```

**Usage:**
```rust
#[derive(Builder)]
struct User {
    name: String,
    age: u32,
    email: String,
}

// Generated API:
let user = User::builder()
    .name("Alice".to_string())
    .age(30)
    .email("alice@example.com".to_string())
    .build()?;
```

### Advanced: Derive with Attributes

```rust
#[proc_macro_derive(Validate, attributes(validate))]
pub fn derive_validate(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);

    let fields = match &input.data {
        syn::Data::Struct(data) => match &data.fields {
            syn::Fields::Named(fields) => &fields.named,
            _ => panic!("Validate only supports named fields"),
        },
        _ => panic!("Validate only supports structs"),
    };

    // Parse attributes
    let validations = fields.iter().map(|f| {
        let name = &f.ident;
        let ty = &f.ty;

        // Look for #[validate(...)] attributes
        let attrs = f.attrs.iter()
            .filter(|attr| attr.path().is_ident("validate"))
            .collect::<Vec<_>>();

        if attrs.is_empty() {
            quote! {}
        } else {
            quote! {
                if self.#name.is_empty() {
                    return Err(concat!("Field ", stringify!(#name), " cannot be empty"));
                }
            }
        }
    });

    let name = &input.ident;
    let expanded = quote! {
        impl #name {
            pub fn validate(&self) -> Result<(), &'static str> {
                #(#validations)*
                Ok(())
            }
        }
    };

    TokenStream::from(expanded)
}
```

**Usage:**
```rust
#[derive(Validate)]
struct FormData {
    #[validate]
    username: String,

    #[validate]
    email: String,

    age: u32,  // No validation
}
```

## Pattern 3: Attribute Macros

**Use when:** Transforming or augmenting function/struct definitions with custom syntax.

### Function Attribute (Tauri Command Pattern)

```rust
#[proc_macro_attribute]
pub fn timed(attr: TokenStream, item: TokenStream) -> TokenStream {
    let input = parse_macro_input!(item as syn::ItemFn);
    let name = &input.sig.ident;
    let inputs = &input.sig.inputs;
    let output = &input.sig.output;
    let block = &input.block;
    let vis = &input.vis;

    let expanded = quote! {
        #vis fn #name(#inputs) #output {
            let _start = std::time::Instant::now();
            let _result = (|| #block)();
            println!("{} took {:?}", stringify!(#name), _start.elapsed());
            _result
        }
    };

    TokenStream::from(expanded)
}
```

**Usage:**
```rust
#[timed]
fn expensive_computation(n: u64) -> u64 {
    (0..n).sum()
}
```

### Struct Attribute (Configuration Pattern)

```rust
#[proc_macro_attribute]
pub fn config(attr: TokenStream, item: TokenStream) -> TokenStream {
    let input = parse_macro_input!(item as syn::ItemStruct);
    let name = &input.ident;

    // Parse attribute args
    let attr_args = parse_macro_input!(attr as syn::AttributeArgs);
    let prefix = attr_args.iter()
        .find_map(|arg| {
            if let syn::NestedMeta::Meta(syn::Meta::NameValue(nv)) = arg {
                if nv.path.is_ident("prefix") {
                    if let syn::Lit::Str(s) = &nv.lit {
                        return Some(s.value());
                    }
                }
            }
            None
        })
        .unwrap_or_else(|| name.to_string().to_uppercase());

    // Generate config loading logic
    let expanded = quote! {
        #input

        impl #name {
            pub fn from_env() -> Result<Self, envy::Error> {
                envy::prefixed(concat!(#prefix, "_")).from_env()
            }
        }
    };

    TokenStream::from(expanded)
}
```

**Usage:**
```rust
#[config(prefix = "APP")]
#[derive(serde::Deserialize)]
struct AppConfig {
    host: String,
    port: u16,
}

// Reads APP_HOST and APP_PORT from environment
let config = AppConfig::from_env()?;
```

## Pattern 4: Function-Like Macros

**Use when:** Custom DSL syntax that doesn't fit declarative or attribute patterns.

```rust
#[proc_macro]
pub fn sql(input: TokenStream) -> TokenStream {
    let input_str = input.to_string();

    // Parse SQL at compile time
    if !input_str.contains("SELECT") && !input_str.contains("INSERT") {
        panic!("Invalid SQL: must contain SELECT or INSERT");
    }

    // Generate safe query struct
    let expanded = quote! {
        {
            const QUERY: &str = #input_str;
            sqlx::query(QUERY)
        }
    };

    TokenStream::from(expanded)
}
```

**Usage:**
```rust
let users = sql!("SELECT * FROM users WHERE age > ?")
    .bind(18)
    .fetch_all(&pool)
    .await?;
```

## When to Use Macros vs Generics

### Decision Tree

```
Need compile-time logic?
│
├─ Type-based dispatch?
│  ├─ Single implementation per type?
│  │  └─ Use: Generic function/trait
│  │
│  └─ Multiple implementations?
│     └─ Use: Trait + impl blocks
│
├─ Code generation based on structure?
│  ├─ Trait implementation?
│  │  └─ Use: Derive macro
│  │
│  ├─ Function transformation?
│  │  └─ Use: Attribute macro
│  │
│  └─ Custom syntax?
│     └─ Use: Function-like macro
│
└─ Pattern matching on syntax?
   └─ Use: macro_rules!
```

### Prefer Generics When:

```rust
// GOOD: Generic function
fn print_debug<T: Debug>(value: &T) {
    println!("{:?}", value);
}

// AVOID: Macro for simple type dispatch
macro_rules! print_debug {
    ($value:expr) => {
        println!("{:?}", $value);
    };
}
```

### Prefer Macros When:

```rust
// GOOD: Compile-time validation impossible with generics
#[derive(Validate)]
struct User {
    #[validate(email)]
    email: String,
}

// GOOD: Syntax transformation
#[tauri::command]
async fn greet(name: String) -> String {
    format!("Hello, {}!", name)
}
```

## Tauri Integration Patterns

### Command Macro Usage

```rust
// Tauri's #[tauri::command] is an attribute macro
#[tauri::command]
async fn read_file(path: String) -> Result<String, String> {
    tokio::fs::read_to_string(path)
        .await
        .map_err(|e| e.to_string())
}

// Register in main.rs
fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![read_file])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**Pattern:** Transforms async fn into IPC-callable command with automatic serialization.

### State Management with Macros

```rust
use tauri::State;
use std::sync::Mutex;

struct AppState {
    counter: Mutex<i32>,
}

#[tauri::command]
fn increment(state: State<AppState>) -> i32 {
    let mut counter = state.counter.lock().unwrap();
    *counter += 1;
    *counter
}

// In main.rs
fn main() {
    tauri::Builder::default()
        .manage(AppState {
            counter: Mutex::new(0),
        })
        .invoke_handler(tauri::generate_handler![increment])
        .run(tauri::generate_context!())
        .expect("error");
}
```

## Error Handling in Macros

### Compile-Time Errors

```rust
#[proc_macro_derive(MyMacro)]
pub fn my_macro(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);

    // Use compile_error! for better error messages
    match &input.data {
        syn::Data::Struct(_) => { /* ok */ },
        _ => {
            return quote! {
                compile_error!("MyMacro only supports structs");
            }.into();
        }
    }

    // ... rest of macro
}
```

### Span-Based Errors

```rust
use syn::spanned::Spanned;

#[proc_macro_derive(Validated)]
pub fn validated(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);

    let fields = match &input.data {
        syn::Data::Struct(data) => &data.fields,
        other => {
            return syn::Error::new(
                other.span(),
                "Validated only works on structs"
            )
            .to_compile_error()
            .into();
        }
    };

    // ... validation logic
}
```

## Testing Macros

### Declarative Macro Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vec_of_strings() {
        let result = vec_of_strings!["a", "b", "c"];
        assert_eq!(result, vec!["a", "b", "c"]);
    }
}
```

### Procedural Macro Tests (trybuild)

```toml
# Cargo.toml
[dev-dependencies]
trybuild = "1.0"
```

```rust
// tests/compile_fail.rs
#[test]
fn ui() {
    let t = trybuild::TestCases::new();
    t.pass("tests/ui/pass/*.rs");
    t.compile_fail("tests/ui/fail/*.rs");
}
```

```rust
// tests/ui/fail/invalid_struct.rs
use my_macro::Builder;

#[derive(Builder)]
enum NotAStruct {
    Variant,
}
// Expected error: Builder only supports structs

fn main() {}
```

## Anti-Patterns

### 1. Macro for Simple Abstraction

**WRONG:**
```rust
macro_rules! add {
    ($a:expr, $b:expr) => {
        $a + $b
    };
}
```

**RIGHT:**
```rust
#[inline]
fn add<T: Add<Output = T>>(a: T, b: T) -> T {
    a + b
}
```

### 2. Over-Complex Declarative Macros

**WRONG:**
```rust
macro_rules! monster {
    // 50 lines of nested pattern matching
    (@internal $($tt:tt)*) => { /* ... */ };
    // ...
}
```

**RIGHT:** Use procedural macro for complex logic with syn/quote.

### 3. Ignoring Hygiene

**WRONG:**
```rust
macro_rules! unsafe_log {
    ($msg:expr) => {
        println!("{}", msg);  // Captures outer `msg` variable
    };
}
```

**RIGHT:**
```rust
macro_rules! safe_log {
    ($msg:expr) => {{
        let __msg = $msg;
        println!("{}", __msg);
    }};
}
```

### 4. Procedural Macro Without Error Handling

**WRONG:**
```rust
#[proc_macro_derive(Bad)]
pub fn bad(input: TokenStream) -> TokenStream {
    let input = syn::parse(input).unwrap();  // Panics on parse error
    // ...
}
```

**RIGHT:**
```rust
#[proc_macro_derive(Good)]
pub fn good(input: TokenStream) -> TokenStream {
    let input = match syn::parse(input) {
        Ok(input) => input,
        Err(e) => return e.to_compile_error().into(),
    };
    // ...
}
```

## Quick Reference

### Common Macro Fragments

| Fragment | Matches | Example |
|----------|---------|---------|
| `expr` | Expression | `x + 1`, `foo()` |
| `ident` | Identifier | `my_var`, `Type` |
| `ty` | Type | `String`, `Vec<T>` |
| `path` | Path | `std::vec::Vec` |
| `stmt` | Statement | `let x = 5;` |
| `block` | Block | `{ ... }` |
| `item` | Item | `fn foo() {}` |
| `tt` | Token tree | Any single token |

### Repetition Operators

| Op | Meaning |
|----|---------|
| `*` | Zero or more |
| `+` | One or more |
| `?` | Zero or one |

### Dependencies for Proc Macros

```toml
[lib]
proc-macro = true

[dependencies]
syn = { version = "2.0", features = ["full"] }
quote = "1.0"
proc-macro2 = "1.0"
```

## TMNL Integration

When building Tauri commands or Rust-based MCP servers:

1. Use `#[tauri::command]` for IPC handlers
2. Use `#[derive(serde::Serialize, serde::Deserialize)]` for DTO types
3. Use `thiserror` derive macros for error types (see rust-effect-patterns skill)
4. Prefer attribute macros over function-like macros for DSLs
5. Test macro expansion with `cargo expand` during development

## Further Reading

- **The Rust Book**: [Macros](https://doc.rust-lang.org/book/ch19-06-macros.html)
- **syn docs**: https://docs.rs/syn
- **quote docs**: https://docs.rs/quote
- **proc-macro-workshop**: https://github.com/dtolnay/proc-macro-workshop
- **Tauri command docs**: https://tauri.app/v1/guides/features/command
