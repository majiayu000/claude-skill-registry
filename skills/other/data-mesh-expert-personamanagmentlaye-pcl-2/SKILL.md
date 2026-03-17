---
name: data-mesh-expert
version: 1.0.0
description: Expert-level data mesh architecture, domain-oriented ownership, data products, federated governance, and self-serve platforms
category: data
author: PCL Team
license: Apache-2.0
tags:
  - data-mesh
  - architecture
  - domain-driven
  - data-products
  - governance
  - platform
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Data Mesh Expert

You are an expert in data mesh architecture with deep knowledge of domain-oriented data ownership, data as a product, federated computational governance, and self-serve data infrastructure platforms. You design and implement decentralized data architectures that scale with organizational growth.

## Core Expertise

### Data Mesh Principles

**Four Foundational Principles:**

1. **Domain-Oriented Decentralized Data Ownership**
2. **Data as a Product**
3. **Self-Serve Data Infrastructure as a Platform**
4. **Federated Computational Governance**

### Domain-Oriented Data Ownership

**Domain Decomposition:**
```yaml
# Domain structure
organization:
  domains:
    - name: sales
      bounded_context: "Customer transactions and revenue"
      data_products:
        - sales_orders
        - customer_interactions
        - revenue_metrics
      team:
        product_owner: "Sales Analytics Lead"
        data_engineers: 3
        analytics_engineers: 2

    - name: marketing
      bounded_context: "Customer acquisition and campaigns"
      data_products:
        - campaign_performance
        - lead_attribution
        - customer_segments
      team:
        product_owner: "Marketing Analytics Lead"
        data_engineers: 2
        analytics_engineers: 2

    - name: product
      bounded_context: "Product usage and features"
      data_products:
        - feature_usage
        - product_events
        - user_engagement
      team:
        product_owner: "Product Analytics Lead"
        data_engineers: 3
        analytics_engineers: 1

    - name: finance
      bounded_context: "Financial reporting and compliance"
      data_products:
        - general_ledger
        - accounts_receivable
        - financial_metrics
      team:
        product_owner: "Finance Analytics Lead"
        data_engineers: 2
        analytics_engineers: 2
```

**Domain Data Product Architecture:**
```
Sales Domain
├── Operational Data
│   ├── PostgreSQL: orders, customers, transactions
│   └── Salesforce: opportunities, accounts
├── Analytical Data Products
│   ├── sales_orders_analytical (daily aggregate)
│   ├── customer_lifetime_value (computed metric)
│   └── sales_performance_metrics (real-time)
├── Data Product APIs
│   ├── REST API: /api/v1/sales/orders
│   ├── GraphQL: sales_orders query
│   └── Streaming: kafka://sales.orders.events
└── Documentation
    ├── README.md (product overview)
    ├── SCHEMA.md (data contracts)
    ├── SLA.md (quality guarantees)
    └── CHANGELOG.md (version history)
```

### Data as a Product

**Data Product Contract:**
```yaml
# data_product.yaml
name: sales_orders_analytical
version: 2.1.0
domain: sales
owner:
  team: sales-analytics
  contact: sales-analytics@company.com
  slack: #sales-data

description: |
  Analytical view of sales orders with customer and product enrichments.
  Updated daily at 2 AM UTC with full refresh.

schema:
  type: parquet
  location: s3://data-products/sales/orders/
  partitioned_by:
    - order_date
  fields:
    - name: order_id
      type: string
      description: Unique order identifier
      constraints:
        - unique
        - not_null
    - name: customer_id
      type: string
      description: Customer identifier
      constraints:
        - not_null
    - name: order_date
      type: date
      description: Date order was placed
      constraints:
        - not_null
    - name: total_amount
      type: decimal(12,2)
      description: Total order amount in USD
      constraints:
        - not_null
        - min: 0
    - name: status
      type: string
      description: Order status
      constraints:
        - in: [pending, completed, cancelled, refunded]
    - name: customer_segment
      type: string
      description: Customer value segment
    - name: product_count
      type: integer
      description: Number of products in order

access:
  discovery: public
  read:
    - role: analyst
    - role: data_scientist
    - domain: marketing
    - domain: finance
  write:
    - domain: sales

sla:
  availability: 99.9%
  freshness:
    max_age_hours: 24
    update_schedule: "0 2 * * *"
  completeness:
    min_threshold: 99.5%
  quality_checks:
    - name: no_negative_amounts
      query: "SELECT COUNT(*) FROM orders WHERE total_amount < 0"
      threshold: 0
    - name: valid_status
      query: "SELECT COUNT(*) FROM orders WHERE status NOT IN ('pending', 'completed', 'cancelled', 'refunded')"
      threshold: 0
    - name: referential_integrity
      query: "SELECT COUNT(*) FROM orders o LEFT JOIN customers c ON o.customer_id = c.id WHERE c.id IS NULL"
      threshold: 0

observability:
  metrics:
    - row_count
    - avg_order_value
    - null_percentage_by_column
    - schema_drift
  alerts:
    - type: freshness
      condition: age_hours > 26
      severity: critical
    - type: volume
      condition: row_count_change > 50%
      severity: warning
    - type: quality
      condition: quality_check_failed
      severity: critical

changelog:
  - version: 2.1.0
    date: 2024-01-15
    changes:
      - Added customer_segment field
      - Improved null handling in total_amount
    breaking: false
  - version: 2.0.0
    date: 2023-12-01
    changes:
      - Changed order_id from integer to string
      - Removed legacy status values
    breaking: true
```

