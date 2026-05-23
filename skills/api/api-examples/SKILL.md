---
name: api-examples
description: Generate API usage examples and tutorials from code analysis
disable-model-invocation: false
---

# API Examples & Tutorial Generator

I'll analyze your API and generate comprehensive usage examples, code snippets, and tutorials for developers.

Arguments: `$ARGUMENTS` - specific API focus or language (e.g., "REST", "GraphQL", "python", "javascript")

## Strategic Planning Process

<think>
Effective API examples require understanding:

1. **API Analysis**
   - What type of API? (REST, GraphQL, gRPC, WebSocket)
   - What endpoints/operations exist?
   - What's the authentication method?
   - What are common use cases?
   - What error handling is needed?

2. **Audience Consideration**
   - Who are the API consumers? (internal, external, partners)
   - What languages do they use?
   - What's their experience level?
   - What examples will be most valuable?

3. **Example Types**
   - Quick start / Getting started
   - Authentication examples
   - CRUD operation examples
   - Complex workflow examples
   - Error handling patterns
   - Best practices and anti-patterns

4. **Format & Organization**
   - Code snippets for common operations
   - Complete working examples
   - Interactive tutorials
   - SDK usage examples
   - cURL/HTTP examples for testing
</think>

## Token Optimization

**Status:** ✅ Fully Optimized (Phase 2 Batch 4B, 2026-01-27)

**Target:** 65-80% reduction (3,500-5,000 → 900-1,500 tokens)

### Core Strategy: Cache-Based Example Generation

Generate API usage examples efficiently by reusing cached API schemas and pre-built templates instead of analyzing implementation code.

**Optimization Impact:**
- **Before:** 3,500-5,000 tokens (full API analysis + schema reading + example generation)
- **After:** 900-1,500 tokens (cache lookup + template rendering + targeted examples)
- **Savings:** 65-80% reduction

### 1. Cached API Schema (75% savings)

**Pattern:** Reuse OpenAPI/GraphQL schema from `/api-validate`, `/api-docs-generate` cache

```bash
# Instead of analyzing route files (HIGH COST):
# Read: src/routes/*.js (2,000+ tokens)
# Read: src/controllers/*.js (2,000+ tokens)
# Analyze request/response schemas (1,000+ tokens)

# Use cached schema (LOW COST):
cat .claude/cache/api/api_schema.json  # 200 tokens
```

**Cache Structure:**
```json
{
  "schema_version": "1.0",
  "api_type": "REST",
  "framework": "express",
  "base_url": "/api/v1",
  "endpoints": [
    {
      "path": "/users",
      "methods": ["GET", "POST"],
      "auth_required": true,
      "request_schema": {...},
      "response_schema": {...}
    }
  ],
  "auth_methods": ["Bearer", "API Key"],
  "last_updated": "2026-01-27T10:00:00Z"
}
```

**Implementation:**
```bash
# Check cache first
if [ -f .claude/cache/api/api_schema.json ]; then
  echo "✓ Using cached API schema"
  ENDPOINTS=$(jq -r '.endpoints[] | "\(.methods[]) \(.path)"' .claude/cache/api/api_schema.json)
  AUTH_TYPE=$(jq -r '.auth_methods[0]' .claude/cache/api/api_schema.json)
else
  echo "⚠ Cache miss - suggest running /api-validate first"
  # Fallback to minimal discovery
fi
```

**Savings:** 2,000-3,000 tokens avoided per invocation

### 2. Template-Based Examples (70% savings)

**Pattern:** Use pre-built language templates instead of generating from scratch

```bash
# Instead of generating examples from scratch (HIGH COST):
# Analyze endpoint parameters (500+ tokens)
# Generate JavaScript example (400+ tokens)
# Generate Python example (400+ tokens)
# Generate cURL example (300+ tokens)

# Use cached templates (LOW COST):
cat .claude/cache/api/example_templates.json  # 150 tokens
# Fill in endpoint-specific data (100 tokens)
```

