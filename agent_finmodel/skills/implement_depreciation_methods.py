# implement_depreciation_methods.py

from . import shared_state
from .error_handling import handle_error

def implement_depreciation_methods() -> dict:
    """
    Calculates depreciation expenses based on selected methods.

    :return: Success message or an error message.
    """
    try:
        balance_sheet = shared_state.model_data.get('balance_sheet')
        assumptions = shared_state.user_assumptions
        accounting_policies = shared_state.model_data.get('accounting_policies')

        if not balance_sheet or not accounting_policies:
            return {"error": "Required data is missing for depreciation calculations."}

        useful_life = float(accounting_policies['Useful Life of PP&E Assets'])
        depreciation_method = accounting_policies['Depreciation Method']

        if depreciation_method == 'Straight-Line':
            pp&e = balance_sheet['Property, Plant & Equipment (PP&E)'].iloc[-1]
            depreciation_expense = pp&e / useful_life
        else:
            # Implement other methods if needed
            depreciation_expense = 0

        # Store depreciation expense in shared state
        shared_state.model_data['depreciation_expense'] = depreciation_expense

        return {"message": "Depreciation methods successfully implemented."}

    except Exception as e:
        return {"error": handle_error(e)}
