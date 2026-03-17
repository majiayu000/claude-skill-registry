---
name: AI Auditability
description: Implementing comprehensive logging, tracking, and audit trails for AI systems to ensure compliance and enable debugging.
---

# AI Auditability

## Overview

AI Auditability ensures that all AI decisions are logged, traceable, and explainable. This is critical for regulatory compliance, debugging, bias detection, and incident investigation.

**Core Principle**: "If it's not logged, it didn't happen. Every AI decision must be auditable."

---

## 1. Why AI Auditability Matters

- **Regulatory Compliance**: GDPR right to explanation, EU AI Act record-keeping, CCPA transparency
- **Debugging**: Trace why a model made a specific decision
- **Bias Detection**: Analyze decisions across demographic groups
- **Incident Investigation**: Root cause analysis when things go wrong
- **Legal Defense**: Prove compliance in case of disputes
- **Model Improvement**: Analyze patterns to improve accuracy

---

## 2. What to Log

### Comprehensive Audit Log Structure
```typescript
interface AIAuditLog {
  // Unique identifiers
  eventId: string;
  decisionId: string;
  
  // Temporal
  timestamp: Date;
  processingTimeMs: number;
  
  // Actor
  userId?: string;
  systemActor: string;  // Which service made the request
  
  // Model information
  modelId: string;
  modelVersion: string;
  modelType: 'classification' | 'regression' | 'llm' | 'recommendation';
  
  // Input (anonymized if sensitive)
  inputFeatures: Record<string, any>;
  inputHash?: string;  // Hash for PII data
  
  // Output
  prediction: any;
  confidence: number;
  alternativePredictions?: Array<{value: any; confidence: number}>;
  
  // Explanation
  explanation?: {
    topFeatures: Array<{feature: string; importance: number}>;
    reasoning?: string;
  };
  
  // Human interaction
  humanReviewed: boolean;
  humanDecision?: any;
  overridden: boolean;
  overrideReason?: string;
  
  // Metadata
  environment: 'production' | 'staging' | 'development';
  requestId: string;
  sessionId?: string;
  
  // Compliance
  dataRetentionPolicy: string;
  consentGiven: boolean;
}
```

### Implementation
```python
import json
from datetime import datetime
import hashlib

class AIAuditLogger:
    """Comprehensive audit logging for AI decisions"""
    
    def __init__(self, storage_backend):
        self.storage = storage_backend
    
    def log_decision(
        self,
        model_id: str,
        model_version: str,
        input_data: dict,
        prediction: any,
        confidence: float,
        user_id: str = None,
        explanation: dict = None,
        metadata: dict = None
    ) -> str:
        """Log an AI decision"""
        
        # Generate unique event ID
        event_id = self.generate_event_id()
        
        # Anonymize PII if present
        anonymized_input = self.anonymize_pii(input_data)
        
        # Create audit log entry
        log_entry = {
            'event_id': event_id,
            'timestamp': datetime.utcnow().isoformat(),
            'model_id': model_id,
            'model_version': model_version,
            'user_id': user_id,
            'input_features': anonymized_input,
            'input_hash': self.hash_input(input_data),
            'prediction': prediction,
            'confidence': confidence,
            'explanation': explanation,
            'metadata': metadata or {},
            'environment': os.getenv('ENVIRONMENT', 'production')
        }
        
        # Store in audit log
        self.storage.write(log_entry)
        
        return event_id
    
    def anonymize_pii(self, data: dict) -> dict:
        """Remove or hash PII fields"""
        pii_fields = ['email', 'phone', 'ssn', 'name', 'address']
        
        anonymized = data.copy()
        for field in pii_fields:
            if field in anonymized:
                # Hash instead of removing (allows correlation)
                anonymized[field] = hashlib.sha256(
                    str(anonymized[field]).encode()
                ).hexdigest()[:16]
        
        return anonymized
    
    def hash_input(self, data: dict) -> str:
        """Create hash of input for deduplication"""
        return hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()
```

---

## 3. Audit Log Storage

