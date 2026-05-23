---
name: arcore
cluster: ar-vr
description: "ARCore is Google\'s SDK for creating augmented reality experiences on Android using motion tracking and environmental und"
tags: ["ar","android","augmented-reality"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "ar core augmented reality android google sdk development"
---

# arcore

## Purpose
ARCore is Google's SDK for building augmented reality experiences on Android devices. It enables motion tracking, environmental understanding, and light estimation to overlay digital content on the real world. Use it to create AR apps that interact with the physical environment.

## When to Use
Use ARCore for Android apps requiring AR features, such as visualizing 3D models in real space, measuring distances, or gaming with environmental interactions. Apply it when targeting devices with ARCore support (e.g., Pixel phones or compatible hardware) and when you need cross-app AR functionality without custom hardware.

## Key Capabilities
- Motion tracking: Uses device's camera and sensors to track position and orientation in 3D space.
- Environmental understanding: Detects planes, points, and lighting for realistic AR overlays.
- Light estimation: Adjusts virtual objects' lighting to match real-world conditions.
- Augmented images: Recognizes predefined images for AR triggers.
- Cloud Anchors: Shares AR anchors across devices for multiplayer experiences.

## Usage Patterns
To use ARCore, integrate it into an Android project via Gradle, then initialize an AR session in your activity. Always check device compatibility first. Pattern: Add dependency in build.gradle, create an ARFragment in layout, and handle session lifecycle in code. For plane detection, set up a listener in the AR session loop. Avoid running AR sessions in background threads; use the main thread for UI updates.

## Common Commands/API
Add ARCore dependency in your app's build.gradle file:
```
dependencies {
    implementation 'com.google.ar:core:1.35.0'
}
```
Initialize an AR session in your Activity:
```
ArCoreApk.getInstance().checkAvailability(this).thenAccept(availability -> {
    if (availability.isSupported()) { startARSession(); }
});
```
Common API calls: Use `Session` for configuration, e.g., `session.configure(config)` with `Config` object for features like plane detection. CLI equivalent: Use Android Studio's Gradle wrapper, e.g., `./gradlew assembleDebug` to build with ARCore. For testing, run `adb shell dumpsys ar` to check ARCore status on device.

## Integration Notes
First, ensure your app targets API level 24+. Add the ARCore dependency as shown above. For auth, no API keys are needed, but verify Google Play Services via `$GOOGLE_PLAY_SERVICES_KEY` if using related features (set as an environment variable in your build script). Configure the AndroidManifest.xml with:
```
<uses-feature android:name="android.hardware.camera.ar" android:required="false" />
```
Handle permissions: Request CAMERA at runtime. For Unity integration, import the ARCore Unity plugin and enable it in project settings. Test on a physical device; emulators don't support ARCore.

## Error Handling
Check for common errors like device incompatibility: Use `ArCoreApk.Availability.UNAVAILABLE_DEVICE_NOT_COMPATIBLE` and prompt users to update or switch devices. For session failures, catch `com.google.ar.core.exceptions.FatalException` and restart the session. Example:
```
try {
    session.resume();
} catch (CameraNotAvailableException e) {
    Log.e("ARCore", "Camera unavailable: " + e.getMessage());
    // Retry after user grants permission
}
```
Handle plane detection timeouts by setting a timer in your AR loop, e.g., if no planes detected in 5 seconds, show a UI message. Use `session.setCameraTextureName()` carefully to avoid rendering issues; log errors with `session.getLastFatalException()`.

## Concrete Usage Examples
Example 1: Basic AR scene setup in an Android Activity.
```
public class MainActivity extends AppCompatActivity {
    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState); setContentView(R.layout.activity_main);
        ArFragment arFragment = (ArFragment) getSupportFragmentManager().findFragmentById(R.id.ar_fragment);
        arFragment.getArSceneView().getScene().addOnUpdateListener(frameTime -> { /* Handle updates */ });
    }
}
```
This creates an AR view and listens for updates to detect planes.

Example 2: Detecting and placing an object on a plane.
```
Plane detectedPlane = ...; // From ARFrame.getUpdatedTrackables()
if (detectedPlane.getType() == Plane.Type.HORIZONTAL_UPWARD_FACING) {
    Pose pose = detectedPlane.getCenterPose();
    // Place 3D model at pose.getTranslation()
}
```
Use this in your AR loop to anchor objects on detected surfaces.

## Graph Relationships
- arcore is part of the ar-vr cluster.
- arcore relates to: android (for platform integration), augmented-reality (for core functionality).
- arcore connects to: unity (via ARCore Unity plugin for cross-engine use).
