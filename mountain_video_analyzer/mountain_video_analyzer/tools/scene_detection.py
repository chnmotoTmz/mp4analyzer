"""
FFmpegを使用したシーン検出ツール
"""
import os
import subprocess
import json
import tempfile
import logging

def detect_scenes(video_path, min_scene_length=5.0):
    """
    FFmpegを使用して動画からシーンを検出します。
    
    Args:
        video_path: 分析する動画のパス
        min_scene_length: 最小シーン長（秒）
        
    Returns:
        dict: 検出されたシーンのリスト（開始時間、終了時間を含む）
    """
    # ログ出力
    logging.info(f"動画 {video_path} のシーン検出を開始します")
    
    try:
        # 一時ファイルの作成
        fd, temp_file = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        
        # FFmpegを使用してシーン検出を実行
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-filter:v', f'select=\'gt(scene,0.3)\',showinfo',
            '-f', 'null',
            '-'
        ]
        
        # コマンド実行と出力キャプチャ
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        stdout, stderr = process.communicate()
        
        # 'showinfo'フィルターの出力からシーン変更点を抽出
        scene_changes = []
        for line in stderr.split('\n'):
            if 'pts_time' in line:
                try:
                    time_str = line.split('pts_time:')[1].split(' ')[0]
                    time = float(time_str)
                    scene_changes.append(time)
                except (IndexError, ValueError) as e:
                    logging.warning(f"時間の解析に失敗しました: {e}")
        
        # シーンの開始時間と終了時間のペアを作成
        scenes = []
        video_duration = get_video_duration(video_path)
        
        if not scene_changes:
            # シーン変更点がない場合は動画全体を1つのシーンとして扱う
            scenes.append({
                "scene_id": 1,
                "start_time": 0.0,
                "end_time": video_duration
            })
        else:
            # シーン変更点を基にシーンを構築
            scene_changes.insert(0, 0.0)  # 最初のシーンの開始時間
            
            for i in range(len(scene_changes)):
                if i < len(scene_changes) - 1:
                    start_time = scene_changes[i]
                    end_time = scene_changes[i + 1]
                    
                    # 最小シーン長より長いシーンのみ含める
                    if end_time - start_time >= min_scene_length:
                        scenes.append({
                            "scene_id": i + 1,
                            "start_time": start_time,
                            "end_time": end_time
                        })
                else:
                    # 最後のシーン
                    start_time = scene_changes[i]
                    end_time = video_duration
                    
                    if end_time - start_time >= min_scene_length:
                        scenes.append({
                            "scene_id": i + 1,
                            "start_time": start_time,
                            "end_time": end_time
                        })
        
        return {"scenes": scenes}
        
    except Exception as e:
        logging.error(f"シーン検出中にエラーが発生しました: {e}")
        return {"error": str(e)}
    finally:
        # 一時ファイルを削除
        if 'temp_file' in locals():
            if os.path.exists(temp_file):
                os.remove(temp_file)

def get_video_duration(video_path):
    """
    動画の長さを取得します。
    
    Args:
        video_path: 動画ファイルのパス
        
    Returns:
        float: 動画の長さ（秒）
    """
    cmd = [
        'ffprobe', 
        '-v', 'error', 
        '-show_entries', 'format=duration', 
        '-of', 'json', 
        video_path
    ]
    
    process = subprocess.Popen(
        cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    
    stdout, stderr = process.communicate()
    
    if stderr:
        logging.warning(f"動画の長さ取得中に警告: {stderr}")
    
    try:
        data = json.loads(stdout)
        return float(data['format']['duration'])
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        logging.error(f"動画の長さの解析に失敗しました: {e}")
        return 0.0
