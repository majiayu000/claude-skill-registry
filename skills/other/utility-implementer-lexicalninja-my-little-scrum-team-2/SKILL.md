---
name: utility-implementer
description: Implements utility functions, helpers, and shared code. Use when implementing reusable functions, validation utilities, formatting functions, or helper modules. Creates clean, reusable utility code.
---

# Utility Implementer Skill

## Instructions

1. Analyze utility requirements from task
2. Design utility function interface
3. Implement utility function with proper error handling
4. Add input validation
5. Handle edge cases
6. Write comprehensive tests
7. Return implementation with:
   - Utility function code
   - Input validation
   - Error handling
   - Documentation
   - Tests

## Examples

**Input:** "Implement password hashing utility"
**Output:**
```javascript
// utils/password.js
const bcrypt = require('bcrypt');

/**
 * Hash a password using bcrypt
 * @param {string} password - Plain text password
 * @param {number} rounds - Number of bcrypt rounds (default: 10)
 * @returns {Promise<string>} Hashed password
 * @throws {Error} If password is invalid
 */
async function hashPassword(password, rounds = 10) {
    if (!password || typeof password !== 'string') {
        throw new Error('Password must be a non-empty string');
    }
    if (password.length < 8) {
        throw new Error('Password must be at least 8 characters');
    }
    return await bcrypt.hash(password, rounds);
}

/**
 * Verify a password against a hash
 * @param {string} password - Plain text password
 * @param {string} hash - Hashed password
 * @returns {Promise<boolean>} True if password matches
 */
async function verifyPassword(password, hash) {
    if (!password || !hash) {
        return false;
    }
    return await bcrypt.compare(password, hash);
}

module.exports = { hashPassword, verifyPassword };
```

## Utility Types

- **Validation Utilities**: Input validation, data validation
- **Formatting Utilities**: Date formatting, number formatting, text formatting
- **Transformation Utilities**: Data transformation, conversion functions
- **Security Utilities**: Password hashing, token generation, encryption
- **Helper Functions**: Common operations, calculations, string manipulation
- **Constants**: Shared constants, configuration values

## Best Practices

- **Pure Functions**: Prefer pure functions when possible
- **Error Handling**: Comprehensive error handling
- **Input Validation**: Validate all inputs
- **Documentation**: Document function purpose, parameters, return values
- **Reusability**: Make utilities reusable
- **Testing**: Comprehensive test coverage
- **Performance**: Consider performance implications
