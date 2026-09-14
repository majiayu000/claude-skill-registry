---
name: wordpress-security-review
description: "Use when the user asks 'is my site secure', 'run a security audit', 'check for vulnerabilities', 'was my site hacked', or 'fix the vulnerable plugins'. Runs the Respira security audit, reads its indicators, coverage and known vulnerabilities honestly, never calls a partial scan clean, and fixes what it finds one approved step at a time."
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: audit
  respira_min_version: 9.0.0
---

# WordPress Security Review

Runs the security audit built into Respira, explains what it found in plain words, and fixes what can be fixed, one approved step at a time.

## What this skill does

A security check an agent improvises usually grades a site on whether a security plugin is installed. That says nothing about whether the site is patched, whether an administrator appeared last week, or whether the uploads folder runs PHP. The Respira audit answers those questions from evidence WordPress itself can verify, and it says which questions it could not answer.

This skill runs it, reads every part of the result, and keeps the report honest: a check that did not run is reported as not run, a scan that hit its limit is reported as partial, and a vulnerability database that could not be reached means "not checked", never "clean".

**Handles:**
- The audit: core checksums, administrators and their application passwords, plugins, themes, must-use plugins, cron hooks, indicators and coverage
- Known vulnerabilities: installed core, plugin and theme versions matched against the Wordfence vulnerability database (plugin 9.0 and later)
- The uploads execution probe, only with the owner's consent
- Fixes: plugin, theme and core security updates behind approval, and credential clean-up with explicit consent
- A second audit after the fixes, saying what cleared and what remains

## What this skill does NOT do

- **Call a site clean when it could not look.** Partial coverage, a check that did not run, or an unavailable vulnerability database are reported as exactly that.
- **Delete, deactivate or replace anything without asking.** Not plugins, not users, not files. The audit never runs clean-up queries, and neither does this skill.
- **Revoke a credential on its own judgement.** An application password is revoked only when the owner names it and says yes.
- **See the host.** Server cron, access logs, wp-config secrets and backups are outside what WordPress can verify. The audit says so in `coverage`, and so does the report.
- **Replace a forensic investigation.** Indicators are questions. A confirmed break-in needs the host and a professional.

## Requirements

- Respira for WordPress 9.0 or later for the known-vulnerability match, `respira_update_theme` and `respira_revoke_application_password`. On 8.x the audit still runs: say that the vulnerability match needs plugin 9.0, and list themes to update by hand.
- Plugin management switched on in Respira settings, for plugin and theme updates.
- A recent backup the owner can restore, confirmed before any update. Respira's page snapshots do not cover plugin, theme or core files.
- A connection made with an administrator's key. From 9.0 the audit answers administrators only, because its result names every administrator and credential.

## Trigger Phrase

- "is my site secure"

## Alternative Triggers

- "run a security audit"
- "check for vulnerabilities"
- "was my site hacked"
- "fix the vulnerable plugins"
- "security review"

## Execution Workflow

### Phase 1: Run the audit

1. `respira_get_site_context` to confirm the site and its Respira plugin version.
2. `respira_run_security_audit` with `deep_scan: true`. The deep scan inspects uploads, wp-content/cache and must-use plugin paths for executable files, within strict time, file and result limits. On plugin 9.0 and later it only reads. On older plugins it also writes and deletes one inert probe file in uploads, so ask the owner first there, because file-change monitors may report it.
3. Leave `probe_uploads_execution` off for now. Phase 3 asks for it.

### Phase 2: Read the whole result

Read every block and report each one in plain words:

- **`indicators`**: each has an `id`, a `severity` and a `summary`, and its `evidence` often carries a `note`. Report every indicator with its summary and note. An indicator is a question, not a verdict: `recent-administrator` looks the same for an account the owner added last week, which is why it asks.
- **`coverage`**: what was and was not checked.
  - `executable_file_scan` is `complete`, `partial` (the bounded scan reached a limit) or `not_run`. Partial or not run means the uploads were not fully checked; never describe them as clean.
  - `host_cron`, `host_access_logs`, `wp_config_secrets` and `external_backup_state` are false: Respira cannot see these. Say so once.
  - `application_passwords`, `database_file_privilege` and `wp2shell_database_artifacts` say whether each check completed or was unavailable.
  - `recent_administrators` gives the window in days and how many accounts it flagged, so a 0 is read against how far back it looked.
- **`known_vulnerabilities`** (plugin 9.0 and later): installed software matched against the vulnerability database. Its `status` is `ok` when the match ran, and then every match carries the version that fixes it: report them most severe first. `unavailable` means the database could not be consulted, and `reason` says why (for example, no Respira licence is connected); `not_run` means the call switched it off. In both cases, and when the block is missing because the plugin is older, say the vulnerability check did not run. Only `ok` with no matches means no known vulnerabilities were found. `coverage.known_vulnerabilities` repeats the status.
- **`checks`**: the evidence behind the indicators (core checksums, administrators and their application passwords, plugins, themes). Use it to answer follow-up questions, not to pad the report.
- **`warnings`**: repeat each one. They are written for the owner.

