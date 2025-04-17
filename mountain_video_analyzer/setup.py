"""
setup.pyファイル - パッケージのセットアップスクリプト
"""
from setuptools import setup, find_packages

setup(
    name="mountain_video_analyzer",
    version="1.0.0",
    author="Mountain Video Analyzer Team",
    description="Google ADKを活用した登山動画シーン説明ジェネレーター",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mountain-video-analyzer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "google-adk",
        "google-generativeai",
        "ffmpeg-python",
        "faster-whisper",
        "uvicorn",
        "fastapi",
    ],
    entry_points={
        "console_scripts": [
            "mountain-video-analyzer=mountain_video_analyzer.main:main",
        ],
    },
)
