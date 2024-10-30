import os
import logging
from dotenv import load_dotenv

# Import the financial assistant agent and the chatbot interface
from agent_finmodel.financial_assistant import FinancialAssistantAgent
from gui.chatbot_interface import show_chatbot  # Import the function to launch the chatbot interface

# Set the logging level to ERROR to suppress warnings from autogen.oai.client
logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# OpenAI API key is expected to be used within the agent or other scripts

def main():
    # Initialize the FinancialAssistantAgent
    agent = FinancialAssistantAgent()
    
    # Run the chatbot interface with the agent instance
    show_chatbot(agent_instance=agent)
    
if __name__ == "__main__":
    main()
