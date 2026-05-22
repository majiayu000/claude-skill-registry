---
name: auth-comprehensive
description: Production-grade authentication & authorization covering JWT, cookies, sessions, hashing, MFA, OAuth2, RBAC, and permissions across all frameworks (Next.js, Express.js, FastAPI, Django, Spring, etc.). Includes intelligent pattern selection, Better Auth integration, email verification, social login, token revocation, permission management, and 10+ years security expertise. Use when implementing authentication, authorization, user management, MFA, OAuth integration, or securing APIs in any framework.
---

# Comprehensive Authentication & Authorization

Enterprise-grade authentication system supporting multiple frameworks with intelligent pattern selection, advanced security hardening, and production-ready implementations across all authentication methods (JWT, sessions, cookies, hybrid approaches).

## Quick Decision Tree

**Choose authentication method based on requirements:**

```
Need stateless, API-first, microservices?
├─ YES → JWT Tokens (access + refresh)
└─ NO → Continue

Need session-based, traditional web app?
├─ YES → Sessions (server-side)
└─ NO → Continue

Need browser cookies, XSS protection?
├─ YES → HTTP-Only Cookies
└─ NO → Continue

Need best of both worlds?
└─ Hybrid (JWT + Cookies)

Need enhanced security & ease?
└─ Better Auth / Auth Libraries
```

## Core Authentication Patterns

### Pattern 1: JWT (JSON Web Tokens) - Stateless

**Best For:** APIs, microservices, mobile apps, single-page applications

```python
# Python/FastAPI
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

class JWTManager:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain: str, hashed: str) -> bool:
        return self.pwd_context.verify(plain, hashed)
    
    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": datetime.utcnow() + timedelta(days=7)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
```

```javascript
// JavaScript/Node.js/Express
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

class JWTManager {
    constructor(secretKey, algorithm = 'HS256') {
        this.secretKey = secretKey;
        this.algorithm = algorithm;
    }
    
    hashPassword(password) {
        return bcrypt.hashSync(password, 10);
    }
    
    verifyPassword(plain, hashed) {
        return bcrypt.compareSync(plain, hashed);
    }
    
    createAccessToken(data, expiresIn = '15m') {
        return jwt.sign(
            { ...data, type: 'access' },
            this.secretKey,
            { algorithm: this.algorithm, expiresIn }
        );
    }
    
    createRefreshToken(userId) {
        return jwt.sign(
            { sub: userId, type: 'refresh' },
            this.secretKey,
            { expiresIn: '7d' }
        );
    }
    
    decodeToken(token) {
        try {
            return jwt.verify(token, this.secretKey);
        } catch (error) {
            return null;
        }
    }
}

module.exports = JWTManager;
```

```typescript
// TypeScript/Next.js
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

interface TokenPayload {
    sub: string;
    type: 'access' | 'refresh';
    iat: number;
    exp: number;
}

class JWTManager {
    private secretKey: string;
    private algorithm: string = 'HS256';
    
    constructor(secretKey: string) {
        this.secretKey = secretKey;
    }
    
    hashPassword(password: string): string {
        return bcrypt.hashSync(password, 10);
    }
    
    verifyPassword(plain: string, hashed: string): boolean {
        return bcrypt.compareSync(plain, hashed);
    }
    
    createAccessToken(data: any, expiresIn: string = '15m'): string {
        return jwt.sign(
            { ...data, type: 'access' },
            this.secretKey,
            { algorithm: this.algorithm, expiresIn }
        );
    }
    
    createRefreshToken(userId: number): string {
        return jwt.sign(
            { sub: userId, type: 'refresh' },
            this.secretKey,
            { expiresIn: '7d' }
        );
    }
    
    decodeToken(token: string): TokenPayload | null {
        try {
            return jwt.verify(token, this.secretKey) as TokenPayload;
        } catch (error) {
            return null;
        }
    }
}

export default JWTManager;
```

### Pattern 2: Session-Based Authentication

**Best For:** Traditional web apps, server-rendered applications, CSRF protection needed

