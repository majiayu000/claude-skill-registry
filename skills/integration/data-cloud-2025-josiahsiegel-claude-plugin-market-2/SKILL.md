---
name: data-cloud-2025
description: Salesforce Data Cloud integration patterns and architecture (2025)
---

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems


### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation


---

# Salesforce Data Cloud Integration Patterns (2025)

## What is Salesforce Data Cloud?

Salesforce Data Cloud is a real-time customer data platform (CDP) that unifies data from any source to create a complete, actionable view of every customer. It powers AI, automation, and analytics across the entire Customer 360 platform.

**Key Capabilities**:
- **Data Ingestion**: Connect 200+ sources (Salesforce, external systems, data lakes)
- **Data Harmonization**: Map disparate data to unified data model
- **Identity Resolution**: Match and merge customer records across sources
- **Real-Time Activation**: Trigger actions based on streaming data
- **Zero Copy Architecture**: Query data in place without moving it
- **AI/ML Ready**: Powers Einstein, Agentforce, and predictive models
- **Vector Database** (GA March 2025): Store and query unstructured data with semantic search
- **Hybrid Search** (Pilot 2025): Combine semantic and keyword search for accuracy

## Data Cloud Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Data Sources                          │
├──────────────────────────────────────────────────────────┤
│  Salesforce CRM │ External Apps │ Data Warehouses │ APIs │
└────────┬─────────────────┬──────────────┬───────────┬────┘
         │                 │              │           │
    ┌────▼─────────────────▼──────────────▼───────────▼────┐
    │         Data Cloud Connectors & Ingestion            │
    │  ├─ Real-time Streaming (Change Data Capture)        │
    │  ├─ Batch Import (scheduled/on-demand)               │
    │  └─ Zero Copy (Snowflake, Databricks, BigQuery)      │
    └────────────────────────┬─────────────────────────────┘
                             │
    ┌────────────────────────▼─────────────────────────────┐
    │            Data Model & Harmonization                │
    │  ├─ Map to Common Data Model (DMO objects)           │
    │  ├─ Identity Resolution (match & merge)              │
    │  └─ Data Transformation (calculated insights)        │
    └────────────────────────┬─────────────────────────────┘
                             │
    ┌────────────────────────▼─────────────────────────────┐
    │         Unified Customer Profile (360° View)         │
    │  ├─ Demographics, Transactions, Behavior, Events     │
    │  └─ Real-time Profile API for instant access         │
    └────────────────────────┬─────────────────────────────┘
                             │
    ┌────────────────────────▼─────────────────────────────┐
    │              Activation & Actions                    │
    │  ├─ Salesforce Flow (real-time automation)           │
    │  ├─ Marketing Cloud (segmentation/journeys)          │
    │  ├─ Agentforce (AI agents)                           │
    │  ├─ Einstein AI (predictions/recommendations)        │
    │  └─ External Systems (reverse ETL)                   │
    └──────────────────────────────────────────────────────┘
```

## Data Ingestion Patterns

### Pattern 1: Real-Time Streaming with Change Data Capture

**Use Case**: Keep Data Cloud synchronized with Salesforce objects in real-time

```apex
// Enable Change Data Capture for objects
// Setup → Change Data Capture → Select: Account, Contact, Opportunity

// Data Cloud automatically subscribes to CDC channels
// No code needed - configure in Data Cloud UI

// Optional: Custom streaming logic
public class DataCloudStreamHandler {
    public static void publishCustomEvent(Id recordId, String changeType) {
        // Publish custom platform event for Data Cloud
        DataCloudChangeEvent__e event = new DataCloudChangeEvent__e(
            RecordId__c = recordId,
            ObjectType__c = 'Custom_Object__c',
            ChangeType__c = changeType,
            Timestamp__c = System.now(),
            PayloadJson__c = JSON.serialize(getRecordData(recordId))
        );

        EventBus.publish(event);
    }

    private static Map<String, Object> getRecordData(Id recordId) {
        // Retrieve and return record data
        String objectType = recordId.getSObjectType().getDescribe().getName();
        String query = 'SELECT FIELDS(ALL) FROM ' + objectType +
                      ' WHERE Id = :recordId LIMIT 1';
        SObject record = Database.query(query);
        return (Map<String, Object>)JSON.deserializeUntyped(JSON.serialize(record));
    }
}
```

### Pattern 2: Batch Import from External Systems

**Use Case**: Import data from ERP, e-commerce, or other business systems

**Data Cloud Configuration**:
```
1. Create Data Source (Setup → Data Cloud → Data Sources)
   - Type: Amazon S3, SFTP, Azure Blob, Google Cloud Storage
   - Authentication: API key, OAuth, IAM role
   - Schedule: Hourly, Daily, Weekly

