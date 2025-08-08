import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import pygame
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from renderer import TTMLRenderer
from file_manager import FileManager
from clipboard.clipboard_manager import ClipboardManager
from parser.ttml_parser import TTMLParser
from parser.lrc_parser import LRCParser
from convert.lrc_to_ttml import LRCToTTML
from convert.ttml_to_lrc import TTMLToLRC

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TTML歌词生成器")
        self.root.geometry("900x700")
        
        self.renderer = TTMLRenderer()
        self.file_manager = FileManager()
        self.clipboard = ClipboardManager()
        self.ttml_parser = TTMLParser()
        self.lrc_parser = LRCParser()
        self.lrc_to_ttml = LRCToTTML()
        self.ttml_to_lrc = TTMLToLRC()
        
        self.lyrics_data = []
        self.history = []
        self.current_selection = None
        
        # 播放器变量
        self.audio = None
        self.audio_file = None
        self.is_playing = False
        self.current_pos = 0
        self.speed = 1.0
        self.start_time = 0


        
        self.setup_ui()
        self.update_timer()
    
    def setup_ui(self):
        # 工具栏
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(toolbar, text="打开文件", command=self.open_file).pack(side='left', padx=2)
        ttk.Button(toolbar, text="保存文件", command=self.save_file).pack(side='left', padx=2)
        ttk.Button(toolbar, text="撤销", command=self.undo).pack(side='left', padx=2)
        ttk.Button(toolbar, text="查找替换", command=self.find_replace).pack(side='left', padx=2)
        ttk.Button(toolbar, text="格式转换", command=self.format_convert).pack(side='left', padx=2)
        ttk.Button(toolbar, text="从剪贴板导入", command=self.import_clipboard).pack(side='left', padx=2)
        ttk.Button(toolbar, text="复制到剪贴板", command=self.export_clipboard).pack(side='left', padx=2)
        
        # 音频播放器
        player_frame = ttk.LabelFrame(self.root, text="音频播放器")
        player_frame.pack(fill='x', padx=5, pady=5)
        
        # 播放控制
        control_frame = ttk.Frame(player_frame)
        control_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(control_frame, text="选择音频", command=self.load_audio).pack(side='left', padx=2)
        self.file_label = ttk.Label(control_frame, text="未选择文件")
        self.file_label.pack(side='left', padx=10)
        
        self.play_btn = ttk.Button(control_frame, text="播放 (SPACE)", command=self.toggle_play)
        self.play_btn.pack(side='left', padx=5)
        
        ttk.Label(control_frame, text="速度:").pack(side='left', padx=5)
        self.speed_var = tk.StringVar(value="1.0x")
        self.speed_label = ttk.Label(control_frame, textvariable=self.speed_var)
        self.speed_label.pack(side='left')
        
        ttk.Label(control_frame, text="时间:").pack(side='left', padx=10)
        self.time_var = tk.StringVar(value="00:00.000")
        self.time_label = ttk.Label(control_frame, textvariable=self.time_var, font=('Consolas', 10))
        self.time_label.pack(side='left')
        
        # 进度条
        self.progress = ttk.Scale(player_frame, from_=0, to=100, orient='horizontal', command=self.on_progress_change)
        self.progress.pack(fill='x', padx=5, pady=5)
        
        # 时间戳控制
        timestamp_frame = ttk.Frame(player_frame)
        timestamp_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(timestamp_frame, text="标记开始(F)", command=self.mark_start).pack(side='left', padx=2)
        ttk.Button(timestamp_frame, text="标记结束(G)", command=self.mark_end).pack(side='left', padx=2)
        ttk.Label(timestamp_frame, text="歌词:").pack(side='left', padx=10)
        self.lyric_entry = ttk.Entry(timestamp_frame, width=30)
        self.lyric_entry.pack(side='left', padx=5)
        
        # 歌词列表
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        columns = ('序号', '开始时间', '结束时间', '歌词', '角色')
        self.lyrics_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.lyrics_tree.heading(col, text=col)
            self.lyrics_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.lyrics_tree.yview)
        self.lyrics_tree.configure(yscrollcommand=scrollbar.set)
        
        self.lyrics_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 编辑控件
        edit_frame = ttk.Frame(self.root)
        edit_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(edit_frame, text="开始:").grid(row=0, column=0)
        self.start_entry = ttk.Entry(edit_frame, width=15)
        self.start_entry.grid(row=0, column=1, padx=2)
        
        ttk.Label(edit_frame, text="结束:").grid(row=0, column=2)
        self.end_entry = ttk.Entry(edit_frame, width=15)
        self.end_entry.grid(row=0, column=3, padx=2)
        
        ttk.Label(edit_frame, text="歌词:").grid(row=0, column=4)
        self.text_entry = ttk.Entry(edit_frame, width=30)
        self.text_entry.grid(row=0, column=5, padx=2)
        
        ttk.Label(edit_frame, text="角色:").grid(row=0, column=6)
        self.role_combo = ttk.Combobox(edit_frame, values=['', 'x-bg', 'x-duet-a', 'x-duet-b'], width=10)
        self.role_combo.grid(row=0, column=7, padx=2)
        
        # 按钮
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(btn_frame, text="添加", command=self.add_lyric).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="修改", command=self.edit_lyric).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="删除", command=self.delete_lyric).pack(side='left', padx=2)
        
        # 预览
        preview_frame = ttk.Frame(self.root)
        preview_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        ttk.Label(preview_frame, text="TTML预览").pack(anchor='w')
        
        self.preview_text = tk.Text(preview_frame, height=10, font=('Consolas', 9))
        preview_scroll = ttk.Scrollbar(preview_frame, orient='vertical', command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=preview_scroll.set)
        
        self.preview_text.pack(side='left', fill='both', expand=True)
        preview_scroll.pack(side='right', fill='y')
        
        self.lyrics_tree.bind('<<TreeviewSelect>>', self.on_select)
        self.lyrics_tree.bind('<Delete>', self.on_delete_key)
        
        # 绑定编辑框事件实现自动保存
        self.start_entry.bind('<KeyRelease>', self.auto_save_edit)
        self.end_entry.bind('<KeyRelease>', self.auto_save_edit)
        self.text_entry.bind('<KeyRelease>', self.auto_save_edit)
        self.role_combo.bind('<<ComboboxSelected>>', self.auto_save_edit)
        
        # 绑定快捷键
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-h>', lambda e: self.find_replace())
        self.root.bind('<KeyPress-f>', lambda e: self.mark_start())
        self.root.bind('<KeyPress-g>', lambda e: self.mark_end())
        self.root.bind('<space>', lambda e: self.toggle_play())
        self.root.bind('<bracketleft>', lambda e: self.change_speed(-0.25))
        self.root.bind('<bracketright>', lambda e: self.change_speed(0.25))
        
        self.lyrics_tree.focus_set()
    
    def save_history(self):
        """保存当前状态到历史记录"""
        import copy
        self.history.append(copy.deepcopy(self.lyrics_data))
        if len(self.history) > 50:  # 限制历史记录数量
            self.history.pop(0)
    
    def undo(self):
        """撤销操作"""
        if self.history:
            self.lyrics_data = self.history.pop()
            self.refresh_tree()
            self.update_preview()
            self.clear_entries()
    
    def auto_save_edit(self, event=None):
        """自动保存编辑内容"""
        selection = self.lyrics_tree.selection()
        if selection and self.current_selection == selection[0]:
            index = int(selection[0]) - 1
            start = self.start_entry.get()
            end = self.end_entry.get()
            text = self.text_entry.get()
            role = self.role_combo.get()
            
            if start and end and text:  # 只有在有效数据时才保存
                self.lyrics_data[index] = {'text': text, 'start': start, 'end': end}
                if role:
                    self.lyrics_data[index]['role'] = role
                
                self.refresh_tree()
                self.update_preview()
                # 重新选中当前行
                self.lyrics_tree.selection_set(selection[0])
    
    def add_lyric(self):
        start = self.start_entry.get()
        end = self.end_entry.get()
        text = self.text_entry.get()
        role = self.role_combo.get()
        
        if not all([start, end, text]):
            messagebox.showwarning("警告", "请填写完整信息")
            return
        
        self.save_history()
        lyric = {'text': text, 'start': start, 'end': end}
        if role:
            lyric['role'] = role
        
        self.lyrics_data.append(lyric)
        self.refresh_tree()
        self.update_preview()
        self.clear_entries()
    
    def edit_lyric(self):
        selection = self.lyrics_tree.selection()
        if not selection:
            return
        
        index = int(selection[0]) - 1
        start = self.start_entry.get()
        end = self.end_entry.get()
        text = self.text_entry.get()
        role = self.role_combo.get()
        
        self.lyrics_data[index] = {'text': text, 'start': start, 'end': end}
        if role:
            self.lyrics_data[index]['role'] = role
        
        self.refresh_tree()
        self.update_preview()
    
    def delete_lyric(self):
        selection = self.lyrics_tree.selection()
        if selection:
            self.save_history()
            index = int(selection[0]) - 1
            del self.lyrics_data[index]
            self.refresh_tree()
            self.update_preview()
            self.clear_entries()
    
    def on_delete_key(self, event):
        self.delete_lyric()
    
    def on_select(self, event):
        selection = self.lyrics_tree.selection()
        if selection:
            self.current_selection = selection[0]
            index = int(selection[0]) - 1
            lyric = self.lyrics_data[index]
            
            self.start_entry.delete(0, tk.END)
            self.start_entry.insert(0, lyric['start'])
            self.end_entry.delete(0, tk.END)
            self.end_entry.insert(0, lyric['end'])
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(0, lyric['text'])
            self.role_combo.set(lyric.get('role', ''))
        else:
            self.current_selection = None
    
    def refresh_tree(self):
        for item in self.lyrics_tree.get_children():
            self.lyrics_tree.delete(item)
        
        for i, lyric in enumerate(self.lyrics_data):
            self.lyrics_tree.insert('', 'end', iid=str(i+1), values=(
                i+1, lyric['start'], lyric['end'], lyric['text'], lyric.get('role', '')
            ))
    
    def update_preview(self):
        if self.lyrics_data:
            ttml_content = self.renderer.render(self.lyrics_data)
        else:
            ttml_content = "<!-- 暂无歌词数据 -->"
        
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(1.0, ttml_content)
    
    def clear_entries(self):
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)
        self.text_entry.delete(0, tk.END)
        self.role_combo.set('')
    
    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("TTML文件", "*.ttml"), ("LRC文件", "*.lrc"), ("所有文件", "*.*")]
        )
        if file_path:
            try:
                if file_path.lower().endswith('.lrc'):
                    self.lyrics_data = self.lrc_parser.parse(file_path)
                else:
                    self.lyrics_data = self.ttml_parser.parse(file_path)
                
                self.refresh_tree()
                self.update_preview()
                messagebox.showinfo("成功", f"已加载 {len(self.lyrics_data)} 条歌词")
            except Exception as e:
                messagebox.showerror("错误", f"打开文件失败: {e}")
    
    def save_file(self):
        if not self.lyrics_data:
            messagebox.showwarning("警告", "没有歌词数据")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".ttml",
            filetypes=[("TTML文件", "*.ttml"), ("LRC文件", "*.lrc")]
        )
        if file_path:
            try:
                if file_path.lower().endswith('.lrc'):
                    self.ttml_to_lrc.convert('temp.ttml', file_path)
                    # 先保存临时TTML文件
                    import tempfile
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.ttml', delete=False, encoding='utf-8') as tmp:
                        tmp.write(self.renderer.render(self.lyrics_data))
                        temp_path = tmp.name
                    self.ttml_to_lrc.convert(temp_path, file_path)
                    os.unlink(temp_path)
                else:
                    ttml_content = self.renderer.render(self.lyrics_data)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(ttml_content)
                
                messagebox.showinfo("成功", f"文件已保存: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("错误", f"保存文件失败: {e}")
    
    def import_clipboard(self):
        try:
            imported_data = self.clipboard.import_from_clipboard()
            self.lyrics_data.extend(imported_data)
            self.refresh_tree()
            self.update_preview()
            messagebox.showinfo("成功", f"已导入 {len(imported_data)} 条歌词")
        except Exception as e:
            messagebox.showerror("错误", f"导入失败: {e}")
    
    def export_clipboard(self):
        if not self.lyrics_data:
            messagebox.showwarning("警告", "没有歌词数据")
            return
        
        ttml_content = self.renderer.render(self.lyrics_data)
        self.clipboard.export_to_clipboard(ttml_content)
        messagebox.showinfo("成功", "TTML内容已复制到剪贴板")
    
    def load_audio(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("音频文件", "*.mp3 *.wav *.flac *.aac *.m4a *.ogg")]
        )
        if file_path:
            try:
                import pygame
                from pydub import AudioSegment
                from pydub.utils import which
                
                # 设置本地ffmpeg路径
                local_ffmpeg = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ffmpeg", "bin", "ffmpeg.exe")
                choco_ffmpeg = r"C:\ProgramData\chocolatey\bin\ffmpeg.exe"
                pip_ffmpeg = r"C:\Users\Administrator\AppData\Local\Programs\Python\Python313\Lib\site-packages\ffmpeg\bin\ffmpeg.exe"
                
                if os.path.exists(local_ffmpeg):
                    AudioSegment.converter = local_ffmpeg
                    AudioSegment.ffmpeg = local_ffmpeg
                    AudioSegment.ffprobe = local_ffmpeg.replace("ffmpeg.exe", "ffprobe.exe")
                elif os.path.exists(pip_ffmpeg):
                    AudioSegment.converter = pip_ffmpeg
                    AudioSegment.ffmpeg = pip_ffmpeg
                    AudioSegment.ffprobe = pip_ffmpeg.replace("ffmpeg.exe", "ffprobe.exe")
                elif os.path.exists(choco_ffmpeg):
                    AudioSegment.converter = choco_ffmpeg
                    AudioSegment.ffmpeg = choco_ffmpeg
                    AudioSegment.ffprobe = choco_ffmpeg.replace("ffmpeg.exe", "ffprobe.exe")
                    # 添加到PATH
                    choco_bin = os.path.dirname(choco_ffmpeg)
                    current_path = os.environ.get('PATH', '')
                    if choco_bin not in current_path:
                        os.environ['PATH'] = choco_bin + os.pathsep + current_path
                elif not which("ffmpeg"):
                    # 提示安装ffmpeg
                    result = messagebox.askyesno("需要ffmpeg", "需要ffmpeg支持多种音频格式\n\n是否自动下载安装？")
                    if result:
                        import subprocess
                        subprocess.run(["python", "install_ffmpeg_minimal.py"])
                        messagebox.showinfo("提示", "请重新加载音频文件")
                        return
                    else:
                        messagebox.showinfo("提示", "只能加载WAV和MP3格式")
                        if not file_path.lower().endswith(('.wav', '.mp3')):
                            return
                
                pygame.mixer.init()
                self.audio = AudioSegment.from_file(file_path)
                self.audio_file = file_path
                self.current_pos = 0
                self.is_playing = False

                
                self.file_label.config(text=os.path.basename(file_path))
                self.progress.config(to=len(self.audio))
                
                messagebox.showinfo("成功", f"已加载音频: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("错误", f"加载音频失败: {e}\n\n请确保文件格式正确或安装ffmpeg")
    
    def toggle_play(self):
        if not self.audio:
            messagebox.showwarning("警告", "请先选择音频文件")
            return
        
        try:
            import pygame
            import time
            
            if self.is_playing:
                pygame.mixer.music.pause()
                self.play_btn.config(text="播放 (SPACE)")
                self.is_playing = False
            else:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.unpause()
                else:
                    if self.speed != 1.0:
                        try:
                            import librosa
                            import soundfile as sf
                            import tempfile
                            
                            # 使用librosa实现变速不变调
                            y, sr = librosa.load(self.audio_file, sr=None, offset=self.current_pos/1000.0, duration=15.0)
                            y_stretched = librosa.effects.time_stretch(y, rate=self.speed)
                            
                            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                                sf.write(tmp.name, y_stretched, sr)
                                pygame.mixer.music.load(tmp.name)
                                pygame.mixer.music.play()
                                self.root.after(100, lambda: self.cleanup_temp_file(tmp.name))
                        except ImportError:
                            # 如果没有librosa，使用pydub的speedup
                            try:
                                import tempfile
                                segment = self.audio[self.current_pos:self.current_pos + 15000]
                                speed_segment = segment.speedup(playback_speed=self.speed)
                                
                                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                                    speed_segment.export(tmp.name, format='wav')
                                    pygame.mixer.music.load(tmp.name)
                                    pygame.mixer.music.play()
                                    self.root.after(100, lambda: self.cleanup_temp_file(tmp.name))
                            except:
                                pygame.mixer.music.load(self.audio_file)
                                pygame.mixer.music.play(start=self.current_pos / 1000.0)
                        except:
                            pygame.mixer.music.load(self.audio_file)
                            pygame.mixer.music.play(start=self.current_pos / 1000.0)
                    else:
                        pygame.mixer.music.load(self.audio_file)
                        pygame.mixer.music.play(start=self.current_pos / 1000.0)
                    
                    self.start_time = time.time() - (self.current_pos / 1000.0 / self.speed)
                
                self.play_btn.config(text="暂停 (SPACE)")
                self.is_playing = True
        except Exception as e:
            messagebox.showerror("错误", f"播放失败: {e}")
    
    def change_speed(self, delta):
        self.speed = max(0.5, min(2.0, self.speed + delta))
        self.speed_var.set(f"{self.speed:.2f}x")
    
    def cleanup_temp_file(self, filepath):
        """清理临时文件"""
        try:
            if os.path.exists(filepath):
                os.unlink(filepath)
        except:
            pass
    

    
    def on_progress_change(self, value):
        if self.audio:
            self.current_pos = int(float(value))
            if not self.is_playing:
                self.update_time_display()
    
    def update_timer(self):
        try:
            if self.is_playing and pygame.mixer.music.get_busy():
                import time
                elapsed = time.time() - self.start_time
                # 考虑变速的时间计算
                self.current_pos = min(int(elapsed * 1000 * self.speed), len(self.audio) if self.audio else 0)
                
                if self.current_pos >= len(self.audio) if self.audio else 0:
                    self.is_playing = False
                    self.play_btn.config(text="播放 (SPACE)")
            
            if self.audio:
                self.update_time_display()
                self.progress.set(self.current_pos)
        except:
            pass
        
        self.root.after(50, self.update_timer)
    
    def update_time_display(self):
        if self.audio:
            current_seconds = self.current_pos / 1000.0
            total_seconds = len(self.audio) / 1000.0
            
            current_time = self.format_time_display(current_seconds)
            total_time = self.format_time_display(total_seconds)
            
            self.time_var.set(f"{current_time} / {total_time}")
    
    def format_time_display(self, seconds):
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes:02d}:{secs:06.3f}"
    
    def mark_start(self):
        if self.audio:
            current_time = self.format_time(self.current_pos)
            lyric_text = self.lyric_entry.get().strip() or "新歌词"
            
            self.start_entry.delete(0, tk.END)
            self.start_entry.insert(0, current_time)
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(0, lyric_text)
            self.auto_save_edit()
        else:
            messagebox.showwarning("警告", "请先加载音频文件")
    
    def mark_end(self):
        if self.audio:
            current_time = self.format_time(self.current_pos)
            self.end_entry.delete(0, tk.END)
            self.end_entry.insert(0, current_time)
            self.auto_save_edit()
            self.lyric_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("警告", "请先加载音频文件")
    
    def format_time(self, ms):
        seconds = ms / 1000
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
    
    def find_replace(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("查找替换")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="查找:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        find_entry = tk.Entry(dialog, width=40)
        find_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="替换:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        replace_entry = tk.Entry(dialog, width=40)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def do_replace():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            if not find_text:
                return
            
            count = 0
            self.save_history()
            for item in self.lyrics_data:
                if find_text in item['text']:
                    item['text'] = item['text'].replace(find_text, replace_text)
                    count += 1
                if 'bg_text' in item and item['bg_text'] and find_text in item['bg_text']:
                    item['bg_text'] = item['bg_text'].replace(find_text, replace_text)
                    count += 1
            
            self.refresh_tree()
            self.update_preview()
            messagebox.showinfo("完成", f"已替换 {count} 处")
            dialog.destroy()
        
        tk.Button(dialog, text="替换全部", command=do_replace).grid(row=2, column=1, pady=10)
    
    def format_convert(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("格式转换")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="选择输入文件:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        input_var = tk.StringVar()
        input_entry = tk.Entry(dialog, textvariable=input_var, width=50)
        input_entry.grid(row=0, column=1, padx=5, pady=5)
        
        def browse_input():
            file_path = filedialog.askopenfilename(
                filetypes=[("TTML文件", "*.ttml"), ("LRC文件", "*.lrc"), ("所有文件", "*.*")]
            )
            if file_path:
                input_var.set(file_path)
        
        tk.Button(dialog, text="浏览", command=browse_input).grid(row=0, column=2, padx=5)
        
        tk.Label(dialog, text="转换为:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        format_var = tk.StringVar(value="TTML")
        format_combo = ttk.Combobox(dialog, textvariable=format_var, values=["TTML", "LRC"], state="readonly")
        format_combo.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        def do_convert():
            input_file = input_var.get()
            if not input_file or not os.path.exists(input_file):
                messagebox.showwarning("警告", "请选择有效的输入文件")
                return
            
            target_format = format_var.get()
            ext = ".ttml" if target_format == "TTML" else ".lrc"
            
            output_file = filedialog.asksaveasfilename(
                defaultextension=ext,
                filetypes=[(f"{target_format}文件", f"*{ext}")]
            )
            
            if output_file:
                try:
                    if input_file.lower().endswith('.lrc') and target_format == "TTML":
                        self.lrc_to_ttml.convert(input_file, output_file)
                    elif input_file.lower().endswith('.ttml') and target_format == "LRC":
                        self.ttml_to_lrc.convert(input_file, output_file)
                    else:
                        messagebox.showwarning("警告", "无需转换，文件格式相同")
                        return
                    
                    messagebox.showinfo("成功", f"转换完成: {os.path.basename(output_file)}")
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("错误", f"转换失败: {e}")
        
        tk.Button(dialog, text="开始转换", command=do_convert).grid(row=2, column=1, pady=20)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()