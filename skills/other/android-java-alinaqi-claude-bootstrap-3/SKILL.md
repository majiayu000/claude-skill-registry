---
name: android-java
description: Android Java development with MVVM, ViewBinding, and Espresso testing
---

# Android Java Skill

*Load with: base.md*

---

## Project Structure

```
project/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/example/app/
│   │   │   │   ├── data/           # Data layer
│   │   │   │   │   ├── local/      # Room database, SharedPreferences
│   │   │   │   │   ├── remote/     # Retrofit services, API clients
│   │   │   │   │   └── repository/ # Repository implementations
│   │   │   │   ├── di/             # Dependency injection (Hilt/Dagger)
│   │   │   │   ├── domain/         # Business logic
│   │   │   │   │   ├── model/      # Domain models
│   │   │   │   │   ├── repository/ # Repository interfaces
│   │   │   │   │   └── usecase/    # Use cases
│   │   │   │   ├── ui/             # Presentation layer
│   │   │   │   │   ├── feature/    # Feature screens
│   │   │   │   │   │   ├── FeatureActivity.java
│   │   │   │   │   │   ├── FeatureFragment.java
│   │   │   │   │   │   └── FeatureViewModel.java
│   │   │   │   │   └── common/     # Shared UI components
│   │   │   │   └── App.java        # Application class
│   │   │   ├── res/
│   │   │   │   ├── layout/
│   │   │   │   ├── values/
│   │   │   │   └── drawable/
│   │   │   └── AndroidManifest.xml
│   │   ├── test/                   # Unit tests
│   │   └── androidTest/            # Instrumentation tests
│   └── build.gradle
├── build.gradle                    # Project-level build file
├── gradle.properties
├── settings.gradle
└── CLAUDE.md
```

---

## Gradle Configuration

### App-level build.gradle
```groovy
plugins {
    id 'com.android.application'
}

android {
    namespace 'com.example.app'
    compileSdk 34

    defaultConfig {
        applicationId "com.example.app"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }

    buildFeatures {
        viewBinding true
    }
}

dependencies {
    // AndroidX
    implementation 'androidx.core:core:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'

    // Lifecycle
    implementation 'androidx.lifecycle:lifecycle-viewmodel:2.7.0'
    implementation 'androidx.lifecycle:lifecycle-livedata:2.7.0'

    // Testing
    testImplementation 'junit:junit:4.13.2'
    testImplementation 'org.mockito:mockito-core:5.8.0'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
```

---

## Architecture Patterns

### MVVM with ViewModel
```java
// ViewModel - holds UI state, survives configuration changes
public class UserViewModel extends ViewModel {
    private final UserRepository repository;
    private final MutableLiveData<User> user = new MutableLiveData<>();
    private final MutableLiveData<Boolean> loading = new MutableLiveData<>(false);
    private final MutableLiveData<String> error = new MutableLiveData<>();

    public UserViewModel(UserRepository repository) {
        this.repository = repository;
    }

    public LiveData<User> getUser() {
        return user;
    }

    public LiveData<Boolean> isLoading() {
        return loading;
    }

    public LiveData<String> getError() {
        return error;
    }

    public void loadUser(String userId) {
        loading.setValue(true);
        repository.getUser(userId, new Callback<User>() {
            @Override
            public void onSuccess(User result) {
                user.setValue(result);
                loading.setValue(false);
            }

            @Override
            public void onError(String message) {
                error.setValue(message);
                loading.setValue(false);
            }
        });
    }
}
```

### Repository Pattern
```java
// Repository interface (domain layer)
public interface UserRepository {
    void getUser(String userId, Callback<User> callback);
    void saveUser(User user, Callback<Void> callback);
}

// Repository implementation (data layer)
public class UserRepositoryImpl implements UserRepository {
    private final UserApi api;
    private final UserDao dao;

    public UserRepositoryImpl(UserApi api, UserDao dao) {
        this.api = api;
        this.dao = dao;
    }

    @Override
    public void getUser(String userId, Callback<User> callback) {
        // Try cache first, then network
        User cached = dao.getUserById(userId);
        if (cached != null) {
            callback.onSuccess(cached);
            return;
        }
        api.getUser(userId).enqueue(new retrofit2.Callback<User>() {
            @Override
            public void onResponse(Call<User> call, Response<User> response) {
                if (response.isSuccessful() && response.body() != null) {
                    dao.insert(response.body());
                    callback.onSuccess(response.body());
                } else {
                    callback.onError("Failed to load user");
                }
            }

            @Override
            public void onFailure(Call<User> call, Throwable t) {
                callback.onError(t.getMessage());
            }
        });
    }
}
```

