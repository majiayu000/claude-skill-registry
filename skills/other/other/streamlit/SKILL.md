---
name: streamlit
description: Build interactive web UIs for AI agents and chatbots with Streamlit from hello-world to production-ready interfaces. Use when working with (1) Chat interfaces with st.chat_input, st.chat_message, streaming responses, (2) AI agent dashboards for monitoring autonomous employees, (3) Human-in-the-loop approval workflows with forms and buttons, (4) Agent configuration panels with settings and parameters, (5) Conversation history and session state management, (6) Status indicators and progress bars for agent activities, (7) Multi-page apps for Personal AI Employee projects. Perfect for Personal AI Employee hackathon projects, Claude Code integrations, agent monitoring dashboards, and conversational AI applications. Covers chat components, UI widgets, layouts, session state, streaming, and production deployment patterns.
---

# Streamlit for AI Agents and Chatbots

Build production-ready web interfaces for AI agents, chatbots, and autonomous systems using Streamlit - the fastest way to create interactive data apps in pure Python.

## When to Use This Skill

Use Streamlit when you need to:

- **Build chatbot interfaces** for AI agents (OpenAI, Anthropic, custom LLMs)
- **Create dashboards** to monitor autonomous AI employees
- **Implement human-in-the-loop workflows** with approval interfaces
- **Visualize agent activities** and conversation histories
- **Configure AI agents** through interactive settings panels
- **Prototype quickly** with minimal frontend code

## Quick Start

### Option 1: Using the Init Script

Create a new chatbot project instantly:

```bash
# Basic chatbot with simulated responses
python scripts/init_chatbot.py my_chatbot --template basic

# Advanced chatbot with OpenAI integration
python scripts/init_chatbot.py my_chatbot --template advanced

cd my_chatbot
pip install -r requirements.txt
streamlit run app.py
```

### Option 2: From Scratch

Minimal chatbot in 30 lines:

```python
import streamlit as st

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Accept user input
if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate response (replace with your LLM)
    response = your_llm_function(prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
```

## Core Patterns for AI Agents

### Pattern 1: Chat Interface with Streaming

Perfect for OpenAI, Anthropic, or any LLM with streaming support:

```python
import streamlit as st
from openai import OpenAI

@st.cache_resource
def get_client():
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

client = get_client()

def stream_response(messages):
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# In your chat loop:
if prompt := st.chat_input("Ask anything"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response = st.write_stream(stream_response(st.session_state.messages))
        st.session_state.messages.append({"role": "assistant", "content": response})
```

### Pattern 2: Human-in-the-Loop Approval Workflow

Essential for Personal AI Employee projects where agents need approval for sensitive actions:

```python
import streamlit as st

if "pending_approvals" not in st.session_state:
    st.session_state.pending_approvals = []

# Agent creates approval request
def request_approval(action_type, details):
    approval = {
        "id": len(st.session_state.pending_approvals),
        "action": action_type,
        "details": details,
        "status": "pending"
    }
    st.session_state.pending_approvals.append(approval)

# Display approval interface
st.title("Pending Approvals")

for approval in st.session_state.pending_approvals:
    if approval["status"] == "pending":
        with st.container():
            st.subheader(f"{approval['action']} Request")
            st.json(approval["details"])

            col1, col2 = st.columns(2)
            if col1.button("✅ Approve", key=f"approve_{approval['id']}"):
                approval["status"] = "approved"
                # Execute the approved action
                execute_action(approval)
                st.success("Action approved and executed!")
                st.rerun()

            if col2.button("❌ Reject", key=f"reject_{approval['id']}"):
                approval["status"] = "rejected"
                st.warning("Action rejected")
                st.rerun()
```

### Pattern 3: Agent Configuration Panel

Create a sidebar for configuring AI agent behavior:

```python
import streamlit as st

with st.sidebar:
    st.title("⚙️ Agent Configuration")

    # Model settings
    st.subheader("Model Settings")
    model = st.selectbox("Model", ["gpt-4", "gpt-3.5-turbo", "claude-3-sonnet"])
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.number_input("Max tokens", 100, 4000, 2000)

    # System prompt
    st.subheader("System Prompt")
    system_prompt = st.text_area(
        "Customize agent behavior",
        value="You are a helpful assistant.",
        height=100
    )

    # Tools and capabilities
    st.subheader("Capabilities")
    enable_web_search = st.checkbox("Enable web search")
    enable_code_exec = st.checkbox("Enable code execution")
    enable_file_ops = st.checkbox("Enable file operations")

    # Actions
    st.divider()
    if st.button("Reset to defaults", use_container_width=True):
        # Reset logic
        st.rerun()
```

