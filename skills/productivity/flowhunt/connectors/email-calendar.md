# Email + Calendar connector

Email and calendar are **optional context** for the audit — ActivityWatch is the core source and the audit runs fine without either. Wire them only if the user said so in intake (`email` / `calendar` from `setup.md` Step 1c).

Two ecosystems, two branches:

- `email` / `calendar` = `gmail` / `google` → **Google Workspace** section
- `email` / `calendar` = `outlook` → **Microsoft 365** section
- `email` = `other` → **IMAP fallback** section

None of these require you to create a Google Cloud or Azure project. Every path either ships from a big vendor (Anthropic / OpenAI / Google) or is a first-party protocol (IMAP + app password).

All paths give the agent **read-only** access to mail metadata (headers, subjects, dates, snippets) and calendar events — never write access. FlowHunt only reads.

Pick the branch matching the agent detected by `reference/environment.md`, and follow it exactly.

---
---

# GOOGLE WORKSPACE (Gmail + Calendar)

## Claude Code (and Claude Desktop)

**Source of truth:** https://support.claude.com/en/articles/10166901-use-google-workspace-connectors

### Flow

1. Open the connector settings page for the user:
   ```bash
   open "https://claude.ai/settings/connectors"   # macOS
   xdg-open "https://claude.ai/settings/connectors"  # Linux
   start "https://claude.ai/settings/connectors"   # Windows
   ```
2. Tell the user: "Kliknij **Connect** obok Gmail. Zaloguj się w Google, przeklikaj wszystkie zgody (Anthropic prosi o read-only). Zrób to samo dla Google Calendar. Potem wróć tutaj i napisz 'gotowe'."
3. When they confirm, verify by calling a Gmail tool:
   ```
   mcp__claude_ai_Gmail__gmail_get_profile
   ```
   If it returns the user's email address, Gmail is wired. Do the same for `mcp__claude_ai_Google_Calendar__list_calendars` for Calendar.
4. If verification fails, the connector did not propagate. Possible reasons:
   - User is in a Team/Enterprise workspace where the Owner hasn't enabled connectors org-wide. Tell the user: "Twój workspace wymaga zgody Ownera. Albo poproś kogoś kto ma admina, albo podłącz się na osobistym koncie Claude."
   - User is on Claude Code version older than v2.1.46 (before connector propagation). Tell them to update: `npm install -g @anthropic-ai/claude-code@latest`.

### Permissions hardening (optional but recommended)

In the connector UI the user can restrict each tool. Set these to "Always allow":
- `gmail_search_messages`
- `gmail_read_message` (only if you want snippets)
- `gmail_list_labels`
- `gmail_get_profile`

And set these to "Never allow":
- `gmail_create_draft`
- `gmail_send_message` (if exposed)
- Any calendar write tools

FlowHunt only reads; never writes.

## Codex CLI

**Source of truth:** https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan and https://developers.openai.com/codex/plugins

### Flow

1. Confirm the user is signed into Codex with a ChatGPT account (not an API key):
   ```bash
   codex auth status
   ```
   If they're on an API-key plan, fall through to the **IMAP fallback** section below. The one-click path requires the ChatGPT app ecosystem.
2. If signed in with ChatGPT Plus/Business: open the apps page:
   ```bash
   open "https://chatgpt.com/apps"
   ```
   Tell the user: "Włącz Gmail i Google Calendar w tej liście. OAuth zrobi się w przeglądarce, jeden klik."
3. Alternatively, inside Codex CLI in interactive mode: type `/apps` to see the status and enable apps from there.
4. Verify: inside the Codex composer the user types `$` — the app picker should list Gmail. If it does, it's wired.
5. OpenAI confirms: "Controls apply to all surfaces (ChatGPT web, Atlas, mobile, and Codex)." Apps enabled on chatgpt.com propagate to Codex CLI automatically.

### Codex Plugins directory (alternative zero-config path)

Inside Codex CLI interactive session:
```
/plugins
```
Opens the plugins marketplace in the browser. The curated `gmail@openai-curated` and `slack@openai-curated` plugins use the ChatGPT connector OAuth under the hood — same result, different UX.

## Gemini CLI

**Source of truth:** https://github.com/gemini-cli-extensions/workspace

This is the cleanest path of all four agents. Google ships its own Workspace extension that reuses the user's existing Gemini OAuth token (the `oauth-personal` mode every Gemini CLI user already has after first login).

### Flow

```bash
gemini extensions install https://github.com/gemini-cli-extensions/workspace
```

