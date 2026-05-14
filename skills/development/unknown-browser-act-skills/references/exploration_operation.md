# Operation-Type Capability Exploration

This file is read during Phase 2 execution (operation-type capabilities only).

**Goal**: Capture how the target operation is executed, confirm it can be triggered in a controlled manner, and record the complete submission parameters. Prefer API direct connection; use DOM automation for submission when necessary.

**Pass Criteria** (API direct connection path):
- HAR captures the expected non-GET request
- All required fields in the request body have clear sources and can be parameterized
- No dynamic credential blocking
- Enumeration parameter retrieval methods have been determined (partial `[collection failed]` still counts as passing)

**Pass Criteria** (DOM fallback path):
- All required form fields can be filled (via script or AI intervention)
- Submission can be triggered
- HAR captures the expected submission request
- Enumeration parameter retrieval methods have been determined (partial `[collection failed]` still counts as passing)

---

## Exploration Decision Tree

```
Navigate → Initial traffic observation → HAR safety verification → API feasible?
  ├── Yes → Record API information
  └── No → [DOM fallback submission]

Verification failure fallback: [API direct] → [DOM fallback submission] → [AI Workflow] → Report obstacles

All paths ultimately → [Enumeration collection]
```

---

## Navigation and Initial Observation

Navigate to the target page, wait for loading to complete, then read initial traffic:

```
network requests --type xhr,fetch --filter {domain keyword}
```

Record two types of information:
- **Enumeration prefetch requests**: Requests that return enumeration data such as dropdown options, category lists (for subsequent parameter enumeration collection)
- **Form initialization requests**: Configuration or state requests made during page load, which may contain CSRF Tokens, form field configurations, etc.

---

## Safety Verification Protocol

> **HAR recording vs. network traffic capture distinction**: Safety verification involves **capturing request intent while offline** (the scenario in this file), with the goal of obtaining the operation request structure with zero side effects; network traffic capture involves **observing already-sent requests** (used in extraction-type exploration), with the goal of discovering API endpoints. The two serve different purposes and are not interchangeable.

Operation-type verification must capture request details **without actually triggering the operation**. This is achieved through browser offline mode for zero side effects:

### Execution Flow

1. **Start HAR recording**: `network har start`
2. **Switch to offline mode**: `network offline on`
3. **Fill the form and click submit**: eval to scan control structure (supplement with a `screenshot` if purpose is unclear) → eval using setter pattern (`HTMLInputElement.prototype` value setter + input event) to batch-fill all inputs → select a non-default item for select/dropdown → click submit. Do not execute `input` field by field
4. **Wait 1~2s**: Give time for async event handlers to fire
5. **Stop HAR recording**: `network har stop {path}`, extract non-GET request details from HAR
6. **Restore online and immediately leave**: `network offline off` → immediately navigate to another page to prevent retry logic from re-sending requests

### Information Extracted from HAR

For each non-GET request, record:
- Endpoint URL + HTTP method (POST/PUT/PATCH/DELETE)
- Request body structure (field names, types, required/optional)
- **Input conditions at capture time**: What values were filled that triggered this request (different inputs may produce different request structures; recording input conditions helps verify generality)

### GraphQL Mutation Identification

Request body contains a `query` field starting with `mutation` → GraphQL write operation. Extract mutation name and variables structure.

---

## Operation Feasibility Assessment

Based on request details captured from HAR, select the strategy path:

**API direct connection feasible** (all of the following are satisfied):
- All required fields in the request body have clear sources and can be parameterized
- Serialization is transparent (request body can be reproduced directly from parameters, no opaque encoding)
- No dynamic credentials found in HAR

→ Use API submission strategy, record endpoint URL + request structure.

> **Verification failure fallback**: Subsequent scripted verification discovers dynamic credentials or opaque encoding missed by HAR analysis → fall back to [DOM fallback submission].

**API incompatible** (any of the following):
- HAR reveals frontend dynamically generated Tokens, Nonces, or HMAC signatures
- Request body contains opaque encoding (cannot be reproduced directly from form fields)

→ **Fall back to DOM operation submission**, execute the "DOM Fallback Submission" steps below.

---

## DOM Fallback Submission

This path is taken when API is incompatible. Let the page's native JS handle credential generation; only automate form filling and submission triggering.

### Step 1 — Control Locating

**When HAR field information is available (preferred)**: Directly use HAR request body field names to locate corresponding controls (`name`/`id` usually match field names), use a single eval to batch-find, skipping full scan:

```javascript
// Batch locate by field name
const fields = ['{field_name_1}', '{field_name_2}'];
JSON.stringify(fields.map(f => {
  const el = document.querySelector(`[name="${f}"], [id="${f}"]`);
  return el ? { field: f, tag: el.tagName, type: el.type, found: true } : { field: f, found: false };
}))
```

**When no field information is available or controls remain unknown (fallback)**: Perform a full scan of the form, returning a complete mapping of all controls (traverse upward from controls to find the nearest container for label text, do not hardcode component library class names):

```javascript
// Full scan of form controls
JSON.stringify(
  Array.from(document.querySelectorAll('input, select, textarea')).map(el => ({
    tag: el.tagName, type: el.type, name: el.name, id: el.id, placeholder: el.placeholder
  }))
)
```