```python
# Python/Flask or FastAPI with sessions
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets

class SessionManager:
    def __init__(self, db: Session, session_timeout_minutes: int = 30):
        self.db = db
        self.timeout = timedelta(minutes=session_timeout_minutes)
    
    def create_session(self, user_id: int) -> str:
        """Create new session and return session ID"""
        session_token = secrets.token_urlsafe(32)
        
        session_record = {
            'user_id': user_id,
            'token': session_token,
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + self.timeout,
            'last_activity': datetime.utcnow()
        }
        
        # Save to database
        self.db.create(UserSession, session_record)
        self.db.commit()
        
        return session_token
    
    def get_session(self, token: str) -> dict | None:
        """Retrieve and validate session"""
        session = self.db.query(UserSession).filter(
            UserSession.token == token,
            UserSession.expires_at > datetime.utcnow()
        ).first()
        
        if session:
            # Update last activity
            session.last_activity = datetime.utcnow()
            self.db.commit()
            return {'user_id': session.user_id}
        
        return None
    
    def invalidate_session(self, token: str) -> bool:
        """Logout - invalidate session"""
        session = self.db.query(UserSession).filter(
            UserSession.token == token
        ).first()
        
        if session:
            self.db.delete(session)
            self.db.commit()
            return True
        return False
```

```javascript
// JavaScript/Express with express-session
const session = require('express-session');
const RedisStore = require('connect-redis').default;
const { createClient } = require('redis');

const redisClient = createClient();
redisClient.connect();

const sessionMiddleware = session({
    store: new RedisStore({ client: redisClient }),
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: true,  // HTTPS only
        httpOnly: true, // No JS access
        sameSite: 'strict',
        maxAge: 30 * 60 * 1000 // 30 minutes
    }
});

app.use(sessionMiddleware);

app.post('/login', (req, res) => {
    if (authenticateUser(req.body)) {
        req.session.userId = user.id;
        req.session.role = user.role;
        res.json({ message: 'Logged in' });
    }
});

app.post('/logout', (req, res) => {
    req.session.destroy((err) => {
        if (err) return res.status(500).json({ error: 'Logout failed' });
        res.json({ message: 'Logged out' });
    });
});
```

### Pattern 3: HTTP-Only Cookies (Browser Security)

**Best For:** Web applications, maximum XSS protection

```javascript
// Express/Node.js - Setting HTTP-Only Cookies
app.post('/login', async (req, res) => {
    const user = await authenticateUser(req.body.email, req.body.password);
    
    if (!user) {
        return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    const accessToken = jwt.sign(
        { userId: user.id, role: user.role },
        process.env.JWT_SECRET,
        { expiresIn: '15m' }
    );
    
    const refreshToken = jwt.sign(
        { userId: user.id },
        process.env.REFRESH_SECRET,
        { expiresIn: '7d' }
    );
    
    // Set HTTP-Only cookie - cannot be accessed by JavaScript
    res.cookie('accessToken', accessToken, {
        httpOnly: true,      // No JS access (prevents XSS)
        secure: true,        // HTTPS only
        sameSite: 'strict',  // CSRF protection
        maxAge: 15 * 60 * 1000, // 15 minutes
        path: '/',
        domain: process.env.COOKIE_DOMAIN
    });
    
    res.cookie('refreshToken', refreshToken, {
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
        maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
        path: '/api/auth/refresh'
    });
    
    res.json({ message: 'Login successful' });
});

// Middleware to extract token from cookies
function authenticateRequest(req, res, next) {
    const token = req.cookies.accessToken;
    
    if (!token) {
        return res.status(401).json({ error: 'No token' });
    }
    
    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.userId = decoded.userId;
        req.role = decoded.role;
        next();
    } catch (error) {
        return res.status(401).json({ error: 'Invalid token' });
    }
}

app.get('/api/protected', authenticateRequest, (req, res) => {
    res.json({ data: 'Protected content', userId: req.userId });
});
```

