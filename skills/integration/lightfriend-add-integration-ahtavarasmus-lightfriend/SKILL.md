---
name: lightfriend-add-integration
description: Step-by-step guide for adding new OAuth integrations to Lightfriend
---

# Adding a New OAuth Integration

This skill guides you through adding a new OAuth service integration (e.g., Google Calendar, Spotify, GitHub) to Lightfriend.

## Overview

A complete integration includes:
- Backend OAuth flow (authorization + callback)
- Database migration for storing encrypted tokens
- Repository methods for token management
- Frontend UI for connection management
- Protected API endpoints for using the integration

## Step-by-Step Process

### 1. Create Database Migration

First, create a table to store the OAuth credentials:

```bash
cd backend && diesel migration generate add_{service}_connection
```

Edit `up.sql`:
```sql
CREATE TABLE {service}_connection (
    id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    access_token TEXT NOT NULL,        -- Encrypted
    refresh_token TEXT,                -- Encrypted (if applicable)
    expires_at TEXT,                   -- ISO 8601 timestamp
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_{service}_connection_user_id ON {service}_connection(user_id);
```

Edit `down.sql`:
```sql
DROP TABLE {service}_connection;
```

Run migration:
```bash
cd backend && diesel migration run
cd backend && diesel print-schema > src/schema.rs
```

### 2. Add Diesel Model

In `backend/src/models/user_models.rs`, add:

```rust
#[derive(Queryable, Insertable, Debug, Clone)]
#[diesel(table_name = {service}_connection)]
pub struct {Service}Connection {
    pub id: i32,
    pub user_id: i32,
    pub access_token: String,      // Encrypted
    pub refresh_token: Option<String>,  // Encrypted
    pub expires_at: Option<String>,
    pub created_at: String,
}

#[derive(Insertable)]
#[diesel(table_name = {service}_connection)]
pub struct New{Service}Connection {
    pub user_id: i32,
    pub access_token: String,
    pub refresh_token: Option<String>,
    pub expires_at: Option<String>,
}
```

### 3. Add Repository Methods

In `backend/src/repositories/connection_auth.rs`, add methods:

```rust
use crate::schema::{service}_connection;
use crate::models::user_models::{Service}Connection, New{Service}Connection;

pub fn create_{service}_connection(
    conn: &mut SqliteConnection,
    new_connection: New{Service}Connection,
) -> Result<{Service}Connection, diesel::result::Error> {
    diesel::insert_into({service}_connection::table)
        .values(&new_connection)
        .get_result(conn)
}

pub fn get_{service}_connection(
    conn: &mut SqliteConnection,
    user_id: i32,
) -> Result<{Service}Connection, diesel::result::Error> {
    {service}_connection::table
        .filter({service}_connection::user_id.eq(user_id))
        .first(conn)
}

pub fn update_{service}_tokens(
    conn: &mut SqliteConnection,
    user_id: i32,
    access_token: &str,
    refresh_token: Option<&str>,
    expires_at: Option<&str>,
) -> Result<usize, diesel::result::Error> {
    diesel::update({service}_connection::table)
        .filter({service}_connection::user_id.eq(user_id))
        .set((
            {service}_connection::access_token.eq(access_token),
            {service}_connection::refresh_token.eq(refresh_token),
            {service}_connection::expires_at.eq(expires_at),
        ))
        .execute(conn)
}

pub fn delete_{service}_connection(
    conn: &mut SqliteConnection,
    user_id: i32,
) -> Result<usize, diesel::result::Error> {
    diesel::delete({service}_connection::table)
        .filter({service}_connection::user_id.eq(user_id))
        .execute(conn)
}
```

### 4. Create OAuth Handler

Create `backend/src/handlers/{service}_auth.rs`:

