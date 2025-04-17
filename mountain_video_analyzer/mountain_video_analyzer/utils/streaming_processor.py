"""
ストリーミング処理サポート - リアルタイム分析機能
"""
import asyncio
from ..agents.main_agent import MountainVideoAnalyzerAgent
from ..utils.session_manager import SessionManager
from google.adk.runners import Runner

class StreamingProcessor:
    """
    動画のストリーミング処理を行うクラス
    """
    def __init__(self, main_agent=None):
        """
        StreamingProcessorの初期化
        
        Args:
            main_agent: メインエージェント（Noneの場合は新しく作成）
        """
        self.main_agent = main_agent or MountainVideoAnalyzerAgent()
        self.session_manager = None
        self.runner = Runner()
    
    async def start_streaming(self, video_path, callback):
        """
        ストリーミング処理を開始
        
        Args:
            video_path: 動画ファイルのパス
            callback: 結果を受け取るコールバック関数
        """
        # セッションを初期化
        self.session_manager = SessionManager()
        self.session_manager.set_state("video_path", video_path)
        self.session_manager.set_state("streaming", True)
        
        # エージェントを実行
        async for event in self.runner.run_agent(
            agent=self.main_agent.get_agent(),
            session=self.session_manager.get_session(),
            message=f"動画 {video_path} をストリーミング分析します。リアルタイムで結果を返してください。",
            stream=True  # ストリーミングモードを有効化
        ):
            # イベントをコールバックに渡す
            if event.content:
                await callback({
                    "type": event.type,
                    "author": event.author,
                    "content": event.content,
                    "timestamp": asyncio.get_event_loop().time()
                })
    
    def stop_streaming(self):
        """
        ストリーミング処理を停止
        """
        if self.session_manager:
            self.session_manager.set_state("streaming", False)
    
    async def get_final_result(self):
        """
        最終結果を取得
        
        Returns:
            dict: 処理結果
        """
        if not self.session_manager:
            return {"error": "ストリーミングが開始されていません"}
        
        return {
            "scenes": self.session_manager.get_state("scenes", []),
            "descriptions": self.session_manager.get_state("descriptions", []),
            "editing_suggestions": self.session_manager.get_state("editing_suggestions", [])
        }
