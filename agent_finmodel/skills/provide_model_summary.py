# provide_model_summary.py

from . import shared_state
from .error_handling import handle_error

def provide_model_summary() -> dict:
    """
    Generates a summary of the financial model's key outputs.

    :return: A dictionary containing the summary or an error message.
    """
    try:
        forecast_income = shared_state.model_data['forecast_income_statement']
        forecast_balance = shared_state.model_data['forecast_balance_sheet']

        # Extract key metrics
        revenue = forecast_income['Total Revenue'].iloc[-1]
        net_income = forecast_income['Net Income'].iloc[-1]
        total_assets = forecast_balance['Total Assets'].iloc[-1]
        total_equity = forecast_balance['Total Equity'].iloc[-1]

        summary = {
            'Final Year Revenue': revenue,
            'Final Year Net Income': net_income,
            'Final Year Total Assets': total_assets,
            'Final Year Total Equity': total_equity
        }

        return {"summary": summary}

    except Exception as e:
        return {"error": handle_error(e)}
