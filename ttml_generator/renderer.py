from jinja2 import Environment, FileSystemLoader
import os
from utils import generate_key

class TTMLRenderer:
    def __init__(self, template_dir=None):
        if template_dir is None:
            template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def render(self, lyrics_data, template_name="lyric_block.xml.j2", **kwargs):
        """渲染TTML文件"""
        # 自动生成key
        for i, line in enumerate(lyrics_data):
            if 'key' not in line:
                line['key'] = generate_key(i + 1)
        
        # 计算总时长
        total_duration = "00:00.000"
        if lyrics_data:
            last_lyric = max(lyrics_data, key=lambda x: x.get('end', '00:00.000'))
            total_duration = last_lyric.get('end', '00:00.000')
        
        template = self.env.get_template(template_name)
        return template.render(
            lyrics=lyrics_data,
            total_duration=total_duration,
            song_title=kwargs.get('song_title'),
            artist=kwargs.get('artist'),
            album=kwargs.get('album')
        )