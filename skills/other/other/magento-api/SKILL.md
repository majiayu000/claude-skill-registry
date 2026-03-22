---
name: magento-api
description: Build Magento 2 REST and GraphQL APIs — webapi.xml, schema.graphqls, resolvers, authentication, and ACL. Use when creating custom API endpoints, extending the GraphQL schema, or integrating external systems.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# Magento 2 REST & GraphQL API Development

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.adobe.com/commerce/webapi/` for Web API overview
2. Fetch `https://developer.adobe.com/commerce/webapi/graphql/develop/` for GraphQL development guide
3. Fetch `https://developer.adobe.com/commerce/webapi/get-started/authentication/gs-authentication-token/` for authentication
4. Web-search `site:developer.adobe.com commerce php development components web-api` for webapi.xml reference

## REST API

### How It Works

REST endpoints map HTTP methods + URL paths to service contract methods. Defined in `etc/webapi.xml`.

### webapi.xml Structure

Each route defines:
- `url` — endpoint path (e.g., `/V1/custom/items/:id`)
- `method` — HTTP method (GET, POST, PUT, DELETE)
- `service` — class + method implementing the endpoint
- `resource` — ACL resource for authorization

Path parameters (`:id`) map to method parameters by name.

### Authentication Types

| Type | Header | Use Case |
|------|--------|----------|
| **Admin Token** | `Authorization: Bearer <token>` | Back-office integrations |
| **Customer Token** | `Authorization: Bearer <token>` | Customer-facing apps |
| **OAuth 1.0a** | OAuth headers | Third-party integrations |
| **Session** | PHP session cookie | Storefront JS widgets |
| **Anonymous** | `resource="anonymous"` | Public endpoints |

### Swagger/OpenAPI

Available at `/rest/<store>/schema` — auto-generated from webapi.xml and service contracts.

## GraphQL API

### How It Works

GraphQL uses a single endpoint (`/graphql`) with schema files and resolver classes.

### Schema Files (schema.graphqls)

Define types, queries, and mutations in `etc/schema.graphqls`:
- Custom types with fields
- Query definitions mapping to resolver classes
- Mutation definitions with input/output types
- Extend existing types with new fields

### Resolver Classes

Implement `Magento\Framework\GraphQl\Query\ResolverInterface`:
- `resolve(Field $field, $context, ResolveInfo $info, array $value = null, array $args = null)`
- Return arrays matching the GraphQL type definition
- Context provides store, customer, and extension attributes

### Identity for Cache

Implement `Magento\Framework\GraphQl\Query\Resolver\IdentityInterface` for full-page cache invalidation of GraphQL responses.

### GraphQL Authorization

- Customer context via `Authorization: Bearer <customer-token>` header
- Admin context not supported in GraphQL (by design — GraphQL is storefront-facing)
- Use `$context->getExtensionAttributes()->getIsCustomer()` for auth checks

## ACL (Access Control List)

### acl.xml

Defines the resource tree for authorization:
- Nested `<resource>` elements form a hierarchy
- Referenced in `webapi.xml` via `<resource ref="Vendor_Module::resource_name"/>`
- Special values: `anonymous` (no auth), `self` (customer's own data)

## Best Practices

- Always define service contract interfaces first, then expose via webapi.xml
- Use ACL resources for all non-public endpoints
- Prefer GraphQL for storefront/headless, REST for integrations
- Return proper HTTP status codes (200, 201, 400, 401, 403, 404)
- Use SearchCriteria for list endpoints
- Add cache identity classes for GraphQL resolver performance

Fetch the Web API and GraphQL development docs for exact XML schema, resolver signatures, and authentication patterns before implementing.
