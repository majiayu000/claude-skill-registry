---
name: hospitality-expert
version: 1.0.0
description: Expert-level hotel management, reservation systems, guest services, revenue management, and hospitality technology
category: domains
tags: [hospitality, hotel, reservation, pms, revenue-management]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Hospitality Expert

Expert guidance for hotel management, reservation systems, property management systems (PMS), guest services, revenue management, and hospitality technology solutions.

## Core Concepts

### Hotel Management Systems
- Property Management System (PMS)
- Central Reservation System (CRS)
- Revenue Management System (RMS)
- Channel Manager
- Point of Sale (POS)
- Guest Relationship Management (GRM)
- Housekeeping management

### Technologies
- Mobile check-in/check-out
- Digital key systems
- Guest messaging platforms
- IoT for room automation
- AI chatbots for customer service
- Contactless payments
- Energy management systems

### Standards and Protocols
- HTNG (Hotel Technology Next Generation)
- OpenTravel Alliance standards
- PCI-DSS for payment security
- ADA compliance for accessibility
- Brand standards (if franchise)
- OTA integrations (Booking.com, Expedia)

## Property Management System

```python
from dataclasses import dataclass
from datetime import datetime, timedelta, date
from typing import List, Optional, Dict
from decimal import Decimal
from enum import Enum

class RoomType(Enum):
    STANDARD = "standard"
    DELUXE = "deluxe"
    SUITE = "suite"
    EXECUTIVE = "executive"

class RoomStatus(Enum):
    VACANT_CLEAN = "vacant_clean"
    VACANT_DIRTY = "vacant_dirty"
    OCCUPIED_CLEAN = "occupied_clean"
    OCCUPIED_DIRTY = "occupied_dirty"
    OUT_OF_ORDER = "out_of_order"
    OUT_OF_SERVICE = "out_of_service"

class ReservationStatus(Enum):
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

@dataclass
class Room:
    """Hotel room information"""
    room_number: str
    room_type: RoomType
    floor: int
    status: RoomStatus
    base_rate: Decimal
    features: List[str]
    bed_type: str
    max_occupancy: int
    square_feet: int
    is_smoking: bool

@dataclass
class Reservation:
    """Guest reservation"""
    reservation_id: str
    guest_name: str
    guest_email: str
    guest_phone: str
    room_type: RoomType
    check_in_date: date
    check_out_date: date
    num_adults: int
    num_children: int
    status: ReservationStatus
    rate_per_night: Decimal
    total_amount: Decimal
    special_requests: str
    created_at: datetime
    booking_source: str  # 'direct', 'ota', 'phone', etc.
    assigned_room: Optional[str]

@dataclass
class Folio:
    """Guest folio (bill)"""
    folio_id: str
    reservation_id: str
    room_number: str
    guest_name: str
    charges: List[Dict]
    total_charges: Decimal
    payments: List[Dict]
    balance: Decimal

class PropertyManagementSystem:
    """Hotel property management system"""

    def __init__(self):
        self.rooms = {}
        self.reservations = {}
        self.folios = {}
        self.guests = {}

    def create_reservation(self, reservation_data: dict) -> Reservation:
        """Create new reservation"""
        reservation_id = self._generate_reservation_id()

        # Calculate total amount
        check_in = reservation_data['check_in_date']
        check_out = reservation_data['check_out_date']
        num_nights = (check_out - check_in).days

        rate_per_night = Decimal(str(reservation_data['rate_per_night']))
        total_amount = rate_per_night * num_nights

        reservation = Reservation(
            reservation_id=reservation_id,
            guest_name=reservation_data['guest_name'],
            guest_email=reservation_data['guest_email'],
            guest_phone=reservation_data['guest_phone'],
            room_type=RoomType(reservation_data['room_type']),
            check_in_date=check_in,
            check_out_date=check_out,
            num_adults=reservation_data['num_adults'],
            num_children=reservation_data.get('num_children', 0),
            status=ReservationStatus.CONFIRMED,
            rate_per_night=rate_per_night,
            total_amount=total_amount,
            special_requests=reservation_data.get('special_requests', ''),
            created_at=datetime.now(),
            booking_source=reservation_data.get('booking_source', 'direct'),
            assigned_room=None
        )

        self.reservations[reservation_id] = reservation

        return reservation

    def check_in_guest(self, reservation_id: str) -> dict:
        """Process guest check-in"""
        reservation = self.reservations.get(reservation_id)
        if not reservation:
            return {'error': 'Reservation not found'}

        # Find available room of requested type
        available_room = self._find_available_room(
            reservation.room_type,
            reservation.check_in_date,
            reservation.check_out_date
        )

        if not available_room:
            return {'error': 'No rooms available of requested type'}

        # Assign room
        reservation.assigned_room = available_room.room_number
        reservation.status = ReservationStatus.CHECKED_IN

        # Update room status
        available_room.status = RoomStatus.OCCUPIED_CLEAN

        # Create folio
        folio = self._create_folio(reservation, available_room)

        return {
            'reservation_id': reservation_id,
            'room_number': available_room.room_number,
            'guest_name': reservation.guest_name,
            'check_in_time': datetime.now().isoformat(),
            'check_out_date': reservation.check_out_date.isoformat(),
            'folio_id': folio.folio_id
        }

    def check_out_guest(self, reservation_id: str) -> dict:
        """Process guest check-out"""
        reservation = self.reservations.get(reservation_id)
        if not reservation:
            return {'error': 'Reservation not found'}

        # Get folio
        folio = next(
            (f for f in self.folios.values() if f.reservation_id == reservation_id),
            None
        )

        if not folio:
            return {'error': 'Folio not found'}

        # Check for outstanding balance
        if folio.balance > 0:
            return {
                'error': 'Outstanding balance',
                'balance_due': float(folio.balance)
            }

        # Update reservation status
        reservation.status = ReservationStatus.CHECKED_OUT

        # Update room status
        if reservation.assigned_room:
            room = self.rooms.get(reservation.assigned_room)
            if room:
                room.status = RoomStatus.VACANT_DIRTY

        return {
            'reservation_id': reservation_id,
            'guest_name': reservation.guest_name,
            'check_out_time': datetime.now().isoformat(),
            'total_charges': float(folio.total_charges),
            'folio_summary': {
                'room_charges': float(folio.total_charges),
                'payments_received': float(folio.total_charges - folio.balance)
            }
        }

    def _find_available_room(self,
                            room_type: RoomType,
                            check_in: date,
                            check_out: date) -> Optional[Room]:
        """Find available room of specified type"""
        for room in self.rooms.values():
            if room.room_type != room_type:
                continue

            if room.status not in [RoomStatus.VACANT_CLEAN, RoomStatus.VACANT_DIRTY]:
                continue

            # Check if room is available for date range
            if self._is_room_available(room.room_number, check_in, check_out):
                return room

        return None

    def _is_room_available(self, room_number: str, check_in: date, check_out: date) -> bool:
        """Check if room is available for date range"""
        for reservation in self.reservations.values():
            if reservation.assigned_room != room_number:
                continue

            if reservation.status in [ReservationStatus.CANCELLED, ReservationStatus.NO_SHOW]:
                continue

            # Check for date overlap
            if not (check_out <= reservation.check_in_date or check_in >= reservation.check_out_date):
                return False

        return True

    def _create_folio(self, reservation: Reservation, room: Room) -> Folio:
        """Create guest folio"""
        folio_id = self._generate_folio_id()

        # Calculate room charges
        num_nights = (reservation.check_out_date - reservation.check_in_date).days
        room_charge = reservation.rate_per_night * num_nights

        charges = [{
            'date': datetime.now(),
            'description': f'Room {room.room_number} - {num_nights} nights',
            'amount': float(room_charge)
        }]

        folio = Folio(
            folio_id=folio_id,
            reservation_id=reservation.reservation_id,
            room_number=room.room_number,
            guest_name=reservation.guest_name,
            charges=charges,
            total_charges=room_charge,
            payments=[],
            balance=room_charge
        )

        self.folios[folio_id] = folio

        return folio

    def post_charge(self, folio_id: str, charge_data: dict) -> dict:
        """Post charge to guest folio"""
        folio = self.folios.get(folio_id)
        if not folio:
            return {'error': 'Folio not found'}

        charge = {
            'date': datetime.now(),
            'description': charge_data['description'],
            'amount': float(Decimal(str(charge_data['amount'])))
        }

        folio.charges.append(charge)
        folio.total_charges += Decimal(str(charge_data['amount']))
        folio.balance += Decimal(str(charge_data['amount']))

        return {
            'folio_id': folio_id,
            'charge_posted': charge,
            'new_balance': float(folio.balance)
        }

    def process_payment(self, folio_id: str, payment_data: dict) -> dict:
        """Process payment for folio"""
        folio = self.folios.get(folio_id)
        if not folio:
            return {'error': 'Folio not found'}

        payment_amount = Decimal(str(payment_data['amount']))

        if payment_amount > folio.balance:
            return {'error': 'Payment exceeds balance'}

        payment = {
            'date': datetime.now(),
            'payment_method': payment_data['payment_method'],
            'amount': float(payment_amount)
        }

        folio.payments.append(payment)
        folio.balance -= payment_amount

        return {
            'folio_id': folio_id,
            'payment_processed': payment,
            'remaining_balance': float(folio.balance)
        }

    def get_room_availability(self, check_in: date, check_out: date) -> dict:
        """Get room availability for date range"""
        availability = {}

        for room_type in RoomType:
            available_count = 0

            for room in self.rooms.values():
                if room.room_type == room_type:
                    if self._is_room_available(room.room_number, check_in, check_out):
                        available_count += 1

            availability[room_type.value] = available_count

        return {
            'check_in_date': check_in.isoformat(),
            'check_out_date': check_out.isoformat(),
            'availability': availability
        }

    def _generate_reservation_id(self) -> str:
        import uuid
        return f"RES-{uuid.uuid4().hex[:10].upper()}"

    def _generate_folio_id(self) -> str:
        import uuid
        return f"FOL-{uuid.uuid4().hex[:8].upper()}"
```

