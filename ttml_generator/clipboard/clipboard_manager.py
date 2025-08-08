import pyperclip
import re

class ClipboardManager:
    def __init__(self):
        self.lrc_pattern = r'\[(\d{2}):(\d{2})\.(\d{2})\](.+)'
    
    def import_from_clipboard(self):
        """从剪贴板导入内容"""
        content = pyperclip.paste()
        
        # 检测格式
        if content.startswith('<?xml'):
            return self._parse_ttml_content(content)
        elif re.search(self.lrc_pattern, content):
            return self._parse_lrc_content(content)
        else:
            return self._parse_plain_text(content)
    
    def export_to_clipboard(self, content):
        """导出内容到剪贴板"""
        pyperclip.copy(content)
    
    def _parse_ttml_content(self, content):
        """解析TTML内容"""
        # 简化解析，实际应使用TTMLParser
        return [{'text': 'TTML content detected', 'start': '00:00:00.000', 'end': '00:00:03.000'}]
    
    def _parse_lrc_content(self, content):
        """解析LRC内容"""
        lyrics = []
        for line in content.split('\n'):
            match = re.match(self.lrc_pattern, line.strip())
            if match:
                minutes, seconds, centiseconds, text = match.groups()
                start_time = f"00:{minutes}:{seconds}.{centiseconds}0"
                lyrics.append({
                    'text': text.strip(),
                    'start': start_time,
                    'end': None
                })
        return lyrics
    
    def _parse_plain_text(self, content):
        """解析纯文本"""
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        lyrics = []
        for i, line in enumerate(lines):
            start_time = f"00:00:{i*3:02d}.000"
            end_time = f"00:00:{(i+1)*3:02d}.000"
            lyrics.append({
                'text': line,
                'start': start_time,
                'end': end_time
            })
        return lyrics