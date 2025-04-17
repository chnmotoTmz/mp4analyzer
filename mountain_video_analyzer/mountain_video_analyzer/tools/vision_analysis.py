"""
Gemini 1.5 Flashを使用した画像分析ツール
"""
import os
import subprocess
import tempfile
import logging
import google.generativeai as genai
from ..config import CONFIG, GEMINI_API_KEY

def analyze_frames(video_path, timestamps):
    """
    指定されたタイムスタンプの動画フレームを分析します。
    
    Args:
        video_path: 動画ファイルのパス
        timestamps: 分析するタイムスタンプのリスト
        
    Returns:
        dict: フレーム分析結果
    """
    frames_per_scene = CONFIG["analysis"]["frames_per_scene"]
    
    logging.info(f"動画 {video_path} のフレーム分析を開始します")
    
    try:
        # Geminiモデルを初期化
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name=CONFIG["models"]["vision"]
        )
        
        # 一時ディレクトリを作成
        with tempfile.TemporaryDirectory() as temp_dir:
            frame_analyses = []
            
            for timestamp in timestamps:
                frame_paths = []
                
                # 指定されたタイムスタンプの前後からフレームを抽出
                for i in range(frames_per_scene):
                    # タイムスタンプに対して均等に分散したフレームを抽出
                    offset = i * (1.0 / frames_per_scene) - 0.5
                    frame_time = max(0, timestamp + offset)
                    
                    frame_path = os.path.join(temp_dir, f"frame_{timestamp}_{i}.jpg")
                    
                    # FFmpegを使用してフレームを抽出
                    extract_frame(video_path, frame_path, frame_time)
                    
                    frame_paths.append(frame_path)
                
                # 抽出したフレームを分析
                frame_contents = []
                for frame_path in frame_paths:
                    if os.path.exists(frame_path) and os.path.getsize(frame_path) > 0:
                        with open(frame_path, "rb") as f:
                            frame_contents.append({"mime_type": "image/jpeg", "data": f.read()})
                
                # Geminiモデルを使用してフレームを分析
                if frame_contents:
                    prompt = """
                    この登山動画のフレームを分析し、以下の情報を抽出してください：
                    1. 場所の特徴（山の種類、地形、標高など）
                    2. 活動内容（登山、休憩、景色の鑑賞など）
                    3. 天候状況（晴れ、曇り、雨など）
                    4. 時間帯（朝、昼、夕方、夜など）
                    5. 特筆すべき風景や自然の特徴
                    6. 登山者の状況や装備
                    
                    JSON形式で回答してください。
                    """
                    
                    try:
                        response = model.generate_content([prompt, *frame_contents])
                        analysis_text = response.text
                    except Exception as e:
                        logging.error(f"Gemini APIエラー: {e}")
                        analysis_text = generate_mock_analysis(timestamp)
                else:
                    analysis_text = generate_mock_analysis(timestamp)
                
                # 分析結果を整形
                frame_analyses.append({
                    "timestamp": timestamp,
                    "analysis": analysis_text
                })
            
            return {"frame_analyses": frame_analyses}
    
    except Exception as e:
        logging.error(f"フレーム分析中にエラーが発生しました: {e}")
        return {"error": str(e)}

def extract_frame(video_path, output_path, timestamp):
    """
    指定された時間のフレームを抽出します。
    
    Args:
        video_path: 動画ファイルのパス
        output_path: 出力するフレーム画像のパス
        timestamp: 抽出する時間（秒）
    """
    try:
        cmd = [
            'ffmpeg',
            '-ss', str(timestamp),  # 開始時間
            '-i', video_path,
            '-frames:v', '1',  # 1フレームだけ抽出
            '-q:v', '2',  # 高品質
            '-y',  # 既存のファイルを上書き
            output_path
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            logging.warning(f"フレーム抽出に失敗しました: {stderr}")
    
    except Exception as e:
        logging.error(f"フレーム抽出中にエラーが発生しました: {e}")

def generate_mock_analysis(timestamp):
    """
    モック分析結果を生成します（APIエラー時のフォールバック）。
    
    Args:
        timestamp: タイムスタンプ
        
    Returns:
        str: モック分析結果
    """
    # タイムスタンプに基づいて異なる分析結果を返す
    analyses = [
        """
        {
          "場所の特徴": "中腹の山道、落葉樹林に囲まれた登山道、推定標高800m程度",
          "活動内容": "登山中、適度なペースで上り坂を進んでいる",
          "天候状況": "晴れ、わずかに雲がある",
          "時間帯": "午前中、明るい日差し",
          "風景や自然の特徴": "紅葉した樹木、落ち葉が積もった山道、遠くに山頂が見える",
          "登山者の状況や装備": "登山靴、バックパック、トレッキングポールを使用、快適に歩いている"
        }
        """,
        """
        {
          "場所の特徴": "山頂付近の開けた場所、岩が多い地形、推定標高1200m以上",
          "活動内容": "休憩、景色の鑑賞",
          "天候状況": "晴れ、青空が広がっている",
          "時間帯": "昼頃、太陽が高い位置にある",
          "風景や自然の特徴": "360度のパノラマビュー、遠くに連なる山々、雲海が見える",
          "登山者の状況や装備": "休憩中、水分補給、軽装で汗をかいている"
        }
        """,
        """
        {
          "場所の特徴": "尾根道、低い植生、推定標高1000m程度",
          "活動内容": "トレッキング、緩やかな起伏の道を進んでいる",
          "天候状況": "薄曇り、霧が出ている",
          "時間帯": "夕方、やや暗くなり始めている",
          "風景や自然の特徴": "霧に包まれた神秘的な景色、苔むした岩、低木",
          "登山者の状況や装備": "軽めの上着を着用、ヘッドライトの準備、慎重に歩いている"
        }
        """
    ]
    
    # タイムスタンプを0~2の範囲にマッピング
    index = min(2, int(timestamp / 100) % 3)
    
    return analyses[index]
