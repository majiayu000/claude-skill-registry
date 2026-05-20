---
name: video-audio-processing
description: Video and audio processing capabilities for Flutter applications
keywords: video, audio, media, player, recorder, camera, ffmpeg
---

# Skill 19: Video/Audio Processing

## Overview

This skill provides comprehensive video and audio processing capabilities for Flutter applications. Includes video playback, recording, audio capture, processing, and streaming.

## Features

- Video playback (local and network)
- Video recording with camera
- Audio recording and playback
- Video trimming and editing
- Audio processing and filters
- Screen recording
- Live streaming
- Format conversion

## Installation

### Dependencies

```yaml
dependencies:
  video_player: ^2.8.1
  chewie: ^1.7.1  # Better video player UI
  camera: ^0.10.5+5
  audio_session: ^0.1.18
  just_audio: ^0.9.36
  record: ^5.0.4
  ffmpeg_kit_flutter: ^6.0.3
  image_picker: ^1.0.7
  file_picker: ^6.1.1
  path_provider: ^2.1.1
```

## Video Playback

### 1. Basic Video Player

```dart
import 'package:video_player/video_player.dart';
import 'package:flutter/material.dart';

class VideoPlayerScreen extends StatefulWidget {
  final String videoUrl;

  const VideoPlayerScreen({super.key, required this.videoUrl});

  @override
  State<VideoPlayerScreen> createState() => _VideoPlayerScreenState();
}

class _VideoPlayerScreenState extends State<VideoPlayerScreen> {
  late VideoPlayerController _controller;

  @override
  void initState() {
    super.initState();
    _controller = VideoPlayerController.network(widget.videoUrl)
      ..initialize().then((_) {
        setState(() {});
        _controller.play();
      });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: _controller.value.isInitialized
            ? AspectRatio(
                aspectRatio: _controller.value.aspectRatio,
                child: VideoPlayer(_controller),
              )
            : const CircularProgressIndicator(),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          setState(() {
            _controller.value.isPlaying
                ? _controller.pause()
                : _controller.play();
          });
        },
        child: Icon(
          _controller.value.isPlaying ? Icons.pause : Icons.play_arrow,
        ),
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
```

### 2. Enhanced Player with Chewie

```dart
import 'package:chewie/chewie.dart';

class EnhancedVideoPlayer extends StatefulWidget {
  final String videoUrl;

  const EnhancedVideoPlayer({super.key, required this.videoUrl});

  @override
  State<EnhancedVideoPlayer> createState() => _EnhancedVideoPlayerState();
}

class _EnhancedVideoPlayerState extends State<EnhancedVideoPlayer> {
  VideoPlayerController? _videoController;
  ChewieController? _chewieController;

  @override
  void initState() {
    super.initState();
    _initializePlayer();
  }

  Future<void> _initializePlayer() async {
    _videoController = VideoPlayerController.network(widget.videoUrl);
    await _videoController!.initialize();

    _chewieController = ChewieController(
      videoPlayerController: _videoController!,
      autoPlay: true,
      looping: false,
      aspectRatio: _videoController!.value.aspectRatio,
      allowFullScreen: true,
      allowMuting: true,
      showControls: true,
      placeholder: Container(
        color: Colors.black,
        child: const Center(
          child: CircularProgressIndicator(),
        ),
      ),
    );

    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return _chewieController != null
        ? Chewie(controller: _chewieController!)
        : const Center(child: CircularProgressIndicator());
  }

  @override
  void dispose() {
    _videoController?.dispose();
    _chewieController?.dispose();
    super.dispose();
  }
}
```

## Video Recording

