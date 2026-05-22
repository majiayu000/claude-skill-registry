---
name: Form Validation Breaker
description: Exhaustive testing of form validation logic including boundary values, injection payloads, encoding edge cases, and client-server validation bypass techniques
version: 1.0.0
author: Pramod
license: MIT
tags: [form-validation, input-testing, boundary-testing, injection-testing, xss-prevention, validation-bypass, fuzzing]
testingTypes: [security, e2e]
frameworks: [playwright]
languages: [typescript, javascript]
domains: [web]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# Form Validation Breaker Skill

You are an expert QA security engineer specializing in form validation testing. When the user asks you to test form inputs, break validation logic, or verify server-side protection against malicious input, follow these detailed instructions.

## Core Principles

1. **Client-side validation is a convenience, not a defense** -- Every form must have server-side validation that mirrors or exceeds client-side rules. Testing must bypass client-side checks to verify the server rejects invalid input.
2. **Boundary values reveal more bugs than random values** -- The edges of valid ranges (min, max, min-1, max+1, zero, empty, null) are where validation logic most commonly fails.
3. **Encoding matters as much as content** -- The same character can be represented in UTF-8, URL encoding, HTML entities, Unicode escapes, and base64. Validation that blocks `<script>` but allows `%3Cscript%3E` is broken.
4. **Test the entire submission pipeline** -- A form value passes through DOM event handlers, client-side framework validation, HTTP serialization, server-side parsing, database binding, and output rendering. Each stage can transform or mishandle the input.
5. **Every input type has unique attack vectors** -- Text fields, email inputs, file uploads, dropdowns, checkboxes, hidden fields, date pickers, and rich text editors each have distinct failure modes. Test each type specifically.
6. **Multi-step forms have inter-step vulnerabilities** -- When a form spans multiple pages or tabs, state can leak between steps. Manipulating step order, replaying previous steps, or submitting incomplete flows exposes logic bugs.
7. **Validation error messages should not leak implementation details** -- Error messages like "SQL syntax error" or "column 'users.email' not found" reveal the database schema. Verify that error messages are generic and user-friendly.

## Project Structure

Organize your form validation testing suite with this structure:

```
tests/
  form-validation/
    boundary-values.spec.ts
    injection-payloads.spec.ts
    encoding-edge-cases.spec.ts
    file-upload-validation.spec.ts
    client-bypass.spec.ts
    multi-step-forms.spec.ts
    real-time-validation.spec.ts
  fixtures/
    form-breaker.fixture.ts
  helpers/
    payload-generator.ts
    boundary-calculator.ts
    encoding-transformer.ts
    validation-reporter.ts
  payloads/
    xss-vectors.json
    sql-injection.json
    unicode-edge-cases.json
playwright.config.ts
```

## Payload Generator

The payload generator creates targeted test inputs for different validation scenarios.

