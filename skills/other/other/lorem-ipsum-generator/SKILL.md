---
name: lorem-ipsum-generator
description: Generate placeholder text (lorem ipsum) in various formats. Create paragraphs, sentences, words, or custom templates for mockups and testing.
---

# Lorem Ipsum Generator

Generate placeholder text for mockups, wireframes, and testing purposes.

## Features

- **Classic Lorem**: Traditional lorem ipsum text
- **Multiple Formats**: Paragraphs, sentences, words, lists
- **Custom Length**: Specify exact word/sentence/paragraph counts
- **HTML Output**: Generate with HTML tags
- **Alternative Sources**: Hipster, bacon, corporate ipsum variations
- **Templates**: Fill templates with placeholder text

## Quick Start

```python
from lorem_gen import LoremGenerator

gen = LoremGenerator()

# Generate paragraphs
text = gen.paragraphs(3)
print(text)

# Generate sentences
sentences = gen.sentences(5)
print(sentences)

# Generate words
words = gen.words(50)
print(words)
```

## CLI Usage

```bash
# Generate 3 paragraphs
python lorem_gen.py --paragraphs 3

# Generate 5 sentences
python lorem_gen.py --sentences 5

# Generate 100 words
python lorem_gen.py --words 100

# HTML output
python lorem_gen.py --paragraphs 3 --html

# Generate bullet list
python lorem_gen.py --list 5

# Generate with specific word count per paragraph
python lorem_gen.py --paragraphs 3 --words-per 50

# Alternative style
python lorem_gen.py --paragraphs 3 --style hipster

# Save to file
python lorem_gen.py --paragraphs 5 --output placeholder.txt
```

## API Reference

### LoremGenerator Class

```python
class LoremGenerator:
    def __init__(self, style: str = "classic")

    # Basic generation
    def paragraphs(self, count: int = 3, words_per: int = None) -> str
    def sentences(self, count: int = 5) -> str
    def words(self, count: int = 50) -> str

    # Structured output
    def list_items(self, count: int = 5, ordered: bool = False) -> str
    def heading(self, level: int = 1) -> str
    def title(self, words: int = 4) -> str

    # HTML output
    def html_paragraphs(self, count: int = 3) -> str
    def html_list(self, count: int = 5, ordered: bool = False) -> str
    def html_article(self, sections: int = 3) -> str

    # Templates
    def fill_template(self, template: str) -> str

    # Configuration
    def set_style(self, style: str) -> 'LoremGenerator'
```

## Output Formats

### Paragraphs

```python
text = gen.paragraphs(2)

# Output:
# Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do
# eiusmod tempor incididunt ut labore et dolore magna aliqua.
#
# Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
# nisi ut aliquip ex ea commodo consequat.
```

### Sentences

```python
text = gen.sentences(3)

# Output:
# Lorem ipsum dolor sit amet. Consectetur adipiscing elit. Sed do eiusmod tempor.
```

### Words

```python
text = gen.words(10)

# Output:
# Lorem ipsum dolor sit amet consectetur adipiscing elit sed do
```

### Lists

```python
# Unordered list
text = gen.list_items(3)
# - Lorem ipsum dolor sit amet
# - Consectetur adipiscing elit
# - Sed do eiusmod tempor

# Ordered list
text = gen.list_items(3, ordered=True)
# 1. Lorem ipsum dolor sit amet
# 2. Consectetur adipiscing elit
# 3. Sed do eiusmod tempor
```

## HTML Output

### HTML Paragraphs

```python
html = gen.html_paragraphs(2)

# <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
# <p>Sed do eiusmod tempor incididunt ut labore.</p>
```

### HTML List

```python
html = gen.html_list(3, ordered=False)

# <ul>
#   <li>Lorem ipsum dolor sit amet</li>
#   <li>Consectetur adipiscing elit</li>
#   <li>Sed do eiusmod tempor</li>
# </ul>
```

### HTML Article

```python
html = gen.html_article(sections=2)

# <article>
#   <h1>Lorem Ipsum Dolor</h1>
#   <p>Lorem ipsum dolor sit amet...</p>
#   <h2>Consectetur Adipiscing</h2>
#   <p>Ut enim ad minim veniam...</p>
# </article>
```

## Text Styles

### Classic Lorem Ipsum

Traditional Latin placeholder text:

```python
gen = LoremGenerator(style="classic")
```

### Hipster Ipsum

Trendy, modern vocabulary:

```python
gen = LoremGenerator(style="hipster")
# "Artisan cold-pressed pour-over, sustainable raw denim..."
```

### Corporate Ipsum

Business jargon:

```python
gen = LoremGenerator(style="corporate")
# "Leverage agile frameworks to provide robust synopsis..."
```

### Tech Ipsum

Technology-focused text:

```python
gen = LoremGenerator(style="tech")
# "API endpoints serverless microservices kubernetes..."
```

## Templates

Fill templates with placeholder text:

```python
template = """
# {{title}}

{{paragraph}}

## Features

{{list:5}}

## Details

{{paragraph}}
{{paragraph}}
"""

result = gen.fill_template(template)
```

### Template Placeholders

| Placeholder | Output |
|-------------|--------|
| `{{title}}` | 3-5 word title |
| `{{heading}}` | Section heading |
| `{{paragraph}}` | Single paragraph |
| `{{sentence}}` | Single sentence |
| `{{words:N}}` | N words |
| `{{list:N}}` | N list items |
| `{{name}}` | Random name |
| `{{email}}` | Random email |
| `{{date}}` | Random date |

## Specific Word Counts

Control exact word count per paragraph:

```python
# Each paragraph will have exactly 50 words
text = gen.paragraphs(3, words_per=50)

# Generate exactly 200 words
text = gen.words(200)
```

## Example Workflows

### Mockup Text Generation

```python
gen = LoremGenerator()

# Generate blog post mockup
title = gen.title(words=6)
intro = gen.paragraphs(1, words_per=100)
body = gen.paragraphs(3, words_per=150)
conclusion = gen.paragraphs(1, words_per=75)

print(f"# {title}\n\n{intro}\n\n{body}\n\n{conclusion}")
```

### HTML Page Content

```python
gen = LoremGenerator()

html = f"""
<!DOCTYPE html>
<html>
<body>
  <header>
    <h1>{gen.title()}</h1>
  </header>
  <main>
    {gen.html_paragraphs(3)}
    <h2>Features</h2>
    {gen.html_list(5)}
    {gen.html_paragraphs(2)}
  </main>
</body>
</html>
"""
```

### Test Data Generation

```python
gen = LoremGenerator()

# Generate test articles
articles = []
for i in range(10):
    articles.append({
        "title": gen.title(),
        "excerpt": gen.sentences(2),
        "body": gen.paragraphs(5),
        "tags": gen.words(3).split()
    })
```

## Dependencies

- faker>=22.0.0 (optional, for enhanced fake data)
