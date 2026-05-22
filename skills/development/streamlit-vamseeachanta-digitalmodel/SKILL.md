---
name: streamlit
version: 1.0.0
description: Build interactive data applications and dashboards with pure Python - no frontend experience required
author: workspace-hub
category: data-analysis
capabilities:
  - Rapid prototyping of data applications
  - Interactive widgets and user inputs
  - Data visualization integration (Plotly, Matplotlib, Altair)
  - Caching for performance optimization
  - Session state management
  - Multi-page application support
  - Cloud deployment ready
tools:
  - streamlit
  - plotly
  - pandas
  - polars
tags: [streamlit, dashboard, data-app, visualization, python, web-app, interactive, prototyping]
platforms: [python, web]
related_skills:
  - polars
  - dash
  - plotly
  - pandas-data-processing
---

# Streamlit Data Application Skill

Build beautiful, interactive data applications with pure Python. Transform data scripts into shareable web apps in minutes with widgets, charts, and layouts.

## When to Use This Skill

### USE Streamlit when:
- **Rapid prototyping** - Need to build a data app quickly
- **Internal tools** - Creating tools for your team
- **Data exploration** - Interactive exploration of datasets
- **Demo applications** - Showcasing data science projects
- **ML model demos** - Building interfaces for model inference
- **Simple dashboards** - Quick insights without complex setup
- **Python-only development** - No JavaScript/frontend knowledge required

### DON'T USE Streamlit when:
- **Complex interactivity** - Need fine-grained callback control (use Dash)
- **Enterprise deployment** - Require advanced authentication/scaling (use Dash Enterprise)
- **Custom components** - Heavy custom JavaScript requirements
- **High-traffic production** - Thousands of concurrent users
- **Real-time streaming** - Sub-second update requirements

## Prerequisites

```bash
# Basic installation
pip install streamlit

# With common extras
pip install streamlit plotly pandas polars

# Using uv (recommended)
uv pip install streamlit plotly pandas polars altair

# Verify installation
streamlit hello
```

## Core Capabilities

### 1. Basic Application Structure

**Minimal App (app.py):**
```python
import streamlit as st
import pandas as pd
import polars as pl

# Page configuration (must be first Streamlit command)
st.set_page_config(
    page_title="My Data App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and header
st.title("My Data Application")
st.header("Welcome to the Dashboard")
st.subheader("Data Analysis Section")

# Text elements
st.text("This is plain text")
st.markdown("**Bold** and *italic* text with [links](https://streamlit.io)")
st.caption("This is a caption for additional context")
st.code("print('Hello, Streamlit!')", language="python")

# Display data
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["NYC", "LA", "Chicago"]
})

st.dataframe(df)  # Interactive table
st.table(df)       # Static table
st.json({"key": "value", "list": [1, 2, 3]})

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Revenue", "$1.2M", "+12%")
col2.metric("Users", "10,234", "-2%")
col3.metric("Conversion", "3.2%", "+0.5%")
```

**Run the app:**
```bash
streamlit run app.py
```

### 2. Widgets and User Input

**Input Widgets:**
```python
import streamlit as st
from datetime import datetime, date

# Text inputs
name = st.text_input("Enter your name", value="User")
bio = st.text_area("Tell us about yourself", height=100)
password = st.text_input("Password", type="password")

# Numeric inputs
age = st.number_input("Age", min_value=0, max_value=120, value=25, step=1)
price = st.slider("Price Range", 0.0, 100.0, (25.0, 75.0))  # Range slider
rating = st.slider("Rating", 1, 5, 3)

# Selection widgets
option = st.selectbox("Choose an option", ["Option A", "Option B", "Option C"])
options = st.multiselect("Select multiple", ["Red", "Green", "Blue"], default=["Red"])
radio_choice = st.radio("Pick one", ["Small", "Medium", "Large"], horizontal=True)

# Boolean inputs
agree = st.checkbox("I agree to the terms")
toggle = st.toggle("Enable feature")

# Date and time
selected_date = st.date_input("Select a date", value=date.today())
date_range = st.date_input(
    "Date range",
    value=(date(2025, 1, 1), date.today()),
    format="YYYY-MM-DD"
)
selected_time = st.time_input("Select a time")

# File upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv", "xlsx"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(f"Loaded {len(df)} rows")

# Color picker
color = st.color_picker("Pick a color", "#00FF00")

# Buttons
if st.button("Click me"):
    st.write("Button clicked!")

# Download button
@st.cache_data
def get_data():
    return pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

csv = get_data().to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="data.csv",
    mime="text/csv"
)
```

