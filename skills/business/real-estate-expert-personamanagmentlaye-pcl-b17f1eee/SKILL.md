---
name: real-estate-expert
version: 1.0.0
description: Expert-level real estate systems, property management, MLS integration, CRM, virtual tours, and market analysis
category: domains
tags: [real-estate, property, mls, crm, proptech, listings]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Real Estate Expert

Expert guidance for real estate systems, property management, Multiple Listing Service (MLS) integration, customer relationship management, virtual tours, and market analysis.

## Core Concepts

### Real Estate Systems
- Multiple Listing Service (MLS) integration
- Property Management Systems (PMS)
- Customer Relationship Management (CRM)
- Transaction management
- Document management
- Lease management
- Maintenance tracking

### PropTech Solutions
- Virtual tours and 3D walkthroughs
- AI-powered property valuation
- Digital signatures and e-closing
- Smart home integration
- IoT sensors for properties
- Blockchain for title management
- Augmented reality for staging

### Standards and Regulations
- RESO (Real Estate Standards Organization)
- Fair Housing Act compliance
- RESPA (Real Estate Settlement Procedures Act)
- Data privacy (GDPR, CCPA)
- ADA compliance for websites
- NAR Code of Ethics

## Property Listing System

```python
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from enum import Enum

class PropertyType(Enum):
    SINGLE_FAMILY = "single_family"
    CONDO = "condo"
    TOWNHOUSE = "townhouse"
    MULTI_FAMILY = "multi_family"
    LAND = "land"
    COMMERCIAL = "commercial"

class ListingStatus(Enum):
    ACTIVE = "active"
    PENDING = "pending"
    SOLD = "sold"
    WITHDRAWN = "withdrawn"
    EXPIRED = "expired"

@dataclass
class Property:
    """Property information"""
    property_id: str
    mls_number: str
    property_type: PropertyType
    address: dict
    listing_price: Decimal
    bedrooms: int
    bathrooms: float
    square_feet: int
    lot_size: float  # acres
    year_built: int
    description: str
    features: List[str]
    photos: List[str]
    status: ListingStatus
    listing_date: datetime
    listing_agent_id: str
    coordinates: tuple  # (latitude, longitude)

@dataclass
class ShowingRequest:
    """Property showing request"""
    showing_id: str
    property_id: str
    buyer_agent_id: str
    buyer_name: str
    requested_date: datetime
    duration_minutes: int
    status: str  # 'pending', 'confirmed', 'cancelled'
    notes: str

class PropertyListingSystem:
    """Real estate listing management system"""

    def __init__(self):
        self.properties = {}
        self.showings = []
        self.saved_searches = {}

    def create_listing(self,
                      property_data: dict,
                      agent_id: str) -> Property:
        """Create new property listing"""
        property_id = self._generate_property_id()
        mls_number = self._generate_mls_number()

        property = Property(
            property_id=property_id,
            mls_number=mls_number,
            property_type=PropertyType(property_data['property_type']),
            address=property_data['address'],
            listing_price=Decimal(str(property_data['price'])),
            bedrooms=property_data['bedrooms'],
            bathrooms=property_data['bathrooms'],
            square_feet=property_data['square_feet'],
            lot_size=property_data.get('lot_size', 0),
            year_built=property_data['year_built'],
            description=property_data['description'],
            features=property_data.get('features', []),
            photos=property_data.get('photos', []),
            status=ListingStatus.ACTIVE,
            listing_date=datetime.now(),
            listing_agent_id=agent_id,
            coordinates=property_data.get('coordinates', (0, 0))
        )

        self.properties[property_id] = property

        # Notify matching saved searches
        self._notify_saved_searches(property)

        return property

    def search_properties(self, criteria: dict) -> List[Property]:
        """Search properties based on criteria"""
        results = []

        for property in self.properties.values():
            if property.status != ListingStatus.ACTIVE:
                continue

            # Price range
            if 'min_price' in criteria:
                if property.listing_price < Decimal(str(criteria['min_price'])):
                    continue

            if 'max_price' in criteria:
                if property.listing_price > Decimal(str(criteria['max_price'])):
                    continue

            # Bedrooms
            if 'min_bedrooms' in criteria:
                if property.bedrooms < criteria['min_bedrooms']:
                    continue

            # Bathrooms
            if 'min_bathrooms' in criteria:
                if property.bathrooms < criteria['min_bathrooms']:
                    continue

            # Square footage
            if 'min_sqft' in criteria:
                if property.square_feet < criteria['min_sqft']:
                    continue

            # Property type
            if 'property_type' in criteria:
                if property.property_type.value != criteria['property_type']:
                    continue

            # Location-based search (within radius)
            if 'location' in criteria and 'radius_miles' in criteria:
                distance = self._calculate_distance(
                    property.coordinates,
                    criteria['location']
                )
                if distance > criteria['radius_miles']:
                    continue

            results.append(property)

        # Sort by price or other criteria
        if criteria.get('sort_by') == 'price_asc':
            results.sort(key=lambda p: p.listing_price)
        elif criteria.get('sort_by') == 'price_desc':
            results.sort(key=lambda p: p.listing_price, reverse=True)
        elif criteria.get('sort_by') == 'newest':
            results.sort(key=lambda p: p.listing_date, reverse=True)

        return results

    def schedule_showing(self,
                        property_id: str,
                        buyer_agent_id: str,
                        buyer_name: str,
                        requested_date: datetime) -> dict:
        """Schedule property showing"""
        property = self.properties.get(property_id)
        if not property:
            return {'error': 'Property not found'}

        if property.status != ListingStatus.ACTIVE:
            return {'error': 'Property not available for showings'}

        # Check availability
        conflicts = self._check_showing_conflicts(property_id, requested_date)
        if conflicts:
            return {
                'error': 'Time slot not available',
                'conflicts': conflicts
            }

        showing = ShowingRequest(
            showing_id=self._generate_showing_id(),
            property_id=property_id,
            buyer_agent_id=buyer_agent_id,
            buyer_name=buyer_name,
            requested_date=requested_date,
            duration_minutes=30,
            status='pending',
            notes=''
        )

        self.showings.append(showing)

        # Notify listing agent
        self._notify_listing_agent(property.listing_agent_id, showing)

        return {
            'success': True,
            'showing_id': showing.showing_id,
            'status': 'pending_confirmation'
        }

    def calculate_price_per_sqft(self, property: Property) -> Decimal:
        """Calculate price per square foot"""
        if property.square_feet == 0:
            return Decimal('0')

        price_per_sqft = property.listing_price / property.square_feet
        return price_per_sqft.quantize(Decimal('0.01'))

    def generate_cma(self,
                    subject_property: Property,
                    radius_miles: float = 1.0) -> dict:
        """Generate Comparative Market Analysis (CMA)"""
        # Find comparable properties
        comparables = []

        for property in self.properties.values():
            # Skip the subject property
            if property.property_id == subject_property.property_id:
                continue

            # Similar property type
            if property.property_type != subject_property.property_type:
                continue

            # Recently sold (last 6 months)
            if property.status != ListingStatus.SOLD:
                continue

            days_since_sale = (datetime.now() - property.listing_date).days
            if days_since_sale > 180:
                continue

            # Within radius
            distance = self._calculate_distance(
                subject_property.coordinates,
                property.coordinates
            )
            if distance > radius_miles:
                continue

            # Similar size (within 20%)
            size_diff = abs(property.square_feet - subject_property.square_feet)
            size_diff_pct = size_diff / subject_property.square_feet
            if size_diff_pct > 0.2:
                continue

            # Similar bedrooms
            if abs(property.bedrooms - subject_property.bedrooms) > 1:
                continue

            comparables.append(property)

        if not comparables:
            return {'error': 'No comparable properties found'}

        # Calculate statistics
        prices = [float(p.listing_price) for p in comparables]
        price_per_sqft_values = [
            float(self.calculate_price_per_sqft(p)) for p in comparables
        ]

        avg_price = sum(prices) / len(prices)
        avg_price_per_sqft = sum(price_per_sqft_values) / len(price_per_sqft_values)

        # Estimate subject property value
        estimated_value = avg_price_per_sqft * subject_property.square_feet

        return {
            'subject_property_id': subject_property.property_id,
            'comparable_count': len(comparables),
            'comparables': [
                {
                    'property_id': p.property_id,
                    'address': p.address,
                    'price': float(p.listing_price),
                    'square_feet': p.square_feet,
                    'price_per_sqft': float(self.calculate_price_per_sqft(p))
                }
                for p in comparables[:5]  # Top 5 comparables
            ],
            'market_statistics': {
                'average_price': avg_price,
                'average_price_per_sqft': avg_price_per_sqft,
                'min_price': min(prices),
                'max_price': max(prices)
            },
            'estimated_value': estimated_value,
            'suggested_listing_price': estimated_value * 0.98  # Slightly below estimate
        }

    def save_search(self, user_id: str, search_criteria: dict) -> str:
        """Save search criteria for notifications"""
        search_id = self._generate_search_id()

        self.saved_searches[search_id] = {
            'user_id': user_id,
            'criteria': search_criteria,
            'created_at': datetime.now(),
            'active': True
        }

        return search_id

    def _calculate_distance(self, coord1: tuple, coord2: tuple) -> float:
        """Calculate distance between two coordinates (miles)"""
        from math import radians, sin, cos, sqrt, atan2

        lat1, lon1 = radians(coord1[0]), radians(coord1[1])
        lat2, lon2 = radians(coord2[0]), radians(coord2[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        radius_miles = 3959  # Earth's radius in miles
        distance = radius_miles * c

        return distance

    def _check_showing_conflicts(self,
                                property_id: str,
                                requested_date: datetime) -> List[dict]:
        """Check for scheduling conflicts"""
        conflicts = []

        for showing in self.showings:
            if showing.property_id != property_id:
                continue

            if showing.status == 'cancelled':
                continue

            # Check for time overlap (within 1 hour)
            time_diff = abs((showing.requested_date - requested_date).total_seconds() / 3600)
            if time_diff < 1:
                conflicts.append({
                    'showing_id': showing.showing_id,
                    'time': showing.requested_date.isoformat()
                })

        return conflicts

    def _notify_saved_searches(self, property: Property):
        """Notify users with matching saved searches"""
        # Implementation would check saved searches and send notifications
        pass

    def _notify_listing_agent(self, agent_id: str, showing: ShowingRequest):
        """Notify listing agent of showing request"""
        # Implementation would send email/SMS notification
        pass

    def _generate_property_id(self) -> str:
        import uuid
        return f"PROP-{uuid.uuid4().hex[:8].upper()}"

    def _generate_mls_number(self) -> str:
        import uuid
        return f"MLS-{uuid.uuid4().hex[:10].upper()}"

    def _generate_showing_id(self) -> str:
        import uuid
        return f"SHOW-{uuid.uuid4().hex[:8].upper()}"

    def _generate_search_id(self) -> str:
        import uuid
        return f"SEARCH-{uuid.uuid4().hex[:8].upper()}"
```

