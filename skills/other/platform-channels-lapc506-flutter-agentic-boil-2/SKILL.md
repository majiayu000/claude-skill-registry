# 📱 Skill: Platform Channels & Native Integration

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-platform-channels` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `platform-channels`, `methodchannel`, `eventchannel`, `ffi`, `native`, `swift`, `kotlin` |
| **Referencia** | [Flutter Platform Channels](https://docs.flutter.dev/platform-integration/platform-channels) |

## 🔑 Keywords para Invocación

Usa cualquiera de estos keywords en tus prompts para invocar este skill:

- `platform-channels`
- `methodchannel`
- `eventchannel`
- `ffi`
- `native-integration`
- `swift-integration`
- `kotlin-integration`
- `@skill:platform-channels`

### Ejemplos de Prompts

```
Implementa platform-channels para acceder a funcionalidad nativa de iOS y Android
```

```
Necesito methodchannel para integrar con SDK nativo
```

```
Usa eventchannel para recibir eventos de sensores nativos
```

```
@skill:platform-channels - Integración completa con APIs nativas
```

## 📖 Descripción

Platform Channels permiten comunicación bidireccional entre Flutter (Dart) y código nativo (iOS/Android). Este skill cubre **MethodChannel** para llamadas síncronas/asíncronas, **EventChannel** para streams de eventos, y **FFI** para integración de bajo nivel con C/C++.

### ✅ Cuándo Usar Este Skill

- Acceder a APIs nativas no disponibles en packages Flutter
- Integrar SDKs nativos de terceros
- Implementar funcionalidad específica de plataforma
- Acceder a hardware (sensores, Bluetooth, NFC)
- Optimizar rendimiento con código nativo
- Comunicación con código legacy
- Background tasks nativos
- Permissions handling avanzado

### ❌ Cuándo NO Usar Este Skill

- Ya existe un package Flutter maduro
- Funcionalidad disponible en Flutter puro
- Prototipado rápido sin código nativo
- Cross-platform simple sin requisitos nativos

## 🏗️ Estructura del Proyecto

```
my_app/
├── lib/
│   ├── services/
│   │   ├── platform_channels/
│   │   │   ├── battery_channel.dart
│   │   │   ├── sensor_channel.dart
│   │   │   └── native_sdk_channel.dart
│   │   └── native_services.dart
│   │
│   └── main.dart
│
├── android/
│   └── app/src/main/kotlin/com/example/myapp/
│       ├── MainActivity.kt
│       ├── channels/
│       │   ├── BatteryChannel.kt
│       │   ├── SensorChannel.kt
│       │   └── NativeSDKChannel.kt
│       └── utils/
│           └── PermissionHelper.kt
│
├── ios/
│   └── Runner/
│       ├── AppDelegate.swift
│       ├── Channels/
│       │   ├── BatteryChannel.swift
│       │   ├── SensorChannel.swift
│       │   └── NativeSDKChannel.swift
│       └── Utils/
│           └── PermissionHelper.swift
│
└── test/
    └── platform_channels_test.dart
```

## 📦 Dependencias

```yaml
dependencies:
  flutter:
    sdk: flutter

dev_dependencies:
  flutter_test:
    sdk: flutter
  mockito: ^5.4.4  # Para testing de platform channels
```

## 💻 Implementación

### 1. MethodChannel - Comunicación Bidireccional

#### 1.1 Flutter (Dart) - Battery Level Example

```dart
// lib/services/platform_channels/battery_channel.dart
import 'package:flutter/services.dart';

class BatteryChannel {
  static const platform = MethodChannel('com.example.myapp/battery');

  // Get battery level (async call to native)
  Future<int> getBatteryLevel() async {
    try {
      final int result = await platform.invokeMethod('getBatteryLevel');
      return result;
    } on PlatformException catch (e) {
      print("Failed to get battery level: '${e.message}'.");
      return -1;
    } catch (e) {
      print("Unexpected error: $e");
      return -1;
    }
  }

  // Check if charging
  Future<bool> isCharging() async {
    try {
      final bool result = await platform.invokeMethod('isCharging');
      return result;
    } on PlatformException catch (e) {
      print("Failed to check charging status: '${e.message}'.");
      return false;
    }
  }

