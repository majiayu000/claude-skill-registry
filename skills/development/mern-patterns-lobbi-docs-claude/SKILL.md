---
name: mern-patterns
description: MERN stack patterns including React with Vite, Express middleware, MongoDB schemas, API Gateway architecture, session management, error handling, and testing strategies. Activate for MERN development, microservices architecture, and full-stack JavaScript applications.
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
triggers:
  - mern
  - react
  - express
  - mongodb
  - node
  - vite
  - api
  - microservices
  - full-stack
---

# MERN Stack Patterns Skill

Comprehensive MERN stack development patterns for the keycloak-alpha multi-tenant platform with 8 microservices.

## When to Use This Skill

Activate this skill when:
- Building React + Vite frontend applications
- Implementing Express microservices
- Designing MongoDB schemas and data models
- Setting up API Gateway architecture
- Implementing session and cookie management
- Adding error handling and validation
- Writing tests for MERN stack applications

## keycloak-alpha Project Structure

```
keycloak-alpha/
├── apps/
│   ├── web-app/                    # Main React + Vite SPA
│   │   ├── src/
│   │   │   ├── components/
│   │   │   ├── pages/
│   │   │   ├── hooks/
│   │   │   ├── contexts/
│   │   │   ├── config/
│   │   │   ├── utils/
│   │   │   └── main.jsx
│   │   ├── vite.config.js
│   │   └── package.json
│   └── admin-portal/               # Admin dashboard (React + Vite)
│
├── services/
│   ├── api-gateway/                # Express API Gateway
│   ├── user-service/               # User management
│   ├── org-service/                # Organization management
│   ├── tenant-service/             # Multi-tenant provisioning
│   ├── notification-service/       # Email/SMS notifications
│   ├── billing-service/            # Stripe integration
│   ├── analytics-service/          # Usage analytics
│   └── keycloak-service/          # Keycloak integration
│
├── routes/
│   ├── api/
│   │   ├── users.js
│   │   ├── organizations.js
│   │   └── tenants.js
│   └── index.js
│
├── shared/
│   ├── types/
│   ├── utils/
│   └── constants/
│
└── package.json
```

## React + Vite Frontend Patterns

### Vite Configuration

```javascript
// apps/web-app/vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],

  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@contexts': path.resolve(__dirname, './src/contexts'),
      '@utils': path.resolve(__dirname, './src/utils'),
      '@config': path.resolve(__dirname, './src/config'),
    }
  },

  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:4000',
        changeOrigin: true,
      }
    }
  },

  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['react', 'react-dom', 'react-router-dom'],
          'keycloak': ['keycloak-js'],
          'ui': ['@chakra-ui/react', '@emotion/react']
        }
      }
    }
  },

  optimizeDeps: {
    include: ['react', 'react-dom', 'keycloak-js']
  }
});
```

### Component Organization

```javascript
// apps/web-app/src/components/features/UserProfile/index.jsx
import { useState, useEffect } from 'react';
import { useAuth } from '@hooks/useAuth';
import { useToast } from '@chakra-ui/react';
import { updateUserProfile } from '@/api/users';

export function UserProfile() {
  const { user } = useAuth();
  const toast = useToast();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchProfile();
  }, []);

  async function fetchProfile() {
    setLoading(true);
    try {
      const data = await getUserProfile(user.sub);
      setProfile(data);
    } catch (error) {
      toast({
        title: 'Error loading profile',
        description: error.message,
        status: 'error',
        duration: 5000,
      });
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(formData) {
    try {
      await updateUserProfile(user.sub, formData);
      toast({
        title: 'Profile updated',
        status: 'success',
        duration: 3000,
      });
    } catch (error) {
      toast({
        title: 'Update failed',
        description: error.message,
        status: 'error',
        duration: 5000,
      });
    }
  }

  if (loading) return <Spinner />;
  if (!profile) return <Alert>Profile not found</Alert>;

  return <ProfileForm profile={profile} onSubmit={handleSubmit} />;
}
```

### Custom Hooks Pattern

