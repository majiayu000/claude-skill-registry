---
name: azure-api-management
description: API gateway and management with Azure API Management. Configure policies, rate limiting, authentication, and developer portal. Use for API lifecycle management, gateway patterns, and API security on Azure.
---

# Azure API Management

Expert guidance for API gateway and management on Azure.

## Create Instance

```bash
# Create APIM instance
az apim create \
  --name myapim \
  --resource-group myResourceGroup \
  --location eastus \
  --publisher-email admin@contoso.com \
  --publisher-name Contoso \
  --sku-name Developer

# Create API from OpenAPI
az apim api import \
  --resource-group myResourceGroup \
  --service-name myapim \
  --path myapi \
  --specification-format OpenApiJson \
  --specification-url https://api.example.com/openapi.json
```

## Policies

### Inbound Policies

```xml
<policies>
    <inbound>
        <!-- Rate limiting -->
        <rate-limit calls="100" renewal-period="60" />
        <quota calls="10000" renewal-period="86400" />

        <!-- CORS -->
        <cors allow-credentials="true">
            <allowed-origins>
                <origin>https://myapp.com</origin>
            </allowed-origins>
            <allowed-methods>
                <method>GET</method>
                <method>POST</method>
            </allowed-methods>
        </cors>

        <!-- JWT validation -->
        <validate-jwt header-name="Authorization" require-scheme="Bearer">
            <openid-config url="https://login.microsoftonline.com/{tenant}/.well-known/openid-configuration" />
            <required-claims>
                <claim name="aud" match="all">
                    <value>{client-id}</value>
                </claim>
            </required-claims>
        </validate-jwt>

        <!-- Set backend URL -->
        <set-backend-service base-url="https://backend.example.com" />
    </inbound>
</policies>
```

### Transformation Policies

```xml
<policies>
    <inbound>
        <!-- Add header -->
        <set-header name="X-Request-ID" exists-action="override">
            <value>@(Guid.NewGuid().ToString())</value>
        </set-header>

        <!-- Rewrite URL -->
        <rewrite-uri template="/api/v2{path}" />

        <!-- Set query parameter -->
        <set-query-parameter name="api-version" exists-action="override">
            <value>2023-01-01</value>
        </set-query-parameter>
    </inbound>

    <outbound>
        <!-- Transform response -->
        <set-body>@{
            var response = context.Response.Body.As<JObject>();
            response["timestamp"] = DateTime.UtcNow.ToString("o");
            return response.ToString();
        }</set-body>

        <!-- Remove headers -->
        <set-header name="X-Powered-By" exists-action="delete" />
    </outbound>
</policies>
```

### Backend Policies

```xml
<policies>
    <backend>
        <!-- Retry -->
        <retry condition="@(context.Response.StatusCode == 503)" count="3" interval="1">
            <forward-request />
        </retry>

        <!-- Circuit breaker -->
        <forward-request timeout="30" />
    </backend>

    <on-error>
        <!-- Custom error response -->
        <return-response>
            <set-status code="500" reason="Internal Server Error" />
            <set-body>@{
                return new JObject(
                    new JProperty("error", context.LastError.Message),
                    new JProperty("requestId", context.RequestId)
                ).ToString();
            }</set-body>
        </return-response>
    </on-error>
</policies>
```

## Caching

```xml
<policies>
    <inbound>
        <!-- Cache lookup -->
        <cache-lookup vary-by-developer="false" vary-by-developer-groups="false">
            <vary-by-header>Accept</vary-by-header>
            <vary-by-query-parameter>version</vary-by-query-parameter>
        </cache-lookup>
    </inbound>

    <outbound>
        <!-- Cache store -->
        <cache-store duration="3600" />
    </outbound>
</policies>
```

## Authentication

### OAuth 2.0

```xml
<policies>
    <inbound>
        <validate-jwt header-name="Authorization">
            <openid-config url="https://login.microsoftonline.com/{tenant}/v2.0/.well-known/openid-configuration" />
            <audiences>
                <audience>api://myapi</audience>
            </audiences>
            <issuers>
                <issuer>https://sts.windows.net/{tenant}/</issuer>
            </issuers>
        </validate-jwt>
    </inbound>
</policies>
```

### Subscription Key

```xml
<policies>
    <inbound>
        <!-- Require subscription key -->
        <check-header name="Ocp-Apim-Subscription-Key" failed-check-httpcode="401" failed-check-error-message="Subscription key required" />
    </inbound>
</policies>
```

### Managed Identity to Backend

```xml
<policies>
    <inbound>
        <authentication-managed-identity resource="https://backend.azure.com" />
    </inbound>
</policies>
```

## Products and Subscriptions

```bash
# Create product
az apim product create \
  --resource-group myResourceGroup \
  --service-name myapim \
  --product-id premium \
  --display-name "Premium" \
  --description "Premium API access" \
  --subscription-required true \
  --approval-required true

# Add API to product
az apim product api add \
  --resource-group myResourceGroup \
  --service-name myapim \
  --product-id premium \
  --api-id myapi

# Create subscription
az apim subscription create \
  --resource-group myResourceGroup \
  --service-name myapim \
  --display-name "My App Subscription" \
  --scope /products/premium
```

## Named Values

```bash
# Create named value
az apim nv create \
  --resource-group myResourceGroup \
  --service-name myapim \
  --named-value-id backend-url \
  --display-name "Backend URL" \
  --value "https://backend.example.com"

# Reference in policy
# {{backend-url}}
```

## Bicep Deployment

```bicep
resource apim 'Microsoft.ApiManagement/service@2023-03-01-preview' = {
  name: apimName
  location: location
  sku: {
    name: 'Developer'
    capacity: 1
  }
  properties: {
    publisherEmail: publisherEmail
    publisherName: publisherName
  }
}

resource api 'Microsoft.ApiManagement/service/apis@2023-03-01-preview' = {
  parent: apim
  name: 'myapi'
  properties: {
    displayName: 'My API'
    path: 'myapi'
    protocols: ['https']
    serviceUrl: 'https://backend.example.com'
  }
}

resource policy 'Microsoft.ApiManagement/service/apis/policies@2023-03-01-preview' = {
  parent: api
  name: 'policy'
  properties: {
    format: 'xml'
    value: loadTextContent('policy.xml')
  }
}
```

## Resources

- [API Management Documentation](https://learn.microsoft.com/azure/api-management/)
- [Policy Reference](https://learn.microsoft.com/azure/api-management/api-management-policies)
- [Best Practices](https://learn.microsoft.com/azure/api-management/api-management-howto-use-azure-monitor)
