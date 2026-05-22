---
name: pypi-readme-creator
description: When creating a README for a Python package. When preparing a package for PyPI publication. When README renders incorrectly on PyPI. When choosing between README.md and README.rst. When running twine check and seeing rendering errors. When configuring readme field in pyproject.toml.
---

# PyPI README Creator

Generate professional, PyPI-compliant README files in Markdown or reStructuredText that render correctly on PyPI, GitHub, GitLab, and BitBucket.

## When to Use This Skill

Use this skill when:

- Creating README files for Python packages intended for PyPI publication
- Converting between Markdown and reStructuredText formats
- Validating README markup before publishing to PyPI
- Setting up `pyproject.toml` metadata for README inclusion
- Generating README.rst files from Sphinx documentation
- Ensuring README compatibility across multiple platforms (PyPI, GitHub, GitLab, BitBucket)
- Troubleshooting README rendering issues on PyPI
- Creating documentation that balances technical accuracy with user accessibility

## Core Capabilities

### Supported Formats

PyPI's README renderer supports three formats with specific constraints:

1. **Plain Text** (`text/plain`)
   - Use for minimal documentation
   - No formatting capabilities
   - Renders exactly as written

2. **reStructuredText** (`text/x-rst`)
   - Rich formatting with directives and roles
   - **Critical limitation**: Sphinx extensions NOT allowed on PyPI
   - No `:py:func:`, `:ref:`, `:doc:`, or other Sphinx-specific roles
   - Standard docutils directives only (admonitions, code blocks, tables)
   - Use `sphinx-readme` extension to generate PyPI-compatible RST from Sphinx docs

3. **Markdown** (`text/markdown`)
   - GitHub Flavored Markdown (GFM) by default
   - Alternative: CommonMark
   - Modern, widely supported format
   - Excellent compatibility across platforms

### Format Selection Strategy

**Choose Markdown when:**

- Starting a new project without existing RST documentation
- Prioritizing GitHub/GitLab compatibility
- Team prefers Markdown syntax
- Documentation is primarily user-facing

**Choose reStructuredText when:**

- Project uses Sphinx for documentation
- Need advanced table formatting
- Existing RST documentation infrastructure
- Using `sphinx-readme` to generate from Sphinx docs

**Use sphinx-readme when:**

- Maintaining Sphinx documentation alongside PyPI README
- Need consistent formatting between docs and README
- Want to leverage Sphinx features while generating PyPI-compatible output
- Converting Sphinx-heavy documentation to PyPI-friendly format

## README Content Guidelines

### Essential Sections

Include these sections for comprehensive project documentation:

**Project Identity (Required)**

- Project name and one-line description
- Badges (build status, PyPI version, license, coverage)
- Quick value proposition

**Installation (Required)**

- Primary installation method: `pip install package-name`
- Alternative methods: `uv add package-name`, development installation
- System requirements and Python version compatibility

**Quick Start (Highly Recommended)**

- Minimal working example (3-10 lines)
- Expected output or result
- Link to full documentation

**Features (Recommended)**

- Bulleted list of key capabilities
- What makes this package unique
- Comparison with alternatives (if applicable)

**Usage Examples (Recommended)**

- 2-3 concrete examples showing common use cases
- Progressive complexity (basic → intermediate)
- Code samples with expected output

**Documentation Link (Required if comprehensive docs exist)**

- Link to Read the Docs, GitHub Pages, or hosted documentation
- Brief description of what's in the full docs

**Contributing (Recommended for open source)**

- How to report issues
- How to submit changes
- Link to CONTRIBUTING.md if detailed

**License (Required)**

- License name and link to LICENSE file
- Brief permissions statement

**Changelog/Release Notes (Optional)**

- Link to CHANGELOG.md or GitHub releases
- Brief summary of latest version

### Writing Style Principles

Follow these principles from documentation-expert and gitlab-docs-expert:

**Clarity and Simplicity**

- Write for users who are discovering your project for the first time
- Avoid jargon unless necessary and explained
- Use active voice and present tense
- Keep sentences concise (under 25 words)

**Focus on the User**

- Answer: "What can this do for me?" early
- Show working examples before explaining internals
- Provide copy-paste ready code snippets
- Include expected outputs to verify success

**Accuracy and Synchronization**

- Ensure code examples actually work with current version
- Test all commands before including
- Keep version numbers current
- Update README with each release

