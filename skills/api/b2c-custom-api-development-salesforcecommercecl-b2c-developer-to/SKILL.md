---
name: b2c-custom-api-development
description: Develop Custom SCAPI endpoints for B2C Commerce. Use when creating REST APIs, defining api.json routes, writing schema.yaml (OAS 3.0), or building headless commerce integrations. Covers cartridge structure, endpoint implementation, and OAuth scope configuration.
---

# Custom API Development Skill

This skill guides you through developing Custom APIs for Salesforce B2C Commerce. Custom APIs let you expose custom script code as REST endpoints under the SCAPI framework.

## Overview

A Custom API URL has this structure:

```
https://{shortCode}.api.commercecloud.salesforce.com/custom/{apiName}/{apiVersion}/organizations/{organizationId}/{endpointPath}
```

Three components are required to create a Custom API:

1. **API Contract** - An OAS 3.0 schema file (YAML)
2. **API Implementation** - A script using the B2C Commerce Script API
3. **API Mapping** - An `api.json` file binding endpoints to implementations

## Cartridge Structure

Custom APIs are defined within cartridges. Create a `rest-apis` folder in the cartridge directory with subdirectories for each API:

```
/my-cartridge
    /cartridge
        package.json
        /rest-apis
            /my-api-name              # API name (lowercase alphanumeric and hyphens only)
                api.json              # Mapping file
                schema.yaml           # OAS 3.0 contract
                script.js             # Implementation
        /scripts
        /controllers
```

**Important:** API directory names can only contain alphanumeric lowercase characters and hyphens.

## Component 1: API Contract (schema.yaml)

The API contract defines endpoints using OAS 3.0 format:

```yaml
openapi: 3.0.0
info:
  version: 1.0.0                      # API version (1.0.0 becomes v1 in URL)
  title: My Custom API
components:
  securitySchemes:
    ShopperToken:                     # For Shopper APIs (requires siteId)
      type: oauth2
      flows:
        clientCredentials:
          tokenUrl: https://{shortCode}.api.commercecloud.salesforce.com/shopper/auth/v1/organizations/{organizationId}/oauth2/token
          scopes:
            c_my_scope: Description of my scope
    AmOAuth2:                         # For Admin APIs (no siteId)
      type: oauth2
      flows:
        clientCredentials:
          tokenUrl: https://account.demandware.com/dwsso/oauth2/access_token
          scopes:
            c_my_admin_scope: Description of my admin scope
  parameters:
    siteId:
      name: siteId
      in: query
      required: true
      schema:
        type: string
        minLength: 1
    locale:
      name: locale
      in: query
      required: false
      schema:
        type: string
        minLength: 1
paths:
  /my-endpoint:
    get:
      summary: Get something
      operationId: getMyData         # Must match function name in script
      parameters:
        - $ref: '#/components/parameters/siteId'
        - in: query
          name: c_my_param           # Custom params must start with c_
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
security:
  - ShopperToken: ['c_my_scope']     # Global security (or per-operation)
```

### Contract Requirements

- **Version:** Defined in `info.version`, transformed to URL version (e.g., `1.0.1` becomes `v1`)
- **Security Scheme:** Use `ShopperToken` for Shopper APIs or `AmOAuth2` for Admin APIs
- **Custom Scopes:** Must start with `c_`, contain only alphanumeric/hyphen/period/underscore, max 25 chars
- **Parameters:** All request parameters must be defined; custom params must have `c_` prefix
- **System Parameters:** `siteId` and `locale` must have `type: string` and `minLength: 1`
- **No additionalProperties:** The `additionalProperties` attribute is not allowed in request body schemas

### Shopper vs Admin APIs

| Aspect | Shopper API | Admin API |
|--------|-------------|-----------|
| Security Scheme | `ShopperToken` | `AmOAuth2` |
| `siteId` Parameter | Required | Must omit |
| Max Runtime | 10 seconds | 60 seconds |
| Max Request Body | 5 MiB | 20 MB |
| Activity Type | STOREFRONT | BUSINESS_MANAGER |

