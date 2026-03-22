---
name: "flutter-architecting-apps"
description: "Architects a Flutter application using the recommended layered approach (UI, Logic, Data). Use when structuring a new project or refactoring for scalability."
metadata:
  model: "models/gemini-3.1-pro-preview"
  last_modified: "Thu, 12 Mar 2026 22:13:42 GMT"

---
# Architecting Flutter Applications

## Contents
- [Core Architectural Principles](#core-architectural-principles)
- [Structuring the Layers](#structuring-the-layers)
- [Implementing the Data Layer](#implementing-the-data-layer)
- [Feature Implementation Workflow](#feature-implementation-workflow)
- [Examples](#examples)

## Core Architectural Principles

Design Flutter applications to scale by strictly adhering to the following principles:

*   **Enforce Separation of Concerns:** Decouple UI rendering from business logic and data fetching. Organize the codebase into distinct layers (UI, Logic, Data) and further separate by feature within those layers.
*   **Maintain a Single Source of Truth (SSOT):** Centralize application state and data in the Data layer. Ensure the SSOT is the only component authorized to mutate its respective data.
*   **Implement Unidirectional Data Flow (UDF):** Flow state downwards from the Data layer to the UI layer. Flow events upwards from the UI layer to the Data layer.
*   **Treat UI as a Function of State:** Drive the UI entirely via immutable state objects. Rebuild widgets reactively when the underlying state changes.

## Structuring the Layers

Separate the application into 2 to 3 distinct layers depending on complexity. Restrict communication so that a layer only interacts with the layer directly adjacent to it.

### 1. UI Layer (Presentation)
*   **Views (Widgets):** Build reusable, lean widgets. Strip all business and data-fetching logic from the widget tree. Restrict widget logic to UI-specific concerns (e.g., animations, routing, layout constraints).
*   **ViewModels:** Manage the UI state. Consume domain models from the Data/Logic layers and transform them into presentation-friendly formats. Expose state to the Views and handle user interaction events.

### 2. Logic Layer (Domain) - *Conditional*
*   **If the application requires complex client-side business logic:** Implement a Logic layer containing Use Cases or Interactors. Use this layer to orchestrate interactions between multiple repositories before passing data to the UI layer.
*   **If the application is a standard CRUD app:** Omit this layer. Allow ViewModels to interact directly with Repositories.

### 3. Data Layer (Model)
*   **Responsibilities:** Act as the SSOT for all application data. Handle business data, external API consumption, event processing, and data synchronization.
*   **Components:** Divide the Data layer strictly into **Repositories** and **Services**.

## Implementing the Data Layer

### Services
*   **Role:** Wrap external APIs (HTTP servers, local databases, platform plugins).
*   **Implementation:** Write Services as stateless Dart classes. Do not store application state here.
*   **Mapping:** Create exactly one Service class per external data source.

### Repositories
*   **Role:** Act as the SSOT for domain data. 
*   **Implementation:** Consume raw data from Services. Handle caching, offline synchronization, and retry logic. 
*   **Transformation:** Transform raw API/Service data into clean Domain Models formatted for consumption by ViewModels.

## Feature Implementation Workflow

Follow this sequential workflow when adding a new feature to the application.

**Task Progress:**
- [ ] **Step 1: Define Domain Models.** Create immutable Dart classes representing the core data structures required by the feature.
- [ ] **Step 2: Implement Services.** Create stateless Service classes to handle raw data fetching (e.g., HTTP GET/POST).
- [ ] **Step 3: Implement Repositories.** Create Repository classes that consume the Services, handle caching, and return Domain Models.
- [ ] **Step 4: Implement ViewModels.** Create ViewModels that consume the Repositories. Expose immutable state and define methods (commands) for user actions.
- [ ] **Step 5: Implement Views.** Create Flutter Widgets that bind to the ViewModel state and trigger ViewModel methods on user interaction.
- [ ] **Step 6: Run Validator.** Execute unit tests for Services, Repositories, and ViewModels. Execute widget tests for Views.
    *   *Feedback Loop:* Review test failures -> Fix logic/mocking errors -> Re-run tests until passing.

## Examples

### Data Layer: Service and Repository

```dart
// 1. Service (Stateless API Wrapper)
class UserApiService {
  final HttpClient _client;
  
  UserApiService(this._client);

  Future<Map<String, dynamic>> fetchUserRaw(String userId) async {
    final response = await _client.get('/users/$userId');
    return response.data;
  }
}

// 2. Domain Model (Immutable)
class User {
  final String id;
  final String name;
  
  const User({required this.id, required this.name});
}

// 3. Repository (SSOT & Data Transformer)
class UserRepository {
  final UserApiService _apiService;
  User? _cachedUser;

  UserRepository(this._apiService);

  Future<User> getUser(String userId) async {
    if (_cachedUser != null && _cachedUser!.id == userId) {
      return _cachedUser!;
    }
    
    final rawData = await _apiService.fetchUserRaw(userId);
    final user = User(id: rawData['id'], name: rawData['name']);
    
    _cachedUser = user; // Cache data
    return user;
  }
}
```

### UI Layer: ViewModel and View

```dart
// 4. ViewModel (State Management)
class UserViewModel extends ChangeNotifier {
  final UserRepository _userRepository;
  
  User? user;
  bool isLoading = false;
  String? error;

  UserViewModel(this._userRepository);

  Future<void> loadUser(String userId) async {
    isLoading = true;
    error = null;
    notifyListeners();

    try {
      user = await _userRepository.getUser(userId);
    } catch (e) {
      error = e.toString();
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }
}

// 5. View (Lean UI)
class UserProfileView extends StatelessWidget {
  final UserViewModel viewModel;

  const UserProfileView({Key? key, required this.viewModel}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: viewModel,
      builder: (context, child) {
        if (viewModel.isLoading) return const CircularProgressIndicator();
        if (viewModel.error != null) return Text('Error: ${viewModel.error}');
        if (viewModel.user == null) return const Text('No user data.');
        
        return Text('Hello, ${viewModel.user!.name}');
      },
    );
  }
}
```
