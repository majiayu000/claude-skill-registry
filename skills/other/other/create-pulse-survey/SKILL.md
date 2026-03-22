---
name: create-pulse-survey
description: Creates short employee pulse surveys (5–15 questions) and eNPS surveys. Pulse themes include morale, manager trust, workload, remote/hybrid, DEI, onboarding, change management, team cohesion, leadership communication, psychological safety, learning & development, and all-hands/event feedback. Use this skill when asked to run a pulse check, create a quick employee sentiment survey, check in on how the team is feeling, run an eNPS, measure employee net promoter score, or build an HR survey on a specific topic. Works for open-ended requests ("create a pulse survey", "run an eNPS") and goal-directed briefs ("check morale after the reorg", "how do people feel about the new leadership?"). Creates surveys directly in FeedbackPulse via MCP tool when available, or produces a CSV ready to import into FeedbackPulse (Surveys → Templates → Import Questions) or other survey tools.
metadata:
  author: feedbackpulse
  version: "1.1"
  alias: fp:pulse
---

# Create Pulse Survey

Pulse surveys are short, focused check-ins designed for frequent use — after significant events or on a recurring monthly/quarterly cadence. They should take under 3 minutes to complete.

## Step 1: Identify the Survey Type

**If the user asks for an eNPS, employee NPS, or employee Net Promoter Score** — skip directly to Step 1b.

**Otherwise**, identify the pulse theme from `references/question-library.md`:

| Theme | When to use |
|---|---|
| **morale** | General sentiment, motivation, happiness at work |
| **manager-trust** | Manager relationship, feedback, support, communication |
| **workload** | Capacity, sustainable pace, priority clarity |
| **change-management** | Post-reorg, layoff, leadership change, pivot, merger, or any major announcement |
| **dei** | Belonging, inclusion, psychological safety, fair treatment |
| **remote-hybrid** | Ongoing remote/hybrid experience, connection, and productivity |
| **onboarding** | New hire experience — first 30, 60, or 90 days |
| **team-cohesion** | Within-team collaboration, trust, and camaraderie |
| **leadership-communication** | Senior leadership direction, visibility, trust in strategy |
| **psychological-safety** | Speaking up, risk-taking, learning from mistakes |
| **l-and-d** | Career growth, learning opportunities, development support |
| **all-hands** | Post-event feedback — all-hands, town hall, or offsite |

**If the brief is vague** (e.g., "run a pulse survey"), ask exactly one clarifying question:

> "What is the current focus area for this pulse? For example: general morale, leadership communication, a recent change, workload, or something else?"

Do not ask multiple questions. If the user provides any context at all, infer the theme and proceed.

**Multi-theme requests** (e.g., "check morale and workload"): select up to 5 questions from each theme, staying within the 15-question maximum. Prioritise `core` questions from each theme.

## Step 1b: eNPS (Employee Net Promoter Score)

eNPS has a fixed, standardised structure. Do not add Likert questions — the value of eNPS is consistency and comparability over time.

**Standard structure:**

1. "On a scale of 0–10, how likely are you to recommend [Company] as a great place to work?" — type `enps`, required
2. "What is the main reason for your score?" — type `text`, not required
3. *(Optional)* "What would most improve your experience at [Company]?" — type `text`, not required. Add this if the user asks for improvement suggestions or additional context.

**Cadence guidance:** Run eNPS quarterly or biannually. Running it more frequently than quarterly makes it difficult to detect meaningful change; less than biannually loses the pulse character. Always run it at the same interval so results are comparable.

**Benchmark context:** eNPS = % Promoters (9–10) − % Detractors (0–6). Below 0 is a concern; 0–20 is acceptable; 20–50 is strong; above 50 is excellent. Benchmarks vary by industry, so track your own trend over time.

After building an eNPS survey, skip Steps 2–3 and proceed directly to Step 4.

## Step 2: Select Questions

Read `references/question-library.md` and select questions for the identified theme.

**Question count guidance:**

| Scenario | Target length |
|---|---|
| Post-event (all-hands, offsite, announcement) | 3–5 questions |
| Ongoing pulse check | 5–8 questions |
| Deep dive on a specific theme | 8–12 questions |

**Maximum:** 15 questions. If asked for more, explain that pulse surveys above 15 questions see lower completion rates, and offer to split into two focused surveys instead. If the user asks to "keep it short", aim for the low end of the appropriate range.

**Composition rules:**
- Prioritise `core` questions first; add `supplementary` to reach the target length
- End with 1–2 open-ended questions (never more than 2)
- Use the **5-point agreement scale** (`Strongly Disagree → Strongly Agree`) for all Likert questions — this is the only Likert scale FeedbackPulse supports in CSV import and the MCP tool
- Never include demographic questions — keep surveys brief and anonymous-feeling

**Adapting questions:** Replace `[Company]` with the company name if provided. If the company name is not known, leave `[Company]` as a visible placeholder and note in your response that the user should replace it before sending. When rephrasing to match context (e.g., "after the reorg", "since the announcement"), change only the contextual phrase — do not alter the core construct being measured.

