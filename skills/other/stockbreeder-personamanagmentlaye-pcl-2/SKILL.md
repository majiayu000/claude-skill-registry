---
name: stockbreeder-expert
version: 1.0.0
description: Expert-level livestock management, animal health monitoring, breeding programs, and ranch management
category: domains
tags: [livestock, animal-husbandry, breeding, ranch-management, veterinary]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Stockbreeder Expert

Expert guidance for livestock management, animal health monitoring, breeding programs, feed optimization, and ranch operations.

## Core Concepts

### Livestock Management
- Herd/flock management
- Animal identification and tracking
- Health monitoring
- Nutrition and feed management
- Breeding and genetics
- Facility management

### Animal Health
- Disease prevention and control
- Vaccination schedules
- Biosecurity protocols
- Health records
- Veterinary care coordination
- Early warning systems

### Technologies
- RFID ear tags
- Automated feeding systems
- Wearable sensors
- Milking automation
- Genetic analysis
- Precision livestock farming

## Livestock Management System

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, timedelta
from enum import Enum

class AnimalType(Enum):
    CATTLE = "cattle"
    SHEEP = "sheep"
    GOAT = "goat"
    PIG = "pig"
    POULTRY = "poultry"

class HealthStatus(Enum):
    HEALTHY = "healthy"
    OBSERVATION = "observation"
    SICK = "sick"
    QUARANTINE = "quarantine"
    DECEASED = "deceased"

@dataclass
class Animal:
    animal_id: str
    tag_number: str
    type: AnimalType
    breed: str
    sex: str
    birth_date: datetime
    weight_kg: float
    sire_id: Optional[str]
    dam_id: Optional[str]
    health_status: HealthStatus
    location: str
    vaccinations: List[dict]
    treatments: List[dict]

@dataclass
class HealthRecord:
    record_id: str
    animal_id: str
    date: datetime
    type: str  # 'vaccination', 'treatment', 'check-up'
    diagnosis: Optional[str]
    treatment: Optional[str]
    veterinarian_id: Optional[str]
    notes: str
    follow_up_date: Optional[datetime]

class LivestockManagement:
    """Livestock management system"""

    def __init__(self, db):
        self.db = db

    def register_animal(self, animal_data):
        """Register new animal in system"""
        animal = Animal(**animal_data)

        # Generate unique tag if not provided
        if not animal.tag_number:
            animal.tag_number = self.generate_tag_number(animal.type)

        # Create initial health record
        health_record = HealthRecord(
            record_id=generate_id(),
            animal_id=animal.animal_id,
            date=datetime.now(),
            type='registration',
            diagnosis=None,
            treatment=None,
            veterinarian_id=None,
            notes='Initial registration',
            follow_up_date=None
        )

        self.db.save_animal(animal)
        self.db.save_health_record(health_record)

        return animal

    def monitor_animal_health(self, animal_id):
        """Monitor individual animal health"""
        animal = self.db.get_animal(animal_id)
        sensor_data = self.get_sensor_data(animal_id)

        health_indicators = {
            'temperature': sensor_data.get('temperature'),
            'activity_level': sensor_data.get('activity_score'),
            'rumination_time': sensor_data.get('rumination_minutes'),  # For ruminants
            'feeding_behavior': self.analyze_feeding_pattern(animal_id),
            'weight_change': self.calculate_weight_trend(animal_id)
        }

        # Detect health issues
        alerts = []
        if health_indicators['temperature'] > 39.5:  # Cattle normal: 38.5-39.5°C
            alerts.append({
                'severity': 'high',
                'issue': 'Elevated temperature - possible fever',
                'recommendation': 'Veterinary examination recommended'
            })

        if health_indicators['activity_level'] < 0.5:  # Below 50% of normal
            alerts.append({
                'severity': 'medium',
                'issue': 'Reduced activity',
                'recommendation': 'Monitor closely, check for injury or illness'
            })

        return {
            'animal_id': animal_id,
            'tag_number': animal.tag_number,
            'health_indicators': health_indicators,
            'alerts': alerts,
            'health_score': self.calculate_health_score(health_indicators)
        }

    def schedule_vaccinations(self, herd_id):
        """Generate vaccination schedule for herd"""
        animals = self.db.get_herd_animals(herd_id)
        vaccination_schedule = []

        for animal in animals:
            # Check vaccination history
            last_vaccinations = self.db.get_vaccinations(animal.animal_id)

            # Required vaccinations based on animal type and age
            required_vaccines = self.get_required_vaccines(animal)

            for vaccine in required_vaccines:
                last_admin = next(
                    (v for v in last_vaccinations if v['vaccine'] == vaccine['name']),
                    None
                )

                # Check if due
                if not last_admin or self.is_vaccine_due(last_admin, vaccine):
                    vaccination_schedule.append({
                        'animal_id': animal.animal_id,
                        'tag_number': animal.tag_number,
                        'vaccine': vaccine['name'],
                        'due_date': self.calculate_vaccine_due_date(last_admin, vaccine),
                        'priority': vaccine['priority']
                    })

        # Sort by priority and due date
        vaccination_schedule.sort(key=lambda x: (x['priority'], x['due_date']))

        return vaccination_schedule
