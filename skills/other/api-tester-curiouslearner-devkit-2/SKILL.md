---
name: api-tester
description: Quick API endpoint testing with comprehensive request/response validation.
---

# API Tester Skill

Quick API endpoint testing with comprehensive request/response validation.

## Instructions

You are an API testing expert. When invoked:

1. **Test API Endpoints**:
   - Validate HTTP methods (GET, POST, PUT, PATCH, DELETE)
   - Test request headers and body formats
   - Verify response status codes
   - Validate response schema and data types
   - Check authentication and authorization

2. **Generate Test Cases**:
   - Create curl commands for testing
   - Generate Postman collections
   - Write automated test scripts
   - Test edge cases and error scenarios
   - Validate API contracts

3. **Performance Testing**:
   - Load testing with concurrent requests
   - Response time benchmarking
   - Rate limit verification
   - Timeout handling
   - Connection pooling tests

4. **Security Testing**:
   - Authentication/authorization checks
   - Input validation testing
   - SQL injection prevention
   - XSS prevention
   - CORS configuration

## Usage Examples

```
@api-tester
@api-tester --endpoint /api/users
@api-tester --method POST
@api-tester --load-test
@api-tester --generate-collection
```

## REST API Testing

### GET Request Examples

#### Basic GET Request
```bash
# curl
curl -X GET https://api.example.com/api/users \
  -H "Content-Type: application/json"

# With authentication
curl -X GET https://api.example.com/api/users \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"

# With query parameters
curl -X GET "https://api.example.com/api/users?page=1&limit=10&sort=created_at" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Verbose output (includes headers)
curl -v -X GET https://api.example.com/api/users
```

#### JavaScript/Node.js
```javascript
// Using fetch
async function getUsers() {
  const response = await fetch('https://api.example.com/api/users', {
    method: 'GET',
    headers: {
      'Authorization': 'Bearer YOUR_TOKEN',
      'Content-Type': 'application/json'
    }
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return data;
}

// Using axios
const axios = require('axios');

async function getUsers() {
  try {
    const response = await axios.get('https://api.example.com/api/users', {
      headers: {
        'Authorization': 'Bearer YOUR_TOKEN'
      },
      params: {
        page: 1,
        limit: 10
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
    throw error;
  }
}
```

#### Python
```python
import requests

# Basic GET request
response = requests.get('https://api.example.com/api/users')
print(response.json())

# With authentication and parameters
headers = {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
}

params = {
    'page': 1,
    'limit': 10,
    'sort': 'created_at'
}

response = requests.get(
    'https://api.example.com/api/users',
    headers=headers,
    params=params
)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

### POST Request Examples

#### Create Resource
```bash
# curl
curl -X POST https://api.example.com/api/users \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user"
  }'

# From file
curl -X POST https://api.example.com/api/users \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d @user.json
```

#### JavaScript/Node.js
```javascript
// Using fetch
async function createUser(userData) {
  const response = await fetch('https://api.example.com/api/users', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer YOUR_TOKEN',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(userData)
  });

  const data = await response.json();
  return data;
}

// Usage
const newUser = {
  name: 'John Doe',
  email: 'john@example.com',
  role: 'user'
};

createUser(newUser)
  .then(user => console.log('Created:', user))
  .catch(error => console.error('Error:', error));

// Using axios with error handling
async function createUser(userData) {
  try {
    const response = await axios.post(
      'https://api.example.com/api/users',
      userData,
      {
        headers: {
          'Authorization': 'Bearer YOUR_TOKEN'
        }
      }
    );
    return response.data;
  } catch (error) {
    if (error.response) {
      // Server responded with error
      console.error('Error:', error.response.status);
      console.error('Message:', error.response.data);
    } else if (error.request) {
      // No response received
      console.error('No response from server');
    } else {
      console.error('Error:', error.message);
    }
    throw error;
  }
}
```

#### Python
```python
import requests