## Revenue Management System

```python
import numpy as np

class RevenueManagementSystem:
    """Hotel revenue management and dynamic pricing"""

    def __init__(self):
        self.pricing_rules = []
        self.demand_forecast = {}

    def calculate_dynamic_rate(self,
                              room_type: RoomType,
                              check_in_date: date,
                              days_until_arrival: int,
                              current_occupancy: float,
                              historical_data: dict) -> Decimal:
        """Calculate dynamic room rate"""
        # Base rate
        base_rates = {
            RoomType.STANDARD: Decimal('150'),
            RoomType.DELUXE: Decimal('200'),
            RoomType.SUITE: Decimal('350'),
            RoomType.EXECUTIVE: Decimal('450')
        }

        base_rate = base_rates.get(room_type, Decimal('150'))

        # Demand multiplier based on occupancy
        if current_occupancy > 0.85:
            demand_multiplier = Decimal('1.30')  # High demand
        elif current_occupancy > 0.70:
            demand_multiplier = Decimal('1.15')  # Moderate demand
        elif current_occupancy > 0.50:
            demand_multiplier = Decimal('1.00')  # Normal
        else:
            demand_multiplier = Decimal('0.85')  # Low demand

        # Booking window multiplier
        if days_until_arrival < 7:
            window_multiplier = Decimal('1.20')  # Last minute
        elif days_until_arrival < 14:
            window_multiplier = Decimal('1.10')
        elif days_until_arrival > 60:
            window_multiplier = Decimal('0.90')  # Early bird
        else:
            window_multiplier = Decimal('1.00')

        # Day of week adjustment
        if check_in_date.weekday() in [4, 5]:  # Friday, Saturday
            day_multiplier = Decimal('1.25')
        elif check_in_date.weekday() == 6:  # Sunday
            day_multiplier = Decimal('0.95')
        else:
            day_multiplier = Decimal('1.00')

        # Calculate final rate
        dynamic_rate = base_rate * demand_multiplier * window_multiplier * day_multiplier

        # Round to nearest dollar
        dynamic_rate = dynamic_rate.quantize(Decimal('1'))

        return dynamic_rate

    def forecast_demand(self, start_date: date, days: int) -> dict:
        """Forecast demand for upcoming period"""
        forecast = {}

        for i in range(days):
            forecast_date = start_date + timedelta(days=i)

            # Simplified demand forecast
            # In production, would use ML models
            base_demand = 70.0  # 70% base occupancy

            # Day of week factor
            if forecast_date.weekday() in [4, 5]:  # Weekend
                day_factor = 15
            elif forecast_date.weekday() == 6:
                day_factor = -10
            else:
                day_factor = 0

            # Seasonality factor (simplified)
            month = forecast_date.month
            if month in [6, 7, 8]:  # Summer
                season_factor = 10
            elif month in [12, 1]:  # Holiday season
                season_factor = 15
            else:
                season_factor = 0

            forecasted_occupancy = base_demand + day_factor + season_factor
            forecasted_occupancy = min(100, max(0, forecasted_occupancy))

            forecast[forecast_date.isoformat()] = {
                'date': forecast_date.isoformat(),
                'forecasted_occupancy': forecasted_occupancy,
                'confidence': 'high' if i < 14 else 'medium' if i < 30 else 'low'
            }

        return forecast

    def optimize_inventory(self, total_rooms: int, date_range: tuple) -> dict:
        """Optimize room inventory allocation"""
        # Allocate rooms across different channels
        # Direct bookings, OTAs, corporate contracts, etc.

        allocation = {
            'direct': int(total_rooms * 0.40),  # 40% direct
            'ota': int(total_rooms * 0.35),     # 35% OTAs
            'corporate': int(total_rooms * 0.15),  # 15% corporate
            'walk_in': int(total_rooms * 0.10)  # 10% walk-ins
        }

        return {
            'total_rooms': total_rooms,
            'allocation': allocation,
            'date_range': {
                'start': date_range[0].isoformat(),
                'end': date_range[1].isoformat()
            }
        }

    def calculate_revpar(self, revenue: Decimal, available_rooms: int) -> Decimal:
        """Calculate Revenue Per Available Room"""
        if available_rooms == 0:
            return Decimal('0')

        revpar = revenue / available_rooms
        return revpar.quantize(Decimal('0.01'))

    def calculate_adr(self, revenue: Decimal, rooms_sold: int) -> Decimal:
        """Calculate Average Daily Rate"""
        if rooms_sold == 0:
            return Decimal('0')

        adr = revenue / rooms_sold
        return adr.quantize(Decimal('0.01'))
```

