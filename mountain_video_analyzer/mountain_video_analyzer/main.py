"""
メインエントリーポイント - 登山動画シーン説明ジェネレーターの起動スクリプト
"""
import os
import argparse
import asyncio
from mountain_video_analyzer.agents.main_agent import MountainVideoAnalyzerAgent
from mountain_video_analyzer.utils.session_manager import process_video
from mountain_video_analyzer.ui.web_app import start_server
from mountain_video_analyzer.tests.test_components import run_tests

def main():
    """
    メインエントリーポイント
    """
    parser = argparse.ArgumentParser(description="登山動画シーン説明ジェネレーター")
    subparsers = parser.add_subparsers(dest="command", help="実行するコマンド")
    
    # Webサーバーを起動するコマンド
    server_parser = subparsers.add_parser("server", help="Webサーバーを起動")
    server_parser.add_argument("--host", default="0.0.0.0", help="ホスト名")
    server_parser.add_argument("--port", type=int, default=8000, help="ポート番号")
    
    # 動画を分析するコマンド
    analyze_parser = subparsers.add_parser("analyze", help="動画を分析")
    analyze_parser.add_argument("video_path", help="分析する動画ファイルのパス")
    analyze_parser.add_argument("--output", help="結果を保存するJSONファイルのパス")
    
    # テストを実行するコマンド
    test_parser = subparsers.add_parser("test", help="テストを実行")
    test_parser.add_argument("--video_path", help="テスト用動画ファイルのパス")
    
    args = parser.parse_args()
    
    if args.command == "server":
        # Webサーバーを起動
        print(f"Webサーバーを起動します（{args.host}:{args.port}）")
        start_server(host=args.host, port=args.port)
    
    elif args.command == "analyze":
        # 動画を分析
        if not os.path.exists(args.video_path):
            print(f"エラー: 動画ファイル {args.video_path} が見つかりません")
            return
        
        print(f"動画 {args.video_path} を分析します")
        
        # メインエージェントを作成
        main_agent = MountainVideoAnalyzerAgent()
        
        # 動画を処理
        result = asyncio.run(process_video(main_agent, args.video_path))
        
        # 結果を表示または保存
        if args.output:
            import json
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"結果を {args.output} に保存しました")
        else:
            import json
            print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "test":
        # テストを実行
        video_path = args.video_path
        if not video_path:
            print("警告: テスト用動画ファイルが指定されていません。サンプル動画を使用します。")
            # サンプル動画のパスを設定（実際の環境に合わせて変更）
            video_path = "sample_videos/sample_mountain.mp4"
        
        if not os.path.exists(video_path):
            print(f"エラー: テスト用動画ファイル {video_path} が見つかりません")
            return
        
        print(f"テスト用動画 {video_path} を使用してテストを実行します")
        asyncio.run(run_tests(video_path))
    
    else:
        # コマンドが指定されていない場合はヘルプを表示
        parser.print_help()

if __name__ == "__main__":
    main()
