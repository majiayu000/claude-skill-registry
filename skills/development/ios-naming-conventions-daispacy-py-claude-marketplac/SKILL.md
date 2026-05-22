---
name: ios-naming-conventions
description: Check Swift naming conventions for iOS code. Validates class names, variables, functions, and IBOutlets against project standards. Use when reviewing code readability, checking abbreviations, or enforcing naming consistency in Swift files.
allowed-tools: Read, Grep, Glob
---

# iOS Naming Conventions Checker

Validate Swift code naming against Payoo Merchant project standards for clarity and consistency.

## When to Activate

- "check naming", "naming conventions", "code readability"
- "abbreviations", "variable names", "rename"
- Reviewing code quality or consistency
- Onboarding new developers

## Naming Rules Summary

### Types (Classes, Structs, Enums, Protocols)
- **PascalCase**: `PaymentViewModel`, `TransactionRepository`
- **Descriptive**: Purpose immediately clear
- **Proper suffixes**: ViewModel, ViewController, UseCase, Repository

### Variables & Properties
- **camelCase**: `paymentAmount`, `isProcessing`
- **Meaningful**: No abbreviations (except URL, ID, VC, UC)
- **Booleans**: Prefix `is`, `has`, `should`, `can`
- **Collections**: Plural names (`transactions`, `stores`)

### Functions & Methods
- **camelCase** with verb prefix
- **Actions**: `loadTransactions()`, `processPayment()`
- **Queries**: `getTransaction()`, `hasPermission()`

### IBOutlets
- **Type suffix**: `amountTextField`, `confirmButton`, `tableView`

## Review Process

### Step 1: Scan Code

Read files and identify all declarations:
- Class/struct/enum/protocol declarations
- Variable and property declarations
- Function declarations
- IBOutlet declarations

### Step 2: Check Against Rules

For each identifier, verify:

**Classes/Types**:
- ✅ PascalCase
- ✅ Descriptive (not generic like "Manager")
- ✅ No abbreviations (except standard ones)
- ✅ Proper suffix (ViewModel, UseCase, etc.)

**Variables**:
- ✅ camelCase
- ✅ Meaningful names
- ✅ Boolean prefixes (is/has/should/can)
- ✅ Plural for collections
- ✅ No single letters (except loop indices)

**Functions**:
- ✅ Verb-based names
- ✅ Clear action or query intent
- ✅ No generic names (doSomething, handle)

**IBOutlets**:
- ✅ Type suffix included

### Step 3: Generate Report

```markdown
# Naming Conventions Review

## Summary
- 🔴 Critical (meaningless): X
- 🟠 High (abbreviations): X
- 🟡 Medium (missing prefixes): X
- 🟢 Low (style): X

## Issues by Type

### Classes/Structs/Enums
**File**: `path/to/file.swift:line`
Current: `PayVC`
Should be: `PaymentViewController`
Reason: [Explanation]

### Variables/Properties
[List with specific fixes]

### Functions
[List with specific fixes]

### IBOutlets
[List with specific fixes]

## Batch Rename Suggestions
Found `amt` in 5 locations → Rename all to `paymentAmount`

## Good Examples Found ✅
[Acknowledge well-named elements]
```

## Common Violations

### ❌ Abbreviations
```swift
class PayVC { }        → PaymentViewController
let amt: Double        → paymentAmount
func procPmt() { }     → processPayment()
```

### ❌ Single Letters
```swift
let x = transaction    → currentTransaction
let a = amount         → paymentAmount
```

### ❌ Generic/Meaningless
```swift
class Manager { }      → PaymentManager
func doSomething() { } → processRefundRequest()
func handle() { }      → handlePaymentError()
```

### ❌ Missing Prefixes
```swift
let loading: Bool      → isLoading: Bool
let valid: Bool        → isValid: Bool
```

### ❌ Missing Type Suffix
```swift
@IBOutlet weak var amount: UITextField!  → amountTextField
@IBOutlet weak var btn: UIButton!       → confirmButton
```

## Search Patterns

Use Grep to find:
- **Abbreviations**: `(let|var)\s+[a-z]{1,3}\s*[=:]`
- **IBOutlets**: `@IBOutlet.*weak var`
- **Booleans**: `(let|var)\s+[a-z]+.*:\s*Bool`

## Output Guidelines

**For each violation**:
1. File path and line number
2. Current name
3. Recommended name
4. Reason for change
5. Impact on code clarity

**Prioritize**:
- Critical: Meaningless names (hurts maintainability)
- High: Abbreviations (reduces clarity)
- Medium: Missing prefixes/suffixes
- Low: Style inconsistencies

## Quick Fixes

1. **Expand Abbreviation**: Use Xcode refactor tool
2. **Add Boolean Prefix**: Rename with is/has/should/can
3. **Add Type Suffix**: Update IBOutlet names

## Common Abbreviations to Fix

| ❌ Bad | ✅ Good |
|--------|---------|
| amt | paymentAmount |
| trx, tx | transaction |
| btn | button |
| lbl | label |
| vc | viewController |
| uc | useCase |
| repo | repository |

## Reference

**Detailed Examples**: See `examples.md` for extensive naming patterns and scenarios.
