---
name: docx-templates
description: Template-based Word document generation using Jinja2 syntax. Create reports, contracts, and documents with loops, conditionals, tables, and mail merge capabilities.
version: 1.0.0
author: workspace-hub
category: office-docs
type: skill
trigger: manual
auto_execute: false
capabilities:
  - jinja2_templates
  - loop_rendering
  - conditional_content
  - table_generation
  - image_insertion
  - mail_merge
  - batch_generation
  - nested_data_support
tools:
  - Read
  - Write
  - Bash
  - Grep
tags: [docx, templates, jinja2, word, document-generation, mail-merge, reports, automation]
platforms: [python]
related_skills:
  - python-docx
  - openpyxl
  - pypdf
---

# Docx-Templates Skill

> Generate Word documents from templates using Jinja2 syntax. Create professional reports, contracts, and documents with dynamic content, loops, conditionals, and tables.

## Quick Start

```bash
# Install docxtpl
pip install docxtpl

# Install with image support
pip install docxtpl Pillow

# For Excel data sources
pip install docxtpl openpyxl pandas

# Verify installation
python -c "from docxtpl import DocxTemplate; print('docxtpl ready!')"
```

## When to Use This Skill

**USE when:**
- Generating documents from templates with dynamic data
- Creating mail merge documents from data sources
- Building reports with loops and conditional sections
- Need to maintain consistent formatting across generated documents
- Generating contracts, invoices, letters from templates
- Processing batch document generation from databases or spreadsheets
- Templates need professional formatting preserved
- Non-technical users maintain template design

**DON'T USE when:**
- Building documents programmatically from scratch (use python-docx)
- Need complex document manipulation beyond template filling
- PDF output is the final format (generate docx then convert)
- Templates require complex macros or VBA
- Real-time collaborative editing needed

## Prerequisites

```bash
# Core installation
pip install docxtpl>=0.16.0

# For image handling
pip install docxtpl Pillow>=9.0.0

# For data processing
pip install docxtpl pandas>=2.0.0 openpyxl>=3.1.0

# For database connections
pip install docxtpl sqlalchemy psycopg2-binary

# All dependencies
pip install docxtpl Pillow pandas openpyxl sqlalchemy
```

### Verify Installation

```python
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm, Inches

print("docxtpl installed successfully!")

# Quick test
# template = DocxTemplate("template.docx")
# context = {"name": "World"}
# template.render(context)
# template.save("output.docx")
```

## Core Capabilities

### 1. Basic Template Rendering

**Simple Variable Substitution:**
```python
"""
Basic template rendering with variable substitution.
"""
from docxtpl import DocxTemplate
from typing import Dict, Any
from pathlib import Path

def render_simple_template(
    template_path: str,
    output_path: str,
    context: Dict[str, Any]
) -> None:
    """
    Render a template with simple variable substitution.

    Args:
        template_path: Path to .docx template
        output_path: Path for output document
        context: Dictionary of values to substitute

    Template syntax:
        {{ variable_name }} - Simple variable
        {{ object.property }} - Nested property
    """
    # Load template
    template = DocxTemplate(template_path)

    # Render with context
    template.render(context)

    # Save output
    template.save(output_path)
    print(f"Document saved to {output_path}")


def create_sample_letter(output_path: str) -> None:
    """Create a sample letter using template rendering."""

    # First, create a simple template (normally you'd have this prepared)
    # Template content would have: {{ recipient_name }}, {{ date }}, etc.

    context = {
        "recipient_name": "John Smith",
        "recipient_title": "Director of Operations",
        "company_name": "Acme Corporation",
        "street_address": "123 Business Ave",
        "city_state_zip": "New York, NY 10001",
        "date": "January 17, 2026",
        "subject": "Project Proposal",
        "salutation": "Dear Mr. Smith",
        "body_paragraph_1": """
            We are pleased to submit our proposal for the infrastructure
            upgrade project. Our team has extensive experience in similar
            projects and we are confident we can deliver exceptional results.
        """.strip(),
        "body_paragraph_2": """
            The attached documents outline our approach, timeline, and
            budget estimates. We would welcome the opportunity to discuss
            this proposal at your convenience.
        """.strip(),
        "closing": "Sincerely",
        "sender_name": "Jane Doe",
        "sender_title": "Project Manager"
    }

    # Render template
    render_simple_template("letter_template.docx", output_path, context)


# Example context for a business report
report_context = {
    "report_title": "Q4 2025 Performance Report",
    "prepared_by": "Analytics Team",
    "date": "January 15, 2026",
    "executive_summary": "Strong performance across all metrics...",
    "total_revenue": "$2,450,000",
    "growth_rate": "15.3%",
    "customer_count": "1,250",
    "key_achievements": [
        "Launched new product line",
        "Expanded to 3 new markets",
        "Achieved ISO certification"
    ]
}
```

