# 🔧 Skill: Native Integration (Swift/Kotlin)

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-native-integration` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `native-integration`, `swift`, `kotlin`, `uikit`, `android-sdk`, `native-ui` |
| **Referencia** | [Flutter Platform Integration](https://docs.flutter.dev/platform-integration) |

## 🔑 Keywords para Invocación

Usa cualquiera de estos keywords en tus prompts para invocar este skill:

- `native-integration`
- `swift-integration`
- `kotlin-integration`
- `uikit`
- `android-sdk`
- `native-ui`
- `native-camera`
- `@skill:native-integration`

### Ejemplos de Prompts

```
Implementa native-integration para acceso a cámara nativa en iOS y Android
```

```
Necesito swift + kotlin integration para usar SDKs nativos
```

```
Integra componentes de UIKit nativos en Flutter
```

```
@skill:native-integration - Setup completo de native APIs
```

## 📖 Descripción

Este skill cubre la integración profunda con APIs y frameworks nativos de iOS (Swift/UIKit) y Android (Kotlin/Android SDK), más allá de simples Platform Channels. Incluye componentes UI nativos, acceso a hardware, file system, y extensiones de aplicaciones.

### ✅ Cuándo Usar Este Skill

- Integrar componentes UI nativos complejos
- Acceso avanzado a cámara/galería
- Manipulación del file system
- Integración con frameworks nativos (UIKit, SwiftUI, Jetpack Compose)
- App Extensions (Today Widgets, Share Extensions)
- Universal Links / Deep Links nativos
- Push Notifications nativas
- Background fetch y tasks
- Integración con Apple/Google services

### ❌ Cuándo NO Usar Este Skill

- Flutter puro satisface los requisitos
- Package existente cubre la funcionalidad
- No necesitas funcionalidad específica de plataforma

## 🏗️ Estructura del Proyecto

```
my_app/
├── lib/
│   ├── native/
│   │   ├── camera_native.dart
│   │   ├── file_system_native.dart
│   │   ├── native_ui_components.dart
│   │   └── platform_view_factory.dart
│   │
│   └── main.dart
│
├── android/
│   └── app/src/main/kotlin/com/example/myapp/
│       ├── native/
│       │   ├── CameraManager.kt
│       │   ├── FileSystemManager.kt
│       │   ├── NativeViewFactory.kt
│       │   └── CustomNativeView.kt
│       ├── utils/
│       │   ├── PermissionManager.kt
│       │   └── BitmapUtils.kt
│       └── MainActivity.kt
│
├── ios/
│   └── Runner/
│       ├── Native/
│       │   ├── CameraManager.swift
│       │   ├── FileSystemManager.swift
│       │   ├── NativeViewFactory.swift
│       │   └── CustomNativeView.swift
│       ├── Extensions/
│       │   ├── TodayExtension/
│       │   └── ShareExtension/
│       └── AppDelegate.swift
│
└── integration_test/
    └── native_integration_test.dart
```

## 📦 Dependencias

```yaml
dependencies:
  flutter:
    sdk: flutter
  path_provider: ^2.1.1
  image_picker: ^1.0.5
  permission_handler: ^11.1.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  integration_test:
    sdk: flutter
```

## 💻 Implementación

### 1. Camera Integration Nativa

#### 1.1 Flutter Interface

```dart
// lib/native/camera_native.dart
import 'package:flutter/services.dart';
import 'dart:typed_data';

class CameraNative {
  static const platform = MethodChannel('com.example.myapp/camera');

  // Open native camera with custom settings
  Future<CameraResult?> openNativeCamera({
    CameraQuality quality = CameraQuality.high,
    bool allowEditing = false,
    CameraDevice preferredDevice = CameraDevice.back,
  }) async {
    try {
      final Map<dynamic, dynamic> result = await platform.invokeMethod(
        'openCamera',
        {
          'quality': quality.value,
          'allowEditing': allowEditing,
          'preferredDevice': preferredDevice.value,
        },
      );

      if (result['success'] == true) {
        return CameraResult(
          imagePath: result['imagePath'] as String,
          imageData: result['imageData'] as Uint8List?,
          width: result['width'] as int,
          height: result['height'] as int,
          metadata: Map<String, dynamic>.from(result['metadata'] ?? {}),
        );
      }
      return null;
    } on PlatformException catch (e) {
      print('Camera error: ${e.message}');
      return null;
    }
  }

