---
name: flutter-duit-bdui
description: Integrate Duit framework into Flutter applications including setup, driver configuration, HTTP/WebSocket transports, custom widgets, and themes. Use when integrating backend-driven UI, configuring Duit, or adding Duit to Flutter applications.
---

# Fluttter Duit Backend-driven UI

## Overview

Duit enables backend-driven UI in Flutter applications. The server controls both data and layout via JSON, allowing UI updates without app releases.

## Quick Start

1. Add dependency to pubspec.yaml
2. Initialize DuitRegistry (optional: with themes/custom widgets)
3. Create XDriver (HTTP, WebSocket, or static)
4. Wrap UI in DuitViewHost
5. Server sends JSON layouts → Duit renders them

## Prerequisites

### SDK Requirements

```yaml
- Dart SDK: >=3.4.4 <4.0.0
- Flutter: >=3.24.0
```

### Add Dependency

```bash
flutter pub add flutter_duit
```

Install:

```bash
flutter pub get
```

## Basic Integration

### Minimal Setup

```dart
import 'package:flutter/material.dart';
import 'package:flutter_duit/flutter_duit.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: DuitViewHost.withDriver(
          driver: XDriver.static({
            "type": "Text",
            "id": "1",
            "attributes": {"data": "Hello, World!"},
          }),
        ),
      ),
    );
  }
}
```

### Driver Lifecycle Management

Always dispose drivers to prevent memory leaks:

```dart
class MyWidgetState extends State<MyWidget> {
  late final XDriver driver;

  @override
  void initState() {
    super.initState();
    driver = XDriver.static(/* ... */);
  }

  @override
  void dispose() {
    driver.dispose();
    super.dispose();
  }
}
```

## Transport Configuration

### HTTP Transport

Fetch layouts from REST API endpoints:

```dart
final driver = XDriver(
  transportManager: HttpTransportManager(
    options: HttpTransportOptions(
      baseUrl: 'https://api.example.com/view',
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    ),
  ),
);
```

### WebSocket Transport

Real-time bidirectional communication:

```dart
final driver = XDriver(
  transportManager: WSTransportManager(
    options: WSTransportOptions(
      url: 'wss://api.example.com/ws',
      headers: {
        'Authorization': 'Bearer $token',
      },
      reconnectInterval: Duration(seconds: 5),
      heartbeatInterval: Duration(seconds: 30),
    ),
  ),
);
```

### Static/Stub Transport

For testing or local layouts:

```dart
final driver = XDriver.static(
  layoutJson,
);
```

### Custom Decoder/Encoder

```dart
import 'dart:convert';
import 'dart:typed_data';

class CustomDecoder extends Converter<Uint8List, Map<String, dynamic>> {
  @override
  Map<String, dynamic> convert(Uint8List input) {
    // Custom decode logic
    return jsonDecode(utf8.decode(input));
  }
}

final driver = XDriver(
  transportManager: HttpTransportManager(
    options: HttpTransportOptions(
      baseUrl: 'https://api.example.com',
      decoder: CustomDecoder(),
    ),
  ),
);
```

### Custom Transport

Create your own transport implementation if needed:

```dart
class MyCustomTransportManager with TransportCapabilityDelegate {
  @override
  void linkDriver(UIDriver driver) {
    // Implement linkDriver method
  }

  @override
  Stream<Map<String, dynamic>> connect({
    Map<String, dynamic>? initialRequestData,
    Map<String, dynamic>? staticContent,
  }) async* {
    // Implement connect method
  }

  @override
  Future<Map<String, dynamic>?> executeRemoteAction(
    ServerAction action,
    Map<String, dynamic> payload,
  ) async {
    //Implement executeRemoteAction method
  }

  @override
  Future<Map<String, dynamic>?> request(
    String url,
    Map<String, dynamic> meta,
    Map<String, dynamic> body,
  ) async {
    //Implement request method
  }

  @override
  void releaseResources() {
    // Implement linkDriver method
  }
}
```

## Custom Widgets

### Create and register Custom Widget

```dart
import 'package:flutter_duit/flutter_duit.dart';

// 1. Define custom widget
class MyCustomWidget extends StatelessWidget {
  final ViewAttribute attributes;

  const MyCustomWidget({
    required this.attributes,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    final attrs = attributes.payload;
    return Container(
      child: Text(attrs.getString(key: "message")),
    );
  }
}

// 2. Create build factory fn for widget
Widget myCustomBuildFactory(ElementPropertyView model) {
    if (model.isControlled) {
        return MyCustomWidget(
            attributes: model.attributes,
        );
    } else {
        return const SizedBox.shrink();
    }
}

// 3. Register build-fn
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  DuitRegistry.register(
    "MyCustomWidget",
    buildFactory: myCustomBuildFactory,
  );

  runApp(const MyApp());
}
```

## Components

### Components registration

Components allow you to create reusable UI templates that can be referenced by a tag and populated with dynamic data.

```dart
import 'package:flutter_duit/flutter_duit.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Define component template
  final cardComponent = {
    "tag": "CardComponent",
    "layoutRoot": {
      "type": "Container",
      "id": "cardContainer",
      "controlled": false,
      "attributes": {
        "padding": {"all": 16},
        "margin": {"all": 8},
        "decoration": {
          "borderRadius": 12,
          "color": "#FFFFFF",
          "boxShadow": [
            {
              "color": "#00000033",
              "blurRadius": 6,
              "offset": {"dx": 0, "dy": 2},
            },
          ],
        },
      },
      "children": [
        {
          "type": "Text",
          "id": "cardTitle",
          "controlled": false,
          "attributes": {
            "data": {
              "style": {
                "fontSize": 18,
                "fontWeight": "w600",
                "color": "#333333",
              },
            },
            "refs": [
              {
                "objectKey": "title",
                "attributeKey": "data",
              },
            ],
          },
        },
        {
          "type": "Text",
          "id": "cardDescription",
          "controlled": false,
          "attributes": {
            "data": {
              "style": {
                "fontSize": 14,
                "color": "#666666",
              },
            },
            "refs": [
              {
                "objectKey": "description",
                "attributeKey": "data",
              },
            ],
          },
        },
      ],
    },
  };

  // Register the component
  await DuitRegistry.registerComponents([cardComponent]);

  runApp(const MyApp());
}

// Usage in JSON layout from server:
// {
//   "type": "Component",
//   "id": "card1",
//   "tag": "CardComponent",
//   "data": {
//     "title": "Hello World",
//     "description": "This is a card component"
//   }
// }
```

**Key concepts:**

- **tag**: Unique identifier for the component
- **layoutRoot**: Root element of the component template
- **refs**: References to dynamic data passed via the `data` field
- **objectKey**: Key in the `data` object
- **attributeKey**: Attribute in the widget to bind to
- **defaultValue**: Optional default value if data key is missing

You can register multiple components at once:

```dart
await DuitRegistry.registerComponents([
  cardComponent,
  buttonComponent,
  listItemComponent,
]);
```

## When to Use This Skill

Use this skill when:

- Integration flutter_duit library into project
- Custom widet creation
- Components registration
- Basic framework behavior overriding via capabilities implementation
- Need help with the framework API

## Resources

### Reference Documentation

- [capabilities.md](./references/capabiliteis.md) — Notes about capability-based design and core framework parts overriding
- [troubleshooting.md](./references/troubleshooting.md) - Notes about common issues in framework integration
- [environvent_vars.md](./references//environment_vars.md) — Notes about avalilable env variables and its usage
- [public_api.md](./references/public_api.md) — Notes about driver public API
- <https://duit.pro/docs/en> — official documentation site
