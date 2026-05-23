---
name: Manus AI Agent Integration
description: Use this skill when delegating complex autonomous tasks to Manus AI - an AI agent that can browse the web, execute code, generate files, and comple...
allowed-tools: Bash, Read, Grep
---

# Manus AI Agent Integration

Use this skill when delegating complex autonomous tasks to Manus AI - an AI agent that can browse the web, execute code, generate files, and complete multi-step workflows independently.

## When to Use Manus

- **Research tasks**: Market research, competitor analysis, fact-checking
- **Content creation**: Presentations, videos, websites, documents
- **Data processing**: PDF translation, data analysis, report generation
- **Development**: Chrome extensions, proof of concepts, prototypes
- **Planning**: Trip planning, fitness plans, business strategies

## API Reference

### Base URL
```
https://api.manus.ai/v1
```

### Authentication
```bash
# Header authentication
API_KEY: your-api-key
```

### Create Task
```bash
POST /v1/tasks
Content-Type: application/json
API_KEY: $MANUS_API_KEY

{
  "prompt": "Your task description",
  "agentProfile": "manus-1.5",  # manus-1.5 | manus-1.5-lite | speed | quality
  "taskMode": "agent",          # agent | chat | adaptive (optional)
  "projectId": "proj_xxx",      # optional
  "connectors": ["uuid1"],      # optional - gmail, calendar, notion
  "attachments": []             # optional - files, URLs, base64
}
```

**Response:**
```json
{
  "task_id": "TeBim6FDQf9peS52xHtAyh",
  "task_title": "Generated Title",
  "task_url": "https://manus.im/app/TeBim6FDQf9peS52xHtAyh"
}
```

### Agent Profiles
| Profile | Best For |
|---------|----------|
| `manus-1.5` | Full capabilities - browsing, code, files (default) |
| `manus-1.5-lite` | Lighter tasks, faster response |
| `speed` | Quick responses, simpler tasks |
| `quality` | Complex research, detailed outputs |

### Create Project
```bash
POST /v1/projects

{
  "name": "Project Name",
  "instruction": "Default instruction for all tasks in this project"
}
```

### Webhooks

Register webhook for real-time notifications:
```bash
POST /v1/webhooks
{"url": "https://your-server.com/webhook"}
```

**Webhook Events:**
- `task_created` - Task started
- `task_progress` - Task making progress (plan updates)
- `task_stopped` - Task completed or needs input

**Webhook Payload (task_stopped):**
```json
{
  "event_type": "task_stopped",
  "task_detail": {
    "task_id": "xxx",
    "task_title": "...",
    "task_url": "https://manus.im/app/xxx",
    "message": "Completion message",
    "attachments": [
      {"file_name": "report.pdf", "url": "...", "size_bytes": 1234}
    ],
    "stop_reason": "finish"  # or "ask" if needs input
  }
}
```

## CLI Usage

The `manus` CLI is installed at `~/.local/bin/manus`:

```bash
# Set API key
export MANUS_API_KEY="sk-xxx"

# Create simple task
manus task "Summarize AI news from this week"

# Use quality mode for research
manus task -m quality "Research iOS 26 SwiftUI changes"

# Use playbook template
manus playbook use market-research "electric vehicles"
manus playbook use slide-generator "quarterly report"
manus playbook use video-generator "product demo"

# List all playbook templates
manus playbook list

# Create project with instruction
manus project create "Q4 Research" "Always cite sources"

# Task within project
manus task -p proj_xxx "Research task"

# Webhook management
manus webhook add https://my-server.com/hook
manus webhook remove webhook_id
```

## Playbook Templates

Pre-built prompts for common use cases:

| Template | Use Case |
|----------|----------|
| `market-research` | Comprehensive market analysis reports |
| `slide-generator` | Professional presentations (PPT/PDF) |
| `video-generator` | AI-generated videos from prompts |
| `website-builder` | Build complete websites |
| `resume-builder` | Professional resumes |
| `swot-analysis` | Business SWOT analysis |
| `chrome-extension` | Browser extension development |
| `trip-planner` | Travel itineraries |
| `influencer-finder` | YouTube creator discovery |
| `fact-checker` | Claim verification |
| `pdf-translator` | Document translation |
| `interior-design` | Room/space design |
| `fitness-coach` | Custom workout plans |
| `startup-poc` | Proof of concept prototypes |
| `profile-builder` | Research profiles on people/companies |
| `sentiment-analyzer` | Reddit sentiment analysis |
| `viral-content` | YouTube viral content analysis |
| `business-canvas` | Business model canvas |

