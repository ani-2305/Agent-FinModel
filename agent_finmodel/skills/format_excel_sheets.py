# format_excel_sheets.py

from openpyxl.styles import Font, Alignment, Border, Side
from .error_handling import handle_error

def format_excel_sheets(workbook) -> dict:
    """
    Applies consistent formatting to the Excel sheets.

    :param workbook: An openpyxl Workbook object.
    :return: Success message or an error message.
    """
    try:
        sheets = workbook.sheetnames
        thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                            top=Side(style='thin'), bottom=Side(style='thin'))

        for sheet_name in sheets:
            ws = workbook[sheet_name]
            for row in ws.iter_rows():
                for cell in row:
                    cell.font = Font(name='Arial', size=10)
                    cell.alignment = Alignment(horizontal='right')
                    cell.border = thin_border
                    if isinstance(cell.value, (int, float)):
                        cell.number_format = '#,##0.00'

            # Adjust column widths
            for column_cells in ws.columns:
                length = max(len(str(cell.value or '')) for cell in column_cells)
                ws.column_dimensions[column_cells[0].column_letter].width = length + 2

        return {"message": "Excel sheets successfully formatted."}

    except Exception as e:
        return {"error": handle_error(e)}
