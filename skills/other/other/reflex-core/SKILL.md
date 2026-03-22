---
name: reflex-core
description: "Core guide for building Reflex (Python full-stack framework) applications. Use when working with state management, event handlers, components, routing, styling, database integration (DuckDB), common patterns (forms, tables, uploads), logging, testing, and project structure. Covers everything except FastAPI custom endpoints and visual design aesthetics."
---

# Reflex Core Developer

This skill covers the core technical aspects of building full-stack web applications with Reflex — a Python framework that compiles to a React frontend and FastAPI backend. It includes state management, components, event handlers, styling, routing, database integration, logging, testing, and best practices.

For visual design and aesthetics → see skill `reflex-design`.
For custom FastAPI endpoints → see skill `reflex-fastapi`.

---

## Architecture Overview

Reflex is a full-stack Python framework for building web applications without writing JavaScript. Apps compile to a React frontend and FastAPI backend, with state management and event handlers running entirely in Python.

- **Frontend**: Compiled to React (JavaScript) for UI rendering
- **Backend**: FastAPI server running Python event handlers
- **Communication**: WebSockets for real-time state updates
- **State**: Server-side Python state synchronized to frontend

---

## Project Structure

```
my_app/
├── my_app/
│   ├── __init__.py
│   ├── my_app.py            # App entry point and route registration
│   ├── states/
│   │   ├── auth_state.py    # Authentication state
│   │   ├── data_state.py    # Business data state
│   │   └── ui_state.py      # UI state (modals, loading, etc.)
│   ├── components/
│   │   ├── navbar.py
│   │   └── shared.py        # Reusable components
│   ├── pages/
│   │   ├── index.py
│   │   └── dashboard.py
│   ├── api/
│   │   ├── routes.py        # FastAPI custom endpoints
│   │   └── schemas.py       # Pydantic V2 models
│   ├── exceptions.py        # Custom exception classes
│   └── logging_config.py   # Logging configuration
├── tests/
│   ├── test_states.py
│   └── test_api.py
├── docs/
│   ├── README.md
│   └── CHANGELOG.md
├── assets/
├── .web/                    # Auto-generated, do not edit
├── .env                     # Environment variables (never in git)
├── rxconfig.py
├── version.py               # __version__ = "1.0.0"
└── requirements.txt
```


---

## Core Concepts

### State Management

State is a Python class that holds all mutable data and event handlers. All state variables must be JSON-serializable.

```python
import reflex as rx

class AppState(rx.State):
    # State variables (any JSON-serializable type)
    count: int = 0
    items: list[str] = []
    user_name: str = ""

    # Event handlers - the ONLY way to modify state
    def increment(self):
        self.count += 1

    def add_item(self, item: str):
        self.items.append(item)

    # Computed vars (derived state)
    @rx.var
    def item_count(self) -> int:
        return len(self.items)
```

**Key Rules:**
- State vars MUST be JSON-serializable (int, str, list, dict, bool, float)
- Only event handlers can modify state
- Use `@rx.var` decorator for computed/derived values
- State is per-user session (isolated between users)
- Split large states into substates (`AuthState`, `DataState`, `UIState`)

### Components

Components are UI building blocks. Reflex provides 60+ built-in components.

```python
import reflex as rx

def header() -> rx.Component:
    return rx.heading("My App", size="lg")

def counter_component(state: AppState) -> rx.Component:
    return rx.vstack(
        rx.text(f"Count: {state.count}"),
        rx.button("Increment", on_click=state.increment),
        spacing="4"
    )
```

**Common Components:**
- Layout: `rx.vstack`, `rx.hstack`, `rx.box`, `rx.container`
- Text: `rx.heading`, `rx.text`, `rx.code`
- Input: `rx.input`, `rx.text_area`, `rx.select`, `rx.checkbox`
- Interactive: `rx.button`, `rx.link`, `rx.icon_button`
- Data: `rx.table`, `rx.data_table`, `rx.list`
- Charts: `rx.recharts.line_chart`, `rx.recharts.bar_chart`, etc.

