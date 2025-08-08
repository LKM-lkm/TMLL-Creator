import re

class LRCParser:
    def __init__(self):
        self.timestamp_pattern = r'\[(\d{2}):(\d{2})\.(\d{2})\](.+)'
    
    def parse(self, lrc_file):
        """解析LRC文件为统一数据结构"""
        lyrics = []
        
        with open(lrc_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            match = re.match(self.timestamp_pattern, line.strip())
            if match:
                minutes, seconds, centiseconds, text = match.groups()
                
                # 转换为TTML时间格式
                start_time = f"00:{minutes}:{seconds}.{centiseconds}0"
                
                lyrics.append({
                    'text': text.strip(),
                    'start': start_time,
                    'end': None  # LRC通常只有开始时间
                })
        
        # 计算结束时间
        for i in range(len(lyrics) - 1):
            lyrics[i]['end'] = lyrics[i + 1]['start']
        
        # 最后一句默认持续3秒
        if lyrics:
            last_start = lyrics[-1]['start']
            parts = last_start.split(':')
            end_seconds = float(parts[2]) + 3.0
            lyrics[-1]['end'] = f"{parts[0]}:{parts[1]}:{end_seconds:06.3f}"
        
        return lyrics