**Template Cache:**
```json
{
  "templates": {
    "rest_get_js": "async function get{Resource}(id) {\n  const response = await fetch(`${API_BASE}/{resource}/${id}`, {\n    headers: { 'Authorization': 'Bearer {token}' }\n  });\n  return response.json();\n}",
    "rest_post_js": "async function create{Resource}(data) {\n  const response = await fetch(`${API_BASE}/{resource}`, {\n    method: 'POST',\n    headers: { 'Authorization': 'Bearer {token}', 'Content-Type': 'application/json' },\n    body: JSON.stringify(data)\n  });\n  return response.json();\n}",
    "rest_get_py": "def get_{resource}(id):\n    response = requests.get(f'{API_BASE}/{resource}/{id}', headers={'Authorization': f'Bearer {token}'})\n    response.raise_for_status()\n    return response.json()",
    "graphql_query_js": "const {QUERY_NAME} = gql`\n  query {QueryName}($id: ID!) {\n    {resource}(id: $id) {\n      {fields}\n    }\n  }\n`;"
  },
  "languages": ["javascript", "python", "curl", "typescript"],
  "patterns": ["CRUD", "authentication", "pagination", "error_handling"]
}
```

**Implementation:**
```bash
# Generate examples from templates
ENDPOINT="/users"
METHOD="GET"
RESOURCE="User"

# Lookup and fill template
TEMPLATE=$(jq -r '.templates.rest_get_js' .claude/cache/api/example_templates.json)
echo "$TEMPLATE" | sed "s/{Resource}/$RESOURCE/g" | sed "s|{resource}|${ENDPOINT#/}|g"
```

**Savings:** 1,000-1,500 tokens per language set

### 3. Grep for Endpoints (80% savings)

**Pattern:** Find API routes without reading full implementation files

```bash
# Instead of reading all route files (HIGH COST):
# Read: src/routes/users.js (800 tokens)
# Read: src/routes/posts.js (800 tokens)
# Read: src/routes/auth.js (800 tokens)

# Grep for route definitions (LOW COST):
rg "^\s*(app|router)\.(get|post|put|delete|patch)" src/routes/ \
  --no-filename --only-matching -A 1 | head -20  # 100 tokens
```

**Pattern Matching:**
```bash
# Express routes
rg "router\.(get|post|put|delete)\(['\"]([^'\"]+)" src/routes/ -o

# FastAPI routes
rg "@app\.(get|post|put|delete)\(['\"]([^'\"]+)" --type py -o

# GraphQL schema
rg "type Query|type Mutation" schema.graphql -A 5
```

**Example Output:**
```
router.get('/users
router.post('/users
router.get('/users/:id
router.put('/users/:id
router.delete('/users/:id
```

**Savings:** 2,000-2,500 tokens avoided by not reading implementation

### 4. Language-Specific Templates (75% savings)

**Pattern:** Focus on requested language(s) instead of generating all examples

```bash
# Instead of generating all languages (HIGH COST):
# JavaScript examples (600 tokens)
# Python examples (600 tokens)
# TypeScript examples (600 tokens)
# cURL examples (400 tokens)
# Go examples (600 tokens)

# Generate only requested language (LOW COST):
LANG="${ARGUMENTS:-javascript}"  # From user arguments
TEMPLATE_KEY="rest_get_${LANG}"
# Generate single language (200 tokens)
```

**Smart Language Detection:**
```bash
# Auto-detect primary language
if [ -f package.json ]; then
  PRIMARY_LANG="javascript"
elif [ -f requirements.txt ]; then
  PRIMARY_LANG="python"
elif [ -f go.mod ]; then
  PRIMARY_LANG="go"
fi

# Generate examples for primary language only
echo "Generating $PRIMARY_LANG examples (others available on request)"
```

**Savings:** 1,500-2,000 tokens by focusing on relevant language

### 5. Progressive Examples (60% savings)

**Pattern:** Generate basic example first, advanced on explicit request

```bash
# Default: Quick start example only (300 tokens)
cat .claude/cache/api/quickstart_template.md

# On request: Advanced examples
if [[ "$ARGUMENTS" =~ "advanced" ]]; then
  # Error handling (200 tokens)
  # Pagination (200 tokens)
  # Rate limiting (200 tokens)
  # Batch operations (200 tokens)
fi
```