### Event Handlers

Event handlers respond to user interactions and are the ONLY way to modify state.

```python
class FormState(rx.State):
    form_data: dict[str, str] = {}

    # Simple event handler
    def handle_submit(self):
        print(f"Submitted: {self.form_data}")

    # Event handler with argument
    def update_field(self, field: str, value: str):
        self.form_data[field] = value

    # Async event handler (for API calls, DB queries)
    async def fetch_data(self):
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.example.com/data")
            self.data = response.json()
```

**Event Triggers** (connect components to handlers):
- `on_click`: Button clicks
- `on_change`: Input field changes
- `on_submit`: Form submissions
- `on_mount`: Component first renders
- `on_blur`, `on_focus`: Input focus events

---

## Main App File Pattern

```python
import reflex as rx

# 1. Define State
class State(rx.State):
    count: int = 0

    def increment(self):
        self.count += 1

# 2. Define Pages
def index() -> rx.Component:
    return rx.container(
        rx.heading("Welcome"),
        rx.button("Click", on_click=State.increment),
        rx.text(f"Count: {State.count}")
    )

def about() -> rx.Component:
    return rx.container(
        rx.heading("About"),
        rx.link("Home", href="/")
    )

# 3. Create App and Add Routes
app = rx.App()
app.add_page(index, route="/")
app.add_page(about, route="/about")
```

---

## Common Patterns

### Form Handling

```python
class FormState(rx.State):
    name: str = ""
    email: str = ""

    def handle_submit(self, form_data: dict):
        self.name = form_data.get("name", "")
        self.email = form_data.get("email", "")

def form_page():
    return rx.form(
        rx.vstack(
            rx.input(name="name", placeholder="Name"),
            rx.input(name="email", placeholder="Email"),
            rx.button("Submit", type="submit"),
        ),
        on_submit=FormState.handle_submit,
    )
```

### Data Tables

```python
class DataState(rx.State):
    data: list[dict] = [
        {"id": 1, "name": "Alice", "age": 25},
        {"id": 2, "name": "Bob", "age": 30},
    ]

def data_table_page():
    return rx.data_table(
        data=DataState.data,
        columns=["id", "name", "age"],
        sort=True,
        search=True,
        pagination=True,
    )
```

### File Upload

```python
class UploadState(rx.State):
    async def handle_upload(self, files: list[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            outfile = f"./uploads/{file.filename}"
            with open(outfile, "wb") as f:
                f.write(upload_data)

def upload_page():
    return rx.vstack(
        rx.upload(
            rx.button("Select Files"),
            id="upload1",
        ),
        rx.button(
            "Upload",
            on_click=UploadState.handle_upload(rx.upload_files(upload_id="upload1"))
        ),
    )
```

### Database Integration (DuckDB)

```python
import duckdb
import polars as pl

class DBState(rx.State):
    records: list[dict] = []

    async def load_data(self):
        conn = duckdb.connect("data/mydb.duckdb")
        df = conn.execute("SELECT * FROM mytable").pl()
        self.records = df.to_dicts()
        conn.close()

    async def insert_record(self, data: dict):
        conn = duckdb.connect("data/mydb.duckdb")
        conn.execute(
            "INSERT INTO mytable (name, value) VALUES (?, ?)",
            [data["name"], data["value"]]
        )
        conn.close()
        await self.load_data()  # Refresh
```

---

## Styling & Layout

### Inline Styling

```python
rx.box(
    rx.text("Styled text"),
    bg="#1a5f9e",
    color="white",
    padding="4",
    border_radius="md",
)
```

### Responsive Layout

```python
rx.container(
    rx.responsive_grid(
        rx.box("Item 1", bg="blue"),
        rx.box("Item 2", bg="green"),
        rx.box("Item 3", bg="red"),
        columns=[1, 2, 3],  # 1 col mobile, 2 tablet, 3 desktop
        spacing="4",
    ),
    max_width="1200px",
)
```

