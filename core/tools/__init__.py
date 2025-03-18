from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Dict, Any

class ToolConfig(BaseModel):
    name: str
    description: str
    version: str = "1.0"

class BaseTool(BaseModel, ABC):
    """工具抽象基类"""
    config: ToolConfig
    enabled: bool = True

    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> Dict:
        """必须实现的执行方法"""
        pass

    def validate_config(self) -> bool:
        """配置验证基础实现"""
        return bool(self.config.name.strip())

    @classmethod
    def create_from_config(cls, config: Dict) -> 'BaseTool':
        """根据配置创建工具实例"""
        return cls(config=ToolConfig(**config))