**Progressive Disclosure:**
```markdown
## Quick Start (Generated by default)
Basic authentication and simple GET/POST examples

## Advanced Topics (Generated on request)
- Error handling patterns: `/api-examples advanced error-handling`
- Pagination strategies: `/api-examples advanced pagination`
- WebSocket real-time: `/api-examples advanced websocket`
- Batch operations: `/api-examples advanced batch`
```

**Implementation:**
```bash
# Minimal quick start
echo "## Quick Start"
echo "Basic example using cached template..."

# List available advanced topics
echo ""
echo "## Available Advanced Topics"
echo "Run '/api-examples advanced <topic>' for detailed examples:"
echo "- error-handling"
echo "- pagination"
echo "- authentication"
echo "- rate-limiting"
```

**Savings:** 1,000-1,500 tokens by deferring advanced examples

### Cache Structure & Integration

**Shared Cache Directory:** `.claude/cache/api/`

**Files:**
```
.claude/cache/api/
├── api_schema.json           # Shared with /api-validate, /api-docs-generate
├── example_templates.json    # Language-specific example templates
├── endpoint_inventory.json   # Quick endpoint list with metadata
├── quickstart_template.md    # Default quick start example
└── advanced_examples/        # Advanced topic templates
    ├── error_handling.md
    ├── pagination.md
    ├── authentication.md
    └── rate_limiting.md
```

**Cache Management:**
```bash
# Initialize cache
mkdir -p .claude/cache/api/advanced_examples

# Check cache freshness
if [ -f .claude/cache/api/api_schema.json ]; then
  CACHE_AGE=$(( $(date +%s) - $(stat -f %m .claude/cache/api/api_schema.json 2>/dev/null || stat -c %Y .claude/cache/api/api_schema.json) ))
  if [ $CACHE_AGE -gt 86400 ]; then
    echo "⚠ API schema cache is >24h old, consider refreshing with /api-validate"
  fi
fi
```

**Integration with Other Skills:**
- **`/api-validate`:** Generates and caches `api_schema.json`
- **`/api-docs-generate`:** Uses and updates `api_schema.json`
- **`/api-test-generate`:** Shares `endpoint_inventory.json`
- **`/types-generate`:** Uses schema for type generation

### Optimization Workflow

**Optimized Execution Flow:**
```bash
# 1. Check cache (50 tokens)
CACHE_DIR=".claude/cache/api"
if [ ! -f "$CACHE_DIR/api_schema.json" ]; then
  echo "⚠ API schema not cached. Run /api-validate first for best results."
  exit 1
fi

# 2. Load cached schema (100 tokens)
API_TYPE=$(jq -r '.api_type' "$CACHE_DIR/api_schema.json")
ENDPOINTS=$(jq -r '.endpoints[].path' "$CACHE_DIR/api_schema.json" | head -5)

# 3. Detect target language (50 tokens)
TARGET_LANG="${ARGUMENTS:-javascript}"

# 4. Load templates (100 tokens)
TEMPLATES=$(cat "$CACHE_DIR/example_templates.json")

# 5. Generate basic examples (300 tokens)
for endpoint in $ENDPOINTS; do
  # Render template with endpoint data
  echo "Generating example for $endpoint..."
done

# 6. Offer advanced topics (100 tokens)
echo "Run with 'advanced' flag for detailed error handling, pagination, etc."

# Total: 700 tokens (vs 3,500+ tokens without optimization)
```

**Token Usage Breakdown:**

| Operation | Before | After | Savings |
|-----------|--------|-------|---------|
| API schema discovery | 2,000 | 100 | 95% |
| Endpoint analysis | 1,500 | 50 | 97% |
| Example generation | 1,500 | 300 | 80% |
| Language templates | 600 | 150 | 75% |
| Advanced topics | 800 | 100 | 88% |
| **Total** | **3,500-5,000** | **900-1,500** | **65-80%** |

### Performance Metrics

**Before Optimization:**
- API discovery: 2,000 tokens
- Schema analysis: 1,500 tokens
- Example generation: 1,500-2,000 tokens
- Multi-language output: 500-1,000 tokens
- **Total: 3,500-5,000 tokens**

