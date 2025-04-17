"""
説明文生成エージェント - シーンの説明文を生成するエージェント
"""
from .base_agent import BaseAgent

class DescriptionAgent(BaseAgent):
    """
    Gemini 1.5 Proを使用してシーンの説明文を生成するエージェント
    """
    def __init__(self):
        super().__init__(
            name="description_generator",
            model="gemini-1.5-pro",
            description="シーンの説明文を生成するエージェント",
            instruction="視覚情報と音声情報を組み合わせて、自然で情報量の多いシーン説明文を生成します。登山動画に特化した説明を行います。",
            tools=[]  # 主にLLMの推論能力を使用
        )