  // Access photo library
  Future<List<String>> pickMultiplePhotos({
    int maxImages = 10,
    CameraQuality quality = CameraQuality.medium,
  }) async {
    try {
      final List<dynamic> result = await platform.invokeMethod(
        'pickMultiple',
        {
          'maxImages': maxImages,
          'quality': quality.value,
        },
      );
      return result.cast<String>();
    } on PlatformException catch (e) {
      print('Pick photos error: ${e.message}');
      return [];
    }
  }

  // Take photo with custom overlay
  Future<String?> takePhotoWithOverlay(String overlayImagePath) async {
    try {
      final String? result = await platform.invokeMethod(
        'takePhotoWithOverlay',
        {'overlayPath': overlayImagePath},
      );
      return result;
    } on PlatformException catch (e) {
      print('Take photo with overlay error: ${e.message}');
      return null;
    }
  }

  // Request camera permission
  Future<bool> requestPermission() async {
    try {
      final bool result = await platform.invokeMethod('requestPermission');
      return result;
    } on PlatformException catch (e) {
      print('Permission error: ${e.message}');
      return false;
    }
  }
}

enum CameraQuality {
  low('low'),
  medium('medium'),
  high('high'),
  max('max');

  final String value;
  const CameraQuality(this.value);
}

enum CameraDevice {
  front('front'),
  back('back');

  final String value;
  const CameraDevice(this.value);
}

class CameraResult {
  final String imagePath;
  final Uint8List? imageData;
  final int width;
  final int height;
  final Map<String, dynamic> metadata;

  CameraResult({
    required this.imagePath,
    this.imageData,
    required this.width,
    required this.height,
    required this.metadata,
  });
}
```

#### 1.2 iOS (Swift) Implementation

```swift
// ios/Runner/Native/CameraManager.swift
import UIKit
import AVFoundation
import Photos

class CameraManager: NSObject {
    private var currentViewController: UIViewController?
    private var completion: ((Bool, [String: Any]?) -> Void)?
    
    func openCamera(
        quality: String,
        allowEditing: Bool,
        preferredDevice: String,
        completion: @escaping (Bool, [String: Any]?) -> Void
    ) {
        self.completion = completion
        
        // Check camera permission
        AVCaptureDevice.requestAccess(for: .video) { granted in
            DispatchQueue.main.async {
                if granted {
                    self.presentCamera(
                        quality: quality,
                        allowEditing: allowEditing,
                        preferredDevice: preferredDevice
                    )
                } else {
                    completion(false, ["error": "Camera permission denied"])
                }
            }
        }
    }
    
    private func presentCamera(
        quality: String,
        allowEditing: Bool,
        preferredDevice: String
    ) {
        guard let viewController = UIApplication.shared.keyWindow?.rootViewController else {
            completion?(false, ["error": "No view controller available"])
            return
        }
        
        let picker = UIImagePickerController()
        picker.delegate = self
        picker.sourceType = .camera
        picker.allowsEditing = allowEditing
        
        // Set camera device
        if preferredDevice == "front" {
            picker.cameraDevice = .front
        } else {
            picker.cameraDevice = .rear
        }
        
        // Set quality
        switch quality {
        case "high":
            picker.cameraCaptureMode = .photo
            picker.cameraFlashMode = .auto
        case "max":
            picker.cameraCaptureMode = .photo
        default:
            break
        }
        
        currentViewController = viewController
        viewController.present(picker, animated: true)
    }
    
