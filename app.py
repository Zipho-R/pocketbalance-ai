from flask import Flask, render_template, request
from budget_calculator import (
    calculate_totals,
    classify_expenses,
    calculate_percentages,
    calculate_remaining_after_needs,
    check_deficit,
    get_financial_health_status,
    get_top_variable_category
)
from recommendations import generate_recommendations, detect_income_band

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze")
def analyze():
    return render_template("analyze.html")

@app.route("/results", methods=["POST"])
def results():
    try:
        # ----------------------------
        # STEP 1: COLLECT FORM INPUTS
        # ----------------------------
        income = float(request.form.get("income", 0))

        fixed = {
            "Rent": float(request.form.get("rent", 0)),
            "Insurance": float(request.form.get("insurance", 0)),
            "Debt Repayments": float(request.form.get("debt_repayments", 0)),
            "Contracts": float(request.form.get("contracts", 0)),
            "Utilities": float(request.form.get("utilities", 0)),
            "Internet": float(request.form.get("internet", 0))
        }
        variable = {
            "Groceries": float(request.form.get("groceries", 0)),
            "Transport": float(request.form.get("transport", 0)),
            "Lifestyle & Entertainment": float(request.form.get("lifestyle", 0)),
            "Personal Care": float(request.form.get("personal_care", 0)),
            "Airtime/Data": float(request.form.get("airtime", 0)),
            "Other": float(request.form.get("other", 0))
        }
        savings = {
            "Savings Account": float(request.form.get("savings_account", 0)),
            "Investments": float(request.form.get("investments", 0))
        }

        # ----------------------------
        # STEP 2: RUN CORE CALCULATIONS
        # ----------------------------
        total_fixed, total_variable, total_savings, total_expenses = calculate_totals(
            fixed, variable, savings
        )

        strict_needs, flexible_needs, wants_total = classify_expenses(fixed, variable)
        needs_total = strict_needs + flexible_needs

        needs_percent, wants_percent, savings_percent = calculate_percentages(
            income,
            needs_total,
            wants_total,
            total_savings
        )

        remaining_money = calculate_remaining_after_needs(income, needs_total)
        is_deficit, deficit = check_deficit(income, total_expenses)

        # ----------------------------
        # STEP 3: DETECT MODEL + HEALTH STATUS
        # ----------------------------
        income_band, needs_model, wants_model, savings_model = detect_income_band(income)

        health_status = get_financial_health_status(
            is_deficit,
            needs_percent,
            wants_percent,
            savings_percent,
            needs_model,
            wants_model,
            savings_model
        )
        top_category, top_amount = get_top_variable_category(variable)

        # ----------------------------
        # STEP 4: GENERATE RECOMMENDATIONS
        # ----------------------------
        summary_text, recommendations = generate_recommendations(
            income,
            variable,
            needs_percent,
            wants_percent,
            savings_percent,
            remaining_money,
            is_deficit,
            deficit
        )
        # ----------------------------
        # STEP 5: RENDER RESULTS PAGE
        # ----------------------------
        return render_template(
            "results.html",
            income=income,
            total_fixed=total_fixed,
            total_variable=total_variable,
            total_savings=total_savings,
            total_expenses=total_expenses,
            needs_percent=round(needs_percent, 2),
            wants_percent=round(wants_percent, 2),
            savings_percent=round(savings_percent, 2),
            income_band=income_band,
            needs_model=needs_model,
            wants_model=wants_model,
            savings_model=savings_model,
            health_status=health_status,
            top_category=top_category,
            top_amount=top_amount,
            summary_text=summary_text,
            recommendations=recommendations,
            fixed=fixed,
            variable=variable,
            savings=savings
        )
    except ValueError:
        return "Invalid input. Please go back and enter valid numeric values."

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
    