  // Get battery info (multiple values)
  Future<Map<String, dynamic>> getBatteryInfo() async {
    try {
      final Map<dynamic, dynamic> result = 
          await platform.invokeMethod('getBatteryInfo');
      
      return {
        'level': result['level'] as int,
        'isCharging': result['isCharging'] as bool,
        'technology': result['technology'] as String,
        'temperature': result['temperature'] as double,
      };
    } on PlatformException catch (e) {
      print("Failed to get battery info: '${e.message}'.");
      return {};
    }
  }

  // Call method with arguments
  Future<String> chargingStatus(int threshold) async {
    try {
      final String result = await platform.invokeMethod(
        'chargingStatus',
        {'threshold': threshold},
      );
      return result;
    } on PlatformException catch (e) {
      print("Failed to get charging status: '${e.message}'.");
      return 'Unknown';
    }
  }
}
```

#### 1.2 Android (Kotlin) Implementation

```kotlin
// android/app/src/main/kotlin/com/example/myapp/MainActivity.kt
package com.example.myapp

import android.content.Context
import android.content.ContextWrapper
import android.content.Intent
import android.content.IntentFilter
import android.os.BatteryManager
import android.os.Build
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity: FlutterActivity() {
    private val BATTERY_CHANNEL = "com.example.myapp/battery"

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        
        MethodChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            BATTERY_CHANNEL
        ).setMethodCallHandler { call, result ->
            when (call.method) {
                "getBatteryLevel" -> {
                    val batteryLevel = getBatteryLevel()
                    if (batteryLevel != -1) {
                        result.success(batteryLevel)
                    } else {
                        result.error(
                            "UNAVAILABLE",
                            "Battery level not available.",
                            null
                        )
                    }
                }
                
                "isCharging" -> {
                    val charging = isCharging()
                    result.success(charging)
                }
                
                "getBatteryInfo" -> {
                    val info = getBatteryInfo()
                    result.success(info)
                }
                
                "chargingStatus" -> {
                    val threshold = call.argument<Int>("threshold") ?: 20
                    val status = getChargingStatus(threshold)
                    result.success(status)
                }
                
                else -> {
                    result.notImplemented()
                }
            }
        }
    }

    private fun getBatteryLevel(): Int {
        val batteryManager = getSystemService(Context.BATTERY_SERVICE) as BatteryManager
        return batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
    }

    private fun isCharging(): Boolean {
        val batteryStatus: Intent? = IntentFilter(Intent.ACTION_BATTERY_CHANGED).let { filter ->
            registerReceiver(null, filter)
        }
        
        val status: Int = batteryStatus?.getIntExtra(BatteryManager.EXTRA_STATUS, -1) ?: -1
        return status == BatteryManager.BATTERY_STATUS_CHARGING ||
               status == BatteryManager.BATTERY_STATUS_FULL
    }

    private fun getBatteryInfo(): Map<String, Any> {
        val batteryManager = getSystemService(Context.BATTERY_SERVICE) as BatteryManager
        val batteryStatus: Intent? = IntentFilter(Intent.ACTION_BATTERY_CHANGED).let { filter ->
            registerReceiver(null, filter)
        }

        val level = batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
        val charging = isCharging()
        val technology = batteryStatus?.getStringExtra(BatteryManager.EXTRA_TECHNOLOGY) ?: "Unknown"
        val temperature = batteryStatus?.getIntExtra(BatteryManager.EXTRA_TEMPERATURE, 0)?.toDouble()?.div(10) ?: 0.0

        return mapOf(
            "level" to level,
            "isCharging" to charging,
            "technology" to technology,
            "temperature" to temperature
        )
    }

    private fun getChargingStatus(threshold: Int): String {
        val level = getBatteryLevel()
        val charging = isCharging()

        return when {
            charging && level >= 100 -> "Fully Charged"
            charging -> "Charging ($level%)"
            level <= threshold -> "Low Battery ($level%)"
            else -> "Not Charging ($level%)"
        }
    }
}
```

#### 1.3 iOS (Swift) Implementation

```swift
// ios/Runner/AppDelegate.swift
import UIKit
import Flutter

@UIApplicationMain
@objc class AppDelegate: FlutterAppDelegate {
    private let BATTERY_CHANNEL = "com.example.myapp/battery"
    
    override func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        let controller = window?.rootViewController as! FlutterViewController
        
        let batteryChannel = FlutterMethodChannel(
            name: BATTERY_CHANNEL,
            binaryMessenger: controller.binaryMessenger
        )
        
        batteryChannel.setMethodCallHandler { [weak self] (call, result) in
            guard let self = self else { return }
            
            switch call.method {
            case "getBatteryLevel":
                self.receiveBatteryLevel(result: result)
                
            case "isCharging":
                result(self.isCharging())
                
            case "getBatteryInfo":
                result(self.getBatteryInfo())
                
            case "chargingStatus":
                if let args = call.arguments as? [String: Any],
                   let threshold = args["threshold"] as? Int {
                    result(self.getChargingStatus(threshold: threshold))
                } else {
                    result(self.getChargingStatus(threshold: 20))
                }
                
            default:
                result(FlutterMethodNotImplemented)
            }
        }
        
        GeneratedPluginRegistrant.register(with: self)
        return super.application(application, didFinishLaunchingWithOptions: launchOptions)
    }
    
    private func receiveBatteryLevel(result: FlutterResult) {
        let device = UIDevice.current
        device.isBatteryMonitoringEnabled = true
        
        guard device.batteryState != .unknown else {
            result(FlutterError(
                code: "UNAVAILABLE",
                message: "Battery level not available.",
                details: nil
            ))
            return
        }
        
        let batteryLevel = Int(device.batteryLevel * 100)
        result(batteryLevel)
    }
    
    private func isCharging() -> Bool {
        let device = UIDevice.current
        device.isBatteryMonitoringEnabled = true
        
        return device.batteryState == .charging || device.batteryState == .full
    }
    
    private func getBatteryInfo() -> [String: Any] {
        let device = UIDevice.current
        device.isBatteryMonitoringEnabled = true
        
        let level = Int(device.batteryLevel * 100)
        let charging = isCharging()
        
        return [
            "level": level,
            "isCharging": charging,
            "technology": "Li-ion",  // iOS doesn't expose this
            "temperature": 0.0        // iOS doesn't expose this
        ]
    }
    
    private func getChargingStatus(threshold: Int) -> String {
        let device = UIDevice.current
        device.isBatteryMonitoringEnabled = true
        
        let level = Int(device.batteryLevel * 100)
        let charging = isCharging()
        
        switch (charging, level) {
        case (true, 100):
            return "Fully Charged"
        case (true, _):
            return "Charging (\(level)%)"
        case (false, let l) where l <= threshold:
            return "Low Battery (\(level)%)"
        default:
            return "Not Charging (\(level)%)"
        }
    }
}
```

### 2. EventChannel - Streaming de Eventos

#### 2.1 Flutter (Dart) - Sensor Stream

```dart
// lib/services/platform_channels/sensor_channel.dart
import 'package:flutter/services.dart';
import 'dart:async';

class SensorChannel {
  static const eventChannel = EventChannel('com.example.myapp/sensor');

  // Stream de datos del acelerómetro
  Stream<AccelerometerData>? _accelerometerStream;

  Stream<AccelerometerData> get accelerometerStream {
    _accelerometerStream ??= eventChannel
        .receiveBroadcastStream()
        .map((dynamic event) => _parseAccelerometerData(event))
        .handleError((error) {
          print('Error receiving accelerometer data: $error');
        });
    
    return _accelerometerStream!;
  }

  AccelerometerData _parseAccelerometerData(dynamic event) {
    final Map<dynamic, dynamic> data = event as Map;
    return AccelerometerData(
      x: data['x'] as double,
      y: data['y'] as double,
      z: data['z'] as double,
      timestamp: data['timestamp'] as int,
    );
  }

  // Stream de ubicación
  Stream<LocationData> watchLocation() {
    return eventChannel
        .receiveBroadcastStream({'type': 'location'})
        .map((dynamic event) {
          final Map<dynamic, dynamic> data = event as Map;
          return LocationData(
            latitude: data['latitude'] as double,
            longitude: data['longitude'] as double,
            accuracy: data['accuracy'] as double,
            timestamp: data['timestamp'] as int,
          );
        });
  }
}

class AccelerometerData {
  final double x;
  final double y;
  final double z;
  final int timestamp;

  AccelerometerData({
    required this.x,
    required this.y,
    required this.z,
    required this.timestamp,
  });

  @override
  String toString() => 'Accelerometer(x: $x, y: $y, z: $z, time: $timestamp)';
}