**Nested Object Access:**
```python
"""
Access nested objects and complex data structures in templates.
"""
from docxtpl import DocxTemplate
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import date

@dataclass
class Address:
    """Address data structure."""
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"

    @property
    def full_address(self) -> str:
        return f"{self.street}\n{self.city}, {self.state} {self.zip_code}"


@dataclass
class Contact:
    """Contact information."""
    name: str
    email: str
    phone: str
    title: Optional[str] = None


@dataclass
class Company:
    """Company data structure."""
    name: str
    address: Address
    contacts: List[Contact]
    industry: str
    website: str

    def to_dict(self) -> Dict:
        """Convert to dictionary for template rendering."""
        return {
            "name": self.name,
            "address": asdict(self.address),
            "contacts": [asdict(c) for c in self.contacts],
            "industry": self.industry,
            "website": self.website
        }


def render_with_nested_data(
    template_path: str,
    output_path: str,
    company: Company
) -> None:
    """
    Render template with nested data structures.

    Template syntax for nested access:
        {{ company.name }}
        {{ company.address.street }}
        {{ company.contacts[0].email }}
    """
    template = DocxTemplate(template_path)

    context = {
        "company": company.to_dict(),
        "generated_date": date.today().strftime("%B %d, %Y")
    }

    template.render(context)
    template.save(output_path)


# Example usage
company = Company(
    name="TechCorp Industries",
    address=Address(
        street="456 Innovation Blvd",
        city="San Francisco",
        state="CA",
        zip_code="94105"
    ),
    contacts=[
        Contact(
            name="Alice Johnson",
            email="alice@techcorp.com",
            phone="555-0101",
            title="CEO"
        ),
        Contact(
            name="Bob Williams",
            email="bob@techcorp.com",
            phone="555-0102",
            title="CTO"
        )
    ],
    industry="Technology",
    website="https://techcorp.com"
)

# render_with_nested_data("company_profile.docx", "techcorp_profile.docx", company)
```

### 2. Loops and Iterations

**Rendering Lists and Tables:**
```python
"""
Use loops to render lists, tables, and repeated content.
"""
from docxtpl import DocxTemplate
from typing import List, Dict, Any
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class LineItem:
    """Invoice line item."""
    description: str
    quantity: int
    unit_price: Decimal
    discount: Decimal = Decimal("0")

    @property
    def subtotal(self) -> Decimal:
        return self.quantity * self.unit_price * (1 - self.discount / 100)


@dataclass
class Invoice:
    """Invoice data structure."""
    invoice_number: str
    date: str
    due_date: str
    client_name: str
    client_address: str
    items: List[LineItem]
    tax_rate: Decimal = Decimal("8.5")
    notes: str = ""

    @property
    def subtotal(self) -> Decimal:
        return sum(item.subtotal for item in self.items)

    @property
    def tax_amount(self) -> Decimal:
        return self.subtotal * self.tax_rate / 100

    @property
    def total(self) -> Decimal:
        return self.subtotal + self.tax_amount

    def to_context(self) -> Dict[str, Any]:
        """Convert to template context."""
        return {
            "invoice_number": self.invoice_number,
            "date": self.date,
            "due_date": self.due_date,
            "client_name": self.client_name,
            "client_address": self.client_address,
            "items": [
                {
                    "description": item.description,
                    "quantity": item.quantity,
                    "unit_price": f"${item.unit_price:.2f}",
                    "discount": f"{item.discount}%" if item.discount else "",
                    "subtotal": f"${item.subtotal:.2f}"
                }
                for item in self.items
            ],
            "subtotal": f"${self.subtotal:.2f}",
            "tax_rate": f"{self.tax_rate}%",
            "tax_amount": f"${self.tax_amount:.2f}",
            "total": f"${self.total:.2f}",
            "notes": self.notes
        }


def render_invoice(
    template_path: str,
    output_path: str,
    invoice: Invoice
) -> None:
    """
    Render invoice template with line items.

    Template syntax for loops:
        {%tr for item in items %}
        {{ item.description }} | {{ item.quantity }} | {{ item.unit_price }}
        {%tr endfor %}

    Note: {%tr %} is for table rows, {%p %} for paragraphs
    """
    template = DocxTemplate(template_path)
    context = invoice.to_context()
    template.render(context)
    template.save(output_path)


def render_list_document(
    template_path: str,
    output_path: str,
    items: List[str],
    title: str
) -> None:
    """
    Render document with bullet list.

    Template syntax for paragraph loops:
        {%p for item in items %}
        - {{ item }}
        {%p endfor %}
    """
    template = DocxTemplate(template_path)

    context = {
        "title": title,
        "items": items,
        "item_count": len(items)
    }

    template.render(context)
    template.save(output_path)


# Example: Create invoice
invoice = Invoice(
    invoice_number="INV-2026-0042",
    date="January 17, 2026",
    due_date="February 16, 2026",
    client_name="Acme Corp",
    client_address="123 Main St\nNew York, NY 10001",
    items=[
        LineItem("Consulting Services", 40, Decimal("150.00")),
        LineItem("Software License", 1, Decimal("500.00")),
        LineItem("Training Session", 8, Decimal("100.00"), Decimal("10")),
    ],
    notes="Payment due within 30 days. Thank you for your business!"
)

# render_invoice("invoice_template.docx", "invoice_output.docx", invoice)


def render_nested_loops(
    template_path: str,
    output_path: str,
    departments: List[Dict]
) -> None:
    """
    Render template with nested loops.

    Template syntax:
        {%p for dept in departments %}
        Department: {{ dept.name }}
        {%p for emp in dept.employees %}
        - {{ emp.name }} ({{ emp.role }})
        {%p endfor %}
        {%p endfor %}
    """
    template = DocxTemplate(template_path)

    context = {
        "company_name": "TechCorp",
        "departments": departments
    }

    template.render(context)
    template.save(output_path)


# Example data for nested loops
departments = [
    {
        "name": "Engineering",
        "head": "Alice Johnson",
        "employees": [
            {"name": "Bob Smith", "role": "Senior Developer"},
            {"name": "Carol White", "role": "Developer"},
            {"name": "David Brown", "role": "QA Engineer"}
        ]
    },
    {
        "name": "Marketing",
        "head": "Eve Davis",
        "employees": [
            {"name": "Frank Miller", "role": "Marketing Manager"},
            {"name": "Grace Lee", "role": "Content Writer"}
        ]
    }
]
```

