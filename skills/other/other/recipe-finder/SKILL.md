---
name: recipe_finder
description: Search recipes by ingredients, cuisine, or dietary needs. Get nutrition info, meal plans, and cooking instructions. Use when user asks about cooking, recipes, meals, or food.
version: 1.0.0
author: Workshop Team
---

# Recipe Finder Skill

Find recipes, get nutrition information, and create meal plans using free recipe APIs. Supports searching by ingredients, dietary restrictions, cuisine type, and more.

## When to Use

- User asks for recipe suggestions
- User wants to know what to cook with specific ingredients
- User has dietary restrictions (vegetarian, gluten-free, keto, etc.)
- User asks about nutrition or calories in a recipe
- User wants meal planning help
- User asks about cooking instructions or techniques
- User asks "what can I make with..."

## Available Operations

1. **Recipe Search**: Find recipes by keyword, ingredient, or cuisine
2. **Ingredient-Based Search**: "What can I make with chicken and broccoli?"
3. **Dietary Filtering**: Filter by diet (vegan, keto, paleo) or intolerances
4. **Nutrition Analysis**: Get calorie and nutrient breakdown
5. **Random Recipe**: Get a random recipe for inspiration
6. **Recipe Details**: Get full instructions, ingredients, and nutrition

## Instructions

When a user asks about recipes or cooking:

### Step 1: Understand the Query

Identify what the user needs:
- **Ingredient-based**: "What can I make with [ingredients]?"
- **Cuisine search**: "Give me Italian recipes"
- **Dietary needs**: "Keto dinner ideas"
- **Specific dish**: "How do I make chicken parmesan?"
- **Nutrition focused**: "Low calorie lunch ideas"

### Step 2: Load API Reference

ALWAYS read `references/api_reference.md` before making API calls. The APIs have specific parameter formats.

### Step 3: Choose the Right API

**Option A: TheMealDB (Simpler, Completely Free)**
- Good for: Basic recipe search, random recipes, category browsing
- URL: `https://www.themealdb.com/api/json/v1/1/`
- No API key needed (use "1" as the key)

**Option B: Spoonacular (More Powerful, Free Tier)**
- Good for: Ingredient search, nutrition, dietary filters
- Requires API key (free tier: 150 points/day)
- More detailed data but limited calls

### Step 4: Make the API Call

**TheMealDB Example** (search by name):
```
https://www.themealdb.com/api/json/v1/1/search.php?s=chicken
```

**Spoonacular Example** (search by ingredients):
```
https://api.spoonacular.com/recipes/findByIngredients?ingredients=chicken,broccoli&number=5&apiKey=YOUR_KEY
```

### Step 5: Present Results

Format recipes clearly with:
- Recipe name
- Brief description or cuisine type
- Key ingredients
- Cooking time (if available)
- Dietary info (vegetarian, gluten-free, etc.)
- Link to full recipe or instructions

## Dietary Restriction Mappings

| User Says... | API Parameter |
|--------------|---------------|
| "vegetarian" | `diet=vegetarian` |
| "vegan" | `diet=vegan` |
| "gluten-free" | `intolerances=gluten` |
| "dairy-free" | `intolerances=dairy` |
| "keto" or "low-carb" | `diet=ketogenic` |
| "paleo" | `diet=paleo` |
| "nut-free" | `intolerances=tree nut,peanut` |
| "healthy" | `maxCalories=500` or `diet=whole30` |

## Cuisine Types

TheMealDB categories: American, British, Canadian, Chinese, Croatian, Dutch, Egyptian, Filipino, French, Greek, Indian, Irish, Italian, Jamaican, Japanese, Kenyan, Malaysian, Mexican, Moroccan, Polish, Portuguese, Russian, Spanish, Thai, Tunisian, Turkish, Vietnamese

## Resources

ALWAYS read these before making API calls:
- `references/api_reference.md` - Complete API documentation for both services
- `references/dietary_guide.md` - Detailed dietary restriction information

## Examples

### Example 1: Ingredient-Based Search
User asks: "What can I make with chicken, garlic, and lemon?"

1. Load API reference
2. Use TheMealDB search or Spoonacular findByIngredients
3. Return 3-5 recipe suggestions with names and key details

### Example 2: Dietary Restriction
User asks: "I need gluten-free dinner ideas"

1. Load API reference
2. Use Spoonacular with `intolerances=gluten`
3. Or use TheMealDB and filter results manually
4. Highlight that recipes are gluten-free in response

### Example 3: Quick Recipe
User asks: "Give me an easy pasta recipe"

1. Search TheMealDB for "pasta"
2. Pick a result with simple ingredients
3. Provide full recipe with ingredients and instructions

### Example 4: Nutrition Query
User asks: "How many calories in chicken alfredo?"

1. Search for chicken alfredo recipe
2. Use Spoonacular nutrition endpoint or estimate
3. Provide calorie and macro breakdown per serving

### Example 5: Random Inspiration
User asks: "What should I cook tonight?"

1. Use TheMealDB random endpoint: `/random.php`
2. Present the recipe with ingredients and instructions
3. Offer to find alternatives if they don't like it

## Notes

- TheMealDB is completely free with no limits - prefer it for basic searches
- Spoonacular free tier is 150 points/day (searches cost ~1 point each)
- Always check dietary restrictions before recommending recipes
- Cooking times are estimates - actual time varies by skill level
- Ingredient quantities may need scaling based on servings
- When nutrition data isn't available, note that it's an estimate
