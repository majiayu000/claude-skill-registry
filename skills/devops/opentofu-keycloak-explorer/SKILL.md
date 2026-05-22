---
name: opentofu-keycloak-explorer
description: Explore and manage Keycloak identity and access management resources using OpenTofu/Terraform
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: identity-management
---

# OpenTofu Keycloak Explorer

## What I do

I guide you through managing Keycloak identity and access management (IAM) resources using the Keycloak provider for OpenTofu/Terraform. I help you:

- **Realm Management**: Create and configure Keycloak realms
- **Client Configuration**: Setup OAuth2/OpenID Connect clients
- **User and Role Management**: Manage users, groups, and roles
- **Authentication Flows**: Configure authentication flows and mappers
- **Best Practices**: Follow Keycloak provider documentation patterns

## When to use me

Use this skill when you need to:
- Automate Keycloak infrastructure as code
- Manage identity providers (GitHub, Google, Azure AD, etc.)
- Setup authentication and authorization flows
- Manage users, groups, and roles programmatically
- Configure client applications with OAuth2/OpenID Connect
- Implement fine-grained access control

**Note**: OpenTofu and Terraform are used interchangeably throughout this skill. OpenTofu is an open-source implementation of Terraform and maintains full compatibility with Terraform providers.

## Prerequisites

- **OpenTofu CLI installed**: Install from https://opentofu.org/docs/intro/install/
- **Keycloak Server**: Running Keycloak instance (managed or self-hosted)
- **Keycloak Admin Account**: Credentials with admin privileges
- **Basic IAM Knowledge**: Understanding of OAuth2, OpenID Connect, and SAML

## Provider Documentation

- **Terraform Registry**: https://registry.terraform.io/providers/keycloak/keycloak/latest/docs
- **Latest Provider Version**: keycloak/keycloak ~> 5.0.0
- **Provider Source**: https://github.com/mrparkers/terraform-provider-keycloak

## Steps

### Step 1: Install and Configure OpenTofu

```bash
# Verify OpenTofu installation
tofu version

# Initialize project
mkdir keycloak-terraform
cd keycloak-terraform
tofu init
```

### Step 2: Configure Keycloak Provider

Create `versions.tf`:

```hcl
terraform {
  required_providers {
    keycloak = {
      source  = "keycloak/keycloak"
      version = "~> 5.0.0"
    }
  }
  required_version = ">= 1.0"
}

# State backend configuration
backend "s3" {
  bucket = "keycloak-state"
  key    = "terraform.tfstate"
  region = "us-east-1"
}
```

### Step 3: Configure Provider Connection

Create `provider.tf`:

```hcl
provider "keycloak" {
  # Method 1: Direct URL (local development)
  url       = "http://localhost:8080"
  client_id = "admin-cli"
  username  = "admin"
  password  = "admin"

  # Method 2: Managed Keycloak (e.g., Red Hat SSO)
  url       = "https://sso.example.com/auth"
  client_id = "terraform"
  username  = var.keycloak_admin_username
  password  = var.keycloak_admin_password

  # Method 3: Client Credentials (recommended for production)
  url       = "https://keycloak.example.com"
  client_id = "terraform"
  # Read from environment variable: KEYCLOAK_CLIENT_SECRET
}
```

### Step 4: Configure Environment Variables

```bash
# For production usage, use environment variables
export KEYCLOAK_CLIENT_SECRET="your-client-secret"

# Or use variable file
cat > terraform.tfvars <<EOF
keycloak_admin_username = "admin"
keycloak_admin_password = "secure-password"
EOF
```

### Step 5: Create Keycloak Realm

Create `realm.tf`:

