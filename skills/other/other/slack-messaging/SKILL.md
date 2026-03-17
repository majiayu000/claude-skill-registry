---
name: slack-messaging
description: Slack messaging patterns and principles for gh-pr-linear-issue-linker. Use when writing Slack notifications, formatting messages, or working with Block Kit layouts.
---

# Slack Messaging Principles

## Core Principle: Thread Replies Should Not Repeat Context

**CRITICAL RULE**: Thread replies must only add new information. Never repeat data that's already in the parent message.

When posting to an existing thread, the parent message contains:
- PR title
- PR number
- PR author
- Repository name
- PR URL
- Original event context

**Thread replies should be concise and focused on what changed.**

## Message Type Patterns

### 1. Parent Messages (New Threads)

Parent messages establish context and should include full details:

```python
SlackNotification(
    event_type=SlackNotificationEvent.FIND_MATCHES,
    repo="owner/repo",
    pr_number=123,
    pr_title="Fix authentication bug",
    pr_author="john-doe",
    pr_url="https://github.com/owner/repo/pull/123",
    result_summary="Matched 1 ticket: ENG-456",
    is_thread_reply=False,  # This creates a new thread
    thread_ts=None,
)
```

**Block Kit structure:**
```
┌──────────────────────────────────────┐
│ 🔍  Gupri matched a ticket          │ (header)
├──────────────────────────────────────┤
│ owner/repo | PR #123 | by @john-doe │ (context)
│ Fix authentication bug               │
├──────────────────────────────────────┤
│ Matched 1 ticket: ENG-456           │ (result)
└──────────────────────────────────────┘
```

### 2. PR Lifecycle Thread Replies (Merged/Closed)

For PR state changes, use minimal format - just the action and actor:

```python
SlackNotification(
    event_type=SlackNotificationEvent.PR_MERGED,  # or PR_CLOSED
    actor="merger-username",  # Who performed the action
    is_thread_reply=True,
    thread_ts="1234567890.123456",  # Parent message timestamp
)
```

**Block Kit structure:**
```
┌──────────────────────────────────────┐
│ ✅ Merged by @sarah-smith           │
└──────────────────────────────────────┘
```

**Why this format?**
- Parent already shows PR details
- Only new info: what happened and who did it
- Keeps thread clean and scannable
- Respects Slack threading UX

### 3. Action Thread Replies (Link/Unknown Intent)

For actions with context, include relevant details but omit redundant PR info:

```python
SlackNotification(
    event_type=SlackNotificationEvent.LINK,
    result_summary="Linked ticket ENG-789",
    ticket_identifier="ENG-789",
    is_thread_reply=True,
    thread_ts="1234567890.123456",
)
```

**Block Kit structure:**
```
┌──────────────────────────────────────┐
│ 🔗 Ticket linked to PR               │
├──────────────────────────────────────┤
│ Linked ticket ENG-789                │
│ View ticket: [link]                  │
└──────────────────────────────────────┘
```

## Event Type Configuration

All event types must be configured in three places:

### 1. Event Enum (`src/slack/models.py`)

```python
class SlackNotificationEvent(str, Enum):
    """Slack notification event types."""
    FIND_MATCHES = "find_matches"
    LINK = "link"
    UNKNOWN_INTENT = "unknown_intent"
    PR_MERGED = "pr_merged"
    PR_CLOSED = "pr_closed"
```

### 2. Emoji Mapping (`src/services/slack_notifier.py`)

```python
_EMOJI_MAP: Final[dict[SlackNotificationEvent, str]] = {
    SlackNotificationEvent.FIND_MATCHES: ":mag:",
    SlackNotificationEvent.LINK: ":link:",
    SlackNotificationEvent.UNKNOWN_INTENT: ":question:",
    SlackNotificationEvent.PR_MERGED: ":white_check_mark:",
    SlackNotificationEvent.PR_CLOSED: ":no_entry_sign:",
}
```

**Emoji selection guidelines:**
- Use emojis that clearly indicate the event type
- Prefer standard Slack emojis (work everywhere)
- Green (✅) for success, red (❌) for closure/failure
- Neutral colors for informational events

### 3. Header Mapping (`src/services/slack_notifier.py`)

