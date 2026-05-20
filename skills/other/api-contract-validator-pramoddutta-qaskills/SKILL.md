---
name: API Contract Validator
description: Validate API responses against OpenAPI/Swagger specifications, JSON Schema definitions, and consumer-driven contracts to prevent breaking changes
version: 1.0.0
author: Pramod
license: MIT
tags: [api-contract, openapi, swagger, json-schema, contract-testing, schema-validation, api-compatibility, breaking-changes]
testingTypes: [contract, api]
frameworks: [postman, rest-assured]
languages: [typescript, javascript, python, java]
domains: [api]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# API Contract Validator Skill

You are an expert QA engineer specializing in API contract validation. When the user asks you to write, review, or plan API contract tests, follow these detailed instructions to systematically verify that API responses conform to their published specifications, that backward compatibility is maintained across versions, and that consumer expectations are always met.

## Core Principles

1. **Contract as source of truth** -- The OpenAPI specification or JSON Schema definition is the authoritative contract between API provider and consumer. Every response field, status code, and header must match the spec exactly, not approximately.
2. **Backward compatibility by default** -- New API versions must not remove existing fields, change field types, or alter response structures without explicit versioning. Additive changes are safe; subtractive changes break consumers.
3. **Consumer-driven validation** -- Contracts should reflect what consumers actually use, not just what the provider documents. Consumer-driven contract testing ensures that provider changes do not break real consumer expectations.
4. **Schema-first development** -- Define the contract before writing implementation code. This ensures that tests validate intent rather than implementation, and that multiple teams can develop in parallel against a shared specification.
5. **Fail fast on drift** -- Contract validation must run in CI on every commit. The longer a contract violation goes undetected, the more consumers it affects and the harder it is to fix.
6. **Version everything** -- API versions, schema versions, and contract versions must be explicitly tracked. Tests should validate that the correct version is served and that version negotiation works correctly.
7. **Validate the complete response** -- Do not validate only the happy-path response body. Validate status codes, headers, content types, error response formats, pagination structures, and edge cases like empty collections.

## Project Structure

```
tests/
  contracts/
    openapi/
      validate-responses.spec.ts     # Validate responses against OpenAPI spec
      validate-request.spec.ts       # Validate request schemas
      backward-compat.spec.ts        # Backward compatibility checks
    json-schema/
      schema-validation.spec.ts      # JSON Schema validation tests
      schema-evolution.spec.ts       # Schema change detection
    consumer-driven/
      consumer-contracts.spec.ts     # Consumer-driven contract tests
      pact-provider.spec.ts          # Pact provider verification
    graphql/
      schema-validation.spec.ts      # GraphQL schema validation
      breaking-changes.spec.ts       # GraphQL breaking change detection
    fixtures/
      api-client.ts                  # Typed API client helper
      schema-loader.ts              # Load and parse OpenAPI specs
      contract-helpers.ts           # Contract validation utilities
    specs/
      openapi.yaml                  # OpenAPI 3.x specification
      schemas/                      # JSON Schema definitions
        user.schema.json
        document.schema.json
        error.schema.json
  playwright.config.ts
```

## Configuration

```typescript
// tests/contracts/fixtures/schema-loader.ts
import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

export interface OpenAPISpec {
  openapi: string;
  info: { title: string; version: string };
  paths: Record<string, Record<string, PathOperation>>;
  components: { schemas: Record<string, JSONSchema> };
}

export interface PathOperation {
  operationId: string;
  summary?: string;
  parameters?: ParameterObject[];
  requestBody?: RequestBodyObject;
  responses: Record<string, ResponseObject>;
}

export interface JSONSchema {
  type?: string;
  properties?: Record<string, JSONSchema>;
  required?: string[];
  items?: JSONSchema;
  enum?: unknown[];
  format?: string;
  minimum?: number;
  maximum?: number;
  minLength?: number;
  maxLength?: number;
  pattern?: string;
  additionalProperties?: boolean | JSONSchema;
}

interface ParameterObject {
  name: string;
  in: string;
  required?: boolean;
  schema: JSONSchema;
}

interface RequestBodyObject {
  required?: boolean;
  content: Record<string, { schema: JSONSchema }>;
}

interface ResponseObject {
  description: string;
  content?: Record<string, { schema: JSONSchema }>;
  headers?: Record<string, { schema: JSONSchema }>;
}

export function loadOpenAPISpec(specPath: string): OpenAPISpec {
  const content = fs.readFileSync(specPath, 'utf-8');
  if (specPath.endsWith('.yaml') || specPath.endsWith('.yml')) {
    return yaml.load(content) as OpenAPISpec;
  }
  return JSON.parse(content);
}

export function loadJSONSchema(schemaPath: string): JSONSchema {
  const content = fs.readFileSync(schemaPath, 'utf-8');
  return JSON.parse(content);
}

export function getResponseSchema(
  spec: OpenAPISpec,
  path: string,
  method: string,
  statusCode: string
): JSONSchema | null {
  const pathObj = spec.paths[path];
  if (!pathObj) return null;

  const operation = pathObj[method.toLowerCase()];
  if (!operation) return null;

  const response = operation.responses[statusCode] || operation.responses['default'];
  if (!response?.content) return null;

  const jsonContent = response.content['application/json'];
  return jsonContent?.schema || null;
}
```

