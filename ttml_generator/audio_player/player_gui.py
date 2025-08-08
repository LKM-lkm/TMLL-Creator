import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pygame
from pydub import AudioSegment
import threading
import time
import os
import sys
sys.path.append(os.path.dirname(__file__))

from waveform import WaveformGenerator
from timestamp_manager import TimestampManager

class AudioPlayer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TTML歌词标注播放器")
        self.root.geometry("1000x700")
        
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        self.audio = None
        self.is_playing = False
        self.current_pos = 0
        self.speed = 1.0
        self.start_time = 0
        
        self.waveform = WaveformGenerator(None)
        self.timestamp_manager = TimestampManager()
        
        self.setup_ui()
        self.setup_bindings()
        self.update_timer()
    
    def setup_ui(self):
        # 文件选择和播放控制
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill='x', padx=10, pady=5)
        
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
        self.time_label = ttk.Label(control_frame, textvariable=self.time_var, font=('Consolas', 12))
        self.time_label.pack(side='left')
        
        # 进度条
        progress_frame = ttk.Frame(self.root)
        progress_frame.pack(fill='x', padx=10, pady=5)
        
        self.progress = ttk.Scale(progress_frame, from_=0, to=100, orient='horizontal', command=self.on_progress_change)
        self.progress.pack(fill='x')
        
        # 波形图
        waveform_frame = ttk.LabelFrame(self.root, text="波形图")
        waveform_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.waveform.canvas_parent = waveform_frame
        
        # 时间戳控制
        timestamp_frame = ttk.Frame(self.root)
        timestamp_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(timestamp_frame, text="标记开始 (F)", command=self.mark_start).pack(side='left', padx=2)
        ttk.Button(timestamp_frame, text="标记结束 (G)", command=self.mark_end).pack(side='left', padx=2)
        ttk.Button(timestamp_frame, text="导出歌词", command=self.export_lyrics).pack(side='left', padx=10)
        ttk.Button(timestamp_frame, text="清空记录", command=self.clear_timestamps).pack(side='left', padx=2)
        
        # 歌词输入
        lyric_frame = ttk.Frame(self.root)
        lyric_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(lyric_frame, text="当前歌词:").pack(side='left')
        self.lyric_entry = ttk.Entry(lyric_frame, width=50)
        self.lyric_entry.pack(side='left', padx=5, fill='x', expand=True)
        
        # 时间戳记录显示
        record_frame = ttk.LabelFrame(self.root, text="时间戳记录")
        record_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.record_text = tk.Text(record_frame, height=8, font=('Consolas', 10))
        record_scroll = ttk.Scrollbar(record_frame, orient='vertical', command=self.record_text.yview)
        self.record_text.configure(yscrollcommand=record_scroll.set)
        
        self.record_text.pack(side='left', fill='both', expand=True)
        record_scroll.pack(side='right', fill='y')
    
    def setup_bindings(self):
        self.root.bind('<space>', lambda e: self.toggle_play())
        self.root.bind('<bracketleft>', lambda e: self.change_speed(-0.25))
        self.root.bind('<bracketright>', lambda e: self.change_speed(0.25))
        self.root.bind('<KeyPress-f>', lambda e: self.mark_start())
        self.root.bind('<KeyPress-g>', lambda e: self.mark_end())
        self.root.focus_set()
    
    def load_audio(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("音频文件", "*.mp3 *.wav *.flac *.aac *.m4a *.ogg")]
        )
        if file_path:
            try:
                self.audio = AudioSegment.from_file(file_path)
                self.file_label.config(text=os.path.basename(file_path))
                self.progress.config(to=len(self.audio))
                
                # 生成波形图
                self.waveform.load_audio(file_path)
                
                messagebox.showinfo("成功", "音频文件加载成功")
            except Exception as e:
                messagebox.showerror("错误", f"无法加载音频文件: {e}")
    
    def toggle_play(self):
        if not self.audio:
            messagebox.showwarning("警告", "请先选择音频文件")
            return
        
        if self.is_playing:
            pygame.mixer.music.pause()
            self.play_btn.config(text="播放 (SPACE)")
        else:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
            else:
                # 从当前位置开始播放
                temp_audio = self.audio[self.current_pos:]
                temp_file = "temp_audio.wav"
                temp_audio.export(temp_file, format="wav")
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                self.start_time = time.time() - (self.current_pos / 1000.0)
            
            self.play_btn.config(text="暂停 (SPACE)")
        
        self.is_playing = not self.is_playing
    
    def change_speed(self, delta):
        self.speed = max(0.5, min(2.0, self.speed + delta))
        self.speed_var.set(f"{self.speed:.2f}x")
        # 注意: pygame不直接支持变速，这里只是显示
    
    def on_progress_change(self, value):
        if self.audio:
            self.current_pos = int(float(value))
            if not self.is_playing:
                self.update_time_display()
    
    def mark_start(self):
        if self.audio:
            lyric_text = self.lyric_entry.get().strip() or f"歌词 {len(self.timestamp_manager.timestamps)//2 + 1}"
            timestamp = self.timestamp_manager.add_timestamp(self.current_pos, 'start', lyric_text)
            self.record_text.insert(tk.END, f"开始: {timestamp['formatted_time']} - {lyric_text}\n")
            self.record_text.see(tk.END)
    
    def mark_end(self):
        if self.audio:
            timestamp = self.timestamp_manager.add_timestamp(self.current_pos, 'end')
            self.record_text.insert(tk.END, f"结束: {timestamp['formatted_time']}\n\n")
            self.record_text.see(tk.END)
            self.lyric_entry.delete(0, tk.END)  # 清空歌词输入框
    
    def export_lyrics(self):
        lyrics_data = self.timestamp_manager.get_lyrics_data()
        if not lyrics_data:
            messagebox.showwarning("警告", "没有时间戳记录")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("JSON文件", "*.json")]
        )
        
        if file_path:
            try:
                import json
                with open(file_path, 'w', encoding='utf-8') as f:
                    if file_path.endswith('.json'):
                        json.dump(lyrics_data, f, ensure_ascii=False, indent=2)
                    else:
                        for lyric in lyrics_data:
                            f.write(f"{lyric['start']} - {lyric['end']}: {lyric['text']}\n")
                
                messagebox.showinfo("成功", f"歌词已导出到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {e}")
    
    def clear_timestamps(self):
        self.timestamp_manager.clear_timestamps()
        self.record_text.delete(1.0, tk.END)
    
    def update_timer(self):
        if self.is_playing and pygame.mixer.music.get_busy():
            elapsed = time.time() - self.start_time
            self.current_pos = min(int(elapsed * 1000), len(self.audio) if self.audio else 0)
            
            if self.current_pos >= len(self.audio) if self.audio else 0:
                self.is_playing = False
                self.play_btn.config(text="播放 (SPACE)")
        
        if self.audio:
            self.update_time_display()
            self.progress.set(self.current_pos)
            self.waveform.update_scan_line(self.current_pos / 1000.0)
        
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
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    player = AudioPlayer()
    player.run()