**Data Product Implementation (Python):**
```python
# sales_orders_data_product.py
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd
from great_expectations.core import ExpectationSuite

@dataclass
class DataProductMetadata:
    """Metadata for data product"""
    name: str
    version: str
    domain: str
    owner_team: str
    description: str
    sla_freshness_hours: int
    sla_availability_pct: float

@dataclass
class DataProductQualityCheck:
    """Quality check definition"""
    name: str
    query: str
    threshold: int
    severity: str

class SalesOrdersDataProduct:
    """Sales orders analytical data product"""

    def __init__(self, config: Dict):
        self.config = config
        self.metadata = DataProductMetadata(
            name="sales_orders_analytical",
            version="2.1.0",
            domain="sales",
            owner_team="sales-analytics",
            description="Analytical view of sales orders",
            sla_freshness_hours=24,
            sla_availability_pct=99.9
        )
        self.quality_checks = self._load_quality_checks()

    def _load_quality_checks(self) -> List[DataProductQualityCheck]:
        """Load quality checks from config"""
        return [
            DataProductQualityCheck(
                name="no_negative_amounts",
                query="SELECT COUNT(*) FROM orders WHERE total_amount < 0",
                threshold=0,
                severity="critical"
            ),
            DataProductQualityCheck(
                name="valid_status",
                query="SELECT COUNT(*) FROM orders WHERE status NOT IN ('pending', 'completed', 'cancelled', 'refunded')",
                threshold=0,
                severity="critical"
            ),
            DataProductQualityCheck(
                name="referential_integrity",
                query="SELECT COUNT(*) FROM orders o LEFT JOIN customers c ON o.customer_id = c.id WHERE c.id IS NULL",
                threshold=0,
                severity="critical"
            )
        ]

    def extract(self) -> pd.DataFrame:
        """Extract source data"""
        # Extract from operational database
        orders_df = self._extract_orders()
        customers_df = self._extract_customers()
        products_df = self._extract_products()

        return orders_df, customers_df, products_df

    def transform(self, orders_df: pd.DataFrame,
                  customers_df: pd.DataFrame,
                  products_df: pd.DataFrame) -> pd.DataFrame:
        """Transform and enrich data"""

        # Join with customers
        enriched = orders_df.merge(
            customers_df[['customer_id', 'customer_segment']],
            on='customer_id',
            how='left'
        )

        # Calculate product count per order
        product_counts = products_df.groupby('order_id').size().reset_index(name='product_count')
        enriched = enriched.merge(product_counts, on='order_id', how='left')

        # Apply business logic
        enriched['product_count'] = enriched['product_count'].fillna(0)

        return enriched

    def validate(self, df: pd.DataFrame) -> Dict:
        """Validate data quality"""
        results = {
            'passed': True,
            'checks': []
        }

        # Schema validation
        expected_columns = [
            'order_id', 'customer_id', 'order_date', 'total_amount',
            'status', 'customer_segment', 'product_count'
        ]
        missing_columns = set(expected_columns) - set(df.columns)
        if missing_columns:
            results['passed'] = False
            results['checks'].append({
                'name': 'schema_validation',
                'passed': False,
                'message': f"Missing columns: {missing_columns}"
            })

        # Quality checks
        for check in self.quality_checks:
            result = self._run_quality_check(df, check)
            results['checks'].append(result)
            if not result['passed']:
                results['passed'] = False

        return results

    def _run_quality_check(self, df: pd.DataFrame,
                           check: DataProductQualityCheck) -> Dict:
        """Run individual quality check"""
        # Execute quality check query
        # This is simplified; in practice, use SQL engine
        if check.name == "no_negative_amounts":
            count = len(df[df['total_amount'] < 0])
        elif check.name == "valid_status":
            valid_statuses = ['pending', 'completed', 'cancelled', 'refunded']
            count = len(df[~df['status'].isin(valid_statuses)])
        else:
            count = 0

        passed = count <= check.threshold

        return {
            'name': check.name,
            'passed': passed,
            'count': count,
            'threshold': check.threshold,
            'severity': check.severity
        }

    def publish(self, df: pd.DataFrame) -> None:
        """Publish data product"""
        # Write to storage
        output_path = f"s3://data-products/sales/orders/"
        df.to_parquet(
            output_path,
            partition_cols=['order_date'],
            engine='pyarrow'
        )

        # Register in data catalog
        self._register_in_catalog(output_path)

        # Update metrics
        self._publish_metrics(df)

    def _register_in_catalog(self, path: str) -> None:
        """Register data product in catalog"""
        catalog_entry = {
            'name': self.metadata.name,
            'version': self.metadata.version,
            'domain': self.metadata.domain,
            'location': path,
            'last_updated': datetime.utcnow().isoformat(),
            'owner': self.metadata.owner_team
        }
        # Register with data catalog service
        pass

    def _publish_metrics(self, df: pd.DataFrame) -> None:
        """Publish observability metrics"""
        metrics = {
            'row_count': len(df),
            'avg_order_value': df['total_amount'].mean(),
            'null_percentage': df.isnull().sum().to_dict(),
            'timestamp': datetime.utcnow().isoformat()
        }
        # Send to monitoring system
        pass

    def get_metadata(self) -> Dict:
        """Return data product metadata"""
        return {
            'name': self.metadata.name,
            'version': self.metadata.version,
            'domain': self.metadata.domain,
            'owner': self.metadata.owner_team,
            'description': self.metadata.description,
            'sla': {
                'freshness_hours': self.metadata.sla_freshness_hours,
                'availability_pct': self.metadata.sla_availability_pct
            }
        }
```

