from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Dict, List
from .planner import PlanModel

class Task(BaseModel):
    plan: PlanModel
    current_step: int = 0
    status: str = "pending"

class Orchestrator(BaseModel, ABC):
    """专家层核心协调器抽象类"""
    planner: BasePlanner
    active_tasks: Dict[str, Task] = {}
    agent_registry: Dict[str, BaseAgent] = {}

    @abstractmethod
    def assign_task(self, task_id: str, plan: PlanModel):
        """初始化任务分配"""
        pass

    def execute_step(self, task_id: str):
        """执行当前步骤"""
        task = self.active_tasks[task_id]
        current_step = task.plan.steps[task.current_step]
        agent = self.agent_registry[current_step['agent']]
        return agent.execute(current_step)

    @abstractmethod
    def handle_error(self, task_id: str, error: Exception):
        """异常处理抽象方法"""
        pass

    def track_progress(self, task_id: str) -> Dict:
        """获取任务进度状态"""
        task = self.active_tasks.get(task_id)
        return {
            "progress": f"{task.current_step}/{len(task.plan.steps)}",
            "status": task.status
        }