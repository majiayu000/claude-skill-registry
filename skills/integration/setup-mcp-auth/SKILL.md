---
name: setup-mcp-auth
description: Configure authentication for an existing FastMCP server
argument-hint: "[auth-type]"
---

# Setup MCP Authentication

Configure authentication and authorization for an existing FastMCP server.

## Usage

```bash
/setup-mcp-auth [auth-type]
```

## Arguments

- `[auth-type]`: Optional - Type of authentication (api-key, oauth, custom)

## Execution Instructions for Claude Code

When this command is run:

1. **Locate the FastMCP server** in the current project
2. **Determine authentication requirements**
3. **Configure authentication** based on selected type
4. **Add authorization rules** to tools if needed
5. **Generate environment configuration**

## Interactive Session Flow

### 1. Locate Server

```
Looking for FastMCP server...

Found: src/server.ts

Is this the correct server file? (yes/no):
```

### 2. Authentication Type

```
What type of authentication do you want to configure?

1. API Key - Simple header-based authentication
2. Role-Based - API key with user roles
3. OAuth 2.0 - Google or custom OAuth provider
4. JWT Validation - Validate external JWT tokens
5. Custom - Implement your own authentication logic

Select (1-5):
```

### 3. API Key Configuration

For API Key (option 1):
```
API Key Configuration

Header name for API key [default: x-api-key]:

How should API keys be stored?
1. Environment variable
2. Database lookup
3. Static configuration

Select (1-3):
```

### 4. Role-Based Configuration

For Role-Based (option 2):
```
Role-Based Authentication

What roles do you need?
Example: admin,user,readonly

Roles (comma-separated):
```

```
How are roles determined?
1. From request header (e.g., x-role)
2. From API key lookup
3. From JWT claims

Select (1-3):
```

### 5. OAuth Configuration

For OAuth 2.0 (option 3):
```
OAuth Provider

Which OAuth provider?
1. Google
2. GitHub (custom setup)
3. Custom OAuth provider

Select (1-3):
```

For Google:
```
Google OAuth Setup

You'll need:
- Google Cloud Console project
- OAuth 2.0 credentials (Client ID and Secret)
- Authorized redirect URIs configured

Base URL for your server:
Example: https://your-server.com

Base URL:
```

```
OAuth scopes (comma-separated):
Default: openid,profile,email

Scopes [press Enter for default]:
```

### 6. JWT Validation

For JWT (option 4):
```
JWT Validation Setup

JWKS URI (JSON Web Key Set endpoint):
Example: https://auth.example.com/.well-known/jwks.json

JWKS URI:
```

```
Token issuer (iss claim):
Example: https://auth.example.com

Issuer:
```

```
Expected audience (aud claim):
Example: mcp://my-server

Audience:
```

### 7. Authorization Rules

```
Do you want to add authorization rules to existing tools?

1. Yes - Review and configure tool access
2. No - I'll add authorization manually

Select (1-2):
```

If yes:
```
Found tools:
1. tool-name-1
2. tool-name-2
3. tool-name-3

Which tools should be restricted? (comma-separated numbers, or 'all'):
```

```
For tool "tool-name-1", who can access?
1. Admin only
2. Specific roles (specify)
3. Authenticated users only
4. Custom logic (I'll implement)

Select:
```

## Generated Code Examples

### API Key Authentication

```typescript
const server = new FastMCP({
  name: "{{serverName}}",
  version: "{{version}}",
  authenticate: (request) => {
    const apiKey = request.headers["{{headerName}}"];

    if (!apiKey) {
      throw new Response(null, {
        status: 401,
        statusText: "API key required",
      });
    }

    // Validate API key
    const validKey = process.env.API_KEY;
    if (apiKey !== validKey) {
      throw new Response(null, {
        status: 401,
        statusText: "Invalid API key",
      });
    }

    return { authenticated: true };
  },
});
```

### Role-Based Authentication

```typescript
// Define session type with roles
interface SessionData {
  userId: string;
  role: "admin" | "user" | "readonly";
}

const server = new FastMCP<SessionData>({
  name: "{{serverName}}",
  version: "{{version}}",
  authenticate: async (request) => {
    const apiKey = request.headers["x-api-key"];

    if (!apiKey) {
      throw new Response(null, {
        status: 401,
        statusText: "API key required",
      });
    }

    // Look up user by API key
    const user = await findUserByApiKey(apiKey);
    if (!user) {
      throw new Response(null, {
        status: 401,
        statusText: "Invalid API key",
      });
    }

    return {
      userId: user.id,
      role: user.role,
    };
  },
});

// Admin-only tool
server.addTool({
  name: "admin-dashboard",
  description: "Admin-only dashboard access",
  canAccess: (auth) => auth?.role === "admin",
  execute: async (args, { session }) => {
    return "Welcome admin " + session.userId;
  },
});

// Tool for admin and user roles
server.addTool({
  name: "edit-content",
  description: "Edit content",
  canAccess: (auth) => auth?.role === "admin" || auth?.role === "user",
  execute: async (args) => {
    return "Content edited";
  },
});

// Read-only accessible to all authenticated users
server.addTool({
  name: "view-content",
  description: "View content",
  execute: async (args) => {
    return "Content here";
  },
});
```

### OAuth with Google Provider

