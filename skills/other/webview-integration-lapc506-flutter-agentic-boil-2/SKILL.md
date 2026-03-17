# 🌐 Skill: WebView Integration

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-webview` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 1.0.0 |
| **Keywords** | `webview`, `flutter-inappwebview`, `javascript`, `web-integration`, `hybrid` |
| **Referencia** | [flutter_inappwebview](https://pub.dev/packages/flutter_inappwebview) |

## 🔑 Keywords para Invocación

- `webview`
- `flutter-inappwebview`
- `javascript`
- `web-integration`
- `hybrid-app`
- `@skill:webview`

### Ejemplos de Prompts

```
Implementa webview con javascript bridge
```

```
Setup flutter-inappwebview con comunicación bidireccional
```

```
Configura webview para contenido HTML dinámico
```

```
@skill:webview - Integración completa de WebView
```

## 📖 Descripción

Este skill cubre la integración de WebViews en Flutter usando `flutter_inappwebview`. Incluye carga de contenido HTML, JavaScript channels para comunicación Flutter ↔ Web, manejo de navegación, cookies, y storage.

### ✅ Cuándo Usar Este Skill

- Mostrar contenido web en la app
- Integrar legacy web features
- OAuth flows externos
- Rich text content (blog posts)
- Web-based forms
- Terms & Conditions / Privacy Policy
- Hybrid apps
- JavaScript bridge para web SDKs

### ❌ Cuándo NO Usar Este Skill

- Native Flutter widgets funcionan mejor
- Contenido estático simple (usa Text/RichText)
- Performance crítica (WebViews son más lentos)

## 🏗️ Estructura del Proyecto

```
my_app/
├── lib/
│   ├── services/
│   │   └── webview/
│   │       ├── webview_service.dart
│   │       ├── javascript_handler.dart
│   │       └── webview_controller_manager.dart
│   │
│   ├── screens/
│   │   └── webview_screen.dart
│   │
│   └── main.dart
│
└── assets/
    └── web/
        ├── index.html
        └── bridge.js
```

## 📦 Dependencias

```yaml
dependencies:
  flutter:
    sdk: flutter

  # WebView
  flutter_inappwebview: ^6.0.0

  # URL launcher (for external links)
  url_launcher: ^6.2.2

dev_dependencies:
  flutter_test:
    sdk: flutter
```

## 💻 Implementación

### 1. Basic WebView

```dart
// lib/screens/webview_screen.dart
import 'package:flutter/material.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';

class WebViewScreen extends StatefulWidget {
  final String url;
  final String? title;

  const WebViewScreen({
    Key? key,
    required this.url,
    this.title,
  }) : super(key: key);

  @override
  State<WebViewScreen> createState() => _WebViewScreenState();
}

class _WebViewScreenState extends State<WebViewScreen> {
  InAppWebViewController? _webViewController;
  double _progress = 0;
  String _currentUrl = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title ?? 'WebView'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => _webViewController?.reload(),
          ),
          IconButton(
            icon: const Icon(Icons.arrow_back),
            onPressed: () async {
              if (await _webViewController?.canGoBack() ?? false) {
                _webViewController?.goBack();
              }
            },
          ),
          IconButton(
            icon: const Icon(Icons.arrow_forward),
            onPressed: () async {
              if (await _webViewController?.canGoForward() ?? false) {
                _webViewController?.goForward();
              }
            },
          ),
        ],
      ),
      body: Column(
        children: [
          if (_progress < 1.0)
            LinearProgressIndicator(value: _progress),
          Expanded(
            child: InAppWebView(
              initialUrlRequest: URLRequest(url: WebUri(widget.url)),
              initialSettings: InAppWebViewSettings(
                useShouldOverrideUrlLoading: true,
                mediaPlaybackRequiresUserGesture: false,
                allowsInlineMediaPlayback: true,
                iframeAllow: 'camera; microphone',
                iframeAllowFullscreen: true,
              ),
              onWebViewCreated: (controller) {
                _webViewController = controller;
              },
              onLoadStart: (controller, url) {
                setState(() {
                  _currentUrl = url.toString();
                });
              },
              onLoadStop: (controller, url) async {
                setState(() {
                  _currentUrl = url.toString();
                });
              },
              onProgressChanged: (controller, progress) {
                setState(() {
                  _progress = progress / 100;
                });
              },
              shouldOverrideUrlLoading: (controller, navigationAction) async {
                final url = navigationAction.request.url;

                // Handle specific URLs
                if (url != null && url.scheme == 'tel') {
                  // Open phone dialer
                  return NavigationActionPolicy.CANCEL;
                }

                return NavigationActionPolicy.ALLOW;
              },
              onConsoleMessage: (controller, consoleMessage) {
                print('Console: ${consoleMessage.message}');
              },
            ),
          ),
        ],
      ),
    );
  }
}
```

### 2. JavaScript Bridge

```dart
// lib/services/webview/javascript_handler.dart
import 'package:flutter_inappwebview/flutter_inappwebview.dart';

