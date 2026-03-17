---
name: dev_invoke_kimi-cli
description: |
  Delegate testing, QA, and code review tasks to Opencode CLI using Kimi K2.5 model via markdown file handoff.
  Write test request to TASK.md, Opencode with Kimi K2.5 generates tests/reviews, outputs to OUTPUT.md.
  Use for test generation, QA verification, edge case detection, code coverage analysis, security reviews.

  Triggers: kimi, kimi k2.5, kimi cli, opencode kimi, test generation, QA, quality assurance,
  code review, unit tests, integration tests, edge cases, test coverage, testing, kimisubagent,
  togetherai kimi, opencode/kimi-k2.5-free, togetherai/moonshotai/Kimi-K2.5

  Prerequisites: Opencode CLI installed, Together.ai API key (if using togetherai provider)
  Models: opencode/kimi-k2.5-free (recommended), togetherai/moonshotai/Kimi-K2.5 (alternative)
---

# Invoking Kimi CLI (via Opencode)

Delegate testing, quality assurance, and code review tasks to Opencode CLI using the Kimi K2.5 model via markdown files for input and output.

## Pattern: Markdown File Handoff

```
Claude Code                         Opencode CLI + Kimi K2.5
    |                                   |
    +-- Write TASK.md ------------------+
    |   (test/review requirements)      |
    |                                   |
    +-- Execute: opencode run -m        |
    |   opencode/kimi-k2.5-free         |
    |   "Read TASK.md..."               |
    |                                   |
    |                                   +-- Reads TASK.md
    |                                   +-- Generates tests/review
    |                                   +-- Writes OUTPUT.md
    |                                   |
    +-- Read OUTPUT.md <----------------+
    |   (tests + findings + results)    |
    v                                   v
```

**Benefits**:
- No shell escaping issues
- Full context in structured format
- Explicit output structure
- Supports both Opencode and Together.ai providers
- Excellent for edge case detection

## When to Use

- **Test generation** - Create comprehensive test suites for existing code
- **Test coverage analysis** - Identify gaps in test coverage
- **Edge case detection** - Find boundary conditions and edge cases
- **QA verification** - Validate implementations meet requirements
- **Code review** - Secondary opinion on code quality and correctness
- **Regression testing** - Generate regression test scenarios
- **Integration testing** - Validate component interactions
- **Security reviews** - Security-focused code analysis

## Model Selection

### Recommended Models

| Model | Provider | Use Case | Status |
|-------|----------|----------|--------|
| `opencode/kimi-k2.5-free` | Opencode (Moonshot) | **Recommended.** Free tier, 2,000 req/day, excellent for testing/QA | ✅ Verified |
| `opencode/kimi-k2.5` | Opencode (Moonshot) | Paid tier with higher rate limits | ✅ Available |
| `togetherai/moonshotai/Kimi-K2.5` | Together.ai | Alternative provider, same model quality | ✅ Verified |
| `togetherai/moonshotai/Kimi-K2-5` | Together.ai | Alternative naming convention | ✅ Available |

**Default:** `opencode/kimi-k2.5-free` for testing/QA tasks.

**Recommendation:** Use `opencode/kimi-k2.5-free` for all testing and QA tasks. Kimi K2.5 excels at:
- Identifying edge cases and boundary conditions
- Generating comprehensive test scenarios
- Analyzing code for quality issues
- Providing thorough code reviews

## Provider Selection Guide

### Choose Opencode (`opencode/kimi-k2.5-free`) when:
- ✅ You want a free tier with generous limits (2,000 req/day)
- ✅ You're already using Opencode for other tasks
- ✅ You prefer integrated billing with Opencode
- ✅ You want simpler setup (no additional API keys)

### Choose Together.ai (`togetherai/moonshotai/Kimi-K2.5`) when:
- ✅ You have existing Together.ai credits or API keys
- ✅ You need different rate limits or pricing
- ✅ You prefer Together.ai's infrastructure
- ✅ You're already using Together.ai for other models

## Invocation

### Standard Pattern (Recommended)

```bash
opencode run -m opencode/kimi-k2.5-free \
  "Read TASK.md in the current directory. Follow the testing instructions. Write all results to OUTPUT.md."
```

### Alternative: Together.ai Provider

