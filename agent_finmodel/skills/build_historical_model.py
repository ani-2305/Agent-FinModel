# build_historical_model.py

import pandas as pd # type: ignore
from . import shared_state
from agent_finmodel.skills.error_handling import handle_error

def build_historical_model() -> dict:
    """
    Organizes and structures the extracted historical data for modeling.

    :return: Success message or an error message.
    """
    try:
        income_statement = shared_state.model_data.get('income_statement')
        balance_sheet = shared_state.model_data.get('balance_sheet')
        cash_flow_statement = shared_state.model_data.get('cash_flow_statement')

        if income_statement is None or balance_sheet is None or cash_flow_statement is None:
            return {"error": "Financial statements are missing. Please extract them first."}

        # Data cleaning and preparation can be added here if necessary

        return {"message": "Historical model successfully built."}

    except Exception as e:
        return {"error": handle_error(e)}