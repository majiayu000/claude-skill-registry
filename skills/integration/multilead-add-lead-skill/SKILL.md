---
title: "Multilead Add Lead Campaign Skill"
status: active
---

# Multilead Add Lead Campaign Skill

## Overview

Python scripts for programmatic access to the Multilead API for adding leads to campaigns. Designed to work seamlessly with your personalization workflow, allowing you to add leads with entirely custom, personalised messages.

## Purpose

Add leads to an existing Multilead campaign with support for:
- Required fields: Campaign ID, LinkedIn profile URL or email
- Standard lead data: first name, last name, job title, phone
- Custom personalised message field for each lead (integrates with your separate personalisation skill)
- Single lead or batch lead creation
- Input validation and duplicate detection across team seats
- JSON batch file import

## Key Capabilities

### 1. **Add Single Lead via CLI**
Add one lead to a campaign with full control over personalisation.

```bash
python add_lead.py --campaign-id 108 \
  --email john@example.com \
  --first-name John \
  --last-name Smith \
  --occupation "Senior Manager" \
  --personalised-message "Hi John, custom message here"
```

### 2. **Add Multiple Leads (Batch via JSON)**
Add multiple leads from a JSON file in a single operation.

```bash
python add_lead.py --campaign-id 108 --batch-file leads.json
```

### 3. **Duplicate Detection**
Check for duplicate leads across team seats before adding.

```bash
python add_lead.py --campaign-id 108 --email john@example.com --remove-duplicates
```

## Integration with Personalization Skill

This skill's `--personalised-message` argument is designed to receive output from your separate personalization skill. The workflow:

1. **Personalization Skill** → Generates custom message for each lead (e.g., via AI analysis)
2. **This Skill** → Receives the message and adds lead to campaign
3. Multilead API stores the personalized message in the `personalizedField`

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` and add your Multilead API key:
```
MULTILEAD_API_KEY=your_actual_api_key_here
```

Or pass via command line:
```bash
python add_lead.py --campaign-id 108 --email john@example.com --api-key your_key_here
```

## Authentication

Requires:
- `MULTILEAD_API_KEY`: Your Multilead API key (from environment variable or `--api-key` argument)
- API key must have permissions for the campaign's seat

## Input Validation

Built-in validation for:
- Campaign ID: Must be positive integer
- Email: Basic email format validation
- LinkedIn URL: Must match LinkedIn profile URL patterns
- Phone: Must contain 7-15 digits (with country code optional)
- Names: Letters, spaces, hyphens, apostrophes only (max 100 chars)
- Occupation: Max 200 characters
- Personalised message: Max 5000 characters
- Duplicates: Optional team-wide duplicate detection

## Response Format

Results are saved to JSON file (default: `result.json`) with structure:

```json
[
  {
    "success": true,
    "data": {
      "message": "Lead added successfully",
      ...
    },
    "error": null,
    "status_code": 200,
    "timestamp": "2025-01-15T10:30:45.123Z"
  }
]
```

## CLI Arguments

```
--campaign-id          Campaign ID (required)
--email                Email address (required if no profile-url)
--profile-url          LinkedIn profile URL (required if no email)
--first-name           First name (optional)
--last-name            Last name (optional)
--occupation           Job title or company (optional)
--phone                Phone number (optional)
--personalised-message Custom personalised message (optional)
--remove-duplicates    Check for duplicates across team seats
--batch-file           JSON file with array of leads (optional)
--output               Output file for results (default: result.json)
--api-key              API key (or use MULTILEAD_API_KEY env var)
--help                 Show help message
```

## Usage Examples

### Single Lead with Personalised Message
```bash
python add_lead.py \
  --campaign-id 108 \
  --email john@example.com \
  --first-name John \
  --last-name Smith \
  --occupation "Senior Marketing Manager" \
  --personalised-message "Hi John, your recent LinkedIn posts on AI implementation caught my attention..."
```

### Single Lead with LinkedIn Profile URL
```bash
python add_lead.py \
  --campaign-id 108 \
  --profile-url https://www.linkedin.com/in/john-smith-marketing \
  --first-name John \
  --last-name Smith
```

### Batch Import from JSON
```bash
python add_lead.py \
  --campaign-id 108 \
  --batch-file example_leads.json \
  --output batch_results.json
```

### With Duplicate Detection
```bash
python add_lead.py \
  --campaign-id 108 \
  --email john@example.com \
  --first-name John \
  --remove-duplicates
```

### Using Custom API Key (Override Environment)
```bash
python add_lead.py \
  --campaign-id 108 \
  --email john@example.com \
  --api-key your_actual_api_key_here
