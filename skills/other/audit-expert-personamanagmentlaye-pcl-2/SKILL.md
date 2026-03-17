---
name: audit-expert
version: 1.0.0
description: Expert-level security auditing, compliance, code review, and vulnerability assessment
category: security
tags: [audit, compliance, security-review, code-review, vulnerability-assessment, soc2, gdpr]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(git:*, grep:*, find:*)
---

# Audit Expert

Expert guidance for security auditing, compliance assessments, code reviews, vulnerability assessments, and regulatory compliance (SOC 2, GDPR, HIPAA, PCI-DSS).

## Core Concepts

### Audit Types
- **Security Audit**: Vulnerability assessment, penetration testing
- **Code Audit**: Code review, static analysis, security patterns
- **Compliance Audit**: SOC 2, GDPR, HIPAA, PCI-DSS, ISO 27001
- **Infrastructure Audit**: Configuration review, access control
- **Process Audit**: SDLC, change management, incident response

### Audit Frameworks
- OWASP ASVS (Application Security Verification Standard)
- NIST Cybersecurity Framework
- CIS Controls
- ISO 27001/27002
- SOC 2 Trust Service Criteria

### Audit Process
1. Planning and scoping
2. Information gathering
3. Vulnerability identification
4. Risk assessment
5. Reporting
6. Remediation tracking
7. Follow-up verification

## Security Code Review

### Authentication Review
```javascript
// ❌ Issues to flag
class AuthService {
  // Issue 1: Weak password requirements
  validatePassword(password) {
    return password.length >= 6; // Too short!
  }

  // Issue 2: Password stored in plaintext
  async createUser(email, password) {
    await db.users.create({ email, password }); // No hashing!
  }

  // Issue 3: Timing attack vulnerability
  async login(email, password) {
    const user = await db.users.findOne({ email });
    if (!user) return null;

    // Direct comparison reveals timing
    if (user.password === password) {
      return user;
    }
    return null;
  }

  // Issue 4: No rate limiting
  // Issue 5: No MFA support
  // Issue 6: Predictable session tokens
  generateSessionToken() {
    return Math.random().toString(36); // Not cryptographically secure!
  }
}

// ✅ Secure implementation
const bcrypt = require('bcrypt');
const crypto = require('crypto');

class SecureAuthService {
  // Strong password validation
  validatePassword(password) {
    const minLength = 12;
    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecial = /[^A-Za-z0-9]/.test(password);

    return password.length >= minLength &&
           hasUppercase && hasLowercase &&
           hasNumber && hasSpecial;
  }

  // Secure password hashing
  async hashPassword(password) {
    const saltRounds = 12;
    return await bcrypt.hash(password, saltRounds);
  }

  async createUser(email, password) {
    if (!this.validatePassword(password)) {
      throw new Error('Password does not meet requirements');
    }

    const passwordHash = await this.hashPassword(password);
    await db.users.create({
      email: email.toLowerCase(),
      passwordHash
    });
  }

  // Constant-time comparison with rate limiting
  async login(email, password) {
    // Check rate limit
    const attempts = await this.getLoginAttempts(email);
    if (attempts > 5) {
      throw new Error('Too many login attempts. Try again later.');
    }

    const user = await db.users.findOne({
      email: email.toLowerCase()
    });

    // Always hash password even if user not found (timing attack prevention)
    const isValid = user ?
      await bcrypt.compare(password, user.passwordHash) :
      await bcrypt.compare(password, '$2b$12$dummyhash');

    if (!user || !isValid) {
      await this.recordFailedAttempt(email);
      throw new Error('Invalid credentials');
    }

    await this.clearLoginAttempts(email);
    return user;
  }

  // Cryptographically secure tokens
  generateSessionToken() {
    return crypto.randomBytes(32).toString('hex');
  }

  // MFA support
  async verifyMFA(user, token) {
    const speakeasy = require('speakeasy');
    return speakeasy.totp.verify({
      secret: user.mfaSecret,
      encoding: 'base32',
      token,
      window: 2
    });
  }
}
```

