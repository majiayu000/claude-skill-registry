---
name: uikit
description: |
  UIKit framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with UIKit projects, or when the user mentions UIKit.
  Provides view controller patterns, Auto Layout, table/collection views, and navigation guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: swift
  extensions: ".swift"
---

# UIKit Guide

> Applies to: UIKit (iOS 12+), Swift 5.0+, Imperative UI, iOS/tvOS/Mac Catalyst

## Core Principles

1. **MVVM + Coordinator**: Separate view logic (VC), presentation (ViewModel), and navigation (Coordinator)
2. **Programmatic UI**: Build views in code with Auto Layout; avoid storyboards for team projects
3. **Thin View Controllers**: View controllers configure views and bind to view models; no business logic
4. **Protocol-Oriented Delegation**: Use delegate protocols for callbacks; always declare delegates `weak`
5. **Memory Safety**: Use `[weak self]` in closures, cancel tasks in `deinit`, break retain cycles

## Guardrails

### View Controller Rules

- Keep view controllers under 200 lines (extract views, helpers, extensions)
- Override `viewDidLoad` once; call `setupUI()`, `setupConstraints()`, `setupBindings()`
- Never put networking or business logic in view controllers
- Always call `super` in lifecycle methods
- Use `final class` for all view controllers unless explicitly designed for subclassing
- Use `required init?(coder:)` with `fatalError` for programmatic-only controllers
- Mark `@objc` actions as `private`

### Auto Layout Rules

- Always set `translatesAutoresizingMaskIntoConstraints = false` for programmatic views
- Use `NSLayoutConstraint.activate([])` to batch-activate constraints
- Pin to `safeAreaLayoutGuide` for top/bottom content edges
- Use `>=` and `<=` constraints with priorities for flexible layouts
- Never set frames directly when using Auto Layout
- Use stack views (`UIStackView`) to reduce constraint count
- Set `compressionResistance` and `hugging` priorities explicitly when needed

### Memory Management

- Use `[weak self]` in all escaping closures and Combine sinks
- Declare all delegates as `weak var`
- Cancel network tasks and Combine subscriptions in `deinit`
- Use `[unowned self]` only when the closure cannot outlive `self` (rare)
- Override `prepareForReuse()` in cells to clear state and cancel image loads

### Naming Conventions

- View controllers: `{Feature}ViewController` (e.g., `UserListViewController`)
- View models: `{Feature}ViewModel` (e.g., `UserListViewModel`)
- Cells: `{Item}Cell` (e.g., `UserCell`)
- Coordinators: `{Feature}Coordinator` (e.g., `UserCoordinator`)
- Custom views: descriptive name (e.g., `PrimaryButton`, `EmptyStateView`)
- Protocols: `{Name}Protocol` or `{Name}Delegate` (e.g., `UserServiceProtocol`)

## Project Structure

```
MyApp/
├── MyApp.xcodeproj
├── MyApp/
│   ├── Application/
│   │   ├── AppDelegate.swift
│   │   ├── SceneDelegate.swift
│   │   └── AppCoordinator.swift
│   ├── Features/
│   │   ├── Authentication/
│   │   │   ├── Controllers/
│   │   │   ├── ViewModels/
│   │   │   ├── Views/
│   │   │   └── Coordinator/
│   │   ├── Home/
│   │   │   ├── Controllers/
│   │   │   ├── ViewModels/
│   │   │   ├── Views/
│   │   │   └── Cells/
│   │   └── Profile/
│   ├── Core/
│   │   ├── Network/
│   │   ├── Storage/
│   │   ├── Extensions/
│   │   └── Utilities/
│   ├── Shared/
│   │   ├── Views/           # Reusable UI components
│   │   ├── Cells/           # Reusable cells
│   │   └── Protocols/       # Shared protocols
│   └── Resources/
│       ├── Assets.xcassets
│       └── Localizable.strings
├── MyAppTests/
└── MyAppUITests/
```

- Group by feature, not by type (Controllers/, ViewModels/ live inside each feature)
- `Core/` for infrastructure (networking, storage, utilities)
- `Shared/` for reusable UI components used across features
- One primary type per file, file named after the type

## View Controller Lifecycle

### Base View Controller Pattern

```swift
class BaseViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        setupConstraints()
        setupBindings()
    }

    func setupUI() { view.backgroundColor = .systemBackground }
    func setupConstraints() { /* Override in subclasses */ }
    func setupBindings() { /* Override in subclasses */ }

    func showError(_ error: Error) {
        let alert = UIAlertController(
            title: "Error", message: error.localizedDescription, preferredStyle: .alert
        )
        alert.addAction(UIAlertAction(title: "OK", style: .default))
        present(alert, animated: true)
    }
}
```

### Feature View Controller

