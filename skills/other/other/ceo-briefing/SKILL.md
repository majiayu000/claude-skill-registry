---
name: ceo-briefing
description: >
  Automated weekly CEO Briefing generation with AI-powered business insights, task analytics,
  proactive suggestions, and cost tracking. Runs every Sunday at 23:00, analyzes completed
  tasks from previous week, calculates Claude API costs, generates actionable suggestions
  via AI, and creates comprehensive briefing in vault/Briefings/. Includes graceful degradation
  when AI unavailable (data-only mode) and manual trigger for testing. Use when: (1) building
  executive reporting for autonomous agents, (2) implementing scheduled analytics with AI
  insights, (3) creating weekly business summaries, (4) tracking API costs and agent activity,
  (5) generating proactive recommendations from historical data.
---

# CEO Briefing

## Architecture

```
Weekly Trigger (Sunday 23:00) → CEO Briefing Generator (ceo_briefing.py)
                                          ↓
                    ┌─────────────────────┴─────────────────────┐
                    ↓                                           ↓
         Vault Analysis                                  AI Insights
    - Tasks completed (week)                        (Claude API)
    - Tasks pending                                  - Proactive
    - API cost (week)                                  suggestions
    - Logs summary                                   - Next week focus
                    ↓                                           ↓
                    └─────────────────────┬─────────────────────┘
                                          ↓
                      vault/Briefings/YYYY-MM-DD_Monday_Briefing.md
```

---

## Quick Start

### 1. CEO Briefing Generator

```python
# scripts/ceo_briefing.py
from datetime import datetime, timedelta
from agent_skills.vault_parser import parse_markdown_file
from anthropic import Anthropic
import os
import glob

def generate_ceo_briefing(force: bool = False):
    """
    Generate weekly CEO Briefing

    Args:
        force: Manual trigger (bypass Sunday check)
    """

    # Check if Sunday OR force flag
    if not force and datetime.now().weekday() != 6:  # 6 = Sunday
        print("❌ CEO Briefing only runs on Sundays (use --force to override)")
        return

    # Calculate previous week (Monday-Sunday)
    today = datetime.now()
    last_monday = today - timedelta(days=today.weekday() + 7)
    last_sunday = last_monday + timedelta(days=6)

    week_start = last_monday.strftime('%Y-%m-%d')
    week_end = last_sunday.strftime('%Y-%m-%d')

    print(f"📊 Generating CEO Briefing for week: {week_start} to {week_end}")

    # Gather data
    briefing_data = {
        "week_start": week_start,
        "week_end": week_end,
        "tasks_completed": count_completed_tasks(week_start, week_end),
        "tasks_pending": count_pending_tasks(),
        "tasks_blocked": count_blocked_tasks(),
        "api_cost_week": calculate_api_cost(week_start, week_end),
        "completed_task_list": get_completed_task_list(week_start, week_end),
        "pending_items": get_pending_items_summary()
    }

    # Generate AI insights
    try:
        ai_insights = generate_ai_insights(briefing_data)
        briefing_data["proactive_suggestions"] = ai_insights["suggestions"]
        briefing_data["next_week_focus"] = ai_insights["focus"]
        briefing_data["generated_by"] = "ai"
    except Exception as e:
        print(f"⚠️  Claude API unavailable: {e}")
        briefing_data["proactive_suggestions"] = ["[API Unavailable - Manual Review Required]"]
        briefing_data["next_week_focus"] = "Data-only briefing - manual analysis needed"
        briefing_data["generated_by"] = "data_only"

    # Create briefing file
    next_monday = last_sunday + timedelta(days=1)
    briefing_path = f"vault/Briefings/{next_monday.strftime('%Y-%m-%d')}_Monday_Briefing.md"

    save_briefing(briefing_path, briefing_data)

    print(f"✅ CEO Briefing created: {briefing_path}")

def count_completed_tasks(week_start: str, week_end: str) -> int:
    """Count tasks in vault/Done/ completed during week"""
    count = 0
    for file_path in glob.glob('vault/Done/*.md'):
        task = parse_markdown_file(file_path)

        # Check completion date
        completed_at = task.get('completed_at', '')
        if week_start <= completed_at <= week_end:
            count += 1

    return count

def count_pending_tasks() -> int:
    """Count tasks in vault/Needs_Action/"""
    return len(list(glob.glob('vault/Needs_Action/*.md')))

def count_blocked_tasks() -> int:
    """Count blocked plans in vault/In_Progress/"""
    count = 0
    for plan_dir in glob.glob('vault/In_Progress/*/'):
        state_file = os.path.join(plan_dir, 'state.md')
        if os.path.exists(state_file):
            state = parse_markdown_file(state_file)
            if state.get('status') == 'blocked':
                count += 1
    return count

def calculate_api_cost(week_start: str, week_end: str) -> float:
    """Calculate total Claude API cost for week"""
    total_cost = 0.0

    # Read API usage logs
    for log_file in glob.glob('vault/Logs/API_Usage/*.md'):
        log = parse_markdown_file(log_file)

        # Check if log is within week
        log_date = log.get('timestamp', '')[:10]  # YYYY-MM-DD
        if week_start <= log_date <= week_end:
            total_cost += log.get('cost_usd', 0.0)

    return round(total_cost, 4)

def get_completed_task_list(week_start: str, week_end: str) -> list:
    """Get list of completed tasks with file links"""
    tasks = []

    for file_path in glob.glob('vault/Done/*.md'):
        task = parse_markdown_file(file_path)

        completed_at = task.get('completed_at', '')
        if week_start <= completed_at <= week_end:
            tasks.append({
                "filename": os.path.basename(file_path),
                "title": task.get('title', 'Untitled'),
                "completed_at": completed_at
            })

    # Sort by completion date
    tasks.sort(key=lambda t: t['completed_at'])
    return tasks

def get_pending_items_summary() -> list:
    """Get summary of vault/Needs_Action/ items"""
    items = []

    for file_path in glob.glob('vault/Needs_Action/*.md'):
        item = parse_markdown_file(file_path)
        items.append({
            "filename": os.path.basename(file_path),
            "title": item.get('title', 'Untitled'),
            "severity": item.get('severity', 'medium')
        })

    return items
```

