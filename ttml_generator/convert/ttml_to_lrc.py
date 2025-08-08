import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from parser.ttml_parser import TTMLParser

class TTMLToLRC:
    def __init__(self):
        self.parser = TTMLParser()
    
    def convert(self, ttml_file, output_file):
        """将TTML转换为LRC格式"""
        lyrics = self.parser.parse(ttml_file)
        
        lrc_content = []
        for line in lyrics:
            # 转换时间格式 00:01:23.456 -> [01:23.45]
            time_parts = line['start'].split(':')
            minutes = int(time_parts[1])
            seconds = float(time_parts[2])
            
            lrc_time = f"[{minutes:02d}:{seconds:05.2f}]"
            lrc_content.append(f"{lrc_time}{line['text']}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lrc_content))
        
        return output_file