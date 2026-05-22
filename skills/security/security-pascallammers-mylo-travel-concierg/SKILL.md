---
name: security
description: Auto-activates when user mentions security, vulnerabilities, OWASP, or secure coding. Expert in web security including OWASP Top 10, authentication, authorization, and secure coding practices.
category: security
---

# Security Best Practices

**Comprehensive web application security - OWASP Top 10, Authentication, Authorization, Vulnerabilities**

## Core Principles

1. **Never Trust User Input** - Always validate and sanitize
2. **Defense in Depth** - Multiple layers of security
3. **Principle of Least Privilege** - Minimum necessary permissions
4. **Secure by Default** - Security should be the default state
5. **Keep Secrets Secret** - Never commit credentials
6. **Fail Securely** - Errors should not expose sensitive information

## OWASP Top 10 (2024)

### 1. Broken Access Control

Access control enforces policy such that users cannot act outside of their intended permissions. Failures typically lead to unauthorized information disclosure, modification, or destruction of data.

#### ✅ Good: Proper Access Control
```typescript
// Implement Role-Based Access Control (RBAC)
interface User {
  id: string;
  role: 'admin' | 'user' | 'guest';
}

async function checkPermission(
  user: User, 
  resource: string, 
  action: 'read' | 'write' | 'delete'
): Promise<boolean> {
  const permissions = {
    admin: ['read', 'write', 'delete'],
    user: ['read', 'write'],
    guest: ['read'],
  };
  
  return permissions[user.role]?.includes(action) ?? false;
}

// Server-side route protection
export async function GET(request: Request) {
  const session = await getSession(request);
  
  if (!session?.user) {
    return new Response('Unauthorized', { status: 401 });
  }
  
  const hasAccess = await checkPermission(session.user, 'posts', 'read');
  if (!hasAccess) {
    return new Response('Forbidden', { status: 403 });
  }
  
  return Response.json(await getPosts());
}

// Validate object ownership
async function deletePost(userId: string, postId: string) {
  const post = await db.post.findUnique({ where: { id: postId } });
  
  if (!post) {
    throw new Error('Post not found');
  }
  
  if (post.authorId !== userId) {
    throw new Error('Forbidden: You can only delete your own posts');
  }
  
  await db.post.delete({ where: { id: postId } });
}

// Prevent insecure direct object references (IDOR)
// app/api/users/[id]/route.ts
export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const session = await getSession(request);
  
  // ✅ Verify user can access this profile
  if (session.user.id !== id && session.user.role !== 'admin') {
    return new Response('Forbidden', { status: 403 });
  }
  
  const user = await db.user.findUnique({ where: { id } });
  return Response.json(user);
}
```

#### ❌ Bad: Access Control Failures
```typescript
// ❌ WRONG - No authorization check
export async function GET(request: Request) {
  // Anyone can access all posts!
  return Response.json(await db.post.findMany());
}

// ❌ WRONG - Client-side only checks
function DeleteButton({ postId }: { postId: string }) {
  const { user } = useSession();
  
  // This can be bypassed! Must verify server-side
  if (user.role !== 'admin') return null;
  
  return <button onClick={() => deletePost(postId)}>Delete</button>;
}

// ❌ WRONG - Trusting URL parameters
export async function GET(request: Request) {
  const url = new URL(request.url);
  const userId = url.searchParams.get('userId');
  
  // ❌ User can change userId in URL to access others' data!
  return Response.json(await getUserData(userId));
}

// ❌ WRONG - Exposing IDs without validation
// GET /api/admin/users/123
// User changes to /api/admin/users/124 to see another user
```

#### Prevention Strategies
- Deny by default - require explicit grants
- Implement centralized access control mechanisms
- Enforce record ownership at API level
- Disable directory listing on web servers
- Log access control failures and alert admins
- Rate limit API access to minimize automated attacks
- Invalidate JWT tokens on logout server-side

### 2. Cryptographic Failures

Failures related to cryptography (or lack thereof) which often lead to exposure of sensitive data.

#### ✅ Good: Proper Cryptography
```typescript
import bcrypt from 'bcrypt';
import crypto from 'crypto';

// Password hashing with bcrypt
async function hashPassword(password: string): Promise<string> {
  const saltRounds = 12; // 2^12 iterations
  return await bcrypt.hash(password, saltRounds);
}

async function verifyPassword(
  password: string, 
  hash: string
): Promise<boolean> {
  return await bcrypt.compare(password, hash);
}

// Encrypt sensitive data at rest
function encryptData(data: string, key: Buffer): string {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  
  let encrypted = cipher.update(data, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  const authTag = cipher.getAuthTag();
  
  // Return IV + authTag + encrypted data
  return iv.toString('hex') + ':' + authTag.toString('hex') + ':' + encrypted;
}

function decryptData(encryptedData: string, key: Buffer): string {
  const [ivHex, authTagHex, encrypted] = encryptedData.split(':');
  
  const iv = Buffer.from(ivHex, 'hex');
  const authTag = Buffer.from(authTagHex, 'hex');
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
  
  decipher.setAuthTag(authTag);
  
  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  
  return decrypted;
}

// Secure random token generation
function generateSecureToken(length: number = 32): string {
  return crypto.randomBytes(length).toString('hex');
}

// Use HTTPS everywhere
// next.config.js
export default {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=63072000; includeSubDomains; preload'
          }
        ]
      }
    ];
  }
};
```

#### ❌ Bad: Cryptographic Failures
```typescript
// ❌ NEVER - Plain text passwords
await db.user.create({
  email,
  password, // Storing plain text!
});

// ❌ NEVER - Weak hashing algorithms
import crypto from 'crypto';
const hash = crypto.createHash('md5').update(password).digest('hex'); // MD5 is broken!
const hash2 = crypto.createHash('sha1').update(password).digest('hex'); // SHA1 is weak!

// ❌ NEVER - Weak random number generation
const token = Math.random().toString(36); // Predictable!

// ❌ NEVER - Hardcoded encryption keys
const SECRET_KEY = 'my-secret-key-123'; // Should be in env vars!

// ❌ NEVER - Transmitting sensitive data unencrypted
fetch('http://api.example.com/user', { // HTTP instead of HTTPS!
  headers: { 'Authorization': `Bearer ${token}` }
});

// ❌ NEVER - Storing sensitive data in localStorage
localStorage.setItem('creditCard', cardNumber); // XSS can steal this!
```

#### Prevention Strategies
- Classify data and apply controls per classification
- Don't store sensitive data unnecessarily
- Encrypt all sensitive data at rest using strong algorithms
- Ensure encryption keys are properly managed
- Use TLS 1.3+ with perfect forward secrecy (PFS)
- Disable caching for responses containing sensitive data
- Use bcrypt, scrypt, or Argon2 for password storage
- Initialize vectors (IVs) must be random and unique

### 3. Injection Attacks

Injection flaws occur when untrusted data is sent to an interpreter as part of a command or query.