## Integration Patterns

### From Claude Code via CLI
```bash
# Execute via Bash tool
manus task -m quality "Research SwiftUI changes in iOS 26 and create a migration checklist"
```

### Direct API Call
```bash
curl -X POST "https://api.manus.ai/v1/tasks" \
  -H "API_KEY: $MANUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Analyze this codebase and suggest improvements",
    "agentProfile": "quality"
  }'
```

### With Attachments
```json
{
  "prompt": "Analyze this data",
  "attachments": [
    {"type": "url", "url": "https://example.com/data.csv"},
    {"type": "base64", "data": "...", "mimeType": "text/csv", "fileName": "data.csv"}
  ]
}
```

### With Connectors
Available connectors (OAuth required at manus.im):
- Gmail - Email access
- Google Calendar - Calendar events
- Notion - Workspace access
- More at: https://manus.im/app?show_settings=integrations

```json
{
  "prompt": "Schedule a meeting based on my calendar availability",
  "connectors": ["calendar-connector-uuid"]
}
```

## Webhook Server Example

Simple Python webhook receiver:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    event = request.json
    event_type = event.get('event_type')

    if event_type == 'task_created':
        print(f"Task started: {event['task_detail']['task_id']}")

    elif event_type == 'task_progress':
        print(f"Progress: {event['progress_detail']['message']}")

    elif event_type == 'task_stopped':
        detail = event['task_detail']
        if detail['stop_reason'] == 'finish':
            print(f"Completed: {detail['message']}")
            for att in detail.get('attachments', []):
                print(f"  File: {att['file_name']} - {att['url']}")
        else:
            print(f"Needs input: {detail['message']}")

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(port=8080)
```

## Error Codes

| Code | Message | Solution |
|------|---------|----------|
| 8 | credit limit exceeded | Add credits at manus.im |
| 401 | unauthorized | Check API_KEY |
| 400 | bad request | Validate JSON payload |

## Best Practices

1. **Use quality mode** for complex research tasks
2. **Use projects** to group related tasks with shared instructions
3. **Set up webhooks** for async task monitoring
4. **Include context** in prompts - Manus works better with specific details
5. **Use playbooks** for common workflows - they're optimized prompts

## Hybrid Workflow (Claude Code + Manus)

Use the `ai-delegate` CLI to intelligently route tasks:

```bash
# Analyze where a task should go
ai-delegate analyze "scrape competitor reviews from App Store"
ai-delegate analyze "refactor BibleService to use async/await"

# Auto-route based on analysis
ai-delegate run "your task description"

# Force routing
ai-delegate manus "generate PDF report"
ai-delegate local "implement dark mode"

# See capability comparison
ai-delegate compare
```

### Routing Logic

**Use Claude Code (free, instant) for:**
- Code generation, editing, refactoring
- File operations (read/write/search)
- Git operations, GitHub PRs
- Supabase database queries
- Web search, simple page fetching
- Apple docs via Sosumi MCP
- Memory persistence

**Use Manus (costs credits) for:**
- Browser automation (JS-rendered sites)
- Form filling, login-required scraping
- PDF/slide/video generation
- OAuth integrations (Gmail, Calendar)
- Multi-hour autonomous research
- Real purchases/bookings

### Hybrid Example

Task: "Research competitor Bible apps and create a comparison report"

1. **Claude Code**: Web search for competitor list
2. **Claude Code**: Fetch public landing pages
3. **Manus**: Scrape App Store reviews (JS-rendered)
4. **Claude Code**: Analyze and structure data
5. **Manus**: Generate polished PDF report
6. **Claude Code**: Save to local files, commit to git

## Resources

- API Docs: https://open.manus.ai/docs
- Playbook Gallery: https://manus.im/playbook
- API Settings: https://manus.im/app?show_settings=integrations&app_name=api
- Webhook Setup: https://manus.im/app?show_settings=integrations