2. Map to Data Model Objects (DMO)
   - Source Field → DMO Field mapping
   - Data type conversions
   - Formula fields and transformations

3. Configure Identity Resolution
   - Match rules (email, customer ID, phone)
   - Reconciliation rules (which source wins)
```

**API-Based Batch Import**:
```python
# Python example: Push data to Data Cloud via API
import requests
import pandas as pd

def upload_to_data_cloud(csv_file, object_name, access_token, instance_url):
    """Upload CSV to Data Cloud via Bulk API"""

    # Step 1: Create ingestion job
    job_url = f"{instance_url}/services/data/v62.0/jobs/ingest"
    job_payload = {
        "object": object_name,
        "operation": "upsert",
        "externalIdFieldName": "ExternalId__c"
    }

    response = requests.post(
        job_url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        json=job_payload
    )

    job_id = response.json()["id"]

    # Step 2: Upload CSV data
    with open(csv_file, 'rb') as f:
        csv_data = f.read()

    upload_url = f"{job_url}/{job_id}/batches"
    requests.put(
        upload_url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "text/csv"
        },
        data=csv_data
    )

    # Step 3: Close job
    close_url = f"{job_url}/{job_id}"
    requests.patch(
        close_url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        json={"state": "UploadComplete"}
    )

    return job_id
```

### Pattern 3: Zero Copy Integration (Snowflake, Databricks)

**Use Case**: Access data warehouse data without copying to Salesforce

**Benefits**:
- No data duplication (single source of truth)
- No data transfer costs
- Real-time access to warehouse data
- Maintain data governance in warehouse

**Snowflake Zero Copy Setup**:
```sql
-- In Snowflake: Grant access to Salesforce
GRANT USAGE ON DATABASE customer_data TO ROLE salesforce_role;
GRANT USAGE ON SCHEMA customer_data.public TO ROLE salesforce_role;
GRANT SELECT ON TABLE customer_data.public.orders TO ROLE salesforce_role;

-- Create secure share
CREATE SHARE salesforce_data_share;
GRANT USAGE ON DATABASE customer_data TO SHARE salesforce_data_share;
ALTER SHARE salesforce_data_share ADD ACCOUNTS = 'SALESFORCE_ORG_ID';
```

**Data Cloud Configuration**:
```
1. Add Zero Copy Connector (Data Cloud → Data Sources)
   - Type: Snowflake Zero Copy
   - Connection: Account URL, username, private key
   - Database/Schema selection

2. Create Data Stream (virtual tables)
   - Select Snowflake tables to expose
   - Map to DMO or keep as is
   - Configure refresh (real-time or scheduled)

3. Query in Salesforce
   - Use SOQL-like syntax to query Snowflake data
   - Join with Salesforce data
   - No data movement required
```

**Query Zero Copy Data**:
```apex
// Query Snowflake data from Apex (via Data Cloud)
public class DataCloudZeroCopyQuery {
    public static List<Map<String, Object>> querySnowflakeOrders(String customerId) {
        // Data Cloud Query API
        String query = 'SELECT order_id, total_amount, order_date ' +
                      'FROM snowflake_orders ' +
                      'WHERE customer_id = \'' + customerId + '\' ' +
                      'ORDER BY order_date DESC LIMIT 10';

        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:DataCloud/v1/query');
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/json');
        req.setBody(JSON.serialize(new Map<String, String>{'query' => query}));

        Http http = new Http();
        HttpResponse res = http.send(req);

        if (res.getStatusCode() == 200) {
            Map<String, Object> result = (Map<String, Object>)JSON.deserializeUntyped(res.getBody());
            return (List<Map<String, Object>>)result.get('data');
        }

        return new List<Map<String, Object>>();
    }
}
```

## Identity Resolution

### Matching Rules

**Configure identity resolution to create unified profiles**:

```
Match Rules Configuration:
├─ Primary Match (exact match on email)
│  └─ IF email matches THEN merge profiles
├─ Secondary Match (fuzzy match on name + phone)
│  └─ IF firstName + lastName similar AND phone matches THEN merge
└─ Tertiary Match (external ID)
   └─ IF ExternalCustomerId matches THEN merge