```typescript
// tests/contracts/fixtures/contract-helpers.ts
import Ajv, { ErrorObject } from 'ajv';
import addFormats from 'ajv-formats';
import { JSONSchema } from './schema-loader';

const ajv = new Ajv({ allErrors: true, strict: false });
addFormats(ajv);

export interface ValidationResult {
  valid: boolean;
  errors: ErrorObject[] | null;
  summary: string;
}

export function validateAgainstSchema(
  data: unknown,
  schema: JSONSchema
): ValidationResult {
  const validate = ajv.compile(schema);
  const valid = validate(data) as boolean;

  return {
    valid,
    errors: validate.errors || null,
    summary: valid
      ? 'Response matches schema'
      : `Schema violations: ${(validate.errors || [])
          .map((e) => `${e.instancePath} ${e.message}`)
          .join('; ')}`,
  };
}

export function checkBackwardCompatibility(
  oldSchema: JSONSchema,
  newSchema: JSONSchema
): { compatible: boolean; breakingChanges: string[] } {
  const breakingChanges: string[] = [];

  // Check for removed required fields
  const oldRequired = new Set(oldSchema.required || []);
  const newRequired = new Set(newSchema.required || []);
  const oldProperties = oldSchema.properties || {};
  const newProperties = newSchema.properties || {};

  // Removed properties that were in old schema
  for (const prop of Object.keys(oldProperties)) {
    if (!(prop in newProperties)) {
      breakingChanges.push(`Removed property: "${prop}"`);
    }
  }

  // Type changes on existing properties
  for (const [prop, oldPropSchema] of Object.entries(oldProperties)) {
    if (prop in newProperties) {
      const newPropSchema = newProperties[prop];
      if (oldPropSchema.type !== newPropSchema.type) {
        breakingChanges.push(
          `Type changed for "${prop}": ${oldPropSchema.type} -> ${newPropSchema.type}`
        );
      }
    }
  }

  // New required fields (breaking for existing consumers)
  for (const field of newRequired) {
    if (!oldRequired.has(field)) {
      breakingChanges.push(`New required field added: "${field}"`);
    }
  }

  // Enum value removal
  for (const [prop, oldPropSchema] of Object.entries(oldProperties)) {
    if (prop in newProperties && oldPropSchema.enum && newProperties[prop].enum) {
      const removedValues = oldPropSchema.enum.filter(
        (v) => !newProperties[prop].enum!.includes(v)
      );
      if (removedValues.length > 0) {
        breakingChanges.push(
          `Enum values removed from "${prop}": ${removedValues.join(', ')}`
        );
      }
    }
  }

  return {
    compatible: breakingChanges.length === 0,
    breakingChanges,
  };
}
```

## OpenAPI Response Validation

