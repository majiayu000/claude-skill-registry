---
name: travel-planner
description: This skill should be used whenever users need help planning trips, creating travel itineraries, managing travel budgets, or seeking destination advice. On first use, collects comprehensive travel preferences including budget level, travel style, interests, and dietary restrictions. Generates detailed travel plans with day-by-day itineraries, budget breakdowns, packing checklists, cultural do's and don'ts, and region-specific schedules. Maintains database of preferences and past trips for personalized recommendations.
---

# Travel Planner

## Overview

This skill transforms Claude into a comprehensive travel planning assistant that maintains your travel preferences and generates detailed, personalized trip plans including itineraries, budget breakdowns, packing lists, and cultural guidelines for any destination.

## When to Use This Skill

Invoke this skill for travel-related tasks:
- Planning trips and creating itineraries
- Budget planning and expense tracking
- Destination research and recommendations
- Packing checklists
- Cultural etiquette and do's/don'ts
- Pre-trip preparation timelines
- Travel preference management

## Workflow

### Step 1: Check for Existing Preferences

Check if travel preferences exist:

```bash
python3 scripts/travel_db.py is_initialized
```

If "false", proceed to Step 2 (Setup). If "true", proceed to Step 3 (Trip Planning).

### Step 2: Initial Preference Collection

When no preferences exist, collect comprehensive travel information:

**Travel Style & Budget:**
- Budget level: budget, mid-range, luxury
- Travel pace: relaxed, moderate, packed
- Accommodation preferences: hostel, hotel, Airbnb, resort
- Travel companions: solo, couple, family, group

**Interests & Activities:**
- Sightseeing & landmarks
- Food & culinary experiences
- Adventure & outdoor activities
- Culture & history
- Beach & relaxation
- Nightlife & entertainment
- Shopping
- Nature & wildlife
- Photography
- Wellness & spa

**Dietary & Health:**
- Dietary restrictions (vegetarian, vegan, allergies)
- Accessibility needs
- Health considerations
- Fitness level

**Languages & Skills:**
- Languages spoken
- Travel experience level
- Comfort with adventure

**Previous Travel:**
- Countries/cities visited
- Favorite destinations
- Bucket list destinations

**Saving Preferences:**

```python
import sys
sys.path.append('[SKILL_DIR]/scripts')
from travel_db import save_preferences

preferences = {
    "travel_style": "adventurous",
    "budget_level": "mid-range",
    "accommodation_preference": ["boutique hotels", "Airbnb"],
    "interests": ["culture", "food", "hiking", "photography"],
    "dietary_restrictions": ["vegetarian"],
    "pace_preference": "moderate",
    "travel_companions": "couple",
    "language_skills": ["English", "Spanish"],
    "previous_destinations": ["Paris", "Tokyo", "Barcelona"],
    "bucket_list": [
        {"destination": "New Zealand", "notes": "Lord of the Rings locations"},
        {"destination": "Peru", "notes": "Machu Picchu"}
    ]
}

save_preferences(preferences)
```

Replace `[SKILL_DIR]` with actual skill path.

### Step 3: Create New Trip

When user wants to plan a trip, gather:

**Essential Information:**
1. **Destination**: City/country
2. **Dates**: Departure and return dates (or flexible date range)
3. **Duration**: Number of days
4. **Budget**: Total budget or daily budget
5. **Purpose**: Vacation, business, special occasion
6. **Must-see/do**: Specific attractions or activities

**Creating Trip:**

```python
from travel_db import add_trip

trip = {
    "destination": {
        "city": "Barcelona",
        "country": "Spain",
        "region": "Catalonia"
    },
    "departure_date": "2025-06-15",
    "return_date": "2025-06-22",
    "duration_days": 7,
    "budget": {
        "total": 2500,
        "currency": "USD"
    },
    "purpose": "vacation",
    "travelers": 2,
    "climate": "warm Mediterranean",
    "activities": ["sightseeing", "food tours", "beach", "architecture"],
    "accommodation": {
        "type": "boutique hotel",
        "location": "Gothic Quarter"
    }
}

trip_id = add_trip(trip, status="current")
```

