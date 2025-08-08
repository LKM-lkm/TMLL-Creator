import xml.etree.ElementTree as ET

class TTMLParser:
    def __init__(self):
        self.namespaces = {
            'ttml': 'http://www.w3.org/ns/ttml',
            'ttm': 'http://www.w3.org/ns/ttml#metadata'
        }
    
    def parse(self, ttml_file):
        """解析TTML文件为统一数据结构"""
        tree = ET.parse(ttml_file)
        root = tree.getroot()
        
        lyrics = []
        
        # 解析<p>标签
        for p in root.findall('.//ttml:p', self.namespaces):
            start = p.get('begin')
            end = p.get('end')
            key = p.get('{http://music.apple.com/lyric-ttml-internal}key') or p.get('{http://www.w3.org/XML/1998/namespace}id')
            role = p.get('{http://www.w3.org/ns/ttml#metadata}role')
            
            # 检查是否有嵌套的背景歌词 span
            bg_span = p.find('.//ttml:span[@ttm:role="x-bg"]', self.namespaces)
            
            if bg_span is not None:
                # 有背景歌词，分离主歌词和背景歌词
                main_text = ''.join([t for t in p.itertext() if t not in bg_span.itertext()])
                bg_text = ''.join(bg_span.itertext())
                bg_start = bg_span.get('begin') or start
                bg_end = bg_span.get('end') or end
                
                # 主歌词
                lyrics.append({
                    'text': main_text.strip(),
                    'start': start,
                    'end': end,
                    'key': key
                })
                
                # 背景歌词作为单独的x-bg角色
                lyrics.append({
                    'text': bg_text.strip(),
                    'start': bg_start,
                    'end': bg_end,
                    'role': 'x-bg',
                    'key': f"{key}_bg" if key else None
                })
            else:
                # 没有背景歌词，直接添加
                text = ''.join(p.itertext())
                lyrics.append({
                    'text': text.strip(),
                    'start': start,
                    'end': end,
                    'key': key,
                    'role': role
                })
        
        # 解析独立的<span>标签（角色标记）
        # 找到所有不在p标签内的span
        all_spans = root.findall('.//ttml:span', self.namespaces)
        p_spans = root.findall('.//ttml:p//ttml:span', self.namespaces)
        
        for span in all_spans:
            if span in p_spans:
                continue  # 跳过嵌套在p标签内的span
                
            role = span.get('{http://www.w3.org/ns/ttml#metadata}role')
            if role:  # 只处理有角色标记的span
                inner_span = span.find('ttml:span', self.namespaces)
                if inner_span is not None:
                    text = ''.join(inner_span.itertext())
                    start = inner_span.get('begin')
                    end = inner_span.get('end')
                    
                    lyrics.append({
                        'text': text.strip(),
                        'start': start,
                        'end': end,
                        'role': role
                    })
        
        return sorted(lyrics, key=lambda x: x['start'] or '00:00.000')