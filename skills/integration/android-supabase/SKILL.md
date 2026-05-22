---
name: android-supabase
description: Supabase integration patterns for Android - authentication, database, realtime subscriptions. Use when setting up Supabase SDK, implementing OAuth, querying database, or setting up realtime.
license: MIT
version: 2.0.0
---

# Android Supabase Skill

Supabase integration patterns for Android with Kotlin, Jetpack Compose, and Clean Architecture.

## When to Use

- Setting up Supabase SDK in Android project
- Implementing Google OAuth with Credential Manager
- Database CRUD operations (select, insert, update, upsert, delete)
- Real-time subscriptions
- Managing user sessions

## Setup

### Dependencies (libs.versions.toml)

```toml
[versions]
supabase = "3.2.6"
ktor = "3.1.3"

[libraries]
supabase-bom = { module = "io.github.jan-tennert.supabase:bom", version.ref = "supabase" }
supabase-postgrest = { module = "io.github.jan-tennert.supabase:postgrest-kt" }
supabase-gotrue = { module = "io.github.jan-tennert.supabase:gotrue-kt" }
supabase-realtime = { module = "io.github.jan-tennert.supabase:realtime-kt" }
ktor-client = { module = "io.ktor:ktor-client-android", version.ref = "ktor" }
# Google Credential Manager
credentials = { module = "androidx.credentials:credentials", version = "1.3.0" }
credentials-play = { module = "androidx.credentials:credentials-play-services-auth", version = "1.3.0" }
googleid = { module = "com.google.android.libraries.identity.googleid:googleid", version = "1.1.1" }
```

### Client Factory Pattern

```kotlin
object SupabaseClientFactory {
    fun create(): SupabaseClient {
        return createSupabaseClient(
            supabaseUrl = BuildConfig.SUPABASE_URL,
            supabaseKey = BuildConfig.SUPABASE_ANON_KEY
        ) {
            install(Auth)
            install(Postgrest)
            install(Realtime) // Optional
        }
    }
}
```

### Koin DI Module

```kotlin
val supabaseModule = module {
    single { SupabaseClientFactory.create() }
    single<AuthService> { AuthServiceSupabaseImpl(get(), get()) }
    single<UserService> { UserServiceSupabaseImpl(get(), get()) }
}
```

## Google OAuth with Credential Manager

**Critical:** Use **Web Client ID** (not Android Client ID) for native app authentication.

### AuthService Implementation

```kotlin
class AuthServiceSupabaseImpl(
    private val supabaseClient: SupabaseClient,
    private val dispatchers: QzDispatchers
) : AuthService {

    override val authState: Flow<AuthState> = supabaseClient.auth.sessionStatus.map {
        when (it) {
            is SessionStatus.Authenticated -> {
                val user = it.session.user ?: return@map AuthState.Guest
                AuthState.Authenticated(
                    AuthUser(
                        uid = user.id,
                        email = user.email.orEmpty(),
                        displayName = user.userMetadata?.get("full_name")?.jsonPrimitive?.content.orEmpty(),
                        photoUrl = user.userMetadata?.get("avatar_url")?.jsonPrimitive?.content.orEmpty(),
                    )
                )
            }
            else -> AuthState.Guest
        }
    }

    override suspend fun signInWithGoogleCredential(
        context: Context,
        serverClientId: String
    ) = withContext(dispatchers.io) {
        runCatching {
            val credentialManager = CredentialManager.create(context)

            // Generate nonce for security
            val rawNonce = UUID.randomUUID().toString()
            val hashedNonce = MessageDigest.getInstance("SHA-256")
                .digest(rawNonce.toByteArray())
                .fold("") { str, it -> str + "%02x".format(it) }

            // Build Google ID option
            val googleIdOption = GetGoogleIdOption.Builder()
                .setFilterByAuthorizedAccounts(false)
                .setServerClientId(serverClientId)
                .setNonce(hashedNonce)
                .build()

            val request = GetCredentialRequest.Builder()
                .addCredentialOption(googleIdOption)
                .build()

            // Get credential from Google
            val result = credentialManager.getCredential(request, context)
            val googleIdToken = GoogleIdTokenCredential.createFrom(result.credential.data).idToken

            // Sign in with Supabase
            supabaseClient.auth.signInWith(IDToken) {
                idToken = googleIdToken
                provider = Google
                nonce = rawNonce
            }
        }.fold(
            { Result.success(Unit) },
            { Result.failure(it) }
        )
    }

    override suspend fun signOut() = withContext(dispatchers.io) {
        runCatching { supabaseClient.auth.signOut() }
            .fold({ Result.success(Unit) }, { Result.failure(it) })
    }
}
```

### UseCase Pattern

```kotlin
class SignInWithGoogleUseCase(
    private val authService: AuthService,
    private val secretManager: SecretManager
) : UseCase<Context, Result<Unit>>() {
    override suspend operator fun invoke(input: Context): Result<Unit> {
        val serverClientId = secretManager.getStaticSecret(StaticSecretKey.GOOGLE_OAUTH_CLIENT_ID)
        return authService.signInWithGoogleCredential(input, serverClientId)
    }
}
```

## Database Operations

