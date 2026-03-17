---
name: certificate-generator
description: Batch create professional certificates with customizable templates for courses, achievements, and awards. Supports CSV input and PDF export.
---

# Certificate Generator

Create professional certificates for courses, achievements, events, and awards. Supports batch generation from CSV files with customizable templates and branding.

## Quick Start

```python
from scripts.certificate_gen import CertificateGenerator

# Single certificate
cert = CertificateGenerator()
cert.set_title("Certificate of Completion")
cert.set_recipient("John Smith")
cert.set_achievement("Python Programming Course")
cert.set_date("December 14, 2024")
cert.generate().save("certificate.pdf")

# Batch from CSV
CertificateGenerator.batch_generate(
    "students.csv",
    template="achievement",
    title="Certificate of Completion",
    achievement="Data Science Bootcamp",
    output_dir="./certificates/"
)
```

## Features

- **Professional Templates**: Modern, classic, elegant, minimal styles
- **Custom Branding**: Logo, colors, signatures
- **Batch Generation**: Create hundreds of certificates from CSV
- **Dynamic Fields**: Name, date, achievement, instructor, etc.
- **Signatures**: Text or image signatures with titles
- **Certificate IDs**: Auto-generated unique identifiers
- **Export**: PDF output, landscape or portrait

## API Reference

### Initialization

```python
cert = CertificateGenerator()

# With template
cert = CertificateGenerator(template="elegant")
```

### Certificate Content

```python
# Title
cert.set_title("Certificate of Completion")
cert.set_title("Certificate of Achievement")

# Recipient name
cert.set_recipient("Jane Doe")

# Achievement/course/event
cert.set_achievement("Advanced Python Programming")
cert.set_achievement("for outstanding performance in the 2024 Hackathon")

# Description (optional)
cert.set_description(
    "Has successfully completed the 40-hour intensive course "
    "covering advanced topics in Python programming."
)

# Date
cert.set_date("December 14, 2024")
cert.set_date_auto()  # Use today's date

# Certificate ID (auto-generated if not set)
cert.set_certificate_id("CERT-2024-001")
```

### Branding

```python
# Organization name
cert.set_organization("Acme Academy")

# Logo
cert.set_logo("logo.png")
cert.set_logo("logo.png", width=200)

# Colors
cert.set_colors(
    primary="#1e3a5f",    # Main color (title, borders)
    accent="#c9a227",     # Accent color (decorations)
    text="#333333"        # Text color
)
```

### Signatures

```python
# Text signature
cert.add_signature(
    name="Dr. Jane Smith",
    title="Program Director"
)

# Multiple signatures
cert.add_signature("John Doe", "CEO")
cert.add_signature("Jane Smith", "Head of Training")

# Image signature
cert.add_signature(
    name="Dr. Jane Smith",
    title="Program Director",
    signature_image="signature.png"
)
```

### Templates

```python
# Available templates
cert.set_template("modern")    # Clean, contemporary design
cert.set_template("classic")   # Traditional, formal design
cert.set_template("elegant")   # Decorative borders, serif fonts
cert.set_template("minimal")   # Simple, clean design
cert.set_template("academic")  # University/school style

# Orientation
cert.set_orientation("landscape")  # Default
cert.set_orientation("portrait")
```

### Generation and Export

```python
# Generate certificate
cert.generate()

# Save to PDF
cert.save("certificate.pdf")

# Get PDF bytes
pdf_bytes = cert.to_bytes()
```

## Batch Generation

### From CSV

```python
# CSV with recipient data
CertificateGenerator.batch_generate(
    csv_file="students.csv",
    template="achievement",
    title="Certificate of Completion",
    achievement="Python Fundamentals",
    organization="Code Academy",
    output_dir="./certificates/"
)
```

### CSV Format

```csv
name,date,course,certificate_id
John Smith,2024-12-14,Python 101,CERT-001
Jane Doe,2024-12-14,Python 101,CERT-002
Bob Johnson,2024-12-14,Python 101,CERT-003
```

### Programmatic Batch

```python
recipients = [
    {"name": "John Smith", "course": "Python 101"},
    {"name": "Jane Doe", "course": "Data Science"},
    {"name": "Bob Johnson", "course": "Machine Learning"}
]

for r in recipients:
    cert = CertificateGenerator(template="modern")
    cert.set_title("Certificate of Completion")
    cert.set_recipient(r["name"])
    cert.set_achievement(r["course"])
    cert.set_date_auto()
    cert.generate()
    cert.save(f"certificates/{r['name'].replace(' ', '_')}.pdf")
```