```

## Breeding Management

```python
class BreedingManagement:
    """Breeding program management"""

    def select_breeding_pairs(self, herd_id, breeding_goals):
        """Select optimal breeding pairs"""
        eligible_males = self.db.get_breeding_males(herd_id)
        eligible_females = self.db.get_breeding_females(herd_id)

        # Score each potential pairing
        breeding_recommendations = []

        for female in eligible_females:
            scores = []

            for male in eligible_males:
                # Check genetic compatibility
                if self.are_related(male, female, max_generations=3):
                    continue  # Skip closely related animals

                # Calculate breeding value
                score = self.calculate_breeding_value(
                    male,
                    female,
                    breeding_goals
                )

                scores.append({
                    'male_id': male.animal_id,
                    'male_tag': male.tag_number,
                    'score': score,
                    'expected_traits': self.predict_offspring_traits(male, female)
                })

            # Get best male for this female
            if scores:
                best_match = max(scores, key=lambda x: x['score'])
                breeding_recommendations.append({
                    'female_id': female.animal_id,
                    'female_tag': female.tag_number,
                    'recommended_male': best_match,
                    'optimal_breeding_date': self.calculate_optimal_breeding_date(female)
                })

        return breeding_recommendations

    def calculate_breeding_value(self, male, female, goals):
        """Calculate breeding value for pair"""
        score = 0

        # Evaluate based on breeding goals
        if 'milk_production' in goals:
            score += (male.genetics['milk_yield'] + female.genetics['milk_yield']) * 0.3

        if 'growth_rate' in goals:
            score += (male.genetics['growth_rate'] + female.genetics['growth_rate']) * 0.3

        if 'disease_resistance' in goals:
            score += (male.genetics['disease_resistance'] + female.genetics['disease_resistance']) * 0.2

        if 'fertility' in goals:
            score += (male.fertility_score + female.fertility_score) * 0.2

        return score

    def track_pregnancy(self, animal_id):
        """Track pregnancy and predict due date"""
        animal = self.db.get_animal(animal_id)
        breeding_record = self.db.get_last_breeding(animal_id)

        if not breeding_record:
            return {'status': 'not_pregnant'}

        # Check pregnancy status
        pregnancy_check = self.db.get_latest_pregnancy_check(animal_id)

        if pregnancy_check and pregnancy_check['confirmed']:
            gestation_period = self.get_gestation_period(animal.type)
            due_date = breeding_record['date'] + timedelta(days=gestation_period)
            days_pregnant = (datetime.now() - breeding_record['date']).days

            # Schedule checkups
            checkup_schedule = self.generate_pregnancy_checkups(
                breeding_record['date'],
                due_date
            )

            return {
                'status': 'pregnant',
                'breeding_date': breeding_record['date'],
                'due_date': due_date,
                'days_pregnant': days_pregnant,
                'days_remaining': (due_date - datetime.now()).days,
                'checkup_schedule': checkup_schedule
            }

        return {'status': 'unknown', 'needs_pregnancy_check': True}
