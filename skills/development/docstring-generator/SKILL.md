---
name: docstring-generator
description: Generate language-specific docstrings for C#, Java, Python, and TypeScript following industry standards (PEP 257, Javadoc, JSDoc, XML documentation)
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: documentation
---

## What I do

I generate language-specific docstrings and documentation following industry standards:

1. **Detect Language**: Analyze file extension and project structure to determine language
2. **Detect Docstring Style**: Identify existing docstring conventions in codebase
3. **Generate Docstrings**: Create appropriate docstrings following language conventions
4. **Support Multiple Formats**:
   - **Python**: PEP 257 (Google, NumPy, Sphinx/reST styles)
   - **Java**: Javadoc format with @param, @return, @throws
   - **TypeScript**: JSDoc/TSDoc format with @param, @returns, @throws
   - **C#**: XML documentation comments with <summary>, <param>, <returns>, <exception>
5. **Handle Various Types**: Functions, methods, classes, interfaces, properties, exceptions
6. **Enforce Documentation**: Ensure docstrings are added during PR workflow

## When to use me

Use this workflow when:
- Implementing new functions, classes, or methods in Python, Java, TypeScript, or C#
- Refactoring code and updating documentation
- Creating new APIs or public interfaces
- Following documentation best practices and industry standards
- Need to ensure all public code has proper docstrings
- Preparing code for code review and maintainability

**Integration**: This skill integrates with `pr-creation-workflow` and `linting-workflow` to enforce docstring presence as part of quality checks.

## Prerequisites

- Source code files (.py, .java, .ts, .tsx, .cs, .csx)
- File permissions to read and write files
- Knowledge of preferred docstring style (optional, can auto-detect)
- For workflow integration: Git repository initialized

## Supported Languages and Standards

### Python
**Standard**: PEP 257 compliant
**Supported Styles**:
- **Google Style** (recommended for most projects)
- **NumPy Style** (for scientific computing)
- **Sphinx/reST Style** (for documentation generation)

**Features**:
- Type hints support (Python 3.5+)
- Exception documentation with Raises section
- Parameter documentation with Args section
- Return value documentation with Returns section
- Example code blocks in docstrings

### Java
**Standard**: Javadoc
**Supported Tags**:
- `@param` - Parameter documentation
- `@return` / `@returns` - Return value documentation
- `@throws` - Exception documentation
- `@see` - Related references
- `@author` - Author information
- `@version` - Version information
- `@since` - Since version
- `@deprecated` - Deprecation notice
- `@link` - Link to related code

**Features**:
- Generic type parameters
- Method overload documentation
- Interface documentation
- Annotation documentation
- Inheritance documentation

### TypeScript
**Standard**: JSDoc / TSDoc
**Supported Tags**:
- `@param` - Parameter documentation
- `@returns` / `@return` - Return value documentation
- `@throws` - Exception documentation
- `@type` - Type definitions
- `@example` - Usage examples
- `@see` - Related references
- `@deprecated` - Deprecation notice
- `@interface` - Interface documentation
- `@extends` - Inheritance documentation

**Features**:
- Generic type parameters
- Union types documentation
- Optional parameters
- Interface and class documentation
- Module documentation

### C#
**Standard**: XML Documentation Comments
**Supported Tags**:
- `<summary>` - Brief description
- `<param name="">` - Parameter documentation
- `<returns>` - Return value documentation
- `<exception cref="">` - Exception documentation
- `<typeparam>` - Generic type parameter documentation
- `<remarks>` - Additional remarks
- `<example>` - Code examples
- `<seealso>` - Related references

**Features**:
- Generic type parameters
- Method overload documentation
- Property documentation
- Event handler documentation
- XML attribute escaping

## Steps

### Step 1: Detect Language

Analyze file to determine programming language:

```bash
# Check file extension
case "$file_ext" in
    py)    LANG="python" ;;
    java)   LANG="java" ;;
    ts|tsx) LANG="typescript" ;;
    cs|csx) LANG="csharp" ;;
    *)      LANG="unknown" ;;
esac

echo "Detected language: $LANG"
```

### Step 2: Detect Docstring Style

Analyze existing docstrings in codebase to maintain consistency:

```bash
# Python style detection
if grep -q '"""' file.py; then
    if grep -q 'Args:' file.py; then
        STYLE="google"
    elif grep -q 'Parameters' file.py; then
        STYLE="numpy"
    elif grep -q ':param' file.py; then
        STYLE="sphinx"
    fi
fi

echo "Detected docstring style: $STYLE"
```

