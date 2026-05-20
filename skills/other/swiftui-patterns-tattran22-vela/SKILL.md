---
name: swiftui-patterns
description: SwiftUI best practices and patterns for finance app. Use when building SwiftUI views, handling navigation, state management, or creating adaptive layouts for iOS and macOS.
---

# SwiftUI Patterns for FinanceApp

## Navigation

### iOS Navigation
```swift
NavigationStack(path: $router.path) {
    TransactionListView()
        .navigationDestination(for: Route.self) { route in
            switch route {
            case .transactionDetail(let id):
                TransactionDetailView(transactionId: id)
            case .addTransaction:
                AddTransactionView()
            case .accountDetail(let id):
                AccountDetailView(accountId: id)
            }
        }
}
```

### macOS Navigation
```swift
NavigationSplitView(columnVisibility: $visibility) {
    SidebarView()
} content: {
    ContentListView(selection: $selectedItem)
} detail: {
    DetailView(item: selectedItem)
}
.navigationSplitViewStyle(.balanced)
```

## State Management Pattern
```swift
@Observable
final class TransactionListViewModel {
    private let getTransactionsUseCase: GetTransactionsUseCaseProtocol
    
    var transactions: [Transaction] = []
    var isLoading = false
    var error: AppError?
    
    init(getTransactionsUseCase: GetTransactionsUseCaseProtocol) {
        self.getTransactionsUseCase = getTransactionsUseCase
    }
    
    func loadTransactions() async {
        isLoading = true
        defer { isLoading = false }
        
        do {
            transactions = try await getTransactionsUseCase.execute()
        } catch {
            self.error = AppError(from: error)
        }
    }
}
```

## Reusable Component Pattern
```swift
struct AmountText: View {
    let amount: Decimal
    let type: TransactionType
    let style: AmountStyle
    
    var body: some View {
        Text(amount, format: .currency(code: "VND"))
            .font(style.font)
            .foregroundStyle(type.color)
            .accessibilityLabel("\(type.accessibilityPrefix) \(amount)")
    }
}
```

## Cross-Platform Conditional
```swift
struct AdaptiveLayout: View {
    var body: some View {
        #if os(iOS)
        TabView { /* iOS tab layout */ }
        #elseif os(macOS)
        NavigationSplitView { /* macOS sidebar layout */ }
        #endif
    }
}
```