#### ✅ Good: Injection Prevention
```typescript
// SQL Injection Prevention - Use Parameterized Queries
import { sql } from '@/lib/db';

// ✅ Parameterized query (safe)
async function getUserByEmail(email: string) {
  const users = await sql`
    SELECT id, name, email 
    FROM users 
    WHERE email = ${email}
  `;
  return users[0];
}

// ✅ With ORM (Prisma)
async function searchUsers(query: string) {
  return await prisma.user.findMany({
    where: {
      OR: [
        { name: { contains: query } },
        { email: { contains: query } }
      ]
    }
  });
}

// NoSQL Injection Prevention
async function findUserByUsername(username: string) {
  // ✅ Validate input type
  if (typeof username !== 'string') {
    throw new Error('Invalid username type');
  }
  
  // ✅ Use strict equality
  return await db.collection('users').findOne({ 
    username: username // Safe - string value
  });
}

// Command Injection Prevention
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

async function processFile(filename: string) {
  // ✅ Validate input against whitelist
  if (!/^[a-zA-Z0-9_-]+\.txt$/.test(filename)) {
    throw new Error('Invalid filename');
  }
  
  // ✅ Use array syntax (prevents shell interpretation)
  const { spawn } = require('child_process');
  const child = spawn('process', [filename]);
  
  return new Promise((resolve, reject) => {
    child.on('close', (code) => {
      if (code === 0) resolve('Success');
      else reject(new Error(`Process failed: ${code}`));
    });
  });
}

// LDAP Injection Prevention
function escapeLDAP(str: string): string {
  return str
    .replace(/\*/g, '\\2a')
    .replace(/\(/g, '\\28')
    .replace(/\)/g, '\\29')
    .replace(/\\/g, '\\5c')
    .replace(/\0/g, '\\00');
}

// XPath Injection Prevention - Use parameterized XPath
// Or better: avoid XPath entirely, use JSON/safer formats
```

#### ❌ Bad: Injection Vulnerabilities
```typescript
// ❌ SQL Injection
async function getUserByEmail(email: string) {
  // String concatenation = DANGEROUS!
  const query = `SELECT * FROM users WHERE email = '${email}'`;
  // Attacker can use: ' OR '1'='1
  return await db.query(query);
}

// ❌ NoSQL Injection
async function login(username: string, password: string) {
  // If username/password are objects, this is vulnerable!
  // Attacker sends: { $ne: null }
  return await db.collection('users').findOne({ 
    username: username, // Vulnerable if username is an object!
    password: password 
  });
}

// ❌ Command Injection
async function convertImage(filename: string) {
  // User input directly in command!
  // Attacker uses: "file.jpg; rm -rf /"
  await execAsync(`convert ${filename} output.png`);
}

// ❌ Template Injection
function renderTemplate(template: string, data: any) {
  // Directly evaluating user input!
  return eval(`\`${template}\``); // NEVER use eval with user input!
}
```

#### Prevention Strategies
- Use safe APIs that avoid interpreters entirely
- Use parameterized queries (prepared statements)
- Validate input using positive (allow-list) validation
- Escape special characters for the specific interpreter
- Use LIMIT and other SQL controls to prevent mass disclosure
- For NoSQL, ensure inputs are expected types

### 4. Insecure Design

Missing or ineffective security controls in the design phase.

#### ✅ Good: Secure Design Patterns
```typescript
// Threat modeling - identify threats early
// Secure design pattern: Defense in depth
class SecurePaymentProcessor {
  async processPayment(userId: string, amount: number) {
    // Layer 1: Input validation
    if (amount <= 0 || amount > 100000) {
      throw new Error('Invalid amount');
    }
    
    // Layer 2: Authentication check
    const user = await this.authenticateUser(userId);
    if (!user) {
      throw new Error('Unauthorized');
    }
    
    // Layer 3: Rate limiting
    const canProceed = await this.checkRateLimit(userId);
    if (!canProceed) {
      throw new Error('Rate limit exceeded');
    }
    
    // Layer 4: Authorization
    const hasPermission = await this.checkPermission(user, 'payment');
    if (!hasPermission) {
      throw new Error('Forbidden');
    }
    
    // Layer 5: Business logic validation
    const balance = await this.getBalance(userId);
    if (balance < amount) {
      throw new Error('Insufficient funds');
    }
    
    // Layer 6: Transaction
    return await this.executePayment(userId, amount);
  }
}

// Secure password reset flow
async function requestPasswordReset(email: string) {
  const user = await db.user.findUnique({ where: { email } });
  
  // ✅ Don't reveal if email exists (prevent enumeration)
  // Always return success message
  if (!user) {
    // Still send email to avoid timing attacks
    await simulateEmailDelay();
    return { message: 'If email exists, reset link sent' };
  }
  
  // ✅ Generate cryptographically secure token
  const token = crypto.randomBytes(32).toString('hex');
  const expires = new Date(Date.now() + 3600000); // 1 hour
  
  await db.passwordReset.create({
    data: { userId: user.id, token, expires }
  });
  
  // ✅ Send reset link over HTTPS only
  await sendEmail(email, `https://app.com/reset?token=${token}`);
  
  return { message: 'If email exists, reset link sent' };
}

// Secure by default configuration
const secureDefaults = {
  sessionTimeout: 30 * 60 * 1000, // 30 minutes
  maxLoginAttempts: 5,
  lockoutDuration: 15 * 60 * 1000, // 15 minutes
  passwordMinLength: 12,
  requireMFA: true,
  cookieOptions: {
    httpOnly: true,
    secure: true,
    sameSite: 'strict' as const,
  }
};
```

#### ❌ Bad: Insecure Design
```typescript
// ❌ No rate limiting
async function login(email: string, password: string) {
  // Attacker can brute force passwords!
  const user = await db.user.findUnique({ where: { email } });
  if (user && await verifyPassword(password, user.password)) {
    return createSession(user.id);
  }
  throw new Error('Invalid credentials');
}

// ❌ Information disclosure
async function resetPassword(email: string) {
  const user = await db.user.findUnique({ where: { email } });
  
  if (!user) {
    // ❌ Reveals if email exists!
    throw new Error('Email not found');
  }
  
  // ❌ Predictable token
  const token = user.id + '-' + Date.now();
  // Send reset link...
}

// ❌ Insecure defaults
const config = {
  sessionTimeout: Infinity, // Never expires!
  maxLoginAttempts: Infinity, // No limit!
  passwordMinLength: 4, // Too weak!
  requireMFA: false, // MFA should be default!
};
```

#### Prevention Strategies
- Establish and use secure development lifecycle
- Use threat modeling for critical flows
- Integrate security language and controls into user stories
- Establish secure design patterns and component library
- Use unit and integration tests to validate security
- Segregate tier layers (presentation, business, data)
- Implement rate limiting at all application layers

### 5. Security Misconfiguration

Security misconfiguration is the most common vulnerability, often resulting from insecure default configurations.

#### ✅ Good: Secure Configuration
```typescript
// Production-ready Next.js configuration
// next.config.js
export default {
  poweredByHeader: false, // Hide X-Powered-By header
  
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on'
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin'
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=()'
          }
        ]
      }
    ];
  },
  
  // Disable source maps in production
  productionBrowserSourceMaps: false,
};