```typescript
// tests/contracts/openapi/validate-responses.spec.ts
import { test, expect } from '@playwright/test';
import { loadOpenAPISpec, getResponseSchema } from '../fixtures/schema-loader';
import { validateAgainstSchema } from '../fixtures/contract-helpers';
import * as path from 'path';

const spec = loadOpenAPISpec(path.resolve(__dirname, '../specs/openapi.yaml'));

test.describe('OpenAPI Response Validation', () => {
  test('GET /api/users returns response matching spec', async ({ request }) => {
    const response = await request.get('/api/users');
    const status = response.status().toString();
    const body = await response.json();

    const schema = getResponseSchema(spec, '/api/users', 'get', status);
    expect(schema, `No schema found for GET /api/users ${status}`).not.toBeNull();

    const result = validateAgainstSchema(body, schema!);
    expect(result.valid, result.summary).toBe(true);
  });

  test('GET /api/users/:id returns response matching spec', async ({ request }) => {
    const response = await request.get('/api/users/1');
    const status = response.status().toString();
    const body = await response.json();

    const schema = getResponseSchema(spec, '/api/users/{id}', 'get', status);
    expect(schema).not.toBeNull();

    const result = validateAgainstSchema(body, schema!);
    expect(result.valid, result.summary).toBe(true);
  });

  test('POST /api/users error response matches error schema', async ({ request }) => {
    // Send invalid data to trigger validation error
    const response = await request.post('/api/users', {
      data: { invalid: 'payload' },
    });
    const status = response.status().toString();
    const body = await response.json();

    const schema = getResponseSchema(spec, '/api/users', 'post', status);
    if (schema) {
      const result = validateAgainstSchema(body, schema);
      expect(result.valid, result.summary).toBe(true);
    }

    // Verify standard error format
    expect(body).toHaveProperty('error');
    expect(typeof body.error).toBe('object');
    if (body.error) {
      expect(body.error).toHaveProperty('message');
      expect(typeof body.error.message).toBe('string');
    }
  });

  test('response content-type matches spec', async ({ request }) => {
    const response = await request.get('/api/users');
    const contentType = response.headers()['content-type'];

    expect(contentType).toContain('application/json');
  });

  test('pagination response structure matches spec', async ({ request }) => {
    const response = await request.get('/api/users?page=1&limit=10');
    const body = await response.json();

    // Standard pagination contract
    expect(body).toHaveProperty('data');
    expect(Array.isArray(body.data)).toBe(true);
    expect(body).toHaveProperty('pagination');
    expect(body.pagination).toHaveProperty('page');
    expect(body.pagination).toHaveProperty('limit');
    expect(body.pagination).toHaveProperty('total');
    expect(body.pagination).toHaveProperty('totalPages');

    expect(typeof body.pagination.page).toBe('number');
    expect(typeof body.pagination.limit).toBe('number');
    expect(typeof body.pagination.total).toBe('number');
    expect(typeof body.pagination.totalPages).toBe('number');
  });

  test('validate all documented endpoints return conforming responses', async ({ request }) => {
    const violations: string[] = [];

    for (const [pathTemplate, pathObj] of Object.entries(spec.paths)) {
      for (const [method, operation] of Object.entries(pathObj)) {
        if (['get'].includes(method)) {
          // Replace path parameters with test values
          const resolvedPath = pathTemplate.replace(/{(\w+)}/g, '1');

          try {
            const response = await request.get(resolvedPath);
            const status = response.status().toString();
            const body = await response.json().catch(() => null);

            if (body) {
              const schema = getResponseSchema(spec, pathTemplate, method, status);
              if (schema) {
                const result = validateAgainstSchema(body, schema);
                if (!result.valid) {
                  violations.push(
                    `${method.toUpperCase()} ${pathTemplate} (${status}): ${result.summary}`
                  );
                }
              }
            }
          } catch (error) {
            // Skip unreachable endpoints
          }
        }
      }
    }

    expect(
      violations,
      `Contract violations found:\n${violations.join('\n')}`
    ).toHaveLength(0);
  });
});
```

## JSON Schema Validation