### 3. Layout and Organization

**Columns:**
```python
import streamlit as st

# Equal columns
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Column 1")
    st.write("Content for column 1")

with col2:
    st.header("Column 2")
    st.metric("Metric", "100")

with col3:
    st.header("Column 3")
    st.button("Action")

# Unequal columns
left, right = st.columns([2, 1])  # 2:1 ratio

with left:
    st.write("Wider column")

with right:
    st.write("Narrower column")
```

**Sidebar:**
```python
import streamlit as st

# Sidebar content
st.sidebar.title("Navigation")
st.sidebar.header("Filters")

# Sidebar widgets
category = st.sidebar.selectbox("Category", ["All", "A", "B", "C"])
min_value = st.sidebar.slider("Minimum Value", 0, 100, 25)
show_raw = st.sidebar.checkbox("Show raw data")

# Using 'with' syntax
with st.sidebar:
    st.header("Settings")
    theme = st.radio("Theme", ["Light", "Dark"])
    st.divider()
    st.caption("App v1.0.0")
```

**Tabs:**
```python
import streamlit as st

tab1, tab2, tab3 = st.tabs(["📈 Chart", "📊 Data", "⚙️ Settings"])

with tab1:
    st.header("Chart View")
    # Add chart here

with tab2:
    st.header("Data View")
    # Add dataframe here

with tab3:
    st.header("Settings")
    # Add settings here
```

**Expanders and Containers:**
```python
import streamlit as st

# Expander (collapsible section)
with st.expander("Click to expand"):
    st.write("Hidden content revealed!")
    st.code("print('Hello')")

# Container (grouping elements)
with st.container():
    st.write("This is inside a container")
    col1, col2 = st.columns(2)
    col1.write("Left")
    col2.write("Right")

# Container with border
with st.container(border=True):
    st.write("Content with border")

# Empty placeholder (for dynamic updates)
placeholder = st.empty()
placeholder.text("Initial text")
# Later: placeholder.text("Updated text")
```

### 4. Data Visualization

**Plotly Integration:**
```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Sample data
df = pd.DataFrame({
    "date": pd.date_range("2025-01-01", periods=100),
    "value": [i + (i % 7) * 5 for i in range(100)],
    "category": ["A", "B", "C", "D"] * 25
})

# Plotly Express charts
fig = px.line(df, x="date", y="value", color="category", title="Time Series")
st.plotly_chart(fig, use_container_width=True)

# Scatter plot
fig_scatter = px.scatter(
    df, x="date", y="value",
    color="category", size="value",
    hover_data=["category"]
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Bar chart
category_totals = df.groupby("category")["value"].sum().reset_index()
fig_bar = px.bar(category_totals, x="category", y="value", title="Category Totals")
st.plotly_chart(fig_bar, use_container_width=True)

# Graph Objects for more control
fig_go = go.Figure()
fig_go.add_trace(go.Scatter(
    x=df["date"],
    y=df["value"],
    mode="lines+markers",
    name="Values"
))
fig_go.update_layout(title="Custom Plotly Chart", hovermode="x unified")
st.plotly_chart(fig_go, use_container_width=True)
```