class LocationData {
  final double latitude;
  final double longitude;
  final double accuracy;
  final int timestamp;

  LocationData({
    required this.latitude,
    required this.longitude,
    required this.accuracy,
    required this.timestamp,
  });

  @override
  String toString() => 'Location($latitude, $longitude) ±${accuracy}m';
}
```

#### 2.2 Android (Kotlin) - EventChannel Implementation

```kotlin
// android/app/src/main/kotlin/com/example/myapp/channels/SensorChannel.kt
package com.example.myapp.channels

import android.content.Context
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import io.flutter.plugin.common.EventChannel

class SensorChannel(private val context: Context) : EventChannel.StreamHandler {
    private var sensorManager: SensorManager? = null
    private var accelerometer: Sensor? = null
    private var eventSink: EventChannel.EventSink? = null

    override fun onListen(arguments: Any?, events: EventChannel.EventSink?) {
        eventSink = events
        
        sensorManager = context.getSystemService(Context.SENSOR_SERVICE) as SensorManager
        accelerometer = sensorManager?.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)

        if (accelerometer != null) {
            sensorManager?.registerListener(
                sensorEventListener,
                accelerometer,
                SensorManager.SENSOR_DELAY_NORMAL
            )
        } else {
            eventSink?.error(
                "SENSOR_UNAVAILABLE",
                "Accelerometer not available",
                null
            )
        }
    }

    override fun onCancel(arguments: Any?) {
        sensorManager?.unregisterListener(sensorEventListener)
        eventSink = null
    }

    private val sensorEventListener = object : SensorEventListener {
        override fun onSensorChanged(event: SensorEvent?) {
            event?.let {
                val data = mapOf(
                    "x" to it.values[0].toDouble(),
                    "y" to it.values[1].toDouble(),
                    "z" to it.values[2].toDouble(),
                    "timestamp" to System.currentTimeMillis()
                )
                eventSink?.success(data)
            }
        }

        override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {
            // Handle accuracy changes if needed
        }
    }
}

// En MainActivity.kt, registrar el EventChannel:
// EventChannel(flutterEngine.dartExecutor.binaryMessenger, "com.example.myapp/sensor")
//     .setStreamHandler(SensorChannel(this))
```

#### 2.3 iOS (Swift) - EventChannel Implementation

```swift
// ios/Runner/Channels/SensorChannel.swift
import Flutter
import CoreMotion

class SensorChannel: NSObject, FlutterStreamHandler {
    private let motionManager = CMMotionManager()
    private var eventSink: FlutterEventSink?
    
    func onListen(withArguments arguments: Any?, eventSink events: @escaping FlutterEventSink) -> FlutterError? {
        self.eventSink = events
        
        guard motionManager.isAccelerometerAvailable else {
            events(FlutterError(
                code: "SENSOR_UNAVAILABLE",
                message: "Accelerometer not available",
                details: nil
            ))
            return nil
        }
        
        motionManager.accelerometerUpdateInterval = 0.1
        motionManager.startAccelerometerUpdates(to: .main) { [weak self] (data, error) in
            guard let data = data, let eventSink = self?.eventSink else { return }
            
            let sensorData: [String: Any] = [
                "x": data.acceleration.x,
                "y": data.acceleration.y,
                "z": data.acceleration.z,
                "timestamp": Int(Date().timeIntervalSince1970 * 1000)
            ]
            
            eventSink(sensorData)
        }
        
        return nil
    }
    
    func onCancel(withArguments arguments: Any?) -> FlutterError? {
        motionManager.stopAccelerometerUpdates()
        eventSink = nil
        return nil
    }
}

// En AppDelegate.swift:
// let sensorChannel = FlutterEventChannel(
//     name: "com.example.myapp/sensor",
//     binaryMessenger: controller.binaryMessenger
// )
// sensorChannel.setStreamHandler(SensorChannel())
```

### 3. FFI (Foreign Function Interface)

#### 3.1 Configuración FFI con C/C++

```dart
// lib/services/native_ffi.dart
import 'dart:ffi' as ffi;
import 'dart:io';

// Definir la signatura de la función nativa
typedef NativeAddFunc = ffi.Int32 Function(ffi.Int32 a, ffi.Int32 b);
typedef AddFunc = int Function(int a, int b);

typedef NativeStringFunc = ffi.Pointer<Utf8> Function(ffi.Pointer<Utf8> str);
typedef StringFunc = ffi.Pointer<Utf8> Function(ffi.Pointer<Utf8> str);

