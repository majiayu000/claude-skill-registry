---
name: supply-chain-automation
description: When the user wants to automate supply chain processes, build automation systems, or implement robotic process automation (RPA). Also use when the user mentions "process automation," "RPA," "workflow automation," "task automation," "supply chain bots," "automated replenishment," "auto-ordering," "automated decision-making," or "process orchestration." For analytics dashboards, see supply-chain-analytics. For optimization, see optimization-modeling.
---

# Supply Chain Automation

You are an expert in supply chain automation and process optimization. Your goal is to help design, implement, and manage automated systems that reduce manual work, improve efficiency, eliminate errors, and enable faster, data-driven decision-making across supply chain operations.

## Initial Assessment

Before implementing automation, understand:

1. **Process Analysis**
   - What processes need automation? (ordering, replenishment, allocation, invoicing)
   - Current pain points? (manual data entry, errors, delays, inconsistency)
   - Process volume and frequency? (1000 orders/day, hourly replenishment)
   - Process complexity? (simple rules vs. complex logic)

2. **Current State**
   - How is the process done today? (manual, semi-automated, spreadsheets)
   - Time spent on manual tasks? (hours per week)
   - Error rates? (% of errors, cost of errors)
   - Systems involved? (ERP, WMS, TMS, spreadsheets)

3. **Business Value**
   - Expected benefits? (time savings, cost reduction, accuracy improvement)
   - ROI targets?
   - Criticality to business? (mission-critical vs. nice-to-have)
   - Compliance or audit requirements?

4. **Technical Environment**
   - System access? (APIs available, database access, screen scraping needed)
   - IT support and governance?
   - Security and data privacy requirements?
   - Infrastructure? (cloud, on-premise, hybrid)

---

## Automation Framework

### Automation Maturity Levels

**Level 0: Manual**
- All tasks done manually
- Spreadsheet-based processes
- Email and phone communication
- No integration

**Level 1: Task Automation**
- Individual tasks automated
- Basic scripts and macros
- Simple data transfers
- Minimal integration

**Level 2: Process Automation**
- End-to-end processes automated
- Workflow orchestration
- Multi-system integration
- Rule-based decision logic

**Level 3: Intelligent Automation**
- ML-powered decision-making
- Predictive automation
- Exception handling
- Adaptive learning

**Level 4: Autonomous**
- Self-optimizing systems
- Real-time adaptation
- Closed-loop control
- Full autonomy

### Automation Technology Stack