```

## Batch JSON Format

Create a JSON file with array of lead objects:

```json
[
  {
    "profileUrl": "https://www.linkedin.com/in/john-smith",
    "firstName": "John",
    "lastName": "Smith",
    "occupation": "CEO",
    "personalisedMessage": "Custom message for John..."
  },
  {
    "email": "sarah@example.com",
    "firstName": "Sarah",
    "lastName": "Johnson",
    "occupation": "CTO",
    "personalisedMessage": "Custom message for Sarah..."
  }
]
```

## Field Mapping to Multilead API

| Script Argument | JSON Key | Multilead API Field | Type | Notes |
|---|---|---|---|---|
| --campaign-id | campaign_id | :campaignId | path | Required |
| --profile-url | profileUrl | profileUrl | body | Required if no email |
| --email | email | email | body | Required if no profileUrl |
| --first-name | firstName | firstName | body | Optional |
| --last-name | lastName | lastName | body | Optional |
| --occupation | occupation | occupation | body | Optional |
| --phone | phone | phone | body | Optional |
| --personalised-message | personalisedMessage | personalizedField | body | Custom message |

## API Configuration

Base endpoint: `https://api.multilead.io/api/open-api/v1/campaign/:campaignId/leads`

Request method: `POST`

Request type: `application/x-www-form-urlencoded`

Authentication header: `Authorization: {MULTILEAD_API_KEY}`

## Rate Limiting

The Multilead API includes rate limiting. When rate limit is exceeded:
- HTTP Status: 429
- Response includes: `Retry-After` header with seconds to wait
- The script will report this and save the error to results file

## Error Handling

The script handles and reports:
- Invalid inputs (validation errors)
- Missing required fields
- Invalid email/URL format
- Duplicate lead detection
- API errors (4xx, 5xx responses)
- Network/connectivity issues
- Rate limiting (429 responses)

All errors are logged to the results JSON file with specific error messages.

## Python Module Usage

You can also import and use the `MultileadClient` directly in your code:

```python
from add_lead import MultileadClient

client = MultileadClient(api_key='your_api_key')

result = client.add_lead(
    campaign_id=108,
    email='john@example.com',
    first_name='John',
    last_name='Smith',
    personalised_message='Custom message here'
)

if result['success']:
    print("Lead added successfully!")
else:
    print(f"Error: {result['error']}")
```

## Utilities Module

The `utils.py` module provides validation classes for advanced use:

- `LinkedInURLValidator`: Validates LinkedIn profile URLs
- `EmailValidator`: Validates email addresses
- `LeadValidator`: Comprehensive lead field validation
- `PersonalisationMessageValidator`: Validates custom messages
- `LeadData`: Represents validated lead data

## Files Structure

```
multilead-add-lead-skill/
├── add_lead.py              # Main script with CLI and MultileadClient class
├── utils.py                 # Validation and utility functions
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── example_leads.json       # Example batch file
└── SKILL.md                 # This documentation
```

## Troubleshooting

| Error | Cause | Solution |
|---|---|---|
| "MULTILEAD_API_KEY not set" | Missing API key | Set MULTILEAD_API_KEY env var or use --api-key |
| "Invalid campaign ID" | Campaign doesn't exist | Verify campaign ID is correct in Multilead |
| "Email or profileUrl required" | Both missing | Provide at least one contact method |
| "Invalid email format" | Email validation failed | Check email spelling (user@domain.com) |
| "Invalid LinkedIn profile URL" | URL format invalid | Use format: linkedin.com/in/username |
| "Rate limit exceeded" | Too many requests | Wait per Retry-After header in response |
| "API key invalid" | Authentication failed | Verify API key is correct and active |
| "Lead added successfully" | Success ✓ | Check result.json for details |

## Next Steps

1. **Setup**: Install requirements and configure API key
2. **Test**: Try a single lead with `--first-name`, `--email`, etc.
3. **Batch**: Create JSON file and use `--batch-file` for multiple leads
4. **Personalization**: Integrate with your personalization skill to generate `--personalised-message`
5. **Automation**: Call script from CI/CD, cron jobs, or other tools

## Security Notes

- API key is never logged or printed to console (only to results JSON for debugging)
- All requests use HTTPS to Multilead API
- Use `.env` file or environment variables for API key (not in scripts)
- The `personalisedMessage` field is passed through as-is (validate in your personalization skill)
- Results JSON file is created in working directory (may contain sensitive data)

## Support & Resources

- Multilead API Docs: https://documenter.getpostman.com/view/7428744/UV5ZAGMg
- Python Requests: https://docs.python-requests.org/
- LinkedIn URL Format Help: See examples in example_leads.json

