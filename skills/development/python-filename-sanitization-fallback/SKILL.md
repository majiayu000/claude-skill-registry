---
name: Python Filename Sanitization with Fallback
description: Defensive programming pattern for generating valid filenames from user input with intelligent fallback when titles contain only special characters, ensuring compatibility with filesystem and indexer validation requirements
---

# Python Filename Sanitization with Fallback

## Purpose
This skill provides expertise in implementing robust filename sanitization that goes beyond removing invalid characters to ensure the resulting filename meets downstream validation requirements. It addresses the critical gap where user-provided titles containing only special characters (emoji, ellipsis, whitespace) produce invalid filenames after standard sanitization.

## Core Problem

**Conventional Approach Limitation**:
Standard filename sanitization only removes invalid filesystem characters:
```python
# Incomplete sanitization - can produce invalid names
filename = title.replace('/', '-').replace(':', ' -')
filename = re.sub(r'[<>"\\\|?*]', '', filename)
```

**Real-World Failure Cases** (from Readwise MCP Server, 2026-01-24):
- Title: `"…"` → Filename: `"….md"` → qmd indexer error
- Title: `"🍿🍿"` → Filename: `"🍿🍿.md"` → qmd indexer error
- Title: `""` → Filename: `".md"` → qmd indexer error

**Root Issue**: Many indexers and tools require filenames to contain at least one alphanumeric character (`/[\p{L}\p{N}]/u`). Titles with only special characters fail this validation.

## The Validation-Aware Pattern

### Core Principle
**Validate output, not just transform input**. After sanitization, verify the filename meets downstream requirements; fallback to metadata-based naming when validation fails.

### Implementation Pattern

```python
def sanitize_filename(title: str, doc: Optional[Dict] = None) -> str:
    """
    Sanitize title for filename with fallback for invalid names.

    Args:
        title: The document title to sanitize
        doc: Optional document dict for fallback metadata (author, saved_at, category)

    Returns:
        Sanitized filename ending in .md, guaranteed to have alphanumeric content
    """
    # Step 1: Standard character sanitization
    filename = title.replace('/', '-').replace(':', ' -')
    filename = re.sub(r'[<>"\\\|?*]', '', filename)
    filename = filename[:100].strip()

    # Step 2: Validate output meets requirements
    if not any(c.isalnum() for c in filename):
        # Step 3: Intelligent fallback using available metadata
        if doc:
            author = doc.get('author', 'Unknown')
            # Sanitize author name (may also have special chars)
            author = re.sub(r'[<>"\\\|?*/:]', '', author)[:30].strip()

            saved_at = doc.get('saved_at', '')
            date_str = saved_at[:10] if saved_at else datetime.now().strftime('%Y-%m-%d')

            # Use category for context
            category = doc.get('category', 'Document')
            category_label = 'Tweet' if category == 'tweet' else category.capitalize()

            filename = f"{category_label} by {author} - {date_str}"
        else:
            # Generic timestamp-based fallback
            filename = f"Untitled - {datetime.now().strftime('%Y-%m-%d-%H%M%S')}"

    return filename + ".md"
```

### Key Components

**1. Validation Check**:
```python
if not any(c.isalnum() for c in filename):
```
Catches: empty strings, emoji-only, special chars only, whitespace only

**2. Metadata-Based Fallback**:
```python
filename = f"{category_label} by {author} - {date_str}"
```
**Benefits**:
- **Descriptive**: Shows document type and origin
- **Unique**: Date ensures no collisions
- **Searchable**: Author name aids discovery
- **Valid**: Guaranteed alphanumeric content

**3. Defensive Author Sanitization**:
```python
author = re.sub(r'[<>"\\\|?*/:]', '', author)[:30].strip()
```
Authors may also contain special characters; sanitize and truncate them too.

## Real-World Application

### Context: Readwise MCP Server (December 2025 Backfill)

**Scenario**: Importing 985 tweets from Readwise API
**Challenge**: Some tweets have titles with only emoji or special characters
**Impact**: 3 files created with invalid names broke qmd indexer

**Results**:

| Input Title | Standard Sanitization | Enhanced Sanitization |
|-------------|----------------------|----------------------|
| `"…"` | `"….md"` ❌ | `"Tweet by Take Action! - 2025-12-08.md"` ✓ |
| `"🍿🍿"` | `"🍿🍿.md"` ❌ | `"Tweet by Elon Musk - 2025-12-06.md"` ✓ |
| `""` | `".md"` ❌ | `"Tweet by x.com - 2025-12-05.md"` ✓ |
| `"Normal Title"` | `"Normal Title.md"` ✓ | `"Normal Title.md"` ✓ |

