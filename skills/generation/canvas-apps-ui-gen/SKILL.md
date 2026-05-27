---
name: canvas-apps-ui-gen
description: Generates paste-ready Power Apps Canvas App YAML. Invoke when the user wants to replicate a UI mockup, improve an existing Canvas app screen, or build a new screen from a text description. Also invoke when the user asks to "improve", "redesign", or "generate YAML" for a Canvas app screen.
argument-hint: path/to/screenshot.png or description
allowed-tools: Read, Glob, Write, WebFetch, Agent
---

You are an expert Power Apps Canvas App developer and orchestrator. When this skill is invoked, follow the process below exactly.

---

## PHASE 1 — MODE DETECTION

At invocation, determine whether an image is available:

**Image available** (`$ARGUMENTS` contains a file path, OR an image is pasted/dragged into the conversation):
- Load the image now (follow Phase 2 exactly)
- Proceed directly to Phase 3 — do **NOT** ask the mode question
- Mode (Replicate vs Improve) will be determined as part of Phase 3

**No image available** (`$ARGUMENTS` is empty or contains only non-path text, and no pasted image):
- Ask the user exactly this and wait for their answer:

"Which mode would you like to work in?

**1. Replicate** — You have a mockup, wireframe, or design screenshot. I'll replicate it in Power Apps YAML, staying true to the layout, colors, and proportions.

**2. Improvement** — You have a screenshot of an existing Power Apps screen you want modernized, redesigned, or polished.

**3. Build from scratch** — No image. Describe what you want and I'll generate YAML from your description."

- Mode 1 or 2 → ask for the image (Phase 2), then proceed to Phase 3
- Mode 3 → skip Phase 2, proceed directly to Phase 3 in text-only mode

---

## PHASE 2 — LOAD THE IMAGE

*(Skip this phase entirely if Mode 3 was selected in Phase 1.)*

Determine how the image was provided:

**Method A — File path in `$ARGUMENTS`:**
If `$ARGUMENTS` is non-empty and looks like a file path (contains `/` or `\`, or ends in `.png`, `.jpg`, `.jpeg`, or `.webp`), use the `Read` tool to load it. Treat the entire `$ARGUMENTS` string as the path — do NOT split on spaces (paths may contain spaces like `C:\Users\My Documents\screen.png`).

If the file cannot be read, tell the user: "I couldn't load the file at `[path]`. Please check the path is correct and the file is a PNG, JPG, or WEBP — or paste the image directly into the chat." Then stop.

**Method B — Image in conversation:**
If `$ARGUMENTS` is empty (or contains only non-path text), look for an image pasted or dragged into the current conversation. If no image is found, ask: "Please paste your image into the chat (a Canvas app screenshot, a UI mockup, a wireframe, or any design you want to turn into YAML), or provide a file path as an argument: `/canvas-apps-ui-gen C:\path\to\image.png`"

**If both file path and image are provided:** Prefer the file path argument — it is more explicit.

---

## PHASE 3 — COMBINED ANALYSIS AND QUESTIONS

This phase produces the structural description **and** asks all pre-generation questions in a **single response**. Do not split into two messages — the analysis and questions must appear together so the user can answer everything at once.

### Step A — Structural Description

Print a description covering:
1. **Layout sections**: Every distinct UI region (e.g., "A horizontal row of 4 KPI metric cards at the top", "A data table covering the bottom 65% of the screen")
2. **Component types identified**: Cards, table/grid, form fields, navigation bar, header, buttons, status badges, charts, text labels, etc.
3. **Approximate color scheme**: Dark/light background, accent colors visible
4. **Approximate section proportions**: What takes up most of the screen

Example format:
> "I can see the following:
> - A left sidebar (~130px wide) with a logo, vertical navigation gallery, and a profile row at the bottom
> - A top bar with a page title and breadcrumb (~64px tall)
> - A horizontal tab bar with 6 tabs
> - A centered form card (~440px wide) with product title, category, brand, variation, and action button fields
>
> Color scheme: light background (warm gray), white sidebar and cards, orange accent for active states."

*(In Mode 3 / text-only: print your understanding of the description the user provided instead of visual observations.)*

### Step B — Compatibility Check

Read `reference/canvas-apps-limitations.md`. Scan your structural description (or the user's text description in Mode 3) against every entry. Group any matches by their `Handle:` tag:

**Handle: auto** — Apply the Canvas Apps alternative silently. Track each substitution in an internal list (used later in Phase 4 Step 4). Do not mention these here.

**Handle: ask** — Include this block in the current response (user will answer alongside the other questions):

> **Canvas Apps compatibility — your input needed:**
> These elements cannot be implemented natively in Canvas Apps.
> Please choose an alternative for each:
>
> 1. [Element detected] — [one-line reason]
>    (a) [Alternative A]
>    (b) [Alternative B]
>    (c) Omit this element
>
> *(repeat for each `ask` match)*

**Handle: skip** — Include this block and proceed (no user decision needed):

> **Canvas Apps compatibility — elements omitted:**
> The following cannot be generated as Canvas Apps YAML and will be excluded from the output:
> - [Element]: [brief reason]

If no limitations are detected, omit all compatibility blocks entirely.

### Step C — Pre-generation Questions

Immediately after the description and any compatibility blocks, in the **same response**, output the questions block.

---

**If image was provided (mode not yet confirmed):**

> **Ready to generate — quick questions:**
>
> **1. What would you like to do with this design?**
> (a) **Replicate** — recreate this design faithfully as PA YAML
> (b) **Improve** — modernize and polish it (standardize spacing/typography, upgrade controls, add proper hover/focus states)
>
> **2. Where will you paste this YAML?**
> (a) Into an existing screen — I'll generate controls with no Screen wrapper
> (b) As a new screen — I'll generate a `Screens:` block with the screen name and all children
> (c) Just a specific section/component of a screen
>
> **3. Classic or Modern (Fluent) controls?**
> - **Classic** — minimal base styling, fully customizable; every color, border, font, and interaction state is individually tunable
> - **Modern / Fluent** — Microsoft Fluent 2 design built in; polished look, smooth animations, and accessible defaults
>
> *I'll extract the color palette and use the visible field names directly from the image. For responsive design, I'll default to No — mention it in your reply if you need mobile/tablet adaptation.*
>
> **Optional — changes from the image:** Anything you'd like to differ from what's shown? (e.g., "add a Notes textarea at the bottom", "replace the Brand field with a Supplier dropdown", "remove the sidebar"). Leave blank to proceed exactly as shown.

Wait for the user's single reply, then proceed to Phase 4.

---

**If Mode 3 (no image — text-only):**

> **Ready to generate — a few quick questions:**
>
> **1. Where will you paste this YAML?**
> (a) Into an existing screen — no Screen wrapper
> (b) As a new screen — full `Screens:` block
> (c) Just a specific section/component
>
> **2. Classic or Modern (Fluent) controls?**
> - **Classic** — fully customizable; every property individually tunable
> - **Modern / Fluent** — Fluent 2 design built in; polished defaults
>
> **3. What color palette should I use?**
> - Dark theme with blue accents (RGBA(35,36,47,1) background, RGBA(0,142,210,1) accent)
> - Light/white theme
> - Describe your own (e.g., "navy and gold", "corporate blue and white")
>
> **4. What is the overall layout pattern?**
> (e.g., sidebar + main content, full-width single column, wizard/stepped form, split pane, dashboard with cards)
>
> **5. What is the primary purpose of this screen?**
> (e.g., data table/list, data entry form, dashboard with KPIs, record detail view, settings page)

Wait for the user's single reply, then proceed to Phase 4.

---

## PHASE 4 — MULTI-AGENT YAML GENERATION

### Step 0: Resolve Paths

Before doing anything else, resolve two root paths used throughout Phase 4.

**A. Skill Directory (`SKILL_DIR`)**
Determine the absolute path to this skill's directory (the folder containing this SKILL.md file).
Use `SKILL_DIR` only for reading plugin assets: `agents/`, `reference/`, and `templates/`. Never write output files here.

**B. Output Directory (`OUTPUT_DIR`)**
Run this Bash command to get the user's working directory:

```bash
pwd
```

Store the result as `USER_CWD`. Then construct:
`OUTPUT_DIR = {USER_CWD}/canvas-apps-output`

Create it if it does not exist:

```bash
mkdir -p "{USER_CWD}/canvas-apps-output"
```

**Edge case:** If `USER_CWD` contains `.claude/plugins`, warn the user:
> "Note: your terminal appears to be inside the Claude plugins directory. Output will be saved to `{OUTPUT_DIR}`. Navigate to your project folder first if you intended otherwise."

Proceed regardless — do not stop.

Use `SKILL_DIR` for all read operations on plugin assets. Use `OUTPUT_DIR` for all write, read-back, and delete operations on generated files throughout Phase 4.

### Step 1: Generate Skeleton + Design Spec

Based on Phase 3 analysis and the user's answers, produce two artifacts and write them to temp files.

**Before writing, resolve the mode from the user's answer:**
- User answered (a) Replicate → proceed as replicate mode
- User answered (b) Improve → proceed as improvement mode
- Mode 3 invocation → proceed as text-only mode

**If the user specified modifications (optional changes field):** Incorporate them into both the skeleton and design spec before writing. Add a `MODIFICATIONS` section to the design spec listing each requested change. Build the skeleton to reflect those modifications — not the raw mockup.

#### Artifact 1: Structural Skeleton → write to `{OUTPUT_DIR}/temp-skeleton.md` using the Write tool directly (never Python or Bash)

A compact indented text tree showing control names, types, hierarchy, and high-level layout direction. Use this exact format:

```
Screen: [ScreenName]
Paste target: [a / b / c]

  screenRoot [GroupContainer, AutoLayout, fills screen]
  ├── sidebarContainer [GroupContainer, Vertical, fixed-width]
  │   ├── logoArea [GroupContainer, AutoLayout]
  │   │   ├── logoIcon [Image, icon]
  │   │   └── logoText [Label]
  │   ├── navGallery [Gallery, Vertical, items-cols: NavLabel|NavIcon|NavItemID, active-var: CurrentNavID, active-col: NavItemID]
  │   │   └── navItemRow [GroupContainer, ManualLayout]
  │   │       ├── navItemIcon [Image, icon, gallery-child]
  │   │       ├── navItemLabel [Label, gallery-child]
  │   │       └── navItemOverlay [Classic/Button, transparent overlay]
  │   └── profileRow [GroupContainer, AutoLayout]
  └── mainContent [GroupContainer, Vertical, fills remaining]
      ├── topBar [GroupContainer, Vertical]
      │   ├── pageTitle [Label]
      │   └── breadcrumb [Label]
      └── scrollableBody [GroupContainer, Vertical, scrollable]
          └── formCard [GroupContainer, Vertical, centered, card]
              ├── inputTitle [Classic/TextInput]
              └── actionRow [GroupContainer, AutoLayout]
                  ├── btnCancel [Classic/Button]
                  └── btnSave [Classic/Button]
```

Include ALL controls. Mark special roles in square brackets: `transparent overlay`, `icon`, `gallery-child`, `scrollable`, `centered`, `card`.

**Gallery data-contract (required for every Gallery control):** In addition to the role tags, every Gallery line must include three extra annotations that all specialist agents will read to stay coordinated:

- `items-cols: A|B|C` — the exact column names the controls-agent must use in the `Table()`. Derive names from the gallery's semantic purpose:
  - Nav/sidebar gallery → `NavLabel|NavIcon|NavItemID`
  - Tab gallery → `TabLabel|TabID`
  - Data-table row gallery → column names matching the visible fields in the design (e.g., `OrderName|Status|Amount|OrderID`)
  - Simple list gallery → `ItemLabel|ItemID`
- `active-var: CurrentX` — the global variable name that tracks the selected item. Always use the `Current` prefix (never `var`), followed by a semantic noun: `CurrentNavID`, `CurrentTabID`, `CurrentOrderID`. This variable is initialized in `OnVisible` and set in the overlay button's `OnSelect`.
- `active-col: X` — the column from `items-cols` that is compared against `active-var` to determine the active/selected state. This is always the ID/key column.

Example: `navGallery [Gallery, Vertical, items-cols: NavLabel|NavIcon|NavItemID, active-var: CurrentNavID, active-col: NavItemID]`

#### Artifact 2: Design Spec → write to `{OUTPUT_DIR}/temp-design-spec.md` using the Write tool directly (never Python or Bash)

Read `reference/design-spec-formats.md` now. Use the section matching the resolved mode:
- Replicate mode → **## Replicate Mode** section
- Improvement mode → **## Improvement Mode** section
- Text-only mode → **## Text-Only Mode** section

**For Improvement mode and Text-only mode — synthesize the DESIGN TOKENS block first, before filling in any other section:**

Use the following rules to populate each field. All specialist agents treat this block as the primary authority for their respective domains.

- **Palette**: Commit to exactly 7 RGBA values. Derive from the user's described purpose or screen context (e.g., "HR portal" → cool grays + blue; "field service app" → earthy + orange; "analytics dashboard" → dark + teal). Background and Surface must differ by at least 4 lightness points. Leave Accent-Secondary blank if only one accent is needed. Every fill in the output must use one of these 7 values or a transparent version — no independent color invention.

- **Typography**: Pick ONE font family for the entire screen. Do not mix fonts. Scale: Heading must be at least 2 PA size units larger than Body; Body at least 1 unit larger than Caption. Default (Classic controls, nothing suggesting otherwise): Heading=14, Body=11, Caption=9. For Modern controls, apply the Classic→Modern size conversion from `reference/sizing-reference.md`.

- **Density**: Infer from layout type:
  - Data tables / lists → compact: LayoutGap=8, PaddingH=12, PaddingV=8
  - Forms / record detail views → balanced: LayoutGap=12, PaddingH=16, PaddingV=12
  - Dashboards / landing pages → generous: LayoutGap=16, PaddingH=20, PaddingV=16

- **Radius**: Pick one value for containers (0=sharp, 4=slight, 6=standard, 8=rounded, 12=soft). Interactive controls get the same value or half — never more. Default: Container=6, Interactive=4.

- **State Colors**: All derived from Accent-Primary:
  - HoverFill: RGBA(accent_r, accent_g, accent_b, 0.08)
  - PressedFill: RGBA(accent_r, accent_g, accent_b, 0.15)
  - FocusedBorder: Accent-Primary at full opacity
  - DisabledFill: near-background (very low contrast)
  - DisabledColor: Text-Secondary at 0.38 opacity

Fill in the chosen format with values extracted from the screenshot / user answers. Write the result to `{OUTPUT_DIR}/temp-design-spec.md`.

After writing both files, proceed immediately to Step 2 — do **not** re-read `reference/controls-index.md` here (the controls-agent reads it directly).

---

### Step 2: Spawn Parallel Specialty Agents

Read the three agent instruction files from the `agents/` subdirectory of this skill:
- `agents/layout-sizing-agent.md`
- `agents/controls-agent.md`
- `agents/styling-agent.md`

Then launch all three agents **simultaneously in a single message** using the Agent tool. Each agent receives a prompt constructed from its instruction file content plus these specifics:

**For each agent, pass:**
- The full content of its instruction file (as the task description)
- The absolute path to `{OUTPUT_DIR}/temp-skeleton.md`
- The absolute path to `{OUTPUT_DIR}/temp-design-spec.md`
- `SKILL_DIR` (the skill directory absolute path, for reading reference docs in `reference/`)
- The control style preference (classic / modern) from the user's Phase 3 answer — pass this explicitly to the controls-agent so it selects the correct variants
- The absolute path to its output file:
  - Layout+Sizing → `{OUTPUT_DIR}/temp-layout-annotations.yaml`
  - Controls → `{OUTPUT_DIR}/temp-controls-annotations.yaml`
  - Styling → `{OUTPUT_DIR}/temp-styling-annotations.yaml`

Wait for all three agents to complete before proceeding to Step 3.

---

### Step 3: Assembly + QA

Read `agents/assembly-agent.md`. Launch the Assembly agent using the Agent tool with a prompt that includes:
- The full content of `agents/assembly-agent.md`
- Absolute paths to: `{OUTPUT_DIR}/temp-skeleton.md`, `{OUTPUT_DIR}/temp-layout-annotations.yaml`, `{OUTPUT_DIR}/temp-controls-annotations.yaml`, `{OUTPUT_DIR}/temp-styling-annotations.yaml`
- Absolute path to `{OUTPUT_DIR}/temp-design-spec.md` (needed for QA fidelity checks)
- `SKILL_DIR` (the skill directory absolute path, for reading `reference/controls-reference.md` during QA)
- Paste target (a, b, or c) and the screen name
- The output filename: determine a unique filename first using `Glob` on `{OUTPUT_DIR}/[ScreenName]-*-generated.yaml`. If `{OUTPUT_DIR}/[ScreenName]-1-generated.yaml` exists, use `-2-`, and so on.
- Data binding instructions (inline for paste target b; separate block for a and c)
- Responsive design flag (if user mentioned responsive in their Phase 3 reply) with screen name for `ScreenName.Size` formulas

The Assembly agent self-validates and self-fixes all QA issues before writing the output file. Wait for it to complete and confirm the output file was written.

---

### Step 4: Cleanup and Output

Delete the temp files using the Bash tool (never Python):
- `{OUTPUT_DIR}/temp-skeleton.md`
- `{OUTPUT_DIR}/temp-design-spec.md`
- `{OUTPUT_DIR}/temp-layout-annotations.yaml`
- `{OUTPUT_DIR}/temp-controls-annotations.yaml`
- `{OUTPUT_DIR}/temp-styling-annotations.yaml`

Then output to the user:

**1. Prominent file link (place this FIRST):**
> **Your YAML is ready:** Your file has been saved to `{OUTPUT_DIR}/[ScreenName-N-generated.yaml]`. Open it in your editor, press **Ctrl+A** then **Ctrl+C** to copy everything, then paste into Power Apps Studio.

**2. Paste instruction based on paste target:**
- **(a) or (c)**: "In PA Studio: open the tree view, right-click the target screen or container, and select **Paste code**."
- **(b) new screen**: "In PA Studio: right-click in the screen list panel and choose **Paste code**. If unavailable, create a blank screen (Insert → New Screen → Blank), right-click it in the tree view, select **Paste code**, and paste only the content under `Children:`. Then copy the `OnVisible` formula into the screen's `OnVisible` property."

**3. Canvas size note:**
"This is sized for a tablet canvas (1366px wide). If your app targets phone layout, reduce `LayoutMinWidth` values and set container widths to `=Parent.Width`."
(If responsive was requested: "This YAML uses `[ScreenName].Size` for responsiveness. Make sure your app is a **Tablet** canvas type, and in **Settings → Display**, turn off **Scale to fit** and **Lock Orientation**.")

**4. For paste targets (a)/(c) — data binding block:**
If the assembly agent's completion message contains an `ONVISIBLE_BLOCK` field, extract that formula and display it here in chat. Do NOT read it from the output file — the file contains only YAML. Format it as:

> **Also paste this into your screen's `OnVisible` property:**
> ```
> [formula from ONVISIBLE_BLOCK]
> ```

**5. If improvement mode — changes summary:**
A brief bullet list of the key improvements made (color palette applied, controls upgraded, spacing standardized, states added, etc.).

**6. YAML inline display (size-guarded):**
Count the lines in the output file. If **400 lines or fewer**, display the complete YAML in a fenced `yaml` code block. If **over 400 lines**, output: "The YAML is [N] lines — too large to display inline. Open the file above and press **Ctrl+A** → **Ctrl+C** to copy."

**7. QA warnings (if any):**
If the Assembly agent reported PA2105 version warnings or other non-blocking concerns, list them here:

> **QA warnings (non-blocking):**
> - [warning text]

Omit this block entirely if the Assembly agent reported no warnings.

**8. Auto-substitutions applied (if any):**
If any `Handle: auto` limitations were encountered during Phase 3 and silently substituted, list them here:

> **Substitutions applied automatically:**
> - [Original element] → [Canvas Apps alternative used]

Omit this block entirely if no `auto` substitutions occurred.

**On follow-up refinements:** If the user asks to change something, apply changes directly to the same output file using the Edit tool. For replicate follow-ups, change ONLY what was asked — do not adjust other parts.

---

## SELF-GROWING TEMPLATES

After generating YAML for a component type that has no matching template in `templates/`, offer:
"I generated [component type] without a reference template. Would you like me to save this as a new template so future generations can use it as a reference?"

If the user is interested, follow the staging process in **PROTECTED FILE CHANGES** below.

---

## PROTECTED FILE CHANGES

Templates in `templates/` are **immutable references**. Once a template has been accepted into that folder, it must not be edited — only read from during YAML generation.

### Adding a New Template

1. Write a preview to `output/staging-[name].yaml` inside the skill directory
2. Tell the user to paste the preview into Power Apps Studio and verify it renders correctly
3. Wait for the user to confirm the preview works
4. Promote: move the validated file to `templates/[name].yaml` inside the skill directory, and delete the staging file from `output/`

### Never Edit Existing Templates

If the AI needs something similar to an existing template but different, duplicate it as a new staging file — do not touch the original.

### Exception — Version Self-Healing

PA2105 version bumps are the one case where template files may be mechanically updated in place. These change only the `@version` suffix on control type strings and cannot break rendering.

---

## CRITICAL RULES (ALWAYS APPLY)

1. Read `reference/pa-yaml-rules.md` before generating the Skeleton — it contains the exact format rules, sizing strategies, and valid control types.
2. Read `reference/controls-reference.md` for valid property names and enum values.
3. **Never use `context: fork` on this skill itself** — it must remain conversational to access pasted images. However, the **Agent tool IS used within Phase 4** to spawn specialist workers. Those workers receive the pre-analyzed skeleton and design spec as text — they do not need access to the original image.
4. **Never write files unless the user explicitly confirms** (e.g., saving a new template). The temp files in Phase 4 are internal working files — these are fine.
5. **Never expose real data source names or connection strings** in generated YAML.
6. **Version self-healing**: If the user reports a PA2105 warning for any control, immediately update that control's `@version` everywhere it appears: the VALID CONTROL TYPES table in `reference/pa-yaml-rules.md`, all code examples in `reference/pa-yaml-rules.md`, the section heading in `reference/controls-reference.md`, and every `.yaml` file in `templates/`. Use the version number PA reports as current. The same PA2105 warning must never occur twice for the same control.
7. **Never use `Control: Screen`** — this causes PA2101. For new screens always use the `Screens:` top-level format documented in Phase 4 Step 3 and in `reference/controls-reference.md`.
8. **Control fidelity — never substitute an inferior control.** Always use the correct semantic control for the UI element. Use `reference/controls-index.md` to identify the right control. Version uncertainty is not a reason to substitute.
9. **Before using `TextInput@0.0.54`, `ComboBox@0.0.51`, or `Radio@0.0.25`:** Check whether you need `Default` (TextInput/Radio) or `SearchFields` (ComboBox). If yes, use the Classic variant instead. Never add these properties to the previous-gen controls — they cause PA2108.
10. **Never mix Classic and Modern control properties.** Always look up properties in `reference/controls-reference.md` under the exact control type you are using.
11. **No emojis or em dashes in generated text values** — never use emojis or em dashes (—) in any `Text`, `HintText`, `Placeholder`, `TrueText`, `FalseText`, `Tooltip`, or any other string property on a control, unless the user's source image explicitly contains them or the user explicitly requests them.
12. **Always use custom SVG icons — never `Classic/Icon@2.5.0`.** For every icon, use `Image@2.2.3` with an inline SVG. The `Classic/Icon` control must never appear in generated YAML.
13. **Output token budget — always stay within 32 000 tokens per response.** Write YAML to file first (Phase 4 Step 4), then apply the code-block size guard (400 lines threshold).
14. **HtmlText is display-only — never code interactions on it.** For any hyperlink or clickable link, use `Classic/Button@2.2.0` (or a Modern button) with `OnSelect: =Launch("<url>")`. Style it as a text-only button (no fill/border) to visually match a link. Never use `<a>` tags inside HtmlText as an interaction mechanism.
15. **Never use `Variant: GridLayout` on `GroupContainer`.** Use only `Variant: AutoLayout` or `Variant: ManualLayout` for `GroupContainer@1.5.0`. Direction must be expressed with `LayoutDirection`.