```

## Feed Management

```python
class FeedManagement:
    """Feed optimization and management"""

    def calculate_feed_requirements(self, animal_id):
        """Calculate nutritional requirements"""
        animal = self.db.get_animal(animal_id)

        # Base requirements on:
        # - Weight
        # - Age
        # - Production status (lactating, pregnant, growing)
        # - Activity level

        requirements = {
            'dry_matter_kg': self.calculate_dm_requirement(animal),
            'crude_protein_kg': self.calculate_protein_requirement(animal),
            'energy_mcal': self.calculate_energy_requirement(animal),
            'minerals': self.calculate_mineral_requirements(animal)
        }

        return requirements

    def optimize_feed_ration(self, herd_id):
        """Optimize feed ration for herd"""
        animals = self.db.get_herd_animals(herd_id)
        available_feeds = self.db.get_available_feeds()

        # Group animals by similar requirements
        groups = self.group_animals_by_requirements(animals)

        ration_plans = []

        for group in groups:
            # Linear programming for least-cost ration
            avg_requirements = self.calculate_group_requirements(group['animals'])

            optimal_ration = self.solve_ration_optimization(
                avg_requirements,
                available_feeds
            )

            ration_plans.append({
                'group_id': group['id'],
                'animal_count': len(group['animals']),
                'ration': optimal_ration,
                'daily_cost_per_animal': sum(
                    ingredient['amount'] * ingredient['cost_per_kg']
                    for ingredient in optimal_ration
                ),
                'meets_requirements': True
            })

        return ration_plans

    def monitor_feeding_behavior(self, animal_id):
        """Monitor feeding patterns"""
        feeding_data = self.db.get_feeding_data(animal_id, days=7)

        analysis = {
            'avg_daily_intake_kg': np.mean([d['intake'] for d in feeding_data]),
            'feeding_frequency': len(feeding_data) / 7,
            'intake_variation': np.std([d['intake'] for d in feeding_data]),
            'eating_time_minutes': np.mean([d['duration'] for d in feeding_data])
        }

        # Detect issues
        if analysis['avg_daily_intake_kg'] < expected_intake * 0.8:
            analysis['alert'] = 'Low feed intake - possible health issue'

        return analysis
```

## Herd Analytics

```python
class HerdAnalytics:
    """Herd performance analytics"""

    def analyze_herd_performance(self, herd_id):
        """Comprehensive herd performance analysis"""
        animals = self.db.get_herd_animals(herd_id)

        metrics = {
            'total_animals': len(animals),
            'avg_weight': np.mean([a.weight_kg for a in animals]),
            'avg_age_months': np.mean([
                (datetime.now() - a.birth_date).days / 30
                for a in animals
            ]),
            'health_status_distribution': self.get_health_distribution(animals),
            'mortality_rate': self.calculate_mortality_rate(herd_id),
            'reproduction_rate': self.calculate_reproduction_rate(herd_id),
            'avg_daily_gain': self.calculate_avg_daily_gain(herd_id),
            'feed_conversion_ratio': self.calculate_fcr(herd_id)
        }

        # Financial metrics
        metrics['production_value'] = self.calculate_production_value(herd_id)
        metrics['feed_cost'] = self.calculate_total_feed_cost(herd_id)
        metrics['veterinary_cost'] = self.calculate_vet_costs(herd_id)
        metrics['profit_per_animal'] = (
            metrics['production_value'] -
            metrics['feed_cost'] -
            metrics['veterinary_cost']
        ) / metrics['total_animals']

        return metrics

    def predict_production(self, animal_id, days_ahead=30):
        """Predict animal production (milk, eggs, etc.)"""
        animal = self.db.get_animal(animal_id)
        historical_production = self.db.get_production_history(animal_id, days=90)

        # Use time series model
        forecast = self.production_model.forecast(
            historical_production,
            periods=days_ahead
        )

        return {
            'animal_id': animal_id,
            'forecast_period_days': days_ahead,
            'predicted_production': forecast.tolist(),
            'total_predicted': sum(forecast),
            'confidence_interval': self.calculate_confidence_interval(forecast)
        }
```

## Best Practices

- Use individual animal identification
- Maintain detailed health records
- Implement biosecurity protocols
- Monitor animal welfare continuously
- Practice selective breeding
- Optimize feed efficiency
- Schedule regular veterinary checkups
- Use data for decision-making
- Maintain proper facilities
- Follow animal welfare standards
- Track financial performance
- Implement early disease detection

## Anti-Patterns

❌ Poor record keeping
❌ No biosecurity measures
❌ Reactive health management
❌ Inbreeding
❌ Over or underfeeding
❌ Ignoring animal behavior
❌ Manual data collection only

## Resources

- World Organisation for Animal Health: https://www.oie.int/
- Animal Genetics: https://www.animalgenetics.us/
- Livestock Management Systems: https://www.fao.org/livestock-systems/
- Precision Livestock Farming: https://www.plf.eu/