### 3. Conditional Content

**If-Else Logic in Templates:**
```python
"""
Use conditionals to include or exclude content based on data.
"""
from docxtpl import DocxTemplate
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ContractType(Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACTOR = "contractor"


class ConfidentialityLevel(Enum):
    STANDARD = "standard"
    HIGH = "high"
    RESTRICTED = "restricted"


@dataclass
class EmployeeContract:
    """Employee contract data."""
    employee_name: str
    position: str
    department: str
    start_date: str
    contract_type: ContractType
    salary: float
    bonus_eligible: bool
    stock_options: Optional[int] = None
    confidentiality_level: ConfidentialityLevel = ConfidentialityLevel.STANDARD
    probation_period_months: int = 3
    remote_work_allowed: bool = False
    relocation_package: bool = False

    def to_context(self) -> Dict[str, Any]:
        """Convert to template context with conditional flags."""
        return {
            "employee_name": self.employee_name,
            "position": self.position,
            "department": self.department,
            "start_date": self.start_date,
            "salary": f"${self.salary:,.2f}",

            # Contract type flags for conditionals
            "is_full_time": self.contract_type == ContractType.FULL_TIME,
            "is_part_time": self.contract_type == ContractType.PART_TIME,
            "is_contractor": self.contract_type == ContractType.CONTRACTOR,
            "contract_type_display": self.contract_type.value.replace("_", " ").title(),

            # Benefit flags
            "bonus_eligible": self.bonus_eligible,
            "has_stock_options": self.stock_options is not None,
            "stock_options": self.stock_options,

            # Additional terms
            "confidentiality_level": self.confidentiality_level.value,
            "is_high_confidentiality": self.confidentiality_level in [
                ConfidentialityLevel.HIGH,
                ConfidentialityLevel.RESTRICTED
            ],
            "probation_period_months": self.probation_period_months,
            "remote_work_allowed": self.remote_work_allowed,
            "relocation_package": self.relocation_package
        }


def render_contract(
    template_path: str,
    output_path: str,
    contract: EmployeeContract
) -> None:
    """
    Render contract with conditional sections.

    Template syntax for conditionals:
        {% if is_full_time %}
        Full-time benefits section...
        {% endif %}

        {% if bonus_eligible %}
        Bonus clause...
        {% else %}
        Standard compensation only.
        {% endif %}

        {% if is_high_confidentiality %}
        Additional NDA requirements...
        {% endif %}
    """
    template = DocxTemplate(template_path)
    context = contract.to_context()
    template.render(context)
    template.save(output_path)


def render_with_conditions(
    template_path: str,
    output_path: str,
    data: Dict[str, Any]
) -> None:
    """
    Render template with various conditional patterns.

    Supported conditional patterns:
        {% if condition %} ... {% endif %}
        {% if condition %} ... {% else %} ... {% endif %}
        {% if condition %} ... {% elif other %} ... {% else %} ... {% endif %}
        {% if value > 100 %} ... {% endif %}
        {% if value in list %} ... {% endif %}
    """
    template = DocxTemplate(template_path)
    template.render(data)
    template.save(output_path)


# Example contract
contract = EmployeeContract(
    employee_name="John Doe",
    position="Senior Software Engineer",
    department="Engineering",
    start_date="February 1, 2026",
    contract_type=ContractType.FULL_TIME,
    salary=150000,
    bonus_eligible=True,
    stock_options=5000,
    confidentiality_level=ConfidentialityLevel.HIGH,
    remote_work_allowed=True
)

# render_contract("contract_template.docx", "john_doe_contract.docx", contract)


def create_conditional_report(
    template_path: str,
    output_path: str,
    performance_data: Dict
) -> None:
    """
    Create report with conditional formatting based on performance.

    Template example:
        Performance Score: {{ score }}

        {% if score >= 90 %}
        OUTSTANDING PERFORMANCE
        {% elif score >= 75 %}
        MEETS EXPECTATIONS
        {% elif score >= 60 %}
        NEEDS IMPROVEMENT
        {% else %}
        PERFORMANCE PLAN REQUIRED
        {% endif %}

        {% if has_warnings %}
        Warnings:
        {%p for warning in warnings %}
        - {{ warning }}
        {%p endfor %}
        {% endif %}
    """
    template = DocxTemplate(template_path)

    # Add computed flags to context
    score = performance_data.get("score", 0)
    context = {
        **performance_data,
        "performance_level": (
            "Outstanding" if score >= 90 else
            "Meets Expectations" if score >= 75 else
            "Needs Improvement" if score >= 60 else
            "Below Expectations"
        ),
        "has_warnings": len(performance_data.get("warnings", [])) > 0
    }

    template.render(context)
    template.save(output_path)
```

