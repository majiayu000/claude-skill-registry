---
name: express-api-patterns
description: Express.js API development, route handling, middleware, error handling, request validation, CORS. Use when building Express routes, implementing middleware, handling API requests, or setting up the backend server.
allowed-tools: Read, Grep, Glob
---

# Express API Patterns

## Core Principles

1. **RESTful Design** - Use HTTP methods appropriately (GET, POST, PUT, DELETE)
2. **Middleware First** - Use middleware for cross-cutting concerns
3. **Error Handling** - Centralized error handling middleware
4. **Validation** - Validate all inputs before processing
5. **Security** - CORS, rate limiting, input sanitization

---

## Server Setup Pattern

### CORRECT: Well-Structured Express Server

```javascript
// server/index.js
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

// Import routes
import authRoutes from './routes/auth.js';
import generateRoutes from './routes/generate.js';
import imageRoutes from './routes/images.js';

const app = express();
const PORT = process.env.PORT || 3001;

// ===== Middleware =====

// CORS configuration
app.use(cors({
  origin: process.env.CLIENT_URL || 'http://localhost:5173',
  credentials: true
}));

// Body parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Request logging (development only)
if (process.env.NODE_ENV === 'development') {
  app.use((req, res, next) => {
    console.log(`${req.method} ${req.path}`);
    next();
  });
}

// ===== Routes =====

app.use('/api/auth', authRoutes);
app.use('/api/generate', generateRoutes);
app.use('/api/images', imageRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// ===== Error Handling =====

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

// Global error handler
app.use((err, req, res, next) => {
  console.error('Error:', err);

  const status = err.status || 500;
  const message = err.message || 'Internal server error';

  res.status(status).json({ error: message });
});

// ===== Start Server =====

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});

export default app;
```

---

## Route Pattern

### CORRECT: Well-Structured Route

```javascript
// server/routes/generate.js
import express from 'express';
import { generatePage, generatePageStream } from '../services/claude.js';
import fs from 'fs/promises';
import path from 'path';

const router = express.Router();

// Load system prompt
let systemPrompt = '';
try {
  systemPrompt = await fs.readFile(
    path.join(process.cwd(), 'prompts', 'system.txt'),
    'utf-8'
  );
} catch (error) {
  console.error('Failed to load system prompt:', error);
}

/**
 * POST /api/generate
 * Generate or update instructional page
 */
router.post('/', async (req, res, next) => {
  try {
    // 1. Extract and validate input
    const { config, message, history = [] } = req.body;

    if (!config || !config.topic) {
      return res.status(400).json({ error: 'Topic is required' });
    }

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    if (config.depthLevel < 0 || config.depthLevel > 4) {
      return res.status(400).json({ error: 'Depth level must be 0-4' });
    }

    // 2. Call service
    const result = await generatePage(systemPrompt, config, message, history);

    // 3. Return response
    res.json({
      message: result.message,
      html: result.html,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    // Pass to error handler
    next(error);
  }
});

/**
 * POST /api/generate/stream
 * Generate page with streaming response
 */
router.post('/stream', async (req, res, next) => {
  try {
    const { config, message, history = [] } = req.body;

    // Validation (same as above)
    if (!config?.topic || !message) {
      return res.status(400).json({ error: 'Invalid request' });
    }

    // Set headers for Server-Sent Events
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    // Stream generation
    await generatePageStream(systemPrompt, config, message, history, (chunk) => {
      res.write(`data: ${JSON.stringify(chunk)}\n\n`);
    });

    res.end();

  } catch (error) {
    next(error);
  }
});

export default router;
```

### WRONG: Poor Route Structure

```javascript
// ❌ DON'T DO THIS
router.post('/generate', (req, res) => {
  // ❌ No input validation
  // ❌ No error handling
  // ❌ Directly accessing nested properties without checks
  generatePage(req.body.config.topic, req.body.message).then(result => {
    res.send(result); // ❌ Not using res.json()
  });
});
```

---

## Middleware Patterns

### Authentication Middleware

```javascript
// server/middleware/auth.js
export const verifyPassword = (req, res, next) => {
  const { password } = req.body;
  const correctPassword = process.env.FACULTY_PASSWORD;

  if (!correctPassword) {
    return res.status(500).json({ error: 'Server configuration error' });
  }

  if (password !== correctPassword) {
    return res.status(401).json({ error: 'Invalid password' });
  }

  next(); // Password correct, proceed
};

// Usage in route
import { verifyPassword } from '../middleware/auth.js';

router.post('/verify', verifyPassword, (req, res) => {
  res.json({ success: true });
});
```

