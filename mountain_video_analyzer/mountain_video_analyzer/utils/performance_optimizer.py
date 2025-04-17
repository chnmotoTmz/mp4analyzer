"""
パフォーマンス最適化ユーティリティ
"""
import time
import asyncio
import functools
import threading
from concurrent.futures import ThreadPoolExecutor
from ..config import CONFIG

class PerformanceOptimizer:
    """
    パフォーマンス最適化のためのユーティリティクラス
    """
    
    @staticmethod
    def measure_execution_time(func):
        """
        関数の実行時間を測定するデコレータ
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"関数 {func.__name__} の実行時間: {end_time - start_time:.4f} 秒")
            return result
        return wrapper
    
    @staticmethod
    def async_measure_execution_time(func):
        """
        非同期関数の実行時間を測定するデコレータ
        """
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)
            end_time = time.time()
            print(f"非同期関数 {func.__name__} の実行時間: {end_time - start_time:.4f} 秒")
            return result
        return wrapper
    
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
        with ThreadPoolExecutor() as executor:
            future = executor.submit(func, *args, **kwargs)
            return future.result()
    
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
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, 
            functools.partial(func, *args, **kwargs)
        )
    
    @staticmethod
    def cache_result(func):
        """
        関数の結果をキャッシュするデコレータ
        """
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 引数をキーとして使用するためにハッシュ可能な形式に変換
            key = str(args) + str(sorted(kwargs.items()))
            
            if key not in cache:
                cache[key] = func(*args, **kwargs)
            
            return cache[key]
        
        return wrapper
    
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
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_result = process_func(batch)
            results.extend(batch_result)
        
        return results
    
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
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_result = await process_func(batch)
            results.extend(batch_result)
        
        return results
