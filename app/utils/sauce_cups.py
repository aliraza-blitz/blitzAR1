from pydantic import BaseModel, Field


class SauceRule(BaseModel):
    """Sauce cup rules for orders."""
    sauce_cups_per_item: int = Field(default=1, ge=0, le=3)
    free_cups_per_order: int = Field(default=4, ge=0, le=20)
    max_cups_per_order: int = Field(default=12, ge=1, le=40)


def _clamp(value: int, min_val: int, max_val: int) -> int:
    """Clamp value within range."""
    return max(min_val, min(max_val, value))


def calculate_sauce_cups(rule: SauceRule, item_count: int) -> int:
    """Calculate sauce cups for item count."""
    clamped_count = _clamp(item_count, 0, 100)
    clamped_max = _clamp(rule.max_cups_per_order, 1, 40)
    total = clamped_count * _clamp(rule.sauce_cups_per_item, 0, 3)
    return min(total, clamped_max)


def calculate_charged_cups(rule: SauceRule, cups: int) -> int:
    """Calculate charged cups beyond free."""
    clamped_cups = _clamp(cups, 0, 100)
    clamped_free = _clamp(rule.free_cups_per_order, 0, 20)
    charged = clamped_cups - clamped_free
    return max(0, charged)


def is_max_cups_reached(rule: SauceRule, cups: int) -> bool:
    """Check if order reached max cups allowed."""
    clamped_cups = _clamp(cups, 0, 100)
    clamped_max = _clamp(rule.max_cups_per_order, 1, 40)
    return clamped_cups >= clamped_max