```typescript
// tests/helpers/payload-generator.ts

export interface TestPayload {
  name: string;
  value: string;
  category: string;
  expectedResult: 'accept' | 'reject';
  description: string;
}

export function generateBoundaryPayloads(
  fieldName: string,
  options: {
    minLength?: number;
    maxLength?: number;
    minValue?: number;
    maxValue?: number;
    required?: boolean;
    type?: 'text' | 'email' | 'number' | 'url' | 'phone' | 'date';
  }
): TestPayload[] {
  const payloads: TestPayload[] = [];
  const { minLength = 0, maxLength = 255, minValue, maxValue, required = true, type = 'text' } = options;

  // Empty and whitespace
  if (required) {
    payloads.push({
      name: `${fieldName}_empty`,
      value: '',
      category: 'boundary',
      expectedResult: 'reject',
      description: 'Empty string on required field',
    });
    payloads.push({
      name: `${fieldName}_whitespace_only`,
      value: '   ',
      category: 'boundary',
      expectedResult: 'reject',
      description: 'Whitespace-only string on required field',
    });
    payloads.push({
      name: `${fieldName}_tab_only`,
      value: '\t\t',
      category: 'boundary',
      expectedResult: 'reject',
      description: 'Tab-only string on required field',
    });
    payloads.push({
      name: `${fieldName}_newline_only`,
      value: '\n\n',
      category: 'boundary',
      expectedResult: 'reject',
      description: 'Newline-only string on required field',
    });
  }

  // Length boundaries
  if (minLength > 0) {
    payloads.push({
      name: `${fieldName}_below_min_length`,
      value: 'a'.repeat(minLength - 1),
      category: 'boundary',
      expectedResult: 'reject',
      description: `String of length ${minLength - 1} (min is ${minLength})`,
    });
    payloads.push({
      name: `${fieldName}_at_min_length`,
      value: 'a'.repeat(minLength),
      category: 'boundary',
      expectedResult: 'accept',
      description: `String of length ${minLength} (exact minimum)`,
    });
  }

  if (maxLength) {
    payloads.push({
      name: `${fieldName}_at_max_length`,
      value: 'a'.repeat(maxLength),
      category: 'boundary',
      expectedResult: 'accept',
      description: `String of length ${maxLength} (exact maximum)`,
    });
    payloads.push({
      name: `${fieldName}_above_max_length`,
      value: 'a'.repeat(maxLength + 1),
      category: 'boundary',
      expectedResult: 'reject',
      description: `String of length ${maxLength + 1} (above maximum)`,
    });
    payloads.push({
      name: `${fieldName}_extreme_length`,
      value: 'a'.repeat(maxLength * 10),
      category: 'boundary',
      expectedResult: 'reject',
      description: `String of length ${maxLength * 10} (extreme overflow)`,
    });
  }

  // Numeric boundaries
  if (type === 'number' && minValue !== undefined && maxValue !== undefined) {
    payloads.push(
      { name: `${fieldName}_below_min`, value: String(minValue - 1), category: 'boundary', expectedResult: 'reject', description: `Value ${minValue - 1} (below minimum ${minValue})` },
      { name: `${fieldName}_at_min`, value: String(minValue), category: 'boundary', expectedResult: 'accept', description: `Value ${minValue} (exact minimum)` },
      { name: `${fieldName}_at_max`, value: String(maxValue), category: 'boundary', expectedResult: 'accept', description: `Value ${maxValue} (exact maximum)` },
      { name: `${fieldName}_above_max`, value: String(maxValue + 1), category: 'boundary', expectedResult: 'reject', description: `Value ${maxValue + 1} (above maximum ${maxValue})` },
      { name: `${fieldName}_negative_zero`, value: '-0', category: 'boundary', expectedResult: 'accept', description: 'Negative zero' },
      { name: `${fieldName}_float`, value: '3.14159', category: 'boundary', expectedResult: 'reject', description: 'Float value in integer field' },
      { name: `${fieldName}_scientific`, value: '1e10', category: 'boundary', expectedResult: 'reject', description: 'Scientific notation' },
      { name: `${fieldName}_infinity`, value: 'Infinity', category: 'boundary', expectedResult: 'reject', description: 'Infinity value' },
      { name: `${fieldName}_nan`, value: 'NaN', category: 'boundary', expectedResult: 'reject', description: 'NaN value' }
    );
  }

  return payloads;
}

export function generateInjectionPayloads(fieldName: string): TestPayload[] {
  return [
    // XSS vectors
    { name: `${fieldName}_xss_script`, value: '<script>alert("XSS")</script>', category: 'xss', expectedResult: 'reject', description: 'Basic script injection' },
    { name: `${fieldName}_xss_img`, value: '<img src=x onerror=alert(1)>', category: 'xss', expectedResult: 'reject', description: 'Image onerror handler' },
    { name: `${fieldName}_xss_svg`, value: '<svg onload=alert(1)>', category: 'xss', expectedResult: 'reject', description: 'SVG onload handler' },
    { name: `${fieldName}_xss_event`, value: '" onfocus="alert(1)" autofocus="', category: 'xss', expectedResult: 'reject', description: 'Attribute injection with event handler' },
    { name: `${fieldName}_xss_href`, value: 'javascript:alert(1)', category: 'xss', expectedResult: 'reject', description: 'JavaScript protocol in URL context' },
    { name: `${fieldName}_xss_encoded`, value: '&lt;script&gt;alert(1)&lt;/script&gt;', category: 'xss', expectedResult: 'reject', description: 'HTML entity encoded script tag' },
    { name: `${fieldName}_xss_unicode`, value: '\u003cscript\u003ealert(1)\u003c/script\u003e', category: 'xss', expectedResult: 'reject', description: 'Unicode escaped script tag' },
    { name: `${fieldName}_xss_mixed_case`, value: '<ScRiPt>alert(1)</sCrIpT>', category: 'xss', expectedResult: 'reject', description: 'Mixed case script tag' },
    { name: `${fieldName}_xss_null_byte`, value: '<scr\x00ipt>alert(1)</script>', category: 'xss', expectedResult: 'reject', description: 'Null byte in script tag' },

    // SQL injection vectors
    { name: `${fieldName}_sqli_basic`, value: "' OR '1'='1", category: 'sqli', expectedResult: 'reject', description: 'Basic SQL injection' },
    { name: `${fieldName}_sqli_union`, value: "' UNION SELECT * FROM users--", category: 'sqli', expectedResult: 'reject', description: 'UNION-based SQL injection' },
    { name: `${fieldName}_sqli_drop`, value: "'; DROP TABLE users;--", category: 'sqli', expectedResult: 'reject', description: 'DROP TABLE injection' },
    { name: `${fieldName}_sqli_comment`, value: "admin'--", category: 'sqli', expectedResult: 'reject', description: 'Comment-based authentication bypass' },
    { name: `${fieldName}_sqli_blind`, value: "' AND 1=1--", category: 'sqli', expectedResult: 'reject', description: 'Blind SQL injection probe' },
    { name: `${fieldName}_sqli_time`, value: "' OR SLEEP(5)--", category: 'sqli', expectedResult: 'reject', description: 'Time-based blind SQL injection' },

    // Command injection
    { name: `${fieldName}_cmd_pipe`, value: '| ls -la', category: 'command', expectedResult: 'reject', description: 'Pipe command injection' },
    { name: `${fieldName}_cmd_semicolon`, value: '; cat /etc/passwd', category: 'command', expectedResult: 'reject', description: 'Semicolon command injection' },
    { name: `${fieldName}_cmd_backtick`, value: '`whoami`', category: 'command', expectedResult: 'reject', description: 'Backtick command injection' },
    { name: `${fieldName}_cmd_subshell`, value: '$(cat /etc/passwd)', category: 'command', expectedResult: 'reject', description: 'Subshell command injection' },

    // Path traversal
    { name: `${fieldName}_path_traversal`, value: '../../../etc/passwd', category: 'path', expectedResult: 'reject', description: 'Directory traversal' },
    { name: `${fieldName}_path_null_byte`, value: '../../etc/passwd%00.jpg', category: 'path', expectedResult: 'reject', description: 'Null byte path traversal' },

    // LDAP injection
    { name: `${fieldName}_ldap`, value: '*)(uid=*))(|(uid=*', category: 'ldap', expectedResult: 'reject', description: 'LDAP injection' },

    // Template injection
    { name: `${fieldName}_ssti`, value: '{{7*7}}', category: 'template', expectedResult: 'reject', description: 'Server-side template injection' },
    { name: `${fieldName}_ssti_jinja`, value: '{{ config.items() }}', category: 'template', expectedResult: 'reject', description: 'Jinja2 template injection' },
  ];
}

export function generateEncodingPayloads(fieldName: string): TestPayload[] {
  return [
    // Unicode edge cases
    { name: `${fieldName}_zero_width_space`, value: 'test\u200Bvalue', category: 'encoding', expectedResult: 'reject', description: 'Zero-width space character' },
    { name: `${fieldName}_zero_width_joiner`, value: 'test\u200Dvalue', category: 'encoding', expectedResult: 'reject', description: 'Zero-width joiner character' },
    { name: `${fieldName}_bidi_override`, value: '\u202Emalicious\u202C', category: 'encoding', expectedResult: 'reject', description: 'Right-to-left override character' },
    { name: `${fieldName}_homoglyph`, value: '\u0430dmin', category: 'encoding', expectedResult: 'reject', description: 'Cyrillic "a" homoglyph for "admin"' },
    { name: `${fieldName}_emoji`, value: 'test value 🎉🚀💯', category: 'encoding', expectedResult: 'accept', description: 'Emoji characters (should be accepted if field allows unicode)' },
    { name: `${fieldName}_combining_chars`, value: 'te\u0301st', category: 'encoding', expectedResult: 'accept', description: 'Combining diacritical marks' },
    { name: `${fieldName}_surrogate_pair`, value: 'test \uD83D\uDE00 value', category: 'encoding', expectedResult: 'accept', description: 'Surrogate pair emoji' },
    { name: `${fieldName}_null_char`, value: 'test\x00value', category: 'encoding', expectedResult: 'reject', description: 'Null character in string' },
    { name: `${fieldName}_backspace`, value: 'test\x08value', category: 'encoding', expectedResult: 'reject', description: 'Backspace control character' },
    { name: `${fieldName}_bell`, value: 'test\x07value', category: 'encoding', expectedResult: 'reject', description: 'Bell control character' },

    // URL encoding
    { name: `${fieldName}_double_url_encode`, value: '%253Cscript%253E', category: 'encoding', expectedResult: 'reject', description: 'Double URL-encoded script tag' },
    { name: `${fieldName}_overlong_utf8`, value: '%C0%BCscript%C0%BE', category: 'encoding', expectedResult: 'reject', description: 'Overlong UTF-8 encoding' },
  ];
}
```

