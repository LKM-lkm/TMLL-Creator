import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pydub import AudioSegment

class WaveformGenerator:
    def __init__(self, canvas_parent):
        self.canvas_parent = canvas_parent
        self.audio = None
        self.figure = None
        self.canvas = None
        self.scan_line = None
        
    def load_audio(self, file_path):
        """加载音频文件并生成波形"""
        try:
            self.audio = AudioSegment.from_file(file_path)
            self.generate_waveform()
            return True
        except Exception as e:
            print(f"加载音频失败: {e}")
            return False
    
    def generate_waveform(self):
        """生成波形图"""
        if not self.audio:
            return
        
        # 转换为numpy数组
        samples = np.array(self.audio.get_array_of_samples())
        if self.audio.channels == 2:
            samples = samples.reshape((-1, 2))
            samples = samples.mean(axis=1)  # 转为单声道
        
        # 降采样以提高性能
        downsample_factor = max(1, len(samples) // 2000)
        samples = samples[::downsample_factor]
        
        # 创建时间轴
        duration = len(self.audio) / 1000.0  # 秒
        time_axis = np.linspace(0, duration, len(samples))
        
        # 创建图形
        if self.figure:
            plt.close(self.figure)
        
        self.figure, ax = plt.subplots(figsize=(10, 3))
        ax.plot(time_axis, samples, color='blue', linewidth=0.5)
        ax.set_xlabel('时间 (秒)')
        ax.set_ylabel('振幅')
        ax.set_title('音频波形')
        ax.grid(True, alpha=0.3)
        
        # 添加扫描线
        self.scan_line = ax.axvline(x=0, color='red', linewidth=2, alpha=0.7)
        
        # 嵌入到tkinter
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        self.canvas = FigureCanvasTkAgg(self.figure, self.canvas_parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def update_scan_line(self, current_time):
        """更新扫描线位置"""
        if self.scan_line and self.audio:
            duration = len(self.audio) / 1000.0
            if 0 <= current_time <= duration:
                self.scan_line.set_xdata([current_time])
                self.canvas.draw_idle()