```python
_HEADER_MAP: Final[dict[SlackNotificationEvent, str]] = {
    SlackNotificationEvent.FIND_MATCHES: "Gupri matched a ticket",
    SlackNotificationEvent.LINK: "Ticket linked to PR",
    SlackNotificationEvent.UNKNOWN_INTENT: "Clarification requested",
    SlackNotificationEvent.PR_MERGED: "PR merged",
    SlackNotificationEvent.PR_CLOSED: "PR closed",
}
```

## User Mention Resolution

Always resolve GitHub usernames to Slack mentions when possible:

```python
# In SlackNotifier
async def _resolve_author_mention(self, github_username: str) -> str:
    """Resolve GitHub username to Slack mention.

    Returns:
        "<@U123ABC>" if mapped, else "@github-username"
    """
    try:
        slack_user_id = await self._slack_user_mapper.get_slack_user_id(github_username)
        if slack_user_id:
            return f"<@{slack_user_id}>"  # Clickable Slack mention
    except Exception:
        logger.exception("Failed to resolve Slack user")
    return f"@{github_username}"  # Fallback to GitHub username
```

**Benefits:**
- Slack users get notified when mentioned
- Clickable user profiles in Slack
- Graceful fallback to GitHub username if no mapping exists

## Actor vs Author

For PR lifecycle events, distinguish between:

- **Author** (`pr_author`): Person who created the PR
- **Actor** (`actor`): Person who performed the current action (merged/closed)

```python
# Merged PR: show who merged (may differ from author)
SlackNotification(
    event_type=SlackNotificationEvent.PR_MERGED,
    pr_author="john-doe",      # Created the PR
    actor="sarah-smith",       # Merged the PR
)

# Result: "✅ Merged by @sarah-smith"
```

## Threading Behavior

Thread replies use `thread_ts` to nest under parent messages:

```python
# Initial PR opened - creates new thread
notification = SlackNotification(
    event_type=SlackNotificationEvent.FIND_MATCHES,
    is_thread_reply=False,  # New parent message
    thread_ts=None,
)
response = await slack_client.post_message(...)
thread_ts = response["ts"]  # Store for future replies

# Later: PR merged - reply to thread
notification = SlackNotification(
    event_type=SlackNotificationEvent.PR_MERGED,
    is_thread_reply=True,
    thread_ts=thread_ts,  # Reply to parent
)
```

**Threading rules:**
- Store `slack_thread_ts` in Firestore PR state when PR opens
- All subsequent events reply to that thread
- Missing `slack_thread_ts` for lifecycle events = log warning, skip notification

## Error Handling

### Critical Path (Blocking)

For initial PR events, missing data should raise errors:

```python
if not pr_state or not pr_state.slack_thread_ts:
    msg = f"slack_thread_ts missing for {repo}#{pr_number} on link command"
    raise RuntimeError(msg)
```

### Best Effort (Non-Blocking)

For PR lifecycle events, degrade gracefully:

```python
pr_state = await firestore_client.get_pr_state(repo, pr_number)
if not pr_state or not pr_state.slack_thread_ts:
    logger.warning(
        "No slack_thread_ts for closed PR %s#%d - skipping notification",
        repo,
        pr_number,
    )
    return  # Skip notification, don't raise
```

**Rationale:** A closed PR with no thread is not actionable. Better to skip than crash.

## Block Kit Formatting

### Slack mrkdwn Syntax (CRITICAL)

**Slack uses mrkdwn, NOT standard Markdown. The syntax is different:**

| Format | Slack mrkdwn | Standard Markdown | ❌ Wrong |
|--------|--------------|-------------------|----------|
| Bold | `*bold*` | `**bold**` | `**bold**` in Slack shows as-is |
| Italic | `_italic_` | `*italic*` | `*italic*` becomes bold |
| Code | `` `code` `` | `` `code` `` | ✅ Same |
| Code block | ``` ```code``` ``` | ``` ```code``` ``` | ✅ Same |
| Link | `<url\|text>` | `[text](url)` | `[text](url)` shows as-is |

**Common mistake:** AI agents often generate `**bold**` because they default to Markdown. Always use `*bold*` for Slack.

**Example of correct mrkdwn:**
```
I found *1 finding* with high severity.
View the <https://github.com/org/repo/pull/123|pull request> for details.
```

