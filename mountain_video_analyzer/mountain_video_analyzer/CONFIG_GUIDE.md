# 設定ファイル説明

`mountain_video_analyzer/config/config.py`ファイルには、システムの動作を制御するための様々な設定パラメータが含まれています。以下に各設定項目の詳細な説明を示します。

## モデル設定

```python
"models": {
    "default": "gemini-2.0-flash",
    "vision": "gemini-1.5-flash",
    "description": "gemini-1.5-pro",
    "interactive": "gemini-2.0-flash-live-001"
}
```

- **default**: デフォルトで使用されるGeminiモデル。BaseAgentクラスで明示的にモデルが指定されない場合に使用されます。
- **vision**: 画像分析に使用されるモデル。VisionAnalysisAgentで使用されます。
- **description**: 説明文生成に使用されるモデル。DescriptionAgentで使用されます。
- **interactive**: 対話型プロパティ照会に使用されるモデル。PropertyQuerySystemで使用されます。

## シーン検出設定

```python
"scene_detection": {
    "min_scene_length": 5.0,
    "silence_threshold": -30,  # dB
    "silence_duration": 1.0    # seconds
}
```

- **min_scene_length**: 最小シーン長（秒）。これより短いシーンは無視されます。
- **silence_threshold**: 無音と判断する閾値（dB）。この値より小さい音量は無音とみなされます。
- **silence_duration**: 無音と判断する最小時間（秒）。この時間以上無音が続くとシーン境界とみなされます。

## 音声認識設定

```python
"transcription": {
    "model_size": "large-v3",
    "language": "ja",
    "beam_size": 5
}
```

- **model_size**: Faster Whisperのモデルサイズ。"tiny", "base", "small", "medium", "large-v1", "large-v2", "large-v3"のいずれかを指定できます。
- **language**: 認識する言語のコード。"ja"は日本語を表します。
- **beam_size**: ビームサーチのサイズ。大きいほど精度が向上しますが、処理時間も増加します。

## 画像分析設定

```python
"analysis": {
    "frames_per_scene": 3,
    "context_window": 5  # シーン前後の文脈を考慮する数
}
```

- **frames_per_scene**: 各シーンから抽出するフレーム数。多いほど詳細な分析が可能ですが、処理時間も増加します。
- **context_window**: シーン分析時に前後のシーンをいくつ考慮するか。文脈を理解するために使用されます。

## UI設定

```python
"ui": {
    "thumbnail_size": (320, 180),
    "preview_duration": 5.0,
    "max_scenes_per_page": 10
}
```

- **thumbnail_size**: サムネイルのサイズ（幅, 高さ）。
- **preview_duration**: プレビュー再生の長さ（秒）。
- **max_scenes_per_page**: 1ページに表示する最大シーン数。

## Gemini API設定

```python
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

- **GEMINI_API_KEY**: Gemini APIのアクセスキー。実際の使用時には環境変数から取得するなど、安全な方法で管理することをお勧めします。

## 設定のカスタマイズ方法

設定をカスタマイズするには、`config.py`ファイルを直接編集するか、環境変数を使用して上書きする方法があります。

### 環境変数による設定の例

```python
import os

# 環境変数から設定を読み込む
CONFIG = {
    "models": {
        "default": os.environ.get("GEMINI_DEFAULT_MODEL", "gemini-2.0-flash"),
        "vision": os.environ.get("GEMINI_VISION_MODEL", "gemini-1.5-flash"),
        "description": os.environ.get("GEMINI_DESCRIPTION_MODEL", "gemini-1.5-pro"),
        "interactive": os.environ.get("GEMINI_INTERACTIVE_MODEL", "gemini-2.0-flash-live-001")
    },
    # その他の設定...
}

# APIキーを環境変数から取得
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
```

### 設定の動的な変更

アプリケーション実行中に設定を動的に変更するには、以下のようなユーティリティ関数を使用できます：

```python
def update_config(section, key, value):
    """
    設定を動的に更新する
    
    Args:
        section: 設定セクション名
        key: 設定キー
        value: 新しい値
    """
    if section in CONFIG and key in CONFIG[section]:
        CONFIG[section][key] = value
        return True
    return False
```

## 推奨設定

### 高品質優先設定

処理時間よりも品質を優先する場合の推奨設定：

```python
CONFIG = {
    "models": {
        "default": "gemini-2.0-pro",
        "vision": "gemini-1.5-pro",
        "description": "gemini-1.5-pro",
        "interactive": "gemini-2.0-pro-live-001"
    },
    "scene_detection": {
        "min_scene_length": 3.0,
        "silence_threshold": -35,
        "silence_duration": 0.8
    },
    "transcription": {
        "model_size": "large-v3",
        "language": "ja",
        "beam_size": 8
    },
    "analysis": {
        "frames_per_scene": 5,
        "context_window": 7
    }
}
```

### 速度優先設定

処理速度を優先する場合の推奨設定：

```python
CONFIG = {
    "models": {
        "default": "gemini-2.0-flash",
        "vision": "gemini-1.5-flash",
        "description": "gemini-1.5-flash",
        "interactive": "gemini-2.0-flash-live-001"
    },
    "scene_detection": {
        "min_scene_length": 8.0,
        "silence_threshold": -25,
        "silence_duration": 1.5
    },
    "transcription": {
        "model_size": "medium",
        "language": "ja",
        "beam_size": 3
    },
    "analysis": {
        "frames_per_scene": 2,
        "context_window": 3
    }
}
```
