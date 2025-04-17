"""
音声認識ツール - 動画の音声を分析して書き起こし
"""
import os
import tempfile
import subprocess
import json
import logging

def transcribe_audio(video_path, scenes=None):
    """
    動画の音声を書き起こします。
    
    Args:
        video_path: 動画ファイルのパス
        scenes: シーンのリスト。指定された場合、シーンごとに書き起こしを行う
        
    Returns:
        dict: 書き起こし結果
    """
    logging.info(f"動画 {video_path} の音声認識を開始します")
    
    try:
        if scenes is None:
            # シーンが指定されていない場合、動画全体を書き起こし
            return transcribe_whole_video(video_path)
        else:
            # シーンごとに書き起こし
            return transcribe_by_scenes(video_path, scenes)
    
    except Exception as e:
        logging.error(f"音声認識中にエラーが発生しました: {e}")
        return {"error": str(e)}

def transcribe_whole_video(video_path):
    """
    動画全体の音声を書き起こします。
    
    Args:
        video_path: 動画ファイルのパス
        
    Returns:
        dict: 書き起こし結果
    """
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
        temp_audio_path = temp_audio.name
    
    try:
        # 動画から音声を抽出
        extract_audio(video_path, temp_audio_path)
        
        # 音声認識を実行
        result = analyze_audio(temp_audio_path)
        
        return {"transcription": result}
    
    finally:
        # 一時ファイルを削除
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

def transcribe_by_scenes(video_path, scenes):
    """
    シーンごとに音声を書き起こします。
    
    Args:
        video_path: 動画ファイルのパス
        scenes: シーンのリスト
        
    Returns:
        dict: シーンごとの書き起こし結果
    """
    scene_transcriptions = []
    
    for scene in scenes:
        scene_id = scene["scene_id"]
        start_time = scene["start_time"]
        end_time = scene["end_time"]
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
            temp_audio_path = temp_audio.name
        
        try:
            # シーンの音声を抽出
            extract_audio_segment(video_path, temp_audio_path, start_time, end_time)
            
            # 音声認識を実行
            result = analyze_audio(temp_audio_path)
            
            scene_transcriptions.append({
                "scene_id": scene_id,
                "start_time": start_time,
                "end_time": end_time,
                "text": result
            })
        
        finally:
            # 一時ファイルを削除
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
    
    return {"scene_transcriptions": scene_transcriptions}

def extract_audio(video_path, output_path):
    """
    動画から音声を抽出します。
    
    Args:
        video_path: 動画ファイルのパス
        output_path: 出力する音声ファイルのパス
    """
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vn',  # 映像を無効化
        '-acodec', 'pcm_s16le',  # PCM 16ビットリニアオーディオ
        '-ar', '16000',  # サンプルレート 16kHz
        '-ac', '1',  # モノラル
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
        raise Exception(f"音声抽出に失敗しました: {stderr}")

def extract_audio_segment(video_path, output_path, start_time, end_time):
    """
    動画の指定された区間から音声を抽出します。
    
    Args:
        video_path: 動画ファイルのパス
        output_path: 出力する音声ファイルのパス
        start_time: 開始時間（秒）
        end_time: 終了時間（秒）
    """
    duration = end_time - start_time
    
    cmd = [
        'ffmpeg',
        '-ss', str(start_time),  # 開始時間
        '-i', video_path,
        '-t', str(duration),  # 継続時間
        '-vn',  # 映像を無効化
        '-acodec', 'pcm_s16le',  # PCM 16ビットリニアオーディオ
        '-ar', '16000',  # サンプルレート 16kHz
        '-ac', '1',  # モノラル
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
        raise Exception(f"音声セグメント抽出に失敗しました: {stderr}")

def analyze_audio(audio_path):
    """
    音声ファイルを分析し、テキストに変換します。
    シンプルな実装のため、ここではSpeech-to-Text APIを使わず、
    ダミーテキストを返します。実際の実装では外部APIを使用します。
    
    Args:
        audio_path: 音声ファイルのパス
        
    Returns:
        str: 認識されたテキスト
    """
    # 実際のアプリケーションでは、ここでWhisperなどのSTTモデルを使うか
    # Google Speech-to-Text APIなどの外部APIを使用します
    
    # ここでは音声の長さに応じてダミーテキストを生成
    file_size = os.path.getsize(audio_path)
    
    # 100KBごとに文を追加（ダミーロジック）
    num_sentences = max(1, file_size // 100000)
    
    dummy_texts = [
        "山の頂上に向かって登っています。景色が素晴らしいです。",
        "鳥のさえずりが聞こえます。自然の中にいる感じがします。",
        "ここから見える景色は最高です。頑張って登ってきた甲斐がありました。",
        "小さな小川を渡ります。水がとても冷たくて気持ちいいです。",
        "休憩を取って水分補給します。体力を回復させましょう。"
    ]
    
    result = ""
    for i in range(min(num_sentences, len(dummy_texts))):
        result += dummy_texts[i] + " "
    
    return result.strip()