---

## AI Insights Generation

```python
def generate_ai_insights(briefing_data: dict) -> dict:
    """Generate proactive suggestions via Claude API"""

    client = Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))

    # Build context
    context = f"""
Week: {briefing_data['week_start']} to {briefing_data['week_end']}

Completed Tasks: {briefing_data['tasks_completed']}
Pending Tasks: {briefing_data['tasks_pending']}
Blocked Plans: {briefing_data['tasks_blocked']}
API Cost (week): ${briefing_data['api_cost_week']}

Pending Items:
{format_pending_items(briefing_data['pending_items'])}

Completed Tasks:
{format_completed_tasks(briefing_data['completed_task_list'][:10])}  # Top 10
"""

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": f"""Analyze this week's AI assistant activity and provide:

{context}

Generate:
1. **Proactive Suggestions** (3-5 actionable items based on patterns, bottlenecks, pending items)
2. **Next Week Focus** (1-2 priority areas for the coming week)

Requirements:
- Specific, actionable suggestions
- Reference actual data (pending items, blocked plans)
- Business-focused (not technical)
- Concise (2-3 sentences each)

Format:
SUGGESTIONS:
1. [Suggestion 1]
2. [Suggestion 2]
...

FOCUS:
[Next week focus paragraph]
"""
        }]
    )

    # Parse response
    text = response.content[0].text

    suggestions_match = re.search(r'SUGGESTIONS:\n(.*?)\n\nFOCUS:', text, re.DOTALL)
    focus_match = re.search(r'FOCUS:\n(.*)', text, re.DOTALL)

    suggestions = []
    if suggestions_match:
        suggestions_text = suggestions_match.group(1)
        suggestions = [s.strip() for s in re.findall(r'\d+\.\s+(.*)', suggestions_text)]

    focus = focus_match.group(1).strip() if focus_match else "Continue current priorities"

    return {
        "suggestions": suggestions,
        "focus": focus
    }

def format_pending_items(items: list) -> str:
    """Format pending items for AI context"""
    if not items:
        return "None"

    return '\n'.join([
        f"- {item['title']} (severity: {item['severity']})"
        for item in items[:5]  # Top 5
    ])

def format_completed_tasks(tasks: list) -> str:
    """Format completed tasks for AI context"""
    if not tasks:
        return "None"

    return '\n'.join([
        f"- {task['title']}"
        for task in tasks
    ])
```