### 4. Table Generation

**Dynamic Tables with Data:**
```python
"""
Generate tables dynamically from data.
"""
from docxtpl import DocxTemplate
from typing import List, Dict, Any
import pandas as pd

def render_data_table(
    template_path: str,
    output_path: str,
    headers: List[str],
    rows: List[List[Any]],
    table_title: str = ""
) -> None:
    """
    Render a simple data table.

    Template structure:
        {{ table_title }}

        | Header 1 | Header 2 | Header 3 |
        |----------|----------|----------|
        {%tr for row in rows %}
        | {{ row[0] }} | {{ row[1] }} | {{ row[2] }} |
        {%tr endfor %}
    """
    template = DocxTemplate(template_path)

    # Convert rows to list of dicts for easier template access
    row_dicts = []
    for row in rows:
        row_dict = {f"col{i}": val for i, val in enumerate(row)}
        row_dicts.append(row_dict)

    context = {
        "table_title": table_title,
        "headers": headers,
        "rows": row_dicts,
        "column_count": len(headers)
    }

    template.render(context)
    template.save(output_path)


def render_pandas_table(
    template_path: str,
    output_path: str,
    df: pd.DataFrame,
    title: str = ""
) -> None:
    """
    Render a pandas DataFrame as a table.

    Template:
        {%tr for row in data %}
        {%tc for cell in row %}{{ cell }}{%tc endfor %}
        {%tr endfor %}
    """
    template = DocxTemplate(template_path)

    # Convert DataFrame to list of dicts
    headers = df.columns.tolist()
    data = df.values.tolist()

    context = {
        "title": title,
        "headers": headers,
        "data": data,
        "row_count": len(data),
        "col_count": len(headers)
    }

    template.render(context)
    template.save(output_path)


def render_grouped_table(
    template_path: str,
    output_path: str,
    grouped_data: Dict[str, List[Dict]]
) -> None:
    """
    Render table with grouped rows and subtotals.

    Template:
        {%tr for group_name, items in groups.items() %}
        {{ group_name }} ({{ items|length }} items)
        {%tr for item in items %}
        | {{ item.name }} | {{ item.value }} |
        {%tr endfor %}
        Subtotal: {{ group_subtotals[group_name] }}
        {%tr endfor %}
    """
    template = DocxTemplate(template_path)

    # Calculate subtotals
    subtotals = {}
    for group, items in grouped_data.items():
        subtotals[group] = sum(item.get("value", 0) for item in items)

    context = {
        "groups": grouped_data,
        "group_subtotals": subtotals,
        "total": sum(subtotals.values())
    }

    template.render(context)
    template.save(output_path)


class TableBuilder:
    """
    Builder for complex table structures.
    """

    def __init__(self):
        self.headers: List[str] = []
        self.rows: List[Dict] = []
        self.footer_row: Dict = {}
        self.title: str = ""

    def set_title(self, title: str) -> 'TableBuilder':
        """Set table title."""
        self.title = title
        return self

    def set_headers(self, headers: List[str]) -> 'TableBuilder':
        """Set column headers."""
        self.headers = headers
        return self

    def add_row(self, **kwargs) -> 'TableBuilder':
        """Add a data row."""
        self.rows.append(kwargs)
        return self

    def add_rows_from_dicts(self, rows: List[Dict]) -> 'TableBuilder':
        """Add multiple rows from list of dicts."""
        self.rows.extend(rows)
        return self

    def add_rows_from_dataframe(self, df: pd.DataFrame) -> 'TableBuilder':
        """Add rows from DataFrame."""
        self.headers = df.columns.tolist()
        self.rows = df.to_dict('records')
        return self

    def set_footer(self, **kwargs) -> 'TableBuilder':
        """Set footer row (e.g., totals)."""
        self.footer_row = kwargs
        return self

    def auto_calculate_footer(self, columns: List[str], operation: str = "sum") -> 'TableBuilder':
        """Auto-calculate footer values."""
        for col in columns:
            values = [row.get(col, 0) for row in self.rows if isinstance(row.get(col), (int, float))]
            if operation == "sum":
                self.footer_row[col] = sum(values)
            elif operation == "avg":
                self.footer_row[col] = sum(values) / len(values) if values else 0
            elif operation == "count":
                self.footer_row[col] = len(values)

        return self

    def to_context(self) -> Dict[str, Any]:
        """Convert to template context."""
        return {
            "table_title": self.title,
            "headers": self.headers,
            "rows": self.rows,
            "footer": self.footer_row,
            "has_footer": bool(self.footer_row),
            "row_count": len(self.rows)
        }

    def render(self, template_path: str, output_path: str) -> None:
        """Render to document."""
        template = DocxTemplate(template_path)
        template.render(self.to_context())
        template.save(output_path)


# Example usage
builder = TableBuilder()
builder.set_title("Monthly Sales Report")
builder.set_headers(["Product", "Units", "Revenue", "Margin"])
builder.add_row(Product="Widget A", Units=100, Revenue=5000, Margin=25)
builder.add_row(Product="Widget B", Units=150, Revenue=7500, Margin=30)
builder.add_row(Product="Widget C", Units=75, Revenue=3750, Margin=22)
builder.auto_calculate_footer(["Units", "Revenue"], operation="sum")

# builder.render("sales_table_template.docx", "sales_report.docx")
```

