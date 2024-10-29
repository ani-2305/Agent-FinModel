# calculate_working_capital.py

from . import shared_state
from .error_handling import handle_error

def calculate_working_capital() -> dict:
    """
    Calculates changes in working capital based on assumptions.

    :return: Success message or an error message.
    """
    try:
        assumptions = shared_state.user_assumptions
        forecast_income = shared_state.model_data['forecast_income_statement']
        forecast_balance = shared_state.model_data['forecast_balance_sheet']

        # Extract assumptions
        ar_days = float(assumptions['Accounts Receivable Days'])
        inventory_days = float(assumptions['Inventory Days'])
        ap_days = float(assumptions['Accounts Payable Days'])

        # Calculate working capital components
        revenue = forecast_income['Total Revenue'].iloc[-1]
        cogs = forecast_income['Total COGS'].iloc[-1]

        accounts_receivable = (revenue / 365) * ar_days
        inventory = (cogs / 365) * inventory_days
        accounts_payable = (cogs / 365) * ap_days

        # Update balance sheet
        forecast_balance.loc[len(forecast_balance)] = {
            'Accounts Receivable': accounts_receivable,
            'Inventory': inventory,
            'Accounts Payable': accounts_payable
        }

        # Store updated balance sheet
        shared_state.model_data['forecast_balance_sheet'] = forecast_balance

        return {"message": "Working capital successfully calculated."}

    except Exception as e:
        return {"error": handle_error(e)}
