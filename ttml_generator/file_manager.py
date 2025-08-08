import os
import shutil
from datetime import datetime

class FileManager:
    def __init__(self, output_dir="output", backup_dir="backup"):
        self.output_dir = output_dir
        self.backup_dir = backup_dir
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(backup_dir, exist_ok=True)
    
    def save_ttml(self, content, filename):
        """保存TTML文件并自动备份"""
        output_path = os.path.join(self.output_dir, filename)
        
        # 保存文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 自动备份
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{os.path.splitext(filename)[0]}_{timestamp}.ttml"
        backup_path = os.path.join(self.backup_dir, backup_filename)
        shutil.copy2(output_path, backup_path)
        
        return output_path