// Environment-specific configurations
// lib/config.ts
const configs = {
  development: {
    apiUrl: 'http://localhost:3000/api',
    debug: true,
    logLevel: 'debug',
  },
  production: {
    apiUrl: 'https://api.example.com',
    debug: false, // ✅ Disable debug in production
    logLevel: 'error',
  }
};

export const config = configs[process.env.NODE_ENV || 'development'];

// Secure error handling
export async function GET(request: Request) {
  try {
    const data = await fetchData();
    return Response.json(data);
  } catch (error) {
    // ✅ Log detailed error server-side
    console.error('Detailed error:', error);
    
    // ✅ Return generic error to client
    return Response.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

#### ❌ Bad: Security Misconfiguration
```typescript
// ❌ Exposing detailed errors
export async function GET(request: Request) {
  try {
    const data = await fetchData();
    return Response.json(data);
  } catch (error) {
    // ❌ Exposes stack trace and internal paths!
    return Response.json(
      { error: error.message, stack: error.stack },
      { status: 500 }
    );
  }
}

// ❌ Debug mode in production
const config = {
  debug: true, // ❌ Shows detailed errors to users
  verboseLogging: true,
};

// ❌ Default credentials
const admin = {
  username: 'admin', // ❌ Default username
  password: 'admin123', // ❌ Default password
};

// ❌ Unnecessary features enabled
const features = {
  autoIndex: true, // ❌ Directory listing enabled
  cors: '*', // ❌ Allow all origins
  fileUpload: true, // ❌ No restrictions
};
```

#### Prevention Strategies
- Repeatable hardening process for all environments
- Minimal platform without unnecessary features
- Review and update configurations regularly
- Segmented application architecture with proper separation
- Send security directives to clients (security headers)
- Automated process to verify configuration effectiveness
- Disable directory listings and error stack traces in production

### 6. Vulnerable and Outdated Components

Using components with known vulnerabilities.

#### ✅ Good: Dependency Management
```bash
# Regular dependency audits
bun audit
npm audit
yarn audit

# Fix vulnerabilities automatically
npm audit fix

# Use Snyk for comprehensive scanning
npx snyk test
npx snyk monitor

# Keep dependencies updated
npm outdated
npm update

# Use Dependabot (GitHub)
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

```typescript
// Pin dependency versions in package.json
{
  "dependencies": {
    "next": "15.0.0", // ✅ Exact version
    "react": "^19.0.0" // ✅ Or use ^ for minor updates
  },
  "overrides": {
    // Force specific version to fix vulnerability
    "lodash": "4.17.21"
  }
}

// Monitor for security advisories
// Use tools like Socket.dev, Snyk, or GitHub Security Advisories
```

#### ❌ Bad: Vulnerable Dependencies
```json
{
  "dependencies": {
    "express": "*", // ❌ Any version - dangerous!
    "lodash": "4.17.0", // ❌ Known vulnerabilities
    "moment": "2.24.0" // ❌ Deprecated, use date-fns
  }
}
```

#### Prevention Strategies
- Remove unused dependencies, features, files
- Continuously inventory versions (client and server)
- Subscribe to security bulletins for components
- Obtain components from official sources over HTTPS
- Monitor for unmaintained libraries
- Use Software Composition Analysis (SCA) tools
- Create security patch policy for critical updates

### 7. Identification and Authentication Failures

Confirmation of user identity, authentication, and session management is critical.

#### ✅ Good: Authentication Security
```typescript
import { hash, verify } from '@node-rs/argon2';
import { SignJWT, jwtVerify } from 'jose';

// Strong password hashing with Argon2
async function hashPassword(password: string): Promise<string> {
  return await hash(password, {
    memoryCost: 19456,
    timeCost: 2,
    outputLen: 32,
    parallelism: 1,
  });
}

async function verifyPassword(
  password: string,
  hash: string
): Promise<boolean> {
  return await verify(hash, password);
}

// Secure session management
interface Session {
  userId: string;
  expiresAt: Date;
}

async function createSession(userId: string): Promise<string> {
  const secret = new TextEncoder().encode(process.env.JWT_SECRET);
  
  const token = await new SignJWT({ userId })
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('7d')
    .sign(secret);
  
  return token;
}

async function validateSession(token: string): Promise<Session> {
  const secret = new TextEncoder().encode(process.env.JWT_SECRET);
  
  try {
    const { payload } = await jwtVerify(token, secret);
    
    return {
      userId: payload.userId as string,
      expiresAt: new Date(payload.exp! * 1000),
    };
  } catch {
    throw new Error('Invalid session');
  }
}

// Multi-factor authentication
import { authenticator } from 'otplib';

function generateTOTPSecret(): string {
  return authenticator.generateSecret();
}

function verifyTOTP(token: string, secret: string): boolean {
  return authenticator.verify({ token, secret });
}

// Account lockout after failed attempts
const loginAttempts = new Map<string, { count: number; lockUntil?: Date }>();

async function attemptLogin(email: string, password: string) {
  const attempts = loginAttempts.get(email);
  
  // Check if account is locked
  if (attempts?.lockUntil && attempts.lockUntil > new Date()) {
    const minutes = Math.ceil(
      (attempts.lockUntil.getTime() - Date.now()) / 60000
    );
    throw new Error(`Account locked. Try again in ${minutes} minutes`);
  }
  
  const user = await db.user.findUnique({ where: { email } });
  
  if (!user || !(await verifyPassword(password, user.passwordHash))) {
    // Increment failed attempts
    const current = loginAttempts.get(email) || { count: 0 };
    current.count++;
    
    if (current.count >= 5) {
      // Lock account for 15 minutes
      current.lockUntil = new Date(Date.now() + 15 * 60 * 1000);
    }
    
    loginAttempts.set(email, current);
    throw new Error('Invalid credentials');
  }
  
  // Reset attempts on successful login
  loginAttempts.delete(email);
  
  return createSession(user.id);
}

// Secure password reset
async function resetPassword(token: string, newPassword: string) {
  const reset = await db.passwordReset.findUnique({ 
    where: { token },
    include: { user: true }
  });
  
  if (!reset || reset.expires < new Date()) {
    throw new Error('Invalid or expired reset token');
  }
  
  // Validate password strength
  if (newPassword.length < 12) {
    throw new Error('Password must be at least 12 characters');
  }
  
  const passwordHash = await hashPassword(newPassword);
  
  await db.user.update({
    where: { id: reset.userId },
    data: { passwordHash }
  });
  
  // Invalidate reset token
  await db.passwordReset.delete({ where: { token } });
  
  // Invalidate all existing sessions
  await db.session.deleteMany({ where: { userId: reset.userId } });
}
```

#### ❌ Bad: Authentication Failures
```typescript
// ❌ Weak password hashing
const hash = crypto.createHash('sha256').update(password).digest('hex');

// ❌ No password requirements
async function register(email: string, password: string) {
  // ❌ Accepts "123" as password
  await db.user.create({ email, password });
}

// ❌ Predictable session tokens
const sessionToken = user.id + '-' + Date.now(); // Easy to guess!

// ❌ No session expiration
const token = jwt.sign({ userId }, secret); // Never expires!

// ❌ No account lockout
async function login(email: string, password: string) {
  // Attacker can try unlimited passwords!
  const user = await db.user.findUnique({ where: { email } });
  // ...
}

// ❌ Exposing user enumeration
async function resetPassword(email: string) {
  const user = await db.user.findUnique({ where: { email } });
  if (!user) {
    throw new Error('User not found'); // ❌ Reveals if email exists!
  }
}
```

#### Prevention Strategies
- Implement multi-factor authentication
- Use weak password checks (check against known breached passwords)
- Limit or delay failed login attempts
- Use secure, random session identifiers
- Invalidate session IDs after logout
- Rotate session IDs after privilege escalation
- Ensure registration and credential recovery are resistant to enumeration

### 8. Software and Data Integrity Failures

Code and infrastructure that don't protect against integrity violations.

#### ✅ Good: Integrity Protection
```typescript
// Verify package integrity with lock files
// package-lock.json, bun.lockb, yarn.lock

// Use Subresource Integrity (SRI) for external scripts
export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <script
          src="https://cdn.example.com/lib.js"
          integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8wC"
          crossOrigin="anonymous"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}

// Digital signatures for critical operations
import { createSign, createVerify } from 'crypto';

function signData(data: string, privateKey: string): string {
  const sign = createSign('RSA-SHA256');
  sign.update(data);
  return sign.sign(privateKey, 'hex');
}

function verifySignature(
  data: string,
  signature: string,
  publicKey: string
): boolean {
  const verify = createVerify('RSA-SHA256');
  verify.update(data);
  return verify.verify(publicKey, signature, 'hex');
}

// CI/CD pipeline security
// .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # ✅ Verify dependencies
      - name: Audit dependencies
        run: npm audit --audit-level=high
      
      # ✅ Run security scans
      - name: Security scan
        run: npx snyk test
      
      # ✅ Build with verification
      - name: Build
        run: npm run build
      
      # ✅ Sign artifacts
      - name: Sign build
        run: |
          echo "${{ secrets.SIGNING_KEY }}" > key.pem
          openssl dgst -sha256 -sign key.pem -out build.sig build/
```

#### ❌ Bad: Integrity Failures
```typescript
// ❌ No integrity verification
<script src="https://cdn.example.com/lib.js" />

// ❌ Insecure deserialization
function loadUserData(serialized: string) {
  return eval(serialized); // ❌ NEVER!
}

// ❌ Auto-update without verification
async function autoUpdate() {
  const update = await fetch('http://updates.example.com/latest');
  // ❌ No signature verification!
  await installUpdate(update);
}
```

#### Prevention Strategies
- Use digital signatures to verify software origin
- Ensure libraries and dependencies are from trusted repos
- Use SRI to verify external resources
- Review code and configuration changes
- Ensure CI/CD pipeline has proper segregation and access control
- Don't send unsigned or unencrypted data to untrusted clients

### 9. Security Logging and Monitoring Failures

Insufficient logging and monitoring can prevent detection of breaches.

#### ✅ Good: Security Logging
```typescript
import winston from 'winston';

// Structured logging
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'api' },
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});