## Property Valuation and Analytics

```python
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler

class PropertyValuationSystem:
    """AI-powered property valuation"""

    def __init__(self):
        self.model = GradientBoostingRegressor(n_estimators=100)
        self.scaler = StandardScaler()
        self.trained = False

    def train_model(self, training_data: List[dict]):
        """Train valuation model on historical data"""
        features = []
        prices = []

        for property_data in training_data:
            feature_vector = self._extract_features(property_data)
            features.append(feature_vector)
            prices.append(property_data['sold_price'])

        X = np.array(features)
        y = np.array(prices)

        # Scale features
        X_scaled = self.scaler.fit_transform(X)

        # Train model
        self.model.fit(X_scaled, y)
        self.trained = True

    def estimate_value(self, property_data: dict) -> dict:
        """Estimate property value"""
        if not self.trained:
            return {'error': 'Model not trained'}

        features = self._extract_features(property_data)
        features_scaled = self.scaler.transform([features])

        estimated_value = self.model.predict(features_scaled)[0]

        # Calculate confidence interval (simplified)
        confidence_range = estimated_value * 0.1  # ±10%

        return {
            'estimated_value': estimated_value,
            'confidence_interval': {
                'lower': estimated_value - confidence_range,
                'upper': estimated_value + confidence_range
            },
            'price_per_sqft': estimated_value / property_data['square_feet']
        }

    def _extract_features(self, property_data: dict) -> List[float]:
        """Extract features for valuation model"""
        return [
            property_data['square_feet'],
            property_data['bedrooms'],
            property_data['bathrooms'],
            property_data['lot_size'],
            property_data['year_built'],
            property_data.get('garage_spaces', 0),
            property_data.get('stories', 1),
            1 if property_data.get('has_pool', False) else 0,
            1 if property_data.get('has_fireplace', False) else 0,
            property_data.get('neighborhood_score', 50)  # 0-100 scale
        ]

class MarketAnalytics:
    """Real estate market analytics"""

    def calculate_market_trends(self, sales_data: List[dict]) -> dict:
        """Calculate market trends and statistics"""
        if not sales_data:
            return {'error': 'No sales data available'}

        # Calculate metrics
        prices = [s['price'] for s in sales_data]
        days_on_market = [s['days_on_market'] for s in sales_data]

        median_price = np.median(prices)
        avg_price = np.mean(prices)
        avg_days_on_market = np.mean(days_on_market)

        # Calculate price trends (compare recent vs older data)
        recent_data = sales_data[-30:]  # Last 30 sales
        older_data = sales_data[-60:-30]  # Previous 30 sales

        if len(recent_data) > 0 and len(older_data) > 0:
            recent_avg = np.mean([s['price'] for s in recent_data])
            older_avg = np.mean([s['price'] for s in older_data])
            price_change = ((recent_avg - older_avg) / older_avg) * 100
        else:
            price_change = 0

        # Market health indicator
        if avg_days_on_market < 30:
            market_health = "Hot"
        elif avg_days_on_market < 60:
            market_health = "Balanced"
        else:
            market_health = "Slow"

        return {
            'median_price': median_price,
            'average_price': avg_price,
            'average_days_on_market': avg_days_on_market,
            'price_trend_percentage': price_change,
            'market_health': market_health,
            'total_sales': len(sales_data)
        }

    def calculate_inventory_metrics(self, active_listings: List[Property]) -> dict:
        """Calculate inventory and absorption metrics"""
        total_listings = len(active_listings)

        # Calculate average price
        avg_price = np.mean([float(p.listing_price) for p in active_listings])

        # Calculate months of inventory (simplified)
        # Would need sales velocity for accurate calculation
        months_of_inventory = 6.0  # Placeholder

        return {
            'total_active_listings': total_listings,
            'average_listing_price': avg_price,
            'months_of_inventory': months_of_inventory,
            'market_condition': 'Balanced' if 4 <= months_of_inventory <= 6 else
                              'Seller' if months_of_inventory < 4 else 'Buyer'
        }
```

