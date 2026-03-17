---
name: multi-tenant
description: Multi-tenant architecture patterns including org_id claim management, JWT token structure with organization context, database isolation strategies for MongoDB and PostgreSQL, theme switching per organization, tenant provisioning workflows, data isolation patterns, and cross-tenant security. Activate for multi-tenancy implementation, tenant isolation, and organization-scoped data access.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - WebFetch
  - WebSearch
dependencies:
  - authentication
  - database
  - keycloak-admin
triggers:
  - multi-tenant
  - tenant
  - org_id
  - organization
  - isolation
  - tenant provisioning
  - data isolation
---

# Multi-Tenant Architecture Skill

Comprehensive multi-tenant architecture patterns for the keycloak-alpha platform with organization-based isolation.

## When to Use This Skill

Activate this skill when:
- Implementing multi-tenant architecture with org_id claims
- Setting up database isolation strategies
- Configuring per-organization themes
- Building tenant provisioning workflows
- Ensuring data isolation and security
- Implementing cross-tenant access controls
- Managing organization-scoped resources

## Multi-Tenant Architecture Overview

The keycloak-alpha platform uses **shared database, isolated schema** approach with org_id-based isolation:

```
┌─────────────────────────────────────────────┐
│          Keycloak (Identity Provider)        │
│  - Manages users across all organizations   │
│  - Issues JWT tokens with org_id claim      │
│  - Handles authentication & SSO             │
└─────────────────────────────────────────────┘
                    ↓ JWT with org_id
┌─────────────────────────────────────────────┐
│            API Gateway                       │
│  - Validates tokens                         │
│  - Extracts org_id claim                    │
│  - Routes to microservices                  │
└─────────────────────────────────────────────┘
                    ↓ org_id in headers
┌─────────────────────────────────────────────┐
│         Microservices (8 services)          │
│  - Enforce org_id filtering                 │
│  - Isolate data by organization             │
│  - Apply org-specific business logic        │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│    MongoDB / PostgreSQL                     │
│  - Shared database                          │
│  - org_id indexed on all collections/tables │
│  - Row-level security (PostgreSQL)          │
└─────────────────────────────────────────────┘
```

## JWT Token Structure with Organization Context

### Token Claims

```json
{
  "sub": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "email": "john.doe@acme.com",
  "name": "John Doe",
  "given_name": "John",
  "family_name": "Doe",
  "org_id": "org_acme",
  "org_name": "ACME Corporation",
  "realm_access": {
    "roles": ["org_admin", "user"]
  },
  "resource_access": {
    "lobbi-web-app": {
      "roles": ["user"]
    }
  },
  "email_verified": true,
  "preferred_username": "john.doe@acme.com",
  "iss": "http://localhost:8080/realms/lobbi",
  "aud": "account",
  "exp": 1702000000,
  "iat": 1701999700,
  "jti": "unique-token-id"
}
```

### Configure org_id Claim Mapper

```bash
# Add protocol mapper to include org_id in tokens
TOKEN=$(curl -X POST "http://localhost:8080/realms/master/protocol/openid-connect/token" \
  -d "username=admin&password=admin&grant_type=password&client_id=admin-cli" \
  | jq -r '.access_token')

CLIENT_UUID=$(curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8080/admin/realms/lobbi/clients?clientId=lobbi-web-app" \
  | jq -r '.[0].id')

curl -X POST "http://localhost:8080/admin/realms/lobbi/clients/$CLIENT_UUID/protocol-mappers/models" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "org_id_mapper",
    "protocol": "openid-connect",
    "protocolMapper": "oidc-usermodel-attribute-mapper",
    "config": {
      "user.attribute": "org_id",
      "claim.name": "org_id",
      "jsonType.label": "String",
      "id.token.claim": "true",
      "access.token.claim": "true",
      "userinfo.token.claim": "true"
    }
  }'

curl -X POST "http://localhost:8080/admin/realms/lobbi/clients/$CLIENT_UUID/protocol-mappers/models" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "org_name_mapper",
    "protocol": "openid-connect",
    "protocolMapper": "oidc-usermodel-attribute-mapper",
    "config": {
      "user.attribute": "org_name",
      "claim.name": "org_name",
      "jsonType.label": "String",
      "id.token.claim": "true",
      "access.token.claim": "true",
      "userinfo.token.claim": "false"
    }
  }'
```