```hcl
resource "keycloak_realm" "example" {
  realm        = "example"
  enabled      = true

  # Display settings
  display_name = "Example Realm"
  display_name_html = "<div class='kc-logo-text'><span>Example</span></div>"

  # Security settings
  ssl_required = "external"

  # User registration
  registration_allowed = true
  registration_email_as_username = true

  # Reset password
  reset_password_allowed = true
  edit_username_allowed = true
  brute_force_protected = true

  # Internationalization
  internationalization_enabled = true
  supported_locales = ["en", "es", "fr"]
  default_locale = "en"

  # Login theme
  login_theme = "keycloak"
  account_theme = "keycloak"

  # SMTP settings (optional)
  smtp_server {
    host = "smtp.gmail.com"
    port = 587
    from = "noreply@example.com"
    starttls = true
    ssl = false
    auth {
      username = var.smtp_username
      password = var.smtp_password
    }
  }

  # Browser security headers
  browser_security_headers {
    content_security_policy_report_only = false
    x_content_type_options = "nosniff"
    x_robots_tag = "none"
    x_frame_options = "SAMEORIGIN"
    content_security_policy = "frame-src 'self'; frame-ancestors 'self'; object-src 'none';"
    x_xss_protection = "1; mode=block"
    strict_transport_security = "max-age=31536000; includeSubDomains"
  }
}
```

### Step 6: Create Identity Providers

Create `identity_providers.tf`:

```hcl
# GitHub OAuth2
resource "keycloak_identity_provider" "github" {
  realm             = keycloak_realm.example.realm
  alias             = "github"
  display_name      = "GitHub"
  provider_id       = "github"
  enabled           = true
  trust_email       = true
  first_broker_login_flow_alias = keycloak_authentication_flow.github.id
  store_token      = true
  add_read_token_role_on_create = false

  config {
    client_id      = var.github_client_id
    client_secret  = var.github_client_secret
    use_jwks_url  = true
  }
}

# Google OAuth2
resource "keycloak_identity_provider" "google" {
  realm             = keycloak_realm.example.realm
  alias             = "google"
  display_name      = "Google"
  provider_id       = "google"
  enabled           = true
  store_token      = false
  trust_email       = true
  first_broker_login_flow_alias = keycloak_authentication_flow.google.id

  config {
    client_id         = var.google_client_id
    client_secret     = var.google_client_secret
    hosted_domain     = "example.com"
    use_jwks_url    = true
  }
}

# Azure AD / Microsoft
resource "keycloak_identity_provider" "azure" {
  realm             = keycloak_realm.example.realm
  alias             = "azure"
  display_name      = "Microsoft"
  provider_id       = "azure"
  enabled           = true
  trust_email       = true

  config {
    client_id           = var.azure_client_id
    client_secret       = var.azure_client_secret
    tenant_id           = var.azure_tenant_id
    gui_order           = 10
    hide_on_login_page  = false
  }
}
```

### Step 7: Create Authentication Flows

Create `authentication.tf`:

```hcl
# Browser flow
resource "keycloak_authentication_flow" "browser" {
  realm_id    = keycloak_realm.example.id
  alias       = "browser"
  description = "Browser based authentication"
  provider_id = "basic-flow"
  top_level   = true
}

# GitHub flow
resource "keycloak_authentication_flow" "github" {
  realm_id    = keycloak_realm.example.id
  alias       = "github"
  description = "GitHub authentication"
  provider_id = "basic-flow"
  top_level   = true
}

# Reset credentials flow
resource "keycloak_authentication_flow" "reset_credentials" {
  realm_id    = keycloak_realm.example.id
  alias       = "reset credentials"
  description = "Reset credentials for a user if they forgot their password or something"
  provider_id = "basic-flow"
  top_level   = true
}
```

### Step 8: Create User and Group

Create `users.tf`:

```hcl
# Group
resource "keycloak_group" "developers" {
  realm_id = keycloak_realm.example.id
  name     = "developers"
  attributes = {
    department = "engineering"
    team = "platform"
  }
}

# Subgroup
resource "keycloak_group" "frontend" {
  realm_id = keycloak_realm.example.id
  parent_id = keycloak_group.developers.id
  name     = "frontend"
}

# Role
resource "keycloak_role" "developer" {
  realm_id    = keycloak_realm.example.id
  name        = "developer"
  description = "Developer role with API access"
  attributes = {
    access_level = "full"
  }
}

# User
resource "keycloak_user" "admin_user" {
  realm_id = keycloak_realm.example.id
  username = "johndoe"
  enabled  = true
  email    = "john.doe@example.com"
  first_name = "John"
  last_name  = "Doe"

  # User attributes
  attributes = {
    job_title  = "Senior Developer"
    department = "Engineering"
  }

  # Initial password
  initial_password {
    value     = var.user_password
    temporary = false
  }

  # Add user to group
  groups = [
    keycloak_group.developers.id
  ]

  # Assign roles
  realm_roles = [
    keycloak_role.developer.name
  ]
}

# Role mapping
resource "keycloak_group_roles" "developers_roles" {
  realm_id = keycloak_realm.example.id
  group_id = keycloak_group.developers.id

  realm_roles = [
    keycloak_role.developer.name
  ]
}
```

