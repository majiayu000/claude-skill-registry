---
name: multi-agent-architecture
description: Multi-agent sistem mimarisi referansi. Use when working with agents, pipelines, or understanding the content generation workflow.
---

# Multi-Agent Architecture

## Agent Overview

| Agent | Role | Key Action |
|-------|------|------------|
| Orchestrator | Koordinasyon | plan_week, daily_check |
| Planner | Konu secimi | suggest_topic |
| Creator | Icerik uretimi | create_post, create_visual_prompt |
| Reviewer | Kalite kontrol | review_post (score 1-10) |
| Publisher | Platform yayin | publish |
| Analytics | Performans takip | fetch_metrics |

## Pipeline Types

| Type | Telegram Approval |
|------|-------------------|
| daily | Yes (each stage) |
| autonomous | No (min_score check) |
| reels | Yes |
| carousel | Yes |

## Daily Pipeline Flow

```
Planner → suggest_topic
    ↓ Telegram approval
Creator → create_post
    ↓ Telegram approval
Creator → create_visual_prompt → Flux/Veo
    ↓ Telegram approval
Reviewer → review_post (score)
    ↓ Telegram approval
Publisher → Instagram
```

## Pipeline States

```python
IDLE → PLANNING → AWAITING_TOPIC_APPROVAL →
CREATING_CONTENT → AWAITING_CONTENT_APPROVAL →
CREATING_VISUAL → AWAITING_VISUAL_APPROVAL →
REVIEWING → AWAITING_FINAL_APPROVAL →
PUBLISHING → COMPLETED | ERROR
```

## Basic Usage

```python
from app.scheduler.pipeline import ContentPipeline

pipeline = ContentPipeline(telegram_callback=callback)

# Daily (with approvals)
result = await pipeline.run_daily_content()

# Autonomous (no approvals, min_score=7)
result = await pipeline.run_autonomous_content(min_score=7)

# Reels
result = await pipeline.run_reels_content()
```

## BaseAgent Pattern

```python
from app.agents.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__("myagent")  # Loads persona

    async def execute(self, input_data):
        response = await self.call_claude_with_retry(
            prompt="...",
            timeout=120,
            max_retries=3
        )
        return json.loads(response)
```

## Retry Logic

```python
@retry_with_backoff(max_retries=3, base_delay=2.0)
# Delays: 2s, 4s, 8s (exponential)
```

## Return Format

```python
# Success
{"success": True, "post_id": 123, "instagram_post_id": "..."}

# Error
{"success": False, "error": "...", "final_state": "error"}
```

## Deep Links

- `app/scheduler/pipeline.py` - Pipeline logic
- `app/agents/base_agent.py` - Base class
- `app/agents/creator.py` - Content creation
- `app/agents/reviewer.py` - Quality control
- `context/agent-personas/` - Agent personas
