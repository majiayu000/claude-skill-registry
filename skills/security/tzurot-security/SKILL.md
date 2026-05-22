---
name: tzurot-security
description: Security best practices for Tzurot v3 - Secret management, AI-specific security (prompt injection, PII scrubbing), Economic DoS prevention, Discord permission verification, microservices security, and supply chain integrity. Use when handling secrets, user input, or security-critical code.
lastUpdated: '2026-01-21'
---

# Security Skill - Tzurot v3

**Use this skill when:** Handling secrets, user input, file uploads, AI providers, admin commands, or when security concerns arise.

## Quick Reference

```bash
# Pre-commit secret check
git diff --cached | grep -iE '(password|secret|token|api.?key|postgresql://|redis://)'

# Audit dependencies
npm audit --audit-level=moderate

# View Railway secrets (values hidden)
railway variables --service <name>
```

## 🚨 Tier 1: Core Security (MUST FOLLOW)

### 1. Never Commit Secrets

**Happened TWICE in this project. Always verify!**

| ❌ NEVER Commit              | ✅ Use Instead                   |
| ---------------------------- | -------------------------------- |
| Database URLs with passwords | Environment variables            |
| API keys/tokens              | `.env.example` with placeholders |
| Private keys                 | Railway secrets management       |
| Real user data in tests      | Generic test data                |

**If you commit a secret:**

1. **Rotate immediately** (regenerate in provider dashboard)
2. Update Railway: `railway variables --set "KEY=new-value"`
3. Consider git history rewrite if not shared

### GitGuardian False Positives (Test Secrets)

GitGuardian CI checks scan for secrets. Test files with fake API keys can trigger false positives.

**Solution Order of Preference:**

1. **Use low-entropy fake keys** (BEST - scanners naturally ignore these):

   ```typescript
   // ❌ WRONG - High entropy, triggers GitGuardian
   const apiKey = 'sk-test-byok-key-abc123xyz789';
   const apiKey = 'test-byok-key-not-a-real-secret';

   // ✅ CORRECT - Low entropy, obviously fake
   const apiKey = 'user-test-key-12345';
   const apiKey = 'fake-key-00000';
   const apiKey = 'PLACEHOLDER_KEY';
   ```

2. **Exclude test patterns in `.gitguardian.yaml`** (if format is strict):

   ```yaml
   # .gitguardian.yaml
   secret:
     ignored-paths:
       - '**/*.test.ts'
       - '**/*.spec.ts'
       - '**/test/**'
       - '**/__mocks__/**'
   ```

3. **Inline `ggignore` comment** (LAST RESORT - clutters code):

   ```typescript
   const apiKey = 'must-be-this-exact-format-abc123'; // ggignore
   ```

**Why low-entropy is best:** GitGuardian uses Shannon entropy to detect secrets. Simple patterns like `12345` or `00000` have low entropy and don't trigger scans. This keeps code clean without config files or comments.