### Self-Serve Data Infrastructure Platform

**Platform Components:**
```yaml
# Platform architecture
platform:
  compute:
    - name: spark_cluster
      type: databricks
      purpose: Large-scale transformations
      auto_scaling: true

    - name: dbt_runner
      type: kubernetes
      purpose: SQL transformations
      resources:
        cpu: 4
        memory: 16Gi

  storage:
    - name: data_lake
      type: s3
      purpose: Raw and processed data
      lifecycle_policies:
        - transition_to_glacier: 90_days
        - expire: 365_days

    - name: data_warehouse
      type: snowflake
      purpose: Analytical queries
      auto_suspend: 10_minutes

  orchestration:
    - name: airflow
      type: managed_airflow
      purpose: Workflow orchestration
      version: 2.8.0

  data_catalog:
    - name: datahub
      purpose: Metadata management
      features:
        - lineage_tracking
        - data_discovery
        - schema_registry

  quality:
    - name: great_expectations
      purpose: Data validation
      integration: airflow

  observability:
    - name: datadog
      purpose: Metrics and monitoring
      dashboards:
        - data_product_health
        - pipeline_performance

  access_control:
    - name: okta
      type: identity_provider
      integration: sso

    - name: ranger
      type: authorization
      purpose: Fine-grained access control
```

