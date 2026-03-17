---
name: mobile-guide
description: Comprehensive mobile development guide for iOS, Android, React Native, and Flutter. Includes Swift, Kotlin, and cross-platform frameworks. Use when building mobile applications, iOS, Android, or cross-platform apps.
sasmp_version: "1.3.0"
bonded_agent: 05-mobile-specialist
bond_type: PRIMARY_BOND
eqhm_enabled: true
---

# Mobile Development Guide

Master native and cross-platform mobile development for iOS and Android platforms.

## Quick Start

### iOS with Swift
```swift
import SwiftUI

struct ContentView: View {
    @State private var todos: [String] = []
    @State private var newTodo = ""

    var body: some View {
        VStack {
            TextField("Add todo", text: $newTodo)
            Button("Add") {
                todos.append(newTodo)
                newTodo = ""
            }

            List {
                ForEach(todos, id: \.self) { todo in
                    Text(todo)
                }
            }
        }
    }
}
```

### Android with Kotlin
```kotlin
import androidx.compose.material3.Button
import androidx.compose.material3.TextField
import androidx.compose.runtime.mutableStateOf

@Composable
fun TodoApp() {
    var todos by remember { mutableStateOf(listOf<String>()) }
    var newTodo by remember { mutableStateOf("") }

    Column {
        TextField(
            value = newTodo,
            onValueChange = { newTodo = it },
            label = { Text("Add todo") }
        )
        Button(onClick = {
            todos = todos + newTodo
            newTodo = ""
        }) {
            Text("Add")
        }

        LazyColumn {
            items(todos) { todo ->
                Text(todo)
            }
        }
    }
}
```

### React Native
```javascript
import React, { useState } from 'react';
import { View, TextInput, TouchableOpacity, FlatList, Text } from 'react-native';

export default function TodoApp() {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');

  const addTodo = () => {
    setTodos([...todos, input]);
    setInput('');
  };

  return (
    <View>
      <TextInput
        placeholder="Add todo"
        value={input}
        onChangeText={setInput}
      />
      <TouchableOpacity onPress={addTodo}>
        <Text>Add</Text>
      </TouchableOpacity>

      <FlatList
        data={todos}
        renderItem={({ item }) => <Text>{item}</Text>}
      />
    </View>
  );
}
```

### Flutter
```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class TodoApp extends StatefulWidget {
  const TodoApp({Key? key}) : super(key: key);

  @override
  State<TodoApp> createState() => _TodoAppState();
}

class _TodoAppState extends State<TodoApp> {
  List<String> todos = [];
  TextEditingController controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          TextField(controller: controller),
          ElevatedButton(
            onPressed: () {
              setState(() => todos.add(controller.text));
              controller.clear();
            },
            child: const Text('Add'),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: todos.length,
              itemBuilder: (context, index) => Text(todos[index]),
            ),
          ),
        ],
      ),
    );
  }
}
```

## iOS Development Path

### Swift Basics
- **Variables & Types**: var, let, type safety
- **Functions**: Parameters, return types, closures
- **Structs & Classes**: Value vs reference types
- **Error Handling**: try/catch, Result type
- **Concurrency**: async/await, actors

### UI Frameworks
- **SwiftUI**: Modern declarative UI (recommended)
  - Views, state management, modifiers
  - Navigation, animation, gestures
  - Data binding with @State, @ObservedObject

- **UIKit**: Older imperative framework
  - View controllers, navigation stack
  - Delegates and data sources
  - Auto Layout constraints

### iOS Architecture
- **MVC**: Model-View-Controller
- **MVVM**: Model-View-ViewModel with observable
- **CLEAN**: Entity, Use Case, Interface
- **Coordinator Pattern**: Navigation management

### Key Frameworks
- **Foundation**: Core utilities and data types
- **CoreData**: Local persistence
- **Networking**: URLSession for API calls
- **CoreLocation**: Location services
- **AVFoundation**: Camera and media

## Android Development Path

### Kotlin Basics
- **Variables & Functions**: val, var, fun
- **Classes & Objects**: Data classes, sealed classes
- **Extension Functions**: Adding methods to types
- **Coroutines**: async/await equivalent
- **Flow**: Reactive streams