### Step 4: Research Destination

Use web search to gather current information:

**Essential Research:**
1. **Entry Requirements** - Visa, passport, vaccinations
2. **Best Time to Visit** - Weather, seasons, festivals
3. **Safety Information** - Travel advisories, safe areas, common scams
4. **Cultural Norms** - Do's and don'ts (use `references/cultural_etiquette.md` as guide)
5. **Local Transportation** - Metro, buses, taxis, apps
6. **Top Attractions** - Must-see places with hours and prices
7. **Food Recommendations** - Local specialties, popular restaurants
8. **Neighborhoods** - Where to stay, where to explore
9. **Day Trip Options** - Nearby attractions
10. **Practical Info** - Currency, tipping, power outlets, language

**Search Topics to Cover:**
- "[Destination] visa requirements for [nationality]"
- "[Destination] best time to visit weather"
- "[Destination] cultural do's and don'ts"
- "[Destination] top attractions and activities"
- "[Destination] local transportation guide"
- "[Destination] where to stay neighborhoods"
- "[Destination] food and restaurants"
- "[Destination] scams to avoid"
- "[Destination] budget guide"
- "[Destination] 7-day itinerary"

### Step 5: Generate Detailed Travel Plan

Create comprehensive plan with all components:

**A. Day-by-Day Itinerary**

Structure each day based on user's pace preference and research:

```
Day 1: Arrival & Gothic Quarter
- Morning (9:00 AM): Arrive Barcelona, hotel check-in
- Late Morning (11:00 AM): Walking tour of Gothic Quarter
  - Barcelona Cathedral
  - Plaça Reial
  - Las Ramblas (brief walk)
- Afternoon (2:00 PM): Lunch at Cal Pep (tapas)
- Afternoon (4:00 PM): Picasso Museum
- Evening (7:00 PM): Dinner in El Born neighborhood
- Evening (9:00 PM): Stroll along waterfront

Transportation: Metro from airport (30 min, €5)
Estimated Cost: €120/person (meals, museum, transport)
Notes: Book Picasso Museum tickets online in advance
```

Repeat for each day, ensuring:
- Logical geographic grouping
- Realistic timing with buffers
- Mix of activity types
- Meal suggestions
- Transportation details
- Estimated costs
- Booking notes

**B. Budget Breakdown**

Use `plan_generator.py` or create manually:

```python
from plan_generator import calculate_budget_breakdown

budget = calculate_budget_breakdown(
    total_budget=2500,
    num_days=7,
    accommodation_level="mid-range"
)
```

Present as:

```
Total Budget: $2,500 (7 days)
Daily Average: $357

Breakdown:
- Accommodation: $875 (35%) - $125/night
  * Boutique hotel in Gothic Quarter
  * Includes breakfast

- Food: $625 (25%) - $89/day
  * Breakfast: Included
  * Lunch: $25-30/person
  * Dinner: $40-50/person
  * Snacks/drinks: $15/day

- Activities: $625 (25%) - $89/day
  * Sagrada Familia: $35
  * Park Güell: $13
  * Picasso Museum: $15
  * Food tour: $95
  * Day trip to Montserrat: $50
  * Other attractions: ~$100

- Transportation: $250 (10%) - $36/day
  * Airport transfers: $35 each way
  * Metro pass (7-day): $40
  * Taxis: ~$100 total

- Miscellaneous: $125 (5%)
  * Tips, emergencies, souvenirs
```

**C. Packing Checklist**

Generate using `plan_generator.py` or based on destination climate/activities:

```python
from plan_generator import generate_packing_checklist

checklist = generate_packing_checklist(
    destination_climate="warm Mediterranean",
    duration_days=7,
    trip_activities=["sightseeing", "beach", "dining"]
)
```

Customize and present:

```
ESSENTIALS:
- [ ] Passport (check 6-month validity)
- [ ] Visa (if required)
- [ ] Travel insurance documents
- [ ] Hotel confirmations
- [ ] Flight tickets
- [ ] Credit cards (notify bank)
- [ ] Euros cash (€200-300)
- [ ] Phone & charger
- [ ] European plug adapter
- [ ] Medications

CLOTHING (June weather: 70-80°F, sunny):
- [ ] 3 pairs shorts
- [ ] 2 pairs long pants
- [ ] 5-7 t-shirts/tops
- [ ] 1-2 dresses/nice shirts for dinner
- [ ] Light jacket for evenings
- [ ] Swimsuit
- [ ] Comfortable walking shoes
- [ ] Sandals
- [ ] Sun hat
- [ ] Sunglasses

ACTIVITIES:
- [ ] Day backpack
- [ ] Reusable water bottle
- [ ] Camera
- [ ] Beach towel (compact)
- [ ] Sunscreen SPF 50
- [ ] Walking tour comfortable shoes
```

**D. Cultural Do's and Don'ts**

Research and present country-specific guidelines (use `references/cultural_etiquette.md` as template):

```
SPAIN / BARCELONA - Cultural Etiquette

DO'S:
✓ Greet with "Hola" and a kiss on each cheek (friends)
✓ Learn basic Spanish/Catalan phrases
✓ Eat dinner late (9-10 PM is normal)
✓ Take your time with meals
✓ Dress stylishly (locals dress well)
✓ Respect siesta time (2-5 PM, some shops close)
✓ Say "Bon profit" before meals
✓ Tip 5-10% for good service

DON'TS:
✗ Don't expect early dinner (restaurants open at 8 PM)
✗ Don't wear beach clothes in city center
✗ Don't assume everyone speaks English
✗ Don't call it Spain - it's Catalunya to locals
✗ Don't rush through meals
✗ Don't yell or be loud in public
✗ Don't take photos in churches during mass

DINING ETIQUETTE:
- Lunch: 2-4 PM
- Dinner: 9-11 PM
- Service charge sometimes included (check bill)
- Say "La cuenta, por favor" for bill
- It's okay to share tapas
- Bread is not free at all restaurants

SAFETY TIPS:
- Watch for pickpockets on Las Ramblas and metro
- Keep bag in front in crowded areas
- Don't leave valuables on beach
- Be cautious accepting help from strangers
- Use official taxis or Uber/Cabify
```

**E. Pre-Trip Preparation Timeline**

Use `plan_generator.py` or create based on departure date:

```python
from plan_generator import generate_pre_trip_checklist

prep_checklist = generate_pre_trip_checklist(
    destination_country="Spain",
    departure_date="2025-06-15"
)
```

Present as timeline:

```
PRE-TRIP CHECKLIST

2 MONTHS BEFORE (April 15):
- [ ] Book flights
- [ ] Book hotel
- [ ] Purchase travel insurance
- [ ] Check passport expiration
- [ ] Research visa requirements
- [ ] Start researching activities

1 MONTH BEFORE (May 15):
- [ ] Book Sagrada Familia tickets (sell out!)
- [ ] Book food tour
- [ ] Book any other popular activities
- [ ] Notify bank of travel dates
- [ ] Set up international phone plan
- [ ] Download offline maps (Google Maps, Citymapper)
- [ ] Make dinner reservations (popular restaurants)

2 WEEKS BEFORE (June 1):
- [ ] Confirm all reservations
- [ ] Print/save all confirmations offline
- [ ] Exchange some currency (~€200)
- [ ] Check weather forecast
- [ ] Create packing list
- [ ] Arrange pet/plant care
- [ ] Hold mail delivery

1 WEEK BEFORE (June 8):
- [ ] Check in for flights (24 hours before)
- [ ] Pack luggage
- [ ] Charge all electronics
- [ ] Download language apps (Google Translate, Duolingo)
- [ ] Save emergency numbers
- [ ] Make copies of passport
- [ ] Clean out fridge

DAY BEFORE (June 14):
- [ ] Re-check flight time
- [ ] Prepare carry-on
- [ ] Take out trash
- [ ] Adjust thermostat
- [ ] Unplug electronics
- [ ] Set multiple alarms for departure
```

