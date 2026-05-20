---
name: flutter-state-management
description: Flutter state management patterns — decision tree for setState, Provider, Riverpod, and BLoC with concrete examples and testing strategies
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[state management question or file]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: flutter, state, patterns
---

# Flutter State Management

## Overview

Reference guide for choosing and implementing state management in Flutter. Apply the right pattern based on state scope, complexity, and testability requirements.

## Decision Tree: Choosing the Right Approach

```
What kind of state?
├── Ephemeral / UI-only (toggle, animation, form field)?
│   └── setState ✓
├── Shared between a few widgets in a subtree?
│   ├── Simple (1-2 values)? → InheritedWidget or ValueNotifier ✓
│   └── Moderate? → Provider / ChangeNotifier ✓
├── App-wide state (auth, theme, user preferences)?
│   ├── Small app? → Provider ✓
│   └── Medium/large app? → Riverpod ✓
├── Complex async flows (pagination, search, real-time)?
│   ├── Prefer declarative/reactive? → Riverpod ✓
│   └── Prefer event-driven with strict patterns? → BLoC ✓
└── Need offline-first or complex sync?
    └── BLoC or Riverpod + Repository pattern ✓
```

## setState — Ephemeral State

Use for state local to a single widget. No infrastructure needed.

```dart
class LikeButton extends StatefulWidget {
  const LikeButton({super.key, required this.initialCount});
  final int initialCount;

  @override
  State<LikeButton> createState() => _LikeButtonState();
}

class _LikeButtonState extends State<LikeButton> {
  late int _count;
  bool _isLiked = false;

  @override
  void initState() {
    super.initState();
    _count = widget.initialCount;
  }

  void _toggleLike() {
    setState(() {
      _isLiked = !_isLiked;
      _count += _isLiked ? 1 : -1;
    });
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: _toggleLike,
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            _isLiked ? Icons.favorite : Icons.favorite_border,
            color: _isLiked ? Colors.red : Colors.grey,
          ),
          const SizedBox(width: 4),
          Text('$_count'),
        ],
      ),
    );
  }
}
```

## Provider — App State (Small to Medium)

### ChangeNotifier Pattern

```dart
// models/cart_model.dart
class CartModel extends ChangeNotifier {
  final List<Product> _items = [];

  List<Product> get items => List.unmodifiable(_items);
  int get totalItems => _items.length;
  double get totalPrice => _items.fold(0, (sum, item) => sum + item.price);

  void add(Product product) {
    _items.add(product);
    notifyListeners();
  }

  void remove(Product product) {
    _items.remove(product);
    notifyListeners();
  }

  void clear() {
    _items.clear();
    notifyListeners();
  }
}
```

### Provider Setup

```dart
// main.dart
void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => CartModel()),
        ChangeNotifierProvider(create: (_) => AuthModel()),
        // ProxyProvider for dependent providers
        ProxyProvider<AuthModel, UserProfileModel>(
          update: (_, auth, previous) =>
              UserProfileModel(userId: auth.currentUser?.id),
        ),
      ],
      child: const MyApp(),
    ),
  );
}
```

### Consuming Providers

```dart
// Read once (does NOT rebuild on change)
final cart = context.read<CartModel>();
cart.add(product);

// Watch (rebuilds when model changes)
@override
Widget build(BuildContext context) {
  final totalItems = context.watch<CartModel>().totalItems;
  return Badge(count: totalItems, child: const Icon(Icons.shopping_cart));
}

// Select (rebuilds only when selected value changes)
@override
Widget build(BuildContext context) {
  final totalPrice = context.select<CartModel, double>((c) => c.totalPrice);
  return Text('\$${totalPrice.toStringAsFixed(2)}');
}

// Consumer widget (scoped rebuild)
Consumer<CartModel>(
  builder: (context, cart, child) {
    return Text('${cart.totalItems} items');
  },
)
```

## Riverpod — App State (Medium to Large)

### Provider Types

```dart
// Simple value provider
final appNameProvider = Provider<String>((ref) => 'My App');

// State provider (simple mutable state)
final counterProvider = StateProvider<int>((ref) => 0);

// FutureProvider (async data)
final userProvider = FutureProvider.family<User, String>((ref, userId) async {
  final api = ref.watch(apiClientProvider);
  return api.getUser(userId);
});

// StreamProvider (real-time data)
final messagesProvider = StreamProvider<List<Message>>((ref) {
  final repo = ref.watch(chatRepoProvider);
  return repo.watchMessages();
});

// NotifierProvider (complex state with methods)
final todosProvider = NotifierProvider<TodosNotifier, List<Todo>>(
  TodosNotifier.new,
);
```

### Notifier Pattern (Riverpod 2.0+)

```dart
// notifiers/todos_notifier.dart
class TodosNotifier extends Notifier<List<Todo>> {
  @override
  List<Todo> build() {
    // Initial state — can also be async with AsyncNotifier
    return [];
  }

  void add(String title) {
    state = [
      ...state,
      Todo(id: const Uuid().v4(), title: title),
    ];
  }

  void toggle(String id) {
    state = [
      for (final todo in state)
        if (todo.id == id)
          todo.copyWith(completed: !todo.completed)
        else
          todo,
    ];
  }

  void remove(String id) {
    state = state.where((t) => t.id != id).toList();
  }
}
```

### AsyncNotifier for Async State

```dart
class UsersNotifier extends AsyncNotifier<List<User>> {
  @override
  Future<List<User>> build() async {
    final api = ref.watch(apiClientProvider);
    return api.getUsers();
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() async {
      final api = ref.read(apiClientProvider);
      return api.getUsers();
    });
  }

  Future<void> addUser(CreateUserInput input) async {
    final api = ref.read(apiClientProvider);
    final newUser = await api.createUser(input);
    state = AsyncData([...state.requireValue, newUser]);
  }
}

final usersProvider = AsyncNotifierProvider<UsersNotifier, List<User>>(
  UsersNotifier.new,
);
```

