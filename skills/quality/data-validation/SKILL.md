---
name: data-validation
description: Data validation patterns including schema validation, input sanitization, output encoding, and type coercion. Use when implementing validate, validation, schema, form validation, API validation, JSON Schema, Zod, Pydantic, Joi, Yup, sanitize, sanitization, XSS prevention, injection prevention, escape, encode, whitelist, constraint checking, invariant validation, data pipeline validation, ML feature validation, or custom validators.
---

# Data Validation

## Overview

Data validation ensures that input data meets expected formats, types, and constraints before processing. This skill covers schema validation libraries, input sanitization, output encoding, type coercion strategies, security-focused validation (XSS, injection prevention), data pipeline validation, and comprehensive error handling.

## Trigger Keywords

Use this skill when working with:
- **Schema validation**: JSON Schema, Zod, Pydantic, Joi, Yup, Ajv, class-validator
- **Input processing**: validate, validation, sanitize, sanitization, input validation, form validation
- **Security validation**: XSS prevention, injection prevention, escape, encode, whitelist, blacklist
- **Constraints**: constraint checking, invariant validation, business rules, data quality
- **API validation**: request validation, response validation, API contracts
- **Data pipelines**: Great Expectations, dbt tests, data quality checks
- **ML/AI**: feature validation, distribution checks, data drift detection

## Agent Assignments

| Agent | Responsibility |
|-------|----------------|
| **senior-software-engineer** (Opus) | Schema architecture, validation strategy design, complex validation patterns |
| **software-engineer** (Sonnet) | Implements validation logic, integrates schema libraries, writes validators |
| **security-engineer** (Opus) | XSS prevention, injection prevention, sanitization strategies, encoding |
| **senior-infrastructure-engineer** (Opus) | Infrastructure config validation, pipeline validation, data quality checks |

## Key Concepts

### JSON Schema Validation

```typescript
import Ajv, { JSONSchemaType, ValidateFunction } from "ajv";
import addFormats from "ajv-formats";

// Initialize Ajv with formats
const ajv = new Ajv({
  allErrors: true, // Return all errors, not just first
  removeAdditional: true, // Remove properties not in schema
  useDefaults: true, // Apply default values
  coerceTypes: true, // Coerce types when possible
});
addFormats(ajv);

// Define schema with TypeScript type
interface CreateUserRequest {
  email: string;
  password: string;
  name: string;
  age?: number;
  role: "user" | "admin" | "moderator";
  preferences?: {
    newsletter: boolean;
    theme: "light" | "dark";
  };
}

const createUserSchema: JSONSchemaType<CreateUserRequest> = {
  type: "object",
  properties: {
    email: { type: "string", format: "email", maxLength: 255 },
    password: {
      type: "string",
      minLength: 12,
      maxLength: 128,
      pattern:
        "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]+$",
    },
    name: { type: "string", minLength: 1, maxLength: 100 },
    age: { type: "integer", minimum: 13, maximum: 150, nullable: true },
    role: { type: "string", enum: ["user", "admin", "moderator"] },
    preferences: {
      type: "object",
      properties: {
        newsletter: { type: "boolean", default: false },
        theme: { type: "string", enum: ["light", "dark"], default: "light" },
      },
      required: ["newsletter", "theme"],
      additionalProperties: false,
      nullable: true,
    },
  },
  required: ["email", "password", "name", "role"],
  additionalProperties: false,
};

// Compile and cache validator
const validateCreateUser = ajv.compile(createUserSchema);

// Usage with error formatting
function validate<T>(
  validator: ValidateFunction<T>,
  data: unknown,
): { success: true; data: T } | { success: false; errors: ValidationError[] } {
  if (validator(data)) {
    return { success: true, data };
  }

  const errors: ValidationError[] = (validator.errors || []).map((err) => ({
    field:
      err.instancePath.replace(/^\//, "").replace(/\//g, ".") ||
      err.params.missingProperty,
    message: formatAjvError(err),
    code: err.keyword,
  }));

  return { success: false, errors };
}

function formatAjvError(error: Ajv.ErrorObject): string {
  switch (error.keyword) {
    case "required":
      return `${error.params.missingProperty} is required`;
    case "minLength":
      return `Must be at least ${error.params.limit} characters`;
    case "maxLength":
      return `Must be at most ${error.params.limit} characters`;
    case "format":
      return `Invalid ${error.params.format} format`;
    case "enum":
      return `Must be one of: ${error.params.allowedValues.join(", ")}`;
    case "pattern":
      return "Invalid format";
    case "minimum":
      return `Must be at least ${error.params.limit}`;
    case "maximum":
      return `Must be at most ${error.params.limit}`;
    default:
      return error.message || "Invalid value";
  }
}
```

