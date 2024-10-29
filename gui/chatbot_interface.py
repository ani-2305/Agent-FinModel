import tkinter as tk
from tkinter import scrolledtext, filedialog
import asyncio
import customtkinter as ctk 
import re
import os  # Import os to work with file paths

# Import the financial assistant agent
from agent_financial.financial_assistant import FinancialAssistantAgent

# Initialize the financial assistant agent
agent = FinancialAssistantAgent()

# Global variable to store the file path
file_path = None
root = None

# Define the skills that require a file path
skills_requiring_file_path = ['open_file', 'change_font', 'modify_chart', 'adjust_bullet_points', 'insert_equation', 'fill_data', 'create_chart']

def parse_file_path(user_input):
    # Extract file and folder names using regex
    pattern = r'(file|folder|directory)\s["\'](.*?)["\']'
    matches = re.findall(pattern, user_input, re.IGNORECASE)
    if not matches:
        return None  # No matches found

    file_name = None
    folder_names = []
    for item in matches:
        if item[0].lower() == 'file':
            file_name = item[1]
        elif item[0].lower() in ['folder', 'directory']:
            folder_names.append(item[1])

    if not file_name:
        return None  # File name is required

    # Build the path starting from the user's home directory
    home_dir = os.path.expanduser('~')
    path_parts = [home_dir] + folder_names[::-1]  # Reverse the folder names
    folder_path = os.path.join(*path_parts)
    full_file_path = os.path.join(folder_path, file_name)
    return full_file_path

def detect_intent(user_input):
    user_input = user_input.lower()
    # Improved pattern matching to extract keywords
    if "open" in user_input and any(app in user_input for app in ['excel', 'word', 'powerpoint']):
        return 'open_application'
    elif "create new" in user_input or "create a new" in user_input:
        return 'create_new'
    elif "open file" in user_input:
        full_file_path = parse_file_path(user_input)
        if full_file_path:
            return 'open_file', full_file_path
        else:
            return 'open_file'
    else:
        skill_keywords = {
            'change font': 'change_font',
            'modify chart': 'modify_chart',
            'adjust bullet points': 'adjust_bullet_points',
            'insert equation': 'insert_equation',
            'fill data': 'fill_data',
            'create chart': 'create_chart',
            'open file': 'open_file',
        }

        for keyword, intent in skill_keywords.items():
            if keyword in user_input:
                return intent

def ask_for_file_path():
    global file_path
    add_message("Agent", "Please select the file that you are working on.")
    root.update()
    # Open file dialog for the user to select a file
    selected_file_path = filedialog.askopenfilename()
    if selected_file_path:
        file_path = selected_file_path.strip()
        print(f"File path entered: {file_path}")
        return file_path
    else:
        return None

def handle_query(event=None):
    global file_path
    user_input = input_box.get("1.0", "end").strip()
    intent_result = detect_intent(user_input)

    if isinstance(intent_result, tuple):
        intent = intent_result[0]
        if intent == 'open_file':
            file_path = intent_result[1]
    else:
        intent = intent_result

    # Check if file path is required and prompt for it if not already set
    if intent in skills_requiring_file_path and not file_path:
        file_path = ask_for_file_path()

    if not file_path and intent in skills_requiring_file_path:
        add_message("Agent", "File path is required for this operation.")
        input_box.delete("1.0", "end")
        return

    print(f"File path being used: {file_path}")

    # Asynchronous function to call the agent and get the response
    async def query_agent(user_input, file_path):
        if file_path:
            result = await agent.user_proxy_agent.a_initiate_chat(
                agent.agent,
                message=user_input,
                cache=None,
                file_path=file_path
            )
        else:
            result = await agent.user_proxy_agent.a_initiate_chat(
                agent.agent,
                message=user_input,
                cache=None
            )
        response = result.summary
        add_message("You", user_input)
        add_message("Agent Fin", response)
    
    asyncio.run(query_agent(user_input, file_path))
    input_box.delete("1.0", "end")

def adjust_input_box_height(event=None):
    """Adjust the height of the input box based on the content."""
    content = input_box.get("1.0", "end").strip()
    lines = content.count("\n") + 1
    new_height = min(max(lines * 20, 60), 200)
    input_box.configure(height=new_height)

def add_message(sender, message):
    # Define fonts using CTkFont
    montserrat_regular = ctk.CTkFont(family="Montserrat", size=12)
    montserrat_semibold = ctk.CTkFont(family="Montserrat", size=12, weight="bold")

    # Create a frame for each message
    message_frame = ctk.CTkFrame(chat_frame, fg_color="transparent")
    message_frame.pack(fill="x", padx=10, pady=5)

    # Sender label
    sender_label = ctk.CTkLabel(message_frame, text=f"{sender}:", font=montserrat_semibold, anchor="w")
    sender_label.pack(fill="x")

    # Message label
    message_label = ctk.CTkLabel(message_frame, text=message, font=montserrat_regular, anchor="w", justify="left", wraplength=320)
    message_label.pack(fill="x", anchor="w")

    # Scroll to the bottom
    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1.0)

def run_chatbot():
    global root, chat_frame, chat_canvas
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("Agent Fin")
    root.geometry("415x465")

    # Optional: Make the window stay on top
    root.wm_attributes("-topmost", True)

    # Create a frame for the chat area
    chat_area = ctk.CTkFrame(root, fg_color="transparent")
    chat_area.pack(pady=10, padx=10, fill="both", expand=True)

    # Create a canvas and scrollbar for the chat area
    chat_canvas = tk.Canvas(chat_area, highlightthickness=0)
    scrollbar = ctk.CTkScrollbar(chat_area, orientation="vertical", command=chat_canvas.yview)
    chat_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    chat_canvas.pack(side="left", fill="both", expand=True)

    # Create a frame inside the canvas
    chat_frame = ctk.CTkFrame(chat_canvas, fg_color="transparent")
    chat_canvas.create_window((0, 0), window=chat_frame, anchor="nw")

    # Update scroll region
    def on_frame_configure(event):
        chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))
    chat_frame.bind("<Configure>", on_frame_configure)

    # Create input box for user to type queries with rounded corners
    global input_box
    montserrat_regular = ctk.CTkFont(family="Montserrat", size=12)
    montserrat_semibold = ctk.CTkFont(family="Montserrat", size=12, weight="bold")

    input_box = ctk.CTkTextbox(root, height=60, corner_radius=15, font=montserrat_regular)
    input_box.pack(pady=(5, 10), padx=20, fill="x")

    # Set focus to the input box when the chatbot starts
    input_box.focus_set()

    # Bind Enter/Return key to send the message
    input_box.bind("<Return>", lambda event: handle_query(event) or "break")
    input_box.bind("<KeyRelease>", adjust_input_box_height)

    # Create a button to send the query with rounded corners
    send_button = ctk.CTkButton(root, text="Send", font=montserrat_semibold,
                                command=handle_query, corner_radius=15)
    send_button.pack(pady=(5, 20), padx=15)

    # Start the main GUI loop
    root.mainloop()

if __name__ == "__main__":
    run_chatbot()