Reconciliation Rules (conflict resolution):
├─ Most Recent: Use most recently updated value
├─ Source Priority: Salesforce > ERP > Website
└─ Field-Level Rules: Email from Salesforce, Revenue from ERP
```

**Custom Matching Logic**:
```apex
// Custom matching for complex scenarios
public class DataCloudMatchingService {
    public static Boolean shouldMatch(Map<String, Object> profile1,
                                     Map<String, Object> profile2) {
        // Custom matching logic beyond standard rules

        String email1 = (String)profile1.get('email');
        String email2 = (String)profile2.get('email');

        // Exact email match
        if (email1 != null && email1.equalsIgnoreCase(email2)) {
            return true;
        }

        // Fuzzy name + address match
        String name1 = (String)profile1.get('fullName');
        String name2 = (String)profile2.get('fullName');
        String address1 = (String)profile1.get('address');
        String address2 = (String)profile2.get('address');

        if (isNameSimilar(name1, name2) && isSameAddress(address1, address2)) {
            return true;
        }

        return false;
    }

    private static Boolean isNameSimilar(String name1, String name2) {
        // Implement Levenshtein distance or phonetic matching
        return calculateSimilarity(name1, name2) > 0.85;
    }
}
```

## Real-Time Activation Patterns

### Pattern 1: Flow Automation Based on Data Cloud Events

**Use Case**: Trigger Flow when customer behavior detected in Data Cloud

```
Data Cloud Calculated Insight: "High-Value Customer at Risk"
- Logic: Purchase frequency decreased by 50% in last 30 days
- Trigger: When insight calculated
↓
Platform Event: HighValueCustomerRisk__e
↓
Salesforce Flow: "Retain High-Value Customer"
- Create Task for Account Manager
- Send personalized offer via Marketing Cloud
- Add to "At-Risk" campaign
- Log activity timeline
```

**Apex Implementation**:
```apex
// Subscribe to Data Cloud insights
trigger DataCloudInsightTrigger on HighValueCustomerRisk__e (after insert) {
    List<Task> tasks = new List<Task>();

    for (HighValueCustomerRisk__e event : Trigger.new) {
        // Create retention task
        Task task = new Task(
            Subject = 'Urgent: High-value customer at risk',
            Description = 'Customer ' + event.CustomerName__c +
                         ' shows declining engagement. Take action.',
            WhatId = event.AccountId__c,
            Priority = 'High',
            Status = 'Open',
            ActivityDate = Date.today().addDays(1)
        );
        tasks.add(task);

        // Trigger retention campaign
        RetentionCampaignService.addToRetentionCampaign(
            event.CustomerId__c,
            event.RiskScore__c
        );
    }

    if (!tasks.isEmpty()) {
        insert tasks;
    }
}
```

### Pattern 2: Agentforce with Data Cloud

**Use Case**: AI agent uses Data Cloud for complete customer context

```apex
// Agentforce action: Get unified customer view
public class AgentforceDataCloudActions {
    @InvocableMethod(label='Get Customer 360 Profile')
    public static List<CustomerProfile> getCustomer360(List<String> customerIds) {
        List<CustomerProfile> profiles = new List<CustomerProfile>();

        for (String customerId : customerIds) {
            // Query Data Cloud unified profile
            HttpRequest req = new HttpRequest();
            req.setEndpoint('callout:DataCloud/v1/profile/' + customerId);
            req.setMethod('GET');

            Http http = new Http();
            HttpResponse res = http.send(req);

            if (res.getStatusCode() == 200) {
                Map<String, Object> data = (Map<String, Object>)
                    JSON.deserializeUntyped(res.getBody());

                CustomerProfile profile = new CustomerProfile();
                profile.customerId = customerId;

                // Demographics
                profile.name = (String)data.get('name');
                profile.email = (String)data.get('email');
                profile.segment = (String)data.get('segment');

                // Behavioral
                profile.totalPurchases = (Decimal)data.get('total_purchases');
                profile.avgOrderValue = (Decimal)data.get('avg_order_value');
                profile.lastPurchaseDate = Date.valueOf((String)data.get('last_purchase_date'));
                profile.preferredChannel = (String)data.get('preferred_channel');

                // Engagement
                profile.emailEngagement = (Decimal)data.get('email_engagement_score');
                profile.websiteVisits = (Integer)data.get('website_visits_30d');
                profile.supportCases = (Integer)data.get('support_cases_90d');

                // Predictive
                profile.churnRisk = (Decimal)data.get('churn_risk_score');
                profile.lifetimeValue = (Decimal)data.get('predicted_lifetime_value');
                profile.nextBestAction = (String)data.get('next_best_action');

                profiles.add(profile);
            }
        }

        return profiles;
    }

    public class CustomerProfile {
        @InvocableVariable public String customerId;
        @InvocableVariable public String name;
        @InvocableVariable public String email;
        @InvocableVariable public String segment;
        @InvocableVariable public Decimal totalPurchases;
        @InvocableVariable public Decimal avgOrderValue;
        @InvocableVariable public Date lastPurchaseDate;
        @InvocableVariable public String preferredChannel;
        @InvocableVariable public Decimal emailEngagement;
        @InvocableVariable public Integer websiteVisits;
        @InvocableVariable public Integer supportCases;
        @InvocableVariable public Decimal churnRisk;
        @InvocableVariable public Decimal lifetimeValue;
        @InvocableVariable public String nextBestAction;
    }
}
```

### Pattern 3: Reverse ETL (Data Cloud → External Systems)

**Use Case**: Push enriched Data Cloud data back to external systems

**Configuration**:
```
Data Cloud → Data Actions → Create Data Action
- Target: External API endpoint
- Trigger: Segment membership change, insight calculated
- Payload: Customer profile fields
- Authentication: Named Credential
- Schedule: Real-time or batch
```

**Apex Outbound Sync**:
```apex
public class DataCloudReverseETL {
    @InvocableMethod(label='Sync Enriched Profile to External System')
    public static void syncToExternalSystem(List<String> customerIds) {
        for (String customerId : customerIds) {
            // Get enriched profile from Data Cloud
            Map<String, Object> profile = DataCloudService.getProfile(customerId);

            // Transform for external system
            Map<String, Object> payload = new Map<String, Object>{
                'customer_id' => customerId,
                'segment' => profile.get('segment'),
                'lifetime_value' => profile.get('ltv'),
                'churn_risk' => profile.get('churn_risk'),
                'next_best_product' => profile.get('next_best_product')
            };

            // Send to external system
            HttpRequest req = new HttpRequest();
            req.setEndpoint('callout:ExternalCRM/api/customers/' + customerId);
            req.setMethod('PUT');
            req.setHeader('Content-Type', 'application/json');
            req.setBody(JSON.serialize(payload));

            Http http = new Http();
            HttpResponse res = http.send(req);

            // Log result
            DataCloudSyncLog__c log = new DataCloudSyncLog__c(
                CustomerId__c = customerId,
                Direction__c = 'Outbound',
                Success__c = res.getStatusCode() == 200,
                Timestamp__c = System.now()
            );
            insert log;
        }
    }
}
```

## Calculated Insights and Segmentation

### Create Calculated Insights

**Use Case**: Define metrics and KPIs on unified data

```sql
-- Example: Customer Lifetime Value
CREATE CALCULATED INSIGHT customer_lifetime_value AS
SELECT
    customer_id,
    SUM(order_total) as total_revenue,
    COUNT(order_id) as total_orders,
    AVG(order_total) as avg_order_value,
    DATEDIFF(day, first_order_date, CURRENT_DATE) as customer_age_days,
    SUM(order_total) / NULLIF(DATEDIFF(day, first_order_date, CURRENT_DATE), 0) * 365 as annual_revenue,
    (SUM(order_total) / NULLIF(DATEDIFF(day, first_order_date, CURRENT_DATE), 0) * 365) * 5 as predicted_ltv_5yr
FROM unified_orders
GROUP BY customer_id, first_order_date
```

### Dynamic Segmentation

**Use Case**: Create segments that update in real-time

```sql
-- Segment: High-Value Active Customers
CREATE SEGMENT high_value_active_customers AS
SELECT customer_id
FROM customer_360_profile
WHERE
    predicted_ltv_5yr > 10000
    AND last_purchase_date >= CURRENT_DATE - INTERVAL '30' DAY
    AND email_engagement_score > 0.7
    AND churn_risk_score < 0.3
```

**Use in Salesforce**:
```apex
// Query segment membership
List<Contact> highValueContacts = [
    SELECT Id, Name, Email
    FROM Contact
    WHERE Id IN (
        SELECT ContactId__c
        FROM DataCloudSegmentMember__c
        WHERE SegmentName__c = 'high_value_active_customers'
    )
];
```

## Data Cloud Vector Database (GA March 2025)

### What is Vector Database?

Data Cloud Vector Database ingests, stores, unifies, indexes, and allows semantic queries of unstructured data using generative AI techniques. It creates embeddings that enable semantic querying and seamless integration with structured data in the Einstein platform.

**Supported Unstructured Data**:
- Emails and email threads
- Text documents (PDFs, Word, etc.)
- Social media content
- Web content and chat transcripts
- Call transcripts and recordings
- Knowledge base articles
- Customer reviews and feedback

### How Vector Database Works

```
┌──────────────────────────────────────────────────────────┐
│            Unstructured Data Sources                     │
│  Emails │ Documents │ Transcripts │ Social │ Knowledge  │
└─────────────────────┬────────────────────────────────────┘
                      │
    ┌─────────────────▼────────────────────────────────────┐
    │          Text Embedding Generation                   │
    │  Uses LLM to convert text → vector embeddings        │
    │  (768-dimensional numeric representations)           │
    └─────────────────┬────────────────────────────────────┘
                      │
    ┌─────────────────▼────────────────────────────────────┐
    │        Vector Database Storage & Indexing            │
    │  Stores embeddings with metadata                     │
    │  Creates high-performance vector index               │
    └─────────────────┬────────────────────────────────────┘
                      │
    ┌─────────────────▼────────────────────────────────────┐
    │           Semantic Search Queries                    │
    │  Natural language query → embedding → similarity     │
    │  Returns most semantically similar content           │
    └──────────────────────────────────────────────────────┘
```

### Semantic Search with Einstein Copilot Search

Semantic search understands the meaning and intent of queries, going beyond keyword matching:

**Example**:
- **Query**: "How do I return a defective product?"
- **Traditional Keyword Search**: Matches documents containing exact words "return", "defective", "product"
- **Semantic Search**: Finds documents about:
  - Return policies
  - Warranty claims
  - Product exchanges
  - Refund procedures
  - RMA processes
  - *Even if they use different wording*

### Implementing Vector Database

**Step 1: Configure Unstructured Data Sources**

```
Setup → Data Cloud → Data Sources → Create
- Source Type: Unstructured Data
- Options:
  ├─ Salesforce Knowledge
  ├─ EmailMessage object
  ├─ External documents (S3, Azure Blob, Google Drive)
  ├─ API-based ingestion
  └─ ContentDocument/File objects
```

**Step 2: Enable Vector Indexing**

```apex
// API to index unstructured content
public class VectorDatabaseService {
    public static void indexDocument(String documentId, String content, Map<String, Object> metadata) {
        // Create vector embedding request
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:DataCloud/v1/vector/index');
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/json');

        Map<String, Object> payload = new Map<String, Object>{
            'documentId' => documentId,
            'content' => content,
            'metadata' => metadata,
            'source' => 'Salesforce',
            'timestamp' => System.now().getTime()
        };

        req.setBody(JSON.serialize(payload));

        Http http = new Http();
        HttpResponse res = http.send(req);

        if (res.getStatusCode() == 200) {
            System.debug('Document indexed: ' + documentId);
        } else {
            System.debug('Indexing failed: ' + res.getBody());
        }
    }
}