    func pickMultiplePhotos(
        maxImages: Int,
        quality: String,
        completion: @escaping (Bool, [String]?) -> Void
    ) {
        if #available(iOS 14, *) {
            var config = PHPickerConfiguration()
            config.selectionLimit = maxImages
            config.filter = .images
            
            let picker = PHPickerViewController(configuration: config)
            picker.delegate = self
            
            guard let viewController = UIApplication.shared.keyWindow?.rootViewController else {
                completion(false, nil)
                return
            }
            
            viewController.present(picker, animated: true)
        } else {
            // Fallback for older iOS versions
            completion(false, ["Requires iOS 14+"])
        }
    }
    
    private func saveImage(_ image: UIImage) -> [String: Any]? {
        guard let data = image.jpegData(compressionQuality: 0.8) else {
            return nil
        }
        
        let filename = UUID().uuidString + ".jpg"
        let documentsPath = FileManager.default.urls(
            for: .documentDirectory,
            in: .userDomainMask
        )[0]
        let imagePath = documentsPath.appendingPathComponent(filename)
        
        do {
            try data.write(to: imagePath)
            
            return [
                "success": true,
                "imagePath": imagePath.path,
                "imageData": data,
                "width": Int(image.size.width),
                "height": Int(image.size.height),
                "metadata": [
                    "orientation": image.imageOrientation.rawValue,
                    "format": "JPEG"
                ]
            ]
        } catch {
            return nil
        }
    }
}

extension CameraManager: UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    func imagePickerController(
        _ picker: UIImagePickerController,
        didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]
    ) {
        picker.dismiss(animated: true)
        
        if let image = info[.editedImage] as? UIImage ?? info[.originalImage] as? UIImage {
            let result = saveImage(image)
            completion?(true, result)
        } else {
            completion?(false, ["error": "No image selected"])
        }
    }
    
    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
        picker.dismiss(animated: true)
        completion?(false, ["error": "User cancelled"])
    }
}

@available(iOS 14, *)
extension CameraManager: PHPickerViewControllerDelegate {
    func picker(_ picker: PHPickerViewController, didFinishPicking results: [PHPickerResult]) {
        picker.dismiss(animated: true)
        
        var imagePaths: [String] = []
        let group = DispatchGroup()
        
        for result in results {
            group.enter()
            result.itemProvider.loadObject(ofClass: UIImage.self) { [weak self] object, error in
                defer { group.leave() }
                
                if let image = object as? UIImage,
                   let result = self?.saveImage(image),
                   let path = result["imagePath"] as? String {
                    imagePaths.append(path)
                }
            }
        }
        
        group.notify(queue: .main) {
            self.completion?(true, ["paths": imagePaths])
        }
    }
}
```

#### 1.3 Android (Kotlin) Implementation

```kotlin
// android/app/src/main/kotlin/com/example/myapp/native/CameraManager.kt
package com.example.myapp.native

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.net.Uri
import android.provider.MediaStore
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.content.FileProvider
import io.flutter.plugin.common.MethodChannel
import java.io.File
import java.io.FileOutputStream
import java.util.*

class CameraManager(private val activity: Activity) {
    private var result: MethodChannel.Result? = null
    private var currentPhotoPath: String? = null

    companion object {
        const val REQUEST_CAMERA = 100
        const val REQUEST_PERMISSION = 101
        const val REQUEST_PICK_MULTIPLE = 102
    }

    fun openCamera(
        quality: String,
        allowEditing: Boolean,
        preferredDevice: String,
        result: MethodChannel.Result
    ) {
        this.result = result

        if (checkCameraPermission()) {
            launchCamera(quality, allowEditing)
        } else {
            requestCameraPermission()
        }
    }

    private fun launchCamera(quality: String, allowEditing: Boolean) {
        val intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        
        // Create file for photo
        val photoFile = createImageFile()
        currentPhotoPath = photoFile.absolutePath
        
        val photoURI = FileProvider.getUriForFile(
            activity,
            "${activity.packageName}.fileprovider",
            photoFile
        )
        
        intent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI)
        
        // Set quality
        when (quality) {
            "high", "max" -> {
                intent.putExtra(MediaStore.EXTRA_SIZE_LIMIT, Long.MAX_VALUE)
            }
            "medium" -> {
                intent.putExtra(MediaStore.EXTRA_SIZE_LIMIT, 1024 * 1024 * 2) // 2MB
            }
            "low" -> {
                intent.putExtra(MediaStore.EXTRA_SIZE_LIMIT, 1024 * 1024) // 1MB
            }
        }
        