**Built-in Charts:**
```python
import streamlit as st
import pandas as pd
import numpy as np

# Sample data
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["A", "B", "C"]
)

# Simple line chart
st.line_chart(chart_data)

# Area chart
st.area_chart(chart_data)

# Bar chart
st.bar_chart(chart_data)

# Scatter chart (Streamlit 1.26+)
scatter_data = pd.DataFrame({
    "x": np.random.randn(100),
    "y": np.random.randn(100),
    "size": np.random.rand(100) * 100
})
st.scatter_chart(scatter_data, x="x", y="y", size="size")

# Map
map_data = pd.DataFrame({
    "lat": np.random.randn(100) / 50 + 37.76,
    "lon": np.random.randn(100) / 50 - 122.4
})
st.map(map_data)
```

**Matplotlib Integration:**
```python
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Create matplotlib figure
fig, ax = plt.subplots(figsize=(10, 6))
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), label="sin(x)")
ax.plot(x, np.cos(x), label="cos(x)")
ax.legend()
ax.set_title("Matplotlib Chart")

# Display in Streamlit
st.pyplot(fig)
```

### 5. Caching for Performance

**Cache Data (for expensive data operations):**
```python
import streamlit as st
import pandas as pd
import polars as pl
import time

@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """Load and cache data. Cache key: file_path."""
    time.sleep(2)  # Simulate slow load
    return pd.read_csv(file_path)

@st.cache_data(ttl=3600)  # Cache expires after 1 hour
def fetch_api_data(endpoint: str) -> dict:
    """Fetch data from API with time-based cache."""
    import requests
    response = requests.get(endpoint)
    return response.json()

@st.cache_data(show_spinner="Loading data...")
def load_with_spinner(path: str) -> pl.DataFrame:
    """Show custom spinner while loading."""
    return pl.read_parquet(path)

# Using cached functions
df = load_data("data/sales.csv")  # First call: slow
df = load_data("data/sales.csv")  # Second call: instant (cached)

# Clear cache programmatically
if st.button("Clear cache"):
    st.cache_data.clear()
```

**Cache Resources (for global resources):**
```python
import streamlit as st
from sqlalchemy import create_engine

@st.cache_resource
def get_database_connection():
    """Cache database connection (singleton pattern)."""
    return create_engine("postgresql://user:pass@localhost/db")

@st.cache_resource
def load_ml_model():
    """Cache ML model (loaded once per session)."""
    import joblib
    return joblib.load("model.pkl")

# Use cached resources
engine = get_database_connection()
model = load_ml_model()
```

### 6. Session State

**Managing State:**
```python
import streamlit as st

# Initialize state
if "counter" not in st.session_state:
    st.session_state.counter = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display current state
st.write(f"Counter: {st.session_state.counter}")

# Update state with buttons
col1, col2, col3 = st.columns(3)

if col1.button("Increment"):
    st.session_state.counter += 1
    st.rerun()

if col2.button("Decrement"):
    st.session_state.counter -= 1
    st.rerun()

if col3.button("Reset"):
    st.session_state.counter = 0
    st.rerun()

# State with widgets
st.text_input("Name", key="user_name")
st.write(f"Hello, {st.session_state.user_name}!")

# State callback
def on_change():
    st.session_state.processed = st.session_state.raw_input.upper()

st.text_input("Raw input", key="raw_input", on_change=on_change)
if "processed" in st.session_state:
    st.write(f"Processed: {st.session_state.processed}")
```

**Form State:**
```python
import streamlit as st

# Forms prevent rerunning on every widget change
with st.form("my_form"):
    st.write("Submit all at once:")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    color = st.selectbox("Favorite color", ["Red", "Green", "Blue"])

    # Every form needs a submit button
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.success(f"Thanks {name}! You're {age} and like {color}.")
```

### 7. Multi-Page Applications

**Directory Structure:**
```
my_app/
├── app.py              # Main entry point (optional)
├── pages/
│   ├── 1_📊_Dashboard.py
│   ├── 2_📈_Analytics.py
│   └── 3_⚙️_Settings.py
└── utils/
    └── helpers.py
```

**Main App (app.py):**
```python
import streamlit as st

st.set_page_config(
    page_title="Multi-Page App",
    page_icon="🏠",
    layout="wide"
)

st.title("Welcome to My App")
st.write("Use the sidebar to navigate between pages.")

# Shared state initialization
if "user" not in st.session_state:
    st.session_state.user = None
```