```dart
import 'package:camera/camera.dart';

class VideoRecorderScreen extends StatefulWidget {
  const VideoRecorderScreen({super.key});

  @override
  State<VideoRecorderScreen> createState() => _VideoRecorderScreenState();
}

class _VideoRecorderScreenState extends State<VideoRecorderScreen> {
  CameraController? _controller;
  bool _isRecording = false;
  String? _videoPath;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    final cameras = await availableCameras();
    if (cameras.isEmpty) return;

    _controller = CameraController(
      cameras.first,
      ResolutionPreset.high,
      enableAudio: true,
    );

    await _controller!.initialize();
    setState(() {});
  }

  Future<void> _startRecording() async {
    if (_controller == null || !_controller!.value.isInitialized) return;

    try {
      await _controller!.startVideoRecording();
      setState(() => _isRecording = true);
    } catch (e) {
      print('Error starting recording: $e');
    }
  }

  Future<void> _stopRecording() async {
    if (!_isRecording) return;

    try {
      final file = await _controller!.stopVideoRecording();
      setState(() {
        _isRecording = false;
        _videoPath = file.path;
      });
    } catch (e) {
      print('Error stopping recording: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_controller == null || !_controller!.value.isInitialized) {
      return const Center(child: CircularProgressIndicator());
    }

    return Scaffold(
      body: CameraPreview(_controller!),
      floatingActionButton: FloatingActionButton(
        onPressed: _isRecording ? _stopRecording : _startRecording,
        backgroundColor: _isRecording ? Colors.red : Colors.blue,
        child: Icon(_isRecording ? Icons.stop : Icons.videocam),
      ),
    );
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }
}
```

## Audio Recording

```dart
import 'package:record/record.dart';
import 'package:just_audio/just_audio.dart';
import 'package:path_provider/path_provider.dart';
import 'dart:io';

class AudioRecorderService {
  final AudioRecorder _audioRecorder = AudioRecorder();
  final AudioPlayer _audioPlayer = AudioPlayer();
  String? _currentRecordingPath;

  Future<void> startRecording() async {
    final hasPermission = await _audioRecorder.hasPermission();
    if (!hasPermission) {
      throw Exception('Microphone permission not granted');
    }

    final directory = await getApplicationDocumentsDirectory();
    _currentRecordingPath = '${directory.path}/recording_${DateTime.now().millisecondsSinceEpoch}.m4a';

    await _audioRecorder.start(
      const RecordConfig(),
      path: _currentRecordingPath!,
    );
  }

  Future<String?> stopRecording() async {
    await _audioRecorder.stop();
    return _currentRecordingPath;
  }

  Future<void> playRecording(String path) async {
    await _audioPlayer.setFilePath(path);
    await _audioPlayer.play();
  }

  Future<void> stopPlayback() async {
    await _audioPlayer.stop();
  }

  Stream<Amplitude> get amplitudeStream => _audioRecorder.onAmplitude;
}

class AudioRecorderWidget extends ConsumerStatefulWidget {
  const AudioRecorderWidget({super.key});

  @override
  ConsumerState<AudioRecorderWidget> createState() => _AudioRecorderWidgetState();
}

class _AudioRecorderWidgetState extends ConsumerState<AudioRecorderWidget> {
  final AudioRecorderService _service = AudioRecorderService();
  bool _isRecording = false;
  bool _isPlaying = false;
  String? _recordingPath;
  double _amplitude = 0.0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Amplitude visualization
        Container(
          height: 100,
          width: double.infinity,
          color: Colors.grey[200],
          child: CustomPaint(
            painter: AmplitudePainter(amplitude: _amplitude),
          ),
        ),
        const SizedBox(height: 20),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Record button
            FloatingActionButton(
              onPressed: _toggleRecording,
              backgroundColor: _isRecording ? Colors.red : Colors.blue,
              child: Icon(_isRecording ? Icons.stop : Icons.mic),
            ),
            const SizedBox(width: 20),
            // Play button
            if (_recordingPath != null)
              FloatingActionButton(
                onPressed: _togglePlayback,
                backgroundColor: _isPlaying ? Colors.orange : Colors.green,
                child: Icon(_isPlaying ? Icons.stop : Icons.play_arrow),
              ),
          ],
        ),
      ],
    );
  }

  Future<void> _toggleRecording() async {
    if (_isRecording) {
      final path = await _service.stopRecording();
      setState(() {
        _isRecording = false;
        _recordingPath = path;
      });
    } else {
      await _service.startRecording();
      setState(() => _isRecording = true);

      // Listen to amplitude
      _service.amplitudeStream.listen((amp) {
        setState(() => _amplitude = amp.current);
      });
    }
  }

  Future<void> _togglePlayback() async {
    if (_isPlaying) {
      await _service.stopPlayback();
      setState(() => _isPlaying = false);
    } else if (_recordingPath != null) {
      await _service.playRecording(_recordingPath!);
      setState(() => _isPlaying = true);
    }
  }
}

// Custom painter for amplitude visualization
class AmplitudePainter extends CustomPainter {
  final double amplitude;

  AmplitudePainter({required this.amplitude});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.blue
      ..strokeWidth = 2;

    final height = size.height;
    final centerY = height / 2;
    final barWidth = size.width / 50;

    for (int i = 0; i < 50; i++) {
      final barHeight = (amplitude / 100) * height * (0.5 + (i % 5) * 0.1);
      final x = i * barWidth;

      canvas.drawLine(
        Offset(x, centerY - barHeight / 2),
        Offset(x, centerY + barHeight / 2),
        paint,
      );
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
```

