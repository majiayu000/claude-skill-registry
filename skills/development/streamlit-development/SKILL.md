---
name: streamlit-development
description:
  Developing, testing, and deploying Streamlit data applications on Snowflake. Use this skill when
  you're building interactive data apps, setting up local development environments, testing with
  pytest or Playwright, or deploying apps to Snowflake using Streamlit in Snowflake.
---

# Streamlit Development

Build interactive data applications using Streamlit, test them locally, and deploy to Snowflake's
native Streamlit environment.

## Quick Start

**Execution Modes:**

- **Local Development** - PyPI packages, full environment
- **Snowflake Deployment** - Snowflake Anaconda packages, managed environment

## Connection Pattern

**Critical:** Support both local development and Snowflake deployment:

```python
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session

@st.cache_resource
def get_snowpark_session():
    try:
        return get_active_session()  # Snowflake
    except:
        return Session.builder.config('connection_name', 'default').create()  # Local
```

**For connection setup**, see the **`snowflake-connections` skill** for:

- Creating `~/.snowflake/connections.toml`
- Authentication methods (SSO, key pair, username/password)
- Multiple environment configurations
- Environment variable overrides

## Local Development

### Setup

```bash
# Install dependencies (pin Streamlit version to match Snowflake)
uv pip install --system -r requirements.txt

# Example requirements.txt
streamlit==1.46.0  # Must match Snowflake version
snowflake-snowpark-python
pandas
```

### Run Locally

```bash
streamlit run app.py
# Or with environment overrides (see snowflake-connections skill)
SNOWFLAKE_DATABASE=MY_DB streamlit run app.py
```

## Testing

### Unit/Integration Tests

```bash
pytest streamlit_app/tests/ -v
```

### Browser Testing

Use Playwright MCP for interactive testing:

- Verify pages load without errors
- Test forms and navigation
- Check responsive design

See `TESTING_GUIDE.md` for patterns.

## Deployment

### Option 1: Snowflake CLI (Recommended)

```bash
snow streamlit deploy --replace -c default
```

### Option 2: Schemachange

Include Streamlit deployment in migration scripts.

## Key Patterns

- Separate data access from UI logic
- Cache Snowpark sessions
- Use forms for multi-field input
- Handle errors gracefully
- Limit column nesting (max 2 levels)

See `TROUBLESHOOTING.md` for common issues.

## Related Skills

**Complementary Testing:**

- `playwright-mcp` skill - Automate browser testing for Streamlit apps

Use playwright-mcp for visual testing, form validation, responsive design testing, and accessibility
checks of your Streamlit applications.

---

## Code Organization Best Practices

### 1. Separate Data Access from UI

✅ **DO: Modular data access**

```python
# utils/data_loader.py
class DataQueries:
    def __init__(self, session):
        self.session = session

    def get_sales(self, start_date, end_date):
        return self.session.sql(f"""
            SELECT * FROM sales
            WHERE date BETWEEN '{start_date}' AND '{end_date}'
        """).to_pandas()

# app.py
from utils.data_loader import DataQueries
session = get_snowpark_session()
queries = DataQueries(session)
df = queries.get_sales('2024-01-01', '2024-12-31')
st.dataframe(df)
```

❌ **DON'T: Mix SQL with UI code**

### 2. Cache Snowpark Session

Always cache your session to avoid reconnection overhead:

```python
@st.cache_resource
def get_snowpark_session():
    """Get or create Snowpark session (cached)"""
    try:
        return get_active_session()  # When running in Snowflake
    except:
        from snowflake.snowpark import Session
        return Session.builder.config('connection_name', 'default').create()
```

### 3. Use Forms for Multi-Field Input

✅ **DO: Group inputs in forms**

```python
with st.form("customer_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")

    if st.form_submit_button("Save"):
        save_customer(name, email, phone)
        st.success("Customer saved!")
```

❌ **DON'T: Trigger rerun on every input** (causes rerun on every keystroke)

### 4. Handle Errors Gracefully

Provide helpful feedback:

```python
try:
    save_customer(name, email)
    st.success("✅ Customer saved successfully!")
except ValueError as e:
    st.error(f"❌ Invalid input: {e}")
    st.info("💡 Tip: Check that email format is correct")
except Exception as e:
    st.error(f"❌ Unexpected error: {e}")
    st.info("💡 Please contact support if this persists")
```

### 5. Limit Column Nesting (Max 2 Levels)

✅ **DO: 2 levels maximum**

```python
col1, col2 = st.columns(2)
with col1:
    label_col, input_col = st.columns([1, 3])
    with label_col:
        st.markdown("**Name:**")
    with input_col:
        name = st.text_input("Name", label_visibility="collapsed")
```

❌ **DON'T: 3+ levels of nested columns** (causes Streamlit errors)

---

## Performance Optimization

### Cache Data Queries