**What the user sees if you use wrong syntax:**
```
I found **1 finding** with high severity.  ← Shows literal asterisks
```

### Section Block with Markdown

```python
{
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": f"✅ Merged by {actor_mention}",
    },
}
```

### Header Block

```python
{
    "type": "header",
    "text": {
        "type": "plain_text",
        "text": f"🔍  {header}",
        "emoji": True,
    },
}
```

### Link Formatting

```python
# Slack link format: <URL|display text>
pr_link = f"<{notification.pr_url}|PR #{notification.pr_number}>"
ticket_link = f"<{ticket_url}|{ticket_identifier}>"
```

## Testing Patterns

Always test:
1. Emoji mapping exists for event type
2. Header mapping exists for event type
3. Block structure matches expected format
4. User mention resolution (Slack user ID vs GitHub username fallback)
5. Thread reply vs parent message logic

```python
@pytest.mark.asyncio
async def test_pr_merged_thread_reply():
    """Verify merged PR sends short thread reply."""
    # Setup
    notification = SlackNotification(
        event_type=SlackNotificationEvent.PR_MERGED,
        actor="merger-user",
        is_thread_reply=True,
        thread_ts="1234.567",
    )

    # Act
    await notifier.notify(notification)

    # Assert
    blocks = mock_slack_client.post_message.call_args.kwargs["blocks"]
    assert len(blocks) == 1  # Single block only
    assert "Merged by @merger-user" in blocks[0]["text"]["text"]
    assert "PR #" not in blocks[0]["text"]["text"]  # No redundant info
```

## Quality Checklist

Before adding new Slack notifications:

- [ ] Event type added to `SlackNotificationEvent` enum
- [ ] Emoji mapping configured in `_EMOJI_MAP`
- [ ] Header mapping configured in `_HEADER_MAP`
- [ ] Thread reply follows "no redundant info" principle
- [ ] User mentions resolved via `_resolve_author_mention`
- [ ] Threading behavior tested (parent vs reply)
- [ ] Missing `slack_thread_ts` handled appropriately
- [ ] Tests cover all formatting variations
- [ ] Block Kit structure validated with Slack API

## Anti-Patterns to Avoid

❌ **Repeating PR details in thread replies:**
```python
# BAD: Thread reply includes redundant PR info
"✅ PR merged\nPR #123: Fix auth bug\nby @author\nView PR: [link]"
```

✅ **Concise thread reply with only new info:**
```python
# GOOD: Just the action and actor
"✅ Merged by @merger"
```

❌ **Inconsistent event type naming:**
```python
# BAD: Mixing naming conventions
SlackNotificationEvent.MERGED = "pr_merged"
SlackNotificationEvent.TICKET_LINK = "link"  # Inconsistent prefix
```

✅ **Consistent enum naming:**
```python
# GOOD: Consistent pattern
SlackNotificationEvent.PR_MERGED = "pr_merged"
SlackNotificationEvent.PR_CLOSED = "pr_closed"
SlackNotificationEvent.LINK = "link"
```

❌ **Hard-coded emoji strings in message builders:**
```python
# BAD: Emoji duplicated across functions
return f"✅ Merged by {user}"
```

✅ **Centralized emoji configuration:**
```python
# GOOD: Single source of truth
emoji = _EMOJI_MAP.get(event_type)
return f"{emoji} Merged by {user}"
```

❌ **Using standard Markdown syntax in Slack messages:**
```python
# BAD: Standard Markdown (double asterisks for bold)
text = "I found **1 finding** with high severity."
# Result in Slack: "I found **1 finding** with high severity." (literal asterisks shown)
```

✅ **Using Slack mrkdwn syntax:**
```python
# GOOD: Slack mrkdwn (single asterisk for bold)
text = "I found *1 finding* with high severity."
# Result in Slack: "I found 1 finding with high severity." (properly bolded)
```

❌ **Using Markdown link syntax in Slack:**
```python
# BAD: Markdown link syntax
text = "[View PR](https://github.com/org/repo/pull/123)"
# Result in Slack: "[View PR](https://github.com/org/repo/pull/123)" (literal text shown)
```

✅ **Using Slack link syntax:**
```python
# GOOD: Slack link syntax
text = "<https://github.com/org/repo/pull/123|View PR>"
# Result in Slack: "View PR" as a clickable link
```