## Video Processing with FFmpeg

```dart
import 'package:ffmpeg_kit_flutter/ffmpeg_kit.dart';
import 'package:ffmpeg_kit_flutter/return_code.dart';

class VideoProcessingService {
  /// Trim video to specific duration
  static Future<String?> trimVideo(
    String inputPath,
    String outputPath,
    Duration start,
    Duration duration,
  ) async {
    final command =
        '-i "$inputPath" -ss ${start.inSeconds} -t ${duration.inSeconds} '
        '-c copy "$outputPath"';

    final session = await FFmpegKit.execute(command);
    final returnCode = await session.getReturnCode();

    if (ReturnCode.isSuccess(returnCode)) {
      return outputPath;
    }
    return null;
  }

  /// Compress video
  static Future<String?> compressVideo(
    String inputPath,
    String outputPath, {
    String quality = 'medium', // low, medium, high
  }) async {
    String crf = '23'; // Default medium
    if (quality == 'low') crf = '28';
    if (quality == 'high') crf = '18';

    final command =
        '-i "$inputPath" -vcodec h264 -acodec aac -crf $crf "$outputPath"';

    final session = await FFmpegKit.execute(command);
    final returnCode = await session.getReturnCode();

    return ReturnCode.isSuccess(returnCode) ? outputPath : null;
  }

  /// Extract thumbnail from video
  static Future<String?> extractThumbnail(
    String videoPath,
    String outputPath, {
    Duration position = const Duration(seconds: 1),
  }) async {
    final command =
        '-i "$videoPath" -ss ${position.inSeconds} -vframes 1 "$outputPath"';

    final session = await FFmpegKit.execute(command);
    final returnCode = await session.getReturnCode();

    return ReturnCode.isSuccess(returnCode) ? outputPath : null;
  }

  /// Get video information
  static Future<Map<String, dynamic>> getVideoInfo(String videoPath) async {
    final session = await FFmpegKit.execute('-i "$videoPath"');
    final output = await session.getOutput();
    final logs = await session.getLogs();

    // Parse duration, resolution, etc. from output
    final info = <String, dynamic>{};

    for (final log in logs) {
      final message = log.getMessage();
      if (message?.contains('Duration') == true) {
        final match = RegExp(r'Duration: (\d{2}):(\d{2}):(\d{2}\.\d{2})')
            .firstMatch(message!);
        if (match != null) {
          final hours = int.parse(match.group(1)!);
          final minutes = int.parse(match.group(2)!);
          final seconds = double.parse(match.group(3)!);
          info['duration'] = Duration(
            hours: hours,
            minutes: minutes,
            seconds: seconds.toInt(),
          );
        }
      }
    }

    return info;
  }
}
```

## Best Practices

1. **Always dispose controllers** - Prevent memory leaks
2. **Handle permissions** - Request camera and microphone permissions
3. **Compress videos** - Before uploading to server
4. **Use background processing** - For long operations
5. **Cache videos** - For better performance
6. **Monitor battery** - Video processing is battery-intensive

## Troubleshooting

### Video not playing
- Check video format is supported
- Verify URL is accessible
- Check for CORS issues with network videos

### Recording fails
- Verify camera permissions
- Check available storage
- Ensure camera is not in use by another app

### Audio not recording
- Check microphone permission
- Verify audio session is properly configured
- Check for hardware issues