```typescript
// tests/contracts/json-schema/schema-validation.spec.ts
import { test, expect } from '@playwright/test';
import { loadJSONSchema } from '../fixtures/schema-loader';
import { validateAgainstSchema } from '../fixtures/contract-helpers';
import * as path from 'path';

const userSchema = loadJSONSchema(
  path.resolve(__dirname, '../specs/schemas/user.schema.json')
);

const errorSchema = loadJSONSchema(
  path.resolve(__dirname, '../specs/schemas/error.schema.json')
);

test.describe('JSON Schema Validation', () => {
  test('user object conforms to user schema', async ({ request }) => {
    const response = await request.get('/api/users/1');
    expect(response.status()).toBe(200);

    const user = await response.json();
    const result = validateAgainstSchema(user, userSchema);
    expect(result.valid, result.summary).toBe(true);
  });

  test('user list items all conform to user schema', async ({ request }) => {
    const response = await request.get('/api/users');
    expect(response.status()).toBe(200);

    const body = await response.json();
    const users = body.data || body;

    for (let i = 0; i < users.length; i++) {
      const result = validateAgainstSchema(users[i], userSchema);
      expect(result.valid, `User at index ${i}: ${result.summary}`).toBe(true);
    }
  });

  test('error responses conform to error schema', async ({ request }) => {
    const response = await request.get('/api/users/nonexistent-id');

    if (response.status() >= 400) {
      const error = await response.json();
      const result = validateAgainstSchema(error, errorSchema);
      expect(result.valid, result.summary).toBe(true);
    }
  });

  test('required fields are always present', async ({ request }) => {
    const response = await request.get('/api/users/1');
    const user = await response.json();

    const requiredFields = userSchema.required || [];
    for (const field of requiredFields) {
      expect(
        user,
        `Required field "${field}" is missing from user response`
      ).toHaveProperty(field);
    }
  });

  test('field types match schema definitions', async ({ request }) => {
    const response = await request.get('/api/users/1');
    const user = await response.json();
    const properties = userSchema.properties || {};

    for (const [field, fieldSchema] of Object.entries(properties)) {
      if (user[field] !== undefined && user[field] !== null) {
        switch (fieldSchema.type) {
          case 'string':
            expect(typeof user[field], `${field} should be string`).toBe('string');
            break;
          case 'number':
          case 'integer':
            expect(typeof user[field], `${field} should be number`).toBe('number');
            break;
          case 'boolean':
            expect(typeof user[field], `${field} should be boolean`).toBe('boolean');
            break;
          case 'array':
            expect(Array.isArray(user[field]), `${field} should be array`).toBe(true);
            break;
          case 'object':
            expect(typeof user[field], `${field} should be object`).toBe('object');
            break;
        }
      }
    }
  });

  test('string format constraints are enforced', async ({ request }) => {
    const response = await request.get('/api/users/1');
    const user = await response.json();
    const properties = userSchema.properties || {};

    for (const [field, fieldSchema] of Object.entries(properties)) {
      if (user[field] && fieldSchema.type === 'string') {
        if (fieldSchema.format === 'email') {
          expect(user[field]).toMatch(/^[^\s@]+@[^\s@]+\.[^\s@]+$/);
        }
        if (fieldSchema.format === 'date-time') {
          expect(new Date(user[field]).toISOString()).toBeTruthy();
        }
        if (fieldSchema.format === 'uri') {
          expect(() => new URL(user[field])).not.toThrow();
        }
        if (fieldSchema.minLength) {
          expect(user[field].length).toBeGreaterThanOrEqual(fieldSchema.minLength);
        }
        if (fieldSchema.maxLength) {
          expect(user[field].length).toBeLessThanOrEqual(fieldSchema.maxLength);
        }
      }
    }
  });
});
```

## Backward Compatibility Testing

```typescript
// tests/contracts/openapi/backward-compat.spec.ts
import { test, expect } from '@playwright/test';
import { loadOpenAPISpec } from '../fixtures/schema-loader';
import { checkBackwardCompatibility } from '../fixtures/contract-helpers';
import * as path from 'path';

test.describe('Backward Compatibility', () => {
  test('current schema is backward compatible with previous version', () => {
    const previousSpec = loadOpenAPISpec(
      path.resolve(__dirname, '../specs/openapi-v1.yaml')
    );
    const currentSpec = loadOpenAPISpec(
      path.resolve(__dirname, '../specs/openapi.yaml')
    );

    const schemasToCheck = ['User', 'Document', 'Error'];

    for (const schemaName of schemasToCheck) {
      const oldSchema = previousSpec.components.schemas[schemaName];
      const newSchema = currentSpec.components.schemas[schemaName];

      if (oldSchema && newSchema) {
        const result = checkBackwardCompatibility(oldSchema, newSchema);
        expect(
          result.compatible,
          `Breaking changes in ${schemaName}:\n${result.breakingChanges.join('\n')}`
        ).toBe(true);
      }
    }
  });

  test('API version header is present and correct', async ({ request }) => {
    const response = await request.get('/api/users');
    const apiVersion = response.headers()['api-version'] ||
      response.headers()['x-api-version'];

    expect(apiVersion).toBeDefined();
    expect(apiVersion).toMatch(/^\d+\.\d+\.\d+$/);
  });

  test('deprecated fields still present but marked', async ({ request }) => {
    const response = await request.get('/api/users/1');
    const body = await response.json();

    // If deprecated fields exist, they should still be present for backward compat
    const spec = loadOpenAPISpec(path.resolve(__dirname, '../specs/openapi.yaml'));
    const userSchema = spec.components.schemas['User'];

    if (userSchema?.properties) {
      for (const [field, fieldSchema] of Object.entries(userSchema.properties)) {
        if ((fieldSchema as Record<string, unknown>).deprecated) {
          // Deprecated fields should still be in the response
          expect(
            body,
            `Deprecated field "${field}" removed before deprecation period ended`
          ).toHaveProperty(field);
        }
      }
    }
  });

  test('new required fields are not added without version bump', async ({ request }) => {
    const v1Response = await request.get('/api/v1/users/1');
    const v2Response = await request.get('/api/v2/users/1');

    if (v1Response.status() === 200 && v2Response.status() === 200) {
      const v1Body = await v1Response.json();
      const v2Body = await v2Response.json();

      const v1Fields = new Set(Object.keys(v1Body));
      const v2Fields = new Set(Object.keys(v2Body));

      // All v1 fields must still exist in v2
      for (const field of v1Fields) {
        expect(
          v2Fields.has(field),
          `Field "${field}" from v1 is missing in v2`
        ).toBe(true);
      }
    }
  });
});
```