---

## Briefing File Format

```python
def save_briefing(path: str, data: dict):
    """Save CEO Briefing to vault/Briefings/"""

    content = f"""---
briefing_date: {data['week_end']}
week_start: {data['week_start']}
week_end: {data['week_end']}
tasks_completed_count: {data['tasks_completed']}
tasks_pending_count: {data['tasks_pending']}
api_cost_week: ${data['api_cost_week']}
generated_by: {data['generated_by']}
---

# CEO Briefing - Week of {data['week_start']}

**Reporting Period:** {data['week_start']} to {data['week_end']}

---

## Executive Summary

- **Tasks Completed:** {data['tasks_completed']}
- **Tasks Pending:** {data['tasks_pending']}
- **Blocked Plans:** {data['tasks_blocked']}
- **API Cost (Week):** ${data['api_cost_week']}

---

## Week in Review

### Completed Tasks

{format_completed_tasks_section(data['completed_task_list'])}

---

## Pending Items

{format_pending_items_section(data['pending_items'])}

---

## Proactive Suggestions

{format_suggestions_section(data['proactive_suggestions'])}

---

## Next Week Focus

{data['next_week_focus']}

---

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**AI Analysis:** {'Enabled' if data['generated_by'] == 'ai' else 'Unavailable (Data Only)'}
"""

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

def format_completed_tasks_section(tasks: list) -> str:
    """Format completed tasks with Obsidian wiki links"""
    if not tasks:
        return "No tasks completed this week."

    lines = []
    for task in tasks:
        # Obsidian wiki link format: [[filename|display text]]
        link = f"[[{task['filename']}|{task['title']}]]"
        lines.append(f"- {link} (completed {task['completed_at']})")

    return '\n'.join(lines)

def format_pending_items_section(items: list) -> str:
    """Format pending items with severity"""
    if not items:
        return "✅ No pending items - all clear!"

    lines = []
    for item in sorted(items, key=lambda i: i['severity'], reverse=True):
        severity_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(item['severity'], '⚪')
        lines.append(f"- {severity_icon} [[{item['filename']}|{item['title']}]]")

    return '\n'.join(lines)

def format_suggestions_section(suggestions: list) -> str:
    """Format AI suggestions"""
    if suggestions == ["[API Unavailable - Manual Review Required]"]:
        return "⚠️  **AI analysis unavailable this week - manual review required.**"

    return '\n'.join([f"{i+1}. {s}" for i, s in enumerate(suggestions)])
```

---

## Scheduled Execution

### Schedule Library

```python
# Run as background service
import schedule
import time

def run_ceo_briefing_scheduler():
    """Schedule CEO Briefing for Sunday 23:00"""

    schedule.every().sunday.at("23:00").do(generate_ceo_briefing)

    print("📅 CEO Briefing scheduled for Sundays at 23:00")

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true', help='Force generation (bypass Sunday check)')
    parser.add_argument('--schedule', action='store_true', help='Run scheduler (background service)')

    args = parser.parse_args()

    if args.schedule:
        run_ceo_briefing_scheduler()
    else:
        generate_ceo_briefing(force=args.force)
```

**Manual Trigger:**
```bash
# Test generation immediately
python scripts/ceo_briefing.py --force

# Run scheduler (background service)
python scripts/ceo_briefing.py --schedule
```

---

## Cost Tracking

### API Usage Logging