That's it. One command. No second browser flow, no API keys, no consent screen beyond what Gemini already asked for at first install.

Verify:

```bash
gemini extensions list | grep workspace
```

And inside Gemini CLI:

```
/gmail/search query:"newer_than:30d" max_results:500
```

Should return a list of message metadata. If it does, Gmail + Calendar + Drive + Docs + Sheets are all wired (the extension bundles the whole Workspace surface).

## OpenCode — IMAP + App Password

OpenCode has no native OAuth broker for Google. Use the **IMAP fallback** section below with `imap.gmail.com:993`. Calendar has no app-password equivalent — for OpenCode, **Calendar is skipped**. Tell the user that explicitly.

---
---

# MICROSOFT 365 (Outlook mail + Calendar)

Anthropic and OpenAI both ship **official, MCP-based, read-only Microsoft 365 connectors** now. There is no IMAP hackery for Claude Code and Codex — use the native connector.

**Shared requirement — read this before starting any branch:** the official Microsoft 365 connectors require a **Microsoft Entra tenant on a Microsoft 365 Business plan**, and a one-time consent by a tenant **Global Administrator**. Personal `@outlook.com` / `@hotmail.com` accounts are **not** supported by the native connectors — for a personal account, fall through to the **IMAP fallback** section.

Before wiring, ask the user:
> "Microsoft 365 firmowy czy osobiste konto Outlook.com? I czy masz dostęp do admina IT (Global Admin) — łączenie wymaga jednorazowej zgody admina tenanta."

If it's a personal account → IMAP fallback. If firmowy but they have no admin access → tell them email/calendar is skipped, the audit runs on ActivityWatch (which sees Outlook usage anyway).

## Claude Code (and Claude Desktop)

**Source of truth:** https://support.claude.com/en/articles/12542951-enable-and-use-the-microsoft-365-connector and https://claude.com/connectors/microsoft-365

The Microsoft 365 connector is Anthropic-hosted, MCP-based, read-only, and available on all Claude plans (Free / Pro / Max / Team / Enterprise). It covers **Outlook mail, Teams Calendar, Teams Chat, SharePoint, and OneDrive** — FlowHunt only uses mail + calendar.

### Flow

1. Open the connector settings page:
   ```bash
   open "https://claude.ai/settings/connectors"   # macOS
   xdg-open "https://claude.ai/settings/connectors"  # Linux
   start "https://claude.ai/settings/connectors"   # Windows
   ```
2. Tell the user: "Wejdź w **Browse connectors**, znajdź **Microsoft 365**, kliknij **Add / Connect**. Zaloguj się kontem firmowym Microsoft i przeklikaj zgody (read-only). Napisz 'gotowe' jak skończysz."
3. **First-time tenant consent:** if the user is the first person in their organization to connect, Microsoft shows an admin-consent screen. Only a Global Administrator can approve it. If the user is not an admin, tell them: "Twój tenant wymaga jednorazowej zgody Global Admina na connector. Poproś IT o zatwierdzenie aplikacji 'M365 MCP Server for Claude' / 'M365 MCP Client for Claude', potem dokończysz łączenie."
4. **Team / Enterprise Claude plans:** the connector must also be enabled org-wide first — an Owner goes to **Organization settings → Connectors → Browse connectors → Add "Microsoft 365"**. Until then it won't appear in personal settings.
5. Verify: ask the agent to search the user's recent Outlook mail (last 30 days, metadata only). If subjects/senders come back, it's wired. Do the same for a calendar-events query.

## Codex CLI

**Source of truth:** https://help.openai.com/en/articles/12512241-outlook-email-and-calendar-connectors-for-chatgpt and https://help.openai.com/en/articles/11487775-connectors-in-chatgpt

ChatGPT ships official **Outlook Email** and **Outlook Calendar** apps. Codex's plugin catalog (90+ connectors as of the April 2026 update) includes the full Microsoft 365 suite. Apps enabled on chatgpt.com propagate to Codex CLI.

### Flow

1. Confirm the user is signed into Codex with a ChatGPT account (not an API key): `codex auth status`. API-key plans → IMAP fallback.
2. Open the apps page:
   ```bash
   open "https://chatgpt.com/apps"
   ```
   Tell the user: "Włącz **Outlook Email** i **Outlook Calendar**. OAuth w przeglądarce, jeden klik. Zaloguj się kontem firmowym Microsoft."
