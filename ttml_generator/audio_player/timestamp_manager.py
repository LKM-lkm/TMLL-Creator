class TimestampManager:
    def __init__(self):
        self.timestamps = []
        self.current_lyric_index = 0
    
    def add_timestamp(self, time_ms, timestamp_type, text=""):
        """添加时间戳"""
        timestamp = {
            'time': time_ms,
            'type': timestamp_type,  # 'start' or 'end'
            'text': text,
            'formatted_time': self.format_time(time_ms)
        }
        self.timestamps.append(timestamp)
        return timestamp
    
    def format_time(self, ms):
        """将毫秒转换为TTML时间格式"""
        seconds = ms / 1000
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
    
    def get_lyrics_data(self):
        """导出为歌词数据结构"""
        lyrics = []
        start_time = None
        
        for i in range(0, len(self.timestamps), 2):
            if i + 1 < len(self.timestamps):
                start = self.timestamps[i]
                end = self.timestamps[i + 1]
                
                if start['type'] == 'start' and end['type'] == 'end':
                    lyrics.append({
                        'text': start.get('text', f'歌词 {len(lyrics) + 1}'),
                        'start': start['formatted_time'],
                        'end': end['formatted_time']
                    })
        
        return lyrics
    
    def clear_timestamps(self):
        """清空时间戳"""
        self.timestamps = []
        self.current_lyric_index = 0