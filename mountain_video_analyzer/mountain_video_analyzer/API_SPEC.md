# API仕様書

## エージェントAPI

### BaseAgent

基本エージェントクラス - すべてのエージェントの基底クラス

```python
class BaseAgent:
    def __init__(self, name, description, instruction, model=None, tools=None):
        """
        BaseAgentの初期化

        Args:
            name: エージェント名
            description: エージェントの説明
            instruction: エージェントの指示
            model: 使用するモデル名（Noneの場合はデフォルトモデルを使用）
            tools: エージェントが使用するツールのリスト
        """
        
    def get_agent(self):
        """
        Google ADK Agentインスタンスを返す
        
        Returns:
            Agent: Google ADK Agentインスタンス
        """
```

### SceneDetectionAgent

シーン検出エージェント - 動画からシーンを検出するエージェント

```python
class SceneDetectionAgent(BaseAgent):
    def __init__(self):
        """
        SceneDetectionAgentの初期化
        FFmpegを使用して動画からシーンを検出するエージェントを作成
        """
```

### TranscriptionAgent

音声認識エージェント - 動画内の音声を文字起こしするエージェント

```python
class TranscriptionAgent(BaseAgent):
    def __init__(self):
        """
        TranscriptionAgentの初期化
        Faster Whisperを使用して高精度な音声認識を行うエージェントを作成
        """
```

### VisionAnalysisAgent

画像分析エージェント - シーンの視覚情報を分析するエージェント

```python
class VisionAnalysisAgent(BaseAgent):
    def __init__(self):
        """
        VisionAnalysisAgentの初期化
        Gemini 1.5 Flashを使用してシーンの視覚情報を分析するエージェントを作成
        """
```

### DescriptionAgent

説明文生成エージェント - シーンの説明文を生成するエージェント

```python
class DescriptionAgent(BaseAgent):
    def __init__(self):
        """
        DescriptionAgentの初期化
        Gemini 1.5 Proを使用してシーンの説明文を生成するエージェントを作成
        """
```

### EditingSuggestionAgent

編集提案エージェント - 編集提案を行うエージェント

```python
class EditingSuggestionAgent(BaseAgent):
    def __init__(self):
        """
        EditingSuggestionAgentの初期化
        Gemini 1.5 Proを使用して編集提案を行うエージェントを作成
        """
```

### MountainVideoAnalyzerAgent

メインオーケストレーションエージェント - 登山動画を包括的に分析するメインエージェント

```python
class MountainVideoAnalyzerAgent:
    def __init__(self):
        """
        MountainVideoAnalyzerAgentの初期化
        各エージェントのインスタンスを作成し、メインのオーケストレーションエージェントを構築
        """
        
    def get_agent(self):
        """
        メインエージェントを返す
        
        Returns:
            SequentialAgent: メインのオーケストレーションエージェント
        """
```

## ツールAPI

### detect_scenes

FFmpegを使用したシーン検出ツール

```python
def detect_scenes(video_path: str, min_scene_length: float = None) -> dict:
    """
    FFmpegを使用して動画からシーンを検出します。
    
    Args:
        video_path: 分析する動画のパス
        min_scene_length: 最小シーン長（秒）。Noneの場合はCONFIGから取得
        
    Returns:
        dict: 検出されたシーンのリスト（開始時間、終了時間を含む）
    """
```

### transcribe_audio

Faster Whisperを使用した音声認識ツール

```python
def transcribe_audio(audio_path: str, language: str = None) -> dict:
    """
    Faster Whisperを使用して音声を文字起こしします。
    
    Args:
        audio_path: 音声ファイルのパス
        language: 言語コード（デフォルトはCONFIGから取得）
        
    Returns:
        dict: 文字起こし結果
    """
```

### analyze_frames

Gemini 1.5 Flashを使用した画像分析ツール

```python
def analyze_frames(video_path: str, timestamps: list) -> dict:
    """
    指定されたタイムスタンプの動画フレームを分析します。
    
    Args:
        video_path: 動画ファイルのパス
        timestamps: 分析するタイムスタンプのリスト
        
    Returns:
        dict: フレーム分析結果
    """
```

## セッション管理API

### SessionManager

セッション状態を管理するクラス

```python
class SessionManager:
    def __init__(self, session_id=None):
        """
        SessionManagerの初期化
        
        Args:
            session_id: セッションID（Noneの場合は自動生成）
        """
        
    def set_state(self, key, value):
        """
        セッション状態に値を設定
        
        Args:
            key: 状態のキー
            value: 状態の値
        """
        
    def get_state(self, key, default=None):
        """
        セッション状態から値を取得
        
        Args:
            key: 状態のキー
            default: キーが存在しない場合のデフォルト値
            
        Returns:
            取得した値またはデフォルト値
        """
        
    def get_session(self):
        """
        セッションオブジェクトを返す
        
        Returns:
            Session: Sessionオブジェクト
        """
```

### process_video

動画を処理し、シーン説明と編集提案を生成する関数

```python
async def process_video(main_agent, video_path):
    """
    動画を処理し、シーン説明と編集提案を生成する
    
    Args:
        main_agent: メインエージェント
        video_path: 動画ファイルのパス
        
    Returns:
        dict: 処理結果
    """
```

### process_video_streaming

動画をストリーミング処理し、結果をリアルタイムでコールバック関数に渡す関数

```python
async def process_video_streaming(main_agent, video_path, callback):
    """
    動画をストリーミング処理し、結果をリアルタイムでコールバック関数に渡す
    
    Args:
        main_agent: メインエージェント
        video_path: 動画ファイルのパス
        callback: コールバック関数
    """
```