```
┌─────────────────────────────────────────────────────────┐
│              User Interface Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Web Apps   │  │    Mobile    │  │  Dashboards  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────┤
│           Intelligent Automation Layer                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  ML Models   │  │     Rules    │  │  Workflows   │ │
│  │  Prediction  │  │    Engine    │  │ Orchestration│ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────┤
│             Process Automation Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │     RPA      │  │  API Gateway │  │  Schedulers  │ │
│  │    Bots      │  │ Integration  │  │   Triggers   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────┤
│               Data Integration Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  ETL/ELT     │  │   Data Lake  │  │   Message    │ │
│  │  Pipelines   │  │  Warehouse   │  │    Queue     │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
├─────────────────────────────────────────────────────────┤
│               System Integration Layer                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │     ERP      │  │     WMS      │  │     TMS      │ │
│  │   SAP/Oracle │  │  Manhattan   │  │  Blue Yonder │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## Automated Replenishment

### Automated Inventory Replenishment System

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AutomatedReplenishment:
    """
    Automated inventory replenishment system

    Monitors inventory levels, calculates reorder needs,
    generates purchase orders automatically
    """

    def __init__(self, config):
        """
        config: dict with system parameters
        - reorder_point_method: 'static', 'dynamic', 'ml'
        - order_approval_threshold: $ value requiring approval
        - supplier_api_endpoints: dict of supplier APIs
        - email_config: SMTP settings for notifications
        """
        self.config = config
        self.inventory_data = None
        self.demand_forecast = None
        self.supplier_info = None
        self.orders_generated = []

    def load_inventory_data(self, data_source):
        """
        Load current inventory levels

        data_source: database connection, API, or file path
        """

        # Example: Load from database
        # In production, connect to ERP/WMS system
        self.inventory_data = pd.DataFrame({
            'sku': ['SKU_001', 'SKU_002', 'SKU_003'],
            'on_hand': [150, 80, 250],
            'on_order': [100, 0, 50],
            'reorder_point': [200, 150, 300],
            'order_quantity': [500, 300, 400],
            'supplier': ['Supplier_A', 'Supplier_B', 'Supplier_A'],
            'lead_time_days': [14, 10, 14],
            'unit_cost': [25.00, 45.00, 15.00],
            'last_order_date': [datetime.now() - timedelta(days=20),
                               datetime.now() - timedelta(days=30),
                               datetime.now() - timedelta(days=15)]
        })

    def calculate_reorder_needs(self):
        """
        Determine which SKUs need reordering

        Checks inventory position (on_hand + on_order) against reorder point
        """

        self.inventory_data['inventory_position'] = (
            self.inventory_data['on_hand'] +
            self.inventory_data['on_order']
        )

        self.inventory_data['needs_reorder'] = (
            self.inventory_data['inventory_position'] <
            self.inventory_data['reorder_point']
        )

        # Calculate order quantity
        # Can use EOQ, fixed quantity, or dynamic calculation
        self.inventory_data['recommended_order_qty'] = np.where(
            self.inventory_data['needs_reorder'],
            self.inventory_data['order_quantity'],
            0
        )

        reorder_items = self.inventory_data[
            self.inventory_data['needs_reorder']
        ].copy()

        return reorder_items

    def optimize_order_quantities(self, reorder_items):
        """
        Optimize order quantities considering multiple factors

        - MOQ (minimum order quantity)
        - Price breaks / volume discounts
        - Container/pallet fill optimization
        - Lead time variability
        """

        for idx, row in reorder_items.iterrows():
            sku = row['sku']

            # Get demand forecast
            forecast = self.get_demand_forecast(sku)

            # Calculate optimal order quantity
            # Simplified EOQ calculation
            annual_demand = forecast['annual_demand']
            order_cost = 100  # $ per order
            holding_cost_rate = 0.25  # 25% of unit cost

            eoq = np.sqrt(
                (2 * annual_demand * order_cost) /
                (row['unit_cost'] * holding_cost_rate)
            )

            # Adjust for MOQ, pack size, etc.
            optimal_qty = max(eoq, row['order_quantity'])

            # Round to case pack
            case_pack = 50  # units per case
            optimal_qty = np.ceil(optimal_qty / case_pack) * case_pack

            reorder_items.at[idx, 'recommended_order_qty'] = optimal_qty

        return reorder_items

    def get_demand_forecast(self, sku):
        """
        Get demand forecast for SKU

        Could integrate with ML forecasting system
        """

        # Placeholder: return dummy forecast
        return {
            'annual_demand': 10000,
            'next_30_days': 850,
            'forecast_error': 0.15
        }

    def generate_purchase_orders(self, reorder_items):
        """
        Generate purchase orders for reorder items

        Groups by supplier for consolidation
        """

        pos_created = []

        # Group by supplier
        for supplier, items in reorder_items.groupby('supplier'):
            po_number = self.generate_po_number()

            po = {
                'po_number': po_number,
                'supplier': supplier,
                'order_date': datetime.now(),
                'items': [],
                'total_value': 0,
                'status': 'draft'
            }

            for idx, item in items.iterrows():
                line_item = {
                    'sku': item['sku'],
                    'quantity': item['recommended_order_qty'],
                    'unit_cost': item['unit_cost'],
                    'line_total': item['recommended_order_qty'] * item['unit_cost']
                }

                po['items'].append(line_item)
                po['total_value'] += line_item['line_total']

            # Check if approval needed
            if po['total_value'] > self.config['order_approval_threshold']:
                po['status'] = 'pending_approval'
                self.send_approval_request(po)
            else:
                po['status'] = 'approved'
                self.submit_po_to_supplier(po)

            pos_created.append(po)
            self.orders_generated.append(po)

        return pos_created

    def generate_po_number(self):
        """Generate unique PO number"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"PO-{timestamp}"

    def submit_po_to_supplier(self, po):
        """
        Submit approved PO to supplier

        Methods:
        - API integration (preferred)
        - EDI
        - Email
        - Portal upload
        """

        supplier = po['supplier']

        # Check if supplier has API integration
        if supplier in self.config.get('supplier_api_endpoints', {}):
            self.submit_via_api(po, supplier)
        else:
            self.submit_via_email(po, supplier)

        print(f"PO {po['po_number']} submitted to {supplier}")

    def submit_via_api(self, po, supplier):
        """Submit PO via supplier API"""

        import requests

        api_endpoint = self.config['supplier_api_endpoints'][supplier]

        payload = {
            'po_number': po['po_number'],
            'order_date': po['order_date'].isoformat(),
            'items': po['items']
        }

        response = requests.post(
            api_endpoint,
            json=payload,
            headers={'Authorization': f"Bearer {self.config['api_keys'][supplier]}"}
        )

        if response.status_code == 200:
            po['submission_status'] = 'success'
            po['supplier_confirmation'] = response.json().get('confirmation_number')
        else:
            po['submission_status'] = 'failed'
            self.send_alert(f"PO submission failed: {po['po_number']}")

    def submit_via_email(self, po, supplier):
        """Send PO via email"""

        # Get supplier email
        supplier_email = self.config['supplier_emails'].get(supplier)

        if not supplier_email:
            self.send_alert(f"No email found for supplier: {supplier}")
            return

        # Create email
        msg = MIMEMultipart()
        msg['From'] = self.config['email_config']['from_address']
        msg['To'] = supplier_email
        msg['Subject'] = f"Purchase Order {po['po_number']}"

        # Email body
        body = self.format_po_email(po)
        msg.attach(MIMEText(body, 'html'))

        # Send
        try:
            with smtplib.SMTP(self.config['email_config']['smtp_server'],
                            self.config['email_config']['smtp_port']) as server:
                server.starttls()
                server.login(self.config['email_config']['username'],
                           self.config['email_config']['password'])
                server.send_message(msg)

            po['submission_status'] = 'success'
        except Exception as e:
            po['submission_status'] = 'failed'
            self.send_alert(f"Email sending failed: {e}")

    def format_po_email(self, po):
        """Format PO as HTML email"""

        html = f"""
        <html>
        <body>
            <h2>Purchase Order {po['po_number']}</h2>
            <p><strong>Order Date:</strong> {po['order_date'].strftime('%Y-%m-%d')}</p>

            <h3>Items:</h3>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    <th>SKU</th>
                    <th>Quantity</th>
                    <th>Unit Cost</th>
                    <th>Line Total</th>
                </tr>
        """

        for item in po['items']:
            html += f"""
                <tr>
                    <td>{item['sku']}</td>
                    <td>{item['quantity']}</td>
                    <td>${item['unit_cost']:.2f}</td>
                    <td>${item['line_total']:.2f}</td>
                </tr>
            """

        html += f"""
            </table>

            <p><strong>Total:</strong> ${po['total_value']:,.2f}</p>

            <p>Please confirm receipt of this order.</p>
        </body>
        </html>
        """

        return html

    def send_approval_request(self, po):
        """Send approval request for high-value PO"""

        approval_url = f"{self.config['approval_portal_url']}/approve/{po['po_number']}"

        msg = MIMEText(f"""
        Purchase Order {po['po_number']} requires approval.

        Supplier: {po['supplier']}
        Total Value: ${po['total_value']:,.2f}
        Items: {len(po['items'])}

        Approve here: {approval_url}
        """)

        msg['Subject'] = f"PO Approval Required: {po['po_number']}"
        msg['From'] = self.config['email_config']['from_address']
        msg['To'] = self.config['approver_email']

        # Send email (simplified)
        print(f"Approval request sent for PO {po['po_number']}")

    def send_alert(self, message):
        """Send alert notification"""
        print(f"ALERT: {message}")
        # In production: send to monitoring system, email, Slack, etc.

    def run_daily_replenishment(self):
        """
        Main execution: daily automated replenishment cycle
        """

        print(f"\n{'='*60}")
        print(f"Starting Automated Replenishment Cycle")
        print(f"Time: {datetime.now()}")
        print(f"{'='*60}\n")

        try:
            # Step 1: Load inventory data
            print("1. Loading inventory data...")
            self.load_inventory_data('erp_database')

            # Step 2: Calculate reorder needs
            print("2. Calculating reorder needs...")
            reorder_items = self.calculate_reorder_needs()
            print(f"   Found {len(reorder_items)} items needing reorder")

            if len(reorder_items) == 0:
                print("\nNo items need reordering. Cycle complete.")
                return

            # Step 3: Optimize order quantities
            print("3. Optimizing order quantities...")
            reorder_items = self.optimize_order_quantities(reorder_items)

            # Step 4: Generate purchase orders
            print("4. Generating purchase orders...")
            pos_created = self.generate_purchase_orders(reorder_items)
            print(f"   Created {len(pos_created)} purchase orders")

            # Step 5: Summary report
            print("\n" + "="*60)
            print("Replenishment Cycle Summary")
            print("="*60)
            for po in pos_created:
                print(f"PO {po['po_number']}: {po['supplier']} - "
                      f"${po['total_value']:,.2f} - {po['status']}")

            print(f"\nTotal Value: ${sum(po['total_value'] for po in pos_created):,.2f}")
            print("\nCycle completed successfully.\n")

        except Exception as e:
            print(f"\nERROR: Replenishment cycle failed: {e}")
            self.send_alert(f"Replenishment automation failed: {e}")

# Example usage
config = {
    'reorder_point_method': 'dynamic',
    'order_approval_threshold': 10000,
    'supplier_api_endpoints': {
        'Supplier_A': 'https://api.suppliera.com/orders'
    },
    'api_keys': {
        'Supplier_A': 'api_key_123'
    },
    'supplier_emails': {
        'Supplier_B': 'orders@supplierb.com'
    },
    'email_config': {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'from_address': 'automation@company.com',
        'username': 'automation@company.com',
        'password': 'password'
    },
    'approver_email': 'manager@company.com',
    'approval_portal_url': 'https://portal.company.com'
}

# Create and run automation
replenishment = AutomatedReplenishment(config)
replenishment.run_daily_replenishment()
```

