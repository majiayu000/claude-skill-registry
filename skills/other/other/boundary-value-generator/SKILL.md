---
name: Boundary Value Generator
description: Generate boundary value test cases for numeric ranges, string lengths, date ranges, collection sizes, and domain-specific constraints using systematic analysis techniques
version: 1.0.0
author: Pramod
license: MIT
tags: [boundary-value, bva, equivalence-partitioning, edge-cases, test-design, numeric-testing, range-testing]
testingTypes: [unit, integration]
frameworks: [jest, vitest, pytest]
languages: [typescript, javascript, python, java]
domains: [web, api]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt, gemini-cli, amp]
---

# Boundary Value Generator Skill

You are an expert QA engineer specializing in boundary value analysis (BVA) and equivalence class partitioning. When the user asks you to generate boundary value tests, identify edge cases, or create systematic test data for ranges and constraints, follow these detailed instructions to produce comprehensive boundary test suites that catch off-by-one errors, overflow conditions, and constraint violations.

## Core Principles

1. **Test at the boundary, not in the middle** -- Most bugs cluster at the boundaries of input domains. For a valid range of 1-100, the most informative test values are 0, 1, 2, 99, 100, and 101, not 50. Always prioritize boundary values over mid-range values.
2. **Apply the BVA triplet pattern** -- For every boundary, test three values: the boundary itself, one value immediately below, and one value immediately above. This catches off-by-one errors in both directions (using < instead of <=, or > instead of >=).
3. **Combine BVA with equivalence partitioning** -- Equivalence partitioning identifies the domains; BVA identifies the specific test values within each domain. Use both techniques together for maximum coverage with minimum test cases.
4. **Domain boundaries are not just numbers** -- Boundary analysis applies to string lengths, date ranges, collection sizes, file sizes, API rate limits, pagination offsets, and any other constrained input. Identify all input dimensions and their boundaries.
5. **Invalid boundaries must reject cleanly** -- Testing below-minimum and above-maximum values verifies that the system rejects invalid input with clear error messages rather than silently truncating, wrapping, or crashing.
6. **Type boundaries are critical** -- Beyond domain-specific boundaries, test the boundaries of the underlying data type: zero, negative zero, MAX_SAFE_INTEGER, MIN_SAFE_INTEGER, NaN, Infinity, empty string, null, and undefined.
7. **Boundary tests must be deterministic** -- Every boundary test must produce the same result every time. Avoid test values that depend on system clock, random generation, or external state.

## Project Structure

```
tests/
  boundary/
    numeric/
      integer-ranges.test.ts
      float-precision.test.ts
      currency-amounts.test.ts
      percentage-values.test.ts
    string/
      length-limits.test.ts
      unicode-boundaries.test.ts
      encoding-limits.test.ts
    date-time/
      date-ranges.test.ts
      time-zones.test.ts
      epoch-boundaries.test.ts
    collection/
      array-sizes.test.ts
      pagination.test.ts
      batch-limits.test.ts
    file/
      file-size-limits.test.ts
      upload-constraints.test.ts
    api/
      rate-limits.test.ts
      payload-sizes.test.ts
      concurrent-connections.test.ts
    generators/
      boundary-generator.ts
      equivalence-partitioner.ts
      test-case-formatter.ts
    fixtures/
      constraint-definitions.ts
      type-boundaries.ts
  vitest.config.ts
```

## Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['tests/boundary/**/*.test.ts'],
    globals: true,
    reporters: ['verbose', 'json'],
    outputFile: 'boundary-test-report.json',
    coverage: {
      provider: 'v8',
      include: ['src/**/*.ts'],
      exclude: ['src/**/*.d.ts'],
    },
  },
});
```

```typescript
// tests/boundary/fixtures/constraint-definitions.ts

/**
 * Centralized constraint definitions for all boundary-testable inputs.
 * Each constraint defines the valid range and metadata for a specific input parameter.
 */
export interface BoundaryConstraint {
  name: string;
  type: 'integer' | 'float' | 'string' | 'date' | 'collection' | 'fileSize';
  min: number | string;
  max: number | string;
  unit?: string;
  description: string;
}

export const constraints: BoundaryConstraint[] = [
  // Numeric constraints
  { name: 'user-age', type: 'integer', min: 13, max: 120, unit: 'years', description: 'User age for registration' },
  { name: 'quantity', type: 'integer', min: 1, max: 99, unit: 'items', description: 'Product quantity in cart' },
  { name: 'price', type: 'float', min: 0.01, max: 999999.99, unit: 'USD', description: 'Product price' },
  { name: 'discount', type: 'float', min: 0, max: 100, unit: 'percent', description: 'Discount percentage' },
  { name: 'rating', type: 'float', min: 1.0, max: 5.0, unit: 'stars', description: 'Product rating' },

  // String constraints
  { name: 'username', type: 'string', min: 3, max: 30, unit: 'characters', description: 'Username length' },
  { name: 'password', type: 'string', min: 8, max: 128, unit: 'characters', description: 'Password length' },
  { name: 'bio', type: 'string', min: 0, max: 500, unit: 'characters', description: 'User biography' },
  { name: 'search-query', type: 'string', min: 1, max: 200, unit: 'characters', description: 'Search input' },

  // Collection constraints
  { name: 'cart-items', type: 'collection', min: 0, max: 50, unit: 'items', description: 'Shopping cart item count' },
  { name: 'tags', type: 'collection', min: 0, max: 10, unit: 'tags', description: 'Tags per item' },
  { name: 'page-size', type: 'integer', min: 1, max: 100, unit: 'results', description: 'Pagination page size' },

  // File constraints
  { name: 'avatar', type: 'fileSize', min: 1, max: 5242880, unit: 'bytes', description: 'Avatar file size (5MB max)' },
  { name: 'document', type: 'fileSize', min: 1, max: 26214400, unit: 'bytes', description: 'Document upload (25MB max)' },
];
```

```typescript
// tests/boundary/fixtures/type-boundaries.ts

