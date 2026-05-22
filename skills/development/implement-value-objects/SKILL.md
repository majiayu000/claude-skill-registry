---
name: implement-value-objects
description: "Step-by-step guide for implementing DDD Value Objects with immutability and validation."
metadata:
  type: implementation
  patterns: ["DDD", "Value Objects"]
---

# Skill: Implement DDD Value Objects

This skill teaches you how to implement Domain-Driven Design value objects following  architectural patterns. You'll learn to create immutable, self-validating types that express domain concepts clearly and prevent invalid data from entering your system.

Value objects are fundamental building blocks in DDD. Unlike entities, they have no identity—they are defined entirely by their attributes. Two value objects with the same attributes are equal. This makes them perfect for representing measurements, quantities, identifiers, and other domain concepts.

## Prerequisites

- Understanding of Clean Architecture principles
- Familiarity with DDD concepts (entities, aggregates, domain layer)
- A domain with concepts that need value objects (measurements, quantities, identifiers)

## Overview

In this skill, you will:
1. Identify value object candidates in your domain
2. Create value objects with constructor validation
3. Implement equality and comparison methods
4. Add domain behavior to value objects
5. Compose complex value objects from simpler ones
6. Write comprehensive tests for value objects

## Step 1: Identify Value Object Candidates

Look for domain concepts defined by attributes rather than identity:

**Measurements**: Temperature, Capacity, Power, StateOfCharge, Distance
**Identifiers**: EmailAddress, PhoneNumber, AssetID
**Composites**: Money (amount + currency), HeatCurve (slope + shift + limits), DateRange

**Rules for Identification:**
- No identity needed—equality based on attributes
- Immutable—cannot change after creation
- Self-validating—constructor ensures valid state
- Replace wholesale—create new instance for new value

## Step 2: Create Value Objects with Constructor Validation

Value objects must validate on construction. If the constructor succeeds, the value is guaranteed valid for its entire lifetime.

### Temperature Value Object

```pseudocode
// core/domain/heating/temperature

CONSTANT ErrInvalidTemperature = Error("temperature must be between -50 and 150 Celsius")

// Temperature represents a validated temperature value in Celsius.
// Immutable - create a new instance for different values.
TYPE Temperature
    celsius Float64  // unexported field enforces immutability
END TYPE

// NewTemperature creates a validated Temperature value object.
CONSTRUCTOR NewTemperature(celsius Float64) RETURNS (Temperature, Error)
    IF celsius < -50 OR celsius > 150 THEN
        RETURN Temperature{}, Error(ErrInvalidTemperature + ": got " + celsius)
    END IF
    RETURN Temperature{celsius: celsius}, nil
END CONSTRUCTOR

// MustTemperature creates a Temperature, panics if invalid.
// Use only in tests or with known-valid values.
CONSTRUCTOR MustTemperature(celsius Float64) RETURNS Temperature
    t, err := NewTemperature(celsius)
    IF err != nil THEN
        PANIC(err)
    END IF
    RETURN t
END CONSTRUCTOR

// Celsius returns the temperature value.
METHOD (t Temperature) Celsius() RETURNS Float64
    RETURN t.celsius
END METHOD

// String provides human-readable representation.
METHOD (t Temperature) String() RETURNS String
    RETURN Format("%.1f°C", t.celsius)
END METHOD
```

Key patterns: unexported field enforces immutability, constructor validation, error wrapping, Must variant for tests.

### EmailAddress Value Object

```pseudocode
// core/domain/identity/email

CONSTANT ErrInvalidEmail = Error("invalid email address format")
CONSTANT emailRegex = Regex("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")

// EmailAddress represents a validated, normalized email address.
TYPE EmailAddress
    value String
END TYPE

// NewEmailAddress creates a validated, normalized EmailAddress.
CONSTRUCTOR NewEmailAddress(email String) RETURNS (EmailAddress, Error)
    normalized := ToLower(Trim(email))
    IF normalized == "" OR Length(normalized) > 254 OR NOT emailRegex.Match(normalized) THEN
        RETURN EmailAddress{}, Error(ErrInvalidEmail + ": " + email)
    END IF
    RETURN EmailAddress{value: normalized}, nil
END CONSTRUCTOR

// String returns the email address.
METHOD (e EmailAddress) String() RETURNS String
    RETURN e.value
END METHOD

// Domain returns the domain part of the email.
METHOD (e EmailAddress) Domain() RETURNS String
    parts := Split(e.value, "@")
    IF Length(parts) == 2 THEN
        RETURN parts[1]
    END IF
    RETURN ""
END METHOD
```