---

## Robotic Process Automation (RPA)

### Invoice Processing Automation

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytesseract
from PIL import Image
import pandas as pd
import time

class InvoiceProcessingBot:
    """
    RPA bot to automate invoice processing

    Tasks:
    1. Download invoices from email/portal
    2. Extract data using OCR
    3. Validate against POs
    4. Enter into ERP system
    5. Route for approval if needed
    """

    def __init__(self, config):
        self.config = config
        self.driver = None
        self.invoices_processed = []

    def initialize_browser(self):
        """Initialize web browser for automation"""

        options = webdriver.ChromeOptions()
        if self.config.get('headless', False):
            options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def login_to_portal(self, url, username, password):
        """Login to supplier portal"""

        self.driver.get(url)

        # Wait for login form
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )

        username_field.send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()

        # Wait for dashboard to load
        time.sleep(2)

    def download_invoices(self):
        """Download new invoices from portal"""

        # Navigate to invoices page
        self.driver.find_element(By.LINK_TEXT, "Invoices").click()

        # Find new invoices
        invoice_rows = self.driver.find_elements(
            By.CSS_SELECTOR,
            "tr.invoice-row.status-new"
        )

        downloaded_files = []

        for row in invoice_rows:
            invoice_number = row.find_element(
                By.CSS_SELECTOR,
                ".invoice-number"
            ).text

            download_button = row.find_element(
                By.CSS_SELECTOR,
                ".download-button"
            )

            download_button.click()
            time.sleep(1)  # Wait for download

            downloaded_files.append({
                'invoice_number': invoice_number,
                'file_path': f"/downloads/{invoice_number}.pdf"
            })

        return downloaded_files

    def extract_invoice_data(self, file_path):
        """
        Extract data from invoice using OCR

        Returns structured invoice data
        """

        # Convert PDF to image (simplified)
        # In production, use pdf2image library
        image = Image.open(file_path)

        # OCR
        text = pytesseract.image_to_string(image)

        # Parse extracted text
        invoice_data = self.parse_invoice_text(text)

        return invoice_data

    def parse_invoice_text(self, text):
        """
        Parse OCR text to extract structured data

        Uses regex and NLP to find key fields
        """

        import re

        data = {}

        # Extract invoice number
        inv_match = re.search(r'Invoice #:?\s*(\w+)', text, re.IGNORECASE)
        if inv_match:
            data['invoice_number'] = inv_match.group(1)

        # Extract date
        date_match = re.search(
            r'Date:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            text,
            re.IGNORECASE
        )
        if date_match:
            data['invoice_date'] = date_match.group(1)

        # Extract PO number
        po_match = re.search(r'PO #:?\s*(\w+)', text, re.IGNORECASE)
        if po_match:
            data['po_number'] = po_match.group(1)

        # Extract total amount
        total_match = re.search(
            r'Total:?\s*\$?\s*([\d,]+\.?\d*)',
            text,
            re.IGNORECASE
        )
        if total_match:
            data['total_amount'] = float(total_match.group(1).replace(',', ''))

        # Extract line items (simplified)
        # In production, use more sophisticated parsing
        data['line_items'] = []

        return data

    def validate_invoice(self, invoice_data):
        """
        Validate invoice against PO and business rules

        Checks:
        - PO exists
        - Amounts match
        - Items match
        - Not a duplicate
        """

        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': []
        }

        # Check PO exists
        po = self.lookup_po(invoice_data.get('po_number'))

        if not po:
            validation_results['valid'] = False
            validation_results['errors'].append(
                f"PO {invoice_data.get('po_number')} not found"
            )
            return validation_results

        # Check amount matches (within tolerance)
        tolerance = 0.01  # 1%
        if abs(invoice_data['total_amount'] - po['total']) / po['total'] > tolerance:
            validation_results['warnings'].append(
                f"Amount mismatch: Invoice ${invoice_data['total_amount']:.2f} "
                f"vs PO ${po['total']:.2f}"
            )

        # Check for duplicate
        if self.is_duplicate_invoice(invoice_data['invoice_number']):
            validation_results['valid'] = False
            validation_results['errors'].append(
                f"Duplicate invoice: {invoice_data['invoice_number']}"
            )

        return validation_results

    def lookup_po(self, po_number):
        """Look up PO in ERP system"""
        # In production: query ERP database or API
        # Placeholder return
        return {
            'po_number': po_number,
            'total': 1250.00,
            'items': []
        }

    def is_duplicate_invoice(self, invoice_number):
        """Check if invoice already processed"""
        # In production: query invoice database
        return False

    def enter_invoice_in_erp(self, invoice_data):
        """
        Enter invoice into ERP system

        Uses RPA to navigate ERP interface
        """

        # Navigate to AP module
        self.driver.get(self.config['erp_url'])

        # Wait for page load
        time.sleep(2)

        # Click on Accounts Payable
        self.driver.find_element(By.LINK_TEXT, "Accounts Payable").click()

        # Click New Invoice
        self.driver.find_element(By.ID, "new-invoice-button").click()

        # Fill in invoice fields
        self.driver.find_element(By.ID, "invoice-number").send_keys(
            invoice_data['invoice_number']
        )

        self.driver.find_element(By.ID, "invoice-date").send_keys(
            invoice_data['invoice_date']
        )

        self.driver.find_element(By.ID, "po-number").send_keys(
            invoice_data['po_number']
        )

        self.driver.find_element(By.ID, "total-amount").send_keys(
            str(invoice_data['total_amount'])
        )

        # Add line items
        for item in invoice_data.get('line_items', []):
            # Click add line
            self.driver.find_element(By.ID, "add-line-button").click()

            # Fill line details
            # ... (detailed field entry)

        # Submit invoice
        self.driver.find_element(By.ID, "submit-button").click()

        # Wait for confirmation
        confirmation = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
        )

        return confirmation.text

    def run_invoice_processing(self):
        """
        Main automation workflow
        """

        print("\nStarting Invoice Processing Automation")
        print("="*60)

        try:
            # Initialize browser
            print("1. Initializing browser...")
            self.initialize_browser()

            # Login to supplier portal
            print("2. Logging in to supplier portal...")
            self.login_to_portal(
                self.config['supplier_portal_url'],
                self.config['portal_username'],
                self.config['portal_password']
            )

            # Download invoices
            print("3. Downloading invoices...")
            invoices = self.download_invoices()
            print(f"   Downloaded {len(invoices)} invoices")

            # Process each invoice
            for invoice_file in invoices:
                print(f"\nProcessing {invoice_file['invoice_number']}...")

                # Extract data
                invoice_data = self.extract_invoice_data(invoice_file['file_path'])

                # Validate
                validation = self.validate_invoice(invoice_data)

                if not validation['valid']:
                    print(f"   FAILED validation: {validation['errors']}")
                    # Route for manual review
                    continue

                if validation['warnings']:
                    print(f"   WARNINGS: {validation['warnings']}")
                    # Route for approval
                    continue

                # Enter in ERP
                result = self.enter_invoice_in_erp(invoice_data)
                print(f"   SUCCESS: {result}")

                self.invoices_processed.append({
                    'invoice_number': invoice_data['invoice_number'],
                    'status': 'processed',
                    'timestamp': datetime.now()
                })

            print(f"\n{'='*60}")
            print(f"Processing complete: {len(self.invoices_processed)} invoices")
            print("="*60 + "\n")

        except Exception as e:
            print(f"\nERROR: Automation failed: {e}")

        finally:
            if self.driver:
                self.driver.quit()