/**
 * Language-level type boundaries for JavaScript/TypeScript.
 * These values represent the limits of the data types themselves,
 * independent of domain-specific constraints.
 */
export const TYPE_BOUNDARIES = {
  integer: {
    MAX_SAFE_INTEGER: Number.MAX_SAFE_INTEGER,     // 9007199254740991
    MIN_SAFE_INTEGER: Number.MIN_SAFE_INTEGER,     // -9007199254740991
    MAX_VALUE: Number.MAX_VALUE,                    // 1.7976931348623157e+308
    MIN_VALUE: Number.MIN_VALUE,                    // 5e-324 (smallest positive)
    POSITIVE_INFINITY: Number.POSITIVE_INFINITY,
    NEGATIVE_INFINITY: Number.NEGATIVE_INFINITY,
    NaN: Number.NaN,
    NEGATIVE_ZERO: -0,
    ZERO: 0,
  },
  string: {
    EMPTY: '',
    SINGLE_CHAR: 'a',
    MAX_PRACTICAL_LENGTH: 10_000_000,  // Most systems struggle beyond this
    NULL_BYTE: '\x00',
    UNICODE_BMP_MAX: '\uFFFF',
    UNICODE_SUPPLEMENTARY: '\u{1F600}',  // Emoji (2 UTF-16 code units)
    RTL_CHAR: '\u0627',                  // Arabic alef
    ZERO_WIDTH_SPACE: '\u200B',
    COMBINING_CHARS: 'e\u0301',          // e + combining acute accent
  },
  date: {
    EPOCH: new Date(0),                           // 1970-01-01T00:00:00Z
    PRE_EPOCH: new Date(-1),                      // 1969-12-31T23:59:59.999Z
    Y2K: new Date('2000-01-01T00:00:00Z'),
    Y2K38: new Date('2038-01-19T03:14:07Z'),      // Unix 32-bit overflow
    FAR_FUTURE: new Date('9999-12-31T23:59:59Z'),
    LEAP_DAY: new Date('2024-02-29T00:00:00Z'),
    DST_SPRING: new Date('2024-03-10T02:00:00'),  // US DST spring forward
    DST_FALL: new Date('2024-11-03T02:00:00'),    // US DST fall back
    INVALID: new Date('invalid'),
  },
};
```

## How-To Guides

### Generating Numeric Boundary Test Cases

The core of boundary value analysis is systematically generating test values at and around the edges of valid ranges.

```typescript
// tests/boundary/generators/boundary-generator.ts

export interface BoundaryTestCase {
  value: number | string;
  expected: 'valid' | 'invalid';
  category: 'below-min' | 'at-min' | 'above-min' | 'nominal' | 'below-max' | 'at-max' | 'above-max' | 'type-boundary';
  description: string;
}

/**
 * Generate boundary value test cases for an integer range.
 * Applies the BVA triplet pattern: boundary, boundary-1, boundary+1.
 */
export function generateIntegerBoundaries(
  min: number,
  max: number,
  name: string
): BoundaryTestCase[] {
  return [
    // Below minimum boundary
    { value: min - 2, expected: 'invalid', category: 'below-min', description: `${name}: far below minimum (${min - 2})` },
    { value: min - 1, expected: 'invalid', category: 'below-min', description: `${name}: just below minimum (${min - 1})` },

    // Minimum boundary
    { value: min, expected: 'valid', category: 'at-min', description: `${name}: exactly at minimum (${min})` },
    { value: min + 1, expected: 'valid', category: 'above-min', description: `${name}: just above minimum (${min + 1})` },

    // Nominal value
    { value: Math.floor((min + max) / 2), expected: 'valid', category: 'nominal', description: `${name}: nominal mid-range` },

    // Maximum boundary
    { value: max - 1, expected: 'valid', category: 'below-max', description: `${name}: just below maximum (${max - 1})` },
    { value: max, expected: 'valid', category: 'at-max', description: `${name}: exactly at maximum (${max})` },

    // Above maximum boundary
    { value: max + 1, expected: 'invalid', category: 'above-max', description: `${name}: just above maximum (${max + 1})` },
    { value: max + 2, expected: 'invalid', category: 'above-max', description: `${name}: far above maximum (${max + 2})` },

    // Type boundaries
    { value: 0, expected: min > 0 ? 'invalid' : 'valid', category: 'type-boundary', description: `${name}: zero` },
    { value: -1, expected: min > -1 ? 'invalid' : 'valid', category: 'type-boundary', description: `${name}: negative one` },
    { value: Number.MAX_SAFE_INTEGER, expected: max < Number.MAX_SAFE_INTEGER ? 'invalid' : 'valid', category: 'type-boundary', description: `${name}: MAX_SAFE_INTEGER` },
  ];
}

/**
 * Generate boundary values for floating-point ranges.
 * Includes precision-sensitive values around the boundaries.
 */
export function generateFloatBoundaries(
  min: number,
  max: number,
  precision: number,
  name: string
): BoundaryTestCase[] {
  const step = Math.pow(10, -precision); // e.g., 0.01 for 2 decimal places

  return [
    // Below minimum
    { value: parseFloat((min - step).toFixed(precision)), expected: 'invalid', category: 'below-min', description: `${name}: one step below minimum` },

    // Minimum boundary
    { value: min, expected: 'valid', category: 'at-min', description: `${name}: exactly at minimum (${min})` },
    { value: parseFloat((min + step).toFixed(precision)), expected: 'valid', category: 'above-min', description: `${name}: one step above minimum` },

    // Nominal
    { value: parseFloat(((min + max) / 2).toFixed(precision)), expected: 'valid', category: 'nominal', description: `${name}: nominal mid-range` },

    // Maximum boundary
    { value: parseFloat((max - step).toFixed(precision)), expected: 'valid', category: 'below-max', description: `${name}: one step below maximum` },
    { value: max, expected: 'valid', category: 'at-max', description: `${name}: exactly at maximum (${max})` },

    // Above maximum
    { value: parseFloat((max + step).toFixed(precision)), expected: 'invalid', category: 'above-max', description: `${name}: one step above maximum` },

    // Floating-point precision edge cases
    { value: 0.1 + 0.2, expected: 'valid', category: 'type-boundary', description: `${name}: IEEE 754 precision (0.1 + 0.2 = ${0.1 + 0.2})` },
    { value: Number.EPSILON, expected: min <= Number.EPSILON ? 'valid' : 'invalid', category: 'type-boundary', description: `${name}: Number.EPSILON` },
  ];
}