### Step 6: Track Trip and Budget

During the trip, track expenses:

```python
from travel_db import add_expense

expense = {
    "category": "food",
    "amount": 45.00,
    "description": "Dinner at Cervecería Catalana",
    "date": "2025-06-16"
}

add_expense(trip_id, expense)
```

View budget status:

```python
from travel_db import get_budget_summary

summary = get_budget_summary(trip_id)
# Shows: total_budget, spent, remaining, percentage_used, by_category
```

### Step 7: Post-Trip Updates

After trip, move to past trips and update:

```python
from travel_db import move_trip_to_past, add_previous_destination

move_trip_to_past(trip_id)
add_previous_destination("Barcelona, Spain")
```

## Best Practices

1. **Research Thoroughly** - Use web search for current, accurate information
2. **Be Realistic** - Don't over-schedule; allow for rest and spontaneity
3. **Book Ahead** - Popular attractions sell out, especially in peak season
4. **Budget Buffer** - Add 10-20% extra for unexpected costs
5. **Cultural Respect** - Research and follow local customs
6. **Safety First** - Check travel advisories, register with embassy
7. **Stay Flexible** - Weather and circumstances change
8. **Document Everything** - Save confirmations, important info offline

## Example Interaction

```
User: "I want to plan a 7-day trip to Barcelona in June"

Claude: [Checks preferences - finds initialized]

Great! I'll create a detailed travel plan for Barcelona. Based on your preferences,
I know you enjoy culture, food, and moderate-paced travel with a mid-range budget.

First, a few questions:
1. What are your exact travel dates?
2. What's your total budget?
3. Any specific must-see attractions?
4. Traveling solo or with someone?

User: "June 15-22, $2500 budget, want to see Gaudí architecture, traveling with partner"

Claude: [Creates trip in database, performs web research]

Perfect! I've created your Barcelona trip plan. Let me present the complete itinerary:

[Generates detailed 7-day itinerary with Sagrada Familia, Park Güell, Casa Batlló, etc.]
[Creates budget breakdown: $2500 over 7 days]
[Generates packing checklist for June Mediterranean weather]
[Provides Spanish cultural do's and don'ts]
[Creates timeline of pre-trip tasks]

Key highlights:
✓ Day 2: Sagrada Familia (book tickets NOW - they sell out)
✓ Day 4: Food tour in El Born (€95/person, worth it!)
✓ Day 6: Day trip to Montserrat
✓ Budget: $357/day average (€325)
✓ Accommodation: €125/night in Gothic Quarter

Important notes:
- Book Sagrada Familia tickets immediately
- Dinner reservations needed for Tickets Bar, Cervecería Catalana
- Pickpocket awareness on Las Ramblas
- Bring European plug adapter (Type C/F)

Would you like me to adjust anything in the itinerary?
```

## Technical Notes

**Data Storage:**
- Preferences: `~/.claude/travel_planner/preferences.json`
- Trips: `~/.claude/travel_planner/trips.json`

**CLI Commands:**
```bash
# Check initialization
python3 scripts/travel_db.py is_initialized

# View data
python3 scripts/travel_db.py get_preferences
python3 scripts/travel_db.py get_trips current
python3 scripts/travel_db.py stats

# Generate plan
python3 scripts/plan_generator.py --trip-id <id> --output plan.json

# Export backup
python3 scripts/travel_db.py export > backup.json
```

## Resources

### scripts/travel_db.py
Database management for preferences, trips, budget tracking, itineraries, and travel statistics.

### scripts/plan_generator.py
Generates itineraries, budget breakdowns, packing checklists, and preparation timelines.

### references/travel_guidelines.md
Comprehensive guide for destination research, budget planning, itinerary creation, packing strategies, and safety tips.

### references/cultural_etiquette.md
Templates and guidelines for researching country-specific customs, dress codes, dining etiquette, religious considerations, and common mistakes to avoid.