### Step 9: Create Client Application

Create `clients.tf`:

```hcl
# Web application (confidential client)
resource "keycloak_openid_client" "web_app" {
  realm_id                    = keycloak_realm.example.id
  client_id                   = "my-web-app"
  name                        = "My Web Application"
  enabled                     = true

  # Access type
  access_type                 = "CONFIDENTIAL"
  client_authenticator_type     = "client-secret"
  standard_flow_enabled        = true
  direct_access_grants_enabled = true
  service_accounts_enabled     = true
  valid_redirect_uris        = [
    "https://app.example.com/callback",
    "https://app.example.com/silent-callback"
  ]
  web_origins               = ["https://app.example.com"]

  # Logout settings
  frontchannel_logout         = true
  frontchannel_logout_url     = "https://app.example.com/logout"
  backchannel_logout_url     = "https://app.example.com/backchannel-logout"

  # Token settings
  access_token_lifespan     = "3600"
  client_session_idle       = "1800"
  client_session_max       = "3600"

  # Fine grain OpenID Connect configuration
  consent_required         = false

  # Protocol mappers
  protocol_mappers {
    name                   = "username"
    protocol               = "openid-connect"
    protocol_mapper        = "user-attribute-mapper"
    user_attribute         = "username"
    claim_name             = "preferred_username"
    json_type_label        = "String"
    add_to_id_token       = true
    add_to_access_token   = true
  }

  protocol_mappers {
    name                   = "email"
    protocol               = "openid-connect"
    protocol_mapper        = "user-attribute-mapper"
    user_attribute         = "email"
    claim_name             = "email"
    json_type_label        = "String"
    add_to_id_token       = true
    add_to_access_token   = true
  }
}

# SPA application (public client)
resource "keycloak_openid_client" "spa_app" {
  realm_id               = keycloak_realm.example.id
  client_id              = "my-spa-app"
  name                   = "My SPA Application"
  enabled                = true

  access_type            = "PUBLIC"
  standard_flow_enabled   = true
  implicit_flow_enabled   = false
  direct_access_grants_enabled = false
  service_accounts_enabled = false

  # SPA settings
  web_origins          = ["+"]
  valid_redirect_uris   = [
    "https://spa.example.com/callback"
  ]

  # PKCE settings (recommended for SPAs)
  pkce_code_challenge_method = "S256"
}

# Machine-to-Machine client
resource "keycloak_openid_client" "api_service" {
  realm_id               = keycloak_realm.example.id
  client_id              = "api-service"
  name                   = "API Service"
  enabled                = true

  access_type            = "CONFIDENTIAL"
  service_accounts_enabled = true
  client_authenticator_type = "client-secret"

  # No user interaction
  standard_flow_enabled   = false
  direct_access_grants_enabled = false
}
```

### Step 10: Configure Client Scopes

Create `scopes.tf`:

```hcl
# Custom scope
resource "keycloak_openid_client_scope" "api_scope" {
  realm_id            = keycloak_realm.example.id
  name                = "api:read"
  description         = "API read access scope"
}

# Protocol mapper in scope
resource "keycloak_generic_protocol_mapper" "api_scope_mapper" {
  realm_id         = keycloak_realm.example.id
  name            = "api-read-mapper"
  protocol         = "openid-connect"
  protocol_mapper = "user-attribute-mapper"

  # Scope configuration
  add_to_id_token  = true
  add_to_access_token = true
  claim_name       = "api_read"
  user_attribute   = "api_read"

  # Add to scope
  client_scope_id = keycloak_openid_client_scope.api_scope.id
}
```

### Step 11: Define Variables

Create `variables.tf`:

```hcl
variable "keycloak_admin_username" {
  description = "Keycloak admin username"
  type        = string
  sensitive   = true
}

variable "keycloak_admin_password" {
  description = "Keycloak admin password"
  type        = string
  sensitive   = true
}

variable "github_client_id" {
  description = "GitHub OAuth2 client ID"
  type        = string
  sensitive   = true
}

variable "github_client_secret" {
  description = "GitHub OAuth2 client secret"
  type        = string
  sensitive   = true
}

variable "google_client_id" {
  description = "Google OAuth2 client ID"
  type        = string
  sensitive   = true
}

variable "google_client_secret" {
  description = "Google OAuth2 client secret"
  type        = string
  sensitive   = true
}

variable "smtp_username" {
  description = "SMTP username"
  type        = string
  sensitive   = true
}

variable "smtp_password" {
  description = "SMTP password"
  type        = string
  sensitive   = true
}
```

### Step 12: Initialize and Apply

```bash
# Initialize providers
tofu init

# Plan changes
tofu plan -out=tfplan

# Apply changes
tofu apply tfplan
```

## Best Practices

### Security

1. **Use Service Accounts**: For production, use service account credentials instead of admin credentials
2. **Least Privilege**: Grant only necessary permissions to service accounts
3. **Secure Secrets**: Store sensitive data in environment variables or secret managers
4. **Enable SSL/TLS**: Always use HTTPS in production environments
5. **Session Management**: Set appropriate session timeouts

### Organization

1. **Modular Configuration**: Split resources into logical files (realm.tf, clients.tf, users.tf)
2. **Terraform Modules**: Create reusable modules for common patterns
3. **State Management**: Use remote backend with encryption and locking
4. **Environment Separation**: Use workspaces or separate state files for dev/staging/prod

### Authentication Flows

1. **Customize for Your Needs**: Modify authentication flows based on requirements
2. **Multi-Factor Authentication**: Enable MFA for sensitive applications
3. **Social Login**: Configure identity providers (GitHub, Google, etc.)
4. **Password Policies**: Set strong password policies

### Client Configuration

1. **Use PKCE for SPAs**: Recommended security practice for single-page applications
2. **Set Appropriate Scopes**: Only request necessary scopes
3. **Configure Redirect URIs**: Only allow trusted redirect URIs
4. **Logout Configuration**: Implement proper logout flows (frontchannel and backchannel)

## Common Issues

### Issue: Provider Connection Failed

**Symptom**: Error `Error: Failed to GET: http://localhost:8080/auth/realms/master/protocol/openid-connect/token`

**Solution**:
```bash
# Verify Keycloak is running
curl http://localhost:8080/health/ready

# Check provider configuration
# Ensure URL includes /auth/ for Keycloak < 18
# Omit /auth/ for Keycloak >= 18

# Test credentials manually
curl -X POST http://localhost:8080/auth/realms/master/protocol/openid-connect/token \
  -d "client_id=admin-cli" \
  -d "username=admin" \
  -d "password=admin" \
  -d "grant_type=password"
```

### Issue: Authentication Flow Not Found

**Symptom**: Error `Error: Could not execute: Authentication flow not found`

**Solution**:
```bash
# Ensure authentication flow is created before assigning
# Check flow existence:
tofu state list | grep authentication_flow

# Verify flow alias matches exactly
```

### Issue: Client Registration Fails

**Symptom**: Error `Error: Error creating client: HTTP 409 Conflict`

**Solution**:
```bash
# Check if client already exists
tofu import keycloak_openid_client.web_app my-realm/my-web-app

# Or use import block in configuration
import {
  to = keycloak_openid_client.web_app
  id = "my-realm/my-web-app"
}
```

### Issue: Identity Provider Configuration

**Symptom**: Error `Error: Failed to configure identity provider`

**Solution**:
```bash
# Verify OAuth2 credentials
# Check client ID and secret from provider console
# Ensure redirect URI matches in Keycloak

# Reference provider documentation:
# GitHub: https://docs.github.com/en/developers/apps/building-oauth-apps
# Google: https://developers.google.com/identity/protocols/oauth2
# Azure: https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow
```

### Issue: User Creation with Password

**Symptom**: Password not set or temporary password not working

**Solution**:
```hcl
# Ensure initial_password block is correctly configured
resource "keycloak_user" "user" {
  username = "testuser"
  enabled  = true

  initial_password {
    value     = "SecurePassword123!"
    temporary = false
  }
}
```