**After Optimization:**
- Cache check: 50 tokens
- Schema load: 100 tokens
- Template rendering: 300 tokens
- Target language: 150 tokens
- Progressive disclosure: 100-200 tokens
- **Total: 900-1,500 tokens**

**Result: 65-80% token reduction**

### Best Practices

**For Maximum Efficiency:**

1. **Run `/api-validate` first** to populate schema cache
2. **Specify target language** in arguments: `/api-examples javascript`
3. **Request advanced topics explicitly**: `/api-examples advanced error-handling`
4. **Use cache indicators**: Check for "✓ Using cached schema" message
5. **Refresh cache periodically**: After API changes or every 24 hours

**Cache Maintenance:**
```bash
# Check cache status
ls -lh .claude/cache/api/

# Refresh schema cache
/api-validate  # Updates api_schema.json

# Clear stale cache
find .claude/cache/api/ -mtime +7 -delete  # Remove week-old cache
```

### Integration Examples

**Workflow 1: Complete API Documentation**
```bash
/api-validate          # Cache schema (500 tokens)
/api-docs-generate     # Use cached schema (400 tokens)
/api-examples          # Use cached schema (900 tokens)
# Total: 1,800 tokens (vs 8,000+ without caching)
```

**Workflow 2: Language-Specific Examples**
```bash
/api-examples python   # Python examples only (900 tokens)
# vs generating all languages (3,500+ tokens)
# Savings: 73%
```

**Workflow 3: Progressive Learning**
```bash
/api-examples                        # Quick start (700 tokens)
/api-examples advanced authentication # Auth details (200 tokens)
/api-examples advanced error-handling # Error patterns (200 tokens)
# Total: 1,100 tokens (on-demand vs 3,500+ upfront)
```

## Phase 1: API Discovery

**MANDATORY FIRST STEPS:**
1. Check for cached API schema (`.claude/cache/api/api_schema.json`)
2. If cache exists, load endpoint inventory
3. If cache missing, suggest running `/api-validate` first
4. Detect target language from arguments or project files

Let me analyze your API:

```bash
# Check for cached API schema first (OPTIMIZED)
CACHE_DIR=".claude/cache/api"
if [ -f "$CACHE_DIR/api_schema.json" ]; then
    echo "✓ Using cached API schema"

    # Extract key information from cache
    API_TYPE=$(jq -r '.api_type' "$CACHE_DIR/api_schema.json")
    FRAMEWORK=$(jq -r '.framework' "$CACHE_DIR/api_schema.json")
    BASE_URL=$(jq -r '.base_url' "$CACHE_DIR/api_schema.json")
    ENDPOINT_COUNT=$(jq '.endpoints | length' "$CACHE_DIR/api_schema.json")

    echo "API Type: $API_TYPE"
    echo "Framework: $FRAMEWORK"
    echo "Base URL: $BASE_URL"
    echo "Endpoints: $ENDPOINT_COUNT"

    # Show first 5 endpoints
    echo ""
    echo "Sample Endpoints:"
    jq -r '.endpoints[0:5] | .[] | "\(.methods | join(",")) \(.path)"' "$CACHE_DIR/api_schema.json"

    # Check cache age
    CACHE_AGE=$(( $(date +%s) - $(stat -f %m "$CACHE_DIR/api_schema.json" 2>/dev/null || stat -c %Y "$CACHE_DIR/api_schema.json") ))
    if [ $CACHE_AGE -gt 86400 ]; then
        echo ""
        echo "⚠ Cache is >24h old. Consider refreshing with /api-validate"
    fi
else
    echo "⚠ API schema not cached"
    echo "For best performance, run /api-validate first to cache API schema"
    echo ""
    echo "Falling back to minimal discovery..."

    # Minimal framework detection only
    if [ -f package.json ] && grep -q "\"express\"" package.json; then
        echo "Framework: Express (Node.js REST)"
    elif [ -f requirements.txt ] && grep -q "fastapi" requirements.txt; then
        echo "Framework: FastAPI (Python REST)"
    elif [ -f package.json ] && grep -q "\"@apollo/server\"" package.json; then
        echo "Framework: GraphQL (Apollo)"
    fi

    # Check for OpenAPI spec
    if [ -f "openapi.yaml" ] || [ -f "openapi.json" ]; then
        echo "✓ OpenAPI spec found - recommend running /api-validate"
    fi
fi
```

