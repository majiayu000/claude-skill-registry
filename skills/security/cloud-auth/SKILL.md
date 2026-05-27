---
name: cloud-auth
description: Flow Nexus authentication and user management. Use for login, registration, session management, password reset, and user account operations.
version: 1.0.0
category: cloud
type: skill
capabilities:
  - user_registration
  - user_login
  - session_management
  - password_management
  - profile_management
  - email_verification
tools:
  - mcp__flow-nexus__auth_status
  - mcp__flow-nexus__auth_init
  - mcp__flow-nexus__user_register
  - mcp__flow-nexus__user_login
  - mcp__flow-nexus__user_logout
  - mcp__flow-nexus__user_profile
  - mcp__flow-nexus__user_update_profile
  - mcp__flow-nexus__user_reset_password
  - mcp__flow-nexus__user_update_password
  - mcp__flow-nexus__user_verify_email
  - mcp__flow-nexus__user_upgrade
  - mcp__flow-nexus__user_stats
related_skills:
  - cloud-user-tools
  - cloud-payments
---

# Cloud Authentication

> Handle Flow Nexus user authentication, registration, session management, and account operations.

## Quick Start

```javascript
// Register a new user
await mcp__flow-nexus__user_register({
  email: "user@example.com",
  password: "secure_password",
  full_name: "User Name"
});

// Login
const session = await mcp__flow-nexus__user_login({
  email: "user@example.com",
  password: "secure_password"
});

// Check auth status
const status = await mcp__flow-nexus__auth_status({ detailed: true });

// Logout
await mcp__flow-nexus__user_logout();
```

## When to Use

- Registering new users on Flow Nexus platform
- Logging in existing users and managing sessions
- Resetting forgotten passwords
- Verifying email addresses
- Updating user profiles and account settings
- Upgrading user subscription tiers
- Troubleshooting authentication issues

## Prerequisites

- MCP server `flow-nexus` configured
- Valid email address for registration
- Secure password meeting requirements

## Core Concepts

### Authentication Flow

```
Register → Verify Email → Login → Session Active → Logout
                ↑                       ↓
          Reset Password ←────── Forgot Password
```

### User Tiers

| Tier | Credits | Features |
|------|---------|----------|
| **Free** | 100/month | Basic features, community support |
| **Pro** | 1000/month | Priority access, email support |
| **Enterprise** | Unlimited | Dedicated resources, SLA |

### Session Management

- Sessions are token-based
- Auto-expiration after inactivity
- Secure logout clears session data

## MCP Tools Reference

### Authentication Status

```javascript
// Check current auth status
mcp__flow-nexus__auth_status({
  detailed: true             // Include detailed auth info
})
// Returns: { authenticated, user_id, tier, session_expires }

// Initialize authentication mode
mcp__flow-nexus__auth_init({
  mode: "user"               // user or service
})
```

### User Registration

```javascript
mcp__flow-nexus__user_register({
  email: "user@example.com",
  password: "secure_password",  // Minimum 8 characters
  username: "username",         // Optional
  full_name: "Full Name"        // Optional
})
// Returns: { user_id, email, verification_sent }
```

### User Login/Logout

```javascript
// Login
mcp__flow-nexus__user_login({
  email: "user@example.com",
  password: "password"
})
// Returns: { user_id, token, expires_at, tier }

// Logout
mcp__flow-nexus__user_logout()
// Returns: { success: true }
```

### Profile Management

```javascript
// Get profile
mcp__flow-nexus__user_profile({
  user_id: "user_id"
})
// Returns: { id, email, full_name, tier, created_at }

// Update profile
mcp__flow-nexus__user_update_profile({
  user_id: "user_id",
  updates: {
    full_name: "New Name",
    bio: "Developer",
    github_username: "username"
  }
})

// Get user statistics
mcp__flow-nexus__user_stats({
  user_id: "user_id"
})
// Returns: { apps_published, credits_earned, challenges_completed }
```

### Password Management

```javascript
// Request password reset
mcp__flow-nexus__user_reset_password({
  email: "user@example.com"
})
// Returns: { email_sent: true }

// Update password with reset token
mcp__flow-nexus__user_update_password({
  token: "reset_token",
  new_password: "new_secure_password"
})
```

### Email Verification

```javascript
mcp__flow-nexus__user_verify_email({
  token: "verification_token"
})
// Returns: { verified: true }
```

### Tier Upgrade

```javascript
mcp__flow-nexus__user_upgrade({
  user_id: "user_id",
  tier: "pro"                // pro or enterprise
})
// Returns: { new_tier, effective_date }
```

## Usage Examples

### Example 1: Complete Registration Flow

