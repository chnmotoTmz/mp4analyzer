# Google ADKを活用した登山動画シーン説明ジェネレーター

## 概要

このプロジェクトは、Google Agent Development Kit (ADK)を活用した登山動画シーン説明ジェネレーターです。動画からシーンを検出し、音声認識と画像分析を行い、シーンの説明文と編集提案を生成します。マルチエージェントアーキテクチャを採用し、各機能を独立したエージェントとして実装することで、拡張性と再利用性を高めています。

## 機能

- シーン検出: FFmpegを使用して動画からシーンを自動検出
- 音声認識: Faster Whisperを使用して高精度な音声認識
- 画像分析: Gemini 1.5 Flashを使用して動画フレームを分析
- 説明文生成: 視覚情報と音声情報を組み合わせて自然な説明文を生成
- 編集提案: シーンの内容に基づいて編集のアドバイスを提供
- ストリーミング処理: リアルタイムで結果を返す機能
- 対話型プロパティ照会: 動画のプロパティに関する質問に答える機能

## インストール

### 前提条件

- Python 3.10以上
- FFmpeg
- インターネット接続（Gemini APIへのアクセス用）

### インストール手順

1. リポジトリをクローン:

```bash
git clone https://github.com/yourusername/mountain-video-analyzer.git
cd mountain-video-analyzer
```

2. 必要なライブラリをインストール:

```bash
pip install google-adk ffmpeg-python faster-whisper
```

3. Gemini APIキーの設定:

`mountain_video_analyzer/config/config.py`ファイル内の`GEMINI_API_KEY`変数に有効なAPIキーを設定するか、環境変数から安全に読み込むように変更してください。

```python
# 環境変数から読み込む例
import os
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
```

## 使用方法

### コマンドラインインターフェース

このプロジェクトは以下のコマンドラインインターフェースを提供しています:

#### Webサーバーの起動

```bash
python -m mountain_video_analyzer.main server --host 0.0.0.0 --port 8000
```

#### 動画の分析

```bash
python -m mountain_video_analyzer.main analyze /path/to/your/video.mp4 --output results.json
```

#### テストの実行

```bash
python -m mountain_video_analyzer.main test --video_path /path/to/test_video.mp4
```

### Webインターフェース

Webサーバーを起動した後、ブラウザで`http://localhost:8000`にアクセスすると、Webインターフェースを使用できます。

1. 「ファイルを選択」ボタンをクリックして動画ファイルをアップロード
2. 「分析開始」ボタンをクリックして分析を開始
3. 分析結果が表示されます

## アーキテクチャ

このプロジェクトはGoogle ADKのマルチエージェントアーキテクチャを採用しています:

### エージェント構成

- **シーン検出エージェント**: FFmpegを使用して動画からシーンを検出
- **音声認識エージェント**: Faster Whisperを使用して音声を文字起こし
- **画像分析エージェント**: Gemini 1.5 Flashを使用してフレームを分析
- **説明文生成エージェント**: 視覚情報と音声情報から説明文を生成
- **編集提案エージェント**: シーンの内容に基づいて編集提案を生成
- **メインオーケストレーションエージェント**: 上記のエージェントを統合

### 処理フロー

1. 動画ファイルがアップロードされる
2. シーン検出エージェントがシーンを検出
3. 音声認識エージェントと画像分析エージェントが並列で処理
4. 説明文生成エージェントが説明文を生成
5. 編集提案エージェントが編集提案を生成
6. 結果がユーザーに返される

## 拡張機能

### ストリーミング処理

リアルタイムで分析結果を返す機能を提供しています:

```python
from mountain_video_analyzer.utils.streaming_processor import StreamingProcessor

async def process_streaming(video_path):
    processor = StreamingProcessor()
    
    async def callback(data):
        print(data)
    
    await processor.start_streaming(video_path, callback)
```

### 対話型プロパティ照会システム

動画のプロパティに関する質問に答える機能を提供しています:

```python
from mountain_video_analyzer.utils.property_query_system import PropertyQuerySystem
from mountain_video_analyzer.utils.session_manager import SessionManager

# セッションマネージャーを初期化
session_manager = SessionManager()
session_manager.set_state("scenes", [...])  # 分析結果をセット

# 対話型プロパティ照会システムを初期化
query_system = PropertyQuerySystem(session_manager)

# 質問に回答
result = query_system.get_weather_conditions(scene_id=1)
print(result)
```

## カスタマイズ

### 設定ファイル

`mountain_video_analyzer/config/config.py`ファイルで各種設定を変更できます:

```python
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
    # その他の設定...
}
```

### エージェントのカスタマイズ

新しいエージェントを追加する場合は、`BaseAgent`クラスを継承して実装します:

```python
from mountain_video_analyzer.agents.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="my_custom_agent",
            model="gemini-2.0-flash",
            description="カスタムエージェントの説明",
            instruction="カスタムエージェントの指示",
            tools=[my_custom_tool]
        )
```

## トラブルシューティング

### よくある問題

1. **APIキーエラー**: Gemini APIキーが正しく設定されているか確認してください。
2. **FFmpegエラー**: FFmpegがインストールされているか確認してください。
3. **メモリエラー**: 大きな動画ファイルを処理する場合、十分なメモリが必要です。

### ログの確認

エラーが発生した場合は、`logs/mountain_video_analyzer.log`ファイルを確認してください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細はLICENSEファイルを参照してください。

## 謝辞

- Google Agent Development Kit (ADK)チーム
- FFmpeg開発者
- Faster Whisper開発者
- その他のオープンソースコミュニティ
