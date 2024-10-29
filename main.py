from dotenv import load_dotenv
import openai
from agent_financial.financial_assistant import FinancialAssistantAgent
from gui.chatbot_interface import run_chatbot  # Import the chatbot interface
import os
import logging

# Set the logging level to ERROR to suppress warnings from autogen.oai.client
logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

def main():
    # Initialize the FinancialAssistantAgent (in case it's used inside the chatbot)
    agent = FinancialAssistantAgent()
    
    # Run the chatbot interface instead of run_conversation
    run_chatbot()  # This launches the chatbot UI
    
if __name__ == "__main__":
    main()