**Page 1 (pages/1_Dashboard.py):**
```python
import streamlit as st

st.set_page_config(page_title="Dashboard", page_icon="📊")

st.title("📊 Dashboard")
st.write("This is the dashboard page")

# Access shared state
if st.session_state.get("user"):
    st.write(f"Welcome back, {st.session_state.user}!")
```

**Page 2 (pages/2_Analytics.py):**
```python
import streamlit as st

st.set_page_config(page_title="Analytics", page_icon="📈")

st.title("📈 Analytics")
st.write("This is the analytics page")

# Add analytics content
```

### 8. Advanced Features

**Status and Progress:**
```python
import streamlit as st
import time

# Progress bar
progress = st.progress(0, text="Processing...")
for i in range(100):
    time.sleep(0.01)
    progress.progress(i + 1, text=f"Processing... {i+1}%")

# Spinner
with st.spinner("Loading data..."):
    time.sleep(2)
st.success("Done!")

# Status messages
st.success("Operation successful!")
st.info("This is informational")
st.warning("Warning: Check your inputs")
st.error("An error occurred")
st.exception(ValueError("Example exception"))

# Toast notifications
st.toast("Data saved!", icon="✅")

# Balloons and snow
st.balloons()
st.snow()
```

**Chat Interface:**
```python
import streamlit as st
import time

st.title("Chat Demo")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        response = f"You said: {prompt}"
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
```

**Data Editor:**
```python
import streamlit as st
import pandas as pd

# Editable dataframe
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Active": [True, False, True]
})

edited_df = st.data_editor(
    df,
    num_rows="dynamic",  # Allow adding/deleting rows
    column_config={
        "Name": st.column_config.TextColumn("Name", required=True),
        "Age": st.column_config.NumberColumn("Age", min_value=0, max_value=120),
        "Active": st.column_config.CheckboxColumn("Active")
    }
)

if st.button("Save changes"):
    st.write("Saved:", edited_df)
```

## Complete Examples

### Example 1: Sales Dashboard

