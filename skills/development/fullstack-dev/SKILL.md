---
name: fullstack-dev
description: World-class #1 expert full stack developer specializing in enterprise-grade JavaScript/Node.js, modern frontend architecture, scalable backend systems, and database optimization. Expert in microservices, CI/CD, cloud infrastructure, and performance tuning. Use when building scalable applications, architecting distributed systems, optimizing database performance, or implementing production-ready features.
argument-hint: [feature-description]
---

# World-Class Full Stack Developer - Enterprise Edition

## Project Context: DriverConnect (eddication.io)

**IMPORTANT**: This project is a Fuel Delivery Management System - full-stack logistics platform.

### Application Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND LAYER                          │
│  ┌──────────────────────┐  ┌──────────────────────────────┐ │
│  │   Admin Panel (Web)  │  │   Driver App (LINE LIFF)     │ │
│  │   admin/index.html   │  │   driverapp/index.html       │ │
│  │   - Vanilla JS       │  │   - Vanilla JS + LIFF SDK    │ │
│  │   - Google Maps API  │  │   - GPS/Geolocation API      │ │
│  │   - Real-time map    │  │   - Camera (alcohol test)    │ │
│  └──────────────────────┘  └──────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                      API LAYER                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ Supabase API │  │ Edge Functions│  │ Google Apps     │   │
│  │ - CRUD       │  │ - geocode     │  │ Script (Legacy)  │   │
│  │ - Realtime   │  │ - enrich-coord│  │ - Sheets API     │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                      DATABASE LAYER                           │
│           Supabase PostgreSQL + Google Sheets               │
└─────────────────────────────────────────────────────────────┘
```

### Key Directories

| Directory | Purpose | Tech |
|:---|:---|:---|
| `PTGLG/driverconnect/admin/` | Admin web panel | Vanilla JS, Google Maps |
| `PTGLG/driverconnect/driverapp/` | Driver LIFF app | LIFF v2, Geolocation API |
| `PTGLG/driverconnect/shared/` | Shared utilities | Config, auth helpers |
| `backend/` | Node.js/Express server | Express, Google APIs |
| `supabase/functions/` | Edge Functions | Deno, TypeScript |
| `supabase/migrations/` | Database migrations | PostgreSQL SQL |

### Recent Refactoring (Phase 2.1)

**Before**: `admin/admin.old.js` (3,118 lines monolithic)

**After**: Modular structure
```
admin/
├── admin.js (162 lines - entry point)
└── js/
    ├── main.js - Initialization
    ├── dashboard.js - Analytics
    ├── map.js - Google Maps + markers
    ├── jobs.js - Job management
    ├── users.js - User management
    ├── reports.js - Reports
    ├── utils.js - Utilities (sanitizeHTML, etc.)
    └── realtime.js - Supabase Realtime
```

### Development Commands

```bash
# Apply database migration
cd supabase
node apply-migration.js

# Start backend server
cd backend
npm install
npm start

# Deploy edge functions
supabase functions deploy geocode
supabase functions deploy enrich-coordinates
```

---

## Philosophy & Principles

## Core Engineering Philosophy

1. **Scalability First** - Design for growth from day one
2. **Observability** - Make systems debuggable and monitorable
3. **Security by Default** - Never trust, always validate
4. **Progressive Enhancement** - Build resilient, degradable systems
5. **Developer Experience** - Great code enables great products
6. **Production Mindset** - Code is live from day one

## Best Practices Mindset

- **Write code for the maintainer** (future you)
- **Measure before optimizing** - data-driven decisions
- **Fail fast, fail gracefully** - proper error handling
- **API design is product design** - thoughtful contracts
- **Database schema is your foundation** - get it right early
- **Test what matters** - critical paths over edge cases

---

# When to Use This Skill

Engage this expertise when the user asks about:

- Building scalable web applications or microservices
- Frontend architecture (React, Vue, vanilla JS systems)
- Backend API development (Node.js, Express, Fastify)
- Database design and optimization (SQL, NoSQL, caching)
- API architecture and integration patterns
- Authentication and authorization systems
- Real-time features and websockets
- Performance optimization and profiling
- CI/CD pipelines and deployment strategies
- Cloud architecture and infrastructure
- Microservices or monolith architecture decisions
- State management and data flow design

---

# Tech Stack Mastery

## Frontend Excellence

### Modern JavaScript Patterns

```javascript
// ============================================
// MODULE ARCHITECTURE - ES6+
// ============================================