```bash
opencode run -m togetherai/moonshotai/Kimi-K2.5 \
  "Read TASK.md in the current directory. Follow the testing instructions. Write all results to OUTPUT.md."
```

### Interactive Mode (if run command has issues)

```bash
# Start opencode TUI with Kimi K2.5 (Opencode)
cd /path/to/project && opencode . -m opencode/kimi-k2.5-free

# Or with Together.ai
cd /path/to/project && opencode . -m togetherai/moonshotai/Kimi-K2.5
```

### Piping Input (Most Reliable)

```bash
# Create a prompt file
echo "Generate unit tests for the Calculator class" > prompt.txt
cat prompt.txt | opencode run -m opencode/kimi-k2.5-free
```

## Core Flags Reference

| Flag | Purpose |
|------|---------|
| `-m, --model` | Model to use (e.g., `opencode/kimi-k2.5-free`) |
| `-C, --continue` | Continue the last session |
| `-s, --session` | Session ID to resume |
| `--prompt` | Initial prompt to send |
| `-h, --help` | Show help |

## Task File Template (TASK.md)

```markdown
# Task: [Test Generation / Code Review / QA]

## Objective
[Clear statement of testing/review goal]

### Examples:
- Generate unit tests for user authentication module
- Review payment processing code for security issues
- Create integration tests for API endpoints
- Perform QA verification of search functionality

## Code to Test/Review

### File: src/auth/login.ts
```typescript
// Paste code here
```

### File: src/auth/validate.ts
```typescript
// Paste supporting code
```

## Requirements

### Test Requirements (if generating tests)
- [ ] Cover all public methods/functions
- [ ] Include happy path scenarios
- [ ] Include error/edge cases
- [ ] Test boundary conditions
- [ ] Mock external dependencies
- [ ] Achieve >80% code coverage

### Review Criteria (if reviewing code)
Rate findings: CRITICAL | HIGH | MEDIUM | LOW

#### Security
- Input validation gaps
- Authentication/authorization issues
- Data exposure risks

#### Reliability
- Error handling coverage
- Race conditions
- Resource leaks

#### Maintainability
- Testability of code
- Code clarity
- Documentation

## Test Framework
- **Framework:** Jest / Mocha / Vitest / pytest / etc.
- **Location:** `tests/` or `__tests__/` directory
- **Naming:** `[filename].test.[ext]` or `[filename].spec.[ext]`

## Context
- [Any relevant background, constraints, or requirements]
- [Dependencies or integrations]
- [Performance requirements]
- [Compliance needs]

## Output Format

Write to OUTPUT.md:
- Summary of tests generated or review findings
- Test scenarios/cases with descriptions
- File locations for generated tests
- Coverage analysis (if applicable)
- Issues found with severity ratings
- Recommendations for fixes
- Session ID for follow-up
```

## Output File Template (OUTPUT.md)

Opencode with Kimi K2.5 should produce:

```markdown
# Results: [Task Title]

## Summary
[Brief overview of what was accomplished]

## Generated Tests (if applicable)

### Test Files Created
| File | Description | Coverage |
|------|-------------|----------|
| `tests/auth/login.test.ts` | Unit tests for login | 95% |
| `tests/auth/validate.test.ts` | Validation tests | 88% |

### Test Scenarios

#### Happy Path
1. [Test case description]
   - Input: [example input]
   - Expected: [expected output]

#### Edge Cases
1. [Edge case description]
   - Input: [boundary value]
   - Expected: [expected behavior]

#### Error Cases
1. [Error scenario]
   - Input: [invalid input]
   - Expected: [error handling]

## Review Findings (if applicable)

| Severity | Location | Issue | Recommendation |
|----------|----------|-------|----------------|
| CRITICAL | login.ts:45 | SQL injection | Use parameterized queries |
| HIGH | auth.ts:23 | Missing rate limiting | Add rate limiter |
| MEDIUM | users.ts:78 | No input validation | Add Zod validation |
| LOW | utils.ts:12 | Magic number | Extract constant |

## Code Coverage Analysis
- **Overall:** 87%
- **Critical paths:** 95%
- **Uncovered lines:** [list of uncovered code sections]

## Issues Encountered
- [Any problems and resolutions]

## Recommendations
1. [Priority action items]
2. [Secondary improvements]
3. [Testing best practices to adopt]

## Session
Session ID: `<session_id>` (for follow-up)
```