### Step 3: Analyze Function/Method

Extract function signature and determine docstring needs:

```bash
# Extract function/method signature
if [[ "$LANG" == "python" ]]; then
    # Python function
    FUNCTION=$(grep -A 5 'def ' file.py | head -1)
elif [[ "$LANG" == "java" ]]; then
    # Java method
    METHOD=$(grep -B 2 'public.*(' file.java | head -1)
fi

echo "Function to document: $FUNCTION"
```

### Step 4: Generate Docstring

Generate appropriate docstring based on language and style:

#### Python (Google Style)
```python
def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two integers.

    Args:
        a: The first integer to add.
        b: The second integer to add.

    Returns:
        The sum of a and b.

    Raises:
        TypeError: If either a or b is not an integer.

    Examples:
        >>> calculate_sum(5, 3)
        8
    """
    return a + b
```

#### Java (Javadoc)
```java
/**
 * Calculates the sum of two integers.
 *
 * @param a The first integer to add
 * @param b The second integer to add
 * @return The sum of a and b
 * @throws IllegalArgumentException If either a or b is not an integer
 *
 * @see #calculateProduct(int, int)
 * @since 1.0
 * @author Developer Name
 */
public int calculateSum(int a, int b) {
    return a + b;
}
```

#### TypeScript (JSDoc)
```typescript
/**
 * Calculates the sum of two integers.
 *
 * @param a - The first integer to add
 * @param b - The second integer to add
 * @returns The sum of a and b
 * @throws {TypeError} If either a or b is not an integer
 *
 * @example
 * ```typescript
 * const result = calculateSum(5, 3); // returns 8
 * ```
 *
 * @see calculateProduct
 * @since 1.0.0
 */
function calculateSum(a: number, b: number): number {
    return a + b;
}
```

#### C# (XML Documentation)
```csharp
/// <summary>
/// Calculates the sum of two integers.
/// </summary>
/// <param name="a">The first integer to add</param>
/// <param name="b">The second integer to add</param>
/// <returns>The sum of a and b</returns>
/// <exception cref="System.ArgumentException">
/// Thrown when either a or b is not an integer
/// </exception>
/// <example>
/// <code>
/// int result = CalculateSum(5, 3); // returns 8
/// </code>
/// </example>
/// <seealso cref="CalculateProduct"/>
public int CalculateSum(int a, int b) {
    return a + b;
}
```

### Step 5: Update File

Insert docstring into the correct location in the file:

```bash
# Find function/method start line
LINE_NUM=$(grep -n "^def\|^public.*(" "$FILE" | head -1 | cut -d: -f1)

# Insert docstring after signature (line + 1)
sed -i "$((LINE_NUM+1))i\\$DOCSTRING" "$FILE"
```

## Docstring Format Reference

### Python Styles

#### Google Style (Recommended)
```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief one-line description.

    Longer description of function's purpose and behavior.

    Args:
        param1: Description of param1 with its type.
        param2: Description of param2 with its type.

    Returns:
        Description of return value and its type.

    Raises:
        ErrorType: Condition when error is raised.

    Examples:
        >>> function_name(arg1, arg2)
        Expected output
    """
```

#### NumPy Style
```python
def function_name(param1, param2):
    """
    Brief description.

    Extended description.

    Parameters
    ----------
    param1 : type
        Description of param1.
    param2 : type
        Description of param2.

    Returns
    -------
    return_type
        Description of return value.

    Raises
    ------
    ErrorType
        Condition when error is raised.

    See Also
    --------
    related_function
    """
```

#### Sphinx/reST Style
```python
def function_name(param1, param2):
    """
    Brief description.

    Extended description.

    :param param1: Description of param1.
    :type param1: type
    :param param2: Description of param2.
    :type param2: type
    :returns: Description of return value.
    :rtype: return_type
    :raises ErrorType: Condition when error is raised.
    :see: related_function
    """
```

### Java Javadoc Tags

```java
/**
 * Brief description on first line.
 *
 * Extended description with details.
 *
 * @param paramName Description of parameter
 * @param paramName2 Description of second parameter
 * @return Description of return value
 * @throws ExceptionType Description of when exception is thrown
 * @see RelatedClass#relatedMethod
 * @see #relatedMethod(int, int)
 * @since 1.0
 * @author Author Name
 * @version 1.1
 * @deprecated Use newMethod instead
 * @link https://example.com Related documentation
 */
```

### TypeScript JSDoc Tags

