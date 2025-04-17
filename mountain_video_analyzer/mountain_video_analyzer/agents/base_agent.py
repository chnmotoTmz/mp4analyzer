"""
基本エージェントクラス - 他のすべてのエージェントの基底クラス
"""
from ..agents.agent import Agent
from ..config import CONFIG

class BaseAgent:
    """
    基本エージェントクラス
    すべてのエージェントはこのクラスを継承します
    """
    def __init__(self, name, model=None, description=None, instruction=None, tools=None):
        """
        BaseAgentの初期化
        
        Args:
            name: エージェント名
            model: 使用するモデル名（Noneの場合はCONFIGからデフォルト値を取得）
            description: エージェントの説明
            instruction: エージェントの指示
            tools: エージェントが使用するツールのリスト
        """
        self.name = name
        self.model = model or CONFIG["models"]["default"]
        self.description = description
        self.instruction = instruction
        self.tools = tools or []
        
        # ADKエージェントの作成
        self.agent = Agent(
            name=self.name,
            model=self.model,
            description=self.description,
            instruction=self.instruction,
            tools=self.tools
        )
    
    def get_agent(self):
        """
        エージェントを返す
        
        Returns:
            Agent: ADKエージェント
        """
        return self.agent