// Log security events
async function login(email: string, password: string, ip: string) {
  const user = await db.user.findUnique({ where: { email } });
  
  if (!user || !(await verifyPassword(password, user.passwordHash))) {
    // ✅ Log failed login attempt
    logger.warn('Failed login attempt', {
      email,
      ip,
      timestamp: new Date().toISOString(),
      event: 'LOGIN_FAILED'
    });
    throw new Error('Invalid credentials');
  }
  
  // ✅ Log successful login
  logger.info('Successful login', {
    userId: user.id,
    email,
    ip,
    timestamp: new Date().toISOString(),
    event: 'LOGIN_SUCCESS'
  });
  
  return createSession(user.id);
}

// Monitor suspicious activity
async function detectSuspiciousActivity(userId: string) {
  const recentLogins = await db.loginLog.findMany({
    where: {
      userId,
      timestamp: { gte: new Date(Date.now() - 24 * 60 * 60 * 1000) }
    }
  });
  
  // Check for multiple locations
  const locations = new Set(recentLogins.map(l => l.location));
  if (locations.size > 3) {
    logger.warn('Suspicious activity detected', {
      userId,
      event: 'MULTIPLE_LOCATIONS',
      locations: Array.from(locations)
    });
    
    // Send alert
    await sendSecurityAlert(userId, 'Multiple login locations detected');
  }
}

// Audit trail
async function updateUserRole(adminId: string, userId: string, newRole: string) {
  const oldUser = await db.user.findUnique({ where: { id: userId } });
  
  await db.user.update({
    where: { id: userId },
    data: { role: newRole }
  });
  
  // ✅ Log privilege escalation
  await db.auditLog.create({
    data: {
      adminId,
      userId,
      action: 'UPDATE_ROLE',
      oldValue: oldUser?.role,
      newValue: newRole,
      timestamp: new Date(),
    }
  });
  
  logger.info('User role updated', {
    adminId,
    userId,
    oldRole: oldUser?.role,
    newRole,
    event: 'ROLE_CHANGE'
  });
}
```

#### ❌ Bad: Logging Failures
```typescript
// ❌ No logging
async function login(email: string, password: string) {
  const user = await db.user.findUnique({ where: { email } });
  if (!user) throw new Error('Invalid credentials');
  return createSession(user.id);
  // ❌ No record of who logged in or when
}

// ❌ Logging sensitive data
logger.info('User login', {
  email,
  password, // ❌ NEVER log passwords!
  creditCard: user.creditCard, // ❌ NEVER log PII!
});

// ❌ Logs not monitored
// Logs exist but nobody reviews them
```

#### Prevention Strategies
- Log all login, access control, and server-side validation failures
- Ensure logs include sufficient context for forensics
- Ensure log data is encoded to prevent injection attacks
- Ensure high-value transactions have audit trail
- Establish effective monitoring and alerting
- Establish incident response and recovery plan
- Use centralized log management (ELK, Splunk, Datadog)

### 10. Server-Side Request Forgery (SSRF)

SSRF flaws occur when a web application fetches a remote resource without validating the user-supplied URL.

#### ✅ Good: SSRF Prevention
```typescript
// Validate and sanitize URLs
function isValidUrl(url: string): boolean {
  try {
    const parsed = new URL(url);
    
    // ✅ Whitelist allowed protocols
    if (!['http:', 'https:'].includes(parsed.protocol)) {
      return false;
    }
    
    // ✅ Block private IP ranges
    const hostname = parsed.hostname;
    
    // Block localhost
    if (hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '::1') {
      return false;
    }
    
    // Block private IP ranges
    const privateIPRanges = [
      /^10\./,
      /^172\.(1[6-9]|2[0-9]|3[0-1])\./,
      /^192\.168\./,
      /^169\.254\./,
    ];
    
    if (privateIPRanges.some(range => range.test(hostname))) {
      return false;
    }
    
    // ✅ Whitelist allowed domains
    const allowedDomains = ['api.example.com', 'cdn.example.com'];
    if (!allowedDomains.some(domain => hostname.endsWith(domain))) {
      return false;
    }
    
    return true;
  } catch {
    return false;
  }
}

