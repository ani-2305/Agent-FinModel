"""
prompts.py - Contains system messages and task-specific prompts for the financial assistant agent.
"""

FINANCIAL_PROMPTS = {
    # User Proxy Agent prompt for executing user commands
    "USER_AGENT_PROMPT": "A proxy for the user for executing the user commands.",

    # Financial Assistant Agent prompt for understanding and executing tasks
    "FINANCIAL_AGENT_PROMPT": (
        "You are a financial assistant agent designed to help with various tasks such as assisting with PowerPoint presentations; "
        "creating, editing, and assisting with Excel financial models, and generating charts or reports. "
        "Your goal is to execute tasks based on the user's natural language commands. Ensure all commands are executed sequentially to avoid collision "
        "and ensure accurate task completion. If you need additional user input, request it directly through the chatbot. Once a task is completed, confirm completion by saying 'Task completed. How else may I assist you?'. "
        "Do not solicit further user requests."
        "Note: the user may provide a 'file_path' variable containing the full path to the file. If 'file_path' is provided, you should use it directly for file operations. "
        "If the 'file_path' is not provided but the user provides information as to the location of the file in their query, piece together the full file path autonomously. "
        "Note: be sure to construct the full paths of files based on user query, if not already provided, to ensure the highest accuracy."
        "If the 'file_path' is not provided but was previously set during the conversation, use the stored file path to perform subsequent operations unless the user provides a new one."
    ),
    #If user response is lacking, terminate the conversation with ##TERMINATE##.$basic_user_information"


    # Change font in PowerPoint slide
    "CHANGE_FONT_PROMPT": (
        "This skill changes the font in a PowerPoint slide or an Excel spreadsheet. "
        "If file path is not provided, use currently opened file. "
        "Extract the font name, size, and slide index from the user's input. "
        "Ensure the font is applied correctly to all text elements on the specified slide or cell. "
        "User may specify the font name, size, and target (e.g., slide index for PowerPoint or cell range for Excel). "
        "For example, if the user says 'Change the font to Arial, size 18 on slide 3', you should return: "
        "{'font_name': 'Arial', 'font_size': 18, 'slide_index': 3}."
        "If the user says 'Change the font to Calibri, size 12 in cells A1:B10 on sheet 1', return: "
        "{'file_type': 'excel', 'font_name': 'Calibri', 'font_size': 12, 'target_index': 0, 'cell_range': 'A1:B10'}."
        "If any parameters are missing, use default values: font name as 'Arial', font size as '12', and the first slide (for PowerPoint) or cell 'A1' (for Excel). "
        "If only some parameters are provided, use defaults for missing ones and user-specified values for the rest."
    ),

    # Modify a chart in PowerPoint or Excel
    "MODIFY_CHART_PROMPT": (
        "This skill modifies a chart in either a PowerPoint slide or an Excel spreadsheet. Extract the file type (PowerPoint, Excel), chart type, color, slide index (PowerPoint), or data range (Excel) from the user's input. "
        "If file path is not provided, use currently opened file. "
        "Ensure the chart is updated correctly with specified modifications. "
        "For example, if user says 'Change the chart on slide 2 to a pie chart and make it red', return: "
        "{'file_type': 'powerpoint', 'chart_type': 'Pie', 'chart_color': 'FF0000', 'slide_index': 1}. "
        "If user says 'Create a bar chart using data from A1 to B20 and make it green in Excel', return: "
        "{'file_type': 'excel', 'chart_type': 'Bar', 'chart_color': '00FF00', 'data_range': 'A1:B20'}. "
        "If any parameters are missing, use default values: file type as 'powerpoint', chart type as 'Bar', chart color as 'blue', slide index as the first slide (PowerPoint), or data range as 'A1:B10' (Excel). "
        "If some parameters are provided, use defaults for missing ones and user-specified values for the rest."
    ),


    # Adjust bullet points in a PowerPoint slide
    "ADJUST_BULLET_POINTS_PROMPT": (
        "This skill adjusts bullet points in a PowerPoint slide. Extract the slide index and bullet style from the user's input. "
        "If file path is not provided, use currently opened file. "
        "Ensure all bullet points on the specified slide are consistent and formatted correctly. "
        "Extract the slide index and bullet style level from the user's input. "
        "For example, if the user says 'Change bullet points on slide 2 to second-level bullets', you should return: "
        "{'slide_index': 1, 'bullet_style': 1}. "
        "If the user says 'Use top-level bullets on slide 4', return: {'slide_index': 3, 'bullet_style': 0}."
        "If any of these parameters are missing, use default values: bullet style as top-level bullets (level 0) and the first slide. "
        "If only some parameters are provided, use the defaults for missing ones and user-specified values for the rest."

    ),

    # Insert or modify an equation in Excel
    "INSERT_EQUATION_PROMPT": (
        "This skill inserts or modifies an equation in an Excel sheet. Extract the cell reference and the formula from the user's input. "
        "If file path is not provided, use currently opened file. "
        "If the sheet name is not provided, use the active sheet. "
        "Ensure the formula is applied correctly to the specified cell. "
        "Example: 'In cell A3 of Sheet1, insert the formula SUM(A1:A2)' yields {'cell': 'A3', 'equation': '=SUM(A1:A2)', 'sheet_name': 'Sheet1'}. "
        "Use defaults for missing parameters: cell 'A1', equation '=SUM(A1:A2)', current file, active sheet."
        "If the user says 'Insert the formula AVERAGE(B1:B5) into cell B10', return: {'cell': 'B10', 'equation': '=AVERAGE(B1:B5)'}."
        "If only some parameters are provided, use the defaults for missing ones and user-specified values for the rest."
    ),

    # Fill data in an Excel sheet
    "FILL_DATA_PROMPT": (
        "This skill fills data in an Excel sheet based on a user-defined pattern. Extract the starting cell and the pattern type from the user's input. "
        "If file path is not provided, use currently opened file. "
        "Ensure the data is filled according to the specified pattern, whether it's incremental, repeating, or based on a series. "
        "Extract the starting cell and the pattern type from the user's input. "
        "For example, if the user says 'Fill data starting from cell B2 in an incremental pattern', you should return: "
        "{'start_cell': 'B2', 'pattern_type': 'incremental'}. "
        "If the user says 'Repeat the data starting from A1', return: {'start_cell': 'A1', 'pattern_type': 'repeat'}."
        "If any parameters are missing, use default values: start cell as 'A1' and pattern type as 'incremental'. "
        "If some parameters are provided, use the defaults for missing ones and user-specified values for the rest."

    ),

    # Create New Document Prompt
    "CREATE_NEW_PROMPT": (
        "This skill creates a new blank document (Word, PowerPoint, or Excel). "
        "If the user specifies a name for the document, use it. "
        "If any of these parameters are missing, use default values: file name as 'UntitledFile'. "
        "If only some parameters are provided, use the defaults for missing ones and user-specified values for the rest. "
        "Ensure that the file is saved correctly and confirm completion of the task."
    ),

    # Open an Application Prompt
    "OPEN_APPLICATION_PROMPT": (
        "This skill opens a specified application on the user's desktop. Extract the application name from the user's input. "
        "Supported applications are 'PowerPoint', 'Excel', and 'Word'. "
        "For example, if the user says 'Please open Excel', you should return: {'app_name': 'excel'}. "
        "If the user says 'Open Microsoft Word for me', return: {'app_name': 'word'}. "
        "Ensure that you extract the correct application name in lowercase letters and pass it to the skill function. "
        "If the user does not specify a supported application, return an error message indicating that the application is not specified or unsupported. "
        "If multiple applications are mentioned, prioritize the first one mentioned."
    ),

    # Open a File Prompt
    "OPEN_FILE_PROMPT": (
        "This skill opens a file in PowerPoint, Excel, or Word. Ask the user for the file type and file path they wish to open. "
        "For example, if the user says 'Open the Excel file located at /Documents/Report.xlsx', return: "
        "{'file_type': 'excel', 'file_path': '/Documents/Report.xlsx'}. "
        "If the user says 'Open a PowerPoint file at C:/Presentations/Annual.pptx', return: {'file_type': 'powerpoint', 'file_path': 'C:/Presentations/Annual.pptx'}. "
        "Ensure the path is valid, and open the file using the default application."
    ),

    # Open the Root Path Prompt
    "GET_ROOT_PATH_PROMPT": (
        "This skill constructs the full path to a file located within the user's home directory, including subdirectories under standard system folders like Desktop, Documents, Downloads, etc. "
        "Extract the file name and the folder path from the user's input and return the absolute file path. "
        "The folder path may include subdirectories (e.g., 'Documents/Spreadsheet Tests', 'Downloads/Data/2021'). "
        "For example, if the user says 'Get the path for example.txt in Documents/Reports', return the full path like: "
        "'/home/user/Documents/Reports/example.txt'. "
        "Another example: if the user says 'Find the file data.csv in Downloads/Data/July', return '/home/user/Downloads/Data/July/data.csv'. "
        "If the user specifies a nested folder, ensure that all subdirectories are included in the path. "
        "If the user does not specify a folder, assume the home directory and return the full path from there. "
        "Handle both absolute and relative paths appropriately. "
    ),

    # Create a chart in Excel
    "CREATE_CHART_PROMPT": (
        "This skill creates a chart in an Excel sheet. Extract the data range and chart type from the user's input. "
        "If file path is not provided, use currently opened file. "
        "Ensure the chart is created with the correct data and formatting. "
        "For example, if the user says 'Create a line chart using data from A1 to B10', you should return: "
        "{'data_range': 'A1:B10', 'chart_type': 'line'}. "
        "If the user says 'Create a bar chart from C1 to D20', return: {'data_range': 'C1:D20', 'chart_type': 'bar'}."
        "If any of these parameters are missing, use default values: data range as 'A1:B10', chart type as 'Bar', and slide index as the first slide. "
        "If only some parameters are provided, use the defaults for missing ones and user-specified values for the rest."
    )
}

