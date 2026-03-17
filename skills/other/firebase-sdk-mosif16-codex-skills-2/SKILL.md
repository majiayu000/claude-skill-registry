 ---
    name: "Firebase Swift & TypeScript SDK Best Practices"
    description: "Guidelines and best practices for integrating and using the Google Firebase SDK in Swift (for Apple platforms) and TypeScript (for web/Node), covering setup, architecture, data handling, security, and usage across supported services and platforms."
    version: "1.0"
    dependencies:
      - "Firebase Apple SDK (Swift) – installed via Swift Package Manager (iOS 15+/macOS 10.15+)"
      - "Firebase Web SDK (TypeScript) – v9+ installed via npm (with module bundler)"
    ---
    # Instructions

    **Overview:** This guide outlines best practices for using Firebase on Apple platforms with Swift and on web/Node platforms with TypeScript. It covers how to set up the SDKs, organize code, handle data efficiently, and ensure security across all supported Firebase services and platforms.

    ## Setup and Initialization  
    - **Use official SDK integration methods:** Integrate Firebase using the recommended tools for each platform. On iOS (and other Apple platforms), use **Swift Package Manager** (or CocoaPods) to add the Firebase Apple SDK to your Xcode project. On web/Node, install the **Firebase JS SDK** via **npm** (e.g. `npm install firebase`) to use the modular API. Using these official methods ensures you get the correct libraries and easier updates.  
    - **Initialize Firebase only once:** Properly initialize Firebase early in your app’s lifecycle. In a Swift app, call `FirebaseApp.configure()` in your application’s startup (e.g. in `AppDelegate.application(_:didFinishLaunchingWithOptions:)` or the SwiftUI App struct initializer) to initialize the default Firebase app instance. In a TypeScript web app, call `initializeApp(firebaseConfig)` with your configuration object exactly once (typically at the entry point of your application). Avoid initializing multiple times or in library code – reuse the initialized app instance by passing it to Firebase services (e.g. `getFirestore(app)`, `getAuth(app)`) rather than calling a new initialize each time. This prevents duplicate app instances and errors.  
    - **Target supported platforms:** Ensure your development environment meets Firebase’s platform requirements. For Apple apps, use supported OS versions (e.g. iOS 15+ for recent Firebase SDKs, with official support for iOS, macOS, Mac Catalyst, and beta support for tvOS; watchOS has community support only). For web/TypeScript, modern browsers are supported, and Node.js can be used for server-side or Cloud Functions. Understanding supported platforms will help avoid using features not available on a given system (for example, Crashlytics is available on mobile but not on web, and certain Apple-specific features like Push Notifications require iOS devices).  
    - **Keep config files and keys safe:** Add the Firebase config files to your app correctly. In iOS/Swift, include the `GoogleService-Info.plist` file in the Xcode project (this contains your app’s Firebase project IDs and API keys). In web/TypeScript, use the Firebase project config object (apiKey, authDomain, etc.) to initialize – do not expose any truly sensitive credentials in client code. Firebase API keys are not secret, but restrict their usage to your app’s domains and bundle IDs in the Firebase console. Treat service account keys (used on servers) as sensitive and never embed those in client apps.  
    - **Separate environments and projects:** A best practice is to use separate Firebase projects for different app environments (development, staging, production). For example, have your app configured to use a “dev” Firebase project when debugging, and a “prod” project for the App Store or live site. This isolation prevents test data or changes from affecting production. In your Swift app, you can include multiple GoogleService-Info.plist files (one per environment) and select the appropriate one at build time (using Xcode schemes or build configurations). In TypeScript/web, use environment variables or config files to switch the Firebase config object based on environment. Keeping environments separate also means you can tailor security rules and database content appropriately for testing vs. production.

    ## Code Organization and Architecture  
    - **Separate Firebase logic from UI:** Organize your code so that Firebase calls (database reads/writes, auth requests, etc.) are not deeply intertwined with view/UI code. In Swift, consider using an architecture pattern like **MVVM (Model-View-ViewModel)** or similar. For example, create service classes or view models that handle Firebase interactions (such as fetching data from Firestore or updating user authentication) and then provide that data to your `UIViewController` or SwiftUI `View`. This separation makes your code more maintainable and testable. In a SwiftUI app, you might use an `ObservableObject` ViewModel that uses Firebase APIs and publishes model updates to the views. In TypeScript (e.g. a React or Node app), similarly abstract Firebase calls into utility modules or context providers. For instance, you can have a `firebaseService.ts` that exports functions for common operations (like `fetchPosts()` or `subscribeToOrders()`) instead of peppering `firebase.firestore()` calls throughout UI components. This improves readability and allows easier changes (or even swapping out the backend) down the line.  
    - **Use the Firebase modular SDK (web):** When using Firebase with TypeScript on the web, prefer the **v9+ modular API**. Instead of importing the entire Firebase namespace, import only the functions you need (e.g. `import { getAuth, signInWithEmailAndPassword } from "firebase/auth";`). The modular SDK is tree-shakeable, meaning your bundler can remove unused code and reduce your app’s bundle size. This leads to better performance for users. Avoid using older namespaced imports like `firebase.auth()` or `firebase.database()` in new projects, as they pull in the whole SDK.  
    - **Avoid tight coupling and singletons where possible:** While using Firebase, you often will use singletons (like the default `Auth.auth()` or Firestore instance). This is fine, but for complex apps consider wrapping these in your own classes or protocols. For example, define an interface (protocol in Swift or TypeScript interface) for your data layer (with methods like `fetchUserProfile(userId)`), and have an implementation that uses Firebase. This way, the rest of your code relies on an abstraction, making it easier to mock for unit tests or to replace Firebase if needed. Don’t scatter raw queries or `.observe()` calls in many view controllers or components; instead funnel them through a centralized layer. This approach keeps your app architecture clean and your Firebase usage consistent.  
    - **Leverage asynchronous patterns:** Firebase operations are inherently asynchronous (network calls). Embrace the async patterns of your language to keep code responsive. In Swift, use completion closures, Combine publishers, or async/await (if using Swift concurrency with Firebase API that supports it) to handle results without blocking the main thread. For example, use `Firestore.asyncAwait` APIs or wrap callback-based calls in `Task { ... }` if appropriate. In TypeScript, take advantage of **Promises** and **async/await** for readability. For instance, instead of nested `.then()` callbacks, write `const doc = await getDoc(docRef)` inside an async function, with proper try/catch for error handling. This makes the code cleaner and less error-prone, while ensuring UI updates happen on the main thread (in Swift) or main event loop (in JS) after data is fetched.

    ## Data Handling and Performance  
    - **Fetch data efficiently:** Design your data requests to minimize bandwidth and improve speed. Retrieve only the data you need from Firebase. For Firestore or Realtime Database, use queries with filters and limits rather than pulling entire collections when possible. For example, if you need a list of items for the current user, query with an appropriate condition (such as `.where("ownerId", "==", currentUserId")` in Firestore, or use database rules to scope data in Realtime DB). Likewise, use **pagination** or infinite scroll techniques for large datasets (Firestore supports query cursors to fetch data in chunks). This ensures your app remains fast and you stay within usage limits.  
    - **Use listeners judiciously:** One of Firebase’s strengths is real-time updates via listeners (observers on database nodes or Firestore snapshots). Use these only when you truly need live updating data. Attach listeners (such as `onSnapshot` for Firestore or `observe(.value)` for Realtime DB in Swift) when the relevant UI is active, and **detach them when not needed**. In iOS, a best practice is to add observers in `viewWillAppear` (or when a SwiftUI view appears) and remove them in `viewWillDisappear`/`deinit`. This way, you’re not consuming resources listening to updates while the user isn’t viewing that data. In a web app, if you set up a real-time subscription (for example, using `onSnapshot` or `onValue`), make sure to unsubscribe when the component unmounts or the user navigates away. Most Firebase listener functions return a callback (unsubscribe function) – call it to stop listening. Properly managing listeners improves performance and prevents memory leaks or unnecessary network usage across all platforms.  
    - **Enable offline persistence (when appropriate):** Firebase client SDKs can cache data locally to keep your app functional offline. In Firestore, offline persistence is enabled by default on native iOS apps; the local cache will allow reads and writes (which sync when connectivity returns). For web apps, you can enable persistence by calling `enableIndexedDbPersistence()` on your Firestore instance (note: do this once, and be aware of multi-tab implications). If using Realtime Database, the iOS SDK also caches data by default while online; on web, you can use `database().goOffline()`/`goOnline()` to control connections. Using offline data helps provide a better user experience during network drops. However, only enable persistence if your app needs it; for simple apps or those with sensitive data, you might keep it off to avoid stale data issues.  
    - **Optimize writes and updates:** Batch and structure your writes to be efficient. If you need to make multiple related updates, use a **batch write or transaction** (Firestore supports `writeBatch()` and transactions, and the Realtime Database can handle multi-location updates atomically). Batching reduces network round-trips and ensures data consistency. Also, avoid overly frequent writes in tight loops – for example, rather than updating a progress value in the database every second, consider throttling updates or using in-memory state and writing infrequently. On the web/TypeScript side, take advantage of Firebase’s ability to handle concurrent updates (the SDK will queue and retry writes that fail due to contention if using transactions). Design your data model for scalability: in Firestore, watch out for hotspots like too many writes to a single document or a very high write rate to a small collection (refer to Firestore best practices for index and hotspot avoidance if your app scales up). In summary, thoughtful data modeling (using subcollections, avoiding deeply nested JSON in RTDB) and using the tools Firebase provides (queries, indexes, batches) will keep your app performing well.  
    - **Monitor performance in production:** Use Firebase Performance Monitoring (supported on iOS and web) and Analytics to gather insight into how your app behaves for users. Although not strictly an SDK usage “pattern,” it’s a best practice to instrument your app – for example, measure how long certain Firebase calls take or whether enabling persistence improved things. On iOS, you can simply add Performance Monitoring SDK and it will auto-track network calls including Firebase queries. On web, performance monitoring can track request latency. Monitoring helps you catch inefficient database queries or large downloads that you might optimize.

    ## Security and Privacy  
    - **Secure your data with Firebase Rules:** Always enforce security on the backend with **Firebase Security Rules** (for Firestore, Realtime Database, and Storage). Never rely solely on client-side checks, because users can inspect or modify client apps. Write rules to ensure users can only access or modify data they should. For example, in Firestore rules, use conditions like `request.auth.uid == resource.data.ownerId` to ensure a user can only read/write their own data. In Realtime Database, structure your data and rules similarly. Test your rules using the Firebase emulator or the Rules Playground to verify they work as intended. Robust security rules are the cornerstone of protecting user data in Firebase apps.  
    - **Use Authentication and validate inputs:** Tie your data access to Firebase Authentication whenever possible, so that each read/write is associated with a known user (or is explicitly marked as public in rules if intended). In Swift, take advantage of the Firebase Auth SDK to handle user sign-ups, logins, and use the `Auth.auth().currentUser` (in iOS) or `auth.currentUser` (in web) to get the UID for data paths or security conditions. Validate important data on a trusted environment. For instance, if your app performs a critical operation (like a financial transaction or awarding points), consider using **Cloud Functions** (with the Admin SDK in TypeScript) to perform that action securely server-side, rather than trusting the client. The client can request the function, and the function (with full admin privileges and additional verifications) updates data. This adds an extra layer of security for sensitive operations.  
    - **Implement App Check (optional but recommended):** Firebase **App Check** helps protect your backend resources by ensuring only your genuine app or website can access Firebase. On Apple platforms, you can enable App Check with DeviceCheck or App Attest, and in web you can use reCAPTCHA v3 or reCAPTCHA Enterprise tokens. Turning on App Check will require your client apps to provide an attestation token on each request; unauthorized requests (e.g. from scripts or modified apps) will be blocked. This is an advanced feature, but a best practice if you want to mitigate abuse (for example, prevent outsiders from using your API keys to troll your database). Make sure to register the app and adjust your Security Rules to enforce App Check if you enable this feature.  
    - **Respect user privacy and platform policies:** Ensure your use of Firebase services complies with user privacy expectations and OS policies. For example, if using Google Analytics in an iOS app, you might need to disclose tracking in App Store privacy nutrition labels. If your iOS app uses push notifications via Firebase Cloud Messaging, request user permission for notifications (Apple’s UNUserNotificationCenter) and handle the APNs device token as required. Always inform users about data collection in your privacy policy (Firebase Auth, by itself, collects minimal personal info, but Analytics or Crashlytics might collect device data). Also, in the EU or regions with GDPR/CCPA, consider enabling Firebase’s data deletion or user consent features where applicable. Keeping transparency with users while leveraging Firebase services is important for trust and compliance.  
    - **Keep Firebase SDKs up-to-date:** Regularly update the Firebase SDK to the latest version for security patches and improvements. Both the Swift and TypeScript SDKs are actively maintained. Upgrading promptly ensures you have fixes for any known vulnerabilities and can take advantage of new features or performance enhancements. If you use package management (SPM/CocoaPods or npm), check for updates frequently. Also monitor Firebase release notes for any breaking changes especially if a major version update is announced. Maintaining your dependencies is a simple but critical best practice to keep your app secure and stable.

    # Workflow

    Following these steps will help you integrate Firebase into your Swift and TypeScript projects with best practices in mind:

    1. **Plan Firebase usage and create projects:** Before coding, determine which Firebase services you’ll use (e.g. Auth, Firestore, Storage, etc.) and create a Firebase project (or multiple projects for different environments). In the Firebase console, register your iOS app (get the `GoogleService-Info.plist`) and/or register your web app (get the config snippet). Enable required services (like turning on Email/Google sign-in providers in Auth if needed, or enabling Firestore). Planning ahead ensures you have the proper configuration and security rules set up from the start.  
    2. **Install SDKs in your app:** Add the Firebase SDK to your Swift project using Swift Package Manager (go to **File > Add Packages** in Xcode, add the Firebase GitHub repository, and select the Firebase products you need). This will download the necessary Firebase libraries (for example, FirebaseAuth, FirebaseFirestore, etc.). For a TypeScript project, install the Firebase SDK via npm (`npm install firebase`). This makes Firebase’s modules (auth, firestore, messaging, etc.) available for import in your code. If you’re using a bundler or framework (like React, Angular, Vite, etc.), the npm package will integrate with it. Make sure the SDK versions are consistent (use the latest stable release, and the same major version across Firebase packages).  
    3. **Configure and initialize Firebase:** After installation, initialize Firebase in your application code. In the Swift app, import Firebase in your AppDelegate or main App file and call `FirebaseApp.configure()` exactly once during startup. Verify that the `GoogleService-Info.plist` is included in the app bundle so configuration can succeed. In the TypeScript app, import the necessary Firebase functions (e.g. `initializeApp`) and call `initializeApp({...config object...})` with your Firebase project’s config. Store the return value (the Firebase app instance) if needed, or immediately initialize services like:  
       ```ts
       const app = initializeApp(firebaseConfig);
       const db = getFirestore(app);
       const auth = getAuth(app);
       ```  
       This sets up the connection to Firebase. Ensure this code runs at app launch (for example, in your main `index.tsx` or equivalent). If your environment has server-side rendering, guard the initialization to only run on the client side. With Firebase initialized, your app is now ready to use Firebase services.  
    4. **Implement features using best practices:** Write your application code to interact with Firebase in a structured way. For example, when building a feature that displays a list of data from Firestore, use a view model or controller on iOS that queries Firestore and listens for updates, updating the UI through published properties or callbacks. On the web, perhaps use a state management solution or React hooks/contexts to fetch and subscribe to data. As you code these, remember to apply the earlier guidelines: query for only the data needed, handle the asynchronous responses properly (updating UI on main thread or state), and detach any real-time listeners when a view/component is disposed. Test each feature with various network conditions (you can simulate offline or slow connections) to ensure your app remains responsive and data stays consistent (thanks to offline persistence or loading states in UI).  
    5. **Apply security rules and validate:** Before going live, implement comprehensive security rules in Firebase for each service. For Firestore, define rules in the Firebase console or locally in firestore.rules – enforce user authentication and any business logic (like “users can only write their own records” or data format validations). Do the equivalent for Realtime DB or Storage if used. Use the Firebase **Emulator Suite** during development to test these rules with your code: the Authentication emulator can create test users, Firestore/RTDB emulators allow you to read/write data and see if rules are blocking or allowing correctly. In your Swift and TS code, ensure you handle permission errors gracefully (e.g. if a write is denied by rules, catch the exception and show an error or re-authenticate the user if their token expired). This step is crucial for protecting data and providing a good user experience around security (like not failing silently).  
    6. **Test on real devices and browsers:** Run your iOS app on real devices (or at least simulators) and your web app in multiple browsers to verify that Firebase features work as expected in each target environment. Check things like: Does FirebaseAuth persist the user session between app launches or page reloads? (By default it should, via Keychain on iOS and localStorage in web, unless configured otherwise.) Are realtime updates coming through and stopping appropriately when views close? Do Cloud Functions calls succeed and return expected results? By testing in realistic conditions, you can catch issues like missing permissions, incorrect config, or performance bottlenecks. Use Xcode’s debug console or browser dev tools to monitor for any error messages from Firebase.  
    7. **Monitor and iterate:** After deployment, keep an eye on your Firebase project’s usage and logs. Use Crashlytics in your iOS app to catch any runtime exceptions (including those related to Firebase calls) and Performance Monitoring to see if any Firebase request is slow. In your TypeScript app, you can also use analytics or logging to track how often certain calls fail or retry. Firebase provides dashboards for things like Firestore throughput, auth failures, etc. Address any issues: for example, if you see a lot of “permission-denied” errors in logs, you may need to adjust security rules or ensure users are logged in properly before accessing data. Continue to update your code following best practices as your app grows – for instance, you might implement caching of certain data to reduce calls, or move some logic to Cloud Functions to offload work from the client. By monitoring and iterating, you’ll maintain an app that is efficient, secure, and scales well with Firebase.

    # Examples

    Below are simple examples in Swift and TypeScript illustrating some best practices in action, such as structured data access, real-time updates with proper listener management, and error handling:

    **Swift (iOS) Example – Using Firestore with a ViewModel (MVVM pattern):**  
    In this Swift example, we define a view model for a list of “Task” items. It uses Firebase Firestore to listen for real-time updates in the “tasks” collection. The view model starts the listener when needed and stops it when not needed, demonstrating clean lifecycle management of Firebase observers on iOS. 

    ```swift
    import FirebaseFirestore

    class TasksViewModel: ObservableObject {
        @Published var tasks: [Task] = []          // Task is a model conforming to Codable for Firestore documents
        private var listener: ListenerRegistration?

        private let db = Firestore.firestore()

        func startListening() {
            // Attach a listener to the "tasks" collection, e.g. all tasks owned by the current user
            listener = db.collection("tasks")
                .whereField("ownerId", isEqualTo: Auth.auth().currentUser?.uid ?? "")
                .addSnapshotListener { [weak self] (snapshot, error) in
                    if let error = error {
                        print("Error fetching tasks: \(error)")
                        return
                    }
                    guard let documents = snapshot?.documents else { return }
                    // Map documents to Task model objects
                    self?.tasks = documents.compactMap { doc in
                        try? doc.data(as: Task.self)   // Uses Firestore Swift Codable to parse data
                    }
                }
        }

        func stopListening() {
            // Detach the real-time listener to avoid updates when not needed
            listener?.remove()
            listener = nil
        }
    }

    // Usage in a SwiftUI View (for example):
    struct TasksView: View {
        @StateObject private var viewModel = TasksViewModel()

        var body: some View {
            List(viewModel.tasks) { task in
                Text(task.title)
            }
            .onAppear {
                viewModel.startListening()   // begin updates when view appears
            }
            .onDisappear {
                viewModel.stopListening()    // stop updates when view disappears
            }
        }
    }

*In this snippet, the view model listens for changes in Firestore and
updates a published list of tasks. When the view appears, we call*
`startListening()` *to fetch and listen to data, and when the view
disappears, we call* `stopListening()` *to remove the Firestore
listener. This ensures we don't leak listeners or do extra work when the
UI is not visible. The query uses a* `whereField` *filter to only
retrieve the current user's tasks, which is efficient. The code also
handles errors by printing them (in a real app, you might display an
alert). The use of* `doc.data(as: Task.self)` *leverages Firebase's
Codable integration to easily convert documents into Swift model
objects.*

**TypeScript (Web) Example -- Initializing and querying Firestore with
onSnapshot:**\
This TypeScript example demonstrates setting up Firebase in a web app
and using the modular API to query Firestore. We initialize the app, get
the Firestore instance, and then set up a real-time listener on a
collection query. We also show how to unsubscribe from the listener,
which would typically be done when the data is no longer needed (such as
when a React component unmounts).

    import { initializeApp } from "firebase/app";
    import { getFirestore, collection, query, where, onSnapshot, QuerySnapshot, DocumentData } from "firebase/firestore";
    import { getAuth, onAuthStateChanged } from "firebase/auth";

    // Your Firebase configuration
    const firebaseConfig = {
      apiKey: "YOUR_API_KEY",
      authDomain: "YOUR_PROJECT.firebaseapp.com",
      projectId: "YOUR_PROJECT_ID",
      // ...other config values...
    };

    // Initialize Firebase app and services
    const app = initializeApp(firebaseConfig);
    const db = getFirestore(app);
    const auth = getAuth(app);

    // Example: Listen to a user's task list in Firestore in real-time
    function listenToUserTasks(userId: string) {
      const q = query(collection(db, "tasks"), where("ownerId", "==", userId));
      const unsubscribe = onSnapshot(q, (snapshot: QuerySnapshot<DocumentData>) => {
        // This callback runs whenever the query results change (added/modified/removed)
        snapshot.docChanges().forEach(change => {
          if (change.type === "added") {
            console.log("New task: ", change.doc.data());
          } else if (change.type === "modified") {
            console.log("Modified task: ", change.doc.data());
          } else if (change.type === "removed") {
            console.log("Removed task: ", change.doc.data());
          }
        });
      }, (error) => {
        console.error("Error listening to tasks: ", error);
      });

      return unsubscribe;  // return the unsubscribe function to call later
    }

    // Example usage: start listening when user is authenticated
    onAuthStateChanged(auth, (user) => {
      if (user) {
        // User is signed in, start listening to their tasks
        const stopListening = listenToUserTasks(user.uid);
        // ... Later, when we want to stop listening (e.g., user navigates away or logs out):
        // stopListening();
      }
    });

*In this TypeScript example, we first initialize Firebase with the
project config. We then define a function* `listenToUserTasks` *that
sets up a Firestore query for tasks owned by a specific user (using*
`where("ownerId", "==", userId)`*). We use* `onSnapshot` *to get
real-time updates, logging changes to the console. We also provide an
error callback to handle any permission or network errors. The*
`listenToUserTasks` *function returns the* `unsubscribe` *function
provided by* `onSnapshot`*. We demonstrate using it in an auth state
listener: when a user logs in (*`onAuthStateChanged`*), we start
listening to their tasks, and we would call the returned*
`stopListening()` *when appropriate (for instance, if the user logs out
or if the component displaying tasks is destroyed). This pattern shows
how to manage real-time listeners in a web app using Firebase's modular
SDK: it ensures we can cleanly stop the listener, and it filters data at
the query level (so we only get relevant tasks). We also handle errors
and use the authentication state to scope our data listening securely to
the current user.*

These examples illustrate a few key practices: initializing the SDK
properly, querying with filters, using real-time listeners responsibly,
and organizing code (the Swift MVVM pattern and the separation of
concerns in the TS example where auth state triggers data listening).
They serve as a starting point; in a full application, you would expand
on these patterns (e.g. updating UI instead of `console.log`, adding
proper error UI, etc.) while adhering to the demonstrated best
practices.

