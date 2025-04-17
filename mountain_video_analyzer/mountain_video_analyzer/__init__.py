"""
__init__.pyファイル - パッケージ初期化
"""
from .config import CONFIG, GEMINI_API_KEY
from .agents import (
    BaseAgent,
    SceneDetectionAgent,
    TranscriptionAgent,
    VisionAnalysisAgent,
    DescriptionAgent,
    EditingSuggestionAgent,
    MountainVideoAnalyzerAgent
)
from .utils import (
    SessionManager,
    process_video,
    process_video_streaming,
    StreamingProcessor,
    PropertyQuerySystem,
    ErrorHandler,
    PerformanceOptimizer
)

__version__ = "1.0.0"
__author__ = "Mountain Video Analyzer Team"
