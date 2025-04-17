"""
テストコード - 実装したコンポーネントのテスト
"""
import asyncio
import os
from ..agents.main_agent import MountainVideoAnalyzerAgent
from ..utils.session_manager import process_video
from ..tools.scene_detection import detect_scenes
from ..tools.transcription import transcribe_audio
from ..tools.vision_analysis import analyze_frames

async def test_scene_detection(video_path):
    """
    シーン検出ツールのテスト
    
    Args:
        video_path: テスト用動画ファイルのパス
    """
    print("=== シーン検出ツールのテスト ===")
    result = detect_scenes(video_path)
    
    if "error" in result:
        print(f"エラー: {result['error']}")
        return False
    
    print(f"検出されたシーン数: {result['total_scenes']}")
    for i, scene in enumerate(result['scenes'][:3]):  # 最初の3シーンのみ表示
        print(f"シーン {scene['scene_id']}: {scene['start_time']:.2f}秒 - {scene['end_time']:.2f}秒 (長さ: {scene['duration']:.2f}秒)")
    
    if len(result['scenes']) > 3:
        print(f"... 他 {len(result['scenes']) - 3} シーン")
    
    return True

async def test_transcription(audio_path):
    """
    音声認識ツールのテスト
    
    Args:
        audio_path: テスト用音声ファイルのパス
    """
    print("\n=== 音声認識ツールのテスト ===")
    result = transcribe_audio(audio_path)
    
    if "error" in result:
        print(f"エラー: {result['error']}")
        return False
    
    print(f"言語: {result['language']} (確信度: {result['language_probability']:.2f})")
    print(f"文字起こし: {result['transcript'][:100]}...")  # 最初の100文字のみ表示
    print(f"セグメント数: {len(result['segments'])}")
    
    return True

async def test_vision_analysis(video_path, timestamps):
    """
    画像分析ツールのテスト
    
    Args:
        video_path: テスト用動画ファイルのパス
        timestamps: 分析するタイムスタンプのリスト
    """
    print("\n=== 画像分析ツールのテスト ===")
    result = analyze_frames(video_path, timestamps)
    
    if "error" in result:
        print(f"エラー: {result['error']}")
        return False
    
    print(f"分析されたフレーム数: {len(result['frame_analyses'])}")
    for i, analysis in enumerate(result['frame_analyses']):
        print(f"タイムスタンプ {analysis['timestamp']}秒の分析結果:")
        print(f"{analysis['analysis'][:100]}...")  # 最初の100文字のみ表示
    
    return True

async def test_full_pipeline(video_path):
    """
    完全なパイプラインのテスト
    
    Args:
        video_path: テスト用動画ファイルのパス
    """
    print("\n=== 完全なパイプラインのテスト ===")
    
    # メインエージェントを作成
    main_agent = MountainVideoAnalyzerAgent()
    
    # 動画を処理
    result = await process_video(main_agent, video_path)
    
    print(f"シーン数: {len(result['scenes'])}")
    print(f"説明数: {len(result['descriptions'])}")
    print(f"編集提案数: {len(result['editing_suggestions'])}")
    
    return True

async def run_tests(video_path):
    """
    すべてのテストを実行
    
    Args:
        video_path: テスト用動画ファイルのパス
    """
    # 音声ファイルを抽出（テスト用）
    audio_path = os.path.splitext(video_path)[0] + ".wav"
    os.system(f"ffmpeg -i {video_path} -q:a 0 -map a {audio_path} -y")
    
    # シーン検出のテスト
    scene_detection_success = await test_scene_detection(video_path)
    
    # 音声認識のテスト
    transcription_success = await test_transcription(audio_path)
    
    # 画像分析のテスト（10秒、30秒、60秒のフレームを分析）
    vision_analysis_success = await test_vision_analysis(video_path, [10.0, 30.0, 60.0])
    
    # 完全なパイプラインのテスト
    pipeline_success = await test_full_pipeline(video_path)
    
    # テスト結果のサマリー
    print("\n=== テスト結果サマリー ===")
    print(f"シーン検出: {'成功' if scene_detection_success else '失敗'}")
    print(f"音声認識: {'成功' if transcription_success else '失敗'}")
    print(f"画像分析: {'成功' if vision_analysis_success else '失敗'}")
    print(f"完全なパイプライン: {'成功' if pipeline_success else '失敗'}")
    
    # 一時ファイルを削除
    if os.path.exists(audio_path):
        os.remove(audio_path)

if __name__ == "__main__":
    # テスト用動画ファイルのパス
    video_path = "path/to/test_video.mp4"
    
    # テストを実行
    asyncio.run(run_tests(video_path))