### Token Verification Middleware

```javascript
// services/api-gateway/src/middleware/auth.js
import jwt from 'jsonwebtoken';
import jwksClient from 'jwks-rsa';
import { UnauthorizedError, ForbiddenError } from '../utils/AppError.js';

const client = jwksClient({
  jwksUri: `${process.env.KEYCLOAK_URL}/realms/${process.env.KEYCLOAK_REALM}/protocol/openid-connect/certs`,
  cache: true,
  rateLimit: true,
  jwksRequestsPerMinute: 10
});

function getKey(header, callback) {
  client.getSigningKey(header.kid, (err, key) => {
    const signingKey = key.publicKey || key.rsaPublicKey;
    callback(null, signingKey);
  });
}

export async function authMiddleware(req, res, next) {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return next(new UnauthorizedError('No token provided'));
  }

  jwt.verify(token, getKey, {
    audience: 'account',
    issuer: `${process.env.KEYCLOAK_URL}/realms/${process.env.KEYCLOAK_REALM}`,
    algorithms: ['RS256']
  }, (err, decoded) => {
    if (err) {
      return next(new UnauthorizedError('Invalid token'));
    }

    // CRITICAL: Verify org_id claim exists
    if (!decoded.org_id) {
      return next(new ForbiddenError('Missing org_id claim in token'));
    }

    // Attach user context to request
    req.user = {
      sub: decoded.sub,
      email: decoded.email,
      name: decoded.name,
      orgId: decoded.org_id,
      orgName: decoded.org_name,
      roles: decoded.realm_access?.roles || []
    };

    next();
  });
}

// Optional: Verify org_id matches resource being accessed
export function requireOrgAccess(req, res, next) {
  const resourceOrgId = req.params.orgId || req.query.org_id || req.body.org_id;

  if (resourceOrgId && resourceOrgId !== req.user.orgId) {
    // Allow super_admin to access any org
    if (!req.user.roles.includes('super_admin')) {
      return next(new ForbiddenError('Cannot access resources from different organization'));
    }
  }

  next();
}
```

## Database Isolation Strategies

### MongoDB Isolation with org_id

```javascript
// services/user-service/src/models/User.js
import mongoose from 'mongoose';

const userSchema = new mongoose.Schema({
  keycloakId: {
    type: String,
    required: true,
    unique: true,
    index: true
  },
  email: {
    type: String,
    required: true,
    lowercase: true,
    trim: true
  },
  org_id: {
    type: String,
    required: true,
    index: true  // CRITICAL: Always index org_id
  },
  firstName: String,
  lastName: String,
  metadata: {
    type: Map,
    of: String
  }
}, {
  timestamps: true
});

// CRITICAL: Compound index for org-scoped queries
userSchema.index({ org_id: 1, email: 1 }, { unique: true });
userSchema.index({ org_id: 1, createdAt: -1 });

// Pre-query hook to enforce org_id filtering
userSchema.pre(/^find/, function(next) {
  // Only enforce if org_id is not already in query
  if (!this.getQuery().org_id && this.options.orgId) {
    this.where({ org_id: this.options.orgId });
  }
  next();
});

export const UserModel = mongoose.model('User', userSchema);
```

### Repository Pattern with org_id Isolation

```javascript
// services/user-service/src/repositories/user.repository.js
import { UserModel } from '../models/User.js';
import { ForbiddenError, NotFoundError } from '../utils/AppError.js';

export class UserRepository {

  constructor(orgId) {
    this.orgId = orgId;
  }

  async findAll(filter = {}, options = {}) {
    // ALWAYS enforce org_id filtering
    const query = {
      ...filter,
      org_id: this.orgId
    };

    const { page = 1, limit = 20, sort = { createdAt: -1 } } = options;

    const users = await UserModel.find(query)
      .select('-password')
      .limit(limit)
      .skip((page - 1) * limit)
      .sort(sort);

    const total = await UserModel.countDocuments(query);

    return {
      data: users,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit)
      }
    };
  }

  async findById(id) {
    const user = await UserModel.findOne({
      _id: id,
      org_id: this.orgId  // CRITICAL: Always filter by org_id
    }).select('-password');

    if (!user) {
      throw new NotFoundError('User');
    }

    return user;
  }

  async create(userData) {
    const user = new UserModel({
      ...userData,
      org_id: this.orgId  // CRITICAL: Always set org_id
    });

    await user.save();
    return user;
  }

  async update(id, updates) {
    // Prevent changing org_id
    delete updates.org_id;

    const user = await UserModel.findOneAndUpdate(
      { _id: id, org_id: this.orgId },  // CRITICAL: Filter by org_id
      updates,
      { new: true, runValidators: true }
    ).select('-password');

    if (!user) {
      throw new NotFoundError('User');
    }

    return user;
  }

  async delete(id) {
    const result = await UserModel.deleteOne({
      _id: id,
      org_id: this.orgId  // CRITICAL: Filter by org_id
    });

    if (result.deletedCount === 0) {
      throw new NotFoundError('User');
    }

    return true;
  }
}

// Usage in controller
export async function listUsers(req, res, next) {
  try {
    const repository = new UserRepository(req.user.orgId);
    const result = await repository.findAll(
      { status: 'active' },
      { page: req.query.page, limit: req.query.limit }
    );

    res.json(result);
  } catch (error) {
    next(error);
  }
}
```

