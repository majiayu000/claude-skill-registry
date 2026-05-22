---
name: solana-security
description: Audit Solana programs (Anchor or native Rust) for security vulnerabilities. Use when reviewing smart contract security, finding exploits, analyzing attack vectors, performing security assessments, or when explicitly asked to audit, review security, check for bugs, or find vulnerabilities in Solana programs.
---

# Solana Security Auditing

Systematic security review framework for Solana programs, supporting both Anchor and native Rust implementations.

## Review Process

Follow this systematic 5-step process for comprehensive security audits:

### Step 1: Initial Assessment

Understand the program's context and structure:

- **Framework**: Anchor vs Native Rust (check for `use anchor_lang::prelude::*`)
- **Anchor version**: Check `Cargo.toml` for compatibility and known issues
- **Dependencies**: Oracles (Pyth, Switchboard), external programs, token programs
- **Program structure**: Count instructions, identify account types, analyze state management
- **Complexity**: Lines of code, instruction count, PDA patterns
- **Purpose**: DeFi, NFT, governance, gaming, etc.

### Step 2: Systematic Security Review

For each instruction, perform security checks in this order:

1. **Account Validation** - Verify signer, owner, writable, and initialization checks
2. **Arithmetic Safety** - Check all math operations use `checked_*` methods
3. **PDA Security** - Validate canonical bumps and seed uniqueness
4. **CPI Security** - Ensure cross-program invocations validate target programs
5. **Oracle/External Data** - Verify price staleness and oracle status checks

**→ See [references/security-checklists.md](references/security-checklists.md) for detailed checklists**

### Step 3: Vulnerability Pattern Detection

Scan for common vulnerability patterns:

- Type cosplay attacks
- Account reloading issues
- Improper account closing
- Missing lamports checks
- PDA substitution attacks
- Arbitrary CPI vulnerabilities
- Missing ownership validation
- Integer overflow/underflow

**→ See [references/vulnerability-patterns.md](references/vulnerability-patterns.md) for code examples and exploit scenarios**

### Step 4: Architecture and Testing Review

Evaluate overall design quality:

- PDA design patterns and collision prevention
- Account space allocation and rent exemption
- Error handling approach and coverage
- Event emission for critical state changes
- Compute budget optimization
- Test coverage (unit, integration, fuzz)
- Upgrade strategy and authority management

### Step 5: Generate Security Report

Provide findings using this structure:

**Severity Levels:**
- 🔴 **Critical**: Funds can be stolen/lost, protocol completely broken
- 🟠 **High**: Protocol can be disrupted, partial fund loss possible
- 🟡 **Medium**: Suboptimal behavior, edge cases, griefing attacks
- 🔵 **Low**: Code quality, gas optimization, best practices
- 💡 **Informational**: Recommendations, improvements, documentation

**Finding Format:**
```markdown
## 🔴 [CRITICAL] Title

**Location:** `programs/vault/src/lib.rs:45-52`

**Issue:**
Brief description of the vulnerability

**Vulnerable Code:**
```rust
// Show the problematic code
```

**Exploit Scenario:**
Step-by-step explanation of how this can be exploited

**Recommendation:**
```rust
// Show the secure alternative
```

**References:**
- [Link to relevant documentation or similar exploits]
```

**Report Summary:**
- Total findings by severity
- Critical issues first (prioritize by risk)
- Quick wins (easy fixes with high impact)
- Recommendations for testing improvements

## Quick Reference

### Essential Checks (Every Instruction)

**Anchor:**
```rust
// ✅ Account validation with constraints
#[derive(Accounts)]
pub struct SecureInstruction<'info> {
    #[account(
        mut,
        has_one = authority,  // Relationship check
        seeds = [b"vault", user.key().as_ref()],
        bump,  // Canonical bump
    )]
    pub vault: Account<'info, Vault>,

    pub authority: Signer<'info>,  // Signer required

    pub token_program: Program<'info, Token>,  // Program validation
}

// ✅ Checked arithmetic
let total = balance.checked_add(amount)
    .ok_or(ErrorCode::Overflow)?;
```

**Native Rust:**
```rust
// ✅ Manual account validation
if !authority.is_signer {
    return Err(ProgramError::MissingRequiredSignature);
}

if vault.owner != program_id {
    return Err(ProgramError::IllegalOwner);
}

// ✅ Checked arithmetic
let total = balance.checked_add(amount)
    .ok_or(ProgramError::ArithmeticOverflow)?;
```

### Critical Anti-Patterns

❌ **Never Do:**
- Use `saturating_*` arithmetic methods (hide errors)
- Use `unwrap()` or `expect()` in production code
- Use `init_if_needed` without additional checks
- Skip signer validation ("they wouldn't call this...")
- Use unchecked arithmetic operations
- Allow arbitrary CPI targets
- Forget to reload accounts after mutations

