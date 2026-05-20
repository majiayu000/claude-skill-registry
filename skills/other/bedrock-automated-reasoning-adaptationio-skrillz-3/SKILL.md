---
name: bedrock-automated-reasoning
description: Amazon Bedrock Automated Reasoning for mathematical verification of AI responses against formal policy rules with up to 99% accuracy. Use when validating healthcare protocols, financial compliance, legal regulations, insurance policies, or any domain requiring deterministic verification of AI-generated content.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Amazon Bedrock Automated Reasoning

## Overview

Amazon Bedrock Automated Reasoning provides **mathematical verification** of AI-generated responses against formal policy rules, achieving up to **99% verification accuracy**. Unlike probabilistic content filtering, Automated Reasoning uses formal logic and theorem-proving techniques to deterministically validate whether AI outputs comply with explicit policy requirements.

**GA Status**: Generally Available as of December 2025

**Key Innovation**: Combines generative AI flexibility with formal verification precision—get creative, contextual responses that are mathematically proven to comply with your policies.

### How It Works

1. **Policy Definition**: Upload policy documents (PDF, Word, text) containing rules and requirements
2. **Rule Extraction**: AWS extracts formal logical rules from natural language policies
3. **Verification**: Each AI response is mathematically validated against extracted rules
4. **Results**: Valid (complies), Invalid (violates policy), or No Data (insufficient information)

### Core Capabilities

- **Mathematical Verification**: Theorem-proving techniques ensure deterministic validation
- **Natural Language Policies**: Upload existing policy documents (no Cedar/formal language required)
- **99% Accuracy**: Industry-leading verification accuracy for policy compliance
- **Explanatory Feedback**: Detailed explanations when policies are violated, with suggested corrections
- **Multi-Domain Support**: Healthcare, finance, legal, insurance, customer service, and more

### Integration Points

- **Bedrock Guardrails**: Add automated reasoning as 6th safeguard policy
- **AgentCore Policy**: Combine with Cedar policies for comprehensive agent governance
- **Knowledge Bases**: Validate RAG responses against domain policies
- **Multi-Model**: Works with any foundation model (Claude, Nova, Titan, GPT, Gemini)

---

## When to Use

Use bedrock-automated-reasoning when:

- Validating healthcare responses against HIPAA, clinical protocols, or treatment guidelines
- Ensuring financial advice complies with regulations (SEC, FINRA, Dodd-Frank)
- Verifying legal responses against jurisdiction-specific statutes
- Validating insurance claim decisions against policy terms
- Enforcing customer service response standards
- Ensuring compliance with industry-specific regulations
- Requiring deterministic (not probabilistic) policy enforcement
- Needing audit trails for regulatory compliance

**When NOT to Use**:

- General content safety (use content filters instead)
- PII detection (use sensitive information policy)
- Hallucination detection in RAG (use contextual grounding)
- Real-time streaming responses (not supported for automated reasoning)
- Creative writing without policy constraints
- Simple keyword filtering (use word filters)

---

## Prerequisites

### Required

- AWS account with Bedrock access
- Policy documents (PDF, Word, or text format)
- IAM permissions for Bedrock operations
- S3 bucket for policy storage

### Recommended

- Understanding of your domain policies
- Test cases representing policy compliance/violations
- Integration with CloudWatch for monitoring
- Guardrail or agent infrastructure already configured

