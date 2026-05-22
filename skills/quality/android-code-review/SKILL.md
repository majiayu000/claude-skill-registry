---
name: android-code-review
description: Critical Android code review for Payoo Android app. Focuses on high-impact issues - naming conventions, memory leaks, UIState patterns, business logic placement, lifecycle management, and MVI/MVVM pattern violations. Use when reviewing Kotlin files, pull requests, or checking ViewModels, Activities, Fragments, UseCases, and Repositories.
allowed-tools: Read, Grep, Glob
---

# Android Code Review - Critical Issues Focus

Expert Android code reviewer for Payoo Android application, focusing on CRITICAL and HIGH PRIORITY issues that impact app stability, maintainability, and architecture.

## When to Activate

- "review android code", "check android file", "review android PR"
- Mentions Kotlin/Java files: Activity, Fragment, ViewModel, UseCase, Repository
- "code quality", "best practices", "check android standards"
- MVI/MVVM patterns, UIState, business logic, lifecycle issues

## Review Process

### Step 1: Identify Scope
Determine what to review:
- Specific files (e.g., "PaymentViewModel.kt")
- Directories (e.g., "payment module")
- Git changes (recent commits, PR diff)
- Entire module or feature

### Step 2: Read and Analyze
Use Read tool to examine files, focusing on CRITICAL and HIGH PRIORITY issues only.

### Step 3: Apply Critical Standards

## 🎯 CRITICAL FOCUS AREAS

### 1. Naming Conventions 🔴 HIGH
**Impact**: Code readability, maintainability, team collaboration

**Check for**:
- **Types**: Must be PascalCase, descriptive (e.g., `PaymentViewModel`, not `pmtVM`)
- **Variables/Functions**: Must be camelCase (e.g., `paymentAmount`, not `payment_amount`)
- **Constants**: Must be UPPER_SNAKE_CASE (e.g., `MAX_RETRY_COUNT`)
- **Booleans**: Must have `is`/`has`/`should`/`can` prefix (e.g., `isLoading`, not `loading`)
- **UIState properties**: Clear, specific names (e.g., `isPaymentProcessing`, not `state1`)
- **NO abbreviations** except URL, ID, API, HTTP, UI (e.g., `user`, not `usr`)

**Common violations**:
```kotlin
// ❌ BAD
var usr: User? = null
val loading = false
var state1 = ""

// ✅ GOOD
var user: User? = null
val isLoading = false
var paymentState = ""
```

### 2. Memory Leaks 🔴 CRITICAL
**Impact**: App crashes, ANR, poor performance

**Check for**:
- **ViewModel references**: NEVER hold Activity/Fragment/View references
- **Coroutine cancellation**: All coroutines must be cancelled with lifecycle
- **Context leaks**: Use ApplicationContext for long-lived objects
- **Listener cleanup**: Remove listeners in onDestroy/onCleared
- **Static references**: Avoid static references to Activities/Views

**Common violations**:
```kotlin
// ❌ CRITICAL - Memory Leak
class PaymentViewModel : ViewModel() {
    private var activity: Activity? = null // LEAK!

    fun setActivity(act: Activity) {
        activity = act
    }
}

// ❌ CRITICAL - Coroutine not cancelled
GlobalScope.launch { // Will leak!
    // work
}

// ✅ GOOD
class PaymentViewModel : ViewModel() {
    // No Activity reference

    fun doWork() {
        viewModelScope.launch { // Cancelled when ViewModel cleared
            // work
        }
    }
}
```

### 3. UIState Pattern 🔴 HIGH
**Impact**: State consistency, UI reliability, debugging

**Check for**:
- **Single source of truth**: Use sealed class or data class for UIState
- **Immutable state**: Use `StateFlow<UIState>` or `State<UIState>`
- **All UI states covered**: Loading, Success, Error, Empty
- **No scattered state**: Don't use multiple LiveData/StateFlow for related state
- **Type safety**: Use sealed classes for state variants