### PostgreSQL Row-Level Security

```sql
-- services/billing-service/migrations/001_create_subscriptions.sql

-- Enable row-level security
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

-- Create policy for org isolation
CREATE POLICY org_isolation ON subscriptions
  USING (org_id = current_setting('app.current_org_id')::text);

-- Grant access to application role
GRANT SELECT, INSERT, UPDATE, DELETE ON subscriptions TO app_user;

-- Function to set org context
CREATE OR REPLACE FUNCTION set_org_context(p_org_id text)
RETURNS void AS $$
BEGIN
  PERFORM set_config('app.current_org_id', p_org_id, false);
END;
$$ LANGUAGE plpgsql;
```

```javascript
// services/billing-service/src/config/postgres.js
import { Pool } from 'pg';

export class PostgresClient {

  constructor() {
    this.pool = new Pool({
      host: process.env.POSTGRES_HOST,
      port: process.env.POSTGRES_PORT,
      database: process.env.POSTGRES_DB,
      user: process.env.POSTGRES_USER,
      password: process.env.POSTGRES_PASSWORD,
      max: 20,
      idleTimeoutMillis: 30000
    });
  }

  async query(orgId, text, params) {
    const client = await this.pool.connect();

    try {
      // Set org context for row-level security
      await client.query('SELECT set_org_context($1)', [orgId]);

      // Execute query (RLS automatically filters by org_id)
      const result = await client.query(text, params);

      return result;
    } finally {
      client.release();
    }
  }
}

// Usage
const db = new PostgresClient();

export async function getSubscription(req, res, next) {
  try {
    const result = await db.query(
      req.user.orgId,
      'SELECT * FROM subscriptions WHERE id = $1',
      [req.params.id]
    );

    if (result.rows.length === 0) {
      throw new NotFoundError('Subscription');
    }

    res.json(result.rows[0]);
  } catch (error) {
    next(error);
  }
}
```

## Theme Switching Per Organization

### Theme Mapping Configuration

```javascript
// services/keycloak-service/src/config/theme-mapping.js
export const themeMapping = {
  // Organization ID -> Theme name mapping
  org_acme: 'acme-custom',
  org_beta: 'beta-theme',
  org_gamma: 'gamma-dark',

  // Default theme for organizations without custom theme
  default: 'lobbi-base'
};

export function getThemeForOrg(orgId) {
  return themeMapping[orgId] || themeMapping.default;
}

export function getAllThemes() {
  const themes = new Set(Object.values(themeMapping));
  return Array.from(themes);
}
```

### Dynamic Theme Application

```javascript
// services/api-gateway/src/middleware/theme-redirect.js
import { getThemeForOrg } from '../config/theme-mapping.js';

export function themeRedirectMiddleware(req, res, next) {
  // Extract org_id from token or session
  const orgId = req.user?.orgId;

  if (!orgId) {
    return next();
  }

  // Get theme for organization
  const theme = getThemeForOrg(orgId);

  // If redirecting to Keycloak login, add theme parameter
  if (req.path.includes('/auth') || req.path.includes('/login')) {
    const keycloakUrl = new URL(process.env.KEYCLOAK_URL);
    keycloakUrl.pathname = `/realms/${process.env.KEYCLOAK_REALM}/protocol/openid-connect/auth`;

    keycloakUrl.searchParams.set('client_id', 'lobbi-web-app');
    keycloakUrl.searchParams.set('redirect_uri', req.query.redirect_uri);
    keycloakUrl.searchParams.set('response_type', 'code');
    keycloakUrl.searchParams.set('scope', 'openid profile email');
    keycloakUrl.searchParams.set('kc_theme', theme);  // Apply theme

    return res.redirect(keycloakUrl.toString());
  }

  // Store theme in session for frontend
  req.session.theme = theme;
  next();
}
```