class NativeFFI {
  late final ffi.DynamicLibrary _dylib;

  NativeFFI() {
    // Cargar la librería nativa
    if (Platform.isAndroid) {
      _dylib = ffi.DynamicLibrary.open('libnative.so');
    } else if (Platform.isIOS) {
      _dylib = ffi.DynamicLibrary.process();
    } else {
      throw UnsupportedError('Platform not supported');
    }
  }

  // Función simple: suma de dos enteros
  int add(int a, int b) {
    final AddFunc nativeAdd = _dylib
        .lookup<ffi.NativeFunction<NativeAddFunc>>('native_add')
        .asFunction();
    
    return nativeAdd(a, b);
  }

  // Función con strings
  String processString(String input) {
    final StringFunc nativeProcess = _dylib
        .lookup<ffi.NativeFunction<NativeStringFunc>>('process_string')
        .asFunction();
    
    final inputPointer = input.toNativeUtf8();
    final resultPointer = nativeProcess(inputPointer);
    final result = resultPointer.toDartString();
    
    // Liberar memoria
    calloc.free(inputPointer);
    
    return result;
  }

  // Función compleja con structs
  ComputeResult compute(double value) {
    final ComputeFunc nativeCompute = _dylib
        .lookup<ffi.NativeFunction<NativeComputeFunc>>('compute')
        .asFunction();
    
    final result = nativeCompute(value);
    return ComputeResult(
      result: result.result,
      executionTime: result.executionTime,
    );
  }
}

// Struct para FFI
class ComputeResult extends ffi.Struct {
  @ffi.Double()
  external double result;
  
  @ffi.Int64()
  external int executionTime;
}

typedef NativeComputeFunc = ComputeResult Function(ffi.Double value);
typedef ComputeFunc = ComputeResult Function(double value);
```

#### 3.2 Código C Nativo

```c
// android/app/src/main/cpp/native.c
#include <jni.h>
#include <string.h>
#include <stdlib.h>

// Función simple
__attribute__((visibility("default"))) __attribute__((used))
int32_t native_add(int32_t a, int32_t b) {
    return a + b;
}

// Función con strings
__attribute__((visibility("default"))) __attribute__((used))
const char* process_string(const char* input) {
    size_t len = strlen(input);
    char* result = (char*)malloc(len + 1);
    
    // Convertir a mayúsculas
    for (size_t i = 0; i < len; i++) {
        result[i] = toupper(input[i]);
    }
    result[len] = '\0';
    
    return result;
}

// Struct result
typedef struct {
    double result;
    int64_t execution_time;
} ComputeResult;

// Función compleja
__attribute__((visibility("default"))) __attribute__((used))
ComputeResult compute(double value) {
    ComputeResult res;
    int64_t start = get_current_time_ms();
    
    // Operación costosa
    res.result = expensive_computation(value);
    
    res.execution_time = get_current_time_ms() - start;
    return res;
}
```

### 4. SDK Integration - Ejemplo Completo

#### 4.1 Flutter Service para SDK Nativo

```dart
// lib/services/native_sdk_service.dart
import 'package:flutter/services.dart';

class NativeSDKService {
  static const platform = MethodChannel('com.example.myapp/native_sdk');

  // Initialize SDK
  Future<bool> initialize(String apiKey) async {
    try {
      final bool result = await platform.invokeMethod(
        'initializeSDK',
        {'apiKey': apiKey},
      );
      return result;
    } on PlatformException catch (e) {
      print('Failed to initialize SDK: ${e.message}');
      return false;
    }
  }

  // Track event
  Future<void> trackEvent(String eventName, Map<String, dynamic> properties) async {
    try {
      await platform.invokeMethod('trackEvent', {
        'eventName': eventName,
        'properties': properties,
      });
    } on PlatformException catch (e) {
      print('Failed to track event: ${e.message}');
    }
  }

  // Get user profile
  Future<Map<String, dynamic>?> getUserProfile() async {
    try {
      final Map<dynamic, dynamic> result = 
          await platform.invokeMethod('getUserProfile');
      return result.cast<String, dynamic>();
    } on PlatformException catch (e) {
      print('Failed to get user profile: ${e.message}');
      return null;
    }
  }