## Workflow Example

### Example 1: Test Generation

#### 1. Claude Code writes TASK.md

```markdown
# Task: Generate Unit Tests for User Authentication

## Objective
Create comprehensive unit tests for the user authentication module covering login, registration, and password reset.

## Code to Test

### File: src/auth/auth.service.ts
```typescript
export class AuthService {
  async login(email: string, password: string): Promise<AuthResult> {
    const user = await this.userRepo.findByEmail(email);
    if (!user) throw new UnauthorizedError('Invalid credentials');
    
    const valid = await bcrypt.compare(password, user.passwordHash);
    if (!valid) throw new UnauthorizedError('Invalid credentials');
    
    const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET);
    return { token, user: this.sanitizeUser(user) };
  }
  
  async register(email: string, password: string): Promise<User> {
    const existing = await this.userRepo.findByEmail(email);
    if (existing) throw new ConflictError('Email already exists');
    
    const hash = await bcrypt.hash(password, 10);
    return this.userRepo.create({ email, passwordHash: hash });
  }
}
```

## Requirements

### Test Requirements
- [ ] Test successful login with valid credentials
- [ ] Test login failure with invalid email
- [ ] Test login failure with wrong password
- [ ] Test successful registration
- [ ] Test registration with existing email
- [ ] Test JWT token generation
- [ ] Mock database repository
- [ ] Mock bcrypt and jwt

## Test Framework
- **Framework:** Jest
- **Location:** `tests/auth/`
- **Mocking:** jest.mock()

## Context
- Application uses TypeScript
- JWT tokens expire in 24 hours
- Passwords must be hashed with bcrypt (10 rounds)
- Database is PostgreSQL via TypeORM

## Output Format
Write to OUTPUT.md with test scenarios, generated test code, coverage analysis, and any edge cases identified.
```

#### 2. Execute Opencode with Kimi K2.5

```bash
opencode run -m opencode/kimi-k2.5-free \
  "Read TASK.md in the current directory. Follow the instructions to generate comprehensive unit tests. Write all results to OUTPUT.md."
```

#### 3. Claude Code reads OUTPUT.md

Review the generated tests, check coverage, and integrate into the test suite.

### Example 2: Code Review

#### 1. Claude Code writes TASK.md

```markdown
# Task: Security Review of Payment Processing

## Objective
Perform security-focused code review of payment processing module.

## Code to Review

### File: src/payments/payment.service.ts
[Code here...]

## Review Criteria
Rate findings: CRITICAL | HIGH | MEDIUM | LOW

### Security Focus
- Input validation
- SQL injection risks
- Authentication/authorization
- Sensitive data handling
- PCI compliance

## Context
- B2B SaaS application
- Handles credit card data
- SOC2 compliance required

## Output Format
Write security findings to OUTPUT.md with severity ratings and specific fix recommendations.
```

#### 2. Execute Opencode with Kimi K2.5

```bash
opencode run -m opencode/kimi-k2.5-free \
  "Read TASK.md, perform security review following the criteria, write findings to OUTPUT.md"
```

#### 3. Review Findings

Claude Code reads OUTPUT.md and addresses security issues.

## Environment Variables

```bash
# For Opencode provider (Moonshot AI)
MOONSHOT_API_KEY=xxx      # Kimi models via Opencode (if needed)

# For Together.ai provider
TOGETHER_API_KEY=xxx      # Kimi models via Together.ai

# Alternative providers
OPENAI_API_KEY=xxx        # OpenAI models
GEMINI_API_KEY=xxx        # Google Gemini models
```

**Note:** Set the appropriate API key for your chosen provider. Opencode will use the key matching the model provider prefix (e.g., `togetherai/*` models need `TOGETHER_API_KEY`).

## Rate Limits

### Opencode (Moonshot AI)
| Limit | Value (Free Tier) |
|-------|-------------------|
| Requests/minute | 60 |
| Requests/day | 2,000 |
| Tokens/request | 128K context window |

### Together.ai
| Limit | Value |
|-------|-------|
| Requests/minute | Varies by plan |
| Requests/day | Varies by plan |
| Tokens/request | 128K context window |

**Note:** Together.ai rate limits depend on your account tier. Check your Together.ai dashboard for current limits.

## Quick Reference Table