## CLI Usage

```bash
# Single certificate
python certificate_gen.py \
    --recipient "John Smith" \
    --title "Certificate of Completion" \
    --achievement "Python Course" \
    --output certificate.pdf

# With options
python certificate_gen.py \
    --recipient "Jane Doe" \
    --title "Certificate of Achievement" \
    --achievement "Excellence in Data Science" \
    --organization "Data Academy" \
    --template elegant \
    --logo logo.png \
    --output achievement.pdf

# Batch from CSV
python certificate_gen.py \
    --batch students.csv \
    --title "Certificate of Completion" \
    --achievement "Bootcamp Graduate" \
    --template modern \
    --output-dir ./certificates/
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--recipient` | Recipient name | Required |
| `--title` | Certificate title | `Certificate` |
| `--achievement` | Achievement text | - |
| `--description` | Description text | - |
| `--organization` | Organization name | - |
| `--date` | Certificate date | Today |
| `--template` | Template style | `modern` |
| `--logo` | Logo image path | - |
| `--output` | Output PDF path | `certificate.pdf` |
| `--batch` | CSV file for batch | - |
| `--output-dir` | Output directory (batch) | `./` |

## Templates

### Modern
Clean, contemporary design with:
- Sans-serif fonts
- Minimal decorations
- Bold color accents
- Professional look

### Classic
Traditional design with:
- Serif fonts
- Formal layout
- Border decorations
- Timeless elegance

### Elegant
Decorative design with:
- Ornate borders
- Script fonts for name
- Gold accents
- Premium feel

### Minimal
Simple design with:
- Clean typography
- No decorations
- Lots of white space
- Modern simplicity

### Academic
University style with:
- Seal/crest placement
- Formal typography
- Official appearance
- Traditional layout

## Examples

### Course Completion Certificate

```python
cert = CertificateGenerator(template="modern")
cert.set_title("Certificate of Completion")
cert.set_recipient("John Smith")
cert.set_achievement("Full Stack Web Development")
cert.set_description(
    "Has successfully completed the 12-week intensive program "
    "covering HTML, CSS, JavaScript, React, Node.js, and databases."
)
cert.set_organization("Tech Academy")
cert.set_logo("tech_academy_logo.png")
cert.set_date("December 14, 2024")
cert.add_signature("Sarah Johnson", "Program Director")
cert.generate().save("completion_cert.pdf")
```

### Achievement Award

```python
cert = CertificateGenerator(template="elegant")
cert.set_title("Certificate of Achievement")
cert.set_recipient("Jane Doe")
cert.set_achievement("First Place - Annual Hackathon 2024")
cert.set_organization("Innovation Labs")
cert.set_colors(primary="#1a1a2e", accent="#d4af37")
cert.add_signature("Michael Chen", "CEO")
cert.add_signature("Emily Brown", "CTO")
cert.generate().save("achievement_award.pdf")
```

### Workshop Participation

```python
cert = CertificateGenerator(template="minimal")
cert.set_title("Certificate of Participation")
cert.set_recipient("Bob Wilson")
cert.set_achievement("Machine Learning Workshop")
cert.set_description("Attended the 2-day intensive workshop on Dec 12-13, 2024")
cert.set_date_auto()
cert.generate().save("workshop_cert.pdf")
```

### Batch Employee Training

```python
# training_completed.csv
# name,department,course
# Alice,Engineering,Safety Training
# Bob,Sales,Product Training
# Carol,HR,Compliance Training

CertificateGenerator.batch_generate(
    csv_file="training_completed.csv",
    template="classic",
    title="Training Completion Certificate",
    organization="Acme Corp",
    logo="acme_logo.png",
    output_dir="./training_certs/",
    filename_pattern="{name}_{course}.pdf"
)
```

## Dependencies

```
reportlab>=4.0.0
Pillow>=10.0.0
```

## Limitations

- PDF output only (no PNG/image export)
- Pre-defined templates (no custom HTML/CSS)
- Maximum 3 signatures per certificate
- Logo should be PNG or JPEG
- English templates only (RTL languages not supported)
