---
name: kotlin-compose-patterns
description: Kotlin and Jetpack Compose best practices for MyFlix Android development
---

# Kotlin & Jetpack Compose Patterns

## State Management

### Remember Patterns
```kotlin
// Simple state
var count by remember { mutableStateOf(0) }

// Derived state - recomputes only when dependencies change
val isValid by remember {
    derivedStateOf { username.isNotBlank() && password.length >= 8 }
}

// State with key - resets when key changes
val formattedDate = remember(timestamp) { dateFormatter.format(timestamp) }
```

### Side Effects
```kotlin
// Run once on composition
LaunchedEffect(Unit) { viewModel.loadData() }

// Run when key changes
LaunchedEffect(userId) { viewModel.loadUserData(userId) }

// Cleanup on disposal
DisposableEffect(lifecycleOwner) {
    val observer = LifecycleEventObserver { _, event -> /* ... */ }
    lifecycleOwner.lifecycle.addObserver(observer)
    onDispose { lifecycleOwner.lifecycle.removeObserver(observer) }
}
```

## MyFlix Card Sizes

```kotlin
object CardSizes {
    val MediaCardWidth = 120.dp      // Portrait 2:3 posters
    val WideMediaCardWidth = 210.dp  // Landscape 16:9 thumbs
}
```

## TV Focus Patterns

### Focus Requester Setup
```kotlin
val focusRequester = remember { FocusRequester() }

LaunchedEffect(Unit) {
    delay(100) // Allow composition to settle
    focusRequester.requestFocus()
}

Box(modifier = Modifier.focusRequester(focusRequester)) { /* ... */ }
```

### Focus Properties for Navigation
```kotlin
Modifier
    .focusRequester(cardFocusRequester)
    .focusProperties { up = heroFocusRequester }
    .onFocusChanged { if (it.isFocused) onCardFocused() }
```

### Focus Group for Rows
```kotlin
// Makes LazyColumn treat row as single focus unit
Column(modifier = Modifier.focusGroup()) {
    Text("Row Title")
    LazyRow(modifier = Modifier.focusRestorer(firstCardFocus)) {
        items(items) { /* cards */ }
    }
}
```

## Lazy List Best Practices

```kotlin
LazyRow(
    state = listState,
    horizontalArrangement = Arrangement.spacedBy(16.dp),
    contentPadding = PaddingValues(horizontal = 10.dp)
) {
    itemsIndexed(
        items = items,
        key = { _, item -> item.id }  // CRITICAL: stable keys
    ) { index, item ->
        MediaCard(
            item = item,
            modifier = Modifier.animateItem()
        )
    }
}
```

## Extension Functions

```kotlin
// Null-safe operations
inline fun <T, R> T?.ifNotNull(block: (T) -> R): R? = this?.let(block)

// Progress calculation
val JellyfinItem.progressPercent: Float
    get() = userData?.let { data ->
        val ticks = data.playbackPositionTicks ?: 0L
        val runtime = runTimeTicks ?: 0L
        if (runtime > 0) (ticks.toFloat() / runtime) else 0f
    } ?: 0f
```

## Image Loading with Coil

```kotlin
AsyncImage(
    model = imageUrl,
    contentDescription = item.name,
    modifier = Modifier
        .fillMaxSize()
        .clip(MaterialTheme.shapes.medium),
    contentScale = ContentScale.Crop
)
```

## Surface for TV Cards

```kotlin
Surface(
    onClick = onClick,
    onLongClick = onLongClick,
    modifier = modifier.width(CardSizes.MediaCardWidth),
    shape = ClickableSurfaceDefaults.shape(shape = MaterialTheme.shapes.medium),
    colors = ClickableSurfaceDefaults.colors(
        containerColor = TvColors.Surface,
        focusedContainerColor = TvColors.FocusedSurface
    ),
    border = ClickableSurfaceDefaults.border(
        focusedBorder = Border(
            border = BorderStroke(2.dp, TvColors.BluePrimary),
            shape = MaterialTheme.shapes.medium
        )
    ),
    scale = ClickableSurfaceDefaults.scale(focusedScale = 1f)
) { /* content */ }
```