**Outcome**:
- All 985 documents imported successfully with enhanced pattern
- Zero indexing errors
- Descriptive fallback names improved organization
- 100% backward compatible (existing valid filenames unchanged)

### Application Points

Update all file creation callsites:

```python
# Before (incomplete)
filename = sanitize_filename(doc["title"])

# After (defensive)
filename = sanitize_filename(doc.get("title", ""), doc)
```

**Critical**: Pass full document dict to enable metadata fallback.

## Testing Strategy

### Essential Test Cases

```python
def test_ellipsis_only_title():
    """Test emoji/special char-only titles use fallback"""
    doc = {"title": "…", "author": "User", "saved_at": "2025-12-08", "category": "tweet"}
    result = sanitize_filename("…", doc)

    assert result == "Tweet by User - 2025-12-08.md"
    assert any(c.isalnum() for c in result[:-3])  # Verify validation

def test_empty_title():
    """Test empty titles use fallback"""
    doc = {"title": "", "author": "User", "saved_at": "2025-12-05", "category": "tweet"}
    result = sanitize_filename("", doc)

    assert any(c.isalnum() for c in result[:-3])

def test_normal_title():
    """Test normal titles are unchanged"""
    result = sanitize_filename("Normal Title", None)
    assert result == "Normal Title.md"

def test_mixed_valid_invalid():
    """Test titles with some alphanumeric use original"""
    result = sanitize_filename("Hello 🍿 World", None)
    assert "Hello" in result and "World" in result
    assert any(c.isalnum() for c in result[:-3])

def test_no_doc_fallback():
    """Test fallback works without metadata"""
    result = sanitize_filename("…", None)
    assert result.startswith("Untitled - ")
    assert any(c.isalnum() for c in result[:-3])
```

### Regression Test

```python
def test_validation_regression():
    """Prevent regression of indexer validation errors"""
    problematic_cases = [
        ("…", {"author": "User1", "saved_at": "2025-12-08", "category": "tweet"}),
        ("🍿🍿", {"author": "User2", "saved_at": "2025-12-06", "category": "tweet"}),
        ("", {"author": "User3", "saved_at": "2025-12-05", "category": "tweet"}),
        ("   ", {"author": "User4", "saved_at": "2025-12-04", "category": "tweet"}),
        ("!@#$%", {"author": "User5", "saved_at": "2025-12-03", "category": "tweet"}),
    ]

    for title, doc in problematic_cases:
        result = sanitize_filename(title, doc)
        filename_without_ext = result[:-3]
        has_alnum = any(c.isalnum() for c in filename_without_ext)
        assert has_alnum, f"Title '{title}' produced invalid filename '{result}'"
```

## Edge Cases

### 1. Author with Special Characters
Author names may also contain invalid characters:
```python
author = re.sub(r'[<>"\\\|?*/:]', '', author)[:30].strip()
```

**Example**:
- Author: `"User/Name:Test"` → `"UserNameTest"`

### 2. Very Long Author Names
Truncate to prevent excessively long filenames:
```python
author[:30].strip()
```

### 3. Category-Specific Labels
Use meaningful labels based on document type:
```python
category_label = 'Tweet' if category == 'tweet' else category.capitalize()
```

**Examples**:
- `category="tweet"` → `"Tweet by Author - 2025-12-08.md"`
- `category="article"` → `"Article by Author - 2025-12-03.md"`
- `category="pdf"` → `"Pdf by Author - 2025-12-10.md"`

### 4. Mixed Valid/Invalid Characters
If title has SOME alphanumeric content, use the original:
```python
# "Hello 🍿 World" has valid chars, don't use fallback
if any(c.isalnum() for c in filename):
    return filename + ".md"  # Keep original
```

## Defensive Programming Principles

### Principle 1: Validate Output, Not Just Input
Don't assume sanitization produces valid names; verify requirements are met.

### Principle 2: Graceful Degradation
When primary approach fails, fallback to alternative strategy using available context.

### Principle 3: Metadata Enrichment
Use document metadata to create meaningful fallback names rather than generic placeholders.

### Principle 4: Idempotency
Same input with same metadata always produces same output; deterministic behavior aids debugging.