```rust
use axum::{Extension, extract::Query, response::Redirect, http::StatusCode};
use serde::Deserialize;
use crate::repositories::connection_auth;
use crate::utils::encryption::{encrypt_data, decrypt_data};
use crate::models::AppState;

#[derive(Deserialize)]
pub struct {Service}AuthQuery {
    code: String,
    state: Option<String>,
}

// Step 1: Redirect to OAuth provider
pub async fn {service}_oauth_start(
    Extension(user_id): Extension<i32>,
) -> Result<Redirect, StatusCode> {
    let client_id = std::env::var("{SERVICE}_CLIENT_ID")
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

    let redirect_uri = format!(
        "{}/api/{service}/oauth/callback",
        std::env::var("BACKEND_URL").unwrap_or_default()
    );

    let auth_url = format!(
        "https://{service}.com/oauth/authorize?client_id={}&redirect_uri={}&response_type=code&scope={}",
        client_id,
        urlencoding::encode(&redirect_uri),
        "read write"  // Adjust scopes as needed
    );

    Ok(Redirect::to(&auth_url))
}

// Step 2: Handle OAuth callback
pub async fn {service}_oauth_callback(
    Extension(user_id): Extension<i32>,
    Extension(state): Extension<AppState>,
    Query(query): Query<{Service}AuthQuery>,
) -> Result<Redirect, StatusCode> {
    let client_id = std::env::var("{SERVICE}_CLIENT_ID")
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    let client_secret = std::env::var("{SERVICE}_CLIENT_SECRET")
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

    // Exchange code for tokens
    let client = reqwest::Client::new();
    let token_response = client
        .post("https://{service}.com/oauth/token")
        .form(&[
            ("grant_type", "authorization_code"),
            ("code", &query.code),
            ("client_id", &client_id),
            ("client_secret", &client_secret),
            ("redirect_uri", &format!("{}/api/{service}/oauth/callback",
                std::env::var("BACKEND_URL").unwrap_or_default())),
        ])
        .send()
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?
        .json::<serde_json::Value>()
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

    let access_token = token_response["access_token"]
        .as_str()
        .ok_or(StatusCode::INTERNAL_SERVER_ERROR)?;
    let refresh_token = token_response["refresh_token"].as_str();
    let expires_in = token_response["expires_in"].as_i64();

    // Encrypt tokens
    let encrypted_access = encrypt_data(access_token)
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    let encrypted_refresh = refresh_token
        .map(|t| encrypt_data(t))
        .transpose()
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

    let expires_at = expires_in.map(|sec| {
        chrono::Utc::now()
            .checked_add_signed(chrono::Duration::seconds(sec))
            .unwrap()
            .to_rfc3339()
    });

    // Store in database
    let mut conn = state.pool.get()
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

    let new_connection = connection_auth::New{Service}Connection {
        user_id,
        access_token: encrypted_access,
        refresh_token: encrypted_refresh,
        expires_at,
    };

    connection_auth::create_{service}_connection(&mut conn, new_connection)
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

    Ok(Redirect::to(&format!("{}/connections",
        std::env::var("FRONTEND_URL").unwrap_or_default())))
}

// Disconnect
pub async fn {service}_disconnect(
    Extension(user_id): Extension<i32>,
    Extension(state): Extension<AppState>,
) -> Result<StatusCode, StatusCode> {
    let mut conn = state.pool.get()
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

    connection_auth::delete_{service}_connection(&mut conn, user_id)
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;

    Ok(StatusCode::OK)
}
```

### 5. Add Routes to Main

In `backend/src/main.rs`, add routes:

```rust
use handlers::{service}_auth;

// In the router setup:
.route("/api/{service}/oauth/start",
    get({service}_auth::{service}_oauth_start)
    .layer(middleware::from_fn_with_state(app_state.clone(), require_auth)))
.route("/api/{service}/oauth/callback",
    get({service}_auth::{service}_oauth_callback)
    .layer(middleware::from_fn_with_state(app_state.clone(), require_auth)))
.route("/api/{service}/disconnect",
    post({service}_auth::{service}_disconnect)
    .layer(middleware::from_fn_with_state(app_state.clone(), require_auth)))
```

