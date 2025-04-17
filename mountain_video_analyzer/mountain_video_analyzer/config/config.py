"""
設定ファイル - 拡張性を考慮した設計
"""
CONFIG = {
    "models": {
        "default": "gemini-2.0-flash",
        "vision": "gemini-1.5-flash",
        "description": "gemini-1.5-pro",
        "interactive": "gemini-2.0-flash-live-001"
    },
    "scene_detection": {
        "min_scene_length": 5.0,
        "silence_threshold": -30,  # dB
        "silence_duration": 1.0    # seconds
    },
    "transcription": {
        "model_size": "large-v3",
        "language": "ja",
        "beam_size": 5
    },
    "analysis": {
        "frames_per_scene": 3,
        "context_window": 5  # シーン前後の文脈を考慮する数
    },
    "ui": {
        "thumbnail_size": (320, 180),
        "preview_duration": 5.0,
        "max_scenes_per_page": 10
    }
}

# Gemini API設定
GEMINI_API_KEY = "AIzaSyDWhsY1oVCat_I1rDtInGOu764zrDObB4I"  # 実際の使用時にはこれを環境変数から取得するか、安全な方法で管理してください