# Configuration
config = {
    'headless': False,
    'supplier_portal_url': 'https://portal.supplier.com',
    'portal_username': 'user@company.com',
    'portal_password': 'password',
    'erp_url': 'https://erp.company.com',
    'download_path': '/downloads'
}

# Run automation
bot = InvoiceProcessingBot(config)
# bot.run_invoice_processing()
```

---

## Workflow Orchestration

### Apache Airflow DAG Example

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# Define workflow tasks
def extract_orders_from_erp():
    """Extract new orders from ERP system"""
    print("Extracting orders from ERP...")
    # Implementation
    return {'orders_count': 150}

def validate_inventory():
    """Check inventory availability"""
    print("Validating inventory...")
    # Implementation
    return {'available': True}

def allocate_inventory():
    """Allocate inventory to orders"""
    print("Allocating inventory...")
    # Implementation
    return {'allocated_orders': 145}

def generate_pick_lists():
    """Generate warehouse pick lists"""
    print("Generating pick lists...")
    # Implementation
    return {'pick_lists_created': 145}

def send_to_wms():
    """Send pick lists to WMS"""
    print("Sending to WMS...")
    # Implementation
    return {'status': 'success'}

# Define DAG
default_args = {
    'owner': 'supply-chain',
    'depends_on_past': False,
    'email': ['alerts@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'order_fulfillment_automation',
    default_args=default_args,
    description='Automated order fulfillment workflow',
    schedule_interval='*/15 * * * *',  # Every 15 minutes
    start_date=days_ago(1),
    catchup=False,
    tags=['supply-chain', 'fulfillment']
)

# Define tasks
t1 = PythonOperator(
    task_id='extract_orders',
    python_callable=extract_orders_from_erp,
    dag=dag
)

t2 = PythonOperator(
    task_id='validate_inventory',
    python_callable=validate_inventory,
    dag=dag
)

t3 = PythonOperator(
    task_id='allocate_inventory',
    python_callable=allocate_inventory,
    dag=dag
)

t4 = PythonOperator(
    task_id='generate_pick_lists',
    python_callable=generate_pick_lists,
    dag=dag
)

t5 = PythonOperator(
    task_id='send_to_wms',
    python_callable=send_to_wms,
    dag=dag
)

t6 = EmailOperator(
    task_id='send_completion_email',
    to='operations@company.com',
    subject='Order Fulfillment Workflow Complete',
    html_content='<p>The order fulfillment workflow has completed successfully.</p>',
    dag=dag
)

# Define dependencies
t1 >> t2 >> t3 >> t4 >> t5 >> t6
```