3. Alternatively, inside Codex CLI interactive mode: `/apps` (or `/plugins` for the marketplace) and enable Outlook from there.
4. **Admin approval:** OpenAI notes that for Microsoft apps "some customers may need Microsoft Entra admin approval for updated scopes before new users can connect." Same as the Claude branch — if the connect screen stalls on a consent error, the tenant Global Admin must approve once.
5. Verify: in the Codex composer type `$` — the app picker should list Outlook. Or ask the agent to pull recent Outlook mail metadata.

## Gemini CLI

Google does **not** ship an official Microsoft 365 connector (its Workspace extension is Google-only), and FlowHunt does not use unofficial SaaS brokers. For Gemini CLI + Microsoft 365:

- **Personal `@outlook.com` account** → IMAP fallback section below works.
- **Business Microsoft 365** → no clean native path. Skip email + calendar. Tell the user: "Dla Gemini CLI nie ma oficjalnego connectora do firmowego Microsoft 365. Audit pójdzie na ActivityWatch (który i tak widzi czas w Outlooku) plus taski. Jak mail/kalendarz są kluczowe — odpal audit na Claude Code albo Codex."

## OpenCode

Same situation as Gemini — no native Microsoft broker.

- **Personal `@outlook.com` account** → IMAP fallback section below.
- **Business Microsoft 365** → skip email + calendar (business Exchange Online has basic-auth IMAP disabled, so the app-password path does not work). Audit runs on ActivityWatch + tasks.

---
---

# IMAP FALLBACK (any agent, any mailbox)

Use this when no native connector path works: OpenCode, an API-key-only Codex plan, a personal Outlook.com account, Proton/Apple Mail/other IMAP hosts, or any case where the native path failed.

**Important limitation:** business **Microsoft 365 / Exchange Online** has disabled basic-auth IMAP — the app-password path below works for **Gmail and personal Outlook.com**, not for a firmowy M365 tenant. For a business M365 tenant, use the native connector (Claude Code / Codex branches above) or skip mail entirely.

IMAP gives you **mail only** — no calendar. IMAP is an IETF RFC from 1988 and per-account app passwords are a first-party security feature of each mail provider; neither is going anywhere, and no SaaS broker sits in the middle.

### Step 1 — get an app password

The user must have 2-Step Verification enabled, then create an app password:

- **Gmail:** https://myaccount.google.com/apppasswords → app name `flowhunt` → Create. 16-char password, shown once.
- **Outlook.com (personal):** https://account.microsoft.com/security → Advanced security options → "App passwords" → Create.

### Step 2 — IMAP host per provider

| Provider | IMAP host | Port |
|---|---|---|
| Gmail | `imap.gmail.com` | 993 |
| Outlook.com (personal) | `outlook.office365.com` | 993 |
| Proton (via Bridge) | `127.0.0.1` | Bridge-assigned |
| Other | ask the user / check provider docs | 993 |

### Step 3 — install the IMAP MCP server

Requires `uv` (https://astral.sh/uv):

```bash
brew install uv                                   # macOS
curl -LsSf https://astral.sh/uv/install.sh | sh   # Linux / anywhere
```

### Step 4 — add the MCP server to the agent

**Claude Code / Claude Desktop** — add to `~/.claude.json` under `mcpServers`:
```json
{
  "mcpServers": {
    "flowhunt-email": {
      "command": "uvx",
      "args": ["mcp-email-server@latest", "stdio"],
      "env": {
        "MCP_EMAIL_SERVER_EMAIL_ADDRESS": "user@example.com",
        "MCP_EMAIL_SERVER_PASSWORD": "xxxx xxxx xxxx xxxx",
        "MCP_EMAIL_SERVER_IMAP_HOST": "imap.gmail.com",
        "MCP_EMAIL_SERVER_IMAP_PORT": "993",
        "MCP_EMAIL_SERVER_SMTP_HOST": "smtp.gmail.com",
        "MCP_EMAIL_SERVER_SMTP_PORT": "465"
      }
    }
  }
}
```

**OpenCode** — the same block under `mcp` in `~/.config/opencode/opencode.json` (with `"type": "local"` and `"enabled": true`).

**Codex** — the equivalent `[mcp_servers.flowhunt-email]` block in `~/.codex/config.toml`.

**Gemini** — `gemini mcp add flowhunt-email stdio -- uvx mcp-email-server@latest stdio`, then set the env vars separately.

Tell the user to edit the config file themselves and replace `user@example.com`, the password, and the IMAP/SMTP host for their provider. **DO NOT write secrets for them unless they insist.**

### Step 5 — restart the agent and verify

Restart the agent, then ask it to search mail from the last 30 days. If results come back, it works. The native connector is always better when available — it's one click, OAuth, full scopes, and includes calendar.