```javascript
// apps/web-app/src/hooks/useAuth.js
import { createContext, useContext, useState, useEffect } from 'react';
import Keycloak from 'keycloak-js';
import { keycloakConfig } from '@config/keycloak.config';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [keycloak, setKeycloak] = useState(null);
  const [authenticated, setAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const kc = new Keycloak(keycloakConfig);

    kc.init({
      onLoad: 'check-sso',
      checkLoginIframe: true,
      pkceMethod: 'S256'
    }).then(authenticated => {
      setKeycloak(kc);
      setAuthenticated(authenticated);

      if (authenticated) {
        setUser({
          sub: kc.tokenParsed.sub,
          email: kc.tokenParsed.email,
          name: kc.tokenParsed.name,
          orgId: kc.tokenParsed.org_id,
          roles: kc.tokenParsed.realm_access?.roles || []
        });
      }

      setLoading(false);
    });

    // Token refresh
    kc.onTokenExpired = () => {
      kc.updateToken(30).catch(() => {
        kc.logout();
      });
    };
  }, []);

  const login = () => keycloak.login();
  const logout = () => keycloak.logout();
  const getToken = () => keycloak.token;

  return (
    <AuthContext.Provider value={{
      authenticated,
      user,
      loading,
      login,
      logout,
      getToken
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```

### API Client Pattern

```javascript
// apps/web-app/src/utils/apiClient.js
import axios from 'axios';
import { useAuth } from '@hooks/useAuth';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:4000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  async (config) => {
    const token = await getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/login';
    }

    const errorMessage = error.response?.data?.message || error.message;
    return Promise.reject(new Error(errorMessage));
  }
);

export default apiClient;

// Typed API methods
export const api = {
  users: {
    getProfile: (userId) => apiClient.get(`/users/${userId}`),
    updateProfile: (userId, data) => apiClient.put(`/users/${userId}`, data),
    listUsers: (orgId) => apiClient.get(`/users?org_id=${orgId}`)
  },
  organizations: {
    get: (orgId) => apiClient.get(`/organizations/${orgId}`),
    create: (data) => apiClient.post('/organizations', data),
    update: (orgId, data) => apiClient.put(`/organizations/${orgId}`, data)
  }
};
```

## Express Microservice Patterns

### Service Structure

```javascript
// services/user-service/src/index.js
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import morgan from 'morgan';
import { connectDB } from './config/database.js';
import { errorHandler } from './middleware/errorHandler.js';
import { authMiddleware } from './middleware/auth.js';
import userRoutes from './routes/users.js';

const app = express();

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGIN?.split(',') || 'http://localhost:3000',
  credentials: true
}));

// Logging
app.use(morgan('combined'));

// Body parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Connect to MongoDB
await connectDB();

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', service: 'user-service' });
});

// API routes (protected)
app.use('/api/users', authMiddleware, userRoutes);

// Error handling
app.use(errorHandler);

const PORT = process.env.PORT || 5001;
app.listen(PORT, () => {
  console.log(`User service running on port ${PORT}`);
});
```

### Route Organization

```javascript
// services/user-service/src/routes/users.js
import express from 'express';
import { body, param, query } from 'express-validator';
import { validate } from '../middleware/validate.js';
import { requireRole } from '../middleware/rbac.js';
import * as userController from '../controllers/user.controller.js';

const router = express.Router();

// GET /api/users - List users (org admin only)
router.get('/',
  requireRole(['org_admin']),
  query('org_id').optional().isString(),
  query('page').optional().isInt({ min: 1 }),
  query('limit').optional().isInt({ min: 1, max: 100 }),
  validate,
  userController.listUsers
);

// GET /api/users/:id - Get user by ID
router.get('/:id',
  param('id').isUUID(),
  validate,
  userController.getUser
);

// POST /api/users - Create user (org admin only)
router.post('/',
  requireRole(['org_admin']),
  body('email').isEmail().normalizeEmail(),
  body('firstName').trim().isLength({ min: 1, max: 50 }),
  body('lastName').trim().isLength({ min: 1, max: 50 }),
  body('orgId').isString(),
  validate,
  userController.createUser
);

// PUT /api/users/:id - Update user
router.put('/:id',
  param('id').isUUID(),
  body('firstName').optional().trim().isLength({ min: 1, max: 50 }),
  body('lastName').optional().trim().isLength({ min: 1, max: 50 }),
  validate,
  userController.updateUser
);

// DELETE /api/users/:id - Delete user (org admin only)
router.delete('/:id',
  requireRole(['org_admin']),
  param('id').isUUID(),
  validate,
  userController.deleteUser
);

export default router;
```

