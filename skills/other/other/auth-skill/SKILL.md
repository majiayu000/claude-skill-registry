---
name: auth-skill
description: Handle secure user authentication including signup, signin, password hashing, JWT tokens, and Better Auth integration. Use for authentication and authorization systems.
---

# Auth Skill – Secure Authentication & Authorization

## Instructions

1. **Signup & Signin**
   - Implement secure signup and login flows
   - Prevent account enumeration
   - Handle failed authentication attempts safely

2. **Password Hashing**
   - Hash passwords using bcrypt or argon2
   - Always apply salting
   - Never store or log plaintext passwords

3. **JWT Token Management**
   - Generate access and refresh tokens securely
   - Validate token signature, claims, and expiration
   - Rotate and revoke tokens when required

4. **Better Auth Integration**
   - Configure Better Auth securely
   - Integrate with existing user models
   - Follow Better Auth recommended defaults

5. **Validation & Error Handling**
   - Validate all authentication inputs
   - Use safe, generic error messages
   - Protect against common auth attacks

## Best Practices
- Apply least-privilege access control
- Use HTTP-only, secure cookies when applicable
- Enforce strong password policies
- Set proper token expiration strategies
- Follow OWASP authentication guidelines

## Example Structure
```ts
// Password hashing
const hashedPassword = await bcrypt.hash(password, 12);

// JWT generation
const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET,
  { expiresIn: "15m" }
);