async function fetchRemoteResource(url: string) {
  if (!isValidUrl(url)) {
    throw new Error('Invalid URL');
  }
  
  // ✅ Use allowlist for domains
  const response = await fetch(url, {
    // ✅ Set timeout
    signal: AbortSignal.timeout(5000),
    // ✅ Don't follow redirects to prevent bypass
    redirect: 'manual'
  });
  
  return response;
}

// Webhook validation
async function handleWebhook(webhookUrl: string, data: any) {
  // ✅ Validate webhook URL is pre-registered
  const webhook = await db.webhook.findUnique({ 
    where: { url: webhookUrl } 
  });
  
  if (!webhook) {
    throw new Error('Webhook not registered');
  }
  
  // ✅ Additional URL validation
  if (!isValidUrl(webhookUrl)) {
    throw new Error('Invalid webhook URL');
  }
  
  await fetch(webhookUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
    signal: AbortSignal.timeout(5000),
  });
}
```

#### ❌ Bad: SSRF Vulnerabilities
```typescript
// ❌ No URL validation
async function fetchAvatar(avatarUrl: string) {
  // ❌ User can request internal resources!
  // Example: http://localhost:6379/
  // Example: http://169.254.169.254/latest/meta-data/
  const response = await fetch(avatarUrl);
  return response.blob();
}

// ❌ Insufficient validation
async function proxyRequest(url: string) {
  // ❌ Only checks protocol, not hostname
  if (url.startsWith('http')) {
    return await fetch(url);
  }
}
```

#### Prevention Strategies
- Sanitize and validate all client-supplied input data
- Enforce URL schema, port, and destination with allow list
- Disable HTTP redirections
- Don't send raw responses to clients
- Implement network segmentation (DMZ, internal network separation)
- Use DNS resolution monitoring and blocking

## Authentication & Authorization

### JSON Web Tokens (JWT) Security

#### ✅ Good: Secure JWT Implementation
```typescript
import { SignJWT, jwtVerify } from 'jose';

const JWT_SECRET = new TextEncoder().encode(process.env.JWT_SECRET);

// Use RS256 for better security (asymmetric)
async function createToken(userId: string) {
  const token = await new SignJWT({ userId })
    .setProtectedHeader({ alg: 'HS256' }) // Or RS256 with key pair
    .setIssuedAt()
    .setIssuer('https://example.com')
    .setAudience('https://example.com')
    .setExpirationTime('15m') // Short-lived access token
    .sign(JWT_SECRET);
  
  return token;
}

async function createRefreshToken(userId: string) {
  const token = await new SignJWT({ userId, type: 'refresh' })
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('7d') // Longer-lived refresh token
    .sign(JWT_SECRET);
  
  // Store refresh token in database for revocation
  await db.refreshToken.create({
    data: { userId, token, expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000) }
  });
  
  return token;
}

async function verifyToken(token: string) {
  try {
    const { payload } = await jwtVerify(token, JWT_SECRET, {
      issuer: 'https://example.com',
      audience: 'https://example.com',
    });
    
    return payload;
  } catch (error) {
    throw new Error('Invalid token');
  }
}

// Token refresh flow
async function refreshAccessToken(refreshToken: string) {
  const { payload } = await verifyToken(refreshToken);
  
  // Verify refresh token exists in database
  const storedToken = await db.refreshToken.findUnique({
    where: { token: refreshToken }
  });
  
  if (!storedToken || storedToken.expiresAt < new Date()) {
    throw new Error('Invalid refresh token');
  }
  
  // Generate new access token
  const accessToken = await createToken(payload.userId as string);
  
  return accessToken;
}

// Logout - revoke refresh token
async function logout(refreshToken: string) {
  await db.refreshToken.delete({ where: { token: refreshToken } });
}
```

#### ❌ Bad: JWT Vulnerabilities
```typescript
// ❌ No expiration
const token = jwt.sign({ userId }, secret); // Never expires!

// ❌ Weak secret
const token = jwt.sign({ userId }, 'secret'); // Brute-forceable!

// ❌ Algorithm confusion
jwt.verify(token, publicKey, { algorithms: ['HS256', 'none'] }); // Allows 'none'!

// ❌ No validation
const decoded = jwt.decode(token); // Doesn't verify signature!

// ❌ Sensitive data in payload
const token = jwt.sign({ 
  userId, 
  password, // ❌ JWT is base64-encoded, not encrypted!
  creditCard 
}, secret);
```

### OAuth 2.0 & OpenID Connect

#### ✅ Good: OAuth Implementation
```typescript
// Authorization Code Flow with PKCE
import crypto from 'crypto';

function generateCodeVerifier(): string {
  return crypto.randomBytes(32).toString('base64url');
}

function generateCodeChallenge(verifier: string): string {
  return crypto
    .createHash('sha256')
    .update(verifier)
    .digest('base64url');
}

async function initiateOAuth() {
  const codeVerifier = generateCodeVerifier();
  const codeChallenge = generateCodeChallenge(codeVerifier);
  const state = crypto.randomBytes(16).toString('hex');
  
  // Store for verification
  await storeOAuthState(state, codeVerifier);
  
  const authUrl = new URL('https://provider.com/oauth/authorize');
  authUrl.searchParams.set('client_id', process.env.OAUTH_CLIENT_ID!);
  authUrl.searchParams.set('redirect_uri', 'https://app.com/callback');
  authUrl.searchParams.set('response_type', 'code');
  authUrl.searchParams.set('scope', 'openid profile email');
  authUrl.searchParams.set('state', state);
  authUrl.searchParams.set('code_challenge', codeChallenge);
  authUrl.searchParams.set('code_challenge_method', 'S256');
  
  return authUrl.toString();
}

async function handleOAuthCallback(code: string, state: string) {
  // Verify state to prevent CSRF
  const stored = await getOAuthState(state);
  if (!stored) {
    throw new Error('Invalid state');
  }
  
  // Exchange code for token
  const response = await fetch('https://provider.com/oauth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: 'https://app.com/callback',
      client_id: process.env.OAUTH_CLIENT_ID!,
      client_secret: process.env.OAUTH_CLIENT_SECRET!,
      code_verifier: stored.codeVerifier,
    }),
  });
  
  const { access_token, id_token } = await response.json();
  
  // Verify ID token
  const userInfo = await verifyIdToken(id_token);
  
  return { access_token, userInfo };
}
```

## Common Vulnerabilities

### Cross-Site Scripting (XSS)

#### ✅ Good: XSS Prevention
```typescript
// React automatically escapes values
export function UserProfile({ name }: { name: string }) {
  // ✅ Automatic escaping
  return <div>{name}</div>;
}

