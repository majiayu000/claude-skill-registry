---
name: kirby-security-and-auth
description: Secures Kirby sites with access restriction, user roles, permissions, and protected downloads. Use when implementing login/role-based access, permissions, or file protection.
---

# Kirby Security and Auth

## KB entry points

- `kirby://kb/scenarios/62-access-restriction-login`
- `kirby://kb/scenarios/43-user-registration-and-login`
- `kirby://kb/scenarios/63-files-firewall-protected-downloads`
- `kirby://kb/scenarios/64-permission-tricks-role-based`
- `kirby://kb/scenarios/67-indieauth-rel-me`

## Required inputs

- Protected pages/data and required roles.
- Login/logout flow and redirect rules.
- Download protection or route constraints.

## Role matrix template

| Role   | Pages | Actions | Downloads |
| ------ | ----- | ------- | --------- |
| admin  | all   | all     | all       |
| editor | edit  | publish | limited   |

## Default guard pattern

- Check `$kirby->user()` and required role/permission before returning content.
- Redirect or return a 403 for unauthorized requests.
- Enforce CSRF and validation on auth-related forms.

## Login redirect rule

- Store intended URL in the session and redirect after successful login.
- Fall back to the home page when no intent is stored.

## Common pitfalls

- Checking access only in templates while routes remain public.
- Returning a 404 for unauthorized access instead of a 403 or redirect.

## Verification checklist

- Test the role matrix across protected pages and downloads.
- Verify login/logout flows and session handling.
- Confirm CSRF failures render safely.

## Workflow

1. Clarify which pages/data are protected, required roles, and login/logout behavior.
2. Call `kirby:kirby_init` and read `kirby://roots`.
3. Inspect templates/controllers/blueprints to align with existing patterns:
   - `kirby:kirby_templates_index`
   - `kirby:kirby_controllers_index`
   - `kirby:kirby_blueprints_index`
4. For protected downloads or auth routes, inspect routes with `kirby:kirby_routes_index` and `kirby://config/routes` (install runtime if needed).
5. Search the KB with `kirby:kirby_search` (examples: "access restriction login", "user registration and login", "files firewall", "permission tricks", "page on own domain").
6. Implement least-privilege checks in templates/controllers or routes; enforce CSRF and validation on auth forms.
7. Verify by rendering protected pages (`kirby:kirby_render_page`) and manually testing login and download URLs.
