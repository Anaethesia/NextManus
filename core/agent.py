from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .tools import BaseTool

class AgentState(BaseModel):
    status: str = "idle"
    last_task: Optional[str] = None
    tools: List[str] = []

class BaseAgent(BaseModel, ABC):
    """Agent抽象基类"""
    agent_id: str
    tools: Dict[str, BaseTool]
    state: AgentState = AgentState()
    max_retries: int = 3

    @abstractmethod
    def execute(self, task: Dict[str, Any]) -> Dict:
        """执行具体任务步骤"""
        pass

    def bind_tools(self, tools: List[BaseTool]):
        """绑定工具集（参考Langchain设计）"""
        self.tools = {tool.name: tool for tool in tools}
        self.state.tools = list(self.tools.keys())

    def report_status(self) -> AgentState:
        """返回当前状态快照"""
        return self.state.copy()

    def validate_tools(self, required_tools: List[str]) -> bool:
        """验证工具集是否满足要求"""
        return all(tool in self.tools for tool in required_tools)