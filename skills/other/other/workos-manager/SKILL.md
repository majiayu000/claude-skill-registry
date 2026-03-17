---
name: WorkOS Manager
description: Complete WorkOS authentication management including OAuth, SSO, SCIM, email templates, domain verification, and user management. Use for enterprise auth configuration.
---

# WorkOS Manager Skill

This skill provides comprehensive access to WorkOS Management API for configuring enterprise authentication for Nanobanna Pro.

## Configuration

### Environment Variables
```env
WORKOS_API_KEY=${WORKOS_API_KEY}
WORKOS_CLIENT_ID=${WORKOS_CLIENT_ID}
WORKOS_ORG_ID=${WORKOS_ORG_ID}
WORKOS_REDIRECT_URI=https://life-os-banner.verridian.ai/api/auth/callback
WORKOS_WEBHOOK_SECRET=${WORKOS_WEBHOOK_SECRET}
```

> **Note**: Get actual values from server/.env or environment variables. Never commit actual secrets.

### API Base URL
```
https://api.workos.com
```

---

## When to Use

- Configuring OAuth providers (Google, GitHub, Microsoft)
- Setting up Enterprise SSO connections
- Managing SCIM directory sync
- Configuring email templates and branding
- Domain verification for email
- User management and authentication flows
- Magic link / passwordless login setup

---

## Available Operations

### 1. Organization Management

#### List Organizations
```bash
curl -X GET "https://api.workos.com/organizations" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

#### Get Organization Details
```bash
curl -X GET "https://api.workos.com/organizations/org_01KETHAB24WTQT83FRYBETZGPW" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

#### Update Organization
```bash
curl -X PUT "https://api.workos.com/organizations/org_01KETHAB24WTQT83FRYBETZGPW" \
  -H "Authorization: Bearer $WORKOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nanobanna Pro",
    "allow_profiles_outside_organization": true,
    "domains": ["verridian.ai", "nanobanna.com"]
  }'
```

---

### 2. SSO Connection Management

#### List SSO Connections
```bash
curl -X GET "https://api.workos.com/connections?organization_id=org_01KETHAB24WTQT83FRYBETZGPW" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

#### Create SSO Connection (Google)
```bash
curl -X POST "https://api.workos.com/connections" \
  -H "Authorization: Bearer $WORKOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "organization_id": "org_01KETHAB24WTQT83FRYBETZGPW",
    "connection_type": "GoogleOAuth",
    "name": "Google OAuth"
  }'
```

#### Create SSO Connection (GitHub)
```bash
curl -X POST "https://api.workos.com/connections" \
  -H "Authorization: Bearer $WORKOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "organization_id": "org_01KETHAB24WTQT83FRYBETZGPW",
    "connection_type": "GitHubOAuth",
    "name": "GitHub OAuth"
  }'
```

---

### 3. Directory Sync (SCIM)

#### List Directories
```bash
curl -X GET "https://api.workos.com/directories?organization_id=org_01KETHAB24WTQT83FRYBETZGPW" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

#### List Directory Users
```bash
curl -X GET "https://api.workos.com/directory_users?directory=dir_xxx" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

---

### 4. User Management

#### List Users
```bash
curl -X GET "https://api.workos.com/user_management/users" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

#### Get User by Email
```bash
curl -X GET "https://api.workos.com/user_management/users?email=user@example.com" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

#### Create User
```bash
curl -X POST "https://api.workos.com/user_management/users" \
  -H "Authorization: Bearer $WORKOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "email_verified": false
  }'
```

#### Delete User
```bash
curl -X DELETE "https://api.workos.com/user_management/users/user_xxx" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

---

### 5. Magic Link (Passwordless)

#### Send Magic Link
```bash
curl -X POST "https://api.workos.com/user_management/magic_auth/send" \
  -H "Authorization: Bearer $WORKOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "redirect_uri": "https://life-os-banner.verridian.ai/api/auth/callback"
  }'
```

---

### 6. Email Verification

#### Send Verification Email
```bash
curl -X POST "https://api.workos.com/user_management/users/user_xxx/email_verification/send" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

#### Verify Email Code
```bash
curl -X POST "https://api.workos.com/user_management/email_verification/verify" \
  -H "Authorization: Bearer $WORKOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "123456"
  }'
```

---

### 7. Domain Verification

#### Add Domain
```bash
curl -X POST "https://api.workos.com/organizations/org_01KETHAB24WTQT83FRYBETZGPW/domains" \
  -H "Authorization: Bearer $WORKOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "verridian.ai"
  }'
```

#### Verify Domain (After DNS Records Added)
```bash
curl -X POST "https://api.workos.com/organizations/org_01KETHAB24WTQT83FRYBETZGPW/domains/dom_xxx/verify" \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

---

## Email Templates Configuration

