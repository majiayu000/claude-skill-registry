---
name: cleanup
description: This skill should be used when the user asks to "clean up the code", "remove unnecessary comments", "simplify docstrings", "parameterize tests", or wants to review and clean up code.
user-invocable: true
---

# Cleanup Code

Review and clean up code, removing unwanted patterns and improving test structure.

## What This Skill Does

1. Removes unnecessary comments
2. Simplifies or removes verbose docstrings
3. Consolidates tests using parameterization
4. Removes other unwanted patterns

## Cleanup Tasks

### 1. Remove Unnecessary Comments

Remove explanatory comments that state the obvious or describe what code does line-by-line. Remove comments that:

- Restate what the code already clearly expresses
- Explain standard library functions or well-known patterns
- Were added "for clarity" but add no value
- Describe obvious variable assignments or function calls

**Keep comments that:**
- Explain *why* something is done (business logic, workarounds, edge cases)
- Document non-obvious behavior or gotchas
- Provide context that can't be inferred from the code

**Example - Before:**
```python
# Get the user from the database
user = db.get_user(user_id)

# Check if user exists
if user is None:
    # Raise an error if user not found
    raise UserNotFoundError(user_id)

# Return the user's email address
return user.email
```

**Example - After:**
```python
user = db.get_user(user_id)
if user is None:
    raise UserNotFoundError(user_id)
return user.email
```

### 2. Simplify Docstrings

Remove verbose docstrings that repeat parameter names and types already visible in type annotations, or describe obvious behavior. Clean up docstrings by:

- Removing docstrings from simple, self-explanatory functions
- Removing Args/Returns sections when types are annotated and obvious
- Keeping only non-obvious information
- Removing filler phrases like "This function..." or "This method..."

**Example - Before:**
```python
def get_user_email(user_id: int) -> str:
    """
    Get the email address for a user.

    This function retrieves the email address associated with the given user ID
    from the database.

    Args:
        user_id: The unique identifier of the user whose email should be retrieved.

    Returns:
        The email address of the user as a string.

    Raises:
        UserNotFoundError: If no user exists with the given ID.
    """
    user = db.get_user(user_id)
    if user is None:
        raise UserNotFoundError(user_id)
    return user.email
```

**Example - After:**
```python
def get_user_email(user_id: int) -> str:
    """Raises UserNotFoundError if user doesn't exist."""
    user = db.get_user(user_id)
    if user is None:
        raise UserNotFoundError(user_id)
    return user.email
```

Or if the function name and signature are completely self-explanatory:
```python
def get_user_email(user_id: int) -> str:
    user = db.get_user(user_id)
    if user is None:
        raise UserNotFoundError(user_id)
    return user.email
```

### 3. Parameterize Tests

Consolidate separate test functions that should be parameterized. Look for:

- Multiple test functions with nearly identical structure
- Tests that differ only in input values and expected outputs
- Copy-paste test patterns with minor variations

Consolidate using `@pytest.mark.parametrize`:

**Example - Before:**
```python
def test_validate_email_valid():
    assert validate_email("user@example.com") is True

def test_validate_email_valid_with_subdomain():
    assert validate_email("user@mail.example.com") is True

def test_validate_email_invalid_no_at():
    assert validate_email("userexample.com") is False

def test_validate_email_invalid_no_domain():
    assert validate_email("user@") is False

def test_validate_email_invalid_empty():
    assert validate_email("") is False
```

**Example - After:**
```python
@pytest.mark.parametrize(
    ("email", "expected"),
    [
        ("user@example.com", True),
        ("user@mail.example.com", True),
        ("userexample.com", False),
        ("user@", False),
        ("", False),
    ],
)
def test_validate_email(email: str, expected: bool):
    assert validate_email(email) is expected
```

**When NOT to parameterize:**
- Tests with significantly different setup/teardown
- Tests that check different aspects of behavior (not just input/output variations)
- Tests where parameterization would obscure the intent

### 4. Other Patterns to Remove

- Unnecessary type: ignore comments (fix the actual type issue instead)
- Defensive `.get()` calls with defaults that hide bugs
- Overly verbose error messages that duplicate context
- Redundant validation that duplicates framework behavior
- Empty except blocks or overly broad exception handling
- Unused imports added "just in case"

## Workflow

1. **Identify files to clean**: Look at recently modified files or files the user specifies
2. **Review systematically**: Go through each cleanup category above
3. **Make changes**: Edit files to remove unwanted patterns
4. **Run tests**: Ensure changes don't break anything
5. **Summarize**: Tell the user what was cleaned up

## Notes

- When in doubt, less is more—remove rather than keep
- If a comment or docstring makes you think "obviously", remove it
- Parameterization should make tests more readable, not less—if a test matrix is confusing, keep separate tests
- Always run tests after cleanup to catch any accidental removals