### SQL Injection Review
```javascript
// Audit checklist for SQL injection:
// 1. Are all queries parameterized?
// 2. Is user input sanitized?
// 3. Are ORM features used correctly?
// 4. Are stored procedures parameterized?

// ❌ Vulnerable patterns to flag
async function searchUsers(name) {
  // Issue: String concatenation
  const query = `SELECT * FROM users WHERE name = '${name}'`;
  return await db.query(query);
}

async function updateUser(id, data) {
  // Issue: Dynamic column names not validated
  const columns = Object.keys(data).join(', ');
  const query = `UPDATE users SET ${columns} WHERE id = ${id}`;
  return await db.query(query);
}

// ❌ ORM misuse
async function findUsers(filters) {
  // Issue: Raw WHERE clause from user input
  return await User.findAll({
    where: db.literal(filters.where)
  });
}

// ✅ Secure patterns
async function searchUsers(name) {
  // Parameterized query
  return await db.query(
    'SELECT * FROM users WHERE name = ?',
    [name]
  );
}

async function updateUser(id, data) {
  // Whitelist allowed columns
  const allowedColumns = ['name', 'email', 'bio'];
  const updates = {};

  for (const [key, value] of Object.entries(data)) {
    if (allowedColumns.includes(key)) {
      updates[key] = value;
    }
  }

  return await User.update(updates, {
    where: { id }
  });
}

async function findUsers(filters) {
  // Use ORM query builder
  return await User.findAll({
    where: {
      name: { [Op.like]: `%${filters.name}%` },
      active: true
    }
  });
}
```

### Authorization Review
```javascript
// Audit checklist:
// 1. Is authentication checked before authorization?
// 2. Are resource ownership checks present?
// 3. Is role-based access control implemented?
// 4. Are there direct object reference vulnerabilities?

// ❌ Insecure patterns
app.delete('/api/posts/:id', authenticate, async (req, res) => {
  // Issue: No authorization check!
  await Post.delete(req.params.id);
  res.status(204).send();
});

app.get('/api/documents/:id', async (req, res) => {
  // Issue: No authentication at all!
  const doc = await Document.findById(req.params.id);
  res.json(doc);
});

// ✅ Secure patterns
const authorize = (resource) => async (req, res, next) => {
  const item = await db[resource].findById(req.params.id);

  if (!item) {
    return res.status(404).json({ error: 'Not found' });
  }

  // Check ownership or admin role
  if (item.userId !== req.user.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  req.resource = item;
  next();
};

app.delete('/api/posts/:id',
  authenticate,
  authorize('posts'),
  async (req, res) => {
    await req.resource.delete();
    res.status(204).send();
  }
);

// Role-based access control
const requireRole = (...roles) => (req, res, next) => {
  if (!req.user || !roles.includes(req.user.role)) {
    return res.status(403).json({ error: 'Insufficient permissions' });
  }
  next();
};

app.post('/api/admin/users',
  authenticate,
  requireRole('admin'),
  async (req, res) => {
    // Admin-only endpoint
  }
);
```

### XSS and Output Encoding Review
```javascript
// Audit checklist:
// 1. Is user input escaped in HTML context?
// 2. Is Content-Security-Policy header set?
// 3. Are dangerous functions (eval, innerHTML) avoided?
// 4. Is templating engine auto-escaping enabled?

// ❌ Vulnerable patterns
app.get('/search', (req, res) => {
  // Issue: No escaping
  res.send(`<h1>Results for: ${req.query.q}</h1>`);
});

app.post('/comment', async (req, res) => {
  // Issue: Storing unsanitized HTML
  await Comment.create({
    text: req.body.comment,
    html: req.body.comment // Dangerous!
  });
});

// Client-side issues
function displayComment(comment) {
  // Issue: Using innerHTML
  document.getElementById('comment').innerHTML = comment;

  // Issue: Using eval
  eval(comment);
}

// ✅ Secure patterns
const escape = require('escape-html');

app.get('/search', (req, res) => {
  res.send(`<h1>Results for: ${escape(req.query.q)}</h1>`);
});

// Or use templating with auto-escape
app.get('/search', (req, res) => {
  res.render('search', { query: req.query.q }); // Auto-escaped
});

// Content Security Policy
app.use((req, res, next) => {
  res.setHeader('Content-Security-Policy',
    "default-src 'self'; " +
    "script-src 'self'; " +
    "style-src 'self' 'unsafe-inline'; " +
    "img-src 'self' data: https:;"
  );
  next();
});

// Client-side: Use textContent
function displayComment(comment) {
  document.getElementById('comment').textContent = comment;
}
```