```python
import streamlit as st
import pandas as pd
import polars as pl
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Sales Analytics Dashboard")

# Sidebar filters
st.sidebar.header("Filters")

# Date range filter
date_range = st.sidebar.date_input(
    "Date Range",
    value=(datetime.now() - timedelta(days=30), datetime.now()),
    format="YYYY-MM-DD"
)

# Category filter
categories = st.sidebar.multiselect(
    "Categories",
    options=["Electronics", "Clothing", "Food", "Home", "Sports"],
    default=["Electronics", "Clothing", "Food"]
)

# Region filter
regions = st.sidebar.multiselect(
    "Regions",
    options=["North", "South", "East", "West"],
    default=["North", "South", "East", "West"]
)

# Load and filter data
@st.cache_data
def load_sales_data():
    """Generate sample sales data."""
    import numpy as np
    np.random.seed(42)

    dates = pd.date_range(start="2024-01-01", end="2025-12-31", freq="D")
    n = len(dates) * 10  # Multiple records per day

    return pd.DataFrame({
        "date": np.random.choice(dates, n),
        "category": np.random.choice(
            ["Electronics", "Clothing", "Food", "Home", "Sports"], n
        ),
        "region": np.random.choice(["North", "South", "East", "West"], n),
        "revenue": np.random.uniform(100, 5000, n),
        "units": np.random.randint(1, 50, n),
        "customer_id": np.random.randint(1000, 9999, n)
    })

# Load data
df = load_sales_data()

# Apply filters
filtered_df = df[
    (df["date"] >= pd.Timestamp(date_range[0])) &
    (df["date"] <= pd.Timestamp(date_range[1])) &
    (df["category"].isin(categories)) &
    (df["region"].isin(regions))
]

# KPI Metrics Row
st.subheader("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_df["revenue"].sum()
total_units = filtered_df["units"].sum()
total_orders = len(filtered_df)
unique_customers = filtered_df["customer_id"].nunique()

col1.metric(
    "Total Revenue",
    f"${total_revenue:,.0f}",
    delta=f"+{(total_revenue * 0.12):,.0f} vs last period"
)
col2.metric(
    "Units Sold",
    f"{total_units:,}",
    delta=f"+{int(total_units * 0.08):,}"
)
col3.metric(
    "Orders",
    f"{total_orders:,}",
    delta=f"+{int(total_orders * 0.05):,}"
)
col4.metric(
    "Unique Customers",
    f"{unique_customers:,}",
    delta=f"+{int(unique_customers * 0.03):,}"
)

# Charts Row
st.subheader("Revenue Analysis")

col1, col2 = st.columns(2)

with col1:
    # Revenue trend
    daily_revenue = filtered_df.groupby("date")["revenue"].sum().reset_index()
    fig_trend = px.line(
        daily_revenue,
        x="date",
        y="revenue",
        title="Daily Revenue Trend"
    )
    fig_trend.update_layout(hovermode="x unified")
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    # Revenue by category
    category_revenue = filtered_df.groupby("category")["revenue"].sum().reset_index()
    fig_category = px.pie(
        category_revenue,
        values="revenue",
        names="category",
        title="Revenue by Category"
    )
    st.plotly_chart(fig_category, use_container_width=True)

# Second charts row
col1, col2 = st.columns(2)

with col1:
    # Regional comparison
    regional_data = filtered_df.groupby("region").agg({
        "revenue": "sum",
        "units": "sum"
    }).reset_index()

    fig_region = px.bar(
        regional_data,
        x="region",
        y="revenue",
        color="region",
        title="Revenue by Region"
    )
    st.plotly_chart(fig_region, use_container_width=True)

with col2:
    # Category by region heatmap
    pivot_data = filtered_df.pivot_table(
        values="revenue",
        index="category",
        columns="region",
        aggfunc="sum"
    )

    fig_heatmap = px.imshow(
        pivot_data,
        title="Revenue Heatmap: Category vs Region",
        color_continuous_scale="Blues",
        text_auto=".0f"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

# Data Table
st.subheader("Detailed Data")

with st.expander("View Raw Data"):
    # Aggregated summary
    summary = filtered_df.groupby(["date", "category", "region"]).agg({
        "revenue": "sum",
        "units": "sum",
        "customer_id": "nunique"
    }).reset_index()
    summary.columns = ["Date", "Category", "Region", "Revenue", "Units", "Customers"]

    st.dataframe(
        summary.sort_values("Date", ascending=False),
        use_container_width=True,
        height=400
    )

    # Download button
    csv = summary.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"sales_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
```

### Example 2: Data Explorer Tool