### Database Schema (PostgreSQL)
```sql
CREATE TABLE ai_audit_logs (
    event_id UUID PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    
    -- Model
    model_id VARCHAR(255) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    
    -- Actor
    user_id VARCHAR(255),
    system_actor VARCHAR(255),
    
    -- Decision
    input_features JSONB NOT NULL,
    input_hash VARCHAR(64),
    prediction JSONB NOT NULL,
    confidence DECIMAL(5,4),
    
    -- Explanation
    explanation JSONB,
    
    -- Human interaction
    human_reviewed BOOLEAN DEFAULT FALSE,
    human_decision JSONB,
    overridden BOOLEAN DEFAULT FALSE,
    override_reason TEXT,
    
    -- Metadata
    processing_time_ms INT,
    environment VARCHAR(20),
    request_id VARCHAR(255),
    
    -- Compliance
    data_retention_days INT DEFAULT 365,
    consent_given BOOLEAN DEFAULT TRUE
);

-- Indexes for common queries
CREATE INDEX idx_audit_timestamp ON ai_audit_logs(timestamp DESC);
CREATE INDEX idx_audit_user ON ai_audit_logs(user_id) WHERE user_id IS NOT NULL;
CREATE INDEX idx_audit_model ON ai_audit_logs(model_id, model_version);
CREATE INDEX idx_audit_overridden ON ai_audit_logs(overridden) WHERE overridden = TRUE;

-- Partition by month for performance
CREATE TABLE ai_audit_logs_2024_01 PARTITION OF ai_audit_logs
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

### Time-Series Storage (ClickHouse)
```sql
-- For high-volume logging
CREATE TABLE ai_audit_logs (
    event_id String,
    timestamp DateTime,
    model_id String,
    model_version String,
    user_id String,
    prediction String,
    confidence Float32,
    input_hash String,
    metadata String  -- JSON as string
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, model_id)
SETTINGS index_granularity = 8192;
```

---

## 4. Querying Audit Logs

### Find All Decisions for a User
```sql
SELECT 
    event_id,
    timestamp,
    model_id,
    prediction,
    confidence,
    overridden
FROM ai_audit_logs
WHERE user_id = 'user_12345'
ORDER BY timestamp DESC
LIMIT 100;
```

### Find Low-Confidence Predictions
```sql
SELECT 
    event_id,
    timestamp,
    model_id,
    prediction,
    confidence,
    input_features
FROM ai_audit_logs
WHERE confidence < 0.70
  AND timestamp > NOW() - INTERVAL '7 days'
ORDER BY confidence ASC;
```

### Bias Analysis Query
```sql
-- Compare approval rates by demographic group
SELECT 
    input_features->>'gender' as gender,
    COUNT(*) as total_decisions,
    SUM(CASE WHEN prediction->>'approved' = 'true' THEN 1 ELSE 0 END) as approvals,
    AVG(CASE WHEN prediction->>'approved' = 'true' THEN 1.0 ELSE 0.0 END) as approval_rate
FROM ai_audit_logs
WHERE model_id = 'loan_approval_model'
  AND timestamp > NOW() - INTERVAL '30 days'
GROUP BY input_features->>'gender';
```

### Find All Overrides
```sql
SELECT 
    event_id,
    timestamp,
    model_id,
    prediction as ai_prediction,
    human_decision,
    override_reason,
    user_id
FROM ai_audit_logs
WHERE overridden = TRUE
  AND timestamp > NOW() - INTERVAL '7 days'
ORDER BY timestamp DESC;
```

---

## 5. Audit Reports

### Model Usage Statistics
```python
def generate_usage_report(model_id: str, days: int = 30):
    """Generate usage statistics for a model"""
    
    query = f"""
    SELECT 
        DATE(timestamp) as date,
        COUNT(*) as total_predictions,
        AVG(confidence) as avg_confidence,
        SUM(CASE WHEN overridden THEN 1 ELSE 0 END) as overrides,
        AVG(processing_time_ms) as avg_latency_ms
    FROM ai_audit_logs
    WHERE model_id = %s
      AND timestamp > NOW() - INTERVAL '%s days'
    GROUP BY DATE(timestamp)
    ORDER BY date DESC
    """
    
    results = db.execute(query, (model_id, days))
    
    return {
        'model_id': model_id,
        'period_days': days,
        'daily_stats': results,
        'total_predictions': sum(r['total_predictions'] for r in results),
        'avg_confidence': sum(r['avg_confidence'] for r in results) / len(results),
        'override_rate': sum(r['overrides'] for r in results) / sum(r['total_predictions'] for r in results)
    }
```

### Confidence Distribution Report
```python
def analyze_confidence_distribution(model_id: str):
    """Analyze confidence score distribution"""
    
    query = """
    SELECT 
        FLOOR(confidence * 10) / 10 as confidence_bucket,
        COUNT(*) as count,
        AVG(CASE WHEN overridden THEN 1.0 ELSE 0.0 END) as override_rate
    FROM ai_audit_logs
    WHERE model_id = %s
      AND timestamp > NOW() - INTERVAL '30 days'
    GROUP BY confidence_bucket
    ORDER BY confidence_bucket
    """
    
    results = db.execute(query, (model_id,))
    
    # Check for calibration issues
    for bucket in results:
        if abs(bucket['confidence_bucket'] - (1 - bucket['override_rate'])) > 0.2:
            logger.warning(
                f"Calibration issue: {bucket['confidence_bucket']} confidence "
                f"has {bucket['override_rate']:.1%} override rate"
            )
    
    return results
```

---

## 6. Compliance Requirements

### GDPR Right to Explanation
```python
def generate_gdpr_explanation(user_id: str, decision_id: str):
    """Generate GDPR-compliant explanation"""
    
    log = get_audit_log(decision_id)
    
    if log['user_id'] != user_id:
        raise PermissionError("User can only request their own explanations")
    
    explanation = {
        'decision_id': decision_id,
        'timestamp': log['timestamp'],
        'decision': log['prediction'],
        'reasoning': log['explanation']['reasoning'],
        'key_factors': log['explanation']['topFeatures'],
        'confidence': log['confidence'],
        'model_type': log['model_id'],
        'human_reviewed': log['human_reviewed'],
        'right_to_object': "You have the right to object to this automated decision. Contact support@company.com"
    }
    
    return explanation