## Compliance Auditing

### GDPR Compliance Checklist
```javascript
// GDPR Requirements Audit

// 1. Lawful Basis for Processing
// ✓ Explicit consent obtained
// ✓ Purpose clearly stated
// ✓ Option to withdraw consent

// 2. Data Minimization
// Review: Are we collecting only necessary data?
async function createUser(data) {
  // ❌ Collecting too much
  const user = {
    email: data.email,
    password: data.password,
    ssn: data.ssn,              // Unnecessary!
    medicalHistory: data.medical, // Unnecessary!
    location: data.location      // May be unnecessary
  };

  // ✅ Only essential data
  const user = {
    email: data.email,
    passwordHash: await hashPassword(data.password)
  };
}

// 3. Right to Access (Subject Access Request)
app.get('/api/gdpr/data', authenticate, async (req, res) => {
  const userData = {
    personalInfo: await User.findById(req.user.id),
    posts: await Post.findByUserId(req.user.id),
    comments: await Comment.findByUserId(req.user.id),
    loginHistory: await LoginHistory.findByUserId(req.user.id)
  };

  res.json(userData);
});

// 4. Right to Erasure (Right to be Forgotten)
app.delete('/api/gdpr/delete-account', authenticate, async (req, res) => {
  const userId = req.user.id;

  await db.transaction(async (tx) => {
    // Anonymize or delete personal data
    await User.anonymize(userId, tx);
    await Post.anonymizeByUser(userId, tx);
    await Comment.anonymizeByUser(userId, tx);

    // Keep audit logs (legal requirement)
    await AuditLog.create({
      action: 'account_deletion',
      userId,
      timestamp: new Date()
    }, tx);
  });

  res.status(204).send();
});

// 5. Right to Data Portability
app.get('/api/gdpr/export', authenticate, async (req, res) => {
  const data = await exportUserData(req.user.id);

  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Content-Disposition', 'attachment; filename="my-data.json"');
  res.json(data);
});

// 6. Breach Notification (72 hours)
async function handleDataBreach(breach) {
  // Log breach
  await SecurityIncident.create({
    type: 'data_breach',
    severity: breach.severity,
    affectedUsers: breach.userIds.length,
    detectedAt: new Date()
  });

  // Notify authorities within 72 hours if high risk
  if (breach.severity === 'high') {
    await notifyDataProtectionAuthority(breach);
  }

  // Notify affected users
  for (const userId of breach.userIds) {
    await notifyUserOfBreach(userId, breach);
  }
}

// 7. Privacy by Design
// - Encryption at rest and in transit
// - Access controls
// - Audit logging
// - Data retention policies

// 8. Data Processing Agreement
// - Document third-party processors
// - Ensure processor compliance
// - Review contracts
```

