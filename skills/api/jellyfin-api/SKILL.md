---
name: jellyfin-api
description: Jellyfin API patterns and JellyfinClient usage for MyFlix
---

# Jellyfin API Skill

## When to Use
Apply when making API calls, handling authentication, or working with media data.

## JellyfinClient Configuration

```kotlin
// Configure after authentication
jellyfinClient.configure(
    serverUrl = "https://jellyfin.example.com",
    accessToken = authResponse.accessToken,
    userId = authResponse.user.id,
    deviceId = "myflix_${System.currentTimeMillis()}"
)

// Check auth status
if (jellyfinClient.isAuthenticated) { /* proceed */ }

// Logout
jellyfinClient.logout()
```

## Common API Calls

### Libraries
```kotlin
jellyfinClient.getLibraries().onSuccess { libraries ->
    val moviesLib = LibraryFinder.findMoviesLibrary(libraries)
    val showsLib = LibraryFinder.findShowsLibrary(libraries)
}
```

### Latest Content
```kotlin
// Latest movies (excludes collections)
jellyfinClient.getLatestMovies(libraryId, limit = 12)

// Latest series (new shows, not episodes)
jellyfinClient.getLatestSeries(libraryId, limit = 12)

// Latest episodes
jellyfinClient.getLatestEpisodes(libraryId, limit = 12)
```

### Resume & Next Up
```kotlin
// Continue watching (in progress)
jellyfinClient.getResume(limit = 12)

// Next episodes to watch
jellyfinClient.getNextUp(limit = 12)
```

### Item Details
```kotlin
// Full item details
jellyfinClient.getItem(itemId).onSuccess { item ->
    // Access: item.name, item.overview, item.genres, etc.
}

// Series seasons
jellyfinClient.getSeasons(seriesId)

// Season episodes
jellyfinClient.getEpisodes(seriesId, seasonId)

// Similar items
jellyfinClient.getSimilarItems(itemId, limit = 12)
```

### Collections & Genres
```kotlin
// All collections
jellyfinClient.getCollections()

// Collection items
jellyfinClient.getCollectionItems(collectionId)

// Available genres
jellyfinClient.getGenres(libraryId)

// Items by genre
jellyfinClient.getItemsByGenre(genreName, libraryId, limit = 20)
```

### Search
```kotlin
jellyfinClient.search(query, limit = 20)
```

## Image URLs

```kotlin
// Primary poster (portrait 2:3)
jellyfinClient.getPrimaryImageUrl(itemId, imageTag, maxWidth = 400)

// Backdrop (landscape 16:9)
jellyfinClient.getBackdropUrl(itemId, backdropTag, maxWidth = 1920)

// Thumbnail
jellyfinClient.getThumbUrl(itemId, thumbTag, maxWidth = 600)

// Blurred backdrop for backgrounds
jellyfinClient.getBlurredBackdropUrl(itemId, backdropTag, blur = 20)

// User avatar
jellyfinClient.getUserImageUrl(userId)
```

## Playback Reporting

```kotlin
// Start playback
jellyfinClient.reportPlaybackStart(itemId, mediaSourceId, positionTicks = 0)

// Progress updates (call every 10 seconds)
jellyfinClient.reportPlaybackProgress(itemId, positionTicks, isPaused = false)

// Stop playback
jellyfinClient.reportPlaybackStopped(itemId, positionTicks)
```

## User Actions

```kotlin
// Mark watched/unwatched
jellyfinClient.setPlayed(itemId, played = true)

// Toggle favorite
jellyfinClient.setFavorite(itemId, favorite = true)
```

## Caching

```kotlin
// Clear all cache (before refresh)
jellyfinClient.clearCache()

// Invalidate specific caches
jellyfinClient.invalidateCache("resume", "nextup", "item:$itemId")
```

## Field Selection Constants

The client optimizes requests by selecting only needed fields:

- `CARD`: Overview, ImageTags, BackdropImageTags, UserData, Ratings
- `EPISODE_CARD`: Above + SeriesName, SeasonName  
- `DETAIL`: Full info including MediaSources, Genres, People, etc.
- `SERIES_DETAIL`: Above + ChildCount, RecursiveItemCount

## Data Models

### JellyfinItem
```kotlin
data class JellyfinItem(
    val id: String,
    val name: String,
    val type: String,              // "Movie", "Series", "Episode", "BoxSet"
    val overview: String?,
    val productionYear: Int?,
    val officialRating: String?,   // "PG-13", "TV-MA"
    val communityRating: Float?,   // 0-10
    val criticRating: Int?,        // Rotten Tomatoes 0-100
    val runTimeTicks: Long?,
    val seriesId: String?,         // For episodes
    val seriesName: String?,
    val seasonName: String?,
    val indexNumber: Int?,         // Episode number
    val parentIndexNumber: Int?,   // Season number
    val imageTags: ImageTags?,
    val backdropImageTags: List<String>?,
    val userData: UserData?,
    val premiereDate: String?,
    val status: String?,           // "Ended", "Continuing"
    val genres: List<String>?,
    val studios: List<Studio>?,
    val people: List<Person>?,
    val mediaSources: List<MediaSource>?,
    val mediaStreams: List<MediaStream>?
)
```

### UserData
```kotlin
data class UserData(
    val playbackPositionTicks: Long?,
    val playCount: Int?,
    val isFavorite: Boolean,
    val played: Boolean,
    val lastPlayedDate: String?
)
```

## Authentication Flow

### Quick Connect
```kotlin
jellyfinClient.quickConnectFlow(serverUrl).collect { state ->
    when (state) {
        is QuickConnectFlowState.WaitingForApproval -> {
            // Display state.code to user
        }
        is QuickConnectFlowState.Authenticated -> {
            // Save state.authResponse
        }
        is QuickConnectFlowState.Error -> {
            // Handle state.message
        }
    }
}
```

### Username/Password
```kotlin
jellyfinClient.authenticate(serverUrl, username, password)
    .onSuccess { authResponse ->
        jellyfinClient.configure(
            serverUrl, 
            authResponse.accessToken,
            authResponse.user.id,
            deviceId
        )
    }
```

## Error Handling Pattern

```kotlin
suspend fun loadData() {
    isLoading = true
    errorMessage = null
    
    jellyfinClient.getData()
        .onSuccess { data ->
            items = data
        }
        .onFailure { e ->
            errorMessage = "Failed to load: ${e.message ?: "Unknown error"}"
        }
    
    isLoading = false
}
```