## The Form Breaker Fixture

The fixture provides utilities for filling forms, bypassing client-side validation, and capturing validation responses.

```typescript
// tests/fixtures/form-breaker.fixture.ts
import { test as base, Page, expect } from '@playwright/test';

export interface ValidationResult {
  fieldName: string;
  payload: string;
  payloadCategory: string;
  clientSideBlocked: boolean;
  serverSideBlocked: boolean;
  errorMessage: string;
  httpStatus?: number;
  responseBody?: string;
}

export class FormBreaker {
  constructor(private page: Page) {}

  /**
   * Fill a form field, bypassing any client-side maxlength or pattern restrictions
   */
  async fillFieldBypassingValidation(
    selector: string,
    value: string
  ): Promise<void> {
    await this.page.evaluate(
      ({ sel, val }) => {
        const element = document.querySelector(sel) as HTMLInputElement;
        if (!element) throw new Error(`Element not found: ${sel}`);

        // Remove client-side constraints
        element.removeAttribute('maxlength');
        element.removeAttribute('minlength');
        element.removeAttribute('pattern');
        element.removeAttribute('required');
        element.removeAttribute('min');
        element.removeAttribute('max');
        element.removeAttribute('step');
        element.type = 'text'; // Override type constraints

        // Set value directly, bypassing React/Vue controlled component logic
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
          HTMLInputElement.prototype,
          'value'
        )!.set!;
        nativeInputValueSetter.call(element, val);

        // Dispatch events to trigger framework change handlers
        element.dispatchEvent(new Event('input', { bubbles: true }));
        element.dispatchEvent(new Event('change', { bubbles: true }));
      },
      { sel: selector, val: value }
    );
  }

  /**
   * Submit a form by intercepting the submit event and sending raw data
   */
  async submitFormWithRawData(
    formSelector: string,
    data: Record<string, string>
  ): Promise<{ status: number; body: string }> {
    // Intercept form submission to capture the response
    const [response] = await Promise.all([
      this.page.waitForResponse(
        (resp) => resp.request().method() === 'POST',
        { timeout: 10000 }
      ).catch(() => null),
      this.page.evaluate(
        ({ sel, formData }) => {
          const form = document.querySelector(sel) as HTMLFormElement;
          if (!form) throw new Error(`Form not found: ${sel}`);

          // Remove form validation
          form.setAttribute('novalidate', 'true');

          // Fill fields
          for (const [name, value] of Object.entries(formData)) {
            const field = form.querySelector(`[name="${name}"]`) as HTMLInputElement;
            if (field) {
              field.removeAttribute('required');
              field.removeAttribute('pattern');
              field.removeAttribute('maxlength');
              const setter = Object.getOwnPropertyDescriptor(
                HTMLInputElement.prototype,
                'value'
              )!.set!;
              setter.call(field, value);
              field.dispatchEvent(new Event('input', { bubbles: true }));
              field.dispatchEvent(new Event('change', { bubbles: true }));
            }
          }

          // Submit the form
          form.submit();
        },
        { sel: formSelector, formData: data }
      ),
    ]);

    if (response) {
      return {
        status: response.status(),
        body: await response.text().catch(() => ''),
      };
    }

    return { status: 0, body: '' };
  }

  /**
   * Send form data directly via API, completely bypassing the browser form
   */
  async submitViaApi(
    url: string,
    data: Record<string, string>,
    method: 'POST' | 'PUT' | 'PATCH' = 'POST'
  ): Promise<{ status: number; body: string }> {
    const response = await this.page.request.fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      data: JSON.stringify(data),
    });

    return {
      status: response.status(),
      body: await response.text(),
    };
  }

  /**
   * Check if a validation error message is displayed on the page
   */
  async getValidationErrors(): Promise<string[]> {
    return await this.page.evaluate(() => {
      const errors: string[] = [];

      // HTML5 validation messages
      document.querySelectorAll(':invalid').forEach((el) => {
        const input = el as HTMLInputElement;
        if (input.validationMessage) {
          errors.push(`[${input.name || input.id}]: ${input.validationMessage}`);
        }
      });

      // Common error display patterns
      const errorSelectors = [
        '[class*="error"]',
        '[class*="invalid"]',
        '[role="alert"]',
        '.field-error',
        '.form-error',
        '.validation-error',
        '[data-testid*="error"]',
        '[aria-invalid="true"]',
      ];

      for (const selector of errorSelectors) {
        document.querySelectorAll(selector).forEach((el) => {
          const text = (el as HTMLElement).textContent?.trim();
          if (text && text.length > 0 && text.length < 500) {
            errors.push(text);
          }
        });
      }

      return [...new Set(errors)];
    });
  }
}

export const test = base.extend<{ formBreaker: FormBreaker }>({
  formBreaker: async ({ page }, use) => {
    const breaker = new FormBreaker(page);
    await use(breaker);
  },
});

export { expect } from '@playwright/test';
```