// Dependency Injection for testability
class UserService {
  constructor(apiClient, cache) {
    this.api = apiClient;
    this.cache = cache;
  }

  async getUser(id) {
    // Check cache first
    const cached = await this.cache.get(`user:${id}`);
    if (cached) return JSON.parse(cached);

    // Fetch from API
    const user = await this.api.get(`/users/${id}`);
    await this.cache.set(`user:${id}`, JSON.stringify(user), 300);

    return user;
  }
}

// Singleton with lazy initialization
class Config {
  constructor() {
    if (Config.instance) return Config.instance;
    this.config = this.loadConfig();
    Config.instance = this;
  }

  loadConfig() {
    // Environment-based config loading
    const env = process.env.NODE_ENV || 'development';
    return require(`./config/${env}.js`);
  }
}

// Factory Pattern for object creation
class DatabaseConnectionFactory {
  create(type, options) {
    switch (type) {
      case 'postgresql':
        return new PostgreSQLConnection(options);
      case 'mongodb':
        return new MongoDBConnection(options);
      case 'redis':
        return new RedisConnection(options);
      default:
        throw new Error(`Unsupported database type: ${type}`);
    }
  }
}

// Observer Pattern for event-driven architecture
class EventEmitter {
  constructor() {
    this.events = new Map();
  }

  on(event, callback) {
    if (!this.events.has(event)) {
      this.events.set(event, []);
    }
    this.events.get(event).push(callback);
    return () => this.off(event, callback); // Unsubscribe function
  }

  emit(event, data) {
    const callbacks = this.events.get(event) || [];
    callbacks.forEach(cb => cb(data));
  }

  off(event, callback) {
    const callbacks = this.events.get(event) || [];
    const index = callbacks.indexOf(callback);
    if (index > -1) callbacks.splice(index, 1);
  }
}
```

### State Management Patterns

```javascript
// ============================================
// STATE MANAGEMENT - Vanilla JS
// ============================================

// Centralized State Store
class StateStore {
  constructor(initialState = {}) {
    this.state = initialState;
    this.listeners = new Set();
    this.middleware = [];
  }

  // Redux-like middleware support
  use(middleware) {
    this.middleware.push(middleware);
  }

  getState() {
    return this.state;
  }

  setState(updater) {
    const prevState = { ...this.state };

    // Apply middleware
    let state = this.state;
    for (const mw of this.middleware) {
      state = mw(state, updater) || state;
    }

    // Apply update
    this.state = typeof updater === 'function'
      ? updater(this.state)
      : { ...this.state, ...updater };

    // Notify listeners
    this.listeners.forEach(listener => listener(this.state, prevState));
  }

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }
}

// Usage with React-like reactivity
const store = new StateStore({
  users: [],
  loading: false,
  error: null
});

// Subscribe to changes
store.subscribe((state, prev) => {
  if (state.users !== prev.users) {
    renderUserList(state.users);
  }
});
```

## Backend Architecture

### Enterprise API Design

```javascript
// ============================================
// EXPRESS API - Enterprise Patterns
// ============================================

const express = require('express');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const { createProxyMiddleware } = require('http-proxy-middleware');

class ApiServer {
  constructor(options = {}) {
    this.app = express();
    this.port = options.port || 3000;
    this.middlewares = [];
    this.routes = new Map();
    this.setupMiddleware();
  }

