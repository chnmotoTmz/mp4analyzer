"""
ADK Webアプリケーション - 登山動画シーン説明ジェネレーターのWebインターフェース
"""
import os
import asyncio
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import tempfile
import shutil
from ..agents.main_agent import MountainVideoAnalyzerAgent
from ..utils.session_manager import process_video, process_video_streaming

# ADK Webアプリケーションを作成
def create_web_app():
    # メインエージェントを作成
    main_agent = MountainVideoAnalyzerAgent()
    
    # FastAPIアプリケーションを作成
    app = FastAPI(
        title="登山動画シーン説明ジェネレーター",
        description="AIを活用した登山動画分析・編集支援ツール"
    )
    
    # 静的ファイルとテンプレートの設定
    app.mount("/static", StaticFiles(directory="static"), name="static")
    templates = Jinja2Templates(directory="templates")
    
    # アップロードディレクトリの作成
    os.makedirs("uploads", exist_ok=True)
    
    # ルートページ
    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})
    
    # 動画アップロードエンドポイント
    @app.post("/upload")
    async def upload_video(file: UploadFile = File(...)):
        # 一時ファイルとして保存
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1])
        try:
            # アップロードされたファイルを一時ファイルにコピー
            with temp_file as f:
                shutil.copyfileobj(file.file, f)
            
            # ファイルパスを返す
            return {"filename": file.filename, "filepath": temp_file.name}
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
    
    # 動画分析エンドポイント
    @app.post("/analyze")
    async def analyze_video(filepath: str = Form(...)):
        try:
            # 動画を分析
            result = await process_video(main_agent, filepath)
            return result
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
    
    # ストリーミング分析エンドポイント
    @app.websocket("/analyze-stream")
    async def analyze_video_stream(websocket):
        await websocket.accept()
        
        # WebSocketからファイルパスを受信
        filepath = await websocket.receive_text()
        
        # コールバック関数
        async def callback(data):
            await websocket.send_json(data)
        
        try:
            # 動画をストリーミング分析
            await process_video_streaming(main_agent, filepath, callback)
        except Exception as e:
            await websocket.send_json({"error": str(e)})
        finally:
            await websocket.close()
    
    return app

# サーバーを起動
def start_server(host="0.0.0.0", port=8000):
    app = create_web_app()
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server()
