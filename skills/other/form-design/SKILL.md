---
name: form-design
description: "Forms have three layers of guidance: helper text below the input explains what to enter, placeholder shows the expected format, and validation confirms correctness. Real-time validation for complex inputs. Submit enables only when the form is valid. Use when designing or reviewing any form, input field, or data entry UI."
metadata:
  priority: 8
  pathPatterns:
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "**/*.html"
    - "design-system/**"
    - "ui/**"
  promptSignals:
    phrases:
      - "form"
      - "input"
      - "validation"
      - "placeholder"
      - "helper text"
      - "field"
      - "submit"
      - "required"
      - "error message"
      - "fieldset"
retrieval:
  aliases:
    - form design
    - input validation
    - helper text
    - placeholder
    - form validation
    - real-time validation
    - submit button state
  intents:
    - design a form
    - add validation to inputs
    - write helper text
    - enable submit when valid
    - add real-time validation
    - improve form usability
  examples:
    - add helper text to this input
    - validate this field in real time
    - disable the submit button until the form is valid
    - design this form with proper validation
---

# Form Design

Forms are where users give the product data. Every unnecessary obstacle between the user and a completed form is a failure. The design goal is to make correct input easy and incorrect input obvious — before the user submits.

---

## The Three Guidance Layers

Each layer serves a distinct purpose. Do not collapse them.

### Layer 1 — Helper Text
Explains *what* to enter. Appears below the input, always visible, in small secondary text.

```
Email address
[                              ]
Use the email you signed up with.
```

- Write in plain language from the user's perspective
- Keep it to one sentence — if you need more, the field is too complex or misnamed
- Do not repeat the label ("Enter your email" below a label that says "Email" is redundant)
- Helper text is not a replacement for a label — the label is still required

### Layer 2 — Placeholder
Shows the *format* or an example value. Appears inside the input, disappears on typing.

```
[jane@example.com              ]
```

- Use a realistic example, not a description: `+358 40 123 4567` not `Enter phone number`
- Never use placeholder as a label — it disappears and leaves the user without context
- Keep it grey (`--color-text-secondary`) and lighter than actual input text
- Optional — not every field needs a placeholder

### Layer 3 — Validation
Confirms whether the input is correct. The most important layer.

```
Email address
[jane@           ] ← invalid
✗ Enter a valid email address.
```

**Validation timing:**
- **On blur** (leaving the field): default for most fields — validates once the user has finished
- **Real-time** (on input): use when the format is complex or the error is likely — password strength, IBAN, VAT number, URL, regex-heavy fields
- **On submit**: catches anything missed, scrolls to the first error

Real-time validation must be forgiving at the start — do not show an error the instant the user starts typing. Show it after a short debounce (300–500ms) or after the first character that makes the input definitively wrong.

---

## Submit Button State

The submit button enables when the form is valid. This is one of the clearest affordance signals in form design — the user sees the goal and knows when they have reached it.

```
[Submit]   ← disabled, low contrast, cursor: not-allowed
           (fields incomplete or invalid)

[Submit]   ← enabled, full colour, cursor: pointer
           (all required fields valid)
```

**Implementation:**
```html
<button type="submit" disabled={!isFormValid}>Submit</button>
```

For long or complex forms where real-time validation is not practical, do not disable the submit — validate on submit and scroll to errors instead. Disabled submit on a long form frustrates users who cannot tell what is missing.

**Loading state on submit:** Replace label with spinner, disable the button. Prevent double-submission.

---

## Field Anatomy

```
[Label]                           [Optional badge if optional]
[Input field                                                  ]
[Helper text — what to enter, format, constraints            ]
[Error message — appears below helper text on validation fail ]
```

```html
<div class="field">
  <label for="vat">VAT number <span class="optional">Optional</span></label>
  <input
    id="vat"
    type="text"
    placeholder="FI12345678"
    aria-describedby="vat-helper vat-error"
    aria-invalid="true"
  >
  <p id="vat-helper" class="helper-text">Finnish VAT numbers start with FI followed by 8 digits.</p>
  <p id="vat-error" class="error-text" role="alert">Enter a valid Finnish VAT number (e.g. FI12345678).</p>
</div>
```

---

## Required vs Optional

Mark the minority. If most fields are required, mark the optional ones. If most are optional, mark the required ones.

- Do not rely on colour alone — add a text label ("Required" or asterisk with legend)
- Place the required/optional indicator in the label, not only in the placeholder or helper text

```html
<label>Email <abbr title="Required">*</abbr></label>
<!-- or -->
<label>Phone <span class="badge">Optional</span></label>
```

---

## Grouping with Fieldset

Related fields belong in a `<fieldset>` with a `<legend>`. This is semantic HTML and helps screen readers announce the group context.

```html
<fieldset>
  <legend>Billing address</legend>
  <label>Street</label><input type="text">
  <label>City</label><input type="text">
  <label>Postal code</label><input type="text">
</fieldset>
```

Use fieldsets for:
- Address groups
- Payment details
- Radio button groups
- Checkbox groups

---

## Input Types

Use the correct `type` — browsers provide free validation, appropriate keyboards, and autofill.

| Data | Input type |
|---|---|
| Email | `type="email"` |
| Phone | `type="tel"` |
| URL | `type="url"` |
| Number | `type="number"` |
| Password | `type="password"` |
| Date | `type="date"` |
| Search | `type="search"` |
| Colour | `type="color"` |

On mobile, `type="email"` shows the email keyboard, `type="tel"` shows the numpad. These are free UX improvements.

---

## Autofill Support

Allow browsers to autofill. Do not disable it unless there is a security requirement.

```html
<input type="text"  autocomplete="name">
<input type="email" autocomplete="email">
<input type="tel"   autocomplete="tel">
<input type="text"  autocomplete="street-address">
<input type="text"  autocomplete="postal-code">
<input type="text"  autocomplete="cc-number">    <!-- credit card -->
<input type="password" autocomplete="new-password">
```

Correct `autocomplete` values reduce friction dramatically for returning users and on mobile.

---

## Review Checklist

- [ ] Every field has a visible label (not just placeholder)
- [ ] Helper text is below the input and explains what to enter
- [ ] Placeholder shows format or example, not a description
- [ ] Validation triggers on blur for simple fields, real-time for complex ones
- [ ] Error message is adjacent to the field that failed
- [ ] Error message is associated via `aria-describedby`
- [ ] Required/optional marked on the minority of fields
- [ ] Submit button is disabled when form is invalid (for short forms)
- [ ] Submit button shows a loading state and prevents re-submission
- [ ] Related fields are grouped in `<fieldset>` with `<legend>`
- [ ] Correct `type` attribute on all inputs
- [ ] `autocomplete` attributes set on address, contact, and payment fields
