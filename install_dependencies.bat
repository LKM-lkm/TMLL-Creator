@echo off
echo 正在安装TTML歌词生成器依赖...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

echo 检测到Python版本:
python --version

echo.
echo 正在安装基础依赖...
pip install -r requirements.txt

echo.
echo 正在检查可选依赖...

REM 尝试安装librosa（变速不变调支持）
echo 正在安装librosa（高质量变速支持）...
pip install librosa soundfile
if errorlevel 1 (
    echo 警告: librosa安装失败，将使用基础变速功能
)

echo.
echo 正在检查FFmpeg...
python check_ffmpeg.py

echo.
echo 依赖安装完成！
echo.
echo 使用方法:
echo   python run_gui.py    # 启动GUI界面
echo   python -m ttml_generator.main  # 命令行版本
echo.
pause