✅ **Always Do:**
- Use `checked_*` arithmetic (`checked_add`, `checked_sub`, etc.)
- Use `ok_or(error)?` for Option unwrapping
- Use explicit `init` with proper validation
- Require `Signer<'info>` or `is_signer` checks
- Use `Program<'info, T>` for CPI program validation
- Reload accounts after external calls that mutate state
- Validate account ownership, discriminators, and relationships

## Framework-Specific Patterns

### Anchor Security Patterns

**→ See [references/anchor-security.md](references/anchor-security.md) for:**
- Account constraint best practices
- Common Anchor-specific vulnerabilities
- Secure CPI patterns with `CpiContext`
- Event emission and monitoring
- Custom error handling

### Native Rust Security Patterns

**→ See [references/native-security.md](references/native-security.md) for:**
- Manual account validation patterns
- Secure PDA derivation and signing
- Low-level CPI security
- Account discriminator patterns
- Rent exemption validation

## Modern Practices (2025)

- **Use Anchor 0.30+** for latest security features
- **Implement Token-2022** with proper extension handling
- **Use `InitSpace` derive** for automatic space calculation
- **Emit events** for all critical state changes
- **Write fuzz tests** with Trident framework
- **Document invariants** in code comments
- **Follow progressive roadmap**: Dev → Audit → Testnet → Audit → Mainnet

## Security Fundamentals

**→ See [references/security-fundamentals.md](references/security-fundamentals.md) for:**
- Security mindset and threat modeling
- Core validation patterns (signers, owners, mutability)
- Input validation best practices
- State management security
- Arithmetic safety
- Re-entrancy considerations

## Common Vulnerabilities

**→ See [references/vulnerability-patterns.md](references/vulnerability-patterns.md) for:**
- Missing signer validation
- Integer overflow/underflow
- PDA substitution attacks
- Account confusion
- Arbitrary CPI
- Type cosplay
- Improper account closing
- Precision loss in calculations

Each vulnerability includes:
- ❌ Vulnerable code example
- 💥 Exploit scenario
- ✅ Secure alternative
- 📚 References

## Security Checklists

**→ See [references/security-checklists.md](references/security-checklists.md) for:**
- Account validation checklist
- Arithmetic safety checklist
- PDA and account security checklist
- CPI security checklist
- Oracle and external data checklist
- Token integration checklist

## Known Issues and Caveats

**→ See [references/caveats.md](references/caveats.md) for:**
- Solana-specific quirks and gotchas
- Anchor framework limitations
- Testing blind spots
- Common misconceptions
- Version-specific issues

## Security Resources

**→ See [references/resources.md](references/resources.md) for:**
- Official security documentation
- Security courses and tutorials
- Vulnerability databases
- Audit report examples
- Security tools (Trident, fuzzers)
- Security firms and auditors

## Key Questions for Every Audit

Always verify these critical security properties:

1. **Can an attacker substitute accounts?**
   - PDA validation, program ID checks, has_one constraints

2. **Can arithmetic overflow or underflow?**
   - All math uses checked operations, division by zero protected

3. **Are all accounts properly validated?**
   - Owner, signer, writable, initialized checks present

4. **Can the program be drained?**
   - Authorization checks, reentrancy protection, account confusion prevention

5. **What happens in edge cases?**
   - Zero amounts, max values, closed accounts, expired data

6. **Are external dependencies safe?**
   - Oracle validation (staleness, status), CPI targets verified, token program checks

## Audit Workflow

### Before Starting

1. Understand the protocol purpose and mechanics
2. Review documentation and specifications
3. Set up local development environment
4. Run existing tests and check coverage

### During Audit

1. Follow the 5-step review process systematically
2. Document findings with severity and remediation
3. Create proof-of-concept exploits for critical issues
4. Test fixes and verify they work

### After Audit

1. Present findings clearly prioritized by severity
2. Provide actionable remediation steps
3. Re-audit after fixes are implemented
4. Document lessons learned for the protocol

## Testing for Security

Beyond code review, validate security through testing:

- **Unit tests**: Test each instruction's edge cases
- **Integration tests**: Test cross-instruction interactions
- **Fuzz testing**: Use Trident to discover unexpected behaviors
- **Exploit scenarios**: Write POCs for found vulnerabilities
- **Upgrade testing**: Verify migration paths are secure

## Core Principle

**In Solana's account model, attackers can pass arbitrary accounts to any instruction.**

Security requires explicitly validating:
- ✅ Every account's ownership
- ✅ Every account's type (discriminator)
- ✅ Every account's relationships
- ✅ Every account's state
- ✅ Every signer requirement
- ✅ Every arithmetic operation
- ✅ Every external call

There are no implicit guarantees. **Validate everything, trust nothing.**