### Zod Validation (TypeScript)

```typescript
import { z, ZodError, ZodSchema } from "zod";

// Basic schemas
const emailSchema = z.string().email().max(255);
const passwordSchema = z
  .string()
  .min(12, "Password must be at least 12 characters")
  .max(128)
  .regex(/[a-z]/, "Password must contain a lowercase letter")
  .regex(/[A-Z]/, "Password must contain an uppercase letter")
  .regex(/[0-9]/, "Password must contain a number")
  .regex(/[^a-zA-Z0-9]/, "Password must contain a special character");

// Complex schema with transforms and refinements
const createUserSchema = z
  .object({
    email: emailSchema.transform((e) => e.toLowerCase().trim()),
    password: passwordSchema,
    confirmPassword: z.string(),
    name: z
      .string()
      .min(1)
      .max(100)
      .transform((n) => n.trim()),
    age: z.number().int().min(13).max(150).optional(),
    role: z.enum(["user", "admin", "moderator"]).default("user"),
    tags: z.array(z.string().max(50)).max(10).default([]),
    metadata: z.record(z.string(), z.unknown()).optional(),
    preferences: z
      .object({
        newsletter: z.boolean().default(false),
        theme: z.enum(["light", "dark"]).default("light"),
        notifications: z
          .object({
            email: z.boolean().default(true),
            push: z.boolean().default(false),
            sms: z.boolean().default(false),
          })
          .default({}),
      })
      .default({}),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords do not match",
    path: ["confirmPassword"],
  })
  .transform(({ confirmPassword, ...data }) => data); // Remove confirmPassword

// Infer TypeScript types from schema
type CreateUserInput = z.input<typeof createUserSchema>;
type CreateUserOutput = z.output<typeof createUserSchema>;

// Validation helper with formatted errors
interface ValidationResult<T> {
  success: boolean;
  data?: T;
  errors?: Array<{
    field: string;
    message: string;
  }>;
}

function validateWithZod<T>(
  schema: ZodSchema<T>,
  data: unknown,
): ValidationResult<T> {
  const result = schema.safeParse(data);

  if (result.success) {
    return { success: true, data: result.data };
  }

  const errors = result.error.errors.map((err) => ({
    field: err.path.join("."),
    message: err.message,
  }));

  return { success: false, errors };
}

// Custom refinements
const uniqueEmailSchema = emailSchema.refine(
  async (email) => {
    const exists = await db.users.findByEmail(email);
    return !exists;
  },
  { message: "Email already registered" },
);

// Conditional validation
const formSchema = z.discriminatedUnion("type", [
  z.object({
    type: z.literal("individual"),
    firstName: z.string().min(1),
    lastName: z.string().min(1),
    ssn: z.string().regex(/^\d{3}-\d{2}-\d{4}$/),
  }),
  z.object({
    type: z.literal("business"),
    companyName: z.string().min(1),
    ein: z.string().regex(/^\d{2}-\d{7}$/),
  }),
]);

// Recursive schemas
interface Category {
  name: string;
  children?: Category[];
}

const categorySchema: z.ZodType<Category> = z.lazy(() =>
  z.object({
    name: z.string().min(1),
    children: z.array(categorySchema).optional(),
  }),
);
```