```python
# Called from draft_generator.py after each Claude API call
def log_api_usage(model: str, prompt_tokens: int, completion_tokens: int):
    """Log Claude API usage for cost tracking"""

    # Calculate cost (Claude Sonnet 4.5 pricing)
    PRICE_INPUT = 0.003 / 1000  # $3 per million input tokens
    PRICE_OUTPUT = 0.015 / 1000  # $15 per million output tokens

    cost_usd = (prompt_tokens * PRICE_INPUT) + (completion_tokens * PRICE_OUTPUT)

    log_entry = f"""---
request_id: {uuid.uuid4()}
model: {model}
prompt_tokens: {prompt_tokens}
completion_tokens: {completion_tokens}
cost_usd: {cost_usd}
timestamp: {datetime.utcnow().isoformat()}
---

# API Usage Log

**Model:** {model}
**Tokens:** {prompt_tokens} (input) + {completion_tokens} (output)
**Cost:** ${cost_usd:.4f}
"""

    # Append to today's API usage log
    log_path = f"vault/Logs/API_Usage/{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(log_path, 'a') as f:
        f.write(log_entry)

    # Check daily thresholds
    check_cost_alerts()

def check_cost_alerts():
    """Alert if daily API cost exceeds thresholds"""
    today = datetime.now().strftime('%Y-%m-%d')
    daily_cost = calculate_api_cost(today, today)

    thresholds = [0.10, 0.25, 0.50]  # Alert at $0.10, $0.25, $0.50

    for threshold in thresholds:
        alert_file = f"vault/Needs_Action/api_cost_alert_{threshold}.md"

        if daily_cost >= threshold and not os.path.exists(alert_file):
            # Create alert
            with open(alert_file, 'w') as f:
                f.write(f"""---
severity: medium
cost_threshold: ${threshold}
current_cost: ${daily_cost}
---

# API Cost Alert

Daily Claude API cost has reached **${daily_cost:.4f}** (threshold: ${threshold}).

Consider optimizing API usage or adjusting thresholds.
""")
```

---

## Testing

```python
# tests/integration/test_ceo_briefing.py
def test_ceo_briefing_generation():
    """Test CEO Briefing creation with mock data"""

    # Create mock completed tasks
    create_mock_completed_tasks(count=15)

    # Create mock pending items
    create_mock_pending_items(count=3)

    # Mock Claude API
    with patch('anthropic.Anthropic.messages.create') as mock_claude:
        mock_claude.return_value.content = [{
            "text": """
SUGGESTIONS:
1. Review blocked plans in vault/In_Progress/
2. Address 3 high-priority pending items
3. Optimize email draft generation (reduce API calls)

FOCUS:
Focus on clearing pending items backlog and optimizing API cost efficiency.
"""
        }]

        # Generate briefing
        briefing_path = generate_ceo_briefing(force=True)

        # Verify briefing created
        assert os.path.exists(briefing_path)

        # Verify content
        briefing = parse_markdown_file(briefing_path)
        assert briefing['tasks_completed_count'] == 15
        assert briefing['tasks_pending_count'] == 3
        assert briefing['generated_by'] == 'ai'
```

---

## Configuration

```bash
# .env
CLAUDE_API_KEY=sk-ant-api03-...

# Optional: Customize briefing
CEO_BRIEFING_DAY=Sunday
CEO_BRIEFING_TIME=23:00
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Briefing not generated** | Check Sunday schedule OR use `--force` |
| **API unavailable** | Data-only briefing created - manual analysis |
| **Empty briefing** | No tasks completed - check vault/Done/ |
| **Cost tracking wrong** | Verify API usage logs in vault/Logs/API_Usage/ |

---

## Key Files

- `scripts/ceo_briefing.py` - Generator and scheduler
- `vault/Briefings/` - Weekly briefings
- `vault/Logs/API_Usage/` - Cost tracking logs
- `vault/Done/` - Completed tasks (data source)
- `vault/Needs_Action/` - Pending items (data source)

---

**Production Ready:** Scheduled execution, AI insights with fallback, cost tracking, comprehensive analytics, Obsidian-compatible formatting.
