---
name: error-handling
description: Error handling patterns for FinanceApp. Use when implementing error types, handling errors in ViewModels, or presenting errors in Views.
---

# Error Handling Patterns

## Domain Error Enums

### AppError — Top-level error type
```swift
/// Top-level error type for the application.
enum AppError: Error, Sendable, Equatable {
    case validation(ValidationError)
    case network(NetworkError)
    case data(DataError)
    case unknown(String)

    var userMessage: String {
        switch self {
        case .validation(let error): error.userMessage
        case .network(let error): error.userMessage
        case .data(let error): error.userMessage
        case .unknown(let message): message
        }
    }

    /// Convert any error to AppError
    init(from error: Error) {
        if let appError = error as? AppError {
            self = appError
        } else if let validationError = error as? ValidationError {
            self = .validation(validationError)
        } else if let networkError = error as? NetworkError {
            self = .network(networkError)
        } else if let dataError = error as? DataError {
            self = .data(dataError)
        } else {
            self = .unknown(error.localizedDescription)
        }
    }
}
```

### ValidationError — Input validation
```swift
enum ValidationError: Error, Sendable, Equatable {
    case invalidAmount(reason: String)
    case invalidDate(reason: String)
    case missingRequiredField(field: String)
    case duplicateEntry(type: String, name: String)
    case budgetExceeded(budget: Decimal, attempted: Decimal)

    var userMessage: String {
        switch self {
        case .invalidAmount(let reason): "Invalid amount: \(reason)"
        case .invalidDate(let reason): "Invalid date: \(reason)"
        case .missingRequiredField(let field): "\(field) is required"
        case .duplicateEntry(let type, let name): "\(type) '\(name)' already exists"
        case .budgetExceeded(let budget, let attempted):
            "Budget limit \(budget) exceeded. Attempted: \(attempted)"
        }
    }
}
```

### NetworkError — API and sync errors
```swift
enum NetworkError: Error, Sendable, Equatable {
    case noConnection
    case timeout
    case serverError(statusCode: Int)
    case syncConflict(localVersion: Int, remoteVersion: Int)
    case unauthorized

    var userMessage: String {
        switch self {
        case .noConnection: "No internet connection. Changes will sync when online."
        case .timeout: "Request timed out. Please try again."
        case .serverError: "Server error. Please try again later."
        case .syncConflict: "Sync conflict detected. Please review changes."
        case .unauthorized: "Session expired. Please sign in again."
        }
    }
}
```

### DataError — Persistence errors
```swift
enum DataError: Error, Sendable, Equatable {
    case notFound(type: String, id: String)
    case saveFailed(reason: String)
    case migrationFailed(from: Int, to: Int)
    case corruptedData(details: String)

    var userMessage: String {
        switch self {
        case .notFound(let type, _): "\(type) not found"
        case .saveFailed: "Failed to save. Please try again."
        case .migrationFailed: "Data upgrade failed. Please contact support."
        case .corruptedData: "Data error detected. Please contact support."
        }
    }
}
```

## ViewModel Error Handling
```swift
@Observable
final class TransactionFormViewModel {
    var error: AppError?
    var showError = false

    func save() async {
        do {
            try validate()
            try await repository.save(transaction)
        } catch {
            self.error = AppError(from: error)
            self.showError = true
        }
    }

    private func validate() throws {
        guard amount > 0 else {
            throw ValidationError.invalidAmount(reason: "Amount must be positive")
        }
        guard !note.isEmpty else {
            throw ValidationError.missingRequiredField(field: "Note")
        }
    }
}
```

## View Error Presentation
```swift
struct TransactionFormView: View {
    @State private var viewModel: TransactionFormViewModel

    var body: some View {
        Form { /* ... */ }
            .alert(
                "Error",
                isPresented: $viewModel.showError,
                presenting: viewModel.error
            ) { _ in
                Button("OK") { }
            } message: { error in
                Text(error.userMessage)
            }
    }
}
```

## Result Type Usage
```swift
// Use Result when you need to pass success/failure without throwing
func validateTransaction(_ transaction: Transaction) -> Result<Transaction, ValidationError> {
    guard transaction.amount > 0 else {
        return .failure(.invalidAmount(reason: "Must be positive"))
    }
    return .success(transaction)
}
```
