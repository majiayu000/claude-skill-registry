---
name: "security-review-construction"
description: "Security review checklist for construction software systems. Use when building integrations, APIs, data pipelines, or dashboards for construction projects."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🛡️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Security Review Skill for Construction Systems

This skill ensures all construction software systems follow security best practices, protecting sensitive project data, financial information, and business intelligence.

## When to Activate

- Building ERP/BIM system integrations
- Creating construction dashboards
- Handling cost/financial data
- Building document management systems
- Creating APIs for field data collection
- Integrating with external platforms (Procore, PlanGrid, etc.)
- Working with subcontractor/vendor data
- Processing payment applications

## Construction-Specific Security Concerns

### 1. Financial Data Protection

```python
# CRITICAL: Construction financial data security

# ❌ NEVER Do This
project_budget = 15000000  # Hardcoded in source
margin_percentage = 0.18   # Business-sensitive info in code

# ✅ ALWAYS Do This
import os
from cryptography.fernet import Fernet

# Load from secure configuration
project_config = load_secure_config(os.environ['PROJECT_CONFIG_PATH'])

# Encrypt sensitive data at rest
def encrypt_financial_data(data: dict) -> bytes:
    key = os.environ.get('ENCRYPTION_KEY')
    f = Fernet(key)
    return f.encrypt(json.dumps(data).encode())
```

#### Financial Data Checklist
- [ ] Cost estimates encrypted at rest
- [ ] Margin/markup data not exposed in logs
- [ ] Payment information tokenized
- [ ] Historical pricing protected from competitors
- [ ] Bid amounts secured until opening

### 2. BIM/CAD Data Security

```python
# BIM data often contains proprietary design information

# ❌ NEVER store BIM directly in public cloud without encryption
s3.upload_file('model.ifc', bucket='public-bucket')

# ✅ ALWAYS encrypt and control access
def upload_bim_secure(file_path: str, project_id: str):
    # Encrypt file
    encrypted_path = encrypt_file(file_path)

    # Generate pre-signed URL with expiration
    presigned_url = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': 'secure-bim-bucket',
            'Key': f'{project_id}/{os.path.basename(file_path)}'
        },
        ExpiresIn=3600  # 1 hour expiration
    )

    # Log access
    audit_log.info(f"BIM access granted: {project_id}")

    return presigned_url
```

#### BIM/CAD Checklist
- [ ] IFC/RVT files encrypted at rest
- [ ] Access logged for audit trail
- [ ] Time-limited download links
- [ ] Version control with access tracking
- [ ] No design data in error messages

### 3. Subcontractor/Vendor Data

```python
# Subcontractor data includes business-sensitive information

class SubcontractorDataHandler:
    """Secure handling of subcontractor data"""

    # Fields that require encryption
    SENSITIVE_FIELDS = [
        'insurance_policy_number',
        'bank_account',
        'tax_id',
        'bonding_capacity',
        'historical_pricing'
    ]

    def store_subcontractor(self, data: dict) -> str:
        # Encrypt sensitive fields
        for field in self.SENSITIVE_FIELDS:
            if field in data:
                data[field] = self.encrypt(data[field])

        # Store with audit trail
        sub_id = self.db.insert(data)
        self.audit.log(f"Subcontractor created: {sub_id}")

        return sub_id

    def get_subcontractor(self, sub_id: str, requester_id: str) -> dict:
        # Check authorization
        if not self.can_access(requester_id, sub_id):
            raise PermissionError("Unauthorized access to subcontractor data")

        # Log access
        self.audit.log(f"Subcontractor accessed: {sub_id} by {requester_id}")

        # Return with decrypted sensitive fields (only to authorized users)
        return self.decrypt_sensitive_fields(self.db.get(sub_id))
```

#### Vendor Data Checklist
- [ ] Insurance/bonding information encrypted
- [ ] Bank details protected (PCI compliance)
- [ ] Tax IDs masked in UI (show last 4 digits only)
- [ ] Pricing history access-controlled
- [ ] Certificate expiration notifications secure

