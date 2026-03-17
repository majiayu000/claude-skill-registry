---
name: security-standards
description: Security standards for credential handling and authentication
---

# Security Rules

## 🚨 CRITICAL RULES (Immediate Failure)

### 1. Never Commit Secrets
- NEVER commit API keys, tokens, passwords
- NEVER commit .env files
- NEVER log sensitive data
- Check before EVERY commit

### 2. Credential Handling
- Credentials only from .env or .connectionProfile.json
- Never hardcode credentials
- Never expose credentials in error messages
- Always mask sensitive data in logs

### 3. No Environment Variables in Production Code
- Module code MUST NOT use process.env directly
- Only test code can access environment variables
- All config through connection profiles

## 🟡 STANDARD RULES

### Authentication Patterns
Priority order for auth methods:
1. Basic Authentication
2. API Token/Key
3. Personal Access Token
4. Bearer Token
5. OAuth2 (when supported)

### Credential Discovery
```javascript
// Priority order for finding credentials
1. .env file (for development/testing)
2. .connectionProfile.json (for module config)
3. Ask user to provide
```

### Connection Profile Format
```json
{
  "auth_type": "token",
  "token": "secret_value_here",
  "base_url": "https://api.example.com"
}
```

### Secure Storage
- Use .env for development credentials
- Add .env to .gitignore
- Use .connectionProfile.json for config
- Never store in code or comments

### API Key Validation
```bash
# Test credentials before implementation
curl -H "Authorization: Bearer $API_TOKEN" \
     https://api.example.com/user

# Store working token in .env
echo "API_TOKEN=verified_token" >> .env
```

## 🟢 GUIDELINES

### Error Messages
```typescript
// Bad - exposes token
throw new Error(`Auth failed with token: ${token}`);

// Good - generic message
throw new InvalidCredentialsError();
```

### Logging Practices
```typescript
// Bad - logs sensitive data
console.log('Connecting with:', credentials);

// Good - logs safe metadata
console.log('Connecting to:', baseUrl);
```

### Token Refresh
- Implement token refresh when applicable
- Store refresh tokens securely
- Handle expiration gracefully
- Don't expose refresh logic

### Rate Limiting
- Respect rate limit headers
- Implement exponential backoff
- Cache responses when appropriate
- Throw RateLimitExceededError

### HTTPS Requirements
- Always use HTTPS for API calls
- Verify SSL certificates
- No downgrade to HTTP
- Reject self-signed certs in production

## 📝 EXCEPTIONS LOG

### Development Exceptions
- Can use HTTP for local testing only
- Can log more details in debug mode
- Must remove before commit

### Special Security Requirements
Document when operations need:
- Elevated permissions
- Admin access
- Specific OAuth scopes
- IP whitelisting