        activity.startActivityForResult(intent, REQUEST_CAMERA)
    }

    fun pickMultiplePhotos(maxImages: Int, quality: String, result: MethodChannel.Result) {
        this.result = result
        
        val intent = Intent(Intent.ACTION_PICK)
        intent.type = "image/*"
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true)
        
        activity.startActivityForResult(
            Intent.createChooser(intent, "Select Pictures"),
            REQUEST_PICK_MULTIPLE
        )
    }

    fun handleActivityResult(requestCode: Int, resultCode: Int, data: Intent?): Boolean {
        when (requestCode) {
            REQUEST_CAMERA -> {
                if (resultCode == Activity.RESULT_OK) {
                    handleCameraResult()
                } else {
                    result?.error("CANCELLED", "User cancelled", null)
                }
                return true
            }
            
            REQUEST_PICK_MULTIPLE -> {
                if (resultCode == Activity.RESULT_OK) {
                    handlePickMultipleResult(data)
                } else {
                    result?.error("CANCELLED", "User cancelled", null)
                }
                return true
            }
        }
        return false
    }

    private fun handleCameraResult() {
        currentPhotoPath?.let { path ->
            val file = File(path)
            if (file.exists()) {
                val bitmap = MediaStore.Images.Media.getBitmap(
                    activity.contentResolver,
                    Uri.fromFile(file)
                )
                
                val resultMap = mapOf(
                    "success" to true,
                    "imagePath" to path,
                    "width" to bitmap.width,
                    "height" to bitmap.height,
                    "metadata" to mapOf(
                        "format" to "JPEG",
                        "size" to file.length()
                    )
                )
                
                result?.success(resultMap)
            } else {
                result?.error("FILE_NOT_FOUND", "Photo file not found", null)
            }
        } ?: result?.error("NO_PATH", "No photo path available", null)
    }

    private fun handlePickMultipleResult(data: Intent?) {
        val imagePaths = mutableListOf<String>()
        
        data?.clipData?.let { clipData ->
            for (i in 0 until clipData.itemCount) {
                val uri = clipData.getItemAt(i).uri
                val path = saveImageFromUri(uri)
                path?.let { imagePaths.add(it) }
            }
        } ?: data?.data?.let { uri ->
            val path = saveImageFromUri(uri)
            path?.let { imagePaths.add(it) }
        }
        
        result?.success(imagePaths)
    }

    private fun saveImageFromUri(uri: Uri): String? {
        try {
            val bitmap = MediaStore.Images.Media.getBitmap(activity.contentResolver, uri)
            val file = createImageFile()
            
            FileOutputStream(file).use { out ->
                bitmap.compress(Bitmap.CompressFormat.JPEG, 90, out)
            }
            
            return file.absolutePath
        } catch (e: Exception) {
            e.printStackTrace()
            return null
        }
    }

    private fun createImageFile(): File {
        val timestamp = Date().time
        val storageDir = activity.getExternalFilesDir(null)
        return File(storageDir, "IMG_$timestamp.jpg")
    }

    private fun checkCameraPermission(): Boolean {
        return ContextCompat.checkSelfPermission(
            activity,
            Manifest.permission.CAMERA
        ) == PackageManager.PERMISSION_GRANTED
    }

    private fun requestCameraPermission() {
        ActivityCompat.requestPermissions(
            activity,
            arrayOf(Manifest.permission.CAMERA),
            REQUEST_PERMISSION
        )
    }

    fun handleRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<String>,
        grantResults: IntArray
    ): Boolean {
        if (requestCode == REQUEST_PERMISSION) {
            if (grantResults.isNotEmpty() && 
                grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                launchCamera("medium", false)
            } else {
                result?.error("PERMISSION_DENIED", "Camera permission denied", null)
            }
            return true
        }
        return false
    }
}
```

### 2. Platform Views - Native UI Components

#### 2.1 Flutter Platform View

```dart
// lib/native/native_ui_components.dart
import 'package:flutter/foundation.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class NativeMapView extends StatelessWidget {
  final double latitude;
  final double longitude;
  final double zoom;
  final Function(double, double)? onLocationChanged;

  const NativeMapView({
    Key? key,
    required this.latitude,
    required this.longitude,
    this.zoom = 15.0,
    this.onLocationChanged,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final Map<String, dynamic> creationParams = {
      'latitude': latitude,
      'longitude': longitude,
      'zoom': zoom,
    };

    if (defaultTargetPlatform == TargetPlatform.android) {
      return AndroidView(
        viewType: 'com.example.myapp/native_map',
        layoutDirection: TextDirection.ltr,
        creationParams: creationParams,
        creationParamsCodec: const StandardMessageCodec(),
        gestureRecognizers: <Factory<OneSequenceGestureRecognizer>>{
          Factory<PanGestureRecognizer>(() => PanGestureRecognizer()),
          Factory<ScaleGestureRecognizer>(() => ScaleGestureRecognizer()),
        },
        onPlatformViewCreated: _onPlatformViewCreated,
      );
    } else if (defaultTargetPlatform == TargetPlatform.iOS) {
      return UiKitView(
        viewType: 'com.example.myapp/native_map',
        layoutDirection: TextDirection.ltr,
        creationParams: creationParams,
        creationParamsCodec: const StandardMessageCodec(),
        gestureRecognizers: <Factory<OneSequenceGestureRecognizer>>{
          Factory<PanGestureRecognizer>(() => PanGestureRecognizer()),
        },
        onPlatformViewCreated: _onPlatformViewCreated,
      );
    }

    return Text('Platform not supported');
  }

  void _onPlatformViewCreated(int id) {
    final channel = MethodChannel('com.example.myapp/native_map_$id');
    
    channel.setMethodCallHandler((call) async {
      if (call.method == 'onLocationChanged') {
        final lat = call.arguments['latitude'] as double;
        final lng = call.arguments['longitude'] as double;
        onLocationChanged?.call(lat, lng);
      }
    });
  }
}