```typescript
// Next.js - Handling cookies securely
import { cookies } from 'next/headers';
import jwt from 'jsonwebtoken';

export async function login(email: string, password: string) {
    const user = await authenticateUser(email, password);
    if (!user) throw new Error('Invalid credentials');
    
    const accessToken = jwt.sign(
        { userId: user.id, role: user.role },
        process.env.JWT_SECRET,
        { expiresIn: '15m' }
    );
    
    const refreshToken = jwt.sign(
        { userId: user.id },
        process.env.REFRESH_SECRET,
        { expiresIn: '7d' }
    );
    
    const cookieStore = await cookies();
    
    // Set HTTP-Only cookie
    cookieStore.set('accessToken', accessToken, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
        maxAge: 15 * 60, // seconds
        path: '/'
    });
    
    cookieStore.set('refreshToken', refreshToken, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
        maxAge: 7 * 24 * 60 * 60,
        path: '/api/auth/refresh'
    });
}

export async function getUser() {
    const cookieStore = await cookies();
    const token = cookieStore.get('accessToken')?.value;
    
    if (!token) return null;
    
    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        return decoded;
    } catch {
        return null;
    }
}
```

### Pattern 4: Hybrid Approach (JWT + Cookies)

**Best For:** Maximum security + flexibility, modern web apps

```python
# FastAPI - Hybrid JWT + HTTP-Only Cookies
from fastapi import FastAPI, Cookie, Depends, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/login")
async def login(email: str, password: str):
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create tokens
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token(user.id)
    
    # Store refresh token in database for revocation
    store_refresh_token(user.id, refresh_token)
    
    response = JSONResponse(content={"access_token": access_token})
    
    # Set refresh token in HTTP-Only cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7 * 24 * 60 * 60
    )
    
    return response

async def get_current_user(
    access_token: str = Cookie(None),
    refresh_token: str = Cookie(None)
):
    """Validate access token, refresh if needed"""
    
    if access_token:
        try:
            payload = jwt.decode(access_token, SECRET_KEY)
            return payload["sub"]
        except JWTError:
            pass
    
    # Try refresh token
    if refresh_token:
        user_id = verify_refresh_token(refresh_token)
        if user_id:
            new_access = create_access_token({"sub": str(user_id)})
            # Return new access token
            return user_id
    
    raise HTTPException(status_code=401, detail="Not authenticated")

@app.get("/protected")
async def protected_route(user_id: str = Depends(get_current_user)):
    return {"user_id": user_id}
```

## Multi-Factor Authentication (MFA)

### TOTP (Time-based One-Time Password)

```python
# FastAPI with TOTP (Google Authenticator)
from pyotp import TOTP
from qrcode import QRCode

class MFAManager:
    @staticmethod
    def generate_secret() -> str:
        """Generate TOTP secret"""
        return TOTP.new().secret
    
    @staticmethod
    def get_provisioning_uri(secret: str, user_email: str, issuer: str) -> str:
        """Get QR code URI for authenticator app"""
        totp = TOTP(secret)
        return totp.provisioning_uri(name=user_email, issuer_name=issuer)
    
    @staticmethod
    def verify_token(secret: str, token: str) -> bool:
        """Verify TOTP token"""
        totp = TOTP(secret)
        return totp.verify(token)

@app.post("/auth/mfa/setup")
async def setup_mfa(current_user: User = Depends(get_current_user)):
    """Generate MFA secret and QR code"""
    secret = MFAManager.generate_secret()
    uri = MFAManager.get_provisioning_uri(secret, current_user.email, "MyApp")
    
    # Return QR code and secret
    return {
        "secret": secret,
        "qr_code_uri": uri
    }

@app.post("/auth/mfa/enable")
async def enable_mfa(
    mfa_token: str,
    mfa_secret: str,
    current_user: User = Depends(get_current_user)
):
    """Enable MFA after verification"""
    if not MFAManager.verify_token(mfa_secret, mfa_token):
        raise HTTPException(status_code=400, detail="Invalid MFA token")
    
    # Save secret to database
    update_user_mfa(current_user.id, mfa_secret)
    return {"message": "MFA enabled"}

@app.post("/auth/login-mfa")
async def login_with_mfa(email: str, password: str, mfa_token: str):
    """Login with MFA verification"""
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=401)
    
    if not MFAManager.verify_token(user.mfa_secret, mfa_token):
        raise HTTPException(status_code=401, detail="Invalid MFA token")
    
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token}
```

### Email Verification

