---
name: writing-docs
description: >
  Expert at writing high-quality documentation for code, APIs, and projects. Auto-invokes when
  generating docstrings, creating README files, writing API documentation, adding code comments,
  or producing any technical documentation. Provides language-specific templates and best practices
  for effective documentation writing.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Writing Documentation Skill

You are an expert at writing clear, comprehensive, and useful documentation for software projects.

## When This Skill Activates

This skill auto-invokes when:
- User asks to "document this function/class/module"
- User wants to create or update a README
- User needs JSDoc, docstrings, or code comments
- User asks for API documentation
- User wants documentation for a specific file or codebase

## Documentation Writing Principles

### Core Principles

1. **Clarity Over Cleverness**
   - Use simple, direct language
   - Avoid jargon when possible
   - Define technical terms when first used

2. **Show, Don't Just Tell**
   - Include working code examples
   - Demonstrate common use cases
   - Show expected outputs

3. **Structure for Scanning**
   - Use clear headings
   - Keep paragraphs short
   - Use lists for multiple items
   - Highlight important information

4. **Write for Your Audience**
   - Consider the reader's expertise level
   - Provide appropriate context
   - Link to prerequisites when needed

## Language-Specific Templates

### JavaScript/TypeScript (JSDoc)

```javascript
/**
 * Brief one-line description of what the function does.
 *
 * Longer description if needed. Explain the purpose, behavior,
 * and any important details about how the function works.
 *
 * @param {string} name - The user's display name
 * @param {Object} options - Configuration options
 * @param {boolean} [options.verbose=false] - Enable verbose output
 * @param {number} [options.timeout=5000] - Timeout in milliseconds
 * @returns {Promise<User>} The created user object
 * @throws {ValidationError} When name is empty or invalid
 * @throws {TimeoutError} When the operation times out
 *
 * @example
 * // Basic usage
 * const user = await createUser('John Doe');
 *
 * @example
 * // With options
 * const user = await createUser('Jane', {
 *   verbose: true,
 *   timeout: 10000
 * });
 *
 * @see {@link User} for the user object structure
 * @since 1.2.0
 */
```

### Python (Google Style Docstrings)

```python
def create_user(name: str, **options) -> User:
    """Create a new user with the given name.

    Longer description if needed. Explain the purpose, behavior,
    and any important details about how the function works.

    Args:
        name: The user's display name. Must be non-empty.
        **options: Optional keyword arguments.
            verbose (bool): Enable verbose output. Defaults to False.
            timeout (int): Timeout in milliseconds. Defaults to 5000.

    Returns:
        User: The created user object with populated fields.

    Raises:
        ValidationError: When name is empty or invalid.
        TimeoutError: When the operation times out.

    Example:
        Basic usage::

            user = create_user('John Doe')

        With options::

            user = create_user('Jane', verbose=True, timeout=10000)

    Note:
        The user is not persisted until `user.save()` is called.

    See Also:
        User: The user object class.
    """
```

### Go

```go
// CreateUser creates a new user with the given name.
//
// CreateUser validates the name, initializes a User struct with default
// values, and returns a pointer to the new user. The user is not persisted
// to the database until Save() is called.
//
// Parameters:
//   - name: The user's display name. Must be non-empty string.
//   - opts: Optional configuration. See UserOptions for available options.
//
// Returns the created User pointer and any error encountered.
//
// Example:
//
//	user, err := CreateUser("John Doe", nil)
//	if err != nil {
//	    log.Fatal(err)
//	}
//
// Errors:
//   - ErrEmptyName: returned when name is empty
//   - ErrInvalidName: returned when name contains invalid characters
func CreateUser(name string, opts *UserOptions) (*User, error) {
```

### Rust

```rust
/// Creates a new user with the given name.
///
/// This function validates the name, initializes a User struct with default
/// values, and returns the new user. The user is not persisted to the
/// database until [`User::save`] is called.
///
/// # Arguments
///
/// * `name` - The user's display name. Must be non-empty.
/// * `options` - Optional configuration settings.
///
/// # Returns
///
/// Returns `Ok(User)` on success, or an error if validation fails.
///
/// # Errors
///
/// * [`UserError::EmptyName`] - If `name` is empty.
/// * [`UserError::InvalidName`] - If `name` contains invalid characters.
///
/// # Examples
///
/// Basic usage:
///
/// ```
/// let user = create_user("John Doe", None)?;
/// ```
///
/// With options:
///
/// ```
/// let opts = UserOptions { verbose: true, ..Default::default() };
/// let user = create_user("Jane", Some(opts))?;
/// ```
///
/// # Panics
///
/// This function does not panic under normal circumstances.
```

## README Template

```markdown
# Project Name

