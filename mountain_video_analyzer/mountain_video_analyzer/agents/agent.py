"""
エージェント - Google ADK代替エージェントクラス
"""

class Agent:
    """
    エージェントクラス
    """
    def __init__(self, name, model=None, description=None, instruction=None, tools=None):
        """
        Agentの初期化
        
        Args:
            name: エージェント名
            model: 使用するモデル名
            description: エージェントの説明
            instruction: エージェントの指示
            tools: エージェントが使用するツールのリスト
        """
        self.name = name
        self.model = model
        self.description = description
        self.instruction = instruction
        self.tools = tools or [] 