## Step 3: Implement Equality and Comparison Methods

Value objects are defined by their attributes, so equality comparison is fundamental.

```pseudocode
// core/domain/heating/temperature (continued)

// Equals checks equality with another temperature.
METHOD (t Temperature) Equals(other Temperature) RETURNS Boolean
    RETURN t.celsius == other.celsius
END METHOD

// GreaterThan returns true if this temperature exceeds other.
METHOD (t Temperature) GreaterThan(other Temperature) RETURNS Boolean
    RETURN t.celsius > other.celsius
END METHOD

// LessThan returns true if this temperature is below other.
METHOD (t Temperature) LessThan(other Temperature) RETURNS Boolean
    RETURN t.celsius < other.celsius
END METHOD

// Between returns true if temperature is within the range (inclusive).
METHOD (t Temperature) Between(min Temperature, max Temperature) RETURNS Boolean
    RETURN t.celsius >= min.celsius AND t.celsius <= max.celsius
END METHOD
```

### Money with Multi-Field Equality

```pseudocode
// core/domain/billing/money

CONSTANT ErrNegativeAmount = Error("amount cannot be negative")
CONSTANT ErrCurrencyMismatch = Error("cannot compare money with different currencies")

TYPE Currency = String

CONSTANT CurrencyUSD Currency = "USD"
CONSTANT CurrencyEUR Currency = "EUR"

// Money represents a monetary amount with currency.
TYPE Money
    amount   Integer  // Minor units (cents)
    currency Currency
END TYPE

// NewMoney creates a Money value from minor units.
CONSTRUCTOR NewMoney(minorUnits Integer, currency Currency) RETURNS (Money, Error)
    IF minorUnits < 0 THEN
        RETURN Money{}, ErrNegativeAmount
    END IF
    RETURN Money{amount: minorUnits, currency: currency}, nil
END CONSTRUCTOR

// Equals checks if two Money values are identical.
METHOD (m Money) Equals(other Money) RETURNS Boolean
    RETURN m.amount == other.amount AND m.currency == other.currency
END METHOD

// Add returns a new Money with summed amounts.
METHOD (m Money) Add(other Money) RETURNS (Money, Error)
    IF m.currency != other.currency THEN
        RETURN Money{}, ErrCurrencyMismatch
    END IF
    RETURN Money{amount: m.amount + other.amount, currency: m.currency}, nil
END METHOD

METHOD (m Money) String() RETURNS String
    RETURN Format("%d.%02d %s", m.amount / 100, m.amount % 100, m.currency)
END METHOD
```

## Step 4: Add Domain Behavior

Value objects should contain behavior relevant to the domain concept they represent.

### StateOfCharge with Domain Logic

