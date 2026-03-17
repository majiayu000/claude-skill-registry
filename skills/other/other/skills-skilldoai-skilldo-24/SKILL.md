---

name: beautifulsoup4
description: Parse, search, and modify HTML/XML documents by building a navigable tree of tags and text.
version: 4.14.3
ecosystem: python
license: MIT License
generated_with: gpt-5.2
---

## Imports

```python
import bs4
from bs4 import BeautifulSoup, Tag, Comment
from bs4.exceptions import FeatureNotFound, ParserRejectedMarkup
from bs4.dammit import UnicodeDammit
```

## Core Patterns

### Parse markup with an explicit parser ✅ Current
```python
from __future__ import annotations

from bs4 import BeautifulSoup

html_doc = "<html><body><p class='body strikeout'>Hello</p></body></html>"

# Always choose the parser explicitly for consistent behavior across environments.
soup = BeautifulSoup(html_doc, "html.parser")

p = soup.find("p")
assert p is not None
print(p.name)          # "p"
print(p.get_text())    # "Hello"
```
* Prefer `BeautifulSoup(markup, "html.parser")`, `"lxml"`, `"html5lib"`, or `"xml"/"lxml-xml"` depending on your needs; different parsers can produce different trees for invalid documents.

### Parse from a file handle (context manager) ✅ Current
```python
from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup

path = Path("example.html")
path.write_text("<html><body><a href='/x'>Link</a></body></html>", encoding="utf-8")

with path.open("r", encoding="utf-8") as fp:
    soup = BeautifulSoup(fp, "html.parser")

a = soup.find("a")
assert a is not None
print(a.get("href"))  # "/x"
```
* Pass an open file handle directly to `BeautifulSoup` to let the builder stream/handle encodings appropriately.

### Find elements and navigate relatives ✅ Current
```python
from __future__ import annotations

from typing import Optional
from bs4 import BeautifulSoup, Tag

html_doc = """
<div id="root">
  <h1>Title</h1>
  <p>First</p>
  <p>Second <span>inner</span></p>
</div>
"""

soup = BeautifulSoup(html_doc, "html.parser")

root: Optional[Tag] = soup.find(id="root")
assert root is not None

h1: Optional[Tag] = root.find("h1")
assert h1 is not None

# Navigate
second_p: Optional[Tag] = h1.find_next("p")
assert second_p is not None
print(second_p.get_text(strip=True))  # "First"

all_ps = root.find_all("p")
print([p.get_text(" ", strip=True) for p in all_ps])  # ["First", "Second inner"]
```
* Use `find`, `find_all`, and the `find_next*` / `find_previous*` / sibling / parent variants for tree navigation.

### Work with tag attributes (including multi-valued `class`) ✅ Current
```python
from __future__ import annotations

from bs4 import BeautifulSoup, Tag

soup = BeautifulSoup("<p id='x' class='body strikeout'></p>", "html.parser")
p = soup.find("p")
assert isinstance(p, Tag)

# Dict-like access
print(p["id"])         # "x"
print(p.get("id"))     # "x"

# Multi-valued HTML attributes like class are lists by default.
print(p["class"])      # ["body", "strikeout"]

# If you always want a list (even for non-multivalued attrs), use get_attribute_list.
print(p.get_attribute_list("id"))     # ["x"]
print(p.get_attribute_list("class"))  # ["body", "strikeout"]

# Mutation
p["data-role"] = "demo"
del p["id"]
print(p.attrs)  # {'class': ['body', 'strikeout'], 'data-role': 'demo'}
```
* In HTML mode, `class`, `rel`, etc. are typically stored as `list[str]`. Use `Tag.get_attribute_list(name)` to normalize to a list.

### Handle text nodes and comments safely ✅ Current
```python
from __future__ import annotations

from bs4 import BeautifulSoup, Comment
from bs4.element import NavigableString

soup = BeautifulSoup("<p>Hello<!--secret--></p>", "html.parser")
p = soup.find("p")
assert p is not None

# Comments are special text nodes.
comment = p.find(string=lambda s: isinstance(s, Comment))
assert isinstance(comment, Comment)
print(comment)  # "secret"

# NavigableString is immutable; replace the node instead of editing in place.
text = p.find(string=lambda s: isinstance(s, NavigableString) and not isinstance(s, Comment))
assert isinstance(text, NavigableString)
text.replace_with("Hi")

print(p.get_text())  # "Hi"
```
* Treat `NavigableString` as immutable; use `replace_with(...)` to change text.

