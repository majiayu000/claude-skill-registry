---
name: word-cloud-generator
description: Generate styled word clouds from text with custom shapes, colors, fonts, and stopword filtering. Supports PNG/SVG export and frequency dictionaries.
---

# Word Cloud Generator

Create visually appealing word clouds from text, files, or word frequency dictionaries. Customize shapes, colors, fonts, and export to multiple formats.

## Quick Start

```python
from scripts.wordcloud_gen import WordCloudGenerator

# From text
wc = WordCloudGenerator("Python is amazing. Python is powerful. Code is fun.")
wc.generate().save("cloud.png")

# From file
wc = WordCloudGenerator.from_file("article.txt")
wc.colors("plasma").max_words(100).generate().save("cloud.png")

# From frequency dict
frequencies = {"python": 50, "code": 30, "data": 25, "analysis": 20}
wc = WordCloudGenerator(frequencies=frequencies)
wc.shape("circle").generate().save("cloud.png")
```

## Features

- **Multiple Input Sources**: Raw text, text files, or word frequency dictionaries
- **Shape Options**: Rectangle, circle, or custom mask images
- **Color Schemes**: 20+ matplotlib colormaps or custom color lists
- **Font Selection**: Use system fonts or custom font files
- **Stopword Filtering**: Built-in English stopwords + custom additions
- **Export Formats**: PNG, SVG

## API Reference

### Initialization

```python
# From text string
wc = WordCloudGenerator("Your text here")

# From frequency dictionary
wc = WordCloudGenerator(frequencies={"word": count, ...})

# From file
wc = WordCloudGenerator.from_file("path/to/file.txt")
```

### Configuration Methods

All methods return `self` for chaining.

```python
# Shape options
wc.shape("rectangle")           # Default rectangle
wc.shape("circle")              # Circular cloud
wc.shape(mask="logo.png")       # Custom shape from image

# Color schemes (matplotlib colormaps)
wc.colors("viridis")            # Default
wc.colors("plasma")             # Purple-yellow gradient
wc.colors("coolwarm")           # Blue-red diverging
wc.colors("Set2")               # Categorical colors
wc.colors(custom=["#FF0000", "#00FF00", "#0000FF"])  # Custom colors

# Font settings
wc.font("/path/to/font.ttf")    # Custom font file

# Stopwords
wc.stopwords(use_default=True)                    # Use built-in stopwords
wc.stopwords(words=["custom", "words"])           # Add custom stopwords
wc.stopwords(words=["the", "and"], use_default=False)  # Only custom

# Word limits
wc.max_words(200)               # Maximum words to display (default: 200)
wc.min_word_length(3)           # Minimum word length (default: 1)

# Size
wc.size(800, 400)               # Width x Height in pixels
```

### Generation and Export

```python
# Generate the word cloud
wc.generate()

# Save to file
wc.save("output.png")           # PNG format
wc.save("output.svg")           # SVG format (auto-detected)
wc.save("output.png", format="png")  # Explicit format

# Display (matplotlib)
wc.show()

# Get word frequencies
freqs = wc.get_frequencies()    # Returns dict of word: frequency
```

## Color Schemes

### Popular Colormaps

| Name | Description |
|------|-------------|
| `viridis` | Blue-green-yellow (default) |
| `plasma` | Purple-orange-yellow |
| `inferno` | Black-red-yellow |
| `magma` | Black-purple-white |
| `cividis` | Blue-yellow (colorblind-safe) |
| `coolwarm` | Blue-white-red |
| `RdYlBu` | Red-yellow-blue |
| `Spectral` | Rainbow spectrum |
| `Set1` | Bold categorical |
| `Set2` | Muted categorical |
| `Pastel1` | Soft categorical |
| `Dark2` | Dark categorical |

### Custom Colors

```python
# Hex colors
wc.colors(custom=["#1a1a2e", "#16213e", "#0f3460", "#e94560"])

# Named colors
wc.colors(custom=["navy", "royalblue", "cornflowerblue", "lightsteelblue"])
```

