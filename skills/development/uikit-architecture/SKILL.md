---
name: ios-uikit-architecture
description: Use when building iOS apps with UIKit, implementing MVVM/MVC/Coordinator patterns, or integrating UIKit with SwiftUI.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# iOS - UIKit Architecture

Architectural patterns and best practices for UIKit-based iOS applications.

## Key Concepts

### MVVM Architecture

The Model-View-ViewModel pattern separates concerns:

- **Model**: Data and business logic
- **View**: UIViewController and UIView subclasses
- **ViewModel**: Presentation logic, transforms model data for display

```swift
// Model
struct User {
    let id: String
    let firstName: String
    let lastName: String
    let email: String
}

// ViewModel
class UserProfileViewModel {
    private let user: User

    var displayName: String {
        "\(user.firstName) \(user.lastName)"
    }

    var emailDisplay: String {
        user.email.lowercased()
    }

    init(user: User) {
        self.user = user
    }
}

// View
class UserProfileViewController: UIViewController {
    private let viewModel: UserProfileViewModel

    init(viewModel: UserProfileViewModel) {
        self.viewModel = viewModel
        super.init(nibName: nil, bundle: nil)
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        nameLabel.text = viewModel.displayName
        emailLabel.text = viewModel.emailDisplay
    }
}
```

### Coordinator Pattern

Coordinators handle navigation flow, removing navigation logic from view controllers:

```swift
protocol Coordinator: AnyObject {
    var childCoordinators: [Coordinator] { get set }
    var navigationController: UINavigationController { get }
    func start()
}

class AppCoordinator: Coordinator {
    var childCoordinators: [Coordinator] = []
    var navigationController: UINavigationController

    init(navigationController: UINavigationController) {
        self.navigationController = navigationController
    }

    func start() {
        let vc = HomeViewController()
        vc.coordinator = self
        navigationController.pushViewController(vc, animated: false)
    }

    func showDetail(for item: Item) {
        let detailCoordinator = DetailCoordinator(
            navigationController: navigationController,
            item: item
        )
        childCoordinators.append(detailCoordinator)
        detailCoordinator.start()
    }
}
```

### Dependency Injection

Inject dependencies through initializers for testability:

```swift
protocol UserServiceProtocol {
    func fetchUser(id: String) async throws -> User
}

class UserViewController: UIViewController {
    private let userService: UserServiceProtocol
    private let userId: String

    init(userService: UserServiceProtocol, userId: String) {
        self.userService = userService
        self.userId = userId
        super.init(nibName: nil, bundle: nil)
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) not supported")
    }
}
```

## Best Practices

### Programmatic UI with Auto Layout

```swift
class ProfileView: UIView {
    private let avatarImageView: UIImageView = {
        let imageView = UIImageView()
        imageView.contentMode = .scaleAspectFill
        imageView.clipsToBounds = true
        imageView.translatesAutoresizingMaskIntoConstraints = false
        return imageView
    }()

    private let nameLabel: UILabel = {
        let label = UILabel()
        label.font = .preferredFont(forTextStyle: .headline)
        label.translatesAutoresizingMaskIntoConstraints = false
        return label
    }()

    override init(frame: CGRect) {
        super.init(frame: frame)
        setupViews()
        setupConstraints()
    }

    private func setupViews() {
        addSubview(avatarImageView)
        addSubview(nameLabel)
    }

    private func setupConstraints() {
        NSLayoutConstraint.activate([
            avatarImageView.topAnchor.constraint(equalTo: topAnchor, constant: 16),
            avatarImageView.centerXAnchor.constraint(equalTo: centerXAnchor),
            avatarImageView.widthAnchor.constraint(equalToConstant: 80),
            avatarImageView.heightAnchor.constraint(equalToConstant: 80),

            nameLabel.topAnchor.constraint(equalTo: avatarImageView.bottomAnchor, constant: 12),
            nameLabel.centerXAnchor.constraint(equalTo: centerXAnchor),
        ])
    }
}
```

### Modern Collection Views with Diffable Data Source

