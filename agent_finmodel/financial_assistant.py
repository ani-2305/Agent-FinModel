from string import Template
import autogen  # type: ignore
import openai
import os
from dotenv import load_dotenv
import logging

from agent_financial.skills import (
    change_font, modify_chart, adjust_bullet_points, insert_equation, fill_data, create_chart, create_new, 
    open_application, open_file, get_root_path
)
from agent_financial.utils.helper_functions import financial_helper
from agent_financial.prompts import FINANCIAL_PROMPTS

logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)

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

        self.agent = autogen.AssistantAgent(
            name="financial_assistant_agent",
            system_message=system_message,
            llm_config={
                "config_list": [{"model": "gpt-4o", "api_key": OPENAI_API_KEY}],
                "cache_seed": 2,
                "temperature": 0.0
            },
        )

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


        self.__register_skills()

    def __get_ltm(self):
        return None

    def __register_skills(self):
        """
        Register skills for the financial assistant agent.
        Each skill will handle a specific task such as changing fonts,
        creating charts, modifying bullet points, etc.
        """
        self.user_proxy_agent.register_for_execution()(change_font.change_font)
        self.agent.register_for_llm(
            description=FINANCIAL_PROMPTS["CHANGE_FONT_PROMPT"]
        )(change_font.change_font)

        self.user_proxy_agent.register_for_execution()(modify_chart.modify_chart)
        self.agent.register_for_llm(
            description=FINANCIAL_PROMPTS["MODIFY_CHART_PROMPT"]
        )(modify_chart.modify_chart)

        self.user_proxy_agent.register_for_execution()(adjust_bullet_points.adjust_bullet_points)
        self.agent.register_for_llm(
            description=FINANCIAL_PROMPTS["ADJUST_BULLET_POINTS_PROMPT"]
        )(adjust_bullet_points.adjust_bullet_points)

        self.user_proxy_agent.register_for_execution()(insert_equation.insert_equation)
        self.agent.register_for_llm(
            description=FINANCIAL_PROMPTS["INSERT_EQUATION_PROMPT"]
        )(insert_equation.insert_equation)

        self.user_proxy_agent.register_for_execution()(fill_data.fill_data)
        self.agent.register_for_llm(
            description=FINANCIAL_PROMPTS["FILL_DATA_PROMPT"]
        )(fill_data.fill_data)

        self.user_proxy_agent.register_for_execution()(create_chart.create_chart)
        self.agent.register_for_llm(
            description=FINANCIAL_PROMPTS["CREATE_CHART_PROMPT"]
        )(create_chart.create_chart)

        self.user_proxy_agent.register_for_execution()(create_new.create_new)
        self.agent.register_for_llm(
            description=FINANCIAL_PROMPTS["CREATE_NEW_PROMPT"]
        )(create_new.create_new)

        self.user_proxy_agent.register_for_execution()(open_application.open_application)
        self.agent.register_for_llm(
            description=FINANCIAL_PROMPTS["OPEN_APPLICATION_PROMPT"]
        )(open_application.open_application)

        self.user_proxy_agent.register_for_execution()(open_file.open_file)
        self.agent.register_for_llm(
            description=FINANCIAL_PROMPTS["OPEN_FILE_PROMPT"]
        )(open_file.open_file)

        self.user_proxy_agent.register_for_execution()(get_root_path.get_root_path)
        self.agent.register_for_llm(
            description=FINANCIAL_PROMPTS["GET_ROOT_PATH_PROMPT"]
        )(get_root_path.get_root_path)


    def print_message_from_user_proxy(self, *args, **kwargs):
        pass

    def print_message_from_agent(self, *args, **kwargs):
        pass

    async def run_conversation(self):
        while True:
            user_input = input("Enter your command: ")
            if user_input.lower() == "exit":
                break

            result = await self.user_proxy_agent.a_initiate_chat(
                self.agent,
                message=user_input,
                cache=None
            )

            summary = result.summary
            response = {'type': 'answer', 'content': summary}
            print(f"Agent response: {response}")