**Platform APIs:**
```python
# platform_api.py
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class DataProductSpec:
    """Specification for creating data product"""
    name: str
    domain: str
    source_tables: List[str]
    transformation_sql: str
    schedule: str
    quality_checks: List[Dict]

class DataMeshPlatform:
    """Self-serve data mesh platform API"""

    def create_data_product(self, spec: DataProductSpec) -> str:
        """
        Create new data product with platform automation

        Steps:
        1. Provision compute resources
        2. Create storage location
        3. Deploy transformation pipeline
        4. Configure quality checks
        5. Register in catalog
        6. Set up monitoring
        """
        # Generate unique ID
        product_id = f"{spec.domain}_{spec.name}"

        # Create storage location
        storage_path = self._provision_storage(product_id)

        # Deploy dbt project
        dbt_project = self._create_dbt_project(spec)
        self._deploy_dbt_project(dbt_project)

        # Create Airflow DAG
        dag = self._create_airflow_dag(spec, storage_path)
        self._deploy_dag(dag)

        # Register in catalog
        self._register_in_catalog(product_id, spec, storage_path)

        # Set up monitoring
        self._setup_monitoring(product_id, spec)

        return product_id

    def _provision_storage(self, product_id: str) -> str:
        """Provision storage for data product"""
        path = f"s3://data-products/{product_id}/"
        # Create S3 bucket/prefix
        # Set lifecycle policies
        # Configure access control
        return path

    def _create_dbt_project(self, spec: DataProductSpec) -> Dict:
        """Generate dbt project for data product"""
        return {
            'name': spec.name,
            'models': {
                f"{spec.name}.sql": spec.transformation_sql
            },
            'tests': self._generate_dbt_tests(spec.quality_checks),
            'docs': self._generate_dbt_docs(spec)
        }

    def _create_airflow_dag(self, spec: DataProductSpec, storage_path: str) -> str:
        """Generate Airflow DAG for data product"""
        dag_template = f"""
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

dag = DAG(
    dag_id='{spec.name}_pipeline',
    schedule='{spec.schedule}',
    start_date=datetime(2024, 1, 1),
    catchup=False
)

dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='dbt run --models {spec.name}',
    dag=dag
)

dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command='dbt test --models {spec.name}',
    dag=dag
)

publish = BashOperator(
    task_id='publish',
    bash_command='python publish_data_product.py {spec.name} {storage_path}',
    dag=dag
)

dbt_run >> dbt_test >> publish
        """
        return dag_template

    def get_data_product(self, product_id: str) -> Dict:
        """Retrieve data product information"""
        return self._catalog.get(product_id)

    def list_data_products(self, domain: Optional[str] = None) -> List[Dict]:
        """List available data products"""
        products = self._catalog.search(domain=domain)
        return products

    def discover_data_products(self, query: str) -> List[Dict]:
        """Search for data products"""
        return self._catalog.search(query=query)

    def request_access(self, product_id: str, requester: str) -> str:
        """Request access to data product"""
        # Create access request ticket
        # Notify data product owner
        # Track approval workflow
        pass

    def grant_access(self, product_id: str, user: str, access_level: str):
        """Grant access to data product"""
        # Update IAM policies
        # Configure row-level security
        # Log access grant
        pass
```

### Federated Computational Governance

**Governance Framework:**
```yaml
# governance_policy.yaml
governance:
  global_policies:
    - name: data_classification
      mandatory: true
      policy: |
        All data products must be classified as:
        - Public: Freely accessible within organization
        - Internal: Restricted to employees
        - Confidential: Restricted to specific roles
        - Restricted: Requires explicit approval

    - name: pii_handling
      mandatory: true
      policy: |
        Data products containing PII must:
        - Mark PII fields in schema
        - Implement column-level encryption
        - Enable audit logging
        - Comply with GDPR/CCPA requirements

    - name: data_retention
      mandatory: true
      policy: |
        Data retention periods:
        - Operational data: 7 years
        - Analytical data: 3 years
        - Logs: 1 year
        - Deleted data: 30 days in trash

  domain_policies:
    sales:
      data_quality:
        - completeness: ">= 99%"
        - accuracy: ">= 99.5%"
        - freshness: "<= 24 hours"
      access_control:
        - default_access: internal
        - pii_fields: [customer_email, customer_phone]
        - approval_required: [customer_ssn]

    finance:
      data_quality:
        - completeness: ">= 99.9%"
        - accuracy: ">= 99.99%"
        - freshness: "<= 1 hour"
      access_control:
        - default_access: confidential
        - sox_compliance: true
        - audit_all_access: true

  automated_policies:
    - name: schema_validation
      enforcement: pre-publish
      check: |
        Schema must include:
        - Primary key
        - Column descriptions
        - Data types
        - Constraints

    - name: quality_gates
      enforcement: pre-publish
      check: |
        All quality checks must pass:
        - No critical failures
        - Warning threshold: <= 5%

    - name: breaking_changes
      enforcement: pre-publish
      check: |
        Breaking changes require:
        - Major version increment
        - 30-day deprecation notice
        - Migration guide

  observability_requirements:
    - metrics:
        - row_count
        - null_rate
        - distinct_count
        - value_distribution
    - alerts:
        - freshness_violation
        - quality_check_failure
        - schema_drift
        - volume_anomaly
```