```pseudocode
// core/domain/asset/state_of_charge

CONSTANT ErrInvalidStateOfCharge = Error("state of charge must be between 0 and 100")

// StateOfCharge represents battery charge level as a percentage (0-100).
TYPE StateOfCharge
    percentage Float64
END TYPE

CONSTRUCTOR NewStateOfCharge(percentage Float64) RETURNS (StateOfCharge, Error)
    IF percentage < 0 OR percentage > 100 THEN
        RETURN StateOfCharge{}, Error(ErrInvalidStateOfCharge + ": got " + percentage)
    END IF
    RETURN StateOfCharge{percentage: percentage}, nil
END CONSTRUCTOR

METHOD (s StateOfCharge) Percentage() RETURNS Float64
    RETURN s.percentage
END METHOD

// IsCriticallyLow returns true if charge is below 10%.
METHOD (s StateOfCharge) IsCriticallyLow() RETURNS Boolean
    RETURN s.percentage < 10
END METHOD

// IsLow returns true if charge is below 20%.
METHOD (s StateOfCharge) IsLow() RETURNS Boolean
    RETURN s.percentage < 20
END METHOD

// IsFull returns true if charge is at or above 95%.
METHOD (s StateOfCharge) IsFull() RETURNS Boolean
    RETURN s.percentage >= 95
END METHOD

// CanDischarge returns true if there's enough charge (above 5% reserve).
METHOD (s StateOfCharge) CanDischarge() RETURNS Boolean
    RETURN s.percentage > 5
END METHOD

// AvailableCapacity returns usable kWh (down to 5% reserve).
METHOD (s StateOfCharge) AvailableCapacity(totalKWh Float64) RETURNS Float64
    usable := s.percentage - 5
    IF usable < 0 THEN
        RETURN 0
    END IF
    RETURN totalKWh * (usable / 100)
END METHOD

METHOD (s StateOfCharge) Equals(other StateOfCharge) RETURNS Boolean
    RETURN s.percentage == other.percentage
END METHOD

METHOD (s StateOfCharge) String() RETURNS String
    RETURN Format("%.1f%%", s.percentage)
END METHOD
```

### Capacity with Unit Conversions

```pseudocode
// core/domain/asset/capacity

CONSTANT ErrInvalidCapacity = Error("capacity must be positive")

// Capacity represents energy storage capacity (internally kWh).
TYPE Capacity
    kWh Float64
END TYPE

CONSTRUCTOR NewCapacity(kWh Float64) RETURNS (Capacity, Error)
    IF kWh <= 0 THEN
        RETURN Capacity{}, Error(ErrInvalidCapacity + ": got " + kWh)
    END IF
    RETURN Capacity{kWh: kWh}, nil
END CONSTRUCTOR

METHOD (c Capacity) KWh() RETURNS Float64
    RETURN c.kWh
END METHOD

METHOD (c Capacity) Wh() RETURNS Float64
    RETURN c.kWh * 1000
END METHOD

METHOD (c Capacity) MWh() RETURNS Float64
    RETURN c.kWh / 1000
END METHOD

METHOD (c Capacity) PercentageOf(used Float64) RETURNS Float64
    IF c.kWh == 0 THEN
        RETURN 0
    END IF
    RETURN (used / c.kWh) * 100
END METHOD

METHOD (c Capacity) Equals(other Capacity) RETURNS Boolean
    RETURN c.kWh == other.kWh
END METHOD
```

## Step 5: Compose Complex Value Objects

Complex value objects can be composed from simpler ones.

### HeatCurve Composite Value Object

```pseudocode
// core/domain/heating/heat_curve

CONSTANT ErrInvalidSlope = Error("slope must be between 0.1 and 3.0")
CONSTANT ErrInvalidParallelShift = Error("parallel shift must be between -10 and 10")
CONSTANT ErrInvalidSupplyLimits = Error("min supply must be less than max supply")

// HeatCurve defines outdoor-to-supply temperature relationship.
TYPE HeatCurve
    slope         Float64
    parallelShift Float64
    minSupply     Temperature
    maxSupply     Temperature
END TYPE

// NewHeatCurve creates a validated HeatCurve.
CONSTRUCTOR NewHeatCurve(slope Float64, parallelShift Float64, minSupply Temperature, maxSupply Temperature)
    RETURNS (HeatCurve, Error)
    IF slope < 0.1 OR slope > 3.0 THEN
        RETURN HeatCurve{}, Error(ErrInvalidSlope + ": got " + slope)
    END IF
    IF parallelShift < -10 OR parallelShift > 10 THEN
        RETURN HeatCurve{}, Error(ErrInvalidParallelShift + ": got " + parallelShift)
    END IF
    IF minSupply.GreaterThan(maxSupply) THEN
        RETURN HeatCurve{}, ErrInvalidSupplyLimits
    END IF
    RETURN HeatCurve{
        slope: slope,
        parallelShift: parallelShift,
        minSupply: minSupply,
        maxSupply: maxSupply
    }, nil
END CONSTRUCTOR

METHOD (h HeatCurve) Slope() RETURNS Float64
    RETURN h.slope
END METHOD

METHOD (h HeatCurve) ParallelShift() RETURNS Float64
    RETURN h.parallelShift
END METHOD

METHOD (h HeatCurve) MinSupply() RETURNS Temperature
    RETURN h.minSupply
END METHOD

METHOD (h HeatCurve) MaxSupply() RETURNS Temperature
    RETURN h.maxSupply
END METHOD

// CalculateSupplyTemp determines supply temperature from outdoor temperature.
METHOD (h HeatCurve) CalculateSupplyTemp(outdoor Temperature) RETURNS Temperature
    supply := 20 + h.slope * (20 - outdoor.Celsius()) + h.parallelShift

    IF supply < h.minSupply.Celsius() THEN
        RETURN h.minSupply
    END IF
    IF supply > h.maxSupply.Celsius() THEN
        RETURN h.maxSupply
    END IF
    RETURN MustTemperature(supply)
END METHOD

METHOD (h HeatCurve) Equals(other HeatCurve) RETURNS Boolean
    RETURN h.slope == other.slope AND
        h.parallelShift == other.parallelShift AND
        h.minSupply.Equals(other.minSupply) AND
        h.maxSupply.Equals(other.maxSupply)
END METHOD
```

