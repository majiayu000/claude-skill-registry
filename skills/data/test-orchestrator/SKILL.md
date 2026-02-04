---
name: test-orchestrator
description: Test ClaudeKit workflows by scanning commands/agents/skills, generating test scenarios, and executing step-by-step with manual verification.
---

# Test Orchestrator

Automated testing framework for ClaudeKit Marketing workflows.

## When to Use

- Testing new commands after implementation
- Validating agent orchestration flows
- Verifying skill integrations work correctly
- Regression testing after changes
- End-to-end workflow validation

## Workflow

### 1. Scan Components

```bash
# Generate fresh catalogs
python .claude/scripts/generate_catalogs.py --all

# Or scan specific type
python .claude/skills/test-orchestrator/scripts/scan-components.py
```

### 2. Select Test Scope

| Scope | Description |
|-------|-------------|
| `command` | Test single command with happy case |
| `workflow` | Test multi-step workflow |
| `integration` | Test skill + agent + command together |
| `full` | Complete end-to-end test suite |

### 3. Execute Tests

Each test step pauses for manual verification:

```
[STEP 1/5] Executing: /youtube:social "https://youtube.com/..."
─────────────────────────────────────────────────
[OUTPUT]
...generated content...
─────────────────────────────────────────────────
[VERIFY] Check output matches expected format
[PASS/FAIL?] > _
```

## Test Case Format

```yaml
name: youtube-to-social-flow
description: Convert YouTube video to multi-platform social posts
type: integration

steps:
  - name: Extract video data
    action: vidcap summary
    input: "https://youtube.com/watch?v=dQw4w9WgXcQ"
    verify:
      - Response contains video title
      - Response contains summary content

  - name: Generate social posts
    action: /youtube:social
    input: "{video_url}"
    verify:
      - Twitter post under 280 chars
      - LinkedIn post has professional tone
      - No anti-pattern hooks used

  - name: Apply writing style
    action: copywriting skill
    input: Apply casual style to Twitter post
    verify:
      - Contains contractions
      - Uses first-person
```

## Pre-Built Test Scenarios

### 1. YouTube Pipeline

| Step | Command/Skill | Input | Verify |
|------|---------------|-------|--------|
| 1 | `vidcap.py info` | YouTube URL | Returns title, views, duration |
| 2 | `vidcap.py summary` | YouTube URL | Returns structured summary |
| 3 | `/youtube:social` | YouTube URL | Multi-platform posts generated |
| 4 | `/youtube:blog` | YouTube URL | SEO article generated |
| 5 | `/youtube:infographic` | YouTube URL | Visual layout generated |

### 2. Content Creation

| Step | Command/Skill | Input | Verify |
|------|---------------|-------|--------|
| 1 | `/content:blog` | Topic | Article with frontmatter |
| 2 | `/content:cro` | Article | CRO-optimized version |
| 3 | `/social` | Article summary | Platform posts |

### 3. Email Automation

| Step | Command/Skill | Input | Verify |
|------|---------------|-------|--------|
| 1 | `/email:flow` | welcome | 5-email sequence |
| 2 | email-marketing skill | Sequence | Timing + decision branches |
| 3 | copywriting skill | Email body | PAS/AIDA formula applied |

### 4. Brand Consistency

| Step | Command/Skill | Input | Verify |
|------|---------------|-------|--------|
| 1 | `inject-brand-context.cjs` | - | Returns brand JSON |
| 2 | `/brand:update` | preset | Tokens synced |
| 3 | Content generation | Any | Brand voice applied |

## Happy Case Prompts

Pre-validated inputs that should always succeed:

```yaml
youtube_url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
blog_topic: "10 productivity tips for remote workers"
email_flow: "welcome"
brand_preset: "ocean-professional"
social_platform: "twitter"
writing_style: "casual"
```

## Manual Verification Checklist

At each step, verify:

- [ ] Output format matches expected structure
- [ ] No error messages in response
- [ ] Content quality acceptable
- [ ] Anti-patterns avoided (for hooks)
- [ ] Brand voice consistent (if applicable)
- [ ] File saved to correct path (if applicable)

## Integration

Use with:
- `/test` command to launch test runner
- `debugging` skill for failure analysis
- `code-review` skill for output validation
