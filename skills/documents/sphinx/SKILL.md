---
name: sphinx
description: Generate comprehensive Python documentation with Sphinx. Covers autodoc for API extraction, Napoleon for Google/NumPy docstrings, intersphinx for cross-references, and multiple output formats including HTML, PDF, and ePub.
version: 1.0.0
category: documentation
type: skill
capabilities:
  - Automatic API documentation from docstrings
  - reStructuredText and MyST Markdown support
  - Napoleon extension for Google/NumPy docstrings
  - Cross-project references with intersphinx
  - Multiple output formats (HTML, PDF, ePub, man pages)
  - Read the Docs theme integration
  - Code documentation with viewcode
  - Type hint documentation with autodoc_typehints
  - Custom domain extensions
  - Internationalization (i18n) support
tools:
  - sphinx
  - sphinx-rtd-theme
  - sphinx-autodoc-typehints
  - myst-parser
  - sphinx-copybutton
  - sphinxcontrib-napoleon
  - sphinx-autoapi
tags:
  - documentation
  - python
  - api-reference
  - autodoc
  - rst
  - pdf
  - readthedocs
platforms:
  - linux
  - macos
  - windows
related_skills:
  - mkdocs
  - pandoc
  - docusaurus
---

# Sphinx Python Documentation Skill

Generate professional, comprehensive documentation for Python projects with Sphinx. This skill covers API documentation extraction, multiple output formats, and integration with Read the Docs.

## When to Use This Skill

### USE When

- Building Python library or package documentation
- Need automatic API reference from docstrings
- Require PDF or ePub documentation output
- Using Google or NumPy docstring styles
- Need cross-references between documentation projects
- Deploying to Read the Docs
- Building scientific or academic documentation
- Need versioned API documentation
- Working with large Python codebases
- Require internationalized documentation

### DON'T USE When

- Simple project documentation without API docs (use MkDocs)
- Non-Python projects (use MkDocs or Docusaurus)
- Need React components in docs (use Docusaurus)
- Quick format conversion only (use Pandoc)
- Building presentation slides (use Marp)
- Collaborative wiki-style docs (use GitBook)

## Prerequisites

### Installation

```bash
# Core Sphinx installation
pip install sphinx

# With common extensions
pip install sphinx \
    sphinx-rtd-theme \
    sphinx-autodoc-typehints \
    sphinx-copybutton \
    myst-parser \
    sphinxcontrib-mermaid

# Using uv
uv pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints

# For PDF output
pip install sphinx latexmk
# Plus LaTeX distribution (texlive-full on Ubuntu, MacTeX on macOS)

# Verify installation
sphinx-build --version
```

### System Requirements

- Python 3.8 or higher
- pip or uv package manager
- LaTeX distribution (for PDF output)
- Graphviz (optional, for diagrams)

## Core Capabilities

### 1. Project Initialization

```bash
# Quick start with sphinx-quickstart
sphinx-quickstart docs

# Answer the prompts:
# > Separate source and build directories (y/n) [n]: y
# > Project name: MyProject
# > Author name(s): Your Name
# > Project release: 1.0.0
# > Project language [en]: en

# Generated structure:
# docs/
# ├── source/
# │   ├── conf.py
# │   ├── index.rst
# │   └── _static/
# │   └── _templates/
# └── build/
#     └── (output files)

# Or manual setup
mkdir -p docs/source docs/build
touch docs/source/conf.py docs/source/index.rst
```

### 2. Basic Configuration (conf.py)

```python
# docs/source/conf.py

# -- Project information -----------------------------------------------------
project = 'MyProject'
copyright = '2024-2026, Your Name'
author = 'Your Name'
release = '1.0.0'
version = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.githubpages',
    'sphinx_rtd_theme',
    'sphinx_copybutton',
    'myst_parser',
]

# Source file suffixes
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# Master document
master_doc = 'index'

# Exclude patterns
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Pygments style
pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = '_static/logo.png'
html_favicon = '_static/favicon.ico'

html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
    'style_nav_header_background': '#2980B9',
    # Toc options
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
}

# -- Options for autodoc -----------------------------------------------------
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__',
    'show-inheritance': True,
}

autodoc_typehints = 'description'
autodoc_typehints_description_target = 'documented'
autodoc_class_signature = 'separated'

# -- Options for Napoleon (Google/NumPy docstrings) -------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_attr_annotations = True

# -- Options for intersphinx -------------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'requests': ('https://requests.readthedocs.io/en/latest/', None),
}

# -- Options for todo extension ----------------------------------------------
todo_include_todos = True

# -- Options for LaTeX/PDF output --------------------------------------------
latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '11pt',
    'preamble': r'''
        \usepackage{charter}
        \usepackage[defaultsans]{lato}
        \usepackage{inconsolata}
    ''',
}

latex_documents = [
    (master_doc, 'MyProject.tex', 'MyProject Documentation',
     'Your Name', 'manual'),
]

# -- Options for EPUB output -------------------------------------------------
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ['search.html']
```

