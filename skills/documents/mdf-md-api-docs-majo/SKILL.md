---
name: mdf-md-api-docs-majo
description: |
  MDF-style API reference documentation for markdown files.
  Use when writing API references or documentation from code using the meadow Docstring Format (MDF).
  Covers function and class documentation templates with proper formatting for arguments, returns, raises, methods, and usage examples.
license: Unlicense OR 0BSD
metadata:
  author: Mark Joshwel <mark@joshwel.co>
  version: "2026.2.2"
---

# MDF API Reference Documentation

API reference format following meadow Docstring Format (MDF) structure for markdown documentation.

## Goal

Provide clear, consistent API documentation in markdown files that mirrors Python docstring conventions while remaining readable as plaintext.

## When to Use This Skill

- Writing API reference sections in README files
- Documenting Python libraries/modules for users
- Creating function/class documentation in markdown
- Following up `writing-docs-majo` when API docs are needed

## Do NOT Use

- Python code docstrings (use `mdf-majo` instead)
- Internal code comments
- Non-API documentation (use `writing-docs-majo`)

## Process

1. **Identify what to document** — functions, classes, or modules
2. **Write the header** — `### def|class module.Name()`
3. **Add preamble** — one-line description
4. **Add signature** — Python code block
5. **Document inputs** — arguments or attributes
6. **Document outputs** — methods or returns
7. **Document errors** — raises section
8. **Add usage example** — if helpful

## Constraints

- **Always use backticks** around Python types and code
- **Two-space linebreak** before descriptions in lists
- **Latest Python syntax** — `T | None` not `Optional[T]`
- **Link when helpful** — to other sections or external docs

## Testing Skills

- [ ] Headers use correct format: `### def|class module.Name()`
- [ ] All Python code wrapped in backticks
- [ ] Two-space linebreaks before descriptions
- [ ] Consistent indentation (4 spaces for nested content)
- [ ] Links use proper markdown format with backticks

## Header Format

```markdown
### <def|class> module.Name()
```

Examples:
- `### def tomlantic.ModelBoundTOML.set_field()`
- `### class tomlantic.ModelBoundTOML`
- `### def surplus.process()`

## Section Structure

Order (all optional except preamble):

1. **preamble** — brief one-line description
2. **body** — longer explanation if needed
3. **signature** — Python code block
4. **attributes** (classes) or **arguments** (functions)
5. **methods** (classes)
6. **returns** — return type
7. **raises** — exceptions
8. **usage** — code example

## Section Formats

### Arguments / Attributes / Methods

Use list format with two-space linebreak:

```markdown
- arguments:
  - `name: str`  
    description of the argument
  - `count: int = 0`  
    optional count with default

- methods:
  - [`def process()`](#def-moduleprocess)  
    processes the data
  - `def validate()`  
    validates inputs
```

### Returns (Single)

```markdown
- returns: `ProcessedResult`  
  structured result containing processed fields
```

### Returns (Multiple Types)

```markdown
- returns:
  - `SuccessResult`  
    when processing succeeds
  - `ErrorResult`  
    when processing fails with error details
```

### Raises (Single)

```markdown
- raises: `ValueError`  
  raised when input is invalid
```

### Raises (Multiple)

```markdown
- raises:
  - `ValueError`  
    raised when input is invalid
  - `TimeoutError`  
    raised when operation exceeds time limit
  - [`CustomError`](#class-modulecustomerror)  
    raised for domain-specific failures
```

## Complete Examples

### Function Example

```markdown
### def tomlantic.ModelBoundTOML.set_field()

sets a field by its location. not recommended for general use due to a lack of
type safety, but useful when setting fields programatically

will handle `pydantic.ValidationError` into more toml-friendly error messages.
set `handle_errors` to `False` to raise the original `pydantic.ValidationError`

- signature:

  ```python
  def set_field(
      self,
      location: str | tuple[str, ...],
      value: object,
      handle_errors: bool = True,
  ) -> None: ...
  ```

- arguments:
  - `location: str | tuple[str, ...]`  
    dot-separated location of the field to set
  - `value: object`  
    value to set at the specified location
  - `handle_errors: bool = True`  
    whether to convert pydantic ValidationErrors to tomlantic errors

- raises:
  - `AttributeError`  
    if the field does not exist
  - [`tomlantic.TOMLValidationError`](#class-tomlantictomlvalidationerror)  
    if validation fails
  - [`pydantic.ValidationError`](https://docs.pydantic.dev/)  
    if validation fails and `handle_errors` is `False`
```

### Class Example

```markdown
### class tomlantic.ModelBoundTOML

glue class for pydantic models and tomlkit documents

- signature:

  ```python
  class ModelBoundTOML(Generic[M]): ...
  ```

- attributes:
  - `model: pydantic.BaseModel`  
    the bound pydantic model instance

- methods:
  - [`def model_dump_toml()`](#def-tomlanticmodelboundtomlmodel_dump_toml)  
    dumps the model as a style-preserved tomlkit.TOMLDocument
  - [`def get_field()`](#def-tomlanticmodelboundtomlget_field)  
    safely retrieve a field by its location
  - [`def set_field()`](#def-tomlanticmodelboundtomlset_field)  
    sets a field by its location

- usage:

  ```python
  toml = ModelBoundTOML(YourModel, tomlkit.parse(...))
  toml.model.message = "hello"
  document = toml.model_dump_toml()
  ```
```

### Simple Function Example

```markdown
### def surplus.process_file()

process a single file through the surplus pipeline

- signature:

  ```python
  def process_file(
      path: Path,
      options: ProcessingOptions | None = None,
  ) -> ProcessingResult: ...
  ```

- arguments:
  - `path: Path`  
    path to the file to process
  - `options: ProcessingOptions | None = None`  
    optional processing configuration

- returns: `ProcessingResult`  
  result containing processed output and metadata

- raises: `FileNotFoundError`  
  if the file does not exist

- usage:

  ```python
  result = process_file(Path("data.txt"))
  if result.success:
      print(result.output)
  ```
```

## Formatting Quick Reference

| Element | Format |
|---------|--------|
| Type | `` `Type` `` or `` `module.Type` `` |
| Variable | `` `name: Type` `` |
| Function signature | `` `def name(...) -> Return: ...` `` |
| Link internal | `` [`Type`](#section) `` |
| Link external | `` [`Type`](https://...) `` |
| Description separator | Two spaces + newline |
| Nested indentation | 4 spaces |

## Integration

This skill works alongside:
- `writing-docs-majo` — General documentation standards
- `mdf-majo` — Python docstring format (the inspiration for this markdown format)
- `python-majo` — Python code standards
