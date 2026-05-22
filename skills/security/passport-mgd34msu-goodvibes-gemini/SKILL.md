---
name: passport
description: Implements Passport.js authentication middleware with local, OAuth, and JWT strategies for Express/Node.js. Use when building Node.js APIs, implementing custom auth flows, or needing flexible authentication strategies.
---

# Passport.js

Passport.js is authentication middleware for Node.js. It supports 500+ authentication strategies including local username/password, OAuth, JWT, and more.

## Quick Start

```bash
npm install passport express-session
npm install passport-local  # For username/password
```

## Basic Setup

```typescript
// app.ts
import express from 'express'
import session from 'express-session'
import passport from 'passport'

const app = express()

app.use(express.json())
app.use(express.urlencoded({ extended: false }))

app.use(session({
  secret: process.env.SESSION_SECRET!,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    maxAge: 24 * 60 * 60 * 1000 // 24 hours
  }
}))

app.use(passport.initialize())
app.use(passport.session())
```

## Local Strategy (Username/Password)

### Configure Strategy

```typescript
// config/passport.ts
import passport from 'passport'
import { Strategy as LocalStrategy } from 'passport-local'
import bcrypt from 'bcrypt'
import { getUserByEmail, getUserById } from './db'

passport.use(new LocalStrategy(
  {
    usernameField: 'email',
    passwordField: 'password'
  },
  async (email, password, done) => {
    try {
      const user = await getUserByEmail(email)

      if (!user) {
        return done(null, false, { message: 'Invalid email or password' })
      }

      const isValid = await bcrypt.compare(password, user.passwordHash)

      if (!isValid) {
        return done(null, false, { message: 'Invalid email or password' })
      }

      return done(null, user)
    } catch (error) {
      return done(error)
    }
  }
))

// Serialize user to session
passport.serializeUser((user: any, done) => {
  done(null, user.id)
})

// Deserialize user from session
passport.deserializeUser(async (id: string, done) => {
  try {
    const user = await getUserById(id)
    done(null, user)
  } catch (error) {
    done(error)
  }
})
```

### Login Route

```typescript
// routes/auth.ts
import express from 'express'
import passport from 'passport'

const router = express.Router()

router.post('/login', (req, res, next) => {
  passport.authenticate('local', (err, user, info) => {
    if (err) {
      return next(err)
    }

    if (!user) {
      return res.status(401).json({ error: info?.message || 'Login failed' })
    }

    req.logIn(user, (err) => {
      if (err) {
        return next(err)
      }
      return res.json({ user: { id: user.id, email: user.email } })
    })
  })(req, res, next)
})

router.post('/logout', (req, res, next) => {
  req.logout((err) => {
    if (err) {
      return next(err)
    }
    res.json({ message: 'Logged out' })
  })
})

router.get('/me', (req, res) => {
  if (!req.user) {
    return res.status(401).json({ error: 'Not authenticated' })
  }
  res.json({ user: req.user })
})

export default router
```

## Protect Routes

### Middleware

```typescript
// middleware/auth.ts
import { Request, Response, NextFunction } from 'express'

export function isAuthenticated(req: Request, res: Response, next: NextFunction) {
  if (req.isAuthenticated()) {
    return next()
  }
  res.status(401).json({ error: 'Authentication required' })
}

export function hasRole(role: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.isAuthenticated()) {
      return res.status(401).json({ error: 'Authentication required' })
    }
    if ((req.user as any).role !== role) {
      return res.status(403).json({ error: 'Insufficient permissions' })
    }
    next()
  }
}
```

### Usage

```typescript
import { isAuthenticated, hasRole } from './middleware/auth'

// Protected route
app.get('/dashboard', isAuthenticated, (req, res) => {
  res.json({ data: 'Protected data' })
})

// Admin only
app.get('/admin', hasRole('admin'), (req, res) => {
  res.json({ data: 'Admin data' })
})
```

## JWT Strategy

For stateless API authentication.

```bash
npm install passport-jwt jsonwebtoken
npm install -D @types/jsonwebtoken @types/passport-jwt
```

### Configure JWT Strategy

```typescript
// config/passport-jwt.ts
import passport from 'passport'
import { Strategy as JwtStrategy, ExtractJwt } from 'passport-jwt'
import { getUserById } from './db'

const options = {
  jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
  secretOrKey: process.env.JWT_SECRET!,
  algorithms: ['HS256'] as const
}

passport.use(new JwtStrategy(options, async (payload, done) => {
  try {
    const user = await getUserById(payload.sub)

    if (!user) {
      return done(null, false)
    }

    return done(null, user)
  } catch (error) {
    return done(error, false)
  }
}))
```

### Issue JWT

```typescript
import jwt from 'jsonwebtoken'

function generateToken(user: { id: string; email: string }) {
  return jwt.sign(
    { sub: user.id, email: user.email },
    process.env.JWT_SECRET!,
    { expiresIn: '7d' }
  )
}

router.post('/login', async (req, res, next) => {
  passport.authenticate('local', { session: false }, (err, user, info) => {
    if (err) return next(err)
    if (!user) return res.status(401).json({ error: info?.message })

    const token = generateToken(user)
    res.json({ token, user: { id: user.id, email: user.email } })
  })(req, res, next)
})
```

### Protect Routes with JWT

```typescript
router.get('/protected',
  passport.authenticate('jwt', { session: false }),
  (req, res) => {
    res.json({ user: req.user })
  }
)
```

