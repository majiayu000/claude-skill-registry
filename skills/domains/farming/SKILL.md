---
name: farming-expert
version: 1.0.0
description: Expert-level precision agriculture, farm management systems, crop monitoring, and agtech
category: domains
tags: [agriculture, farming, precision-agriculture, agtech, crop-management]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Farming Expert

Expert guidance for precision agriculture, farm management systems, crop monitoring, IoT sensors, and agricultural technology.

## Core Concepts

### Precision Agriculture
- GPS-guided equipment
- Variable rate technology
- Crop monitoring and sensors
- Soil analysis and mapping
- Drone/satellite imagery
- Automated irrigation systems

### Farm Management
- Crop planning and rotation
- Resource optimization
- Yield prediction
- Weather forecasting integration
- Equipment maintenance
- Financial management

### AgTech Solutions
- IoT sensors (soil, weather)
- Machine learning for yield prediction
- Automated harvesting
- Livestock tracking
- Supply chain integration
- Marketplace platforms

## Farm Management System

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, timedelta
from enum import Enum

class CropType(Enum):
    WHEAT = "wheat"
    CORN = "corn"
    SOYBEANS = "soybeans"
    RICE = "rice"
    VEGETABLES = "vegetables"

class GrowthStage(Enum):
    PLANTED = "planted"
    GERMINATION = "germination"
    VEGETATIVE = "vegetative"
    FLOWERING = "flowering"
    HARVEST_READY = "harvest_ready"
    HARVESTED = "harvested"

@dataclass
class Field:
    field_id: str
    name: str
    area_hectares: float
    soil_type: str
    coordinates: List[tuple]  # GPS polygon
    irrigation_system: str
    drainage_quality: str

@dataclass
class CropCycle:
    cycle_id: str
    field_id: str
    crop_type: CropType
    variety: str
    planting_date: datetime
    expected_harvest_date: datetime
    growth_stage: GrowthStage
    seed_rate: float
    fertilizer_applied: List[dict]
    pesticides_applied: List[dict]
    irrigation_schedule: List[dict]

class FarmManagementSystem:
    """Farm management and crop tracking"""

    def __init__(self, db):
        self.db = db

    def plan_crop_rotation(self, field_id, years=3):
        """Generate crop rotation plan"""
        field = self.db.get_field(field_id)
        history = self.db.get_crop_history(field_id, years=10)

        # Analyze soil nutrients and previous crops
        rotation_plan = []

        # Rules for rotation:
        # - Alternate nitrogen-fixing and nitrogen-demanding crops
        # - Avoid same crop family consecutively
        # - Consider soil health and pest management

        for year in range(years):
            recommended_crop = self.recommend_next_crop(field, history, year)
            rotation_plan.append({
                'year': datetime.now().year + year,
                'crop': recommended_crop,
                'reason': self.explain_recommendation(recommended_crop, history)
            })

        return rotation_plan

    def monitor_crop_health(self, field_id):
        """Monitor crop health using sensor data"""
        field = self.db.get_field(field_id)
        current_crop = self.db.get_current_crop(field_id)

        # Collect sensor data
        soil_moisture = self.get_soil_moisture_data(field_id)
        weather_data = self.get_weather_data(field.coordinates)
        ndvi_data = self.get_ndvi_from_satellite(field.coordinates)

        # Analyze health indicators
        health_score = self.calculate_health_score(
            soil_moisture,
            weather_data,
            ndvi_data,
            current_crop
        )

        alerts = []
        if soil_moisture < current_crop.optimal_moisture_min:
            alerts.append({
                'type': 'irrigation_needed',
                'severity': 'high',
                'message': 'Soil moisture below optimal level'
            })

        if ndvi_data < 0.6:  # Vegetation health threshold
            alerts.append({
                'type': 'crop_stress',
                'severity': 'medium',
                'message': 'NDVI indicates possible crop stress'
            })

        return {
            'field_id': field_id,
            'health_score': health_score,
            'soil_moisture': soil_moisture,
            'ndvi': ndvi_data,
            'alerts': alerts,
            'recommendations': self.generate_recommendations(alerts)
        }

    def predict_yield(self, field_id):
        """Predict crop yield using ML"""
        field = self.db.get_field(field_id)
        current_crop = self.db.get_current_crop(field_id)

        # Features for prediction
        features = {
            'field_area': field.area_hectares,
            'soil_type': field.soil_type,
            'crop_variety': current_crop.variety,
            'days_since_planting': (datetime.now() - current_crop.planting_date).days,
            'total_rainfall': self.get_accumulated_rainfall(field_id),
            'avg_temperature': self.get_avg_temperature(field_id),
            'fertilizer_amount': sum(f['amount'] for f in current_crop.fertilizer_applied),
            'ndvi_avg': self.get_avg_ndvi(field_id)
        }

        # Use trained model to predict yield
        predicted_yield_per_hectare = self.yield_model.predict([features])[0]
        total_yield = predicted_yield_per_hectare * field.area_hectares

        return {
            'field_id': field_id,
            'predicted_yield_kg': total_yield,
            'yield_per_hectare': predicted_yield_per_hectare,
            'confidence': 0.85,
            'expected_harvest_date': current_crop.expected_harvest_date
        }
