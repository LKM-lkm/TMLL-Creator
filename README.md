# TTML 歌词生成器

专业的歌词制作工具，支持TTML格式生成、多角色标记、时间戳标注和格式转换。

## ✨ 功能特性

- 🎵 **TTML文件生成与渲染** - 符合Apple Music标准的TTML格式
- 🎭 **多角色标记支持** - 主唱、背景、对唱等角色标记
- 🎧 **音频播放器与时间戳标注** - 集成音频播放器，支持变速不变调
- 🔄 **TTML ↔ LRC 格式转换** - 双向格式转换
- 📋 **剪贴板交互支持** - 快速导入导出
- 💾 **自动备份与文件管理** - 防止数据丢失
- 🔍 **查找替换功能** - 批量文本处理
- 🎚️ **变速播放** - 支持0.5x-2.0x变速，保持音调不变

## 🚀 快速开始

### 安装依赖

```bash
# Windows用户
install_dependencies.bat

# 或手动安装
pip install -r requirements.txt
```

### 启动应用

```bash
# GUI界面
python run_gui.py

# 或命令行版本
cd ttml_generator
python main.py
```

## 🎹 快捷键

| 键位 | 功能 |
|------|------|
| `SPACE` | 播放/暂停 |
| `F` | 标记开始时间 |
| `G` | 标记结束时间 |
| `[` / `]` | 减速/加速 |
| `Ctrl+Z` | 撤销 |
| `Ctrl+H` | 查找替换 |

## 📁 项目结构

```
ttml_generator/
├── gui/                # GUI界面
│   └── main_window.py  # 主窗口
├── templates/          # Jinja2模板
│   └── lyric_block.xml.j2
├── parser/             # 文件解析器
│   ├── ttml_parser.py  # TTML解析器
│   └── lrc_parser.py   # LRC解析器
├── convert/            # 格式转换
│   ├── lrc_to_ttml.py  # LRC转TTML
│   └── ttml_to_lrc.py  # TTML转LRC
├── clipboard/          # 剪贴板交互
├── output/             # 生成的TTML文件
├── backup/             # 自动备份
├── renderer.py         # TTML渲染器
├── file_manager.py     # 文件管理
└── utils.py           # 工具函数
```

## 🎯 使用说明

### 基本工作流程

1. **加载音频文件** - 支持MP3、WAV、FLAC、AAC、M4A、OGG格式
2. **播放音频** - 使用播放控制按钮或空格键
3. **标记时间戳** - 按F键标记开始时间，按G键标记结束时间
4. **输入歌词** - 在歌词输入框中输入对应的歌词文本
5. **设置角色** - 选择歌词角色（主唱、背景、对唱等）
6. **保存文件** - 导出为TTML或LRC格式

### 背景歌词处理

程序能够正确识别和处理嵌套的背景歌词：

```xml
<p begin="00:29.800" end="00:34.230" ttm:agent="v1" itunes:key="L7">
  Anytime<span ttm:role="x-bg" begin="00:29.800" end="00:34.230">(Anytime you need a friend)</span>
</p>
```

导入时会自动分离为：
- 主歌词：`Anytime`
- 背景歌词：`(Anytime you need a friend)` (角色：x-bg)

### 变速播放

- 支持0.5x到2.0x变速播放
- 使用librosa实现变速不变调（需安装librosa）
- 降级使用pydub的speedup方法

## 📦 依赖项

### 核心依赖
- `tkinter` - GUI界面
- `pygame` - 音频播放
- `pydub` - 音频处理
- `jinja2` - 模板渲染

### 可选依赖
- `librosa` - 高质量变速不变调
- `soundfile` - 音频文件读写
- `ffmpeg` - 多格式音频支持

## 🔧 安装说明

### Windows

1. 克隆仓库：
```bash
git clone https://github.com/your-username/ttml-generator.git
cd ttml-generator
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 安装FFmpeg（可选，用于多格式音频支持）：
```bash
python install_ffmpeg_minimal.py
```

### 手动安装FFmpeg

如果自动安装失败，可以手动安装：
1. 下载FFmpeg：https://ffmpeg.org/download.html
2. 解压到项目目录的`ffmpeg/bin/`文件夹
3. 或添加到系统PATH环境变量

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [librosa](https://librosa.org/) - 音频分析库
- [pydub](https://github.com/jiaaro/pydub) - 音频处理库
- [pygame](https://www.pygame.org/) - 音频播放支持
- [Jinja2](https://jinja.palletsprojects.com/) - 模板引擎

## 📞 支持

如果您遇到问题或有建议，请：
- 提交 [Issue](https://github.com/your-username/ttml-generator/issues)
- 发送邮件至：[](mailto:lkm836972@outlook.com)

---

⭐ 如果这个项目对您有帮助，请给个星标！