# Create user
user_data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'role': 'user'
}

headers = {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
}

response = requests.post(
    'https://api.example.com/api/users',
    json=user_data,
    headers=headers
)

if response.status_code == 201:
    print('User created:', response.json())
else:
    print(f'Error: {response.status_code}')
    print(response.json())
```

### PUT/PATCH Request Examples

```bash
# PUT - Replace entire resource
curl -X PUT https://api.example.com/api/users/123 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Updated",
    "email": "john.updated@example.com",
    "role": "admin"
  }'

# PATCH - Partial update
curl -X PATCH https://api.example.com/api/users/123 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "admin"
  }'
```

### DELETE Request Examples

```bash
# Delete resource
curl -X DELETE https://api.example.com/api/users/123 \
  -H "Authorization: Bearer YOUR_TOKEN"

# Delete with confirmation
curl -X DELETE https://api.example.com/api/users/123 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "X-Confirm-Delete: true"
```

## Authentication Examples

### Bearer Token (JWT)
```bash
# Get token
curl -X POST https://api.example.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'

# Use token
curl -X GET https://api.example.com/api/users \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### API Key
```bash
# In header
curl -X GET https://api.example.com/api/users \
  -H "X-API-Key: your-api-key-here"

# In query parameter
curl -X GET "https://api.example.com/api/users?api_key=your-api-key-here"
```

### Basic Auth
```bash
# Username and password
curl -X GET https://api.example.com/api/users \
  -u username:password

# Base64 encoded
curl -X GET https://api.example.com/api/users \
  -H "Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ="
```

### OAuth 2.0
```javascript
// Get access token
async function getAccessToken() {
  const response = await fetch('https://oauth.example.com/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({
      grant_type: 'client_credentials',
      client_id: 'YOUR_CLIENT_ID',
      client_secret: 'YOUR_CLIENT_SECRET'
    })
  });

  const data = await response.json();
  return data.access_token;
}

// Use access token
async function callAPI() {
  const token = await getAccessToken();

  const response = await fetch('https://api.example.com/api/users', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  return response.json();
}
```

## GraphQL Testing

### Basic Query
```bash
# curl
curl -X POST https://api.example.com/graphql \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ users { id name email } }"
  }'

# With variables
curl -X POST https://api.example.com/graphql \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query GetUser($id: ID!) { user(id: $id) { id name email } }",
    "variables": { "id": "123" }
  }'
```

### GraphQL Mutations
```javascript
// Create user mutation
async function createUser(name, email) {
  const query = `
    mutation CreateUser($name: String!, $email: String!) {
      createUser(input: { name: $name, email: $email }) {
        id
        name
        email
        createdAt
      }
    }
  `;

  const response = await fetch('https://api.example.com/graphql', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer YOUR_TOKEN',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      query,
      variables: { name, email }
    })
  });

  const data = await response.json();
  return data.data.createUser;
}
```

## Automated Testing

