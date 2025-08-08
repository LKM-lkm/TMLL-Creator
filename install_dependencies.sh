#!/bin/bash

echo "正在安装TTML歌词生成器依赖..."
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.8或更高版本"
    exit 1
fi

echo "检测到Python版本:"
python3 --version

echo
echo "正在安装基础依赖..."
pip3 install -r requirements.txt

echo
echo "正在检查可选依赖..."

# 尝试安装librosa（变速不变调支持）
echo "正在安装librosa（高质量变速支持）..."
if ! pip3 install librosa soundfile; then
    echo "警告: librosa安装失败，将使用基础变速功能"
fi

echo
echo "正在检查FFmpeg..."
python3 check_ffmpeg.py

echo
echo "依赖安装完成！"
echo
echo "使用方法:"
echo "  python3 run_gui.py    # 启动GUI界面"
echo "  python3 -m ttml_generator.main  # 命令行版本"
echo