### Step 2 — Assess Scriptability

Evaluate each field individually:
- Value is fixed or parameterizable → **[Script]**: Fill using eval
- Requires real-time judgment (dynamic dropdowns, captchas, complex interactions) → **[AI intervention]**: Agent performs visual operations

If all fields require AI intervention → produce AI Workflow strategy (see Step 3b).

**Multi-step forms (wizards / stepped flows)**: Page state changes after each step submission, requiring progressive advancement. Re-scan currently visible controls at each step, recording state dependencies between steps (previous step's selection affects which fields appear in the next step), so the complete operation sequence can be reproduced in the generated Skill.

### Step 3a — Scripted Submission Verification (when [Script] steps exist)

Use the safety verification protocol (HAR offline mode) to confirm the script can correctly fill and trigger submission:

```javascript
// [Script] Batch fill all fields (setter pattern triggers framework reactive updates)
const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
[
  ['{selector_1}', '{param_value_1}'],  // Element assertion: el.name === '{field_name_1}'
  ['{selector_2}', '{param_value_2}'],  // Element assertion: el.name === '{field_name_2}'
].forEach(([sel, val]) => {
  const el = document.querySelector(sel);
  setter.call(el, val);
  el.dispatchEvent(new Event('input', { bubbles: true }));
});
```

Then trigger submission, confirm from HAR that the request was sent and the structure matches expectations.

> **Verification failure fallback**: HAR did not capture the expected request (framework not responding to setter, selector invalid, submission not triggered, etc.) → Upgrade failed fields to [AI intervention], re-execute Step 3a (remaining script fields) + 3b (upgraded AI fields) in mixed execution. If all fields fail → entirely transfer to Step 3b.

### Step 3b — AI Workflow (when all fields require AI intervention)

The Agent walks through the operation flow step by step like a user.

**Writing standards**:
1. Each step uses browser-act subcommands in abstract form (no `browser-act` prefix — Agent adds session/flags at runtime), followed by supplementary context, ending with `→ expected result`
2. Element references use only visual descriptions; CSS selectors and DOM characteristics are **prohibited**
   - ✗ `click button[type="submit"]`
   - ✓ `state` locate the blue "Submit" button at the bottom of the form → `click <index>`
3. Record state checkpoints after key steps (URL, page title, visible element characteristics)
4. Submission steps must include the complete safety verification sequence:
   `network har start` → `network offline on` → click submit → `network har stop {path}` → `network offline off`

Example:
```
1. state locate {visually described input field} → input <index> "{param_value}"
2. screenshot → confirm input has been filled (checkpoint)
3. state locate the "Submit" button at the bottom of the form
4. network har start
   network offline on
   click <index>
   (wait 1~2s)
   network har stop tmp/{name}.har
   network offline off → immediately navigate to another page
```

> **Verification failure**: Both scripted submission and AI Workflow fail to correctly trigger the submission request → Report current obstacles and attempted paths to the user, ask for next steps.

---

## Parameter Enumeration Collection (Required)

During the verification process, you **must proactively explore** every enumeration-type control on the page (dropdowns, selectors, radio groups) to determine the **data source and retrieval method** for their options. Do not record specific values — values change; recording retrieval methods is more durable.

Try in order of priority `API > DOM > AI`:

1. **Independently read current page traffic**: `network requests --filter {domain keyword}` to check if there are requests returning enumeration lists. If traffic is empty (navigated away due to HAR protocol), navigate back to the target page first
2. **Expand/interact with the control**, observe whether async requests are triggered → if new API requests appear, record as above. If the control supports search (input field + dropdown linkage), enter a keyword to trigger the search API
3. **API endpoint exists** (hit in step 1 or 2) → Record endpoint URL + request method + response structure (field names, value formats), verify whether independent invocation is feasible
4. **Independent invocation not feasible** → Record as hybrid approach: what prerequisite dependencies need to be obtained from the page + how to obtain them + then how to call the API
5. **No API endpoint** → eval to read option values from DOM (native `<select>` reads `.options`, component library controls try reading instance properties, if that fails expand and read rendered results), record selector and method
6. **DOM also cannot reliably obtain** (multiple attempts failed or control is highly dynamic) → **[AI] approach**: Describe the visual interaction operations the Agent needs to perform

#### Conditional Enumeration (Cascading Linkage)

When cascading relationships are found between enumeration controls (selecting A causes B's options to appear/change), record the dependency chain (A→B→C) and the retrieval method for each level.

#### Writing to Generated Skill

In the generated SKILL.md's "Enum Parameters" section, provide the retrieval approach for each enumeration layered by `[API]` > `[DOM]` > `[AI]`. `[API]` and `[DOM]` must provide executable JS code; `[AI]` describes the interaction operations the Agent needs to perform (used when code cannot obtain the values). Must cover: retrieval method for each enumeration + dependency order when cascading exists. Operation steps also retain inline comments `// {param_name} enumeration retrieval: ...` to provide in-place context.

Enumerations that cannot be collected are marked `[collection failed]` and continue without blocking exploration.
