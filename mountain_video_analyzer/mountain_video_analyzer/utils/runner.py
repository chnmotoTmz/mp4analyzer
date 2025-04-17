"""
ランナー - エージェントを実行するためのクラス
"""
import asyncio

class RunnerEvent:
    """
    ランナーイベントクラス
    """
    def __init__(self, author, content=None, type="message"):
        """
        RunnerEventの初期化
        
        Args:
            author: イベントの発行者
            content: イベントの内容
            type: イベントのタイプ
        """
        self.author = author
        self.content = content
        self.type = type

class Runner:
    """
    エージェント実行ランナークラス
    """
    async def run_agent(self, agent, session, message, stream=False):
        """
        エージェントを実行する
        
        Args:
            agent: 実行するエージェント
            session: セッション
            message: 送信メッセージ
            stream: ストリーミングフラグ
            
        Yields:
            RunnerEvent: ランナーイベント
        """
        # エージェント実行のモック
        yield RunnerEvent("user", message)
        
        # モック応答
        response = f"【エージェント {agent.name}】: メッセージを受信しました: {message}"
        
        if stream:
            # ストリーミングモードの場合は少しずつ応答
            for i in range(3):
                await asyncio.sleep(0.5)
                chunk = f"処理中... {i+1}/3"
                yield RunnerEvent("agent", chunk, "partial")
        
        # 最終応答
        yield RunnerEvent("agent", response) 