  // Upload file with progress
  Stream<double> uploadFile(String filePath) async* {
    final EventChannel progressChannel = 
        EventChannel('com.example.myapp/upload_progress');
    
    // Start upload
    await platform.invokeMethod('uploadFile', {'filePath': filePath});
    
    // Listen to progress
    await for (final progress in progressChannel.receiveBroadcastStream()) {
      yield progress as double;
    }
  }
}
```

#### 4.2 Android Implementation con SDK

```kotlin
// android/app/src/main/kotlin/com/example/myapp/channels/NativeSDKChannel.kt
package com.example.myapp.channels

import android.content.Context
import io.flutter.plugin.common.MethodChannel
import io.flutter.plugin.common.EventChannel
// import com.thirdparty.sdk.SDK  // SDK externo

class NativeSDKChannel(private val context: Context) {
    private var sdk: SDK? = null
    
    fun handleMethodCall(call: MethodCall, result: MethodChannel.Result) {
        when (call.method) {
            "initializeSDK" -> {
                val apiKey = call.argument<String>("apiKey")
                if (apiKey != null) {
                    val initialized = initializeSDK(apiKey)
                    result.success(initialized)
                } else {
                    result.error("INVALID_ARGS", "API key is required", null)
                }
            }
            
            "trackEvent" -> {
                val eventName = call.argument<String>("eventName")
                val properties = call.argument<Map<String, Any>>("properties")
                
                if (eventName != null) {
                    trackEvent(eventName, properties ?: emptyMap())
                    result.success(null)
                } else {
                    result.error("INVALID_ARGS", "Event name is required", null)
                }
            }
            
            "getUserProfile" -> {
                val profile = getUserProfile()
                result.success(profile)
            }
            
            "uploadFile" -> {
                val filePath = call.argument<String>("filePath")
                if (filePath != null) {
                    uploadFileWithProgress(filePath)
                    result.success(null)
                } else {
                    result.error("INVALID_ARGS", "File path is required", null)
                }
            }
            
            else -> result.notImplemented()
        }
    }
    
    private fun initializeSDK(apiKey: String): Boolean {
        return try {
            sdk = SDK.getInstance(context)
            sdk?.initialize(apiKey)
            true
        } catch (e: Exception) {
            println("SDK initialization failed: ${e.message}")
            false
        }
    }
    
    private fun trackEvent(eventName: String, properties: Map<String, Any>) {
        sdk?.trackEvent(eventName, properties)
    }
    
    private fun getUserProfile(): Map<String, Any>? {
        return sdk?.getUserProfile()?.toMap()
    }
    
    private fun uploadFileWithProgress(filePath: String) {
        // Implementar upload con callbacks de progreso
        sdk?.uploadFile(filePath) { progress ->
            // Enviar progreso a través de EventChannel
            eventSink?.success(progress)
        }
    }
}
```

### 5. Background Tasks y Permissions

#### 5.1 Background Service

```dart
// lib/services/background_service.dart
import 'package:flutter/services.dart';

class BackgroundService {
  static const platform = MethodChannel('com.example.myapp/background');

  // Start background task
  Future<bool> startBackgroundTask() async {
    try {
      final bool result = await platform.invokeMethod('startBackgroundTask');
      return result;
    } on PlatformException catch (e) {
      print('Failed to start background task: ${e.message}');
      return false;
    }
  }

  // Stop background task
  Future<void> stopBackgroundTask() async {
    try {
      await platform.invokeMethod('stopBackgroundTask');
    } on PlatformException catch (e) {
      print('Failed to stop background task: ${e.message}');
    }
  }

  // Check if task is running
  Future<bool> isTaskRunning() async {
    try {
      final bool result = await platform.invokeMethod('isTaskRunning');
      return result;
    } on PlatformException catch (e) {
      print('Failed to check task status: ${e.message}');
      return false;
    }
  }
}
```

#### 5.2 Android Background Service

```kotlin
// android/app/src/main/kotlin/com/example/myapp/services/BackgroundService.kt
package com.example.myapp.services

import android.app.Service
import android.content.Intent
import android.os.IBinder
import androidx.core.app.NotificationCompat

class BackgroundService : Service() {
    
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // Create notification
        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Background Task")
            .setContentText("Running...")
            .setSmallIcon(R.drawable.ic_notification)
            .build()
        
        startForeground(NOTIFICATION_ID, notification)
        
