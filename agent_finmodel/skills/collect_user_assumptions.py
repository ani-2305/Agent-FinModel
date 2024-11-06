# collect_user_assumptions.py

import pandas as pd # type: ignore
from . import shared_state
from .error_handling import handle_error

def collect_user_assumptions(file_path: str) -> dict:
    """
    Collects user-provided assumptions from the Excel template.

    :param file_path: Path to the Excel file containing the assumptions.
    :return: Dictionary of assumptions or an error message.
    """
    try:
        if not file_path:
            return {"error": "File path is required to collect user assumptions."}

        # Load the Assumptions sheet
        assumptions_df = pd.read_excel(file_path, 'Assumptions')

        # Convert DataFrame to dictionary
        assumptions = pd.Series(assumptions_df.Value.values, index=assumptions_df.Assumption).to_dict()

        # Store in shared state
        shared_state.user_assumptions = assumptions

        return {"message": "User assumptions successfully collected."}

    except Exception as e:
        return {"error": handle_error(e)}