### Request Validation Middleware

```javascript
// server/middleware/validate.js
export const validateGenerateRequest = (req, res, next) => {
  const { config, message } = req.body;
  const errors = [];

  if (!config) {
    errors.push('config is required');
  } else {
    if (!config.topic) errors.push('config.topic is required');
    if (config.depthLevel === undefined) errors.push('config.depthLevel is required');
    if (config.depthLevel < 0 || config.depthLevel > 4) {
      errors.push('config.depthLevel must be 0-4');
    }
  }

  if (!message) {
    errors.push('message is required');
  }

  if (errors.length > 0) {
    return res.status(400).json({ error: errors.join(', ') });
  }

  next();
};

// Usage
router.post('/', validateGenerateRequest, async (req, res, next) => {
  // Request is validated
  // ... handle request
});
```

### Rate Limiting Middleware

```javascript
// server/middleware/rateLimit.js
import rateLimit from 'express-rate-limit';

export const generateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 50, // 50 requests per window
  message: { error: 'Too many requests, please try again later' },
  standardHeaders: true,
  legacyHeaders: false
});

// Usage
router.post('/', generateLimiter, async (req, res, next) => {
  // Rate limited endpoint
});
```

---

## Error Handling Patterns

### Custom Error Classes

```javascript
// server/utils/errors.js
export class ValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = 'ValidationError';
    this.status = 400;
  }
}

export class APIError extends Error {
  constructor(message, status = 500) {
    super(message);
    this.name = 'APIError';
    this.status = status;
  }
}

// Usage in route
import { ValidationError, APIError } from '../utils/errors.js';

router.post('/', async (req, res, next) => {
  try {
    if (!req.body.config) {
      throw new ValidationError('Config is required');
    }

    const result = await someAPICall();

    if (!result) {
      throw new APIError('API call failed', 503);
    }

    res.json(result);
  } catch (error) {
    next(error); // Pass to error handler
  }
});
```

### Centralized Error Handler

```javascript
// server/middleware/errorHandler.js
export const errorHandler = (err, req, res, next) => {
  // Log error
  console.error('Error:', {
    name: err.name,
    message: err.message,
    stack: process.env.NODE_ENV === 'development' ? err.stack : undefined,
    url: req.url,
    method: req.method
  });

  // Determine status and message
  const status = err.status || 500;
  const message = err.message || 'Internal server error';

  // Send response
  res.status(status).json({
    error: message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
};

// In server setup
app.use(errorHandler);
```

---

## Service Layer Pattern

Separate business logic from route handlers:

```javascript
// server/services/claude.js
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

export const generatePage = async (systemPrompt, config, message, history) => {
  // Business logic here
  const messages = [
    ...history.map(msg => ({ role: msg.role, content: msg.content })),
    { role: 'user', content: buildPrompt(config, message) }
  ];

  try {
    const response = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 8192,
      system: systemPrompt,
      messages: messages
    });

    return {
      message: extractMessage(response.content[0].text),
      html: extractHTML(response.content[0].text)
    };
  } catch (error) {
    throw new APIError(`Claude API error: ${error.message}`, 503);
  }
};

// Helper functions
const buildPrompt = (config, message) => {
  let prompt = message + '\n\n';
  prompt += `Topic: ${config.topic}\n`;
  prompt += `Depth Level: ${config.depthLevel}\n`;

  if (config.styleFlags?.length > 0) {
    prompt += `Style Flags: ${config.styleFlags.join(', ')}\n`;
  }

  return prompt;
};

const extractHTML = (text) => {
  const match = text.match(/```html\n([\s\S]*?)\n```/);
  if (!match) throw new Error('Could not extract HTML');
  return match[1].trim();
};

const extractMessage = (text) => {
  return text.split('```html')[0].trim();
};
```

---

## File Upload Pattern

```javascript
// server/routes/images.js
import express from 'express';
import multer from 'multer';
import { uploadToCloudinary } from '../services/cloudinary.js';

const router = express.Router();

// Configure multer for memory storage
const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 10 * 1024 * 1024 // 10MB
  },
  fileFilter: (req, file, cb) => {
    // Only allow images
    if (!file.mimetype.startsWith('image/')) {
      return cb(new Error('Only image files allowed'));
    }
    cb(null, true);
  }
});

/**
 * POST /api/images/upload
 * Upload image to Cloudinary
 */