### Issue: Protocol Mapper Not Working

**Symptom**: Claims not appearing in token

**Solution**:
```hcl
# Check mapper configuration
# Verify claim_name and user_attribute match
# Ensure add_to_id_token or add_to_access_token is true
protocol_mappers {
  name                 = "email"
  protocol             = "openid-connect"
  protocol_mapper      = "user-attribute-mapper"
  user_attribute       = "email"
  claim_name           = "email"
  add_to_id_token     = true
  add_to_access_token = true
}
```

## Reference Documentation

- **Terraform Registry (Keycloak Provider)**: https://registry.terraform.io/providers/keycloak/keycloak/latest/docs
- **Provider GitHub**: https://github.com/mrparkers/terraform-provider-keycloak
- **Keycloak Documentation**: https://www.keycloak.org/documentation.html
- **OpenTofu Documentation**: https://opentofu.org/docs/
- **OAuth2 Best Practices**: https://datatracker.ietf.org/doc/html/rfc6749

## Examples

### Complete Realm Setup

```hcl
# versions.tf
terraform {
  required_providers {
    keycloak = {
      source  = "keycloak/keycloak"
      version = "~> 5.0.0"
    }
  }
}

# provider.tf
provider "keycloak" {
  url       = "https://keycloak.example.com"
  client_id = "terraform"
  client_secret = var.keycloak_client_secret
}

# realm.tf
resource "keycloak_realm" "production" {
  realm   = "production"
  enabled = true
  ssl_required = "external"

  smtp_server {
    host = "smtp.example.com"
    port = 587
    from = "noreply@example.com"
    starttls = true
  }
}

# clients.tf
resource "keycloak_openid_client" "dashboard" {
  realm_id              = keycloak_realm.production.id
  client_id             = "dashboard"
  name                  = "Dashboard Application"
  enabled               = true
  access_type           = "PUBLIC"
  standard_flow_enabled  = true

  valid_redirect_uris    = ["https://dashboard.example.com/callback"]
  web_origins          = ["https://dashboard.example.com"]

  protocol_mappers {
    name                  = "email"
    protocol              = "openid-connect"
    protocol_mapper       = "user-attribute-mapper"
    user_attribute        = "email"
    claim_name            = "email"
    add_to_id_token      = true
    add_to_access_token  = true
  }
}
```

### Social Login Setup

```hcl
# identity_providers.tf
resource "keycloak_identity_provider" "github" {
  realm  = keycloak_realm.production.id
  alias  = "github"
  provider_id = "github"
  enabled = true

  config {
    client_id = var.github_client_id
    client_secret = var.github_client_secret
  }
}

resource "keycloak_identity_provider" "google" {
  realm  = keycloak_realm.production.id
  alias  = "google"
  provider_id = "google"
  enabled = true

  config {
    client_id = var.google_client_id
    client_secret = var.google_client_secret
  }
}
```

### User and Role Management

```hcl
# users.tf
resource "keycloak_group" "admins" {
  realm_id = keycloak_realm.production.id
  name     = "admins"
}

resource "keycloak_role" "admin" {
  realm_id = keycloak_realm.production.id
  name     = "admin"
}

resource "keycloak_user" "alice" {
  realm_id = keycloak_realm.production.id
  username = "alice"
  enabled  = true
  email    = "alice@example.com"

  initial_password {
    value     = "SecurePassword!"
    temporary = false
  }

  realm_roles = [keycloak_role.admin.name]
  groups     = [keycloak_group.admins.id]
}
```

## Tips and Tricks

- **Use tofu import**: Import existing Keycloak resources into state
- **Validate Configuration**: Run `tofu validate` before applying
- **Use Workspaces**: Manage multiple environments (dev, staging, prod)
- **Backup State**: Regularly backup Terraform state
- **Monitor Changes**: Use `tofu plan` to review changes before applying
- **Use Modules**: Create reusable modules for common patterns

## Next Steps

After mastering Keycloak provider, explore:
- **opentofu-aws-explorer**: AWS cloud provider
- **opentofu-kubernetes-explorer**: Kubernetes deployment provider
- **Keycloak Admin Console**: Learn more about Keycloak features
- **Advanced Authentication**: Configure advanced authentication flows and MFA