### Pydantic Validation (Python)

```python
from datetime import datetime
from typing import Optional, List, Literal
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    validator,
    root_validator,
    constr,
    conint,
)
import re

# Basic model with field validation
class CreateUserRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=12, max_length=128)
    name: constr(min_length=1, max_length=100)
    age: Optional[conint(ge=13, le=150)] = None
    role: Literal['user', 'admin', 'moderator'] = 'user'
    tags: List[str] = Field(default_factory=list, max_items=10)

    class Config:
        # Strip whitespace from strings
        anystr_strip_whitespace = True
        # Validate on assignment
        validate_assignment = True
        # Use enum values
        use_enum_values = True

    @validator('email')
    def email_lowercase(cls, v):
        return v.lower()

    @validator('password')
    def password_strength(cls, v):
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain a lowercase letter')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain an uppercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain a number')
        if not re.search(r'[^a-zA-Z0-9]', v):
            raise ValueError('Password must contain a special character')
        return v

    @validator('tags', each_item=True)
    def validate_tag(cls, v):
        if len(v) > 50:
            raise ValueError('Tag must be at most 50 characters')
        return v.strip().lower()

# Nested models
class Address(BaseModel):
    street: str
    city: str
    state: constr(min_length=2, max_length=2)
    zip_code: constr(regex=r'^\d{5}(-\d{4})?$')
    country: str = 'US'

class UserProfile(BaseModel):
    user: CreateUserRequest
    addresses: List[Address] = Field(default_factory=list, max_items=5)
    primary_address_index: int = 0

    @root_validator
    def validate_primary_address(cls, values):
        addresses = values.get('addresses', [])
        primary_index = values.get('primary_address_index', 0)

        if addresses and primary_index >= len(addresses):
            raise ValueError('Primary address index out of range')

        return values

# Generic response model
from typing import TypeVar, Generic

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    errors: Optional[List[dict]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Custom validator with database lookup
from pydantic import validator
import asyncio

class UniqueEmailModel(BaseModel):
    email: EmailStr

    @validator('email')
    def email_must_be_unique(cls, v):
        # Note: This is synchronous; use root_validator for async
        from app.db import user_exists_sync
        if user_exists_sync(v):
            raise ValueError('Email already registered')
        return v

# Validation error handling
from pydantic import ValidationError
from fastapi import HTTPException

def validate_request(model_class, data: dict):
    try:
        return model_class(**data)
    except ValidationError as e:
        errors = []
        for error in e.errors():
            errors.append({
                'field': '.'.join(str(loc) for loc in error['loc']),
                'message': error['msg'],
                'type': error['type'],
            })
        raise HTTPException(status_code=422, detail={'errors': errors})
```

### Input Sanitization

