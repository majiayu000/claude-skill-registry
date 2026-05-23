---
name: machine-learning
description: Machine Learning integration for Flutter using TensorFlow Lite and Firebase ML
keywords: ml, machine-learning, ai, tflite, tensorflow, firebase-ml, image-classification
---

# Skill 20: Machine Learning Integration

## Overview

This skill enables machine learning capabilities in Flutter applications using TensorFlow Lite and Firebase ML Kit. Supports image classification, object detection, text recognition, and custom model deployment.

## Features

- Image classification with pre-trained models
- Object detection and tracking
- Text recognition (OCR)
- Face detection
- Barcode scanning
- Custom TFLite model integration
- On-device inference
- Cloud-based ML with Firebase

## Installation

### Dependencies

```yaml
dependencies:
  tflite_flutter: ^0.10.4
  tflite_flutter_helper: ^0.3.1
  firebase_ml_model_downloader: ^0.2.4
  google_mlkit_text_recognition: ^0.11.0
  google_mlkit_face_detection: ^0.9.0
  google_mlkit_barcode_scanning: ^0.10.0
  google_mlkit_object_detection: ^0.11.0
  image_picker: ^1.0.7
  image: ^4.1.3
```

## Image Classification

### 1. Model Setup

Add your TensorFlow Lite model to `assets/models/`:

```yaml
# pubspec.yaml
flutter:
  assets:
    - assets/models/model.tflite
    - assets/labels/labels.txt
```

### 2. Image Classification Service

```dart
import 'package:tflite_flutter/tflite_flutter.dart';
import 'package:image/image.dart' as img;
import 'dart:io';

class ImageClassifier {
  Interpreter? _interpreter;
  List<String>? _labels;

  Future<void> loadModel() async {
    try {
      _interpreter = await Interpreter.fromAsset('assets/models/model.tflite');

      // Load labels
      final labelData = await rootBundle.loadString('assets/labels/labels.txt');
      _labels = labelData.split('\n');
    } catch (e) {
      print('Error loading model: $e');
    }
  }

  Future<Map<String, double>> classifyImage(File imageFile) async {
    if (_interpreter == null) {
      throw Exception('Model not loaded');
    }

    // Load and preprocess image
    final imageData = await imageFile.readAsBytes();
    var image = img.decodeImage(imageData)!;

    // Resize to model input size (e.g., 224x224)
    image = img.copyResize(image, width: 224, height: 224);

    // Convert to input format
    final input = _imageToInputList(image);

    // Run inference
    final output = List.filled(1 * _labels!.length, 0).reshape([1, _labels!.length]);
    _interpreter!.run(input, output);

    // Process results
    final results = <String, double>{};
    for (int i = 0; i < _labels!.length; i++) {
      results[_labels![i]] = output[0][i];
    }

    return results;
  }

  List<List<List<List<double>>>> _imageToInputList(img.Image image) {
    final input = List.generate(
      1,
      (_) => List.generate(
        224,
        (y) => List.generate(
          224,
          (x) {
            final pixel = image.getPixel(x, y);
            return [
              pixel.r / 255.0,
              pixel.g / 255.0,
              pixel.b / 255.0,
            ];
          },
        ),
      ),
    );
    return input;
  }

  void dispose() {
    _interpreter?.close();
  }
}
```

### 3. Classification UI

```dart
class ImageClassificationPage extends ConsumerStatefulWidget {
  const ImageClassificationPage({super.key});

  @override
  ConsumerState<ImageClassificationPage> createState() => _ImageClassificationPageState();
}

class _ImageClassificationPageState extends ConsumerState<ImageClassificationPage> {
  final ImageClassifier _classifier = ImageClassifier();
  File? _selectedImage;
  Map<String, double>? _results;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _classifier.loadModel();
  }

  Future<void> _pickImage() async {
    final picker = ImagePicker();
    final picked = await picker.pickImage(source: ImageSource.gallery);

    if (picked != null) {
      setState(() {
        _selectedImage = File(picked.path);
        _isLoading = true;
      });

      final results = await _classifier.classifyImage(_selectedImage!);

      setState(() {
        _results = results;
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Image Classification')),
      body: Column(
        children: [
          if (_selectedImage != null)
            Image.file(_selectedImage!, height: 300),
          const SizedBox(height: 20),
          if (_isLoading)
            const CircularProgressIndicator()
          else if (_results != null)
            Expanded(
              child: ListView.builder(
                itemCount: _results!.length,
                itemBuilder: (context, index) {
                  final label = _results!.keys.elementAt(index);
                  final confidence = _results![label]!;

                  return ListTile(
                    title: Text(label),
                    trailing: Text('${(confidence * 100).toStringAsFixed(1)}%'),
                    subtitle: LinearProgressIndicator(
                      value: confidence,
                    ),
                  );
                },
              ),
            ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _pickImage,
        child: const Icon(Icons.image),
      ),
    );
  }

  @override
  void dispose() {
    _classifier.dispose();
    super.dispose();
  }
}
```