```python
import streamlit as st
import pandas as pd
import polars as pl
import plotly.express as px

st.set_page_config(page_title="Data Explorer", page_icon="🔍", layout="wide")

st.title("🔍 Interactive Data Explorer")

# File upload
uploaded_file = st.file_uploader(
    "Upload your data file",
    type=["csv", "xlsx", "parquet"],
    help="Supported formats: CSV, Excel, Parquet"
)

@st.cache_data
def load_uploaded_file(file, file_type):
    """Load uploaded file based on type."""
    if file_type == "csv":
        return pd.read_csv(file)
    elif file_type == "xlsx":
        return pd.read_excel(file)
    elif file_type == "parquet":
        return pd.read_parquet(file)

if uploaded_file is not None:
    # Determine file type
    file_type = uploaded_file.name.split(".")[-1].lower()

    # Load data
    with st.spinner("Loading data..."):
        df = load_uploaded_file(uploaded_file, file_type)

    st.success(f"Loaded {len(df):,} rows and {len(df.columns)} columns")

    # Data overview tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Overview",
        "📊 Visualize",
        "🔢 Statistics",
        "🔍 Filter & Export"
    ])

    with tab1:
        st.subheader("Data Preview")
        st.dataframe(df.head(100), use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.write("**Column Types:**")
            type_df = pd.DataFrame({
                "Column": df.columns,
                "Type": df.dtypes.astype(str),
                "Non-Null": df.notna().sum(),
                "Null %": (df.isna().sum() / len(df) * 100).round(2)
            })
            st.dataframe(type_df, use_container_width=True)

        with col2:
            st.write("**Data Shape:**")
            st.write(f"- Rows: {len(df):,}")
            st.write(f"- Columns: {len(df.columns)}")
            st.write(f"- Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    with tab2:
        st.subheader("Quick Visualizations")

        # Get column types
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

        chart_type = st.selectbox(
            "Chart Type",
            ["Histogram", "Scatter", "Line", "Bar", "Box Plot"]
        )

        if chart_type == "Histogram":
            col = st.selectbox("Select column", numeric_cols)
            bins = st.slider("Number of bins", 10, 100, 30)
            fig = px.histogram(df, x=col, nbins=bins, title=f"Distribution of {col}")
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Scatter":
            col1, col2 = st.columns(2)
            x_col = col1.selectbox("X axis", numeric_cols)
            y_col = col2.selectbox("Y axis", numeric_cols, index=min(1, len(numeric_cols)-1))
            color_col = st.selectbox("Color by (optional)", ["None"] + categorical_cols)

            fig = px.scatter(
                df, x=x_col, y=y_col,
                color=None if color_col == "None" else color_col,
                title=f"{y_col} vs {x_col}"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Line":
            x_col = st.selectbox("X axis", df.columns.tolist())
            y_cols = st.multiselect("Y axis (select multiple)", numeric_cols)
            if y_cols:
                fig = px.line(df, x=x_col, y=y_cols, title="Line Chart")
                st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Bar":
            cat_col = st.selectbox("Category", categorical_cols if categorical_cols else df.columns.tolist())
            val_col = st.selectbox("Value", numeric_cols)
            agg_func = st.selectbox("Aggregation", ["sum", "mean", "count", "median"])

            agg_data = df.groupby(cat_col)[val_col].agg(agg_func).reset_index()
            fig = px.bar(agg_data, x=cat_col, y=val_col, title=f"{agg_func.title()} of {val_col} by {cat_col}")
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Box Plot":
            val_col = st.selectbox("Value", numeric_cols)
            group_col = st.selectbox("Group by (optional)", ["None"] + categorical_cols)

            fig = px.box(
                df, y=val_col,
                x=None if group_col == "None" else group_col,
                title=f"Distribution of {val_col}"
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Statistical Summary")

        # Numeric statistics
        if numeric_cols:
            st.write("**Numeric Columns:**")
            st.dataframe(df[numeric_cols].describe(), use_container_width=True)

        # Categorical statistics
        if categorical_cols:
            st.write("**Categorical Columns:**")
            for col in categorical_cols[:5]:  # Limit to first 5
                with st.expander(f"{col} value counts"):
                    st.dataframe(
                        df[col].value_counts().head(20).reset_index(),
                        use_container_width=True
                    )

        # Correlation matrix
        if len(numeric_cols) > 1:
            st.write("**Correlation Matrix:**")
            corr = df[numeric_cols].corr()
            fig = px.imshow(
                corr,
                text_auto=".2f",
                color_continuous_scale="RdBu_r",
                aspect="auto"
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("Filter & Export")

        # Dynamic filtering
        st.write("**Apply Filters:**")

        filtered_df = df.copy()

        for col in df.columns[:10]:  # Limit columns for UI
            if df[col].dtype in ["int64", "float64"]:
                min_val, max_val = float(df[col].min()), float(df[col].max())
                if min_val < max_val:
                    range_val = st.slider(
                        f"{col} range",
                        min_val, max_val, (min_val, max_val),
                        key=f"filter_{col}"
                    )
                    filtered_df = filtered_df[
                        (filtered_df[col] >= range_val[0]) &
                        (filtered_df[col] <= range_val[1])
                    ]
            elif df[col].dtype == "object" and df[col].nunique() < 20:
                selected = st.multiselect(
                    f"{col}",
                    options=df[col].unique().tolist(),
                    default=df[col].unique().tolist(),
                    key=f"filter_{col}"
                )
                filtered_df = filtered_df[filtered_df[col].isin(selected)]

        st.write(f"**Filtered data: {len(filtered_df):,} rows**")
        st.dataframe(filtered_df.head(100), use_container_width=True)

        # Export
        col1, col2 = st.columns(2)
        with col1:
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                "Download as CSV",
                csv,
                "filtered_data.csv",
                "text/csv"
            )
        with col2:
            excel_buffer = pd.ExcelWriter("filtered_data.xlsx", engine="openpyxl")
            filtered_df.to_excel(excel_buffer, index=False)

else:
    st.info("Please upload a data file to get started.")

    # Sample data option
    if st.button("Load sample data"):
        import numpy as np
        np.random.seed(42)

        sample_df = pd.DataFrame({
            "date": pd.date_range("2025-01-01", periods=100),
            "category": np.random.choice(["A", "B", "C"], 100),
            "value": np.random.randn(100) * 100 + 500,
            "count": np.random.randint(1, 100, 100)
        })
        sample_df.to_csv("/tmp/sample_data.csv", index=False)
        st.success("Sample data created! Upload '/tmp/sample_data.csv'")
```