### Controller Pattern

```javascript
// services/user-service/src/controllers/user.controller.js
import { UserModel } from '../models/User.js';
import { KeycloakService } from '../services/keycloak.service.js';
import { AppError } from '../utils/AppError.js';

export async function listUsers(req, res, next) {
  try {
    const { org_id, page = 1, limit = 20 } = req.query;

    // Ensure user can only list users from their org (unless super admin)
    const orgIdFilter = req.user.roles.includes('super_admin')
      ? org_id
      : req.user.org_id;

    if (!orgIdFilter) {
      throw new AppError('Organization ID required', 400);
    }

    const users = await UserModel.find({ org_id: orgIdFilter })
      .select('-password')
      .limit(limit)
      .skip((page - 1) * limit)
      .sort({ createdAt: -1 });

    const total = await UserModel.countDocuments({ org_id: orgIdFilter });

    res.json({
      users,
      pagination: {
        page: parseInt(page),
        limit: parseInt(limit),
        total,
        pages: Math.ceil(total / limit)
      }
    });
  } catch (error) {
    next(error);
  }
}

export async function getUser(req, res, next) {
  try {
    const { id } = req.params;

    const user = await UserModel.findById(id).select('-password');

    if (!user) {
      throw new AppError('User not found', 404);
    }

    // Ensure user can only access users from their org
    if (user.org_id !== req.user.org_id && !req.user.roles.includes('super_admin')) {
      throw new AppError('Access denied', 403);
    }

    res.json(user);
  } catch (error) {
    next(error);
  }
}

export async function createUser(req, res, next) {
  try {
    const { email, firstName, lastName, orgId } = req.body;

    // Verify org_id matches user's org (unless super admin)
    if (orgId !== req.user.org_id && !req.user.roles.includes('super_admin')) {
      throw new AppError('Cannot create user for different organization', 403);
    }

    // Create user in Keycloak
    const keycloakService = new KeycloakService();
    const keycloakUserId = await keycloakService.createUser({
      email,
      firstName,
      lastName,
      orgId
    });

    // Create user in MongoDB
    const user = new UserModel({
      keycloakId: keycloakUserId,
      email,
      firstName,
      lastName,
      org_id: orgId,
      createdBy: req.user.sub
    });

    await user.save();

    res.status(201).json({
      id: user._id,
      keycloakId: keycloakUserId,
      email: user.email
    });
  } catch (error) {
    next(error);
  }
}
```

## MongoDB Schema Patterns

### User Model

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
    trim: true,
    index: true
  },
  firstName: {
    type: String,
    required: true,
    trim: true
  },
  lastName: {
    type: String,
    required: true,
    trim: true
  },
  org_id: {
    type: String,
    required: true,
    index: true
  },
  roles: [{
    type: String,
    enum: ['org_admin', 'org_user', 'super_admin']
  }],
  metadata: {
    type: Map,
    of: String
  },
  createdBy: String,
  updatedBy: String
}, {
  timestamps: true,
  toJSON: {
    transform: (doc, ret) => {
      ret.id = ret._id;
      delete ret._id;
      delete ret.__v;
      return ret;
    }
  }
});

// Compound index for org queries
userSchema.index({ org_id: 1, email: 1 }, { unique: true });

// Virtual for full name
userSchema.virtual('fullName').get(function() {
  return `${this.firstName} ${this.lastName}`;
});

// Pre-save hook
userSchema.pre('save', function(next) {
  if (this.isModified('email')) {
    this.email = this.email.toLowerCase();
  }
  next();
});

export const UserModel = mongoose.model('User', userSchema);
```

### Organization Model

```javascript
// services/org-service/src/models/Organization.js
import mongoose from 'mongoose';

