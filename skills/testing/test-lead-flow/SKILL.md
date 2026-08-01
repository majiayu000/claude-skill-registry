---
name: test-lead-flow
description: Test the complete lead submission flow using browser automation. Fills
  out the form with test data, submits, and captures PING/POST network requests to
  verify the lead flow works correctly.
---

# Test Lead Flow Skill

Test the complete lead submission flow using browser automation. Fills out the form with test data, submits, and captures PING/POST network requests to verify the lead flow works correctly.

## Usage

```
/test-lead-flow [service-type]
```

Where `service-type` is one of: `windows`, `bathrooms`, `roofing`, `hvac` (default: windows)

## Test Data

Uses consistent test data for reproducible testing:
- **Name:** Gabe Almeida
- **Email:** gabe.almeida77@gmail.com
- **Phone:** 9787980276
- **Address:** 123 Rodeo Dr, Beverly Hills, CA 90210

## What It Tests

1. Form navigation and field filling
2. Address autocomplete component
3. Form submission to /api/leads
4. PING request to buyer (Modernize)
5. POST request with full lead data
6. Response validation

## Instructions

When this skill is invoked:

1. **Get browser context:**
   ```
   Use mcp__claude-in-chrome__tabs_context_mcp to get available tabs
   Create a new tab if needed with mcp__claude-in-chrome__tabs_create_mcp
   ```

2. **Navigate to the service page:**
   ```
   Navigate to https://mycontractornow.com/{service-type}
   Take a screenshot to verify page loaded
   ```

3. **Start monitoring network requests:**
   ```
   Use mcp__claude-in-chrome__read_network_requests with clear=true to start fresh
   ```

4. **Fill out the form step by step:**

   **Step 1 - Project Scope (windows/roofing):**
   - Click "Install" or appropriate option
   - Take screenshot after each step

   **Step 2 - Service-specific questions:**
   - Windows: Select "3-5" for number of windows
   - Bathrooms: Select appropriate scope
   - Roofing: Select roof type

   **Step 3 - Address:**
   - Type "123 Rodeo Dr, Beverly Hills, CA 90210"
   - Wait for autocomplete suggestions
   - Select the address or press Enter
   - Verify ZIP code 90210 is captured

   **Step 4 - Timeline:**
   - Select "Within 3 months" (maps to "Immediately" for Modernize)

   **Step 5 - Homeowner:**
   - Select "Yes"

   **Step 6 - Name:**
   - First Name: "Gabe"
   - Last Name: "Almeida"

   **Step 7 - Contact Info:**
   - Phone: "9787980276"
   - Email: "gabe.almeida77@gmail.com"

   **Step 8 - TCPA Consent:**
   - Check the TCPA checkbox
   - Click Submit

5. **Capture network requests:**
   ```
   Use mcp__claude-in-chrome__read_network_requests with urlPattern="/api/leads"
   Use mcp__claude-in-chrome__read_network_requests with urlPattern="ping-post"
   ```

6. **Report results:**
   Format output showing:
   - Lead submission request/response
   - PING request payload and response (bid amount, pingToken)
   - POST request payload and response (accepted/rejected)
   - Any errors encountered

## Expected PING Payload (Modernize Windows)

```json
{
  "tagId": "204670250",
  "service": "WINDOWS",
  "postalCode": "90210",
  "buyTimeframe": "Immediately",
  "ownHome": "Yes",
  "NumberOfWindows": "3-5",
  "WindowsProjectScope": "Install",
  "partnerSourceId": "direct"
}
```

## Expected POST Payload (Modernize Windows)

```json
{
  "tagId": "204670250",
  "service": "WINDOWS",
  "postalCode": "90210",
  "buyTimeframe": "Immediately",
  "ownHome": "Yes",
  "NumberOfWindows": "3-5",
  "WindowsProjectScope": "Install",
  "pingToken": "<from PING response>",
  "firstName": "Gabe",
  "lastName": "Almeida",
  "phone": "9787980276",
  "email": "gabe.almeida77@gmail.com",
  "address": "123 Rodeo Dr",
  "city": "Beverly Hills",
  "state": "CA",
  "trustedFormToken": "<certificate URL>",
  "homePhoneConsentLanguage": "<TCPA text>"
}
```

## Troubleshooting

- **Browser not connected:** Ensure Claude browser extension is running
- **Form not loading:** Check if Vercel deployment is complete
- **PING fails:** Check buyer service config in database
- **POST rejected:** Check for duplicate leads or test data detection