| Provider | Model Path | API Key | Free Tier |
|----------|-----------|---------|-----------|
| Opencode | `opencode/kimi-k2.5-free` | Not needed* | 2,000 req/day |
| Opencode | `opencode/kimi-k2.5` | Not needed* | Paid |
| Together.ai | `togetherai/moonshotai/Kimi-K2.5` | `TOGETHER_API_KEY` | Varies |

*Opencode may use built-in credits or require authentication via `opencode auth`

## Comparison: When to Use Kimi vs Gemini vs Codex

| Task | Kimi K2.5 | Gemini | Codex |
|------|:---------:|:------:|:-----:|
| Test generation | ✅ | ✅ | ✅ |
| Edge case detection | ✅ | ✅ | ⚠️ |
| Code coverage analysis | ✅ | ✅ | ⚠️ |
| QA verification | ✅ | ✅ | ⚠️ |
| Security-focused code review | ✅ | ✅ | ⚠️ |
| General code review | ✅ | ✅ | ⚠️ |
| Test maintenance | ✅ | ✅ | ✅ |
| Implementation | ⚠️ | ⚠️ | ✅ |
| Refactoring | ⚠️ | ⚠️ | ✅ |
| Large codebase analysis | ✅ | ✅ | ⚠️ |
| Documentation review | ✅ | ✅ | ⚠️ |

**Legend:**
- ✅ = Excellent choice
- ⚠️ = Viable but not optimal

### Decision Guide

**Use Kimi K2.5 (via Opencode/Together.ai) when:**
- Primary goal is generating comprehensive test suites
- You need thorough edge case identification
- QA verification of existing implementations
- Security-focused code reviews
- Testing TypeScript/JavaScript/Python code
- Free tier with generous limits (2,000 req/day via Opencode)

**Use Gemini (via Gemini CLI) when:**
- Code review is the primary goal (not test generation)
- You need 1M+ token context for large codebase analysis
- Documentation review and knowledge extraction
- Security audits without test generation
- Maximum context window needed

**Use Codex (via Codex CLI) when:**
- Primary goal is implementation or refactoring
- Test generation is secondary to code changes
- Complex multi-file modifications needed
- Heavy reasoning tasks beyond testing

## Integration with Other Skills

**Works well with:**
- `dev_invoke_gemini-cli` - Cross-verify test coverage with Gemini
- `dev_invoke_codex-cli` - Implement fixes after Kimi identifies issues
- `using-git-worktrees` - Create isolated workspace for test development
- `triple-model-code-review` - Multi-model validation

**Sequence example:**
```
1. Kimi K2.5: Generate tests → Identify uncovered edge cases
2. Codex: Implement missing edge case handling
3. Kimi K2.5: Verify fixes and regenerate tests
4. Gemini: Review final implementation
```

## Tips

1. **Include full code** - Paste actual code in TASK.md, don't just reference files
2. **Specify test framework** - Tell Opencode exactly which framework to use
3. **Define coverage targets** - Set clear coverage expectations
4. **List edge cases explicitly** - Ask Kimi K2.5 to identify additional edge cases
5. **Request specific output** - Define exactly what OUTPUT.md should contain
6. **Use full model path** - Use `opencode/kimi-k2.5-free` not just `kimi-k2.5`
7. **Mock external dependencies** - Remind Opencode to mock databases, APIs, etc.
8. **Test data examples** - Provide sample inputs/outputs for clarity
9. **Try piping input** - If `run` command fails, use `cat prompt.txt | opencode run ...`
10. **Use interactive mode** - Start with `opencode . -m <model>` for complex tasks

## Troubleshooting

### Issue: "Session not found" error
**Solution:** Use interactive mode instead:
```bash
opencode . -m opencode/kimi-k2.5-free
```

### Issue: "DecimalError" with Together.ai
**Solution:** This is cosmetic - the output is still generated. Use the interactive mode or piping method.

### Issue: API key errors
**Solution:** Set the appropriate environment variable:
```bash
export TOGETHER_API_KEY=your_key_here
# or
export MOONSHOT_API_KEY=your_key_here
```

## Session Management

- Use `opencode --continue` to resume last session
- Use `opencode -s <session_id>` to resume specific session
- Sessions are stored locally by Opencode
- Session IDs appear in OUTPUT.md for reference