### SELECT with Filter Builder

```kotlin
// Single record with filter
suspend fun fetchUser(uuid: String): User? = withContext(dispatchers.io) {
    runCatching {
        supabaseClient.from("users")
            .select {
                filter {
                    eq("auth_uuid", uuid)
                }
            }
            .decodeSingleOrNull<User>()
    }.getOrNull()
}

// List with pagination and ordering
suspend fun fetchLeaderboard(limit: Int): List<Entry> = withContext(dispatchers.io) {
    try {
        supabaseClient.from("leaderboard")
            .select {
                order("score", Order.DESCENDING)
                limit(limit)
            }
            .decodeList<Entry>()
    } catch (e: Exception) {
        emptyList()
    }
}

// Complex filters
val results = supabaseClient.from("questions")
    .select {
        filter {
            eq("category", "science")
            gte("difficulty", 3)
            neq("status", "draft")
        }
        order("created_at", Order.DESCENDING)
        limit(20)
        offset(page * 20)
    }
    .decodeList<Question>()
```

### INSERT

```kotlin
// Single insert
supabaseClient.from("scores")
    .insert(ScoreEntry(userId = id, score = 100))

// Batch insert
supabaseClient.from("questions")
    .insert(listOf(question1, question2, question3))

// Insert and return
val inserted = supabaseClient.from("users")
    .insert(newUser)
    .decodeSingle<User>()
```

### UPDATE

```kotlin
// Update with filter
supabaseClient.from("users")
    .update(mapOf("name" to "New Name", "updated_at" to now))
    .eq("id", userId)

// Update with object
supabaseClient.from("settings")
    .update(UserSettings(theme = "dark")) {
        filter { eq("user_id", userId) }
    }
```

### UPSERT (Insert or Update)

```kotlin
// Upsert with conflict column
suspend fun upsertUser(request: UpsertUserRequest) = withContext(dispatchers.io) {
    runCatching {
        supabaseClient.from("users").upsert(request) {
            onConflict = "auth_uuid"
        }
    }.fold(
        onSuccess = { Result.success(Unit) },
        onFailure = { Result.failure(it) }
    )
}
```

### DELETE

```kotlin
// ALWAYS include filter - omitting deletes entire table!
supabaseClient.from("sessions")
    .delete {
        filter {
            eq("user_id", userId)
            lt("expires_at", now)
        }
    }
```

## Real-time Subscriptions

```kotlin
// Flow-based reactive pattern
supabaseClient.from("leaderboard")
    .selectAsFlow()
    .collect { entries: List<Entry> ->
        _leaderboard.value = entries
    }

// Manual channel subscription
val channel = supabase.channel("scores")
channel.postgresChangeFlow<PostgresAction.Insert>(schema = "public") {
    table = "scores"
}.collect { change ->
    handleNewScore(change.record)
}
channel.subscribe()

// Cleanup
channel.unsubscribe()
```

**Note:** Enable replication in Supabase Console > Settings > Replication.

## Data Models

```kotlin
@Serializable
data class User(
    val id: String = "",
    @SerialName("auth_uuid") val authUuid: String = "",
    val email: String = "",
    val name: String = "",
    @SerialName("created_at") val createdAt: String? = null,
    @SerialName("updated_at") val updatedAt: String? = null
)

@Serializable
data class LeaderboardEntry(
    val id: String = "",
    @SerialName("user_id") val userId: String = "",
    val score: Int = 0,
    val rank: Int = 0,
    @SerialName("display_name") val displayName: String = ""
)
```

## Error Handling Pattern

```kotlin
suspend fun <T> safeSupabaseCall(block: suspend () -> T): Result<T> = try {
    Result.success(block())
} catch (e: RestException) {
    Timber.e("Supabase REST error: ${e.message}")
    Result.failure(e)
} catch (e: HttpRequestTimeoutException) {
    Timber.e("Supabase timeout")
    Result.failure(e)
} catch (e: Exception) {
    Timber.e("Supabase error: ${e.message}")
    Result.failure(e)
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Check API key, refresh session |
| 403 Forbidden | Verify RLS policies, check user permissions |
| Serialization error | Check `@SerialName` mappings, provide defaults |
| OAuth fails | Use Web Client ID, verify SHA-1 fingerprint |
| Network timeout | Increase Ktor timeout in client config |
| Real-time not working | Enable replication in Supabase console |

## Security Checklist

- [ ] Store credentials in `local.properties` (not committed)
- [ ] Enable RLS on all tables
- [ ] Never expose service_role key in app
- [ ] Use `@SerialName` for snake_case DB columns
- [ ] Validate user input before queries
- [ ] Handle session expiry gracefully

## Version Compatibility

| Supabase SDK | Kotlin | Ktor | Min SDK |
|--------------|--------|------|---------|
| 3.2.x | 2.0+ | 3.x | 26 |
| 3.0.x | 1.9+ | 2.x | 24 |

## References

- [Supabase Kotlin SDK](https://supabase.com/docs/reference/kotlin/introduction)
- [Supabase Auth](https://supabase.com/docs/guides/auth)
- [Google Credential Manager](https://developer.android.com/identity/sign-in/credential-manager)
- [Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)