## OAuth Strategies

### Google OAuth

```bash
npm install passport-google-oauth20
```

```typescript
import { Strategy as GoogleStrategy } from 'passport-google-oauth20'

passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID!,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    callbackURL: '/auth/google/callback',
    scope: ['email', 'profile']
  },
  async (accessToken, refreshToken, profile, done) => {
    try {
      // Find or create user
      let user = await getUserByGoogleId(profile.id)

      if (!user) {
        user = await createUser({
          googleId: profile.id,
          email: profile.emails?.[0].value,
          name: profile.displayName,
          avatar: profile.photos?.[0].value
        })
      }

      return done(null, user)
    } catch (error) {
      return done(error as Error)
    }
  }
))
```

### OAuth Routes

```typescript
// Start OAuth flow
router.get('/auth/google',
  passport.authenticate('google', { scope: ['email', 'profile'] })
)

// Handle callback
router.get('/auth/google/callback',
  passport.authenticate('google', {
    failureRedirect: '/login',
    successRedirect: '/dashboard'
  })
)
```

### GitHub OAuth

```bash
npm install passport-github2
```

```typescript
import { Strategy as GitHubStrategy } from 'passport-github2'

passport.use(new GitHubStrategy({
    clientID: process.env.GITHUB_CLIENT_ID!,
    clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    callbackURL: '/auth/github/callback'
  },
  async (accessToken, refreshToken, profile, done) => {
    try {
      let user = await getUserByGithubId(profile.id)

      if (!user) {
        user = await createUser({
          githubId: profile.id,
          email: profile.emails?.[0].value,
          name: profile.displayName || profile.username,
          avatar: profile.photos?.[0].value
        })
      }

      done(null, user)
    } catch (error) {
      done(error as Error)
    }
  }
))

router.get('/auth/github',
  passport.authenticate('github', { scope: ['user:email'] })
)

router.get('/auth/github/callback',
  passport.authenticate('github', { failureRedirect: '/login' }),
  (req, res) => {
    res.redirect('/dashboard')
  }
)
```

## Multiple Strategies

### Combined Local + OAuth

```typescript
// User model supports multiple auth methods
interface User {
  id: string
  email: string
  passwordHash?: string
  googleId?: string
  githubId?: string
}

// Find user by any method
async function findOrCreateUser(profile: OAuthProfile) {
  // Check for existing user by email first
  let user = await getUserByEmail(profile.email)

  if (user) {
    // Link OAuth account to existing user
    await linkOAuthAccount(user.id, profile.provider, profile.id)
    return user
  }

  // Create new user
  return createUser({
    email: profile.email,
    [profile.provider + 'Id']: profile.id,
    name: profile.name
  })
}
```

## Session Store

### Redis Session Store

```bash
npm install connect-redis redis
```

```typescript
import RedisStore from 'connect-redis'
import { createClient } from 'redis'

const redisClient = createClient({ url: process.env.REDIS_URL })
await redisClient.connect()

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET!,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    maxAge: 24 * 60 * 60 * 1000
  }
}))
```

### Database Session Store

```bash
npm install connect-pg-simple
```

```typescript
import pgSession from 'connect-pg-simple'
import { pool } from './db'

const PostgresStore = pgSession(session)

app.use(session({
  store: new PostgresStore({
    pool,
    tableName: 'sessions'
  }),
  secret: process.env.SESSION_SECRET!,
  resave: false,
  saveUninitialized: false
}))
```

## TypeScript Types

```typescript
// types/express.d.ts
declare global {
  namespace Express {
    interface User {
      id: string
      email: string
      name?: string
      role?: string
    }
  }
}

export {}
```

## Error Handling

```typescript
// Custom authentication error handler
router.post('/login', (req, res, next) => {
  passport.authenticate('local', (err, user, info) => {
    if (err) {
      console.error('Auth error:', err)
      return res.status(500).json({ error: 'Authentication failed' })
    }

    if (!user) {
      return res.status(401).json({
        error: info?.message || 'Invalid credentials',
        code: 'INVALID_CREDENTIALS'
      })
    }

    req.logIn(user, (err) => {
      if (err) {
        console.error('Session error:', err)
        return res.status(500).json({ error: 'Session creation failed' })
      }

      res.json({
        user: {
          id: user.id,
          email: user.email,
          name: user.name
        }
      })
    })
  })(req, res, next)
})
```

## Testing

```typescript
import request from 'supertest'
import app from './app'

describe('Authentication', () => {
  it('should login with valid credentials', async () => {
    const res = await request(app)
      .post('/auth/login')
      .send({ email: 'test@example.com', password: 'password' })
      .expect(200)

    expect(res.body.user.email).toBe('test@example.com')
  })

  it('should reject invalid credentials', async () => {
    await request(app)
      .post('/auth/login')
      .send({ email: 'test@example.com', password: 'wrong' })
      .expect(401)
  })

  it('should protect routes', async () => {
    await request(app)
      .get('/dashboard')
      .expect(401)
  })
})
```

## Best Practices

1. **Use bcrypt for passwords** - Never store plain text
2. **Secure session cookies** - Set secure, httpOnly, sameSite
3. **Use Redis for sessions** - In production with multiple servers
4. **Handle errors gracefully** - Don't expose sensitive info
5. **Validate input** - Before authentication
6. **Rate limit login attempts** - Prevent brute force

## References

- [OAuth Integration](references/oauth.md)
- [Session Management](references/sessions.md)