### 3. Index and Table of Contents

```rst
.. docs/source/index.rst

Welcome to MyProject
====================

MyProject is a powerful library for doing amazing things.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart
   configuration

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   guide/overview
   guide/core-concepts
   guide/advanced-usage
   guide/best-practices

.. toctree::
   :maxdepth: 3
   :caption: API Reference

   api/modules
   api/mypackage

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing
   changelog
   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

### 4. Autodoc - Automatic API Documentation

```python
# src/mypackage/core.py

"""
Core module for MyPackage.

This module provides the main classes and functions for
data processing and analysis.

Example:
    Basic usage of the module::

        from mypackage.core import DataProcessor
        processor = DataProcessor()
        result = processor.process(data)

"""

from typing import Any, Dict, List, Optional, Union
from pathlib import Path


class DataProcessor:
    """
    A class for processing and analyzing data.

    This processor supports multiple data formats and provides
    methods for validation, transformation, and export.

    Attributes:
        config: Configuration dictionary for the processor.
        verbose: Whether to print verbose output.
        _cache: Internal cache for processed results.

    Example:
        >>> processor = DataProcessor(verbose=True)
        >>> processor.load("data.csv")
        >>> result = processor.process()
    """

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        verbose: bool = False
    ) -> None:
        """
        Initialize the DataProcessor.

        Args:
            config: Optional configuration dictionary. If not provided,
                defaults will be used. Keys include:
                - ``max_rows``: Maximum rows to process (default: 10000)
                - ``encoding``: File encoding (default: 'utf-8')
                - ``delimiter``: CSV delimiter (default: ',')
            verbose: If True, print progress information during
                processing. Defaults to False.

        Raises:
            ValueError: If config contains invalid keys.

        Example:
            >>> config = {'max_rows': 5000, 'encoding': 'utf-8'}
            >>> processor = DataProcessor(config=config, verbose=True)
        """
        self.config = config or {}
        self.verbose = verbose
        self._cache: Dict[str, Any] = {}

    def load(
        self,
        path: Union[str, Path],
        *,
        validate: bool = True
    ) -> 'DataProcessor':
        """
        Load data from a file.

        Supports CSV, JSON, and Parquet formats. The format is
        automatically detected from the file extension.

        Args:
            path: Path to the data file. Can be a string or
                :class:`pathlib.Path` object.
            validate: Whether to validate data after loading.
                Defaults to True.

        Returns:
            Self for method chaining.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format is not supported.

        Example:
            >>> processor = DataProcessor()
            >>> processor.load("input.csv", validate=True)
            <DataProcessor object>

        See Also:
            :meth:`save`: Save processed data to file.
            :meth:`validate`: Validate loaded data.

        Note:
            Large files (>1GB) may require additional memory.
            Consider using chunked processing for such files.
        """
        # Implementation here
        return self

    def process(
        self,
        operations: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Process the loaded data with specified operations.

        Args:
            operations: List of operation names to apply.
                Available operations:
                - ``'clean'``: Remove null values
                - ``'normalize'``: Normalize numeric columns
                - ``'aggregate'``: Compute aggregations
                If None, all operations are applied.

        Returns:
            Dictionary containing:
            - ``data``: Processed data
            - ``stats``: Processing statistics
            - ``errors``: List of any errors encountered

        Raises:
            RuntimeError: If no data has been loaded.

        Warning:
            This method modifies the internal data state.
            Use :meth:`copy` first if you need the original.

        Example:
            >>> processor.load("data.csv")
            >>> result = processor.process(['clean', 'normalize'])
            >>> print(result['stats'])
            {'rows_processed': 1000, 'time_ms': 42}
        """
        return {'data': None, 'stats': {}, 'errors': []}

    def save(
        self,
        path: Union[str, Path],
        format: str = 'csv'
    ) -> None:
        """
        Save processed data to a file.

        Args:
            path: Output file path.
            format: Output format. One of:
                - ``'csv'``: Comma-separated values
                - ``'json'``: JSON format
                - ``'parquet'``: Apache Parquet format

        Raises:
            ValueError: If format is not supported.
            IOError: If file cannot be written.

        Example:
            >>> processor.process()
            >>> processor.save("output.csv", format='csv')
        """
        pass


def calculate_metrics(
    data: List[float],
    *,
    include_variance: bool = False
) -> Dict[str, float]:
    """
    Calculate statistical metrics for a list of values.

    This function computes common statistical measures
    for the provided data.

    Args:
        data: List of numeric values to analyze.
        include_variance: Whether to include variance
            in the results. Defaults to False.

    Returns:
        Dictionary with the following keys:
        - ``mean``: Arithmetic mean
        - ``median``: Median value
        - ``min``: Minimum value
        - ``max``: Maximum value
        - ``variance``: (optional) Population variance

    Raises:
        ValueError: If data is empty.
        TypeError: If data contains non-numeric values.

    Example:
        >>> metrics = calculate_metrics([1, 2, 3, 4, 5])
        >>> print(metrics['mean'])
        3.0

    Note:
        For large datasets (>1M values), consider using
        NumPy functions for better performance.
    """
    if not data:
        raise ValueError("Data cannot be empty")

    result = {
        'mean': sum(data) / len(data),
        'median': sorted(data)[len(data) // 2],
        'min': min(data),
        'max': max(data),
    }

    if include_variance:
        mean = result['mean']
        result['variance'] = sum((x - mean) ** 2 for x in data) / len(data)

    return result
```

```rst
.. docs/source/api/mypackage.rst

mypackage package
=================

.. automodule:: mypackage
   :members:
   :undoc-members:
   :show-inheritance:

mypackage.core module
---------------------

.. automodule:: mypackage.core
   :members:
   :undoc-members:
   :show-inheritance:

mypackage.utils module
----------------------

.. automodule:: mypackage.utils
   :members:
   :undoc-members:
   :show-inheritance:
```

### 5. Generate API Documentation

```bash
# Auto-generate API documentation stubs
sphinx-apidoc -o docs/source/api src/mypackage -f -e -M

# Options:
# -o: Output directory
# -f: Force overwrite
# -e: Separate pages for each module
# -M: Module-first ordering
# -d 2: TOC depth

# Build HTML documentation
sphinx-build -b html docs/source docs/build/html

# Build with verbose output
sphinx-build -b html docs/source docs/build/html -v

# Clean and rebuild
rm -rf docs/build && sphinx-build -b html docs/source docs/build/html
```

### 6. MyST Markdown Support

```python
# conf.py - Enable MyST
extensions = [
    'myst_parser',
]

# MyST configuration
myst_enable_extensions = [
    'amsmath',
    'colon_fence',
    'deflist',
    'dollarmath',
    'fieldlist',
    'html_admonition',
    'html_image',
    'replacements',
    'smartquotes',
    'strikethrough',
    'substitution',
    'tasklist',
]

myst_heading_anchors = 3
myst_footnote_transition = True
```

```markdown
<!-- docs/source/guide/overview.md -->

# Overview

This guide provides an overview of MyProject.

## Features

MyProject includes the following features:

- Fast data processing
- Multiple format support
- Extensible architecture

## Quick Example

```{code-block} python
:linenos:
:emphasize-lines: 2,4

from mypackage import DataProcessor

processor = DataProcessor()
result = processor.process(data)
```

## Admonitions

```{note}
This is a note admonition in MyST syntax.
```

```{warning}
Be careful with this operation!
```

```{tip}
Use this feature for better performance.
```

## Cross-References

See the {ref}`installation` guide for setup instructions.

Check the {py:class}`mypackage.core.DataProcessor` class reference.

## Math Support

Inline math: $E = mc^2$

Display math:

$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$

## Task Lists

- [x] Write documentation
- [x] Add code examples
- [ ] Review and publish

## Definition Lists

Term 1
: Definition for term 1

Term 2
: Definition for term 2
```

### 7. Intersphinx Cross-References

```python
# conf.py
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'sklearn': ('https://scikit-learn.org/stable/', None),
}

# Timeout for fetching inventory files
intersphinx_timeout = 30
```

```rst
.. Usage in documentation

Using NumPy Arrays
------------------

This function accepts :class:`numpy.ndarray` objects.

See :func:`numpy.array` for creating arrays.

The algorithm is based on :meth:`pandas.DataFrame.groupby`.

For plotting, use :func:`matplotlib.pyplot.plot`.
```

### 8. Multiple Output Formats

```bash
# Build HTML
sphinx-build -b html docs/source docs/build/html

# Build PDF (requires LaTeX)
sphinx-build -b latex docs/source docs/build/latex
cd docs/build/latex && make

# Build ePub
sphinx-build -b epub docs/source docs/build/epub

# Build man pages
sphinx-build -b man docs/source docs/build/man

# Build single HTML file
sphinx-build -b singlehtml docs/source docs/build/singlehtml

# Build plain text
sphinx-build -b text docs/source docs/build/text

# Check for broken links
sphinx-build -b linkcheck docs/source docs/build/linkcheck

# Check documentation coverage
sphinx-build -b coverage docs/source docs/build/coverage
```

```python
# conf.py - PDF customization
latex_engine = 'xelatex'

latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'figure_align': 'htbp',
    'preamble': r'''
        \usepackage{charter}
        \usepackage[defaultsans]{lato}
        \usepackage{inconsolata}

        % Custom chapter styling
        \usepackage{titlesec}
        \titleformat{\chapter}[display]
          {\normalfont\huge\bfseries}
          {\chaptertitlename\ \thechapter}{20pt}{\Huge}

        % Code block styling
        \usepackage{fancyvrb}
        \fvset{fontsize=\small}
    ''',
    'maketitle': r'''
        \begin{titlepage}
            \centering
            \vspace*{2cm}
            {\Huge\bfseries MyProject Documentation\par}
            \vspace{1cm}
            {\Large Version 1.0.0\par}
            \vspace{2cm}
            {\large Your Name\par}
            \vfill
            {\large \today\par}
        \end{titlepage}
    ''',
}

latex_documents = [
    (master_doc, 'myproject.tex', 'MyProject Documentation',
     'Your Name', 'manual', True),
]

latex_show_urls = 'footnote'
latex_show_pagerefs = True
```

### 9. Read the Docs Configuration

```yaml
# .readthedocs.yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.11"
  jobs:
    pre_build:
      - pip install -e ".[docs]"

sphinx:
  configuration: docs/source/conf.py
  fail_on_warning: true

python:
  install:
    - requirements: docs/requirements.txt
    - method: pip
      path: .
      extra_requirements:
        - docs

formats:
  - pdf
  - epub
```

```text
# docs/requirements.txt
sphinx>=7.0.0
sphinx-rtd-theme>=2.0.0
sphinx-autodoc-typehints>=1.25.0
sphinx-copybutton>=0.5.0
myst-parser>=2.0.0
sphinxcontrib-mermaid>=0.9.0
```

### 10. Custom Extensions

```python
# docs/source/_extensions/custom_directive.py

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.application import Sphinx


class VersionAddedDirective(Directive):
    """
    Custom directive to mark version additions.

    Usage::

        .. versionadded:: 1.2.0

            This feature was added in version 1.2.0.
    """

    required_arguments = 1
    optional_arguments = 0
    has_content = True

    def run(self):
        version = self.arguments[0]
        content = '\n'.join(self.content)

        para = nodes.paragraph()
        para += nodes.strong(text=f'New in version {version}: ')
        para += nodes.Text(content)

        container = nodes.container(classes=['versionadded'])
        container += para

        return [container]


class APIEndpointDirective(Directive):
    """
    Custom directive for API endpoints.

    Usage::

        .. api-endpoint:: GET /api/v1/users

            Retrieve list of users.

            :param page: Page number
            :param limit: Items per page
            :returns: JSON array of users
    """

    required_arguments = 1
    optional_arguments = 0
    has_content = True
    option_spec = {
        'deprecated': lambda x: x,
    }

    def run(self):
        method_path = self.arguments[0]
        parts = method_path.split(' ', 1)
        method = parts[0] if len(parts) > 0 else 'GET'
        path = parts[1] if len(parts) > 1 else '/'

        # Create container
        container = nodes.container(classes=['api-endpoint'])

        # Add method badge
        method_node = nodes.literal(text=method, classes=[f'method-{method.lower()}'])
        path_node = nodes.literal(text=path, classes=['endpoint-path'])

        header = nodes.paragraph()
        header += method_node
        header += nodes.Text(' ')
        header += path_node
        container += header

        # Add content
        if self.content:
            content = nodes.container()
            self.state.nested_parse(self.content, self.content_offset, content)
            container += content

        return [container]


def setup(app: Sphinx):
    app.add_directive('versionadded', VersionAddedDirective)
    app.add_directive('api-endpoint', APIEndpointDirective)

    return {
        'version': '1.0.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
```

```python
# conf.py - Register custom extension
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / '_extensions'))

extensions = [
    # ... other extensions
    'custom_directive',
]
```

### 11. GitHub Actions Deployment

```yaml
# .github/workflows/docs.yml
name: Documentation

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'src/**/*.py'
      - '.github/workflows/docs.yml'
  pull_request:
    paths:
      - 'docs/**'
      - 'src/**/*.py'

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e ".[docs]"
          pip install -r docs/requirements.txt

      - name: Build documentation
        run: |
          cd docs
          sphinx-build -b html source build/html -W --keep-going

      - name: Check links
        run: |
          cd docs
          sphinx-build -b linkcheck source build/linkcheck

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: documentation
          path: docs/build/html

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: documentation
          path: docs/build/html

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: docs/build/html
```

### 12. API Documentation with sphinx-autoapi

```python
# conf.py - Using sphinx-autoapi (alternative to autodoc)
extensions = [
    'autoapi.extension',
]

# AutoAPI configuration
autoapi_type = 'python'
autoapi_dirs = ['../../src/mypackage']
autoapi_template_dir = '_templates/autoapi'
autoapi_options = [
    'members',
    'undoc-members',
    'show-inheritance',
    'show-module-summary',
    'special-members',
    'imported-members',
]
autoapi_python_class_content = 'both'
autoapi_member_order = 'groupwise'
autoapi_root = 'api'
autoapi_keep_files = True
autoapi_add_toctree_entry = True

# Suppress autodoc if using autoapi
autodoc_default_options = {}
```

## Integration Examples

### Integration with pyproject.toml

```toml
# pyproject.toml
[project]
name = "mypackage"
version = "1.0.0"
description = "A Python package with Sphinx docs"
readme = "README.md"
requires-python = ">=3.8"

[project.optional-dependencies]
docs = [
    "sphinx>=7.0.0",
    "sphinx-rtd-theme>=2.0.0",
    "sphinx-autodoc-typehints>=1.25.0",
    "sphinx-copybutton>=0.5.0",
    "myst-parser>=2.0.0",
]

[tool.setuptools.packages.find]
where = ["src"]
```

### Integration with Makefile

```makefile
# docs/Makefile
SPHINXOPTS    ?= -W --keep-going
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

.PHONY: help clean html pdf epub linkcheck livehtml

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

clean:
	rm -rf $(BUILDDIR)/*

html:
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS)
	@echo "Build finished. Open $(BUILDDIR)/html/index.html"

pdf:
	@$(SPHINXBUILD) -b latex "$(SOURCEDIR)" "$(BUILDDIR)/latex" $(SPHINXOPTS)
	@$(MAKE) -C "$(BUILDDIR)/latex" all-pdf
	@echo "Build finished. PDF at $(BUILDDIR)/latex/*.pdf"

epub:
	@$(SPHINXBUILD) -b epub "$(SOURCEDIR)" "$(BUILDDIR)/epub" $(SPHINXOPTS)
	@echo "Build finished. EPUB at $(BUILDDIR)/epub/*.epub"

linkcheck:
	@$(SPHINXBUILD) -b linkcheck "$(SOURCEDIR)" "$(BUILDDIR)/linkcheck" $(SPHINXOPTS)

livehtml:
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS)
```

### Integration with Pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: sphinx-build
        name: Build Sphinx documentation
        entry: sphinx-build -b html docs/source docs/build/html -W
        language: system
        pass_filenames: false
        types: [python, rst, markdown]
```

## Best Practices

### 1. Docstring Style Guide

```python
# Use Google style (recommended)
def function(arg1: str, arg2: int = 10) -> bool:
    """
    Short description of function.

    Longer description that provides more detail about
    what the function does and how it works.

    Args:
        arg1: Description of arg1.
        arg2: Description of arg2. Defaults to 10.

    Returns:
        Description of return value.

    Raises:
        ValueError: If arg1 is empty.
        TypeError: If arg2 is not an integer.

    Example:
        >>> function("hello", 5)
        True

    Note:
        Additional notes about usage.

    See Also:
        related_function: Description of related function.
    """
    pass
```

### 2. Documentation Structure

```
docs/
├── source/
│   ├── _static/
│   │   ├── css/
│   │   │   └── custom.css
│   │   └── images/
│   ├── _templates/
│   │   └── layout.html
│   ├── api/
│   │   ├── index.rst
│   │   └── modules.rst
│   ├── guide/
│   │   ├── installation.rst
│   │   ├── quickstart.rst
│   │   └── advanced.rst
│   ├── tutorials/
│   │   └── basic.rst
│   ├── conf.py
│   ├── index.rst
│   └── changelog.rst
├── build/
├── Makefile
└── requirements.txt
```

### 3. Cross-Reference Best Practices

```rst
.. Use these reference styles

Classes and Methods
~~~~~~~~~~~~~~~~~~~

See :class:`mypackage.core.DataProcessor` for the main class.

Use :meth:`~mypackage.core.DataProcessor.process` method.

The :attr:`mypackage.core.DataProcessor.config` attribute.

Functions
~~~~~~~~~

Call :func:`mypackage.utils.helper` for utility functions.

Modules
~~~~~~~

Import from :mod:`mypackage.core` module.

External References
~~~~~~~~~~~~~~~~~~~

Uses :class:`numpy.ndarray` for array storage.

See :func:`pandas.read_csv` for file loading.
```

### 4. Version Documentation

```rst
.. Document version changes

API Changes
-----------

.. versionadded:: 1.2.0
   Added support for Parquet format.

.. versionchanged:: 1.3.0
   The ``format`` parameter now defaults to ``'auto'``.

.. deprecated:: 2.0.0
   Use :meth:`new_method` instead. Will be removed in v3.0.

.. versionremoved:: 2.0.0
   The ``old_param`` parameter has been removed.
```

## Troubleshooting

### Common Issues

#### Autodoc Cannot Find Module

```python
# conf.py - Add source to path
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / 'src'))
```

#### Intersphinx Inventory Not Loading

```python
# conf.py - Use local inventory file
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', 'python-objects.inv'),
}

# Download inventory manually
# curl -O https://docs.python.org/3/objects.inv
```

#### Build Warnings as Errors

```bash
# Build without -W flag for debugging
sphinx-build -b html docs/source docs/build/html

# Then fix warnings before re-enabling
sphinx-build -b html docs/source docs/build/html -W
```

#### Napoleon Not Parsing Docstrings

```python
# conf.py - Ensure napoleon is configured
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# Check docstring format - must have proper indentation
def func():
    """
    Summary line.

    Args:
        param: Description.  # Note: proper indentation
    """
```

#### PDF Build Fails

```bash
# Install full LaTeX distribution
# Ubuntu
sudo apt-get install texlive-full

# macOS
brew install --cask mactex

# Check LaTeX installation
pdflatex --version
latexmk --version
```

### Debug Mode

```bash
# Verbose build
sphinx-build -b html docs/source docs/build/html -v

# Very verbose
sphinx-build -b html docs/source docs/build/html -vvv

# Show traceback on errors
sphinx-build -b html docs/source docs/build/html -T

# Keep going on errors
sphinx-build -b html docs/source docs/build/html --keep-going
```

## Version History

### v1.0.0 (2026-01-17)

- Initial skill creation
- Autodoc configuration for Python API
- Napoleon support for Google/NumPy docstrings
- Intersphinx cross-references
- Multiple output formats (HTML, PDF, ePub)
- Read the Docs configuration
- MyST Markdown support
- Custom extensions guide
- GitHub Actions deployment

## Related Resources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Read the Docs](https://docs.readthedocs.io/)
- [Napoleon Extension](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)
- [MyST Parser](https://myst-parser.readthedocs.io/)
- [Sphinx Themes Gallery](https://sphinx-themes.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

---

*Generate comprehensive Python documentation with automatic API extraction and professional output formats.*