// Sanitize HTML with DOMPurify
import DOMPurify from 'isomorphic-dompurify';

export function RichContent({ html }: { html: string }) {
  const sanitized = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
    ALLOWED_ATTR: ['href', 'title'],
  });
  
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}

// Content Security Policy (detailed in Security Headers section)
```

#### ❌ Bad: XSS Vulnerabilities
```typescript
// ❌ Dangerous HTML injection
export function Comment({ text }: { text: string }) {
  return <div dangerouslySetInnerHTML={{ __html: text }} />; // XSS!
}

// ❌ Direct DOM manipulation
function updateContent(userInput: string) {
  document.getElementById('content')!.innerHTML = userInput; // XSS!
}
```

### Cross-Site Request Forgery (CSRF)

#### ✅ Good: CSRF Protection
```typescript
// Next.js Server Actions have built-in CSRF protection

// For API routes, use CSRF tokens
import { getCsrfToken, validateCsrfToken } from '@/lib/csrf';

export async function POST(request: Request) {
  const csrfToken = request.headers.get('x-csrf-token');
  
  if (!validateCsrfToken(csrfToken)) {
    return new Response('Invalid CSRF token', { status: 403 });
  }
  
  // Process request...
}

// SameSite cookies
export function setSessionCookie(token: string) {
  return `session=${token}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=86400`;
}

// Double submit cookie pattern
async function handleFormSubmit(request: Request) {
  const cookies = parseCookies(request.headers.get('cookie'));
  const formData = await request.formData();
  const csrfToken = formData.get('csrf_token');
  
  if (cookies.csrf_token !== csrfToken) {
    throw new Error('CSRF token mismatch');
  }
  
  // Process form...
}
```

#### ❌ Bad: Missing CSRF Protection
```typescript
// ❌ No CSRF protection
export async function POST(request: Request) {
  // Any site can POST to this endpoint!
  const data = await request.json();
  await updateUserSettings(data);
}
```

### Clickjacking

#### ✅ Good: Clickjacking Prevention
```typescript
// X-Frame-Options header
export async function middleware(request: Request) {
  const response = NextResponse.next();
  response.headers.set('X-Frame-Options', 'DENY');
  // Or: 'SAMEORIGIN' to allow same-origin frames
  return response;
}

// Content-Security-Policy frame-ancestors
response.headers.set(
  'Content-Security-Policy',
  "frame-ancestors 'none'" // Or 'self' for same-origin
);
```

### Path Traversal

#### ✅ Good: Path Traversal Prevention
```typescript
import path from 'path';
import { promises as fs } from 'fs';

async function readUserFile(filename: string) {
  // ✅ Validate filename
  if (!/^[a-zA-Z0-9_-]+\.txt$/.test(filename)) {
    throw new Error('Invalid filename');
  }
  
  // ✅ Resolve path and verify it's within allowed directory
  const uploadsDir = path.resolve('./uploads');
  const filePath = path.resolve(uploadsDir, filename);
  
  if (!filePath.startsWith(uploadsDir)) {
    throw new Error('Path traversal detected');
  }
  
  return await fs.readFile(filePath, 'utf-8');
}
```

#### ❌ Bad: Path Traversal Vulnerability
```typescript
// ❌ No validation
async function readFile(filename: string) {
  // User can use: ../../etc/passwd
  return await fs.readFile(`./uploads/${filename}`);
}
```

### Prototype Pollution

#### ✅ Good: Prototype Pollution Prevention
```typescript
// Create objects without prototype
const obj = Object.create(null);
obj.data = 'safe';

// Freeze prototypes
Object.freeze(Object.prototype);
Object.freeze(Array.prototype);

// Validate object keys
function merge(target: any, source: any) {
  const dangerousKeys = ['__proto__', 'constructor', 'prototype'];
  
  for (const key in source) {
    if (dangerousKeys.includes(key)) {
      continue; // Skip dangerous keys
    }
    
    target[key] = source[key];
  }
  
  return target;
}

// Use Map instead of objects for user data
const userSettings = new Map<string, string>();
userSettings.set('theme', 'dark');
```

#### ❌ Bad: Prototype Pollution
```typescript
// ❌ Unsafe merge
function merge(target: any, source: any) {
  for (const key in source) {
    target[key] = source[key]; // Can pollute prototype!
  }
}

// Attacker sends: { "__proto__": { "isAdmin": true } }
```

### XML External Entity (XXE) Attacks

#### ✅ Good: XXE Prevention
```typescript
// Use JSON instead of XML when possible

// If XML is necessary, disable external entities
import { parseStringPromise } from 'xml2js';

async function parseXML(xmlString: string) {
  return await parseStringPromise(xmlString, {
    explicitArray: false,
    // Disable external entities
    strict: true,
  });
}

// For libxmljs
import libxmljs from 'libxmljs';

function parseXMLSafe(xmlString: string) {
  return libxmljs.parseXml(xmlString, {
    noent: false, // Disable entity expansion
    nonet: true, // Disable network access
  });
}
```

## Security Headers

### Content Security Policy (CSP)

#### ✅ Good: Strict CSP with Nonces
```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import crypto from 'crypto';

export function middleware(request: Request) {
  const nonce = crypto.randomBytes(16).toString('base64');
  
  const cspHeader = `
    default-src 'self';
    script-src 'self' 'nonce-${nonce}' 'strict-dynamic' https: http:;
    style-src 'self' 'nonce-${nonce}';
    img-src 'self' blob: data: https:;
    font-src 'self';
    object-src 'none';
    base-uri 'self';
    form-action 'self';
    frame-ancestors 'none';
    upgrade-insecure-requests;
  `.replace(/\s{2,}/g, ' ').trim();
  
  const response = NextResponse.next();
  response.headers.set('Content-Security-Policy', cspHeader);
  response.headers.set('X-Nonce', nonce);
  
  return response;
}

// Use nonce in layout
import { headers } from 'next/headers';

export default async function RootLayout({ children }) {
  const headersList = await headers();
  const nonce = headersList.get('X-Nonce');
  
  return (
    <html>
      <head>
        <script nonce={nonce} src="/app.js" />
        <style nonce={nonce}>{`body { margin: 0; }`}</style>
      </head>
      <body>{children}</body>
    </html>
  );
}
```

#### ✅ Good: Hash-based CSP
```typescript
// For static inline scripts, use hashes
const cspHeader = `
  default-src 'self';
  script-src 'self' 'sha256-abc123...';
  style-src 'self' 'sha256-def456...';
`;