  setupMiddleware() {
    // Security headers
    this.app.use(helmet({
      contentSecurityPolicy: {
        directives: {
          defaultSrc: ["'self'"],
          styleSrc: ["'self'", "'unsafe-inline'"],
          scriptSrc: ["'self'"],
          imgSrc: ["'self'", 'data:', 'https:'],
        },
      },
    }));

    // Rate limiting
    const limiter = rateLimit({
      windowMs: 15 * 60 * 1000, // 15 minutes
      max: 100, // Limit each IP to 100 requests per windowMs
      standardHeaders: true,
      legacyHeaders: false,
    });

    // Body parsing with validation
    this.app.use(express.json({ limit: '1mb' }));
    this.app.use(express.urlencoded({ extended: true, limit: '1mb' }));

    // Request logging
    this.app.use((req, res, next) => {
      const start = Date.now();
      res.on('finish', () => {
        const duration = Date.now() - start;
        console.log(`${req.method} ${req.path} ${res.statusCode} - ${duration}ms`);
      });
      next();
    });
  }

  // Route registration with metadata
  registerRoute(method, path, handlers) {
    const route = this.routes.get(path) || {};
    route[method] = handlers;
    this.routes.set(path, route);

    this.app[method.toLowerCase()](path, ...handlers);
  }

  // Error handling middleware
  setupErrorHandling() {
    // 404 handler
    this.app.use((req, res) => {
      res.status(404).json({
        error: 'Not Found',
        path: req.path,
        method: req.method,
        timestamp: new Date().toISOString()
      });
    });

    // Global error handler
    this.app.use((err, req, res, next) => {
      console.error('Error:', err);

      // Don't leak error details in production
      const isDev = process.env.NODE_ENV === 'development';
      res.status(err.status || 500).json({
        error: err.message || 'Internal Server Error',
        ...(isDev && { stack: err.stack }),
        timestamp: new Date().toISOString()
      });
    });
  }

  async start() {
    return new Promise((resolve) => {
      this.server = this.app.listen(this.port, () => {
        console.log(`API server listening on port ${this.port}`);
        resolve();
      });
    });
  }

  async stop() {
    if (this.server) {
      return new Promise((resolve) => {
        this.server.close(resolve);
      });
    }
  }
}
```

### Database Connection Pooling

```javascript
// ============================================
// DATABASE CONNECTION POOL - PostgreSQL
// ============================================

const { Pool } = require('pg');

class DatabaseManager {
  constructor(config) {
    this.pool = new Pool({
      host: config.host,
      port: config.port || 5432,
      database: config.database,
      user: config.user,
      password: config.password,
      max: config.max || 20, // Maximum pool size
      idleTimeoutMillis: config.idleTimeout || 30000,
      connectionTimeoutMillis: config.connectTimeout || 2000,
    });

    this.pool.on('error', (err) => {
      console.error('Unexpected error on idle client', err);
      process.exit(-1);
    });
  }

  async query(text, params) {
    const start = Date.now();

    try {
      const result = await this.pool.query(text, params);
      const duration = Date.now() - start;

      // Log slow queries (>100ms)
      if (duration > 100) {
        console.warn(`Slow query (${duration}ms):`, { text, params });
      }

      return result;
    } catch (error) {
      console.error('Query error:', { text, params, error });
      throw error;
    }
  }