### Pattern 4: Agent Dashboard

Monitor autonomous AI employee activities:

```python
import streamlit as st
from datetime import datetime

st.set_page_config(layout="wide")

# Metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Tasks Completed", "47", "+3")
col2.metric("Pending Approvals", "2", "0")
col3.metric("Active Watchers", "3/3", "✓")
col4.metric("Revenue This Week", "$2,450", "+12%")

# Activity timeline
st.subheader("Recent Activity")
activities = [
    {"time": "10:45 AM", "action": "Invoice sent to Client A", "status": "✅"},
    {"time": "10:30 AM", "action": "Email draft created", "status": "⏳"},
    {"time": "09:15 AM", "action": "WhatsApp message processed", "status": "✅"}
]

for activity in activities:
    col1, col2, col3 = st.columns([2, 6, 1])
    col1.write(activity["time"])
    col2.write(activity["action"])
    col3.write(activity["status"])

# Pending approvals section
st.subheader("Pending Approvals")
# Implementation from Pattern 2...

# Live logs
with st.expander("Agent Logs"):
    st.code("""
    [2026-01-07 10:45:00] INFO: Email sent successfully
    [2026-01-07 10:30:00] INFO: Draft created: Invoice for Client A
    [2026-01-07 09:15:00] INFO: Processed WhatsApp message
    """, language="log")
```

## Key Components

All components are documented with official examples in the reference files. Key components include:

**Chat Components:** (See `references/chat-components.md`)
- `st.chat_input` - Accept user messages
- `st.chat_message` - Display messages with roles
- `st.write_stream` - Stream responses with typewriter effect
- `st.feedback` - Collect user feedback on responses

**UI Components:** (See `references/ui-components.md`)
- Input widgets (text, numbers, sliders, selects)
- Buttons and forms for actions
- File uploaders for document processing
- Layouts (columns, sidebar, tabs, expanders)

**Session State:** (See `references/session-state.md`)
- Managing conversation history
- Multi-stage workflows
- Persistent settings
- Avoiding common pitfalls

**Configuration:** (See `references/app-config.md`)
- Page setup and styling
- Themes and custom CSS
- Secrets management
- Caching and performance

## Integration Examples

### OpenAI Integration

```python
from openai import OpenAI
import streamlit as st

@st.cache_resource
def get_openai_client():
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

client = get_openai_client()

def chat(messages):
    return client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        stream=True
    )
```

### Anthropic Claude Integration

```python
from anthropic import Anthropic
import streamlit as st

@st.cache_resource
def get_claude_client():
    return Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

client = get_claude_client()

def chat(messages):
    with client.messages.stream(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=messages
    ) as stream:
        for text in stream.text_stream:
            yield text
```

### OpenAI Agents SDK Integration

```python
from agents import Agent
import streamlit as st

@st.cache_resource
def get_agent():
    return Agent(
        name="assistant",
        model="gpt-4",
        instructions="You are a helpful assistant."
    )

agent = get_agent()

def chat(thread_id, message):
    return agent.stream_run(thread_id=thread_id, input=message)
```

## Personal AI Employee Use Cases

Based on the hackathon requirements, here are common Streamlit patterns:

### Use Case 1: CEO Briefing Dashboard

Display autonomous business audit results:

```python
st.title("📊 Monday Morning CEO Briefing")

# Executive summary
st.subheader("Executive Summary")
st.success("Strong week with revenue ahead of target. One bottleneck identified.")

# Revenue metrics
col1, col2, col3 = st.columns(3)
col1.metric("This Week", "$2,450")
col2.metric("MTD", "$4,500", "45% of target")
col3.metric("Trend", "On track", "✓")

# Bottlenecks table
st.subheader("Bottlenecks")
st.dataframe([
    {"Task": "Client B proposal", "Expected": "2 days", "Actual": "5 days", "Delay": "+3 days"}
])

# Proactive suggestions
st.subheader("Proactive Suggestions")
with st.container():
    st.warning("**Notion**: No team activity in 45 days. Cost: $15/month.")
    if st.button("Cancel subscription? (Needs approval)"):
        request_approval("cancel_subscription", {"service": "Notion", "cost": 15})
```

### Use Case 2: Watcher Status Monitor