```typescript
/**
 * Brief description.
 *
 * Extended description.
 *
 * @param paramName - Description of parameter
 * @param paramName2 - Description of second parameter
 * @returns Description of return value
 * @throws {ErrorType} Description of when error is thrown
 * @type TypeName - Type definition
 * @extends ParentType - Inheritance
 * @implements InterfaceName - Interface implementation
 * @example
 * ```typescript
 * const result = functionName(arg1, arg2);
 * ```
 * @see RelatedClass#relatedMethod
 * @since 1.0.0
 * @deprecated Use newFunction instead
 * @see relatedFunction
 */
```

### C# XML Tags

```csharp
/// <summary>
/// Brief description.
/// </summary>
/// <remarks>
/// Extended description with details.
/// </remarks>
/// <param name="paramName">Description of parameter</param>
/// <param name="paramName2">Description of second parameter</param>
/// <returns>Description of return value</returns>
/// <exception cref="System.Exception">
/// Description of when exception is thrown
/// </exception>
/// <typeparam name="T">Generic type parameter</typeparam>
/// <example>
/// <code>
/// var result = FunctionName(arg1, arg2);
/// </code>
/// </example>
/// <seealso cref="RelatedClass.RelatedMethod"/>
/// <permission cref="System.Security.Permissions">
/// Required permissions
/// </permission>
```

## Special Cases

### Generics

#### Java
```java
/**
 * Processes a list of items.
 *
 * @param <T> The type of items in the list
 * @param items List of items to process
 * @return Processed list of items
 */
public <T> List<T> processItems(List<T> items) {
    // Implementation
}
```

#### TypeScript
```typescript
/**
 * Processes a list of items.
 *
 * @type T - The type of items in the list
 * @param items - List of items to process
 * @returns Processed list of items
 */
function processItems<T>(items: T[]): T[] {
    // Implementation
}
```

#### C#
```csharp
/// <summary>
/// Processes a list of items.
/// </summary>
/// <typeparam name="T">The type of items in the list</typeparam>
/// <param name="items">List of items to process</param>
/// <returns>Processed list of items</returns>
public List<T> ProcessItems<T>(List<T> items) {
    // Implementation
}
```

### Method Overloads

#### Java
```java
/**
 * Calculates the sum.
 *
 * @param a First integer
 * @param b Second integer
 * @return Sum of two integers
 */
public int calculateSum(int a, int b) {
    return a + b;
}

/**
 * Calculates the sum of three integers.
 *
 * @param a First integer
 * @param b Second integer
 * @param c Third integer
 * @return Sum of three integers
 */
public int calculateSum(int a, int b, int c) {
    return a + b + c;
}
```

#### C#
```csharp
/// <summary>
/// Calculates the sum.
/// </summary>
/// <param name="a">First integer</param>
/// <param name="b">Second integer</param>
/// <returns>Sum of two integers</returns>
public int CalculateSum(int a, int b) {
    return a + b;
}

/// <summary>
/// Calculates the sum of three integers.
/// </summary>
/// <param name="a">First integer</param>
/// <param name="b">Second integer</param>
/// <param name="c">Third integer</param>
/// <returns>Sum of three integers</returns>
public int CalculateSum(int a, int b, int c) {
    return a + b + c;
}
```

### Type Hints

#### Python (3.5+)
```python
def process_data(
    data: list[dict[str, Any]],
    options: dict[str, Any] | None = None
) -> dict[str, list[Any]]:
    """
    Process data with optional configuration.

    Args:
        data: List of dictionaries containing data entries.
        options: Optional dictionary of configuration options.

    Returns:
        Dictionary with processed data organized by category.
    """
    # Implementation
```

#### TypeScript
```typescript
/**
 * Process data with optional configuration.
 *
 * @type DataItem - Type of items in data array
 * @param data - Array of data items to process
 * @param options - Optional configuration object
 * @returns Processed data organized by category
 */
function processData<DataItem>(
    data: DataItem[],
    options?: Record<string, unknown>
): Record<string, DataItem[]> {
    // Implementation
}
```

## Best Practices

### General
- **Document all public APIs**: Functions, classes, methods, properties
- **Use clear language**: Write as if explaining to another developer
- **Keep descriptions concise**: Be thorough but not overly verbose
- **Follow existing style**: Maintain consistency with codebase conventions
- **Include examples**: Show typical usage patterns
- **Document edge cases**: What happens with null, empty, invalid inputs?
- **Update docstrings**: Keep them in sync with code changes
- **Document exceptions**: Clearly state what exceptions can be raised/thrown

### Python-Specific
- Use triple quotes (`"""`) for docstrings
- Place docstring immediately after function/class definition
- Include type hints in function signatures
- Use Google style by default (most popular)
- Document all parameters, even optional ones
- Include type information in Args/Returns sections

### Java-Specific
- Use `/** ... */` format for Javadoc
- Place docstring immediately before method/class
- Document all @param tags (one per parameter)
- Use `@return` for simple types, `@returns` for complex types
- Include @throws for all checked exceptions
- Document generics with `<T>` notation
- Add @see for related methods

### TypeScript-Specific
- Use `/** ... */` format for JSDoc
- Place docstring immediately before function/class
- Include type information in @param tags
- Use @throws with {Type} for type safety
- Document exported members
- Include @example blocks for usage
- Document generic type parameters with @type

### C#-Specific
- Use `///` for single-line XML comments
- Use `/** ... */` for multi-line XML comments
- Place docstring immediately before element
- Use XML tags for structured documentation
- Escape special characters in XML (e.g., `<` becomes `&lt;`)
- Document generics with <typeparam>
- Include <remarks> for extended descriptions

## Common Issues

### Python: Indentation Errors
**Issue**: Docstring indentation doesn't match code indentation

**Solution**: Use consistent indentation (4 spaces preferred)

```python
def function():
    """Docstring at same indent as code."""
    pass
```

### Java: Missing @param Tags
**Issue**: Javadoc warnings about missing parameter documentation

**Solution**: Document all parameters, even if obvious

```java
/**
 * Method description.
 *
 * @param x First parameter
 * @param y Second parameter  <-- Often forgotten
 */
public void method(int x, int y) {
}
```

### TypeScript: Missing Type in @throws
**Issue**: Type safety lost without exception type

**Solution**: Always include type in @throws

```typescript
/**
 * Method description.
 *
 * @throws {Error} When something goes wrong  <-- Good
 */
```

### C#: XML Escaping Issues
**Issue**: Special characters break XML documentation

**Solution**: Use HTML entities or CDATA sections

```csharp
/// <summary>
/// Method with <special> characters  <-- Bad
/// </summary>

/// <summary>
/// Method with &lt;special&gt; characters  <-- Good
/// </summary>
```

## Workflow Integration

### PR Creation
Check for missing docstrings during PR creation:

```bash
# Find undocumented functions/methdos
for file in $(git diff --name-only); do
    case "$file" in
        *.py)    UNDOC=$(grep -c 'def ' "$file") \
                    - $(grep -c '"""' "$file") ;;
        *.java)   UNDOC=$(grep -c 'public.*(' "$file") \
                    - $(grep -c '/\*\*' "$file") ;;
        *.ts)     UNDOC=$(grep -c 'function' "$file") \
                    - $(grep -c '/\*\*' "$file") ;;
        *.cs)     UNDOC=$(grep -c 'public.*(' "$file") \
                    - $(grep -c '///' "$file") ;;
    esac

    if [[ $UNDOC -gt 0 ]]; then
        echo "Found $UNDOC undocumented items in $file"
    fi
done
```

### Linting Integration
Add docstring validation to linters:

**Python**:
```bash
# Use pydocstyle for style checking
pydocstyle file.py
```

**Java**:
```bash
# Use Checkstyle for Javadoc validation
checkstyle -c checkstyle_javadoc.xml file.java
```

**TypeScript**:
```bash
# Use TSDoc linter
tslint --doc file.ts
```

### Code Review Checklist
- [ ] All public functions have docstrings
- [ ] All public classes have docstrings
- [ ] All parameters are documented
- [ ] Return values are documented
- [ ] Exceptions are documented
- [ ] Docstrings follow language conventions
- [ ] Docstrings are accurate and up-to-date

## Troubleshooting Checklist

Before generating docstrings:
- [ ] Language is correctly detected
- [ ] File extension is recognized
- [ ] Docstring style is determined
- [ ] Existing style in codebase is detected

After generating docstrings:
- [ ] Docstrings are inserted at correct location
- [ ] Docstrings follow language conventions
- [ ] All parameters are documented
- [ ] Return values are documented
- [ ] Exceptions are documented
- [ ] Examples are included (if applicable)
- [ ] Docstrings are formatted correctly

## Related Skills

- `nextjs-standard-setup`: For creating standardized Next.js 16 applications with proper documentation standards
- `opencode-skill-creation`: For creating OpenCode skills
- `pr-creation-workflow`: For adding docstring validation to PR workflow
- `linting-workflow`: For enforcing docstring presence in code
- `python-pytest-creator`: For generating Python tests with docstrings
