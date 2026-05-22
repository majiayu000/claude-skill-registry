---
name: websocket-integration
description: WebSocket and Socket.io integration for real-time communication in Flutter
keywords: websocket, socket.io, realtime, chat, streaming
---

# Skill 16: WebSocket Integration

## Overview

This skill enables real-time bidirectional communication between Flutter apps and servers using WebSocket or Socket.io protocols. Perfect for chat applications, live updates, notifications, and collaborative features.

## Features

- WebSocket client with auto-reconnection
- Socket.io integration with fallback
- Connection state management
- Message queuing when offline
- Heartbeat/ping-pong handling
- Multiple concurrent connections

## Installation

### Dependencies

```yaml
dependencies:
  web_socket_channel: ^2.4.0
  socket_io_client: ^2.0.3
  connectivity_plus: ^5.0.2
```

## Basic Usage

### 1. WebSocket Service

```dart
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:web_socket_channel/io.dart';

class WebSocketService {
  WebSocketChannel? _channel;
  final String url;
  final Function(dynamic)? onMessage;
  final Function()? onConnect;
  final Function(dynamic)? onError;
  final Function(int?)? onClose;

  WebSocketService({
    required this.url,
    this.onMessage,
    this.onConnect,
    this.onError,
    this.onClose,
  });

  void connect() {
    try {
      _channel = IOWebSocketChannel.connect(url);

      _channel!.stream.listen(
        (message) {
          onMessage?.call(message);
        },
        onDone: () {
          onClose?.call(_channel?.closeCode);
        },
        onError: (error) {
          onError?.call(error);
        },
      );

      onConnect?.call();
    } catch (e) {
      onError?.call(e);
    }
  }

  void send(dynamic message) {
    _channel?.sink.add(message);
  }

  void disconnect() {
    _channel?.sink.close();
    _channel = null;
  }
}
```

### 2. WebSocket Provider with Riverpod

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

class WebSocketState {
  final bool isConnected;
  final List<String> messages;
  final String? error;

  WebSocketState({
    this.isConnected = false,
    this.messages = const [],
    this.error,
  });

  WebSocketState copyWith({
    bool? isConnected,
    List<String>? messages,
    String? error,
  }) {
    return WebSocketState(
      isConnected: isConnected ?? this.isConnected,
      messages: messages ?? this.messages,
      error: error,
    );
  }
}

class WebSocketNotifier extends StateNotifier<WebSocketState> {
  late final WebSocketService _service;

  WebSocketNotifier() : super(WebSocketState()) {
    _service = WebSocketService(
      url: 'wss://your-server.com/ws',
      onMessage: _handleMessage,
      onConnect: () => state = state.copyWith(isConnected: true),
      onClose: (_) => state = state.copyWith(isConnected: false),
      onError: (error) => state = state.copyWith(error: error.toString()),
    );
  }

  void connect() => _service.connect();
  void disconnect() => _service.disconnect();
  void send(String message) => _service.send(message);

  void _handleMessage(dynamic message) {
    final messages = [...state.messages, message.toString()];
    state = state.copyWith(messages: messages);
  }
}

final webSocketProvider = StateNotifierProvider<WebSocketNotifier, WebSocketState>(
  (ref) => WebSocketNotifier(),
);
```

### 3. Socket.io Implementation

```dart
import 'package:socket_io_client/socket_io_client.dart' as io;

class SocketIOService {
  io.Socket? _socket;
  final String url;

  SocketIOService({required this.url});

  void connect() {
    _socket = io.io(url, <String, dynamic>{
      'transports': ['websocket'],
      'autoConnect': true,
    });

    _socket!.onConnect((_) {
      print('Connected to Socket.io');
    });

    _socket!.onDisconnect((_) {
      print('Disconnected from Socket.io');
    });

    _socket!.on('message', (data) {
      print('Received: $data');
    });
  }

  void emit(String event, dynamic data) {
    _socket?.emit(event, data);
  }

  void on(String event, Function(dynamic) handler) {
    _socket?.on(event, handler);
  }

  void disconnect() {
    _socket?.disconnect();
  }
}
```

## Advanced Features

### Auto-Reconnection with Exponential Backoff

```dart
class ReconnectingWebSocket {
  final String url;
  final Duration initialDelay;
  final Duration maxDelay;
  final int maxAttempts;

  int _attempts = 0;
  Timer? _reconnectTimer;

  void _scheduleReconnect() {
    if (_attempts >= maxAttempts) return;

    final delay = Duration(
      milliseconds: min(
        initialDelay.inMilliseconds * pow(2, _attempts),
        maxDelay.inMilliseconds,
      ),
    );

    _reconnectTimer = Timer(delay, () {
      _attempts++;
      connect();
    });
  }
}
```

### Message Queue for Offline Support

```dart
class WebSocketMessageQueue {
  final List<String> _queue = [];

  void enqueue(String message) {
    _queue.add(message);
  }

  void flush(WebSocketService service) {
    while (_queue.isNotEmpty) {
      final message = _queue.removeAt(0);
      service.send(message);
    }
  }
}
```

## Usage Example: Chat Application

```dart
class ChatPage extends ConsumerWidget {
  const ChatPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final wsState = ref.watch(webSocketProvider);
    final wsNotifier = ref.read(webSocketProvider.notifier);
    final messageController = TextEditingController();

    return Scaffold(
      appBar: AppBar(
        title: Text('Chat ${wsState.isConnected ? "(Online)" : "(Offline)"}'),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: wsState.messages.length,
              itemBuilder: (context, index) {
                return ListTile(
                  title: Text(wsState.messages[index]),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: messageController,
                    decoration: const InputDecoration(
                      hintText: 'Type a message...',
                    ),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send),
                  onPressed: () {
                    if (messageController.text.isNotEmpty) {
                      wsNotifier.send(messageController.text);
                      messageController.clear();
                    }
                  },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
```

## Testing

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';

class MockWebSocketChannel extends Mock implements WebSocketChannel {}

void main() {
  test('WebSocket connection test', () async {
    final service = WebSocketService(url: 'ws://test.com');

    bool connected = false;
    service.onConnect = () => connected = true;

    service.connect();

    expect(connected, true);
  });
}
```

## Best Practices

1. **Always handle disconnection gracefully** - Implement reconnection logic
2. **Use message queuing** - Queue messages when offline
3. **Implement heartbeat** - Keep connection alive with ping/pong
4. **Secure connections** - Use WSS (WebSocket Secure) in production
5. **Limit concurrent connections** - Don't open too many WebSocket connections
6. **Clean up on dispose** - Always close connections when not needed

## Security Considerations

- Use WSS (WebSocket Secure) instead of WS
- Implement authentication tokens in connection headers
- Validate all incoming messages
- Rate limiting on server side
- Sanitize user inputs

## Troubleshooting

### Connection drops frequently
- Check network stability
- Implement heartbeat/ping-pong
- Increase timeout values

### Messages not received
- Verify server is broadcasting correctly
- Check event names match exactly
- Ensure listener is registered before connection

### High battery usage
- Reduce reconnection frequency
- Close connection when app is backgrounded
- Use push notifications instead of persistent connection