### Frontend Theme Consumption

```javascript
// apps/web-app/src/contexts/ThemeContext.jsx
import { createContext, useContext, useState, useEffect } from 'react';
import { useAuth } from '@hooks/useAuth';
import { getThemeForOrg } from '@/api/theme';

const ThemeContext = createContext(null);

export function ThemeProvider({ children }) {
  const { user } = useAuth();
  const [theme, setTheme] = useState('lobbi-base');
  const [themeConfig, setThemeConfig] = useState(null);

  useEffect(() => {
    if (user?.orgId) {
      loadTheme(user.orgId);
    }
  }, [user?.orgId]);

  async function loadTheme(orgId) {
    try {
      const config = await getThemeForOrg(orgId);
      setTheme(config.name);
      setThemeConfig(config);

      // Apply CSS variables
      if (config.branding) {
        document.documentElement.style.setProperty('--primary-color', config.branding.primaryColor);
        document.documentElement.style.setProperty('--secondary-color', config.branding.secondaryColor);
      }
    } catch (error) {
      console.error('Failed to load theme:', error);
    }
  }

  return (
    <ThemeContext.Provider value={{ theme, themeConfig }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => useContext(ThemeContext);
```

## Tenant Provisioning Workflow

### Organization Creation Service

```javascript
// services/org-service/src/services/provisioning.service.js
import { OrganizationModel } from '../models/Organization.js';
import { KeycloakService } from './keycloak.service.js';
import { DatabaseService } from './database.service.js';
import { ThemeService } from './theme.service.js';
import { BillingService } from './billing.service.js';

export class ProvisioningService {

  async provisionOrganization(data) {
    const {
      name,
      domain,
      adminEmail,
      adminFirstName,
      adminLastName,
      plan = 'free'
    } = data;

    // Generate org_id
    const orgId = `org_${domain.replace(/[^a-z0-9]/gi, '_').toLowerCase()}`;

    try {
      // 1. Create organization in database
      const org = await this.createOrganization({
        orgId,
        name,
        domain,
        plan
      });

      // 2. Create Keycloak group for organization
      const keycloakService = new KeycloakService();
      const groupId = await keycloakService.createOrganizationGroup(orgId, name);

      // 3. Create admin user in Keycloak
      const adminUserId = await keycloakService.createUser({
        email: adminEmail,
        firstName: adminFirstName,
        lastName: adminLastName,
        orgId,
        roles: ['org_admin']
      });

      // 4. Add user to organization group
      await keycloakService.addUserToGroup(adminUserId, groupId);

      // 5. Initialize database schemas/collections
      const databaseService = new DatabaseService();
      await databaseService.initializeOrgCollections(orgId);

      // 6. Set up default theme
      const themeService = new ThemeService();
      await themeService.createOrgTheme(orgId, {
        parent: 'lobbi-base',
        branding: {
          logoUrl: null,
          primaryColor: '#3182ce',
          secondaryColor: '#805ad5'
        }
      });

      // 7. Create billing customer (if not free plan)
      if (plan !== 'free') {
        const billingService = new BillingService();
        await billingService.createCustomer({
          orgId,
          email: adminEmail,
          name,
          plan
        });
      }

      // 8. Send welcome email
      await this.sendWelcomeEmail(adminEmail, {
        orgName: name,
        loginUrl: process.env.APP_URL
      });

      return {
        orgId,
        organizationId: org._id,
        adminUserId,
        message: 'Organization provisioned successfully'
      };

    } catch (error) {
      // Rollback on failure
      await this.rollbackProvisioning(orgId);
      throw error;
    }
  }

  async createOrganization(data) {
    const org = new OrganizationModel({
      org_id: data.orgId,
      name: data.name,
      domain: data.domain,
      settings: {
        theme: 'lobbi-base',
        features: new Map([
          ['sso', data.plan !== 'free'],
          ['advanced_analytics', data.plan === 'enterprise'],
          ['custom_branding', data.plan !== 'free']
        ])
      },
      subscription: {
        plan: data.plan,
        status: 'active',
        billingCycle: 'monthly'
      },
      status: 'active'
    });

    await org.save();
    return org;
  }

  async rollbackProvisioning(orgId) {
    console.error(`Rolling back provisioning for ${orgId}`);

    try {
      // Delete organization from database
      await OrganizationModel.deleteOne({ org_id: orgId });

      // Delete Keycloak group and users
      const keycloakService = new KeycloakService();
      await keycloakService.deleteOrganizationGroup(orgId);

      // Clean up database collections
      const databaseService = new DatabaseService();
      await databaseService.cleanupOrgCollections(orgId);

    } catch (rollbackError) {
      console.error('Rollback failed:', rollbackError);
    }
  }
}
```