### Branding Settings

Configure via WorkOS Dashboard or API:

#### Update Branding
```bash
curl -X PUT "https://api.workos.com/user_management/email_templates/branding" \
  -H "Authorization: Bearer $WORKOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "logo_url": "https://life-os-banner.verridian.ai/logo.png",
    "primary_color": "#D4AF37",
    "background_color": "#1a1a2e",
    "text_color": "#ffffff",
    "link_color": "#D4AF37",
    "button_color": "#D4AF37",
    "button_text_color": "#1a1a2e",
    "font_family": "Inter, system-ui, sans-serif"
  }'
```

### Email Template Types

WorkOS supports customization of these email templates:

1. **Magic Link Email** - Passwordless login
2. **Email Verification** - Verify user email address
3. **Password Reset** - Reset forgotten password
4. **Invitation Email** - Invite new users
5. **MFA Enrollment** - Multi-factor authentication setup

### Recommended Template Content

#### Magic Link Email
```html
Subject: Sign in to Nanobanna Pro

<table style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 16px; padding: 40px;">
  <tr>
    <td align="center">
      <img src="https://life-os-banner.verridian.ai/logo.png" width="180" alt="Nanobanna Pro" />
    </td>
  </tr>
  <tr>
    <td style="color: #ffffff; font-family: Inter, sans-serif; padding: 20px;">
      <h1 style="color: #D4AF37; margin-bottom: 16px;">Sign In to Your Account</h1>
      <p style="font-size: 16px; line-height: 1.6;">
        Click the button below to securely sign in to Nanobanna Pro. This link will expire in 15 minutes.
      </p>
    </td>
  </tr>
  <tr>
    <td align="center" style="padding: 24px;">
      <a href="{{magic_link}}" style="background: linear-gradient(135deg, #D4AF37 0%, #C5A028 100%); color: #1a1a2e; padding: 16px 48px; border-radius: 12px; text-decoration: none; font-weight: 600; font-size: 16px; display: inline-block; box-shadow: 0 4px 14px rgba(212, 175, 55, 0.3);">
        Sign In Securely
      </a>
    </td>
  </tr>
  <tr>
    <td style="color: #888; font-size: 14px; padding: 20px; text-align: center;">
      <p>If you didn't request this email, you can safely ignore it.</p>
      <p style="margin-top: 16px;">
        <a href="https://life-os-banner.verridian.ai" style="color: #D4AF37;">Nanobanna Pro</a> - AI-Powered Banner Design
      </p>
    </td>
  </tr>
</table>
```

#### Email Verification
```html
Subject: Verify your email for Nanobanna Pro

<table style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 16px; padding: 40px;">
  <tr>
    <td align="center">
      <img src="https://life-os-banner.verridian.ai/logo.png" width="180" alt="Nanobanna Pro" />
    </td>
  </tr>
  <tr>
    <td style="color: #ffffff; font-family: Inter, sans-serif; padding: 20px;">
      <h1 style="color: #D4AF37; margin-bottom: 16px;">Welcome to Nanobanna Pro!</h1>
      <p style="font-size: 16px; line-height: 1.6;">
        Thank you for signing up. Please verify your email address to unlock all features including AI-powered banner generation.
      </p>
    </td>
  </tr>
  <tr>
    <td align="center" style="padding: 24px;">
      <div style="background: rgba(212, 175, 55, 0.1); border: 2px solid #D4AF37; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <span style="color: #D4AF37; font-size: 32px; font-weight: 700; letter-spacing: 8px;">{{verification_code}}</span>
      </div>
      <p style="color: #888; font-size: 14px;">Or click the button below:</p>
    </td>
  </tr>
  <tr>
    <td align="center" style="padding: 16px;">
      <a href="{{verification_link}}" style="background: linear-gradient(135deg, #D4AF37 0%, #C5A028 100%); color: #1a1a2e; padding: 16px 48px; border-radius: 12px; text-decoration: none; font-weight: 600; font-size: 16px; display: inline-block;">
        Verify Email
      </a>
    </td>
  </tr>
  <tr>
    <td style="color: #888; font-size: 14px; padding: 20px; text-align: center;">
      <p>This code expires in 24 hours.</p>
    </td>
  </tr>
</table>
```

