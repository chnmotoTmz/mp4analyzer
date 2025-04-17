"""
音声認識エージェント - 動画内の音声を文字起こしするエージェント
"""
from .base_agent import BaseAgent
from ..tools.transcription import transcribe_audio

class TranscriptionAgent(BaseAgent):
    """
    Faster Whisperを使用して音声を文字起こしするエージェント
    """
    def __init__(self):
        super().__init__(
            name="transcription_agent",
            model="gemini-2.0-flash",
            description="動画内の音声を文字起こしするエージェント",
            instruction="Faster Whisperを使用して高精度な音声認識を行います。日本語に最適化されています。",
            tools=[transcribe_audio]
        )