```typescript
import DOMPurify from "dompurify";
import { JSDOM } from "jsdom";
import validator from "validator";

// Server-side DOMPurify setup
const window = new JSDOM("").window;
const purify = DOMPurify(window);

// HTML sanitization
function sanitizeHtml(dirty: string, options?: DOMPurify.Config): string {
  const defaultOptions: DOMPurify.Config = {
    ALLOWED_TAGS: ["b", "i", "em", "strong", "a", "p", "br", "ul", "ol", "li"],
    ALLOWED_ATTR: ["href", "target", "rel"],
    ALLOW_DATA_ATTR: false,
    ADD_ATTR: ["target"], // Add target="_blank" to links
    FORBID_TAGS: ["script", "style", "iframe", "form", "input"],
    FORBID_ATTR: ["onerror", "onclick", "onload"],
  };

  return purify.sanitize(dirty, { ...defaultOptions, ...options });
}

// Rich text sanitization (more permissive)
function sanitizeRichText(dirty: string): string {
  return purify.sanitize(dirty, {
    ALLOWED_TAGS: [
      "h1",
      "h2",
      "h3",
      "h4",
      "h5",
      "h6",
      "p",
      "br",
      "hr",
      "b",
      "i",
      "em",
      "strong",
      "u",
      "s",
      "strike",
      "ul",
      "ol",
      "li",
      "a",
      "img",
      "blockquote",
      "pre",
      "code",
      "table",
      "thead",
      "tbody",
      "tr",
      "th",
      "td",
    ],
    ALLOWED_ATTR: ["href", "src", "alt", "title", "class", "id"],
    ALLOW_DATA_ATTR: false,
  });
}

// SQL-safe string (use parameterized queries instead when possible)
function sanitizeForSql(input: string): string {
  return input
    .replace(/'/g, "''")
    .replace(/\\/g, "\\\\")
    .replace(/\x00/g, "\\0")
    .replace(/\n/g, "\\n")
    .replace(/\r/g, "\\r")
    .replace(/\x1a/g, "\\Z");
}

// Filename sanitization
function sanitizeFilename(filename: string): string {
  return filename
    .replace(/[^a-zA-Z0-9._-]/g, "_") // Replace special chars
    .replace(/\.{2,}/g, ".") // Remove consecutive dots
    .replace(/^\.+|\.+$/g, "") // Remove leading/trailing dots
    .substring(0, 255); // Limit length
}

// Path traversal prevention
function sanitizePath(userPath: string, basePath: string): string {
  const path = require("path");
  const resolvedPath = path.resolve(basePath, userPath);

  if (!resolvedPath.startsWith(path.resolve(basePath))) {
    throw new Error("Path traversal detected");
  }

  return resolvedPath;
}

// Comprehensive input sanitizer
interface SanitizationOptions {
  trim?: boolean;
  lowercase?: boolean;
  stripHtml?: boolean;
  maxLength?: number;
  allowedChars?: RegExp;
}

function sanitizeString(
  input: string,
  options: SanitizationOptions = {},
): string {
  let result = input;

  if (options.trim !== false) {
    result = result.trim();
  }

  if (options.stripHtml) {
    result = validator.stripLow(validator.escape(result));
  }

  if (options.lowercase) {
    result = result.toLowerCase();
  }

  if (options.allowedChars) {
    result = result.replace(
      new RegExp(`[^${options.allowedChars.source}]`, "g"),
      "",
    );
  }

  if (options.maxLength) {
    result = result.substring(0, options.maxLength);
  }

  // Remove null bytes
  result = result.replace(/\x00/g, "");

  return result;
}

// Common sanitization presets
const sanitizers = {
  username: (input: string) =>
    sanitizeString(input, {
      lowercase: true,
      maxLength: 30,
      allowedChars: /[a-z0-9_-]/,
    }),

  email: (input: string) => validator.normalizeEmail(input) || "",

  phone: (input: string) => input.replace(/[^0-9+()-\s]/g, "").substring(0, 20),

  slug: (input: string) =>
    sanitizeString(input, {
      lowercase: true,
      maxLength: 100,
    })
      .replace(/\s+/g, "-")
      .replace(/[^a-z0-9-]/g, ""),

  searchQuery: (input: string) =>
    sanitizeString(input, {
      trim: true,
      maxLength: 200,
      stripHtml: true,
    }),
};
```

### Output Encoding

