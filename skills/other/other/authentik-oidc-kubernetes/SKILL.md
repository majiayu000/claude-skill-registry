---
name: authentik-oidc-kubernetes
description: |
  Configure Authentik as OIDC provider for Kubernetes API server authentication.
  Use when: (1) setting up OIDC auth for kubectl with Authentik, (2) kube-apiserver
  rejects OIDC tokens with "oidc: email not verified", (3) JWKS endpoint returns
  empty {} despite provider being configured, (4) kubelogin fails with "claim not
  present" for email, (5) redirect_uri mismatch errors during kubelogin browser auth,
  (6) kube-apiserver static pod manifest changes don't take effect after restart.
  Covers all gotchas discovered when integrating Authentik 2025.10.x with Kubernetes
  1.34.x using kubelogin (int128/kubelogin).
author: Claude Code
version: 1.0.0
date: 2026-02-17
---

# Authentik OIDC for Kubernetes API Authentication

## Problem
Setting up Authentik as an OIDC identity provider for Kubernetes kubectl access
involves multiple non-obvious pitfalls that cause silent failures at different
stages of the authentication flow.

## Context / Trigger Conditions
- Setting up multi-user kubectl access with OIDC
- Using Authentik as the identity provider and kubelogin (int128/kubelogin) as the kubectl plugin
- Any of these errors:
  - `oidc: email not verified`
  - `oidc: parse username claims "email": claim not present`
  - `The request fails due to a missing, invalid, or mismatching redirection URI`
  - JWKS endpoint (`/application/o/<app>/jwks/`) returns `{}`
  - `Unauthorized` after successful browser login

## Solution

### Gotcha 1: Signing Key Must Be Assigned

Authentik's OAuth2 provider does NOT assign a signing key by default. Without it,
the JWKS endpoint returns `{}` and kube-apiserver can't validate tokens.

**Fix:** Assign a signing key (e.g., "authentik Self-signed Certificate") to the
OAuth2 provider:
```python
# Via Django shell (kubectl exec into authentik server pod)
from authentik.providers.oauth2.models import OAuth2Provider
from authentik.crypto.models import CertificateKeyPair

provider = OAuth2Provider.objects.get(name='kubernetes')
cert = CertificateKeyPair.objects.filter(name='authentik Self-signed Certificate').first()
provider.signing_key = cert
provider.save()
```

Or via API:
```bash
curl -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "$AUTHENTIK_URL/api/v3/providers/oauth2/<pk>/" \
  -d '{"signing_key": "<certificate-keypair-uuid>"}'
```

### Gotcha 2: Default Email Mapping Sets `email_verified: False`

Authentik's built-in email scope mapping hardcodes `email_verified: False`:
```python
return {
    "email": request.user.email,
    "email_verified": False  # <-- This causes kube-apiserver to reject the token
}
```

kube-apiserver requires `email_verified: true` by default.

**Fix:** Create a custom scope mapping with `email_verified: True` and assign it
to the provider instead of the default:
```python
from authentik.providers.oauth2.models import OAuth2Provider, ScopeMapping

# Create custom mapping
mapping, _ = ScopeMapping.objects.get_or_create(
    name='Kubernetes Email (verified)',
    defaults={
        'scope_name': 'email',
        'expression': 'return {"email": request.user.email, "email_verified": True}'
    }
)

# Replace default email mapping on the provider
provider = OAuth2Provider.objects.get(name='kubernetes')
default_email = ScopeMapping.objects.filter(
    managed='goauthentik.io/providers/oauth2/scope-email'
).first()
if default_email:
    provider.property_mappings.remove(default_email)
provider.property_mappings.add(mapping)
```

### Gotcha 3: kubelogin Needs Extra Scopes

By default, kubelogin only requests the `openid` scope. The token will lack
`email` and `groups` claims, causing:
```
oidc: parse username claims "email": claim not present
```

**Fix:** Add `--oidc-extra-scope` flags to the kubeconfig exec plugin:
```yaml
users:
- name: oidc-user
  user:
    exec:
      command: kubectl
      args:
        - oidc-login
        - get-token
        - --oidc-issuer-url=https://authentik.example.com/application/o/kubernetes/
        - --oidc-client-id=kubernetes
        - --oidc-extra-scope=email      # Required!
        - --oidc-extra-scope=profile
        - --oidc-extra-scope=groups
```

### Gotcha 4: Redirect URIs Must Use Regex Mode

kubelogin picks a random available port (tries 8000, 18000, then random).
Strict redirect URI matching like `http://localhost:8000/callback` will fail
when kubelogin uses a different port.

**Fix:** Use regex matching in the Authentik provider:
```json
{
  "redirect_uris": [
    {"matching_mode": "regex", "url": "http://localhost:.*"},
    {"matching_mode": "regex", "url": "http://127\\.0\\.0\\.1:.*"}
  ]
}
```

### Gotcha 5: Property Mappings API Endpoint Changed

In Authentik 2025.10.x, scope mappings are at:
- `propertymappings/provider/scope/` (new, correct)
- NOT `propertymappings/scope/` (old, returns 405 Method Not Allowed on POST)

### Gotcha 6: Static Pod Manifest Changes Need Full Cycle

See skill: `kubelet-static-pod-manifest-update` for the full restart procedure.

## Verification

After all fixes:
```bash
# 1. JWKS has a key
curl -s https://authentik.example.com/application/o/kubernetes/jwks/ | jq '.keys | length'
# Expected: 1 (or more)

# 2. Test auth
KUBECONFIG=/path/to/oidc-kubeconfig kubectl get namespaces
# Expected: browser opens, login, namespaces returned

# 3. Check API server logs for success
ssh master "sudo kubectl logs -n kube-system kube-apiserver-* | grep oidc | tail -5"
# Expected: no "Unable to authenticate" errors
```

## Notes
- The OAuth2 provider should use `client_type: public` (no client secret needed for kubelogin)
- Set `sub_mode: user_email` so the OIDC subject matches the RBAC binding
- Set `include_claims_in_id_token: true` for the token to contain claims directly
- Use `issuer_mode: per_provider` for a clean issuer URL
- RBAC ClusterRoleBindings should match on the user's email (the `--oidc-username-claim=email` value)