/**
 * Generate boundary values for string length constraints.
 */
export function generateStringLengthBoundaries(
  minLength: number,
  maxLength: number,
  name: string
): BoundaryTestCase[] {
  return [
    // Empty and below minimum
    { value: '', expected: minLength > 0 ? 'invalid' : 'valid', category: 'below-min', description: `${name}: empty string (0 chars)` },
    { value: 'a'.repeat(Math.max(0, minLength - 1)), expected: minLength > 0 ? 'invalid' : 'valid', category: 'below-min', description: `${name}: ${Math.max(0, minLength - 1)} characters` },

    // Minimum boundary
    { value: 'a'.repeat(minLength), expected: 'valid', category: 'at-min', description: `${name}: exactly ${minLength} characters (minimum)` },
    { value: 'a'.repeat(minLength + 1), expected: 'valid', category: 'above-min', description: `${name}: ${minLength + 1} characters` },

    // Nominal
    { value: 'a'.repeat(Math.floor((minLength + maxLength) / 2)), expected: 'valid', category: 'nominal', description: `${name}: mid-range length` },

    // Maximum boundary
    { value: 'a'.repeat(maxLength - 1), expected: 'valid', category: 'below-max', description: `${name}: ${maxLength - 1} characters` },
    { value: 'a'.repeat(maxLength), expected: 'valid', category: 'at-max', description: `${name}: exactly ${maxLength} characters (maximum)` },

    // Above maximum
    { value: 'a'.repeat(maxLength + 1), expected: 'invalid', category: 'above-max', description: `${name}: ${maxLength + 1} characters` },
    { value: 'a'.repeat(maxLength + 100), expected: 'invalid', category: 'above-max', description: `${name}: significantly over maximum` },
  ];
}
```

### Writing Numeric Boundary Tests

Using the generator to produce actual test suites.

```typescript
// tests/boundary/numeric/integer-ranges.test.ts

import { describe, it, expect } from 'vitest';
import { generateIntegerBoundaries } from '../generators/boundary-generator';
import { constraints } from '../fixtures/constraint-definitions';

// Example: testing a validation function
function validateAge(age: number): { valid: boolean; error?: string } {
  if (!Number.isInteger(age)) return { valid: false, error: 'Age must be a whole number' };
  if (age < 13) return { valid: false, error: 'Must be at least 13 years old' };
  if (age > 120) return { valid: false, error: 'Age exceeds maximum allowed value' };
  return { valid: true };
}

function validateQuantity(qty: number): { valid: boolean; error?: string } {
  if (!Number.isInteger(qty)) return { valid: false, error: 'Quantity must be a whole number' };
  if (qty < 1) return { valid: false, error: 'Quantity must be at least 1' };
  if (qty > 99) return { valid: false, error: 'Maximum quantity is 99' };
  return { valid: true };
}

describe('Integer Range Boundaries', () => {
  describe('User Age Validation', () => {
    const ageConstraint = constraints.find((c) => c.name === 'user-age')!;
    const testCases = generateIntegerBoundaries(
      ageConstraint.min as number,
      ageConstraint.max as number,
      'age'
    );

    for (const tc of testCases) {
      it(`${tc.description} -> ${tc.expected}`, () => {
        const result = validateAge(tc.value as number);
        if (tc.expected === 'valid') {
          expect(result.valid).toBe(true);
          expect(result.error).toBeUndefined();
        } else {
          expect(result.valid).toBe(false);
          expect(result.error).toBeDefined();
          expect(result.error!.length).toBeGreaterThan(0);
        }
      });
    }

    // Additional type boundary tests
    it('rejects NaN', () => {
      const result = validateAge(NaN);
      expect(result.valid).toBe(false);
    });

    it('rejects Infinity', () => {
      const result = validateAge(Infinity);
      expect(result.valid).toBe(false);
    });

    it('rejects floating-point numbers', () => {
      const result = validateAge(25.5);
      expect(result.valid).toBe(false);
    });

    it('rejects negative zero', () => {
      const result = validateAge(-0);
      // -0 is technically 0, which is below minimum
      expect(result.valid).toBe(false);
    });
  });

  describe('Product Quantity Validation', () => {
    const qtyConstraint = constraints.find((c) => c.name === 'quantity')!;
    const testCases = generateIntegerBoundaries(
      qtyConstraint.min as number,
      qtyConstraint.max as number,
      'quantity'
    );

    for (const tc of testCases) {
      it(`${tc.description} -> ${tc.expected}`, () => {
        const result = validateQuantity(tc.value as number);
        expect(result.valid).toBe(tc.expected === 'valid');
      });
    }
  });
});
```

### Testing Floating-Point and Currency Boundaries

Financial calculations require special boundary attention due to IEEE 754 floating-point precision.

```typescript
// tests/boundary/numeric/currency-amounts.test.ts

import { describe, it, expect } from 'vitest';
import { generateFloatBoundaries } from '../generators/boundary-generator';

function validatePrice(price: number): { valid: boolean; error?: string } {
  if (typeof price !== 'number' || isNaN(price)) {
    return { valid: false, error: 'Price must be a number' };
  }
  if (!isFinite(price)) {
    return { valid: false, error: 'Price must be finite' };
  }
  if (price < 0.01) {
    return { valid: false, error: 'Price must be at least $0.01' };
  }
  if (price > 999999.99) {
    return { valid: false, error: 'Price exceeds maximum' };
  }

  // Check for more than 2 decimal places
  const decimalStr = price.toString();
  const decimalPart = decimalStr.includes('.') ? decimalStr.split('.')[1] : '';
  if (decimalPart.length > 2) {
    return { valid: false, error: 'Price must have at most 2 decimal places' };
  }

  return { valid: true };
}

