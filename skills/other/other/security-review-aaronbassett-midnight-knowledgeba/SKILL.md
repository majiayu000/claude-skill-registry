---
name: compact-reviewer:security-review
description: Use when reviewing Compact contracts for security vulnerabilities, privacy leaks, disclosure violations, access control issues, or ZK-specific attack vectors.
---

# Security Review Skill

Comprehensive security analysis for Compact smart contracts on the Midnight Network.

## When to Use

This skill activates for queries about:
- Security vulnerabilities in Compact contracts
- Privacy and disclosure issues
- Access control verification
- ZK-specific attack patterns
- Audit and security review

**Trigger words**: security, vulnerability, audit, disclosure, access control, privacy leak, attack vector

## Quick Reference

### Security Checklist

| Category | Check | Severity if Failed |
|----------|-------|-------------------|
| **Access Control** | Exported circuits verify caller authorization | 🔴 Critical |
| **Disclosure** | All public outputs use `disclose()` | 🔴 Critical |
| **Input Validation** | All witness inputs validated/bounded | 🔴 Critical |
| **State Protection** | Ledger writes have authorization checks | 🟠 High |
| **ZK Attacks** | Low-entropy witnesses not used in hashes | 🔴 Critical |
| **Timing** | No witness-dependent control flow | 🟠 High |

### Common Vulnerabilities

```compact
// ❌ Missing access control
export circuit withdraw(amount: Uint<64>): [] {
    balance.decrement(amount);  // Anyone can call!
}

// ✅ With access control
export circuit withdraw(amount: Uint<64>): [] {
    const caller = get_caller_secret();
    assert hash(caller) == owner_hash.read();
    balance.decrement(amount);
}
```

```compact
// ❌ Disclosure violation
export circuit get_balance(): Uint<64> {
    return balance.read();  // Missing disclose!
}

// ✅ Explicit disclosure
export circuit get_balance(): Uint<64> {
    return disclose(balance.read());
}
```

### ZK Attack Vectors

| ID | Attack | Risk | Detection |
|----|--------|------|-----------|
| AV-03 | Nullifier Linkability | 🔴 Critical | Low-entropy input to `persistentHash()` |
| AV-06 | Witness Entropy Exhaustion | 🔴 Critical | Bounded witness types (Uint<8>, enums) |
| AV-01 | Implicit Taint Leakage | 🟠 High | Witness-dependent control flow |
| AV-08 | Circuit Under-Constraint | 🔴 Critical | Missing assertions on witness ranges |

## Review Process

### 1. Access Control Verification

For each `export circuit`:

1. Identify who should be authorized to call it
2. Verify authorization check exists (witness + assertion)
3. Check authorization uses proper cryptographic verification

```compact
// Pattern: Authorization check
witness get_admin_key(): Bytes<32>;

export circuit admin_action(): [] {
    const admin = get_admin_key();
    assert hash(admin) == admin_hash.read();  // ✓ Crypto verification
    // ... perform action
}
```

### 2. Disclosure Analysis

For each value returned from a circuit:

1. Trace value origin (ledger, witness, computation)
2. Verify `disclose()` is used for public outputs
3. Check for implicit disclosure via ledger writes

```compact
// Must use disclose() for:
// - Return values from export circuits
// - Values derived from witnesses that become public
// - Ledger state that should be visible
```

### 3. Input Validation

For each witness function:

1. Check type bounds (Uint<N> has 2^N values)
2. Verify assertions bound the valid range
3. Look for missing null/empty checks

```compact
// ❌ Unbounded witness
witness get_choice(): Uint<8>;  // 256 possibilities

export circuit vote(): [] {
    const choice = get_choice();
    voteTally[choice].increment(1);  // No bounds check!
}

// ✅ Bounded witness
export circuit vote(): [] {
    const choice = get_choice();
    assert choice < 5;  // Only 5 valid choices
    voteTally[choice].increment(1);
}
```

### 4. ZK-Specific Checks

Run through attack vector checklist:

| Check | Look For | If Found |
|-------|----------|----------|
| AV-01 | `if disclose(witness)` or witness in loop count | Flag timing leak |
| AV-03 | `persistentHash(low_entropy)` | Flag nullifier linkability |
| AV-06 | Uint<1-16> in security-critical paths | Flag brute-force risk |
| AV-08 | Witness used without range assertion | Flag under-constraint |

## References

- [Vulnerability Checklist](./references/vulnerability-checklist.md) - Complete vulnerability catalog
- [Disclosure Rules](./references/disclosure-rules.md) - Privacy leak detection patterns
- [ZK Attack Vectors](./references/zk-attack-vectors.md) - AV-01 through AV-12 documentation

## Related Skills

- [critical-issues](../critical-issues/SKILL.md) - Bug and logic error detection
- [compact-core/privacy-disclosure](../../../compact-core/skills/privacy-disclosure/SKILL.md) - Compact privacy model
- [compact-core/standard-library](../../../compact-core/skills/standard-library/SKILL.md) - Crypto function safety