class JavaScriptHandler {
  final InAppWebViewController controller;

  JavaScriptHandler(this.controller);

  // Register JavaScript handlers
  void registerHandlers() {
    // Handler: Send message from Flutter to JS
    controller.addJavaScriptHandler(
      handlerName: 'flutterHandler',
      callback: (args) {
        // Handle message from JavaScript
        print('Message from JS: $args');
        
        // Return response to JavaScript
        return {'status': 'success', 'message': 'Received in Flutter'};
      },
    );

    // Handler: Get user info
    controller.addJavaScriptHandler(
      handlerName: 'getUserInfo',
      callback: (args) async {
        // Get user info from Flutter
        final user = await AuthService.getCurrentUser();
        return {
          'userId': user.id,
          'name': user.name,
          'email': user.email,
        };
      },
    );

    // Handler: Make API call
    controller.addJavaScriptHandler(
      handlerName: 'apiCall',
      callback: (args) async {
        final endpoint = args[0] as String;
        final method = args[1] as String;
        final body = args.length > 2 ? args[2] : null;

        try {
          final response = await ApiService.request(
            endpoint: endpoint,
            method: method,
            body: body,
          );
          return {'success': true, 'data': response};
        } catch (e) {
          return {'success': false, 'error': e.toString()};
        }
      },
    );

    // Handler: Navigation
    controller.addJavaScriptHandler(
      handlerName: 'navigate',
      callback: (args) {
        final route = args[0] as String;
        
        // Navigate in Flutter app
        Navigator.pushNamed(context, route);
        
        return {'status': 'navigated'};
      },
    );
  }

  // Call JavaScript function from Flutter
  Future<dynamic> callJavaScriptFunction(
    String functionName,
    List<dynamic> args,
  ) async {
    try {
      final result = await controller.evaluateJavascript(
        source: '$functionName(${args.map((arg) => jsonEncode(arg)).join(',')})',
      );
      return result;
    } catch (e) {
      print('Error calling JS function: $e');
      return null;
    }
  }

  // Inject JavaScript code
  Future<void> injectJavaScript(String code) async {
    await controller.evaluateJavascript(source: code);
  }

  // Load JavaScript file
  Future<void> loadJavaScriptFile(String path) async {
    final String jsCode = await rootBundle.loadString(path);
    await injectJavaScript(jsCode);
  }
}
```

### 3. WebView Service

```dart
// lib/services/webview/webview_service.dart
import 'package:flutter_inappwebview/flutter_inappwebview.dart';