// Custom video player usando native views
class NativeVideoPlayer extends StatefulWidget {
  final String videoUrl;
  final bool autoPlay;

  const NativeVideoPlayer({
    Key? key,
    required this.videoUrl,
    this.autoPlay = false,
  }) : super(key: key);

  @override
  State<NativeVideoPlayer> createState() => _NativeVideoPlayerState();
}

class _NativeVideoPlayerState extends State<NativeVideoPlayer> {
  late MethodChannel _channel;
  bool isPlaying = false;
  double progress = 0.0;

  @override
  Widget build(BuildContext context) {
    final Map<String, dynamic> creationParams = {
      'videoUrl': widget.videoUrl,
      'autoPlay': widget.autoPlay,
    };

    Widget platformView;
    if (defaultTargetPlatform == TargetPlatform.android) {
      platformView = AndroidView(
        viewType: 'com.example.myapp/video_player',
        creationParams: creationParams,
        creationParamsCodec: const StandardMessageCodec(),
        onPlatformViewCreated: _onPlatformViewCreated,
      );
    } else if (defaultTargetPlatform == TargetPlatform.iOS) {
      platformView = UiKitView(
        viewType: 'com.example.myapp/video_player',
        creationParams: creationParams,
        creationParamsCodec: const StandardMessageCodec(),
        onPlatformViewCreated: _onPlatformViewCreated,
      );
    } else {
      platformView = Text('Platform not supported');
    }

    return Column(
      children: [
        Expanded(child: platformView),
        _buildControls(),
      ],
    );
  }

  Widget _buildControls() {
    return Row(
      children: [
        IconButton(
          icon: Icon(isPlaying ? Icons.pause : Icons.play_arrow),
          onPressed: _togglePlayPause,
        ),
        Expanded(
          child: Slider(
            value: progress,
            onChanged: _seekTo,
          ),
        ),
      ],
    );
  }