Build the verdict only from what ran. When coverage is partial, the vulnerability check did not run, or a high-severity indicator is present, the report cannot say "clean" or "secure". Say "no problems found in what was checked", then name what was not checked.

### Phase 3: The uploads probe, only with consent

`probe_uploads_execution: true` tests whether the web server would run PHP from the uploads folder, which is the difference between a stray file and a working backdoor. It writes one inert PHP file to uploads, requests it and deletes it. Ask first, in words close to these:

> One more check is available: whether your server would run a PHP file placed in uploads. It writes a harmless test file for a moment and deletes it. A security plugin or your host may log it as a new PHP file. Run it?

Run it only on a yes, with the same `deep_scan` setting, and report the `uploads-execute-php` indicator if it appears.

### Phase 4: Plan the fixes

Before the first change, say in one line that an update replaces the software's files, that Respira's page snapshots do not cover those files, and that the host's backup is the way back. Then propose an ordered plan, most severe first:

- Plugins with a known vulnerability and an update that reaches the fixed version
- Themes with a known vulnerability
- WordPress core, when the audit reports a security release for the site's own branch
- Application passwords on administrator accounts the owner does not recognise
- Anything with no published fix: recommend what to do and wait for the owner

Do not add anything that is not on the list. If the update WordPress offers is lower than the fixed version, or no update is offered (common for premium plugins with a lapsed licence), do not force it: say which ones and why.

### Phase 5: Fix, one approved step at a time

Every fix tool here is approval-gated: the first call returns `respira_approval_required` with an `approval_token`, and repeating the same call with that token completes it. Tell the owner what the call will do before sending the token back.

- **Plugins:** `respira_update_plugin` with the `slug`, one plugin at a time. After each one, load the home page; if it fails, stop the batch and report.
- **Themes:** `respira_update_theme`, the same way.
- **Core:** `respira_update_core_security` with the `advisory_id` and `target_version` the audit reported (never guessed), and `backup_confirmed: true` only after the owner confirms a recent backup. WordPress core has no automatic rollback, and the receipt says so.
- **Application passwords:** `respira_revoke_application_password` only when the owner names the credential and says yes to revoking that one. Never revoke one because it looks old or unused, and never several in one go.
- **Nothing else.** Never delete, deactivate or replace a plugin, delete a user or remove a file as part of a fix without asking first, even when an indicator points at it.

### Phase 6: Check again

1. Load the home page to confirm the site works.
2. Run `respira_run_security_audit` again with the same options.
3. Report what cleared, what remains, and what still needs a person: an update that was not offered, a credential the owner has not decided on, anything outside what WordPress can see.

The security page in the respira.press dashboard has a "Fix in AER" link that starts this same flow in Respira AER.

## Safety Model

- Reads first; nothing changes before the owner sees the plan
- The one check that writes, the uploads probe, runs only with consent and says what it will do
- Every fix is approval-gated and runs one at a time, with a home-page check between steps
- Nothing is deleted, deactivated or revoked without an explicit yes for that specific item
- Partial, not run and unavailable are reported as such, never rounded up to clean
- Updates have no Respira snapshot, so the owner's backup is confirmed first

## Honest Disclaimer

This skill reviews a WordPress site's security from inside WordPress.

It cannot: see the server, its logs, its cron or its backups; prove a site was never compromised; or patch a plugin whose author has not published a fix.

It can: check core files against WordPress.org, list every administrator and credential, match installed versions against a database of known vulnerabilities, find executable files where they should not be, and apply the published fixes one approved step at a time, then check again.

## Tooling

`respira_get_site_context`, `respira_run_security_audit`, `respira_list_plugins`, `respira_update_plugin`, `respira_update_theme`, `respira_update_core_security`, `respira_revoke_application_password`

## Telemetry

After run completion, fire-and-forget to `POST https://www.respira.press/api/skills/track-usage` with `skill_slug = wordpress-security-review`, site and version context, duration, indicator counts by severity, the number of known vulnerabilities and the number of fixes applied. No logins, credentials, file paths or IP addresses are sent. Never block the user on telemetry.

## Related Skills

- WordPress Site DNA (the wider archaeology; its security step uses this audit)
- Respira Site Audit (SEO, accessibility and performance, with a security summary)
- Technical Debt Audit (plugins nobody uses are attack surface too)

---

Built by Respira for WordPress
https://respira.press/skills/wordpress-security-review