---

## Activity & Fragment Patterns

### Activity with ViewBinding
```java
public class MainActivity extends AppCompatActivity {
    private ActivityMainBinding binding;
    private MainViewModel viewModel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        viewModel = new ViewModelProvider(this).get(MainViewModel.class);
        setupObservers();
        setupListeners();
    }

    private void setupObservers() {
        viewModel.getUser().observe(this, user -> {
            binding.userName.setText(user.getName());
        });

        viewModel.isLoading().observe(this, isLoading -> {
            binding.progressBar.setVisibility(isLoading ? View.VISIBLE : View.GONE);
        });
    }

    private void setupListeners() {
        binding.refreshButton.setOnClickListener(v -> {
            viewModel.loadUser(getCurrentUserId());
        });
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        binding = null;
    }
}
```

### Fragment with ViewBinding
```java
public class UserFragment extends Fragment {
    private FragmentUserBinding binding;
    private UserViewModel viewModel;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        binding = FragmentUserBinding.inflate(inflater, container, false);
        return binding.getRoot();
    }

    @Override
    public void onViewCreated(View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        viewModel = new ViewModelProvider(requireActivity()).get(UserViewModel.class);
        setupObservers();
    }

    private void setupObservers() {
        viewModel.getUser().observe(getViewLifecycleOwner(), user -> {
            binding.userName.setText(user.getName());
        });
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;  // Prevent memory leaks
    }
}
```

---

## Testing

### Unit Tests with JUnit & Mockito
```java
@RunWith(MockitoJUnitRunner.class)
public class UserViewModelTest {
    @Mock
    private UserRepository repository;

    @Rule
    public InstantTaskExecutorRule instantTaskExecutorRule = new InstantTaskExecutorRule();

    private UserViewModel viewModel;

    @Before
    public void setup() {
        viewModel = new UserViewModel(repository);
    }

    @Test
    public void loadUser_success_updatesUserLiveData() {
        // Arrange
        User expectedUser = new User("1", "John Doe");
        doAnswer(invocation -> {
            Callback<User> callback = invocation.getArgument(1);
            callback.onSuccess(expectedUser);
            return null;
        }).when(repository).getUser(eq("1"), any());

        // Act
        viewModel.loadUser("1");

        // Assert
        assertEquals(expectedUser, viewModel.getUser().getValue());
        assertFalse(viewModel.isLoading().getValue());
    }

    @Test
    public void loadUser_error_updatesErrorLiveData() {
        // Arrange
        doAnswer(invocation -> {
            Callback<User> callback = invocation.getArgument(1);
            callback.onError("Network error");
            return null;
        }).when(repository).getUser(eq("1"), any());

        // Act
        viewModel.loadUser("1");

        // Assert
        assertEquals("Network error", viewModel.getError().getValue());
        assertFalse(viewModel.isLoading().getValue());
    }
}
```

### Instrumentation Tests with Espresso
```java
@RunWith(AndroidJUnit4.class)
public class MainActivityTest {
    @Rule
    public ActivityScenarioRule<MainActivity> activityRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Test
    public void userName_isDisplayed() {
        onView(withId(R.id.userName))
                .check(matches(isDisplayed()));
    }

    @Test
    public void refreshButton_click_triggersRefresh() {
        onView(withId(R.id.refreshButton))
                .perform(click());

        onView(withId(R.id.progressBar))
                .check(matches(isDisplayed()));
    }

    @Test
    public void userList_scrollToItem_displaysCorrectly() {
        onView(withId(R.id.userList))
                .perform(RecyclerViewActions.scrollToPosition(10));

        onView(withText("User 10"))
                .check(matches(isDisplayed()));
    }
}
```