describe('Currency Amount Boundaries', () => {
  const testCases = generateFloatBoundaries(0.01, 999999.99, 2, 'price');

  for (const tc of testCases) {
    it(`${tc.description} -> ${tc.expected}`, () => {
      const result = validatePrice(tc.value as number);
      expect(result.valid).toBe(tc.expected === 'valid');
    });
  }

  describe('Floating-point precision edge cases', () => {
    it('handles 0.1 + 0.2 correctly', () => {
      // 0.1 + 0.2 = 0.30000000000000004 in IEEE 754
      // The system must handle this gracefully
      const sum = 0.1 + 0.2;
      const result = validatePrice(parseFloat(sum.toFixed(2)));
      expect(result.valid).toBe(true);
    });

    it('handles currency multiplication precision', () => {
      // $19.99 * 3 = 59.97, but floating-point may produce 59.96999...
      const total = 19.99 * 3;
      const result = validatePrice(parseFloat(total.toFixed(2)));
      expect(result.valid).toBe(true);
    });

    it('rejects amounts with more than 2 decimal places', () => {
      expect(validatePrice(9.999).valid).toBe(false);
      expect(validatePrice(0.001).valid).toBe(false);
      expect(validatePrice(100.123).valid).toBe(false);
    });

    it('accepts exact boundary: $0.01', () => {
      expect(validatePrice(0.01).valid).toBe(true);
    });

    it('accepts exact boundary: $999999.99', () => {
      expect(validatePrice(999999.99).valid).toBe(true);
    });

    it('rejects $0.00', () => {
      expect(validatePrice(0.00).valid).toBe(false);
    });

    it('rejects negative amounts', () => {
      expect(validatePrice(-0.01).valid).toBe(false);
      expect(validatePrice(-100).valid).toBe(false);
    });
  });
});
```

### Testing Date and Time Boundaries

Dates have unique boundary conditions: leap years, daylight saving time transitions, epoch boundaries, and the Y2K38 problem.

```typescript
// tests/boundary/date-time/date-ranges.test.ts

import { describe, it, expect } from 'vitest';
import { TYPE_BOUNDARIES } from '../fixtures/type-boundaries';

function validateEventDate(date: Date): { valid: boolean; error?: string } {
  if (!(date instanceof Date) || isNaN(date.getTime())) {
    return { valid: false, error: 'Invalid date' };
  }

  const now = new Date();
  const oneYearFromNow = new Date(now);
  oneYearFromNow.setFullYear(oneYearFromNow.getFullYear() + 1);

  if (date < now) {
    return { valid: false, error: 'Event date must be in the future' };
  }

  if (date > oneYearFromNow) {
    return { valid: false, error: 'Event date must be within one year' };
  }

  return { valid: true };
}

function validateBirthDate(date: Date): { valid: boolean; error?: string } {
  if (!(date instanceof Date) || isNaN(date.getTime())) {
    return { valid: false, error: 'Invalid date' };
  }

  const now = new Date();
  const age = now.getFullYear() - date.getFullYear();

  if (date > now) {
    return { valid: false, error: 'Birth date cannot be in the future' };
  }

  if (age > 150) {
    return { valid: false, error: 'Birth date too far in the past' };
  }

  return { valid: true };
}

describe('Date Range Boundaries', () => {
  describe('Event Date Validation', () => {
    it('rejects dates in the past', () => {
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      expect(validateEventDate(yesterday).valid).toBe(false);
    });

    it('accepts tomorrow', () => {
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      expect(validateEventDate(tomorrow).valid).toBe(true);
    });

    it('accepts exactly one year from now', () => {
      const oneYear = new Date();
      oneYear.setFullYear(oneYear.getFullYear() + 1);
      expect(validateEventDate(oneYear).valid).toBe(true);
    });

    it('rejects one year and one day from now', () => {
      const beyondOneYear = new Date();
      beyondOneYear.setFullYear(beyondOneYear.getFullYear() + 1);
      beyondOneYear.setDate(beyondOneYear.getDate() + 1);
      expect(validateEventDate(beyondOneYear).valid).toBe(false);
    });

    it('rejects invalid date object', () => {
      expect(validateEventDate(TYPE_BOUNDARIES.date.INVALID).valid).toBe(false);
    });
  });

  describe('Critical Date Boundaries', () => {
    it('handles leap year boundary: Feb 29', () => {
      const leapDay = new Date('2024-02-29T12:00:00Z');
      expect(leapDay.getDate()).toBe(29);
      expect(leapDay.getMonth()).toBe(1); // 0-indexed
    });

    it('handles non-leap year: Feb 28 to Mar 1', () => {
      const feb28 = new Date('2023-02-28T23:59:59Z');
      const mar1 = new Date(feb28.getTime() + 1000);
      expect(mar1.getDate()).toBe(1);
      expect(mar1.getMonth()).toBe(2); // March
    });

    it('handles epoch boundary', () => {
      const result = validateBirthDate(TYPE_BOUNDARIES.date.EPOCH);
      expect(result.valid).toBe(true);
    });

    it('handles pre-epoch date', () => {
      const result = validateBirthDate(new Date('1969-12-31T23:59:59Z'));
      expect(result.valid).toBe(true);
    });

    it('handles Y2K38 boundary', () => {
      // Unix 32-bit timestamp overflow: 2038-01-19T03:14:07Z
      const y2k38 = TYPE_BOUNDARIES.date.Y2K38;
      expect(y2k38.getTime()).toBeGreaterThan(0);
    });

    it('handles far future date', () => {
      const farFuture = TYPE_BOUNDARIES.date.FAR_FUTURE;
      expect(farFuture.getFullYear()).toBe(9999);
    });

    it('handles month-end transitions', () => {
      const monthEnds = [
        new Date('2024-01-31T23:59:59Z'), // Jan 31 -> Feb 1
        new Date('2024-03-31T23:59:59Z'), // Mar 31 -> Apr 1
        new Date('2024-04-30T23:59:59Z'), // Apr 30 -> May 1
        new Date('2024-12-31T23:59:59Z'), // Dec 31 -> Jan 1 (year transition)
      ];

      for (const date of monthEnds) {
        const nextSecond = new Date(date.getTime() + 1000);
        expect(nextSecond.getDate()).toBe(1);
      }
    });

    it('handles year-end transition', () => {
      const yearEnd = new Date('2024-12-31T23:59:59Z');
      const newYear = new Date(yearEnd.getTime() + 1000);
      expect(newYear.getFullYear()).toBe(2025);
      expect(newYear.getMonth()).toBe(0);
      expect(newYear.getDate()).toBe(1);
    });
  });
});
```

### Testing Collection Size Boundaries

Arrays, lists, and other collections have their own boundary conditions related to size, indexing, and pagination.

```typescript
// tests/boundary/collection/array-sizes.test.ts