## Shape Masks

### Built-in Shapes

```python
wc.shape("rectangle")  # Default
wc.shape("circle")     # Circular
wc.shape("square")     # Square
```

### Custom Mask Images

Use any image where **white areas are filled** with words:

```python
# Use logo or shape image as mask
wc.shape(mask="company_logo.png")
wc.shape(mask="heart.png")
wc.shape(mask="map_outline.png")
```

**Mask Image Requirements:**
- White (#FFFFFF) areas will be filled with words
- Black/dark areas will be empty
- Works best with high-contrast images
- Recommended: 800x800 pixels or larger

## CLI Usage

```bash
# Basic usage
python wordcloud_gen.py --text "Your text here" --output cloud.png

# From file
python wordcloud_gen.py --file article.txt --output cloud.png

# With options
python wordcloud_gen.py --file data.txt \
    --shape circle \
    --colors plasma \
    --max-words 150 \
    --output cloud.png

# Custom mask
python wordcloud_gen.py --file speech.txt \
    --mask logo.png \
    --colors Set2 \
    --output branded_cloud.png

# SVG output
python wordcloud_gen.py --text "Hello World" --output cloud.svg
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--text` | Input text string | - |
| `--file` | Input text file path | - |
| `--output` | Output file path | `wordcloud.png` |
| `--shape` | Shape: rectangle, circle, square | `rectangle` |
| `--mask` | Custom mask image path | - |
| `--colors` | Colormap name | `viridis` |
| `--max-words` | Maximum words | 200 |
| `--min-length` | Minimum word length | 1 |
| `--width` | Image width | 800 |
| `--height` | Image height | 400 |
| `--font` | Custom font file | - |
| `--no-stopwords` | Disable stopword filtering | False |
| `--stopwords` | Additional stopwords (comma-separated) | - |

## Examples

### Basic Word Cloud

```python
text = """
Python is a versatile programming language. Python is used for web development,
data science, machine learning, and automation. Python's simplicity makes it
perfect for beginners while its power serves experts.
"""

wc = WordCloudGenerator(text)
wc.colors("plasma").generate().save("python_cloud.png")
```

### Frequency-Based Cloud

```python
# Word frequencies from analysis
tech_terms = {
    "Python": 100,
    "JavaScript": 85,
    "Machine Learning": 70,
    "API": 65,
    "Database": 60,
    "Cloud": 55,
    "DevOps": 45,
    "Kubernetes": 40,
    "Docker": 38,
    "React": 35
}

wc = WordCloudGenerator(frequencies=tech_terms)
wc.shape("circle").colors("Set2").generate().save("tech_cloud.png")
```

### Branded Word Cloud

```python
# Use company logo as mask
wc = WordCloudGenerator.from_file("company_values.txt")
wc.shape(mask="logo_white_bg.png")
wc.colors(custom=["#003366", "#0066cc", "#3399ff"])
wc.font("/fonts/OpenSans-Bold.ttf")
wc.generate().save("branded_cloud.png")
```

### Article Analysis

```python
# Analyze article removing common words
wc = WordCloudGenerator.from_file("news_article.txt")
wc.stopwords(words=["said", "according", "reported"])  # Add domain stopwords
wc.min_word_length(4)
wc.max_words(100)
wc.colors("RdYlBu")
wc.generate().save("article_themes.png")

# Get top words
top_words = wc.get_frequencies()
for word, freq in list(top_words.items())[:10]:
    print(f"{word}: {freq}")
```

## Dependencies

```
wordcloud>=1.9.0
matplotlib>=3.7.0
Pillow>=10.0.0
numpy>=1.24.0
```

## Limitations

- SVG export converts from PNG (not native vector)
- Very large texts may be slow to process
- Custom fonts must be TrueType (.ttf) or OpenType (.otf)
- Mask images work best with simple, high-contrast shapes
