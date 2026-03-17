---
name: ios-reactive-list-generator
description: Generate reactive iOS list screens with RxSwift MVVM Input/Output pattern. Creates complete list features with reactive bindings, pagination (date range/page number), ViewModel, ViewController, Navigator, and tests for iOS reactive projects. Use when "create reactive list", "generate reactive list", "new reactive list screen", "create rxswift list", or "generate list with rxswift".
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# iOS Reactive List Generator

Generates complete reactive iOS list screens using RxSwift MVVM Input/Output pattern with reactive pagination, pull-to-refresh, and infinite scroll for iOS reactive projects.

## When to Activate

- "create reactive list"
- "generate reactive list"
- "new reactive list screen"
- "create rxswift list"
- "generate list with rxswift"
- "new reactive table view"
- "create ios reactive list"
- "generate reactive list with pagination"
- "new list with reactive bindings"

## Generation Process

### Step 1: Collect Feature Requirements

Use `AskUserQuestion` to collect configuration (present all questions at once):

**Required Information:**
1. Feature name (CamelCase, e.g., "TransactionHistory")
2. Feature path (e.g., "PayooMerchant/Controllers/Transaction/History")
3. Feature display title (for navigation bar)
4. Pagination type: "date_range", "page_number", or "none"
5. Primary UseCase name (e.g., "TransactionHistoryUseCaseType")
6. Primary UseCase main method (e.g., "getTransactions(fromDate:toDate:)")
7. Domain model item type (e.g., "TransactionItem")
8. Main content cell class (e.g., "TransactionCell")

**Optional Information:**
- Additional UseCases (comma-separated)
- Custom Input triggers beyond standard (load, loadMore, refresh, selectItem)
- Custom Output drivers beyond standard (items, isLoading, shouldLoadMore, error)
- Header cells (comma-separated class names)
- Additional navigation destinations

### Step 2: Read Reference Implementations

Read these files to extract patterns:

```bash
# Core reference implementations
PayooMerchant/Controllers/Balance/Information/BalanceInformationViewModel.swift
PayooMerchant/Controllers/Balance/Information/BalanceInformationController.swift
PayooMerchant/Controllers/History/BaseListTransaction/BaseListPaginateDateRangeViewModel.swift

# Form template
/Users/homac34/payoo-ios-app-merchant/PRESENTATION_LAYER_FORM.md
```

### Step 3: Generate Files

Generate these files in the specified `feature_path`:

#### 1. ViewModel (`[Feature]ViewModel.swift`)

From `templates.md` → Template 1: ViewModel

**Key components:**
- Import Domain module
- Struct `[Feature]Filter: FilterPaginationDateRangeProvider`
- Class extending `BaseListPaginationDateRangeViewModel<DomainItem, Filter, Any>`
- Input struct with all triggers
- Output struct with all drivers
- `transform()` method
- Override `fetchItems(_ toDate: Date)` for pagination

**Critical patterns:**
- Use `[weak self]` in all closures
- All subscriptions use `.disposed(by: disposeBag)`
- API calls use `.catchSessionError(sessionUC)` (inherited from base)
- Use `Driver` for all outputs (UI-safe)
- Use `Observable` for all inputs

#### 2. ViewController (`[Feature]Controller.swift`)

From `templates.md` → Template 2: ViewController

**Key components:**
- Extend `BaseViewController`
- IBOutlet for tableView
- PublishSubject triggers matching Input
- `viewDidLoad()` setup
- `setupUI()` - register cells, configure table
- `bindViewModel()` - create Input, transform, bind Output

**Critical patterns:**
- Pull-to-refresh setup
- Infinite scroll detection (last 3 items)
- Cell registration with `registerCellByNib`
- Error handling with `showError()`
- Navigation via `navigator.navigate(to:)`

#### 3. Navigator Extension (`Navigator+[Feature].swift`)

From `templates.md` → Template 3: Navigator

**Key components:**
- Protocol `[Feature]NavigatorType`
- Enum `[Feature]Destination` with all navigation cases
- Extension `Navigator: [Feature]NavigatorType`
- Implementation using `viewControllerFactory`