## Phase 2: Target Language Selection

**OPTIMIZED:** Detect target language from arguments or project context to generate focused examples.

```bash
# Parse target language from arguments
TARGET_LANG="${ARGUMENTS:-auto}"

# Auto-detect if not specified
if [ "$TARGET_LANG" = "auto" ]; then
    if [ -f package.json ]; then
        TARGET_LANG="javascript"
    elif [ -f requirements.txt ] || [ -f pyproject.toml ]; then
        TARGET_LANG="python"
    elif [ -f go.mod ]; then
        TARGET_LANG="go"
    elif [ -f Gemfile ]; then
        TARGET_LANG="ruby"
    else
        TARGET_LANG="javascript"  # Default
    fi
fi

echo "Target Language: $TARGET_LANG"
echo "For other languages, use: /api-examples <language>"
echo ""

# Load language-specific templates
if [ -f "$CACHE_DIR/example_templates.json" ]; then
    echo "✓ Using cached example templates"
    AVAILABLE_TEMPLATES=$(jq -r ".templates | keys[] | select(contains(\"_${TARGET_LANG}\"))" "$CACHE_DIR/example_templates.json" | wc -l)
    echo "Available templates: $AVAILABLE_TEMPLATES"
else
    echo "Using built-in example templates"
fi
```

## Phase 3: Example Generation

**OPTIMIZED:** Generate examples using cached templates and schema data.

```bash
# Determine example scope
EXAMPLE_SCOPE="${ARGUMENTS}"

if [[ "$EXAMPLE_SCOPE" =~ "advanced" ]]; then
    echo "Generating advanced examples..."
    SCOPE="advanced"
else
    echo "Generating quick start examples (use 'advanced' for more)"
    SCOPE="basic"
fi

# Extract sample endpoints from cache
if [ -f "$CACHE_DIR/endpoint_inventory.json" ]; then
    SAMPLE_ENDPOINTS=$(jq -r '.endpoints[0:3] | .[] | .path' "$CACHE_DIR/endpoint_inventory.json")
else
    # Grep for common patterns if cache unavailable
    SAMPLE_ENDPOINTS=$(rg "^\s*(router|app)\.(get|post)" src/ -o | head -3 | cut -d'(' -f2 | tr -d "'\"")
fi

echo "Generating examples for:"
echo "$SAMPLE_ENDPOINTS"
```

### Quick Start Example

**JavaScript/Node.js:**
```javascript
// Quick Start - API Client Setup
const API_BASE_URL = 'https://api.example.com/v1';
const API_KEY = 'your_api_key_here';

// Initialize API client
const headers = {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${API_KEY}`
};

// Example: Fetch user data
async function getUser(userId) {
  const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
    method: 'GET',
    headers: headers
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return data;
}

// Usage
getUser('123')
  .then(user => console.log('User:', user))
  .catch(error => console.error('Error:', error));
```

**Python:**
```python
# Quick Start - API Client Setup
import requests

API_BASE_URL = 'https://api.example.com/v1'
API_KEY = 'your_api_key_here'

# Initialize session
session = requests.Session()
session.headers.update({
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
})

# Example: Fetch user data
def get_user(user_id):
    response = session.get(f'{API_BASE_URL}/users/{user_id}')
    response.raise_for_status()  # Raise exception for bad status codes
    return response.json()

# Usage
try:
    user = get_user('123')
    print('User:', user)
except requests.exceptions.RequestException as e:
    print('Error:', e)
```

**cURL:**
```bash
# Quick Start - cURL Examples

# Fetch user data
curl -X GET "https://api.example.com/v1/users/123" \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json"
```

### Authentication Examples

**OAuth 2.0 Flow:**
```javascript
// OAuth 2.0 Authentication Example
const CLIENT_ID = 'your_client_id';
const CLIENT_SECRET = 'your_client_secret';
const REDIRECT_URI = 'https://yourapp.com/callback';

