---
description: Test AI meal plan generation with keto compliance and structural validation
handoffs:
  - label: Fix AI Generation Issues
    agent: ai-specialist
    prompt: Fix the AI generation issues identified in the validation report
    send: false
---

## User Input

```text
$ARGUMENTS
```

Profile options: `weight-loss`, `muscle-gain`, `maintenance`, or custom quiz data

## Task

Generate a test meal plan using the AI service and validate keto compliance and structural integrity.

### Steps

1. **Parse Arguments**:
   - `weight-loss`: Use female, sedentary, weight loss profile
   - `muscle-gain`: Use male, very active, muscle gain profile
   - `maintenance`: Use female, moderately active, maintenance profile
   - Empty: Use default weight-loss profile
   - Custom: Parse as JSON quiz data

2. **Prepare Test Quiz Data**:

   **Weight Loss Profile**:
   ```json
   {
     "gender": "female",
     "activity_level": "sedentary",
     "age": 32,
     "weight_kg": 75,
     "height_cm": 165,
     "goal": "weight_loss",
     "excluded_foods": ["beef", "pork"],
     "preferred_proteins": ["chicken", "salmon", "eggs"],
     "dietary_restrictions": "No dairy from cows"
   }
   ```

   **Muscle Gain Profile**:
   ```json
   {
     "gender": "male",
     "activity_level": "very_active",
     "age": 28,
     "weight_kg": 80,
     "height_cm": 180,
     "goal": "muscle_gain",
     "excluded_foods": ["shellfish"],
     "preferred_proteins": ["beef", "chicken", "turkey", "eggs"],
     "dietary_restrictions": "None"
   }
   ```

3. **Calculate Calorie Target**:
   ```bash
   cd backend
   python -c "
   from src.services.calorie_calculator import calculate_calories
   target = calculate_calories(
       gender='[gender]',
       age=[age],
       weight_kg=[weight],
       height_cm=[height],
       activity_level='[activity]',
       goal='[goal]'
   )
   print(f'Calorie Target: {target} kcal/day')
   "
   ```

4. **Generate Meal Plan**:
   ```bash
   cd backend
   python -c "
   import asyncio
   from src.services.meal_plan_generator import generate_meal_plan

   async def test():
       meal_plan = await generate_meal_plan(
           calorie_target=[calorie_target],
           preferences={
               'excluded_foods': [excluded_foods],
               'preferred_proteins': [preferred_proteins],
               'dietary_restrictions': '[dietary_restrictions]'
           }
       )
       return meal_plan

   result = asyncio.run(test())
   print('✅ Meal plan generated successfully')
   print(f'Days: {len(result.days)}')
   "
   ```

5. **Validate Keto Compliance** (FR-A-007):
   ```python
   # Check each day's carbs
   failed_days = []
   for day in meal_plan.days:
       if day.total_carbs > 30:
           failed_days.append({
               'day': day.day,
               'carbs': day.total_carbs
           })

   if failed_days:
       print(f'❌ Keto Compliance FAILED: {len(failed_days)} days exceed 30g carbs')
       for fail in failed_days:
           print(f'  Day {fail["day"]}: {fail["carbs"]}g carbs')
   else:
       print('✅ Keto Compliance PASSED: All 30 days <30g carbs')
   ```

6. **Validate Structural Integrity** (FR-A-015):
   ```python
   # Check structure
   issues = []

   # Must have exactly 30 days
   if len(meal_plan.days) != 30:
       issues.append(f'Expected 30 days, got {len(meal_plan.days)}')

   # Each day must have 3 meals
   for day in meal_plan.days:
       if len(day.meals) != 3:
           issues.append(f'Day {day.day}: Expected 3 meals, got {len(day.meals)}')

   # Must have 4 weekly shopping lists
   if len(meal_plan.shopping_lists) != 4:
       issues.append(f'Expected 4 shopping lists, got {len(meal_plan.shopping_lists)}')

   # All fields must be populated
   for day in meal_plan.days:
       for meal in day.meals:
           if not meal.recipe or not meal.ingredients:
               issues.append(f'Day {day.day} {meal.name}: Missing recipe or ingredients')

   if issues:
       print(f'❌ Structure Validation FAILED: {len(issues)} issues')
       for issue in issues:
           print(f'  - {issue}')
   else:
       print('✅ Structure Validation PASSED')
   ```

7. **Calculate Quality Score**:
   ```
   Quality Score: [X]/10
   - Keto Compliance: [Pass/Fail] (5 points)
   - Structure Valid: [Pass/Fail] (3 points)
   - Variety: [High/Medium/Low] (2 points)

   Generation Time: X.XX seconds
   Model Used: [gpt-4o/gemini-1.5-pro]
   ```

8. **Output Summary**:
   ```
   ✅ AI Meal Plan Validation Report
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Profile: Weight Loss (Female, Sedentary, 32 years)
   Calorie Target: 1650 kcal/day

   Generation Results:
   ✅ Meal plan generated successfully
   ⏱️  Generation time: 18.3s (target: <20s)

   Keto Compliance (FR-A-007):
   ✅ All 30 days <30g carbs
   📊 Average: 22g carbs/day
   📊 Range: 18-28g carbs/day

   Structural Integrity (FR-A-015):
   ✅ Exactly 30 days
   ✅ Each day has 3 meals (breakfast, lunch, dinner)
   ✅ 4 weekly shopping lists included
   ✅ All fields populated

   Quality Score: 9/10 ⭐
   Model: gpt-4o

   Recommendation: ✅ AI output meets quality standards
   ```

9. **Save Results**:
   - Save generated meal plan to `backend/tests/fixtures/test_meal_plan_[profile].json`
   - Can be used for PDF testing

## Example Usage

```bash
/validate-ai                  # Test with default weight-loss profile
/validate-ai weight-loss      # Female, sedentary, weight loss
/validate-ai muscle-gain      # Male, very active, muscle gain
/validate-ai maintenance      # Female, moderate, maintenance
```

## Exit Criteria

- Meal plan generated within 20s timeout
- Keto compliance validated (all days <30g carbs)
- Structural integrity validated (30 days, 3 meals each, 4 shopping lists)
- Quality score calculated
- Results saved for further testing

## Success Criteria (SC-004)

**Target**: 9/10 meal plans must pass keto compliance
- Run this skill 10 times with different profiles
- At least 9 must score ≥8/10
