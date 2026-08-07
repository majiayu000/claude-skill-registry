---
name: cc-analytics
description: Use when user asks for Claude Code usage stats, weekly analytics, project activity summary, or wants to see what projects were worked on. Triggers on "аналитика", "статистика claude", "cc stats", "weekly report", "что делал"
---

# Claude Code Analytics

Generate HTML report of Claude Code usage from `~/.claude/history.jsonl`.

## Data Sources

- **History:** `~/.claude/history.jsonl` — prompts with timestamps and project paths
- **Git:** Remote URLs and commit counts per project

## Output

Single HTML file with terminal aesthetic:
- ASCII art header
- Summary stats (projects, prompts, commits, days)
- Project table with remote links
- ASCII bar chart

## Generation Script

Run this Python script to generate the report:

```python
import json
import os
import subprocess
from datetime import datetime, timedelta
from collections import defaultdict

def get_git_info(path):
    if not os.path.isdir(path) or not os.path.exists(os.path.join(path, '.git')):
        return None, 0
    try:
        result = subprocess.run(['git', '-C', path, 'remote', 'get-url', 'origin'],
                                capture_output=True, text=True, timeout=5)
        remote = result.stdout.strip() if result.returncode == 0 else None
        if remote:
            remote = remote.replace('git@github.com:', 'github.com/').replace('.git', '').replace('https://', '')

        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        result = subprocess.run(['git', '-C', path, 'rev-list', '--count', f'--since={week_ago}', 'HEAD'],
                                capture_output=True, text=True, timeout=5)
        commits = int(result.stdout.strip()) if result.returncode == 0 else 0
        return remote, commits
    except:
        return None, 0

# Parse history
history = []
with open(os.path.expanduser('~/.claude/history.jsonl'), 'r') as f:
    for line in f:
        try:
            history.append(json.loads(line))
        except:
            pass

# Filter last N days (default 7)
days = 7
now = datetime.now()
cutoff = (now - timedelta(days=days)).timestamp() * 1000

projects = defaultdict(lambda: {'prompts': [], 'sessions': set()})
for entry in history:
    ts = entry.get('timestamp', 0)
    if ts >= cutoff:
        project = entry.get('project', 'unknown')
        projects[project]['prompts'].append(entry)
        projects[project]['sessions'].add(datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d'))

# Collect data
results = []
total_commits = 0
for project, data in projects.items():
    remote, commits = get_git_info(project)
    total_commits += commits
    results.append({
        'name': os.path.basename(project) or project.replace('/Users/ris/', '~/'),
        'folder': project.replace('/Users/ris/', '~/'),
        'remote': remote,
        'prompts': len(data['prompts']),
        'sessions': len(data['sessions']),
        'commits': commits
    })

results.sort(key=lambda x: -x['prompts'])
max_prompts = results[0]['prompts'] if results else 1
```

## HTML Template

Use terminal aesthetic with:
- Monospace system fonts: `'SF Mono', 'Monaco', 'Inconsolata', monospace`
- Dark background: `#0d0d0d`
- Muted colors: `#b0b0b0` (text), `#555` (dim), `#4ec9b0` (cyan), `#ce9178` (orange)
- ASCII box-drawing for header
- `$ command --flags` style section headers
- ASCII bar chart using `█` characters

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>claude-analytics</title>
  <style>
    body {
      font-family: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
      background: #0d0d0d;
      color: #b0b0b0;
      font-size: 14px;
      line-height: 1.6;
      padding: 24px;
    }
    .container { max-width: 900px; margin: 0 auto; }
    .header { color: #6a9955; margin-bottom: 24px; }
    .dim { color: #555; }
    .bright { color: #e0e0e0; }
    .cyan { color: #4ec9b0; }
    .orange { color: #ce9178; }
    .row {
      display: grid;
      grid-template-columns: 24px 200px 1fr 80px 80px 60px;
      gap: 8px;
      padding: 6px 0;
      border-bottom: 1px solid #1a1a1a;
    }
    .row:hover { background: #141414; }
    a { color: #555; text-decoration: none; }
    a:hover { color: #888; }
    .stat-box { display: inline-block; margin-right: 32px; }
    .stat-value { font-size: 28px; color: #e0e0e0; }
    .stat-label { color: #555; font-size: 12px; }
  </style>
</head>
<body>
  <div class="container">
    <pre class="header">
┌─────────────────────────────────────────────────────────────────┐
│   ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗              │
│  ██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝              │
│  ██║     ██║     ███████║██║   ██║██║  ██║█████╗                │
│  ██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝                │
│  ╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗              │
│   ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝              │
│   Weekly Analytics Report                                       │
│   {start_date} .. {end_date}                                    │
└─────────────────────────────────────────────────────────────────┘
</pre>
    <!-- Stats, table, chart sections -->
  </div>
</body>
</html>
```

## Bar Chart Generation

```python
def make_bar(value, max_val, width=40):
    filled = int((value / max_val) * width)
    return '█' * filled

# Example output:
# cohorts          ████████████████████████████████████████ 194
# ai-whisper       █████████████████████████████████████▋ 183
```

## Usage

1. User asks for analytics: "покажи статистику cc", "weekly report", "что делал за неделю"
2. Run Python script to collect data
3. Generate HTML with template
4. Save to `~/claude-analytics.html`
5. Open in browser: `open ~/claude-analytics.html`

## Customization

- **Period:** Change `days = 7` to desired range
- **Output path:** Change save location
- **Colors:** Adjust CSS variables
- **Columns:** Add/remove metrics in grid
