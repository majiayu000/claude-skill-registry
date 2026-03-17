---
name: android-jetpack
cluster: mobile
description: "Jetpack: Room, Navigation, WorkManager, DataStore, CameraX, Hilt injection, Paging 3"
tags: ["jetpack","room","hilt","workmanager","android"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "jetpack room hilt workmanager navigation camera datastore android paging"
---

# android-jetpack

## Purpose
This skill provides tools for integrating Android Jetpack components to build efficient, maintainable Android apps, focusing on Room for databases, Navigation for UI flows, WorkManager for background tasks, DataStore for preferences, CameraX for camera operations, Hilt for dependency injection, and Paging 3 for data loading.

## When to Use
Use this skill when building Android apps that need persistent storage (e.g., Room for SQLite), navigation between screens (e.g., Navigation Component), scheduled tasks (e.g., WorkManager), secure preferences (e.g., DataStore), camera features (e.g., CameraX), modular dependency injection (e.g., Hilt), or efficient pagination (e.g., Paging 3). Apply it in apps with complex data flows, background processing, or hardware interactions.

## Key Capabilities
- **Room**: ORM for SQLite databases; supports entities, DAOs, and migrations.
- **Navigation**: Manages fragment transactions and deep links via NavController.
- **WorkManager**: Schedules deferrable tasks with constraints like network availability.
- **DataStore**: Replaces SharedPreferences with protocol buffers for typed storage.
- **CameraX**: Abstracts camera hardware for preview, capture, and analysis.
- **Hilt**: Simplifies Dagger for dependency injection with Android-specific annotations.
- **Paging 3**: Loads data in pages for lists, integrating with LiveData or Flow.

## Usage Patterns
To use Room, add the dependency in build.gradle: `implementation 'androidx.room:room-runtime:2.5.0'`. Define an Entity: `@Entity class User(val id: Int, val name: String)`. Create a DAO: `interface UserDao { @Query("SELECT * FROM user") fun getAll(): List<User> }`. Set up the database: `Room.databaseBuilder(context, AppDatabase::class.java, "database-name").build()`.

For Navigation, add in build.gradle: `implementation 'androidx.navigation:navigation-fragment-ktx:2.5.0'`. Create a Nav Graph in XML: `<navigation xmlns:android="http://schemas.android.com/apk/res/android" ...> <fragment android:id="@+id/mainFragment" ...> <action android:id="@+id/action_to_detail" app:destination="@id/detailFragment" /> </fragment> </navigation>`. Navigate in code: `findNavController().navigate(R.id.action_to_detail)`.

Integrate Hilt by adding: `implementation 'com.google.dagger:hilt-android:2.44'`. Annotate your application: `@HiltAndroidApp class MyApp : Application()`. Inject dependencies: `@AndroidEntryPoint class MainActivity : AppCompatActivity() { @Inject lateinit var viewModel: MyViewModel }`.

For WorkManager, enqueue a task: `WorkManager.getInstance(context).enqueue(OneTimeWorkRequestBuilder<MyWorker>().build())`. Define the worker: `class MyWorker(context: Context, params: WorkerParameters) : Worker(context, params) { override fun doWork(): Result { // Perform task return Result.success() } }`.

Use DataStore for preferences: Add `implementation 'androidx.datastore:datastore-preferences:1.0.0'`. Access it: `val dataStore = applicationContext.dataStore`. Read/write: `dataStore.edit { settings -> settings[STRING_KEY] = "value" }`.

With CameraX, bind the camera: `ProcessCameraProvider.getInstance(context).use { provider -> val camera = provider.bindToLifecycle(this, cameraSelector, preview) }`. Configure preview: `val preview = Preview.Builder().build().also { it.setSurfaceProvider(viewFinder.surfaceProvider) }`.

For Paging 3, create a PagingSource: `class UserPagingSource : PagingSource<Int, User>() { override suspend fun load(params: LoadParams<Int>): LoadResult<Int, User> { // Fetch data return LoadResult.Page(data, prevKey, nextKey) } }`. Use in ViewModel: `val pager = Pager(config) { UserPagingSource() }.flow`.

## Common Commands/API
- **Room CLI**: Use `./gradlew dependencies` to verify Room integration. For migrations, run database queries via ADB: `adb shell sqlite3 /data/data/your.package/databases/yourdb "PRAGMA user_version;"`.
- **Navigation API**: Call `NavController.navigate(actionId)` for transitions. Use deep links: `<deepLink app:uri="yourapp://details/{id}" />` in Nav Graph.
- **WorkManager API**: Enqueue with constraints: `OneTimeWorkRequestBuilder<MyWorker>().setConstraints(Constraints.Builder().setRequiredNetworkType(NetworkType.CONNECTED).build()).build()`. Query status: `WorkManager.getInstance().getWorkInfosForUniqueWork("workName").observe(...)`.
- **DataStore API**: Read preferences: `dataStore.data.map { preferences -> preferences[STRING_KEY] }`. Handle flows: Use `collect { value -> /* process */ }`.
- **CameraX API**: Capture image: `imageCapture.takePicture(outputFileOptions, executor, object : ImageCapture.OnImageSavedCallback { override fun onImageSaved(output: ImageCapture.OutputFileResults) { // Handle saved file } })`.
- **Hilt API**: Generate code with `./gradlew hiltGenerateSources`. Inject modules: `@Module @InstallIn(SingletonComponent::class) class AppModule { @Provides fun provideService(): Service = Service() }`.
- **Paging 3 API**: Combine with RemoteMediator for network + DB: `Pager( config = PagingConfig(pageSize = 20), remoteMediator = UserRemoteMediator(), pagingSourceFactory = { UserPagingSource() } )`.

## Integration Notes
Integrate Room with Hilt by annotating the database: `@Database(entities = [User::class], version = 1) @HiltDatabase abstract class AppDatabase : RoomDatabase() { abstract fun userDao(): UserDao }`. For WorkManager and Navigation, observe work status in a fragment: `WorkManager.getInstance().getWorkInfoByIdLiveData(workId).observe(viewLifecycleOwner) { info -> if (info.state == WorkInfo.State.SUCCEEDED) navigateToResult() }`. Use DataStore with Paging: Store pagination keys in DataStore and retrieve via flows. For CameraX, ensure permissions: Check with `ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED`. If API keys are needed (e.g., for external services in WorkManager), use env vars like `$GOOGLE_API_KEY` in build.gradle or strings.xml. Combine Paging with Room: Use Room as the data source in PagingSource.

## Error Handling
For Room, catch SQLite exceptions: `try { dao.insert(user) } catch (e: SQLiteConstraintException) { Log.e("RoomError", e.message ?: "Constraint violation") }`. Handle Navigation errors: Use `NavController.addOnDestinationChangedListener` to catch invalid actions. For WorkManager, check `Result.retry()` in doWork: `if (error) return Result.retry()`. DataStore errors: Wrap reads in try-catch for IOException. CameraX: Handle `CameraX.bindToLifecycle` failures with `try { provider.unbindAll() } catch (e: IllegalStateException) { Log.e("CameraError", "Binding failed") }`. Hilt: Resolve injection errors by checking `@Inject` annotations and running `./gradlew clean`. Paging 3: Catch LoadState errors: `pager.loadStateFlow.collect { state -> if (state.refresh is LoadState.Error) Log.e("PagingError", state.refresh.error.message ?: "Load failed") }`.

## Concrete Usage Examples
1. **Example: User app with Room and Hilt**: In a ViewModel, inject Room DAO: `@HiltViewModel class UserViewModel @Inject constructor(private val userDao: UserDao) : ViewModel() { fun getUsers() = userDao.getAll() }`. In Activity: Use Hilt to inject and display: `viewModel.getUsers().observe(this) { users -> adapter.submitList(users) }`.
2. **Example: Background sync with WorkManager and DataStore**: Enqueue a worker to fetch data and store in DataStore: `WorkManager.enqueue(OneTimeWorkRequestBuilder<SyncWorker>().build())`. In worker: `dataStore.edit { it[LAST_SYNC_KEY] = System.currentTimeMillis() }`. Then, in UI, read from DataStore to check last sync.

## Graph Relationships
- Room depends on: Android core (for SQLite) and Hilt (for injection).
- Navigation integrates with: WorkManager (for async nav) and Paging 3 (for list navigation).
- WorkManager relates to: DataStore (for storing results) and CameraX (for background processing).
- DataStore connects to: Room (as an alternative storage) and Hilt (for injected access).
- CameraX links to: Navigation (for camera UI flow).
- Hilt provides injection for: All other components (Room, WorkManager, etc.).
- Paging 3 works with: Room (as data source) and Navigation (for infinite lists).
