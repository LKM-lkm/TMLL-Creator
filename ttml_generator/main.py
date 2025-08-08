#!/usr/bin/env python3
"""
TTML歌词生成器主程序
"""

from renderer import TTMLRenderer
from file_manager import FileManager
from clipboard.clipboard_manager import ClipboardManager
from convert.ttml_to_lrc import TTMLToLRC
from convert.lrc_to_ttml import LRCToTTML

def main():
    # 示例歌词数据
    lyrics_data = [
        {"text": "你好，世界", "start": "00:00:10.000", "end": "00:00:12.500", "role": "x-duet-a"},
        {"text": "我一直在等你", "start": "00:00:12.500", "end": "00:00:15.000", "role": "x-duet-b"},
        {"text": "(Held)", "start": "00:00:15.000", "end": "00:00:16.000", "role": "x-bg"},
        {"text": "主唱段落", "start": "00:00:16.000", "end": "00:00:18.000"}
    ]
    
    # 初始化组件
    renderer = TTMLRenderer()
    file_manager = FileManager()
    
    # 渲染TTML
    ttml_content = renderer.render(lyrics_data)
    
    # 保存文件
    output_file = file_manager.save_ttml(ttml_content, "example.ttml")
    print(f"TTML文件已生成: {output_file}")
    
    # 演示剪贴板功能
    clipboard = ClipboardManager()
    clipboard.export_to_clipboard(ttml_content)
    print("TTML内容已复制到剪贴板")

if __name__ == "__main__":
    main()