```typescript
import { FastMCP } from "fastmcp";
import { GoogleProvider } from "fastmcp/auth";

// Set up Google OAuth provider
const authProxy = new GoogleProvider({
  clientId: process.env.GOOGLE_CLIENT_ID!,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
  baseUrl: "{{baseUrl}}",
  scopes: [{{#each scopes}}"{{this}}"{{#unless @last}}, {{/unless}}{{/each}}],
});

interface SessionData {
  email: string;
  name: string;
}

const server = new FastMCP<SessionData>({
  name: "{{serverName}}",
  version: "{{version}}",
  oauth: {
    enabled: true,
    authorizationServer: authProxy.getAuthorizationServerMetadata(),
    proxy: authProxy,
  },
  authenticate: async (request) => {
    // OAuth tokens are validated by the proxy
    // Extract user info from the validated session
    const userInfo = await authProxy.getUserInfo(request);

    return {
      email: userInfo.email,
      name: userInfo.name,
    };
  },
});

// Access user info in tools
server.addTool({
  name: "whoami",
  description: "Get current user info",
  execute: async (args, { session }) => {
    return "Logged in as: " + session.name + " (" + session.email + ")";
  },
});
```

### JWT Validation

```typescript
import { FastMCP, DiscoveryDocumentCache } from "fastmcp";
import { buildGetJwks } from "get-jwks";
import fastJwt from "fast-jwt";

// Cache for OIDC discovery documents
const discoveryCache = new DiscoveryDocumentCache({
  ttl: 3600000, // 1 hour
});

interface SessionData {
  userId: string;
  email?: string;
  scope?: string;
}

const server = new FastMCP<SessionData>({
  name: "{{serverName}}",
  version: "{{version}}",
  oauth: {
    enabled: true,
    authorizationServer: {
      issuer: "{{issuer}}",
      authorizationEndpoint: "{{issuer}}/oauth/authorize",
      tokenEndpoint: "{{issuer}}/oauth/token",
      jwksUri: "{{jwksUri}}",
      responseTypesSupported: ["code"],
    },
    protectedResource: {
      resource: "{{audience}}",
      authorizationServers: ["{{issuer}}"],
    },
  },
  authenticate: async (request) => {
    const authHeader = request.headers.authorization;

    if (!authHeader?.startsWith("Bearer ")) {
      throw new Response(null, {
        status: 401,
        statusText: "Missing or invalid authorization header",
      });
    }

    const token = authHeader.slice(7);

    try {
      // Get JWKS for token validation
      const getJwks = buildGetJwks({
        jwksUrl: "{{jwksUri}}",
        cache: true,
        rateLimit: true,
      });

      // Create JWT verifier
      const verify = fastJwt.createVerifier({
        key: async (token) => {
          const { header } = fastJwt.decode(token, { complete: true });
          const jwk = await getJwks.getJwk({
            kid: header.kid,
            alg: header.alg,
          });
          return jwk;
        },
        algorithms: ["RS256", "ES256"],
        issuer: "{{issuer}}",
        audience: "{{audience}}",
      });

      // Validate token
      const payload = await verify(token);

      return {
        userId: payload.sub,
        email: payload.email,
        scope: payload.scope,
      };
    } catch (error) {
      throw new Response(null, {
        status: 401,
        statusText: "Invalid token",
      });
    }
  },
});
```

### Custom Authentication

```typescript
interface SessionData {
  userId: string;
  permissions: string[];
}

const server = new FastMCP<SessionData>({
  name: "{{serverName}}",
  version: "{{version}}",
  authenticate: async (request) => {
    // Implement your custom authentication logic
    const token = request.headers["authorization"]?.replace("Bearer ", "");

    if (!token) {
      throw new Response(null, {
        status: 401,
        statusText: "Authentication required",
      });
    }

    // Validate token and get user info
    const user = await validateToken(token);
    if (!user) {
      throw new Response(null, {
        status: 401,
        statusText: "Invalid token",
      });
    }

    return {
      userId: user.id,
      permissions: user.permissions,
    };
  },
});

// Permission-based access control
server.addTool({
  name: "protected-action",
  description: "Requires specific permission",
  canAccess: (auth) => auth?.permissions.includes("action:execute"),
  execute: async () => {
    return "Action executed";
  },
});
```

### Passing Headers to Tools

```typescript
import { IncomingHttpHeaders } from "http";

interface SessionData {
  headers: IncomingHttpHeaders;
  userId?: string;
}

const server = new FastMCP<SessionData>({
  name: "{{serverName}}",
  version: "{{version}}",
  authenticate: async (request) => {
    // Pass headers through for use in tools
    return {
      headers: request.headers,
      userId: request.headers["x-user-id"] as string,
    };
  },
});

server.addTool({
  name: "check-headers",
  description: "Access request headers",
  execute: async (args, { session }) => {
    const userAgent = session.headers["user-agent"] || "Unknown";
    return "User-Agent: " + userAgent;
  },
});
```

## Environment File Generation

Create `.env.example`:

```bash
# API Key Authentication
API_KEY=your-api-key-here

# OAuth (Google)
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret

# JWT Validation
JWT_ISSUER=https://auth.example.com
JWT_AUDIENCE=mcp://my-server
JWKS_URI=https://auth.example.com/.well-known/jwks.json
```

## Implementation Notes

1. **Find existing server**: Locate and analyze FastMCP server configuration
2. **Backup current code**: Create backup before modifying
3. **Update server config**: Add authenticate function and oauth config
4. **Add type definitions**: Create SessionData interface
5. **Update tools**: Add canAccess to restricted tools
6. **Generate .env.example**: Create environment template
7. **Add dependencies**: Install required packages (get-jwks, fast-jwt for JWT)
8. **Summary**: Show configuration and next steps