## Configuration

- **Parser selection (`features`)**:
  - `"html.parser"`: built-in, decent baseline.
  - `"lxml"`: fast (requires `lxml`).
  - `"html5lib"`: most lenient (slow; requires `html5lib`).
  - `"xml"` / `"lxml-xml"`: XML parsing mode (attribute handling differs from HTML).
- **`parse_only`**: pass a `SoupStrainer` (not covered here) to parse only parts of a document for speed/memory.
- **`from_encoding` / `exclude_encodings`**: hint or restrict encoding detection when input is bytes.
- **Large text nodes with lxml**: when using an lxml builder and documents may contain a single text node > 10,000,000 bytes, pass `huge_tree=True` to `BeautifulSoup(...)` to avoid lxml security limits truncating the parse.
- **Multi-valued attributes**:
  - Default (HTML): `class`/`rel` etc. become lists.
  - To disable list conversion: `BeautifulSoup(markup, "html.parser", multi_valued_attributes=None)`
  - In XML mode, multi-valued attributes are not enabled by default; you can opt in via `multi_valued_attributes={'*': 'class'}`.

## Pitfalls

### Wrong: Not specifying a parser (inconsistent trees)
```python
from bs4 import BeautifulSoup

html_doc = "<p><b>badly nested</p></b>"
soup = BeautifulSoup(html_doc)  # parser not specified
print(soup.find("b"))
```

### Right: Choose a parser explicitly
```python
from bs4 import BeautifulSoup

html_doc = "<p><b>badly nested</p></b>"
soup = BeautifulSoup(html_doc, "html.parser")
print(soup.find("b"))
```

### Wrong: Treating `class` as a string in HTML mode
```python
from bs4 import BeautifulSoup

soup = BeautifulSoup("<p class='body strikeout'></p>", "html.parser")
# In HTML mode, soup.p["class"] is a list, so this fails.
classes = soup.p["class"].split()  # type: ignore[attr-defined]
print(classes)
```

### Right: Use the list directly (or normalize with `get_attribute_list`)
```python
from bs4 import BeautifulSoup

soup = BeautifulSoup("<p class='body strikeout'></p>", "html.parser")
classes = soup.p["class"]
print(classes)  # ["body", "strikeout"]

ids = soup.p.get_attribute_list("id")
print(ids)  # []
```

### Wrong: Assuming multi-valued attributes exist in XML mode
```python
from bs4 import BeautifulSoup

soup = BeautifulSoup("<p class='body strikeout'></p>", "xml")
# In XML mode, "class" is a string by default; indexing returns a character.
first = soup.p["class"][0]
print(first)  # "b" (not "body")
```

### Right: Opt in to multi-valued attributes when parsing XML
```python
from bs4 import BeautifulSoup

class_is_multi = {"*": "class"}
soup = BeautifulSoup("<p class='body strikeout'></p>", "xml", multi_valued_attributes=class_is_multi)
first = soup.p["class"][0]
print(first)  # "body"
```

### Wrong: Editing a `NavigableString` “in place”
```python
from bs4 import BeautifulSoup
from bs4.element import NavigableString

soup = BeautifulSoup("<p>Hello</p>", "html.parser")
text = soup.p.string
assert isinstance(text, NavigableString)

# Strings are immutable; this does not update the parse tree.
text = NavigableString("Hi")
print(soup.p.get_text())  # still "Hello"
```

### Right: Replace the existing node with `replace_with`
```python
from bs4 import BeautifulSoup
from bs4.element import NavigableString

soup = BeautifulSoup("<p>Hello</p>", "html.parser")
text = soup.p.string
assert isinstance(text, NavigableString)

text.replace_with("Hi")
print(soup.p.get_text())  # "Hi"
```