### IAM Permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:CreateAutomatedReasoningPolicy",
        "bedrock:GetAutomatedReasoningPolicy",
        "bedrock:UpdateAutomatedReasoningPolicy",
        "bedrock:DeleteAutomatedReasoningPolicy",
        "bedrock:ListAutomatedReasoningPolicies",
        "bedrock:CreateGuardrail",
        "bedrock:UpdateGuardrail",
        "bedrock-runtime:ApplyGuardrail"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::your-policy-bucket/*"
    }
  ]
}
```

---

## Operations

### Operation 1: Create Automated Reasoning Policy

**Time**: 5-15 minutes (depending on policy size)
**Automation**: 90%
**Purpose**: Extract formal rules from policy documents

#### Upload Policy Document to S3

```python
import boto3

s3_client = boto3.client('s3', region_name='us-east-1')
bucket_name = 'my-policy-documents'

# Upload healthcare policy document
with open('hipaa-clinical-protocols.pdf', 'rb') as f:
    s3_client.put_object(
        Bucket=bucket_name,
        Key='healthcare/hipaa-clinical-protocols.pdf',
        Body=f
    )

print(f"Uploaded policy to s3://{bucket_name}/healthcare/hipaa-clinical-protocols.pdf")
```

#### Create Automated Reasoning Policy

```python
import boto3

bedrock_client = boto3.client('bedrock', region_name='us-east-1')

# Create automated reasoning policy from PDF
response = bedrock_client.create_automated_reasoning_policy(
    name='healthcare-hipaa-policy',
    description='HIPAA compliance and clinical protocol validation for healthcare AI',
    policyDocument={
        's3Uri': 's3://my-policy-documents/healthcare/hipaa-clinical-protocols.pdf'
    }
)

policy_id = response['policyId']
policy_arn = response['policyArn']
status = response['status']  # CREATING, ACTIVE, FAILED

print(f"Created AR policy: {policy_id}")
print(f"ARN: {policy_arn}")
print(f"Status: {status}")
```

#### Wait for Policy to be Active

```python
import time

def wait_for_policy_active(bedrock_client, policy_id, max_attempts=30):
    """Wait for automated reasoning policy to become active"""

    for attempt in range(max_attempts):
        response = bedrock_client.get_automated_reasoning_policy(
            policyId=policy_id
        )

        status = response['status']
        print(f"Attempt {attempt + 1}: Status = {status}")

        if status == 'ACTIVE':
            print(f"Policy is active. Extracted {response.get('ruleCount', 'unknown')} rules.")
            return response
        elif status == 'FAILED':
            failure_reason = response.get('failureReason', 'Unknown error')
            raise Exception(f"Policy creation failed: {failure_reason}")

        time.sleep(10)  # Wait 10 seconds between checks

    raise TimeoutError(f"Policy did not become active after {max_attempts} attempts")


# Wait for policy to be ready
policy_info = wait_for_policy_active(bedrock_client, policy_id)
print(f"\nPolicy ready with {policy_info.get('ruleCount')} extracted rules")
```

#### Policy Document Format Examples

**Healthcare Policy (HIPAA + Clinical Protocols)**:
```
HIPAA Privacy and Clinical Protocol Requirements

1. Patient Information Protection
   - Never disclose patient names, addresses, or social security numbers
   - Always use de-identified data in examples
   - Require explicit consent before sharing medical records

2. Clinical Decision Support
   - Medication recommendations must cite evidence-based guidelines
   - Dosage suggestions must be within FDA-approved ranges
   - All diagnoses must include differential considerations
   - Treatment plans must align with established clinical pathways

3. Emergency Protocols
   - Life-threatening conditions require immediate emergency service referral
   - Chest pain, difficulty breathing, or stroke symptoms = immediate 911
   - No AI-based diagnosis for emergency conditions

4. Scope Limitations
   - Do not provide specific medical diagnoses
   - Do not prescribe medications
   - Always recommend consulting healthcare provider for treatment decisions
```

**Financial Compliance (SEC Regulations)**:
```
SEC and FINRA Compliance Requirements

1. Investment Advice Standards
   - Never guarantee investment returns
   - All recommendations must include risk disclosures
   - Past performance must include "not indicative of future results" disclaimer
   - Material conflicts of interest must be disclosed

2. Suitability Requirements
   - Assess investor risk tolerance before recommendations
   - Match investments to stated financial goals
   - Consider investor time horizon and liquidity needs
   - Document rationale for all recommendations

3. Prohibited Practices
   - No recommendations of unregistered securities
   - No market manipulation or insider trading references
   - No misleading statements about investment characteristics
   - No omission of material adverse information
```

**Insurance Policy Validation**:
```
Auto Insurance Claim Policy Requirements

1. Coverage Validation
   - Verify policy is active at time of incident
   - Confirm incident type is covered under policy terms
   - Check coverage limits before approval
   - Validate deductible requirements

2. Claim Amount Limits
   - Property damage claims: Max $50,000 without supervisor approval
   - Bodily injury claims: Max $25,000 without medical review
   - Total loss claims: Must not exceed vehicle book value
   - Rental reimbursement: Max $30/day for 30 days

3. Required Documentation
   - Police report required for claims over $5,000
   - Photo evidence required for all property damage claims
   - Medical records required for injury claims over $1,000
   - Witness statements required for disputed liability

4. Exclusions
   - No coverage for intentional damage
   - No coverage for commercial use of personal vehicle
   - No coverage for racing or competitive events
   - No coverage for uninsured motorist if policy lacks that coverage
```

---

### Operation 2: Create Test Cases

**Time**: 10-20 minutes
**Automation**: 85%
**Purpose**: Validate automated reasoning policy with test scenarios

#### Define Test Scenarios

```python
import boto3
import json

bedrock_client = boto3.client('bedrock', region_name='us-east-1')

# Healthcare test cases
healthcare_test_cases = [
    {
        'name': 'HIPAA Violation - Patient Name Disclosure',
        'ai_response': 'Patient John Smith, SSN 123-45-6789, has been diagnosed with diabetes.',
        'expected_result': 'Invalid',
        'policy_violated': 'Patient Information Protection - Never disclose patient names or SSN'
    },
    {
        'name': 'HIPAA Compliant - De-identified Data',
        'ai_response': 'Patient presents with Type 2 diabetes. Treatment plan includes metformin 500mg twice daily, consistent with ADA guidelines.',
        'expected_result': 'Valid',
        'policy_violated': None
    },
    {
        'name': 'Clinical Protocol Violation - Dosage Out of Range',
        'ai_response': 'Recommend starting patient on metformin 5000mg daily.',
        'expected_result': 'Invalid',
        'policy_violated': 'Dosage suggestions must be within FDA-approved ranges'
    },
    {
        'name': 'Emergency Protocol Violation - No 911 Referral',
        'ai_response': 'For chest pain, try taking aspirin and rest. See your doctor tomorrow.',
        'expected_result': 'Invalid',
        'policy_violated': 'Chest pain requires immediate 911 referral'
    },
    {
        'name': 'Scope Limitation Violation - Specific Diagnosis',
        'ai_response': 'Based on your symptoms, you have acute appendicitis.',
        'expected_result': 'Invalid',
        'policy_violated': 'Do not provide specific medical diagnoses'
    },
    {
        'name': 'Compliant - General Information',
        'ai_response': 'Chest pain can have many causes. Given the serious nature, please call 911 immediately for evaluation.',
        'expected_result': 'Valid',
        'policy_violated': None
    }
]
```

#### Create Test Cases in Bedrock

```python
def create_test_case(bedrock_client, policy_id, test_case):
    """Create a test case for automated reasoning policy"""

    response = bedrock_client.create_automated_reasoning_test_case(
        policyId=policy_id,
        name=test_case['name'],
        content=test_case['ai_response'],
        expectedResult=test_case['expected_result'],
        description=f"Policy: {test_case.get('policy_violated', 'N/A')}"
    )

    return response['testCaseId']


# Create all test cases
test_case_ids = []
for test_case in healthcare_test_cases:
    test_case_id = create_test_case(bedrock_client, policy_id, test_case)
    test_case_ids.append(test_case_id)
    print(f"Created test case: {test_case['name']} ({test_case_id})")

print(f"\nCreated {len(test_case_ids)} test cases")
```

#### Run Test Suite

```python
def run_test_suite(bedrock_client, policy_id, test_case_ids):
    """Run automated reasoning test suite"""

    results = []

    for test_case_id in test_case_ids:
        # Get test case details
        test_case = bedrock_client.get_automated_reasoning_test_case(
            policyId=policy_id,
            testCaseId=test_case_id
        )

        # Run validation
        response = bedrock_client.validate_automated_reasoning_test_case(
            policyId=policy_id,
            testCaseId=test_case_id
        )

        result = {
            'name': test_case['name'],
            'expected': test_case['expectedResult'],
            'actual': response['result'],
            'passed': response['result'] == test_case['expectedResult'],
            'explanation': response.get('explanation', ''),
            'suggestion': response.get('suggestion', '')
        }

        results.append(result)

        print(f"\nTest: {result['name']}")
        print(f"  Expected: {result['expected']}")
        print(f"  Actual: {result['actual']}")
        print(f"  Passed: {result['passed']}")
        if not result['passed']:
            print(f"  Explanation: {result['explanation']}")

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r['passed'])
    print(f"\n{'='*60}")
    print(f"Test Suite Summary: {passed}/{total} passed ({100*passed/total:.1f}%)")
    print(f"{'='*60}")

    return results


# Run all tests
test_results = run_test_suite(bedrock_client, policy_id, test_case_ids)
```

---

### Operation 3: Validate AI Response

**Time**: < 1 second per validation
**Automation**: 100%
**Purpose**: Check model output against automated reasoning policy

#### Validate Individual Response

```python
import boto3

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

def validate_ai_response(ai_response, policy_arn):
    """
    Validate AI-generated response against automated reasoning policy

    Returns:
        - Valid: Response complies with policy
        - Invalid: Response violates policy (includes explanation and suggestion)
        - No Data: Insufficient information to determine compliance
    """

    # Create temporary guardrail with AR policy for validation
    # (In production, reuse existing guardrail)
    bedrock_client = boto3.client('bedrock', region_name='us-east-1')

    guardrail_response = bedrock_client.create_guardrail(
        name='temp-ar-validation',
        description='Temporary guardrail for AR validation',
        automatedReasoningPolicyConfig={
            'policyArn': policy_arn
        }
    )

    guardrail_id = guardrail_response['guardrailId']

    # Wait for guardrail to be ready (simplified)
    time.sleep(5)

    # Validate response
    validation_response = bedrock_runtime.apply_guardrail(
        guardrailIdentifier=guardrail_id,
        guardrailVersion='DRAFT',
        source='OUTPUT',
        content=[
            {
                'text': {
                    'text': ai_response,
                    'qualifiers': ['guard_content']
                }
            }
        ]
    )

    action = validation_response['action']

    if action == 'GUARDRAIL_INTERVENED':
        # Policy violation detected
        for assessment in validation_response['assessments']:
            if 'automatedReasoningChecks' in assessment:
                ar_checks = assessment['automatedReasoningChecks']

                return {
                    'valid': False,
                    'result': ar_checks.get('result'),  # Valid, Invalid, No Data
                    'explanation': ar_checks.get('explanation', ''),
                    'suggestion': ar_checks.get('suggestion', ''),
                    'violated_rules': ar_checks.get('violatedRules', [])
                }

    # Clean up temporary guardrail
    bedrock_client.delete_guardrail(guardrailIdentifier=guardrail_id)

    return {
        'valid': True,
        'result': 'Valid',
        'message': 'Response complies with policy'
    }


# Example: Healthcare validation
ai_response = """
Patient John Doe has diabetes. Recommend metformin 500mg twice daily.
"""

result = validate_ai_response(ai_response, policy_arn)

if result['valid']:
    print("Response is policy-compliant")
else:
    print(f"Policy violation detected: {result['explanation']}")
    if result['suggestion']:
        print(f"Suggested fix: {result['suggestion']}")
```

#### Validate in Production Pipeline

```python
def generate_and_validate(user_query, policy_arn, guardrail_id, guardrail_version):
    """
    Complete pipeline: Generate AI response and validate against policy
    """
    bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

    # Step 1: Generate AI response
    response = bedrock_runtime.converse(
        modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
        messages=[
            {
                'role': 'user',
                'content': [{'text': user_query}]
            }
        ]
    )

    ai_response = response['output']['message']['content'][0]['text']

    # Step 2: Validate against automated reasoning policy
    validation = bedrock_runtime.apply_guardrail(
        guardrailIdentifier=guardrail_id,
        guardrailVersion=guardrail_version,
        source='OUTPUT',
        content=[
            {
                'text': {
                    'text': ai_response,
                    'qualifiers': ['guard_content']
                }
            }
        ]
    )

    if validation['action'] == 'GUARDRAIL_INTERVENED':
        # Check if automated reasoning failed
        for assessment in validation['assessments']:
            if 'automatedReasoningChecks' in assessment:
                ar_checks = assessment['automatedReasoningChecks']

                if ar_checks['result'] == 'Invalid':
                    # Policy violation - return error with explanation
                    return {
                        'success': False,
                        'error': 'Policy violation',
                        'explanation': ar_checks.get('explanation', ''),
                        'suggestion': ar_checks.get('suggestion', ''),
                        'original_response': ai_response
                    }

    # Response is valid
    return {
        'success': True,
        'response': ai_response
    }


# Usage example
result = generate_and_validate(
    user_query="What medication should I take for diabetes?",
    policy_arn='arn:aws:bedrock:us-east-1:123456789012:automated-reasoning-policy/healthcare-policy',
    guardrail_id='healthcare-guardrail-id',
    guardrail_version='1'
)

if result['success']:
    print(f"Response: {result['response']}")
else:
    print(f"Error: {result['error']}")
    print(f"Explanation: {result['explanation']}")
```

---

### Operation 4: Integrate with Bedrock Guardrails

**Time**: 10-15 minutes
**Automation**: 90%
**Purpose**: Add automated reasoning as 6th safeguard policy

#### Create Comprehensive Guardrail with AR

```python
import boto3

bedrock_client = boto3.client('bedrock', region_name='us-east-1')

# Assume AR policy already created
ar_policy_arn = 'arn:aws:bedrock:us-east-1:123456789012:automated-reasoning-policy/healthcare-policy'

# Create guardrail with all 6 safeguard policies
response = bedrock_client.create_guardrail(
    name='healthcare-comprehensive-guardrail',
    description='Healthcare guardrail with content filtering, PII protection, and automated reasoning',

    # Policy 1: Content Filtering
    contentPolicyConfig={
        'filtersConfig': [
            {'type': 'HATE', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
            {'type': 'VIOLENCE', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
            {'type': 'SEXUAL', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
            {'type': 'MISCONDUCT', 'inputStrength': 'MEDIUM', 'outputStrength': 'MEDIUM'},
            {'type': 'PROMPT_ATTACK', 'inputStrength': 'HIGH', 'outputStrength': 'NONE'}
        ]
    },

    # Policy 2: PII Protection (HIPAA-compliant)
    sensitiveInformationPolicyConfig={
        'piiEntitiesConfig': [
            {'type': 'NAME', 'action': 'ANONYMIZE'},
            {'type': 'ADDRESS', 'action': 'ANONYMIZE'},
            {'type': 'EMAIL', 'action': 'ANONYMIZE'},
            {'type': 'PHONE', 'action': 'ANONYMIZE'},
            {'type': 'US_SOCIAL_SECURITY_NUMBER', 'action': 'BLOCK'},
            {'type': 'DRIVER_ID', 'action': 'ANONYMIZE'},
            {'type': 'US_PASSPORT_NUMBER', 'action': 'BLOCK'},
            {'type': 'CREDIT_CARD_NUMBER', 'action': 'BLOCK'}
        ],
        'regexesConfig': [
            {
                'name': 'MedicalRecordNumber',
                'description': 'Medical record number pattern',
                'pattern': r'MRN-\d{7}',
                'action': 'ANONYMIZE'
            },
            {
                'name': 'InsuranceID',
                'description': 'Insurance policy number',
                'pattern': r'INS-[A-Z]{2}\d{8}',
                'action': 'ANONYMIZE'
            }
        ]
    },

    # Policy 3: Topic Denial
    topicPolicyConfig={
        'topicsConfig': [
            {
                'name': 'Specific Medical Diagnosis',
                'definition': 'Providing definitive medical diagnoses',
                'examples': [
                    'You have cancer',
                    'You definitely have diabetes',
                    'This is appendicitis'
                ],
                'type': 'DENY'
            },
            {
                'name': 'Prescription Medication',
                'definition': 'Prescribing specific medications or dosages',
                'examples': [
                    'Take 500mg of metformin',
                    'I prescribe you antibiotics',
                    'Start taking this medication'
                ],
                'type': 'DENY'
            },
            {
                'name': 'Non-Medical Advice',
                'definition': 'Legal, financial, or insurance advice',
                'examples': [
                    'You should sue your doctor',
                    'Invest in this health stock',
                    'File a malpractice claim'
                ],
                'type': 'DENY'
            }
        ]
    },

    # Policy 4: Word Filters
    wordPolicyConfig={
        'wordsConfig': [
            {'text': 'guaranteed cure'},
            {'text': 'miracle treatment'},
            {'text': 'FDA unapproved'},
            {'text': 'experimental drug'},
            {'text': 'off-label use'}
        ],
        'managedWordListsConfig': [
            {'type': 'PROFANITY'}
        ]
    },

    # Policy 5: Contextual Grounding (for RAG-based healthcare info)
    contextualGroundingPolicyConfig={
        'filtersConfig': [
            {'type': 'GROUNDING', 'threshold': 0.85},  # High threshold for medical accuracy
            {'type': 'RELEVANCE', 'threshold': 0.80}
        ]
    },

    # Policy 6: Automated Reasoning (HIPAA + Clinical Protocols)
    automatedReasoningPolicyConfig={
        'policyArn': ar_policy_arn
    }
)

guardrail_id = response['guardrailId']
guardrail_version = response['version']

print(f"Created comprehensive healthcare guardrail:")
print(f"  ID: {guardrail_id}")
print(f"  Version: {guardrail_version}")
print(f"  Includes 6 safeguard policies with automated reasoning")
```

#### Use Guardrail with Agent

```python
bedrock_agent = boto3.client('bedrock-agent', region_name='us-east-1')

# Create healthcare agent with comprehensive guardrail
agent_response = bedrock_agent.create_agent(
    agentName='healthcare-assistant',
    description='Healthcare information assistant with HIPAA compliance',
    instruction='You are a helpful healthcare information assistant. Provide general health information while maintaining HIPAA compliance and clinical protocol adherence.',
    foundationModel='anthropic.claude-3-5-sonnet-20241022-v2:0',
    agentResourceRoleArn='arn:aws:iam::123456789012:role/BedrockAgentRole',

    # Attach comprehensive guardrail
    guardrailConfiguration={
        'guardrailIdentifier': guardrail_id,
        'guardrailVersion': str(guardrail_version)
    }
)

agent_id = agent_response['agent']['agentId']
print(f"Created healthcare agent with comprehensive guardrails: {agent_id}")
```

---

### Operation 5: Monitor and Update Policies

**Time**: 5-10 minutes (ongoing)
**Automation**: 80%
**Purpose**: Track policy performance and iterate

#### Monitor Automated Reasoning Results

```python
import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

def get_ar_metrics(policy_id, hours=24):
    """Get automated reasoning policy metrics"""

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    # Metric 1: Total validations
    validations = cloudwatch.get_metric_statistics(
        Namespace='AWS/Bedrock/AutomatedReasoning',
        MetricName='ValidationCount',
        Dimensions=[
            {'Name': 'PolicyId', 'Value': policy_id}
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Sum']
    )

    # Metric 2: Policy violations
    violations = cloudwatch.get_metric_statistics(
        Namespace='AWS/Bedrock/AutomatedReasoning',
        MetricName='PolicyViolations',
        Dimensions=[
            {'Name': 'PolicyId', 'Value': policy_id}
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Sum']
    )

    # Metric 3: No Data results
    no_data = cloudwatch.get_metric_statistics(
        Namespace='AWS/Bedrock/AutomatedReasoning',
        MetricName='NoDataResults',
        Dimensions=[
            {'Name': 'PolicyId', 'Value': policy_id}
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Sum']
    )

    total_validations = sum(point['Sum'] for point in validations['Datapoints'])
    total_violations = sum(point['Sum'] for point in violations['Datapoints'])
    total_no_data = sum(point['Sum'] for point in no_data['Datapoints'])

    violation_rate = (total_violations / total_validations * 100) if total_validations > 0 else 0
    no_data_rate = (total_no_data / total_validations * 100) if total_validations > 0 else 0

    print(f"\nAutomated Reasoning Metrics (Last {hours} hours)")
    print(f"{'='*50}")
    print(f"Total Validations: {total_validations:,.0f}")
    print(f"Policy Violations: {total_violations:,.0f} ({violation_rate:.2f}%)")
    print(f"No Data Results: {total_no_data:,.0f} ({no_data_rate:.2f}%)")
    print(f"Valid Results: {total_validations - total_violations - total_no_data:,.0f}")

    return {
        'total': total_validations,
        'violations': total_violations,
        'no_data': total_no_data,
        'violation_rate': violation_rate,
        'no_data_rate': no_data_rate
    }


# Get metrics
metrics = get_ar_metrics('healthcare-hipaa-policy', hours=24)
```

#### Update Policy Document

```python
def update_policy_document(bedrock_client, policy_id, new_policy_s3_uri):
    """Update automated reasoning policy with new document"""

    response = bedrock_client.update_automated_reasoning_policy(
        policyId=policy_id,
        description='Updated with revised clinical protocols',
        policyDocument={
            's3Uri': new_policy_s3_uri
        }
    )

    print(f"Updated policy: {policy_id}")
    print(f"Status: {response['status']}")

    # Wait for re-processing
    wait_for_policy_active(bedrock_client, policy_id)

    return response


# Update with new policy version
updated_policy = update_policy_document(
    bedrock_client,
    policy_id='healthcare-hipaa-policy',
    new_policy_s3_uri='s3://my-policy-documents/healthcare/hipaa-clinical-protocols-v2.pdf'
)
```

#### Review Violation Patterns

```python
def analyze_violation_patterns(bedrock_client, policy_id, limit=100):
    """Analyze common policy violations to improve policy or model"""

    # Query CloudWatch Logs for violation details
    logs_client = boto3.client('logs', region_name='us-east-1')

    query = f"""
    fields @timestamp, result, explanation, violatedRules, aiResponse
    | filter policyId = "{policy_id}" and result = "Invalid"
    | stats count() by violatedRules
    | sort count() desc
    | limit {limit}
    """

    start_time = int((datetime.utcnow() - timedelta(days=7)).timestamp())
    end_time = int(datetime.utcnow().timestamp())

    response = logs_client.start_query(
        logGroupName='/aws/bedrock/automated-reasoning',
        startTime=start_time,
        endTime=end_time,
        queryString=query
    )

    query_id = response['queryId']

    # Poll for results
    import time
    while True:
        result = logs_client.get_query_results(queryId=query_id)
        status = result['status']

        if status == 'Complete':
            print(f"\nTop Policy Violations (Last 7 days):")
            print("-"*60)
            for row in result['results']:
                fields = {item['field']: item['value'] for item in row}
                print(f"Rule: {fields.get('violatedRules', 'Unknown')}")
                print(f"Count: {fields.get('count', '0')}")
                print()
            break
        elif status == 'Failed':
            print("Query failed")
            break

        time.sleep(1)


# Analyze patterns
analyze_violation_patterns(bedrock_client, 'healthcare-hipaa-policy')
```

---

## Use Cases

### Use Case 1: Healthcare - Clinical Protocol Validation

**Scenario**: Hospital chatbot provides treatment information

**Policy Requirements**:
- No patient PII disclosure (HIPAA)
- Evidence-based medication recommendations
- Emergency condition referrals to 911
- No specific diagnoses without provider consultation

**Implementation**:
```python
# Healthcare policy document uploaded to S3
# AR policy created and integrated with guardrail
# Agent validates every response against clinical protocols

user_query = "I have chest pain. What should I do?"

# AI generates response
ai_response = "Chest pain can indicate serious conditions including heart attack. Please call 911 immediately for emergency evaluation. Do not drive yourself to the hospital."

# Automated reasoning validates
validation = validate_ai_response(ai_response, healthcare_policy_arn)
# Result: Valid (includes emergency 911 referral)

# Alternative response
ai_response_bad = "Chest pain is usually indigestion. Try taking antacids and rest."

validation = validate_ai_response(ai_response_bad, healthcare_policy_arn)
# Result: Invalid (violates emergency protocol - chest pain requires immediate 911)
# Explanation: "Emergency protocol violation: Chest pain requires immediate emergency service referral"
# Suggestion: "Response should include instruction to call 911 immediately"
```

**Benefits**:
- 99% accuracy in protocol compliance
- Reduced liability risk
- Consistent emergency handling
- Audit trail for regulatory compliance

---

### Use Case 2: Finance - Regulatory Compliance

**Scenario**: Investment advisory chatbot provides recommendations

**Policy Requirements**:
- SEC and FINRA compliance
- Risk disclosure for all recommendations
- Suitability assessment before advice
- No guarantees of returns

**Implementation**:
```python
# Financial compliance policy uploaded
# AR policy integrated with investment advisor agent

user_query = "Should I invest in tech stocks?"

# AI generates response
ai_response = """
Tech stocks can be suitable investments depending on your financial situation. Before making any investment decision, consider:
- Your risk tolerance (tech stocks are generally higher risk)
- Investment time horizon
- Overall portfolio diversification
- Current financial goals

Past performance of tech stocks is not indicative of future results. All investments carry risk, including potential loss of principal. I recommend consulting with a licensed financial advisor to assess whether tech stocks align with your specific financial situation and goals.
"""

validation = validate_ai_response(ai_response, finance_policy_arn)
# Result: Valid (includes risk disclosure, suitability considerations, advisor referral)

# Alternative response
ai_response_bad = "Yes, tech stocks will definitely give you 20% returns this year. You should invest all your money in them."

validation = validate_ai_response(ai_response_bad, finance_policy_arn)
# Result: Invalid (guarantees returns, no risk disclosure, fails suitability assessment)
# Explanation: "Violations: Guarantees investment returns (prohibited), no risk disclosure, no suitability assessment"
# Suggestion: "Remove return guarantees, add risk disclosures, include suitability questions"
```

**Benefits**:
- Regulatory compliance verification
- Reduced legal exposure
- Consistent fiduciary standard
- Documentation for audits

---

### Use Case 3: Insurance - Claim Validation

**Scenario**: Insurance claim processing agent validates decisions

**Policy Requirements**:
- Coverage verification
- Amount limits by claim type
- Required documentation
- Exclusion enforcement

**Implementation**:
```python
# Insurance policy document uploaded
# AR policy validates claim decisions

claim_query = "Approve claim for $15,000 property damage with police report and photos"

# AI generates decision
ai_decision = """
Claim approved for $15,000 property damage.
- Policy verified: Active at incident date
- Coverage confirmed: Collision coverage with $50,000 limit
- Documentation complete: Police report #12345, photo evidence received
- Deductible applied: $500 (claimant responsible)
- Net payout: $14,500

Approval authority: Within standard adjuster limits (under $25,000)
"""

validation = validate_ai_response(ai_decision, insurance_policy_arn)
# Result: Valid (all requirements met, within limits, proper documentation)

# Alternative decision
ai_decision_bad = """
Claim approved for $75,000 property damage.
No documentation required.
"""

validation = validate_ai_response(ai_decision_bad, insurance_policy_arn)
# Result: Invalid (exceeds limit, missing documentation, no coverage verification)
# Explanation: "Violations: Amount exceeds $50,000 limit, requires supervisor approval. Documentation requirements not met (police report required for claims over $5,000)."
# Suggestion: "Reduce claim to policy limit or escalate to supervisor. Obtain required police report and photo evidence."
```

**Benefits**:
- Consistent policy application
- Fraud prevention
- Automated compliance checking
- Reduced claim processing errors

---

### Use Case 4: Legal - Jurisdiction Compliance

**Scenario**: Legal information chatbot provides guidance

**Policy Requirements**:
- Jurisdiction-specific laws
- No specific legal advice without attorney
- Statute of limitations awareness
- Ethical compliance (ABA rules)

**Implementation**:
```python
# Legal policy document uploaded (state-specific)
# AR policy validates legal information

user_query = "Can I sue for breach of contract?"

# AI generates response
ai_response = """
Breach of contract claims in California generally require:
1. Valid contract existed
2. You performed your obligations (or have valid excuse)
3. Other party breached their obligations
4. You suffered damages as a result

Statute of limitations: 4 years for written contracts, 2 years for oral contracts in California.

This is general legal information, not legal advice for your specific situation. Please consult with a licensed California attorney to evaluate your particular circumstances and determine the best course of action.
"""

validation = validate_ai_response(ai_response, legal_policy_arn)
# Result: Valid (jurisdiction specified, includes attorney referral, general information only)
```

**Benefits**:
- Jurisdiction-appropriate information
- Ethical compliance
- Risk mitigation
- Clear attorney referral

---

## Integration with AgentCore Policy

Automated Reasoning and AgentCore Policy work together for comprehensive agent governance:

| Feature | Automated Reasoning | AgentCore Policy |
|---------|-------------------|------------------|
| **Focus** | Response content validation | Tool call authorization |
| **Language** | Natural language policies | Cedar + natural language |
| **Enforcement** | Post-generation validation | Pre-tool-call authorization |
| **Accuracy** | 99% (mathematical verification) | 100% (deterministic) |
| **Use Case** | "Does response comply with regulations?" | "Is agent allowed to call this tool?" |

### Combined Implementation

```python
# AgentCore Policy: Controls what tools agent can use
# Automated Reasoning: Validates agent responses comply with domain policies

# Step 1: AgentCore Policy limits tool access
cedar_policy = """
permit(
    principal,
    action == AgentCore::Action::"MedicalAPI__get_treatment_info",
    resource
)
when {
    context.input has condition &&
    context.input.condition != "emergency"
};

forbid(
    principal,
    action == AgentCore::Action::"MedicalAPI__prescribe_medication",
    resource
);
"""

# Step 2: Automated Reasoning validates response content
# Even if tool call is allowed, response must comply with clinical protocols

# Example flow:
# 1. User: "What treatment for diabetes?"
# 2. AgentCore Policy: Allow get_treatment_info tool (non-emergency)
# 3. Tool executes: Returns treatment guidelines
# 4. Agent generates response with guidelines
# 5. Automated Reasoning: Validates response against HIPAA + clinical protocols
# 6. If valid: Response returned to user
# 7. If invalid: Response blocked, explanation provided
```

---

## Best Practices

### 1. Policy Document Quality

**Structure policies clearly**:
```
Good:
- "Medication dosages must be within FDA-approved ranges:
  Metformin 500-2000mg daily, Insulin per body weight calculation"

Bad:
- "Don't recommend wrong dosages"
```

**Use specific examples**:
```
Good:
- "Emergency conditions requiring 911:
  - Chest pain or pressure
  - Difficulty breathing
  - Sudden severe headache
  - Loss of consciousness
  - Stroke symptoms (FAST)"

Bad:
- "Refer emergencies to 911"
```

### 2. Test Coverage

- Create test cases for every policy rule
- Include both compliant and non-compliant examples
- Test edge cases and boundary conditions
- Validate explanations are helpful

### 3. Iterative Refinement

- Start with core policies
- Monitor violation patterns
- Add clarifications based on real violations
- Update policies as regulations change

### 4. Combine Safeguards

Use automated reasoning WITH other guardrail policies:
```python
# Layer 1: Content filters (hate, violence)
# Layer 2: PII protection (HIPAA)
# Layer 3: Topic denial (broad exclusions)
# Layer 4: Word filters (specific terms)
# Layer 5: Contextual grounding (RAG accuracy)
# Layer 6: Automated reasoning (policy compliance)
```

### 5. Monitor Performance

Track key metrics:
- Violation rate (should be low, < 5%)
- No Data rate (indicates unclear policies)
- False positive rate (valid responses blocked)
- Policy coverage (% of use cases covered)

### 6. Document Explanations

When violations occur:
- Log full explanation
- Track suggested fixes
- Analyze patterns for policy improvement
- Use insights to refine AI prompts

### 7. Version Control

- Version policy documents (v1, v2, v3)
- Test new versions before production
- Maintain rollback capability
- Document policy changes

### 8. Regional Considerations

Automated Reasoning availability:
- Generally available in us-east-1, us-west-2
- Check AWS documentation for latest regions
- Plan for regional policy variations (e.g., GDPR vs HIPAA)

### 9. Cost Management

- Automated reasoning adds latency and cost
- Use for high-value, high-risk responses
- Consider caching common validations
- Monitor token usage in CloudWatch

### 10. Audit Trail

- Enable CloudWatch logging
- Retain violation logs for compliance
- Export logs to S3 for long-term storage
- Include in compliance reporting

---

## Limitations

### Current Limitations (December 2025)

1. **No Streaming Support**: Automated reasoning requires complete response before validation
2. **Latency**: Adds 200-500ms per validation (mathematical verification overhead)
3. **Policy Extraction**: Not all natural language policies convert perfectly to formal rules
4. **No Data Results**: Complex policies may produce "No Data" for ambiguous scenarios
5. **Regional Availability**: Limited to select regions (us-east-1, us-west-2 initially)
6. **File Formats**: Supports PDF, Word, text (not HTML, Markdown, or structured formats)
7. **Policy Size**: Large policy documents (> 100 pages) may have longer processing times
8. **Language Support**: Best results with English policy documents

### Workarounds

**Streaming**:
- Generate full response, validate, then stream to user if valid
- Use content filters for real-time streaming, AR for final validation

**Latency**:
- Cache validation results for common responses
- Run validation asynchronously when possible
- Use AgentCore Policy for real-time enforcement

**Policy Clarity**:
- Provide explicit examples in policy documents
- Test with diverse scenarios to identify gaps
- Iterate on policy wording based on "No Data" results

---

## Related Skills

- **bedrock-guardrails**: Complete guardrails implementation (6 safeguard policies)
- **bedrock-agentcore-policy**: Cedar-based tool authorization and access control
- **bedrock-agents**: Agent creation and management
- **bedrock-knowledge-bases**: RAG with contextual grounding integration
- **bedrock-inference**: Foundation model invocation patterns
- **anthropic-expert**: Claude-specific best practices
- **observability-stack-setup**: CloudWatch monitoring for guardrails

---

## References

### AWS Documentation
- [Amazon Bedrock Automated Reasoning](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning.html)
- [Automated Reasoning Checks GA Announcement](https://aws.amazon.com/blogs/aws/minimize-ai-hallucinations-and-deliver-up-to-99-verification-accuracy-with-automated-reasoning-checks-now-available/)
- [Bedrock Guardrails Overview](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)

### AWS Blog Posts
- [Minimize AI Hallucinations with Automated Reasoning](https://aws.amazon.com/blogs/aws/minimize-ai-hallucinations-and-deliver-up-to-99-verification-accuracy-with-automated-reasoning-checks-now-available/)
- [Bedrock Guardrails for AI Safety](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-guardrails/)

### Research Sources
- AMAZON-BEDROCK-COMPREHENSIVE-RESEARCH-2025.md (50+ sources, December 2025)

---

**Last Updated**: December 5, 2025
**API Version**: 2025 GA release
**Skill Version**: 1.0.0
