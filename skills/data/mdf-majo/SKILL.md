---
name: mdf-majo
description: meadow Docstring Format (MDF) specification for Python documentation. Use when writing, editing, or reviewing docstrings for Python code. Provides a plaintext-first, readable format that closely follows Python syntax. Trigger when the user mentions docstrings, Python documentation, function documentation, class documentation, or writing documentation for Python code.
license: Unlicense
metadata:
  author: mark@joshwel.co
  version: "2026.2.2"
---

# meadow Docstring Format (MDF)

## Goal

Standardize Python docstring formatting to be plaintext-first, readable, and closely aligned with Python syntax. MDF provides an intuitive documentation style that works across editors while maintaining clarity and consistency.

## When to Use This Skill

**Use this skill when:**
- Writing new docstrings for Python functions, classes, or modules
- Editing or reviewing existing Python documentation
- The user asks about docstring format or Python documentation style
- Adding documentation to Python codebases following the meadow standards
- Reviewing code that lacks proper documentation

## Do NOT use

- For general markdown documentation (use `writing-docs-majo` instead)
- For non-Python languages
- For external API documentation not embedded in Python code
- When the user explicitly requests a different docstring format (Google, NumPy, Sphinx)
- For standalone README files (use `writing-docs-majo`)

## Process

1. **Identify what needs documentation**: Check if functions, classes, or methods lack docstrings
2. **Determine section requirements**: Check the Format Overview table to see which sections are needed
3. **Write the preamble**: One-line description that starts with a lowercase letter
4. **Add optional body**: Longer explanation if the functionality is complex
5. **Document signatures**: Add `attributes`, `arguments`, or `parameters` for incoming data
6. **Document exports**: Add `functions` or `methods` for outgoing APIs
7. **Add returns and raises**: Document return types and exceptions
8. **Include usage examples**: Add code examples for complex functionality
9. **Review against constraints**: Ensure Python syntax is modern and all code uses backticks

## Constraints

- **Always use latest Python syntax**: Use `T | None` instead of `Optional[T]`, even for older Python versions
- **Always wrap code in backticks**: All Python code in docstrings must be surrounded by backticks
- **Preamble starts lowercase**: The first line should begin with a lowercase letter
- **Follow section order**: Preamble → Body → Signatures → Functions/Methods → Returns → Raises → Usage

## Testing Skills

- Verify docstrings follow the Format Overview section order
- Check that all Python syntax uses modern patterns (`|` union syntax)
- Ensure backticks wrap all code elements in the docstring
- Confirm one-line preamble starts with a lowercase letter
- Test that usage examples are valid Python code

A plaintext-first alternative documentation string style for Python.

## Why MDF?

- Easy and intuitive to read and write — it's just plaintext
- Closely follows Python syntax, including type annotations
- Works well across editors (best on Zed, good on VS Code)

## Format Overview

MDF docstrings are composed of sections in a specific order:

| Section | Required | Position | Purpose |
|---------|----------|----------|---------|
| preamble | Yes | Start | One-line description |
| body | No | Start or End | Longer explanation |
| attributes/arguments/parameters | If applicable | Middle | Incoming signatures |
| functions/methods | If applicable | Middle | Outgoing signatures |
| returns | If not None | Middle | Return type with description |
| raises | If applicable | Middle | Exceptions |
| usage | No | Start or End | Code example |

## Section Details

### 1. Preamble (Required)

A mandatory short one-line description:

```python
"""a baker's confectionery, usually baked, a lie"""
```

### 2. Body (Optional)

A longer, potentially multi-line description:

```python
"""a baker's confectionery, usually baked, a lie

this is a longer description that explains more about cakes
and why they might be lies in certain contexts.
"""
```

### 3. Accepted (Incoming) Signatures

For classes: `attributes`  
For functions: `arguments` or `parameters`

General format:
```text
{attributes,arguments,parameters}:
    `<python variable declaration syntax>`
        <description>
```

Example:
```python
"""
attributes:
    `name: str`
        name of the cake
    `ingredients: list[Ingredient]`
        ingredients of the cake
    `baking_temperature: int = 4000`
        temperature in degrees kelvin
"""
```

### 4. Exported (Outgoing) Signatures

For modules: `functions`  
For classes: `methods`

General format:
```text
{functions,methods}:
    `<python function declaration syntax without trailing colon>`
        <description of the function>
```

Example:
```python
"""
methods:
    `def bake(self, override: BakingOverride | None = None) -> bool`
        bakes the cake and returns True if successful
"""
```

### 5. Returns and Raises

**Single type format:**
```text
{returns,raises}: `<return type annotation>`
    <description>
```

**Multiple types format:**
```text
{returns,raises}:
    `<first possible return type annotation/exception class>`
        <description>
    `<second possible return type annotation/exception class>`
        <description>
```

Example:
```python
def certain_unsafe_div(a: int | float, b: int | float) -> float:
    """divide a by b

    arguments:
        `a: int | float`
            numerator
        `b: int | float`
            denominator

    raises:
        `ZeroDivisionError`
            raised when denominator is 0
        `OverflowError`
            raised when the resulting number is too big

    returns: `float`
        the result, a divided by b
    """
    return a / b
```

### 6. Usage (Optional)

A markdown triple backtick block with usage examples:

```python
"""
usage:
    ```python
    cake = Cake(name="Chocolate", ingredients=[...])
    result = cake.bake()
    ```
"""
```

## Guidelines

### Use Latest Syntax

Use modern Python syntax in docstrings, even if the codebase targets older versions:

```python
# Always use
optional_argument: T | None = None

# Not
optional_argument: Optional[T] = None
```

### External References

Reference third-party classes in full for attributes, but use short names in method signatures:

```python
class ThirdPartyExample(Exception):
    """blah blah

    attributes:
        `field_day: external.ExternalClass`
            blah blah

    methods:
        `def __init__(self, field_day: ExternalClass) -> None: ...`
            blah blah
    """
```

### Overloads

For overloaded functions, use variable declaration syntax that makes sense:

```python
@overload
def get_field(self) -> object: ...

@overload
def get_field(self, default: DefaultT) -> Union[object, DefaultT]: ...

def get_field(self, default: object = None) -> object:
    """...

    arguments:
        `default: object | None = None`
            ...

    returns: `object`
    """
```

### Long Declarations

Split long declarations across multiple lines within the same indentation:

```text
methods:
    `def woah_many_argument_function(
        ...
    ) -> None`
        blah blah blah blah blah blah
```

## When NOT to Document

### 1. Namespace Classes

Simple exception hierarchies or marker classes:

```python
class TomlanticException(Exception):
    """base exception class for all tomlantic errors"""
    pass
```

### 2. Obvious Returns

When the return is self-explanatory from the preamble:

```python
def difference_between_document(self, incoming_document: TOMLDocument) -> Difference:
    """returns a `tomlantic.Difference` namedtuple object of the incoming and
    outgoing fields that were changed between the model and the comparison document

    arguments:
        `incoming_document: tomlkit.TOMLDocument`

    returns: `tomlantic.Difference`
    """
```

## Complete Examples

### Class with Attributes and Methods

```python
class Result(NamedTuple, Generic[ResultType]):
    """typing.NamedTuple representing a result for safe value retrieval

    attributes:
        `value: ResultType`
            value to return or fallback value if erroneous
        `error: BaseException | None = None`
            exception if any

    methods:
        `def __bool__(self) -> bool: ...`
            boolean comparison for truthiness-based exception safety
        `def get(self) -> ResultType: ...`
            method that raises or returns an error if the Result is erroneous
        `def cry(self, string: bool = False) -> str: ...`
            method that returns the result value or raises an error
    """

    value: ResultType
    error: BaseException | None = None

    def __bool__(self) -> bool:
        """boolean comparison for truthiness-based exception safety
        
        returns: `bool`
            that returns True if `self.error` is not None
        """
        ...

    def cry(self, string: bool = False) -> str:
        """raises or returns an error if the Result is erroneous

        arguments:
            `string: bool = False`
                if `self.error` is an Exception, returns it as a string error message
        
        returns: `str`
            returns `self.error` if it is a string, or returns an empty string if
            `self.error` is None
        """
        ...

    def get(self) -> ResultType:
        """returns the result value or raises an error

        returns: `ResultType`
            returns `self.value` if `self.error` is None

        raises: `BaseException`
            if `self.error` is not None
        """
        ...
```

### Complex Class with Usage

```python
class ModelBoundTOML(Generic[M]):
    """glue class for pydantic models and tomlkit documents

    attributes:
        `model: BaseModel`

    methods:
        `def __init__(self, model: type[M], document: TOMLDocument, handle_errors: bool = True) -> None: ...`
            instantiates the class with a `pydantic.BaseModel` and a `tomlkit.TOMLDocument`
        `def model_dump_toml(self) -> TOMLDocument: ...`
            dumps the model as a style-preserved `tomlkit.TOMLDocument`
        `def get_field(self, location: str | Sequence[str], default: object | None = None) -> object | None: ...`
            safely retrieve a field by it's location
        `def set_field(self, location: str | Sequence[str], value: object) -> None: ...`
            sets a field by it's location
        `def from_another_model_bound_toml(cls, model_bound_toml: ModelBoundToml[M]) -> "ModelBoundToml": ...`
             classmethod that fully initialises from the data from another ModelBoundToml

    usage:
        ```py
        # instantiate the class
        toml = ModelBoundTOML(YourModel, tomlkit.parse(...))
        # access your model with .model
        toml.model.message = "blowy red vixens fight for a quick jump"
        # dump the model back to a toml document
        toml_document = toml.model_dump_toml()
        # or to a toml string
        toml_string = toml.model_dump_toml().as_string()
        ```
    """

    def set_field(
        self,
        location: Union[str, tuple[str, ...]],
        value: object,
        handle_errors: bool = True,
    ) -> None:
        """sets a field by it's location.
        
        not recommended for general use due to a lack of type safety, but useful when
        setting fields programatically

        will handle `pydantic.ValidationError` into more toml-friendly error messages.
        set `handle_errors` to `False` to raise the original `pydantic.ValidationError`

        arguments:
            `location: Union[str, tuple[str, ...]]`
                dot-separated location of the field to set
            `value: object`
                value to set at the specified location
            `handle_errors: bool = True`
                whether to convert pydantic ValidationErrors to tomlantic errors

        raises:
            `AttributeError`
                if the field does not exist
            `tomlantic.TOMLValidationError`
                if the document does not validate with the model
            `pydantic.ValidationError`
                if the document does not validate with the model and `handle_errors` is `False`
        """
        ...
```

## Quick Reference

| Section | Syntax |
|---------|--------|
| preamble | Plain text (first line) |
| body | Plain text |
| attributes/arguments/parameters | `` `name: Type` `` + description |
| functions/methods | `` `def name(...) -> Return` `` + description |
| returns | `` `ReturnType` `` + description |
| raises | `` `ExceptionClass` `` + description |
| usage | Code block with example |

**Key rule**: Always use backticks around Python code in docstrings.

## Integration

This skill is standalone but commonly used with:
- `python-majo` — Python development standards
- `mdf-md-api-docs-majo` — MDF-style API reference documentation in markdown
- `writing-docs-majo` — Documentation writing standards