---

## API Integration & Middleware

### REST API Integration

```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
from datetime import datetime

class SupplyChainAPIIntegration:
    """
    Middleware for integrating multiple supply chain systems
    """

    def __init__(self, config):
        self.config = config
        self.session = self.create_session()

    def create_session(self):
        """
        Create requests session with retry logic
        """

        session = requests.Session()

        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS", "POST"],
            backoff_factor=1
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        return session

    def get_erp_orders(self, date_from, date_to):
        """
        Fetch orders from ERP system

        ERP: SAP, Oracle, NetSuite, etc.
        """

        url = f"{self.config['erp_base_url']}/api/orders"

        headers = {
            'Authorization': f"Bearer {self.config['erp_api_token']}",
            'Content-Type': 'application/json'
        }

        params = {
            'date_from': date_from.isoformat(),
            'date_to': date_to.isoformat(),
            'status': 'open'
        }

        response = self.session.get(url, headers=headers, params=params)

        response.raise_for_status()

        return response.json()['orders']

    def check_wms_inventory(self, sku):
        """
        Check inventory levels in WMS

        WMS: Manhattan, Blue Yonder, HighJump, etc.
        """

        url = f"{self.config['wms_base_url']}/api/inventory/{sku}"

        headers = {
            'X-API-Key': self.config['wms_api_key']
        }

        response = self.session.get(url, headers=headers)

        response.raise_for_status()

        inventory_data = response.json()

        return {
            'sku': sku,
            'on_hand': inventory_data['quantity_on_hand'],
            'allocated': inventory_data['quantity_allocated'],
            'available': inventory_data['quantity_available']
        }

    def create_wms_shipment(self, order_data):
        """
        Create shipment in WMS
        """

        url = f"{self.config['wms_base_url']}/api/shipments"

        headers = {
            'X-API-Key': self.config['wms_api_key'],
            'Content-Type': 'application/json'
        }

        payload = {
            'order_number': order_data['order_number'],
            'customer': order_data['customer'],
            'ship_to_address': order_data['shipping_address'],
            'line_items': order_data['items'],
            'priority': order_data.get('priority', 'normal'),
            'requested_ship_date': order_data['requested_ship_date']
        }

        response = self.session.post(url, headers=headers, json=payload)

        response.raise_for_status()

        return response.json()

    def get_tms_rates(self, shipment_details):
        """
        Get shipping rates from TMS

        TMS: MercuryGate, Oracle TMS, Manhattan TMS, etc.
        """

        url = f"{self.config['tms_base_url']}/api/rates/quote"

        headers = {
            'Authorization': f"Bearer {self.config['tms_api_token']}",
            'Content-Type': 'application/json'
        }

        payload = {
            'origin': shipment_details['origin'],
            'destination': shipment_details['destination'],
            'weight': shipment_details['weight'],
            'dimensions': shipment_details['dimensions'],
            'service_type': shipment_details.get('service_type', 'ground')
        }

        response = self.session.post(url, headers=headers, json=payload)

        response.raise_for_status()

        rates = response.json()['rates']

        # Return best rate
        return min(rates, key=lambda x: x['total_cost'])

    def sync_order_status(self, order_number):
        """
        Sync order status across systems

        Ensures ERP, WMS, TMS all have current status
        """

        # Get status from WMS
        wms_status = self.get_wms_order_status(order_number)

        # Update ERP
        self.update_erp_order_status(order_number, wms_status)

        # If shipped, update TMS
        if wms_status['status'] == 'shipped':
            self.update_tms_tracking(order_number, wms_status)

        return wms_status

    def orchestrate_order_fulfillment(self, order_number):
        """
        End-to-end order fulfillment orchestration

        Coordinates across ERP, WMS, TMS
        """

        print(f"\nOrchestrating fulfillment for order {order_number}")

        try:
            # 1. Get order details from ERP
            order = self.get_order_from_erp(order_number)
            print(f"  Order retrieved from ERP")

            # 2. Check inventory in WMS
            inventory_available = True
            for item in order['items']:
                inventory = self.check_wms_inventory(item['sku'])
                if inventory['available'] < item['quantity']:
                    inventory_available = False
                    print(f"  WARNING: Insufficient inventory for {item['sku']}")

            if not inventory_available:
                return {'status': 'backorder'}

            # 3. Create shipment in WMS
            shipment = self.create_wms_shipment(order)
            print(f"  Shipment created in WMS: {shipment['shipment_id']}")

            # 4. Get shipping rates from TMS
            rate = self.get_tms_rates({
                'origin': shipment['origin'],
                'destination': order['shipping_address'],
                'weight': shipment['total_weight'],
                'dimensions': shipment['dimensions']
            })
            print(f"  Best shipping rate: ${rate['total_cost']:.2f}")

            # 5. Update ERP with shipping info
            self.update_erp_order(order_number, {
                'shipment_id': shipment['shipment_id'],
                'carrier': rate['carrier'],
                'freight_cost': rate['total_cost'],
                'status': 'in_fulfillment'
            })
            print(f"  ERP updated with shipment details")

            return {
                'status': 'success',
                'shipment_id': shipment['shipment_id'],
                'freight_cost': rate['total_cost']
            }

        except Exception as e:
            print(f"  ERROR: {e}")
            return {'status': 'error', 'message': str(e)}

# Configuration
config = {
    'erp_base_url': 'https://erp.company.com',
    'erp_api_token': 'erp_token_123',
    'wms_base_url': 'https://wms.company.com',
    'wms_api_key': 'wms_key_456',
    'tms_base_url': 'https://tms.company.com',
    'tms_api_token': 'tms_token_789'
}

# Example usage
integration = SupplyChainAPIIntegration(config)
result = integration.orchestrate_order_fulfillment('ORDER-12345')
print(f"\nResult: {result}")
```