## Writing the Tests

### Boundary Value Testing

```typescript
// tests/form-validation/boundary-values.spec.ts
import { test, expect } from '../fixtures/form-breaker.fixture';
import { generateBoundaryPayloads } from '../helpers/payload-generator';

test.describe('Form Boundary Value Testing', () => {
  test.beforeEach(async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'http://localhost:3000';
    await page.goto(`${baseUrl}/signup`, { waitUntil: 'networkidle' });
  });

  test('email field should enforce valid email format', async ({ page, formBreaker }) => {
    const invalidEmails = [
      'plainaddress',
      '@missing-local.com',
      'missing-at-sign.com',
      'missing-domain@.com',
      'missing-tld@domain.',
      'spaces in@email.com',
      'double@@email.com',
      '.leading-dot@email.com',
      'trailing-dot.@email.com',
      'multiple...dots@email.com',
      'email@-leading-hyphen.com',
      'email@domain..double-dot.com',
      '<script>@email.com',
      'email@domain.com<script>',
    ];

    for (const email of invalidEmails) {
      await formBreaker.fillFieldBypassingValidation('input[name="email"]', email);

      // Try to submit
      const submitButton = page.getByRole('button', { name: /sign up|register|submit/i });
      if (await submitButton.isVisible()) {
        await submitButton.click();
        await page.waitForTimeout(1000);
      }

      // Check that the form was not successfully submitted
      const errors = await formBreaker.getValidationErrors();
      const currentUrl = page.url();

      // Either there should be validation errors visible,
      // or the URL should not have changed to a success page
      const wasRejected = errors.length > 0 || currentUrl.includes('signup');
      expect(wasRejected, `Email "${email}" should have been rejected`).toBe(true);

      // Reset the form
      await page.reload();
    }
  });

  test('username field should enforce length boundaries', async ({ page, formBreaker }) => {
    const payloads = generateBoundaryPayloads('username', {
      minLength: 3,
      maxLength: 50,
      required: true,
      type: 'text',
    });

    for (const payload of payloads) {
      await formBreaker.fillFieldBypassingValidation(
        'input[name="username"]',
        payload.value
      );

      const submitButton = page.getByRole('button', { name: /sign up|register|submit/i });
      if (await submitButton.isVisible()) {
        await submitButton.click();
        await page.waitForTimeout(1000);
      }

      const errors = await formBreaker.getValidationErrors();

      if (payload.expectedResult === 'reject') {
        expect(
          errors.length > 0 || page.url().includes('signup'),
          `Payload "${payload.name}" should have been rejected: ${payload.description}`
        ).toBe(true);
      }

      await page.reload();
    }
  });

  test('password field should enforce complexity requirements', async ({
    page,
    formBreaker,
  }) => {
    const weakPasswords = [
      '123',
      'password',
      '12345678',
      'abcdefgh',
      'ABCDEFGH',
      '!@#$%^&*',
      'aA1',      // Too short but meets complexity
      ' '.repeat(20), // Whitespace only
    ];

    for (const password of weakPasswords) {
      await formBreaker.fillFieldBypassingValidation(
        'input[name="password"]',
        password
      );

      const submitButton = page.getByRole('button', { name: /sign up|register|submit/i });
      if (await submitButton.isVisible()) {
        await submitButton.click();
        await page.waitForTimeout(1000);
      }

      const errors = await formBreaker.getValidationErrors();
      expect(
        errors.length > 0 || page.url().includes('signup'),
        `Weak password "${password}" should have been rejected`
      ).toBe(true);

      await page.reload();
    }
  });
});
```