```typescript
// HTML encoding
function encodeHtml(str: string): string {
  const entities: Record<string, string> = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#x27;",
    "/": "&#x2F;",
    "`": "&#x60;",
    "=": "&#x3D;",
  };

  return str.replace(/[&<>"'`=/]/g, (char) => entities[char]);
}

// JavaScript string encoding (for embedding in <script> tags)
function encodeJsString(str: string): string {
  return str
    .replace(/\\/g, "\\\\")
    .replace(/'/g, "\\'")
    .replace(/"/g, '\\"')
    .replace(/\n/g, "\\n")
    .replace(/\r/g, "\\r")
    .replace(/\t/g, "\\t")
    .replace(/</g, "\\x3c")
    .replace(/>/g, "\\x3e")
    .replace(/&/g, "\\x26");
}

// URL encoding
function encodeUrlParam(str: string): string {
  return encodeURIComponent(str);
}

// CSS encoding
function encodeCss(str: string): string {
  return str.replace(/[^a-zA-Z0-9]/g, (char) => {
    const hex = char.charCodeAt(0).toString(16);
    return `\\${hex} `;
  });
}

// JSON encoding (safe for embedding in HTML)
function encodeJsonForHtml(obj: unknown): string {
  return JSON.stringify(obj)
    .replace(/</g, "\\u003c")
    .replace(/>/g, "\\u003e")
    .replace(/&/g, "\\u0026")
    .replace(/'/g, "\\u0027");
}

// Context-aware output encoding
type OutputContext = "html" | "htmlAttribute" | "javascript" | "url" | "css";

function encode(str: string, context: OutputContext): string {
  switch (context) {
    case "html":
      return encodeHtml(str);
    case "htmlAttribute":
      return encodeHtml(str).replace(/"/g, "&quot;");
    case "javascript":
      return encodeJsString(str);
    case "url":
      return encodeUrlParam(str);
    case "css":
      return encodeCss(str);
    default:
      return encodeHtml(str);
  }
}

// React-style escaping (for JSX)
function escapeForReact(str: string): string {
  // React already escapes, but for dangerouslySetInnerHTML:
  return encodeHtml(str);
}

// Template literal tag for safe HTML
function safeHtml(strings: TemplateStringsArray, ...values: unknown[]): string {
  return strings.reduce((result, str, i) => {
    const value = values[i - 1];
    const encoded =
      typeof value === "string" ? encodeHtml(value) : String(value ?? "");
    return result + encoded + str;
  });
}

// Usage
const userInput = '<script>alert("xss")</script>';
const safe = safeHtml`<div class="user-content">${userInput}</div>`;
// Result: <div class="user-content">&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;</div>
```

### API Request/Response Validation

```typescript
// Express middleware for request validation
import { Request, Response, NextFunction } from "express";
import { z, ZodSchema } from "zod";

function validate<T>(
  schema: ZodSchema<T>,
  source: "body" | "query" | "params" = "body",
) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req[source]);

    if (!result.success) {
      return res.status(422).json({
        error: "Validation Error",
        details: result.error.errors.map((e) => ({
          field: e.path.join("."),
          message: e.message,
        })),
      });
    }

    req[source] = result.data;
    next();
  };
}

// Usage
const createUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(12),
  name: z.string().min(1).max(100),
});

app.post("/users", validate(createUserSchema), async (req, res) => {
  // req.body is now typed and validated
  const user = await createUser(req.body);
  res.status(201).json(user);
});

// Response validation
const userResponseSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string(),
  createdAt: z.string().datetime(),
});

function validateResponse<T>(schema: ZodSchema<T>, data: unknown): T {
  const result = schema.safeParse(data);
  if (!result.success) {
    throw new Error("Invalid response format");
  }
  return result.data;
}
```

### Data Pipeline Validation (Great Expectations)

```python
# Great Expectations for data quality validation
import great_expectations as ge
from great_expectations.dataset import PandasDataset

# Load dataset with expectations
df = ge.read_csv('data.csv')

# Basic expectations
df.expect_column_to_exist('user_id')
df.expect_column_values_to_not_be_null('email')
df.expect_column_values_to_be_unique('email')
df.expect_column_values_to_match_regex('email', r'^[^@]+@[^@]+\.[^@]+$')
df.expect_column_values_to_be_in_set('status', ['active', 'inactive', 'pending'])

# Numeric expectations
df.expect_column_values_to_be_between('age', 0, 150)
df.expect_column_mean_to_be_between('price', 10, 1000)

# Date expectations
df.expect_column_values_to_be_dateutil_parseable('created_at')

# Custom expectations
def custom_validation(df):
    # Email domain must match company_domain
    emails = df['email'].str.split('@', expand=True)[1]
    return (emails == df['company_domain']).all()

