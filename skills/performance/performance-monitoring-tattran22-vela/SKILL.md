---
name: performance-monitoring
description: Performance targets and optimization patterns for FinanceApp. Use when optimizing SwiftUI views, CoreData queries, app launch time, or memory usage.
---

# Performance Monitoring & Optimization

## Performance Targets
| Metric | Target | Critical |
|--------|--------|----------|
| App launch (cold) | < 1.5s | < 3s |
| App launch (warm) | < 0.5s | < 1s |
| Screen transition | < 0.3s | < 0.5s |
| Transaction list scroll | 60 fps | > 30 fps |
| Data sync (100 items) | < 5s | < 10s |
| Memory usage (idle) | < 50MB | < 100MB |
| Memory usage (active) | < 150MB | < 300MB |

## SwiftUI Optimization

### Avoid Unnecessary View Updates
```swift
// Use @Observable with computed properties carefully
@Observable
final class TransactionListViewModel {
    // Only published properties trigger view updates
    var transactions: [Transaction] = []
    var isLoading = false

    // Derived state — does NOT trigger extra updates
    var totalAmount: Decimal {
        transactions.reduce(0) { $0 + $1.amount }
    }
}
```

### Lazy Loading for Lists
```swift
// ALWAYS use LazyVStack for long lists
ScrollView {
    LazyVStack(spacing: FinanceSpacing.sm) {
        ForEach(viewModel.transactions) { transaction in
            TransactionRow(transaction: transaction)
                .id(transaction.id) // Stable identity
        }
    }
}
```

### Reduce View Body Complexity
```swift
// Break complex views into smaller components
// BAD: One massive body
// GOOD: Composed from focused subviews
struct TransactionDetailView: View {
    var body: some View {
        ScrollView {
            headerSection
            amountSection
            categorySection
            notesSection
        }
    }

    private var headerSection: some View { /* ... */ }
    private var amountSection: some View { /* ... */ }
}
```

## CoreData / SwiftData Query Optimization

### Fetch with Limits and Predicates
```swift
// ALWAYS use predicates and limits — never fetch all then filter
let descriptor = FetchDescriptor<TransactionEntity>(
    predicate: #Predicate { $0.date >= startDate && $0.date <= endDate },
    sortBy: [SortDescriptor(\.date, order: .reverse)]
)
descriptor.fetchLimit = 50
descriptor.fetchOffset = page * 50
```

### Background Fetching
```swift
// Heavy queries on ModelActor, not main thread
@ModelActor
actor BackgroundDataHandler {
    func fetchMonthlyReport(month: Date) throws -> MonthlyReport {
        let transactions = try modelContext.fetch(descriptor)
        return MonthlyReport(from: transactions)
    }
}
```

## Instruments Profiling Checklist
1. **Time Profiler**: Identify slow functions, especially in `body` computations
2. **SwiftUI Instruments**: Check for excessive view updates
3. **Allocations**: Monitor memory growth, look for leaks
4. **Core Data**: Check fetch count, batch sizes, faulting behavior
5. **Network**: Monitor CloudKit sync payload sizes and frequency

## OSLog for Performance Tracking
```swift
import OSLog

extension Logger {
    static let performance = Logger(subsystem: "com.app.finance", category: "Performance")
}

// Usage
func loadTransactions() async {
    let signpost = OSSignposter(logger: .performance)
    let state = signpost.beginInterval("LoadTransactions")
    defer { signpost.endInterval("LoadTransactions", state) }

    // ... load data
}
```

## Memory Management
- Use `weak` references in closures capturing `self`
- Prefer value types (struct) to avoid retain cycles
- Use `@Environment(\.dismiss)` instead of storing navigation state
- Release image caches when receiving memory warnings
- Use `prefetchItemsAt` for collection view data prefetching
