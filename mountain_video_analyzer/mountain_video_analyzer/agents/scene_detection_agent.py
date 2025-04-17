"""
シーン検出エージェント - 動画からシーンを検出するエージェント
"""
from .base_agent import BaseAgent
from ..tools.scene_detection import detect_scenes

class SceneDetectionAgent(BaseAgent):
    """
    FFmpegを使用して動画からシーンを検出するエージェント
    """
    def __init__(self):
        super().__init__(
            name="scene_detector",
            model="gemini-2.0-flash",
            description="動画からシーンを検出するエージェント",
            instruction="FFmpegを使用して動画を分析し、無音区間などに基づいて自然なシーン区切りを検出します。",
            tools=[detect_scenes]
        )
