"""
エラーハンドリングとロギングのユーティリティ
"""
import logging
import os
import sys
import traceback
from functools import wraps

# ロガーの設定
logger = logging.getLogger("mountain_video_analyzer")
logger.setLevel(logging.INFO)

# コンソールハンドラ
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

# ファイルハンドラ
os.makedirs("logs", exist_ok=True)
file_handler = logging.FileHandler("logs/mountain_video_analyzer.log")
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)

def log_exception(func):
    """
    例外をログに記録するデコレータ
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"関数 {func.__name__} で例外が発生しました: {str(e)}")
            logger.debug(traceback.format_exc())
            raise
    return wrapper

async def async_log_exception(func):
    """
    非同期関数の例外をログに記録するデコレータ
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"非同期関数 {func.__name__} で例外が発生しました: {str(e)}")
            logger.debug(traceback.format_exc())
            raise
    return wrapper

class ErrorHandler:
    """
    エラーハンドリングユーティリティ
    """
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
        error_message = message or str(error)
        error_type = error_type or type(error).__name__
        
        logger.error(f"{error_type}: {error_message}")
        logger.debug(traceback.format_exc())
        
        return {
            "error": True,
            "error_type": error_type,
            "message": error_message
        }
    
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
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"ファイル {file_path} が見つかりません")
        return True
    
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
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in allowed_extensions:
            raise ValueError(f"ファイル拡張子 {ext} は許可されていません。許可される拡張子: {', '.join(allowed_extensions)}")
        return True
