import re
from datetime import datetime

def generate_key(index):
    """生成itunes:key"""
    return f"L{index + 1}"

def validate_timestamp(timestamp):
    """校验时间戳格式 hh:mm:ss.mmm"""
    pattern = r'^\d{2}:\d{2}:\d{2}\.\d{3}$'
    return bool(re.match(pattern, timestamp))

def format_timestamp(seconds):
    """将秒数转换为TTML时间戳格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"

def parse_timestamp(timestamp):
    """解析时间戳为秒数"""
    parts = timestamp.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds