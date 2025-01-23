from typing import Dict, Any, List, Tuple, Union, Literal, Annotated
import json
from inspect import signature, Parameter, getdoc

from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from loguru import logger

from app.agent.prompts import understand_prompt, execute_prompt
from app.agent.tools import get_tools
from app.agent.openai_service import OpenAIService
from app.agent.schema.response import AgentResponse, ExecuteResponse


class State(BaseModel):
    input: str
    response: str = ""
    understanding: Dict[str, Any] = {}

class Agent:
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Inicjalizacja agenta.
        
        Args:
            config: Konfiguracja agenta
        """
        self.config = config or {}
        self.openai = OpenAIService()
        self.workflow = self._create_workflow()
        self.tools = get_tools()

    def _create_workflow(self) -> StateGraph:
        """
        Tworzy graf przepływu pracy agenta.
        """
        workflow = StateGraph(State)
        
        # Dodanie węzłów
        workflow.add_node("understand", self.understand)
        workflow.add_node("execute", self.execute_tool)
        
        # Dodanie krawędzi
        workflow.add_edge(START, "understand")
        workflow.add_edge("understand", "execute")
        workflow.add_edge("execute", END)
        
        return workflow.compile()
    
    @classmethod
    async def process(cls, input: str) -> str:
        agent = cls()
        workflow = agent._create_workflow()
        state = State(input=input)
        result = await workflow.ainvoke(state)
        return result
    
    async def understand(self, state: State) -> str:
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
        response = await self.openai.completion(config)
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
        tool_descriptions = []
        for name, tool in self.tools.items():
            sig = signature(tool)
            params = []
            for param_name, param in sig.parameters.items():
                if param.annotation == Parameter.empty:
                    param_type = "any"
                elif hasattr(param.annotation, "__name__"):
                    param_type = param.annotation.__name__
                else:
                    param_type = str(param.annotation)
                
                default = f" (default: {param.default})" if param.default != Parameter.empty else ""
                params.append(f"{param_name}: {param_type}{default}")
            
            params_str = ", ".join(params)
            doc = getdoc(tool) or "No description available"
            tool_descriptions.append(f"- {name}: {doc}\n  Parameters: {params_str}")
        
        tool_descriptions = "\n".join(tool_descriptions)
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
    
    async def match_input_data(self, input: str) -> str:
        pass
    