// Step 1: Get authorization URL
function getAuthorizationUrl() {
  const params = new URLSearchParams({
    client_id: CLIENT_ID,
    redirect_uri: REDIRECT_URI,
    response_type: 'code',
    scope: 'read write'
  });
  return `https://api.example.com/oauth/authorize?${params}`;
}

// Step 2: Exchange code for access token
async function getAccessToken(code) {
  const response = await fetch('https://api.example.com/oauth/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      code: code,
      redirect_uri: REDIRECT_URI,
      grant_type: 'authorization_code'
    })
  });

  const data = await response.json();
  return data.access_token;
}

// Step 3: Use access token for API calls
async function makeAuthenticatedRequest(accessToken) {
  const response = await fetch('https://api.example.com/v1/user', {
    headers: {
      'Authorization': `Bearer ${accessToken}`
    }
  });
  return response.json();
}
```

### CRUD Operation Examples

**Complete CRUD Example:**
```javascript
// CRUD Operations Example

class UserAPI {
  constructor(baseUrl, apiKey) {
    this.baseUrl = baseUrl;
    this.headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    };
  }

  // CREATE - Create a new user
  async createUser(userData) {
    const response = await fetch(`${this.baseUrl}/users`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(userData)
    });
    return response.json();
  }

  // READ - Get user by ID
  async getUser(userId) {
    const response = await fetch(`${this.baseUrl}/users/${userId}`, {
      method: 'GET',
      headers: this.headers
    });
    return response.json();
  }

  // READ - List all users with pagination
  async listUsers(page = 1, limit = 10) {
    const params = new URLSearchParams({ page, limit });
    const response = await fetch(`${this.baseUrl}/users?${params}`, {
      method: 'GET',
      headers: this.headers
    });
    return response.json();
  }

  // UPDATE - Update user
  async updateUser(userId, updates) {
    const response = await fetch(`${this.baseUrl}/users/${userId}`, {
      method: 'PUT',
      headers: this.headers,
      body: JSON.stringify(updates)
    });
    return response.json();
  }

  // DELETE - Delete user
  async deleteUser(userId) {
    const response = await fetch(`${this.baseUrl}/users/${userId}`, {
      method: 'DELETE',
      headers: this.headers
    });
    return response.ok;
  }
}

// Usage Example
const api = new UserAPI('https://api.example.com/v1', 'your_api_key');

// Create user
const newUser = await api.createUser({
  name: 'John Doe',
  email: 'john@example.com'
});
console.log('Created:', newUser);

// Get user
const user = await api.getUser(newUser.id);
console.log('Retrieved:', user);

// Update user
const updated = await api.updateUser(newUser.id, {
  name: 'Jane Doe'
});
console.log('Updated:', updated);

// List users
const users = await api.listUsers(1, 10);
console.log('Users:', users);

// Delete user
const deleted = await api.deleteUser(newUser.id);
console.log('Deleted:', deleted);
```

### Error Handling Examples

**Comprehensive Error Handling:**
```javascript
// Error Handling Best Practices

class APIError extends Error {
  constructor(message, statusCode, response) {
    super(message);
    this.statusCode = statusCode;
    this.response = response;
    this.name = 'APIError';
  }
}

async function makeAPIRequest(url, options) {
  try {
    const response = await fetch(url, options);

    // Handle different error status codes
    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));

      switch (response.status) {
        case 400:
          throw new APIError(
            'Bad Request: ' + (errorBody.message || 'Invalid parameters'),
            400,
            errorBody
          );
        case 401:
          throw new APIError(
            'Unauthorized: Invalid or expired token',
            401,
            errorBody
          );
        case 403:
          throw new APIError(
            'Forbidden: Insufficient permissions',
            403,
            errorBody
          );
        case 404:
          throw new APIError(
            'Not Found: Resource does not exist',
            404,
            errorBody
          );
        case 429:
          throw new APIError(
            'Rate Limit Exceeded: Too many requests',
            429,
            errorBody
          );
        case 500:
          throw new APIError(
            'Internal Server Error: Please try again later',
            500,
            errorBody
          );
        default:
          throw new APIError(
            `HTTP Error ${response.status}`,
            response.status,
            errorBody
          );
      }
    }

    return response.json();
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    // Network errors, timeout, etc.
    throw new APIError(
      'Network Error: ' + error.message,
      0,
      null
    );
  }
}