## Guest Services Management

```python
@dataclass
class GuestRequest:
    """Guest service request"""
    request_id: str
    reservation_id: str
    room_number: str
    guest_name: str
    request_type: str  # 'housekeeping', 'maintenance', 'concierge', 'amenity'
    description: str
    priority: str  # 'low', 'medium', 'high'
    status: str  # 'open', 'in_progress', 'completed'
    created_at: datetime
    assigned_to: Optional[str]
    completed_at: Optional[datetime]

class GuestServicesSystem:
    """Guest services and experience management"""

    def __init__(self):
        self.requests = []
        self.guest_preferences = {}
        self.loyalty_members = {}

    def submit_guest_request(self, request_data: dict) -> GuestRequest:
        """Submit guest service request"""
        request = GuestRequest(
            request_id=self._generate_request_id(),
            reservation_id=request_data['reservation_id'],
            room_number=request_data['room_number'],
            guest_name=request_data['guest_name'],
            request_type=request_data['request_type'],
            description=request_data['description'],
            priority=request_data.get('priority', 'medium'),
            status='open',
            created_at=datetime.now(),
            assigned_to=None,
            completed_at=None
        )

        self.requests.append(request)

        # Auto-assign based on request type
        self._auto_assign_request(request)

        return request

    def track_guest_preferences(self, guest_id: str, preferences: dict):
        """Track guest preferences for personalization"""
        self.guest_preferences[guest_id] = {
            'room_preferences': {
                'floor': preferences.get('preferred_floor'),
                'bed_type': preferences.get('bed_type'),
                'view': preferences.get('view_preference')
            },
            'amenities': preferences.get('amenities', []),
            'dietary_restrictions': preferences.get('dietary_restrictions', []),
            'special_occasions': preferences.get('special_occasions', {}),
            'communication_preference': preferences.get('communication', 'email')
        }

    def calculate_guest_satisfaction_score(self, reservation_id: str) -> dict:
        """Calculate guest satisfaction metrics"""
        # Simulate guest satisfaction score
        # In production, would be based on surveys and feedback

        metrics = {
            'overall_satisfaction': 4.5,  # Out of 5
            'check_in_experience': 4.7,
            'room_quality': 4.3,
            'staff_friendliness': 4.8,
            'cleanliness': 4.6,
            'value_for_money': 4.2,
            'likelihood_to_recommend': 9.0  # NPS score (0-10)
        }

        return {
            'reservation_id': reservation_id,
            'satisfaction_metrics': metrics,
            'nps_category': 'promoter' if metrics['likelihood_to_recommend'] >= 9 else
                          'passive' if metrics['likelihood_to_recommend'] >= 7 else
                          'detractor'
        }

    def _auto_assign_request(self, request: GuestRequest):
        """Auto-assign request to staff"""
        # Would implement smart assignment logic
        assignments = {
            'housekeeping': 'housekeeping_team',
            'maintenance': 'maintenance_team',
            'concierge': 'concierge_team',
            'amenity': 'front_desk'
        }

        request.assigned_to = assignments.get(request.request_type, 'front_desk')

    def _generate_request_id(self) -> str:
        import uuid
        return f"REQ-{uuid.uuid4().hex[:8].upper()}"
```

