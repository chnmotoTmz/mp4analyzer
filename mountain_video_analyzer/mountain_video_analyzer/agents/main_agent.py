"""
メインオーケストレーションエージェント - 登山動画を包括的に分析するメインエージェント
"""
from .sequential_agent import SequentialAgent
from .parallel_agent import ParallelAgent
from .scene_detection_agent import SceneDetectionAgent
from .transcription_agent import TranscriptionAgent
from .vision_analysis_agent import VisionAnalysisAgent
from .description_agent import DescriptionAgent
from .editing_suggestion_agent import EditingSuggestionAgent

class MountainVideoAnalyzerAgent:
    """
    登山動画を包括的に分析し、説明と編集提案を生成するメインエージェント
    """
    def __init__(self):
        # 各エージェントのインスタンスを作成
        self.scene_detection_agent = SceneDetectionAgent()
        self.transcription_agent = TranscriptionAgent()
        self.vision_analysis_agent = VisionAnalysisAgent()
        self.description_agent = DescriptionAgent()
        self.editing_suggestion_agent = EditingSuggestionAgent()
        
        # メインのオーケストレーションエージェントを作成
        self.agent = SequentialAgent(
            name="mountain_video_analyzer",
            description="登山動画を包括的に分析し、説明と編集提案を生成するシステム",
            sub_agents=[
                self.scene_detection_agent.get_agent(),
                ParallelAgent(
                    name="parallel_analysis",
                    sub_agents=[
                        self.transcription_agent.get_agent(), 
                        self.vision_analysis_agent.get_agent()
                    ]
                ),
                self.description_agent.get_agent(),
                self.editing_suggestion_agent.get_agent()
            ]
        )
    
    def get_agent(self):
        """
        メインエージェントを返す
        """
        return self.agent