## Java REST Assured Contract Validation

```java
// src/test/java/contracts/ApiContractTest.java
package contracts;

import io.restassured.RestAssured;
import io.restassured.module.jsv.JsonSchemaValidator;
import io.restassured.response.Response;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;

public class ApiContractTest {

    @BeforeAll
    static void setup() {
        RestAssured.baseURI = System.getProperty("api.baseUrl", "http://localhost:3000");
    }

    @Test
    @DisplayName("GET /api/users response matches JSON Schema")
    void getUsersResponseMatchesSchema() {
        given()
            .header("Accept", "application/json")
        .when()
            .get("/api/users")
        .then()
            .statusCode(200)
            .contentType("application/json")
            .body(JsonSchemaValidator.matchesJsonSchemaInClasspath(
                "schemas/users-list-response.json"
            ));
    }

    @Test
    @DisplayName("GET /api/users/:id response matches User schema")
    void getUserByIdMatchesSchema() {
        given()
            .header("Accept", "application/json")
            .pathParam("id", 1)
        .when()
            .get("/api/users/{id}")
        .then()
            .statusCode(200)
            .contentType("application/json")
            .body(JsonSchemaValidator.matchesJsonSchemaInClasspath(
                "schemas/user.schema.json"
            ))
            .body("id", notNullValue())
            .body("email", matchesPattern("^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$"))
            .body("createdAt", matchesPattern(
                "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}"
            ));
    }

    @Test
    @DisplayName("Error responses follow standard error contract")
    void errorResponseFollowsContract() {
        given()
            .header("Accept", "application/json")
        .when()
            .get("/api/users/nonexistent")
        .then()
            .statusCode(anyOf(is(404), is(400)))
            .contentType("application/json")
            .body("error", notNullValue())
            .body("error.message", not(emptyOrNullString()))
            .body("error.code", notNullValue());
    }

    @Test
    @DisplayName("Pagination contract is consistent across endpoints")
    void paginationContractConsistency() {
        String[] paginatedEndpoints = {
            "/api/users",
            "/api/documents",
            "/api/reports"
        };

        for (String endpoint : paginatedEndpoints) {
            Response response = given()
                .queryParam("page", 1)
                .queryParam("limit", 10)
            .when()
                .get(endpoint);

            if (response.statusCode() == 200) {
                response.then()
                    .body("data", instanceOf(java.util.List.class))
                    .body("pagination.page", equalTo(1))
                    .body("pagination.limit", equalTo(10))
                    .body("pagination.total", instanceOf(Integer.class))
                    .body("pagination.totalPages", instanceOf(Integer.class));
            }
        }
    }

    @ParameterizedTest
    @ValueSource(strings = {"application/json", "application/xml"})
    @DisplayName("Content negotiation returns correct content type")
    void contentNegotiation(String acceptHeader) {
        Response response = given()
            .header("Accept", acceptHeader)
        .when()
            .get("/api/users");

        String contentType = response.getContentType();

        if (response.statusCode() == 200) {
            // If the API supports the requested format, it should return it
            assertThat(contentType, containsString(acceptHeader));
        } else if (response.statusCode() == 406) {
            // 406 Not Acceptable is the correct response for unsupported types
            assertThat(response.statusCode(), equalTo(406));
        }
    }

    @Test
    @DisplayName("Required response headers are present")
    void requiredHeadersPresent() {
        given()
            .header("Accept", "application/json")
        .when()
            .get("/api/users")
        .then()
            .statusCode(200)
            .header("Content-Type", containsString("application/json"))
            .header("X-Request-Id", notNullValue())
            .header("Cache-Control", notNullValue());
    }

    @Test
    @DisplayName("POST request validates required fields from schema")
    void postRequestValidation() {
        // Missing required fields should return 400 with specific validation errors
        given()
            .header("Content-Type", "application/json")
            .body("{\"invalid\": \"data\"}")
        .when()
            .post("/api/users")
        .then()
            .statusCode(anyOf(is(400), is(422)))
            .body("error.message", not(emptyOrNullString()));
    }

    @Test
    @DisplayName("Response field types match schema definitions")
    void responseFieldTypes() {
        given()
            .header("Accept", "application/json")
            .pathParam("id", 1)
        .when()
            .get("/api/users/{id}")
        .then()
            .statusCode(200)
            .body("id", anyOf(instanceOf(Integer.class), instanceOf(String.class)))
            .body("name", instanceOf(String.class))
            .body("email", instanceOf(String.class))
            .body("active", instanceOf(Boolean.class))
            .body("createdAt", instanceOf(String.class));
    }

    @Test
    @DisplayName("Null handling follows schema nullable definitions")
    void nullHandling() {
        Response response = given()
            .header("Accept", "application/json")
            .pathParam("id", 1)
        .when()
            .get("/api/users/{id}");

        if (response.statusCode() == 200) {
            // Non-nullable required fields should never be null
            response.then()
                .body("id", notNullValue())
                .body("email", notNullValue())
                .body("name", notNullValue());
        }
    }
}
```

