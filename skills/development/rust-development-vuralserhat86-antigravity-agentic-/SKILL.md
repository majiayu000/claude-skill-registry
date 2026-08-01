---
name: rust-development
description: '> Rust systems programming rehberi.'
---

---
name: rust_development
router_kit: FullStackKit
description: Rust systems programming, memory safety, Axum/Tokio ve WebAssembly rehberi.
metadata:
  skillport:
    category: development
    tags: [automation, aws, bash scripting, ci/cd, cloud computing, containerization, deployment strategies, devops, docker, gitops, infrastructure, infrastructure as code, kubernetes, linux, logging, microservices, monitoring, orchestration, pipelines, reliability, rust development, scalability, security, server management, terraform]      - wasm
---

# 🦀 Rust Development

> Rust systems programming rehberi.

---

## 📋 Temel Syntax

```rust
// Variables
let x = 5;           // Immutable
let mut y = 10;      // Mutable

// Functions
fn add(a: i32, b: i32) -> i32 {
    a + b  // No semicolon = return
}

// Structs
struct User {
    name: String,
    age: u32,
}

// Enums
enum Status {
    Active,
    Inactive,
    Pending(String),
}
```

---

## 🔒 Ownership & Borrowing

```rust
// Ownership
let s1 = String::from("hello");
let s2 = s1;  // s1 moved to s2

// Borrowing
fn print(s: &String) {
    println!("{}", s);
}

// Mutable borrow
fn append(s: &mut String) {
    s.push_str(" world");
}
```

---

## ⚡ Axum Web Framework

```rust
use axum::{routing::get, Router, Json};
use serde::Serialize;

#[derive(Serialize)]
struct User { name: String }

async fn get_user() -> Json<User> {
    Json(User { name: "John".into() })
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/user", get(get_user));

    axum::serve(listener, app).await.unwrap();
}
```

---

## 🔄 Async with Tokio

```rust
use tokio;

#[tokio::main]
async fn main() {
    let result = fetch_data().await;
}

async fn fetch_data() -> String {
    tokio::time::sleep(Duration::from_secs(1)).await;
    "data".to_string()
}
```

---

## 🎯 Error Handling

```rust
use anyhow::Result;
use thiserror::Error;

#[derive(Error, Debug)]
enum AppError {
    #[error("Not found: {0}")]
    NotFound(String),
}

fn find_user(id: &str) -> Result<User> {
    // Returns Result with anyhow
    Ok(user)
}
```

---

*Rust Development v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/) & [Zero To Production in Rust](https://www.zero2prod.com/)

### Aşama 1: Project Setup & Structure
- [ ] **Workspace**: Büyük projeler için Cargo Workspace yapısını kur (Monorepo).
- [ ] **Linter**: `clippy`'yi en sıkı modda (`-D warnings`) çalıştıracak şekilde CI pipeline'ına ekle.
- [ ] **Dependency Management**: `cargo-deny` ile lisans ve güvenlik kontrolü yap.

### Aşama 2: Implementation Patterns
- [ ] **Error Handling**: Kütüphaneler için `thiserror`, uygulamalar için `anyhow` kullan. Asla `unwrap()` kullanma (testler hariç).
- [ ] **Async Runtime**: Web sunucuları için `tokio` ve `axum` (veya `actix-web`) standartını benimse.
- [ ] **Type Safety**: "Newtype Pattern" kullanarak primitive obsession'dan kaçın (`struct UserId(Uuid)`).

### Aşama 3: Performance & Reliability
- [ ] **Tracing**: `tracing` ve `tracing-subscriber` ile structured logging kur. `println!` kullanma.
- [ ] **Benchmarks**: Kritik fonksiyonlar için `criterion` ile benchmark testleri yaz.
- [ ] **Release Profile**: Production build için `Cargo.toml` içinde `lto = true` ve `codegen-units = 1` ayarlarını yap.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | `cargo clippy` hatasız geçiyor mu? ve `cargo fmt` uygulandı mı? |
| 2 | Tüm public API'ler dökümante edildi mi? (`///` doc comments). |
| 3 | Docker imajı `distroless` veya `alpine` tabanlı optimize edildi mi? |