// Usage with error handling
async function getUserSafely(userId) {
  try {
    const user = await makeAPIRequest(
      `https://api.example.com/v1/users/${userId}`,
      {
        method: 'GET',
        headers: { 'Authorization': 'Bearer token' }
      }
    );
    return user;
  } catch (error) {
    if (error instanceof APIError) {
      switch (error.statusCode) {
        case 401:
          // Redirect to login
          console.log('Please log in again');
          break;
        case 404:
          // User not found
          console.log('User not found');
          return null;
        case 429:
          // Retry with backoff
          console.log('Rate limited, retrying...');
          await new Promise(r => setTimeout(r, 5000));
          return getUserSafely(userId);
        default:
          console.error('API Error:', error.message);
      }
    } else {
      console.error('Unexpected error:', error);
    }
    throw error;
  }
}
```

### GraphQL Examples

**GraphQL Query & Mutation Examples:**
```javascript
// GraphQL API Examples

const GRAPHQL_ENDPOINT = 'https://api.example.com/graphql';

// Helper function for GraphQL requests
async function graphqlRequest(query, variables = {}) {
  const response = await fetch(GRAPHQL_ENDPOINT, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer your_token_here'
    },
    body: JSON.stringify({
      query,
      variables
    })
  });

  const result = await response.json();

  if (result.errors) {
    throw new Error(result.errors[0].message);
  }

  return result.data;
}

// Query Example: Fetch user with posts
const GET_USER_QUERY = `
  query GetUser($userId: ID!) {
    user(id: $userId) {
      id
      name
      email
      posts {
        id
        title
        content
        createdAt
      }
    }
  }
`;

async function getUser(userId) {
  const data = await graphqlRequest(GET_USER_QUERY, { userId });
  return data.user;
}

// Mutation Example: Create post
const CREATE_POST_MUTATION = `
  mutation CreatePost($input: CreatePostInput!) {
    createPost(input: $input) {
      id
      title
      content
      author {
        id
        name
      }
    }
  }
`;

async function createPost(title, content, authorId) {
  const data = await graphqlRequest(CREATE_POST_MUTATION, {
    input: { title, content, authorId }
  });
  return data.createPost;
}

// Usage
const user = await getUser('123');
console.log('User:', user);

const post = await createPost('My Post', 'Content here', '123');
console.log('Created post:', post);
```

### SDK Usage Examples

**TypeScript SDK Example:**
```typescript
// TypeScript SDK Usage

import { ApiClient, User, CreateUserRequest } from '@example/api-sdk';

// Initialize client
const client = new ApiClient({
  apiKey: 'your_api_key',
  baseUrl: 'https://api.example.com/v1'
});

