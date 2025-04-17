"""
画像分析エージェント - シーンの視覚情報を分析するエージェント
"""
from .base_agent import BaseAgent
from ..tools.vision_analysis import analyze_frames

class VisionAnalysisAgent(BaseAgent):
    """
    Gemini 1.5 Flashを使用してシーンの視覚情報を分析するエージェント
    """
    def __init__(self):
        super().__init__(
            name="vision_analyst",
            model="gemini-1.5-flash",
            description="シーンの視覚情報を分析するエージェント",
            instruction="動画フレームから場所、活動、天候などの情報を抽出します。登山動画に特化した分析を行います。",
            tools=[analyze_frames]
        )