### Jest Test Suite
```javascript
const axios = require('axios');

describe('User API Tests', () => {
  const API_URL = 'https://api.example.com';
  const token = 'YOUR_TEST_TOKEN';

  const api = axios.create({
    baseURL: API_URL,
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  describe('GET /api/users', () => {
    test('should return list of users', async () => {
      const response = await api.get('/api/users');

      expect(response.status).toBe(200);
      expect(Array.isArray(response.data)).toBe(true);
      expect(response.data.length).toBeGreaterThan(0);
    });

    test('should return user by ID', async () => {
      const response = await api.get('/api/users/123');

      expect(response.status).toBe(200);
      expect(response.data).toHaveProperty('id', '123');
      expect(response.data).toHaveProperty('name');
      expect(response.data).toHaveProperty('email');
    });

    test('should return 404 for non-existent user', async () => {
      try {
        await api.get('/api/users/999999');
      } catch (error) {
        expect(error.response.status).toBe(404);
      }
    });
  });

  describe('POST /api/users', () => {
    test('should create new user', async () => {
      const newUser = {
        name: 'Test User',
        email: 'test@example.com'
      };

      const response = await api.post('/api/users', newUser);

      expect(response.status).toBe(201);
      expect(response.data).toHaveProperty('id');
      expect(response.data.name).toBe(newUser.name);
      expect(response.data.email).toBe(newUser.email);
    });

    test('should validate required fields', async () => {
      const invalidUser = { name: 'Test' }; // missing email

      try {
        await api.post('/api/users', invalidUser);
      } catch (error) {
        expect(error.response.status).toBe(400);
        expect(error.response.data).toHaveProperty('error');
      }
    });

    test('should prevent duplicate emails', async () => {
      const user = {
        name: 'Duplicate',
        email: 'existing@example.com'
      };

      try {
        await api.post('/api/users', user);
      } catch (error) {
        expect(error.response.status).toBe(409);
      }
    });
  });

  describe('Authentication', () => {
    test('should reject requests without token', async () => {
      const noAuthAPI = axios.create({ baseURL: API_URL });

      try {
        await noAuthAPI.get('/api/users');
      } catch (error) {
        expect(error.response.status).toBe(401);
      }
    });

    test('should reject invalid token', async () => {
      const badAuthAPI = axios.create({
        baseURL: API_URL,
        headers: { 'Authorization': 'Bearer invalid-token' }
      });

      try {
        await badAuthAPI.get('/api/users');
      } catch (error) {
        expect(error.response.status).toBe(401);
      }
    });
  });
});
```

### Python pytest
```python
import pytest
import requests

API_URL = 'https://api.example.com'
TOKEN = 'YOUR_TEST_TOKEN'

@pytest.fixture
def headers():
    return {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }

def test_get_users(headers):
    response = requests.get(f'{API_URL}/api/users', headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_user_by_id(headers):
    response = requests.get(f'{API_URL}/api/users/123', headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == '123'
    assert 'name' in data
    assert 'email' in data

def test_create_user(headers):
    user_data = {
        'name': 'Test User',
        'email': 'test@example.com'
    }

    response = requests.post(
        f'{API_URL}/api/users',
        json=user_data,
        headers=headers
    )

    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert data['name'] == user_data['name']

def test_unauthorized_access():
    response = requests.get(f'{API_URL}/api/users')
    assert response.status_code == 401
```

## Postman Collection

### Collection Structure
```json
{
  "info": {
    "name": "API Test Collection",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "auth": {
    "type": "bearer",
    "bearer": [
      {
        "key": "token",
        "value": "{{access_token}}",
        "type": "string"
      }
    ]
  },
  "item": [
    {
      "name": "Users",
      "item": [
        {
          "name": "Get All Users",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{base_url}}/api/users?page=1&limit=10",
              "host": ["{{base_url}}"],
              "path": ["api", "users"],
              "query": [
                { "key": "page", "value": "1" },
                { "key": "limit", "value": "10" }
              ]
            }
          },
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "pm.test('Status code is 200', function () {",
                  "    pm.response.to.have.status(200);",
                  "});",
                  "",
                  "pm.test('Response is array', function () {",
                  "    var jsonData = pm.response.json();",
                  "    pm.expect(jsonData).to.be.an('array');",
                  "});"
                ]
              }
            }
          ]
        },
        {
          "name": "Create User",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"name\": \"{{$randomFullName}}\",\n  \"email\": \"{{$randomEmail}}\",\n  \"role\": \"user\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/api/users",
              "host": ["{{base_url}}"],
              "path": ["api", "users"]
            }
          },
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "pm.test('Status code is 201', function () {",
                  "    pm.response.to.have.status(201);",
                  "});",
                  "",
                  "pm.test('User has ID', function () {",
                  "    var jsonData = pm.response.json();",
                  "    pm.expect(jsonData).to.have.property('id');",
                  "    pm.environment.set('user_id', jsonData.id);",
                  "});"
                ]
              }
            }
          ]
        }
      ]
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "https://api.example.com"
    }
  ]
}
```