### Common Style Props

- Layout: `width`, `height`, `padding`, `margin`, `display`
- Colors: `bg` (background), `color` (text)
- Typography: `font_size`, `font_weight`, `text_align`
- Borders: `border`, `border_radius`, `border_color`
- Spacing: `spacing` (for stacks), `gap`

---

## Routing

```python
app = rx.App()

# Route with parameters
@rx.page(route="/user/[id]")
def user_page() -> rx.Component:
    return rx.text(f"User ID: {State.router.page.params.get('id')}")

# Simple routes
app.add_page(index, route="/")
app.add_page(about, route="/about")

# Links
rx.link("Go to About", href="/about")

# Programmatic navigation
def go_home(self):
    return rx.redirect("/")
```

---

## Best Practices

1. **State Organization**: Split large states into substates
   ```python
   class AuthState(rx.State):
       user: str = ""

   class DataState(rx.State):
       items: list = []
   ```

2. **Component Reusability**: Create reusable component functions
   ```python
   def card(title: str, content: str) -> rx.Component:
       return rx.box(
           rx.heading(title, size="md"),
           rx.text(content),
           padding="4",
           border="1px solid #ddd",
       )
   ```

3. **Event Handler Performance**: Use async for I/O operations
   ```python
   async def fetch_data(self):
       # Async I/O won't block other users
       self.data = await some_api_call()
   ```

4. **Type Hints**: Always type-hint state vars and event handlers
   ```python
   count: int = 0
   items: list[str] = []

   def update_count(self, value: int) -> None:
       self.count = value
   ```

5. **Design Intentionality**: Every component should reflect the chosen aesthetic — padding, color, font, and motion must be cohesive. Use `rx.html.style` for global CSS variables and keyframe animations. See skill `reflex-design` for full guidelines.

6. **FastAPI Scope**: Use custom FastAPI endpoints only for logic that lives outside Reflex state (webhooks, external integrations, JWT auth). Everything else belongs in event handlers. See skill `reflex-fastapi` for endpoint patterns.

---

## Logging

Never use `print()`. Configure structured logging at module level.

```python
import logging

# Global setup — place in logging_config.py and import at app startup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

# In each module
logger = logging.getLogger(__name__)

class DataState(rx.State):
    async def load_data(self):
        try:
            logger.info("Starting data load")
            # ... logic
            logger.debug("Data loaded: %d records", len(self.records))
        except Exception as e:
            logger.error("Error loading data: %s", e, exc_info=True)
            raise
```

**Recommended levels:**
- `DEBUG`: internal flow and intermediate values (development only)
- `INFO`: relevant normal operations (process start/end)
- `WARNING`: unexpected non-critical situations
- `ERROR`: recoverable failures with full context
- `CRITICAL`: failures that halt the application

---

## Testing

### State Test (pytest-asyncio)

```python
import pytest
from my_app.states.data_state import DataState

@pytest.mark.asyncio
async def test_load_data_success():
    state = DataState()
    await state.load_data()
    assert isinstance(state.records, list)

@pytest.mark.asyncio
async def test_load_data_empty_returns_list():
    state = DataState()
    state.records = []
    assert len(state.records) == 0
```

---

## Development Workflow

```bash
pip install reflex
reflex init
reflex run          # Dev server at http://localhost:3000
reflex export       # Production build
reflex db init      # Initialize database (if using Reflex DB)
reflex db migrate   # Run migrations
```

---

## References

- Reflex Docs: https://reflex.dev/docs/getting-started/introduction/
- Reflex Component Library: https://reflex.dev/docs/library
- Reflex Tutorials: https://reflex.dev/docs/getting-started/tutorial/
- Example Apps: See `examples/` directory for complete working examples
- Common Patterns Reference: See `references/patterns.md` for authentication flows, real-time updates, complex form validation, multi-step workflows, and data visualization