Monitor Gmail, WhatsApp, and other watchers:

```python
st.title("🔍 Watcher Status")

watchers = [
    {"name": "Gmail", "status": "running", "last_check": "2 min ago", "items": 3},
    {"name": "WhatsApp", "status": "running", "last_check": "30 sec ago", "items": 0},
    {"name": "File System", "status": "error", "last_check": "5 min ago", "items": 0}
]

for watcher in watchers:
    col1, col2, col3, col4 = st.columns([2, 1, 2, 1])
    col1.write(f"**{watcher['name']}**")

    if watcher["status"] == "running":
        col2.success("Running")
    else:
        col2.error("Error")

    col3.write(f"Last check: {watcher['last_check']}")
    col4.metric("Items", watcher["items"])
```

### Use Case 3: Task Approval Interface

Human-in-the-loop for sensitive actions:

```python
st.title("✋ Pending Approvals")

# Payment approval
with st.container():
    st.subheader("💰 Payment Request")
    st.write("**Amount:** $500.00")
    st.write("**To:** Client A (Bank: XXXX1234)")
    st.write("**Reference:** Invoice #1234")

    col1, col2 = st.columns(2)
    if col1.button("✅ Approve Payment", type="primary"):
        # Execute payment via MCP
        st.success("Payment approved and executed!")

    if col2.button("❌ Reject"):
        st.warning("Payment rejected")

# Email approval
with st.container():
    st.subheader("📧 Email Draft")
    st.write("**To:** new.client@example.com")
    st.write("**Subject:** Proposal for Q1 Project")

    with st.expander("View draft"):
        st.text_area("Email body", value="Dear Client,\n\n...")

    col1, col2, col3 = st.columns(3)
    if col1.button("Send"):
        st.success("Email sent!")
    if col2.button("Edit"):
        st.info("Opening editor...")
    if col3.button("Discard"):
        st.warning("Draft discarded")
```

## Production Deployment

### Local Development

```bash
streamlit run app.py
```

### Streamlit Cloud (Free)

1. Push code to GitHub
2. Visit share.streamlit.io
3. Connect repository
4. Add secrets in app settings
5. Deploy

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

### Custom Server

```bash
# Production server with custom port
streamlit run app.py --server.port 8080 --server.address 0.0.0.0
```

## Reference Files

For detailed component documentation and examples:

- **chat-components.md** - Complete chat interface patterns
- **ui-components.md** - All widgets, layouts, and display elements
- **session-state.md** - State management patterns and best practices
- **app-config.md** - Configuration, styling, secrets, and performance

## Templates

Pre-built templates in `assets/`:

- **basic-chatbot/** - Minimal chatbot with simulated responses
- **advanced-chatbot/** - Production-ready OpenAI chatbot with feedback

## Common Patterns Summary

1. **Always set page config first** - Before any other Streamlit command
2. **Initialize session state** - Check existence before using variables
3. **Use st.cache_resource** - Cache LLM clients and heavy objects
4. **Stream responses** - Use `st.write_stream` for better UX
5. **Sidebar for settings** - Keep main area for chat/content
6. **Human-in-the-loop** - Always require approval for sensitive actions
7. **Error handling** - Wrap LLM calls in try/except with user-friendly messages

## Troubleshooting

**Chat input not working:**
- Ensure session state is initialized before rendering chat_input
- Check that prompt variable is being used correctly

**Page keeps rerunning:**
- Avoid calling `st.rerun()` in loops
- Ensure widget keys are unique

**Streaming not showing:**
- Verify generator function yields strings
- Check that streaming is enabled in LLM API call

**Secrets not found:**
- Create `.streamlit/secrets.toml` file
- Never commit secrets to version control
- For production, use Streamlit Cloud secrets management

## Next Steps

1. **Start simple** - Use basic template, get it running
2. **Add your LLM** - Replace simulated responses with real API calls
3. **Customize UI** - Adjust layout, styling, and components
4. **Add features** - Feedback, history export, multi-agent support
5. **Deploy** - Streamlit Cloud, Docker, or custom server

For the Personal AI Employee hackathon, consider building:
- Agent monitoring dashboard (Gold/Platinum tier)
- Approval interface for HITL workflows (Silver/Gold tier)
- CEO briefing visualization (Gold tier)
- Conversation export and analysis tools

---

**Official Documentation:** https://docs.streamlit.io/
**GitHub:** https://github.com/streamlit/streamlit
**Community:** https://discuss.streamlit.io/