        // Start background work
        performBackgroundWork()
        
        return START_STICKY
    }
    
    override fun onBind(intent: Intent?): IBinder? = null
    
    private fun performBackgroundWork() {
        Thread {
            // Long-running operation
            while (isRunning) {
                // Do work...
                Thread.sleep(1000)
            }
        }.start()
    }
    
    companion object {
        private const val CHANNEL_ID = "background_channel"
        private const val NOTIFICATION_ID = 1
        private var isRunning = false
    }
}
```

## 🎯 Mejores Prácticas

### 1. Error Handling

✅ **DO:** Maneja todos los errores posibles
```dart
try {
  final result = await platform.invokeMethod('someMethod');
  return result;
} on PlatformException catch (e) {
  print('Platform error: ${e.code} - ${e.message}');
  // Handle specific error codes
  switch (e.code) {
    case 'UNAVAILABLE':
      // Handle unavailable
      break;
    case 'PERMISSION_DENIED':
      // Handle permission denied
      break;
  }
} on MissingPluginException catch (e) {
  print('Plugin not registered: $e');
} catch (e) {
  print('Unexpected error: $e');
}
```

### 2. Type Safety

✅ **DO:** Usa tipos fuertes
```dart
// Definir constantes para method names
class BatteryChannelMethods {
  static const getBatteryLevel = 'getBatteryLevel';
  static const isCharging = 'isCharging';
}

// Usar enums para error codes
enum BatteryError {
  unavailable,
  permissionDenied,
  unknown;
  
  static BatteryError fromCode(String code) {
    switch (code) {
      case 'UNAVAILABLE':
        return BatteryError.unavailable;
      case 'PERMISSION_DENIED':
        return BatteryError.permissionDenied;
      default:
        return BatteryError.unknown;
    }
  }
}
```

### 3. Memory Management

✅ **DO:** Limpia recursos
```dart
class SensorService {
  StreamSubscription? _subscription;
  
  void startListening() {
    _subscription = sensorChannel.accelerometerStream.listen((data) {
      // Handle data
    });
  }
  
  void dispose() {
    _subscription?.cancel();
    _subscription = null;
  }
}
```

### 4. Platform-Specific Code

✅ **DO:** Usa Platform checks
```dart
import 'dart:io';

Future<String> getPlatformVersion() async {
  if (Platform.isAndroid) {
    return await platform.invokeMethod('getAndroidVersion');
  } else if (Platform.isIOS) {
    return await platform.invokeMethod('getIOSVersion');
  } else {
    throw UnsupportedError('Platform not supported');
  }
}
```

## 🧪 Testing

### Platform Channel Testing

```dart
// test/battery_channel_test.dart
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  const MethodChannel channel = MethodChannel('com.example.myapp/battery');

  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() {
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(channel, (MethodCall methodCall) async {
      switch (methodCall.method) {
        case 'getBatteryLevel':
          return 90;
        case 'isCharging':
          return true;
        default:
          throw PlatformException(code: 'UNIMPLEMENTED');
      }
    });
  });

  tearDown(() {
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(channel, null);
  });

  test('getBatteryLevel returns correct value', () async {
    final batteryChannel = BatteryChannel();
    expect(await batteryChannel.getBatteryLevel(), 90);
  });

  test('isCharging returns correct value', () async {
    final batteryChannel = BatteryChannel();
    expect(await batteryChannel.isCharging(), true);
  });
}
```

## 🚨 Troubleshooting

### Error: Method Not Implemented

```dart
// Verificar que el método está registrado en ambas plataformas
// y el nombre coincide exactamente
```

### Error: MissingPluginException

```
// Verificar que configuraste el channel en MainActivity/AppDelegate
// y llamaste a GeneratedPluginRegistrant.register()
```

### Error: EventChannel No Recibe Datos

```kotlin
// Android: Asegúrate de llamar a eventSink?.success() 
// en el hilo principal
runOnUiThread {
    eventSink?.success(data)
}
```

## 📚 Recursos Adicionales

- [Flutter Platform Channels](https://docs.flutter.dev/platform-integration/platform-channels)
- [FFI Package](https://pub.dev/packages/ffi)
- [Android JNI Documentation](https://developer.android.com/training/articles/perf-jni)
- [iOS Native Extensions](https://developer.apple.com/documentation/)

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025  
**Total líneas:** 1,200+