## GraphQL Schema Validation

```typescript
// tests/contracts/graphql/schema-validation.spec.ts
import { test, expect } from '@playwright/test';

test.describe('GraphQL Schema Validation', () => {
  test('introspection returns expected types', async ({ request }) => {
    const response = await request.post('/graphql', {
      data: {
        query: `
          {
            __schema {
              types {
                name
                kind
              }
              queryType { name }
              mutationType { name }
            }
          }
        `,
      },
    });

    expect(response.status()).toBe(200);
    const body = await response.json();
    const typeNames = body.data.__schema.types.map(
      (t: { name: string }) => t.name
    );

    // Verify expected types exist
    expect(typeNames).toContain('User');
    expect(typeNames).toContain('Document');
    expect(typeNames).toContain('Query');
    expect(typeNames).toContain('Mutation');
  });

  test('query returns data matching declared return type', async ({ request }) => {
    const response = await request.post('/graphql', {
      data: {
        query: `
          query GetUser($id: ID!) {
            user(id: $id) {
              id
              name
              email
              createdAt
            }
          }
        `,
        variables: { id: '1' },
      },
    });

    expect(response.status()).toBe(200);
    const body = await response.json();

    expect(body.errors).toBeUndefined();
    expect(body.data.user).toBeDefined();
    expect(typeof body.data.user.id).toBe('string');
    expect(typeof body.data.user.name).toBe('string');
    expect(typeof body.data.user.email).toBe('string');
  });

  test('non-nullable fields never return null', async ({ request }) => {
    const response = await request.post('/graphql', {
      data: {
        query: `
          {
            __type(name: "User") {
              fields {
                name
                type {
                  kind
                  name
                  ofType {
                    kind
                    name
                  }
                }
              }
            }
          }
        `,
      },
    });

    const body = await response.json();
    const fields = body.data.__type?.fields || [];

    const nonNullableFields = fields
      .filter((f: Record<string, unknown>) => {
        const fieldType = f.type as { kind: string };
        return fieldType.kind === 'NON_NULL';
      })
      .map((f: Record<string, unknown>) => f.name as string);

    // Fetch actual data and verify non-nullable fields are not null
    const dataResponse = await request.post('/graphql', {
      data: {
        query: `{ users { ${nonNullableFields.join(' ')} } }`,
      },
    });

    const dataBody = await dataResponse.json();
    if (dataBody.data?.users) {
      for (const user of dataBody.data.users) {
        for (const field of nonNullableFields) {
          expect(
            user[field],
            `Non-nullable field "${field}" is null`
          ).not.toBeNull();
        }
      }
    }
  });

  test('deprecated fields trigger warnings but still work', async ({ request }) => {
    const schemaResponse = await request.post('/graphql', {
      data: {
        query: `
          {
            __type(name: "User") {
              fields(includeDeprecated: true) {
                name
                isDeprecated
                deprecationReason
              }
            }
          }
        `,
      },
    });

    const body = await schemaResponse.json();
    const deprecatedFields = body.data.__type?.fields?.filter(
      (f: Record<string, boolean>) => f.isDeprecated
    ) || [];

    for (const field of deprecatedFields) {
      expect(
        field.deprecationReason,
        `Deprecated field "${field.name}" should have a deprecation reason`
      ).toBeTruthy();

      // Verify deprecated field still returns data
      const queryResponse = await request.post('/graphql', {
        data: {
          query: `{ users { ${field.name} } }`,
        },
      });
      expect(queryResponse.status()).toBe(200);
    }
  });
});
```