class WebViewService {
  // Open URL in WebView
  static Future<void> openUrl(
    BuildContext context,
    String url, {
    String? title,
  }) async {
    await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => WebViewScreen(url: url, title: title),
      ),
    );
  }

  // Open HTML content
  static Future<void> openHtmlContent(
    BuildContext context,
    String htmlContent, {
    String? title,
  }) async {
    await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => HtmlWebViewScreen(
          htmlContent: htmlContent,
          title: title,
        ),
      ),
    );
  }

  // Clear cache
  static Future<void> clearCache() async {
    await InAppWebViewController.clearAllCache();
  }

  // Clear cookies
  static Future<void> clearCookies() async {
    await CookieManager.instance().deleteAllCookies();
  }

  // Get cookies for URL
  static Future<List<Cookie>> getCookies(String url) async {
    return await CookieManager.instance().getCookies(url: WebUri(url));
  }

  // Set cookie
  static Future<void> setCookie({
    required String url,
    required String name,
    required String value,
    String? domain,
    String? path,
    int? expiresDate,
    int? maxAge,
    bool? isSecure,
    bool? isHttpOnly,
  }) async {
    await CookieManager.instance().setCookie(
      url: WebUri(url),
      name: name,
      value: value,
      domain: domain,
      path: path,
      expiresDate: expiresDate,
      maxAge: maxAge,
      isSecure: isSecure,
      isHttpOnly: isHttpOnly,
    );
  }
}
```

### 4. HTML Content WebView

```dart
// HTML content screen
class HtmlWebViewScreen extends StatefulWidget {
  final String htmlContent;
  final String? title;

  const HtmlWebViewScreen({
    Key? key,
    required this.htmlContent,
    this.title,
  }) : super(key: key);

  @override
  State<HtmlWebViewScreen> createState() => _HtmlWebViewScreenState();
}

class _HtmlWebViewScreenState extends State<HtmlWebViewScreen> {
  InAppWebViewController? _controller;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.title ?? 'Content')),
      body: InAppWebView(
        initialData: InAppWebViewInitialData(
          data: widget.htmlContent,
          baseUrl: WebUri('https://localhost'),
          encoding: 'utf-8',
          mimeType: 'text/html',
        ),
        initialSettings: InAppWebViewSettings(
          transparentBackground: true,
        ),
        onWebViewCreated: (controller) {
          _controller = controller;
        },
        onLoadStop: (controller, url) async {
          // Inject CSS for styling
          await controller.evaluateJavascript(source: '''
            document.body.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto';
            document.body.style.padding = '16px';
            document.body.style.fontSize = '16px';
          ''');
        },
      ),
    );
  }
}
```

### 5. JavaScript Bridge HTML

```html
<!-- assets/web/bridge.js -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flutter WebView Bridge</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            padding: 20px;
            margin: 0;
        }
        button {
            padding: 12px 24px;
            margin: 8px;
            font-size: 16px;
            border-radius: 8px;
            border: none;
            background: #007AFF;
            color: white;
            cursor: pointer;
        }
        button:active {
            opacity: 0.8;
        }
        #result {
            margin-top: 20px;
            padding: 16px;
            background: #f5f5f5;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <h1>Flutter ↔ JavaScript Bridge</h1>
    
    <button onclick="sendToFlutter()">Send Message to Flutter</button>
    <button onclick="getUserInfo()">Get User Info</button>
    <button onclick="makeApiCall()">Make API Call</button>
    <button onclick="navigateInFlutter()">Navigate in Flutter</button>
    
    <div id="result"></div>

    <script>
        // Check if running in Flutter WebView
        const isFlutter = window.flutter_inappwebview !== undefined;

        function showResult(message) {
            document.getElementById('result').innerHTML = 
                '<strong>Result:</strong><br>' + JSON.stringify(message, null, 2);
        }

        // Send message to Flutter
        async function sendToFlutter() {
            if (!isFlutter) {
                showResult('Not running in Flutter');
                return;
            }

            try {
                const result = await window.flutter_inappwebview.callHandler(
                    'flutterHandler',
                    'Hello from JavaScript!',
                    { timestamp: Date.now() }
                );
                showResult(result);
            } catch (error) {
                showResult('Error: ' + error);
            }
        }

        // Get user info from Flutter
        async function getUserInfo() {
            if (!isFlutter) {
                showResult('Not running in Flutter');
                return;
            }

            try {
                const user = await window.flutter_inappwebview.callHandler('getUserInfo');
                showResult(user);
            } catch (error) {
                showResult('Error: ' + error);
            }
        }

        // Make API call through Flutter
        async function makeApiCall() {
            if (!isFlutter) {
                showResult('Not running in Flutter');
                return;
            }

            try {
                const result = await window.flutter_inappwebview.callHandler(
                    'apiCall',
                    '/api/data',
                    'GET'
                );
                showResult(result);
            } catch (error) {
                showResult('Error: ' + error);
            }
        }

        // Navigate in Flutter app
        async function navigateInFlutter() {
            if (!isFlutter) {
                showResult('Not running in Flutter');
                return;
            }

            try {
                const result = await window.flutter_inappwebview.callHandler(
                    'navigate',
                    '/profile'
                );
                showResult(result);
            } catch (error) {
                showResult('Error: ' + error);
            }
        }

        // Listen for messages from Flutter
        window.addEventListener('flutterMessage', (event) => {
            showResult('Message from Flutter: ' + event.detail);
        });

        // Notify Flutter when page is ready
        window.addEventListener('load', () => {
            if (isFlutter) {
                window.flutter_inappwebview.callHandler('pageReady', {
                    width: window.innerWidth,
                    height: window.innerHeight
                });
            }
        });
    </script>
