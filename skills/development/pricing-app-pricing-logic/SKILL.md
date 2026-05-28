---
name: pricing-app-pricing-logic
description: Pricing calculation engine - markup, ML fees, shipping, tiered commissions, multi-currency
license: MIT
metadata:
  author: pricing-app
  version: "1.0.0"
  scope: [backend, root]
  auto_invoke:
    - "Calculating product prices"
    - "Computing ML commissions"
    - "Working with pricing tiers"
    - "Currency conversion (USD/ARS)"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Pricing App - Pricing Logic & Calculations

---

## CRITICAL RULES - NON-NEGOTIABLE

### Pricing Constants
- ALWAYS: Use database-driven constants from `PricingConstants` table
- ALWAYS: Filter by date range (fecha_desde/fecha_hasta) to get active version
- ALWAYS: Provide fallback defaults if no DB constants exist
- NEVER: Hardcode pricing values in business logic

### Currency Handling
- ALWAYS: Store prices in cents (integer) to avoid float precision issues
- ALWAYS: Convert USD to ARS using latest `TipoCambio.venta` rate
- ALWAYS: Fallback to latest available exchange rate if today's is missing
- NEVER: Use float for money calculations (use Decimal or int cents)

### Commission Tiers
- ALWAYS: Use versioned commission system (ComisionVersion, ComisionBase)
- ALWAYS: Map PVP pricelists to Web equivalents (same commissions)
- ALWAYS: Handle tier-based ML fees (different rates by price range)
- NEVER: Assume commission rates are static

### Markup Calculation
- ALWAYS: Consider brand-specific markup overrides
- ALWAYS: Consider category/subcategory group markup
- ALWAYS: Add additional markup for installment plans (cuotas)
- NEVER: Apply markup to final price (markup is on cost only)

---

## TECH STACK

SQLAlchemy | PostgreSQL | Decimal (for precision) | Python datetime

---

## PATTERNS

### Get Active Pricing Constants

```python
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import date
from app.models.pricing_constants import PricingConstants

def obtener_constantes_pricing(db: Session) -> dict:
    """
    Get active pricing constants from database.
    Falls back to hardcoded defaults if none found.
    
    Returns:
        Dict with pricing constants
    """
    constants = db.query(PricingConstants).filter(
        and_(
            PricingConstants.fecha_desde <= date.today(),
            or_(
                PricingConstants.fecha_hasta.is_(None),
                PricingConstants.fecha_hasta >= date.today()
            )
        )
    ).order_by(PricingConstants.fecha_desde.desc()).first()
    
    if constants:
        return {
            "monto_tier1": float(constants.monto_tier1),
            "monto_tier2": float(constants.monto_tier2),
            "monto_tier3": float(constants.monto_tier3),
            "tier1": float(constants.comision_tier1),
            "tier2": float(constants.comision_tier2),
            "tier3": float(constants.comision_tier3),
            "varios": float(constants.varios_porcentaje),
            "grupo_default": constants.grupo_comision_default,
            "markup_adicional_cuotas": float(constants.markup_adicional_cuotas)
        }
    
    # Fallback defaults
    return {
        "monto_tier1": 15000,
        "monto_tier2": 24000,
        "monto_tier3": 33000,
        "tier1": 1095,
        "tier2": 2190,
        "tier3": 2628,
        "varios": 6.5,
        "grupo_default": 1,
        "markup_adicional_cuotas": 4.0
    }
```

### Currency Conversion

```python
from app.models.tipo_cambio import TipoCambio
from typing import Optional

def obtener_tipo_cambio_actual(db: Session, moneda: str = "USD") -> Optional[float]:
    """
    Get current exchange rate (venta).
    Falls back to latest available if today's is missing.
    """
    # Try today's rate first
    tc = db.query(TipoCambio).filter(
        TipoCambio.moneda == moneda,
        TipoCambio.fecha == date.today()
    ).first()
    
    if tc:
        return tc.venta
    
    # Fallback to latest available
    tc = db.query(TipoCambio).filter(
        TipoCambio.moneda == moneda
    ).order_by(TipoCambio.fecha.desc()).first()
    
    return tc.venta if tc else None

def convertir_a_pesos(costo: float, moneda: str, tipo_cambio: Optional[float]) -> float:
    """Convert cost to ARS"""
    if moneda == "ARS":
        return costo
    if tipo_cambio:
        return costo * tipo_cambio
    return costo
```

### Tier-Based Commission

```python
def calcular_comision_ml_tiered(precio_final: float, constants: dict) -> float:
    """
    Calculate ML commission using tiered pricing.
    
    Tier 1: Up to monto_tier1 → fixed tier1 fee
    Tier 2: Up to monto_tier2 → fixed tier2 fee
    Tier 3: Up to monto_tier3 → fixed tier3 fee
    Above tier3: percentage-based
    
    Args:
        precio_final: Final selling price in cents
        constants: Pricing constants dict
    
    Returns:
        Commission amount in cents
    """
    precio_pesos = precio_final / 100  # Convert cents to pesos
    
    if precio_pesos <= constants["monto_tier1"]:
        return constants["tier1"]
    elif precio_pesos <= constants["monto_tier2"]:
        return constants["tier2"]
    elif precio_pesos <= constants["monto_tier3"]:
        return constants["tier3"]
    else:
        # Above tier3, use percentage
        comision_pct = constants.get("comision_porcentaje_alta", 12.0)
        return (precio_final * comision_pct) / 100
```

### Full Price Calculation

