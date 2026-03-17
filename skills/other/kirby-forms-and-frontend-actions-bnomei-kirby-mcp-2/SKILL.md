---
name: kirby-forms-and-frontend-actions
description: Implements frontend forms and actions in Kirby (contact forms, file uploads, email with attachments, creating pages from frontend). Use when handling user input or building submission flows.
---

# Kirby Forms and Frontend Actions

## KB entry points

- `kirby://kb/scenarios/39-basic-contact-form`
- `kirby://kb/scenarios/40-frontend-file-uploads`
- `kirby://kb/scenarios/41-email-with-attachments`
- `kirby://kb/scenarios/42-creating-pages-from-frontend`
- `kirby://kb/scenarios/43-user-registration-and-login`

## Required inputs

- Form fields and validation rules.
- Spam protection choice and error handling expectations.
- Storage target and email settings.
- Upload constraints (MIME/size) if files are involved.

## Default controller flow

- Verify CSRF and require the expected POST fields.
- Validate and normalize input; return errors early.
- Apply a single spam guard (default: honeypot).
- Persist data or send email, then redirect with a success state.

## Error payload shape

```php
return [
  'errors' => ['email' => 'Invalid email'],
  'old' => $data,
];
```

## Upload storage convention

- Store files under a dedicated page (e.g. `page('uploads')`) or the current page.
- Normalize filenames and enforce MIME/size limits before saving.

## Common pitfalls

- Missing CSRF verification on POST handlers.
- Accepting uploads without MIME or size checks.

## Workflow

1. Clarify the form type, validation rules, spam protection, storage target, and email requirements.
2. Call `kirby:kirby_init` and read `kirby://roots`.
3. Inspect existing templates/controllers/snippets for patterns:
   - `kirby:kirby_templates_index`
   - `kirby:kirby_controllers_index`
   - `kirby:kirby_snippets_index`
4. Read relevant config options via `kirby://config/{option}` (e.g. `email`, `routes`) when needed.
5. Search the KB with `kirby:kirby_search` (examples: "basic contact form", "frontend file uploads", "email with attachments", "creating pages from frontend").
6. Implement controller-driven validation and CSRF checks; keep templates thin and escape output.
7. For uploads, enforce MIME/size limits and store files in safe locations.
8. Verify by submitting forms in a browser and rendering success/error states with `kirby:kirby_render_page`.