#### 4. Unit Tests (`[Feature]ViewModelTests.swift`)

From `templates.md` → Template 4: Unit Tests

**Key components:**
- RxTest with TestScheduler
- Mock UseCases and Navigator
- Test cases for load, loadMore, refresh, selection
- Memory leak test (weak self verification)

### Step 4: Generate DI Registration Instructions

Create markdown instructions for manual updates:

**File: `DependencyContainer.swift`**
```swift
// Register ViewModel
container.register([Feature]ViewModel.self) { resolver in
    [Feature]ViewModel(
        [feature]UC: resolver.resolve([PrimaryUseCase].self)!,
        navigator: resolver.resolve([Feature]NavigatorType.self)!
    )
}
```

**File: `ViewControllerFactory` extension**
```swift
extension ViewControllerFactory {
    func make[Feature]Controller() -> [Feature]Controller {
        let controller = [Feature]Controller.instantiate()
        controller.viewModel = DependencyContainer.shared.provide([Feature]ViewModel.self)
        return controller
    }
}
```

### Step 5: Validation Checklist

Before presenting results, verify:

- ✓ All generated files use correct feature name
- ✓ Import statements include `Domain`, `RxSwift`, `RxCocoa`
- ✓ ViewModel extends correct base class for pagination type
- ✓ All closures use `[weak self]`
- ✓ All subscriptions disposed with `disposeBag`
- ✓ Cell classes match existing cells (verify with Glob)
- ✓ Navigator protocol and enum follow naming conventions
- ✓ File paths are absolute and correct

## Output Format

Present results as:

```markdown
✅ iOS Feature Generated: [FeatureName]

📁 Files Created:
  - [feature_path]/[Feature]ViewModel.swift
  - [feature_path]/[Feature]Controller.swift
  - [feature_path]/Navigator+[Feature].swift
  - PayooMerchantTests/ViewModel/[Feature]ViewModelTests.swift

📋 Manual Steps Required:

1. **Register in DependencyContainer.swift**
   [Show code snippet]

2. **Add factory method to ViewControllerFactory**
   [Show code snippet]

3. **Update parent Navigator** (if adding to existing flow)
   [Show navigation destination enum case]

4. **Create XIB file** (optional)
   - File → New → View
   - Name: [Feature]Controller.xib
   - Set File's Owner to [Feature]Controller
   - Connect tableView outlet

🧪 Test the Feature:

1. Build project:
   ```bash
   xcodebuild -workspace PayooMerchant.xcworkspace \
     -scheme "Payoo Merchant Sandbox" \
     -configuration "Debug Sandbox" \
     -sdk iphonesimulator \
     -destination 'platform=iOS Simulator,OS=17.5,name=iPhone 15,arch=x86_64' \
     clean build
   ```

2. Run tests:
   ```bash
   xcodebuild test \
     -workspace PayooMerchant.xcworkspace \
     -scheme "PayooMerchantTests" \
     -configuration "Debug Sandbox" \
     -destination 'platform=iOS Simulator,OS=17.5,name=iPhone 15,arch=x86_64' \
     -enableCodeCoverage YES
   ```

3. Navigate to feature: `navigator.navigate(to: .[featureName]())`

⏱️  Estimated completion time: 15-30 minutes (manual steps)
```

## Key Patterns Reference

### Date Range Pagination
- Filter conforms to `FilterPaginationDateRangeProvider`
- Domain item conforms to `PaginationDateRangeProvider`
- Uses item's `createdDate` as cursor for next page
- `toDate` becomes last item's date on load more

### RxSwift Memory Safety
- Always `[weak self]` in closures
- Always `.disposed(by: disposeBag)`
- Use `Driver` (never fails, main thread) for UI
- Use `Observable` for inputs

### Navigation Pattern
- Protocol defines interface
- Enum defines destinations with associated values
- Navigator extension implements using factory

---

See `templates.md` for complete code templates.
See `examples.md` for full generated feature example.
