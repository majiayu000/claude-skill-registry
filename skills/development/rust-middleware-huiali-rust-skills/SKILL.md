---
name: rust-middleware
description: "请求追踪、CORS 配置、限流、中间件模式"
category: infrastructure
triggers: ["middleware", "cors", "rate-limit", "tracing", "中间件", "请求追踪"]
related_skills:
  - rust-web
  - rust-error
  - rust-concurrency
---

# Rust Middleware - 中间件技能

> 本技能提供 Web 中间件的系统化解决方案。

## 核心模式

### 1. 请求追踪中间件

```rust
use actix_web::{
    dev::{forward_ready, Service, ServiceRequest, ServiceResponse, Transform},
    Error, HttpMessage,
};
use futures::future::{ready, LocalBoxFuture, Ready};
use std::rc::Rc;
use uuid::Uuid;

#[derive(Debug, Clone)]
pub struct RequestId(pub String);

pub struct RequestTracking;

impl<S, B> Transform<S, ServiceRequest> for RequestTracking
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error> + 'static,
    S::Future: 'static,
    B: 'static,
{
    type Response = ServiceResponse<B>;
    type Error = Error;
    type InitError = ();
    type Transform = RequestTrackingMiddleware<S>;
    type Future = Ready<Result<Self::Transform, Self::InitError>>;

    fn new_transform(&self, service: S) -> Self::Future {
        ready(Ok(RequestTrackingMiddleware {
            service: Rc::new(service),
        }))
    }
}

pub struct RequestTrackingMiddleware<S> {
    service: Rc<S>,
}

impl<S, B> Service<ServiceRequest> for RequestTrackingMiddleware<S>
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error> + 'static,
    S::Future: 'static,
    B: 'static,
{
    type Response = ServiceResponse<B>;
    type Error = Error;
    type Future = LocalBoxFuture<'static, Result<Self::Response, Self::Error>>;

    forward_ready!(service);

    fn call(&self, req: ServiceRequest) -> Self::Future {
        let service = Rc::clone(&self.service);

        Box::pin(async move {
            let request_id = req
                .headers()
                .get("X-Request-ID")
                .or_else(|| req.headers().get("Request-ID"))
                .and_then(|v| v.to_str().ok())
                .map(|s| s.to_string())
                .unwrap_or_else(|| Uuid::new_v4().to_string());

            req.extensions_mut().insert(RequestId(request_id.clone()));

            let start_time = std::time::Instant::now();
            log::info!("Request: {} {} - ID: {}", req.method(), req.path(), request_id);

            let mut res = service.call(req).await?;

            let duration = start_time.elapsed();
            log::info!("Response: {} - Duration: {:?} - ID: {}", res.status().as_u16(), duration, request_id);

            res.headers_mut().insert(
                actix_web::http::header::HeaderName::from_static("x-request-id"),
                actix_web::http::header::HeaderValue::from_str(&request_id).unwrap(),
            );

            Ok(res)
        })
    }
}
```

### 2. CORS 配置

```rust
use actix_cors::Cors;

pub struct CorsBuilder;

impl CorsBuilder {
    pub fn production() -> Cors {
        Cors::default()
            .allowed_origin_fn(|origin, _req_head| {
                log::debug!("CORS: allowing {:?}", origin);
                true
            })
            .allowed_methods(vec!["OPTIONS", "HEAD", "GET", "POST", "PUT", "PATCH", "DELETE"])
            .allowed_headers(vec![
                actix_web::http::header::AUTHORIZATION,
                actix_web::http::header::ACCEPT,
                actix_web::http::header::CONTENT_TYPE,
            ])
            .expose_headers(vec!["x-request-id"])
            .supports_credentials()
            .max_age(3600)
    }

    pub fn development() -> Cors {
        Cors::default()
            .allow_any_origin()
            .allow_any_method()
            .allow_any_header()
    }

    pub fn api(strict_origins: &[&str]) -> Cors {
        Cors::default()
            .allowed_origins(strict_origins)
            .allowed_methods(vec!["GET", "POST", "PUT", "DELETE", "PATCH"])
            .allowed_headers(vec![
                actix_web::http::header::AUTHORIZATION,
                actix_web::http::header::CONTENT_TYPE,
            ])
            .max_age(86400)
    }
}
```

