---
name: rust-error-handling
description: Production error patterns with thiserror and anyhow, including error classification, HTTP/gRPC protocol mappings, context chains, retry logic, and testing. Use when designing error types for libraries or applications, mapping errors to API responses, or implementing retry mechanisms.
---

# Rust Error Handling

*Production error patterns with thiserror, anyhow, and protocol mappings*

## Version Context
- **thiserror**: 2.x (derive Error trait)
- **anyhow**: 1.x (dynamic errors)
- **Standard Library**: Result, Option

## When to Use This Skill

- Designing error types for libraries
- Application-level error handling
- Mapping errors to HTTP/gRPC status codes
- Adding context to error chains
- Implementing retry logic
- Testing error paths

## Library Errors with thiserror

```rust
use thiserror::Error;

/// Domain-specific error type for libraries
#[derive(Debug, Error)]
pub enum UserError {
    #[error("user not found: {id}")]
    NotFound { id: String },

    #[error("invalid email format: {email}")]
    InvalidEmail { email: String },

    #[error("user already exists: {email}")]
    AlreadyExists { email: String },

    #[error("database error")]
    Database(#[from] sqlx::Error),

    #[error("validation failed: {field}")]
    Validation {
        field: String,
        #[source]
        cause: ValidationError,
    },
}

// Usage
async fn find_user(id: &str) -> Result<User, UserError> {
    let user = sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
        .fetch_one(&pool)
        .await?; // Automatically converts sqlx::Error to UserError

    Ok(user)
}
```

## Application Errors with anyhow

```rust
use anyhow::{Context, Result, bail, ensure};

/// Application-level errors with context
async fn process_order(order_id: &str) -> Result<()> {
    let order = fetch_order(order_id)
        .await
        .context("failed to fetch order")?;

    ensure!(order.status == OrderStatus::Pending, "order not in pending state");

    let payment = process_payment(&order)
        .await
        .with_context(|| format!("payment failed for order {}", order_id))?;

    if payment.amount != order.total {
        bail!("payment amount mismatch: expected {}, got {}", order.total, payment.amount);
    }

    Ok(())
}
```

## Error Classification

### Layered Error Architecture

```rust
use thiserror::Error;

/// Infrastructure layer errors
#[derive(Debug, Error)]
pub enum InfraError {
    #[error("database connection failed")]
    DatabaseConnection(#[source] sqlx::Error),

    #[error("cache operation failed")]
    Cache(#[from] redis::RedisError),

    #[error("message queue error")]
    MessageQueue(#[source] Box<dyn std::error::Error + Send + Sync>),
}

/// Domain layer errors
#[derive(Debug, Error)]
pub enum DomainError {
    #[error("business rule violated: {rule}")]
    BusinessRule { rule: String, context: String },

    #[error("entity not found: {entity_type} with id {id}")]
    NotFound { entity_type: String, id: String },

    #[error("duplicate entity: {entity_type}")]
    Duplicate { entity_type: String },
}

/// Application layer errors (combines all layers)
#[derive(Debug, Error)]
pub enum AppError {
    #[error("domain error: {0}")]
    Domain(#[from] DomainError),

    #[error("infrastructure error: {0}")]
    Infrastructure(#[from] InfraError),

    #[error("validation error: {0}")]
    Validation(#[from] validator::ValidationErrors),

    #[error("authentication failed")]
    AuthenticationFailed,

    #[error("authorization failed: insufficient permissions")]
    AuthorizationFailed,
}
```

## Protocol Mappings

### HTTP Status Mapping (Axum)

```rust
use axum::{
    response::{IntoResponse, Response},
    http::StatusCode,
    Json,
};
use serde_json::json;

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, error_type, message) = match self {
            AppError::Domain(DomainError::NotFound { .. }) => {
                (StatusCode::NOT_FOUND, "not_found", self.to_string())
            }
            AppError::Domain(DomainError::Duplicate { .. }) => {
                (StatusCode::CONFLICT, "conflict", self.to_string())
            }
            AppError::Domain(DomainError::BusinessRule { .. }) => {
                (StatusCode::UNPROCESSABLE_ENTITY, "business_rule_violation", self.to_string())
            }
            AppError::Validation(_) => {
                (StatusCode::BAD_REQUEST, "validation_error", self.to_string())
            }
            AppError::AuthenticationFailed => {
                (StatusCode::UNAUTHORIZED, "authentication_failed", "Authentication required".to_string())
            }
            AppError::AuthorizationFailed => {
                (StatusCode::FORBIDDEN, "authorization_failed", "Insufficient permissions".to_string())
            }
            AppError::Infrastructure(_) => {
                (StatusCode::INTERNAL_SERVER_ERROR, "internal_error", "Internal server error".to_string())
            }
        };

        let body = Json(json!({
            "error": {
                "type": error_type,
                "message": message,
            }
        }));

        (status, body).into_response()
    }
}
```

