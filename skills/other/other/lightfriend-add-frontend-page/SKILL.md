---
name: lightfriend-add-frontend-page
description: Step-by-step guide for adding new pages to the Yew frontend
---

# Adding a New Frontend Page

This skill guides you through adding a new page to the Lightfriend Yew WebAssembly frontend.

## Overview

A complete page includes:
- Page component in `frontend/src/pages/`
- Route enum variant in `main.rs`
- Route handler in switch function
- Navigation link (if applicable)

## Step-by-Step Process

### 1. Create Page Component

Create `frontend/src/pages/{page_name}.rs`:

```rust
use yew::prelude::*;
use gloo_net::http::Request;
use crate::config;

#[function_component(PageName)]
pub fn page_name() -> Html {
    // State management
    let data = use_state(|| None::<SomeData>);
    let loading = use_state(|| true);
    let error = use_state(|| None::<String>);

    // Load data on mount
    {
        let data = data.clone();
        let loading = loading.clone();
        let error = error.clone();

        use_effect_with((), move |_| {
            wasm_bindgen_futures::spawn_local(async move {
                match fetch_data().await {
                    Ok(result) => {
                        data.set(Some(result));
                        loading.set(false);
                    }
                    Err(e) => {
                        error.set(Some(e.to_string()));
                        loading.set(false);
                    }
                }
            });
        });
    }

    html! {
        <div class="page-container">
            <h1>{"Page Title"}</h1>

            if *loading {
                <p>{"Loading..."}</p>
            } else if let Some(err) = (*error).clone() {
                <p class="error">{err}</p>
            } else if let Some(content) = (*data).clone() {
                // Render content
                <div>
                    {format!("Content: {:?}", content)}
                </div>
            }
        </div>
    }
}

// Helper functions
async fn fetch_data() -> Result<SomeData, Box<dyn std::error::Error>> {
    let token = /* get from context or local storage */;
    let backend_url = config::get_backend_url();

    let response = Request::get(&format!("{}/api/endpoint", backend_url))
        .header("Authorization", &format!("Bearer {}", token))
        .send()
        .await?
        .json::<SomeData>()
        .await?;

    Ok(response)
}

#[derive(Clone, serde::Deserialize, serde::Serialize)]
struct SomeData {
    // Define your data structure
}
```

### 2. Add Module Declaration

**CRITICAL: This codebase does NOT use `mod.rs` files!**

Instead, add the module declaration to the inline `mod pages { }` block in `frontend/src/main.rs`:

```rust
mod pages {
    pub mod home;
    pub mod landing;
    pub mod {page_name};  // Add your new page here
    // ... other pages
}
```

**NEVER create a `mod.rs` file** - this is a common mistake. Lightfriend uses named module files (e.g., `home.rs`, `landing.rs`) and declares them in the inline module block in `main.rs`.

### 3. Add Route Variant

In `frontend/src/main.rs`, add a route variant to the `Route` enum:

```rust
#[derive(Clone, Routable, PartialEq)]
pub enum Route {
    #[at("/")]
    Home,
    #[at("/page-name")]
    PageName,
    // ... other routes
    #[not_found]
    #[at("/404")]
    NotFound,
}
```

### 4. Add Route Handler

In the `switch()` function in `frontend/src/main.rs`, add:

```rust
fn switch(route: Route) -> Html {
    match route {
        Route::Home => html! { <Home /> },
        Route::PageName => html! { <PageName /> },
        // ... other routes
        Route::NotFound => html! { <h1>{"404 - Page Not Found"}</h1> },
    }
}
```

### 5. Add Navigation Link (Optional)

If the page should appear in navigation, add to the `Nav` component in `frontend/src/main.rs`:

```rust
#[function_component(Nav)]
fn nav() -> Html {
    html! {
        <nav>
            <Link<Route> to={Route::Home}>{"Home"}</Link<Route>>
            <Link<Route> to={Route::PageName}>{"Page Name"}</Link<Route>>
            // ... other links
        </nav>
    }
}
```

### 6. Test the Page

```bash
cd frontend && trunk serve
```

Navigate to `http://localhost:8080/page-name`

## Common Patterns

### Protected Routes (Require Auth)

```rust
use yew_hooks::use_local_storage;

#[function_component(ProtectedPage)]
pub fn protected_page() -> Html {
    let token = use_local_storage::<String>("token".to_string());

    if token.is_none() {
        // Redirect to login
        let navigator = use_navigator().unwrap();
        navigator.push(&Route::Login);
        return html! {};
    }

    html! {
        <div>{"Protected content"}</div>
    }
}
```

### Page with Form

