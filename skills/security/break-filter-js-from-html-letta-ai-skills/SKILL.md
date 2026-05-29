---
name: filter-js-from-html
description: Guidance for removing JavaScript from HTML while preserving structure and formatting. This skill applies when filtering XSS vectors, sanitizing HTML content, removing script tags and event handlers, or building HTML sanitization tools. It covers comprehensive XSS vector identification, format-preserving transformations, and verification strategies.
---

# Filter JavaScript from HTML

This skill provides guidance for tasks involving the removal of JavaScript from HTML documents while preserving the original structure and formatting. These tasks require careful handling of multiple XSS attack vectors and strict format preservation.

## Task Recognition

This skill applies to tasks that involve:
- Removing JavaScript from HTML files
- Building HTML sanitizers or filters
- Stripping script tags and event handlers
- Sanitizing user-generated HTML content
- XSS prevention through HTML transformation

## Core Challenges

### 1. Multiple JavaScript Injection Vectors

JavaScript can be embedded in HTML through numerous mechanisms:

| Vector Type | Examples |
|-------------|----------|
| Script elements | `<script>`, `<script src="...">` |
| Event handlers | `onclick`, `onerror`, `onload`, `onmouseover`, etc. |
| URL schemes | `javascript:`, `vbscript:`, `data:` |
| Special elements | `<svg>`, `<math>`, `<iframe>`, `<object>`, `<embed>` |
| Attribute contexts | `href`, `src`, `action`, `formaction`, `srcdoc`, `data` |
| CSS-based | `expression()`, `-moz-binding`, `behavior` |
| Meta redirects | `<meta http-equiv="refresh">` |

### 2. Format Preservation Requirements

When a task specifies preserving original formatting:
- Whitespace (spaces, tabs, newlines) must remain unchanged
- HTML entity encoding must be preserved (e.g., `&amp;` stays as `&amp;`)
- Attribute quote styles must be maintained
- Self-closing tag format must be preserved exactly
- Comments and CDATA sections may require preservation

### 3. Parser Bypass Techniques

Attackers use various techniques to bypass naive filters:
- Mixed/unusual casing: `<ScRiPt>`, `jAvAsCrIpT:`
- Whitespace injection: `java script:`, `on\nclick`
- Null bytes and control characters
- HTML entity encoding within attributes
- Malformed HTML that browsers still parse
- Unicode variations and homoglyphs

## Recommended Approach

### Step 1: Understand the Complete Requirements

Before implementation, clarify:
1. What constitutes "JavaScript" in this context (scripts only, or all executable content?)
2. Format preservation requirements (exact byte preservation vs semantic preservation)
3. How to handle edge cases (malformed HTML, unknown attributes)
4. What elements/attributes are allowed vs blocked (allowlist vs blocklist)

### Step 2: Choose an Appropriate Parser

For Python implementations:
- `html.parser.HTMLParser` - Built-in, handles most cases
- `lxml` - Faster, better malformed HTML handling
- `BeautifulSoup` - User-friendly but may alter formatting
- `html5lib` - Most browser-accurate parsing

**Critical Configuration:**
- Disable character reference conversion to preserve entities (e.g., `convert_charrefs=False` for HTMLParser)
- Configure parser to preserve whitespace

### Step 3: Identify All Dangerous Patterns

Reference `references/xss_vectors.md` for comprehensive patterns. Key categories:

**Event Handler Attributes** - Block all `on*` attributes:
```
onclick, ondblclick, onmousedown, onmouseup, onmouseover, onmousemove,
onmouseout, onmouseenter, onmouseleave, onkeydown, onkeyup, onkeypress,
onfocus, onblur, onchange, onsubmit, onreset, onselect, oninput, onload,
onerror, onabort, onbeforeunload, onunload, onresize, onscroll, etc.
```

**Dangerous URL Attributes** - Check for `javascript:`, `vbscript:`, `data:` schemes in:
```
href, src, action, formaction, poster, data, codebase, cite, background,
profile, usemap, longdesc, dynsrc, lowsrc, srcdoc
```

**Dangerous Elements** - Consider blocking entirely:
```
script, iframe, object, embed, applet, base, meta (with http-equiv),
link (with rel=import), svg (contains script), math
```

### Step 4: Implement with Defense in Depth

1. **Normalize before checking** - Lowercase, strip whitespace, decode entities
2. **Use allowlists over blocklists** - Safer to specify what's allowed
3. **Handle attribute values carefully** - Escape quotes, check for encoded payloads
4. **Process nested contexts** - SVG/MathML have their own parsing rules

### Step 5: Verify Format Preservation

To ensure exact format preservation:
1. Compare byte-by-byte, not just visual output
2. Use diff tools to identify any alterations
3. Test with HTML containing:
   - Various whitespace patterns
   - Different quote styles
   - HTML entities that should remain encoded
   - Self-closing tags with/without spaces

## Verification Strategy

### Test Categories

1. **Basic Functionality**
   - Script tag removal
   - Event handler removal
   - JavaScript URL removal
   - Safe content preservation

2. **Format Preservation**
   - Whitespace unchanged
   - Entities preserved
   - Quote styles maintained
   - Self-closing tag format

3. **XSS Bypass Attempts**
   - Case variations
   - Whitespace injection
   - Entity encoding
   - Malformed HTML
   - See `references/xss_vectors.md` for comprehensive list

4. **Error Handling**
   - Empty files
   - Invalid HTML
   - Non-existent files
   - Binary files
   - Permission errors

### Testing Best Practices

- Create a single comprehensive test file covering all cases
- Keep test files for regression testing (do not delete)
- Use diff tools to verify exact output
- Test with real-world malicious payloads
- Verify the complete implementation after all edits

## Common Pitfalls

### 1. Incomplete Vector Coverage
**Problem:** Only removing `<script>` tags while ignoring event handlers and URL schemes.
**Solution:** Reference `references/xss_vectors.md` for all vectors.

### 2. Altering Format While Filtering
**Problem:** Parser converts entities, changes whitespace, or modifies tag format.
**Solution:** Configure parser to preserve format; verify with byte-level comparison.

### 3. Case-Sensitive Matching
**Problem:** Checking for `onclick` but missing `ONCLICK` or `OnClick`.
**Solution:** Normalize to lowercase before comparison.

### 4. Ignoring Dangerous URL Schemes
**Problem:** Only blocking `javascript:` while allowing `data:text/html,...`.
**Solution:** Block all executable URL schemes in relevant attributes.

### 5. Keeping Style Attributes
**Problem:** CSS can contain `expression()`, `-moz-binding`, or exfiltration URLs.
**Solution:** Either sanitize style content or remove style attributes entirely.

### 6. Incomplete Verification
**Problem:** Deleting test files, not reading final code, minimal test coverage.
**Solution:** Keep all tests, verify complete file contents, test adversarially.

### 7. Trusting Parser Output
**Problem:** Assuming the parser handles all malformed HTML correctly.
**Solution:** Test with intentionally malformed HTML; consider browser parsing quirks.

## Implementation Checklist

Before considering the task complete:

- [ ] All script elements removed
- [ ] All event handler attributes removed (entire `on*` family)
- [ ] All `javascript:`, `vbscript:`, `data:` URLs handled
- [ ] Dangerous elements handled (`iframe`, `object`, `embed`, `svg/script`, etc.)
- [ ] Format preservation verified with diff
- [ ] Entity encoding preserved
- [ ] Case-insensitive matching implemented
- [ ] Whitespace in attributes handled
- [ ] Error cases tested
- [ ] Complete code verified (read final file)
- [ ] Test files retained for verification
