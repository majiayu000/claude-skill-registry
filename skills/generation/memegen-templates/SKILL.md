---
name: memegen-templates
description: Generate classic meme images using 207+ templates from memegen.link. Use when creating memes with popular formats like Drake, Distracted Boyfriend, This is Fine, or any classic internet meme template.
allowed-tools: Read, Bash(python:*)
model: claude-sonnet-4-20250514
---

# Memegen Templates

Generate classic internet memes using 207+ popular meme templates from [memegen.link](https://memegen.link).

## Overview

This Skill provides access to all classic meme formats:
- **207+ meme templates** (Drake, Distracted Boyfriend, Expanding Brain, etc.)
- **FREE API** - No API key required
- **URL-based generation** - Simple and fast
- **Custom text** - Top/bottom or multi-line text
- **Image overlays** - Optional background images

## Quick Start

### Basic Usage

```python
from src.memegen_api import MemegenAPI

api = MemegenAPI()

# Generate Drake meme
meme_url = api.generate_meme(
    template="drake",
    top_text="Manually creating memes",
    bottom_text="Using memegen templates"
)

print(f"Meme URL: {meme_url}")
# https://api.memegen.link/images/drake/Manually_creating_memes/Using_memegen_templates.png
```

### Download Meme

```python
# Generate and download
image = api.generate_and_download(
    template="drake",
    top_text="Old way",
    bottom_text="New way"
)

# Save to file
image.save("my_meme.png")
```

## Popular Templates

### Top 20 Most Used

| Template | Name | Format |
|----------|------|--------|
| `drake` | Drake Hotline Bling | Top = No, Bottom = Yes |
| `distracted` | Distracted Boyfriend | Left/Center/Right text |
| `iw` | Inhaling Seagull | Top/Bottom |
| `ants` | Do You Want Ants? | Top/Bottom |
| `afraid` | Afraid to Ask Andy | Top/Bottom |
| `fine` | This is Fine | Top/Bottom |
| `expanding` | Expanding Brain | Multi-level |
| `buzz` | Buzz and Woody | Left/Right |
| `both` | Why Not Both? | Top/Bottom |
| `captain` | Captain Phillips | Top/Bottom |
| `wonka` | Condescending Wonka | Top/Bottom |
| `xy` | X, X Everywhere | Top/Bottom |
| `awesome` | Socially Awesome Penguin | Top/Bottom |
| `awkward` | Socially Awkward Penguin | Top/Bottom |
| `ive` | I Should Buy a Boat | Top/Bottom |
| `disastergirl` | Disaster Girl | Top/Bottom |
| `odi` | One Does Not Simply | Top/Bottom |
| `blb` | Bad Luck Brian | Top/Bottom |
| `yuno` | Y U No | Top/Bottom |
| `success` | Success Kid | Top/Bottom |

**Full list**: See [TEMPLATE_LIST.md](TEMPLATE_LIST.md) for all 207 templates

## Usage Examples

### Example 1: Drake Meme

```python
api = MemegenAPI()

# Classic Drake format
meme = api.generate_meme(
    template="drake",
    top_text="Complicated setup",
    bottom_text="One-line API call"
)
```

**Output**:
```
Drake rejecting: "Complicated setup"
Drake approving: "One-line API call"
```

---

### Example 2: Distracted Boyfriend

```python
# Three-part meme
meme = api.generate_meme(
    template="distracted",
    texts=["Boyfriend", "Girlfriend", "Other Girl"]
)
# Texts: [Left (boyfriend), Center (girlfriend), Right (other girl)]
```

---

### Example 3: Expanding Brain

```python
# Multi-level intelligence meme
meme = api.generate_meme(
    template="expanding",
    texts=[
        "Small brain idea",
        "Medium brain idea",
        "Big brain idea",
        "Galaxy brain idea"
    ]
)
```

---

### Example 4: This is Fine

```python
# Classic "This is Fine" dog
meme = api.generate_meme(
    template="fine",
    top_text="Everything is fine",
    bottom_text="*server is on fire*"
)
```

---

### Example 5: Custom Styling

```python
# With custom styling
meme = api.generate_meme(
    template="drake",
    top_text="Normal memes",
    bottom_text="Customized memes",
    style={
        "font": "impact",
        "color": "white",
        "stroke": "black"
    }
)
```

## Advanced Features

### 1. Background Images

```python
# Use custom background image
meme = api.generate_with_background(
    template="drake",
    top_text="Stock templates",
    bottom_text="Custom backgrounds",
    background_url="https://example.com/custom-bg.jpg"
)
```

### 2. Multi-Line Text

```python
# Text with line breaks
meme = api.generate_meme(
    template="drake",
    top_text="Single_line_text",
    bottom_text="Multi~nline~ntext"  # ~n = newline
)
```

### 3. Special Characters

```python
# Handle special characters
meme = api.generate_meme(
    template="drake",
    top_text="Text with spaces",
    bottom_text="Text_with_underscores"
)
# Spaces → underscores in URL
# Use ~s for literal spaces
```

### 4. Batch Generation

```python
# Generate multiple memes
templates = ["drake", "distracted", "fine"]
texts = [
    ("Option A", "Option B"),
    ("Thing 1", "Thing 2", "Thing 3"),
    ("Before", "After")
]

memes = []
for template, text in zip(templates, texts):
    meme = api.generate_meme(template=template, texts=text)
    memes.append(meme)
```

## Template Categories

### Advice Animals
- `insanity` - Insanity Wolf
- `success` - Success Kid
- `awkward` - Socially Awkward Penguin
- `awesome` - Socially Awesome Penguin
- `blb` - Bad Luck Brian
- `fry` - Futurama Fry
- `scumbag` - Scumbag Steve

### Reaction Memes
- `drake` - Drake Hotline Bling
- `distracted` - Distracted Boyfriend
- `buzz` - Buzz and Woody
- `both` - Why Not Both?
- `ants` - Do You Want Ants?
- `fine` - This is Fine

### Text-Based
- `expanding` - Expanding Brain
- `jetpack` - Jetpack Meme
- `troll` - Troll Face
- `yuno` - Y U No
- `od` - Overly Attached Girlfriend

### Movie/TV
- `wonka` - Condescending Wonka
- `morpheus` - Matrix Morpheus
- `captain` - Captain Phillips
- `trek` - Star Trek
- `mini` - Austin Powers Mini-Me

## API Reference

### MemegenAPI Class

```python
class MemegenAPI:
    def generate_meme(
        self,
        template: str,
        top_text: str = "",
        bottom_text: str = "",
        texts: list = None,
        style: dict = None
    ) -> str:
        """
        Generate meme URL.

        Args:
            template: Template name (e.g., "drake")
            top_text: Top text (optional)
            bottom_text: Bottom text (optional)
            texts: List of texts for multi-part memes
            style: Custom styling options

        Returns:
            URL to generated meme image
        """

    def generate_and_download(self, ...) -> PIL.Image:
        """Generate meme and download as PIL Image"""

    def list_templates(self) -> list:
        """List all available templates"""

    def get_template_info(self, template: str) -> dict:
        """Get template metadata"""
```

## Common Use Cases

### 1. Social Media Posts

```python
# Generate for Twitter/Instagram
meme = api.generate_and_download(
    template="drake",
    top_text="Boring posts",
    bottom_text="Meme posts"
)
meme.save("social_media_post.png")
```

### 2. Presentation Slides

```python
# Add humor to presentations
meme = api.generate_meme(
    template="expanding",
    texts=[
        "Basic approach",
        "Optimized approach",
        "Over-engineered approach",
        "Actually using memegen.link"
    ]
)
```

### 3. Team Communication

```python
# Internal team memes
meme = api.generate_meme(
    template="fine",
    top_text="Production is down",
    bottom_text="This is fine"
)
```

### 4. Content Creation

```python
# Blog posts, videos, etc.
meme = api.generate_meme(
    template="distracted",
    texts=["Old method", "Current workflow", "New shiny tool"]
)
```

## Text Formatting

### Special Characters

| Character | Encoding | Example |
|-----------|----------|---------|
| Space | `_` or `~s` | `Hello_World` |
| Newline | `~n` | `Line1~nLine2` |
| Underscore | `__` | `Snake__case` |
| Dash | `-` or `~-` | `Hyphen-ated` |
| Question | `~q` | `Why~q` |
| Percent | `~p` | `100~p` |
| Hash | `~h` | `~htag` |
| Slash | `~f` | `and~for` |

### Examples

```python
# Multi-line text
api.generate_meme(
    template="drake",
    top_text="Single line",
    bottom_text="Line 1~nLine 2~nLine 3"
)

# Special characters
api.generate_meme(
    template="drake",
    top_text="100~p normal",
    bottom_text="200~p meme power"
)
```

## Error Handling

```python
try:
    meme = api.generate_meme(
        template="invalid_template",
        top_text="Test"
    )
except ValueError as e:
    print(f"Invalid template: {e}")

try:
    meme = api.generate_meme(
        template="drake",
        top_text="",  # Empty text
        bottom_text=""
    )
except ValueError as e:
    print(f"Invalid text: {e}")
```

## Integration Examples

### With Lark Bot

```python
# In Lark bot command
def handle_memegen_command(template, top, bottom):
    api = MemegenAPI()
    image = api.generate_and_download(
        template=template,
        top_text=top,
        bottom_text=bottom
    )
    upload_to_lark(image)
```

### With Twitter Bot

```python
# Generate and post to Twitter
api = MemegenAPI()
meme = api.generate_and_download("drake", "Old way", "New way")
twitter_client.post_with_image(
    text="Choose wisely!",
    image=meme
)
```

### With Milady Generator

```python
# Combine with Milady memes
from skills.milady_meme_generator.src.meme_generator_v2 import MemeGeneratorV2

# Generate Milady
milady_gen = MemeGeneratorV2()
milady_img = milady_gen.generate_meme(nft_id=5050)

# Generate classic meme
memegen_api = MemegenAPI()
classic_meme = memegen_api.generate_and_download("drake", "NFTs", "Milady NFTs")

# Combine or use separately
```

## Tips & Best Practices

1. **Keep text short** - Max 2-3 words per line works best
2. **Use appropriate templates** - Match format to message
3. **Test special characters** - Preview before sharing
4. **Cache downloads** - Save bandwidth on repeated use
5. **Batch process** - Generate multiple at once for efficiency

## Troubleshooting

**Template not found:**
```python
# Check available templates
templates = api.list_templates()
print(templates)
```

**Image not loading:**
```python
# Use download instead of URL
image = api.generate_and_download(...)  # More reliable
```

**Text formatting issues:**
```python
# Use encoding helper
text = api.encode_text("Hello, World!")  # Handles special chars
```

## Related Skills

- [milady-meme-generator](../milady-meme-generator/SKILL.md) - Milady NFT memes
- [lark-bot-integration](../lark-bot-integration/SKILL.md) - Use in Lark bot

---

**Cost:** FREE (memegen.link is a free service)

**API Docs:** https://memegen.link/