### 5. Image Insertion

**Adding Images to Templates:**
```python
"""
Insert images into templates with proper sizing.
"""
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm, Inches, Cm
from pathlib import Path
from typing import Optional, Union
from io import BytesIO
import requests

def add_image_to_template(
    template_path: str,
    output_path: str,
    image_path: str,
    context: dict,
    width: Optional[Union[Mm, Inches, Cm]] = None,
    height: Optional[Union[Mm, Inches, Cm]] = None
) -> None:
    """
    Add an image to a template.

    Template syntax:
        {{ image }}

    Args:
        template_path: Path to template
        output_path: Path for output
        image_path: Path to image file
        context: Additional context data
        width: Image width (optional)
        height: Image height (optional)
    """
    template = DocxTemplate(template_path)

    # Create InlineImage
    image = InlineImage(
        template,
        image_path,
        width=width,
        height=height
    )

    # Add image to context
    context["image"] = image

    template.render(context)
    template.save(output_path)


def add_image_from_url(
    template: DocxTemplate,
    url: str,
    width: Optional[Mm] = None
) -> InlineImage:
    """
    Create InlineImage from URL.

    Args:
        template: DocxTemplate instance
        url: Image URL
        width: Desired width

    Returns:
        InlineImage object
    """
    response = requests.get(url)
    response.raise_for_status()

    image_stream = BytesIO(response.content)

    return InlineImage(
        template,
        image_stream,
        width=width
    )


def render_document_with_images(
    template_path: str,
    output_path: str,
    data: dict,
    images: dict
) -> None:
    """
    Render document with multiple images.

    Template:
        Company Logo: {{ logo }}

        Product Images:
        {% for product in products %}
        {{ product.name }}: {{ product.image }}
        {% endfor %}
    """
    template = DocxTemplate(template_path)

    # Process images
    context = data.copy()

    for key, image_info in images.items():
        if isinstance(image_info, str):
            # Simple path
            context[key] = InlineImage(template, image_info, width=Mm(50))
        elif isinstance(image_info, dict):
            # Dict with path and dimensions
            context[key] = InlineImage(
                template,
                image_info["path"],
                width=image_info.get("width"),
                height=image_info.get("height")
            )

    template.render(context)
    template.save(output_path)


class ImageHandler:
    """
    Handle images for template rendering.
    """

    def __init__(self, template: DocxTemplate):
        self.template = template
        self._images: dict = {}

    def add_image(
        self,
        key: str,
        source: Union[str, BytesIO],
        width: Optional[int] = None,
        height: Optional[int] = None,
        unit: str = "mm"
    ) -> 'ImageHandler':
        """
        Add an image to the handler.

        Args:
            key: Context key for the image
            source: File path or BytesIO stream
            width: Width in specified units
            height: Height in specified units
            unit: Unit type ('mm', 'inches', 'cm')
        """
        # Convert units
        if unit == "mm":
            w = Mm(width) if width else None
            h = Mm(height) if height else None
        elif unit == "inches":
            w = Inches(width) if width else None
            h = Inches(height) if height else None
        elif unit == "cm":
            w = Cm(width) if width else None
            h = Cm(height) if height else None
        else:
            w = h = None

        self._images[key] = InlineImage(
            self.template,
            source,
            width=w,
            height=h
        )

        return self

    def add_image_from_url(
        self,
        key: str,
        url: str,
        width: int = 50,
        unit: str = "mm"
    ) -> 'ImageHandler':
        """Add image from URL."""
        response = requests.get(url)
        response.raise_for_status()

        image_stream = BytesIO(response.content)

        return self.add_image(key, image_stream, width=width, unit=unit)

    def get_context(self) -> dict:
        """Get images as context dictionary."""
        return self._images.copy()


# Example usage
def create_product_catalog(
    template_path: str,
    output_path: str,
    products: List[Dict]
) -> None:
    """Create product catalog with images."""
    template = DocxTemplate(template_path)
    handler = ImageHandler(template)

    # Process products and add images
    processed_products = []
    for i, product in enumerate(products):
        if "image_path" in product:
            handler.add_image(
                f"product_image_{i}",
                product["image_path"],
                width=60,
                unit="mm"
            )
            product["image"] = handler._images[f"product_image_{i}"]
        processed_products.append(product)

    context = {
        "catalog_title": "2026 Product Catalog",
        "products": processed_products,
        **handler.get_context()
    }

    template.render(context)
    template.save(output_path)
```

### 6. Mail Merge and Batch Generation

