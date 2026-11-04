from pydantic import BaseModel, Field


class FuelRule(BaseModel):
    litres_per_100km: float = Field(default=3.0, ge=1.0, le=15.0)
    price_per_litre: float = Field(default=1.5, ge=0.1, le=10.0)
    distance_multiplier: float = Field(default=2.0, ge=1.0, le=2.0)


def _clamp(value: float, min_val: float, max_val: float) -> float:
    """Keep a value within the given range."""
    return max(min_val, min(max_val, value))


def calculate_litres_used(distance_km: float, rule: FuelRule) -> float:
    """Calculate litres of fuel used for a one-way distance."""
    distance_km = _clamp(distance_km, 0.0, 100.0)
    litres = (distance_km / 100.0) * rule.litres_per_100km
    return round(litres, 2)


def calculate_fuel_cost(distance_km: float, rule: FuelRule) -> float:
    """Calculate total fuel cost for a one-way distance."""
    distance_km = _clamp(distance_km, 0.0, 100.0)
    total_distance = distance_km * rule.distance_multiplier
    litres = (total_distance / 100.0) * rule.litres_per_100km
    cost = litres * rule.price_per_litre
    return round(cost, 2)


def calculate_cost_per_km(distance_km: float, rule: FuelRule) -> float:
    """Calculate fuel cost per kilometer of one-way distance."""
    distance_km = _clamp(distance_km, 0.0, 100.0)
    if distance_km == 0:
        return 0.0
    total_cost = calculate_fuel_cost(distance_km, rule)
    return round(total_cost / distance_km, 2)
