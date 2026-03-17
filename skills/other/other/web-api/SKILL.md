---
name: web-api
cluster: web-dev
description: "REST + GraphQL + tRPC API design: OpenAPI 3.1, auth JWT/OAuth2, rate limiting, pagination"
tags: ["api","rest","graphql","trpc","web"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "api rest graphql design openapi jwt oauth rate limit trpc"
---

# web-api

## Purpose
This skill enables OpenClaw to design and implement web APIs using REST, GraphQL, and tRPC, focusing on OpenAPI 3.1 specifications, JWT/OAuth2 authentication, rate limiting, and pagination. Use it to generate secure, scalable API blueprints and code snippets for web applications.

## When to Use
Apply this skill when building backend services that require API endpoints, such as creating a user authentication system or fetching paginated data. Use it for projects involving RESTful architectures, GraphQL queries, or tRPC procedures, especially if you need to enforce rate limits or handle authentication.

## Key Capabilities
- Design REST APIs with OpenAPI 3.1: Generate schemas using `openapi-generator` CLI with flags like `--input spec.yaml --generator spring`.
- Implement GraphQL APIs: Define schemas with types and resolvers, e.g., using Apollo Server config: `const typeDefs = gql`query { users }`;`.
- Handle tRPC procedures: Create typed endpoints, e.g., `export const appRouter = router({ hello: publicProcedure.query(() => 'world') });`.
- Authentication: Enforce JWT or OAuth2 via middleware; set env var `$WEB_API_JWT_SECRET` for token signing.
- Rate limiting: Apply limits using libraries like `express-rate-limit` with options `{ windowMs: 15*60*1000, max: 100 }`.
- Pagination: Implement cursor-based or offset pagination in queries, e.g., `query { users(first: 10, after: "cursor") }`.

## Usage Patterns
To design a REST API, invoke this skill with: `openclaw run web-api --design rest --spec openapi.yaml`. For GraphQL, use: `openclaw run web-api --type graphql --schema schema.graphql`. Always include auth by setting `$WEB_API_OAUTH_CLIENT_ID` and `$WEB_API_OAUTH_CLIENT_SECRET`. For tRPC, specify: `openclaw run web-api --type trpc --router path/to/router.ts`. Include rate limiting by adding `--rate-limit 100:15m`. Example 1: To create a paginated user endpoint, run `openclaw run web-api --design rest --endpoint /users --paginate offset:10` then integrate the generated code. Example 2: For a secured GraphQL query, use `openclaw run web-api --type graphql --auth jwt --query "query { protectedData }"`, which outputs a resolver with JWT validation.

## Common Commands/API
- CLI Command: `openclaw run web-api --cluster web-dev --action generate --format openapi` to create an OpenAPI spec file.
- API Endpoint: Simulate requests like `POST /api/v1/login` with body `{ "username": "user", "password": "pass" }` and header `Authorization: Bearer $WEB_API_JWT_TOKEN`.
- Code Snippet: For REST server setup: `app.use(express.json()); app.get('/api/items', (req, res) => res.json(items));`.
- Code Snippet: For GraphQL: `const server = new ApolloServer({ typeDefs, resolvers }); server.listen();`.
- Config Format: Use YAML for OpenAPI, e.g., `openapi: 3.1.0 info: title: API paths: /users: get: parameters: - name: page in: query schema: type: integer`.
- tRPC Example: `import { initTRPC } from '@trpc/server'; const t = initTRPC.create(); export const router = t.router({});`.

## Integration Notes
Integrate this skill with other OpenClaw skills by chaining commands, e.g., `openclaw run web-api --output code.js; openclaw run database --import code.js`. For auth, ensure `$WEB_API_API_KEY` is set in your environment before running. Use it with frontend skills by exporting APIs as JSON schemas for React components. Handle dependencies by installing via `npm install express graphql @trpc/server`, and configure rate limiting in the generated code with `app.use(rateLimit({ max: 100 }));`. Test integrations with tools like Postman by importing the OpenAPI spec.

## Error Handling
When errors occur, check for common issues like invalid JWTs by catching exceptions: `try { jwt.verify(token, process.env.WEB_API_JWT_SECRET); } catch (err) { res.status(401).send('Invalid token'); }`. For rate limiting, return 429 responses with a retry-after header. Use OpenClaw's error logging: `openclaw log error --message "API rate limit exceeded" --skill web-api`. Parse API errors from responses, e.g., if status is 400, extract the error body like `{ error: 'Bad request' }`. Always wrap API calls in try-catch blocks and use env vars for sensitive data to avoid exposure.

## Graph Relationships
- Related to: "frontend" skill for UI-to-API integration.
- Connected to: "database" skill for querying data sources in APIs.
- Links with: "auth" skill for shared JWT/OAuth2 implementations.
- Associated with: "deployment" skill for hosting API servers.
