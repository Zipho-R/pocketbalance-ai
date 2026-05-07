# budget_calculator.py
# Handles totals, classifications, percentages, and financial health indicators

from models import STRICT_NEEDS, FLEXIBLE_NEEDS, DISCRETIONARY


def calculate_totals(fixed_costs, variable_costs, savings):
    """Compute total expenses per section and overall total."""
    total_fixed = sum(fixed_costs.values())
    total_variable = sum(variable_costs.values())
    total_savings = sum(savings.values())
    total_expenses = total_fixed + total_variable + total_savings

    return total_fixed, total_variable, total_savings, total_expenses


def classify_expenses(fixed_costs, variable_costs):
    """
    Classify expenses into:
    - strict needs
    - flexible needs
    - discretionary spending
    """
    strict_total = 0
    flexible_total = 0
    wants_total = 0

    for category, amount in fixed_costs.items():
        if category in STRICT_NEEDS:
            strict_total += amount
        elif category in FLEXIBLE_NEEDS:
            flexible_total += amount

    for category, amount in variable_costs.items():
        if category in FLEXIBLE_NEEDS:
            flexible_total += amount
        elif category in DISCRETIONARY:
            wants_total += amount

    return strict_total, flexible_total, wants_total


def calculate_percentages(income, needs_total, wants_total, savings_total):
    """Calculate spending percentages relative to income."""
    if income == 0:
        return 0, 0, 0

    needs_percent = (needs_total / income) * 100
    wants_percent = (wants_total / income) * 100
    savings_percent = (savings_total / income) * 100

    return needs_percent, wants_percent, savings_percent


def calculate_remaining_after_needs(income, needs_total):
    """Calculate money remaining after essential spending."""
    return income - needs_total


def check_deficit(income, total_expenses):
    """Check whether the user is overspending."""
    if total_expenses > income:
        return True, total_expenses - income
    return False, 0


def get_financial_health_status(
    is_deficit,
    needs_percent,
    wants_percent,
    savings_percent,
    needs_model,
    wants_model,
    savings_model
):
    """
    Return an overall financial health label.
    - Critical: overspending
    - Needs Attention: multiple warning signs
    - Stable: one warning sign
    - Healthy: generally balanced
    """
    if is_deficit:
        return "Critical"

    warning_count = 0

    if needs_percent > needs_model:
        warning_count += 1
    if wants_percent > wants_model:
        warning_count += 1
    if savings_percent < savings_model:
        warning_count += 1

    if warning_count >= 2:
        return "Needs Attention"
    if warning_count == 1:
        return "Stable"

    return "Healthy"


def get_top_variable_category(variable_costs):
    """Return the highest variable expense category and amount."""
    if not variable_costs:
        return None, 0

    top_category = max(variable_costs, key=variable_costs.get)
    return top_category, variable_costs[top_category]
