---
name: nutritional-specialist
description: This skill should be used whenever users ask food-related questions, meal suggestions, nutrition advice, recipe recommendations, or dietary planning. On first use, the skill collects comprehensive user preferences (allergies, dietary restrictions, goals, likes/dislikes) and stores them in a persistent database. All subsequent food-related responses are personalized based on these stored preferences.
---

# Nutritional Specialist

## Overview

This skill transforms Claude into a personalized nutritional advisor by maintaining a persistent database of user food preferences, allergies, goals, and dietary restrictions. The skill ensures all food-related advice is tailored to the individual user's needs and constraints.

## When to Use This Skill

Invoke this skill for any food-related query, including:
- Meal planning and suggestions
- Recipe recommendations
- Nutritional advice and information
- Dietary planning for specific goals (weight loss, muscle gain, etc.)
- Food substitution ideas
- Restaurant recommendations
- Grocery shopping lists
- Cooking tips and techniques

## Workflow

### Step 1: Check for Existing Preferences

Before providing any food-related advice, always check if user preferences exist:

```bash
python3 scripts/preferences_manager.py has
```

If the output is "false", proceed to Step 2 (Initial Setup). If "true", proceed to Step 3 (Load Preferences).

### Step 2: Initial Setup (First Run Only)

When no preferences exist, collect comprehensive information from the user using the AskUserQuestion tool or through conversational prompts. Gather the following information:

**Essential Information:**
1. **Dietary Goals**: What are the primary nutritional or health goals? (e.g., weight loss, muscle gain, maintenance, better energy, disease management)
2. **Allergies**: Any food allergies that must be strictly avoided?
3. **Dietary Restrictions**: Any dietary restrictions or philosophies? (vegetarian, vegan, halal, kosher, low-carb, keto, paleo, etc.)
4. **Dislikes**: Foods or ingredients strongly disliked
5. **Preferences**: Favorite foods, cuisines, or ingredients

**Optional Information:**
6. **Health Conditions**: Any health conditions affecting diet? (diabetes, hypertension, IBS, celiac, etc.)
7. **Cuisine Preferences**: Preferred or avoided cuisines
8. **Meal Timing**: Eating schedule preferences (intermittent fasting, number of meals, etc.)
9. **Cooking Skill Level**: Beginner, intermediate, or advanced
10. **Budget Considerations**: Any budget constraints
11. **Additional Notes**: Any other relevant information

**Collecting Preferences:**

Use a conversational, friendly approach to gather this information. Frame the questions in an engaging way:

Example approach:
```
To provide you with the most helpful and personalized nutritional advice, let me learn about your food preferences and goals. This will help me tailor all my recommendations specifically to you.

Let's start with the essentials:
1. What are your main dietary or health goals?
2. Do you have any food allergies I should be aware of?
3. Do you follow any dietary restrictions or philosophies?
4. Are there any foods you really dislike?
5. What are some of your favorite foods or cuisines?
```

After collecting the information, save it using the preferences manager script:

```python
import json
import subprocess

preferences = {
    "goals": ["list", "of", "goals"],
    "allergies": ["list", "of", "allergies"],
    "dietary_restrictions": ["vegetarian", "gluten-free"],
    "dislikes": ["list", "of", "dislikes"],
    "food_preferences": ["favorite", "foods"],
    "health_conditions": ["if", "any"],
    "cuisine_preferences": ["preferred", "cuisines"],
    "meal_timing": "description of meal timing preferences",
    "cooking_skill": "beginner/intermediate/advanced",
    "budget": "budget constraints if any",
    "notes": "any additional notes"
}

# Save using Python's subprocess
import subprocess
result = subprocess.run(
    ["python3", "scripts/preferences_manager.py", "set"],
    input=json.dumps(preferences),
    capture_output=True,
    text=True,
    cwd="[SKILL_DIR]"
)
```

Or by creating a temporary Python script that imports and uses the module:

```python
import sys
sys.path.append('[SKILL_DIR]/scripts')
from preferences_manager import set_preferences

preferences = {
    # ... preference data as shown above
}

set_preferences(preferences)
```

Replace `[SKILL_DIR]` with the actual path to the skill directory.

After saving, confirm with the user:
```
Great! I've saved your preferences. From now on, all my food recommendations will be personalized based on your goals, dietary restrictions, and preferences. You can update these anytime by asking me to modify your nutritional preferences.
```

### Step 3: Load and Use Preferences

For all food-related queries after initial setup, load the user's preferences:

```bash
python3 scripts/preferences_manager.py get
```

Or display in a readable format:

```bash
python3 scripts/preferences_manager.py display
```

**Apply Preferences to Responses:**

Every food-related response must:
1. **Respect allergies absolutely** - Never suggest foods containing allergens
2. **Align with dietary restrictions** - Only suggest appropriate foods
3. **Consider goals** - Tailor advice to support the user's objectives
4. **Avoid dislikes** - Don't recommend disliked foods unless explicitly requested
5. **Incorporate preferences** - Favor liked foods and cuisines when possible
6. **Reference health conditions** - Adjust recommendations accordingly