  async transaction(callback) {
    const client = await this.pool.connect();

    try {
      await client.query('BEGIN');

      const result = await callback(client);

      await client.query('COMMIT');
      return result;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  async close() {
    await this.pool.end();
  }
}
```

---

# Database Architecture

## Schema Design Patterns

```sql
-- ============================================
-- ENTERPRISE DATABASE SCHEMA
-- ============================================

-- Users table with audit trail
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    email_verified_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ, -- Soft delete
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_active ON users(is_active) WHERE is_active = true;
CREATE INDEX idx_users_created ON users(created_at DESC);

-- GIN index for JSONB queries (if needed)
-- CREATE INDEX idx_users_metadata ON users USING GIN (metadata);

-- Audit log table
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_name TEXT NOT NULL,
    record_id UUID NOT NULL,
    action TEXT NOT NULL, -- INSERT, UPDATE, DELETE
    old_data JSONB,
    new_data JSONB,
    changed_by UUID REFERENCES users(id),
    changed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for audit queries
CREATE INDEX idx_audit_table_record ON audit_logs(table_name, record_id);
CREATE INDEX idx_audit_changed_at ON audit_logs(changed_at DESC);

-- Trigger for automatic audit logging
CREATE OR REPLACE FUNCTION audit_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO audit_logs (table_name, record_id, action, old_data, changed_by)
        VALUES (TG_TABLE_NAME, OLD.id, 'DELETE', row_to_json(OLD), NULL);
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO audit_logs (table_name, record_id, action, old_data, new_data, changed_by)
        VALUES (TG_TABLE_NAME, NEW.id, 'UPDATE', row_to_json(OLD), row_to_json(NEW), NULL);
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO audit_logs (table_name, record_id, action, new_data)
        VALUES (TG_TABLE_NAME, NEW.id, 'INSERT', row_to_json(NEW));
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply audit trigger to users table
CREATE TRIGGER users_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();
```

---

# API Design Patterns

## RESTful API Best Practices

```javascript
// ============================================
// RESTful API CONTROLLER
// ============================================

class ApiController {
  constructor(db, logger) {
    this.db = db;
    this.logger = logger;
  }

  // Generic CRUD operations
  async list(req, res) {
    try {
      const {
        page = 1,
        limit = 20,
        sort = '-created_at',
        filter = {}
      } = req.query;

      // Parse filter parameter
      const where = this.parseFilter(filter);

      // Parse sort parameter
      const orderBy = this.parseSort(sort);

      // Calculate offset
      const offset = (page - 1) * limit;

      // Execute query
      const [data, countResult] = await Promise.all([
        this.db.query('SELECT * FROM users WHERE ?::jsonb ORDER BY ? LIMIT ? OFFSET ?', [where, orderBy, limit, offset]),
        this.db.query('SELECT COUNT(*) FROM users WHERE ?::jsonb', [where])
      ]);

      // Build response with pagination metadata
      res.json({
        data: data.rows,
        meta: {
          page: parseInt(page),
          limit: parseInt(limit),
          total: parseInt(countResult.rows[0].count),
          totalPages: Math.ceil(countResult.rows[0].count / limit)
        }
      });
    } catch (error) {
      this.handleError(res, error);
    }
  }

  async create(req, res) {
    try {
      const { body } = req;

      // Validate input
      const validation = this.validateCreateInput(body);
      if (!validation.valid) {
        return res.status(400).json({
          error: 'Validation Failed',
          details: validation.errors
        });
      }

      // Insert record
      const result = await this.db.query(
        'INSERT INTO users (email, password_hash, full_name, role) VALUES ($1, $2, $3, $4) RETURNING *',
        [body.email, body.password_hash, body.full_name, body.role || 'user']
      );

      res.status(201).json({
        data: result.rows[0],
        meta: {
          timestamp: new Date().toISOString()
        }
      });
    } catch (error) {
      if (error.code === '23505') { // Unique violation
        return res.status(409).json({
          error: 'Conflict',
          message: 'Email already exists'
        });
      }
      this.handleError(res, error);
    }
  }

  parseFilter(filterString) {
    // Convert filter string to WHERE clause
    // Example: {"name":"John","age":30} -> SQL WHERE clause
    try {
      return JSON.stringify(JSON.parse(filterString || '{}'));
    } catch {
      return '{}';
    }
  }

  parseSort(sortString) {
    // Convert sort string to ORDER BY clause
    // Example: "-created_at,name" -> ORDER BY created_at DESC, name ASC
    if (!sortString) return ['created_at DESC'];

    return sortString.split(',').map(field => {
      const direction = field.startsWith('-') ? 'DESC' : 'ASC';
      const columnName = field.replace(/^[+-]/, '');
      return `${columnName} ${direction}`;
    }).join(', ');
  }

  handleError(res, error) {
    this.logger.error('API Error:', error);

    const statusCode = error.statusCode || 500;
    const message = error.message || 'Internal Server Error';

    res.status(statusCode).json({
      error: message,
      ...(process.env.NODE_ENV === 'development' && { stack: error.stack })
    });
  }
}
```

## GraphQL API Patterns

```javascript
// ============================================
// GRAPHQL API STRUCTURE
// ============================================

const { ApolloServer, gql, ApolloError, AuthenticationError } = require('apollo-server-express');

const typeDefs = gql`
  type User {
    id: ID!
    email: String!
    fullName: String!
    role: String!
    isActive: Boolean!
    createdAt: DateTime!
    updatedAt: DateTime!
    posts(limit: Int, offset: Int): PostConnection!
  }

  type Post {
    id: ID!
    title: String!
    content: String!
    author: User!
    publishedAt: DateTime!
    tags: [String!]!
  }

  type PostConnection {
    nodes: [Post!]!
    pageInfo: PageInfo!
    totalCount: Int!
  }

  type PageInfo {
    hasNextPage: Boolean!
    hasPreviousPage: Boolean!
    startCursor: String
    endCursor: String
  }

  type Query {
    me: User
    user(id: ID!): User
    users(limit: Int, offset: Int): UserConnection!
  }

  type Mutation {
    login(email: String!, password: String!): AuthPayload!
    createPost(input: CreatePostInput!): Post!
    updateProfile(input: UpdateProfileInput!): User!
  }

  type AuthPayload {
    token: String!
    user: User!
  }

  scalar DateTime
`;

const resolvers = {
  Query: {
    me: async (parent, args, { user }) => {
      if (!user) throw new AuthenticationError('Not authenticated');
      return getUserById(user.id);
    }
  },

  User: {
    posts: async (user, { limit = 10, offset = 0 }, { dataSources }) => {
      const { nodes, totalCount } = await dataSources.postAPI.getPostsByUser(
        user.id,
        limit,
        offset
      );
      return {
        nodes,
        pageInfo: get pageInfo(nodes),
        totalCount
      };
    }
  }
};

// Data loader for batching
const { DataLoader } = require('dataloader');

const userLoader = new DataLoader(async (ids) => {
  const users = await db.query(
    'SELECT * FROM users WHERE id = ANY($1)',
    [ids]
  );
  return ids.map(id => users.rows.find(u => u.id === id));
});
```

---

# Authentication & Authorization

## JWT-Based Authentication

```javascript
// ============================================
// JWT AUTHENTICATION
// ============================================

const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const crypto = require('crypto');

class AuthService {
  constructor(secretKey, refreshTokenSecret) {
    this.secretKey = secretKey;
    this.refreshTokenSecret = refreshTokenSecret;
  }

  async hashPassword(password) {
    const salt = await bcrypt.genSalt(12);
    return bcrypt.hash(password, salt);
  }

  async comparePassword(password, hash) {
    return bcrypt.compare(password, hash);
  }

  generateAccessToken(payload) {
    return jwt.sign(payload, this.secretKey, {
      expiresIn: '15m', // Short-lived access token
      issuer: 'your-api',
      audience: 'your-app'
    });
  }

  generateRefreshToken(payload) {
    return jwt.sign(payload, this.refreshTokenSecret, {
      expiresIn: '7d', // Longer-lived refresh token
      issuer: 'your-api',
      audience: 'your-app'
    });
  }

  verifyAccessToken(token) {
    try {
      return jwt.verify(token, this.secretKey, {
        issuer: 'your-api',
        audience: 'your-app'
      });
    } catch (error) {
      throw new Error('Invalid or expired token');
    }
  }

  generateResetToken() {
    // Secure random token for password reset
    return crypto.randomBytes(32).toString('hex');
  }
}

// Authentication middleware
function authenticate(req, res, next) {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing or invalid authorization header' });
  }

  const token = authHeader.substring(7);

  try {
    const decoded = authService.verifyAccessToken(token);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
}

// Authorization middleware - RBAC
function authorize(...roles) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Not authenticated' });
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }

    next();
  };
}
```

---

# Real-Time Features

## WebSocket Implementation

```javascript
// ============================================
// WEBSOCKET SERVER - Real-time Updates
// ============================================

const WebSocket = require('ws');

class WebSocketServer {
  constructor(options = {}) {
    this.wss = new WebSocket.Server({
      port: options.port || 8080,
      perMessageDeflate: false, // Compression
      clientTracking: true
    });

    this.clients = new Map(); // userId -> WebSocket
    this.rooms = new Map(); // room -> Set of WebSocket

    this.setupHandlers();
  }

  setupHandlers() {
    this.wss.on('connection', (ws, req) => {
      this.handleConnection(ws, req);
    });
  }

  handleConnection(ws, req) {
    const userId = this.extractUserId(req);

    if (!userId) {
      ws.close(4001, 'Unauthorized');
      return;
    }

    // Store connection
    this.clients.set(userId, ws);

    // Send welcome message
    this.sendToClient(ws, {
      type: 'connected',
      timestamp: new Date().toISOString()
    });

    // Handle incoming messages
    ws.on('message', (data) => {
      this.handleMessage(ws, userId, data);
    });

    // Handle disconnection
    ws.on('close', () => {
      this.handleDisconnection(userId);
    });

    // Handle errors
    ws.on('error', (error) => {
      console.error(`WebSocket error for user ${userId}:`, error);
    });
  }

