---
name: interface-auditor
version: 1.0.0
description: Detect UX antipatterns (smells) in interface descriptions using the uxuiprinciples smell taxonomy. Returns structured findings with matched symptoms, severity, and step-by-step remediation recipes. API key optional — full remediation recipes require uxuiprinciples.com API Access.
author: uxuiprinciples
homepage: https://uxuiprinciples.com
tags:
  - ux
  - ui
  - antipatterns
  - smells
  - audit
  - remediation
env:
  UXUI_API_KEY:
    description: API key from uxuiprinciples.com (pro tier unlocks full smell taxonomy with remediation recipes, time estimates, and refactor prompts)
    required: false
---

```toml
[toolbox.list_smells]
description = "List all UX smells for a category. Valid categories: efficiency, error-prevention, feedback, learnability, accessibility, consistency. Returns smell IDs, names, symptoms, and remediation recipe titles."
command = "curl"
args = ["-s", "-H", "Authorization: Bearer ${UXUI_API_KEY}", "https://uxuiprinciples.com/api/v1/smells?category={category}"]

[toolbox.lookup_smell]
description = "Fetch a specific UX smell by ID. Returns full data: symptoms, detection time, related principles, recipe steps, before/after examples, and AI prompts."
command = "curl"
args = ["-s", "-H", "Authorization: Bearer ${UXUI_API_KEY}", "https://uxuiprinciples.com/api/v1/smells?id={smell_id}"]
```

## What This Skill Does

You audit interface descriptions for UX smells: named antipatterns that signal design problems before user testing. Each smell has a canonical set of symptoms, a detection approach, and a remediation recipe with numbered steps.

You match symptoms from the interface description to the smell taxonomy, then return structured JSON. When `UXUI_API_KEY` is set, you call the toolbox to retrieve full recipe steps, time estimates, and related principle codes. Without a key, you apply the taxonomy from internal knowledge and note the limitation.

The output is always JSON. No prose audit reports.

## Smell Taxonomy

The taxonomy covers 8 smells across 6 categories. Each smell maps to one or more Nielsen heuristics and related uxuiprinciples codes.

### Category: efficiency
**Symptoms of this category:** Too many visible elements, redundant steps, unnecessary clicks, information density causing scroll fatigue.

| Smell ID | Name | Core Signal |
|----------|------|-------------|
| `overloaded-screen` | Overloaded Screen | More than 7 distinct action areas visible; users say "where do I start?" |
| `click-cemetery` | Click Cemetery | Users must click 3+ times to complete a simple task; dead-end paths with no outcome |

### Category: error-prevention
**Symptoms of this category:** Forms with high abandonment, no inline validation, errors revealed only after submission.

| Smell ID | Name | Core Signal |
|----------|------|-------------|
| `form-graveyard` | Form Graveyard | More than 10 required fields visible at once; no inline validation; submit-only error display |

### Category: feedback
**Symptoms of this category:** Actions with no visible result, dead ends with no guidance, silent failures.

| Smell ID | Name | Core Signal |
|----------|------|-------------|
| `silent-errors` | Silent Errors | Errors occur but no message is shown; user does not know what went wrong or what to do next |
| `dead-end-states` | Dead-End States | Empty state or error with no action to take; user is stuck |

### Category: learnability
**Symptoms of this category:** Users cannot find key features, navigation labels are opaque, interface does not match mental models.

| Smell ID | Name | Core Signal |
|----------|------|-------------|
| `mystery-navigation` | Mystery Navigation | Unclear labels, icon-only navigation with no labels, features users cannot find on first attempt |

### Category: accessibility
**Symptoms of this category:** Low color contrast, color as the only information signal, missing labels.

| Smell ID | Name | Core Signal |
|----------|------|-------------|
| `contrast-blindness` | Contrast Blindness | Text on background with contrast ratio below 4.5:1; relying on color alone to communicate status |

### Category: consistency
**Symptoms of this category:** Same action named differently in different places, button styles vary without semantic reason, patterns that differ across screens.

| Smell ID | Name | Core Signal |
|----------|------|-------------|
| `inconsistent-actions` | Inconsistent Actions | Submit is "Save" on one screen and "Continue" on another with no semantic difference; visual styles for equivalent actions differ |

## Audit Workflow

Follow these steps in order.

### Step 1: Extract Signals from Description

Read the interface description and extract every observable signal:
- Counts (number of fields, buttons, navigation items, steps)
- Labels and copy (button text, navigation labels, error messages)
- Layout patterns (where elements are placed, what is visible above the fold)
- Feedback patterns (what happens after user actions)
- Color and contrast mentions
- Mobile vs desktop context

### Step 2: Map Signals to Smell Categories

For each signal, determine which smell categories it most likely belongs to:

| Signal Type | Primary Categories |
|-------------|-------------------|
| High element count, density | efficiency |
| Form with many fields | error-prevention |
| Missing feedback after actions | feedback |
| Unclear labels, hidden features | learnability |
| Color mentions, low contrast | accessibility |
| Same action described differently | consistency |

### Step 3: Fetch Smell Data (if API key is set)

For each suspected category, call `list_smells` with the category name. Review returned symptoms against your extracted signals.

Then for each matched smell, call `lookup_smell` with the smell ID to get the full recipe.

If `UXUI_API_KEY` is not set, or if calls return non-200 status, continue with internal taxonomy knowledge. Set `api_enriched: false`.

### Step 4: Match Symptoms

For each smell, list which specific symptoms from the taxonomy match the description. A smell is "detected" when two or more symptoms match, or one critical symptom matches with high confidence.

A smell is "suspected" when one weak signal matches but the description does not provide enough detail to confirm.

### Step 5: Assign Severity

| Severity | Criteria |
|----------|----------|
| `critical` | The smell blocks primary task completion or causes data loss, abandonment, or accessibility failure |
| `warning` | The smell degrades the experience and will affect conversion or satisfaction metrics measurably |
| `suggestion` | The smell is present but does not block users; fixing it would improve metrics |

### Step 6: Output JSON

Return exactly this structure. No prose before or after the JSON block.

```json
{
  "interface_description_summary": "One sentence summarizing what was audited.",
  "smells_detected": [
    {
      "id": "overloaded-screen",
      "name": "Overloaded Screen",
      "category": "efficiency",
      "severity": "critical|warning|suggestion",
      "matched_symptoms": [
        "Exact symptom text that matches the description.",
        "Second matched symptom."
      ],
      "message": "Specific explanation of how this smell manifests in the described interface.",
      "recipe_summary": "One-sentence summary of the fix approach.",
      "recipe_steps": [
        {
          "step": 1,
          "action": "Step title from recipe.",
          "detail": "Supporting detail from recipe."
        }
      ],
      "time_estimate": "30-45 minutes",
      "related_principles": ["cognitive-load", "progressive-disclosure"],
      "before_example": "Short before state description.",
      "after_example": "Short after state description."
    }
  ],
  "smells_suspected": [
    {
      "id": "string",
      "name": "string",
      "category": "string",
      "reason": "Why this smell might be present but could not be confirmed from the description."
    }
  ],
  "clean_areas": [
    "Description of what the interface does well with respect to UX patterns."
  ],
  "priority_order": ["overloaded-screen", "form-graveyard"],
  "api_enriched": true,
  "api_note": "null or 'Install the uxuiprinciples API key for full remediation recipes, time estimates, and AI refactor prompts. See uxuiprinciples.com/pricing'"
}
```

`priority_order` lists detected smell IDs ordered from most to least urgent. Critical smells first, then warnings affecting the primary user action.

`recipe_steps` should be populated from the API when enriched. When not enriched, provide a condensed 3-step version from internal knowledge.

## Severity Guidelines

**Contrast Blindness is always `critical`** when detected. Accessibility failures affect all users.

**Overloaded Screen and Form Graveyard are `critical`** when the count-based signals are clearly over threshold (15+ elements, 12+ form fields). They are `warning` when signals suggest overload but counts are not stated.

**Silent Errors and Dead-End States are `critical`** when the interface description shows error scenarios with no feedback. They are `warning` when feedback exists but is incomplete or delayed.

**Mystery Navigation and Inconsistent Actions are `warning`** by default. Escalate to `critical` only when the primary task requires the missing navigation path.

## Edge Cases

**No smells detected:** Return `smells_detected: []`. Populate `clean_areas` with at least 2 observations. This is valid and correct output.

**Description does not mention error states:** Do not assume `silent-errors` is present. Add it to `smells_suspected` with a note like "Error handling not described; verify inline validation and failure states."

**Icon-only navigation mentioned:** Flag `mystery-navigation` as at least `warning`. Icons without labels consistently fail learnability tests.

**"Simple" or "minimal" interface:** Take the description at face value. Do not invent complexity. If signals are absent, output fewer detected smells.

**Mobile interface:** Apply tighter thresholds. More than 5 navigation items at root level maps to `mystery-navigation warning`. Touch targets under 44px map to `contrast-blindness suggestion` (accessibility bucket, closest match).

**Ambiguous count ("several buttons", "a few fields"):** Treat "several" as 5-7, "a few" as 3-4, "many" as 8+. State the assumption in `message`.

**Two or more smells share the same root cause:** Detect both. Cross-reference them in `message` with "This compounds the [other-smell-id] finding."

## Examples

### Example 1: Form with Abandonment Signals

