#!/usr/bin/env python3
"""
安装TTML歌词生成器所需的依赖
"""

import subprocess
import sys
import os
import platform

def install_package(package):
    """安装Python包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} 安装成功")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ {package} 安装失败")
        return False

def install_ffmpeg():
    """安装ffmpeg"""
    system = platform.system().lower()
    
    if system == "windows":
        print("🔧 Windows系统需要手动安装ffmpeg:")
        print("1. 访问 https://ffmpeg.org/download.html")
        print("2. 下载Windows版本")
        print("3. 解压到任意目录")
        print("4. 将ffmpeg.exe所在目录添加到系统PATH环境变量")
        print("5. 重启命令行窗口")
        
        # 尝试检查是否已安装
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            print("✅ ffmpeg 已安装")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  ffmpeg 未安装或未配置PATH")
            return False
    
    elif system == "darwin":  # macOS
        try:
            subprocess.check_call(["brew", "install", "ffmpeg"])
            print("✅ ffmpeg 安装成功")
            return True
        except subprocess.CalledProcessError:
            print("❌ ffmpeg 安装失败，请手动安装: brew install ffmpeg")
            return False
    
    elif system == "linux":
        try:
            subprocess.check_call(["sudo", "apt", "update"])
            subprocess.check_call(["sudo", "apt", "install", "-y", "ffmpeg"])
            print("✅ ffmpeg 安装成功")
            return True
        except subprocess.CalledProcessError:
            print("❌ ffmpeg 安装失败，请手动安装: sudo apt install ffmpeg")
            return False
    
    return False

def main():
    print("🎵 TTML歌词生成器依赖安装程序")
    print("=" * 40)
    
    # 安装Python包
    packages = [
        "jinja2>=3.0.0",
        "pydub>=0.25.0", 
        "pygame>=2.0.0",
        "pyperclip>=1.8.0",
        "matplotlib>=3.5.0",
        "numpy>=1.21.0"
    ]
    
    print("📦 安装Python依赖包...")
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 Python包安装结果: {success_count}/{len(packages)} 成功")
    
    # 安装ffmpeg
    print("\n🎬 安装ffmpeg...")
    ffmpeg_success = install_ffmpeg()
    
    print("\n" + "=" * 40)
    if success_count == len(packages) and ffmpeg_success:
        print("🎉 所有依赖安装完成！")
        print("现在可以运行: python run_gui.py")
    else:
        print("⚠️  部分依赖安装失败，请手动安装缺失的组件")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()