  handleMessage(ws, userId, data) {
    try {
      const message = JSON.parse(data);

      switch (message.type) {
        case 'subscribe':
          this.handleSubscribe(ws, userId, message);
          break;
        case 'unsubscribe':
          this.handleUnsubscribe(ws, userId, message);
          break;
        case 'ping':
          this.sendToClient(ws, { type: 'pong', timestamp: new Date().toISOString() });
          break;
        default:
          console.warn(`Unknown message type: ${message.type}`);
      }
    } catch (error) {
      console.error('Failed to parse WebSocket message:', error);
    }
  }

  handleSubscribe(ws, userId, message) {
    const room = message.room;

    if (!this.rooms.has(room)) {
      this.rooms.set(room, new Set());
    }

    this.rooms.get(room).add(ws);

    // Send confirmation
    this.sendToClient(ws, {
      type: 'subscribed',
      room,
      timestamp: new Date().toISOString()
    });
  }

  handleUnsubscribe(ws, userId, message) {
    const room = message.room;

    if (this.rooms.has(room)) {
      this.rooms.get(room).delete(ws);

      if (this.rooms.get(room).size === 0) {
        this.rooms.delete(room);
      }
    }
  }

  handleDisconnection(userId) {
    this.clients.delete(userId);

    // Remove from all rooms
    for (const [room, clients] of this.rooms.entries()) {
      clients.forEach((client) => {
        if (client === this.clients.get(userId)) {
          clients.delete(client);
        }
      });

      if (clients.size === 0) {
        this.rooms.delete(room);
      }
    }
  }

  broadcastToRoom(room, message) {
    const clients = this.rooms.get(room);

    if (clients) {
      clients.forEach((client) => {
        if (client.readyState === WebSocket.OPEN) {
          this.sendToClient(client, message);
        }
      });
    }
  }

  sendToClient(ws, message) {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(message));
    }
  }

  extractUserId(req) {
    // Extract user ID from session or token
    return req.user?.id;
  }
}
```

---

# Performance Optimization

## Caching Strategies

```javascript
// ============================================
// MULTI-LAYER CACHING
// ============================================

const NodeCache = require('node-cache');
const Redis = require('ioredis');

class CacheManager {
  constructor(config) {
    // L1: In-memory cache (fast, local)
    this.memoryCache = new NodeCache({
      stdTTL: 60, // 1 minute default
      checkperiod: 120
    });

    // L2: Redis cache (shared across instances)
    this.redis = new Redis({
      host: config.redis.host,
      port: config.redis.port || 6379,
      password: config.redis.password,
      db: config.redis.db || 0
    });

    // L3: CDN cache (for static assets)
  }