**Promote Consistency**

- Use consistent terminology throughout
- Follow same code style as project
- Match heading hierarchy (# → ## → ###)
- Use parallel structure in lists

**Leverage Visuals and Examples**

- Include code examples with syntax highlighting
- Show expected output or results
- Use badges for quick status information
- Consider diagrams for architecture (Mermaid on GitHub/GitLab)

## Format-Specific Guidance

### Markdown (README.md)

**Syntax Highlighting**

````markdown
```python
import package_name

result = package_name.process("example")
print(result)
# Output: Processed: example
```
````

**Badges**

```markdown
![PyPI version](https://img.shields.io/pypi/v/package-name.svg)
![Python versions](https://img.shields.io/pypi/pyversions/package-name.svg)
![License](https://img.shields.io/pypi/l/package-name.svg)
```

**Tables**

```markdown
| Feature | Support |
|---------|---------|
| Python 3.11+ | ✓ |
| Type hints | ✓ |
| Async support | ✓ |
```

**Alerts (GitHub/GitLab)**

```markdown
> [!NOTE]
> This feature requires Python 3.11 or higher.

> [!WARNING]
> Breaking changes in version 2.0. See migration guide.
```

**Links**

```markdown
[Documentation](https://package-name.readthedocs.io)
[PyPI](https://pypi.org/project/package-name/)
[Issues](https://github.com/user/package-name/issues)
```

### reStructuredText (README.rst)

**Syntax Highlighting**

```rst
.. code-block:: python

   import package_name

   result = package_name.process("example")
   print(result)
   # Output: Processed: example
```

**Badges**

```rst
.. image:: https://img.shields.io/pypi/v/package-name.svg
   :target: https://pypi.org/project/package-name/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/package-name.svg
   :alt: Python versions
```

**Tables**

```rst
+------------------+----------+
| Feature          | Support  |
+==================+==========+
| Python 3.11+     | ✓        |
+------------------+----------+
| Type hints       | ✓        |
+------------------+----------+
```

Or using simple table syntax:

```rst
========  =========
Feature   Support
========  =========
Python 3.11+  ✓
Type hints    ✓
========  =========
```

**Admonitions**

```rst
.. note::

   This feature requires Python 3.11 or higher.

.. warning::

   Breaking changes in version 2.0. See migration guide.

.. tip::

   Use the async API for better performance.
```

**Links**

```rst
`Documentation <https://package-name.readthedocs.io>`_
`PyPI <https://pypi.org/project/package-name/>`_
`Issues <https://github.com/user/package-name/issues>`_
```

**Section Headers**

```rst
================
Main Title
================

Section
=========

Subsection
-----------

Subsubsection
^^^^^^^^^^^^^^
```

### Sphinx README Integration

For projects using Sphinx, leverage `sphinx-readme` to generate PyPI-compatible README.rst files.

**Installation**

```bash
uv add --group docs sphinx-readme
```

**Configuration in conf.py**

```python
extensions = [
    'sphinx_readme',
]

# Optional configuration
readme_config = {
    'src_file': 'index.rst',  # Source file in docs/
    'out_file': '../README.rst',  # Output to project root
}
```

**Key Benefits**

- Converts Sphinx-specific roles to PyPI-compatible equivalents
- Preserves admonitions, code blocks, and formatting
- Maintains single source of truth in Sphinx docs
- Automatically handles cross-references

**Limitations**

- Sphinx roles (`:py:func:`, `:ref:`) converted to plain text or removed
- Advanced Sphinx features may not translate
- Review generated output before publishing

**Workflow**

```bash
# Build Sphinx docs (generates README.rst automatically)
uv run sphinx-build -b html docs/ docs/_build/html

# Verify README rendering
uv run --with twine twine check dist/*
```

## PyPI Integration

### pyproject.toml Configuration

**For Markdown README**

```toml
[project]
name = "package-name"
version = "1.0.0"
description = "Short one-line description"
readme = "README.md"  # Automatically sets content-type to text/markdown
requires-python = ">=3.11"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
keywords = ["keyword1", "keyword2"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

[project.urls]
Homepage = "https://github.com/user/package-name"
Documentation = "https://package-name.readthedocs.io"
Repository = "https://github.com/user/package-name"
Issues = "https://github.com/user/package-name/issues"
Changelog = "https://github.com/user/package-name/blob/main/CHANGELOG.md"
```

**For reStructuredText README**

```toml
[project]
readme = "README.rst"  # Automatically sets content-type to text/x-rst
# ... rest of configuration
```

**For custom content type**

```toml
[project]
readme = {file = "README.md", content-type = "text/markdown"}
# or
readme = {file = "README.rst", content-type = "text/x-rst"}
```

**For GitHub Flavored Markdown (explicit)**

```toml
[project]
readme = {file = "README.md", content-type = "text/markdown; variant=GFM"}
```

**For CommonMark**

```toml
[project]
readme = {file = "README.md", content-type = "text/markdown; variant=CommonMark"}
```

### Building and Publishing

**Build distribution packages**

```bash
# Using uv (modern approach)
uv build

# Outputs to dist/:
# - package_name-1.0.0-py3-none-any.whl
# - package_name-1.0.0.tar.gz
```

**Validate README rendering**

```bash
# Check that README will render on PyPI
uv run --with twine twine check dist/*
```

Expected output for success:

```
Checking dist/package_name-1.0.0-py3-none-any.whl: Passed
Checking dist/package_name-1.0.0.tar.gz: Passed
```

**Common validation errors**

| Error | Cause | Solution |
| --- | --- | --- |
| `Unknown interpreted text role "py:func"` | Sphinx role in RST | Remove Sphinx-specific roles, use plain text |
| `Unexpected indentation` | RST indentation error | Fix indentation, ensure blank lines before/after directives |
| `Unknown directive type "automodule"` | Sphinx directive in RST | Remove Sphinx directives, use standard docutils only |
| `Invalid markup` | Malformed RST | Run `rst2html.py README.rst /dev/null` to test |
| Content not showing | Wrong content-type | Verify `readme` setting in pyproject.toml matches file format |

**Publish to PyPI**

```bash
# Upload to PyPI (requires API token)
uv run --with twine twine upload dist/*

# Test on TestPyPI first (recommended)
uv run --with twine twine upload --repository testpypi dist/*
```

**Setting up PyPI credentials**

```bash
# Create ~/.pypirc
cat > ~/.pypirc << 'EOF'
[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
username = __token__
password = pypi-your-testpypi-token-here
EOF

chmod 600 ~/.pypirc
```

## Validation Workflow

### Pre-Publish Checklist

Run this workflow before publishing to PyPI:

```bash
# 1. Build the package
uv build

# 2. Validate README rendering
uv run --with twine twine check dist/*

# 3. Test installation locally
uv pip install dist/*.whl

# 4. Upload to TestPyPI
uv run --with twine twine upload --repository testpypi dist/*

# 5. Visit TestPyPI page and verify README renders correctly
# https://test.pypi.org/project/package-name/

# 6. Test installation from TestPyPI
uv pip install --index-url https://test.pypi.org/simple/ package-name

# 7. If all looks good, upload to production PyPI
uv run --with twine twine upload dist/*
```

### Local README Testing

**Test Markdown rendering locally**

```bash
# Install grip (GitHub README previewer)
uv tool install grip

# Preview README.md
uvx grip README.md
# Opens browser at http://localhost:6419
```

**Test reStructuredText rendering locally**

```bash
# Convert RST to HTML for preview
uv run --with docutils rst2html.py README.rst README.html

# Open in browser
xdg-open README.html  # Linux
open README.html      # macOS
```

**Validate RST syntax**

```bash
# Check for RST errors
uv run --with docutils rst2html.py README.rst /dev/null
# Only shows errors/warnings, no output file
```

## Common Issues and Solutions

### reStructuredText Issues

**Issue: Sphinx roles not rendering**

```rst
❌ WRONG (will fail on PyPI):
See :py:func:`package.function` for details.
Use :ref:`my-label` for more information.

✓ CORRECT (PyPI-compatible):
See ``package.function()`` for details.
Use `my-label`_ for more information.

.. _my-label: https://docs.example.com/section
```

**Issue: Code block indentation**

```rst
❌ WRONG:
.. code-block:: python
import package  # No blank line, incorrect indent

✓ CORRECT:
.. code-block:: python

   import package  # Blank line after directive, proper indent
   package.run()
```

**Issue: Link definition spacing**

```rst
❌ WRONG:
`Documentation`_
.. _Documentation: https://example.com  # Too close

✓ CORRECT:
`Documentation`_

.. _Documentation: https://example.com  # Blank line before
```

### Markdown Issues

**Issue: Code fence language specification**

````markdown
❌ WRONG:
```
import package  # No language specified
```

✓ CORRECT:
```python
import package
```
````

**Issue: Heading hierarchy**

```markdown
❌ WRONG:
# Title
### Subsection  # Skipped ##

✓ CORRECT:
# Title
## Section
### Subsection
```

### Cross-Platform Compatibility

**Issue: Platform-specific line endings**

```bash
# Convert to Unix line endings (LF)
dos2unix README.md  # or README.rst

# Or using Python
uv run python -c "
import sys
with open('README.md', 'r') as f:
    content = f.read()
with open('README.md', 'w', newline='\n') as f:
    f.write(content)
"
```

**Issue: Rendering differences GitHub vs PyPI**

- **GitHub**: Supports GFM extensions (alerts, task lists, tables)
- **PyPI**: Supports basic GFM, but may render differently
- **Solution**: Test on TestPyPI before publishing

## Example README Templates

See reference files for complete examples:

- [./references/markdown-template.md](./references/markdown-template.md) - Modern Markdown README template
- [./references/rst-template.rst](./references/rst-template.rst) - reStructuredText README template
- [./references/sphinx-readme-example.md](./references/sphinx-readme-example.md) - Using sphinx-readme extension

## Related Skills and Tools

**Skills to activate:**

- `uv` - For Python project and package management
- `hatchling` - For build backend configuration
- `gitlab-skill` - For GitLab Flavored Markdown features

**External tools:**

- `twine` - README validation and PyPI publishing
- `sphinx-readme` - Generate PyPI-compatible RST from Sphinx
- `grip` - Preview Markdown as GitHub renders it
- `docutils` - Validate and convert reStructuredText
- `pandoc` - Convert between Markdown and RST

## Quality Standards

Before finalizing a README:

- [ ] One-line description clearly states project purpose
- [ ] Installation instructions tested and accurate
- [ ] Code examples run successfully with current version
- [ ] All links valid and point to correct destinations
- [ ] Badges display correctly and are current
- [ ] Markup validated with `twine check`
- [ ] Tested rendering on target platforms (PyPI, GitHub/GitLab)
- [ ] Spelling and grammar checked
- [ ] Heading hierarchy is consistent (no skipped levels)
- [ ] License clearly stated
- [ ] Python version requirements specified
- [ ] Content type correctly set in pyproject.toml

## Key Principles

1. **User-First Design**: Answer "What does this do for me?" in the first paragraph
2. **Show, Don't Tell**: Working code examples over abstract descriptions
3. **Platform Compatibility**: Test rendering on all target platforms
4. **Format Constraints**: Respect PyPI limitations (no Sphinx extensions in RST)
5. **Validation Before Publishing**: Always run `twine check` before uploading
6. **Single Source of Truth**: Use `sphinx-readme` for Sphinx-based projects
7. **Accessibility**: Write for diverse audiences (beginners to experts)
8. **Maintenance**: Update README with each release

## References

### Official Documentation

- [Making a PyPI-friendly README](https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/) - Official Python Packaging Guide
- [PyPI README Renderer](https://github.com/pypa/readme_renderer) - PyPI's rendering engine
- [sphinx-readme Documentation](https://sphinx-readme.readthedocs.io/) - Sphinx to PyPI README converter
- [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html) - Sphinx RST guide
- [GitHub Flavored Markdown](https://github.github.com/gfm/) - GFM specification
- [CommonMark](https://commonmark.org/) - CommonMark specification

### Tool Documentation

- [Twine Documentation](https://twine.readthedocs.io/) - Package upload tool
- [uv Documentation](https://docs.astral.sh/uv/) - Modern Python package manager
- [Hatchling Documentation](https://hatchling.pypa.io/) - Modern build backend

### Related Resources

- [readme-renderer on PyPI](https://pypi.org/project/readme-renderer/) - Test README rendering
- [Grip](https://github.com/joeyespo/grip) - Preview Markdown as GitHub renders
- [m2rr](https://github.com/qhua948/m2rr) - Markdown to reStructuredText converter
- [Pandoc](https://pandoc.org/) - Universal document converter