```

## IoT Sensor Integration

```python
class AgricultureIoT:
    """IoT sensor data collection and analysis"""

    def process_soil_sensor_data(self, sensor_id):
        """Process soil sensor readings"""
        readings = self.db.get_recent_readings(sensor_id, hours=24)

        analysis = {
            'sensor_id': sensor_id,
            'avg_moisture': np.mean([r['moisture'] for r in readings]),
            'avg_temperature': np.mean([r['temperature'] for r in readings]),
            'avg_ph': np.mean([r['ph'] for r in readings]),
            'avg_ec': np.mean([r['ec'] for r in readings]),  # Electrical conductivity
            'nitrogen_level': np.mean([r['nitrogen'] for r in readings]),
            'phosphorus_level': np.mean([r['phosphorus'] for r in readings]),
            'potassium_level': np.mean([r['potassium'] for r in readings])
        }

        # Detect anomalies
        anomalies = []
        if analysis['avg_moisture'] < 20:
            anomalies.append('Low soil moisture - irrigation recommended')
        if analysis['avg_ph'] < 5.5 or analysis['avg_ph'] > 7.5:
            anomalies.append(f'Soil pH out of optimal range: {analysis["avg_ph"]:.1f}')

        analysis['anomalies'] = anomalies

        return analysis

    def automate_irrigation(self, field_id):
        """Automated irrigation control"""
        field = self.db.get_field(field_id)
        soil_moisture = self.get_soil_moisture_data(field_id)
        weather_forecast = self.get_weather_forecast(field.coordinates, days=3)

        # Decision logic
        should_irrigate = False
        duration_minutes = 0

        # Check if irrigation is needed
        if soil_moisture < field.moisture_threshold:
            # Check if rain is expected
            expected_rainfall = sum(day['rainfall_mm'] for day in weather_forecast)

            if expected_rainfall < 10:  # Less than 10mm expected
                should_irrigate = True
                # Calculate irrigation duration
                moisture_deficit = field.moisture_threshold - soil_moisture
                duration_minutes = int(moisture_deficit * field.area_hectares * 60 / field.irrigation_rate)

        if should_irrigate:
            self.activate_irrigation(field_id, duration_minutes)

        return {
            'field_id': field_id,
            'irrigation_activated': should_irrigate,
            'duration_minutes': duration_minutes,
            'reason': 'Soil moisture below threshold' if should_irrigate else 'No irrigation needed'
        }