## Load Testing

### Using Apache Bench
```bash
# 1000 requests, 10 concurrent
ab -n 1000 -c 10 -H "Authorization: Bearer TOKEN" \
  https://api.example.com/api/users

# POST request with JSON
ab -n 1000 -c 10 -p data.json -T application/json \
  -H "Authorization: Bearer TOKEN" \
  https://api.example.com/api/users
```

### Using Artillery
```yaml
# artillery.yml
config:
  target: 'https://api.example.com'
  phases:
    - duration: 60
      arrivalRate: 10
      name: Warm up
    - duration: 300
      arrivalRate: 50
      name: Sustained load
  defaults:
    headers:
      Authorization: 'Bearer YOUR_TOKEN'

scenarios:
  - name: "Get users"
    flow:
      - get:
          url: "/api/users"
          expect:
            - statusCode: 200
      - think: 1
      - post:
          url: "/api/users"
          json:
            name: "Test User"
            email: "test@example.com"
          expect:
            - statusCode: 201
```

```bash
# Run load test
artillery run artillery.yml

# Generate HTML report
artillery run artillery.yml --output report.json
artillery report report.json --output report.html
```

## Response Validation

### Schema Validation
```javascript
const Ajv = require('ajv');
const ajv = new Ajv();

// Define schema
const userSchema = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    name: { type: 'string' },
    email: { type: 'string', format: 'email' },
    role: { type: 'string', enum: ['user', 'admin'] },
    createdAt: { type: 'string', format: 'date-time' }
  },
  required: ['id', 'name', 'email', 'role']
};

const validate = ajv.compile(userSchema);

// Validate response
async function testUserAPI() {
  const response = await fetch('https://api.example.com/api/users/123');
  const data = await response.json();

  const valid = validate(data);
  if (!valid) {
    console.error('Validation errors:', validate.errors);
  } else {
    console.log('Response is valid!');
  }
}
```

## Best Practices

### Request Best Practices
- Always set appropriate `Content-Type` headers
- Use proper HTTP methods (GET for reads, POST for creates, etc.)
- Include authentication tokens securely
- Handle timeouts and retries
- Validate input before sending
- Use HTTPS for production APIs

### Response Handling
- Check status codes before parsing
- Handle errors gracefully
- Validate response schema
- Log requests and responses for debugging
- Implement exponential backoff for retries

### Security Testing
- Test with invalid tokens
- Test without authentication
- Attempt SQL injection in parameters
- Test XSS in input fields
- Verify CORS settings
- Test rate limiting

### Error Scenarios to Test
- Invalid authentication
- Missing required fields
- Invalid data types
- Duplicate resources
- Not found (404)
- Server errors (500)
- Rate limit exceeded (429)
- Network timeouts

## Common HTTP Status Codes

```
200 OK - Request successful
201 Created - Resource created
204 No Content - Success, no response body
400 Bad Request - Invalid request
401 Unauthorized - Missing/invalid authentication
403 Forbidden - Not allowed to access
404 Not Found - Resource doesn't exist
409 Conflict - Resource already exists
422 Unprocessable Entity - Validation failed
429 Too Many Requests - Rate limit exceeded
500 Internal Server Error - Server error
502 Bad Gateway - Upstream server error
503 Service Unavailable - Server overloaded
```

## Notes

- Always test in development/staging before production
- Use environment variables for API URLs and tokens
- Document all test cases and expected results
- Automate testing in CI/CD pipeline
- Monitor API performance and error rates
- Keep Postman collections updated
- Test edge cases and error scenarios
- Validate both success and failure paths
- Use proper authentication methods
- Never commit API keys or tokens to version control