### Principle 5: Backward Compatibility
Enhanced validation shouldn't break existing valid filenames; only activate for edge cases.

## When to Apply This Pattern

✓ **Apply when**:
- Generating filenames from user input (titles, names, descriptions)
- Working with API data (tweets, articles, documents)
- Files will be indexed by tools with validation requirements
- Filesystem compatibility across platforms is critical
- Content may contain emoji, special characters, or non-Latin scripts

✗ **Not needed when**:
- Filenames are programmatically generated (UUIDs, hashes)
- User input is already validated/constrained
- Files are temporary and won't be indexed
- System tolerates any filename format

## Integration with Other Skills

### Defensive Programming Patterns
- Input validation alone is insufficient; validate output
- Multiple validation layers (character removal → alphanumeric check → fallback)
- Fail gracefully with context-aware alternatives

### Test-Driven Development
- Write tests for edge cases BEFORE encountering them in production
- Regression tests prevent reintroduction of fixed bugs
- Property-based testing: "All filenames must have alphanumeric chars"

### API Integration Best Practices
- Don't trust external data format assumptions
- Metadata-driven fallbacks for robustness
- Document edge cases discovered in production

### Cross-Domain Pattern Recognition
- Similar validation patterns apply across domains (URLs, identifiers, paths)
- Fallback strategy: primary approach → metadata-based → generic timestamp
- Universal principle: Validate requirements, not just constraints

## Common Mistakes

### Mistake 1: Assuming Sanitization Produces Valid Names
**Wrong**:
```python
filename = remove_invalid_chars(title)  # Might be empty!
save_file(filename)  # Could fail
```

**Right**:
```python
filename = sanitize_filename(title, doc)  # Validates + fallback
save_file(filename)  # Guaranteed valid
```

### Mistake 2: Generic Fallbacks Without Context
**Wrong**:
```python
if not valid(filename):
    filename = "untitled.md"  # All failures get same name!
```

**Right**:
```python
if not valid(filename):
    filename = f"Tweet by {author} - {date}.md"  # Unique + descriptive
```

### Mistake 3: Not Sanitizing Metadata
**Wrong**:
```python
filename = f"Tweet by {author} - {date}.md"  # Author might have invalid chars!
```

**Right**:
```python
author = sanitize_author(author)  # Clean metadata too
filename = f"Tweet by {author} - {date}.md"
```

### Mistake 4: Overly Complex Validation
**Wrong**:
```python
if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9\s\-_\.]*[a-zA-Z0-9]$', filename):  # Too strict!
```

**Right**:
```python
if not any(c.isalnum() for c in filename):  # Simple, effective validation
```

## Strategic Value

### Production Robustness
- Prevents runtime failures from unexpected input
- Reduces manual intervention (no file renaming needed)
- Improves user experience (meaningful names vs. errors)

### Operational Efficiency
- Zero manual fixes required during 985-document import
- Automated recovery from edge cases
- Self-documenting fallback names aid troubleshooting

### Knowledge Transfer
- Pattern applies beyond Python (JavaScript, Ruby, Go, etc.)
- Defensive strategy works across domains (API design, database schemas, URLs)
- Validation + fallback principle is universal

## Source Documentation

**Origin**: Readwise MCP Server Enhancement (2026-01-24)
- **Problem**: qmd indexer validation errors during December 2025 backfill
- **Impact**: 3 invalid filenames out of 985 documents imported
- **Solution**: Enhanced sanitization with validation + metadata fallback
- **Result**: 100% success rate, zero manual intervention
- **Repository**: `/Users/ngpestelos/src/readwise-mcp-server`
- **Commit**: `9c361e8`
- **Tests**: 13 new tests in `TestFilenameQmdValidation` class
- **Documentation**: `0 Projects/Readwise MCP Enhancement - Filename Sanitization.md`

## When to Apply This Skill

Use Python Filename Sanitization with Fallback expertise when:
- Building systems that import user-generated content
- Integrating with APIs that provide unpredictable text data
- Working with indexing tools that validate filename format
- Implementing document management systems
- Creating robust file-based workflows
- Ensuring cross-platform filesystem compatibility
- Preventing production failures from edge-case input
- Designing defensive, self-healing systems

---

**Quality Note**: This pattern demonstrates defensive programming in practice—going beyond "remove bad characters" to "ensure valid output with graceful degradation." The metadata-enriched fallback strategy transforms potential failures into opportunities for improved organization and user experience.
