"""
関数ツール - 関数をエージェントツールとしてラップするクラス
"""

class FunctionTool:
    """
    関数ツールクラス
    """
    def __init__(self, func):
        """
        FunctionToolの初期化
        
        Args:
            func: ラップする関数
        """
        self.func = func
        self.name = func.__name__
        self.description = func.__doc__ or "" 