```python
@st.cache_data(ttl=600)  # Cache for 10 minutes
def load_sales_data(start_date, end_date):
    return session.sql(f"""
        SELECT * FROM sales
        WHERE date BETWEEN '{start_date}' AND '{end_date}'
    """).to_pandas()
```

### Use Session State

```python
# Initialize state
if 'data' not in st.session_state:
    st.session_state.data = load_data()

# Access throughout app
df = st.session_state.data
```

### Lazy Load Heavy Computations

```python
if st.button("Run Analysis"):
    with st.spinner("Analyzing..."):
        result = expensive_computation()
        st.session_state.result = result

if 'result' in st.session_state:
    st.write(st.session_state.result)
```

---

## Snowflake-Specific Considerations

### API Limitations

Some Streamlit features don't work in Snowflake:

| Feature           | Status                 | Alternative                   |
| ----------------- | ---------------------- | ----------------------------- |
| `st.dialog()`     | ❌ Not supported       | Use `st.expander()` or modals |
| `st.toggle()`     | ❌ Not supported       | Use `st.checkbox()`           |
| `st.rerun()`      | ⚠️ Older versions only | Use `st.experimental_rerun()` |
| `st.connection()` | ❌ Not supported       | Use `get_active_session()`    |

### Package Availability

**Only Snowflake Anaconda packages available:**

```yaml
# environment.yml
name: streamlit_env
channels:
  - snowflake
dependencies:
  - pandas
  - plotly
  # ❌ DON'T include:
  # - streamlit  (already provided)
  # - snowflake-snowpark-python  (already provided)
```

**Check package availability:** <https://repo.anaconda.com/pkgs/snowflake/>

### Python Version Support

**Don't specify Python version** - Snowflake controls this:

```yaml
# ❌ DON'T DO THIS
dependencies:
  - python=3.11  # Wrong!

# ✅ DO THIS
dependencies:
  - pandas
  - plotly
```

---

## Common Pitfalls

### DuplicateWidgetID Error

**Problem:** Two widgets with same implicit key

**Solution:** Add explicit keys

```python
st.text_input("Name", key="customer_name")
st.text_input("Name", key="product_name")
```

### IndentationError

**Check before deploying:**

```bash
python -c "import ast; ast.parse(open('streamlit_app/app.py').read())"
```

### Session Not Found (Local Development)

**Ensure proper fallback:**

```python
def get_snowpark_session():
    try:
        return get_active_session()  # Snowflake
    except:
        from snowflake.snowpark import Session
        return Session.builder.config('connection_name', 'default').create()
```

### Form Parameter Errors

**Some parameters not supported in Snowflake:**

- ❌ `border=False` in `st.form()`
- ❌ `border=True` in `st.container()`
- ❌ `hide_index=True` in `st.dataframe()` (older versions)

---

## Pre-Deployment Checklist

### Before Deploying

- [ ] ✅ Fix all indentation errors
- [ ] ✅ Run unit tests: `pytest streamlit_app/tests/ -v`
- [ ] ✅ Test locally: `streamlit run streamlit_app/app.py`
- [ ] ✅ Verify forms and navigation with browser testing
- [ ] ✅ Check `environment.yml` only has non-default packages
- [ ] ✅ Remove development dependencies
- [ ] ✅ Test with different user roles/permissions
- [ ] ✅ Verify data access controls

### Deployment Commands

```bash
# Method 1: Snowflake CLI (Recommended)
snow streamlit deploy --replace --connection default

# Method 2: Schemachange
schemachange deploy --config-folder . --connection-name default
```

### Post-Deployment

- [ ] ✅ Verify app appears in Snowflake: Data → Databases → Schema → Streamlit
- [ ] ✅ Test all features in Snowflake UI
- [ ] ✅ Check permissions for different roles
- [ ] ✅ Monitor for errors in Streamlit logs

---

## Security Best Practices

### 1. Never Hardcode Credentials

✅ **DO:**

```python
session = get_active_session()  # Uses Snowflake auth
```

❌ **DON'T:**

```python
password = "secret123"  # Never do this!
```

### 2. Use Role-Based Access Control

```python
# Check user role
current_role = session.sql("SELECT CURRENT_ROLE()").collect()[0][0]

if current_role == "ADMIN":
    st.write("Admin features visible")
else:
    st.info("Admin access required")
```

### 3. Validate User Inputs

```python
def save_customer(name, email):
    if not name or len(name) < 2:
        raise ValueError("Name must be at least 2 characters")
    if "@" not in email:
        raise ValueError("Invalid email format")

    # Proceed with save
    ...
```

---

## Resources

- **`connections.py`** - Required session pattern for local/Snowflake compatibility
- `snowflake-connections` skill - Connection setup, authentication, and multi-environment
  configuration
- `playwright-mcp` skill - Browser testing automation for Streamlit apps

---

**Goal:** Transform AI agents into expert Streamlit developers who build production-ready data
applications with proper code organization, performance optimization, and Snowflake-specific best
practices.