```python
# FastAPI with Email Verification
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import secrets

class EmailVerificationManager:
    @staticmethod
    def create_verification_token(user_id: int) -> str:
        token = secrets.token_urlsafe(32)
        store_verification_token(user_id, token)
        return token
    
    @staticmethod
    def send_verification_email(email: str, token: str):
        verification_link = f"https://yourapp.com/auth/verify?token={token}"
        
        message = Mail(
            from_email="noreply@yourapp.com",
            to_emails=email,
            subject="Verify your email",
            html_content=f'<a href="{verification_link}">Click to verify</a>'
        )
        
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.send(message)
    
    @staticmethod
    def verify_email(token: str) -> int | None:
        user_id = get_user_id_from_token(token)
        if user_id and is_token_valid(token):
            mark_email_verified(user_id)
            delete_verification_token(token)
            return user_id
        return None

@app.post("/auth/register")
async def register(email: str, password: str):
    user = create_user(email, hash_password(password))
    token = EmailVerificationManager.create_verification_token(user.id)
    EmailVerificationManager.send_verification_email(email, token)
    return {"message": "Verification email sent"}

@app.get("/auth/verify")
async def verify_email(token: str):
    user_id = EmailVerificationManager.verify_email(token)
    if user_id:
        return {"message": "Email verified"}
    raise HTTPException(status_code=400, detail="Invalid token")
```

## OAuth2 & Social Login

### Google OAuth2

```python
# FastAPI with Google OAuth2
from google.auth.transport import requests
from google.oauth2 import id_token

class GoogleOAuth:
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    
    @staticmethod
    def verify_token(token: str) -> dict | None:
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                GoogleOAuth.GOOGLE_CLIENT_ID
            )
            return idinfo
        except ValueError:
            return None

@app.post("/auth/google")
async def google_login(token: str):
    idinfo = GoogleOAuth.verify_token(token)
    if not idinfo:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    # Create or get user
    user = get_or_create_user(
        email=idinfo["email"],
        name=idinfo["name"],
        picture=idinfo["picture"]
    )
    
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "user": user}
```

```typescript
// Next.js with Google OAuth2
import GoogleProvider from "next-auth/providers/google";
import { NextAuthOptions } from "next-auth";

export const authOptions: NextAuthOptions = {
    providers: [
        GoogleProvider({
            clientId: process.env.GOOGLE_CLIENT_ID!,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET!
        })
    ],
    callbacks: {
        async jwt({ token, account }) {
            if (account) {
                token.accessToken = account.access_token;
            }
            return token;
        },
        async session({ session, token }) {
            session.user.id = token.sub;
            return session;
        }
    }
};
```

## Role-Based Access Control (RBAC)

```python
# FastAPI RBAC
from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    MANAGE_USERS = "manage_users"

ROLE_PERMISSIONS = {
    Role.ADMIN: [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.MANAGE_USERS],
    Role.MODERATOR: [Permission.READ, Permission.WRITE, Permission.DELETE],
    Role.USER: [Permission.READ]
}

def has_permission(required_permission: Permission):
    async def permission_checker(current_user: User = Depends(get_current_user)):
        user_permissions = ROLE_PERMISSIONS.get(current_user.role, [])
        if required_permission not in user_permissions:
            raise HTTPException(status_code=403, detail="Permission denied")
        return current_user
    return permission_checker

@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(has_permission(Permission.MANAGE_USERS))
):
    delete_user_from_db(user_id)
    return {"message": "User deleted"}
```

## Password Hashing & Security

### Bcrypt

```python
# Python/FastAPI
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Cost factor - higher = more secure but slower
)

def hash_password(password: str) -> str:
    # Ensure password is at least 8 chars, has uppercase, digit, special char
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not any(c.isupper() for c in password):
        raise ValueError("Password must contain uppercase letter")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain digit")
    if not any(c in "!@#$%^&*.-_" for c in password):
        raise ValueError("Password must contain special character")
    
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

```javascript
// JavaScript/Node.js
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 12;

async function hashPassword(password) {
    // Validate password strength
    const strongRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    
    if (!strongRegex.test(password)) {
        throw new Error('Password must be 8+ chars with uppercase, digit, and special char');
    }
    
    return bcrypt.hash(password, SALT_ROUNDS);
}

