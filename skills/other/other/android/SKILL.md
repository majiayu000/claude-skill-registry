---
name: android
cluster: mobile
description: "Android root: SDK, activity/fragment lifecycle, permissions model, Material Design, Play Store"
tags: ["android","google","sdk"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "android sdk activity fragment permissions play store material"
---

# android

## Purpose
This skill equips the AI to handle core Android development tasks, including SDK setup, managing activity and fragment lifecycles, implementing the permissions model, applying Material Design principles, and preparing apps for Google Play Store distribution. It focuses on practical implementation for efficient app building.

## When to Use
Use this skill for Android app development scenarios, such as initializing projects with SDK tools, debugging lifecycle events (e.g., onPause or onDestroy), requesting runtime permissions, designing responsive UIs with Material components, or automating Play Store uploads. Apply it when working on mobile apps in the "mobile" cluster, especially for Google ecosystem integrations.

## Key Capabilities
- Set up Android SDK: Download and configure via SDK Manager with commands like `sdkmanager --list` to view packages.
- Manage activity/fragment lifecycles: Implement methods like onCreate() for activities or onViewCreated() for fragments to handle state changes.
- Handle permissions model: Use runtime checks with ContextCompat.checkSelfPermission() and request via ActivityCompat.requestPermissions().
- Apply Material Design: Integrate components like MaterialButton or BottomNavigationView from the Material library.
- Manage Play Store: Prepare app bundles and use Google Play Console API for uploads, requiring authentication with $GOOGLE_API_KEY.

## Usage Patterns
To set up a new Android project:
1. Use Android Studio or CLI: Run `gradle init --type android-library` to create a basic project.
2. Add dependencies in build.gradle: e.g., implementation 'com.android.support:appcompat-v7:28.0.0'.
For handling fragment lifecycles:
1. Extend Fragment and override onCreateView() to inflate layouts.
2. Use getActivity() in fragments to access activity context for permission requests.
When requesting permissions:
1. Check status first: If not granted, call requestPermissions() with a request code.
2. Handle results in onRequestPermissionsResult() to proceed or show errors.
For Material Design: Wrap layouts with CoordinatorLayout and add behaviors like app:layout_behavior="@string/appbar_scrolling_view_behavior".

## Common Commands/API
- CLI Commands: Use `adb devices` to list devices; `adb logcat` with flags like `-s MyApp` for filtered logs; `sdkmanager --install "build-tools;30.0.3"` to install specific SDK components.
- API Endpoints: For Play Store, use Google Play Developer API (e.g., POST to https://www.googleapis.com/androidpublisher/v3/applications/{packageName}/edits with $GOOGLE_API_KEY in headers).
- Code Snippets:
  - Activity lifecycle example:
    ```java
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
    ```
  - Permissions request:
    ```java
    if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
        ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);
    }
    ```
  - Material Design component:
    ```xml
    <com.google.android.material.button.MaterialButton
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Click Me" />
    ```
  - Fragment lifecycle:
    ```java
    @Override
    public void onViewCreated(View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        // Initialize views here
    }
    ```

## Integration Notes
Integrate Android SDK by setting environment variables: export ANDROID_HOME=/path/to/sdk and add to PATH. For Google services, include Google Play Services in build.gradle: implementation 'com.google.android.gms:play-services-auth:20.1.0' and use $GOOGLE_API_KEY for API calls (e.g., in HTTP requests: Authorization: Bearer $GOOGLE_API_KEY). When combining with other skills, ensure compatibility: For mobile cluster integrations, align with iOS skill for cross-platform configs; use JSON config files like {"apiKey": "$GOOGLE_API_KEY"} for Play Store automation scripts.

## Error Handling
Handle permission errors by checking results in onRequestPermissionsResult(): If request is denied, log with Log.e("Permission", "Denied") and prompt user via AlertDialog. For lifecycle issues (e.g., NullPointerException in onDestroy), use try-catch blocks around resource releases. Common SDK errors: If `sdkmanager` fails, verify internet connectivity or use --verbose flag for details. For Play Store API, catch HttpException for 401 errors by re-authenticating with $GOOGLE_API_KEY. Always wrap API calls in try { ... } catch (Exception e) { Log.d("Error", e.getMessage()); }.

## Concrete Usage Examples
1. **Implementing an activity with permission check:**
   Create an activity to request camera access:
   ```java
   public class CameraActivity extends AppCompatActivity {
       @Override
       protected void onCreate(Bundle savedInstanceState) {
           super.onCreate(savedInstanceState);
           setContentView(R.layout.activity_camera);
           if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
               ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CAMERA}, 100);
           }
       }
   }
   ```
   Then build and run: `./gradlew assembleDebug && adb install app/build/outputs/apk/debug/app-debug.apk`.

2. **Using Material Design for a login screen:**
   Design a fragment with Material components:
   ```xml
   <com.google.android.material.textfield.TextInputLayout
       android:layout_width="match_parent"
       android:layout_height="wrap_content">
       <com.google.android.material.textfield.TextInputEditText
           android:hint="Username" />
   </com.google.android.material.textfield.TextInputLayout>
   ```
   In the fragment: Override onCreateView() to inflate and handle user input, ensuring compatibility with activity lifecycle.

## Graph Relationships
- Related to cluster: mobile (shares mobile development concepts).
- Connected to skills: ios (for cross-platform mobile strategies), google (via shared tags like "google" for ecosystem tools).
- Links: sdk (direct overlap in Android SDK usage), permissions (common with web skills for access control).