**Governance Implementation:**
```python
# governance_engine.py
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class PolicyViolationSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class PolicyViolation:
    policy_name: str
    severity: PolicyViolationSeverity
    message: str
    field: Optional[str] = None

class GovernanceEngine:
    """Automated governance enforcement"""

    def __init__(self, policies: Dict):
        self.policies = policies

    def validate_data_product(self, product_spec: Dict) -> List[PolicyViolation]:
        """Validate data product against governance policies"""
        violations = []

        # Check data classification
        violations.extend(self._check_data_classification(product_spec))

        # Check PII handling
        violations.extend(self._check_pii_compliance(product_spec))

        # Check schema requirements
        violations.extend(self._check_schema_requirements(product_spec))

        # Check quality checks
        violations.extend(self._check_quality_requirements(product_spec))

        # Check retention policy
        violations.extend(self._check_retention_policy(product_spec))

        return violations

    def _check_data_classification(self, product_spec: Dict) -> List[PolicyViolation]:
        """Verify data classification is set"""
        violations = []

        if 'classification' not in product_spec:
            violations.append(PolicyViolation(
                policy_name="data_classification",
                severity=PolicyViolationSeverity.ERROR,
                message="Data classification not specified"
            ))

        valid_classifications = ['public', 'internal', 'confidential', 'restricted']
        if product_spec.get('classification') not in valid_classifications:
            violations.append(PolicyViolation(
                policy_name="data_classification",
                severity=PolicyViolationSeverity.ERROR,
                message=f"Invalid classification. Must be one of: {valid_classifications}"
            ))

        return violations

    def _check_pii_compliance(self, product_spec: Dict) -> List[PolicyViolation]:
        """Check PII handling compliance"""
        violations = []

        schema = product_spec.get('schema', {})
        pii_fields = [f for f in schema.get('fields', []) if f.get('is_pii')]

        if pii_fields:
            # Check encryption
            if not product_spec.get('encryption_enabled'):
                violations.append(PolicyViolation(
                    policy_name="pii_handling",
                    severity=PolicyViolationSeverity.CRITICAL,
                    message="PII fields present but encryption not enabled"
                ))

            # Check audit logging
            if not product_spec.get('audit_logging_enabled'):
                violations.append(PolicyViolation(
                    policy_name="pii_handling",
                    severity=PolicyViolationSeverity.CRITICAL,
                    message="PII fields present but audit logging not enabled"
                ))

            # Check field marking
            for field in pii_fields:
                if not field.get('pii_category'):
                    violations.append(PolicyViolation(
                        policy_name="pii_handling",
                        severity=PolicyViolationSeverity.ERROR,
                        message=f"PII field {field['name']} missing pii_category",
                        field=field['name']
                    ))

        return violations

    def _check_schema_requirements(self, product_spec: Dict) -> List[PolicyViolation]:
        """Validate schema completeness"""
        violations = []

        schema = product_spec.get('schema', {})
        if not schema:
            violations.append(PolicyViolation(
                policy_name="schema_validation",
                severity=PolicyViolationSeverity.ERROR,
                message="Schema not defined"
            ))
            return violations

        # Check for primary key
        fields = schema.get('fields', [])
        has_primary_key = any(f.get('is_primary_key') for f in fields)
        if not has_primary_key:
            violations.append(PolicyViolation(
                policy_name="schema_validation",
                severity=PolicyViolationSeverity.WARNING,
                message="No primary key defined"
            ))

        # Check field documentation
        for field in fields:
            if not field.get('description'):
                violations.append(PolicyViolation(
                    policy_name="schema_validation",
                    severity=PolicyViolationSeverity.WARNING,
                    message=f"Field {field['name']} missing description",
                    field=field['name']
                ))

        return violations

    def _check_quality_requirements(self, product_spec: Dict) -> List[PolicyViolation]:
        """Validate quality check configuration"""
        violations = []

        quality_checks = product_spec.get('sla', {}).get('quality_checks', [])
        if not quality_checks:
            violations.append(PolicyViolation(
                policy_name="quality_gates",
                severity=PolicyViolationSeverity.WARNING,
                message="No quality checks defined"
            ))

        # Check for minimum required checks
        check_names = [check['name'] for check in quality_checks]
        required_checks = ['completeness', 'freshness']
        missing_checks = set(required_checks) - set(check_names)

        if missing_checks:
            violations.append(PolicyViolation(
                policy_name="quality_gates",
                severity=PolicyViolationSeverity.WARNING,
                message=f"Missing required quality checks: {missing_checks}"
            ))

        return violations

    def _check_retention_policy(self, product_spec: Dict) -> List[PolicyViolation]:
        """Validate retention policy"""
        violations = []

        if 'retention_days' not in product_spec:
            violations.append(PolicyViolation(
                policy_name="data_retention",
                severity=PolicyViolationSeverity.ERROR,
                message="Retention policy not specified"
            ))

        return violations

    def enforce_policies(self, violations: List[PolicyViolation]) -> bool:
        """Determine if data product can be published based on violations"""
        # Block on ERROR or CRITICAL violations
        blocking_violations = [
            v for v in violations
            if v.severity in [PolicyViolationSeverity.ERROR, PolicyViolationSeverity.CRITICAL]
        ]

        return len(blocking_violations) == 0

    def generate_compliance_report(self, product_id: str) -> Dict:
        """Generate compliance report for data product"""
        return {
            'product_id': product_id,
            'compliance_status': 'compliant',
            'last_checked': datetime.utcnow().isoformat(),
            'policies_evaluated': len(self.policies),
            'violations': []
        }
```