## Step 6: Test Value Objects

Value objects are pure and side-effect free, making them ideal for unit testing.

```pseudocode
// core/domain/heating/temperature_test

TEST TestNewTemperature
    tests := [
        {name: "valid room temp", celsius: 22.5, wantErr: false},
        {name: "valid minimum", celsius: -50, wantErr: false},
        {name: "valid maximum", celsius: 150, wantErr: false},
        {name: "invalid below min", celsius: -51, wantErr: true},
        {name: "invalid above max", celsius: 151, wantErr: true}
    ]

    FOR EACH tt IN tests DO
        temp, err := NewTemperature(tt.celsius)
        IF tt.wantErr THEN
            ASSERT err != nil
        ELSE
            ASSERT err == nil
            ASSERT temp.Celsius() == tt.celsius
        END IF
    END FOR
END TEST

TEST TestTemperature_Equals
    t1 := MustTemperature(22.5)
    t2 := MustTemperature(22.5)
    t3 := MustTemperature(23.0)

    ASSERT t1.Equals(t2) == true   // equal temperatures should be equal
    ASSERT t1.Equals(t3) == false  // different temperatures should not be equal
END TEST

TEST TestStateOfCharge_DomainBehavior
    tests := [
        {percentage: 5, criticallyLow: true, low: true, full: false, canDischarge: false},
        {percentage: 15, criticallyLow: false, low: true, full: false, canDischarge: true},
        {percentage: 50, criticallyLow: false, low: false, full: false, canDischarge: true},
        {percentage: 95, criticallyLow: false, low: false, full: true, canDischarge: true}
    ]

    FOR EACH tt IN tests DO
        soc := MustStateOfCharge(tt.percentage)
        ASSERT soc.IsCriticallyLow() == tt.criticallyLow
        ASSERT soc.IsLow() == tt.low
        ASSERT soc.IsFull() == tt.full
        ASSERT soc.CanDischarge() == tt.canDischarge
    END FOR
END TEST
```

Use table-driven tests for domain behavior to cover all business rules systematically. Test boundary conditions, domain methods, and ensure `Equals` works correctly for identical and different values.

## Verification Checklist

After implementing your value objects, verify:

- [ ] All value objects are immutable (unexported fields, no setters)
- [ ] Constructor validation ensures only valid states exist
- [ ] Constructors return error for invalid input (not panic)
- [ ] `Must*` variants exist for tests and known-valid values
- [ ] Domain errors are exported for error checking
- [ ] `Equals` method compares all relevant attributes
- [ ] Comparison methods exist where domain-relevant
- [ ] Domain behavior is encapsulated in value object methods
- [ ] Composite value objects accept other value objects (not primitives)
- [ ] `String()` method provides human-readable output
- [ ] Zero value is not valid (forces use of constructor)
- [ ] Table-driven tests cover validation boundaries and domain behavior
