"""
セッション - 簡易的なセッション管理クラス
"""

class SessionState:
    """
    セッション状態管理クラス
    """
    def __init__(self):
        """
        SessionStateの初期化
        """
        self.state = {}
        
    def set(self, key, value):
        """
        状態に値を設定
        
        Args:
            key: 状態のキー
            value: 状態の値
        """
        self.state[key] = value
        
    def get(self, key, default=None):
        """
        状態から値を取得
        
        Args:
            key: 状態のキー
            default: キーが存在しない場合のデフォルト値
            
        Returns:
            取得した値またはデフォルト値
        """
        return self.state.get(key, default)

class Session:
    """
    セッションクラス
    """
    def __init__(self, id=None):
        """
        Sessionの初期化
        
        Args:
            id: セッションID
        """
        self.id = id
        self.state = SessionState() 