### 4. Field Data Collection Security

```python
# Mobile/field data collection must be secure

from datetime import datetime, timedelta
import hashlib

class FieldDataCollector:
    """Secure field data collection"""

    def validate_photo_submission(self, photo_data: dict) -> bool:
        # Verify GPS timestamp is recent (within 24 hours)
        photo_time = datetime.fromisoformat(photo_data['timestamp'])
        if datetime.now() - photo_time > timedelta(hours=24):
            raise ValueError("Photo timestamp too old - possible replay attack")

        # Verify file hash matches
        file_hash = hashlib.sha256(photo_data['content']).hexdigest()
        if file_hash != photo_data['declared_hash']:
            raise ValueError("File integrity check failed")

        # Validate GPS coordinates are within project boundary
        if not self.is_within_project_bounds(
            photo_data['lat'],
            photo_data['lon'],
            photo_data['project_id']
        ):
            self.audit.warn(f"Photo from outside project bounds: {photo_data}")

        return True

    def submit_daily_report(self, report: dict, user_id: str) -> str:
        # Verify user is assigned to project
        if not self.is_assigned_to_project(user_id, report['project_id']):
            raise PermissionError("User not assigned to this project")

        # Sign report with user credentials
        report['signature'] = self.sign_report(report, user_id)
        report['submitted_at'] = datetime.now().isoformat()

        return self.db.insert(report)
```

#### Field Data Checklist
- [ ] GPS data validated for reasonableness
- [ ] Photo timestamps verified
- [ ] File integrity checks (hashing)
- [ ] User authentication for submissions
- [ ] Offline data sync secured

### 5. CWICR Database Security

```python
# CWICR contains proprietary cost data

class CWICRAccessControl:
    """Access control for CWICR database"""

    TIERS = {
        'basic': ['public_rates', 'standard_descriptions'],
        'professional': ['regional_rates', 'productivity_factors'],
        'enterprise': ['custom_rates', 'historical_data', 'analytics']
    }

    def search(self, query: str, user_id: str) -> list:
        # Get user tier
        tier = self.get_user_tier(user_id)

        # Limit results based on tier
        allowed_fields = self.TIERS[tier]

        # Execute search with field restrictions
        results = self.vector_search(
            query=query,
            fields=allowed_fields,
            limit=self.get_tier_limit(tier)
        )

        # Log search for analytics
        self.audit.log(f"CWICR search: {user_id}, query='{query[:50]}...'")

        return results

    def export_data(self, user_id: str, format: str) -> bytes:
        # Enterprise only
        if self.get_user_tier(user_id) != 'enterprise':
            raise PermissionError("Export requires enterprise tier")

        # Watermark exported data
        data = self.get_exportable_data(user_id)
        watermarked = self.add_watermark(data, user_id)

        return watermarked
```

#### CWICR Checklist
- [ ] Tiered access control implemented
- [ ] API rate limiting per user/tier
- [ ] Data exports watermarked
- [ ] Bulk download restrictions
- [ ] Competitor access monitoring

### 6. Integration Security (Procore, PlanGrid, etc.)

```python
# Secure OAuth integration with construction platforms

class ConstructionPlatformIntegration:
    """Secure integration with external platforms"""

    def __init__(self, platform: str):
        self.platform = platform
        # Load credentials from secure vault
        self.credentials = self.vault.get(f'{platform}_oauth')

    def authenticate(self) -> str:
        # Use OAuth 2.0 with PKCE
        code_verifier = secrets.token_urlsafe(32)
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode()).digest()
        ).decode().rstrip('=')

        # Never store tokens in code or logs
        token = self.oauth_flow(code_verifier, code_challenge)

        # Store token securely
        self.secure_token_store.set(
            key=f'{self.platform}_token',
            value=token,
            ttl=token['expires_in']
        )

        return token

    def sync_data(self, project_id: str) -> dict:
        # Validate project access before sync
        if not self.has_project_access(project_id):
            raise PermissionError(f"No access to project {project_id}")

        # Rate limit syncs
        self.rate_limiter.check(f'sync_{self.platform}')

        # Sync with retry and error handling
        try:
            data = self.api_client.get_project_data(project_id)
            self.validate_incoming_data(data)
            return data
        except APIError as e:
            # Log error without sensitive details
            self.logger.error(f"Sync failed for {project_id}: {type(e).__name__}")
            raise
```