### 6. Create Frontend Component

Create `frontend/src/connections/{service}.rs`:

```rust
use yew::prelude::*;
use gloo_net::http::Request;
use crate::config;

#[function_component(ServiceConnection)]
pub fn {service}_connection() -> Html {
    let connected = use_state(|| false);
    let loading = use_state(|| true);

    // Check connection status on mount
    {
        let connected = connected.clone();
        let loading = loading.clone();
        use_effect_with((), move |_| {
            wasm_bindgen_futures::spawn_local(async move {
                // Check if connected via API call
                // Set connected state accordingly
                loading.set(false);
            });
        });
    }

    let on_connect = {
        let token = /* get from context */;
        Callback::from(move |_| {
            let backend_url = config::get_backend_url();
            web_sys::window()
                .unwrap()
                .location()
                .set_href(&format!("{}/api/{service}/oauth/start", backend_url))
                .unwrap();
        })
    };

    let on_disconnect = {
        let connected = connected.clone();
        let token = /* get from context */;
        Callback::from(move |_| {
            let connected = connected.clone();
            wasm_bindgen_futures::spawn_local(async move {
                let _ = Request::post(&format!("{}/api/{service}/disconnect", config::get_backend_url()))
                    .header("Authorization", &format!("Bearer {}", token))
                    .send()
                    .await;
                connected.set(false);
            });
        })
    };

    html! {
        <div class="connection-card">
            <h3>{"Service Integration"}</h3>
            if *loading {
                <p>{"Loading..."}</p>
            } else if *connected {
                <button onclick={on_disconnect}>{"Disconnect"}</button>
            } else {
                <button onclick={on_connect}>{"Connect"}</button>
            }
        </div>
    }
}
```

### 7. Add Frontend Route

In `frontend/src/main.rs`, add the connection component to the connections page or create a dedicated route.

### 8. Add Environment Variables

In `backend/.env`:
```bash
{SERVICE}_CLIENT_ID=your_client_id
{SERVICE}_CLIENT_SECRET=your_client_secret
```

## Testing Checklist

- [ ] OAuth flow redirects correctly
- [ ] Tokens are encrypted in database
- [ ] Connection appears in frontend
- [ ] Disconnect removes connection
- [ ] Token refresh works (if applicable)
- [ ] Error handling for failed OAuth

## Common Patterns

### Token Refresh
```rust
pub async fn refresh_{service}_token(
    user_id: i32,
    state: &AppState,
) -> Result<String, Box<dyn std::error::Error>> {
    let mut conn = state.pool.get()?;
    let connection = connection_auth::get_{service}_connection(&mut conn, user_id)?;

    let refresh_token = decrypt_data(&connection.refresh_token.unwrap())?;

    // Exchange refresh token for new access token
    // Update database with new tokens
    // Return decrypted access token
}
```

### API Calls with Integration
```rust
pub async fn call_{service}_api(
    user_id: i32,
    state: &AppState,
    endpoint: &str,
) -> Result<serde_json::Value, Box<dyn std::error::Error>> {
    let mut conn = state.pool.get()?;
    let connection = connection_auth::get_{service}_connection(&mut conn, user_id)?;
    let access_token = decrypt_data(&connection.access_token)?;

    let client = reqwest::Client::new();
    let response = client
        .get(&format!("https://api.{service}.com{}", endpoint))
        .bearer_auth(access_token)
        .send()
        .await?
        .json()
        .await?;

    Ok(response)
}
```

## Security Notes

- **Always encrypt tokens** using `utils/encryption.rs`
- **Use HTTPS** for OAuth redirects in production
- **Validate state parameter** to prevent CSRF
- **Set minimum scopes** required for functionality
- **Implement token refresh** before expiration
- **Handle revoked tokens** gracefully
