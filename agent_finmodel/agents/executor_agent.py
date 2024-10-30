# executor_agent.py

from skills import shared_state
from autogen import UserProxyAgent

class ExecutorAgent:
    def __init__(self, user_proxy_agent: UserProxyAgent):
        self.user_proxy_agent = user_proxy_agent

    async def execute(self, actions: list, context: dict) -> dict:
        """
        Executes the planned actions using the user proxy agent.

        :param actions: List of actions to execute.
        :param context: Shared context and data.
        :return: Result of the execution.
        """
        shared_state.shared_state.current_file_path = context.get('file_path')
        shared_state.shared_state.output_path = context.get('output_path')
        shared_state.shared_state.template_path = context.get('template_path')

        for action in actions:
            # Prepare the execution command
            message = {
                'type': 'command',
                'content': action,
                'context': context
            }

            # Invoke the skill via the user proxy agent
            result = await self.user_proxy_agent.a_handle_message(message)

            if isinstance(result, dict) and 'error' in result:
                return result  # Stop execution if an error occurs

        # After all actions are executed, provide the final result or summary
        summary_result = await self.user_proxy_agent.a_handle_message({
            'type': 'command',
            'content': 'provide_model_summary',
            'context': context
        })

        return summary_result