### Injection Payload Testing

```typescript
// tests/form-validation/injection-payloads.spec.ts
import { test, expect } from '../fixtures/form-breaker.fixture';
import { generateInjectionPayloads } from '../helpers/payload-generator';

test.describe('Injection Payload Testing', () => {
  test('search field should sanitize XSS payloads', async ({ page, formBreaker }) => {
    const baseUrl = process.env.BASE_URL || 'http://localhost:3000';
    await page.goto(`${baseUrl}/search`, { waitUntil: 'networkidle' });

    const xssPayloads = generateInjectionPayloads('search').filter(
      (p) => p.category === 'xss'
    );

    for (const payload of xssPayloads) {
      await formBreaker.fillFieldBypassingValidation(
        'input[name="q"], input[type="search"], input[name="search"]',
        payload.value
      );

      // Submit the search
      await page.keyboard.press('Enter');
      await page.waitForTimeout(2000);

      // Check that no script was executed
      const alertTriggered = await page.evaluate(() => {
        return (window as any).__xssTriggered === true;
      });
      expect(alertTriggered, `XSS payload should not execute: ${payload.name}`).toBeFalsy();

      // Check that the raw HTML is not reflected unescaped
      const pageContent = await page.content();
      expect(
        pageContent.includes('<script>alert'),
        `Raw script tag should not appear in page content for: ${payload.name}`
      ).toBe(false);

      await page.goto(`${baseUrl}/search`);
    }
  });

  test('login form should resist SQL injection', async ({ page, formBreaker }) => {
    const baseUrl = process.env.BASE_URL || 'http://localhost:3000';
    await page.goto(`${baseUrl}/login`, { waitUntil: 'networkidle' });

    const sqliPayloads = generateInjectionPayloads('email').filter(
      (p) => p.category === 'sqli'
    );

    for (const payload of sqliPayloads) {
      await formBreaker.fillFieldBypassingValidation(
        'input[name="email"], input[name="username"]',
        payload.value
      );
      await formBreaker.fillFieldBypassingValidation(
        'input[name="password"]',
        payload.value
      );

      const submitButton = page.getByRole('button', { name: /log in|sign in|submit/i });
      if (await submitButton.isVisible()) {
        await submitButton.click();
        await page.waitForTimeout(2000);
      }

      // Verify we are NOT logged in
      const loggedIn = await page
        .getByText(/dashboard|welcome|logout/i)
        .isVisible()
        .catch(() => false);
      expect(loggedIn, `SQL injection should not bypass auth: ${payload.name}`).toBe(false);

      // Check for SQL error messages in the response
      const pageText = await page.textContent('body');
      const sqlErrorPatterns = [
        /sql syntax/i,
        /mysql_/i,
        /pg_query/i,
        /sqlite3?_/i,
        /ORA-\d+/,
        /unclosed quotation/i,
        /unterminated string/i,
      ];

      for (const pattern of sqlErrorPatterns) {
        expect(
          pattern.test(pageText || ''),
          `SQL error should not be exposed for: ${payload.name}`
        ).toBe(false);
      }

      await page.goto(`${baseUrl}/login`);
    }
  });
});
```