## Text Recognition (OCR)

```dart
import 'package:google_mlkit_text_recognition/google_mlkit_text_recognition.dart';

class TextRecognitionService {
  final TextRecognizer _textRecognizer = TextRecognizer();

  Future<String> recognizeText(File imageFile) async {
    final inputImage = InputImage.fromFile(imageFile);
    final recognizedText = await _textRecognizer.processImage(inputImage);

    return recognizedText.text;
  }

  Future<List<TextBlock>> recognizeTextBlocks(File imageFile) async {
    final inputImage = InputImage.fromFile(imageFile);
    final recognizedText = await _textRecognizer.processImage(inputImage);

    return recognizedText.blocks;
  }

  void dispose() {
    _textRecognizer.close();
  }
}

class OCRWidget extends StatefulWidget {
  const OCRWidget({super.key});

  @override
  State<OCRWidget> createState() => _OCRWidgetState();
}

class _OCRWidgetState extends State<OCRWidget> {
  final TextRecognitionService _service = TextRecognitionService();
  File? _image;
  String _recognizedText = '';

  Future<void> _scanText() async {
    final picker = ImagePicker();
    final picked = await picker.pickImage(source: ImageSource.camera);

    if (picked != null) {
      setState(() => _image = File(picked.path));

      final text = await _service.recognizeText(_image!);
      setState(() => _recognizedText = text);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            if (_image != null)
              Image.file(_image!, height: 200),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _scanText,
              child: const Text('Scan Text'),
            ),
            const SizedBox(height: 20),
            Text(
              'Recognized Text:',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 10),
            Text(_recognizedText),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _service.dispose();
    super.dispose();
  }
}
```

## Object Detection

```dart
import 'package:google_mlkit_object_detection/google_mlkit_object_detection.dart';

class ObjectDetectionService {
  late ObjectDetector _objectDetector;

  void initialize() {
    final options = ObjectDetectorOptions(
      mode: DetectionMode.single,
      classifyObjects: true,
      trackMultipleObjects: true,
    );
    _objectDetector = ObjectDetector(options: options);
  }

  Future<List<DetectedObject>> detectObjects(File imageFile) async {
    final inputImage = InputImage.fromFile(imageFile);
    return await _objectDetector.processImage(inputImage);
  }

  void dispose() {
    _objectDetector.close();
  }
}

class ObjectDetectionPainter extends CustomPainter {
  final List<DetectedObject> objects;
  final Size imageSize;

  ObjectDetectionPainter({required this.objects, required this.imageSize});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3.0
      ..color = Colors.green;

    final textPainter = TextPainter(
      textDirection: TextDirection.ltr,
    );

    for (final object in objects) {
      final rect = _scaleRect(object.boundingBox, imageSize, size);
      canvas.drawRect(rect, paint);

      // Draw label
      if (object.labels.isNotEmpty) {
        final label = object.labels.first;
        textPainter.text = TextSpan(
          text: '${label.text} ${(label.confidence * 100).toStringAsFixed(0)}%',
          style: const TextStyle(
            color: Colors.green,
            fontSize: 16,
            fontWeight: FontWeight.bold,
            backgroundColor: Colors.white,
          ),
        );
        textPainter.layout();
        textPainter.paint(canvas, Offset(rect.left, rect.top - 20));
      }
    }
  }

  Rect _scaleRect(Rect rect, Size imageSize, Size canvasSize) {
    final scaleX = canvasSize.width / imageSize.width;
    final scaleY = canvasSize.height / imageSize.height;

    return Rect.fromLTRB(
      rect.left * scaleX,
      rect.top * scaleY,
      rect.right * scaleX,
      rect.bottom * scaleY,
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
```

## Barcode Scanning

