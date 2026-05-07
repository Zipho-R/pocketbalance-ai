# models.py
# Stores category groupings, income bands, and recommendation thresholds
# ----------------------------
# CATEGORY CLASSIFICATION
# ----------------------------

STRICT_NEEDS = [
    "Rent",
    "Insurance",
    "Debt Repayments"
]
FLEXIBLE_NEEDS = [
    "Utilities",
    "Internet",
    "Groceries",
    "Transport",
    "Personal Care"
]
DISCRETIONARY = [
    "Lifestyle & Entertainment",
    "Airtime/Data",
    "Other"
]
SAVINGS_CATEGORIES = [
    "Savings Account",
    "Investments"
]
# ----------------------------
# INCOME BANDS
# Adaptive budget models based on income level
# Format: Needs %, Wants %, Savings %
# ----------------------------
INCOME_BANDS = {
    "Low Income": {
        "max_income": 10000,
        "model": (70, 20, 10)
    },
    "Middle Income": {
        "max_income": 50000,
        "model": (60, 25, 15)
    },
    "High Income": {
        "max_income": float("inf"),
        "model": (50, 30, 20)
    }
}
# ----------------------------
# DISCRETIONARY THRESHOLDS
# Harder limits for wants as % of total income
# ----------------------------
DISCRETIONARY_THRESHOLDS = {
    "Lifestyle & Entertainment": 15,
    "Airtime/Data": 3,
    "Other": 10
}
# ----------------------------
# FLEXIBLE NEED GUIDELINES
# Soft guidelines for flexible essentials as % of income
# ----------------------------
FLEXIBLE_NEED_GUIDELINES = {
    "Utilities": 10,
    "Internet": 5,
    "Groceries": None,   # context-based
    "Transport": 10,
    "Personal Care": 5
}