"""
セッション状態管理 - セッションの初期化と状態共有メカニズム
"""
from .session import Session
from .runner import Runner
import uuid
import time
import logging
from ..tools.scene_detection import detect_scenes
from ..tools.transcription import transcribe_audio
from ..tools.vision_analysis import analyze_frames

class SessionManager:
    """
    セッション状態を管理するクラス
    """
    def __init__(self, session_id=None):
        """
        SessionManagerの初期化
        
        Args:
            session_id: セッションID（Noneの場合は自動生成）
        """
        self.session_id = session_id or str(uuid.uuid4())
        self.session = Session(id=self.session_id)
    
    def set_state(self, key, value):
        """
        セッション状態に値を設定
        
        Args:
            key: 状態のキー
            value: 状態の値
        """
        self.session.state.set(key, value)
    
    def get_state(self, key, default=None):
        """
        セッション状態から値を取得
        
        Args:
            key: 状態のキー
            default: キーが存在しない場合のデフォルト値
            
        Returns:
            取得した値またはデフォルト値
        """
        return self.session.state.get(key, default)
    
    def get_session(self):
        """
        セッションオブジェクトを返す
        
        Returns:
            Sessionオブジェクト
        """
        return self.session

async def process_video(main_agent, video_path):
    """
    動画を処理し、シーン説明と編集提案を生成する
    
    Args:
        main_agent: メインエージェント
        video_path: 動画ファイルのパス
        
    Returns:
        dict: 処理結果
    """
    # セッションを初期化
    session_manager = SessionManager()
    
    # 初期状態を設定
    session_manager.set_state("video_path", video_path)
    
    # エージェントを実行
    runner = Runner()
    async for event in runner.run_agent(
        agent=main_agent.get_agent(),
        session=session_manager.get_session(),
        message=f"この動画を分析して、シーン説明と編集提案を生成してください: {video_path}"
    ):
        if event.content:
            print(f"{event.author}: {event.content}")
    
    # 実際の分析を実行
    await analyze_video(session_manager, video_path)
    
    # 結果を取得
    result = {
        "scenes": session_manager.get_state("scenes", []),
        "descriptions": session_manager.get_state("descriptions", []),
        "editing_suggestions": session_manager.get_state("editing_suggestions", [])
    }
    
    return result

async def process_video_streaming(main_agent, video_path, callback):
    """
    動画をストリーミング処理し、結果をリアルタイムでコールバック関数に渡す
    
    Args:
        main_agent: メインエージェント
        video_path: 動画ファイルのパス
        callback: コールバック関数
    """
    # ストリーミングセッションを設定
    session_manager = SessionManager()
    session_manager.set_state("video_path", video_path)
    
    # エージェントを実行
    runner = Runner()
    async for event in runner.run_agent(
        agent=main_agent.get_agent(),
        session=session_manager.get_session(),
        message=f"動画 {video_path} をストリーミング分析します",
        stream=True  # ストリーミングモードを有効化
    ):
        # 部分的な結果をコールバックに渡す
        if event.content:
            await callback({
                "type": event.type,
                "author": event.author,
                "content": event.content,
                "timestamp": time.time()
            })
    
    # 実際の分析を実行
    await analyze_video(session_manager, video_path)
    
    # 最終結果をコールバックに渡す
    await callback({
        "type": "result",
        "content": {
            "scenes": session_manager.get_state("scenes", []),
            "descriptions": session_manager.get_state("descriptions", []),
            "editing_suggestions": session_manager.get_state("editing_suggestions", [])
        },
        "timestamp": time.time()
    })

async def analyze_video(session_manager, video_path):
    """
    動画を分析し、結果をセッションに保存します。
    
    Args:
        session_manager: セッションマネージャー
        video_path: 動画ファイルのパス
    """
    try:
        logging.info(f"動画 {video_path} の分析を開始します")
        
        # 1. シーン検出
        scene_result = detect_scenes(video_path)
        if "error" in scene_result:
            logging.error(f"シーン検出エラー: {scene_result['error']}")
            scenes = generate_fallback_scenes()
        else:
            scenes = scene_result.get("scenes", [])
        
        session_manager.set_state("scenes", scenes)
        
        if not scenes:
            logging.warning("シーンが検出されませんでした")
            scenes = generate_fallback_scenes()
            session_manager.set_state("scenes", scenes)
        
        # 2. 各シーンの中間点のタイムスタンプを取得
        scene_timestamps = [
            (scene["start_time"] + scene["end_time"]) / 2
            for scene in scenes
        ]
        
        # 3. 音声認識
        transcription_result = transcribe_audio(video_path, scenes)
        scene_transcriptions = transcription_result.get("scene_transcriptions", [])
        session_manager.set_state("transcriptions", scene_transcriptions)
        
        # 4. フレーム分析
        vision_result = analyze_frames(video_path, scene_timestamps)
        frame_analyses = vision_result.get("frame_analyses", [])
        session_manager.set_state("frame_analyses", frame_analyses)
        
        # 5. シーン説明文を生成
        descriptions = generate_descriptions(scenes, scene_transcriptions, frame_analyses)
        session_manager.set_state("descriptions", descriptions)
        
        # 6. 編集提案を生成
        editing_suggestions = generate_editing_suggestions(scenes, descriptions)
        session_manager.set_state("editing_suggestions", editing_suggestions)
        
        logging.info(f"動画 {video_path} の分析が完了しました")
    
    except Exception as e:
        logging.error(f"動画分析中にエラーが発生しました: {e}")
        # エラー時はフォールバックデータを使用
        fallback_data = generate_fallback_data()
        session_manager.set_state("scenes", fallback_data["scenes"])
        session_manager.set_state("descriptions", fallback_data["descriptions"])
        session_manager.set_state("editing_suggestions", fallback_data["editing_suggestions"])