```dart
import 'package:google_mlkit_barcode_scanning/google_mlkit_barcode_scanning.dart';

class BarcodeScannerService {
  final BarcodeScanner _scanner = BarcodeScanner();

  Future<List<Barcode>> scanBarcodes(File imageFile) async {
    final inputImage = InputImage.fromFile(imageFile);
    return await _scanner.processImage(inputImage);
  }

  void dispose() {
    _scanner.close();
  }
}

// Real-time barcode scanning with camera
class BarcodeScannerPage extends StatefulWidget {
  const BarcodeScannerPage({super.key});

  @override
  State<BarcodeScannerPage> createState() => _BarcodeScannerPageState();
}

class _BarcodeScannerPageState extends State<BarcodeScannerPage> {
  CameraController? _cameraController;
  final BarcodeScanner _scanner = BarcodeScanner();
  bool _isProcessing = false;
  String? _scannedBarcode;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    final cameras = await availableCameras();
    _cameraController = CameraController(
      cameras.first,
      ResolutionPreset.medium,
      enableAudio: false,
    );

    await _cameraController!.initialize();
    await _cameraController!.startImageStream(_processCameraImage);

    setState(() {});
  }

  Future<void> _processCameraImage(CameraImage image) async {
    if (_isProcessing) return;
    _isProcessing = true;

    try {
      final WriteBuffer allBytes = WriteBuffer();
      for (final Plane plane in image.planes) {
        allBytes.putUint8List(plane.bytes);
      }
      final bytes = allBytes.done().buffer.asUint8List();

      final imageSize = Size(image.width.toDouble(), image.height.toDouble());

      final inputImage = InputImage.fromBytes(
        bytes: bytes,
        metadata: InputImageMetadata(
          size: imageSize,
          rotation: InputImageRotation.rotation0,
          format: InputImageFormat.nv21,
          bytesPerRow: image.planes.first.bytesPerRow,
        ),
      );

      final barcodes = await _scanner.processImage(inputImage);

      if (barcodes.isNotEmpty) {
        setState(() {
          _scannedBarcode = barcodes.first.rawValue;
        });
      }
    } finally {
      _isProcessing = false;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Scan Barcode')),
      body: Stack(
        children: [
          if (_cameraController != null)
            CameraPreview(_cameraController!),
          if (_scannedBarcode != null)
            Center(
              child: Container(
                padding: const EdgeInsets.all(16),
                color: Colors.black54,
                child: Text(
                  'Scanned: $_scannedBarcode',
                  style: const TextStyle(color: Colors.white, fontSize: 20),
                ),
              ),
            ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _cameraController?.dispose();
    _scanner.close();
    super.dispose();
  }
}
```

## Firebase ML Model Download

```dart
import 'package:firebase_ml_model_downloader/firebase_ml_model_downloader.dart';

class FirebaseMLService {
  Future<void> downloadModel(String modelName) async {
    final model = await FirebaseModelDownloader.instance.getModel(
      modelName,
      FirebaseModelDownloadType.localModel,
      FirebaseModelDownloadConditions(
        iosAllowsCellularAccess: true,
        iosAllowsBackgroundDownloading: false,
        androidChargingRequired: false,
        androidWifiRequired: false,
        androidDeviceIdleRequired: false,
      ),
    );

    print('Model downloaded to: ${model.file}');
  }
}
```

## Best Practices

1. **Load models asynchronously** - Don't block UI thread
2. **Dispose properly** - Release model resources
3. **Use quantized models** - Smaller, faster inference
4. **Cache results** - Avoid re-processing same images
5. **Handle low confidence** - Filter results below threshold
6. **Test on real devices** - Simulators may not support ML

## Performance Optimization

```dart
class OptimizedMLService {
  Interpreter? _interpreter;
  bool _isModelLoaded = false;

  Future<void> loadModel() async {
    if (_isModelLoaded) return;

    final options = InterpreterOptions()
      ..threads = 4  // Use multiple threads
      ..useNnApiForAndroid = true;  // Use NNAPI acceleration

    _interpreter = await Interpreter.fromAsset(
      'model.tflite',
      options: options,
    );

    _isModelLoaded = true;
  }

  // Process multiple images in batch
  Future<List<dynamic>> batchInference(List<File> images) async {
    final results = <dynamic>[];

    for (final image in images) {
      final result = await _singleInference(image);
      results.add(result);
    }

    return results;
  }

  Future<dynamic> _singleInference(File image) async {
    // Preprocess and run inference
    // ...
  }
}
```

## Troubleshooting

### Model not loading
- Check model format is valid TFLite
- Verify model path is correct
- Ensure model is included in pubspec.yaml

### Out of memory
- Use smaller input sizes
- Load model on-demand, not at startup
- Dispose models when not needed

### Slow inference
- Use quantized models (INT8)
- Enable NNAPI/GPU delegates
- Reduce image resolution
