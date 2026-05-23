---
name: rust-macros
description: Master Rust macros - declarative and procedural macros
sasmp_version: "1.3.0"
bonded_agent: rust-type-system-agent
bond_type: SECONDARY_BOND
version: "1.0.0"
---

# Rust Macros Skill

Master Rust's macro system: declarative macros (macro_rules!) and procedural macros.

## Quick Start

### Declarative Macros

```rust
macro_rules! vec_of_strings {
    ($($x:expr),* $(,)?) => {
        vec![$($x.to_string()),*]
    };
}

let v = vec_of_strings!["a", "b", "c"];
```

### Fragment Specifiers

| Specifier | Matches |
|-----------|---------|
| `ident` | Identifier |
| `expr` | Expression |
| `ty` | Type |
| `pat` | Pattern |
| `tt` | Token tree |
| `literal` | Literal |

### Repetition

```rust
macro_rules! hashmap {
    ($($key:expr => $value:expr),* $(,)?) => {{
        let mut map = std::collections::HashMap::new();
        $(map.insert($key, $value);)*
        map
    }};
}

let m = hashmap! { "one" => 1, "two" => 2 };
```

## Procedural Macros

```toml
[lib]
proc-macro = true

[dependencies]
syn = { version = "2", features = ["full"] }
quote = "1"
```

### Derive Macro

```rust
use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, DeriveInput};

#[proc_macro_derive(HelloMacro)]
pub fn hello_derive(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    let name = input.ident;

    quote! {
        impl HelloMacro for #name {
            fn hello() {
                println!("Hello from {}!", stringify!(#name));
            }
        }
    }.into()
}
```

## Debugging

```bash
cargo expand              # Expand all macros
cargo expand main         # Expand specific
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Hygiene issues | Use `$crate::` |
| Order matters | Define before use |

## Resources

- [The Little Book of Rust Macros](https://veykril.github.io/tlborm/)
- [syn docs](https://docs.rs/syn)
