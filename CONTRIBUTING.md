# 贡献指南

感谢您对TTML歌词生成器项目的关注！我们欢迎各种形式的贡献。

## 🤝 如何贡献

### 报告问题
- 使用 [GitHub Issues](https://github.com/your-username/ttml-generator/issues) 报告bug
- 提供详细的问题描述和复现步骤
- 包含系统信息（操作系统、Python版本等）

### 提交功能请求
- 在Issues中描述您希望的新功能
- 解释功能的用途和价值
- 提供具体的使用场景

### 代码贡献

#### 开发环境设置
1. Fork 项目到您的GitHub账户
2. 克隆您的fork：
```bash
git clone https://github.com/your-username/ttml-generator.git
cd ttml-generator
```

3. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

4. 安装依赖：
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 开发依赖
```

#### 开发流程
1. 创建功能分支：
```bash
git checkout -b feature/your-feature-name
```

2. 进行开发并测试
3. 提交更改：
```bash
git add .
git commit -m "feat: add your feature description"
```

4. 推送到您的fork：
```bash
git push origin feature/your-feature-name
```

5. 创建Pull Request

## 📝 代码规范

### Python代码风格
- 遵循 PEP 8 代码风格
- 使用有意义的变量和函数名
- 添加适当的注释和文档字符串
- 保持函数简洁，单一职责

### 提交信息规范
使用约定式提交格式：
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

类型：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat(audio): add variable speed playback with pitch preservation

- Implement librosa-based time stretching
- Add fallback to pydub speedup method
- Support 0.5x to 2.0x speed range
```

## 🧪 测试

### 运行测试
```bash
python -m pytest tests/
```

### 添加测试
- 为新功能添加单元测试
- 确保测试覆盖率不降低
- 测试文件放在 `tests/` 目录下

## 📚 文档

### 更新文档
- 更新README.md中的功能描述
- 添加新功能的使用说明
- 更新CHANGELOG.md

### 代码文档
- 为公共API添加文档字符串
- 使用清晰的注释解释复杂逻辑
- 保持文档与代码同步

## 🏗️ 项目架构

### 核心模块
- `gui/` - 图形用户界面
- `parser/` - 文件解析器
- `convert/` - 格式转换器
- `templates/` - TTML模板
- `clipboard/` - 剪贴板交互

### 设计原则
- 模块化设计，低耦合高内聚
- 单一职责原则
- 开放封闭原则
- 依赖注入

## 🐛 调试指南

### 常见问题
1. **音频播放问题** - 检查pygame和音频驱动
2. **FFmpeg相关** - 确保FFmpeg正确安装
3. **编码问题** - 确保文件使用UTF-8编码

### 调试工具
- 使用Python调试器 `pdb`
- 添加日志输出
- 使用IDE断点调试

## 📋 Pull Request检查清单

提交PR前请确认：
- [ ] 代码遵循项目风格规范
- [ ] 添加了必要的测试
- [ ] 测试全部通过
- [ ] 更新了相关文档
- [ ] 提交信息清晰明确
- [ ] 没有引入不必要的依赖

## 🎯 优先级任务

当前需要帮助的领域：
- 🌐 国际化支持
- 🎨 UI/UX改进
- 📱 跨平台兼容性
- 🔊 更多音频格式支持
- 📖 文档翻译

## 💬 交流讨论

- GitHub Issues - 问题报告和功能讨论
- GitHub Discussions - 一般性讨论
- Email - 私人联系

## 🙏 致谢

感谢所有贡献者的努力！您的贡献让这个项目变得更好。

---

再次感谢您的贡献！🎉