## Component 2: Implementation (script.js)

The implementation script exports functions matching `operationId` values:

```javascript
var RESTResponseMgr = require('dw/system/RESTResponseMgr');

exports.getMyData = function() {
    // Get query parameters
    var myParam = request.getHttpParameterMap().get('c_my_param').getStringValue();

    // Get path parameters (for paths like /items/{itemId})
    var itemId = request.getSCAPIPathParameters().get('itemId');

    // Get request body (for POST/PUT/PATCH)
    var requestBody = JSON.parse(request.httpParameterMap.requestBodyAsString);

    // Business logic here...
    var result = {
        data: 'my data',
        param: myParam
    };

    // Return success response
    RESTResponseMgr.createSuccess(result).render();
};
exports.getMyData.public = true;  // Required: mark function as public

// Error response example
exports.getMyDataWithError = function() {
    RESTResponseMgr
        .createError(404, 'not-found', 'Resource Not Found', 'The requested resource was not found.')
        .render();
};
exports.getMyDataWithError.public = true;
```

### Implementation Best Practices

- Always return JSON format responses
- Use RFC 9457 error format with at least the `type` field
- Mark all exported functions with `.public = true`
- Handle errors gracefully to avoid circuit breaker activation
- GET requests cannot commit transactions

### Caching Responses

Enable Page Caching for the site, then use:

```javascript
// Cache for 60 seconds
response.setExpires(Date.now() + 60000);

// Personalized caching
response.setVaryBy('price_promotion');
```

### Remote Includes

Include responses from other SCAPI endpoints:

```javascript
var include = dw.system.RESTResponseMgr.createScapiRemoteInclude(
    'custom', 'other-api', 'v1', 'endpointPath',
    dw.web.URLParameter('siteId', 'MySite')
);

var response = {
    data: 'my data',
    included: [include]
};
RESTResponseMgr.createSuccess(response).render();
```

## Component 3: Mapping (api.json)

The mapping file binds endpoints to implementations:

```json
{
  "endpoints": [
    {
      "endpoint": "getMyData",
      "schema": "schema.yaml",
      "implementation": "script"
    },
    {
      "endpoint": "getMyDataV2",
      "schema": "schema_v2.yaml",
      "implementation": "script_v2"
    }
  ]
}
```

**Important:**
- Implementation name must NOT include file extension
- Schema and implementation files must be in the same folder as api.json
- No relative paths allowed

## Endpoint Registration

Endpoints are registered when **activating the code version** containing the API definitions. After uploading your cartridge:

1. **Upload the cartridge** to your B2C instance
2. **Activate the code version** to trigger registration
3. **Check registration status** to verify endpoints are active

For Shopper APIs, the cartridge must be in the site's cartridge path. For Admin APIs, the cartridge must be in the Business Manager site's cartridge path.

## Circuit Breaker Protection

Custom APIs have a circuit breaker that blocks requests when error rate exceeds 50%:

1. Circuit opens after 50+ errors in 100 requests
2. Requests return 503 for 60 seconds
3. Circuit enters half-open state, testing next 10 requests
4. If >5 fail, circuit reopens; otherwise closes

**Prevention:** Write robust code with error handling and avoid long-running remote calls.

## Troubleshooting

When endpoints return 404 or fail to register:

1. **Check registration status** using the Custom API status report
2. **Review error reasons** in the status report for specific guidance
3. **Verify cartridge structure:** `rest-apis/{api-name}/` contains all files
4. **Check code version:** Ensure the active version contains your API
5. **Verify site assignment:** Cartridge must be in site's cartridge path
6. **Review logs** in Log Center with LCQL filter `CustomApiRegistry`

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 400 Bad Request | Contract violation (unknown/invalid params) | Define all params in schema |
| 401 Unauthorized | Invalid/missing token | Check token validity and header |
| 403 Forbidden | Missing scope | Verify scope in token matches contract |
| 404 Not Found | Endpoint not registered | Check status report, verify structure |
| 500 Internal Error | Script error | Check logs for `CustomApiInvocationException` |
| 503 Service Unavailable | Circuit breaker open | Fix script errors, wait for reset |

