# 项目文件结构

## 📁 完整目录结构

```
TMLL Creator/
├── 📁 ttml_generator/              # 核心代码包
│   ├── 📁 audio_player/            # 音频播放器模块
│   │   ├── player_gui.py           # 播放器GUI组件
│   │   ├── timestamp_manager.py    # 时间戳管理器
│   │   └── waveform.py            # 波形显示组件
│   ├── 📁 backup/                  # 备份目录
│   ├── 📁 clipboard/               # 剪贴板交互模块
│   │   └── clipboard_manager.py    # 剪贴板管理器
│   ├── 📁 convert/                 # 格式转换模块
│   │   ├── lrc_to_ttml.py         # LRC转TTML转换器
│   │   └── ttml_to_lrc.py         # TTML转LRC转换器
│   ├── 📁 gui/                     # 图形用户界面
│   │   └── main_window.py         # 主窗口界面
│   ├── 📁 output/                  # 输出目录
│   ├── 📁 parser/                  # 文件解析器模块
│   │   ├── lrc_parser.py          # LRC文件解析器
│   │   └── ttml_parser.py         # TTML文件解析器
│   ├── 📁 renderer/                # 渲染器目录
│   ├── 📁 templates/               # 模板文件
│   │   └── lyric_block.xml.j2     # TTML模板
│   ├── __init__.py                # 包初始化文件
│   ├── file_manager.py            # 文件管理器
│   ├── main.py                    # 命令行入口
│   ├── renderer.py                # TTML渲染器
│   └── utils.py                   # 工具函数
├── 📁 backup/                      # 全局备份目录
│   ├── example_20250808_125014.ttml
│   └── test_20250808_125154.ttml
├── 📁 output/                      # 全局输出目录
│   ├── example.ttml
│   └── test.ttml
├── .gitignore                     # Git忽略文件
├── CHANGELOG.md                   # 更新日志
├── CONTRIBUTING.md                # 贡献指南
├── LICENSE                        # 开源许可证
├── README.md                      # 项目说明文档
├── requirements.txt               # 项目依赖
├── requirements-dev.txt           # 开发依赖
├── setup.py                       # 包安装配置
├── run_gui.py                     # GUI启动脚本
├── install_dependencies.py       # 依赖安装脚本
├── check_ffmpeg.py               # FFmpeg检查脚本
├── test_ttml.py                  # 测试脚本
├── 项目文档.md                    # 中文项目文档
└── TTML标准.md                    # TTML标准说明
```

## 🗂️ 文件分类

### 核心代码文件
- `ttml_generator/` - 主要代码包
- `run_gui.py` - GUI启动入口
- `setup.py` - 包安装配置

### 文档文件
- `README.md` - 项目主文档
- `CHANGELOG.md` - 更新日志
- `CONTRIBUTING.md` - 贡献指南
- `LICENSE` - 开源许可证
- `项目文档.md` - 中文文档
- `TTML标准.md` - 技术标准
- `PROJECT_STRUCTURE.md` - 本文件

### 配置文件
- `requirements.txt` - 运行依赖
- `requirements-dev.txt` - 开发依赖
- `.gitignore` - Git忽略配置

### 工具脚本
- `install_dependencies.py` - 依赖安装
- `check_ffmpeg.py` - FFmpeg检查
- `test_ttml.py` - 测试脚本

### 数据目录
- `backup/` - 备份文件
- `output/` - 输出文件

## 🧹 文件整理建议

### 需要保留的文件
✅ 所有核心代码文件
✅ 所有文档文件
✅ 配置文件
✅ 工具脚本

### 可以清理的文件
🗑️ `backup/` 中的测试文件（可选）
🗑️ `output/` 中的示例文件（可选）
🗑️ 临时文件和缓存文件

### 建议的目录结构优化
```
TMLL Creator/
├── 📁 src/ttml_generator/          # 重命名为src结构
├── 📁 docs/                        # 文档目录
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── CONTRIBUTING.md
│   ├── 项目文档.md
│   └── TTML标准.md
├── 📁 scripts/                     # 脚本目录
│   ├── install_dependencies.py
│   ├── check_ffmpeg.py
│   └── run_gui.py
├── 📁 tests/                       # 测试目录
│   └── test_ttml.py
├── 📁 examples/                    # 示例目录
├── .gitignore
├── LICENSE
├── requirements.txt
├── requirements-dev.txt
└── setup.py
```

## 📊 文件统计

- **总文件数**: ~30个文件
- **代码文件**: ~15个
- **文档文件**: ~6个
- **配置文件**: ~5个
- **工具脚本**: ~4个

## 🎯 开源准备状态

- ✅ 代码完整性 - 100%
- ✅ 文档完整性 - 100%
- ✅ 配置完整性 - 100%
- ✅ 许可证 - MIT
- ✅ 贡献指南 - 完整
- ✅ 更新日志 - 详细

项目已完全准备好开源发布！🚀