const organizationSchema = new mongoose.Schema({
  org_id: {
    type: String,
    required: true,
    unique: true,
    index: true
  },
  name: {
    type: String,
    required: true,
    trim: true
  },
  domain: {
    type: String,
    required: true,
    unique: true,
    lowercase: true
  },
  settings: {
    theme: {
      type: String,
      default: 'lobbi-base'
    },
    features: {
      type: Map,
      of: Boolean,
      default: new Map()
    },
    branding: {
      logoUrl: String,
      primaryColor: String,
      secondaryColor: String
    }
  },
  subscription: {
    plan: {
      type: String,
      enum: ['free', 'starter', 'professional', 'enterprise'],
      default: 'free'
    },
    status: {
      type: String,
      enum: ['active', 'inactive', 'suspended'],
      default: 'active'
    },
    billingCycle: {
      type: String,
      enum: ['monthly', 'annual']
    },
    stripeCustomerId: String,
    stripeSubscriptionId: String
  },
  adminUsers: [{
    userId: String,
    email: String,
    addedAt: Date
  }],
  status: {
    type: String,
    enum: ['active', 'inactive', 'suspended'],
    default: 'active'
  }
}, {
  timestamps: true
});

export const OrganizationModel = mongoose.model('Organization', organizationSchema);
```

## API Gateway Architecture

### Gateway Setup

```javascript
// services/api-gateway/src/index.js
import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';
import { authMiddleware } from './middleware/auth.js';
import { rateLimiter } from './middleware/rateLimit.js';
import { cacheMiddleware } from './middleware/cache.js';

const app = express();

// Rate limiting
app.use(rateLimiter);

// Authentication
app.use(authMiddleware);

// Service routing
const services = {
  users: process.env.USER_SERVICE_URL || 'http://localhost:5001',
  orgs: process.env.ORG_SERVICE_URL || 'http://localhost:5002',
  tenants: process.env.TENANT_SERVICE_URL || 'http://localhost:5003',
  notifications: process.env.NOTIFICATION_SERVICE_URL || 'http://localhost:5004',
  billing: process.env.BILLING_SERVICE_URL || 'http://localhost:5005',
  analytics: process.env.ANALYTICS_SERVICE_URL || 'http://localhost:5006'
};

// Proxy to microservices
Object.entries(services).forEach(([name, target]) => {
  app.use(`/api/${name}`, createProxyMiddleware({
    target,
    changeOrigin: true,
    pathRewrite: { [`^/api/${name}`]: '' },
    onProxyReq: (proxyReq, req) => {
      // Forward user context
      if (req.user) {
        proxyReq.setHeader('X-User-Id', req.user.sub);
        proxyReq.setHeader('X-Org-Id', req.user.org_id);
        proxyReq.setHeader('X-User-Roles', JSON.stringify(req.user.roles));
      }
    }
  }));
});

app.listen(4000, () => {
  console.log('API Gateway running on port 4000');
});
```

## Session and Cookie Management

### Session Configuration

```javascript
// services/api-gateway/src/config/session.js
import session from 'express-session';
import MongoStore from 'connect-mongo';

export const sessionConfig = session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,

  store: MongoStore.create({
    mongoUrl: process.env.MONGODB_URL,
    ttl: 24 * 60 * 60, // 1 day
    touchAfter: 24 * 3600 // lazy session update
  }),

  cookie: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    maxAge: 1000 * 60 * 60 * 24, // 24 hours
    sameSite: 'lax',
    domain: process.env.COOKIE_DOMAIN
  },

  name: 'lobbi.sid'
});
```

## Error Handling Patterns

### Custom Error Classes

```javascript
// shared/utils/AppError.js
export class AppError extends Error {
  constructor(message, statusCode = 500, isOperational = true) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = isOperational;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class ValidationError extends AppError {
  constructor(message, errors = []) {
    super(message, 400);
    this.errors = errors;
  }
}

export class NotFoundError extends AppError {
  constructor(resource) {
    super(`${resource} not found`, 404);
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401);
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Forbidden') {
    super(message, 403);
  }
}
```

### Error Handler Middleware

```javascript
// services/user-service/src/middleware/errorHandler.js
import { AppError } from '../utils/AppError.js';

