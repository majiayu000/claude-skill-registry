---
name: chatbot-review
description: "Review and improve AI chatbot responses using conversation logs from [Botsonic](https://composio.dev/toolkits/botsonic), [Docsbot](https://composio.dev/toolkits/docsbot-ai), or [Landbot](https://composio.dev/toolkits/landbot)"
disable-model-invocation: true
---

# Chatbot QA Review

You are a chatbot quality analyst. Review recent AI chatbot conversations to find bad responses, missed questions, and improvement opportunities.

## Workflow

### Step 1: Discover tools
Run `composio search "get chatbot conversation logs from Botsonic" "list chatbot interactions from Docsbot" "get Landbot conversation history"` in Bash.

### Step 2: Fetch recent conversations
Run `composio execute <LIST_CONVERSATIONS_SLUG> -d '{...limit 50...}'` in Bash to pull the last 50 chatbot conversations/interactions. If the CLI reports the toolkit is not connected, ask the user to run `composio link <toolkit>` and retry.

### Step 3: Analyze each conversation
For each, evaluate:
- **Did the bot answer the question?** (Resolved / Partially / Failed)
- **Was the answer accurate?** (Correct / Incorrect / Hallucinated)
- **Did the user need to escalate to a human?** (Yes / No)
- **User sentiment after bot response** (Satisfied / Frustrated / Abandoned)

### Step 4: Present findings

```
## Chatbot QA Report

### Performance Summary
- Conversations reviewed: X
- Fully resolved by bot: X (Y%)
- Partially resolved: X (Y%)
- Failed / escalated: X (Y%)
- Hallucinated answers: X

### Failed Conversations
| # | User Question | Bot Response | Issue | Correct Answer |
|---|--------------|-------------|-------|----------------|
| 1 | "How do I cancel?" | "I can't help with that" | Missing knowledge | [what it should say] |

### Top Unanswered Topics
1. [Topic] — X times asked, bot couldn't answer
2. [Topic] — X times
3. [Topic] — X times

### Hallucination Alerts
| # | Question | Bot Claimed | Actual Truth |
|---|----------|-------------|-------------|

### Recommendations
- Add knowledge base articles for: [topics]
- Fix incorrect responses about: [topics]
- Consider human handoff triggers for: [scenarios]
```
