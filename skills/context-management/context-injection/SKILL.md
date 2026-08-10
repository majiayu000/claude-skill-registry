---
name: context-injection
description: "Place trusted contextual information into prompts or agent state using explicit boundaries, provenance, and templates. Use when relevant context has already been selected and must be inserted safely; use context-retrieval to find it or context-optimization to choose and order it."
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: "1.0.0"
---

# Context Injection

Context injection is the practice of dynamically inserting relevant information — documents, data, examples, or tool outputs — into an AI prompt so the model has the knowledge it needs to produce accurate, grounded responses. Effective injection is about more than pasting text; it requires deliberate placement, formatting, and token budget allocation to maximize the model's ability to use the injected material.

## Workflow

1. **Identify the Context Need**: Analyze the task to determine what types of external information the model requires. A code review needs the source file; a support question needs product documentation; a personalized reply needs the user's profile. Clearly categorize each need as document grounding, few-shot examples, tool output, or metadata.

2. **Gather the Context**: Retrieve the necessary information from its source — a database, file system, API response, vector store, or prior conversation. Apply any necessary compression or truncation before injection so the material fits within the allocated token budget.

3. **Select an Injection Strategy**: Choose the appropriate injection method based on the context type and the model's attention patterns:
   - *System prompt injection* — persistent context like role definitions, rules, and user preferences go in the system message.
   - *Document grounding* — retrieved documents or files are inserted in the user message, typically before the question.
   - *Few-shot examples* — input/output pairs demonstrating the desired format are placed between the system prompt and the user query.
   - *Tool output injection* — results from function calls or API invocations are injected as assistant/tool messages in the conversation.

4. **Format and Delimit the Context**: Wrap injected content in clear delimiters (XML tags, markdown headers, or triple-backtick fences) so the model can distinguish instructions from context from the user's query. Label each section explicitly (e.g., `<retrieved_document>`, `<user_profile>`, `<code_file>`).

5. **Assemble the Prompt**: Combine the system prompt, injected context blocks, conversation history, and the current user query into the final prompt. Place the most critical context closest to the user's query (recency bias) and the most stable context (rules, persona) in the system message.

6. **Validate Token Allocation**: Confirm the total prompt fits within the model's context window with enough headroom for the expected generation length. If over budget, compress or remove the lowest-priority context blocks first.

## Key Concepts

- **Context Placement**: Where context appears in the prompt matters. Models exhibit a "lost in the middle" effect — they attend most strongly to the beginning and end of the context window. Place the highest-priority information at the start of the context block or immediately before the query.
- **Token Budget Allocation**: A well-designed prompt allocates tokens deliberately: ~10–15% for system instructions, ~50–70% for injected context, ~5–10% for conversation history, and ~15–25% reserved for the model's response.
- **Delimiters and Labeling**: Clear delimiters (XML tags, markdown fences) help the model parse injected sections. Without them, the model may confuse context content with instructions, especially in long prompts.
- **Few-Shot Examples**: Injecting 2–3 input/output examples dramatically improves format compliance and task understanding. Place examples after the system prompt and before the actual query.

## Usage

Use this skill whenever an AI model needs external information to complete a task accurately. Provide the raw context, the task description, and optionally a prompt template. The skill assembles a well-structured prompt with the context injected in the optimal position.

## Examples

### Example 1: Injecting a Code File for a Code Review Task

**Prompt Template:**
```
<system>
You are a senior software engineer performing a code review. Identify bugs,
security issues, and style violations. Be specific and cite line numbers.
</system>

<code_file path="src/api/users.py">
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    return sqlite3.connect("users.db")

@app.route("/users", methods=["GET"])
def list_users():
    db = get_db()
    query = f"SELECT * FROM users WHERE role = '{request.args.get('role')}'"
    results = db.execute(query).fetchall()
    return jsonify(results)

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    db = get_db()
    db.execute(f"DELETE FROM users WHERE id = {user_id}")
    db.commit()
    return "", 204
</code_file>

Review the above code file. List all issues found.
```