### Example 3: ML Model Demo

```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

st.set_page_config(page_title="ML Demo", page_icon="🤖", layout="wide")

st.title("🤖 Machine Learning Model Demo")

# Sidebar
st.sidebar.header("Model Configuration")

# Model parameters
n_estimators = st.sidebar.slider("Number of trees", 10, 200, 100)
max_depth = st.sidebar.slider("Max depth", 1, 20, 5)
test_size = st.sidebar.slider("Test size", 0.1, 0.5, 0.2)

# Generate sample data
@st.cache_data
def generate_sample_data(n_samples=1000):
    np.random.seed(42)

    # Features
    X = pd.DataFrame({
        "feature_1": np.random.randn(n_samples),
        "feature_2": np.random.randn(n_samples),
        "feature_3": np.random.uniform(0, 100, n_samples),
        "feature_4": np.random.choice(["A", "B", "C"], n_samples)
    })

    # Target (based on features with some noise)
    y = (
        (X["feature_1"] > 0).astype(int) +
        (X["feature_3"] > 50).astype(int)
    ) >= 1
    y = y.astype(int)

    return X, y

X, y = generate_sample_data()

# Convert categorical
X_encoded = pd.get_dummies(X, columns=["feature_4"])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=test_size, random_state=42
)

# Train model
@st.cache_resource
def train_model(n_est, depth, _X_train, _y_train):
    model = RandomForestClassifier(
        n_estimators=n_est,
        max_depth=depth,
        random_state=42
    )
    model.fit(_X_train, _y_train)
    return model

# Training
with st.spinner("Training model..."):
    model = train_model(n_estimators, max_depth, X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Results
st.subheader("Model Performance")

col1, col2, col3 = st.columns(3)
col1.metric("Accuracy", f"{accuracy:.2%}")
col2.metric("Training Samples", f"{len(X_train):,}")
col3.metric("Test Samples", f"{len(X_test):,}")

# Feature importance
st.subheader("Feature Importance")
importance_df = pd.DataFrame({
    "Feature": X_encoded.columns,
    "Importance": model.feature_importances_
}).sort_values("Importance", ascending=True)

fig = px.bar(
    importance_df,
    x="Importance",
    y="Feature",
    orientation="h",
    title="Feature Importance"
)
st.plotly_chart(fig, use_container_width=True)

# Interactive prediction
st.subheader("Make a Prediction")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        f1 = st.number_input("Feature 1", value=0.0)
        f2 = st.number_input("Feature 2", value=0.0)

    with col2:
        f3 = st.number_input("Feature 3", min_value=0.0, max_value=100.0, value=50.0)
        f4 = st.selectbox("Feature 4", ["A", "B", "C"])

    submitted = st.form_submit_button("Predict")

    if submitted:
        # Prepare input
        input_data = pd.DataFrame({
            "feature_1": [f1],
            "feature_2": [f2],
            "feature_3": [f3],
            "feature_4": [f4]
        })
        input_encoded = pd.get_dummies(input_data, columns=["feature_4"])

        # Align columns
        for col in X_encoded.columns:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        input_encoded = input_encoded[X_encoded.columns]

        # Predict
        prediction = model.predict(input_encoded)[0]
        proba = model.predict_proba(input_encoded)[0]

        st.success(f"Prediction: **{'Positive' if prediction == 1 else 'Negative'}**")
        st.write(f"Confidence: {max(proba):.2%}")
```

