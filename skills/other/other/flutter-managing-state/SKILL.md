---
name: "flutter-managing-state"
description: "Manages application and ephemeral state in a Flutter app. Use when sharing data between widgets or handling complex UI state transitions."
metadata:
  model: "models/gemini-3.1-pro-preview"
  last_modified: "Thu, 12 Mar 2026 22:18:06 GMT"

---
# Managing State in Flutter

## Contents
- [Core Concepts](#core-concepts)
- [Architecture and Data Flow](#architecture-and-data-flow)
- [Workflow: Selecting a State Management Approach](#workflow-selecting-a-state-management-approach)
- [Workflow: Implementing MVVM with Provider](#workflow-implementing-mvvm-with-provider)
- [Examples](#examples)

## Core Concepts

Flutter's UI is declarative; it is built to reflect the current state of the app (`UI = f(state)`). When state changes, trigger a rebuild of the UI that depends on that state. 

Distinguish between two primary types of state to determine your management strategy:
*   **Ephemeral State (Local State):** State contained neatly within a single widget (e.g., current page in a `PageView`, current selected tab, animation progress). Manage this using a `StatefulWidget` and `setState()`.
*   **App State (Shared State):** State shared across multiple parts of the app and maintained between user sessions (e.g., user preferences, login info, shopping cart contents). Manage this using advanced approaches like `InheritedWidget`, the `provider` package, and the MVVM architecture.

## Architecture and Data Flow

Implement the **Model-View-ViewModel (MVVM)** design pattern combined with **Unidirectional Data Flow (UDF)** for scalable app state management.

*   **Unidirectional Data Flow (UDF):** Enforce a strict flow where state flows *down* from the data layer, through the logic layer, to the UI layer. Events from user interactions flow *up* from the UI layer, to the logic layer, to the data layer.
*   **Single Source of Truth (SSOT):** Ensure data changes always happen in the data layer (Repositories). The SSOT class must be the only class capable of modifying its respective data.
*   **Model (Data Layer):** Handle low-level tasks like HTTP requests, data caching, and system resources using Repository classes.
*   **ViewModel (Logic Layer):** Manage the UI state. Convert app data from the Model into UI State. Extend `ChangeNotifier` and call `notifyListeners()` to trigger UI rebuilds when data changes.
*   **View (UI Layer):** Display the state provided by the ViewModel. Keep views lean; they should contain minimal logic (only routing, animations, or simple UI conditionals).

## Workflow: Selecting a State Management Approach

Evaluate the scope of the state to determine the correct implementation strategy.

*   **If managing Ephemeral State (single widget scope):**
    1. Subclass `StatefulWidget` and `State`.
    2. Store mutable state as private fields within the `State` class.
    3. Mutate state exclusively inside a `setState()` callback to mark the widget as dirty and schedule a rebuild.
*   **If managing App State (shared across widgets):**
    1. Implement the MVVM pattern.
    2. Use the `provider` package (a wrapper around `InheritedWidget`) to inject state into the widget tree.
    3. Use `ChangeNotifier` to emit state updates.

## Workflow: Implementing MVVM with Provider

Follow this sequential workflow to implement app-level state management using MVVM and `provider`.

**Task Progress:**
- [ ] 1. Define the Model (Repository).
- [ ] 2. Create the ViewModel (`ChangeNotifier`).
- [ ] 3. Inject the ViewModel into the Widget Tree.
- [ ] 4. Consume the State in the View.
- [ ] 5. Validate the implementation.

### 1. Define the Model (Repository)
Create a repository class to act as the Single Source of Truth (SSOT) for the specific data domain. Handle all external API calls or database queries here.

### 2. Create the ViewModel (`ChangeNotifier`)
Create a ViewModel class that extends `ChangeNotifier`.
*   Pass the Repository into the ViewModel via dependency injection.
*   Define properties for the UI state (e.g., `isLoading`, `data`, `errorMessage`).
*   Implement methods to handle UI events. Inside these methods, mutate the state and call `notifyListeners()` to trigger UI rebuilds.

### 3. Inject the ViewModel into the Widget Tree
Use `ChangeNotifierProvider` from the `provider` package to provide the ViewModel to the widget subtree that requires it. Place the provider as low in the widget tree as possible to avoid polluting the scope.

### 4. Consume the State in the View
Access the ViewModel in your `StatelessWidget` or `StatefulWidget`.
*   Use `Consumer<MyViewModel>` to rebuild specific parts of the UI when `notifyListeners()` is called.
*   Use `context.read<MyViewModel>()` (or `Provider.of<MyViewModel>(context, listen: false)`) inside event handlers (like `onPressed`) to call ViewModel methods without triggering a rebuild of the calling widget.

### 5. Validate the implementation
Run the following feedback loop to ensure data flows correctly:
1. Trigger a user action in the View.
2. Verify the ViewModel receives the event and calls the Repository.
3. Verify the Repository updates the SSOT and returns data.
4. Verify the ViewModel updates its state and calls `notifyListeners()`.
5. Verify the View rebuilds with the new state.
*Run validator -> review errors -> fix missing `notifyListeners()` calls or incorrect `Provider` scopes.*

## Examples

### Ephemeral State Implementation (`setState`)

Use this pattern strictly for local, UI-only state.

```dart
class EphemeralCounter extends StatefulWidget {
  const EphemeralCounter({super.key});

  @override
  State<EphemeralCounter> createState() => _EphemeralCounterState();
}

class _EphemeralCounterState extends State<EphemeralCounter> {
  int _counter = 0; // Local state

  void _increment() {
    setState(() {
      _counter++; // Mutate state and schedule rebuild
    });
  }

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: _increment,
      child: Text('Count: $_counter'),
    );
  }
}
```

### App State Implementation (MVVM + Provider)

Use this pattern for shared data and complex business logic.

```dart
// 1. Model (Repository)
class CartRepository {
  Future<void> saveItemToCart(String item) async {
    // Simulate network/database call
    await Future.delayed(const Duration(milliseconds: 500));
  }
}

// 2. ViewModel (ChangeNotifier)
class CartViewModel extends ChangeNotifier {
  final CartRepository repository;
  
  CartViewModel({required this.repository});

  final List<String> _items = [];
  bool isLoading = false;
  String? errorMessage;

  List<String> get items => List.unmodifiable(_items);

  Future<void> addItem(String item) async {
    isLoading = true;
    errorMessage = null;
    notifyListeners(); // Trigger loading UI

    try {
      await repository.saveItemToCart(item);
      _items.add(item);
    } catch (e) {
      errorMessage = 'Failed to add item';
    } finally {
      isLoading = false;
      notifyListeners(); // Trigger success/error UI
    }
  }
}

// 3. Injection & 4. View (UI)
class CartApp extends StatelessWidget {
  const CartApp({super.key});

  @override
  Widget build(BuildContext context) {
    // Inject ViewModel
    return ChangeNotifierProvider(
      create: (_) => CartViewModel(repository: CartRepository()),
      child: const CartScreen(),
    );
  }
}

class CartScreen extends StatelessWidget {
  const CartScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Consumer<CartViewModel>(
        builder: (context, viewModel, child) {
          if (viewModel.isLoading) {
            return const CircularProgressIndicator();
          }
          if (viewModel.errorMessage != null) {
            return Text(viewModel.errorMessage!);
          }
          return ListView.builder(
            itemCount: viewModel.items.length,
            itemBuilder: (_, index) => Text(viewModel.items[index]),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        // Use read() to access methods without listening for rebuilds
        onPressed: () => context.read<CartViewModel>().addItem('New Item'),
        child: const Icon(Icons.add),
      ),
    );
  }
}
```
