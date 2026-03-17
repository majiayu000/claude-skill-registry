---
name: "supabase-email-templates"
description: "Generate and deploy Supabase Auth email templates with hosted logos for reliable display; use when email images aren't displaying, updating email content/styling, or deploying template changes"
version: "2.0.0"
---

# Supabase Email Templates Skill

Manage Supabase Auth email templates with hosted logos for reliable display across all email clients.

## When to Use This Skill

Use this skill when:
- Email images are not displaying in received emails
- Need to update email template content or styling
- Adding new email templates to the system
- Updating the Ballee logo in emails
- Debugging email rendering issues
- Deploying template changes to production/staging

**DO NOT use** for:
- Transactional emails sent via Resend (use email-templates package directly)
- Custom notification emails (use notification system)
- SMTP configuration (use Supabase Dashboard)

## Quick Commands

```bash
# Generate templates locally (creates HTML from React Email)
pnpm email:templates:generate

# Deploy templates to production
pnpm email:templates:deploy

# Deploy to staging
pnpm email:templates:deploy --staging

# Verify current production templates
pnpm email:templates:deploy --verify

# Full workflow (generate + deploy)
pnpm email:templates:update
```

## Image Handling Best Practice

### Why Hosted Images (Not Base64)

Base64-encoded images are **blocked by Gmail and Outlook** (majority of email clients). Research shows:

| Method | Gmail | Outlook | Apple Mail | Email Size |
|--------|-------|---------|------------|------------|
| **Hosted (recommended)** | Works | Works | Works | Small |
| Base64 | Blocked | Blocked | Works | +30% bloat |
| CID embedded | Fails | Works | Works | Increases |

**Solution**: Use hosted images on `flow.ballee.app`:
- Works in all email clients when user allows images
- Small email size, fast delivery
- Good alt text provides fallback when images blocked
- Used by Amazon, GitHub, PayPal, Twitter

### Logo Configuration

Logo hosted at: `https://flow.ballee.app/images/ballee-logo-email.png`

Source file: `apps/web/public/images/ballee-logo-email.png` (120x120px PNG)

Defined in: `packages/email-templates/src/components/logo.tsx`

```typescript
export const DEFAULT_LOGO_URL =
  'https://flow.ballee.app/images/ballee-logo-email.png';
```

## Templates Managed

| Template | Supabase API Field | Local File |
|----------|-------------------|------------|
| Confirm Signup | `mailer_templates_confirmation_content` | `confirm-signup.html` |
| Invite User | `mailer_templates_invite_content` | `invite-user.html` |
| Magic Link | `mailer_templates_magic_link_content` | `magic-link.html` |
| Change Email | `mailer_templates_email_change_content` | `change-email-address.html` |
| Reset Password | `mailer_templates_recovery_content` | `reset-password.html` |
| Reauthentication | `mailer_templates_reauthentication_content` | `reauthentication.html` |

## Architecture

```
packages/email-templates/src/
├── components/
│   ├── logo.tsx              # Shared logo component (hosted URL)
│   └── wrapper.tsx           # Email wrapper (includes logo by default)
├── emails/
│   ├── auth-base.email.tsx   # Base template for auth emails
│   ├── confirm-signup.email.tsx
│   ├── invite-user.email.tsx
│   └── ...                   # Other email templates
└── lib/
    └── colors.ts             # Brand colors

scripts/
├── generate-supabase-templates.tsx    # Generates HTML from React Email
└── update-supabase-email-templates.sh # Deploys to Supabase via API

supabase-email-templates/              # Generated HTML files (gitignored)
├── confirm-signup.html
├── invite-user.html
└── ...
```

## Logo Management

### To Update the Logo

1. Create new logo as PNG (recommended: 120x120px)
2. Replace the file:
   ```bash
   # Replace the logo file
   cp new-logo.png apps/web/public/images/ballee-logo-email.png
   ```
3. Deploy to production (logo is served from `flow.ballee.app`)
4. Regenerate templates (optional, only if logo URL changes):
   ```bash
   pnpm email:templates:update
   ```

### To Change Logo URL

If hosting location changes, update `packages/email-templates/src/components/logo.tsx`:

```typescript
export const DEFAULT_LOGO_URL =
  'https://new-domain.com/path/to/logo.png';
```

Then regenerate and deploy templates.

## API Details

### Supabase Management API

**Endpoint**: `https://api.supabase.com/v1/projects/{project_ref}/config/auth`

**Method**: `PATCH`

**Authentication**: Bearer token from 1Password (`uipc6jse6q32hu3nyfh6qmssoq`)

**Project References**:
- Production: `csjruhqyqzzqxnfeyiaf`
- Staging: `hxpcknyqswetsqmqmeep`

## Troubleshooting

### Images Not Displaying

**Symptom**: Email received but logo shows broken image or placeholder

**Possible Causes**:
1. User has image blocking enabled (normal behavior)
2. Logo file not deployed to production server
3. Logo URL incorrect in templates

**Solution**:
```bash
# 1. Verify logo file exists on production
curl -I https://flow.ballee.app/images/ballee-logo-email.png

# 2. Verify templates use correct URL
pnpm email:templates:deploy --verify

# 3. If needed, regenerate and deploy
pnpm email:templates:update
```

### Template Variables Not Rendering

**Symptom**: Email shows `{{ .Email }}` instead of actual email address

**Cause**: URL-encoded template variables

**Solution**: The generation script automatically fixes these. Regenerate:
```bash
pnpm email:templates:generate
```

### 1Password Token Issues

**Symptom**: "Could not retrieve Supabase access token"

**Solution**:
```bash
# Login to 1Password CLI
op signin

# Verify token exists
op item get uipc6jse6q32hu3nyfh6qmssoq --fields password --reveal
```

### API Update Fails

**Symptom**: "Error updating templates" with API response

**Common Causes**:
1. Invalid HTML in templates - regenerate
2. Token expired - re-authenticate with `op signin`
3. Rate limiting - wait and retry

## Local Development

For local development, email templates are configured in `apps/web/supabase/config.toml`:

```toml
[auth.email.template.recovery]
subject = "Reset your password - Ballee"
content_path = "./supabase/templates/reset-password.html"
```

Local templates use file paths and are loaded when Supabase starts. Changes require:
```bash
pnpm supabase:web:stop && pnpm supabase:web:start
```

## Related Files

| File | Purpose |
|------|---------|
| `packages/email-templates/src/components/logo.tsx` | Shared logo component |
| `packages/email-templates/src/components/wrapper.tsx` | Email wrapper with logo |
| `packages/email-templates/src/emails/auth-base.email.tsx` | Base template for auth emails |
| `apps/web/public/images/ballee-logo-email.png` | Logo image file (120x120px) |
| `scripts/generate-supabase-templates.tsx` | Template generator script |
| `scripts/update-supabase-email-templates.sh` | Production deployment script |

## Workflow Example

**Scenario**: User reports logo not showing in password reset email

```bash
# 1. Verify logo file is accessible
curl -I https://flow.ballee.app/images/ballee-logo-email.png
# Should return HTTP 200

# 2. Verify current templates
pnpm email:templates:deploy --verify
# Output shows: ✅ recovery: hosted image - src="https://flow.ballee.app/..."

# 3. If templates correct, explain to user that email clients may block images
# by default. They need to click "Display images" or add sender to safe list.

# 4. If templates incorrect, regenerate and deploy
pnpm email:templates:update
```
