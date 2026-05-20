---
name: invoice-generator
description: Generate professional PDF invoices from line items with customizable templates, tax calculations, and branding. Supports batch generation from CSV.
---

# Invoice Generator

Create professional PDF invoices with customizable templates, automatic tax calculations, and company branding. Perfect for freelancers, small businesses, and automated billing systems.

## Quick Start

```python
from scripts.invoice_gen import InvoiceGenerator

# Create a simple invoice
invoice = InvoiceGenerator()
invoice.set_company("Acme Corp", "123 Business St, City, ST 12345")
invoice.set_client("John Smith", "456 Client Ave, Town, ST 67890")
invoice.add_item("Consulting Services", 8, 150.00)
invoice.add_item("Software License", 1, 500.00)
invoice.generate().save("invoice_001.pdf")

# From dictionary
data = {
    'invoice_number': 'INV-2024-001',
    'company': {'name': 'My Company', 'address': '123 Main St'},
    'client': {'name': 'Client Inc', 'address': '456 Oak Ave'},
    'items': [
        {'description': 'Web Design', 'quantity': 1, 'rate': 2500},
        {'description': 'Hosting (Annual)', 'quantity': 1, 'rate': 300}
    ]
}
invoice = InvoiceGenerator.from_dict(data)
invoice.generate().save("invoice.pdf")
```

## Features

- **Professional Templates**: Clean, modern invoice designs
- **Custom Branding**: Logo, colors, fonts
- **Tax Calculations**: Multiple tax rates, compound taxes
- **Discounts**: Percentage or fixed amount discounts
- **Payment Terms**: Due dates, payment instructions, bank details
- **Multi-Currency**: Support for various currency symbols
- **Batch Generation**: Create multiple invoices from CSV
- **Export**: PDF output with optional preview

## API Reference

### Initialization

```python
invoice = InvoiceGenerator()

# From dictionary
invoice = InvoiceGenerator.from_dict(data)

# From CSV (batch)
invoices = InvoiceGenerator.from_csv("invoices.csv")
```

### Company Information

```python
# Basic company info
invoice.set_company(
    name="Acme Corporation",
    address="123 Business Street\nCity, State 12345"
)

# Full company details
invoice.set_company(
    name="Acme Corporation",
    address="123 Business Street\nCity, State 12345",
    email="billing@acme.com",
    phone="+1 (555) 123-4567",
    website="www.acme.com",
    tax_id="12-3456789"
)

# Add logo
invoice.set_logo("logo.png")
invoice.set_logo("logo.png", width=150)  # Specify width in pixels
```

### Client Information

```python
# Basic client info
invoice.set_client(
    name="John Smith",
    address="456 Client Avenue\nTown, State 67890"
)

# Full client details
invoice.set_client(
    name="John Smith",
    company="Smith Enterprises",
    address="456 Client Avenue\nTown, State 67890",
    email="john@smithent.com"
)
```

### Invoice Details

```python
# Invoice number and dates
invoice.set_invoice_number("INV-2024-001")
invoice.set_date("2024-01-15")  # Invoice date
invoice.set_due_date("2024-02-14")  # Due date

# Or use days from invoice date
invoice.set_due_days(30)  # Due in 30 days

# Currency
invoice.set_currency("USD")  # $
invoice.set_currency("EUR")  # €
invoice.set_currency("GBP")  # £
invoice.set_currency("$", symbol_only=True)  # Custom symbol
```

### Line Items

```python
# Add items
invoice.add_item(
    description="Consulting Services",
    quantity=8,
    rate=150.00
)

# With unit
invoice.add_item("Development", 40, 125.00, unit="hours")

# With item-level discount
invoice.add_item("Product", 10, 50.00, discount=10)  # 10% discount

# From list
items = [
    {"description": "Item 1", "quantity": 2, "rate": 100},
    {"description": "Item 2", "quantity": 1, "rate": 250}
]
invoice.add_items(items)
```

### Taxes and Discounts

```python
# Add tax
invoice.add_tax("Sales Tax", 8.25)  # 8.25%
invoice.add_tax("State Tax", 5.0)

# Compound tax (applied after other taxes)
invoice.add_tax("GST", 10.0, compound=True)

# Discount on subtotal
invoice.set_discount(10)  # 10% off
invoice.set_discount(50, is_percentage=False)  # $50 off
```

### Payment Information

```python
# Payment terms
invoice.set_payment_terms("Net 30")

# Payment instructions
invoice.set_payment_instructions("""
Payment Methods:
- Bank Transfer: Account #12345, Routing #67890
- PayPal: payments@acme.com
- Check payable to: Acme Corporation
""")

# Bank details
invoice.set_bank_details(
    bank_name="First National Bank",
    account_name="Acme Corporation",
    account_number="1234567890",
    routing_number="987654321",
    swift_code="FNBKUS12"
)
```

### Notes and Terms

```python
# Notes (appears on invoice)
invoice.set_notes("Thank you for your business!")

# Terms and conditions
invoice.set_terms("""
1. Payment due within 30 days
2. Late payments subject to 1.5% monthly interest
3. All sales are final
""")
```

### Styling

```python
# Color theme
invoice.set_colors(
    primary="#2563eb",    # Headers, accent
    secondary="#64748b",  # Secondary text
    background="#f8fafc"  # Background
)

# Template style
invoice.set_template("modern")    # Default
invoice.set_template("classic")   # Traditional look
invoice.set_template("minimal")   # Clean, minimal

# Font
invoice.set_font("Helvetica")  # Default
invoice.set_font("Times")
```

