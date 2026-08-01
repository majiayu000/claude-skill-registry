---
name: delegate-my-work
description: Interview employees to identify recurring daily work, office workflows, and repetitive tasks that can be automated, co-piloted, or supported by AI. Use when the user wants to find what AI can take off their plate, map available tools such as ChatGPT/OpenAI, Claude, Microsoft Copilot, Excel or PowerPoint add-ins, Google Workspace, no-code/RPA tools, coding agents, or internal automation platforms, and write tool-aware specs with fallback paths.
---

# Delegate My Work

Interview the user about their work to find **loops** -- recurring patterns worth handing to AI -- and write one buildable spec per loop. The primary audience is nontechnical employees: use plain workplace language, focus on daily work, and do not assume any AI or automation tool is available until the user confirms access.

The method is **grilling**: relentless, one question at a time. The output is a tool-aware spec in the user's workspace that recommends a preferred route, states tool access, includes at least one fallback route, and gives an implementer enough detail to build without asking a question.

## The grilling discipline

Interview the user relentlessly about one loop until reaching a shared, buildable understanding. Walk down each branch of the design tree, resolving dependencies between decisions one by one. Attach a **recommended answer** to every question.

Ask **one question at a time**, waiting for the answer before continuing. Asking several at once is bewildering.

If a question can be answered by exploring the user's files, codebase, workspace, or existing notes, explore instead of asking.

## Asking with the question tool

Use the host's question tool when available:

- In Codex, use `request_user_input`.
- In Claude, use `AskUserQuestion`.
- If no question tool is available, ask the same one question in plain text.

For every question:

- Ask **exactly one** question per call -- never batch.
- Offer 2-4 options. Put the **recommended answer first** and append `(Recommended)` to its label.
- Let the built-in **Other** option carry free-text answers when the host provides it; do not add an "Other" option of your own.

## Tool access map

Before recommending a tool route, build or update the user's **tool access map** in `NOTES.md`. Ask one question at a time about the tools the employee can actually use:

- ChatGPT/OpenAI tools, including Codex or coding agents.
- Claude tools, including any document, spreadsheet, or presentation support.
- Microsoft Copilot and Microsoft 365 access.
- Excel and PowerPoint add-ins or extensions.
- Google Workspace AI tools and add-ons.
- No-code/RPA tools such as Zapier, Make, Power Automate, UiPath, or similar.
- IT-approved automation platforms, internal APIs, scripts, or service accounts.

Record each tool with one of these exact access statuses:

- **Available**
- **Available with admin approval**
- **Unavailable**
- **Blocked by policy**
- **Unknown - verify**

Never recommend only one route unless access is confirmed and policy-safe. If access is unknown, blocked, or unavailable, state that and include a fallback route.

## Tool routes and fallbacks

Every loop spec must include a preferred route and at least one fallback route.

Use these route types:

- **Existing AI assistant** -- the employee can do the loop with a currently available assistant.
- **Office add-in/extension** -- an Excel, PowerPoint, Outlook, Google Workspace, or similar extension supports the loop.
- **Coding/agentic builder** -- OpenAI/Codex, Claude Code, another coding agent, or a developer builds the automation.
- **No-code/RPA/API automation** -- a workflow platform, Office Scripts, Power Automate, Zapier, Make, UiPath, API integration, or internal automation handles it.
- **Manual bridge** -- a safer human-run process improvement while access, policy, or data issues are unresolved.
- **Do not automate yet** -- the loop is too ambiguous, sensitive, rare, or policy-blocked for AI support today.

Default fallback rules:

- If an Excel or PowerPoint extension is unavailable, consider manual upload/export, Office Scripts, VBA, Power Query, Microsoft Copilot, no-code/RPA, or a buildable automation spec.
- If OpenAI/Codex is unavailable, consider Claude, Microsoft Copilot, a no-code workflow, or an internal IT implementation path.
- If all AI tools are blocked, produce a human-run process improvement checklist and a future-ready automation spec.
- If data is sensitive, prefer a route that keeps data inside approved company systems or requires IT/security approval before execution.

