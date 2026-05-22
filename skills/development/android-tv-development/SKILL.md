---
name: android-tv-development
description: Android TV-specific patterns for D-pad navigation, focus management, and TV UI
---

# Android TV Development Skill

## When to Use
Apply when building TV screens, implementing D-pad navigation, or handling focus management.

## Focus Management Fundamentals

### FocusRequester Pattern
```kotlin
// Create requesters for key navigation targets
val heroPlayFocusRequester = remember { FocusRequester() }
val topNavFocusRequester = remember { FocusRequester() }
val firstRowFocusRequester = remember { FocusRequester() }

// Request focus after composition settles
LaunchedEffect(Unit) {
    delay(100)
    heroPlayFocusRequester.requestFocus()
}
```

### Focus Properties for D-pad Navigation
```kotlin
// Define explicit navigation paths
Modifier
    .focusRequester(buttonFocusRequester)
    .focusProperties {
        up = topNavFocusRequester      // D-pad UP goes here
        down = firstRowFocusRequester  // D-pad DOWN goes here
        left = FocusRequester.Cancel   // Prevent left navigation
    }
```

### Key Event Handling
```kotlin
Modifier.onPreviewKeyEvent { keyEvent ->
    if (keyEvent.type == KeyEventType.KeyDown && keyEvent.key == Key.DirectionUp) {
        if (atTopOfList) {
            coroutineScope.launch {
                listState.scrollToItem(0)
                heroFocusRequester.requestFocus()
            }
            true // Consumed
        } else false
    } else false
}
```

## Home Screen Pattern

### Layer Structure
```kotlin
Box(modifier = Modifier.fillMaxSize()) {
    // Layer 1: Dynamic background (blurred backdrop)
    DynamicBackground(imageUrl = previewItem?.backdropUrl)
    
    // Layer 2: Content (Hero + Rows)
    Column {
        HeroSection(
            items = featuredItems,
            onPlayClick = onPlayClick,
            playButtonFocusRequester = heroPlayFocusRequester
        )
        LazyColumn {
            items(rows) { row ->
                ItemRow(
                    items = row.items,
                    upFocusRequester = heroPlayFocusRequester
                )
            }
        }
    }
    
    // Layer 3: Top Navigation
    TopNavigationBar(
        downFocusRequester = heroPlayFocusRequester,
        modifier = Modifier.align(Alignment.TopCenter)
    )
}
```

### Hero Section (30% screen height)
```kotlin
Box(
    modifier = Modifier
        .fillMaxWidth()
        .fillMaxHeight(0.30f)
) {
    // Backdrop image
    AsyncImage(model = backdropUrl, ...)
    
    // Gradient overlay
    Box(modifier = Modifier
        .fillMaxSize()
        .background(Brush.verticalGradient(
            colors = listOf(Color.Transparent, TvColors.Background)
        ))
    )
    
    // Content (title, buttons)
    Column {
        Text(item.name, style = MaterialTheme.typography.displayMedium)
        Row {
            Button(
                onClick = onPlayClick,
                modifier = Modifier.focusRequester(playFocusRequester)
            ) { Text("Play") }
        }
    }
}
```

## Item Row Pattern

```kotlin
@Composable
private fun ItemRow(
    title: String,
    items: List<JellyfinItem>,
    upFocusRequester: FocusRequester? = null,
    modifier: Modifier = Modifier
) {
    val firstCardFocus = remember { FocusRequester() }
    
    Column(
        modifier = modifier.focusGroup()  // Row as single focus unit
    ) {
        // Header with accent bar
        Row {
            Box(modifier = Modifier
                .width(4.dp)
                .height(24.dp)
                .background(accentColor))
            Text(title, style = MaterialTheme.typography.titleLarge)
        }
        
        // Cards
        LazyRow(
            modifier = Modifier.focusRestorer(firstCardFocus),
            horizontalArrangement = Arrangement.spacedBy(16.dp),
            contentPadding = PaddingValues(horizontal = 10.dp)
        ) {
            itemsIndexed(items, key = { _, item -> item.id }) { index, item ->
                MediaCard(
                    item = item,
                    modifier = Modifier
                        .then(if (index == 0) Modifier.focusRequester(firstCardFocus) else Modifier)
                        .then(upFocusRequester?.let { 
                            Modifier.focusProperties { up = it } 
                        } ?: Modifier)
                )
            }
        }
    }
}
```

## Navigation Rail Pattern

```kotlin
@Composable
fun TopNavigationBar(
    selectedItem: NavItem,
    onItemSelected: (NavItem) -> Unit,
    downFocusRequester: FocusRequester,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .background(Brush.verticalGradient(
                colors = listOf(TvColors.Background, Color.Transparent)
            ))
            .padding(16.dp),
        horizontalArrangement = Arrangement.spacedBy(24.dp)
    ) {
        NavItem.entries.forEach { item ->
            NavigationButton(
                item = item,
                isSelected = item == selectedItem,
                onClick = { onItemSelected(item) },
                modifier = Modifier.focusProperties { down = downFocusRequester }
            )
        }
    }
}
```

## Long-Press Dialog Pattern

```kotlin
// State
var dialogParams by remember { mutableStateOf<DialogParams?>(null) }

// On long click
onLongClick = { item ->
    dialogParams = DialogParams(
        title = item.name,
        items = buildHomeDialogItems(item, jellyfinClient)
    )
}

// Dialog display
dialogParams?.let { params ->
    DialogPopup(
        params = params,
        onDismiss = { dialogParams = null },
        onItemSelected = { action -> handleAction(action) }
    )
}
```

## TV-Specific Tips

1. **Focus Indicators**: Use `focusedContainerColor` and `focusedBorder` for clear visual feedback
2. **Scale on Focus**: Keep `focusedScale = 1f` to avoid layout shifts
3. **Scroll Position**: Save/restore scroll positions during navigation
4. **Loading States**: Show TvLoadingIndicator during data fetches
5. **Error Handling**: Display errors in dialogs, not inline
6. **Background Polling**: Use `POLL_INTERVAL_MS = 30_000L` for home screen refresh