## Best Practices

### 1. Domain Design
- Align domains with organizational structure
- Clear bounded contexts for each domain
- Domain teams own their data end-to-end
- Cross-domain collaboration through well-defined interfaces
- Avoid centralized data teams; embed in domains

### 2. Data Product Design
- Treat data as a product with SLAs
- Document data contracts explicitly
- Version data products semantically
- Implement comprehensive quality checks
- Provide discoverability and self-service access
- Monitor data product health continuously

### 3. Platform Design
- Abstract infrastructure complexity
- Provide self-serve capabilities
- Automate repetitive tasks
- Enable domain autonomy
- Standardize common patterns
- Invest in developer experience

### 4. Governance
- Automate policy enforcement
- Make governance policies executable
- Balance autonomy with control
- Federate decisions to domains
- Global standards, local implementation
- Continuous compliance monitoring

### 5. Cultural Transformation
- Shift from centralized to federated model
- Build data literacy across organization
- Incentivize data product quality
- Foster collaboration between domains
- Celebrate data product owners

## Anti-Patterns

### 1. Centralized Data Team
```
// Bad: Central data team owns all data
Central Team -> All domains (bottleneck)

// Good: Domain teams own their data
Sales Domain -> Sales data products
Marketing Domain -> Marketing data products
Product Domain -> Product data products
```

### 2. Monolithic Data Lake
```
// Bad: Single giant data lake
s3://data-lake/everything/

// Good: Domain-oriented storage
s3://data-products/sales/
s3://data-products/marketing/
s3://data-products/product/
```

### 3. No Data Contracts
```
// Bad: Undocumented schema changes
Breaking change deployed without notice

// Good: Versioned contracts with deprecation
v1: Deprecated (30 days notice)
v2: Current
v3: Beta
```

### 4. Manual Governance
```
// Bad: Manual approval processes
Email -> Ticket -> Manual review -> Access granted (weeks)

// Good: Automated governance
Request -> Policy check -> Auto-approval (minutes)
```

## Resources

- [Data Mesh by Zhamak Dehghani](https://www.oreilly.com/library/view/data-mesh/9781492092384/)
- [Data Mesh Principles](https://martinfowler.com/articles/data-mesh-principles.html)
- [ThoughtWorks Data Mesh](https://www.thoughtworks.com/en-us/what-we-do/data-and-ai/data-mesh)
- [Data Mesh Architecture](https://www.datamesh-architecture.com/)
- [Data Product Canvas](https://www.datamesh-architecture.com/data-product-canvas)
- [Data Mesh Learning](https://datameshlearning.com/)
- [Awesome Data Mesh](https://github.com/jhole89/awesome-data-mesh)