**Reference:** [ggshield documentation](https://docs.gitguardian.com/ggshield-docs/reference/secret/ignore)

### 2. Environment Variable Management

```typescript
// ✅ CORRECT - Fail fast if missing
const required = ['DISCORD_TOKEN', 'DATABASE_URL', 'REDIS_URL'] as const;
for (const v of required) {
  if (!process.env[v]) throw new Error(`Missing: ${v}`);
}
```

### 3. Security Logging (No PII)

```typescript
// ❌ WRONG - Logs PII
logger.info({ user }, 'User authenticated');
logger.debug({ token }, 'Initializing');

// ✅ CORRECT - Log only safe identifiers
logger.info({ userId: user.id }, 'User authenticated');
logger.debug({ tokenPrefix: token.slice(0, 10) }, 'Initializing');
```

**NEVER log:** Emails, phones, IPs, usernames, message content, API keys
**Safe to log:** User IDs, guild IDs, channel IDs, timestamps, error codes

### 4. Token Budgeting (Economic DoS Prevention)

AI APIs cost money. Implement per-user token limits:

```typescript
// In Redis: token_budget:{userId} → { tokensUsed, windowStart }
if (budget.tokensUsed + estimated > BUDGET_PER_HOUR) {
  return res.status(429).json({ error: 'Token budget exceeded' });
}
```

### 5. Discord Permission Verification

```typescript
// ❌ WRONG - Trusts client-side
if (interaction.member.permissions.has('Administrator')) {
}

// ✅ CORRECT - Server-side with cache
const guild = await client.guilds.fetch(guildId);
const member = await guild.members.fetch(userId);
const hasAdmin = member.permissions.has(PermissionFlagsBits.Administrator);
```

### 6. Shell Command Safety (Command Injection Prevention)

**This vulnerability has occurred multiple times.** When executing shell commands with user-controlled or external data, NEVER use string interpolation.

```typescript
import { execFileSync, execSync } from 'node:child_process';

// ❌ WRONG - Command injection via string interpolation
execSync(`railway variables --set "${key}=${value}"`);
// If value = 'foo"; rm -rf /; echo "' → disaster!

// ❌ WRONG - Even with "trusted" variables, avoid habits
execSync(`git commit -m "${message}"`);

// ✅ CORRECT - Use execFileSync with array arguments
execFileSync('railway', ['variables', '--set', `${key}=${value}`]);

// ✅ CORRECT - Shell never interprets the arguments
execFileSync('git', ['commit', '-m', message]);

// ✅ OK - Static commands without interpolation
execSync('railway status');
execSync('git log --oneline -5');
```

**Why `execFileSync` is safe:**

- Arguments are passed directly to the process, not through a shell
- Shell metacharacters (`"; $ \` ()`) are treated as literal strings
- No possibility of command injection regardless of input

**When to use which:**
| Function | Use When | Safety |
|----------|----------|--------|
| `execFileSync(cmd, args)` | Any external data in args | ✅ Safe |
| `execSync(staticCmd)` | Fully static command string | ✅ Safe |
| `execSync(\`...\${var}\`)` | ❌ NEVER | ⚠️ Vulnerable |

**Test for this:** Add tests with shell metacharacters in values:

```typescript
const maliciousValue = 'test"; rm -rf /; echo "pwned';
// Verify your code passes this literally, not interprets it
```

## 🛡️ Tier 2: Important Security (SHOULD IMPLEMENT)

### 7. PII Scrubbing Before Embedding

Scrub emails, phones, SSNs before storing in pgvector:

```typescript
const EMAIL_REGEX = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}/g;
const scrubbedText = text.replace(EMAIL_REGEX, '<EMAIL_REDACTED>');
```

### 8. Prompt Injection Detection

```typescript
const JAILBREAK_PATTERNS = [
  /ignore (previous|all) (instructions|rules)/i,
  /dan mode/i,
  /developer mode/i,
  /forget (everything|all)/i,
];

if (JAILBREAK_PATTERNS.some(p => p.test(prompt))) {
  return { content: '⚠️ Prompt violates policies.', flagged: true };
}
```

### 9. Signed BullMQ Jobs (If Redis Compromised)

Sign jobs with HMAC to prevent injection:

```typescript
const signature = crypto.createHmac('sha256', SECRET).update(JSON.stringify(payload)).digest('hex');
// Include signature in job, verify in worker
```

### 10. Content Validation for Attachments

Validate using magic numbers, not extensions:

```typescript
import fileType from 'file-type';
const detected = await fileType.fromBuffer(buffer);
if (!ALLOWED_TYPES.includes(detected?.mime)) {
  /* reject */
}
```

### 11. Dependency Management

**Before installing ANY package:**

```bash
npm view <package>           # Exists?
npm audit                    # Vulnerabilities?
```

**Pin exact versions** in package.json (no `^` or `~`)

**Dependabot** handles weekly updates. See `.github/dependabot.yml`.

### 12. Discord Markdown Injection Prevention

**ALWAYS escape user-provided content** before displaying in Discord embeds:

```typescript
import { escapeMarkdown } from 'discord.js';

// ✅ CORRECT - Escape at display time
const displayName = escapeMarkdown(character.displayName);
embed.setTitle(`Character: ${displayName}`);

// ❌ WRONG - Raw user input in embed
embed.setTitle(`Character: ${character.displayName}`); // Vulnerable!
```

**Fields to always escape:**

- Guild names, channel names, usernames
- Character names, display names, persona fields
- Personality names, config names, preset names
- Any user-provided text in embeds

**Pattern:** Store raw values in data structures, escape at display time only.

## Admin Endpoint Security

Current: `X-Owner-Id` header validation
Future: HMAC signatures with `INTERNAL_SERVICE_SECRET`

```bash
# Rate limit admin endpoints
const adminRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, max: 10
});
```

## Red Flags - Consult This Skill When:

- Committing changes with credentials
- Handling user input to AI
- Processing file uploads
- Installing npm packages suggested by AI
- Implementing admin/destructive commands
- Logging anything with user data
- **Writing shell commands with execSync/spawn** (use execFileSync with arrays!)

## Related Skills

- **tzurot-observability** - Security logging without PII
- **tzurot-types** - Input validation with Zod schemas
- **tzurot-git-workflow** - Pre-commit verification checks

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Discord Bot Security](https://discord.com/developers/docs/topics/security)
- [Prompt Injection Primer](https://simonwillison.net/2023/Apr/14/worst-that-can-happen/)
- Project post-mortems: `docs/postmortems/PROJECT_POSTMORTEMS.md`