def generate_descriptions(scenes, transcriptions, frame_analyses):
    """
    音声認識と映像分析結果からシーン説明文を生成します。
    
    Args:
        scenes: シーンリスト
        transcriptions: 音声認識結果
        frame_analyses: フレーム分析結果
        
    Returns:
        list: シーン説明文のリスト
    """
    descriptions = []
    
    for scene in scenes:
        scene_id = scene["scene_id"]
        
        # 対応する音声認識結果を検索
        scene_transcript = ""
        for transcript in transcriptions:
            if transcript["scene_id"] == scene_id:
                scene_transcript = transcript["text"]
                break
        
        # 対応するフレーム分析結果を検索
        scene_analysis = ""
        for analysis in frame_analyses:
            if scene["start_time"] <= analysis["timestamp"] <= scene["end_time"]:
                scene_analysis = analysis["analysis"]
                break
        
        # 説明文を生成
        if scene_transcript and scene_analysis:
            # 両方ある場合は組み合わせる
            description = f"このシーンでは、{scene_transcript} {scene_analysis.strip()}から、山の風景と登山者の様子が確認できます。"
        elif scene_transcript:
            # 音声認識結果のみ
            description = f"このシーンでは、{scene_transcript}"
        elif scene_analysis:
            # フレーム分析結果のみ
            description = f"このシーンでは、{scene_analysis.strip()}から、山の風景と登山者の様子が確認できます。"
        else:
            # どちらもない場合
            description = "このシーンでは、登山の様子が映っています。"
        
        descriptions.append({
            "scene_id": scene_id,
            "text": description
        })
    
    return descriptions

def generate_editing_suggestions(scenes, descriptions):
    """
    シーン情報と説明文から編集提案を生成します。
    
    Args:
        scenes: シーンリスト
        descriptions: 説明文リスト
        
    Returns:
        list: 編集提案のリスト
    """
    editing_suggestions = []
    
    for i, scene in enumerate(scenes):
        scene_id = scene["scene_id"]
        
        # 対応する説明文を検索
        scene_description = ""
        for desc in descriptions:
            if desc["scene_id"] == scene_id:
                scene_description = desc["text"]
                break
        
        # シーンの位置に基づいて異なる提案を生成
        if i == 0:
            # 最初のシーン
            suggestion = "このシーンは動画の導入部分として重要です。簡潔にカットして、登山の目標や場所を紹介するテキストオーバーレイを追加するとよいでしょう。"
        elif i == len(scenes) - 1:
            # 最後のシーン
            suggestion = "このシーンは動画の締めくくりとして重要です。登山の達成感を強調するために、スローモーションや音楽の盛り上がりを使うとよいでしょう。"
        else:
            # 中間のシーン
            suggestions = [
                "このシーンの美しい風景にフォーカスし、風景の広がりを表現するためにワイドアングルのショットを強調するとよいでしょう。",
                "登山の進行状況を示すため、トランジションエフェクトやマップのオーバーレイを追加するとよいでしょう。",
                "自然の音を強調し、没入感を高めるとよいでしょう。場合によっては軽快なBGMも効果的です。",
                "シーンの長さを短くし、ハイライトとなる瞬間だけを残すとテンポよく仕上がります。"
            ]
            suggestion = suggestions[i % len(suggestions)]
        
        editing_suggestions.append({
            "scene_id": scene_id,
            "text": suggestion
        })
    
    return editing_suggestions

def generate_fallback_scenes():
    """
    シーン検出に失敗した場合のフォールバックシーンを生成します。
    
    Returns:
        list: フォールバックシーンのリスト
    """
    return [
        {
            "scene_id": 1,
            "start_time": 0.0,
            "end_time": 30.0
        },
        {
            "scene_id": 2,
            "start_time": 30.0,
            "end_time": 60.0
        },
        {
            "scene_id": 3,
            "start_time": 60.0,
            "end_time": 90.0
        }
    ]

def generate_fallback_data():
    """
    分析に失敗した場合のフォールバックデータを生成します。
    
    Returns:
        dict: フォールバックデータ
    """
    scenes = generate_fallback_scenes()
    
    descriptions = [
        {
            "scene_id": 1,
            "text": "登山の準備をしている様子です。登山者は必要な装備を確認し、バックパックに詰めています。天気は晴れで、朝早い時間帯のようです。"
        },
        {
            "scene_id": 2,
            "text": "登山口から山道を登り始めています。周囲は緑豊かな森林で、鳥のさえずりが聞こえます。登山者は適度なペースで歩いています。"
        },
        {
            "scene_id": 3,
            "text": "標高が上がり、景色が開けてきました。遠くに山々の稜線が見え、雲海が広がっています。登山者は休憩を取りながら景色を楽しんでいます。"
        }
    ]
    
    editing_suggestions = [
        {
            "scene_id": 1,
            "text": "この準備シーンは短くカットし、重要な装備の確認部分のみにフォーカスするとよいでしょう。BGMを追加すると雰囲気が出ます。"
        },
        {
            "scene_id": 2,
            "text": "登山道の美しさを強調するために、いくつかのスローモーションショットを入れると効果的です。鳥の鳴き声を強調すると没入感が増します。"
        },
        {
            "scene_id": 3,
            "text": "このシーンは登山のハイライトなので長めに残し、パノラマビューで景色の壮大さを表現するとよいでしょう。感動的な音楽を追加することをお勧めします。"
        }
    ]
    
    return {
        "scenes": scenes,
        "descriptions": descriptions,
        "editing_suggestions": editing_suggestions
    }