```swift
import Combine

final class UserListViewController: BaseViewController {
    private let viewModel: UserListViewModel
    private var cancellables = Set<AnyCancellable>()
    weak var coordinator: UserCoordinator?

    private lazy var tableView: UITableView = {
        let table = UITableView(frame: .zero, style: .plain)
        table.translatesAutoresizingMaskIntoConstraints = false
        table.register(UserCell.self, forCellReuseIdentifier: UserCell.identifier)
        table.delegate = self
        table.dataSource = self
        table.rowHeight = UITableView.automaticDimension
        table.estimatedRowHeight = 80
        return table
    }()

    init(viewModel: UserListViewModel = UserListViewModel()) {
        self.viewModel = viewModel
        super.init(nibName: nil, bundle: nil)
    }

    required init?(coder: NSCoder) { fatalError("init(coder:) has not been implemented") }

    override func setupUI() {
        super.setupUI()
        title = "Users"
        view.addSubview(tableView)
    }

    override func setupConstraints() {
        NSLayoutConstraint.activate([
            tableView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
            tableView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            tableView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            tableView.bottomAnchor.constraint(equalTo: view.bottomAnchor)
        ])
    }

    override func setupBindings() {
        viewModel.$users
            .receive(on: DispatchQueue.main)
            .sink { [weak self] _ in self?.tableView.reloadData() }
            .store(in: &cancellables)

        viewModel.$error
            .compactMap { $0 }
            .receive(on: DispatchQueue.main)
            .sink { [weak self] error in self?.showError(error) }
            .store(in: &cancellables)
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        viewModel.loadUsers()
    }
}
```

## MVVM View Model

```swift
import Foundation
import Combine

final class UserListViewModel {
    @Published private(set) var users: [User] = []
    @Published private(set) var isLoading = false
    @Published private(set) var error: Error?

    private let userService: UserServiceProtocol

    init(userService: UserServiceProtocol = UserService()) {
        self.userService = userService
    }

    func loadUsers() {
        isLoading = true
        error = nil
        Task { @MainActor in
            do { users = try await userService.fetchUsers() }
            catch { self.error = error }
            isLoading = false
        }
    }

    func deleteUser(at index: Int) {
        let user = users[index]
        users.remove(at: index)
        Task {
            do { try await userService.deleteUser(id: user.id) }
            catch { await MainActor.run { users.insert(user, at: index); self.error = error } }
        }
    }
}
```

## Table Views and Collection Views

### UITableView with DataSource/Delegate

```swift
extension UserListViewController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        viewModel.users.count
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        guard let cell = tableView.dequeueReusableCell(
            withIdentifier: UserCell.identifier, for: indexPath
        ) as? UserCell else { return UITableViewCell() }
        cell.configure(with: viewModel.users[indexPath.row])
        return cell
    }
}

extension UserListViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        coordinator?.showUserDetail(viewModel.users[indexPath.row])
    }
}
```

### Diffable Data Source (iOS 13+)

```swift
enum Section { case main }
typealias DataSource = UICollectionViewDiffableDataSource<Section, Photo>
typealias Snapshot = NSDiffableDataSourceSnapshot<Section, Photo>

private func setupDataSource() {
    let registration = UICollectionView.CellRegistration<PhotoCell, Photo> { cell, _, photo in
        cell.configure(with: photo)
    }
    dataSource = DataSource(collectionView: collectionView) { cv, indexPath, photo in
        cv.dequeueConfiguredReusableCell(using: registration, for: indexPath, item: photo)
    }
}

private func applySnapshot(photos: [Photo], animating: Bool = true) {
    var snapshot = Snapshot()
    snapshot.appendSections([.main])
    snapshot.appendItems(photos)
    dataSource.apply(snapshot, animatingDifferences: animating)
}
```

### Compositional Layout (iOS 13+)

```swift
private func createGridLayout() -> UICollectionViewLayout {
    let itemSize = NSCollectionLayoutSize(
        widthDimension: .fractionalWidth(1/3),
        heightDimension: .fractionalWidth(1/3)
    )
    let item = NSCollectionLayoutItem(layoutSize: itemSize)
    item.contentInsets = NSDirectionalEdgeInsets(top: 2, leading: 2, bottom: 2, trailing: 2)

    let groupSize = NSCollectionLayoutSize(
        widthDimension: .fractionalWidth(1.0),
        heightDimension: .fractionalWidth(1/3)
    )
    let group = NSCollectionLayoutGroup.horizontal(layoutSize: groupSize, subitems: [item])
    return UICollectionViewCompositionalLayout(section: NSCollectionLayoutSection(group: group))
}
```

## Navigation Patterns

### Coordinator Protocol

```swift
protocol Coordinator: AnyObject {
    var childCoordinators: [Coordinator] { get set }
    var navigationController: UINavigationController { get set }
    func start()
}

extension Coordinator {
    func addChild(_ coordinator: Coordinator) {
        childCoordinators.append(coordinator)
    }

    func removeChild(_ coordinator: Coordinator) {
        childCoordinators.removeAll { $0 === coordinator }
    }
}
```

