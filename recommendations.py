# recommendations.py
# Functions for adaptive recommendations and income-profile analysis

from models import (
    INCOME_BANDS,
    DISCRETIONARY_THRESHOLDS,
    FLEXIBLE_NEED_GUIDELINES,
    DISCRETIONARY,
    FLEXIBLE_NEEDS
)


def detect_income_band(income):
    """Detect the user's income band and return the matching budget model."""
    for band, data in INCOME_BANDS.items():
        if income <= data["max_income"]:
            needs, wants, savings = data["model"]
            return band, needs, wants, savings
    return "Unknown", 0, 0, 0


def describe_difference(actual, target, lower_is_better=False):
    """
    Return a human-friendly comparison phrase.
    Example outputs:
    - slightly above target
    - well above target
    - close to target
    - slightly below target
    """
    difference = actual - target
    gap = abs(difference)

    if gap <= 2:
        return "close to target"

    if lower_is_better:
        if actual < target:
            return "below target"
        if gap <= 5:
            return "slightly above target"
        return "well above target"

    if actual > target:
        if gap <= 5:
            return "slightly above target"
        return "well above target"

    if gap <= 5:
        return "slightly below target"
    return "well below target"


def generate_recommendations(
    income,
    variable_costs,
    needs_percent,
    wants_percent,
    savings_percent,
    remaining_money,
    is_deficit,
    deficit
):
    """Generate a summary paragraph and detailed financial recommendations."""
    recommendations = []

    band, needs_model, wants_model, savings_model = detect_income_band(income)

    if income <= 0:
        return (
            "A financial report could not be generated properly because the income entered is zero or invalid.",
            [
                "Please enter a valid monthly income to receive meaningful analysis."
            ]
        )

    needs_comparison = describe_difference(needs_percent, needs_model)
    wants_comparison = describe_difference(wants_percent, wants_model)
    savings_comparison = describe_difference(savings_percent, savings_model)

    top_variable_category = None
    top_variable_amount = 0

    if variable_costs:
        top_variable_category = max(variable_costs, key=variable_costs.get)
        top_variable_amount = variable_costs[top_variable_category]

    # ----------------------------
    # STEP 1: SUMMARY PARAGRAPH
    # ----------------------------
    if is_deficit:
        summary = (
            f"Based on the {band} model, your budget is currently under pressure because your total spending exceeds your income by "
            f"R{deficit:,.2f}. Your needs are {needs_comparison}, your wants are {wants_comparison}, and your savings are {savings_comparison} "
            f"against the recommended model."
        )
    else:
        summary = (
            f"Based on the {band} model, your spending pattern shows that your needs are {needs_comparison}, your wants are {wants_comparison}, "
            f"and your savings are {savings_comparison} against the recommended budget targets."
        )

    # ----------------------------
    # STEP 2: DEFICIT CHECK
    # ----------------------------
    if is_deficit:
        recommendations.append(
            "Your first priority should be restoring balance by reducing non-essential spending before making cuts to essentials."
        )

        if top_variable_category and top_variable_amount > 0:
            recommendations.append(
                f"Your highest flexible spending category is {top_variable_category}, so reviewing that area first may help free up money faster."
            )

        if savings_percent > 0:
            recommendations.append(
                "Because your budget is already in deficit, it may help to temporarily rebalance some savings contributions while protecting the habit of saving where possible."
            )

        return summary, recommendations

    # ----------------------------
    # STEP 3: MODEL-BASED INSIGHTS
    # ----------------------------
    if needs_percent > needs_model:
        recommendations.append(
            f"Your essential spending is {describe_difference(needs_percent, needs_model)} for the {band} model, which means a large share of your income is already committed early in the month."
        )
    else:
        recommendations.append(
            f"Your essential spending is {describe_difference(needs_percent, needs_model)} for your income profile, which helps preserve more monthly flexibility."
        )

    if wants_percent > wants_model:
        recommendations.append(
            f"Your discretionary spending is {describe_difference(wants_percent, wants_model)}. A small reduction in lifestyle-based categories could improve breathing room without affecting essentials."
        )
    else:
        recommendations.append(
            f"Your discretionary spending is {describe_difference(wants_percent, wants_model)}, which suggests reasonable control over flexible spending."
        )

    if savings_percent < savings_model:
        recommendations.append(
            f"Your savings rate is {describe_difference(savings_percent, savings_model)}. Increasing it gradually, even in small monthly steps, could strengthen long-term stability."
        )
    else:
        recommendations.append(
            f"Your savings contribution is {describe_difference(savings_percent, savings_model)}, which is a positive sign for long-term financial resilience."
        )

    # ----------------------------
    # STEP 4: CATEGORY INSIGHTS
    # ----------------------------
    for category, amount in variable_costs.items():
        percent_income = (amount / income) * 100

        if remaining_money > 0:
            percent_after_needs = (amount / remaining_money) * 100
        else:
            percent_after_needs = 0

        if category in DISCRETIONARY:
            threshold = DISCRETIONARY_THRESHOLDS.get(category)
            if threshold is not None and percent_income > threshold:
                recommendations.append(
                    f"{category} is using {percent_income:.1f}% of your income, which is above its suggested range and may be one of the easiest areas to review."
                )

        if category in FLEXIBLE_NEEDS:
            guideline = FLEXIBLE_NEED_GUIDELINES.get(category)
            if guideline is not None and percent_income > guideline:
                recommendations.append(
                    f"{category} is relatively high compared to your income, so small reductions here could improve your overall balance without requiring major lifestyle changes."
                )

        if percent_after_needs > 50:
            recommendations.append(
                f"After covering essentials, {category} takes up {percent_after_needs:.1f}% of your remaining money, making it one of your strongest spending pressure points."
            )

    # ----------------------------
    # STEP 5: TOP CATEGORY COMMENTARY
    # ----------------------------
    if top_variable_category and top_variable_amount > 0:
        recommendations.append(
            f"Your highest variable expense is {top_variable_category} at R{top_variable_amount:,.2f}, so that category deserves the most attention if you want the biggest improvement from one change."
        )

    # ----------------------------
    # STEP 6: FALLBACK
    # ----------------------------
    if not recommendations:
        recommendations.append(
            "Your spending pattern appears balanced, with no major pressure points standing out in this report."
        )

    return summary, recommendations