---
name: fastapi
description: FastAPI documentation optimized for AI coding agents
---

# Fastapi Skill

Fastapi documentation optimized for ai coding agents, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with fastapi
- Asking about fastapi features or APIs
- Implementing fastapi solutions
- Debugging fastapi code
- Learning fastapi best practices

## Quick Reference

### Common Patterns

**Pattern 1:** This includes, for example:

```
BackgroundTasks
```

**Pattern 2:** For example:

```
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

**Pattern 3:** Info To use forms, first install python-multipart

```
python-multipart
```

**Pattern 4:** Make sure you create a virtual environment, activate it, and then install it, for example:

```
$ pip install python-multipart
```

**Pattern 5:** For example:

```
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```

**Pattern 6:** But if you go to, for example:

```
http://127.0.0.1:8000/items/?skip=20
```

**Pattern 7:** Let's take this application as example:

```
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

**Pattern 8:** If you are inside of a normal def path operation function, you can access the UploadFile

```
def
```

### Example Code Patterns

**Example 1** (sql):
```sql
from app.routers import items
```

**Example 2** (php):
```php
$ pip install "fastapi[standard]"

---> 100%
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Api documentation
- **tutorial.md** - Tutorial documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
