"""
編集提案エージェント - 編集提案を行うエージェント
"""
from .base_agent import BaseAgent

class EditingSuggestionAgent(BaseAgent):
    """
    Gemini 1.5 Proを使用して編集提案を行うエージェント
    """
    def __init__(self):
        super().__init__(
            name="editing_advisor",
            model="gemini-1.5-pro",
            description="編集提案を行うエージェント",
            instruction="シーンの内容に基づいて、編集のアドバイスを提供します。編集ポイント、特殊効果、BGMなどを提案します。登山動画に特化した編集提案を行います。",
            tools=[]  # 主にLLMの推論能力を使用
        )