---

## GitHub Actions

```yaml
name: Android CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3

      - name: Grant execute permission for gradlew
        run: chmod +x gradlew

      - name: Run Lint
        run: ./gradlew lint

      - name: Run Unit Tests
        run: ./gradlew testDebugUnitTest

      - name: Build Debug APK
        run: ./gradlew assembleDebug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: debug-apk
          path: app/build/outputs/apk/debug/app-debug.apk

  instrumentation-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Enable KVM
        run: |
          echo 'KERNEL=="kvm", GROUP="kvm", MODE="0666", OPTIONS+="static_node=kvm"' | sudo tee /etc/udev/rules.d/99-kvm4all.rules
          sudo udevadm control --reload-rules
          sudo udevadm trigger --name-match=kvm

      - name: Run Instrumentation Tests
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 29
          script: ./gradlew connectedDebugAndroidTest
```

---

## Lint Configuration

### lint.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<lint>
    <!-- Treat these as errors -->
    <issue id="HardcodedText" severity="error" />
    <issue id="MissingTranslation" severity="error" />
    <issue id="UnusedResources" severity="warning" />

    <!-- Memory leak detection -->
    <issue id="StaticFieldLeak" severity="error" />

    <!-- Security -->
    <issue id="HardcodedDebugMode" severity="error" />
    <issue id="AllowBackup" severity="warning" />

    <!-- Performance -->
    <issue id="ViewHolder" severity="error" />
    <issue id="Overdraw" severity="warning" />

    <!-- Ignore for tests -->
    <issue id="InvalidPackage">
        <ignore path="**/test/**" />
        <ignore path="**/androidTest/**" />
    </issue>
</lint>
```

### build.gradle lint options
```groovy
android {
    lint {
        abortOnError true
        warningsAsErrors false
        checkReleaseBuilds true
        xmlReport true
        htmlReport true
    }
}
```

---

## Common Patterns

### Null-Safe Callbacks
```java
// Define callback interface
public interface Callback<T> {
    void onSuccess(T result);
    void onError(String message);
}

// Use with null checks
public void fetchData(Callback<Data> callback) {
    if (callback == null) return;

    try {
        Data result = performFetch();
        callback.onSuccess(result);
    } catch (Exception e) {
        callback.onError(e.getMessage());
    }
}
```

### Safe Context Usage
```java
// Use application context for long-lived objects
public class DataManager {
    private final Context appContext;

    public DataManager(Context context) {
        // Always use application context to prevent Activity leaks
        this.appContext = context.getApplicationContext();
    }
}

// Check for null context in callbacks
private void updateUI() {
    Context context = getContext();
    if (context == null || !isAdded()) return;
    // Safe to use context
}
```

### Thread-Safe Singleton
```java
public class ApiClient {
    private static volatile ApiClient instance;
    private final Retrofit retrofit;

    private ApiClient() {
        retrofit = new Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build();
    }

    public static ApiClient getInstance() {
        if (instance == null) {
            synchronized (ApiClient.class) {
                if (instance == null) {
                    instance = new ApiClient();
                }
            }
        }
        return instance;
    }
}
```

---

## Android Anti-Patterns

- ❌ **Context leaks** - Never hold Activity/Fragment references in static fields or singletons
- ❌ **Memory leaks in callbacks** - Always use WeakReference or clear callbacks in onDestroy
- ❌ **UI updates on background thread** - Always post to main thread for UI changes
- ❌ **Hardcoded strings** - Use string resources for all user-visible text
- ❌ **God Activities** - Keep Activities under 200 lines, extract logic to ViewModels
- ❌ **NetworkOnMainThreadException** - Never perform network calls on main thread
- ❌ **Ignoring lifecycle** - Always respect Activity/Fragment lifecycle states
- ❌ **Blocking the main thread** - Keep main thread operations under 16ms
- ❌ **Not handling configuration changes** - Use ViewModel to survive rotation
- ❌ **Hardcoded dimensions** - Use dp/sp units and dimension resources
- ❌ **Deep view hierarchies** - Keep layout depth under 10 levels, use ConstraintLayout
- ❌ **Not closing resources** - Always close Cursor, InputStream, database connections

