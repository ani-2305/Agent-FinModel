# validate_user_inputs.py

from . import shared_state
from .error_handling import handle_error

def validate_user_inputs() -> dict:
    """
    Validates the user inputs to ensure they are within acceptable ranges.

    :return: Success message or an error message.
    """
    try:
        assumptions = shared_state.user_assumptions

        # Define acceptable ranges
        acceptable_ranges = {
            'Revenue Growth Rate': (0, 1),
            'COGS as % of Revenue': (0, 1),
            'Operating Expenses Growth Rate': (0, 1),
            'Tax Rate': (0, 1),
            'CapEx Growth Rate': (0, 1),
            'Change in Working Capital': (-1, 1),
            'Dividends Growth Rate': (0, 1)
        }

        for key, (min_val, max_val) in acceptable_ranges.items():
            value = assumptions.get(key)
            if value is not None:
                if not (min_val <= float(value) <= max_val):
                    return {"error": f"{key} of {value} is out of acceptable range ({min_val} to {max_val})."}

        return {"message": "User inputs successfully validated."}

    except Exception as e:
        return {"error": handle_error(e)}