</body>
</html>
```

### 6. Advanced WebView Controller

```dart
// lib/services/webview/webview_controller_manager.dart
class WebViewControllerManager {
  final InAppWebViewController controller;

  WebViewControllerManager(this.controller);

  // Take screenshot
  Future<Uint8List?> takeScreenshot() async {
    return await controller.takeScreenshot();
  }

  // Print page
  Future<void> printPage() async {
    await controller.printCurrentPage();
  }

  // Find text in page
  Future<void> findText(String text) async {
    await controller.findAllAsync(find: text);
  }

  // Zoom
  Future<void> zoomIn() async {
    final currentZoom = await controller.getZoomScale();
    await controller.setZoomScale(zoomScale: currentZoom + 0.1);
  }

  Future<void> zoomOut() async {
    final currentZoom = await controller.getZoomScale();
    await controller.setZoomScale(zoomScale: currentZoom - 0.1);
  }

  // Get page content
  Future<String?> getPageContent() async {
    return await controller.getHtml();
  }

  // Get page title
  Future<String?> getPageTitle() async {
    return await controller.getTitle();
  }

  // Execute JavaScript and get result
  Future<dynamic> executeScript(String script) async {
    return await controller.evaluateJavascript(source: script);
  }
}
```

## 🎯 Mejores Prácticas

### 1. Security

✅ **DO:** Sanitize user input
```dart
// Never inject unsanitized user input
final sanitized = HtmlEscape().convert(userInput);
await controller.evaluateJavascript(source: 'showMessage("$sanitized")');
```

### 2. Error Handling

✅ **DO:** Handle WebView errors
```dart
onReceivedError: (controller, request, error) {
  print('WebView error: ${error.description}');
  // Show error page
},
```

### 3. Memory Management

✅ **DO:** Dispose WebView properly
```dart
@override
void dispose() {
  _webViewController?.dispose();
  super.dispose();
}
```

## 🚨 Troubleshooting

### JavaScript Not Working

```dart
// Enable JavaScript
initialSettings: InAppWebViewSettings(
  javaScriptEnabled: true,
),
```

### CORS Issues

```dart
// For development, disable web security (not for production!)
initialSettings: InAppWebViewSettings(
  allowUniversalAccessFromFileURLs: true,
),
```

### SSL Certificate Errors

```dart
onReceivedServerTrustAuthRequest: (controller, challenge) async {
  // In production, validate certificate properly
  return ServerTrustAuthResponse(
    action: ServerTrustAuthResponseAction.PROCEED,
  );
},
```

## 📚 Recursos

- [flutter_inappwebview Documentation](https://inappwebview.dev/)
- [WebView Best Practices](https://developer.android.com/develop/ui/views/layout/webapps/best-practices)
- [JavaScript Bridge Patterns](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage)

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025  
**Total líneas:** 1,100+