Brief description of what this project does and why it exists.

## Features

- Feature 1: Brief description
- Feature 2: Brief description
- Feature 3: Brief description

## Installation

### Prerequisites

- Requirement 1 (version X.X+)
- Requirement 2

### Install via [package manager]

\`\`\`bash
npm install project-name
# or
pip install project-name
\`\`\`

### Install from source

\`\`\`bash
git clone https://github.com/user/project-name
cd project-name
npm install
\`\`\`

## Quick Start

\`\`\`javascript
import { Project } from 'project-name';

const project = new Project();
project.doSomething();
\`\`\`

## Usage

### Basic Example

\`\`\`javascript
// Code example with comments
\`\`\`

### Advanced Usage

\`\`\`javascript
// More complex example
\`\`\`

## API Reference

### `functionName(param1, param2)`

Description of the function.

**Parameters:**
- `param1` (Type): Description
- `param2` (Type, optional): Description. Default: `value`

**Returns:** Type - Description

**Example:**
\`\`\`javascript
const result = functionName('value', { option: true });
\`\`\`

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `option1` | string | `"default"` | Description |
| `option2` | number | `10` | Description |

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## License

[License Type] - see [LICENSE](LICENSE) for details.
```

## Writing Guidelines

### Function Documentation

**Always Include:**
1. Brief description (first line)
2. Parameter descriptions with types
3. Return value description
4. Possible errors/exceptions
5. At least one example

**Include When Relevant:**
- Side effects
- Performance considerations
- Thread safety notes
- Deprecation notices
- Links to related functions

### Class Documentation

**Always Include:**
1. Class purpose and responsibility
2. Constructor documentation
3. Public method documentation
4. Important properties

**Include When Relevant:**
- Inheritance relationships
- Interface implementations
- State management notes
- Lifecycle information

### Module/File Documentation

**Always Include:**
1. Module purpose
2. Main exports
3. Usage overview

**Include When Relevant:**
- Dependencies
- Configuration requirements
- Architecture notes

## Common Patterns

### Documenting Options Objects

```javascript
/**
 * @typedef {Object} CreateUserOptions
 * @property {boolean} [verbose=false] - Enable verbose logging
 * @property {number} [timeout=5000] - Operation timeout in ms
 * @property {string} [role='user'] - Initial user role
 */

/**
 * Creates a user with the specified options.
 * @param {string} name - User name
 * @param {CreateUserOptions} [options] - Configuration options
 */
```

### Documenting Callbacks

```javascript
/**
 * @callback UserCallback
 * @param {Error|null} error - Error if operation failed
 * @param {User} user - The user object if successful
 */

/**
 * Fetches a user asynchronously.
 * @param {string} id - User ID
 * @param {UserCallback} callback - Called with result
 */
```

### Documenting Generic Types

```typescript
/**
 * A generic result wrapper.
 * @template T - The type of the success value
 * @template E - The type of the error value
 */
interface Result<T, E> {
  /** Whether the operation succeeded */
  success: boolean;
  /** The success value, if success is true */
  value?: T;
  /** The error value, if success is false */
  error?: E;
}
```

## Quality Checklist

Before finalizing documentation, verify:

- [ ] First line is a clear, concise summary
- [ ] All parameters are documented with types
- [ ] Return value is documented
- [ ] Errors/exceptions are documented
- [ ] At least one working example is included
- [ ] Example code is tested and correct
- [ ] Language is clear and grammatically correct
- [ ] Formatting is consistent with codebase style
- [ ] Links to related documentation are included
- [ ] Edge cases and limitations are noted

## Integration

This skill works with:
- **analyzing-docs** skill for identifying what needs documentation
- **managing-docs** skill for organizing documentation structure
- **docs-analyzer** agent for comprehensive documentation projects