df.expect_column_pair_values_to_be_equal('email_domain', 'company_domain',
                                          custom_fn=custom_validation)

# Run validation suite
results = df.validate()
if not results['success']:
    for result in results['results']:
        if not result['success']:
            print(f"Validation failed: {result['expectation_config']}")

# dbt tests for SQL data validation
# models/schema.yml
version: 2

models:
  - name: users
    columns:
      - name: user_id
        tests:
          - unique
          - not_null
      - name: email
        tests:
          - unique
          - not_null
          - email_format  # Custom test
      - name: age
        tests:
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 150
      - name: status
        tests:
          - accepted_values:
              values: ['active', 'inactive', 'pending']
      - name: created_at
        tests:
          - not_null
          - dbt_utils.recency:
              datepart: day
              field: created_at
              interval: 7
```

### ML Feature Validation

```python
# Feature validation for ML pipelines
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

class FeatureValidator:
    def __init__(self, expected_schema: Dict[str, str]):
        self.expected_schema = expected_schema
        self.baseline_stats = {}

    def validate_schema(self, df: pd.DataFrame) -> List[str]:
        errors = []

        # Check column presence
        expected_cols = set(self.expected_schema.keys())
        actual_cols = set(df.columns)

        missing = expected_cols - actual_cols
        if missing:
            errors.append(f"Missing columns: {missing}")

        extra = actual_cols - expected_cols
        if extra:
            errors.append(f"Unexpected columns: {extra}")

        # Check data types
        for col, expected_type in self.expected_schema.items():
            if col in df.columns:
                actual_type = str(df[col].dtype)
                if not actual_type.startswith(expected_type):
                    errors.append(f"Column {col}: expected {expected_type}, got {actual_type}")

        return errors

    def validate_distributions(self, df: pd.DataFrame,
                               threshold: float = 3.0) -> List[str]:
        errors = []

        for col in df.select_dtypes(include=[np.number]).columns:
            if col not in self.baseline_stats:
                continue

            baseline_mean = self.baseline_stats[col]['mean']
            baseline_std = self.baseline_stats[col]['std']

            current_mean = df[col].mean()
            current_std = df[col].std()

            # Check for distribution drift using z-score
            mean_zscore = abs((current_mean - baseline_mean) / baseline_std)
            if mean_zscore > threshold:
                errors.append(f"Column {col}: mean drift detected (z-score: {mean_zscore:.2f})")

            # Check for variance change
            variance_ratio = current_std / baseline_std
            if variance_ratio < 0.5 or variance_ratio > 2.0:
                errors.append(f"Column {col}: variance change detected (ratio: {variance_ratio:.2f})")

        return errors

    def validate_null_rates(self, df: pd.DataFrame,
                            max_null_rate: float = 0.05) -> List[str]:
        errors = []
        null_rates = df.isnull().sum() / len(df)

        for col, rate in null_rates.items():
            if rate > max_null_rate:
                errors.append(f"Column {col}: null rate {rate:.2%} exceeds threshold {max_null_rate:.2%}")

        return errors

    def validate_categorical_values(self, df: pd.DataFrame,
                                     expected_categories: Dict[str, List]) -> List[str]:
        errors = []

        for col, expected in expected_categories.items():
            if col not in df.columns:
                continue

            actual = set(df[col].dropna().unique())
            expected_set = set(expected)

            unexpected = actual - expected_set
            if unexpected:
                errors.append(f"Column {col}: unexpected categories {unexpected}")

        return errors

    def set_baseline(self, df: pd.DataFrame):
        for col in df.select_dtypes(include=[np.number]).columns:
            self.baseline_stats[col] = {
                'mean': df[col].mean(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
            }

# Usage
validator = FeatureValidator({
    'user_id': 'int',
    'age': 'float',
    'income': 'float',
    'category': 'object',
})

# Set baseline from training data
validator.set_baseline(training_df)

# Validate new data
errors = []
errors.extend(validator.validate_schema(new_df))
errors.extend(validator.validate_distributions(new_df))
errors.extend(validator.validate_null_rates(new_df))
errors.extend(validator.validate_categorical_values(new_df, {
    'category': ['A', 'B', 'C']
}))

if errors:
    raise ValueError(f"Feature validation failed:\n" + "\n".join(errors))
```

### Infrastructure Configuration Validation

```yaml
# JSON Schema for Kubernetes config validation
apiVersion: v1
kind: ConfigMap
metadata:
  name: validation-schema
data:
  deployment-schema.json: |
    {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "type": "object",
      "required": ["apiVersion", "kind", "metadata", "spec"],
      "properties": {
        "apiVersion": {
          "type": "string",
          "pattern": "^apps/v1$"
        },
        "kind": {
          "type": "string",
          "enum": ["Deployment"]
        },
        "spec": {
          "type": "object",
          "required": ["replicas", "selector", "template"],
          "properties": {
            "replicas": {
              "type": "integer",
              "minimum": 1,
              "maximum": 100
            },
            "selector": {
              "type": "object",
              "required": ["matchLabels"]
            },
            "template": {
              "type": "object",
              "required": ["metadata", "spec"],
              "properties": {
                "spec": {
                  "type": "object",
                  "required": ["containers"],
                  "properties": {
                    "containers": {
                      "type": "array",
                      "minItems": 1,
                      "items": {
                        "type": "object",
                        "required": ["name", "image"],
                        "properties": {
                          "resources": {
                            "type": "object",
                            "required": ["requests", "limits"]
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
```

```python
# Terraform configuration validation
import hcl2
import json
from jsonschema import validate, ValidationError

def validate_terraform_config(config_path: str, schema_path: str):
    # Parse HCL
    with open(config_path, 'r') as f:
        config = hcl2.load(f)

    # Load schema
    with open(schema_path, 'r') as f:
        schema = json.load(f)

    # Validate
    try:
        validate(instance=config, schema=schema)
        print("Terraform config is valid")
    except ValidationError as e:
        print(f"Validation error: {e.message}")
        print(f"Path: {' -> '.join(str(p) for p in e.path)}")
        raise

# Custom business rule validation
def validate_aws_resource_tags(config: dict) -> List[str]:
    errors = []
    required_tags = {'Environment', 'Owner', 'CostCenter'}

    for resource in config.get('resource', {}).values():
        for resource_name, resource_config in resource.items():
            tags = set(resource_config.get('tags', {}).keys())
            missing = required_tags - tags

            if missing:
                errors.append(f"Resource {resource_name} missing tags: {missing}")

    return errors
```

## Best Practices

1. **Validate Early**
   - Validate at the boundary (API endpoints, form submissions, pipeline ingestion)
   - Fail fast with clear error messages
   - Don't trust any external input

2. **Use Schema Validation Libraries**
   - Prefer Zod/Pydantic for type safety
   - JSON Schema for language-agnostic validation
   - Generate TypeScript types from schemas

3. **Sanitize and Encode**
   - Sanitize input based on context (HTML, SQL, paths)
   - Encode output based on where it's rendered
   - Use parameterized queries instead of escaping for SQL

4. **Security-First Validation**
   - Whitelist allowed values rather than blacklist
   - Prevent XSS with output encoding
   - Prevent injection with parameterized queries and sanitization
   - Validate file uploads (type, size, content)

5. **Data Pipeline Validation**
   - Validate schema before processing
   - Check data distributions for drift
   - Monitor null rates and cardinality
   - Use Great Expectations for comprehensive data quality

6. **ML Feature Validation**
   - Validate schema matches training data
   - Detect distribution drift
   - Check for unexpected categories
   - Monitor feature correlations

7. **Error Messages**
   - Provide specific, actionable error messages
   - Include field names in errors
   - Don't expose internal details in production

8. **Defense in Depth**
   - Validate on both client and server
   - Apply principle of least privilege
   - Validate at multiple layers (API, service, database)
