"""
対話型プロパティ照会システム - 動画のプロパティに関する質問に答えるシステム
"""
from ..agents.agent import Agent
from ..utils.function_tool import FunctionTool
from ..config import CONFIG, GEMINI_API_KEY
import google.generativeai as genai

class PropertyQuerySystem:
    """
    動画のプロパティに関する質問に答えるシステム
    """
    def __init__(self, session_manager=None):
        """
        PropertyQuerySystemの初期化
        
        Args:
            session_manager: セッションマネージャー
        """
        self.session_manager = session_manager
        
        # Geminiモデルを初期化
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=CONFIG["models"]["interactive"]
        )
        
        # 対話型プロパティ照会エージェントを作成
        self.agent = Agent(
            name="property_query_agent",
            model=CONFIG["models"]["interactive"],
            description="動画のプロパティに関する質問に答えるエージェント",
            instruction="""
            ユーザーからの質問に基づいて、動画の特定のプロパティを返します。
            セッション状態から動画分析結果を参照し、質問に最適な情報を提供してください。
            わからない場合は正直に認め、回答可能な質問の例を提案してください。
            """,
            tools=[
                FunctionTool(self.get_scene_by_time),
                FunctionTool(self.search_scenes_by_keyword),
                FunctionTool(self.get_emotional_tone),
                FunctionTool(self.get_weather_conditions)
            ]
        )
    
    def get_scene_by_time(self, time: float) -> dict:
        """
        指定された時間のシーン情報を取得
        
        Args:
            time: 動画内の時間（秒）
            
        Returns:
            dict: シーン情報
        """
        if not self.session_manager:
            return {"error": "セッションが初期化されていません"}
        
        scenes = self.session_manager.get_state("scenes", [])
        
        for scene in scenes:
            if scene["start_time"] <= time <= scene["end_time"]:
                return {"scene": scene}
        
        return {"error": f"時間 {time} 秒のシーンが見つかりません"}
    
    def search_scenes_by_keyword(self, keyword: str) -> dict:
        """
        キーワードに一致するシーンを検索
        
        Args:
            keyword: 検索キーワード
            
        Returns:
            dict: 一致するシーンのリスト
        """
        if not self.session_manager:
            return {"error": "セッションが初期化されていません"}
        
        scenes = self.session_manager.get_state("scenes", [])
        descriptions = self.session_manager.get_state("descriptions", [])
        
        matching_scenes = []
        
        for scene in scenes:
            scene_id = scene["scene_id"]
            
            # 対応する説明文を検索
            scene_description = None
            for desc in descriptions:
                if desc["scene_id"] == scene_id:
                    scene_description = desc["text"]
                    break
            
            # キーワードが説明文に含まれているか確認
            if scene_description and keyword.lower() in scene_description.lower():
                matching_scenes.append({
                    "scene_id": scene_id,
                    "start_time": scene["start_time"],
                    "end_time": scene["end_time"],
                    "description": scene_description
                })
        
        return {
            "matching_scenes": matching_scenes,
            "total_matches": len(matching_scenes)
        }
    
    def get_emotional_tone(self, scene_id: int) -> dict:
        """
        指定されたシーンの感情的なトーンを取得
        
        Args:
            scene_id: シーンID
            
        Returns:
            dict: 感情的なトーン情報
        """
        if not self.session_manager:
            return {"error": "セッションが初期化されていません"}
        
        scenes = self.session_manager.get_state("scenes", [])
        descriptions = self.session_manager.get_state("descriptions", [])
        
        # 対応するシーンを検索
        target_scene = None
        for scene in scenes:
            if scene["scene_id"] == scene_id:
                target_scene = scene
                break
        
        if not target_scene:
            return {"error": f"シーンID {scene_id} が見つかりません"}
        
        # 対応する説明文を検索
        scene_description = None
        for desc in descriptions:
            if desc["scene_id"] == scene_id:
                scene_description = desc["text"]
                break
        
        if not scene_description:
            return {"error": f"シーンID {scene_id} の説明文が見つかりません"}
        
        # Geminiモデルを使用して感情的なトーンを分析
        prompt = f"""
        以下の登山動画シーンの説明文から、感情的なトーンを分析してください。
        感情（興奮、平穏、緊張、喜び、驚きなど）と強度（1-5のスケール）を特定してください。
        
        説明文: {scene_description}
        
        JSON形式で回答してください。
        """
        
        response = self.model.generate_content(prompt)
        
        return {
            "scene_id": scene_id,
            "emotional_tone": response.text
        }
    
    def get_weather_conditions(self, scene_id: int) -> dict:
        """
        指定されたシーンの天候状況を取得
        
        Args:
            scene_id: シーンID
            
        Returns:
            dict: 天候状況情報
        """
        if not self.session_manager:
            return {"error": "セッションが初期化されていません"}
        
        scenes = self.session_manager.get_state("scenes", [])
        frame_analyses = self.session_manager.get_state("frame_analyses", [])
        
        # 対応するシーンを検索
        target_scene = None
        for scene in scenes:
            if scene["scene_id"] == scene_id:
                target_scene = scene
                break
        
        if not target_scene:
            return {"error": f"シーンID {scene_id} が見つかりません"}
        
        # 対応するフレーム分析を検索
        scene_analyses = []
        for analysis in frame_analyses:
            if target_scene["start_time"] <= analysis["timestamp"] <= target_scene["end_time"]:
                scene_analyses.append(analysis["analysis"])
        
        if not scene_analyses:
            return {"error": f"シーンID {scene_id} のフレーム分析が見つかりません"}
        
        # Geminiモデルを使用して天候状況を抽出
        prompt = f"""
        以下の登山動画シーンのフレーム分析から、天候状況に関する情報を抽出してください。
        天候（晴れ、曇り、雨、雪など）、気温（推定）、視界（良好、普通、不良）などを特定してください。
        
        フレーム分析:
        {' '.join(scene_analyses)}
        
        JSON形式で回答してください。
        """
        
        response = self.model.generate_content(prompt)
        
        return {
            "scene_id": scene_id,
            "weather_conditions": response.text
        }
    
    def get_agent(self):
        """
        エージェントを返す
        """
        return self.agent