## Authentication Setup

### For Shopper APIs (ShopperToken)

1. **Create or update a SLAS client** with your custom scope(s)
   - Use `b2c slas client create --default-scopes --scopes "c_my_scope"` to create a test client
   - See `b2c-cli:b2c-slas` skill for full client management options
2. Obtain token via Shopper Login (SLAS) using the client credentials
3. Include `siteId` in all requests

### For Admin APIs (AmOAuth2)

1. Configure custom scope in Account Manager
2. Obtain token via Account Manager OAuth
3. Omit `siteId` from requests

### Custom API Status Report Access

To query the Custom API status report, use an Account Manager token with scope:
- `sfcc.custom-apis` (read-only)
- `sfcc.custom-apis.rw` (read-write)

## Development Workflow

1. **Create cartridge** with `rest-apis/{api-name}/` structure
2. **Define contract** (schema.yaml) with endpoints and security
3. **Implement logic** (script.js) with exported functions
4. **Create mapping** (api.json) binding endpoints to implementation
5. **Deploy and activate** to register endpoints
6. **Check registration status** to verify endpoints are active
7. **Test endpoints** with appropriate authentication
8. **Monitor logs** for errors during development
9. **Iterate** on implementation as needed

### Deployment Commands

Deploy your cartridge and activate to trigger Custom API registration:

```bash
# Deploy cartridge and reload (re-activate) to register endpoints
b2c code deploy ./my-cartridge --reload

# Or deploy then activate separately
b2c code deploy ./my-cartridge
b2c code activate my-code-version
```

See the `b2c-cli:b2c-code` skill for more deployment options.

### Check Registration Status

After deployment, verify your endpoints are registered:

```bash
# Check Custom API registration status
# Tenant ID: derive from hostname (e.g., zzpq-013 → zzpq_013)
b2c scapi custom status --tenant-id zzpq_013

# Filter to see only failed registrations
b2c scapi custom status --tenant-id zzpq_013 --status not_registered

# Show error reasons for failed registrations
b2c scapi custom status --tenant-id zzpq_013 --status not_registered --columns apiName,endpointPath,errorReason
```

See the `b2c-cli:b2c-scapi-custom` skill for more status options.

### Common Registration Issues

| Issue | Solution |
|-------|----------|
| Endpoint shows `not_registered` | Check errorReason column, verify schema.yaml syntax |
| Endpoint not appearing | Verify cartridge is in site's cartridge path, re-activate code version |
| 404 on requests | Endpoint not registered or wrong URL path |

## Testing Custom APIs

Test your Custom API endpoints using curl after deployment.

### Prerequisites for Testing

Before testing a Shopper API with custom scopes, ensure you have a SLAS client configured with those scopes:

```bash
# Create a test client with your custom scope (replace c_my_scope with your scope)
b2c slas client create \
  --tenant-id zzpq_013 \
  --channels RefArch \
  --default-scopes \
  --scopes "c_my_scope" \
  --redirect-uri http://localhost:3000/callback \
  --json

# Save the client_id and client_secret from the output
```

**Warning:** Use `--scopes` (plural) for client scopes, NOT `--scope` (singular).

See `b2c-cli:b2c-slas` skill for more options.

### Get a Shopper Token (Private Client)

Using a private SLAS client with client credentials grant:

```bash
# Set your credentials
SHORTCODE="your-short-code" # see b2c-cli:b2c-config (b2c setup config) skill to find this value; this it NOT the instance realm ID
ORG="f_ecom_xxxx_xxx"
SLAS_CLIENT_ID="your-client-id"
SLAS_CLIENT_SECRET="your-client-secret"
SITE="RefArch" # b2c-cli:b2c-sites skill to find site IDs

# Get access token
TOKEN=$(curl -s "https://$SHORTCODE.api.commercecloud.salesforce.com/shopper/auth/v1/organizations/$ORG/oauth2/token" \
    -u "$SLAS_CLIENT_ID:$SLAS_CLIENT_SECRET" \
    -d "grant_type=client_credentials&channel_id=$SITE" | jq -r '.access_token')

echo $TOKEN
```