### SOC 2 Compliance Audit
```javascript
// SOC 2 Trust Service Criteria

// 1. Security - Access Control
class AccessControlAudit {
  async auditUserAccess() {
    // Review user permissions
    const users = await User.findAll();
    const issues = [];

    for (const user of users) {
      // Check for overprivileged users
      if (user.role === 'admin' && !user.adminJustification) {
        issues.push({
          type: 'excessive_privilege',
          user: user.email,
          message: 'Admin access without justification'
        });
      }

      // Check for inactive users with access
      const daysSinceLogin = daysBetween(user.lastLoginAt, new Date());
      if (daysSinceLogin > 90) {
        issues.push({
          type: 'stale_access',
          user: user.email,
          message: `No login for ${daysSinceLogin} days`
        });
      }
    }

    return issues;
  }

  async auditAPIKeys() {
    const apiKeys = await APIKey.findAll();
    const issues = [];

    for (const key of apiKeys) {
      // Check for keys without expiration
      if (!key.expiresAt) {
        issues.push({
          type: 'no_expiration',
          keyId: key.id,
          message: 'API key has no expiration'
        });
      }

      // Check for unused keys
      if (!key.lastUsedAt ||
          daysBetween(key.lastUsedAt, new Date()) > 90) {
        issues.push({
          type: 'unused_key',
          keyId: key.id,
          message: 'API key not used in 90 days'
        });
      }
    }

    return issues;
  }
}

// 2. Availability - Monitoring
class AvailabilityAudit {
  async auditMonitoring() {
    const checks = [
      { name: 'Health checks configured', check: this.hasHealthChecks },
      { name: 'Uptime monitoring active', check: this.hasUptimeMonitoring },
      { name: 'Alert policies defined', check: this.hasAlertPolicies },
      { name: 'On-call rotation configured', check: this.hasOnCallRotation },
      { name: 'Backup systems tested', check: this.hasBackupTesting }
    ];

    const results = await Promise.all(
      checks.map(async (check) => ({
        name: check.name,
        passed: await check.check()
      }))
    );

    return results;
  }
}

// 3. Processing Integrity - Data Validation
class ProcessingIntegrityAudit {
  async auditDataValidation() {
    // Review all API endpoints for input validation
    const endpoints = [
      { path: '/api/users', method: 'POST' },
      { path: '/api/posts', method: 'POST' },
      // ... all endpoints
    ];

    const issues = [];

    for (const endpoint of endpoints) {
      const hasValidation = await this.checkValidation(endpoint);
      if (!hasValidation) {
        issues.push({
          endpoint: `${endpoint.method} ${endpoint.path}`,
          message: 'Missing input validation'
        });
      }
    }

    return issues;
  }
}

// 4. Confidentiality - Encryption Audit
class ConfidentialityAudit {
  async auditEncryption() {
    const issues = [];

    // Check encryption at rest
    const tables = await this.getDatabaseTables();
    for (const table of tables) {
      if (table.containsSensitiveData && !table.encrypted) {
        issues.push({
          type: 'encryption_at_rest',
          table: table.name,
          message: 'Sensitive data not encrypted'
        });
      }
    }

    // Check TLS configuration
    const tlsConfig = await this.getTLSConfig();
    if (tlsConfig.version < '1.2') {
      issues.push({
        type: 'weak_tls',
        message: 'TLS version below 1.2'
      });
    }

    // Check for hardcoded secrets
    const secrets = await this.scanForHardcodedSecrets();
    if (secrets.length > 0) {
      issues.push({
        type: 'hardcoded_secrets',
        count: secrets.length,
        message: 'Found hardcoded secrets in code'
      });
    }

    return issues;
  }
}

// 5. Privacy - Data Retention
class PrivacyAudit {
  async auditDataRetention() {
    // Check for data retention policies
    const policies = await DataRetentionPolicy.findAll();
    const issues = [];

    if (policies.length === 0) {
      issues.push({
        type: 'no_retention_policy',
        message: 'No data retention policies defined'
      });
    }

    // Check for old data
    const oldRecords = await this.findOldRecords();
    for (const record of oldRecords) {
      issues.push({
        type: 'old_data',
        table: record.table,
        count: record.count,
        message: `${record.count} records older than retention period`
      });
    }

    return issues;
  }
}
```

