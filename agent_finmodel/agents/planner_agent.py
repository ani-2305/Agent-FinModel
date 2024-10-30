# planner_agent.py

class PlannerAgent:
    def __init__(self):
        pass

    def plan(self, user_request: str) -> list:
        """
        Parses the user's request and plans the sequence of actions.

        :param user_request: The user's input.
        :return: Ordered list of actions to be executed.
        """
        actions = []
        request_lower = user_request.lower()

        if 'build a 3-statement model' in request_lower or 'create financial model' in request_lower:
            actions = [
                'extract_financial_statements',
                'collect_user_assumptions',
                'validate_user_inputs',
                'build_historical_model',
                'apply_accounting_policies',
                'implement_depreciation_methods',
                'calculate_working_capital',
                'forecast_financials',
                'implement_tax_calculations',
                'insert_formulas',
                'render_excel_model',
                'format_excel_sheets',
                'apply_conditional_formatting',
                'provide_model_summary'
            ]
        elif 'extract financial statements' in request_lower:
            actions = ['extract_financial_statements']
        elif 'forecast financials' in request_lower:
            actions = ['forecast_financials']
        else:
            actions = ['provide_model_summary']

        return actions