// Generate hash:
// echo -n "console.log('Hello')" | openssl dgst -sha256 -binary | openssl base64
```

### Comprehensive Security Headers

```typescript
// next.config.js
export default {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on'
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=63072000; includeSubDomains; preload'
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block'
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin'
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=(), interest-cohort=()'
          }
        ]
      }
    ];
  }
};
```

### Security Headers Explained

#### Strict-Transport-Security (HSTS)
Forces browsers to use HTTPS for all requests.

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

- `max-age`: How long to enforce HTTPS (seconds)
- `includeSubDomains`: Apply to all subdomains
- `preload`: Submit to HSTS preload list

#### X-Frame-Options
Prevents clickjacking attacks.

```http
X-Frame-Options: DENY
# Or: SAMEORIGIN
```

#### X-Content-Type-Options
Prevents MIME type sniffing.

```http
X-Content-Type-Options: nosniff
```

#### Referrer-Policy
Controls how much referrer information is sent.

```http
Referrer-Policy: strict-origin-when-cross-origin
```

Options:
- `no-referrer`: Never send
- `same-origin`: Only to same origin
- `strict-origin-when-cross-origin`: Send origin to cross-origin HTTPS

#### Permissions-Policy
Controls browser features.

```http
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

## Secrets Management

### Environment Variables

#### ✅ Good: Secure Environment Variables
```typescript
// .env.local (gitignored)
DATABASE_URL=postgresql://...
JWT_SECRET=...
STRIPE_SECRET_KEY=sk_...

// Client vs Server environment variables in Next.js
NEXT_PUBLIC_API_URL=https://api.example.com  // Exposed to browser
API_SECRET_KEY=secret  // Server-only

// Type-safe environment variables
// lib/env.ts
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
  NEXT_PUBLIC_API_URL: z.string().url(),
});

export const env = envSchema.parse(process.env);

// .gitignore
.env
.env.local
.env.*.local
*.key
*.pem
```

#### ❌ Bad: Secrets Mismanagement
```typescript
// ❌ Hardcoded secrets
const apiKey = 'sk-abc123'; // NEVER!

// ❌ Committed .env file
// Should be in .gitignore!

// ❌ Logging secrets
console.log('API Key:', process.env.API_KEY);

// ❌ Exposing server secrets to client
const config = {
  DATABASE_URL: process.env.DATABASE_URL // ❌ Exposed to browser!
};
```

### Secret Rotation

```typescript
// Implement secret rotation
interface SecretVersion {
  version: number;
  secret: string;
  createdAt: Date;
  expiresAt: Date;
}

class SecretManager {
  private secrets: SecretVersion[] = [];
  
  async getCurrentSecret(): Promise<string> {
    const current = this.secrets.find(s => s.expiresAt > new Date());
    if (!current) {
      throw new Error('No valid secret');
    }
    return current.secret;
  }
  
  async validateSecret(token: string): Promise<boolean> {
    // Try all non-expired secrets (allows grace period)
    for (const { secret } of this.secrets) {
      try {
        await jwtVerify(token, new TextEncoder().encode(secret));
        return true;
      } catch {
        continue;
      }
    }
    return false;
  }
  
  async rotateSecret(): Promise<void> {
    const newSecret = generateSecureToken(64);
    const newVersion: SecretVersion = {
      version: this.secrets.length + 1,
      secret: newSecret,
      createdAt: new Date(),
      expiresAt: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000), // 90 days
    };
    
    this.secrets.push(newVersion);
    
    // Remove expired secrets
    this.secrets = this.secrets.filter(s => s.expiresAt > new Date());
  }
}
```

### Cloud Secret Managers

```typescript
// AWS Secrets Manager
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager';

const client = new SecretsManagerClient({ region: 'us-east-1' });

async function getSecret(secretName: string): Promise<string> {
  const command = new GetSecretValueCommand({ SecretId: secretName });
  const response = await client.send(command);
  return response.SecretString!;
}

// Vercel Environment Variables
// Use Vercel CLI or dashboard
// vercel env pull .env.local

// HashiCorp Vault
import vault from 'node-vault';

const vaultClient = vault({
  endpoint: process.env.VAULT_ADDR,
  token: process.env.VAULT_TOKEN,
});

async function getVaultSecret(path: string) {
  const result = await vaultClient.read(path);
  return result.data;
}
```

## HTTPS & Certificates

### TLS Best Practices

#### ✅ Good: TLS Configuration
```nginx
# nginx.conf
server {
  listen 443 ssl http2;
  server_name example.com;
  
  # Modern TLS configuration
  ssl_certificate /path/to/cert.pem;
  ssl_certificate_key /path/to/key.pem;
  
  # Use TLS 1.2 and 1.3 only
  ssl_protocols TLSv1.2 TLSv1.3;
  
  # Strong cipher suites
  ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
  ssl_prefer_server_ciphers on;
  
  # Enable OCSP stapling
  ssl_stapling on;
  ssl_stapling_verify on;
  
  # HSTS
  add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
  
  # Session cache
  ssl_session_cache shared:SSL:10m;
  ssl_session_timeout 10m;
}
```

### Certificate Management

```bash
# Let's Encrypt with Certbot
sudo certbot --nginx -d example.com -d www.example.com

# Auto-renewal
sudo certbot renew --dry-run

# Certificate expiration monitoring
openssl x509 -in cert.pem -noout -dates

# Test SSL configuration
openssl s_client -connect example.com:443 -servername example.com
```

### HSTS Preload

To submit your domain to the HSTS preload list:

1. Serve valid HTTPS
2. Redirect HTTP to HTTPS
3. Serve HSTS header on all requests:
   ```http
   Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
   ```
4. Submit to https://hstspreload.org/

### Mixed Content Prevention

```typescript
// Ensure all resources use HTTPS
export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        {/* ✅ HTTPS URLs */}
        <link href="https://fonts.googleapis.com/css?family=Inter" rel="stylesheet" />
        <script src="https://cdn.example.com/lib.js" />
        
        {/* ❌ HTTP URLs will be blocked */}
        {/* <script src="http://cdn.example.com/lib.js" /> */}
      </head>
      <body>{children}</body>
    </html>
  );
}

// Upgrade insecure requests with CSP
// Content-Security-Policy: upgrade-insecure-requests
```

## Security Testing

### Dependency Scanning

```bash
# npm audit
npm audit
npm audit fix
npm audit fix --force

# Snyk
npx snyk test
npx snyk monitor
npx snyk wizard

# OWASP Dependency Check
dependency-check --project MyApp --scan .

# GitHub Dependabot
# Enable in repository settings > Security & analysis

# Socket.dev - detect malicious packages
npx socket npm audit
```

### Static Application Security Testing (SAST)

```bash
# ESLint security plugins
npm install --save-dev eslint-plugin-security

# .eslintrc.js
module.exports = {
  plugins: ['security'],
  extends: ['plugin:security/recommended'],
};

# Semgrep - multi-language static analysis
npm install -g @semgrep/cli
semgrep --config=auto .

# CodeQL (GitHub)
# .github/workflows/codeql.yml
name: "CodeQL"
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: javascript, typescript
      - uses: github/codeql-action/analyze@v3
```