**Common violations**:
```kotlin
// ❌ BAD - Scattered state
class PaymentViewModel : ViewModel() {
    val isLoading = MutableStateFlow(false)
    val errorMessage = MutableStateFlow<String?>(null)
    val data = MutableStateFlow<Payment?>(null)
    val isEmpty = MutableStateFlow(false)
}

// ✅ GOOD - Single UIState
sealed class PaymentUIState {
    object Loading : PaymentUIState()
    data class Success(val payment: Payment) : PaymentUIState()
    data class Error(val message: String) : PaymentUIState()
    object Empty : PaymentUIState()
}

class PaymentViewModel : ViewModel() {
    private val _uiState = MutableStateFlow<PaymentUIState>(PaymentUIState.Loading)
    val uiState: StateFlow<PaymentUIState> = _uiState.asStateFlow()
}
```

### 4. Business Logic Placement 🔴 HIGH
**Impact**: Testability, reusability, architecture integrity

**Check for**:
- **ViewModels**: Should ONLY orchestrate, NOT contain business logic
- **UseCases**: Must contain ALL business logic
- **Repositories**: Data operations only, NO business decisions
- **Activities/Fragments**: UI logic only, NO business/data logic
- **Single Responsibility**: Each UseCase does ONE thing

**Common violations**:
```kotlin
// ❌ BAD - Business logic in ViewModel
class PaymentViewModel(private val repository: PaymentRepository) : ViewModel() {
    fun processPayment(amount: Double) {
        viewModelScope.launch {
            // ❌ Business logic in ViewModel!
            if (amount <= 0) return@launch
            val fee = amount * 0.02
            val total = amount + fee
            repository.savePayment(total)
        }
    }
}

// ✅ GOOD - Business logic in UseCase
class ProcessPaymentUseCase(private val repository: PaymentRepository) {
    suspend operator fun invoke(amount: Double): Result<Payment> {
        // ✅ Business logic here
        if (amount <= 0) return Result.failure(Exception("Invalid amount"))
        val fee = amount * 0.02
        val total = amount + fee
        return repository.savePayment(total)
    }
}

class PaymentViewModel(private val processPaymentUseCase: ProcessPaymentUseCase) : ViewModel() {
    fun processPayment(amount: Double) {
        viewModelScope.launch {
            // ✅ ViewModel only orchestrates
            processPaymentUseCase(amount)
        }
    }
}
```

### 5. Lifecycle Management 🔴 CRITICAL
**Impact**: Crashes, memory leaks, state loss

**Check for**:
- **Coroutine scopes**: Use `viewModelScope` or `lifecycleScope`, NEVER `GlobalScope`
- **Fragment observers**: Must use `viewLifecycleOwner`, NOT `this`
- **Resource cleanup**: Cleanup in `onCleared()` (ViewModel) or `onDestroy()`
- **Configuration changes**: Handle rotation properly with ViewModel
- **Flow collection**: Use `repeatOnLifecycle` or `flowWithLifecycle`

**Common violations**:
```kotlin
// ❌ CRITICAL - Wrong lifecycle owner in Fragment
class PaymentFragment : Fragment() {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        viewModel.uiState.observe(this) { // ❌ Should be viewLifecycleOwner
            // Update UI
        }
    }
}

// ❌ CRITICAL - GlobalScope leak
GlobalScope.launch {
    repository.getData()
}

// ✅ GOOD
class PaymentFragment : Fragment() {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        viewModel.uiState.observe(viewLifecycleOwner) { // ✅ Correct
            // Update UI
        }

        viewLifecycleOwner.lifecycleScope.launch {
            viewModel.uiState.collect { state ->
                // Handle state
            }
        }
    }
}
```

### 6. MVI/MVVM Pattern Violations 🔴 HIGH
**Impact**: Architecture consistency, maintainability, testability

**MVVM Pattern Requirements**:
- **ViewModel**: Holds UI state, handles user actions, calls UseCases
- **View (Activity/Fragment)**: Observes state, renders UI, sends user events
- **Model (UseCase + Repository)**: Business logic and data operations

