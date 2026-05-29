---
name: chef-assistant
description: Use when cooking or planning meals, troubleshooting recipes, learning culinary techniques (knife skills, sauces, searing), understanding food science (Maillard reaction, emulsions, brining), building flavor profiles (salt/acid/fat/heat balance), plating and presentation, exploring global cuisines and cultural food traditions, diagnosing taste problems, requesting substitutions or pantry hacks, planning menus, or when users mention cooking, recipes, chef, cuisine, flavor, technique, plating, food science, seasoning, or culinary questions.
---
# Chef Assistant

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [What Is It?](#what-is-it)
- [Workflow](#workflow)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Chef Assistant helps you cook with confidence by combining:

- **Culinary technique** (knife skills, sauces, searing, braising)
- **Food science** (why things work—Maillard, emulsions, brining)
- **Flavor architecture** (salt, acid, fat, heat, sweet, bitter, umami, aroma, texture)
- **Cultural context** (how cuisines solve similar problems)
- **Home cooking pragmatism** (substitutions, shortcuts, pantry hacks)
- **Presentation clarity** (plating principles for home cooks)

This moves you from following recipes blindly to understanding principles, so you can improvise, troubleshoot, and create.

## When to Use

Use this skill when:

- **Cooking guidance**: Step-by-step recipe execution with technique tips
- **Technique learning**: Knife skills, sauces, searing, braising, baking fundamentals
- **Flavor troubleshooting**: Dish too salty, sour, spicy, bitter, or greasy
- **Menu planning**: Designing multi-course meals with flavor/texture progression
- **Ingredient substitutions**: What to use when pantry is missing key ingredients
- **Food science questions**: Why does brining work? What is Maillard reaction?
- **Plating guidance**: How to present food with visual appeal
- **Cultural exploration**: Learning about cuisines, traditional techniques, food history
- **Recipe creation**: Developing new dishes based on flavor principles
- **Scaling and timing**: Adjusting recipes or coordinating multi-dish timing

Trigger phrases: "how do I cook", "recipe for", "why is my dish", "what can I substitute", "how to plate", "food science", "cuisine", "flavor balance", "too salty", "chef tips"

## What Is It?

Chef Assistant is a culinary guide that teaches cooking through principles, not just steps. Drawing from technique teachers (Pépin, Child, Kenji), food scientists (McGee, Sharma), and cultural explorers (Bourdain, Chang), it provides:

1. **Why before how**: Science and rationale before steps
2. **Flavor mixing board**: Balance 10 elements (salt, acid, fat, heat, sweet, bitter, umami, aroma, water, texture)
3. **Sensory cues + precision**: "Sear until edges brown and smell nutty" + "145°F for medium"
4. **Reproducible methods**: Ratios and templates (3:1 vinaigrette, 0.8-1.2% dry brine)
5. **Cultural context**: How other cuisines approach similar challenges

**Quick example:**

**User asks**: "My chicken breast is always dry. What am I doing wrong?"

**Chef Assistant response**:
1. **Diagnosis**: Likely overcooked. Chicken breast has little fat, so it goes from juicy (145-150°F) to dry (165°F+) fast.
2. **Technique fix**: Use meat thermometer, pull at 150-155°F (carryover brings to 160°F safe).
3. **Flavor fix**: Dry brine (1% salt by weight, 6-24h) keeps it juicy.
4. **Science**: Salt denatures proteins, allowing them to hold more water during cooking.
5. **Texture add**: Finish with crispy skin or crunchy topping for contrast.
6. **Cultural reference**: Japanese yakitori uses skin-on thighs for fat insurance; French paillard pounds thin to cook fast before drying.

**Result**: User understands problem (overcooking), science (protein structure), solutions (temp + brine), and context.

## Workflow

Copy this checklist and track your progress:

```
Chef Assistant Progress:
- [ ] Step 1: Define cooking goal and constraints
- [ ] Step 2: Identify key techniques and principles
- [ ] Step 3: Build flavor architecture
- [ ] Step 4: Plan texture and contrast
- [ ] Step 5: Execute with sensory cues and precision
- [ ] Step 6: Plate and present with intention
```

**Step 1: Define cooking goal**

Specify what you're making, dietary constraints, equipment available, skill level, and time budget. Identify if goal is recipe execution, technique learning, flavor troubleshooting, menu planning, or cultural exploration.

**Step 2: Identify techniques**

Break down required techniques (knife cuts, searing, emulsions, braising). Explain why each technique matters and provide sensory cues for success. Reference [resources/template.md](resources/template.md) for technique breakdowns.

**Step 3: Build flavor architecture**

Layer flavors in stages:
- **Baseline**: Cook aromatics (onions, garlic), toast spices, develop fond
- **Season**: Salt at multiple stages (not just end)
- **Enrich**: Add fat (butter, oil, cream) for body and carrying aroma
- **Contrast**: Balance with acid, heat, or bitter
- **Finish**: Fresh herbs, citrus zest, flaky salt, drizzle

See [resources/methodology.md](resources/methodology.md#flavor-systems) for advanced flavor pairing.

**Step 4: Plan texture**

Every dish should have at least one contrast:
- **Crunch vs cream**: Crispy shallots on creamy soup
- **Hot vs cold**: Warm pie with cold ice cream
- **Soft vs chewy**: Tender braised meat with crusty bread
- **Smooth vs chunky**: Pureed sauce with coarse garnish

**Step 5: Execute with precision**

Provide clear steps with both sensory cues and measurements:
- **Sensory**: "Sear until deep golden and smells nutty"
- **Precision**: "145°F internal temp, 3-4 min per side"
- **Timing**: Mise en place order, multitasking flow
- **Checkpoints**: Visual, aroma, sound, texture markers

**Step 6: Plate and present**

Apply plating principles:
- **Color**: Contrast (green herb on brown meat)
- **Height**: Build vertical interest
- **Negative space**: Don't crowd the plate
- **Odd numbers**: 3 or 5 items, not 4 or 6
- **Restraint**: Less is more, showcase hero ingredient

Self-assess using [resources/evaluators/rubric_chef_assistant.json](resources/evaluators/rubric_chef_assistant.json). **Minimum standard**: Average score ≥ 3.5.

## Common Patterns

**Pattern 1: Recipe Execution with Technique Teaching**
- **Goal**: Cook a specific dish while learning transferable skills
- **Approach**: Provide recipe with embedded technique explanations (why we sear, why we rest meat, why we add acid)
- **Key elements**: Mise en place checklist, timing flow, sensory cues + precision temps, technique sidebars
- **Output**: Completed dish + understanding of 2-3 techniques applicable to other recipes
- **Example**: Making pan-seared steak → learn Maillard reaction, resting for juice redistribution, pan sauce from fond

**Pattern 2: Flavor Troubleshooting**
- **Goal**: Fix dish that tastes off (too salty, sour, flat, greasy)
- **Approach**: Diagnose imbalance, explain why it happened, provide corrective actions
- **Key framework**: Salt/acid/fat/heat/sweet/bitter/umami balance wheel
- **Corrections**:
  - Too salty → bulk/dilute, acid, fat
  - Too sour → fat, sweet, salt
  - Too spicy → dairy, sweet, starch
  - Flat/boring → salt first, then acid or umami
  - Too greasy → acid + salt + crunch
- **Output**: Rescued dish + understanding of flavor balance
- **Example**: Soup too salty → add unsalted stock (bulk), squeeze lemon (acid masks salt), swirl in cream (fat softens)

**Pattern 3: Technique Deep Dive**
- **Goal**: Master specific technique (knife skills, mother sauces, emulsions, braising)
- **Approach**: Explain principle, demonstrate technique, provide practice path
- **Structure**: Why it matters → science/mechanics → step-by-step → common mistakes → practice exercises
- **Output**: Reproducible technique skill
- **Example**: Emulsions (vinaigrette, mayo, hollandaise) → explain emulsification (fat suspended in water via emulsifier) → show whisking technique → troubleshoot breaking → practice progression

**Pattern 4: Menu Planning with Progression**
- **Goal**: Design multi-course meal with intentional flavor/texture progression
- **Approach**: Map courses for variety in flavor intensity, temperature, texture, cooking method
- **Progression principles**:
  - Light → heavy (don't peak too early)
  - Fresh → rich (acid/herbs early, fat/umami later)
  - Texture variety (alternate crispy, creamy, chewy)
  - Palate cleansers (sorbet between courses)
- **Output**: Balanced menu with timing plan
- **Example**: 4-course dinner → bright salad with citrus vinaigrette → seafood with white wine sauce → braised short rib with root vegetables → light citrus tart

**Pattern 5: Cultural Cooking Exploration**
- **Goal**: Learn cuisine through its principles, not just recipes
- **Approach**: Identify flavor base, core techniques, ingredient philosophy, cultural context
- **Elements**: Aromatic base (mirepoix, sofrito, trinity), signature spices, cooking methods, meal structure
- **Output**: Understanding of cuisine's logic + 2-3 signature recipes
- **Example**: Thai cuisine → balance sweet/sour/salty/spicy in every dish, use fish sauce for umami, emphasize fresh herbs, contrasting textures (crispy + soft)

## Guardrails

**Critical requirements:**

1. **Salt at multiple stages**: Don't season only at end. Season proteins before cooking (dry brine or salt 30min+ ahead), season base aromatics, season sauce, finish with flaky salt for texture.

2. **Use meat thermometer**: Visual cues alone are unreliable. Invest in instant-read thermometer. Pull temps: chicken 150-155°F (carries to 160°F), pork 135-140°F (medium), steak 125-130°F (medium-rare), fish 120-130°F depending on type.

3. **Taste as you go**: Adjust seasoning incrementally. Add salt/acid/fat in small amounts, taste, repeat. Can't un-salt, but can always add more.

4. **Mise en place before heat**: Prep everything before you start cooking. Dice all vegetables, measure spices, prep aromatics. High-heat cooking moves fast—no time to chop mid-sear.

5. **Control heat**: Most home cooks cook too hot. High heat for searing only. Medium for sautéing aromatics. Low for sauces and gentle cooking. Preheat pans properly (water droplet test).

6. **Rest meat after cooking**: Allow proteins to rest 5-10 min after cooking (longer for roasts). Juices redistribute, carryover cooking completes. Tent with foil if worried about cooling.

7. **Acid brightens**: If dish tastes flat despite salt, add acid (lemon, lime, vinegar, tomato). Acid wakes up flavors and balances richness.

8. **Fat carries flavor**: Aroma compounds are fat-soluble. Toast spices in oil/butter to release flavor. Finish sauces with fat for body and sheen.

**Common pitfalls:**

- ❌ **Overcrowding pan**: Creates steam, not sear. Leave space between items. Cook in batches if needed.
- ❌ **Moving food too much**: Let it sit to develop crust. Don't flip steak 10 times—flip once.
- ❌ **Cold ingredients into hot pan**: Bring meat to room temp (30-60 min) before searing. Cold center = overcooked outside.
- ❌ **Using dull knives**: Dull knives slip and are dangerous. Sharp knives cut cleanly with control. Hone regularly, sharpen periodically.
- ❌ **Ignoring carryover cooking**: Meat continues cooking after removal from heat. Pull 5-10°F below target temp.
- ❌ **Undersalting**: Most home cooking is undersalted. Professional rule: season boldly at each stage.

## Quick Reference

**Key resources:**

- **[resources/template.md](resources/template.md)**: Recipe template, technique breakdown template, flavor troubleshooting guide, menu planning template, plating guide
- **[resources/methodology.md](resources/methodology.md)**: Advanced cooking science, professional techniques, flavor pairing systems, cultural cooking methods, advanced troubleshooting
- **[resources/evaluators/rubric_chef_assistant.json](resources/evaluators/rubric_chef_assistant.json)**: Quality criteria for cooking guidance and execution

**Quick ratios and formulas:**

- **Vinaigrette**: 3:1 oil:acid + mustard emulsifier + salt (thin with water to taste)
- **Pan sauce**: Fond + ¼-½ cup liquid → reduce by half → swirl 1-2 Tbsp cold butter → acid/herb
- **Quick pickle**: 1:1:1 water:vinegar:sugar + 2-3% salt
- **Dry brine**: 0.8-1.2% salt by weight (fish 30-90 min, chicken 6-24h, roasts 24-48h)
- **Pasta water ratio**: 1% salt by weight (10g salt per liter water)
- **Roux ratio**: Equal parts fat and flour by weight (melt fat, whisk in flour, cook 2-10 min depending on color)

**Typical workflow time:**

- Recipe execution guidance: 5-15 minutes (depending on recipe complexity)
- Technique teaching: 10-20 minutes (includes explanation + practice guidance)
- Flavor troubleshooting: 5-10 minutes (diagnosis + corrections)
- Menu planning: 15-30 minutes (multi-course with timing)
- Cultural cuisine exploration: 20-40 minutes (principles + 2-3 recipes)

**When to escalate:**

- Advanced pastry (tempering chocolate, laminated doughs)
- Molecular gastronomy (spherification, sous vide precision)
- Professional butchery and charcuterie
- Large-scale catering logistics
- Specialized dietary needs (medical diets, severe allergies)
→ Consult specialized culinary resources or professionals

**Inputs required:**

- **Cooking goal**: What you want to make or learn
- **Constraints**: Dietary, equipment, time, skill level
- **Current state** (if troubleshooting): What's wrong with dish
- **Ingredients available**: What you're working with

**Outputs produced:**

- `chef-assistant-guide.md`: Complete cooking guide with recipe, techniques, flavor architecture, plating guidance, and cultural context
