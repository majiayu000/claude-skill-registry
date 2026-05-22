---
name: security-first
description: "Universal security checklist and fixes for ANY project type or language"
---

# Security First - Shield Your Code

## 🎯 When to Use This Skill

Use BEFORE:
- Deploying to production
- Handling sensitive data
- Opening API endpoints
- Processing user input
- Storing passwords
- Accepting file uploads
- Going live with payments

## ⚡ 5-Minute Security Audit

### WITH MCP (Security Scanner):
```
"Run complete security audit on my codebase"
"Find and fix all OWASP Top 10 vulnerabilities"
```

### WITHOUT MCP - Quick Scan:

```bash
# 1. Find hardcoded secrets (CRITICAL!)
grep -r "password\|secret\|token\|api[_-]key" --include="*.js" --include="*.env" | grep -v ".example"

# 2. Check for SQL injection
grep -r "query.*\+\|query.*\$\{" --include="*.js"

# 3. Find eval/exec usage
grep -r "eval(\|exec(\|Function(" --include="*.js"

# 4. Check dependencies
npm audit  # or pip check, bundle audit

# 5. Find unvalidated input
grep -r "req.body\|req.query\|req.params" --include="*.js" | grep -v "validate\|sanitize"
```

## 🛡️ OWASP Top 10 Checklist (2024)

### 1. Injection (SQL, NoSQL, Command) 💉

**Vulnerable Code:**
```javascript
// ❌ NEVER DO THIS
const query = `SELECT * FROM users WHERE id = ${req.params.id}`;
db.query(query);  // SQL Injection!

// ❌ Command injection
exec(`ping ${userInput}`);  // Dangerous!
```

**Secure Code:**
```javascript
// ✅ Parameterized queries
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [req.params.id]);

// ✅ For MongoDB
User.findOne({ _id: sanitize(req.params.id) });

// ✅ Command execution
const { spawn } = require('child_process');
spawn('ping', [userInput], { shell: false });
```

### 2. Broken Authentication 🔐

**Security Checklist:**
```javascript
// ✅ Strong password requirements
function validatePassword(password) {
  const requirements = {
    minLength: 12,
    hasUpperCase: /[A-Z]/.test(password),
    hasLowerCase: /[a-z]/.test(password),
    hasNumbers: /\d/.test(password),
    hasSpecialChar: /[!@#$%^&*]/.test(password),
    notCommon: !commonPasswords.includes(password)
  };

  return Object.values(requirements).every(req => req);
}

// ✅ Secure session management
app.use(session({
  secret: process.env.SESSION_SECRET,  // From environment
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,      // HTTPS only
    httpOnly: true,    // No JS access
    maxAge: 3600000,   // 1 hour
    sameSite: 'strict' // CSRF protection
  }
}));

// ✅ Rate limiting
const rateLimit = require('express-rate-limit');
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 5,  // 5 attempts
  message: 'Too many login attempts'
});
app.post('/login', loginLimiter, loginHandler);
```

### 3. Sensitive Data Exposure 🔒

**Never Store in Code:**
```javascript
// ❌ WRONG
const API_KEY = "sk_live_abcd1234";
const DB_PASSWORD = "admin123";

// ✅ CORRECT - Use environment variables
const API_KEY = process.env.API_KEY;
const DB_PASSWORD = process.env.DB_PASSWORD;

// ✅ Use .env file (never commit!)
require('dotenv').config();

// ✅ Encrypt sensitive data at rest
const crypto = require('crypto');
const algorithm = 'aes-256-gcm';

function encrypt(text) {
  const key = Buffer.from(process.env.ENCRYPTION_KEY, 'hex');
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(algorithm, key, iv);

  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');

  const authTag = cipher.getAuthTag();

  return {
    encrypted,
    iv: iv.toString('hex'),
    authTag: authTag.toString('hex')
  };
}
```

### 4. XML External Entities (XXE) 📄