### 3. 限流中间件

```rust
use actix_web::{dev::{forward_ready, Service, ServiceRequest, ServiceResponse, Transform}, Error, HttpResponse};
use futures::future::{ready, LocalBoxFuture, Ready};
use std::sync::Arc;
use std::time::{Duration, Instant};
use tokio::sync::RwLock;

#[derive(Debug, Clone)]
pub struct RateLimitConfig {
    pub requests_per_second: u64,
    pub window_seconds: u64,
    pub whitelist: Vec<String>,
}

struct SlidingWindow {
    count: u64,
    window_start: Instant,
}

pub struct RateLimiting {
    config: RateLimitConfig,
    counters: Arc<RwLock<Vec<(String, SlidingWindow)>>>,
}

impl<S, B> Transform<S, ServiceRequest> for RateLimiting
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error> + 'static,
    S::Future: 'static,
    B: 'static,
{
    type Response = ServiceResponse<B>;
    type Error = Error;
    type InitError = ();
    type Transform = RateLimitingMiddleware<S>;
    type Future = Ready<Result<Self::Transform, Self::InitError>>;

    fn new_transform(&self, service: S) -> Self::Future {
        ready(Ok(RateLimitingMiddleware {
            service,
            config: self.config.clone(),
            counters: self.counters.clone(),
        }))
    }
}

pub struct RateLimitingMiddleware<S> {
    service: S,
    config: RateLimitConfig,
    counters: Arc<RwLock<Vec<(String, SlidingWindow)>>>,
}

impl<S, B> Service<ServiceRequest> for RateLimitingMiddleware<S>
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error> + 'static,
    S::Future: 'static,
    B: 'static,
{
    type Response = ServiceResponse<B>;
    type Error = Error;
    type Future = LocalBoxFuture<'static, Result<Self::Response, Self::Error>>;

    forward_ready!(service);

    fn call(&self, req: ServiceRequest) -> Self::Future {
        let client_ip = req
            .connection_info()
            .peer_addr()
            .map(|s| s.to_string())
            .unwrap_or_else(|| "unknown".to_string());

        if self.config.whitelist.contains(&client_ip) {
            return Box::pin(self.service.call(req));
        }

        if self.is_rate_limited(&client_ip) {
            let response = HttpResponse::TooManyRequests()
                .json(serde_json::json!({"error": "RATE_LIMIT_EXCEEDED", "message": "Too many requests"}));
            return Box::pin(async { Ok(response.into()) });
        }

        Box::pin(self.service.call(req))
    }
}

impl RateLimiting {
    pub fn new(config: RateLimitConfig) -> Self {
        Self { config, counters: Arc::new(RwLock::new(Vec::new())) }
    }

    fn is_rate_limited(&self, key: &str) -> bool {
        let mut counters = self.counters.write();
        let now = Instant::now();

        counters.retain(|(_, w)| now.duration_since(w.window_start) < Duration::from_secs(self.config.window_seconds));

        if let Some((_, window)) = counters.iter_mut().find(|(k, _)| k == key) {
            if now.duration_since(window.window_start) < Duration::from_secs(self.config.window_seconds) {
                window.count += 1;
                return window.count > self.config.requests_per_second;
            }
            window.count = 1;
            window.window_start = now;
            return false;
        }

        counters.push((key.to_string(), SlidingWindow { count: 1, window_start: now }));
        false
    }
}
```

---

## 常见问题

| 问题 | 原因 | 解决 |
|-----|------|-----|
| CORS 失败 | Origin 配置 | 检查 `allowed_origin_fn` |
| 限流误伤 | 内存计数 | 生产环境用 Redis |

---

## 关联技能

- `rust-web` - Web 框架集成
- `rust-auth` - 认证中间件
