from typing import Dict, Any
import json
from loguru import logger

from app.agent.schema.response import AgentResponse, ExecuteResponse
from app.agent.prompts import understand_prompt, execute_prompt
from app.agent.openai_service import OpenAIService
from app.agent.tools import get_tool_descriptions
from app.agent.schema import State


class Nodes:
    def __init__(self):
        self.openai = OpenAIService()

    @classmethod
    async def understand(cls, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Node responsible for understanding user input and converting it to a structured format.
        """
        node = cls()
        system_prompt = await understand_prompt()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": state["input"]},
        ]
        config = {
            "messages": messages,
            "jsonMode": True,
            "name": "understand",
        }

        response = await node.openai.completion(config)
        try:
            response = json.loads(response)
            logger.info(f"Agent response: {response}")
            response = AgentResponse(**response)
        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            raise e
        return {"understanding": response.model_dump()}

    async def execute_tool(self, state: State) -> State:
        # Get tool descriptions with parameters
        tool_descriptions = await get_tool_descriptions()
        logger.info(f"Tool descriptions: {tool_descriptions}")

        system_prompt = await execute_prompt(tool_descriptions)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Understanding: {json.dumps(state.understanding)}"}
        ]
        
        config = {
            "messages": messages,
            "jsonMode": True,
            "name": "execute",
        }
        
        try:
            response = await self.openai.completion(config)
            execution_plan = json.loads(response)
            logger.info(f"Execution plan: {execution_plan}")
            execution_plan = ExecuteResponse(**execution_plan)
            tool_name = execution_plan.tool_name
            arguments = execution_plan.arguments
            
            if tool_name in self.tools:
                tool = self.tools[tool_name]
                result = await tool(**arguments)
                state.response = json.dumps(result)
            else:
                state.response = json.dumps({"error": f"Tool {tool_name} not found"})
            
            return state
        except Exception as e:
            logger.error(f"Error executing tool: {e}")
            state.response = json.dumps({"error": str(e)})
            return state