### gRPC Status Mapping (tonic)

```rust
use tonic::{Status, Code};

impl From<AppError> for Status {
    fn from(err: AppError) -> Self {
        match err {
            AppError::Domain(DomainError::NotFound { .. }) => {
                Status::new(Code::NotFound, err.to_string())
            }
            AppError::Domain(DomainError::BusinessRule { .. }) => {
                Status::new(Code::FailedPrecondition, err.to_string())
            }
            AppError::Validation(_) => {
                Status::new(Code::InvalidArgument, err.to_string())
            }
            AppError::AuthenticationFailed => {
                Status::new(Code::Unauthenticated, "Authentication required")
            }
            AppError::AuthorizationFailed => {
                Status::new(Code::PermissionDenied, "Insufficient permissions")
            }
            AppError::Infrastructure(_) => {
                Status::new(Code::Internal, "Internal server error")
            }
            _ => Status::new(Code::Unknown, "Unknown error"),
        }
    }
}
```

## Error Context

### Adding Context with anyhow

```rust
use anyhow::{Context, Result};

async fn load_user_profile(user_id: &str) -> Result<UserProfile> {
    let user = fetch_user(user_id)
        .await
        .context("failed to fetch user")?;

    let profile = fetch_profile(user_id)
        .await
        .with_context(|| format!("failed to fetch profile for user {}", user_id))?;

    let orders = fetch_orders(user_id)
        .await
        .context("failed to fetch user orders")?;

    Ok(UserProfile {
        user,
        profile,
        order_count: orders.len(),
    })
}
```

## Error Patterns

### Early Return with ?

```rust
async fn create_order(request: CreateOrderRequest) -> Result<Order, OrderError> {
    // Validate early
    let customer = find_customer(&request.customer_id).await?;
    let product = find_product(&request.product_id).await?;

    // Business validation
    if product.stock < request.quantity {
        return Err(OrderError::InsufficientStock {
            product_id: request.product_id,
            available: product.stock,
            requested: request.quantity,
        });
    }

    // Create order
    let order = Order::new(customer, product, request.quantity);
    save_order(&order).await?;

    Ok(order)
}
```

### Option to Result Conversion

```rust
async fn get_user_email(user_id: &str) -> Result<String, UserError> {
    let user = find_user(user_id).await?;

    // Convert Option to Result
    user.email.ok_or_else(|| UserError::EmailNotSet {
        user_id: user_id.to_string(),
    })
}
```

## Retry Logic

### Simple Retry with Exponential Backoff

```rust
use tokio::time::{sleep, Duration};

async fn retry_with_backoff<F, Fut, T, E>(
    mut operation: F,
    max_attempts: u32,
) -> Result<T, E>
where
    F: FnMut() -> Fut,
    Fut: Future<Output = Result<T, E>>,
    E: std::fmt::Display,
{
    let mut attempts = 0;
    let base_delay = Duration::from_millis(100);

    loop {
        attempts += 1;

        match operation().await {
            Ok(result) => return Ok(result),
            Err(e) if attempts >= max_attempts => return Err(e),
            Err(e) => {
                let delay = base_delay * 2_u32.pow(attempts - 1);
                eprintln!("Attempt {} failed, waiting {:?}", attempts, delay);
                sleep(delay).await;
            }
        }
    }
}

// Usage
let result = retry_with_backoff(
    || async { fetch_user("user_123").await },
    3,
).await?;
```

## Testing Errors

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_error_conversion() {
        let db_error = sqlx::Error::RowNotFound;
        let user_error: UserError = db_error.into();

        assert!(matches!(user_error, UserError::Database(_)));
    }

    #[tokio::test]
    async fn test_not_found_error() {
        let result = find_user("nonexistent").await;

        assert!(result.is_err());
        assert!(matches!(result.unwrap_err(), UserError::NotFound { .. }));
    }

    #[test]
    fn test_error_display() {
        let error = UserError::InvalidEmail {
            email: "invalid".to_string(),
        };

        assert_eq!(error.to_string(), "invalid email format: invalid");
    }
}
```

## Best Practices

1. **Libraries use thiserror**: Concrete error types with `#[derive(Error)]`
2. **Applications use anyhow**: Dynamic errors with context chains
3. **Classify errors**: Validation, Business Logic, Infrastructure
4. **Map to protocols**: HTTP status codes, gRPC codes
5. **Add context**: Use `.context()` and `.with_context()`
6. **Fail fast**: Validate early, return errors immediately
7. **Don't panic in libraries**: Return `Result` instead
8. **Preserve error chains**: Use `#[source]` and `#[from]`
9. **Test error paths**: Verify error types and messages

## Common Dependencies

```toml
[dependencies]
thiserror = "2"
anyhow = "1"
```
