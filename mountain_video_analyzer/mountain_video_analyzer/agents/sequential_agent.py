"""
シーケンシャルエージェント - 複数のエージェントを順番に実行するエージェント
"""

class SequentialAgent:
    """
    シーケンシャルエージェントクラス
    """
    def __init__(self, name, description=None, sub_agents=None):
        """
        SequentialAgentの初期化
        
        Args:
            name: エージェント名
            description: エージェントの説明
            sub_agents: 実行するサブエージェントのリスト
        """
        self.name = name
        self.description = description
        self.sub_agents = sub_agents or [] 