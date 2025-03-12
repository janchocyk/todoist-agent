from typing import Dict, Tuple, List
import json
from loguru import logger

from app.agent.schema.response import AgentResponse, ExecuteResponse
from app.agent.prompts import understand_prompt, execute_prompt, finalizer_prompt
from app.agent.openai_service import OpenAIService
from app.agent.tools import get_tool_descriptions, get_tools
from app.agent.schema import State


class Nodes:
    def __init__(self):
        self.llm = OpenAIService()

    @classmethod    
    async def understand_node(cls, state: State) -> Dict[str, Dict[str, str]]:
        """
        Node responsible for understanding user input and converting it to a structured format.
        """
        node = cls()
        system_prompt = await understand_prompt()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": state.input},
        ]
        config = {
            "messages": messages,
            "jsonMode": True,
            "name": "understand",
        }

        response = await node.llm.completion(config)
        try:
            response = json.loads(response)
            logger.info(f"Agent response: {response}")
            response = AgentResponse(**response)
            steps, go_tool = cls._prepare_steps(response)
            logger.info(f"Steps: {steps}")
        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            raise e
        return {
            "understanding": response.model_dump(), 
            "steps": steps, 
            "go_tool": go_tool
        }

    @classmethod
    async def decision_router(cls, state: State) -> str:
        if state.go_tool:
            return "execute"
        else:
            return "finalize"

    @classmethod
    async def execute_tool_node(cls, state: State) -> State:
        try:
            node = cls()
            steps = state.steps
            tool_calls = state.tool_calls
            tool_descriptions = await get_tool_descriptions()
            step = steps[0]
            system_prompt = await execute_prompt(tool_descriptions)
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"User intent: {step}"}
            ]
            config = {
                "messages": messages,
                "jsonMode": True,
                "name": "execute",
            }
        except Exception as e:
            logger.error(f"Error executing tool: {e}")
            raise e

        try:
            response = await node.llm.completion(config)
            execution_plan = json.loads(response)
            logger.info(f"Execution plan: {execution_plan}")
            actions = []
            if isinstance(execution_plan, list):
                for plan in execution_plan:
                    action_to_call = ExecuteResponse(**plan)
                    actions.append(action_to_call)
            elif isinstance(execution_plan, dict):
                if execution_plan.get("error"):
                    tool_response = {"step": step, "error": execution_plan.get("info")}
                else:
                    action_to_call = ExecuteResponse(**execution_plan)
                    actions.append(action_to_call)
            tools = await get_tools()
            
            for action in actions:
                try:
                    tool = tools[action.tool_name]
                    result = await tool(**action.arguments)
                    tool_response = {"step": action.model_dump(), "result": result}
                    logger.info(f"Tool response: {tool_response}")
                except Exception as e:
                    tool_response = {"step": step, "error": f"Tool {action.tool_name} not found"}
                    logger.error(f"Error executing tool: {e}")
            steps.remove(step)   
            tool_calls.append(tool_response)      
            if len(steps) > 0:
                go_tool = True
            else:
                go_tool = False

            return {
                "steps": steps, 
                "tool_calls": tool_calls, 
                "go_tool": go_tool
            }
        except Exception as e:
            logger.error(f"Error executing tool: {e}")
            raise e
    
    @classmethod
    async def finalizer_node(cls, state: State) -> State:
        node = cls()
        user_query = state.input
        tool_calls = state.tool_calls
        system_prompt = await finalizer_prompt(user_query, tool_calls)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Raport: "}
        ]
        config = {
            "messages": messages,
            "jsonMode": False,
            "name": "finalizer",
        }
        response = await node.llm.completion(config)
        return {"final_response": response}
    
    @staticmethod
    def _prepare_steps(response: AgentResponse) -> Tuple[List[str], bool]:
        steps = []
        for action, content in response.model_dump().items():
            if content:
                steps.append(f"{action}: {content}")
        if len(steps) > 0:
            go_tool = True
        else:
            go_tool = False
        return steps, go_tool