**Input:**
```
Registration form asking for: first name, last name, email, password, phone number, company name, job title, company size, country, city, postal code, industry, referral source, marketing consent. All fields shown at once. Submit button at the bottom.
```

**Expected output structure:**
```json
{
  "interface_description_summary": "14-field registration form with all fields visible at once and submit at bottom.",
  "smells_detected": [
    {
      "id": "form-graveyard",
      "name": "Form Graveyard",
      "category": "error-prevention",
      "severity": "critical",
      "matched_symptoms": [
        "Too many required fields visible at once",
        "Users start but never finish"
      ],
      "message": "14 fields displayed simultaneously exceeds cognitive capacity and signals high abandonment risk. Baymard Institute data shows forms with more than 7 visible required fields have abandonment rates above 60%.",
      "recipe_summary": "Break the form into a 3-step wizard with 4-5 fields per step and inline validation.",
      "recipe_steps": [
        {
          "step": 1,
          "action": "Audit required fields ruthlessly",
          "detail": "Every required field is a potential dropout. Phone, company size, and referral source can be deferred post-registration."
        },
        {
          "step": 2,
          "action": "Break into logical steps",
          "detail": "Step 1: Account (email, password). Step 2: Identity (name, company, title). Step 3: Context (country, industry, consent)."
        },
        {
          "step": 3,
          "action": "Add inline validation on blur",
          "detail": "Validate email format and password strength as users type, not after submit."
        }
      ],
      "time_estimate": "30-45 minutes",
      "related_principles": ["progressive-disclosure", "serial-position-effect", "cognitive-load"],
      "before_example": "Registration form with 14 required fields, validation on submit only",
      "after_example": "3-step wizard with 4-5 fields each, inline validation, deferred optional fields"
    }
  ],
  "smells_suspected": [
    {
      "id": "silent-errors",
      "name": "Silent Errors",
      "category": "feedback",
      "reason": "Inline validation not mentioned in description. Verify whether error messages appear on blur or only on submit."
    }
  ],
  "clean_areas": [],
  "priority_order": ["form-graveyard"],
  "api_enriched": false,
  "api_note": "Install the uxuiprinciples API key for full remediation recipes, time estimates, and AI refactor prompts. See uxuiprinciples.com/pricing"
}
```

### Example 2: Navigation Audit

**Input:**
```
Mobile app with a bottom navigation bar showing 4 icons only: no labels under the icons.
```

**Expected output structure:**
```json
{
  "interface_description_summary": "Mobile app with icon-only bottom navigation (4 items, no labels).",
  "smells_detected": [
    {
      "id": "mystery-navigation",
      "name": "Mystery Navigation",
      "category": "learnability",
      "severity": "warning",
      "matched_symptoms": [
        "Icon-only navigation with no labels"
      ],
      "message": "Icon-only navigation requires users to learn icon meanings before they can navigate. NNGroup usability studies consistently show icon-only navigation reduces first-attempt success rates, especially for new users.",
      "recipe_summary": "Add short text labels under each navigation icon.",
      "recipe_steps": [
        { "step": 1, "action": "Add text labels under all icons", "detail": "Labels of 1-2 words maximum. Match label to the primary action (Home, Search, Inbox, Profile)." },
        { "step": 2, "action": "Test icon recognition without labels first", "detail": "If recognition is below 90% on first attempt, the icon should be replaced, not just labeled." },
        { "step": 3, "action": "Ensure touch target is 44px minimum per item", "detail": "Labels increase the tap target area, reducing mistouch errors on small screens." }
      ],
      "time_estimate": "15-30 minutes",
      "related_principles": ["recognition-rather-than-recall", "mental-model"],
      "before_example": "4 icons with no labels in bottom nav",
      "after_example": "4 icons each with a 1-2 word label beneath"
    }
  ],
  "smells_suspected": [],
  "clean_areas": [
    "Four-item navigation stays within Hick's Law optimal range (3-5 items for time-critical decisions)."
  ],
  "priority_order": ["mystery-navigation"],
  "api_enriched": false,
  "api_note": "Install the uxuiprinciples API key for full remediation recipes, time estimates, and AI refactor prompts. See uxuiprinciples.com/pricing"
}
```

## Completion Criteria

The skill output is complete when:

1. Every detected smell has an `id` that matches the taxonomy (one of the 8 IDs listed above)
2. Every smell in `smells_detected` has at least one entry in `matched_symptoms`
3. `severity` is one of: `critical`, `warning`, `suggestion`
4. `recipe_steps` has at least 3 steps per detected smell (from API or internal knowledge)
5. `priority_order` lists only IDs from `smells_detected`, not `smells_suspected`
6. `api_enriched` accurately reflects whether toolbox calls returned successful data
7. The output is valid JSON with no prose before or after
8. When `smells_detected` is empty, `clean_areas` has at least 2 entries