#### Password Reset
```html
Subject: Reset your Nanobanna Pro password

<table style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 16px; padding: 40px;">
  <tr>
    <td align="center">
      <img src="https://life-os-banner.verridian.ai/logo.png" width="180" alt="Nanobanna Pro" />
    </td>
  </tr>
  <tr>
    <td style="color: #ffffff; font-family: Inter, sans-serif; padding: 20px;">
      <h1 style="color: #D4AF37; margin-bottom: 16px;">Reset Your Password</h1>
      <p style="font-size: 16px; line-height: 1.6;">
        We received a request to reset your password. Click the button below to create a new password. This link expires in 1 hour.
      </p>
    </td>
  </tr>
  <tr>
    <td align="center" style="padding: 24px;">
      <a href="{{reset_link}}" style="background: linear-gradient(135deg, #D4AF37 0%, #C5A028 100%); color: #1a1a2e; padding: 16px 48px; border-radius: 12px; text-decoration: none; font-weight: 600; font-size: 16px; display: inline-block;">
        Reset Password
      </a>
    </td>
  </tr>
  <tr>
    <td style="color: #888; font-size: 14px; padding: 20px; text-align: center;">
      <p>If you didn't request this, your account is safe. No action needed.</p>
    </td>
  </tr>
</table>
```

---

## DNS Records for Custom Email Domain

To send emails from your domain (e.g., `noreply@verridian.ai`), add these DNS records:

### SPF Record
```
Type: TXT
Name: @
Value: v=spf1 include:_spf.workos.com ~all
```

### DKIM Record
```
Type: CNAME
Name: workos._domainkey
Value: workos._domainkey.workos.com
```

### DMARC Record (Recommended)
```
Type: TXT
Name: _dmarc
Value: v=DMARC1; p=quarantine; rua=mailto:dmarc@verridian.ai
```

---

## Webhook Events

### Configure Webhook Endpoint
```bash
curl -X POST "https://api.workos.com/webhooks" \
  -H "Authorization: Bearer $WORKOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://life-os-banner.verridian.ai/api/webhooks/workos",
    "events": [
      "user.created",
      "user.updated",
      "user.deleted",
      "dsync.user.created",
      "dsync.user.updated",
      "dsync.user.deleted",
      "dsync.group.created",
      "dsync.group.updated",
      "dsync.group.deleted",
      "connection.activated",
      "connection.deactivated"
    ]
  }'
```

### Webhook Event Types

| Event | Description |
|-------|-------------|
| `user.created` | New user registered |
| `user.updated` | User profile updated |
| `user.deleted` | User account deleted |
| `dsync.user.created` | User added via SCIM |
| `dsync.user.updated` | SCIM user updated |
| `dsync.user.deleted` | SCIM user removed |
| `dsync.group.created` | SCIM group created |
| `connection.activated` | SSO connection enabled |
| `connection.deactivated` | SSO connection disabled |

---

## OAuth Provider Setup

### Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth 2.0 credentials
3. Add redirect URI: `https://api.workos.com/sso/oauth/callback`
4. Copy Client ID and Secret to WorkOS Dashboard

### GitHub OAuth
1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Create new OAuth App
3. Set Authorization callback URL: `https://api.workos.com/sso/oauth/callback`
4. Copy Client ID and Secret to WorkOS Dashboard

### Microsoft OAuth
1. Go to [Azure Portal](https://portal.azure.com/)
2. Register new application in Azure AD
3. Add redirect URI: `https://api.workos.com/sso/oauth/callback`
4. Create client secret and copy to WorkOS Dashboard

---

## Best Practices

1. **Always Verify Webhooks**: Check webhook signatures before processing
2. **Handle Idempotency**: Webhook events may be delivered multiple times
3. **Use State Parameter**: Include CSRF token in OAuth state
4. **Secure Redirect URIs**: Only allow registered redirect URIs
5. **Log Authentication Events**: Track all auth events for security auditing
6. **Implement Proper Logout**: Clear both local session and WorkOS session

---

## Example Workflow

### Setup New Organization SSO

1. User: "Set up Google OAuth for our org"
2. Agent: Lists current connections
3. Agent: Creates Google OAuth connection
4. Agent: Provides setup instructions for Google Console
5. Agent: Verifies connection is active

### Configure Email Branding

1. User: "Update email templates with our branding"
2. Agent: Updates branding colors and logo
3. Agent: Tests magic link email
4. Agent: Confirms template renders correctly

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| OAuth callback fails | Verify redirect URI matches exactly |
| Emails not delivered | Check SPF/DKIM DNS records |
| SSO loop | Clear cookies, check state parameter |
| SCIM sync fails | Verify bearer token, check directory connection |

### Debug Mode

Enable debug logging:
```typescript
import WorkOS from '@workos-inc/node';

const workos = new WorkOS(process.env.WORKOS_API_KEY, {
  logLevel: 'debug'
});
```

---

## Related Files in Codebase

- `server/src/lib/workos.ts` - SDK initialization
- `server/src/lib/authBridge.ts` - Lucia + WorkOS bridge
- `server/src/routes/auth.ts` - Auth endpoints
- `server/src/routes/webhooks.ts` - Webhook handlers
- `src/context/AuthContext.tsx` - Frontend auth state
- `src/components/auth/AuthModal.tsx` - Login UI