import { describe, it, expect } from 'vitest';

function validateCartItems(items: unknown[]): { valid: boolean; error?: string } {
  if (!Array.isArray(items)) {
    return { valid: false, error: 'Items must be an array' };
  }
  if (items.length === 0) {
    return { valid: false, error: 'Cart must have at least one item' };
  }
  if (items.length > 50) {
    return { valid: false, error: 'Cart cannot exceed 50 items' };
  }
  return { valid: true };
}

function validateTags(tags: string[]): { valid: boolean; error?: string } {
  if (!Array.isArray(tags)) {
    return { valid: false, error: 'Tags must be an array' };
  }
  if (tags.length > 10) {
    return { valid: false, error: 'Maximum 10 tags allowed' };
  }
  // Each tag has its own constraints
  for (const tag of tags) {
    if (tag.length < 1 || tag.length > 50) {
      return { valid: false, error: 'Each tag must be 1-50 characters' };
    }
  }
  return { valid: true };
}

describe('Collection Size Boundaries', () => {
  describe('Cart Items', () => {
    it('rejects empty cart', () => {
      expect(validateCartItems([]).valid).toBe(false);
    });

    it('accepts single item (minimum)', () => {
      expect(validateCartItems(['item1']).valid).toBe(true);
    });

    it('accepts two items (above minimum)', () => {
      expect(validateCartItems(['item1', 'item2']).valid).toBe(true);
    });

    it('accepts 49 items (below maximum)', () => {
      const items = Array.from({ length: 49 }, (_, i) => `item${i}`);
      expect(validateCartItems(items).valid).toBe(true);
    });

    it('accepts 50 items (at maximum)', () => {
      const items = Array.from({ length: 50 }, (_, i) => `item${i}`);
      expect(validateCartItems(items).valid).toBe(true);
    });

    it('rejects 51 items (above maximum)', () => {
      const items = Array.from({ length: 51 }, (_, i) => `item${i}`);
      expect(validateCartItems(items).valid).toBe(false);
    });
  });

  describe('Tags', () => {
    it('accepts empty tags array', () => {
      expect(validateTags([]).valid).toBe(true);
    });

    it('accepts single tag', () => {
      expect(validateTags(['typescript']).valid).toBe(true);
    });

    it('accepts 10 tags (at maximum)', () => {
      const tags = Array.from({ length: 10 }, (_, i) => `tag${i}`);
      expect(validateTags(tags).valid).toBe(true);
    });

    it('rejects 11 tags (above maximum)', () => {
      const tags = Array.from({ length: 11 }, (_, i) => `tag${i}`);
      expect(validateTags(tags).valid).toBe(false);
    });

    it('rejects tag with 0 characters', () => {
      expect(validateTags(['']).valid).toBe(false);
    });

    it('rejects tag with 51 characters', () => {
      expect(validateTags(['a'.repeat(51)]).valid).toBe(false);
    });
  });
});
```

### Testing Pagination Boundaries

Pagination has multiple boundary dimensions: page number, page size, total count, and offset calculations.

```typescript
// tests/boundary/collection/pagination.test.ts

import { describe, it, expect } from 'vitest';

interface PaginationParams {
  page: number;
  pageSize: number;
  totalItems: number;
}

interface PaginationResult {
  valid: boolean;
  error?: string;
  offset?: number;
  limit?: number;
  totalPages?: number;
  hasNext?: boolean;
  hasPrevious?: boolean;
}

function calculatePagination(params: PaginationParams): PaginationResult {
  const { page, pageSize, totalItems } = params;

  if (!Number.isInteger(page) || page < 1) {
    return { valid: false, error: 'Page must be a positive integer' };
  }
  if (!Number.isInteger(pageSize) || pageSize < 1 || pageSize > 100) {
    return { valid: false, error: 'Page size must be between 1 and 100' };
  }
  if (totalItems < 0) {
    return { valid: false, error: 'Total items cannot be negative' };
  }

  const totalPages = Math.max(1, Math.ceil(totalItems / pageSize));

  if (page > totalPages) {
    return { valid: false, error: `Page ${page} exceeds total pages (${totalPages})` };
  }

  const offset = (page - 1) * pageSize;

  return {
    valid: true,
    offset,
    limit: pageSize,
    totalPages,
    hasNext: page < totalPages,
    hasPrevious: page > 1,
  };
}