```python
from typing import Dict

def calcular_precio_venta(
    costo: int,
    markup_percentage: float,
    incluir_envio: bool,
    envio_costo: float,
    pricelist_id: int,
    constants: dict,
    db: Session
) -> Dict[str, float]:
    """
    Calculate final selling price with full breakdown.
    
    Args:
        costo: Product cost in cents
        markup_percentage: Markup % (e.g., 25.5 for 25.5%)
        incluir_envio: Whether to include shipping in calculation
        envio_costo: Shipping cost in cents
        pricelist_id: Pricelist ID (4=clasica, 17=3c, etc.)
        constants: Pricing constants
        db: Database session
    
    Returns:
        Dict with detailed breakdown
    """
    # Base price with markup
    markup_amount = int(costo * (markup_percentage / 100))
    precio_base = costo + markup_amount
    
    # Add shipping if applicable
    if incluir_envio:
        precio_base += int(envio_costo)
    
    # ML commission (tiered)
    comision_ml = calcular_comision_ml_tiered(precio_base, constants)
    
    # Additional fees (varios)
    varios_amount = int(precio_base * (constants["varios"] / 100))
    
    # Final price
    precio_final = precio_base + int(comision_ml) + varios_amount
    
    # Net profit
    ganancia_neta = precio_final - costo - int(comision_ml) - varios_amount
    if incluir_envio:
        ganancia_neta -= int(envio_costo)
    
    # Profit margin %
    margen_porcentaje = (ganancia_neta / precio_final * 100) if precio_final > 0 else 0
    
    return {
        "costo": costo,
        "markup_porcentaje": markup_percentage,
        "markup_amount": markup_amount,
        "envio": int(envio_costo) if incluir_envio else 0,
        "comision_ml": int(comision_ml),
        "varios": varios_amount,
        "precio_final": precio_final,
        "ganancia_neta": ganancia_neta,
        "margen_porcentaje": round(margen_porcentaje, 2)
    }
```

### Installment Markup (Cuotas)

```python
def aplicar_markup_cuotas(precio_base: int, num_cuotas: int, constants: dict) -> int:
    """
    Apply additional markup for installment plans.
    
    Args:
        precio_base: Base price in cents
        num_cuotas: Number of installments (3, 6, 9, 12)
        constants: Pricing constants
    
    Returns:
        Price with installment markup in cents
    """
    if num_cuotas <= 1:
        return precio_base
    
    # Additional markup per installment tier
    markup_adicional = constants.get("markup_adicional_cuotas", 4.0)
    
    # Scale by number of installments
    cuotas_multiplier = {
        3: 1.0,
        6: 1.5,
        9: 2.0,
        12: 2.5
    }.get(num_cuotas, 1.0)
    
    markup_total = markup_adicional * cuotas_multiplier
    markup_amount = int(precio_base * (markup_total / 100))
    
    return precio_base + markup_amount
```

### Group-Based Shipping

```python
from app.models.comision_config import SubcategoriaGrupo
from app.models.producto import ProductoERP
from sqlalchemy import func

def obtener_envio_promedio_grupo(db: Session, grupo_id: int) -> float:
    """
    Get average shipping cost for active products in a group.
    
    Args:
        db: Database session
        grupo_id: Commission group ID
    
    Returns:
        Average shipping cost in cents, or 0 if no data
    """
    # Get subcategories in group
    subcategorias = db.query(SubcategoriaGrupo.subcat_id).filter(
        SubcategoriaGrupo.grupo_id == grupo_id
    ).all()
    
    if not subcategorias:
        return 0.0
    
    subcat_ids = [s[0] for s in subcategorias]
    
    # Calculate average shipping for active products
    resultado = db.query(func.avg(ProductoERP.envio)).filter(
        ProductoERP.subcategoria_id.in_(subcat_ids),
        ProductoERP.activo == True,
        ProductoERP.envio > 0
    ).scalar()
    
    return float(resultado) if resultado else 0.0
```

---

## PRICING FORMULA SUMMARY

```
1. Base Price = Cost + (Cost × Markup%)
2. Add Shipping (if applicable)
3. Calculate ML Commission (tiered)
4. Add Varios % (operational costs)
5. Final Price = Base + ML Commission + Varios
6. Net Profit = Final Price - Cost - Fees - Shipping
7. Profit Margin % = (Net Profit / Final Price) × 100
```

---

## COMMON PITFALLS

- ❌ Don't use float for money → Use int (cents) or Decimal
- ❌ Don't hardcode commission rates → Use versioned system
- ❌ Don't ignore date ranges → Check fecha_desde/fecha_hasta
- ❌ Don't forget PVP→Web mapping → Same commissions for both
- ❌ Don't apply markup to fees → Markup is on cost only
- ❌ Don't forget installment markup → Extra % for 3c, 6c, 9c, 12c

---

## DATABASE TABLES

- `pricing_constants` → Versioned pricing config (tiers, varios, defaults)
- `tb_cur_exch_history` (TipoCambio) → Daily exchange rates
- `comision_versionada` → Versioned commission system
- `comision_base` → Base commissions per group/pricelist
- `subcategoria_grupo` → Subcategory to commission group mapping
- `marcas_pm` → Brand-specific markup overrides

---

## REFERENCES

### Internal
- [Pricing Formulas Reference](references/pricing-formulas.md) - Mathematical formulas and examples
- Pricing Calculator: [pricing_calculator.py](../../backend/app/services/pricing_calculator.py)
- Pricing Constants Model: [pricing_constants.py](../../backend/app/models/pricing_constants.py)
- Commission Models: [comision_versionada.py](../../backend/app/models/comision_versionada.py)
- Exchange Rate Model: [tipo_cambio.py](../../backend/app/models/tipo_cambio.py)
- Tipo Cambio Service: [tipo_cambio_service.py](../../backend/app/services/tipo_cambio_service.py)