## Content-Type and Error Response Contracts

```typescript
// tests/contracts/openapi/content-type-validation.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Content-Type and Error Response Contracts', () => {
  test('JSON responses have correct Content-Type header', async ({ request }) => {
    const response = await request.get('/api/users');
    const contentType = response.headers()['content-type'];
    expect(contentType).toMatch(/application\/json/);
  });

  test('error responses use consistent structure', async ({ request }) => {
    const errorEndpoints = [
      { path: '/api/users/nonexistent', expectedStatus: 404 },
      { path: '/api/nonexistent-endpoint', expectedStatus: 404 },
    ];

    for (const { path, expectedStatus } of errorEndpoints) {
      const response = await request.get(path);
      expect(response.status()).toBe(expectedStatus);

      const body = await response.json();
      expect(body).toHaveProperty('error');
      expect(body.error).toHaveProperty('message');
      expect(typeof body.error.message).toBe('string');
      expect(body.error.message.length).toBeGreaterThan(0);

      // Error should not contain stack traces in production
      expect(body.error).not.toHaveProperty('stack');
      expect(JSON.stringify(body)).not.toContain('at Object');
      expect(JSON.stringify(body)).not.toContain('node_modules');
    }
  });

  test('400 validation errors include field-level details', async ({ request }) => {
    const response = await request.post('/api/users', {
      data: { email: 'not-an-email', name: '' },
    });

    if (response.status() === 400 || response.status() === 422) {
      const body = await response.json();
      expect(body.error).toHaveProperty('message');

      // Should include validation details
      if (body.error.details) {
        expect(Array.isArray(body.error.details)).toBe(true);
        for (const detail of body.error.details) {
          expect(detail).toHaveProperty('field');
          expect(detail).toHaveProperty('message');
        }
      }
    }
  });

  test('API returns 406 for unsupported Accept headers', async ({ request }) => {
    const response = await request.get('/api/users', {
      headers: { Accept: 'application/xml' },
    });

    // Either serve JSON anyway or return 406
    if (response.status() === 406) {
      // Correct behavior for unsupported content type
    } else {
      const contentType = response.headers()['content-type'];
      expect(contentType).toContain('application/json');
    }
  });

  test('rate limit responses include retry headers', async ({ request }) => {
    // Make many rapid requests to trigger rate limiting
    let rateLimitResponse = null;
    for (let i = 0; i < 100; i++) {
      const response = await request.get('/api/users');
      if (response.status() === 429) {
        rateLimitResponse = response;
        break;
      }
    }

    if (rateLimitResponse) {
      const retryAfter = rateLimitResponse.headers()['retry-after'];
      const rateLimitRemaining =
        rateLimitResponse.headers()['x-ratelimit-remaining'];
      const rateLimitLimit =
        rateLimitResponse.headers()['x-ratelimit-limit'];

      expect(retryAfter || rateLimitRemaining).toBeDefined();
      if (rateLimitLimit) {
        expect(parseInt(rateLimitLimit)).toBeGreaterThan(0);
      }
    }
  });
});
```

## Best Practices

1. **Validate against the spec, not the implementation** -- Your contract tests should read the OpenAPI spec file and dynamically generate validations. If you hardcode expected fields in tests, you are testing your assumptions, not the contract.

2. **Use JSON Schema validators, not manual field checks** -- Libraries like AJV (TypeScript) and json-schema-validator (Java) provide comprehensive validation including nested objects, format constraints, and pattern matching. Manual checks miss edge cases.

3. **Test every documented status code** -- If your spec documents 200, 400, 404, and 500 responses, write tests that trigger each one and validate the response body against its respective schema.

4. **Run backward compatibility checks in CI** -- Keep the previous version of your spec in the repository and automatically compare it with the current version. Breaking changes should fail the build unless explicitly overridden.

