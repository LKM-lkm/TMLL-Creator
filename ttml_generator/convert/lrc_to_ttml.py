import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from parser.lrc_parser import LRCParser
from renderer import TTMLRenderer

class LRCToTTML:
    def __init__(self):
        self.parser = LRCParser()
        self.renderer = TTMLRenderer()
    
    def convert(self, lrc_file, output_file):
        """将LRC转换为TTML格式"""
        lyrics = self.parser.parse(lrc_file)
        ttml_content = self.renderer.render(lyrics)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(ttml_content)
        
        return output_file