describe('Pagination Boundaries', () => {
  describe('Page number boundaries', () => {
    it('accepts page 1 (minimum)', () => {
      const result = calculatePagination({ page: 1, pageSize: 20, totalItems: 100 });
      expect(result.valid).toBe(true);
      expect(result.offset).toBe(0);
      expect(result.hasPrevious).toBe(false);
    });

    it('rejects page 0', () => {
      const result = calculatePagination({ page: 0, pageSize: 20, totalItems: 100 });
      expect(result.valid).toBe(false);
    });

    it('rejects negative page', () => {
      const result = calculatePagination({ page: -1, pageSize: 20, totalItems: 100 });
      expect(result.valid).toBe(false);
    });

    it('accepts last page', () => {
      const result = calculatePagination({ page: 5, pageSize: 20, totalItems: 100 });
      expect(result.valid).toBe(true);
      expect(result.hasNext).toBe(false);
      expect(result.offset).toBe(80);
    });

    it('rejects page beyond last', () => {
      const result = calculatePagination({ page: 6, pageSize: 20, totalItems: 100 });
      expect(result.valid).toBe(false);
    });
  });

  describe('Page size boundaries', () => {
    it('accepts page size 1 (minimum)', () => {
      const result = calculatePagination({ page: 1, pageSize: 1, totalItems: 100 });
      expect(result.valid).toBe(true);
      expect(result.totalPages).toBe(100);
    });

    it('accepts page size 100 (maximum)', () => {
      const result = calculatePagination({ page: 1, pageSize: 100, totalItems: 100 });
      expect(result.valid).toBe(true);
      expect(result.totalPages).toBe(1);
    });

    it('rejects page size 0', () => {
      const result = calculatePagination({ page: 1, pageSize: 0, totalItems: 100 });
      expect(result.valid).toBe(false);
    });

    it('rejects page size 101', () => {
      const result = calculatePagination({ page: 1, pageSize: 101, totalItems: 100 });
      expect(result.valid).toBe(false);
    });
  });

  describe('Total items edge cases', () => {
    it('handles zero total items', () => {
      const result = calculatePagination({ page: 1, pageSize: 20, totalItems: 0 });
      expect(result.valid).toBe(true);
      expect(result.totalPages).toBe(1);
    });

    it('handles single item', () => {
      const result = calculatePagination({ page: 1, pageSize: 20, totalItems: 1 });
      expect(result.valid).toBe(true);
      expect(result.totalPages).toBe(1);
    });

    it('handles exact page boundary (100 items, 20 per page = 5 pages)', () => {
      const result = calculatePagination({ page: 5, pageSize: 20, totalItems: 100 });
      expect(result.valid).toBe(true);
      expect(result.totalPages).toBe(5);
      expect(result.hasNext).toBe(false);
    });

    it('handles one over page boundary (101 items = 6 pages)', () => {
      const result = calculatePagination({ page: 6, pageSize: 20, totalItems: 101 });
      expect(result.valid).toBe(true);
      expect(result.totalPages).toBe(6);
    });
  });
});
```

### Testing API Rate Limit Boundaries

API rate limits are a critical boundary that affects system behavior under load.

```typescript
// tests/boundary/api/rate-limits.test.ts

import { describe, it, expect } from 'vitest';

interface RateLimitConfig {
  maxRequests: number;
  windowMs: number;
}

interface RateLimitResult {
  allowed: boolean;
  remaining: number;
  resetAt: number;
  retryAfterMs?: number;
}

class RateLimiter {
  private requests: number[] = [];

  constructor(private config: RateLimitConfig) {}

  check(now: number = Date.now()): RateLimitResult {
    // Remove expired requests
    const windowStart = now - this.config.windowMs;
    this.requests = this.requests.filter((t) => t > windowStart);

    if (this.requests.length >= this.config.maxRequests) {
      const oldestRequest = this.requests[0];
      const resetAt = oldestRequest + this.config.windowMs;
      return {
        allowed: false,
        remaining: 0,
        resetAt,
        retryAfterMs: resetAt - now,
      };
    }

    this.requests.push(now);
    return {
      allowed: true,
      remaining: this.config.maxRequests - this.requests.length,
      resetAt: now + this.config.windowMs,
    };
  }

  reset(): void {
    this.requests = [];
  }
}

describe('API Rate Limit Boundaries', () => {
  const config: RateLimitConfig = { maxRequests: 100, windowMs: 60000 };

  it('allows request 1 (first request)', () => {
    const limiter = new RateLimiter(config);
    const result = limiter.check();
    expect(result.allowed).toBe(true);
    expect(result.remaining).toBe(99);
  });

  it('allows request 99 (one below limit)', () => {
    const limiter = new RateLimiter(config);
    const now = Date.now();

    for (let i = 0; i < 98; i++) {
      limiter.check(now + i);
    }

    const result = limiter.check(now + 98);
    expect(result.allowed).toBe(true);
    expect(result.remaining).toBe(1);
  });

  it('allows request 100 (at limit)', () => {
    const limiter = new RateLimiter(config);
    const now = Date.now();

    for (let i = 0; i < 99; i++) {
      limiter.check(now + i);
    }

    const result = limiter.check(now + 99);
    expect(result.allowed).toBe(true);
    expect(result.remaining).toBe(0);
  });

  it('rejects request 101 (above limit)', () => {
    const limiter = new RateLimiter(config);
    const now = Date.now();

    for (let i = 0; i < 100; i++) {
      limiter.check(now + i);
    }

    const result = limiter.check(now + 100);
    expect(result.allowed).toBe(false);
    expect(result.remaining).toBe(0);
    expect(result.retryAfterMs).toBeGreaterThan(0);
  });

  it('allows requests after window resets', () => {
    const limiter = new RateLimiter(config);
    const now = Date.now();

    // Fill the window
    for (let i = 0; i < 100; i++) {
      limiter.check(now + i);
    }

    // After the window passes, requests should be allowed again
    const afterWindow = now + config.windowMs + 1;
    const result = limiter.check(afterWindow);
    expect(result.allowed).toBe(true);
  });
});
```

### Python Implementation: Boundary Value Generation

For Python teams using pytest, boundary generation follows the same systematic pattern.

```python
# tests/boundary/generators/boundary_generator.py

from dataclasses import dataclass
from typing import Union, Literal
import math


@dataclass
class BoundaryTestCase:
    value: Union[int, float, str]
    expected: Literal["valid", "invalid"]
    category: str
    description: str


