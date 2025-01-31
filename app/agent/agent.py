from typing import Dict, Any

from langgraph.graph import StateGraph, START, END

from app.agent.nodes import Nodes
from app.agent.schema import State
from app.core import logger

class Agent:
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Inicjalizacja agenta.
        
        Args:
            config: Konfiguracja agenta
        """
        self.config = config or {}
        self.workflow = self._create_workflow()

    def _create_workflow(self) -> StateGraph:
        """
        Tworzy graf przepływu pracy agenta.
        """
        workflow = StateGraph(State)
        
        # Dodanie węzłów
        workflow.add_node("understand", Nodes.understand_node)
        workflow.add_node("execute", Nodes.execute_tool_node)
        workflow.add_node("finalize", Nodes.finalizer_node)
        # Dodanie krawędzi
        workflow.add_edge(START, "understand")
        workflow.add_conditional_edges("understand", Nodes.decision_router, ["execute", "finalize"])
        workflow.add_conditional_edges("execute", Nodes.decision_router, ["execute", "finalize"])
        workflow.add_edge("finalize", END)
        
        return workflow.compile()
    
    @classmethod
    async def process(cls, input: str) -> str:
        agent = cls()
        workflow = agent._create_workflow()
        state = State(input=input)
        logger.info(f"State: {state}")
        result = await workflow.ainvoke(state)
        return result