### Generation and Export

```python
# Generate invoice
invoice.generate()

# Save to PDF
invoice.save("invoice.pdf")

# Save with custom filename pattern
invoice.save_as("INV-{number}-{client}.pdf")

# Get PDF bytes (for email attachment, etc.)
pdf_bytes = invoice.to_bytes()
```

## Data Formats

### Dictionary Format

```python
data = {
    'invoice_number': 'INV-2024-001',
    'date': '2024-01-15',
    'due_date': '2024-02-14',
    'currency': 'USD',

    'company': {
        'name': 'Acme Corporation',
        'address': '123 Business St\nCity, ST 12345',
        'email': 'billing@acme.com',
        'phone': '+1 (555) 123-4567',
        'logo': 'logo.png'  # Optional
    },

    'client': {
        'name': 'John Smith',
        'company': 'Smith Enterprises',
        'address': '456 Client Ave\nTown, ST 67890',
        'email': 'john@smithent.com'
    },

    'items': [
        {'description': 'Consulting', 'quantity': 8, 'rate': 150, 'unit': 'hours'},
        {'description': 'Software License', 'quantity': 1, 'rate': 500}
    ],

    'taxes': [
        {'name': 'Sales Tax', 'rate': 8.25}
    ],

    'discount': 10,  # Optional: percentage
    'notes': 'Thank you for your business!',
    'payment_terms': 'Net 30'
}
```

### CSV Format for Batch

```csv
invoice_number,date,due_date,client_name,client_address,item_description,quantity,rate,tax_rate
INV-001,2024-01-15,2024-02-14,John Smith,123 Main St,Consulting,8,150,8.25
INV-001,2024-01-15,2024-02-14,John Smith,123 Main St,Software,1,500,8.25
INV-002,2024-01-16,2024-02-15,Jane Doe,456 Oak Ave,Design,1,2000,8.25
```

## CLI Usage

```bash
# Generate from JSON
python invoice_gen.py --input invoice.json --output invoice.pdf

# Batch from CSV
python invoice_gen.py --batch invoices.csv --output-dir ./invoices/

# Quick invoice
python invoice_gen.py --quick \
    --company "My Company" \
    --client "Client Name" \
    --items "Service,1,500;Product,2,100" \
    --output invoice.pdf

# With options
python invoice_gen.py --input data.json \
    --template modern \
    --currency EUR \
    --output invoice.pdf
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input` | Input JSON file | - |
| `--batch` | Batch CSV file | - |
| `--output` | Output PDF path | `invoice.pdf` |
| `--output-dir` | Output directory (batch) | `./` |
| `--template` | Template style | `modern` |
| `--currency` | Currency code | `USD` |
| `--logo` | Logo image path | - |
| `--quick` | Quick mode with inline data | - |

## Examples

### Freelancer Invoice

```python
invoice = InvoiceGenerator()

invoice.set_company(
    name="Jane Developer",
    address="123 Freelance Lane\nRemote, WFH 00000",
    email="jane@developer.com"
)

invoice.set_client(
    name="Startup Inc",
    address="456 Venture Blvd\nSilicon Valley, CA 94000"
)

invoice.set_invoice_number("2024-001")
invoice.add_item("Frontend Development", 40, 125, unit="hours")
invoice.add_item("Backend Development", 32, 150, unit="hours")
invoice.add_item("Code Review", 8, 100, unit="hours")

invoice.set_payment_terms("Net 15")
invoice.set_notes("Thank you for the opportunity!")

invoice.generate().save("freelance_invoice.pdf")
```

### Business Invoice with Taxes

```python
invoice = InvoiceGenerator()

invoice.set_company("Acme Corp", "123 Business St, City, ST 12345")
invoice.set_logo("acme_logo.png")
invoice.set_client("Big Client LLC", "456 Corporate Ave, Metro, ST 67890")

invoice.add_item("Enterprise License", 1, 5000)
invoice.add_item("Implementation", 20, 200, unit="hours")
invoice.add_item("Training", 2, 500, unit="sessions")
invoice.add_item("Support (Annual)", 1, 1200)

invoice.add_tax("State Tax", 6.0)
invoice.add_tax("County Tax", 2.25)

invoice.set_discount(5)  # 5% volume discount

invoice.set_bank_details(
    bank_name="Business Bank",
    account_number="9876543210",
    routing_number="123456789"
)

invoice.generate().save("business_invoice.pdf")
```

### Batch Invoice Generation

```python
# From CSV
invoices = InvoiceGenerator.from_csv("monthly_invoices.csv")

for inv in invoices:
    inv.set_company("My Company", "123 Main St")
    inv.set_logo("logo.png")
    inv.generate()
    inv.save(f"invoices/{inv.invoice_number}.pdf")

# Or with batch save
InvoiceGenerator.batch_generate(
    "invoices.csv",
    output_dir="./invoices/",
    company_name="My Company",
    company_address="123 Main St",
    logo="logo.png"
)
```

## Dependencies

```
reportlab>=4.0.0
Pillow>=10.0.0
```

## Limitations

- Logo images should be PNG or JPEG
- Maximum ~50 line items per page (auto-pagination for more)
- PDF only (no HTML or DOCX export)
- Single currency per invoice