// Trigger to auto-index Knowledge articles
trigger KnowledgeArticleTrigger on Knowledge__kav (after insert, after update) {
    for (Knowledge__kav article : Trigger.new) {
        if (article.PublishStatus == 'Online') {
            Map<String, Object> metadata = new Map<String, Object>{
                'articleNumber' => article.ArticleNumber,
                'title' => article.Title,
                'category' => article.Category__c,
                'language' => article.Language
            };

            VectorDatabaseService.indexDocument(
                article.Id,
                article.Body__c,
                metadata
            );
        }
    }
}
```

**Step 3: Perform Semantic Search**

```apex
public class SemanticSearchService {
    @InvocableMethod(label='Semantic Search' description='Search unstructured data semantically')
    public static List<SearchResult> semanticSearch(List<SearchRequest> requests) {
        List<SearchResult> results = new List<SearchResult>();

        for (SearchRequest req : requests) {
            HttpRequest httpReq = new HttpRequest();
            httpReq.setEndpoint('callout:DataCloud/v1/vector/search');
            httpReq.setMethod('POST');
            httpReq.setHeader('Content-Type', 'application/json');

            Map<String, Object> payload = new Map<String, Object>{
                'query' => req.query,
                'topK' => req.maxResults,
                'filters' => req.filters,
                'includeMetadata' => true
            };

            httpReq.setBody(JSON.serialize(payload));

            Http http = new Http();
            HttpResponse httpRes = http.send(httpReq);

            if (httpRes.getStatusCode() == 200) {
                Map<String, Object> response = (Map<String, Object>)
                    JSON.deserializeUntyped(httpRes.getBody());

                List<Object> hits = (List<Object>)response.get('results');

                SearchResult result = new SearchResult();
                result.query = req.query;
                result.matches = new List<String>();

                for (Object hit : hits) {
                    Map<String, Object> doc = (Map<String, Object>)hit;
                    result.matches.add((String)doc.get('content'));
                }

                results.add(result);
            }
        }

        return results;
    }

    public class SearchRequest {
        @InvocableVariable(required=true)
        public String query;
        @InvocableVariable
        public Integer maxResults = 10;
        @InvocableVariable
        public Map<String, String> filters;
    }

    public class SearchResult {
        @InvocableVariable
        public String query;
        @InvocableVariable
        public List<String> matches;
    }
}
```

### Hybrid Search (Pilot 2025)

Hybrid search combines semantic search with traditional keyword search for improved accuracy:

**Benefits**:
- Understands semantic similarities and context (semantic search)
- Recognizes company-specific words and concepts (keyword search)
- Higher accuracy than either method alone
- Handles acronyms, product codes, and technical terms better

**Use Case Example**:
```
Service agent searches: "customer wants refund for SKU-12345"

Semantic Search finds:
- Return policy documents
- Refund procedures
- Customer satisfaction articles

Keyword Search finds:
- Specific SKU-12345 product documentation
- Previous cases mentioning SKU-12345
- Product-specific return windows

Hybrid Search combines both:
- Return procedures specifically for SKU-12345
- Previous refund cases for this product
- Product warranty terms
```

**Implementation**:
```apex
public class HybridSearchService {
    public static List<Map<String, Object>> hybridSearch(String query, Map<String, Object> filters) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:DataCloud/v1/search/hybrid');
        req.setMethod('POST');
        req.setHeader('Content-Type', 'application/json');

        Map<String, Object> payload = new Map<String, Object>{
            'query' => query,
            'semantic' => new Map<String, Object>{
                'enabled' => true,
                'weight' => 0.6  // 60% semantic
            },
            'keyword' => new Map<String, Object>{
                'enabled' => true,
                'weight' => 0.4  // 40% keyword
            },
            'filters' => filters,
            'topK' => 20
        };

        req.setBody(JSON.serialize(payload));

        Http http = new Http();
        HttpResponse res = http.send(req);

        if (res.getStatusCode() == 200) {
            Map<String, Object> response = (Map<String, Object>)JSON.deserializeUntyped(res.getBody());
            return (List<Map<String, Object>>)response.get('results');
        }

