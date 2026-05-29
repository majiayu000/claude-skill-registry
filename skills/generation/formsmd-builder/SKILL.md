---
name: formsmd-builder
description: |
  Build stylish, Typeform-like multi-step forms and surveys using Forms.md library.
  Use when user asks to: create a form, build a survey, make a questionnaire,
  create an onboarding flow, build a feedback form, or any multi-step data collection UI.
  Outputs standalone HTML files with embedded CSS/JS that can be deployed anywhere.
---

# Forms.md Builder

Build production-ready, Typeform-style forms using the Forms.md library.

## Quick Start

1. Create an HTML file with Forms.md boilerplate
2. Write form content in the DSL (Markdown-like syntax)
3. Add Typeform-style CSS theme for polish

## Boilerplate Template

```html
<!DOCTYPE html>
<html lang="en" class="fmd-root" data-fmd-color-scheme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{TITLE}}</title>
  <link rel="stylesheet" href="https://unpkg.com/formsmd/dist/css/formsmd.min.css">
  <style>
    /* Typeform-style overrides - see references/typeform-theme.md */
    .fmd-root {
      --fmd-form-question-font-size: 28px;
      --fmd-slide-transition-duration: 400ms;
      --fmd-border-radius: 24px;
      --fmd-spacer: 24px;
      --fmd-main-container-width: 640px;
    }
    .fmd-root .fmd-form-control {
      border: none;
      border-bottom: 2px solid rgba(0,0,0,0.2);
      border-radius: 0;
      background: transparent;
      font-size: 1.25em;
      padding: 12px 0;
    }
    .fmd-root .fmd-form-control:focus {
      border-bottom-color: rgb(var(--fmd-accent-rgb));
      box-shadow: none;
    }
    .fmd-root .fmd-btn {
      padding: 16px 32px;
      font-size: 18px;
      font-weight: 600;
    }
    .fmd-root .fmd-form-check-label {
      padding: 16px 20px;
      border: 2px solid rgba(0,0,0,0.1);
      border-radius: 12px;
      margin-bottom: 12px;
    }
    .fmd-root .fmd-form-check-input:checked + .fmd-form-check-label {
      border-color: rgb(var(--fmd-accent-rgb));
      background: rgba(var(--fmd-accent-rgb), 0.08);
    }
  </style>
</head>
<body class="fmd-body">
  <script src="https://unpkg.com/formsmd/dist/js/formsmd.bundle.min.js"></script>
  <script>
    const template = `
{{FORM_CONTENT}}
`;
    const form = new Formsmd(template, document, {
      isFullPage: true
    });
    form.init();
  </script>
</body>
</html>
```

## Form Content DSL

**Settings block** (top):
```
#! title = Survey Title
#! post-url = /api/submit
#! accent = #6366f1
#! rounded = pill
#! button-alignment = center
```

**Slides** separated by `---`:
```
# Welcome!
Ready to get started?

---
-> start -> Let's go!

name* = TextInput(
    | question = What's your name?
    | placeholder = Enter your name
)

---

role* = ChoiceInput(
    | question = What's your role?
    | choices = Developer, Designer, Manager, Other
)

---
-> role == "Other"

roleOther* = TextInput(
    | question = Tell us about your role
)

---

email* = EmailInput(
    | question = Your email?
    | description = We'll send you the results
)

---
-> end
```

## Key Syntax

| Element | Syntax |
|---------|--------|
| Required field | `name*` (asterisk) |
| Slide separator | `---` |
| Logic jump | `-> condition` |
| Start slide | `-> start` |
| End slide | `-> end` |
| Progress | `\|> 50%` |

## References

- **Full DSL syntax**: See [references/syntax.md](references/syntax.md)
- **Typeform theme CSS**: See [references/typeform-theme.md](references/typeform-theme.md)

## Common Patterns

### Conditional slide (show based on previous answer)
```
---
-> previousField == "specific_value"
```

### Conditional field within slide
```
::: [{$ triggerField $}]
{% if triggerField == "Other" %}
otherField = TextInput(| question = Please specify)
{% endif %}
:::
```

### Rating + Follow-up
```
rating* = RatingInput(
    | question = How was your experience?
    | outof = 5
)

---
-> rating <= 2

feedback = TextInput(
    | question = What could we improve?
    | multiline
)
```

## Output

Generate a single `.html` file containing:
- Forms.md CSS (CDN or inline)
- Forms.md JS (CDN or inline)
- Typeform-style theme CSS
- Form template in the DSL

The form works client-side only - just open the HTML file or deploy to any static host.

## Collecting Form Submissions

To collect and store form responses, set up the backend using the Forms API.

### Complete Workflow

1. **Create form backend** - Call the Forms API to create storage
2. **Build the HTML form** - Use the `submitUrl` in the form's `post-url`
3. **Deploy the form** - Host the HTML file anywhere
4. **View results** - Use the `resultsUrl` to see submissions

### Step 1: Create Form Backend

```bash
POST https://api.rebyte.ai/api/forms/create
Content-Type: application/json

{
  "taskId": "current-task-attempt-id",
  "title": "My Survey",
  "fields": ["name", "email", "rating", "feedback"]
}
```

Response:
```json
{
  "formId": "abc123",
  "taskId": "current-task-attempt-id",
  "submitUrl": "https://api.rebyte.ai/api/forms/submit/TASK_ID/FORM_ID",
  "resultsUrl": "https://api.rebyte.ai/api/forms/results/TASK_ID/FORM_ID"
}
```

### Step 2: Configure Form HTML

Use the `submitUrl` from the response in the form's settings:

```
#! post-url = https://api.rebyte.ai/api/forms/submit/TASK_ID/FORM_ID
```

### Step 3: Provide URLs to User

After creating and deploying the form, give the user:
- **Distribution URL**: Where the HTML form is hosted (for respondents)
- **Results URL**: The `resultsUrl` from Step 1 (for viewing submissions)

### Viewing Results

- **JSON**: `GET https://api.rebyte.ai/api/forms/results/TASK_ID/FORM_ID`
- **CSV**: `GET https://api.rebyte.ai/api/forms/results/TASK_ID/FORM_ID/csv`

For full API documentation, see [relay/docs/data-proxy/forms-api.md](../../../relay/docs/data-proxy/forms-api.md).