**Model Output:**
> 1. **SQL Injection (critical)** — Lines 12–13: User input from `request.args.get('role')` is interpolated directly into the SQL query. Use parameterized queries: `db.execute("SELECT * FROM users WHERE role = ?", (role,))`.
> 2. **SQL Injection** — Line 19: `user_id` is interpolated into the DELETE query. Use a parameterized query.
> 3. **No connection cleanup** — `get_db()` opens a connection but it is never closed. Use a context manager or Flask's `teardown_appcontext`.
> 4. **No authentication/authorization** — The DELETE endpoint has no access control. Any caller can delete any user.

### Example 2: Injecting User Profile Data for Personalized Responses

**Prompt Template:**
```
<system>
You are a helpful fitness assistant. Use the user's profile to personalize
your recommendations. Be encouraging and specific.
</system>

<user_profile>
Name: Sarah
Age: 34
Fitness level: Intermediate
Goals: Lose 10 lbs, improve 5K time
Injuries: Mild left knee tendinitis
Preferred activities: Running, yoga, swimming
Available equipment: Dumbbells (5-30 lbs), resistance bands, yoga mat
Schedule: Can train 4 days/week, 45 min per session
</user_profile>

Sarah asks: "Can you suggest a weekly workout plan for me?"
```

**Model Output:**
> Here's a 4-day plan tailored to you, Sarah — it protects your left knee while building toward your 5K and weight-loss goals:
>
> **Monday — Easy Run + Mobility (45 min):** 25-min easy run at conversational pace, followed by 20 min of yoga focusing on hip flexors and quad stretches to support your knee.
>
> **Wednesday — Strength + Swimming (45 min):** 20-min dumbbell circuit (goblet squats with light weight, lunges, rows, overhead press) + 25-min low-impact swim for cardio without knee stress.
>
> **Friday — Interval Run (45 min):** 10-min warmup, 6×2-min intervals at 5K goal pace with 90-sec walk recovery, 10-min cooldown. If knee flares, switch to swimming.
>
> **Sunday — Active Recovery Yoga (45 min):** Full yoga flow emphasizing hamstring flexibility and core stability.

## Best Practices

- **Use explicit delimiters** — wrap each injected block in labeled XML tags or markdown headers. This prevents the model from confusing injected content with its own instructions.
- **Place critical context near the query** — due to attention patterns, the model is most likely to use information placed immediately before the question or at the very beginning of the prompt.
- **Inject only what's needed** — resist the urge to dump everything available into the prompt. Irrelevant context dilutes attention and increases cost. Be selective.
- **Separate instructions from content** — never embed behavioral instructions inside injected documents. Keep the system prompt for rules and the context blocks for data.
- **Version your prompt templates** — as injected context sources change, prompt templates should be versioned and tested to catch regressions in output quality.
- **Test with and without context** — always compare the model's output with injected context against a baseline without it to confirm the injection actually helps.

## Edge Cases

- **Context exceeds token budget**: When injected content is too large, prioritize by relevance and compress or truncate the lowest-priority sections. Never silently drop context without adjusting the prompt's instructions.
- **Conflicting context sources**: If two injected documents contradict each other (e.g., two versions of a policy), explicitly tell the model which source takes precedence or instruct it to flag the conflict.
- **Sensitive data in context**: User profiles, PII, and credentials may appear in injected context. Ensure your injection pipeline redacts or masks sensitive fields before they reach the model.
- **Empty or missing context**: If a retrieval step returns no results, inject a fallback message (e.g., "No relevant documents were found") rather than leaving an empty block, which the model may misinterpret.
- **Injection of untrusted content**: When injecting user-supplied or web-scraped content, be aware of prompt injection attacks. Delimit untrusted content clearly and instruct the model to treat it as data, not instructions.
