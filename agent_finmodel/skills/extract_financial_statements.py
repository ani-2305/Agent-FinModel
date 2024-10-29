# extract_financial_statements.py

import pandas as pd
import os
from . import shared_state
from .error_handling import handle_error

def extract_financial_statements(file_path: str) -> dict:
    """
    Extracts historical financial statements from an Excel template.

    :param file_path: Path to the Excel file containing the financial statements.
    :return: Dictionary containing DataFrames of financial statements or an error message.
    """
    try:
        if not file_path:
            return {"error": "File path is required to extract financial statements."}

        if not os.path.exists(file_path):
            return {"error": f"The file path '{file_path}' does not exist."}

        # Load the Excel file
        excel_file = pd.ExcelFile(file_path)

        # Read the financial statements
        income_statement = pd.read_excel(excel_file, 'Income Statement')
        balance_sheet = pd.read_excel(excel_file, 'Balance Sheet')
        cash_flow_statement = pd.read_excel(excel_file, 'Cash Flow Statement')

        # Store in shared state
        shared_state.model_data['income_statement'] = income_statement
        shared_state.model_data['balance_sheet'] = balance_sheet
        shared_state.model_data['cash_flow_statement'] = cash_flow_statement

        return {"message": "Financial statements successfully extracted."}

    except Exception as e:
        return {"error": handle_error(e)}