**Generating Multiple Documents:**
```python
"""
Generate multiple documents from a template with different data.
"""
from docxtpl import DocxTemplate
from typing import List, Dict, Any, Iterator
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import json
import pandas as pd

def mail_merge_from_list(
    template_path: str,
    output_dir: str,
    records: List[Dict[str, Any]],
    filename_field: str = "id"
) -> List[str]:
    """
    Generate documents for multiple records.

    Args:
        template_path: Path to template
        output_dir: Directory for output files
        records: List of data records
        filename_field: Field to use for output filename

    Returns:
        List of generated file paths
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    generated_files = []

    for record in records:
        # Load fresh template for each document
        template = DocxTemplate(template_path)

        # Generate filename
        filename = f"{record.get(filename_field, 'document')}.docx"
        file_path = output_path / filename

        # Render and save
        template.render(record)
        template.save(str(file_path))

        generated_files.append(str(file_path))

    print(f"Generated {len(generated_files)} documents in {output_dir}")
    return generated_files


def mail_merge_from_csv(
    template_path: str,
    csv_path: str,
    output_dir: str,
    filename_field: str = "id"
) -> List[str]:
    """
    Generate documents from CSV data source.

    Args:
        template_path: Path to template
        csv_path: Path to CSV file
        output_dir: Directory for output files
        filename_field: Field to use for output filename

    Returns:
        List of generated file paths
    """
    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        records = list(reader)

    return mail_merge_from_list(template_path, output_dir, records, filename_field)


def mail_merge_from_excel(
    template_path: str,
    excel_path: str,
    output_dir: str,
    sheet_name: str = None,
    filename_field: str = "id"
) -> List[str]:
    """
    Generate documents from Excel data source.

    Args:
        template_path: Path to template
        excel_path: Path to Excel file
        output_dir: Directory for output files
        sheet_name: Sheet to read (default: first sheet)
        filename_field: Field to use for output filename

    Returns:
        List of generated file paths
    """
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    records = df.to_dict('records')

    return mail_merge_from_list(template_path, output_dir, records, filename_field)


def mail_merge_parallel(
    template_path: str,
    output_dir: str,
    records: List[Dict[str, Any]],
    filename_field: str = "id",
    max_workers: int = 4
) -> List[str]:
    """
    Generate documents in parallel for better performance.

    Args:
        template_path: Path to template
        output_dir: Directory for output files
        records: List of data records
        filename_field: Field to use for output filename
        max_workers: Maximum parallel workers

    Returns:
        List of generated file paths
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    def generate_single(record: Dict) -> str:
        """Generate a single document."""
        template = DocxTemplate(template_path)
        filename = f"{record.get(filename_field, 'document')}.docx"
        file_path = output_path / filename

        template.render(record)
        template.save(str(file_path))

        return str(file_path)

    generated_files = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(generate_single, r): r for r in records}

        for future in as_completed(futures):
            try:
                result = future.result()
                generated_files.append(result)
            except Exception as e:
                record = futures[future]
                print(f"Error generating document for {record.get(filename_field)}: {e}")

    print(f"Generated {len(generated_files)} documents")
    return generated_files


class MailMergeGenerator:
    """
    Full-featured mail merge generator.
    """

    def __init__(self, template_path: str):
        self.template_path = template_path
        self._validate_template()

    def _validate_template(self) -> None:
        """Validate template file exists."""
        if not Path(self.template_path).exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")

    def _get_template_variables(self) -> List[str]:
        """Extract variable names from template."""
        template = DocxTemplate(self.template_path)
        return list(template.get_undeclared_template_variables())

    def validate_data(self, records: List[Dict]) -> Dict[str, List]:
        """
        Validate data against template variables.

        Returns:
            Dict with 'missing' and 'extra' variable lists
        """
        template_vars = set(self._get_template_variables())

        if not records:
            return {"missing": list(template_vars), "extra": []}

        data_vars = set(records[0].keys())

        return {
            "missing": list(template_vars - data_vars),
            "extra": list(data_vars - template_vars)
        }

    def generate(
        self,
        output_dir: str,
        records: List[Dict],
        filename_pattern: str = "{id}",
        parallel: bool = False,
        max_workers: int = 4
    ) -> Dict[str, Any]:
        """
        Generate documents with full reporting.

        Args:
            output_dir: Output directory
            records: Data records
            filename_pattern: Pattern for filenames (e.g., "{name}_{date}")
            parallel: Use parallel processing
            max_workers: Number of parallel workers

        Returns:
            Generation report
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        results = {
            "total": len(records),
            "successful": 0,
            "failed": 0,
            "files": [],
            "errors": []
        }

        def process_record(record: Dict) -> Dict:
            """Process single record."""
            try:
                template = DocxTemplate(self.template_path)

                # Generate filename from pattern
                filename = filename_pattern.format(**record) + ".docx"
                file_path = output_path / filename

                template.render(record)
                template.save(str(file_path))

                return {"success": True, "file": str(file_path)}
            except Exception as e:
                return {"success": False, "error": str(e), "record": record}

        if parallel and len(records) > 1:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(process_record, r) for r in records]
                for future in as_completed(futures):
                    result = future.result()
                    if result["success"]:
                        results["successful"] += 1
                        results["files"].append(result["file"])
                    else:
                        results["failed"] += 1
                        results["errors"].append(result)
        else:
            for record in records:
                result = process_record(record)
                if result["success"]:
                    results["successful"] += 1
                    results["files"].append(result["file"])
                else:
                    results["failed"] += 1
                    results["errors"].append(result)

        return results


# Example usage
def generate_personalized_letters():
    """Generate personalized letters for recipients."""
    recipients = [
        {
            "id": "001",
            "name": "John Smith",
            "title": "Mr.",
            "company": "Acme Corp",
            "address": "123 Main St",
            "city": "New York",
            "offer_amount": "$50,000"
        },
        {
            "id": "002",
            "name": "Jane Doe",
            "title": "Ms.",
            "company": "TechStart Inc",
            "address": "456 Oak Ave",
            "city": "San Francisco",
            "offer_amount": "$75,000"
        }
    ]

    generator = MailMergeGenerator("offer_letter_template.docx")

    # Validate data
    validation = generator.validate_data(recipients)
    if validation["missing"]:
        print(f"Warning: Missing variables: {validation['missing']}")

    # Generate documents
    results = generator.generate(
        output_dir="generated_letters",
        records=recipients,
        filename_pattern="{id}_{name}",
        parallel=True
    )

    print(f"Generated: {results['successful']}/{results['total']}")
    if results["errors"]:
        for error in results["errors"]:
            print(f"Error: {error}")


# generate_personalized_letters()
```