## Deployment Patterns

### Streamlit Cloud Deployment

```yaml
# requirements.txt
streamlit>=1.32.0
pandas>=2.0.0
polars>=0.20.0
plotly>=5.18.0
numpy>=1.24.0
```

```toml
# .streamlit/config.toml
[theme]
primaryColor="#1f77b4"
backgroundColor="#ffffff"
secondaryBackgroundColor="#f0f2f6"
textColor="#262730"
font="sans serif"

[server]
maxUploadSize=200
enableXsrfProtection=true
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
# Build and run
docker build -t my-streamlit-app .
docker run -p 8501:8501 my-streamlit-app
```

## Best Practices

### 1. Use Caching Appropriately

```python
# GOOD: Cache data loading
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

# GOOD: Cache resources (DB connections, models)
@st.cache_resource
def get_model():
    return load_model("model.pkl")

# AVOID: Caching with unhashable arguments
# Use _arg prefix to skip hashing
@st.cache_data
def process_data(_db_connection, query):
    return _db_connection.execute(query)
```

### 2. Organize Large Apps

```python
# utils/data.py
def load_data():
    pass

# utils/charts.py
def create_chart(df):
    pass

# app.py
from utils.data import load_data
from utils.charts import create_chart
```

### 3. Handle State Carefully

```python
# GOOD: Initialize state at the top
if "data" not in st.session_state:
    st.session_state.data = None

# GOOD: Use callbacks for complex updates
def on_filter_change():
    st.session_state.filtered_data = apply_filter(st.session_state.data)

st.selectbox("Filter", options, on_change=on_filter_change)
```

### 4. Optimize Performance

```python
# Use containers for layout stability
placeholder = st.empty()

# Batch widget updates in forms
with st.form("filters"):
    # Multiple widgets
    st.form_submit_button()

# Use columns for responsive layout
cols = st.columns([1, 2, 1])
```

## Troubleshooting

### Common Issues

**Issue: App reruns on every interaction**
```python
# Use forms to batch inputs
with st.form("my_form"):
    input1 = st.text_input("Input")
    submit = st.form_submit_button()
```

**Issue: Slow data loading**
```python
# Add caching
@st.cache_data(ttl=3600)
def load_data():
    return pd.read_csv("large_file.csv")
```

**Issue: Memory issues with large files**
```python
# Use chunking
@st.cache_data
def load_large_file(path, nrows=10000):
    return pd.read_csv(path, nrows=nrows)
```

**Issue: Widget state lost on rerun**
```python
# Persist in session state
if "value" not in st.session_state:
    st.session_state.value = default_value

# Use key parameter
st.text_input("Name", key="user_name")
```

## Version History

- **1.0.0** (2026-01-17): Initial release
  - Basic app structure and widgets
  - Layout and organization patterns
  - Data visualization integration
  - Caching strategies
  - Session state management
  - Multi-page applications
  - Complete dashboard examples
  - Deployment patterns
  - Best practices and troubleshooting

## Resources

- **Official Docs**: https://docs.streamlit.io/
- **Gallery**: https://streamlit.io/gallery
- **Components**: https://streamlit.io/components
- **Cloud**: https://streamlit.io/cloud
- **GitHub**: https://github.com/streamlit/streamlit

---

**Build beautiful data apps with pure Python - no frontend experience required!**