---

## Tools & Technologies

### RPA Platforms

**Commercial:**
- **UiPath**: Leading RPA platform
- **Blue Prism**: Enterprise RPA
- **Automation Anywhere**: Cloud-native RPA
- **Microsoft Power Automate**: Microsoft ecosystem integration
- **WorkFusion**: AI-powered automation

**Open Source:**
- **Robot Framework**: Generic automation framework
- **Selenium**: Web browser automation
- **Puppeteer**: Node.js browser automation
- **TagUI**: RPA tool for automating websites

### Workflow Orchestration

**Apache Airflow**: Python-based workflow orchestration
**Prefect**: Modern workflow orchestration
**Luigi (Spotify)**: Python workflow engine
**Dagster**: Data orchestration platform
**n8n**: Workflow automation (low-code)
**Zapier**: No-code automation (SaaS)
**Make (Integromat)**: Visual automation platform

### API Integration

**Python Libraries:**
- `requests`: HTTP library
- `httpx`: Async HTTP client
- `aiohttp`: Async HTTP client/server
- `fastapi`: Build APIs
- `celery`: Distributed task queue

**iPaaS (Integration Platform as a Service):**
- **MuleSoft**: Enterprise integration
- **Dell Boomi**: Cloud integration
- **Informatica**: Data integration
- **Jitterbit**: Integration platform
- **Workato**: Enterprise automation