```javascript
// ❌ Vulnerable XML parsing
const libxmljs = require('libxmljs');
const doc = libxmljs.parseXml(userInput);  // XXE vulnerable!

// ✅ Safe XML parsing
const parser = new DOMParser();
const doc = parser.parseFromString(userInput, 'text/xml');

// ✅ Or disable external entities
const options = {
  xmlMode: true,
  recognizeSelfClosing: true,
  decodeEntities: false  // Disable entity expansion
};
```

### 5. Broken Access Control 🚪

```javascript
// ❌ No authorization check
app.get('/api/user/:id', (req, res) => {
  const user = User.findById(req.params.id);
  res.json(user);  // Anyone can see any user!
});

// ✅ Proper authorization
app.get('/api/user/:id', authenticate, (req, res) => {
  // Check if user can access this resource
  if (req.user.id !== req.params.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  const user = User.findById(req.params.id);
  res.json(user);
});

// ✅ Role-based access control (RBAC)
const authorize = (roles) => {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
};

app.delete('/api/users/:id', authenticate, authorize(['admin']), deleteUser);
```

### 6. Security Misconfiguration ⚙️

```bash
# ✅ Security headers
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
}));

# ✅ Disable unnecessary features
app.disable('x-powered-by');  # Hide Express

# ✅ Error handling (don't leak info)
app.use((err, req, res, next) => {
  console.error(err.stack);  // Log full error

  // Send generic message to client
  res.status(500).json({
    error: 'Internal server error',
    // Don't send: err.stack or err.message
  });
});
```

### 7. Cross-Site Scripting (XSS) 🎭

```javascript
// ❌ Vulnerable to XSS
app.get('/search', (req, res) => {
  res.send(`Results for: ${req.query.q}`);  // XSS!
});

// ✅ Sanitize output
const DOMPurify = require('isomorphic-dompurify');

app.get('/search', (req, res) => {
  const clean = DOMPurify.sanitize(req.query.q);
  res.send(`Results for: ${clean}`);
});

// ✅ React automatically escapes
<div>{userInput}</div>  // Safe

// ❌ But dangerouslySetInnerHTML is dangerous
<div dangerouslySetInnerHTML={{__html: userInput}} />  // XSS!

// ✅ Content-Type headers
res.set('Content-Type', 'text/plain');  // Not HTML
res.set('X-Content-Type-Options', 'nosniff');
```

### 8. Insecure Deserialization 📦

```javascript
// ❌ Dangerous deserialization
const userData = JSON.parse(req.body.data);
eval(userData.code);  // Code execution!

// ✅ Validate before deserializing
const schema = Joi.object({
  name: Joi.string().required(),
  age: Joi.number().min(0).max(120)
});

const { error, value } = schema.validate(JSON.parse(req.body.data));
if (error) return res.status(400).json({ error });

// ✅ Never deserialize untrusted data into code
// Use JSON.parse() only, never eval() or Function()
```

### 9. Components with Known Vulnerabilities 📚

```bash
# ✅ Regular dependency checks
# Add to package.json
{
  "scripts": {
    "security": "npm audit && npm outdated",
    "security:fix": "npm audit fix",
    "preinstall": "npm audit"
  }
}

# ✅ Automated updates (GitHub)
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 10
```

### 10. Insufficient Logging & Monitoring 📊

```javascript
// ✅ Comprehensive logging
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});

// ✅ Log security events
function logSecurityEvent(event, user, details) {
  logger.warn({
    type: 'SECURITY',
    event,
    user: user?.id,
    ip: user?.ip,
    timestamp: new Date().toISOString(),
    details
  });
}

// Usage
logSecurityEvent('FAILED_LOGIN', req.user, {
  attempts: failedAttempts,
  ip: req.ip
});

logSecurityEvent('UNAUTHORIZED_ACCESS', req.user, {
  resource: req.path,
  method: req.method
});
```

## 🔐 Password Security