## Integration Examples

### Database Integration

```python
"""
Generate documents from database queries.
"""
from docxtpl import DocxTemplate
from typing import List, Dict
import sqlite3
from sqlalchemy import create_engine, text
import pandas as pd

def generate_from_database(
    template_path: str,
    output_dir: str,
    db_connection: str,
    query: str,
    filename_field: str = "id"
) -> List[str]:
    """
    Generate documents from database query results.

    Args:
        template_path: Path to template
        output_dir: Output directory
        db_connection: Database connection string
        query: SQL query to fetch data
        filename_field: Field for output filename

    Returns:
        List of generated file paths
    """
    # Connect and fetch data
    engine = create_engine(db_connection)

    with engine.connect() as conn:
        result = conn.execute(text(query))
        records = [dict(row._mapping) for row in result]

    # Generate documents
    return mail_merge_from_list(template_path, output_dir, records, filename_field)


def generate_customer_reports(
    template_path: str,
    output_dir: str,
    db_path: str
) -> Dict:
    """Generate customer reports from SQLite database."""

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # Fetch customers with their orders
    query = """
    SELECT
        c.id,
        c.name,
        c.email,
        c.address,
        COUNT(o.id) as order_count,
        SUM(o.total) as total_spent
    FROM customers c
    LEFT JOIN orders o ON c.id = o.customer_id
    GROUP BY c.id
    """

    cursor = conn.cursor()
    cursor.execute(query)

    records = []
    for row in cursor.fetchall():
        record = dict(row)

        # Fetch order details for each customer
        cursor.execute(
            "SELECT * FROM orders WHERE customer_id = ?",
            (record["id"],)
        )
        record["orders"] = [dict(r) for r in cursor.fetchall()]
        records.append(record)

    conn.close()

    # Generate reports
    generated = mail_merge_from_list(
        template_path,
        output_dir,
        records,
        filename_field="id"
    )

    return {
        "total_customers": len(records),
        "generated_reports": len(generated),
        "files": generated
    }
```

### FastAPI Service

```python
"""
Document generation service with FastAPI.
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from docxtpl import DocxTemplate
from pathlib import Path
import tempfile
import uuid

app = FastAPI(title="Document Generation Service")

# Template storage
TEMPLATES_DIR = Path("./templates")
OUTPUT_DIR = Path("./generated")
OUTPUT_DIR.mkdir(exist_ok=True)


class GenerateRequest(BaseModel):
    """Request model for document generation."""
    template_name: str
    data: Dict[str, Any]
    output_filename: Optional[str] = None


class BatchGenerateRequest(BaseModel):
    """Request for batch generation."""
    template_name: str
    records: List[Dict[str, Any]]
    filename_field: str = "id"


@app.get("/templates")
async def list_templates():
    """List available templates."""
    templates = []
    for f in TEMPLATES_DIR.glob("*.docx"):
        templates.append({
            "name": f.stem,
            "filename": f.name
        })
    return {"templates": templates}


@app.post("/generate")
async def generate_document(request: GenerateRequest):
    """Generate a single document."""
    template_path = TEMPLATES_DIR / f"{request.template_name}.docx"

    if not template_path.exists():
        raise HTTPException(404, f"Template '{request.template_name}' not found")

    try:
        template = DocxTemplate(str(template_path))
        template.render(request.data)

        # Generate output filename
        output_name = request.output_filename or f"{uuid.uuid4()}.docx"
        if not output_name.endswith(".docx"):
            output_name += ".docx"

        output_path = OUTPUT_DIR / output_name
        template.save(str(output_path))

        return FileResponse(
            str(output_path),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=output_name
        )

    except Exception as e:
        raise HTTPException(500, f"Generation failed: {str(e)}")


@app.post("/generate/batch")
async def generate_batch(request: BatchGenerateRequest):
    """Generate multiple documents."""
    template_path = TEMPLATES_DIR / f"{request.template_name}.docx"

    if not template_path.exists():
        raise HTTPException(404, f"Template '{request.template_name}' not found")

    generated = []
    errors = []

    for record in request.records:
        try:
            template = DocxTemplate(str(template_path))
            template.render(record)

            filename = f"{record.get(request.filename_field, uuid.uuid4())}.docx"
            output_path = OUTPUT_DIR / filename

            template.save(str(output_path))
            generated.append(filename)

        except Exception as e:
            errors.append({
                "record": record.get(request.filename_field),
                "error": str(e)
            })

    return {
        "generated": len(generated),
        "failed": len(errors),
        "files": generated,
        "errors": errors
    }


@app.post("/templates/upload")
async def upload_template(file: UploadFile = File(...)):
    """Upload a new template."""
    if not file.filename.endswith(".docx"):
        raise HTTPException(400, "Only .docx files are supported")

    template_path = TEMPLATES_DIR / file.filename

    content = await file.read()
    with open(template_path, "wb") as f:
        f.write(content)

    return {"message": f"Template '{file.filename}' uploaded", "name": Path(file.filename).stem}


# Run with: uvicorn service:app --reload
```