### Dynamic Application Security Testing (DAST)

```bash
# OWASP ZAP
# Download from https://www.zaproxy.org/

# Baseline scan
docker run -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t https://example.com

# Full scan
docker run -t ghcr.io/zaproxy/zaproxy:stable zap-full-scan.py -t https://example.com

# Burp Suite
# Professional tool for manual testing
# https://portswigger.net/burp

# Nuclei - vulnerability scanner
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
nuclei -u https://example.com
```

### Penetration Testing

```bash
# Reconnaissance
nmap -sV -sC example.com
whatweb https://example.com

# Subdomain enumeration
subfinder -d example.com
amass enum -d example.com

# Directory brute force
gobuster dir -u https://example.com -w /path/to/wordlist.txt

# SQL injection testing
sqlmap -u "https://example.com/page?id=1"

# XSS testing
dalfox url https://example.com/search?q=test
```

### Security Testing Checklist

- [ ] Run dependency audit (npm audit, Snyk)
- [ ] Static code analysis (ESLint security, Semgrep)
- [ ] Dynamic scanning (OWASP ZAP)
- [ ] Test authentication flows
- [ ] Test authorization controls
- [ ] Input validation testing
- [ ] XSS testing
- [ ] CSRF protection verification
- [ ] SQL injection testing
- [ ] API security testing
- [ ] Security headers verification
- [ ] TLS/SSL configuration check
- [ ] Secrets scanning (no hardcoded credentials)
- [ ] Review access controls
- [ ] Test rate limiting
- [ ] Verify logging and monitoring

## Input Validation

### ✅ Good: Comprehensive Validation
```typescript
import { z } from 'zod';

// Validate all inputs with Zod
const UserSchema = z.object({
  email: z.string().email().max(255),
  password: z.string().min(12).max(128),
  age: z.number().int().min(13).max(120),
  website: z.string().url().optional(),
  bio: z.string().max(1000).optional(),
});

function createUser(input: unknown) {
  // Validate throws if invalid
  const data = UserSchema.parse(input);
  
  // Now safe to use
  return db.users.create(data);
}

// Sanitize HTML input
import DOMPurify from 'isomorphic-dompurify';

function sanitizeHtml(html: string): string {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p'],
    ALLOWED_ATTR: ['href'],
  });
}

// File upload validation
const FileUploadSchema = z.object({
  filename: z.string().regex(/^[a-zA-Z0-9_-]+\.(jpg|jpeg|png|pdf)$/),
  size: z.number().max(5 * 1024 * 1024), // 5MB
  mimetype: z.enum(['image/jpeg', 'image/png', 'application/pdf']),
});
```

### ❌ Bad: No Validation
```typescript
// ❌ No validation
function createUser(input: any) {
  return db.users.create(input);  // Accepts anything!
}

// ❌ Direct HTML injection
function renderComment(comment: string) {
  return <div dangerouslySetInnerHTML={{ __html: comment }} />;  // XSS!
}
```

## Rate Limiting

### ✅ Good: API Rate Limiting
```typescript
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import { Redis } from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

// API rate limiting
const apiLimiter = rateLimit({
  store: new RedisStore({ client: redis }),
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,  // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP',
  standardHeaders: true,
  legacyHeaders: false,
});

// Stricter limits for sensitive endpoints
const authLimiter = rateLimit({
  store: new RedisStore({ client: redis }),
  windowMs: 15 * 60 * 1000,
  max: 5,  // 5 login attempts per 15 minutes
  skipSuccessfulRequests: true,
  message: 'Too many login attempts',
});

// Apply to routes
app.use('/api/', apiLimiter);
app.post('/api/login', authLimiter, loginHandler);

// Next.js middleware rate limiting
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'),
});

export async function middleware(request: Request) {
  const ip = request.headers.get('x-forwarded-for') ?? 'anonymous';
  const { success } = await ratelimit.limit(ip);
  
  if (!success) {
    return new Response('Too Many Requests', { status: 429 });
  }
  
  return NextResponse.next();
}
```

## File Upload Security

### ✅ Good: Secure File Uploads
```typescript
import multer from 'multer';
import path from 'path';
import crypto from 'crypto';

const upload = multer({
  limits: {
    fileSize: 5 * 1024 * 1024,  // 5MB limit
    files: 5,  // Max 5 files
  },
  fileFilter: (req, file, cb) => {
    // Whitelist allowed extensions
    const allowedExtensions = ['.jpg', '.jpeg', '.png', '.pdf'];
    const ext = path.extname(file.originalname).toLowerCase();
    
    if (allowedExtensions.includes(ext)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type'));
    }
  },
  storage: multer.diskStorage({
    destination: 'uploads/',
    filename: (req, file, cb) => {
      // Generate unique, safe filename
      const uniqueSuffix = crypto.randomBytes(16).toString('hex');
      const ext = path.extname(file.originalname);
      cb(null, `${uniqueSuffix}${ext}`);
    },
  }),
});

// Verify file content matches extension
import fileType from 'file-type';

async function verifyFileType(filePath: string) {
  const type = await fileType.fromFile(filePath);
  const ext = path.extname(filePath).toLowerCase();
  
  const allowedTypes = {
    '.jpg': ['image/jpeg'],
    '.jpeg': ['image/jpeg'],
    '.png': ['image/png'],
    '.pdf': ['application/pdf'],
  };
  
  if (!type || !allowedTypes[ext]?.includes(type.mime)) {
    throw new Error('File type mismatch');
  }
}
```

### ❌ Bad: Insecure Uploads
```typescript
// ❌ No validation
const upload = multer({ dest: 'uploads/' });  // No limits or filtering!

// ❌ Using original filename
filename: (req, file, cb) => {
  cb(null, file.originalname);  // Path traversal risk!
}
```

## CORS Configuration

### ✅ Good: Strict CORS
```typescript
// Next.js API route
export async function OPTIONS(request: Request) {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': 'https://trusted-site.com',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      'Access-Control-Max-Age': '86400',
    },
  });
}

// Express CORS
import cors from 'cors';

app.use(cors({
  origin: (origin, callback) => {
    const allowedOrigins = ['https://app.com', 'https://admin.app.com'];
    
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}));
```

### ❌ Bad: Permissive CORS
```typescript
// ❌ Allow all origins
app.use(cors({ origin: '*' })); // Anyone can call your API!

// ❌ Reflecting origin
app.use(cors({ 
  origin: (origin, callback) => callback(null, origin) // Dangerous!
}));
```

---

**Remember: Security is not a feature, it's a process. Stay updated with security advisories, regularly audit dependencies, and always follow the principle of defense in depth.**

**Resources:**
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [MDN Web Security](https://developer.mozilla.org/en-US/docs/Web/Security)
- [CSP Evaluator](https://csp-evaluator.withgoogle.com/)
- [Mozilla Observatory](https://observatory.mozilla.org/)
- [Security Headers](https://securityheaders.com/)