---

## Common Challenges & Solutions

### Challenge: System Downtime and Failures

**Problem:**
- Automated processes fail when systems are down
- No manual fallback
- Data inconsistency

**Solutions:**
- Implement retry logic with exponential backoff
- Circuit breaker pattern
- Health checks and monitoring
- Fallback to manual process
- Queue-based processing (can resume after downtime)
- Comprehensive error logging

### Challenge: Change Management

**Problem:**
- UI changes break RPA bots
- API versioning issues
- Business process changes

**Solutions:**
- Use APIs instead of UI automation when possible
- Modular design (easy to update components)
- Version control for automation scripts
- Regular maintenance schedule
- Monitoring for automation failures
- Documentation of dependencies

### Challenge: Data Quality Issues

**Problem:**
- Bad data causes automation failures
- Garbage in, garbage out

**Solutions:**
- Input validation before processing
- Data quality checks
- Exception handling and alerts
- Human review for edge cases
- Data cleansing preprocessing
- Clear business rules for data standards

### Challenge: Security and Compliance

**Problem:**
- Bots have access to sensitive systems
- Audit trail concerns
- Regulatory compliance

**Solutions:**
- Principle of least privilege (minimal access)
- Credential vaulting (no hardcoded passwords)
- Comprehensive logging of all actions
- Regular security audits
- Encryption of sensitive data
- Compliance with SOX, GDPR, etc.

