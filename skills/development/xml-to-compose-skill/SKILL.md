---
name: xml-to-compose
description: Convert Android XML layouts to Jetpack Compose. Use when asked to migrate XML layouts, convert views to composables, or help with Compose migration. Handles layouts, widgets, attributes, styles, and resource references.
---

# XML to Jetpack Compose Converter

Convert Android XML layouts to idiomatic Jetpack Compose code.

## Conversion Process

1. Analyze the XML structure and identify root layout
2. Map each view to its Compose equivalent
3. Convert attributes to Modifier chains (order matters!)
4. Handle resource references (@string, @dimen, @color)
5. Extract styles into reusable composables or theme values

## Quick Reference

### Layouts
| XML | Compose |
|-----|---------|
| `LinearLayout (vertical)` | `Column` |
| `LinearLayout (horizontal)` | `Row` |
| `FrameLayout` | `Box` |
| `ConstraintLayout` | `Column`/`Row` or `ConstraintLayout` (dependency) |
| `ScrollView` | `Column` + `Modifier.verticalScroll()` |
| `RecyclerView` | `LazyColumn` / `LazyRow` |
| `ViewPager2` | `HorizontalPager` |

### Common Widgets
| XML | Compose |
|-----|---------|
| `TextView` | `Text` |
| `EditText` | `TextField` / `OutlinedTextField` |
| `Button` | `Button` |
| `ImageView` | `Image` / `AsyncImage` (Coil) |
| `CheckBox` | `Checkbox` |
| `Switch` | `Switch` |
| `ProgressBar` | `CircularProgressIndicator` / `LinearProgressIndicator` |
| `CardView` | `Card` |

### Modifier Order
Order matters! Follow this sequence:
1. `clickable` / `toggleable`
2. `padding` (outer)
3. `size` / `fillMaxWidth` / `weight`
4. `background` / `clip`
5. `border`
6. `padding` (inner)

## Detailed Mappings

See reference files for complete mappings:
- `references/layouts.md` — Layout containers
- `references/widgets.md` — UI components  
- `references/attributes.md` — XML attributes to Modifiers

## Output Guidelines

1. **Use Material 3** — Import from `androidx.compose.material3`
2. **Prefer built-in modifiers** — Avoid custom implementations
3. **Handle nullability** — XML allows null text, Compose needs defaults
4. **Extract dimensions** — Use `dimensionResource()` or define in theme
5. **Keep composables stateless** — Hoist state to caller
6. **Add Preview** — Include `@Preview` function for each composable

## Example

Input:
```xml
<LinearLayout
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:padding="16dp">
    
    <TextView
        android:id="@+id/title"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/welcome"
        android:textSize="24sp"
        android:textStyle="bold"/>
        
    <Button
        android:id="@+id/action_button"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:text="@string/get_started"/>
</LinearLayout>
```

Output:
```kotlin
@Composable
fun WelcomeSection(
    onGetStartedClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxWidth()
            .padding(16.dp)
    ) {
        Text(
            text = stringResource(R.string.welcome),
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold
        )
        
        Spacer(modifier = Modifier.height(8.dp))
        
        Button(
            onClick = onGetStartedClick,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(text = stringResource(R.string.get_started))
        }
    }
}

@Preview(showBackground = true)
@Composable
private fun WelcomeSectionPreview() {
    WelcomeSection(onGetStartedClick = {})
}
```

Key conversions:
- `match_parent` → `fillMaxWidth()` / `fillMaxHeight()`
- `wrap_content` → default (no modifier needed)
- `layout_marginTop` → `Spacer` between elements
- Click listeners → lambda parameters
- IDs → not needed (state hoisting instead)
