---
name: Android Networking
description: Standards for Retrofit, OkHttp, and API Communication
metadata:
  labels: [android, networking, retrofit, okhttp]
  triggers:
    files: ['**/*Api.kt', '**/*Service.kt', '**/*Client.kt']
    keywords: ['Retrofit', 'OkHttpClient', '@GET', '@POST']
---

# Android Networking Standards

## **Priority: P0**

## Implementation Guidelines

### Libraries

- **Client**: Retrofit 2 + OkHttp 4.
- **Serialization**: Kotlinx Serialization (Preferred over Moshi/Gson).
- **Format**: JSON. Use `@SerialName` for field mapping.

### Best Practices

- **Interceptors**: Use for Auth Headers (Bearer Token) and Logging (`HttpLoggingInterceptor`).
- **Response Handling**: Wrap responses in a `Result` type (Success/Error/Loading) in Repository/DataSource, NOT in the API interface.
- **Threads**: API calls must be `suspend` functions.

## Anti-Patterns

- **Main Thread**: `**No Blocking Calls**: Use suspend.`
- **Logic in API**: `**No Logic in Interface**: Only definitions.`
- **Missing Content-Type**: `**No Raw Factory**: When using kotlinx.serialization, always explicitly specify "application/json" MediaType in your converter factory.`

## References

- [Setup & Wrappers](references/implementation.md)