**MVI Pattern Requirements**:
- **Intent**: User actions as sealed class
- **Model/State**: Single immutable UIState
- **View**: Renders state, sends intents
- **ViewModel**: Processes intents, updates state

**Check for**:
- **No direct repository calls from ViewModel** (must use UseCase)
- **ViewModel doesn't expose mutable state** (use private Mutable, public immutable)
- **View doesn't contain business logic**
- **Unidirectional data flow** (View → Intent/Action → ViewModel → State → View)

**Common violations**:
```kotlin
// ❌ BAD - MVVM violation: ViewModel calling Repository directly
class PaymentViewModel(
    private val paymentRepository: PaymentRepository // ❌ Should inject UseCase
) : ViewModel() {
    fun loadPayments() {
        viewModelScope.launch {
            val payments = paymentRepository.getPayments() // ❌ Skip UseCase layer
        }
    }
}

// ❌ BAD - Exposed mutable state
class PaymentViewModel : ViewModel() {
    val uiState = MutableStateFlow<UIState>(UIState.Loading) // ❌ Mutable exposed!
}

// ❌ BAD - Business logic in View
class PaymentActivity : AppCompatActivity() {
    fun onPayClick() {
        val amount = amountEditText.text.toString().toDouble()
        if (amount > 1000) { // ❌ Business logic in Activity!
            // apply discount
        }
        viewModel.processPayment(amount)
    }
}

// ✅ GOOD - Proper MVVM
class PaymentViewModel(
    private val getPaymentsUseCase: GetPaymentsUseCase, // ✅ UseCase injected
    private val processPaymentUseCase: ProcessPaymentUseCase
) : ViewModel() {
    private val _uiState = MutableStateFlow<PaymentUIState>(PaymentUIState.Loading)
    val uiState: StateFlow<PaymentUIState> = _uiState.asStateFlow() // ✅ Immutable exposed

    fun loadPayments() {
        viewModelScope.launch {
            _uiState.value = PaymentUIState.Loading
            when (val result = getPaymentsUseCase()) { // ✅ Use UseCase
                is Result.Success -> _uiState.value = PaymentUIState.Success(result.data)
                is Result.Error -> _uiState.value = PaymentUIState.Error(result.message)
            }
        }
    }
}

class PaymentActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // ✅ Only UI logic
        lifecycleScope.launch {
            viewModel.uiState.collect { state ->
                when (state) {
                    is PaymentUIState.Loading -> showLoading()
                    is PaymentUIState.Success -> showPayments(state.payments)
                    is PaymentUIState.Error -> showError(state.message)
                }
            }
        }

        payButton.setOnClickListener {
            viewModel.processPayment(amountEditText.text.toString()) // ✅ Just forward to ViewModel
        }
    }
}
```

### Step 4: Generate Report

Focus ONLY on CRITICAL (🔴) and HIGH (🟠) priority issues. Skip medium and low priority findings.

Provide structured output with:
- **Summary**: Only 🔴 Critical and 🟠 High counts
- **Critical Issues**: Memory leaks, lifecycle violations, crashes
- **High Priority Issues**: Architecture violations, naming, UIState problems, business logic misplacement
- **Code examples**: Current vs. fixed code
- **Explanations**: Why it matters and impact
- **Recommendations**: Prioritized actions

## Severity Levels - CRITICAL & HIGH ONLY

🔴 **CRITICAL** - Fix immediately (blocks release)
- **Memory leaks**: Activity/Context/View references in ViewModel
- **Lifecycle violations**: GlobalScope usage, wrong lifecycle owner in Fragments
- **Coroutine leaks**: Coroutines not cancelled with lifecycle
- **Crash risks**: UI updates on background thread, unhandled exceptions
- **Resource leaks**: Listeners/callbacks not cleaned up

🟠 **HIGH PRIORITY** - Fix before merge
- **Naming violations**: Abbreviations, wrong case, unclear names, missing is/has prefix
- **UIState problems**: Scattered state, no sealed class, mutable state exposed
- **Business logic misplacement**: Logic in ViewModel/Activity instead of UseCase
- **Architecture violations**: ViewModel calling Repository directly (skipping UseCase layer)
- **Wrong pattern usage**: MVVM/MVI principles violated
- **Lifecycle issues**: Not using viewLifecycleOwner, improper Flow collection

