# Publication Rubric

Use this rubric when converting private skills into public skills.

## 1. Source Inventory

Record the source skill name, source path, bundled files, referenced commands, referenced paths, and any README/plugin metadata that will be published.

Classify each piece of content:

| Class | Keep? | Treatment |
| --- | --- | --- |
| Reusable workflow | Yes | Keep and tighten. |
| Tool-specific command | Usually | Keep if portable; otherwise document setup. |
| Personal preference | Maybe | Generalize into an option or remove. |
| Private path or host | No | Replace with placeholder or setup variable. |
| Credential, token, cookie, key | No | Remove entirely. |
| Transcript quote | Rarely | Summarize or sanitize. |
| One-project fact | Usually no | Move to an example only if generic. |

## 2. Generalization Pass

Ask these questions:

- Could a new user understand when this skill applies from the description alone?
- Does the skill require the author's exact machine, aliases, repos, or memories?
- Are there hidden prerequisites that should become setup instructions?
- Are examples domain-specific by necessity, or just copied from the author's work?
- Is the skill teaching a reusable judgment pattern rather than narrating one past session?

## 3. Public Safety Pass

Remove or rewrite:

- Absolute home paths such as `/Users/<name>/...`
- Internal hostnames, SSH aliases, VPN-only URLs, private org names, private repos
- Email addresses, phone numbers, personal calendars, chat names, account IDs
- Cookies, tokens, API keys, OAuth scopes, screenshots with private data
- "My", "our internal", "the user's usual", or other context that assumes one person

Use placeholders like `<workspace>`, `<repo>`, `<skill-name>`, `<agent-skills-dir>`, and `<platform-config>`.

## 4. Packaging Checklist

- `skills/<skill-name>/SKILL.md` exists.
- Frontmatter has only `name` and `description`.
- Skill name is lowercase hyphen-case.
- Description starts with `Use when` and contains only trigger conditions.
- `SKILL.md` is short enough to scan.
- Long checklists, scripts, examples, and templates live in bundled resources.
- README install instructions match the actual folder names.
- Plugin metadata names the real skills in the package.

## 5. Promotion Copy

Good public copy says:

- Who it helps.
- What problem it solves.
- What evidence or workflow it uses.
- What platforms it supports.
- What is intentionally not included.

Avoid hype that implies deterministic automation when the repo only contains instructions.