        return new List<Map<String, Object>>();
    }
}
```

### Multi-Language Semantic Search

Vector database supports cross-language semantic search:

**Example**:
- Service agent types case subject in French: "Problème de connexion"
- Semantic search finds similar cases in English:
  - "Login issues"
  - "Connection problems"
  - "Unable to access account"
- Returns relevant solutions regardless of language

**Configuration**:
```
Data Cloud → Vector Database → Settings
- Enable multi-language support
- Supported languages: 100+ languages via multilingual embeddings
- Automatic language detection
- Cross-language similarity matching
```

### Use Cases for Vector Database

**1. Customer Service Knowledge Retrieval**
```apex
// Agentforce action: Find relevant knowledge articles
@InvocableMethod(label='Find Relevant Articles')
public static List<String> findRelevantArticles(List<String> customerQueries) {
    List<String> articles = new List<String>();

    for (String query : customerQueries) {
        // Semantic search finds conceptually similar articles
        List<SearchResult> results = SemanticSearchService.semanticSearch(
            new List<SearchRequest>{new SearchRequest(query, 5)}
        );

        if (!results.isEmpty()) {
            articles.addAll(results[0].matches);
        }
    }

    return articles;
}
```

**2. Case Similarity Detection**
```apex
// Find similar past cases to suggest solutions
public class CaseSimilarityService {
    public static List<Case> findSimilarCases(String caseDescription) {
        // Semantic search in past cases
        List<SearchResult> results = SemanticSearchService.semanticSearch(
            new List<SearchRequest>{new SearchRequest(caseDescription, 10)}
        );

        // Extract case IDs from metadata
        Set<Id> caseIds = new Set<Id>();
        // ... extract IDs from results

        return [SELECT Id, Subject, Description, Status, Resolution__c
                FROM Case
                WHERE Id IN :caseIds
                AND Status = 'Closed'
                ORDER BY ClosedDate DESC];
    }
}
```

**3. Lead Scoring from Unstructured Data**
```apex
// Analyze email content and web behavior for lead scoring
public class LeadScoringService {
    public static Decimal scoreLeadFromContent(Id leadId) {
        // Get all email interactions
        List<EmailMessage> emails = [SELECT Id, TextBody
                                      FROM EmailMessage
                                      WHERE RelatedToId = :leadId];

        Decimal score = 0;

        // Semantic search for buying intent keywords
        String allContent = '';
        for (EmailMessage email : emails) {
            allContent += email.TextBody + ' ';
        }

        // Check semantic similarity to high-intent phrases
        List<String> intentPhrases = new List<String>{
            'ready to purchase',
            'need pricing quote',
            'schedule demo',
            'implementation timeline'
        };

        for (String phrase : intentPhrases) {
            // Semantic similarity score
            Decimal similarity = calculateSemanticSimilarity(allContent, phrase);
            score += similarity * 10;
        }

        return score;
    }
}
```

## Data Cloud SQL (ANSI SQL Support)

Query Data Cloud using standard SQL:

```sql
-- Complex analytical query across multiple sources
SELECT
    c.customer_id,
    c.name,
    c.segment,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(o.order_total) as revenue,
    AVG(s.satisfaction_score) as avg_satisfaction,
    MAX(o.order_date) as last_order_date
FROM
    unified_customer c
    INNER JOIN unified_orders o ON c.customer_id = o.customer_id
    LEFT JOIN support_interactions s ON c.customer_id = s.customer_id
WHERE
    o.order_date >= CURRENT_DATE - INTERVAL '90' DAY
GROUP BY
    c.customer_id, c.name, c.segment
HAVING
    COUNT(DISTINCT o.order_id) >= 3
ORDER BY
    revenue DESC
LIMIT 100
```

## Authentication Patterns

### OAuth 2.0 JWT Bearer Flow (Server-to-Server)

```python
# External system → Data Cloud authentication
import jwt
import time
import requests

def get_data_cloud_access_token(client_id, private_key, username, instance_url):
    """Get access token for Data Cloud API"""

    # Create JWT
    payload = {
        'iss': client_id,
        'sub': username,
        'aud': instance_url,
        'exp': int(time.time()) + 180  # 3 minutes
    }

    encoded_jwt = jwt.encode(payload, private_key, algorithm='RS256')

    # Exchange JWT for access token
    token_url = f"{instance_url}/services/oauth2/token"
    response = requests.post(token_url, data={
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': encoded_jwt
    })

    return response.json()['access_token']
```

## Best Practices

### Performance
- **Use Zero Copy** for large datasets (>10M records)
- **Batch imports** outside business hours
- **Index frequently queried fields** in Data Cloud
- **Limit real-time triggers** to critical events
- **Cache unified profiles** when possible

### Security
- **Field-level security** applies to Data Cloud queries from Salesforce
- **Data masking** for PII in non-production environments
- **Encryption at rest** and in transit (TLS 1.2+)
- **Audit logging** for all data access
- **Role-based access control** (RBAC) for Data Cloud users

### Data Quality
- **Data validation** before ingestion
- **Deduplication rules** at source and in Data Cloud
- **Data lineage tracking** (know source of each field)
- **Quality scores** for unified profiles
- **Regular data audits** and cleansing

## Resources

- **Data Cloud Documentation**: https://developer.salesforce.com/docs/data/data-cloud-int/guide
- **Zero Copy Partner Network**: https://www.salesforce.com/data/zero-copy/
- **Data Cloud Pricing**: Part of Customer 360 platform, usage-based pricing
- **Trailhead**: "Data Cloud Basics" and "Data Cloud for Developers"