### UI Frameworks
- **Jetpack Compose**: Modern declarative UI (recommended)
  - Composables, state hoisting
  - Layouts and modifiers
  - Navigation, animation

- **XML Layouts**: Traditional approach
  - Activity, Fragment architecture
  - View binding, data binding

### Android Architecture
- **MVC**: Model-View-Controller
- **MVVM**: ViewModel, LiveData, Data Binding
- **CLEAN**: Separation of concerns
- **Repository Pattern**: Data abstraction

### Key Libraries
- **Jetpack Components**: Room, Lifecycle, ViewModel
- **Retrofit**: HTTP client
- **Hilt**: Dependency injection
- **Firebase**: Analytics, push notifications

## Cross-Platform: React Native

### Setup & Development
- **Expo**: Managed development environment
- **React Native CLI**: Full control
- **Navigation**: React Navigation
- **State Management**: Redux, Context API

### Advantages & Tradeoffs
- **Pros**: Code sharing, JavaScript ecosystem
- **Cons**: Performance, native feel, tooling maturity

### Best Practices
- Platform-specific code separation
- Native module development
- Performance optimization
- Bridge communication with native

## Cross-Platform: Flutter

### Setup & Development
- **Dart Language**: Flutter's language
- **Widget Tree**: UI composition
- **State Management**: Provider, Riverpod, Bloc
- **Navigation**: Named routes, deep linking

### Advantages
- **Performance**: Compiled to native
- **Hot Reload**: Fast development
- **Beautiful UI**: Rich widget library
- **Single Codebase**: iOS and Android

### Ecosystem
- **Pub.dev**: Package registry
- **Popular Packages**: http, provider, get
- **Plugins**: Native functionality access
- **Firebase Integration**: Easy setup

## Mobile Development Essentials

### Networking
- **REST APIs**: JSON parsing, error handling
- **GraphQL**: Mobile query language
- **Offline Sync**: Local storage, sync strategies
- **SSL Pinning**: Security

### Local Data
- **SQLite**: Structured data
- **Key-Value Storage**: SharedPreferences, UserDefaults
- **File System**: Documents, cache directories

### Authentication
- **OAuth 2.0**: Third-party login
- **JWT**: Token-based auth
- **Biometric**: Face ID, fingerprint
- **Session Management**: Token refresh

### Testing
- **Unit Tests**: Business logic
- **Widget/Component Tests**: UI testing
- **Integration Tests**: Full app flows
- **UI Automation**: End-to-end testing

## Deployment

### iOS
1. Apple Developer Account registration
2. Create certificates and identifiers
3. Build and archive app
4. Submit to App Store
5. Review and approval (1-3 days)

### Android
1. Google Play Account registration
2. Create signing certificate
3. Build release APK/AAB
4. Upload to Google Play
5. Testing and release (instant)

### Publishing Best Practices
- App Store Optimization (ASO)
- Beta testing programs
- Update strategy
- Versioning and release notes

## Projects

1. **Todo App** - Basic CRUD, storage
2. **Weather App** - API integration, UI
3. **Chat Application** - Real-time, networking
4. **E-commerce App** - Complex UI, payments
5. **Fitness Tracker** - Sensors, data analysis

## Resources

### Learning Platforms
- **Udemy**: Framework-specific courses
- **Pluralsight**: In-depth iOS/Android paths
- **Google Codelabs**: Official Android tutorials
- **Apple Developer**: Official iOS resources

### Documentation
- [Swift.org](https://swift.org/)
- [Android Developers](https://developer.android.com/)
- [React Native](https://reactnative.dev/)
- [Flutter](https://flutter.dev/)

### Communities
- **Stack Overflow**: Question and answers
- **Reddit**: r/iOSProgramming, r/android, r/flutterdev
- **GitHub**: Open source projects
- **Local Meetups**: Developer communities

**Roadmap.sh Reference**: https://roadmap.sh/mobile

---

**Status**: ✅ Production Ready | **SASMP**: v1.3.0 | **Bonded Agent**: 05-mobile-specialist
