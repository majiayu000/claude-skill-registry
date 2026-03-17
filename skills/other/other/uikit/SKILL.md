---
name: uikit
description: UIKit imperative iOS UI framework. Use for iOS development.
---

# UIKit

UIKit is the traditional, imperative framework for building iOS user interfaces. While SwiftUI is the future, UIKit remains essential for maintaining existing apps and unrestricted access to the OS.

## When to Use

- Maintaining legacy iOS codebases (Objective-C or Swift).
- Fine-grained control over view hierarchy performance not yet possible in SwiftUI.
- Using third-party libraries that haven't migrated to SwiftUI ViewRepresentables.

## Quick Start

```swift
// Programmatic UIKit (No Storyboards) in SceneDelegate
func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options: UIScene.ConnectionOptions) {
    guard let windowScene = (scene as? UIWindowScene) else { return }
    window = UIWindow(windowScene: windowScene)
    window?.rootViewController = UINavigationController(rootViewController: HomeViewController())
    window?.makeKeyAndVisible()
}

class HomeViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .systemBackground
        title = "UIKit Home"

        let button = UIButton(type: .system)
        button.setTitle("Tap Me", for: .normal)
        button.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(button)

        NSLayoutConstraint.activate([
            button.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            button.centerYAnchor.constraint(equalTo: view.centerYAnchor)
        ])
    }
}
```

## Core Concepts

### View Controller Lifecycle

Understanding `viewDidLoad`, `viewWillAppear`, `viewDidLayoutSubviews` is critical for managing state and layout updates correctly in the imperative model.

### Auto Layout

The layout engine based on constraints. Use `NSLayoutConstraint` or library wrappers (SnapKit) to define rules (e.g., "A is 10px below B").

### Delegates & Data Sources

Common pattern for handling events (UITableViewDelegate) and providing data (UITableViewDataSource).

## Common Patterns

### Diffable Data Source

Modern replacement for `reloadData()`.

- Uses `NSDiffableDataSourceSnapshot` to animate changes automatically and safely.
- eliminates "Index out of range" crashes during updates.

### Compositional Layout

Modern API for building complex collection view layouts (grids, carousels) without subclassing `UICollectionViewLayout`.

### Coordinator Pattern

Moving navigation logic out of ViewControllers to improve reusability and testing.

## Best Practices

**Do**:

- Use **Diffable Data Sources** for Lists and Collections.
- Use **Compositional Layouts** instead of FlowLayouts.
- Use **View Binding** mechanisms (like Combine) to update UI, rather than manually setting properties everywhere.

**Don't**:

- Don't use massive Storyboards (merge conflicts hell).
- Don't force `layoutIfNeeded()` unless animating changes.
- Don't forget `[weak self]` in closures to avoid memory leaks (Retain Cycles).

## Troubleshooting

| Error                       | Cause                          | Solution                                                                   |
| :-------------------------- | :----------------------------- | :------------------------------------------------------------------------- |
| `Unsatisfiable Constraints` | Conflicting Auto Layout rules. | Check console log for breaking constraint IDs; simplify rules.             |
| `TableView Updates Crash`   | Inconsistent data vs rows.     | Use Diffable Data Source or ensure data model updates before `insertRows`. |
| `Retain Cycle`              | Strong reference loop.         | Use Memory Graph Debugger; verify `[weak self]`.                           |

## References

- [Apple UIKit Documentation](https://developer.apple.com/documentation/uikit)
- [Modern UIKit Patterns](https://developer.apple.com/videos/play/wwdc2020/10097/)