5. **Validate error responses as rigorously as success responses** -- Error responses are part of the contract. Consumers depend on consistent error formats for error handling. An inconsistent error response is a contract violation.

6. **Test with real-world payloads** -- Use production-like data with unicode characters, empty strings, large numbers, deeply nested objects, and null values. Schema validation is only useful if it covers real edge cases.

7. **Version your schemas explicitly** -- Use schema version fields or API version headers. Tests should verify that the correct version is served and that version negotiation works properly.

8. **Validate response headers** -- Content-Type, Cache-Control, rate limit headers, and CORS headers are all part of the API contract. A missing Content-Type header can break consumers that rely on it.

9. **Generate client SDKs from the spec** -- If you can generate a type-safe client from your OpenAPI spec and the generated client works correctly with the API, your contract is accurate. This is the ultimate contract validation.

10. **Test nullable and optional field behavior** -- Verify that nullable fields can actually be null in responses, that optional fields can be omitted, and that required fields are always present regardless of the resource state.

11. **Include contract tests in provider CI and consumer CI** -- Providers run contract tests to verify they haven't broken the spec. Consumers run contract tests to verify their code handles the contract correctly. Both sides must validate.

12. **Document why each contract rule exists** -- When a contract test fails, the developer needs to know whether the test is wrong or the code is wrong. Comments explaining the business reason for each contract rule prevent accidental test removal.

## Anti-Patterns to Avoid

1. **Snapshot-based contract testing** -- Saving an API response as a JSON file and comparing future responses against it is brittle. Any additive change (new field) breaks the test even though it is not a breaking change. Use schema validation instead.

2. **Testing only with valid inputs** -- If you only send valid requests and check valid responses, you miss half the contract. Error responses, validation messages, and edge case behaviors are critical parts of the contract.

3. **Ignoring response headers in contract tests** -- Many developers validate only the response body. Headers like Content-Type, pagination links, rate limit info, and API version are contractual obligations that consumers depend on.

4. **Using production APIs for contract testing** -- Contract tests should run against a local or staging instance. Testing against production introduces flakiness from network issues and risks modifying production data.

5. **Maintaining contracts only in tests** -- If your OpenAPI spec lives only in test code, it is invisible to API consumers. The spec must be a shared artifact published to a spec portal or versioned alongside the codebase.

6. **Treating all field additions as non-breaking** -- While adding new response fields is generally safe, adding new required request fields or changing default values are breaking changes that contract tests must catch.

7. **Skipping contract tests for internal APIs** -- Internal APIs have consumers too. Other teams, microservices, and future developers depend on internal API contracts just as much as external consumers do.

## Debugging Tips

1. **Use Ajv verbose mode for schema failures** -- When a schema validation fails, the default error message may be cryptic. Configure AJV with `verbose: true` to see the actual data that failed validation alongside the expected schema.

2. **Diff specs visually** -- When backward compatibility tests fail, use tools like `openapi-diff` or `swagger-diff` to generate a human-readable diff between the old and new specs. This shows exactly what changed and whether it is breaking.

3. **Log full request and response** -- When a contract test fails unexpectedly, capture and log the complete HTTP request (method, URL, headers, body) and response (status, headers, body). The failure often becomes obvious once you see the raw data.

4. **Check content negotiation** -- If responses fail schema validation, verify that the client is sending the correct Accept header and that the server is returning the expected Content-Type. A mismatch can cause the server to return HTML instead of JSON.

5. **Validate the spec itself** -- Before running contract tests, validate your OpenAPI spec with a linter like `spectral` or `openapi-generator validate`. A malformed spec produces misleading test failures.

6. **Test with minimal and maximal payloads** -- Create test cases with only required fields (minimal) and all possible fields (maximal). This catches issues where optional fields are accidentally required or where extra fields cause parsing errors.

7. **Use test fixtures with known data** -- If contract tests depend on database state, use deterministic seed data. Flaky contract tests are often caused by tests running against non-deterministic data sets.

8. **Separate schema errors from business logic errors** -- When a contract test fails, determine whether the response structure is wrong (schema violation) or the response content is wrong (business logic error). These require different debugging approaches.

9. **Check for schema references that do not resolve** -- OpenAPI specs use `$ref` to reference shared components. If a reference points to a non-existent schema, the validator may silently skip validation, causing false passes.

10. **Verify API version routing** -- If backward compatibility tests pass but consumers report breakage, check that the API correctly routes requests to the appropriate version handler. Version misrouting is a common source of contract violations.