### PCI-DSS Compliance
```javascript
// PCI-DSS Requirements for Payment Card Data

// 1. Never store sensitive authentication data after authorization
// ❌ Don't store:
// - Full magnetic stripe data
// - CVV2/CVC2/CID
// - PIN/PIN blocks

// ✅ Can store (encrypted):
// - Primary Account Number (PAN)
// - Cardholder name
// - Expiration date
// - Service code

class PCICompliantPayment {
  async processPayment(cardData) {
    // ❌ Never log card data
    // console.log('Processing card:', cardData); // VIOLATION!

    // ✅ Use payment processor (tokenization)
    const token = await stripe.tokens.create({
      card: {
        number: cardData.number,
        exp_month: cardData.expMonth,
        exp_year: cardData.expYear,
        cvc: cardData.cvc
      }
    });

    // Store only token, not actual card data
    await Payment.create({
      userId: cardData.userId,
      amount: cardData.amount,
      stripeToken: token.id,
      last4: cardData.number.slice(-4), // OK to store
      // ❌ Don't store: cardNumber, cvv, etc.
    });

    const charge = await stripe.charges.create({
      amount: cardData.amount,
      currency: 'usd',
      source: token.id
    });

    return charge;
  }

  async auditCardDataStorage() {
    // Scan database for potential card data
    const suspiciousColumns = [
      'card_number', 'cvv', 'pin', 'magnetic_stripe'
    ];

    const issues = [];
    const tables = await this.getDatabaseTables();

    for (const table of tables) {
      for (const column of table.columns) {
        if (suspiciousColumns.includes(column.name.toLowerCase())) {
          issues.push({
            type: 'potential_card_data_storage',
            table: table.name,
            column: column.name,
            message: 'Possible storage of prohibited card data'
          });
        }
      }
    }

    return issues;
  }
}

// 2. Mask PAN when displayed
function maskCardNumber(pan) {
  // Show only last 4 digits
  return `****-****-****-${pan.slice(-4)}`;
}

// 3. Encryption of cardholder data
// - Use strong cryptography (AES-256)
// - Secure key management
// - Keys separate from data
```

## Audit Reporting

### Security Audit Report Template
```javascript
class SecurityAuditReport {
  constructor() {
    this.findings = [];
    this.summary = {
      critical: 0,
      high: 0,
      medium: 0,
      low: 0,
      info: 0
    };
  }

  addFinding(finding) {
    this.findings.push({
      id: this.findings.length + 1,
      severity: finding.severity,
      title: finding.title,
      description: finding.description,
      location: finding.location,
      recommendation: finding.recommendation,
      references: finding.references || [],
      cvssScore: finding.cvssScore,
      status: 'open',
      discoveredAt: new Date()
    });

    this.summary[finding.severity]++;
  }

  generateReport() {
    return {
      reportDate: new Date(),
      auditor: 'Security Team',
      scope: this.scope,
      summary: this.summary,
      findings: this.findings.sort((a, b) =>
        this.severityWeight(b.severity) - this.severityWeight(a.severity)
      ),
      recommendations: this.generateRecommendations()
    };
  }

  severityWeight(severity) {
    const weights = { critical: 5, high: 4, medium: 3, low: 2, info: 1 };
    return weights[severity] || 0;
  }

  generateRecommendations() {
    return [
      'Address all critical and high severity findings immediately',
      'Implement security code review process',
      'Conduct regular penetration testing',
      'Provide security training for developers',
      'Establish vulnerability disclosure program'
    ];
  }
}

// Usage
const audit = new SecurityAuditReport();

audit.addFinding({
  severity: 'critical',
  title: 'SQL Injection in User Search',
  description: 'User search endpoint concatenates user input into SQL query',
  location: 'src/controllers/users.js:45',
  recommendation: 'Use parameterized queries or ORM with proper escaping',
  references: ['CWE-89', 'OWASP A03:2021'],
  cvssScore: 9.8
});

const report = audit.generateReport();
```

## Best Practices

### Audit Preparation
1. Define scope and objectives
2. Gather documentation
3. Review previous audit findings
4. Prepare audit checklist
5. Schedule with stakeholders

### During Audit
1. Follow systematic approach
2. Document all findings
3. Collect evidence
4. Maintain objectivity
5. Communicate preliminary findings

### Post-Audit
1. Prepare detailed report
2. Present findings to stakeholders
3. Develop remediation plan
4. Track remediation progress
5. Schedule follow-up audit

## Anti-Patterns to Avoid

❌ **Auditing own code**: Use independent reviewers
❌ **Incomplete scope**: Define clear boundaries
❌ **No follow-up**: Track remediation to completion
❌ **Generic findings**: Provide specific, actionable recommendations
❌ **Ignoring context**: Consider business requirements
❌ **No prioritization**: Rank findings by risk and impact

## Resources

- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- NIST Framework: https://www.nist.gov/cyberframework
- CIS Controls: https://www.cisecurity.org/controls/
- SOC 2: https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/aicpasoc2report.html
- GDPR: https://gdpr.eu/
- PCI-DSS: https://www.pcisecuritystandards.org/