export function errorHandler(err, req, res, next) {
  let { statusCode, message, isOperational } = err;

  // Default to 500 server error
  if (!statusCode) {
    statusCode = 500;
    isOperational = false;
  }

  // Log error
  console.error('Error:', {
    message,
    statusCode,
    isOperational,
    stack: err.stack,
    url: req.url,
    method: req.method,
    user: req.user?.sub
  });

  // Send error response
  res.status(statusCode).json({
    error: {
      message: isOperational ? message : 'Internal server error',
      statusCode,
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    }
  });
}

// Async error wrapper
export function asyncHandler(fn) {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}
```

## Testing Strategies

### Unit Tests with Jest

```javascript
// services/user-service/tests/controllers/user.controller.test.js
import { listUsers, createUser } from '../../src/controllers/user.controller.js';
import { UserModel } from '../../src/models/User.js';
import { KeycloakService } from '../../src/services/keycloak.service.js';

jest.mock('../../src/models/User.js');
jest.mock('../../src/services/keycloak.service.js');

describe('UserController', () => {
  describe('listUsers', () => {
    it('should return paginated users for org', async () => {
      const mockUsers = [
        { _id: '1', email: 'user1@test.com', org_id: 'org_1' },
        { _id: '2', email: 'user2@test.com', org_id: 'org_1' }
      ];

      UserModel.find.mockReturnValue({
        select: jest.fn().mockReturnThis(),
        limit: jest.fn().mockReturnThis(),
        skip: jest.fn().mockReturnThis(),
        sort: jest.fn().mockResolvedValue(mockUsers)
      });

      UserModel.countDocuments.mockResolvedValue(2);

      const req = {
        query: { org_id: 'org_1', page: 1, limit: 20 },
        user: { org_id: 'org_1', roles: ['org_admin'] }
      };
      const res = {
        json: jest.fn()
      };
      const next = jest.fn();

      await listUsers(req, res, next);

      expect(res.json).toHaveBeenCalledWith({
        users: mockUsers,
        pagination: expect.objectContaining({
          page: 1,
          total: 2
        })
      });
    });
  });
});
```

### Integration Tests

```javascript
// services/user-service/tests/integration/users.test.js
import request from 'supertest';
import { app } from '../../src/index.js';
import { connectDB, closeDB, clearDB } from '../setup.js';

beforeAll(async () => await connectDB());
afterEach(async () => await clearDB());
afterAll(async () => await closeDB());

describe('User API Integration', () => {
  it('POST /api/users - should create user', async () => {
    const userData = {
      email: 'test@example.com',
      firstName: 'Test',
      lastName: 'User',
      orgId: 'org_test'
    };

    const response = await request(app)
      .post('/api/users')
      .set('Authorization', `Bearer ${mockAdminToken}`)
      .send(userData)
      .expect(201);

    expect(response.body).toMatchObject({
      email: userData.email
    });
  });
});
```

## Best Practices

1. **Use environment variables** for all configuration
2. **Implement proper error handling** with custom error classes
3. **Validate all inputs** using express-validator or Joi
4. **Use async/await** consistently, avoid callback hell
5. **Implement proper logging** with structured logs
6. **Use MongoDB indexes** for frequently queried fields
7. **Implement rate limiting** to prevent abuse
8. **Use CORS properly** with specific origins
9. **Implement request/response compression** with gzip
10. **Use TypeScript** for better type safety (optional)
11. **Implement health checks** for all services
12. **Use connection pooling** for database connections
13. **Implement graceful shutdown** for services
14. **Use dependency injection** for better testability
15. **Implement proper security headers** with Helmet

## File Locations in keycloak-alpha

| Path | Purpose |
|------|---------|
| `apps/web-app/` | React + Vite main application |
| `services/api-gateway/` | API Gateway with routing |
| `services/user-service/` | User management microservice |
| `services/org-service/` | Organization management |
| `routes/api/` | Shared route definitions |
| `shared/utils/` | Shared utilities and helpers |
