Apple 官方并未公开发布完整的 TTML 歌词标准文档，但通过社区项目和逆向分析，我们可以总结出 Apple Music 使用的 TTML 格式具有以下特点和扩展规范。这些信息主要来自 GitHub 上的 Steve-xmh 的 Apple Music Lyrics 工具项目和相关讨论。

---

📘 Apple Music TTML 格式特点（非官方但广泛验证）

✅ 基础结构遵循 W3C TTML1 标准

- 使用 <tt> 根元素，包含 <body> 和 <div>
- 每句歌词使用 <p> 标签，带 begin 和 end 时间戳
- 支持嵌套 <span> 标签用于逐字同步或角色标记

---

🎭 Apple 扩展标记（角色与行为）


| 属性/标记              | 用途说明                         |
| ---------------------- | -------------------------------- |
| ttm:role="x-bg"        | 背景人声（Background vocals）    |
| ttm:role="x-duet-a"    | 对唱角色 A（如男声）             |
| ttm:role="x-duet-b"    | 对唱角色 B（如女声）             |
| ttm:role="x-narration" | 旁白或对白                       |
| style="fade"           | 淡入淡出动画效果（用于歌词渐显） |
| xml:id="L1"            | 唯一标识符，用于歌词行编号       |

---

🧩 示例结构片段

`xml

<p xml:id="L1" begin="00:01.000" end="00:03.000">
  <span ttm:role="x-duet-a">你是否也在想我</span>
</p>
<p xml:id="L2" begin="00:03.000" end="00:05.000">
  <span ttm:role="x-duet-b">我一直在等你</span>
</p>
<span ttm:role="x-bg">
  <span begin="00:05.000" end="00:06.000">(Held)</span>
</span>
`

---

🧠 其他行为支持（根据社区工具）

- 支持逐字时间戳（每个字或词一个 <span>）
- 支持歌词行动画（如呼吸动画、辉光效果）
- 支持歌词角色定位（如副唱靠右显示）
- 支持翻译与音译结构（通过额外 <div> 或 <p>）

---

📚 参考项目与工具

- Steve-xmh/amll-ttml-tool — Apple Music-like Lyrics 编辑器
- Steve-xmh/applemusic-like-lyrics — 前端歌词展示项目
- TTML1 W3C 标准 — 官方基础规范

---

⚠️ 注意事项

- Apple 的 TTML 是其内部格式，未公开完整规范
- 社区工具通过逆向分析和抓取构建了兼容格式
- 本项目建议遵循 W3C TTML1 标准，并参考上述扩展标记