### Tenant Provisioning API Endpoint

```javascript
// services/org-service/src/controllers/provisioning.controller.js
import { ProvisioningService } from '../services/provisioning.service.js';
import { asyncHandler } from '../middleware/errorHandler.js';

export const provisionOrganization = asyncHandler(async (req, res) => {
  const {
    name,
    domain,
    adminEmail,
    adminFirstName,
    adminLastName,
    plan
  } = req.body;

  const provisioningService = new ProvisioningService();

  const result = await provisioningService.provisionOrganization({
    name,
    domain,
    adminEmail,
    adminFirstName,
    adminLastName,
    plan
  });

  res.status(201).json(result);
});

export const deprovisionOrganization = asyncHandler(async (req, res) => {
  const { orgId } = req.params;

  // Only super_admin can deprovision
  if (!req.user.roles.includes('super_admin')) {
    throw new ForbiddenError('Insufficient permissions');
  }

  const provisioningService = new ProvisioningService();
  await provisioningService.deprovisionOrganization(orgId);

  res.json({ message: 'Organization deprovisioned successfully' });
});
```

## Data Isolation Patterns

### Query Middleware for Automatic org_id Filtering

```javascript
// shared/middleware/org-scope.middleware.js
export function orgScopeMiddleware(Model) {
  // Pre-find hooks
  Model.schema.pre(/^find/, function(next) {
    if (this.options.skipOrgFilter) {
      return next();
    }

    // Automatically add org_id filter if not present
    if (!this.getQuery().org_id && this.options.orgId) {
      this.where({ org_id: this.options.orgId });
    }

    next();
  });

  // Pre-update hooks
  Model.schema.pre('updateOne', function(next) {
    if (this.options.skipOrgFilter) {
      return next();
    }

    if (!this.getQuery().org_id && this.options.orgId) {
      this.where({ org_id: this.options.orgId });
    }

    next();
  });

  // Pre-delete hooks
  Model.schema.pre('deleteOne', function(next) {
    if (this.options.skipOrgFilter) {
      return next();
    }

    if (!this.getQuery().org_id && this.options.orgId) {
      this.where({ org_id: this.options.orgId });
    }

    next();
  });
}
```

### Service-Level Isolation

```javascript
// services/user-service/src/services/user.service.js
export class UserService {

  constructor(orgId) {
    if (!orgId) {
      throw new Error('orgId is required for UserService');
    }
    this.orgId = orgId;
  }

  async findAll(filter = {}, options = {}) {
    // ALWAYS enforce org_id
    return await UserModel.find({
      ...filter,
      org_id: this.orgId
    }, null, {
      orgId: this.orgId,
      ...options
    });
  }

  async findById(id) {
    const user = await UserModel.findOne({
      _id: id,
      org_id: this.orgId
    });

    if (!user) {
      throw new NotFoundError('User');
    }

    return user;
  }

  // Prevent cross-org data leaks
  async bulkUpdate(userIds, updates) {
    // First verify all users belong to this org
    const count = await UserModel.countDocuments({
      _id: { $in: userIds },
      org_id: this.orgId
    });

    if (count !== userIds.length) {
      throw new ForbiddenError('Some users do not belong to this organization');
    }

    // Proceed with update
    return await UserModel.updateMany(
      {
        _id: { $in: userIds },
        org_id: this.orgId
      },
      updates
    );
  }
}
```

## Cross-Tenant Security Considerations