```

## Weather and Climate Analysis

```python
class WeatherAnalytics:
    """Weather-based agricultural decisions"""

    def analyze_growing_conditions(self, field_id, date_range):
        """Analyze weather suitability for crops"""
        weather_data = self.get_historical_weather(field_id, date_range)

        # Calculate growing degree days (GDD)
        gdd = sum([
            max(0, (day['temp_max'] + day['temp_min']) / 2 - 10)
            for day in weather_data
        ])

        # Analyze frost risk
        frost_days = len([d for d in weather_data if d['temp_min'] < 0])

        # Water balance
        total_rainfall = sum(d['rainfall_mm'] for d in weather_data)
        total_evapotranspiration = sum(d['et_mm'] for d in weather_data)
        water_deficit = total_evapotranspiration - total_rainfall

        return {
            'growing_degree_days': gdd,
            'frost_days': frost_days,
            'total_rainfall_mm': total_rainfall,
            'water_deficit_mm': water_deficit,
            'avg_temperature': np.mean([d['temp_avg'] for d in weather_data]),
            'suitability_score': self.calculate_suitability_score(gdd, frost_days, water_deficit)
        }

    def optimize_planting_date(self, field_id, crop_type):
        """Determine optimal planting date"""
        historical_weather = self.get_historical_weather(field_id, years=10)
        crop_requirements = self.get_crop_requirements(crop_type)

        # Find window with:
        # - Minimal frost risk
        # - Adequate soil temperature
        # - Good rainfall distribution

        optimal_dates = []

        for year_data in historical_weather:
            for date, conditions in year_data.items():
                score = self.score_planting_conditions(
                    conditions,
                    crop_requirements
                )
                optimal_dates.append((date, score))

        # Return best planting window
        best_dates = sorted(optimal_dates, key=lambda x: x[1], reverse=True)[:10]

        return {
            'recommended_planting_window': {
                'start': best_dates[-1][0],
                'end': best_dates[0][0]
            },
            'confidence': np.mean([d[1] for d in best_dates])
        }
```

## Pest and Disease Management

```python
class PestManagement:
    """Pest and disease monitoring and management"""

    def detect_pest_risk(self, field_id):
        """Predict pest pressure"""
        weather_data = self.get_recent_weather(field_id, days=14)
        crop = self.db.get_current_crop(field_id)

        # Environmental factors affecting pests
        avg_temp = np.mean([d['temperature'] for d in weather_data])
        avg_humidity = np.mean([d['humidity'] for d in weather_data])
        rainfall = sum(d['rainfall_mm'] for d in weather_data)

        risk_factors = {
            'temperature_risk': self.assess_temp_risk(avg_temp, crop.crop_type),
            'humidity_risk': self.assess_humidity_risk(avg_humidity),
            'rainfall_risk': self.assess_rainfall_risk(rainfall)
        }

        overall_risk = sum(risk_factors.values()) / len(risk_factors)

        recommendations = []
        if overall_risk > 0.7:
            recommendations.append('Scout fields for pest activity')
            recommendations.append('Consider preventive treatment')
        elif overall_risk > 0.5:
            recommendations.append('Increase monitoring frequency')

        return {
            'field_id': field_id,
            'overall_risk_score': overall_risk,
            'risk_level': 'high' if overall_risk > 0.7 else 'medium' if overall_risk > 0.4 else 'low',
            'risk_factors': risk_factors,
            'recommendations': recommendations
        }

    def analyze_crop_image(self, image_data):
        """Detect diseases from crop images using ML"""
        # Would use computer vision model (CNN) trained on crop diseases
        # Returns detected diseases and confidence scores

        predictions = self.disease_detection_model.predict(image_data)

        return {
            'detected_diseases': predictions['diseases'],
            'confidence': predictions['confidence'],
            'affected_area_percent': predictions['affected_area'],
            'treatment_recommendations': self.get_treatment_plan(predictions['diseases'])
        }
```

## Best Practices

- Use precision agriculture techniques
- Implement crop rotation
- Monitor soil health regularly
- Integrate weather data for decisions
- Use IoT sensors for real-time monitoring
- Apply variable rate technology
- Optimize water usage
- Practice integrated pest management
- Track field-level profitability
- Use data-driven decision making
- Maintain equipment properly
- Follow sustainable practices

## Anti-Patterns

❌ Over-application of inputs
❌ Ignoring soil health
❌ No crop rotation
❌ Manual data collection only
❌ Ignoring weather forecasts
❌ Reactive instead of proactive management
❌ No yield analysis

## Resources

- Precision Agriculture: https://www.ispag.org/
- FAO Agricultural Data: http://www.fao.org/faostat/
- Crop Science Society: https://www.crops.org/
- Agricultural IoT: https://www.iot-agriculturet.com/
