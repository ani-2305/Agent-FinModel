# implement_tax_calculations.py

from . import shared_state
from .error_handling import handle_error

def implement_tax_calculations() -> dict:
    """
    Calculates tax expenses and updates the Income Statement.

    :return: Success message or an error message.
    """
    try:
        forecast_income = shared_state.model_data['forecast_income_statement']
        assumptions = shared_state.user_assumptions

        tax_rate = float(assumptions['Tax Rate'])

        # Calculate tax expense
        pre_tax_income = forecast_income['Pre-tax Income'].iloc[-1]
        tax_expense = pre_tax_income * tax_rate

        # Update Income Statement
        forecast_income.loc[len(forecast_income)-1, 'Income Tax Expense'] = tax_expense
        net_income = pre_tax_income - tax_expense
        forecast_income.loc[len(forecast_income)-1, 'Net Income'] = net_income

        # Store updated Income Statement
        shared_state.model_data['forecast_income_statement'] = forecast_income

        return {"message": "Tax calculations successfully implemented."}

    except Exception as e:
        return {"error": handle_error(e)}