### Client-Side Validation Bypass

This critical test verifies that the server rejects invalid data even when client-side validation is completely removed.

```typescript
// tests/form-validation/client-bypass.spec.ts
import { test, expect } from '../fixtures/form-breaker.fixture';

test.describe('Client-Side Validation Bypass', () => {
  test('server should reject data when HTML5 validation is removed', async ({
    page,
    formBreaker,
  }) => {
    const baseUrl = process.env.BASE_URL || 'http://localhost:3000';
    await page.goto(`${baseUrl}/signup`, { waitUntil: 'networkidle' });

    // Remove all client-side validation from the form
    await page.evaluate(() => {
      const form = document.querySelector('form');
      if (form) {
        form.setAttribute('novalidate', 'true');
        form.querySelectorAll('input, select, textarea').forEach((el) => {
          el.removeAttribute('required');
          el.removeAttribute('pattern');
          el.removeAttribute('minlength');
          el.removeAttribute('maxlength');
          el.removeAttribute('min');
          el.removeAttribute('max');
          (el as HTMLInputElement).type = 'text';
        });
      }
    });

    // Submit completely empty form
    const submitButton = page.getByRole('button', { name: /sign up|register|submit/i });
    if (await submitButton.isVisible()) {
      await submitButton.click();
      await page.waitForTimeout(3000);
    }

    // Verify server-side rejection
    const currentUrl = page.url();
    const pageText = await page.textContent('body');

    // Either we stayed on the form page, or we got server-side error messages
    const serverRejected =
      currentUrl.includes('signup') ||
      /error|required|invalid|please/i.test(pageText || '');

    expect(serverRejected, 'Server should reject empty form submission').toBe(true);
  });

  test('server should reject data submitted directly via API', async ({
    page,
    formBreaker,
  }) => {
    const baseUrl = process.env.BASE_URL || 'http://localhost:3000';

    // Send invalid data directly to the API endpoint, bypassing the UI entirely
    const invalidSubmissions = [
      { email: '', password: '' },
      { email: 'not-an-email', password: '1' },
      { email: '<script>alert(1)</script>@test.com', password: 'ValidPass123!' },
      { email: 'test@example.com', password: "' OR '1'='1" },
    ];

    for (const data of invalidSubmissions) {
      const result = await formBreaker.submitViaApi(
        `${baseUrl}/api/auth/register`,
        data as Record<string, string>
      );

      expect(
        result.status,
        `API should reject invalid data: ${JSON.stringify(data)}`
      ).toBeGreaterThanOrEqual(400);

      // Verify no SQL or internal errors are exposed
      expect(result.body).not.toMatch(/sql|syntax|stack|trace|internal server/i);
    }
  });

  test('hidden fields should not be blindly trusted', async ({ page, formBreaker }) => {
    const baseUrl = process.env.BASE_URL || 'http://localhost:3000';
    await page.goto(`${baseUrl}/checkout`, { waitUntil: 'networkidle' });

    // Manipulate hidden fields (like price, role, or discount codes)
    await page.evaluate(() => {
      const hiddenFields = document.querySelectorAll('input[type="hidden"]');
      hiddenFields.forEach((field) => {
        const input = field as HTMLInputElement;
        if (input.name.includes('price') || input.name.includes('amount')) {
          input.value = '0.01';
        }
        if (input.name.includes('role') || input.name.includes('admin')) {
          input.value = 'admin';
        }
        if (input.name.includes('discount')) {
          input.value = '99.99';
        }
      });
    });

    const submitButton = page.getByRole('button', { name: /submit|purchase|pay/i });
    if (await submitButton.isVisible()) {
      await submitButton.click();
      await page.waitForTimeout(3000);
    }

    // Verify the server did not accept the manipulated values
    // This assertion depends on your application's behavior
    const pageText = await page.textContent('body');
    expect(pageText).not.toMatch(/order confirmed.*\$0\.01/i);
  });
});
```