## Version Info

- Python: 3.8+
- Dependencies: requests >= 2.28.0, python-dotenv >= 0.20.0
- API Target: Multilead Open API v1
- Last Updated: January 2025

## Field Mapping to Multilead API

| Skill Field | Multilead API Field | Type | Notes |
|---|---|---|---|
| campaignId | :campaignId | path | Required |
| profileUrl | profileUrl | body | Required if no email |
| email | email | body | Required if no profileUrl |
| firstName | firstName | body | Optional |
| lastName | lastName | body | Optional |
| companyName | occupation | body | Maps to occupation field |
| jobTitle | occupation | body | Maps to occupation field |
| phone | phone | body | Optional |
| personalisedMessage | personalizedField | body | Custom message array |
| customFields | {key} | body | Any additional fields |

## Usage Example

### Single Lead with Personalized Message

```python
# Step 1: Generate personalized message (from your separate skill)
personalized_msg = "Hi Sarah, I noticed you're doing marketing at Acme Corp..."

# Step 2: Add lead with that message
result = client.call_tool(
    name="add_lead",
    arguments={
        "campaignId": "108",
        "email": "sarah@acme.com",
        "firstName": "Sarah",
        "lastName": "Johnson",
        "companyName": "Acme Corp",
        "jobTitle": "Marketing Manager",
        "personalisedMessage": personalized_msg
    }
)
```

### Batch with Multiple Personalized Leads

```python
leads = [
    {
        "profileUrl": "https://www.linkedin.com/in/john-smith",
        "firstName": "John",
        "lastName": "Smith",
        "companyName": "TechCorp",
        "jobTitle": "CEO",
        "personalisedMessage": "John, your recent post about AI impressed me..."
    },
    {
        "email": "mary@innovation.com",
        "firstName": "Mary",
        "lastName": "Chen",
        "companyName": "Innovation Labs",
        "jobTitle": "VP Product",
        "personalisedMessage": "Mary, I've followed your work in product strategy..."
    }
]

result = client.call_tool(
    name="add_leads_batch",
    arguments={
        "campaignId": "108",
        "leads": leads,
        "removeDbDuplicates": False
    }
)
```

## Implementation Details

- **Language**: Python 3.8+
- **Framework**: FastMCP (official Anthropic MCP framework)
- **API Target**: Multilead Open API v1
- **Base URL**: `https://api.multilead.io/api/open-api/v1`
- **Method**: POST to `/campaign/:campaignId/leads`

## Rate Limiting

The Multilead API now includes rate limiting (November 2025). The server:
- Respects `X-RateLimit-*` headers
- Returns 429 status when limit exceeded
- Provides `Retry-After` guidance
- Allows configuration of rate limit parameters

## Configuration

Environment variables:
- `MULTILEAD_API_KEY`: Your API key (required)
- `MULTILEAD_API_BASE_URL`: Override default base URL (optional)
- `MCP_SERVER_PORT`: Server port (optional, default: 3000)

## Testing

The skill includes built-in validation for:
- Valid LinkedIn profile URL format
- Valid email format (basic validation)
- Campaign ID is numeric
- Required fields are present
- No conflicting field values

## Troubleshooting

| Error | Cause | Solution |
|---|---|---|
| "Invalid campaign ID" | Campaign doesn't exist | Verify campaign ID exists in Multilead |
| "Email or profileUrl required" | Both missing | Provide at least one |
| "Invalid email format" | Email validation failed | Check email spelling |
| "API rate limit exceeded" | Too many requests | Wait per Retry-After header |
| "API key invalid" | Authentication failed | Verify MULTILEAD_API_KEY is correct |

## Next Steps

1. **Install the skill** in your Claude Code environment
2. **Set your API key** as environment variable: `export MULTILEAD_API_KEY=your_key_here`
3. **Start the MCP server**: `python server.py`
4. **Call from Claude**: Use `add_lead` or `add_leads_batch` tools
5. **Integrate with personalization**: Feed personalized messages into `personalisedMessage` field

## Security Notes

- API key is never logged or exposed in responses
- All requests use HTTPS to Multilead API
- The `personalisedMessage` field is passed through as-is (your personalization skill should handle content validation)
- Environment variables should be set via `.env` file or secure secret management

## Support

For issues with:
- **This skill**: Check the error messages and troubleshooting section
- **Multilead API**: Consult Multilead Open API documentation at https://documenter.getpostman.com/view/7428744/UV5ZAGMg
- **MCP framework**: Refer to Anthropic MCP documentation