def generate_integer_boundaries(
    min_val: int, max_val: int, name: str
) -> list[BoundaryTestCase]:
    """Generate boundary value test cases for an integer range."""
    return [
        BoundaryTestCase(min_val - 2, "invalid", "below-min", f"{name}: far below min ({min_val - 2})"),
        BoundaryTestCase(min_val - 1, "invalid", "below-min", f"{name}: just below min ({min_val - 1})"),
        BoundaryTestCase(min_val, "valid", "at-min", f"{name}: at minimum ({min_val})"),
        BoundaryTestCase(min_val + 1, "valid", "above-min", f"{name}: just above min ({min_val + 1})"),
        BoundaryTestCase((min_val + max_val) // 2, "valid", "nominal", f"{name}: mid-range"),
        BoundaryTestCase(max_val - 1, "valid", "below-max", f"{name}: just below max ({max_val - 1})"),
        BoundaryTestCase(max_val, "valid", "at-max", f"{name}: at maximum ({max_val})"),
        BoundaryTestCase(max_val + 1, "invalid", "above-max", f"{name}: just above max ({max_val + 1})"),
        BoundaryTestCase(max_val + 2, "invalid", "above-max", f"{name}: far above max ({max_val + 2})"),
        BoundaryTestCase(0, "invalid" if min_val > 0 else "valid", "type-boundary", f"{name}: zero"),
        BoundaryTestCase(-1, "invalid" if min_val > -1 else "valid", "type-boundary", f"{name}: negative one"),
    ]


def generate_string_length_boundaries(
    min_len: int, max_len: int, name: str
) -> list[BoundaryTestCase]:
    """Generate boundary value test cases for string length constraints."""
    return [
        BoundaryTestCase("", "invalid" if min_len > 0 else "valid", "below-min", f"{name}: empty string"),
        BoundaryTestCase("a" * max(0, min_len - 1), "invalid" if min_len > 0 else "valid", "below-min", f"{name}: {max(0, min_len - 1)} chars"),
        BoundaryTestCase("a" * min_len, "valid", "at-min", f"{name}: {min_len} chars (minimum)"),
        BoundaryTestCase("a" * (min_len + 1), "valid", "above-min", f"{name}: {min_len + 1} chars"),
        BoundaryTestCase("a" * ((min_len + max_len) // 2), "valid", "nominal", f"{name}: mid-range"),
        BoundaryTestCase("a" * (max_len - 1), "valid", "below-max", f"{name}: {max_len - 1} chars"),
        BoundaryTestCase("a" * max_len, "valid", "at-max", f"{name}: {max_len} chars (maximum)"),
        BoundaryTestCase("a" * (max_len + 1), "invalid", "above-max", f"{name}: {max_len + 1} chars"),
    ]
```

```python
# tests/boundary/test_numeric_boundaries.py

import pytest
from generators.boundary_generator import generate_integer_boundaries


def validate_age(age: int) -> tuple[bool, str]:
    """Validate user age for registration."""
    if not isinstance(age, int):
        return False, "Age must be an integer"
    if age < 13:
        return False, "Must be at least 13 years old"
    if age > 120:
        return False, "Age exceeds maximum"
    return True, ""


class TestAgeBoundaries:
    """Parameterized boundary tests for user age validation."""

    @pytest.fixture
    def boundary_cases(self):
        return generate_integer_boundaries(13, 120, "age")

    @pytest.mark.parametrize(
        "test_case",
        generate_integer_boundaries(13, 120, "age"),
        ids=lambda tc: tc.description,
    )
    def test_age_boundary(self, test_case):
        is_valid, error = validate_age(test_case.value)
        if test_case.expected == "valid":
            assert is_valid, f"Expected valid for {test_case.value}, got error: {error}"
        else:
            assert not is_valid, f"Expected invalid for {test_case.value}"

    def test_rejects_none(self):
        is_valid, _ = validate_age(None)
        assert not is_valid

    def test_rejects_float(self):
        is_valid, _ = validate_age(25.5)
        assert not is_valid

    def test_rejects_string(self):
        is_valid, _ = validate_age("25")
        assert not is_valid
```

### Testing File Size Boundaries

File uploads have both size boundaries and content-type boundaries.

```typescript
// tests/boundary/file/file-size-limits.test.ts

import { describe, it, expect } from 'vitest';

interface FileValidationResult {
  valid: boolean;
  error?: string;
}

function validateFileUpload(
  sizeBytes: number,
  maxBytes: number,
  allowedTypes: string[],
  fileType: string
): FileValidationResult {
  if (sizeBytes <= 0) {
    return { valid: false, error: 'File is empty' };
  }
  if (sizeBytes > maxBytes) {
    return { valid: false, error: `File exceeds maximum size of ${maxBytes} bytes` };
  }
  if (!allowedTypes.includes(fileType)) {
    return { valid: false, error: `File type ${fileType} is not allowed` };
  }
  return { valid: true };
}

describe('File Size Boundaries', () => {
  const MAX_AVATAR_SIZE = 5 * 1024 * 1024; // 5MB
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];

  it('rejects zero-byte file', () => {
    const result = validateFileUpload(0, MAX_AVATAR_SIZE, allowedTypes, 'image/jpeg');
    expect(result.valid).toBe(false);
  });

  it('accepts 1-byte file (minimum)', () => {
    const result = validateFileUpload(1, MAX_AVATAR_SIZE, allowedTypes, 'image/jpeg');
    expect(result.valid).toBe(true);
  });

  it('accepts file at exact maximum (5MB)', () => {
    const result = validateFileUpload(MAX_AVATAR_SIZE, MAX_AVATAR_SIZE, allowedTypes, 'image/jpeg');
    expect(result.valid).toBe(true);
  });

  it('rejects file one byte over maximum', () => {
    const result = validateFileUpload(MAX_AVATAR_SIZE + 1, MAX_AVATAR_SIZE, allowedTypes, 'image/jpeg');
    expect(result.valid).toBe(false);
  });

  it('accepts file one byte under maximum', () => {
    const result = validateFileUpload(MAX_AVATAR_SIZE - 1, MAX_AVATAR_SIZE, allowedTypes, 'image/jpeg');
    expect(result.valid).toBe(true);
  });

  it('rejects file at common misleading boundary (5,000,000 bytes is not 5MB)', () => {
    // 5MB = 5,242,880 bytes, not 5,000,000
    // Files between these values should still be accepted
    const result = validateFileUpload(5_100_000, MAX_AVATAR_SIZE, allowedTypes, 'image/jpeg');
    expect(result.valid).toBe(true);
  });
});
```

## Best Practices

1. **Use the BVA triplet for every boundary** -- For every boundary value B, always test B-1, B, and B+1. This systematic approach catches the most common off-by-one errors with minimal test cases.

2. **Centralize constraint definitions** -- Define all boundary constraints in a single fixture file. This makes it easy to update constraints when requirements change and ensures all test suites reference the same limits.

3. **Use generators, not manual test data** -- Write generator functions that accept constraints and produce test cases. This eliminates manual calculation errors and makes it trivial to generate new test suites when constraints change.

4. **Test both the boundary and the error message** -- Verifying that invalid input is rejected is only half the test. Also verify that the error message is specific, helpful, and does not reveal implementation details.

5. **Include type-level boundaries alongside domain boundaries** -- Domain boundaries (age 13-120) and type boundaries (MAX_SAFE_INTEGER, NaN, Infinity) are both important. Always test what happens when input exceeds the capacity of the underlying data type.

6. **Parameterize boundary tests** -- Use test parameterization (test.each in Vitest/Jest, @pytest.mark.parametrize in pytest) to run the same assertion logic against every generated boundary value.

7. **Test the interaction of multiple boundaries** -- When a function has two constrained inputs (e.g., quantity 1-99 and price 0.01-999999.99), test the combination of both at their boundaries: minimum quantity with maximum price, maximum quantity with minimum price, and so on.

8. **Document why each boundary exists** -- Each boundary constraint should have a description explaining why it exists. "Maximum 50 items" is a business rule; "MAX_SAFE_INTEGER" is a technical constraint. Both need testing, but for different reasons.

9. **Run boundary tests in CI on every commit** -- Boundary tests are fast (they test validation logic, not full integration flows) and catch the most common class of bugs. They should run on every commit, not just nightly.

10. **Version your constraint definitions** -- When constraints change (e.g., max password length increases from 64 to 128), update the constraint definition and regenerate all affected test suites. Keep the constraint definitions under version control.

11. **Test Unicode string length boundaries carefully** -- A string length of 10 characters can mean different things depending on whether you count bytes, UTF-16 code units, or Unicode code points. An emoji like a flag character may count as 1 visible character but occupy 4-8 bytes. Test with multi-byte characters at the boundary.

## Anti-Patterns to Avoid

1. **Testing only mid-range values** -- A test that validates age=25 tells you nothing about what happens at age=12 or age=121. Mid-range values confirm that the happy path works but miss boundary bugs entirely.

2. **Hardcoding boundary values in tests** -- If the maximum price changes from 999999.99 to 1999999.99, every hardcoded test value must be updated. Generate boundary values from centralized constraints instead.

3. **Testing boundaries without testing the adjacent invalid values** -- Knowing that 1 is accepted is useful, but knowing that 0 is rejected is equally important. Always test both sides of every boundary.

4. **Ignoring floating-point precision** -- Testing that 0.01 is accepted and 0.00 is rejected is correct but incomplete. Also test values like 0.009999999 and 0.010000001, which may behave unexpectedly due to IEEE 754 representation.

5. **Using random values for boundary testing** -- Random testing (fuzzing) is valuable for discovering unknown boundaries, but it is not a substitute for systematic BVA. A random test may never generate the exact boundary value needed to expose a bug.

6. **Skipping negative and zero values** -- Many off-by-one bugs occur at the zero boundary. Always test 0, -0, -1, and negative values for any numeric input, even when the valid range is entirely positive.

7. **Treating string length as simple character count** -- String length boundaries must account for multi-byte Unicode characters, combining characters, and surrogate pairs. A test that checks length=10 with ASCII characters should also check length=10 with emoji or CJK characters.

## Debugging Tips

- **Off-by-one in range checks**: If boundary=100 is rejected when it should be accepted, check whether the validation uses `<` instead of `<=`, or `>` instead of `>=`. The BVA triplet pattern (99, 100, 101) is designed to detect exactly this error.

- **Floating-point comparison failures**: If `0.1 + 0.2 === 0.3` returns false in your boundary test, use a tolerance-based comparison: `Math.abs(a - b) < Number.EPSILON` or use `toBeCloseTo()` in Jest/Vitest instead of `toBe()`.

- **String length discrepancies with Unicode**: If a 10-character emoji string fails a maxLength=10 check, the validation may be counting UTF-16 code units instead of grapheme clusters. Use `Intl.Segmenter` for accurate grapheme counting or verify which length metric the validation uses.

- **Date boundary fails across time zones**: If a date boundary test passes locally but fails in CI, check whether the test and the validation function use the same time zone. Use UTC dates in tests (`new Date('2024-01-01T00:00:00Z')`) to eliminate time zone ambiguity.

- **Pagination returns empty on last page**: If the last page returns empty results, check whether the offset calculation uses zero-based or one-based indexing. An off-by-one in `(page - 1) * pageSize` versus `page * pageSize` shifts the entire result window.

- **Rate limiter off by one**: If the rate limiter blocks at 99 requests instead of 100, check whether it counts the current request before or after the limit check. The order of `increment` and `compare` matters.

- **File size check uses wrong units**: If a 5MB file is rejected by a 5MB limit, check whether the validation compares bytes to megabytes or uses 1000 vs 1024 as the conversion factor. 5MB = 5,242,880 bytes (binary) or 5,000,000 bytes (decimal).

- **Integer overflow in boundary math**: If `max + 1` wraps around to a negative number, the language or data type may have overflowed. In JavaScript, this occurs at `Number.MAX_SAFE_INTEGER + 1 === Number.MAX_SAFE_INTEGER + 2` (both equal 9007199254740992). Use BigInt for values that might exceed safe integer range.