#### Integration Checklist
- [ ] OAuth 2.0 with PKCE implemented
- [ ] Tokens stored in secure vault (not env vars)
- [ ] Token refresh automated
- [ ] API rate limiting respected
- [ ] Webhook signatures verified
- [ ] Data validation on incoming data

### 7. Document Management Security

```python
# Construction documents often contain confidential information

class SecureDocumentManager:
    """Secure document handling for construction"""

    # Document classification levels
    CLASSIFICATIONS = {
        'public': [],
        'internal': ['daily_reports', 'schedules'],
        'confidential': ['contracts', 'bids', 'financials'],
        'restricted': ['legal', 'hr', 'insurance']
    }

    def upload_document(self, file: bytes, metadata: dict, user_id: str) -> str:
        # Scan for malware
        if not self.malware_scan(file):
            raise SecurityError("Malware detected in uploaded file")

        # Classify document
        classification = self.classify_document(metadata)

        # Check user can upload to this classification
        if not self.can_upload(user_id, classification):
            raise PermissionError(f"Cannot upload {classification} documents")

        # Encrypt based on classification
        if classification in ['confidential', 'restricted']:
            file = self.encrypt(file)

        # Store with audit trail
        doc_id = self.storage.put(file, metadata)
        self.audit.log(f"Document uploaded: {doc_id} by {user_id}")

        return doc_id

    def download_document(self, doc_id: str, user_id: str) -> bytes:
        # Check access
        doc = self.storage.get_metadata(doc_id)
        if not self.can_access(user_id, doc['classification']):
            raise PermissionError("Access denied")

        # Log download
        self.audit.log(f"Document downloaded: {doc_id} by {user_id}")

        # Return decrypted content
        return self.decrypt(self.storage.get(doc_id))
```

#### Document Checklist
- [ ] Malware scanning on upload
- [ ] Document classification system
- [ ] Role-based access control
- [ ] Download audit logging
- [ ] Encryption for sensitive documents
- [ ] Retention policies enforced

## Pre-Deployment Security Checklist for Construction Systems

### Data Protection
- [ ] Financial data encrypted at rest and in transit
- [ ] BIM/CAD files protected with access control
- [ ] Subcontractor PII secured (GDPR/CCPA compliant)
- [ ] CWICR data access tiered appropriately
- [ ] Backup encryption enabled

### Authentication & Authorization
- [ ] Multi-factor authentication for admin users
- [ ] Role-based access control implemented
- [ ] Session management secure (timeout, single device)
- [ ] API keys rotated regularly
- [ ] OAuth integrations use PKCE

### Audit & Compliance
- [ ] All data access logged
- [ ] Logs tamper-proof (append-only)
- [ ] Retention policies documented
- [ ] Data export capabilities for audits
- [ ] Compliance reports automated

### Integration Security
- [ ] All external APIs authenticated
- [ ] Webhook signatures verified
- [ ] Data validation on all inputs
- [ ] Rate limiting implemented
- [ ] Error messages sanitized

### Field Data Security
- [ ] Mobile apps use certificate pinning
- [ ] Offline data encrypted
- [ ] GPS/timestamp validation
- [ ] Photo integrity verification
- [ ] Secure sync protocols

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CIS Controls for Construction](https://www.cisecurity.org/controls)
- [ISO 27001 for Construction](https://www.iso.org/isoiec-27001-information-security.html)

---

**Remember**: Construction data includes financial, legal, and competitive information. A breach can result in lost bids, legal liability, and reputational damage. Security is not optional.