## Lease Management

```python
@dataclass
class Lease:
    """Rental lease agreement"""
    lease_id: str
    property_id: str
    tenant_name: str
    tenant_contact: dict
    start_date: datetime
    end_date: datetime
    monthly_rent: Decimal
    security_deposit: Decimal
    status: str  # 'active', 'expired', 'terminated'
    auto_renew: bool

@dataclass
class MaintenanceRequest:
    """Maintenance request for property"""
    request_id: str
    property_id: str
    tenant_name: str
    category: str  # 'plumbing', 'electrical', 'hvac', etc.
    priority: str  # 'low', 'medium', 'high', 'emergency'
    description: str
    submitted_date: datetime
    status: str  # 'open', 'in_progress', 'completed'
    assigned_to: Optional[str]

class PropertyManagementSystem:
    """Property management for landlords and property managers"""

    def __init__(self):
        self.leases = {}
        self.maintenance_requests = []
        self.rent_payments = []

    def create_lease(self, lease_data: dict) -> Lease:
        """Create new lease agreement"""
        lease_id = self._generate_lease_id()

        lease = Lease(
            lease_id=lease_id,
            property_id=lease_data['property_id'],
            tenant_name=lease_data['tenant_name'],
            tenant_contact=lease_data['tenant_contact'],
            start_date=lease_data['start_date'],
            end_date=lease_data['end_date'],
            monthly_rent=Decimal(str(lease_data['monthly_rent'])),
            security_deposit=Decimal(str(lease_data['security_deposit'])),
            status='active',
            auto_renew=lease_data.get('auto_renew', False)
        )

        self.leases[lease_id] = lease

        # Schedule rent payment reminders
        self._schedule_rent_reminders(lease)

        return lease

    def record_rent_payment(self,
                           lease_id: str,
                           amount: Decimal,
                           payment_date: datetime,
                           payment_method: str) -> dict:
        """Record rent payment"""
        lease = self.leases.get(lease_id)
        if not lease:
            return {'error': 'Lease not found'}

        payment = {
            'payment_id': self._generate_payment_id(),
            'lease_id': lease_id,
            'amount': amount,
            'payment_date': payment_date,
            'payment_method': payment_method,
            'for_month': payment_date.strftime('%Y-%m')
        }

        self.rent_payments.append(payment)

        # Check if payment is late
        expected_date = datetime(payment_date.year, payment_date.month, 1)
        days_late = (payment_date - expected_date).days

        return {
            'success': True,
            'payment_id': payment['payment_id'],
            'days_late': max(0, days_late),
            'late_fee': self._calculate_late_fee(lease, days_late)
        }

    def submit_maintenance_request(self, request_data: dict) -> MaintenanceRequest:
        """Submit maintenance request"""
        request = MaintenanceRequest(
            request_id=self._generate_request_id(),
            property_id=request_data['property_id'],
            tenant_name=request_data['tenant_name'],
            category=request_data['category'],
            priority=request_data.get('priority', 'medium'),
            description=request_data['description'],
            submitted_date=datetime.now(),
            status='open',
            assigned_to=None
        )

        self.maintenance_requests.append(request)

        # Auto-assign emergency requests
        if request.priority == 'emergency':
            self._assign_emergency_maintenance(request)

        return request

    def check_lease_expiration(self) -> List[dict]:
        """Check for expiring leases"""
        expiring_soon = []
        current_date = datetime.now()

        for lease in self.leases.values():
            if lease.status != 'active':
                continue

            days_until_expiration = (lease.end_date - current_date).days

            if 0 < days_until_expiration <= 60:
                expiring_soon.append({
                    'lease_id': lease.lease_id,
                    'property_id': lease.property_id,
                    'tenant_name': lease.tenant_name,
                    'end_date': lease.end_date.isoformat(),
                    'days_remaining': days_until_expiration,
                    'auto_renew': lease.auto_renew
                })

        return expiring_soon

    def _calculate_late_fee(self, lease: Lease, days_late: int) -> Decimal:
        """Calculate late fee for rent payment"""
        if days_late <= 5:  # Grace period
            return Decimal('0')

        # $50 flat fee + $5 per day after grace period
        late_fee = Decimal('50') + (Decimal('5') * (days_late - 5))
        return late_fee

    def _schedule_rent_reminders(self, lease: Lease):
        """Schedule monthly rent payment reminders"""
        # Implementation would schedule reminder emails/notifications
        pass

    def _assign_emergency_maintenance(self, request: MaintenanceRequest):
        """Auto-assign emergency maintenance requests"""
        # Implementation would assign to on-call maintenance staff
        pass

    def _generate_lease_id(self) -> str:
        import uuid
        return f"LEASE-{uuid.uuid4().hex[:8].upper()}"

    def _generate_payment_id(self) -> str:
        import uuid
        return f"PAY-{uuid.uuid4().hex[:8].upper()}"

    def _generate_request_id(self) -> str:
        import uuid
        return f"MAINT-{uuid.uuid4().hex[:8].upper()}"
```

