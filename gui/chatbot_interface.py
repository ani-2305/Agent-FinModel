# chatbot_interface.py

import tkinter as tk
import customtkinter as ctk # type: ignore
import os
import re
import xlwings as xw # type: ignore
import threading
import asyncio

# Import the financial assistant agent
from agent_finmodel.financial_assistant import FinancialAssistantAgent

# Initialize the financial assistant agent
agent = FinancialAssistantAgent()

# Global variables
file_path = None
root = None

def show_chatbot():
    """
    Function to show the chatbot interface.
    This function can be called from Excel via xlwings.
    """
    threading.Thread(target=run_chatbot).start()

def run_chatbot():
    global root, chat_frame, chat_canvas, input_box

    # Initialize customtkinter appearance
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # Create the main window
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

def adjust_input_box_height(event=None):
    """Adjust the height of the input box based on the content."""
    content = input_box.get("1.0", "end").strip()
    lines = content.count("\n") + 1
    new_height = min(max(lines * 20, 60), 200)
    input_box.configure(height=new_height)

def add_message(sender, message):
    """Add a message to the chat interface."""
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
    message_label = ctk.CTkLabel(message_frame, text=message, font=montserrat_regular, anchor="w",
                                justify="left", wraplength=320)
    message_label.pack(fill="x", anchor="w")

    # Scroll to the bottom
    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1.0)

def handle_query(event=None):
    """Handle the user's query and get a response from the agent."""
    user_input = input_box.get("1.0", "end").strip()
    input_box.delete("1.0", "end")
    add_message("You", user_input)

    # Get the active workbook path
    try:
        wb = xw.Book.caller()
        file_path = wb.fullname
    except Exception:
        file_path = None

    # Asynchronous function to call the agent and get the response
    def query_agent(user_input, file_path):
        # Prepare context
        if file_path:
            context = {
                'file_path': file_path,
                'output_path': 'Financial_Model_Output.xlsx',
                'template_path': 'Financial_Model_Template.xlsx'
            }
        else:
            context = {
                'file_path': 'Financial_Model_Input.xlsx',
                'output_path': 'Financial_Model_Output.xlsx',
                'template_path': 'Financial_Model_Template.xlsx'
            }

        # Run the agent asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(agent.handle_request(user_input, context))
        finally:
            loop.close()

        # Process the result
        if 'error' in result:
            response = f"Error: {result['error']}"
        else:
            response = result.get('message', 'Task completed.')
            if 'summary' in result:
                summary = result['summary']
                response += "\nModel Summary:"
                for key, value in summary.items():
                    response += f"\n{key}: {value}"

        # Add the agent's response to the chat
        add_message("Agent Fin", response)

    # Run the agent query in a separate thread to avoid blocking the GUI
    threading.Thread(target=query_agent, args=(user_input, file_path)).start()

if __name__ == "__main__":
    show_chatbot()