### File Upload Validation

```typescript
// tests/form-validation/file-upload-validation.spec.ts
import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

test.describe('File Upload Validation', () => {
  let tempDir: string;

  test.beforeAll(() => {
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'upload-test-'));
  });

  test.afterAll(() => {
    fs.rmSync(tempDir, { recursive: true, force: true });
  });

  function createTempFile(name: string, content: string | Buffer): string {
    const filePath = path.join(tempDir, name);
    fs.writeFileSync(filePath, content);
    return filePath;
  }

  test('should reject files with dangerous extensions', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'http://localhost:3000';
    await page.goto(`${baseUrl}/upload`, { waitUntil: 'networkidle' });

    const dangerousFiles = [
      createTempFile('malicious.exe', 'MZ fake exe content'),
      createTempFile('script.php', '<?php echo "pwned"; ?>'),
      createTempFile('shell.jsp', '<% Runtime.getRuntime().exec("ls"); %>'),
      createTempFile('backdoor.asp', '<% Response.Write("pwned") %>'),
      createTempFile('exploit.svg', '<svg onload="alert(1)">'),
      createTempFile('payload.html', '<script>alert(1)</script>'),
    ];

    for (const filePath of dangerousFiles) {
      const fileInput = page.locator('input[type="file"]');
      if (await fileInput.isVisible()) {
        await fileInput.setInputFiles(filePath);
        await page.waitForTimeout(1000);

        const submitButton = page.getByRole('button', { name: /upload|submit/i });
        if (await submitButton.isVisible()) {
          await submitButton.click();
          await page.waitForTimeout(2000);
        }

        // Verify the file was rejected
        const pageText = await page.textContent('body');
        const fileName = path.basename(filePath);
        expect(
          /error|rejected|not allowed|invalid/i.test(pageText || '') || page.url().includes('upload'),
          `Dangerous file "${fileName}" should have been rejected`
        ).toBe(true);

        await page.reload();
      }
    }
  });

  test('should reject files that exceed size limits', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'http://localhost:3000';
    await page.goto(`${baseUrl}/upload`, { waitUntil: 'networkidle' });

    // Create a 50MB file (likely exceeds most upload limits)
    const largeFile = createTempFile('large-file.jpg', Buffer.alloc(50 * 1024 * 1024, 0xff));

    const fileInput = page.locator('input[type="file"]');
    if (await fileInput.isVisible()) {
      await fileInput.setInputFiles(largeFile);

      const submitButton = page.getByRole('button', { name: /upload|submit/i });
      if (await submitButton.isVisible()) {
        await submitButton.click();
        await page.waitForTimeout(5000);
      }

      const pageText = await page.textContent('body');
      expect(
        /too large|size limit|exceeds|maximum/i.test(pageText || ''),
        'Large file should trigger size limit error'
      ).toBe(true);
    }
  });

  test('should verify file content matches extension', async ({ page }) => {
    const baseUrl = process.env.BASE_URL || 'http://localhost:3000';
    await page.goto(`${baseUrl}/upload`, { waitUntil: 'networkidle' });

    // Create a PHP file disguised as a JPEG
    const disguisedFile = createTempFile(
      'innocent.jpg',
      '<?php echo shell_exec($_GET["cmd"]); ?>'
    );

    const fileInput = page.locator('input[type="file"]');
    if (await fileInput.isVisible()) {
      await fileInput.setInputFiles(disguisedFile);

      const submitButton = page.getByRole('button', { name: /upload|submit/i });
      if (await submitButton.isVisible()) {
        await submitButton.click();
        await page.waitForTimeout(2000);
      }

      // A robust server should reject files where the content type does not match the extension
      const pageText = await page.textContent('body');
      expect(
        /error|invalid|rejected|not.*valid/i.test(pageText || '') || page.url().includes('upload'),
        'Disguised file should be rejected by content-type validation'
      ).toBe(true);
    }
  });
});
```