  void _onPlatformViewCreated(int id) {
    _channel = MethodChannel('com.example.myapp/video_player_$id');
    
    _channel.setMethodCallHandler((call) async {
      switch (call.method) {
        case 'onPlaybackStateChanged':
          setState(() {
            isPlaying = call.arguments['isPlaying'] as bool;
          });
          break;
        case 'onProgressChanged':
          setState(() {
            progress = call.arguments['progress'] as double;
          });
          break;
      }
    });
  }

  void _togglePlayPause() {
    _channel.invokeMethod(isPlaying ? 'pause' : 'play');
  }

  void _seekTo(double position) {
    _channel.invokeMethod('seekTo', {'position': position});
  }
}
```

#### 2.2 iOS Platform View Factory

```swift
// ios/Runner/Native/NativeViewFactory.swift
import Flutter
import UIKit
import MapKit

class NativeMapViewFactory: NSObject, FlutterPlatformViewFactory {
    private var messenger: FlutterBinaryMessenger

    init(messenger: FlutterBinaryMessenger) {
        self.messenger = messenger
        super.init()
    }

    func create(
        withFrame frame: CGRect,
        viewIdentifier viewId: Int64,
        arguments args: Any?
    ) -> FlutterPlatformView {
        return NativeMapView(
            frame: frame,
            viewIdentifier: viewId,
            arguments: args,
            binaryMessenger: messenger
        )
    }

    func createArgsCodec() -> FlutterMessageCodec & NSObjectProtocol {
        return FlutterStandardMessageCodec.sharedInstance()
    }
}

class NativeMapView: NSObject, FlutterPlatformView, MKMapViewDelegate {
    private var _mapView: MKMapView
    private var _channel: FlutterMethodChannel

    init(
        frame: CGRect,
        viewIdentifier viewId: Int64,
        arguments args: Any?,
        binaryMessenger messenger: FlutterBinaryMessenger
    ) {
        _mapView = MKMapView(frame: frame)
        _channel = FlutterMethodChannel(
            name: "com.example.myapp/native_map_\(viewId)",
            binaryMessenger: messenger
        )
        super.init()

        // Parse arguments
        if let args = args as? [String: Any] {
            let latitude = args["latitude"] as? Double ?? 0.0
            let longitude = args["longitude"] as? Double ?? 0.0
            let zoom = args["zoom"] as? Double ?? 15.0

            // Set initial location
            let coordinate = CLLocationCoordinate2D(
                latitude: latitude,
                longitude: longitude
            )
            let span = MKCoordinateSpan(
                latitudeDelta: 0.01 * (20.0 - zoom),
                longitudeDelta: 0.01 * (20.0 - zoom)
            )
            let region = MKCoordinateRegion(center: coordinate, span: span)
            _mapView.setRegion(region, animated: false)
        }

        _mapView.delegate = self
        setupMethodChannel()
    }

    func view() -> UIView {
        return _mapView
    }

    private func setupMethodChannel() {
        _channel.setMethodCallHandler { [weak self] (call, result) in
            guard let self = self else { return }
            
            switch call.method {
            case "setLocation":
                if let args = call.arguments as? [String: Any],
                   let lat = args["latitude"] as? Double,
                   let lng = args["longitude"] as? Double {
                    let coordinate = CLLocationCoordinate2D(latitude: lat, longitude: lng)
                    self._mapView.setCenter(coordinate, animated: true)
                    result(nil)
                }
            default:
                result(FlutterMethodNotImplemented)
            }
        }
    }

    func mapView(_ mapView: MKMapView, regionDidChangeAnimated animated: Bool) {
        let center = mapView.centerCoordinate
        _channel.invokeMethod("onLocationChanged", arguments: [
            "latitude": center.latitude,
            "longitude": center.longitude
        ])
    }
}

// Register in AppDelegate:
// let registrar = self.registrar(forPlugin: "com.example.myapp/native_map")!
// let factory = NativeMapViewFactory(messenger: registrar.messenger())
// registrar.register(factory, withId: "com.example.myapp/native_map")
```

### 3. File System Integration

```dart
// lib/native/file_system_native.dart
import 'package:flutter/services.dart';
import 'dart:typed_data';

