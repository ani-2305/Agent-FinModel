# financial_assistant.py

from string import Template
import autogen  # Ensure you have autogen installed
import openai
import os
from dotenv import load_dotenv
import logging
import asyncio

from agents.planner_agent import PlannerAgent
from agents.executor_agent import ExecutorAgent

from skills import (
    extract_financial_statements,
    collect_user_assumptions,
    validate_user_inputs,
    build_historical_model,
    forecast_financials,
    apply_accounting_policies,
    implement_depreciation_methods,
    calculate_working_capital,
    implement_tax_calculations,
    insert_formulas,
    render_excel_model,
    file_management,
    error_handling,
    shared_state,
    format_excel_sheets,
    apply_conditional_formatting,
    provide_model_summary
)
from prompts import FINANCIAL_PROMPTS

# Configure logging
logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("API key not found. Make sure it's set correctly in your .env file")
openai.api_key = OPENAI_API_KEY

class FinancialAssistantAgent:
    def __init__(self):
        user_ltm = self.__get_ltm()
        system_message = FINANCIAL_PROMPTS["FINANCIAL_AGENT_PROMPT"]

        if user_ltm:
            user_ltm = "\n" + user_ltm
            system_message = Template(system_message).substitute(basic_user_information=user_ltm)

        # Initialize the assistant agent
        self.agent = autogen.AssistantAgent(
            name="financial_assistant_agent",
            system_message=system_message,
            llm_config={
                "config_list": [{"model": "gpt-4", "api_key": OPENAI_API_KEY}],
                "cache_seed": 2,
                "temperature": 0.0
            },
        )

        # Initialize the user proxy agent
        self.user_proxy_agent = autogen.UserProxyAgent(
            name="user_proxy_agent",
            is_termination_msg=lambda x: x.get("content", "") and 'Task completed. How else may I assist you?' in x.get("content", ""),
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            code_execution_config={
                "work_dir": "financial_tasks",
                "use_docker": False,
            },
        )

        # Initialize Planner and Executor Agents
        self.planner_agent = PlannerAgent()
        self.executor_agent = ExecutorAgent(self.user_proxy_agent)

        # Register skills
        self.__register_skills()

    def __get_ltm(self):
        # Placeholder for long-term memory retrieval
        return None

    def __register_skills(self):
        """
        Register skills for the financial assistant agent.
        """
        # List of skill functions and their descriptions
        skill_functions = [
            (extract_financial_statements.extract_financial_statements, FINANCIAL_PROMPTS["EXTRACT_FINANCIAL_STATEMENTS_PROMPT"]),
            (collect_user_assumptions.collect_user_assumptions, FINANCIAL_PROMPTS["COLLECT_USER_ASSUMPTIONS_PROMPT"]),
            (validate_user_inputs.validate_user_inputs, FINANCIAL_PROMPTS["VALIDATE_USER_INPUTS_PROMPT"]),
            (build_historical_model.build_historical_model, FINANCIAL_PROMPTS["BUILD_HISTORICAL_MODEL_PROMPT"]),
            (forecast_financials.forecast_financials, FINANCIAL_PROMPTS["FORECAST_FINANCIALS_PROMPT"]),
            (apply_accounting_policies.apply_accounting_policies, FINANCIAL_PROMPTS["APPLY_ACCOUNTING_POLICIES_PROMPT"]),
            (implement_depreciation_methods.implement_depreciation_methods, FINANCIAL_PROMPTS["IMPLEMENT_DEPRECIATION_METHODS_PROMPT"]),
            (calculate_working_capital.calculate_working_capital, FINANCIAL_PROMPTS["CALCULATE_WORKING_CAPITAL_PROMPT"]),
            (implement_tax_calculations.implement_tax_calculations, FINANCIAL_PROMPTS["IMPLEMENT_TAX_CALCULATIONS_PROMPT"]),
            (insert_formulas.insert_formulas, FINANCIAL_PROMPTS["INSERT_FORMULAS_PROMPT"]),
            (render_excel_model.render_excel_model, FINANCIAL_PROMPTS["RENDER_EXCEL_MODEL_PROMPT"]),
            (file_management.validate_file_path, FINANCIAL_PROMPTS["VALIDATE_FILE_PATH_PROMPT"]),
            (file_management.save_file, FINANCIAL_PROMPTS["SAVE_FILE_PROMPT"]),
            (file_management.backup_file, FINANCIAL_PROMPTS["BACKUP_FILE_PROMPT"]),
            (format_excel_sheets.format_excel_sheets, FINANCIAL_PROMPTS["FORMAT_EXCEL_SHEETS_PROMPT"]),
            (apply_conditional_formatting.apply_conditional_formatting, FINANCIAL_PROMPTS["APPLY_CONDITIONAL_FORMATTING_PROMPT"]),
            (provide_model_summary.provide_model_summary, FINANCIAL_PROMPTS["PROVIDE_MODEL_SUMMARY_PROMPT"]),
            # Ensure shared_state and error_handling are available
            # but they do not need to be registered as skills
        ]

        # Register each skill with both the user proxy agent and the assistant agent
        for func, prompt in skill_functions:
            # Register for execution with the user proxy agent
            self.user_proxy_agent.register_for_execution()(func)
            # Register with the assistant agent for LLM interaction
            self.agent.register_for_llm(description=prompt)(func)

    def print_message_from_user_proxy(self, *args, **kwargs):
        pass

    def print_message_from_agent(self, *args, **kwargs):
        pass

    async def handle_request(self, user_input: str, context: dict):
        """
        Handles the user's request by planning and executing tasks.

        :param user_input: The user's input.
        :param context: Context containing user data.
        :return: Response to the user.
        """
        # Use the Planner Agent to plan actions
        actions = self.planner_agent.plan(user_input)
        # Use the Executor Agent to execute actions
        result = await self.executor_agent.execute(actions, context)
        return result

    def run(self):
        asyncio.run(self.run_conversation())

    async def run_conversation(self):
        while True:
            user_input = input("Enter your command: ")
            if user_input.lower() == "exit":
                break

            context = {
                'file_path': 'Financial_Model_Input.xlsx',  # Replace with actual file path
                'output_path': 'Financial_Model_Output.xlsx',  # Replace with desired output path
                'template_path': 'Financial_Model_Template.xlsx'  # Path to your Excel template
            }

            result = await self.handle_request(user_input, context)

            if 'error' in result:
                print(f"Error: {result['error']}")
            else:
                print(f"Success: {result.get('message', 'Task completed.')}")
                if 'summary' in result:
                    print("Model Summary:")
                    for key, value in result['summary'].items():
                        print(f"{key}: {value}")

if __name__ == "__main__":
    agent = FinancialAssistantAgent()
    agent.run()