```rust
use web_sys::HtmlInputElement;

#[function_component(FormPage)]
pub fn form_page() -> Html {
    let name_ref = use_node_ref();
    let email_ref = use_node_ref();
    let submitting = use_state(|| false);

    let on_submit = {
        let name_ref = name_ref.clone();
        let email_ref = email_ref.clone();
        let submitting = submitting.clone();

        Callback::from(move |e: SubmitEvent| {
            e.prevent_default();
            let submitting = submitting.clone();

            let name = name_ref.cast::<HtmlInputElement>()
                .unwrap()
                .value();
            let email = email_ref.cast::<HtmlInputElement>()
                .unwrap()
                .value();

            submitting.set(true);

            wasm_bindgen_futures::spawn_local(async move {
                match submit_form(name, email).await {
                    Ok(_) => {
                        // Handle success
                    }
                    Err(e) => {
                        // Handle error
                    }
                }
                submitting.set(false);
            });
        })
    };

    html! {
        <form onsubmit={on_submit}>
            <input
                ref={name_ref}
                type="text"
                placeholder="Name"
                required=true
            />
            <input
                ref={email_ref}
                type="email"
                placeholder="Email"
                required=true
            />
            <button type="submit" disabled={*submitting}>
                if *submitting {
                    {"Submitting..."}
                } else {
                    {"Submit"}
                }
            </button>
        </form>
    }
}

async fn submit_form(name: String, email: String) -> Result<(), Box<dyn std::error::Error>> {
    let token = /* get from context */;

    Request::post(&format!("{}/api/submit", config::get_backend_url()))
        .header("Authorization", &format!("Bearer {}", token))
        .json(&serde_json::json!({
            "name": name,
            "email": email,
        }))?
        .send()
        .await?;

    Ok(())
}
```

### Page with Context

```rust
use yew::prelude::*;

#[derive(Clone, PartialEq)]
pub struct UserContext {
    pub user_id: i32,
    pub email: String,
}

#[function_component(ContextPage)]
pub fn context_page() -> Html {
    let user_ctx = use_context::<UserContext>()
        .expect("UserContext not found");

    html! {
        <div>
            <p>{format!("User ID: {}", user_ctx.user_id)}</p>
            <p>{format!("Email: {}", user_ctx.email)}</p>
        </div>
    }
}
```

### Page with Route Parameters

```rust
#[derive(Clone, Routable, PartialEq)]
pub enum Route {
    #[at("/users/:id")]
    UserDetail { id: i32 },
}

#[derive(Properties, PartialEq)]
pub struct UserDetailProps {
    pub id: i32,
}

#[function_component(UserDetail)]
pub fn user_detail(props: &UserDetailProps) -> Html {
    let user_data = use_state(|| None::<User>);

    {
        let user_data = user_data.clone();
        let user_id = props.id;

        use_effect_with(user_id, move |_| {
            wasm_bindgen_futures::spawn_local(async move {
                if let Ok(user) = fetch_user(user_id).await {
                    user_data.set(Some(user));
                }
            });
        });
    }

    html! {
        <div>
            if let Some(user) = (*user_data).clone() {
                <h1>{user.name}</h1>
            }
        </div>
    }
}

// In switch function:
fn switch(route: Route) -> Html {
    match route {
        Route::UserDetail { id } => html! { <UserDetail id={id} /> },
        // ...
    }
}
```

### Page with Multiple API Calls

```rust
#[function_component(DashboardPage)]
pub fn dashboard_page() -> Html {
    let stats = use_state(|| None::<Stats>);
    let activity = use_state(|| None::<Vec<Activity>>);
    let loading = use_state(|| true);

    {
        let stats = stats.clone();
        let activity = activity.clone();
        let loading = loading.clone();

        use_effect_with((), move |_| {
            wasm_bindgen_futures::spawn_local(async move {
                // Fetch multiple endpoints in parallel
                let (stats_result, activity_result) = tokio::join!(
                    fetch_stats(),
                    fetch_activity()
                );

                if let Ok(s) = stats_result {
                    stats.set(Some(s));
                }
                if let Ok(a) = activity_result {
                    activity.set(Some(a));
                }

                loading.set(false);
            });
        });
    }

    html! {
        <div>
            if *loading {
                <p>{"Loading dashboard..."}</p>
            } else {
                <div>
                    {render_stats(&stats)}
                    {render_activity(&activity)}
                </div>
            }
        </div>
    }
}
```

## Styling

**Lightfriend uses CSS style blocks within the `html!` macro, NOT inline Tailwind classes.**

Common pattern:

```rust
html! {
    <div class="page-container">
        <h1 class="page-title">{"Title"}</h1>
        <div class="content-grid">
            <div class="card">
                {"Card content"}
            </div>
        </div>

        <style>
            {r#"
            .page-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 2rem;
            }
            .page-title {
                font-size: 2rem;
                font-weight: bold;
                margin-bottom: 1rem;
            }
            .content-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 1rem;
            }
            .card {
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                padding: 1rem;
            }
            "#}
        </style>
    </div>
}
```

## Testing Checklist

- [ ] Page renders without errors
- [ ] Route works in browser
- [ ] Navigation link works (if added)
- [ ] API calls succeed
- [ ] Loading states display correctly
- [ ] Error states display correctly
- [ ] Authentication checks work (if protected)
- [ ] Mobile responsive (if applicable)

## File Reference

- Page components: `frontend/src/pages/{page}.rs`
- Routes: `frontend/src/main.rs` (Route enum + switch function)
- Navigation: `frontend/src/main.rs` (Nav component)
- Shared components: `frontend/src/components/`
- Backend config: `frontend/src/config.rs`
