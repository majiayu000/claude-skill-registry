---
description: Seed test database with users, quiz responses, and meal plans for development
---

## User Input

```text
$ARGUMENTS
```

Options: `basic`, `refund-abuse`, `sla-breach`, or empty (basic)

## Task

Populate database with test data for local development and testing.

### Steps

1. **Parse Scenario**:
   - `basic` or empty: 5 users, 10 quiz responses, 3 meal plans
   - `refund-abuse`: User with 3 refunds in 90 days (tests FR-P-011)
   - `sla-breach`: Manual resolution entry past 4h deadline (tests SLA monitoring)

2. **Create Test Users**:
   ```bash
   cd backend
   python -c "
   from src.models.user import User
   from src.lib.database import SessionLocal
   import bcrypt

   db = SessionLocal()

   users = [
       {'email': 'test1@example.com', 'password': 'password123'},
       {'email': 'test2@example.com', 'password': 'password123'},
       {'email': 'test3@example.com', 'password': 'password123'},
   ]

   for user_data in users:
       user = User(
           email=user_data['email'],
           normalized_email=normalize_email(user_data['email']),
           password_hash=bcrypt.hashpw(user_data['password'].encode(), bcrypt.gensalt())
       )
       db.add(user)

   db.commit()
   print(f'✅ Created {len(users)} test users')
   "
   ```

3. **Create Quiz Responses**:
   ```bash
   python -c "
   from src.models.quiz_response import QuizResponse

   quiz_responses = [
       {
           'email': 'test1@example.com',
           'quiz_data': {
               'step_1': 'female',
               'step_2': 'sedentary',
               'step_20': {'age': 30, 'weight_kg': 70, 'height_cm': 165, 'goal': 'weight_loss'}
           },
           'calorie_target': 1650
       },
       # ... more responses
   ]

   for quiz_data in quiz_responses:
       quiz = QuizResponse(**quiz_data)
       db.add(quiz)

   db.commit()
   print(f'✅ Created {len(quiz_responses)} quiz responses')
   "
   ```

4. **Create Meal Plans**:
   ```bash
   python -c "
   from src.models.meal_plan import MealPlan
   import json

   # Load test meal plan JSON
   with open('tests/fixtures/test_meal_plan_weight_loss.json') as f:
       meal_plan_data = json.load(f)

   meal_plans = [
       {
           'payment_id': 'pay_seed_001',
           'user_email': 'test1@example.com',
           'calorie_target': 1650,
           'preferences_summary': {
               'excluded_foods': ['beef'],
               'preferred_proteins': ['chicken', 'salmon'],
               'dietary_restrictions': 'No dairy'
           },
           'pdf_url': 'https://blob.vercel-storage.com/test_001.pdf',
           'status': 'completed'
       }
   ]

   for mp_data in meal_plans:
       meal_plan = MealPlan(**mp_data)
       db.add(meal_plan)

   db.commit()
   print(f'✅ Created {len(meal_plans)} meal plans')
   "
   ```

5. **Scenario: Refund Abuse**:
   ```bash
   # Create user with 3 refunds in 90 days
   python -c "
   from src.models.meal_plan import MealPlan
   from datetime import datetime, timedelta

   user_email = 'refund-abuser@example.com'

   # Create 3 refunded meal plans within 90 days
   for i in range(3):
       meal_plan = MealPlan(
           payment_id=f'pay_refund_{i}',
           user_email=user_email,
           calorie_target=1650,
           status='refunded',
           refund_count=1,
           created_at=datetime.utcnow() - timedelta(days=30*i)
       )
       db.add(meal_plan)

   db.commit()
   print('✅ Created refund abuse scenario (3 refunds in 90 days)')
   "
   ```

6. **Scenario: SLA Breach**:
   ```bash
   # Create manual resolution entry past deadline
   python -c "
   from src.models.manual_resolution import ManualResolution
   from datetime import datetime, timedelta

   breach = ManualResolution(
       payment_id='pay_sla_breach_001',
       user_email='sla-breach@example.com',
       issue_type='ai_generation_failed',
       sla_deadline=datetime.utcnow() - timedelta(hours=2),  # 2h past deadline
       status='pending'
   )

   db.add(breach)
   db.commit()
   print('✅ Created SLA breach scenario (2h past deadline)')
   "
   ```

7. **Output Summary**:
   ```
   ✅ Database Seeding Complete
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Scenario: [basic/refund-abuse/sla-breach]

   Created:
   ✅ 5 users
   ✅ 10 quiz responses
   ✅ 3 meal plans
   [+ scenario-specific data]

   Test Credentials:
   📧 test1@example.com / password123
   📧 test2@example.com / password123
   📧 test3@example.com / password123

   Payment IDs:
   💳 pay_seed_001 (completed)
   💳 pay_seed_002 (completed)
   💳 pay_seed_003 (processing)

   Database: [connection string]
   ```

## Example Usage

```bash
/seed-data                # Basic test data
/seed-data refund-abuse   # Test refund abuse detection
/seed-data sla-breach     # Test SLA monitoring
```

## Exit Criteria

- Test data inserted into database
- Users, quiz responses, and meal plans created
- Scenario-specific data added (if requested)
- Test credentials provided