```swift
class ItemListViewController: UIViewController {
    enum Section { case main }

    private var dataSource: UICollectionViewDiffableDataSource<Section, Item>!
    private var collectionView: UICollectionView!

    override func viewDidLoad() {
        super.viewDidLoad()
        configureCollectionView()
        configureDataSource()
    }

    private func configureCollectionView() {
        let config = UICollectionLayoutListConfiguration(appearance: .insetGrouped)
        let layout = UICollectionViewCompositionalLayout.list(using: config)
        collectionView = UICollectionView(frame: view.bounds, collectionViewLayout: layout)
        collectionView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        view.addSubview(collectionView)
    }

    private func configureDataSource() {
        let cellRegistration = UICollectionView.CellRegistration<UICollectionViewListCell, Item> { cell, indexPath, item in
            var content = cell.defaultContentConfiguration()
            content.text = item.title
            content.secondaryText = item.subtitle
            cell.contentConfiguration = content
        }

        dataSource = UICollectionViewDiffableDataSource<Section, Item>(collectionView: collectionView) {
            collectionView, indexPath, item in
            collectionView.dequeueConfiguredReusableCell(using: cellRegistration, for: indexPath, item: item)
        }
    }

    func updateItems(_ items: [Item]) {
        var snapshot = NSDiffableDataSourceSnapshot<Section, Item>()
        snapshot.appendSections([.main])
        snapshot.appendItems(items)
        dataSource.apply(snapshot, animatingDifferences: true)
    }
}
```

### UIKit and SwiftUI Integration

Hosting SwiftUI in UIKit:

```swift
class SettingsViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()

        let swiftUIView = SettingsView()
        let hostingController = UIHostingController(rootView: swiftUIView)

        addChild(hostingController)
        view.addSubview(hostingController.view)
        hostingController.view.frame = view.bounds
        hostingController.view.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        hostingController.didMove(toParent: self)
    }
}
```

Wrapping UIKit in SwiftUI:

```swift
struct MapViewRepresentable: UIViewRepresentable {
    @Binding var region: MKCoordinateRegion

    func makeUIView(context: Context) -> MKMapView {
        let mapView = MKMapView()
        mapView.delegate = context.coordinator
        return mapView
    }

    func updateUIView(_ mapView: MKMapView, context: Context) {
        mapView.setRegion(region, animated: true)
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, MKMapViewDelegate {
        var parent: MapViewRepresentable

        init(_ parent: MapViewRepresentable) {
            self.parent = parent
        }
    }
}
```

## Common Patterns

### View Controller Lifecycle Management

```swift
class DataViewController: UIViewController {
    private var loadTask: Task<Void, Never>?

    override func viewDidLoad() {
        super.viewDidLoad()
        setupViews()
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        loadData()
    }

    override func viewDidDisappear(_ animated: Bool) {
        super.viewDidDisappear(animated)
        loadTask?.cancel()
    }

    private func loadData() {
        loadTask = Task {
            do {
                let data = try await fetchData()
                guard !Task.isCancelled else { return }
                updateUI(with: data)
            } catch {
                showError(error)
            }
        }
    }
}
```

### Memory Management with Closures

```swift
class NetworkViewController: UIViewController {
    private let networkService: NetworkService

    func fetchData() {
        // Use [weak self] to prevent retain cycles
        networkService.fetch { [weak self] result in
            guard let self else { return }

            switch result {
            case .success(let data):
                self.handleData(data)
            case .failure(let error):
                self.showError(error)
            }
        }
    }
}
```

## Anti-Patterns

### Massive View Controllers

Bad: Putting everything in one view controller.

Good: Extract into separate types:

- ViewModels for presentation logic
- Coordinators for navigation
- Custom views for UI components
- Services for network/data operations

### Storyboard Segue Spaghetti

Bad: Complex storyboard with many segues.

Good: Use coordinators with programmatic navigation.

### Force Casting Cells

Bad:

```swift
let cell = tableView.dequeueReusableCell(withIdentifier: "Cell") as! CustomCell
```

Good:

```swift
guard let cell = tableView.dequeueReusableCell(withIdentifier: "Cell") as? CustomCell else {
    fatalError("Unable to dequeue CustomCell")
}
```

## Related Skills

- **ios-swiftui-patterns**: Modern declarative UI
- **ios-swift-concurrency**: Async data loading