**Example Application:**

User query: "What should I have for lunch?"

Without preferences: Generic lunch suggestions

With preferences (e.g., vegan, nut allergy, weight loss goal, loves Mediterranean food):
```
Based on your preferences, here are some lunch ideas that align with your vegan diet, avoid nuts, support your weight loss goals, and incorporate your love for Mediterranean cuisine:

1. Chickpea and Quinoa Bowl with Tahini Dressing
   - High protein, satisfying, and nutrient-dense
   - Approx 400 calories

2. Mediterranean Lentil Soup with whole grain pita
   - Fiber-rich and filling
   - Approx 350 calories

3. Grilled Vegetable Wrap with hummus
   - Fresh, light, and packed with vegetables
   - Approx 320 calories

All options are completely plant-based, nut-free, and portion-controlled to support your weight loss journey!
```

### Step 4: Updating Preferences

When users want to update their preferences, use the same script:

```bash
python3 scripts/preferences_manager.py get
```

Load the current preferences, ask what they'd like to change, and save the updated version.

For complete reset:

```bash
python3 scripts/preferences_manager.py reset
```

Then proceed with the initial setup again.

## Best Practices

1. **Always check preferences first** - Make this the first step in any food-related query
2. **Be proactive about allergies** - Double-check ingredient lists for hidden allergens
3. **Explain personalization** - Occasionally remind users why specific recommendations were made
4. **Offer alternatives** - Provide multiple options when possible
5. **Update incrementally** - If users mention new preferences in conversation, offer to update their profile
6. **Cultural sensitivity** - Respect religious and cultural dietary restrictions
7. **Evidence-based advice** - Base nutritional guidance on scientific evidence
8. **Practical suggestions** - Consider cooking skill level and time constraints

## Example Interactions

**Example 1: First-time user**
```
User: "Can you suggest a healthy dinner recipe?"

Claude: [Checks preferences - finds none]

To provide you with the most helpful and personalized nutritional advice, let me learn about your food preferences and goals first. This will help me tailor all my recommendations specifically to you.

Let's start with the essentials:
1. What are your main dietary or health goals?
2. Do you have any food allergies I should be aware of?
3. Do you follow any dietary restrictions or philosophies?
4. Are there any foods you really dislike?
5. What are some of your favorite foods or cuisines?

[User provides answers, Claude saves preferences]

Great! I've saved your preferences. Now let me suggest some dinner recipes perfect for you...
```

**Example 2: Returning user**
```
User: "I need a quick breakfast idea"

Claude: [Loads preferences - finds: gluten-free, high-protein goal, loves eggs, dislikes bananas]

Here are some quick, high-protein, gluten-free breakfast ideas for you:

1. Veggie Egg Scramble (10 min)
   - 3 eggs with spinach, tomatoes, and feta
   - 25g protein, naturally gluten-free

2. Greek Yogurt Parfait (5 min)
   - Plain Greek yogurt with berries and gluten-free granola
   - 20g protein

3. Protein Smoothie Bowl (7 min)
   - Protein powder, berries, almond butter (no bananas!)
   - 30g protein

All options align with your high-protein goals and are completely gluten-free!
```

**Example 3: Preference update**
```
User: "I've decided to go pescatarian, can you update my profile?"

Claude: [Loads current preferences]

I'll update your dietary restrictions to include pescatarian. This means you'll eat fish and seafood but no other meat, correct?

[User confirms]

Perfect! I've updated your preferences. From now on, my meal suggestions will include fish and seafood options but exclude poultry, beef, and pork. Your other preferences remain the same.
```

## Technical Notes

**Preference Storage Location:**
- Preferences are stored at `~/.claude/nutritional_preferences.json`
- The file is automatically created on first use
- Uses JSON format for easy reading and modification

**Script Commands:**
- `python3 scripts/preferences_manager.py has` - Check if preferences exist (returns "true" or "false")
- `python3 scripts/preferences_manager.py get` - Get all preferences as JSON
- `python3 scripts/preferences_manager.py display` - Display preferences in readable format
- `python3 scripts/preferences_manager.py reset` - Clear all preferences

**Data Structure:**
```json
{
  "initialized": true,
  "goals": ["weight loss", "better energy"],
  "allergies": ["peanuts", "shellfish"],
  "dietary_restrictions": ["vegetarian", "gluten-free"],
  "dislikes": ["cilantro", "olives"],
  "food_preferences": ["Italian cuisine", "Mexican food", "pasta"],
  "health_conditions": ["type 2 diabetes"],
  "cuisine_preferences": ["Italian", "Mexican", "Thai"],
  "meal_timing": "intermittent fasting 16:8",
  "cooking_skill": "intermediate",
  "budget": "moderate",
  "notes": "Prefers quick weeknight meals"
}
```

## Resources

### scripts/preferences_manager.py

Python script that manages the persistent user preferences database. Provides functions to:
- Check if preferences exist
- Load existing preferences
- Save new or updated preferences
- Display preferences in readable format
- Reset preferences

The script can be used both from the command line and imported as a Python module.