## 🚫 IGNORE (Out of Scope)
- Code style and formatting (handled by linter)
- Documentation and comments
- Performance optimizations (unless critical)
- Security issues (separate review)
- Test coverage
- Dependency injection setup
- Medium/Low priority issues

## Output Format

```markdown
# Android Code Review Report - Critical & High Priority Issues

## Summary
- 🔴 Critical: X issues (MUST fix before release)
- 🟠 High Priority: X issues (MUST fix before merge)
- ⏭️ Medium/Low issues: Skipped (not in scope)

## 🔴 CRITICAL ISSUES

### 🔴 Memory Leak - [Specific Issue]
**File**: `path/to/file.kt:line`
**Impact**: App crash, ANR, memory exhaustion

**Current**:
```kotlin
// problematic code
```

**Fix**:
```kotlin
// corrected code
```

**Why**: [Explanation of memory leak and crash risk]

---

### 🔴 Lifecycle Violation - [Specific Issue]
**File**: `path/to/file.kt:line`
**Impact**: Resource leak, crash on configuration change

**Current**:
```kotlin
// problematic code
```

**Fix**:
```kotlin
// corrected code
```

**Why**: [Explanation]

---

## 🟠 HIGH PRIORITY ISSUES

### 🟠 Naming Convention - [Specific Issue]
**File**: `path/to/file.kt:line`
**Impact**: Code readability, team collaboration

**Violations**:
- Line X: `usr` should be `user`
- Line Y: `loading` should be `isLoading`
- Line Z: `pmtVM` should be `paymentViewModel`

**Why**: [Explanation]

---

### 🟠 UIState Pattern - [Specific Issue]
**File**: `path/to/file.kt:line`
**Impact**: State inconsistency, hard to debug

**Current**:
```kotlin
// scattered state
```

**Fix**:
```kotlin
// sealed class UIState
```

**Why**: [Explanation]

---

### 🟠 Business Logic Misplacement - [Specific Issue]
**File**: `path/to/file.kt:line`
**Impact**: Not testable, hard to reuse, violates Clean Architecture

**Current**:
```kotlin
// business logic in ViewModel
```

**Fix**:
```kotlin
// business logic in UseCase
```

**Why**: [Explanation]

---

### 🟠 MVVM Pattern Violation - [Specific Issue]
**File**: `path/to/file.kt:line`
**Impact**: Architecture inconsistency, hard to maintain

**Current**:
```kotlin
// ViewModel calling Repository directly
```

**Fix**:
```kotlin
// ViewModel calling UseCase
```

**Why**: [Explanation]

---

## ⚠️ MUST FIX

**Before Release**:
1. All 🔴 Critical issues (X total)

**Before Merge**:
1. All 🟠 High Priority issues (X total)

## ✅ Well Done
[If applicable, acknowledge good patterns observed]
```

## Quick Reference

**Focus**: Only report CRITICAL and HIGH priority issues:
1. **Naming Conventions** - Abbreviations, wrong case, missing prefixes
2. **Memory Leaks** - Activity/Context/View references in ViewModel
3. **UIState Patterns** - Scattered state, exposed mutable state
4. **Business Logic Placement** - Logic in wrong layers
5. **Lifecycle Management** - GlobalScope, wrong lifecycle owner
6. **MVI/MVVM Violations** - Repository calls from ViewModel, business logic in View

**Skip**: Code style, documentation, performance (unless critical), security, tests, DI setup

## Tips

- **Focus on impact**: Only report issues that cause crashes, leaks, or violate core architecture
- **Be specific**: Reference exact line numbers and variable names
- **Show examples**: Always provide current vs. fixed code
- **Explain why**: Impact on stability, maintainability, testability
- **Be actionable**: Clear fix recommendations
- **No nitpicking**: Skip style issues handled by linter