class FileSystemNative {
  static const platform = MethodChannel('com.example.myapp/filesystem');

  // Read file with native performance
  Future<Uint8List?> readFileNative(String path) async {
    try {
      final Uint8List result = await platform.invokeMethod(
        'readFile',
        {'path': path},
      );
      return result;
    } on PlatformException catch (e) {
      print('Read file error: ${e.message}');
      return null;
    }
  }

  // Write file with native performance
  Future<bool> writeFileNative(String path, Uint8List data) async {
    try {
      final bool result = await platform.invokeMethod(
        'writeFile',
        {'path': path, 'data': data},
      );
      return result;
    } on PlatformException catch (e) {
      print('Write file error: ${e.message}');
      return false;
    }
  }

  // List directory with metadata
  Future<List<FileInfo>> listDirectoryNative(String path) async {
    try {
      final List<dynamic> result = await platform.invokeMethod(
        'listDirectory',
        {'path': path},
      );
      
      return result.map((item) {
        final map = item as Map<dynamic, dynamic>;
        return FileInfo(
          name: map['name'] as String,
          path: map['path'] as String,
          size: map['size'] as int,
          isDirectory: map['isDirectory'] as bool,
          lastModified: DateTime.fromMillisecondsSinceEpoch(
            map['lastModified'] as int,
          ),
        );
      }).toList();
    } on PlatformException catch (e) {
      print('List directory error: ${e.message}');
      return [];
    }
  }

  // Compress/Decompress with native libraries
  Future<bool> compressFile(String sourcePath, String destinationPath) async {
    try {
      final bool result = await platform.invokeMethod(
        'compressFile',
        {'source': sourcePath, 'destination': destinationPath},
      );
      return result;
    } on PlatformException catch (e) {
      print('Compress error: ${e.message}');
      return false;
    }
  }
}

class FileInfo {
  final String name;
  final String path;
  final int size;
  final bool isDirectory;
  final DateTime lastModified;

  FileInfo({
    required this.name,
    required this.path,
    required this.size,
    required this.isDirectory,
    required this.lastModified,
  });
}
```

## 🎯 Mejores Prácticas

### 1. Memory Management

✅ **DO:** Libera recursos nativos
```swift
// iOS
class SomeNativeComponent {
    deinit {
        // Clean up resources
        timer?.invalidate()
        observer?.removeObserver()
    }
}
```

```kotlin
// Android
override fun onDestroy() {
    super.onDestroy()
    // Clean up resources
    disposables.clear()
}
```

### 2. Thread Safety

✅ **DO:** Usa el thread correcto
```swift
// iOS: Siempre actualiza UI en main thread
DispatchQueue.main.async {
    self.eventSink?(data)
}
```

```kotlin
// Android: Usa runOnUiThread
activity.runOnUiThread {
    eventSink.success(data)
}
```

### 3. Error Handling

✅ **DO:** Maneja errores nativos apropiadamente
```swift
do {
    let result = try someNativeOperation()
    result.success(result)
} catch let error as NSError {
    result.error(
        "NATIVE_ERROR",
        error.localizedDescription,
        error.userInfo
    )
}
```

## 🚨 Troubleshooting

### iOS: View Not Displaying

```swift
// Verificar que registraste el factory en AppDelegate
let factory = NativeViewFactory(messenger: registrar.messenger())
registrar.register(factory, withId: "your_view_id")
```

### Android: View Crashes on Rotation

```kotlin
// Implementa lifecycle methods
override fun onConfigurationChanged(newConfig: Configuration) {
    super.onConfigurationChanged(newConfig)
    // Handle rotation
}
```

## 📚 Recursos

- [Platform Views](https://docs.flutter.dev/platform-integration/platform-views)
- [iOS Platform Views](https://docs.flutter.dev/platform-integration/ios/platform-views)
- [Android Platform Views](https://docs.flutter.dev/platform-integration/android/platform-views)

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025  
**Total líneas:** 1,100+