## The three delegation levels

Classify every loop by how much of it AI takes, which is set by where the human stays in the loop:

- **Automate** -- AI or automation runs the loop end-to-end. No **checkpoint**.
- **Co-pilot** -- AI does the work; the human verifies a **brief** at a **checkpoint**, then it proceeds. (Half-automated.)
- **Assist** -- the human runs the loop; AI helps at specific points. (Supported.)

Mandate nothing structural: a loop needs no AI, no checkpoint, and no schedule unless the grilling shows it does. The operational vocabulary for a spec -- **trigger**, **checkpoint**, **push right**, **brief**, **tool access map**, **fallback route**, and **manual bridge** -- is defined in `references/vocabulary.md`; reach for it while grilling a loop.

## The workspace

State lives in the user's working directory, not in this skill:

- `NOTES.md` -- the user's world: role, recurring work, tools/channels, terminology, sensitive-data constraints, allowed AI tools, tool access map, and loop inventory.
- `automations/<loop>.md` -- one tool-aware spec per loop. The source of truth for what gets built or adopted.

## Steps

Run these in order. Each ends on its completion criterion; do not advance until it is met.

1. **Ground in the user's world.** Read `NOTES.md`. If it is absent or thin, grill about role, daily and weekly work, tools, channels, terminology, data sensitivity, and recurring friction. Sharpen fuzzy terms into canonical ones as they surface, and record them. *Done when `NOTES.md` describes their world in their own vocabulary.*

2. **Map tool access.** Read the existing tool access map from `NOTES.md`, then ask one question at a time until relevant tools have an access status. Cover ChatGPT/OpenAI, Claude, Microsoft Copilot, Excel/PowerPoint add-ins, Google Workspace tools, no-code/RPA tools, coding agents, IT-approved platforms, and internal APIs as relevant to the employee's work. *Done when likely preferred routes can be marked Available, Available with admin approval, Unavailable, Blocked by policy, or Unknown - verify.*

3. **Pick a loop.** If the user named a work area (the command argument), take it. Otherwise read `NOTES.md` and propose loops through the loop lens -- including ones the user has not noticed. *Done when one named loop is on the table.*

4. **Grill the loop.** Walk its design tree one question at a time: trigger; inputs and sources; the work itself, step by step; data sensitivity; tool access constraints; delegation level; where the checkpoint sits and how far right it can be pushed; what the brief shows; failures and edge cases. For ready question trees by work type, load `references/question-bank.md`. *Done when no open question remains on any branch.*

5. **Choose route and fallback.** Choose the preferred tool route using the access map and policy constraints. Add at least one fallback route unless the preferred route is confirmed available and policy-safe. *Done when preferred route, access status, fallback route, approval/install need, and manual bridge are explicit.*

6. **Place the human.** Choose the level -- Automate, Co-pilot, or Assist. For Co-pilot and Assist, place the checkpoint and **push it right**: do maximal work before involving the human, so they are asked once, late, with everything prepared. *Done when the level is chosen and its checkpoint placed -- or declared none, for Automate.*

7. **Write the spec.** Write `automations/<loop>.md` using the structure in `references/spec-template.md`. *Done when it meets the definition of done below.*

8. **Next loop.** Ask whether another loop is worth specifying, then repeat from step 3. *Done when the user is out of loops worth delegating.*

## Definition of done

A spec is done when it states the preferred route, access status, fallback route, approval or install need, data sensitivity, delegation level, and checkpoint placement, and an implementer agent could build the automation or support workflow **without asking a single question**. Grill until then; nothing is done while a question remains.

## Additional resources

- `references/vocabulary.md` -- trigger, checkpoint, push right, brief, tool access map, fallback route, manual bridge, and the loop/delegate anchors. Load while mapping access, grilling, and placing the human (steps 2, 4-6).
- `references/question-bank.md` -- grilling question trees per employee work domain. Load when grilling a specific loop (step 4).
- `references/spec-template.md` -- the `automations/<loop>.md` structure and a worked example. Load when writing a spec (step 7).