### App Coordinator

```swift
final class AppCoordinator: Coordinator {
    var childCoordinators: [Coordinator] = []
    var navigationController: UINavigationController
    private let authManager: AuthManager

    init(navigationController: UINavigationController, authManager: AuthManager = .shared) {
        self.navigationController = navigationController
        self.authManager = authManager
    }

    func start() {
        authManager.isAuthenticated ? showMainFlow() : showAuthFlow()
    }

    private func showAuthFlow() {
        let coordinator = AuthCoordinator(navigationController: navigationController)
        coordinator.delegate = self
        addChild(coordinator)
        coordinator.start()
    }

    private func showMainFlow() {
        let coordinator = MainTabCoordinator(navigationController: navigationController)
        addChild(coordinator)
        coordinator.start()
    }
}
```

## Delegation Pattern

### Delegate Protocol

```swift
protocol AddUserViewControllerDelegate: AnyObject {
    func addUserDidSave(_ controller: AddUserViewController, user: User)
    func addUserDidCancel(_ controller: AddUserViewController)
}

final class AddUserViewController: BaseViewController {
    weak var delegate: AddUserViewControllerDelegate?

    @objc private func saveTapped() {
        guard let user = buildUser() else { return }
        delegate?.addUserDidSave(self, user: user)
    }

    @objc private func cancelTapped() {
        delegate?.addUserDidCancel(self)
    }
}
```

## Custom Cell Pattern

```swift
final class UserCell: UITableViewCell {
    static let identifier = "UserCell"

    private let nameLabel: UILabel = {
        let label = UILabel()
        label.translatesAutoresizingMaskIntoConstraints = false
        label.font = .preferredFont(forTextStyle: .headline)
        return label
    }()

    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        setupUI()
    }

    required init?(coder: NSCoder) { fatalError("init(coder:) has not been implemented") }

    private func setupUI() {
        contentView.addSubview(nameLabel)
        NSLayoutConstraint.activate([
            nameLabel.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: 16),
            nameLabel.trailingAnchor.constraint(equalTo: contentView.trailingAnchor, constant: -16),
            nameLabel.centerYAnchor.constraint(equalTo: contentView.centerYAnchor)
        ])
    }

    func configure(with user: User) { nameLabel.text = user.name }

    override func prepareForReuse() {
        super.prepareForReuse()
        nameLabel.text = nil
    }
}
```

## Testing

### View Controller Tests

```swift
import XCTest
@testable import MyApp

final class UserListViewControllerTests: XCTestCase {
    var sut: UserListViewController!
    var mockViewModel: MockUserListViewModel!

    override func setUp() {
        super.setUp()
        mockViewModel = MockUserListViewModel()
        sut = UserListViewController(viewModel: mockViewModel)
        sut.loadViewIfNeeded()
    }

    override func tearDown() {
        sut = nil; mockViewModel = nil
        super.tearDown()
    }

    func test_viewDidLoad_loadsUsers() {
        XCTAssertTrue(mockViewModel.loadUsersCalled)
    }

    func test_tableView_rowCount_matchesUsers() {
        mockViewModel.users = [User.stub(), User.stub()]
        let count = sut.tableView(sut.tableView, numberOfRowsInSection: 0)
        XCTAssertEqual(count, 2)
    }
}
```

### Testing Standards

- Use protocol-based mocks injected via initializer
- Call `loadViewIfNeeded()` to trigger `viewDidLoad` without displaying
- Test data source methods directly on the view controller
- Test navigation by verifying coordinator method calls
- Test view model state changes with Combine expectations
- Coverage target: >80% for view models, >60% for view controllers

## Commands

```bash
xcodebuild -scheme MyApp -sdk iphonesimulator build   # Build
xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15'
swift format .                                          # Format
swiftlint                                               # Lint
```

## Best Practices

- **Architecture**: MVVM + Coordinator; thin view controllers; dependency injection via protocols
- **Performance**: Reuse cells with `prepareForReuse()`; async image loading; diffable data sources; profile with Instruments
- **Accessibility**: Dynamic Type (`preferredFont`); VoiceOver labels; semantic colors (`.label`, `.systemBackground`)
- **Appearance**: Configure `UINavigationBarAppearance` and `UITabBarAppearance` in `AppDelegate`

## References

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Coordinator, custom views, animations, Core Data, networking, testing

## External References

- [UIKit Documentation](https://developer.apple.com/documentation/uikit)
- [Modern Collection Views (WWDC 2020)](https://developer.apple.com/videos/play/wwdc2020/10026/)
- [Diffable Data Sources (WWDC 2019)](https://developer.apple.com/videos/play/wwdc2019/220/)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