---

## Output Format

### Automation Project Report

**Executive Summary:**
- Process automated
- Expected benefits (time savings, cost reduction, accuracy)
- Implementation timeline
- ROI analysis

**Current State Analysis:**
- Process description
- Volume and frequency
- Current pain points
- Time and cost metrics

**Solution Design:**
- Automation approach
- Systems integrated
- Workflow diagram
- Exception handling

**Implementation Plan:**

| Phase | Activities | Duration | Resources |
|-------|-----------|----------|-----------|
| 1. Setup | Tool installation, access provisioning | 2 weeks | IT, 1 developer |
| 2. Development | Bot development, testing | 4 weeks | 2 developers |
| 3. UAT | User acceptance testing | 2 weeks | Business users |
| 4. Deployment | Production deployment, monitoring | 1 week | IT, developers |
| 5. Support | Hypercare, optimization | 4 weeks | Support team |

**Business Case:**

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Process Time | 4 hours/day | 30 min/day | 88% reduction |
| Error Rate | 5% | 0.5% | 90% reduction |
| FTE Required | 1.0 | 0.25 | 0.75 FTE saved |
| Annual Cost | $80,000 | $20,000 | $60,000 savings |

**ROI:**
- Investment: $150,000 (development + infrastructure)
- Annual Savings: $60,000
- Payback Period: 2.5 years
- 3-Year ROI: 20%

---

## Questions to Ask

If you need more context:
1. What process needs automation?
2. What's the current process? (manual steps, systems involved)
3. What's the volume and frequency? (1000 transactions/day, hourly)
4. What systems are involved? (ERP, WMS, TMS, spreadsheets)
5. Are APIs available or screen scraping needed?
6. What's the expected ROI and timeline?
7. Are there compliance or security requirements?
8. Who will maintain the automation?

---

## Related Skills

- **supply-chain-analytics**: For monitoring automation performance
- **digital-twin-modeling**: For simulating automated processes
- **ml-supply-chain**: For intelligent automation with ML
- **prescriptive-analytics**: For automated decision-making
- **optimization-modeling**: For optimizing automated workflows
- **demand-forecasting**: For automated replenishment
- **inventory-optimization**: For automated reorder triggers
- **order-fulfillment**: For fulfillment automation
