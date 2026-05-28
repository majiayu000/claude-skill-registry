---
name: Knack Auth
description: Handles API key and user token authentication for secure Knack API access. Manages session creation, refresh, and credential validation.
allowed-tools: Read
---

# Knack Auth

## Purpose
Handles API key and user token authentication for secure Knack API access. Manages session creation, refresh, and credential validation.

## Authentication Methods

### 1. API Key Authentication (Server-Side)
**Use**: Backend operations, automated reporting, data sync

**Headers**:
```javascript
{
  "X-Knack-Application-Id": process.env.KNACK_APP_ID,
  "X-Knack-REST-API-Key": process.env.KNACK_API_KEY
}
```

**Permissions**: Full read/write access to all objects

### 2. User Token Authentication (User-Specific)
**Use**: Dashboard views with user-level permissions

**Headers**:
```javascript
{
  "X-Knack-Application-Id": process.env.KNACK_APP_ID,
  "Authorization": user_token
}
```

## Core Functions

### login_user
**Endpoint**: `POST /v1/applications/{app_id}/session`

**Payload**:
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response**:
```json
{
  "session": {
    "user": {
      "id": "user_123",
      "token": "abc123xyz..."
    }
  }
}
```

**Example**:
```javascript
const session = await login_user({
  email: "admin@hubzonetech.org",
  password: process.env.ADMIN_PASSWORD
});

const user_token = session.session.user.token;
```

### refresh_token
**Purpose**: Renew expired user sessions automatically

**Logic**:
- User tokens expire after 24 hours
- Monitor token age
- Auto-refresh before expiration
- Store refreshed token securely

**Example**:
```javascript
if (isTokenExpired(current_token)) {
  const new_token = await refresh_token(current_token);
  updateStoredToken(new_token);
}
```

### validate_credentials
**Purpose**: Verify API key and app ID before operations

**Check**:
```javascript
const isValid = await validate_credentials({
  app_id: process.env.KNACK_APP_ID,
  api_key: process.env.KNACK_API_KEY
});
```

## Environment Variables

Required in `.env`:
```bash
KNACK_APP_ID=your_app_id
KNACK_API_KEY=your_api_key
ADMIN_EMAIL=admin@hubzonetech.org
ADMIN_PASSWORD=secure_password
```

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** for all secrets
3. **Rotate API keys** quarterly (align with QAR schedule)
4. **Limit user token lifespan** to 24 hours
5. **Log authentication failures** for audit trail

## HTI-Specific Roles

### Admin Users
- Full CRUD access
- Grant reporting permissions
- Donor management

### Volunteer Users
- Read-only access to training materials
- Event check-in capabilities

### Public Dashboard
- API key auth only
- No user-specific data

## Error Handling

```javascript
try {
  const token = await login_user(credentials);
} catch (error) {
  if (error.status === 401) {
    console.error("Invalid credentials");
  } else if (error.status === 429) {
    console.error("Rate limit exceeded - retry after delay");
  }
}
```

## Integration Points

- **knack_reader**: Provides auth headers
- **knack_realtime**: Maintains user sessions for webhooks
- **knack_reporting_sync**: Admin-level access for report generation
- **knack_devops**: Manages credential rotation in CI/CD

## Grant Compliance
- Audit logs required for NCDIT reporting
- Track all admin access to donation/device data
- Maintain separation between operational and financial data access