### Preventing Cross-Org Data Access

```javascript
// services/api-gateway/src/middleware/org-validation.middleware.js
export function validateOrgAccess(extractOrgId) {
  return (req, res, next) => {
    // Extract org_id from request (params, query, or body)
    const resourceOrgId = extractOrgId(req);

    if (!resourceOrgId) {
      return next();
    }

    // Verify user has access to this org
    if (resourceOrgId !== req.user.orgId) {
      // Super admins can access any org
      if (req.user.roles.includes('super_admin')) {
        return next();
      }

      // Log potential security violation
      console.warn('Cross-org access attempt:', {
        userId: req.user.sub,
        userOrgId: req.user.orgId,
        attemptedOrgId: resourceOrgId,
        path: req.path,
        method: req.method,
        ip: req.ip
      });

      return next(new ForbiddenError('Access denied to organization resources'));
    }

    next();
  };
}

// Usage in routes
router.get('/organizations/:orgId/users',
  validateOrgAccess(req => req.params.orgId),
  listUsers
);
```

### Audit Logging for Cross-Org Access

```javascript
// services/analytics-service/src/services/audit.service.js
export class AuditService {

  async logAccess(event) {
    const log = {
      timestamp: new Date(),
      userId: event.userId,
      userOrgId: event.userOrgId,
      resourceOrgId: event.resourceOrgId,
      action: event.action,
      resource: event.resource,
      resourceId: event.resourceId,
      success: event.success,
      ipAddress: event.ipAddress,
      userAgent: event.userAgent
    };

    // Flag suspicious cross-org access
    if (event.userOrgId !== event.resourceOrgId && !event.isSuperAdmin) {
      log.suspicious = true;
      log.severity = 'high';

      // Alert security team
      await this.sendSecurityAlert(log);
    }

    await AuditLogModel.create(log);
  }
}
```

## Best Practices

1. **ALWAYS include org_id in JWT tokens** via Keycloak protocol mapper
2. **NEVER trust client-provided org_id** - always use token claim
3. **INDEX org_id on ALL collections/tables** for query performance
4. **Use repository pattern** to enforce org_id filtering
5. **Implement row-level security** in PostgreSQL for additional safety
6. **Validate org_id in middleware** before reaching controllers
7. **Audit cross-org access attempts** for security monitoring
8. **Test isolation thoroughly** with automated tests
9. **Use compound indexes** for org_id + frequently queried fields
10. **Prevent org_id modification** in update operations
11. **Implement graceful tenant deprovisioning** with cleanup
12. **Version control theme mappings** for traceability
13. **Monitor query performance** by org_id to detect issues
14. **Implement rate limiting per org** to prevent abuse
15. **Use separate database connections per org** for critical isolation (optional)

## File Locations in keycloak-alpha

| Path | Purpose |
|------|---------|
| `services/org-service/` | Organization provisioning and management |
| `services/api-gateway/src/middleware/auth.js` | Token validation and org_id extraction |
| `services/keycloak-service/src/config/theme-mapping.js` | Theme per organization mapping |
| `shared/middleware/org-scope.middleware.js` | Automatic org_id filtering |
| `services/analytics-service/src/services/audit.service.js` | Cross-org access auditing |

## Testing Multi-Tenancy

### Test Organization Isolation

```javascript
// services/user-service/tests/isolation.test.js
describe('Multi-tenant isolation', () => {
  it('should prevent cross-org data access', async () => {
    // Create users in two different orgs
    const org1User = await createUser({ org_id: 'org_1', email: 'user1@org1.com' });
    const org2User = await createUser({ org_id: 'org_2', email: 'user2@org2.com' });

    // Try to access org_2 user with org_1 token
    const org1Token = generateToken({ org_id: 'org_1' });

    const response = await request(app)
      .get(`/api/users/${org2User._id}`)
      .set('Authorization', `Bearer ${org1Token}`)
      .expect(403);

    expect(response.body.error.message).toContain('Access denied');
  });

  it('should allow super_admin cross-org access', async () => {
    const org2User = await createUser({ org_id: 'org_2' });
    const superAdminToken = generateToken({
      org_id: 'org_1',
      roles: ['super_admin']
    });

    await request(app)
      .get(`/api/users/${org2User._id}`)
      .set('Authorization', `Bearer ${superAdminToken}`)
      .expect(200);
  });
});
```
