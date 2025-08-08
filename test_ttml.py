#!/usr/bin/env python3
"""
测试TTML文件打开功能
"""

import sys
import os
sys.path.append('ttml_generator')

from ttml_generator.renderer import TTMLRenderer
from ttml_generator.file_manager import FileManager
from ttml_generator.parser.ttml_parser import TTMLParser

# 创建测试数据
lyrics_data = [
    {"text": "你好，世界", "start": "00:00:10.000", "end": "00:00:12.500", "role": "x-duet-a"},
    {"text": "我一直在等你", "start": "00:00:12.500", "end": "00:00:15.000", "role": "x-duet-b"},
    {"text": "(Held)", "start": "00:00:15.000", "end": "00:00:16.000", "role": "x-bg"},
    {"text": "主唱段落", "start": "00:00:16.000", "end": "00:00:18.000"}
]

# 生成TTML文件
renderer = TTMLRenderer()
file_manager = FileManager()
ttml_content = renderer.render(lyrics_data)
output_file = file_manager.save_ttml(ttml_content, "test.ttml")
print(f"生成测试文件: {output_file}")

# 测试解析TTML文件
parser = TTMLParser()
parsed_data = parser.parse(output_file)
print(f"解析结果: {len(parsed_data)} 条歌词")
for item in parsed_data:
    print(f"  {item['start']} - {item['end']}: {item['text']} [{item.get('role', 'main')}]")