// Type-safe API calls
async function exampleUsage() {
  try {
    // Create user with full type safety
    const newUser: CreateUserRequest = {
      name: 'John Doe',
      email: 'john@example.com',
      role: 'admin'
    };

    const createdUser: User = await client.users.create(newUser);
    console.log('Created user:', createdUser.id);

    // Fetch user with autocomplete
    const user: User = await client.users.get(createdUser.id);
    console.log('User details:', user);

    // List users with pagination
    const users = await client.users.list({
      page: 1,
      limit: 10,
      filter: { role: 'admin' }
    });
    console.log('Found', users.total, 'users');

    // Update user
    const updated: User = await client.users.update(user.id, {
      name: 'Jane Doe'
    });

    // Delete user
    await client.users.delete(user.id);
  } catch (error) {
    if (error instanceof ApiClient.ValidationError) {
      console.error('Validation failed:', error.fields);
    } else if (error instanceof ApiClient.AuthenticationError) {
      console.error('Authentication required');
    } else {
      console.error('API error:', error);
    }
  }
}
```

## Phase 4: Tutorial Generation

I'll create complete tutorials for common workflows:

**Tutorial Structure:**
1. **Introduction**: What the tutorial covers
2. **Prerequisites**: Required setup and credentials
3. **Step-by-step guide**: Detailed instructions with code
4. **Expected output**: What success looks like
5. **Troubleshooting**: Common issues and solutions
6. **Next steps**: Advanced topics to explore

**Example Tutorial Topics:**
- Getting started with the API
- Authentication and authorization
- Implementing pagination
- File upload and download
- Webhooks integration
- Real-time updates with WebSockets
- Batch operations and bulk updates
- Advanced filtering and search

## Token Optimization in Practice

**This skill achieves 65-80% token reduction through:**

1. **Cache-First Strategy:** Uses `.claude/cache/api/api_schema.json` from `/api-validate` instead of analyzing code
2. **Template-Based Generation:** Pre-built language templates instead of generating from scratch
3. **Progressive Disclosure:** Quick start by default, advanced examples on explicit request
4. **Language Targeting:** Generates only requested language(s) based on arguments or project detection
5. **Grep-Based Discovery:** Finds endpoints without reading implementation files

**Usage Tips:**
- Run `/api-validate` first to populate schema cache
- Specify target language: `/api-examples python`
- Request advanced topics explicitly: `/api-examples advanced error-handling`
- Check for "✓ Using cached schema" message for optimal performance

**See detailed optimization strategies in the "Token Optimization" section above.**

## Integration Points

**Synergistic Skills:**
- `/api-docs-generate` - Generate OpenAPI/Swagger docs first
- `/api-test-generate` - Generate tests alongside examples
- `/docs` - Add examples to project documentation
- `/types-generate` - Generate TypeScript types for examples

Suggests `/api-docs-generate` when:
- No OpenAPI spec exists
- Need formal API documentation
- Want interactive API explorer

Suggests `/types-generate` when:
- TypeScript project detected
- Need type-safe API client
- SDK generation needed

## Output Files Created

I'll create organized example files:

**Directory Structure:**
```
docs/api-examples/
├── README.md                    # Overview and quick start
├── authentication.md            # Auth examples
├── getting-started.md          # Quick start guide
├── crud-operations.md          # Basic CRUD examples
├── advanced-examples.md        # Complex workflows
├── error-handling.md           # Error handling patterns
├── code-snippets/
│   ├── javascript/
│   │   ├── basic-example.js
│   │   ├── auth-example.js
│   │   └── complete-client.js
│   ├── python/
│   │   ├── basic_example.py
│   │   ├── auth_example.py
│   │   └── complete_client.py
│   ├── typescript/
│   │   └── sdk-usage.ts
│   └── curl/
│       └── examples.sh
└── tutorials/
    ├── tutorial-1-getting-started.md
    ├── tutorial-2-authentication.md
    └── tutorial-3-advanced-usage.md
```

## Safety Mechanisms

**Protection Measures:**
- Never include real API keys in examples
- Use placeholder credentials clearly marked
- Create examples in `docs/api-examples/` directory
- Non-destructive (only creates documentation)
- Validate code syntax before output

**Security Best Practices:**
- Show environment variable usage for secrets
- Demonstrate secure credential storage
- Include rate limiting examples
- Show proper error handling
- Warn about common security pitfalls

## Important Notes

**I will NEVER:**
- Include real API keys, tokens, or credentials
- Add AI attribution to example code
- Generate examples without analyzing actual API
- Create insecure authentication examples
- Expose sensitive endpoint information

**Best Practices:**
- Keep examples simple and focused
- Include error handling in all examples
- Show both success and error cases
- Provide working, tested code
- Document prerequisites clearly

## Credits

**Inspired by:**
- [Stripe API Documentation](https://stripe.com/docs/api) - Excellent API examples
- [Twilio API Docs](https://www.twilio.com/docs) - Comprehensive tutorials
- [GitHub REST API Docs](https://docs.github.com/en/rest) - Clear code examples
- API documentation best practices
- Developer experience research

This skill helps you create comprehensive API documentation with working examples that developers can actually use.