async function verifyPassword(plainPassword, hashedPassword) {
    return bcrypt.compare(plainPassword, hashedPassword);
}
```

## Better Auth Integration

Better Auth is a modern authentication library that simplifies many patterns:

```typescript
// Next.js with Better Auth
import { betterAuth } from "better-auth";
import { nextCookies } from "better-auth/next-js";

export const auth = betterAuth({
    database: prisma,
    secret: process.env.BETTER_AUTH_SECRET,
    plugins: [
        nextCookies()
    ],
    user: {
        additionalFields: {
            role: {
                type: "string",
                required: false,
                defaultValue: "user"
            }
        }
    },
    emailVerification: {
        sendVerificationEmail: async ({ email, url }) => {
            await sendEmail({
                to: email,
                subject: "Verify your email",
                html: `<a href="${url}">Verify email</a>`
            });
        }
    },
    socialProviders: {
        google: {
            clientId: process.env.GOOGLE_CLIENT_ID,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET
        },
        github: {
            clientId: process.env.GITHUB_CLIENT_ID,
            clientSecret: process.env.GITHUB_CLIENT_SECRET
        }
    }
});

// Usage in Next.js
export { auth as default } from '@/auth';

// Client-side
import { signIn, signOut, useSession } from "better-auth/client";

export function LoginButton() {
    return (
        <button onClick={() => signIn.social({ provider: "google" })}>
            Login with Google
        </button>
    );
}
```

## Token Revocation & Logout

```python
# FastAPI - Token Revocation (Blacklist)
from redis import Redis

redis_client = Redis(host='localhost', port=6379, db=0)

class TokenRevocationManager:
    @staticmethod
    def revoke_token(token: str, ttl_seconds: int):
        """Add token to blacklist"""
        redis_client.setex(f"revoked_token:{token}", ttl_seconds, "1")
    
    @staticmethod
    def is_revoked(token: str) -> bool:
        """Check if token is revoked"""
        return redis_client.exists(f"revoked_token:{token}") > 0

async def get_current_user(token: str = Depends(oauth2_scheme)):
    if TokenRevocationManager.is_revoked(token):
        raise HTTPException(status_code=401, detail="Token revoked")
    
    payload = jwt.decode(token, SECRET_KEY)
    return payload["sub"]

@app.post("/auth/logout")
async def logout(current_user: User = Depends(get_current_user), token: str = Header()):
    # Revoke token
    payload = jwt.decode(token, SECRET_KEY)
    remaining_time = payload["exp"] - datetime.utcnow().timestamp()
    TokenRevocationManager.revoke_token(token, int(remaining_time))
    
    return {"message": "Logged out"}
```

## Security Hardening Checklist

✅ **Password Security**
- Minimum 8 characters
- Uppercase + lowercase
- Numbers and special characters
- Bcrypt with cost factor 12+
- Rate limiting on login attempts

✅ **Token Security**
- Short expiration times (15-30 minutes)
- Refresh token rotation
- Token revocation support
- Secure storage (HTTP-Only cookies)

✅ **Database Security**
- Hash passwords (never plain text)
- Salt with bcrypt
- Parameterized queries
- Encrypted sensitive fields

✅ **API Security**
- HTTPS/TLS enforcement
- CORS properly configured
- Rate limiting
- Request size limits

✅ **Frontend Security**
- HTTP-Only cookies (no JS access)
- CSRF protection
- Secure headers (CSP, X-Frame-Options)
- Input validation

✅ **Infrastructure**
- Environment variables for secrets
- Secure key rotation
- Audit logging
- Monitoring and alerts

## Resource Files Included

- **FRAMEWORKS.md** - Framework-specific implementations
- **PATTERNS.md** - All authentication patterns
- **OAUTH.md** - Social login & OAuth2
- **MFA.md** - Multi-factor authentication
- **RBAC.md** - Role & permission management
- **SECURITY.md** - Security best practices
- **INTEGRATION.md** - Database & email integration
- **BETTER_AUTH.md** - Better Auth guide

## Scripts

- **auth_generator.py** - Generate auth boilerplate
- **security_audit.py** - Audit auth implementation