```javascript
// Step 1: Register user
const registration = await mcp__flow-nexus__user_register({
  email: "newuser@example.com",
  password: "SecurePass123!",
  full_name: "New User"
});

console.log("Registration successful. Check email for verification link.");

// Step 2: User clicks verification link (token from email)
const verified = await mcp__flow-nexus__user_verify_email({
  token: "verification_token_from_email"
});

if (verified.verified) {
  console.log("Email verified! You can now login.");
}

// Step 3: Login
const session = await mcp__flow-nexus__user_login({
  email: "newuser@example.com",
  password: "SecurePass123!"
});

console.log(`Welcome! Your tier: ${session.tier}`);
console.log(`Session expires: ${session.expires_at}`);
```

### Example 2: Password Reset Flow

```javascript
// User forgot password
await mcp__flow-nexus__user_reset_password({
  email: "user@example.com"
});

console.log("Password reset email sent.");

// User receives email with reset token
// User clicks link and provides new password
await mcp__flow-nexus__user_update_password({
  token: "reset_token_from_email",
  new_password: "NewSecurePass456!"
});

console.log("Password updated. Please login with new password.");

// Login with new password
const session = await mcp__flow-nexus__user_login({
  email: "user@example.com",
  password: "NewSecurePass456!"
});
```

### Example 3: Profile Management

```javascript
// Check current auth status
const status = await mcp__flow-nexus__auth_status({
  detailed: true
});

if (!status.authenticated) {
  console.log("Please login first.");
  return;
}

// Get current profile
const profile = await mcp__flow-nexus__user_profile({
  user_id: status.user_id
});

console.log(`Current name: ${profile.full_name}`);
console.log(`Tier: ${profile.tier}`);

// Update profile
await mcp__flow-nexus__user_update_profile({
  user_id: status.user_id,
  updates: {
    full_name: "Updated Name",
    bio: "Full-stack developer specializing in AI",
    github_username: "myusername",
    website: "https://mywebsite.com"
  }
});

// Get user statistics
const stats = await mcp__flow-nexus__user_stats({
  user_id: status.user_id
});

console.log(`
User Statistics:
- Apps Published: ${stats.apps_published}
- Credits Earned: ${stats.credits_earned}
- Challenges Completed: ${stats.challenges_completed}
`);
```

### Example 4: Tier Upgrade

```javascript
// Check current status
const status = await mcp__flow-nexus__auth_status({ detailed: true });

console.log(`Current tier: ${status.tier}`);

if (status.tier === "free") {
  // Upgrade to Pro
  const upgrade = await mcp__flow-nexus__user_upgrade({
    user_id: status.user_id,
    tier: "pro"
  });

  console.log(`Upgraded to: ${upgrade.new_tier}`);
  console.log(`Effective: ${upgrade.effective_date}`);
  console.log("You now have access to 1000 credits/month and priority features!");
}
```

## Execution Checklist

### For Registration
- [ ] Provide valid email address
- [ ] Create secure password (8+ characters)
- [ ] Complete registration
- [ ] Check email for verification
- [ ] Click verification link
- [ ] Login with credentials

### For Password Reset
- [ ] Request password reset
- [ ] Check email for reset link
- [ ] Click reset link
- [ ] Enter new secure password
- [ ] Login with new password

## Best Practices

1. **Strong Passwords**: Use 8+ characters with mix of letters, numbers, symbols
2. **Email Verification**: Always verify email before accessing features
3. **Session Security**: Logout when done, especially on shared devices
4. **Profile Completeness**: Fill out profile for better experience
5. **Regular Password Changes**: Update password periodically
6. **Two-Factor Auth**: Enable 2FA when available

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `registration_failed` | Invalid email or weak password | Verify email format, strengthen password |
| `login_failed` | Wrong credentials or unverified email | Check credentials, verify email |
| `session_expired` | Token expired | Login again |
| `email_not_verified` | Account not verified | Check email for verification link |
| `password_reset_failed` | Invalid or expired token | Request new reset link |
| `unauthorized` | Not logged in | Login first |

## Metrics & Success Criteria

- **Login Success Rate**: >99% for valid credentials
- **Registration Completion**: >90% complete verification
- **Password Reset Success**: >95% successful resets
- **Session Duration**: Average session length tracking

## Integration Points

### With User Tools

```javascript
// After login, configure user settings
await mcp__flow-nexus__user_update_profile({
  user_id: session.user_id,
  updates: { preferences: { theme: "dark" } }
});
```

### With Payments

```javascript
// After login, check balance
const balance = await mcp__flow-nexus__check_balance();
console.log(`Available credits: ${balance.credits}`);
```

### Related Skills

- [cloud-user-tools](../cloud-user-tools/SKILL.md) - Profile and storage management
- [cloud-payments](../cloud-payments/SKILL.md) - Credit and billing

## Security Guidelines

1. **Never share passwords** - Use password reset if needed
2. **Check URLs** - Verify you're on official Flow Nexus site
3. **Report suspicious activity** - Contact support immediately
4. **Secure email** - Protect the email linked to your account
5. **Logout on public devices** - Clear sessions on shared computers

## References

- [Flow Nexus Security](https://flow-nexus.ruv.io/security)
- [Privacy Policy](https://flow-nexus.ruv.io/privacy)

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from flow-nexus-auth agent