### Call Your Custom API

```bash
# Call the Custom API endpoint
curl -s "https://$SHORTCODE.api.commercecloud.salesforce.com/custom/my-api/v1/organizations/$ORG/my-endpoint?siteId=$SITE" \
    -H "Authorization: Bearer $TOKEN" | jq
```

### Testing Tips

- Use `b2c slas client list` to find existing SLAS clients
- Use `b2c slas client create --default-scopes --scopes "c_my_scope"` to create a test client
- Check logs with `b2c webdav get` from the `logs` root if requests fail

## HTTP Methods Supported

- GET (no transaction commits)
- POST
- PUT
- PATCH
- DELETE
- HEAD
- OPTIONS

## External Service Configuration

When your Custom API calls external services via `LocalServiceRegistry.createService()`, you must configure the service in Business Manager or import it via site archive.

See the `b2c:b2c-webservices` skill for:
- Service configuration patterns
- Services XML import format (credentials, profiles, services)
- HTTP, FTP, and SOAP service examples

### Calling External Services

```javascript
var LocalServiceRegistry = require('dw/svc/LocalServiceRegistry');

var service = LocalServiceRegistry.createService('my.external.api', {
    createRequest: function(svc, args) {
        svc.setRequestMethod('GET');
        svc.addHeader('Authorization', 'Bearer ' + args.token);
        return null;
    },
    parseResponse: function(svc, client) {
        return JSON.parse(client.text);
    }
});

var result = service.call({ token: 'my-token' });
```

### Inline services.xml Example

For simple HTTP services:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<services xmlns="http://www.demandware.com/xml/impex/services/2014-09-26">

    <service-credential service-credential-id="my.external.api">
        <url>https://api.example.com/v1</url>
    </service-credential>

    <service-profile service-profile-id="my.external.api.profile">
        <timeout-millis>5000</timeout-millis>
        <rate-limit-enabled>false</rate-limit-enabled>
        <rate-limit-calls>0</rate-limit-calls>
        <rate-limit-millis>0</rate-limit-millis>
        <cb-enabled>true</cb-enabled>
        <cb-calls>5</cb-calls>
        <cb-millis>10000</cb-millis>
    </service-profile>

    <service service-id="my.external.api">
        <service-type>HTTP</service-type>
        <enabled>true</enabled>
        <log-prefix>MYAPI</log-prefix>
        <comm-log-enabled>true</comm-log-enabled>
        <force-prd-enabled>false</force-prd-enabled>
        <mock-mode-enabled>false</mock-mode-enabled>
        <profile-id>my.external.api.profile</profile-id>
        <credential-id>my.external.api</credential-id>
    </service>

</services>
```

**Common XML element name mistakes:**
- Use `service-credential-id`, NOT `id`
- Use `user-id`, NOT `user`
- Use `force-prd-enabled`, NOT `force-prd-comm-log-enabled`

Import with: `b2c job import ./my-services-folder`

See `b2c:b2c-webservices` skill for complete schema documentation, or run `b2c docs schema services` for the XSD.

## Related Skills

- `b2c-cli:b2c-code` - Deploying cartridges and activating code versions
- `b2c-cli:b2c-scapi-custom` - Checking Custom API registration status
- `b2c-cli:b2c-slas` - Creating SLAS clients for testing Shopper APIs with custom scopes
- `b2c:b2c-webservices` - Service configuration, HTTP/FTP/SOAP clients, services.xml format
- `b2c-cli:b2c-job` - Running jobs and importing site archives

## Limitations

- Maximum 50 remote includes per request
- Schema attribute `additionalProperties` is not allowed
- Only local `$ref` references supported in schemas (no remote/URL refs)
- Custom parameters must have `c_` prefix
- Custom scope names max 25 characters