  async get(key) {
    // Try L1: In-memory
    const value = this.memoryCache.get(key);
    if (value !== undefined) {
      return { source: 'memory', value };
    }

    // Try L2: Redis
    const redisValue = await this.redis.get(key);
    if (redisValue !== null) {
      // Promote to L1 cache
      this.memoryCache.set(key, JSON.parse(redisValue));
      return { source: 'redis', value: JSON.parse(redisValue) };
    }

    return null;
  }

  async set(key, value, ttl = 300) {
    // Set in all layers
    this.memoryCache.set(key, value, ttl);
    await this.redis.setex(key, ttl, JSON.stringify(value));
  }

  async invalidate(pattern) {
    // Invalidate from all layers
    const keys = this.memoryCache.keys();
    keys.forEach(key => {
      if (key.match(pattern)) {
        this.memoryCache.del(key);
      }
    });

    // Redis scan for pattern matching
    const stream = redis.scanStream();
    for await (const key of stream) {
      if (key.match(pattern)) {
        await this.redis.del(key);
      }
    }
  }

  // Cache-aside pattern for database queries
  async cacheQuery(key, queryFn, ttl = 300) {
    // Check cache first
    const cached = await this.get(key);
    if (cached) {
      return cached.value;
    }

    // Execute query
    const result = await queryFn();

    // Store in cache
    await this.set(key, result, ttl);

    return result;
  }
}
```

---

# Testing Strategy

## Test Patterns

```javascript
// ============================================
// TESTING UTILITIES
// ============================================

// Test database setup
class TestDatabase {
  constructor() {
    this.pool = new Pool({
      host: 'localhost',
      database: 'test_db',
      user: 'test_user',
      password: 'test_pass'
    });
  }

  async setup() {
    // Run migrations
    await this.runMigrations();

    // Seed test data
    await this.seedData();
  }

  async teardown() {
    // Clean up test database
    const tables = await this.pool.query(`
      SELECT tablename FROM pg_tables WHERE schemaname = 'public'
    `);

    for (const table of tables.rows) {
      await this.pool.query(`TRUNCATE TABLE ${table.tablename} CASCADE`);
    }
  }

  async truncate(table) {
    await this.pool.query(`TRUNCATE TABLE ${table} CASCADE`);
  }
}

// API testing helper
class ApiTestClient {
  constructor(app) {
    this.app = app;
  }

  async get(path, headers = {}) {
    return this.request('GET', path, null, headers);
  }

  async post(path, body, headers = {}) {
    return this.request('POST', path, body, headers);
  }

  async request(method, path, body, headers) {
    return this.app.inject({
      method,
      url: path,
      payload: body,
      headers: {
        'content-type': 'application/json',
        ...headers
      }
    });
  }

  async authenticate(email, password) {
    const response = await this.post('/api/auth/login', { email, password });
    return response.result.token;
  }
}
```

---

# Deployment & DevOps

## CI/CD Pipeline

```yaml
# ============================================
# CI/CD PIPELINE - GitHub Actions
# ============================================

name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests
        run: npm test
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info

  build:
    needs: test
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Build Docker image
        run: |
          docker build -t myapp:${{ github.sha }} .
          docker tag myapp:${{ github.sha }} myapp:latest

      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push myapp:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Deploy to production
        run: |
          kubectl set image deployment/myapp myapp=myapp:${{ github.sha }}
          kubectl rollout status deployment/myapp
```

---

# Resources

## Learning Resources

**Backend Architecture**:
- The Twelve-Factor App: https://12factor.net/
- Designing Data-Intensive Applications: https://www.ddia.com/
- Microservices Patterns: https://microservices.io/patterns/

**Frontend Architecture**:
- React Documentation: https://react.dev/
- Web Performance: https://web.dev/
- Progressive Web Apps: https://web.dev/progressive-web-apps/

**Database**:
- PostgreSQL Docs: https://www.postgresql.org/docs/
- Supabase Docs: https://supabase.com/docs
**Node.js Best Practices**:
- Node.js Best Practices: https://github.com/goldbergyoni/nodebestpractices
- Async/Await Patterns: https://javascript.info/async
