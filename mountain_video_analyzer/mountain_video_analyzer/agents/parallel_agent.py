"""
パラレルエージェント - 複数のエージェントを並列に実行するエージェント
"""

class ParallelAgent:
    """
    パラレルエージェントクラス
    """
    def __init__(self, name, sub_agents=None):
        """
        ParallelAgentの初期化
        
        Args:
            name: エージェント名
            sub_agents: 並列に実行するサブエージェントのリスト
        """
        self.name = name
        self.sub_agents = sub_agents or [] 