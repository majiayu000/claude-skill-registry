---
name: passport-js
description: >-
  Add authentication to Express with Passport.js. Use when implementing
  login with Google/GitHub/email, OAuth, session auth, or social login.
license: Apache-2.0
compatibility: 'Express, Node.js'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: development
  tags: [passport, authentication, oauth, express, social-login]
---

# Passport.js

## Overview

Passport.js is the most popular auth middleware for Express with 500+ strategies (Google, GitHub, Facebook, SAML, LDAP, local). Session-based by default, works with JWTs too.

## Instructions

### Step 1: Local Strategy

```typescript
import passport from 'passport'
import { Strategy as LocalStrategy } from 'passport-local'
import bcrypt from 'bcrypt'

passport.use(new LocalStrategy(
  { usernameField: 'email' },
  async (email, password, done) => {
    const user = await db.users.findByEmail(email)
    if (!user) return done(null, false, { message: 'No account' })
    if (!await bcrypt.compare(password, user.passwordHash)) return done(null, false)
    return done(null, user)
  }
))

passport.serializeUser((user: any, done) => done(null, user.id))
passport.deserializeUser(async (id, done) => done(null, await db.users.findById(id)))
```

### Step 2: Google OAuth

```typescript
import { Strategy as GoogleStrategy } from 'passport-google-oauth20'

passport.use(new GoogleStrategy({
  clientID: process.env.GOOGLE_CLIENT_ID!,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
  callbackURL: '/auth/google/callback',
}, async (accessToken, refreshToken, profile, done) => {
  let user = await db.users.findByOAuthId('google', profile.id)
  if (!user) user = await db.users.create({
    email: profile.emails![0].value,
    name: profile.displayName,
    oauthProvider: 'google', oauthId: profile.id,
  })
  return done(null, user)
}))
```

### Step 3: Routes

```typescript
app.post('/login', passport.authenticate('local', {
  successRedirect: '/dashboard', failureRedirect: '/login',
}))
app.get('/auth/google', passport.authenticate('google', { scope: ['profile', 'email'] }))
app.get('/auth/google/callback', passport.authenticate('google', {
  successRedirect: '/dashboard', failureRedirect: '/login',
}))
```

## Guidelines

- Hash passwords with bcrypt (cost 12+). Never store plaintext.
- Use express-session with Redis store in production.
- Implement CSRF protection with session-based auth.
- Link accounts: let users connect multiple OAuth providers to one account.