## Step 3: Write the Preamble

Every survey needs a short preamble (2–3 sentences). Fill the placeholders:

> Thank you for taking a few minutes to share your thoughts. This survey is [purpose, e.g., "a quick check-in on how the team is feeling after last month's changes"]. Your responses are [anonymous / confidential] — results will be reviewed by [audience, e.g., "the People team"] to inform how we can better support you.

**Anonymous vs. confidential — ask the user to confirm if unsure:**
- **Anonymous**: the platform cannot identify the respondent. Safe for honest feedback but limits follow-up.
- **Confidential**: the platform records who responded, but results are aggregated before sharing with managers. Allows the People team to follow up but requires trust in data handling.
- **Note:** On teams smaller than 8–10 people, even anonymous surveys can have identifiable responses. Flag this to the user if they mention a small team.

If the user has not indicated a preference, default to anonymous.

**Preamble placement:** Present the preamble as text for the user to paste into their survey platform's intro/description field. It is not embedded in the MCP tool call or CSV — use the `description` field of the MCP payload and present it separately to the user.

## Step 4: Output the Survey

### Option A — FeedbackPulse MCP Tool (preferred)

Look for a tool named `create_survey_template`. If not found by that name, search for tools matching: `feedbackpulse`, `pulse_survey`, `create_survey`.

Call the tool with this structure. Set `order` to the question's 1-based position in the final list. Set `is_anonymous` to match the anonymity decision from Step 3.

```json
{
  "name": "[Theme] Pulse – [Month YYYY]",
  "description": "[preamble text from Step 3]",
  "type": "pulse",
  "is_anonymous": true,
  "questions": [
    {
      "question": "I feel motivated to do my best work right now.",
      "type": "likert",
      "order": 1,
      "is_required": true,
      "options": { "label_preset": "agreement" }
    },
    {
      "question": "My workload feels manageable right now.",
      "type": "likert",
      "order": 2,
      "is_required": true,
      "options": { "label_preset": "agreement" }
    },
    {
      "question": "What is one thing that would most improve your experience at work right now?",
      "type": "text",
      "order": 3,
      "is_required": false
    }
  ]
}
```

For eNPS, use `"type": "enps"` at the survey level and `"type": "enps"` for the scale question:

```json
{
  "name": "eNPS – [Month YYYY]",
  "description": "[preamble text]",
  "type": "enps",
  "is_anonymous": true,
  "questions": [
    {
      "question": "On a scale of 0–10, how likely are you to recommend [Company] as a great place to work?",
      "type": "enps",
      "order": 1,
      "is_required": true,
      "options": { "low_label": "Not Likely", "high_label": "Extremely Likely" }
    },
    {
      "question": "What is the main reason for your score?",
      "type": "text",
      "order": 2,
      "is_required": false
    }
    // optional Q3 if user requested: { "question": "What would most improve your experience at [Company]?", "type": "text", "order": 3, "is_required": false }
  ]
}
```

Report the returned survey URL or ID to the user. If the tool call fails, tell the user: "The FeedbackPulse tool returned an error — here is your survey as a CSV you can import instead." Then produce the CSV per Option B.

### Option B — CSV File (FeedbackPulse import or fallback)

Read `references/csv-format.md` for the exact column schema and encoding rules.

Name the file: `[theme]-pulse-YYYY-MM-DD.csv` (e.g., `morale-pulse-2026-03-20.csv`) or `enps-YYYY-MM-DD.csv` for eNPS. For event surveys, name it `[event-name]-feedback-YYYY-MM-DD.csv`.

Present the CSV as a code block, and present the preamble separately as text for the user to paste into the survey's intro field.

The CSV imports directly into FeedbackPulse via **Surveys → Templates → Import Questions**.

## Timing Guidance

- **Post-event surveys:** Send within 48 hours of the event while it is fresh. Keep open for 3–5 business days.
- **Ongoing pulse:** Monthly is common; quarterly is sufficient for most organisations. Consistent intervals matter more than frequency — change the interval only deliberately.
- **eNPS:** Quarterly or biannually. Never more frequently than quarterly.
- **Post-change (reorg, layoff):** Send 2–4 weeks after the announcement, once immediate shock has settled.

## Scope Boundaries

| Request | Response |
|---|---|
| Annual or quarterly engagement survey | "That calls for a full engagement survey — use `/fp:create-engagement-survey` when it's available." |
| Peer review or 360-degree feedback | "Peer reviews need a different structure — use `/fp:create-peer-review` when it's available." |
| Performance review questions | "Try `/fp:create-performance-review` when it's available." |
| Exit interview or offboarding survey | "Exit interviews are a distinct format — use `/fp:create-exit-survey` when it's available." |
| Post-training effectiveness survey | "Post-training feedback has its own format — use a general survey tool or check for `/fp:create-training-feedback` when it's available." |
| Analysing or interpreting survey results | "Creating surveys is in scope; analysing results is not — bring your data to a data analysis tool." |
| Sending or distributing the survey | "Distribution isn't in scope here — use FeedbackPulse's platform or your survey tool to send." |
