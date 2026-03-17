---
name: clean-code
description: The Foundation Skill. LLM Firewall + 2025 Security + Cross-Skill Coordination. Use for ALL code output - prevents hallucinations, enforces security, ensures quality.
---
<domain_overview>
# 🛡️ CLEAN CODE: THE FOUNDATION
> **Philosophy:** This skill is the FOUNDATION - it applies to ALL other skills. Every piece of code must pass these gates.
**ALGORITHMIC ELEGANCE MANDATE (CRITICAL):** Never prioritize "clever" code over readable, intent-revealing engineering. AI-generated code often fails by introducing unnecessary abstractions or using vague naming conventions that obscure logic. You MUST use intent-revealing names for every variable and function. Any implementation that increases cognitive complexity without a proportional gain in performance or scalability must be rejected. Avoid "Hype-Driven Development"—proven patterns trump trending but unstable frameworks.
</domain_overview>
<iron_laws>
## 🚨 IRON LAWS
```
1. NO HALLUCINATED PACKAGES - Verify before import
2. NO LAZY PLACEHOLDERS - Code must be runnable
3. NO SECURITY SHORTCUTS - Production-ready defaults
4. NO OVER-ENGINEERING - Simplest solution first
```
</iron_laws>
<security_protocols>
## 📦 PROTOCOL 1: SUPPLY CHAIN SECURITY
LLMs hallucinate packages that sound real but don't exist.
1. **Verify before import** - `npm search` or `pip show` for unfamiliar packages
2. **Prefer battle-tested** - lodash, date-fns, zod over obscure alternatives
3. **Check npm audit / pip-audit** before adding new dependencies
4. **Pin versions** in production - no `^` or `~` for critical deps
**2025 AI Package Risks:**
- Never import AI "wrapper" libraries without verification
- LLM SDKs: Use official only (openai, anthropic, google-generativeai)
- Vector DBs: Stick to established (pinecone, weaviate, chromadb)
## 🔐 PROTOCOL 2: SECURITY-FIRST DEFAULTS
**Frontend Security:**
| Forbidden | Required |
|-----------|----------|
| `dangerouslySetInnerHTML` | DOMPurify sanitization |
| Inline event handlers | Event delegation |
| `eval()`, `new Function()` | Static code only |
| Storing tokens in localStorage | httpOnly cookies |
**Backend Security:**
| Forbidden | Required |
|-----------|----------|
| `CORS: *` | Explicit origin whitelist |
| Raw SQL strings | Parameterized queries |
| `chmod 777` | Principle of least privilege |
| Hardcoded secrets | Environment variables + validation |
**API Security (2025):**
- Rate limiting on ALL public endpoints
- Input validation at the gate (Zod/Pydantic)
- Output sanitization for AI-generated content
- PASETO > JWT for new projects
</security_protocols>
<modularity_and_placeholder_rules>
## 🏗️ PROTOCOL 3: NO LAZY PLACEHOLDERS
**Forbidden Patterns:**
```javascript
// ❌ BANNED
// TODO: Implement this
// ... logic goes here
function placeholder() { }
throw new Error('Not implemented');
```
**Required:**
- Every function must be runnable
- If too complex, break into smaller complete functions
- "Hurry" is not an excuse - write minimal viable implementation
## 📐 PROTOCOL 4: MODULARITY & STRUCTURE
**The 50/300 Rule:**
- Functions > 50 lines → Break down
- Files > 300 lines → Split into modules
**SOLID Principles:**
| Principle | Quick Check |
|-----------|-------------|
| **S**ingle Responsibility | Does this do ONE thing? |
| **O**pen/Closed | Can I extend without modifying? |
| **L**iskov Substitution | Can subtypes replace parent? |
| **I**nterface Segregation | Are interfaces minimal? |
| **D**ependency Inversion | Do I depend on abstractions? |
</modularity_and_placeholder_rules>
<complexity_and_dependencies>
## 🎯 PROTOCOL 5: COMPLEXITY CAP
**Native First:**
```javascript
// ❌ Don't install is-odd
npm install is-odd
// ✅ Use native
const isOdd = n => n % 2 !== 0;
```
**Anti-Patterns:**
- AbstractFactoryBuilderManager for simple functions
- 10 layers of abstraction for CRUD
- "Future-proofing" for requirements that don't exist
**YAGNI:** You Aren't Gonna Need It. Build for today's requirements.
## 🔄 PROTOCOL 6: DEPENDENCY HYGIENE
**Freshness Check:**
```bash
npm outdated      # Check for updates
npm audit         # Check for vulnerabilities
```
**The CVE Brake:**
- "Latest" is not always "Safest"
- If latest has Critical CVE → Rollback to last secure version
- Security > New Features
**2025 Recommended:**
| Category | Recommended |
|----------|-------------|
| Validation | zod, valibot |
| HTTP | ky, ofetch |
| State | zustand, jotai |
| ORM | drizzle, prisma |
| Auth | lucia, better-auth |
</complexity_and_dependencies>
<ai_era_protocols>
## 🤖 PROTOCOL 7: AI-ERA CONSIDERATIONS
**When Building AI Features:**
1. **Validate AI outputs** - Never trust raw LLM responses
2. **Rate limit AI calls** - Prevent cost explosions
3. **Sanitize before display** - AI can generate malicious content
4. **Log AI interactions** - For debugging and compliance
**When AI is Writing Code:**
1. **Verify imports exist** - AI hallucinates packages
2. **Check types are correct** - AI guesses at APIs
3. **Test edge cases** - AI misses boundary conditions
4. **Review security** - AI takes shortcuts
</ai_era_protocols>
<audit_and_reference>
## ✅ QUICK AUDIT CHECKLIST
Before committing ANY code:
- [ ] No hallucinated imports (verified packages exist)
- [ ] No security shortcuts (CORS, eval, hardcoded secrets)
- [ ] No lazy placeholders (// TODO, empty functions)
- [ ] Functions < 50 lines, files < 300 lines
- [ ] Dependencies audited (`npm audit` clean)
- [ ] Types are strict (no `any`)
---
## 🔗 CROSS-SKILL INTEGRATION
| When Using... | Clean Code Adds... |
|---------------|-------------------|
| `@frontend-design` | Security defaults, no eval, CSP awareness |
| `@backend-design` | Input validation, no raw SQL, Zero Trust |
| `@tdd-mastery` | No placeholders (tests enforce completeness) |
| `@planning-mastery` | Modularity guides task breakdown |
| `@brainstorming` | SOLID/YAGNI guide architecture decisions |
| `@debug-mastery` | Logging standards, no silent failures |
</audit_and_reference>