```javascript
// ✅ NEVER store plain text passwords!
const bcrypt = require('bcrypt');

// Hashing
async function hashPassword(password) {
  const saltRounds = 12;  // Higher = more secure but slower
  return await bcrypt.hash(password, saltRounds);
}

// Verifying
async function verifyPassword(password, hash) {
  return await bcrypt.compare(password, hash);
}

// ✅ Password reset flow
async function resetPassword(email) {
  // 1. Generate secure token
  const token = crypto.randomBytes(32).toString('hex');

  // 2. Store hashed token with expiry
  await storeResetToken(email, hashToken(token), Date.now() + 3600000);

  // 3. Send unhashed token via email
  await sendEmail(email, `Reset link: ${BASE_URL}/reset?token=${token}`);
}
```

## 🚪 API Security

```javascript
// ✅ API Security Checklist
const apiSecurity = {
  // 1. Authentication
  authentication: 'Bearer token (JWT)',

  // 2. Rate limiting
  rateLimit: {
    windowMs: 15 * 60 * 1000,  // 15 minutes
    max: 100  // requests per window
  },

  // 3. Input validation
  validateInput: (data, schema) => {
    return Joi.validate(data, schema);
  },

  // 4. CORS configuration
  cors: {
    origin: process.env.ALLOWED_ORIGINS?.split(',') || false,
    credentials: true
  },

  // 5. API versioning
  versioning: '/api/v1/',

  // 6. Request size limit
  bodyLimit: '10mb',

  // 7. Timeout
  timeout: 30000,  // 30 seconds

  // 8. HTTPS only
  httpsOnly: true
};
```

## 📋 Security Deployment Checklist

```markdown
## Pre-Deployment Security Checklist

### Code Security
- [ ] No hardcoded secrets
- [ ] All inputs validated
- [ ] SQL queries parameterized
- [ ] XSS protection enabled
- [ ] CSRF tokens implemented
- [ ] Authentication required
- [ ] Authorization checks present
- [ ] Rate limiting configured

### Dependencies
- [ ] `npm audit` shows 0 vulnerabilities
- [ ] All packages from trusted sources
- [ ] Lock file committed
- [ ] Licenses reviewed

### Configuration
- [ ] Environment variables used
- [ ] HTTPS enforced
- [ ] Security headers set
- [ ] CORS configured
- [ ] Error messages sanitized
- [ ] Debug mode disabled
- [ ] Source maps disabled in production

### Data Protection
- [ ] Passwords hashed (bcrypt)
- [ ] Sensitive data encrypted
- [ ] PII fields marked
- [ ] Data retention policy set
- [ ] Backups encrypted

### Infrastructure
- [ ] Firewall rules configured
- [ ] Ports minimized
- [ ] SSH keys only (no passwords)
- [ ] Monitoring enabled
- [ ] Logging configured
- [ ] Incident response plan ready
```

## 🚨 Incident Response Plan

```javascript
// security-incident.js
class SecurityIncident {
  async respond(incident) {
    // 1. Detect
    this.log('INCIDENT_DETECTED', incident);

    // 2. Contain
    await this.blockIP(incident.sourceIP);
    await this.disableAccount(incident.userId);

    // 3. Investigate
    const logs = await this.gatherLogs(incident);

    // 4. Remediate
    await this.patchVulnerability(incident.vulnerability);

    // 5. Recover
    await this.restoreService();

    // 6. Lessons Learned
    await this.documentIncident(incident);

    // 7. Notify
    await this.notifyStakeholders(incident);
  }
}
```

## 💡 Security Quick Wins

```bash
# 1. Add security.txt
echo "Contact: security@example.com" > public/.well-known/security.txt

# 2. Enable Dependabot
gh api repos/:owner/:repo --method PUT --field security_and_analysis[secret_scanning][status]=enabled

# 3. Add pre-commit hooks
npm install --save-dev husky
npx husky add .husky/pre-commit "npm audit"

# 4. Security headers test
curl -I https://yoursite.com | grep -i "strict-transport\|content-security\|x-frame"
```

Remember: Security is not a feature, it's a requirement! 🛡️