### Wrong: lxml builder truncation with huge text nodes (missing `huge_tree=True`)
```python
from bs4 import BeautifulSoup

# If this markup contains a single >10,000,000 byte text node, lxml may stop early.
markup_with_huge_text = "<root>" + ("x" * 11_000_000) + "</root>"
soup = BeautifulSoup(markup_with_huge_text, "lxml")
print(soup.find("root") is not None)
```

### Right: Enable huge tree support when needed
```python
from bs4 import BeautifulSoup

markup_with_huge_text = "<root>" + ("x" * 11_000_000) + "</root>"
soup = BeautifulSoup(markup_with_huge_text, "lxml", huge_tree=True)
print(soup.find("root") is not None)
```

## References

- [Download](https://www.crummy.com/software/BeautifulSoup/bs4/download/)
- [Homepage](https://www.crummy.com/software/BeautifulSoup/bs4/)

## Migration from v4.13.x

- **Typing changes (4.14.0+)**: `find_*` methods gained overloads to improve type safety.
  - Prefer annotating results as `Optional[Tag]`, `Optional[NavigableString]`, `Sequence[Tag]`, etc.
  - Known edge case: `find_all("a", string="...")` may still confuse type checkers; refactor or use `typing.cast`.

```python
from __future__ import annotations

from typing import Optional, Sequence, cast
from bs4 import BeautifulSoup, Tag

soup = BeautifulSoup("<a>b</a>", "html.parser")

# Preferred: reflect optionality
a: Optional[Tag] = soup.find("a")

# Edge case: mixed filters may require a cast for static type checkers
tags = cast(Sequence[Tag], soup.find_all("a", string="b"))
print([t.get_text() for t in tags])
```

- **`ResultSet` typing churn across 4.14.x**: inheritance changed in 4.14.0/4.14.1/4.14.2; avoid depending on specific ABC inheritance.
  - If you need a stable container type at boundaries: `results = list(soup.find_all(...))`.

- **lxml huge text nodes (4.14.3 note)**: if using an lxml builder and expecting extremely large text nodes, pass `huge_tree=True`.

## API Reference

- **BeautifulSoup(markup, features=..., parse_only=..., from_encoding=..., exclude_encodings=..., element_classes=..., \*\*kwargs)** - parse markup into a tree; specify `features` (parser) explicitly.
- **BeautifulSoup.find(...)** - return the first matching element (often `Tag | None`); supports tag name, attrs, and other filters.
- **BeautifulSoup.find_all(...)** - return all matching elements (list-like result set); convert to `list(...)` if you need a stable container type.
- **BeautifulSoup.find_next(...) / find_all_next(...)** - search forward in document order from a starting node.
- **BeautifulSoup.find_previous(...) / find_all_previous(...)** - search backward in document order from a starting node.
- **BeautifulSoup.find_next_sibling(...) / find_next_siblings(...)** - search among following siblings.
- **BeautifulSoup.find_previous_sibling(...) / find_previous_siblings(...)** - search among preceding siblings.
- **BeautifulSoup.find_parent(...) / find_parents(...)** - search upward to parents/ancestors.
- **BeautifulSoup.get_text(separator="...", strip=False)** - extract combined text content from a subtree.
- **BeautifulSoup.prettify()** - render formatted markup for debugging/inspection.
- **BeautifulSoup.contains_replacement_characters** - flag indicating replacement characters were introduced during entity/encoding handling (builder-dependent).
- **Tag.name** - the tag’s name (e.g., `"a"`, `"p"`).
- **Tag.attrs** - dict of attributes; multi-valued HTML attributes may be lists.
- **Tag.get(key, default=None)** - safe attribute lookup.
- **Tag.get_attribute_list(name)** - normalize an attribute to a list regardless of internal storage.
- **UnicodeDammit(...)** - helper for detecting/decoding unknown encodings before parsing.
- **Comment** - class for HTML/XML comment nodes (a specialized string-like node).
- **ParserRejectedMarkup** - exception raised when the underlying parser rejects markup.
- **FeatureNotFound** - exception raised when the requested parser feature/builder is unavailable.