## Best Practices

### Listing Management
- Use high-quality professional photos
- Write compelling property descriptions
- Include virtual tours and 3D walkthroughs
- Update listings immediately when status changes
- Respond to inquiries within 1 hour
- Maintain accurate MLS data
- Use targeted marketing campaigns

### Property Valuation
- Use multiple valuation methods (CMA, AVM, appraisal)
- Consider local market conditions
- Account for property condition and upgrades
- Review comparable sales regularly
- Factor in seasonal trends
- Include neighborhood analysis
- Document valuation methodology

### Lease Management
- Use standardized lease templates
- Conduct thorough tenant screening
- Document property condition (move-in/move-out)
- Maintain security deposit in separate account
- Schedule regular property inspections
- Respond to maintenance requests promptly
- Maintain clear communication with tenants

### Compliance
- Follow Fair Housing Act requirements
- Maintain proper licensing
- Use compliant lease agreements
- Protect tenant privacy
- Follow eviction procedures properly
- Maintain insurance coverage
- Keep accurate financial records

## Anti-Patterns

❌ Poor quality listing photos
❌ Inaccurate property information
❌ Slow response to inquiries
❌ No virtual tour options
❌ Ignoring online reviews
❌ Manual document management
❌ No tenant screening process
❌ Poor maintenance tracking
❌ Inadequate insurance coverage

## Resources

- NAR (National Association of Realtors): https://www.nar.realtor/
- RESO Standards: https://www.reso.org/
- Zillow API: https://www.zillow.com/howto/api/
- Realtor.com API: https://www.realtor.com/
- CoreLogic: https://www.corelogic.com/
- Redfin Data: https://www.redfin.com/
- Fair Housing Act: https://www.hud.gov/fairhousing