```

### EU AI Act Record-Keeping
```python
class AIActCompliance:
    """EU AI Act compliance for high-risk AI systems"""
    
    REQUIRED_RETENTION_YEARS = 10  # For high-risk systems
    
    @staticmethod
    def ensure_compliance(log_entry: dict):
        """Ensure log entry meets AI Act requirements"""
        
        required_fields = [
            'model_id',
            'model_version',
            'input_features',
            'prediction',
            'timestamp',
            'explanation'
        ]
        
        missing = [f for f in required_fields if f not in log_entry]
        if missing:
            raise ComplianceError(f"Missing required fields: {missing}")
        
        # Set retention period
        log_entry['data_retention_days'] = AIActCompliance.REQUIRED_RETENTION_YEARS * 365
        
        return log_entry
```

---

## 7. Privacy-Preserving Audit Logs

### Differential Privacy
```python
def add_differential_privacy_noise(value: float, epsilon: float = 1.0):
    """Add Laplace noise for differential privacy"""
    import numpy as np
    
    sensitivity = 1.0  # Adjust based on your data
    scale = sensitivity / epsilon
    noise = np.random.laplace(0, scale)
    
    return value + noise

def log_with_privacy(aggregated_stats: dict):
    """Log aggregated statistics with differential privacy"""
    
    return {
        'total_predictions': add_differential_privacy_noise(aggregated_stats['total']),
        'avg_confidence': add_differential_privacy_noise(aggregated_stats['avg_confidence']),
        'approval_rate': add_differential_privacy_noise(aggregated_stats['approval_rate'])
    }
```

---

## 8. Audit Log Retention Policies

```python
class RetentionPolicy:
    """Manage audit log retention"""
    
    POLICIES = {
        'high_risk': 3650,      # 10 years (EU AI Act)
        'financial': 2555,      # 7 years (SOX)
        'healthcare': 2555,     # 7 years (HIPAA)
        'standard': 365,        # 1 year
        'development': 90       # 90 days
    }
    
    @staticmethod
    def apply_retention_policy():
        """Archive or delete old logs based on policy"""
        
        for policy_name, retention_days in RetentionPolicy.POLICIES.items():
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            
            # Archive to cold storage
            old_logs = AuditLog.filter(
                data_retention_policy=policy_name,
                timestamp__lt=cutoff_date,
                archived=False
            )
            
            for log in old_logs:
                archive_to_s3(log)
                log.archived = True
                log.save()
            
            logger.info(f"Archived {len(old_logs)} logs for policy {policy_name}")
```

---

## 9. Real-World Audit Scenarios

### Scenario 1: "Why was my loan rejected?"
```python
def investigate_loan_rejection(user_id: str, application_id: str):
    """Investigate a loan rejection"""
    
    # Find the decision
    log = AuditLog.get(
        user_id=user_id,
        input_features__application_id=application_id
    )
    
    # Generate explanation
    explanation = {
        'decision': log.prediction['approved'],
        'reason': log.explanation['reasoning'],
        'key_factors': [
            f"{f['feature']}: {f['importance']:.1%} importance"
            for f in log.explanation['topFeatures'][:5]
        ],
        'confidence': log.confidence,
        'appeal_process': "You can appeal this decision by contacting..."
    }
    
    return explanation
```

### Scenario 2: "Show all AI decisions for user X"
```python
def get_user_ai_history(user_id: str):
    """Get all AI decisions for a user (GDPR data export)"""
    
    logs = AuditLog.filter(user_id=user_id).order_by('-timestamp')
    
    return [
        {
            'date': log.timestamp,
            'system': log.model_id,
            'decision': log.prediction,
            'explanation': log.explanation['reasoning'] if log.explanation else None
        }
        for log in logs
    ]
```

---

## 10. AI Auditability Checklist

- [ ] **Comprehensive Logging**: Are all AI decisions logged?
- [ ] **PII Protection**: Is sensitive data anonymized or hashed?
- [ ] **Retention Policy**: Do we have compliant retention periods?
- [ ] **Queryability**: Can we efficiently query logs for investigations?
- [ ] **Explanation**: Are explanations logged with decisions?
- [ ] **Override Tracking**: Are human overrides logged?
- [ ] **Access Control**: Is audit log access restricted and logged?
- [ ] **Compliance**: Do logs meet GDPR/AI Act requirements?
- [ ] **Archival**: Are old logs archived to cold storage?
- [ ] **Monitoring**: Do we monitor audit log volume and errors?

---

## Related Skills
* `44-ai-governance/model-explainability`
* `44-ai-governance/override-mechanisms`
* `44-ai-governance/ai-data-privacy`
* `43-data-reliability/data-lineage`
