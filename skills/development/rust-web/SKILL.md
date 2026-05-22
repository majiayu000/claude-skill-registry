---
name: rust-web
description: "Rust Web 开发专家。处理 axum, actix, HTTP, REST, API, 数据库, 状态管理等问题。触发词：web, HTTP, REST, API, axum, actix, handler, database, web开发, 服务器, 路由"
globs: ["**/*.rs"]
---

# Rust Web 开发

## 主流框架选择

| 框架 | 特点 | 推荐场景 |
|-----|------|---------|
| **axum** | 现代、 Tokio 生态、类型安全 | 新项目首选 |
| **actix-web** | 高性能、Actor 模式 | 高性能需求 |
| **rocket** | 开发者友好、零配置 | 快速原型 |

---

## Axum 快速上手

### 基础结构

```rust
use axum::{routing::get, Router};

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", get(root))
        .route("/users", get(list_users).post(create_user))
        .route("/users/:id", get(get_user).delete(delete_user))
        .with_state(pool.clone());

    axum::Server::bind(&"0.0.0.0:3000".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}
```

### Handler 模式

```rust
// 从路径获取参数
async fn get_user(Path(id): Path<u32>) -> Json<User> {
    User::find(id).await
        .map(Json)
        .ok_or_else(|| StatusCode::NOT_FOUND)
}

// 从 JSON body 获取
async fn create_user(Json(user): Json<CreateUserRequest>) -> Result<Json<User>, StatusCode> {
    User::create(user).await
        .map(Json)
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)
}

// 查询参数
async fn list_users(Query(params): Query<ListUsersParams>) -> Json<Vec<User>> {
    User::list(params).await
}
```

### 状态管理

```rust
// AppState 类型
type AppState = Arc<Pool<Postgres>>;

// 提取状态
async fn handler(state: State<AppState>) { ... }

// 共享状态
let pool = PgPoolOptions::new()
    .max_connections(5)
    .connect(&db_url)
    .await?;

let app = Router::new()
    .route("/", get(handler))
    .with_state(Arc::new(pool));
```

---

## 错误处理

```rust
use axum::{
    response::{IntoResponse, Response},
    Json,
};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ApiError {
    #[error("user not found")]
    NotFound,

    #[error("invalid input: {0}")]
    Validation(String),

    #[error("database error")]
    Database(#[from] sqlx::Error),
}

impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        match self {
            ApiError::NotFound => (StatusCode::NOT_FOUND, self.to_string()).into_response(),
            ApiError::Validation(msg) => (StatusCode::BAD_REQUEST, msg).into_response(),
            ApiError::Database(e) => {
                tracing::error!("database error: {}", e);
                (StatusCode::INTERNAL_SERVER_ERROR, "internal error").into_response()
            }
        }
    }
}
```

---

## 中间件模式

```rust
// 记录请求日志
async fn log_requests(req: Request, next: Next) -> Result<Response, Infallible> {
    let start = Instant::now();
    let method = req.method().clone();
    let path = req.uri().path().to_string();

    let response = next.run(req).await;

    tracing::info!(
        "{} {} {} - {:?}",
        method,
        path,
        response.status(),
        start.elapsed()
    );

    Ok(response)
}

// 使用
let app = Router::new()
    .route("/", get(handler))
    .layer(layer_fn(log_requests));
```

---

## 数据库集成

### SQLx 示例

```rust
// 定义模型
#[derive(Debug, FromRow)]
struct User {
    id: i32,
    name: String,
    email: String,
    created_at: chrono::DateTime<Utc>,
}

// 查询
async fn get_user(pool: &Pool<Postgres>, id: i32) -> Result<User, sqlx::Error> {
    sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
        .fetch_one(pool)
        .await
}

// 事务
let mut tx = pool.begin().await?;
sqlx::query!("INSERT INTO ...") .execute(&mut *tx).await?;
tx.commit().await?;
```

---

## Web 开发最佳实践

| 场景 | 推荐做法 |
|-----|---------|
| JSON 序列化 | `#[derive(Serialize, Deserialize)]` + serde |
| 配置管理 | `config` crate + env 文件 |
| 日志 | `tracing` + `tracing-subscriber` |
| 健康检查 | `GET /health` 端点 |
| CORS | `tower_http::cors` |
| 限流 | `tower::limit` |
| OpenAPI | `utoipa` |

---

## 常见错误

| 错误 | 原因 | 解决 |
|-----|-----|-----|
| 状态在 handler 之间共享 | Rc 非线程安全 | 用 `Arc` |
| 异步 handler 持有锁 | 可能死锁 | 缩小锁范围 |
| 错误没传播 | Handler 返回错误 | 实现 `IntoResponse` |
| 大请求体 | 内存压力 | 设置大小限制 |

---

## 项目结构参考

```
src/
├── main.rs           # 入口
├── lib.rs            # 共享代码
├── app.rs            # Router 组装
├── routes/           # 路由定义
│   ├── mod.rs
│   ├── users.rs
│   └── auth.rs
├── models/           # 数据模型
├── services/         # 业务逻辑
├── errors/           # 错误类型
└── middleware/       # 中间件
```