### Consuming in Widgets

```dart
class UserListPage extends ConsumerWidget {
  const UserListPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final usersAsync = ref.watch(usersProvider);

    return usersAsync.when(
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (error, stack) => Center(child: Text('Error: $error')),
      data: (users) => ListView.builder(
        itemCount: users.length,
        itemBuilder: (context, index) => UserTile(user: users[index]),
      ),
    );
  }
}
```

### Provider Dependencies and Overrides

```dart
// Provider that depends on another
final filteredTodosProvider = Provider<List<Todo>>((ref) {
  final filter = ref.watch(filterProvider);
  final todos = ref.watch(todosProvider);

  switch (filter) {
    case TodoFilter.all:
      return todos;
    case TodoFilter.active:
      return todos.where((t) => !t.completed).toList();
    case TodoFilter.completed:
      return todos.where((t) => t.completed).toList();
  }
});

// Override for testing
void main() {
  runApp(
    ProviderScope(
      overrides: [
        apiClientProvider.overrideWithValue(MockApiClient()),
      ],
      child: const MyApp(),
    ),
  );
}
```

## BLoC — Complex Async / Event-Driven

### Events, States, BLoC

```dart
// bloc/auth/auth_event.dart
sealed class AuthEvent {}

class AuthLoginRequested extends AuthEvent {
  AuthLoginRequested({required this.email, required this.password});
  final String email;
  final String password;
}

class AuthLogoutRequested extends AuthEvent {}

class AuthStatusChecked extends AuthEvent {}

// bloc/auth/auth_state.dart
sealed class AuthState {}

class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class AuthAuthenticated extends AuthState {
  AuthAuthenticated({required this.user});
  final User user;
}
class AuthUnauthenticated extends AuthState {}
class AuthFailure extends AuthState {
  AuthFailure({required this.message});
  final String message;
}

// bloc/auth/auth_bloc.dart
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  AuthBloc({required AuthRepository authRepo})
      : _authRepo = authRepo,
        super(AuthInitial()) {
    on<AuthLoginRequested>(_onLoginRequested);
    on<AuthLogoutRequested>(_onLogoutRequested);
    on<AuthStatusChecked>(_onStatusChecked);
  }

  final AuthRepository _authRepo;

  Future<void> _onLoginRequested(
    AuthLoginRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());
    try {
      final user = await _authRepo.login(event.email, event.password);
      emit(AuthAuthenticated(user: user));
    } catch (e) {
      emit(AuthFailure(message: e.toString()));
    }
  }

  Future<void> _onLogoutRequested(
    AuthLogoutRequested event,
    Emitter<AuthState> emit,
  ) async {
    await _authRepo.logout();
    emit(AuthUnauthenticated());
  }

  Future<void> _onStatusChecked(
    AuthStatusChecked event,
    Emitter<AuthState> emit,
  ) async {
    final user = await _authRepo.getCurrentUser();
    if (user != null) {
      emit(AuthAuthenticated(user: user));
    } else {
      emit(AuthUnauthenticated());
    }
  }
}
```

### BLoC in Widgets

```dart
// Providing
BlocProvider(
  create: (context) => AuthBloc(authRepo: context.read<AuthRepository>())
    ..add(AuthStatusChecked()),
  child: const AuthGate(),
)

// Consuming
class AuthGate extends StatelessWidget {
  const AuthGate({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<AuthBloc, AuthState>(
      builder: (context, state) {
        return switch (state) {
          AuthInitial() || AuthLoading() => const LoadingScreen(),
          AuthAuthenticated(:final user) => HomePage(user: user),
          AuthUnauthenticated() => const LoginPage(),
          AuthFailure(:final message) => ErrorPage(message: message),
        };
      },
    );
  }
}

// Side effects with BlocListener
BlocListener<AuthBloc, AuthState>(
  listener: (context, state) {
    if (state is AuthFailure) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(state.message)),
      );
    }
  },
  child: const LoginForm(),
)
```

### Testing BLoC

Use `blocTest` from `bloc_test` package. Inject a mock repository, fire events, and assert state sequences.

```dart
blocTest<AuthBloc, AuthState>(
  'emits [AuthLoading, AuthAuthenticated] on successful login',
  build: () {
    when(() => mockRepo.login(any(), any()))
        .thenAnswer((_) async => testUser);
    return AuthBloc(authRepo: mockRepo);
  },
  act: (bloc) => bloc.add(
    AuthLoginRequested(email: 'test@test.com', password: 'pass'),
  ),
  expect: () => [
    isA<AuthLoading>(),
    isA<AuthAuthenticated>().having((s) => s.user, 'user', testUser),
  ],
);
```

## Anti-patterns

### BLoC for Simple State

Using BLoC for a boolean toggle or counter adds event classes, state classes, and a bloc class for what `setState` does in 3 lines. Match complexity to the tool.

### Global State for Local Concerns

A dialog's open/closed state, a text field's value, or an animation's progress should not be in Provider/Riverpod/BLoC. Keep ephemeral state local with `setState`.

### Mutable State Without Notifying Listeners

```dart
// BAD: Mutating list in place — listeners never fire
class CartModel extends ChangeNotifier {
  final List<Product> items = [];
  void add(Product p) {
    items.add(p); // Mutation — no notification
  }
}

// GOOD: New list triggers notification
void add(Product p) {
  _items = [..._items, p];
  notifyListeners();
}
```

### Not Testing State Changes

State management code is pure logic — it is the easiest code to test. Always write tests for notifiers, blocs, and reducers. If you skip testing state management, you skip testing your app's most critical behavior.
