---
name: cooklang-formatting
description: Format recipes using Cooklang markup syntax. Use when creating, editing, or converting recipes to Cooklang format. Covers ingredients, equipment, timers, metadata, and file organization.
---

# Cooklang Recipe Formatting

## Style Guidelines (IMPORTANT)

### 1. Capitalize ingredients and equipment
```cook
@Leek{1}           -- correct
@leek{1}           -- wrong

#Pan{}             -- correct
#pan{}             -- wrong
```

### 2. No adjectives inside keywords
Adjectives go BEFORE the keyword, not as part of it:
```cook
large #Pan{}       -- correct
#large pan{}       -- wrong

hot #Skillet{}     -- correct
#hot skillet{}     -- wrong

medium @Onion{1}   -- correct
@medium onion{1}   -- wrong
```

### 3. Prefer metric measurements
Use grams, ml, litres instead of cups. Teaspoons and tablespoons are OK:
```cook
@Flour{250%g}      -- correct
@Flour{2%cups}     -- wrong

@Milk{500%ml}      -- correct
@Milk{2%cups}      -- wrong

@Stock{1%litre}    -- correct
@Stock{4%cups}     -- wrong

@Butter{2%tbsp}    -- OK (tbsp allowed)
@Vanilla{1%tsp}    -- OK (tsp allowed)
```

### 4. Include a recipe image
Save the most appealing frame from the video as an image with the same name:
```
Dinner/Garlic Butter Shrimp.cook
Dinner/Garlic Butter Shrimp.jpg    -- same name, .jpg extension
```

## Quick Reference

| Symbol | Purpose | Example |
|--------|---------|---------|
| `@` | Ingredient | `@Butter{30%g}` |
| `#` | Equipment | `#Frying Pan{}` |
| `~` | Timer | `~{5%minutes}` |
| `---` | Metadata block | YAML frontmatter |
| `==` | Section header | `== Sauce ==` |

## Ingredient Syntax

```
@ingredient                      -- name only (to taste)
@ingredient{quantity}            -- with amount, no unit
@ingredient{quantity%unit}       -- full specification
@multi word ingredient{}         -- braces required for multi-word
@ingredient{qty%unit}(prep)      -- with preparation instructions
```

### Examples
```cook
@Salt{}
@Eggs{3}
@Butter{30%g}
@Chicken Breast{500%g}
@Garlic{3%cloves}(minced)
@Onion{1}(diced)
```

### Notes on Ingredients
- For pantry staples (salt, pepper, oil), just use `@Salt{}` with no quantity
- For optional ingredients, write "optional" in the text: `Add optional @Chilli Flakes{1%tsp} if desired.`
- Don't use `-`, `?`, or `&` prefixes - they're not supported by most Cooklang apps
- **Don't mark cooking water as an ingredient** - water for boiling/blanching is not a shopping list item:
  ```cook
  Bring a large #Pot{} of water to a boil.     -- correct (plain text)
  Bring a large #Pot{} of @Water{} to a boil.  -- wrong (creates ingredient)
  ```

## Equipment Syntax

```cook
#Pot{}
#Frying Pan{}
#Mixing Bowl{}
#Baking Sheet{}
```

Adjectives go before, not inside:
```cook
large #Pot{}           -- correct
#large pot{}           -- wrong
```

## Timer Syntax

```cook
~{5%minutes}
~{30%seconds}
~{1%hour}
~resting{10%minutes}     -- named timer
```

**Important**: Use single values only, NOT ranges. Write `~{15%minutes}` not `~{10-15%minutes}`.
For variable times, pick the middle value or write it in text: "about 10-15 minutes".

## Recipe Structure

### Metadata (YAML Frontmatter)
```cook
---
source: https://example.com/recipe
servings: 4
prep_time: 15 minutes
cook_time: 30 minutes
---
```

Note: `servings` must be a number, not text.

### Steps
Each paragraph becomes a numbered step. Separate steps with blank lines:

```cook
Preheat #Oven{} to 190°C.

Season @Chicken Breast{500%g} with @Salt{} and @Pepper{}.

Bake for ~{25%minutes} until internal temperature reaches 75°C.
```

### Sections
Use `==` for complex recipes with multiple parts:

```cook
== Marinade ==

Combine @Soy Sauce{45%ml} and @Honey{30%g} in a #Bowl{}.

== Main Dish ==

Cook @Chicken{500%g} in the marinade.
```

### Notes
Use `>` prefix for tips:

```cook
> For extra flavor, marinate overnight.
```

## File Organization

Save recipes to category folders using Title Case:

```
Breakfast/Fluffy Pancakes.cook
Lunch/Greek Salad.cook
Dinner/Garlic Butter Shrimp.cook
```

### Categories
- **Breakfast**: Morning meals, eggs, pancakes, smoothies
- **Lunch**: Salads, sandwiches, soups, light meals
- **Dinner**: Main courses, proteins, pasta, substantial meals
- **Sides**: Accompaniments, vegetables
- **Sauces**: Dressings, marinades, condiments
- **Desserts**: Sweets, baked goods
- **Drinks**: Beverages, cocktails

## CLI Commands

If the `cook` CLI is installed:

```bash
cook recipe "path/to/recipe.cook"      # Parse and display
cook recipe "path/to/recipe.cook:2"    # Scale by 2x
cook shopping-list *.cook              # Generate shopping list
cook doctor validate                   # Check for syntax errors
```

## Common Patterns

### Simple Recipe
```cook
---
source: https://tiktok.com/@creator/video/123
servings: 2
---

Heat @Olive Oil{2%tbsp} in a large #Skillet{} over medium heat.

Add @Garlic{3%cloves}(minced) and cook for ~{30%seconds}.

Add @Prawns{450%g} and cook for ~{2%minutes} per side until pink.

Season with @Salt{} and @Pepper{} to taste.
```

### Recipe with Sections
```cook
---
servings: 4
---

== Sauce ==

Whisk @Soy Sauce{3%tbsp}, @Honey{2%tbsp}, and @Sesame Oil{1%tsp}.

== Stir Fry ==

Heat #Wok{} over high heat. Cook @Chicken{500%g}(sliced) for ~{5%minutes}.

Add sauce and toss to coat.
```