## ストリーミング処理API

### StreamingProcessor

動画のストリーミング処理を行うクラス

```python
class StreamingProcessor:
    def __init__(self, main_agent=None):
        """
        StreamingProcessorの初期化
        
        Args:
            main_agent: メインエージェント（Noneの場合は新しく作成）
        """
        
    async def start_streaming(self, video_path, callback):
        """
        ストリーミング処理を開始
        
        Args:
            video_path: 動画ファイルのパス
            callback: 結果を受け取るコールバック関数
        """
        
    def stop_streaming(self):
        """
        ストリーミング処理を停止
        """
        
    async def get_final_result(self):
        """
        最終結果を取得
        
        Returns:
            dict: 処理結果
        """
```

## 対話型プロパティ照会API

### PropertyQuerySystem

動画のプロパティに関する質問に答えるシステム

```python
class PropertyQuerySystem:
    def __init__(self, session_manager=None):
        """
        PropertyQuerySystemの初期化
        
        Args:
            session_manager: セッションマネージャー
        """
        
    def get_scene_by_time(self, time: float) -> dict:
        """
        指定された時間のシーン情報を取得
        
        Args:
            time: 動画内の時間（秒）
            
        Returns:
            dict: シーン情報
        """
        
    def search_scenes_by_keyword(self, keyword: str) -> dict:
        """
        キーワードに一致するシーンを検索
        
        Args:
            keyword: 検索キーワード
            
        Returns:
            dict: 一致するシーンのリスト
        """
        
    def get_emotional_tone(self, scene_id: int) -> dict:
        """
        指定されたシーンの感情的なトーンを取得
        
        Args:
            scene_id: シーンID
            
        Returns:
            dict: 感情的なトーン情報
        """
        
    def get_weather_conditions(self, scene_id: int) -> dict:
        """
        指定されたシーンの天候状況を取得
        
        Args:
            scene_id: シーンID
            
        Returns:
            dict: 天候状況情報
        """
        
    def get_agent(self):
        """
        エージェントを返す
        
        Returns:
            Agent: 対話型プロパティ照会エージェント
        """
```

## ユーティリティAPI

### ErrorHandler

エラーハンドリングユーティリティ

```python
class ErrorHandler:
    @staticmethod
    def handle_error(error, error_type=None, message=None):
        """
        エラーを処理し、適切なレスポンスを返す
        
        Args:
            error: 発生したエラー
            error_type: エラータイプ（オプション）
            message: カスタムメッセージ（オプション）
            
        Returns:
            dict: エラー情報を含む辞書
        """
        
    @staticmethod
    def check_file_exists(file_path):
        """
        ファイルが存在するか確認
        
        Args:
            file_path: 確認するファイルパス
            
        Returns:
            bool: ファイルが存在する場合はTrue
            
        Raises:
            FileNotFoundError: ファイルが存在しない場合
        """
        
    @staticmethod
    def check_file_extension(file_path, allowed_extensions):
        """
        ファイル拡張子が許可されているか確認
        
        Args:
            file_path: 確認するファイルパス
            allowed_extensions: 許可される拡張子のリスト
            
        Returns:
            bool: 拡張子が許可されている場合はTrue
            
        Raises:
            ValueError: 拡張子が許可されていない場合
        """
```

### PerformanceOptimizer

パフォーマンス最適化のためのユーティリティクラス

```python
class PerformanceOptimizer:
    @staticmethod
    def measure_execution_time(func):
        """
        関数の実行時間を測定するデコレータ
        """
        
    @staticmethod
    def async_measure_execution_time(func):
        """
        非同期関数の実行時間を測定するデコレータ
        """
        
    @staticmethod
    def run_in_thread_pool(func, *args, **kwargs):
        """
        関数をスレッドプールで実行
        
        Args:
            func: 実行する関数
            *args: 関数の引数
            **kwargs: 関数のキーワード引数
            
        Returns:
            関数の戻り値
        """
        
    @staticmethod
    async def run_in_process_pool(func, *args, **kwargs):
        """
        関数をプロセスプールで実行（CPU負荷の高い処理向け）
        
        Args:
            func: 実行する関数
            *args: 関数の引数
            **kwargs: 関数のキーワード引数
            
        Returns:
            関数の戻り値
        """
        
    @staticmethod
    def cache_result(func):
        """
        関数の結果をキャッシュするデコレータ
        """
        
    @staticmethod
    def batch_process(items, batch_size, process_func):
        """
        アイテムをバッチ処理する
        
        Args:
            items: 処理するアイテムのリスト
            batch_size: バッチサイズ
            process_func: 各バッチを処理する関数
            
        Returns:
            処理結果のリスト
        """
        
    @staticmethod
    async def async_batch_process(items, batch_size, process_func):
        """
        アイテムを非同期バッチ処理する
        
        Args:
            items: 処理するアイテムのリスト
            batch_size: バッチサイズ
            process_func: 各バッチを処理する非同期関数
            
        Returns:
            処理結果のリスト
        """
```

## Webアプリケーション API

### create_web_app

ADK Webアプリケーションを作成する関数

```python
def create_web_app():
    """
    ADK Webアプリケーションを作成
    
    Returns:
        FastAPI: Webアプリケーションインスタンス
    """
```

### start_server

サーバーを起動する関数

```python
def start_server(host="0.0.0.0", port=8000):
    """
    サーバーを起動
    
    Args:
        host: ホスト名
        port: ポート番号
    """
```

## メインエントリーポイント

### main

メインエントリーポイント

```python
def main():
    """
    メインエントリーポイント
    コマンドライン引数を解析し、適切な処理を実行
    """
```