## Best Practices

### Reservations Management
- Implement real-time availability
- Use channel manager for distribution
- Enable mobile booking
- Implement flexible cancellation policies
- Send automated confirmations
- Track booking sources
- Enable group bookings

### Revenue Management
- Implement dynamic pricing
- Monitor competitor rates
- Forecast demand accurately
- Optimize inventory allocation
- Track RevPAR and ADR
- Use yield management strategies
- Analyze booking patterns

### Guest Experience
- Personalize guest interactions
- Enable mobile check-in/out
- Provide digital concierge services
- Track guest preferences
- Respond promptly to requests
- Implement loyalty programs
- Gather feedback systematically

### Operations
- Maintain housekeeping efficiency
- Implement preventive maintenance
- Use automated messaging
- Monitor room status in real-time
- Optimize staff scheduling
- Track operational metrics
- Ensure PCI-DSS compliance

## Anti-Patterns

❌ Manual reservation management
❌ Static pricing year-round
❌ No guest preference tracking
❌ Poor channel management
❌ Slow response to guest requests
❌ No mobile capabilities
❌ Inadequate staff training
❌ Poor data security
❌ No revenue analytics

## Resources

- HTNG (Hotel Technology Next Generation): https://htng.org/
- HSMAI (Hospitality Sales and Marketing Association): https://www.hsmai.org/
- AHLA (American Hotel & Lodging Association): https://www.ahla.com/
- STR (Hotel data and analytics): https://str.com/
- OpenTravel Alliance: https://opentravel.org/
- Hospitality Technology: https://www.hospitalitytech.com/
- Revenue Management Best Practices: https://www.revparguru.com/
