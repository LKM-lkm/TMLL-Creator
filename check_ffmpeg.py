#!/usr/bin/env python3
"""
检查ffmpeg安装状态
"""

import subprocess
import os
from pydub.utils import which
from pydub import AudioSegment

def setup_ffmpeg_path():
    """直接设置ffmpeg路径"""
    # Chocolatey安装的ffmpeg路径
    choco_ffmpeg = r"C:\ProgramData\chocolatey\bin\ffmpeg.exe"
    
    if os.path.exists(choco_ffmpeg):
        print(f"找到Chocolatey ffmpeg: {choco_ffmpeg}")
        # 直接设置pydub使用的ffmpeg路径
        AudioSegment.converter = choco_ffmpeg
        AudioSegment.ffmpeg = choco_ffmpeg
        AudioSegment.ffprobe = choco_ffmpeg.replace("ffmpeg.exe", "ffprobe.exe")
        
        # 添加到当前进程PATH
        choco_bin = os.path.dirname(choco_ffmpeg)
        current_path = os.environ.get('PATH', '')
        if choco_bin not in current_path:
            os.environ['PATH'] = choco_bin + os.pathsep + current_path
        
        print("ffmpeg路径已设置")
        return True
    
    return False

def check_ffmpeg():
    print("检查ffmpeg安装状态...")
    print("=" * 30)
    
    # 先尝试设置路径
    setup_ffmpeg_path()
    
    # 检查系统PATH中的ffmpeg
    system_ffmpeg = which("ffmpeg")
    if system_ffmpeg:
        print(f"系统ffmpeg: {system_ffmpeg}")
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"   版本: {version_line}")
        except:
            pass
    else:
        print("系统PATH中未找到ffmpeg")
    
    # 检查本地ffmpeg
    local_ffmpeg = os.path.join("ffmpeg", "bin", "ffmpeg.exe")
    if os.path.exists(local_ffmpeg):
        print(f"本地ffmpeg: {local_ffmpeg}")
    else:
        print("本地目录中未找到ffmpeg")
    
    print("\n" + "=" * 30)
    if system_ffmpeg or os.path.exists(local_ffmpeg):
        print("ffmpeg可用，支持所有音频格式！")
    else:
        print("ffmpeg不可用，仅支持WAV和MP3格式")

if __name__ == "__main__":
    check_ffmpeg()