## Configuration

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/form-validation',
  timeout: 60_000,
  retries: 0, // Validation tests should be deterministic
  workers: 1, // Sequential to avoid form state conflicts
  reporter: [
    ['html', { outputFolder: 'reports/html' }],
    ['json', { outputFile: 'reports/results.json' }],
    ['list'],
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
  ],
});
```

## Best Practices

1. **Always test server-side validation independently from client-side** -- Use direct API calls (fetch/axios) to submit data that bypasses the browser entirely. If the server accepts it, the validation is incomplete.
2. **Test with the actual character encoding your database uses** -- MySQL in `utf8` mode (not `utf8mb4`) truncates 4-byte Unicode characters silently. Test with emoji and supplementary plane characters to verify full Unicode support.
3. **Verify error messages do not reveal internal details** -- Stack traces, database column names, file paths, and framework version numbers in error messages are information disclosure vulnerabilities.
4. **Test all input fields, not just the obvious ones** -- Hidden fields, dropdown values, radio button values, and URL parameters can all be manipulated by an attacker. Every server-side value that came from the client must be validated.
5. **Include timing-based tests** -- A login form that responds in 100ms for invalid usernames but 500ms for valid ones leaks user enumeration information. Measure response times for different payloads.
6. **Test with and without JavaScript enabled** -- Disable JavaScript in the browser context and verify that the form still works and still validates. HTML5 validation attributes provide a baseline.
7. **Validate CSRF token handling** -- Submit forms without the CSRF token, with an expired token, and with a token from a different session. All should be rejected.
8. **Test rate limiting on form submissions** -- Submit the same form 100 times rapidly. The server should throttle or block excessive submissions to prevent brute force attacks.
9. **Check for mass assignment vulnerabilities** -- Add extra fields to the form submission (like `role=admin` or `isVerified=true`) that are not in the original form. The server must whitelist allowed fields.
10. **Verify consistent validation between create and update operations** -- The same validation rules that apply when creating a record must also apply when updating it. Test both paths.
11. **Test multi-value fields and arrays** -- Fields like `tags[]` or `categories[]` can be manipulated to send unexpected data types. Send a string where an array is expected and vice versa.
12. **Automate regression testing for every fixed vulnerability** -- When a validation bug is found and fixed, add a specific test for that exact payload to prevent regression.

## Anti-Patterns to Avoid

1. **Relying solely on client-side validation** -- HTML5 attributes (`required`, `pattern`, `maxlength`) and JavaScript validation can be removed by any user with browser developer tools. They are a UX convenience, not a security control.
2. **Using blocklist-based input filtering** -- Trying to block known-bad inputs (like `<script>`) while allowing everything else is fragile. New attack vectors bypass blocklists constantly. Use allowlist validation (define what IS valid) instead.
3. **Validating input but not output** -- Even if you validate input, always encode output. If user input is displayed on a page, HTML-encode it. If it goes into a SQL query, use parameterized queries. Defense in depth is essential.
4. **Testing only with well-formed payloads** -- Real attackers send malformed, truncated, and mixed-encoding payloads. Test with broken UTF-8 sequences, mixed encodings, and partial submissions.
5. **Skipping file upload testing** -- File uploads are among the most dangerous input vectors. A single unrestricted file upload can lead to remote code execution. Always validate file type, size, content, and filename.
6. **Trusting Content-Type headers on file uploads** -- The `Content-Type` header is set by the client and can be spoofed. Validate file content by reading magic bytes, not by trusting the declared type.
7. **Ignoring multi-step form state manipulation** -- In wizard-style forms, attackers can skip steps, replay earlier steps with different data, or manipulate the step order. Validate the complete form state on each step transition and on final submission.

## Debugging Tips

- **Use Playwright's request interception to inspect submitted data** -- Add `page.on('request', ...)` to log the exact payload being sent. Compare it against what you intended to verify that the framework is not sanitizing your test payloads before submission.
- **Check for double encoding** -- If your test payload contains `%3C` and the server sees `%253C`, the payload is being URL-encoded twice. This can mask injection vectors during testing.
- **Inspect browser validation API directly** -- Use `page.evaluate(() => document.querySelector('input').validity)` to check the HTML5 ValidityState object and understand exactly which validation constraint is triggering.
- **Test with different Content-Type headers** -- Submitting the same data as `application/json`, `application/x-www-form-urlencoded`, and `multipart/form-data` can produce different server-side parsing behavior. Some validation may only apply to one content type.
- **Use network tab correlation** -- When a form submission is rejected, inspect the full HTTP response including headers. Look for `X-Validation-Error` custom headers or detailed error objects in the JSON response body.
- **Verify database state after submission** -- Even if the UI shows no error, the data might have been silently truncated or transformed. Query the database directly to verify the stored value matches the submitted value.
- **Check for different behavior between GET and POST** -- Some applications validate POST data but not GET parameters. If a form uses POST, try resubmitting the same data via GET to see if validation is bypassed.
- **Watch for timing differences in validation responses** -- If invalid email addresses get rejected in 50ms but SQL injection payloads take 5 seconds, it might indicate that the injection is reaching the database before being caught.