## Best Practices

### 1. Template Design

```python
"""Best practices for template design."""

# DO: Use meaningful variable names
good_context = {
    "customer_name": "John Smith",
    "invoice_date": "2026-01-17",
    "total_amount": "$1,500.00"
}

# DON'T: Use cryptic names
bad_context = {
    "cn": "John Smith",
    "d": "2026-01-17",
    "t": "$1,500.00"
}

# DO: Organize context with nested objects
organized_context = {
    "customer": {
        "name": "John Smith",
        "email": "john@example.com",
        "address": {
            "street": "123 Main St",
            "city": "New York"
        }
    },
    "invoice": {
        "number": "INV-001",
        "date": "2026-01-17",
        "items": [...]
    }
}

# DO: Include computed values
def prepare_context(data: dict) -> dict:
    """Prepare context with computed values."""
    context = data.copy()

    # Add computed fields
    if "items" in context:
        context["item_count"] = len(context["items"])
        context["subtotal"] = sum(i["total"] for i in context["items"])

    # Add display flags
    context["has_discount"] = context.get("discount", 0) > 0

    return context
```

### 2. Error Handling

```python
"""Robust error handling for template rendering."""
from typing import Tuple, Optional

def safe_render(
    template_path: str,
    output_path: str,
    context: dict
) -> Tuple[bool, Optional[str]]:
    """
    Safely render template with error handling.

    Returns:
        Tuple of (success, error_message)
    """
    try:
        # Validate template exists
        if not Path(template_path).exists():
            return False, f"Template not found: {template_path}"

        # Load and render
        template = DocxTemplate(template_path)

        # Check for missing variables
        required_vars = template.get_undeclared_template_variables()
        missing = [v for v in required_vars if v not in context]
        if missing:
            return False, f"Missing variables: {missing}"

        template.render(context)

        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        template.save(output_path)
        return True, None

    except Exception as e:
        return False, str(e)
```

### 3. Performance Optimization

```python
"""Optimize batch document generation."""

# DO: Use parallel processing for large batches
def optimized_batch_generation(
    template_path: str,
    records: List[Dict],
    output_dir: str,
    batch_size: int = 100
) -> List[str]:
    """Generate documents in optimized batches."""
    from concurrent.futures import ThreadPoolExecutor

    def process_batch(batch_records):
        results = []
        for record in batch_records:
            template = DocxTemplate(template_path)
            template.render(record)
            output_path = Path(output_dir) / f"{record['id']}.docx"
            template.save(str(output_path))
            results.append(str(output_path))
        return results

    # Process in batches
    all_results = []
    batches = [records[i:i+batch_size] for i in range(0, len(records), batch_size)]

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_batch, b) for b in batches]
        for future in futures:
            all_results.extend(future.result())

    return all_results
```

## Troubleshooting

### Template Variables Not Rendering

```python
# Problem: Variables appear as {{ variable }} in output
# Solution: Check variable syntax and context keys

def diagnose_template(template_path: str, context: dict):
    """Diagnose template rendering issues."""
    template = DocxTemplate(template_path)

    # Get expected variables
    expected = template.get_undeclared_template_variables()
    print(f"Template expects: {expected}")

    # Check context
    provided = set(context.keys())
    print(f"Context provides: {provided}")

    # Find mismatches
    missing = expected - provided
    if missing:
        print(f"MISSING: {missing}")
```

### Loop Not Iterating

```python
# Problem: Loop content not appearing
# Solution: Verify loop syntax and data structure

# CORRECT loop syntax in template:
# {%tr for item in items %}
#   {{ item.name }}
# {%tr endfor %}

# Ensure data is a list
context = {
    "items": [
        {"name": "Item 1"},  # Must be dict or object
        {"name": "Item 2"}
    ]
}
```

### Image Not Appearing

```python
# Problem: Image placeholder shows error
# Solution: Verify image path and format

from pathlib import Path

def validate_image(image_path: str) -> bool:
    """Validate image file."""
    path = Path(image_path)

    if not path.exists():
        print(f"Image not found: {image_path}")
        return False

    valid_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}
    if path.suffix.lower() not in valid_extensions:
        print(f"Invalid format: {path.suffix}")
        return False

    return True
```

## Resources

- **docxtpl Documentation**: https://docxtpl.readthedocs.io/
- **GitHub Repository**: https://github.com/elapouya/python-docx-template
- **Jinja2 Template Syntax**: https://jinja.palletsprojects.com/
- **python-docx (underlying library)**: https://python-docx.readthedocs.io/

## Version History

- **1.0.0** (2026-01-17): Initial release with template rendering, loops, conditionals, tables, images, mail merge

---

*This skill provides comprehensive patterns for template-based document generation with docxtpl, refined from production document automation workflows.*
