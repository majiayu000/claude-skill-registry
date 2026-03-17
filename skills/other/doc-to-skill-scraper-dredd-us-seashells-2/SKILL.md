---
name: doc-to-skill-scraper
description: Scrape external documentation (API references, library docs, protocol specifications) and generate Claude Agent Skills in SKILL.md format. Use when creating skills from documentation, integrating third-party knowledge, or building domain-specific skills. Parses HTML/Markdown, extracts structure, generates proper frontmatter and instructions. Triggers on "scrape documentation", "docs to skill", "generate skill from docs", "API documentation to skill".
---

# Documentation to Skill Scraper

## Purpose

Meta-skill for converting external documentation into Claude Agent Skills with proper YAML frontmatter and structured instructions following the official specification.

## When to Use

- Creating skills from API documentation
- Integrating third-party library knowledge
- Building domain-specific skills from protocols
- Converting documentation to reusable skills
- Continual learning from new documentation

## Core Instructions

### Step 1: Parse Documentation

```python
from bs4 import BeautifulSoup
import requests
import yaml

def scrape_documentation(url):
    """
    Scrape and parse documentation
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract structure
    title = soup.find('h1').text if soup.find('h1') else 'Unknown'
    sections = []

    for heading in soup.find_all(['h1', 'h2', 'h3']):
        sections.append({
            'level': heading.name,
            'text': heading.text,
            'content': extract_content_after(heading)
        })

    return {
        'title': title,
        'url': url,
        'sections': sections
    }
```

### Step 2: Extract Key Information

```python
def extract_skill_info(doc_data):
    """
    Extract skill components from documentation
    """
    # Generate skill name
    name = doc_data['title'].lower().replace(' ', '-')

    # Extract purpose from first paragraph
    purpose = doc_data['sections'][0]['content'] if doc_data['sections'] else ''

    # Extract examples (look for code blocks)
    examples = extract_code_blocks(doc_data)

    # Extract API methods or key functions
    methods = extract_api_methods(doc_data)

    return {
        'name': name,
        'purpose': purpose,
        'examples': examples,
        'methods': methods
    }
```

### Step 3: Generate SKILL.md

```python
def generate_skill_md(skill_info):
    """
    Generate SKILL.md content
    """
    # Build description
    description = f"{skill_info['purpose']} Use when {infer_use_cases(skill_info)}. " \
                  f"Triggers on {infer_triggers(skill_info)}."

    # Ensure description is 200-1024 chars
    if len(description) > 1024:
        description = description[:1021] + "..."
    elif len(description) < 200:
        description = pad_description(description, skill_info)

    # Generate frontmatter
    frontmatter = {
        'name': skill_info['name'],
        'description': description
    }

    # Generate body
    body = f"""# {skill_info['title']}

## Purpose

{skill_info['purpose']}

## When to Use

{generate_when_to_use(skill_info)}

## Core Instructions

{generate_instructions(skill_info)}

## Examples

{format_examples(skill_info['examples'])}

## Dependencies

{infer_dependencies(skill_info)}

## Version

v1.0.0
"""

    # Combine
    yaml_str = yaml.dump(frontmatter, default_flow_style=False)
    return f"---\n{yaml_str}---\n\n{body}"
```

### Step 4: Validate Generated Skill

```python
def validate_skill(skill_md_content):
    """
    Validate generated SKILL.md
    """
    # Parse frontmatter
    parts = skill_md_content.split('---\n')
    if len(parts) < 3:
        raise ValueError("Invalid frontmatter structure")

    frontmatter = yaml.safe_load(parts[1])

    # Check required fields
    assert 'name' in frontmatter, "Missing 'name' field"
    assert 'description' in frontmatter, "Missing 'description' field"

    # Check description length
    desc_len = len(frontmatter['description'])
    assert 200 <= desc_len <= 1024, f"Description must be 200-1024 chars (got {desc_len})"

    # Check name format
    assert frontmatter['name'].islower(), "Name must be lowercase"
    assert '-' in frontmatter['name'] or '_' not in frontmatter['name'], "Use hyphens, not underscores"

    return True
```

## Example: Stripe API to Skill

### Input Documentation URL
```
https://stripe.com/docs/api/payment_intents
```

### Scraping Process

1. **Parse HTML**: Extract title, sections, code examples
2. **Extract Info**:
   - Name: `stripe-payment-intents`
   - Purpose: "Create and manage PaymentIntents for Stripe payments"
   - Methods: `create`, `retrieve`, `confirm`, `cancel`
   - Examples: Code snippets from docs

3. **Generate SKILL.md**:
```markdown
---
name: stripe-payment-intents
description: Create and manage Stripe PaymentIntents for processing payments with 3D Secure support, automatic payment methods, and webhook integration. Use when building payment flows, processing credit cards, handling payment confirmations, or integrating Stripe checkout. Supports one-time and recurring payments. Triggers on "Stripe payment", "PaymentIntent", "process payment", "Stripe checkout", "payment processing".
---

# Stripe Payment Intents

## Purpose

Create and manage PaymentIntents for Stripe payment processing with support for 3D Secure, multiple payment methods, and webhook confirmations.

## When to Use

- Building payment checkout flows
- Processing credit card payments
- Handling payment confirmations
- Supporting 3D Secure authentication
- Managing payment lifecycle

## Core Instructions

### Create Payment Intent

```python
import stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Create payment intent
intent = stripe.PaymentIntent.create(
    amount=2000,  # Amount in cents
    currency='usd',
    payment_method_types=['card'],
    metadata={'order_id': '12345'}
)
```

### Confirm Payment

```python
# Confirm payment with payment method
stripe.PaymentIntent.confirm(
    intent.id,
    payment_method='pm_card_visa'
)
```

### Handle Webhooks

```python
# Verify webhook signature
payload = request.get_data()
sig_header = request.headers.get('Stripe-Signature')

event = stripe.Webhook.construct_event(
    payload, sig_header, webhook_secret
)

if event['type'] == 'payment_intent.succeeded':
    payment_intent = event['data']['object']
    # Handle successful payment
```

## Dependencies

- Python 3.7+
- stripe library
- Environment variable: STRIPE_SECRET_KEY

## Version

v1.0.0
```

## Best Practices

### Ethics and Respect
- **Respect robots.txt**: Check before scraping
- **Cache locally**: Don't repeatedly scrape same content
- **Rate limiting**: Add delays between requests
- **Attribution**: Credit original documentation source

### Quality
- **Validate generated skills**: Run through validation checks
- **Test in sandbox**: Test generated skill before using
- **Manual review**: Always review generated content
- **Iterate**: Refine based on actual usage

### Description Generation
- Extract key terms from documentation
- Include file types, domain terms, action verbs
- Add specific use cases from examples
- Ensure 200-1024 character length

## Workflow

```bash
# 1. Scrape documentation
python scrape_docs.py https://api.example.com/docs

# 2. Generate SKILL.md
python generate_skill.py scraped_data.json

# 3. Validate
python validate_skill.py generated_skill.md

# 4. Test
# Create .claude/skills/new-skill/SKILL.md
# Test with realistic prompt

# 5. Iterate
# Refine based on testing
```

## Supporting Files

Generated skills can include:
- **examples/**: Usage examples from documentation
- **templates/**: API request templates
- **scripts/**: Helper scripts for common operations

## Dependencies

- Python 3.8+
- beautifulsoup4 - HTML parsing
- requests - HTTP requests
- pyyaml - YAML generation
- Optional: markdown - Markdown parsing

## Version

v1.0.0 (2025-10-23)