router.post('/upload', upload.single('image'), async (req, res, next) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    // Upload to Cloudinary
    const result = await uploadToCloudinary(req.file.buffer);

    res.json({
      url: result.secure_url,
      publicId: result.public_id
    });

  } catch (error) {
    next(error);
  }
});

// Multer error handling
router.use((error, req, res, next) => {
  if (error instanceof multer.MulterError) {
    if (error.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({ error: 'File too large (max 10MB)' });
    }
    return res.status(400).json({ error: error.message });
  }
  next(error);
});

export default router;
```

---

## Environment Configuration

```javascript
// server/config/index.js
import dotenv from 'dotenv';

dotenv.config();

const config = {
  port: parseInt(process.env.PORT || '3001', 10),
  nodeEnv: process.env.NODE_ENV || 'development',

  faculty: {
    password: process.env.FACULTY_PASSWORD
  },

  anthropic: {
    apiKey: process.env.ANTHROPIC_API_KEY
  },

  openai: {
    apiKey: process.env.OPENAI_API_KEY
  },

  cloudinary: {
    cloudName: process.env.CLOUDINARY_CLOUD_NAME,
    apiKey: process.env.CLOUDINARY_API_KEY,
    apiSecret: process.env.CLOUDINARY_API_SECRET
  },

  cors: {
    origin: process.env.CLIENT_URL || 'http://localhost:5173'
  }
};

// Validate required config
const validateConfig = () => {
  const required = [
    'faculty.password',
    'anthropic.apiKey',
    'openai.apiKey'
  ];

  const missing = required.filter(path => {
    const value = path.split('.').reduce((obj, key) => obj?.[key], config);
    return !value;
  });

  if (missing.length > 0) {
    throw new Error(`Missing required config: ${missing.join(', ')}`);
  }
};

validateConfig();

export default config;
```

---

## Testing Express Routes

```javascript
// server/routes/generate.test.js
import { describe, it, expect, vi, beforeEach } from 'vitest';
import request from 'supertest';
import express from 'express';
import generateRoutes from './generate.js';

// Mock the claude service
vi.mock('../services/claude.js', () => ({
  generatePage: vi.fn()
}));

import { generatePage } from '../services/claude.js';

const app = express();
app.use(express.json());
app.use('/api/generate', generateRoutes);

describe('Generate Routes', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should generate page successfully', async () => {
    generatePage.mockResolvedValue({
      message: 'Generated successfully',
      html: '<html>...</html>'
    });

    const response = await request(app)
      .post('/api/generate')
      .send({
        config: { topic: 'React', depthLevel: 2 },
        message: 'Create a page',
        history: []
      });

    expect(response.status).toBe(200);
    expect(response.body.html).toBe('<html>...</html>');
  });

  it('should validate required fields', async () => {
    const response = await request(app)
      .post('/api/generate')
      .send({
        config: { depthLevel: 2 }, // Missing topic
        message: 'Test'
      });

    expect(response.status).toBe(400);
    expect(response.body.error).toContain('topic');
  });

  it('should handle errors gracefully', async () => {
    generatePage.mockRejectedValue(new Error('API error'));

    const response = await request(app)
      .post('/api/generate')
      .send({
        config: { topic: 'Test', depthLevel: 2 },
        message: 'Test'
      });

    expect(response.status).toBe(500);
  });
});
```

---

## Checklist

### Before Creating Route
- [ ] What HTTP method is appropriate?
- [ ] What validation is needed?
- [ ] What middleware should be applied?
- [ ] What error cases need handling?
- [ ] Should logic be in service layer?

### After Creating Route
- [ ] Input validation implemented
- [ ] Error handling in place
- [ ] Success response well-structured
- [ ] Status codes appropriate
- [ ] Service layer used for business logic
- [ ] Tests written
- [ ] Documentation added

---

## Integration with Other Skills

- **api-client-patterns**: Frontend consumption of these APIs
- **prompt-engineering**: Claude API integration
- **react-component-patterns**: Using API responses in UI
- **systematic-debugging**: Debugging API issues

---

## Common Mistakes to Avoid

1. ❌ No input validation
2. ❌ Not using try/catch with async
3. ❌ Business logic in route handlers
4. ❌ Inconsistent error responses
5. ❌ Missing CORS configuration
6. ❌ Hard-coded configuration values
7. ❌ No request logging
8. ❌ Missing rate limiting
9. ❌ Not using middleware for common tasks
10. ❌ Ignoring security best practices
