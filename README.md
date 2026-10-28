# Instagram AI Agent Skills

面向内容创作者、运营、营销人员和研究者的 Instagram 数据工作流。项目计划逐步扩展内容研究、Reels 分析、竞品监测、Creator 和评论分析；这些方向目前尚未提供。

## Instagram Transcript Extractor

本仓库已实现首个 Skill 的指令和随附的离线处理工具：提供公开 Instagram 视频或 Reel 链接，获取转录；也可以要求摘要、翻译或基于文字的简单分析。单条和多条链接均在设计范围内。转录可能不完整或无法取得。

**状态：**手动加载项目工作流后，单条和批量 Actor 与 dataset 数据处理链路已真实运行成功。另一次最新单条端到端会话获得了 transcript，读取了工作流参考并执行了准备脚本；轨迹没有记录 `next_action` 和 `reconcile` 的执行，是否执行无法确认，不能认定完整工作流通过。该次提交使用 `enhancedcrawl: true`，Actor 内部是否实际触发增强解析尚未验证。项目级 Skill 已被 Codex 原生发现接口识别；Codex 曾报告显式触发和自然语言请求测试完成，但最新会话缺少独立宿主激活证据，无法确认自动触发。GitHub 安装、ChatGPT、真实多页 dataset、跨会话恢复、文件上传和导出均未验证。详见 [测试状态](docs/test-status.md)。

### Codex：安装与连接分开进行

仓库 `skills/instagram-transcript-extractor/` 是唯一维护和分发源；`.agents/skills/instagram-transcript-extractor/` 是供 Codex 项目级发现的完整副本。两处是独立文件，不会自动同步。维护者修改源目录后，应检查副本是否已有独立改动，再同步三个文件；提交前运行下方离线一致性测试。保留完整副本让项目级使用无需符号链接；其他 Agent 的发现方式须分别验证。

从 GitHub 安装尚未验证。发布后可尝试在 Codex 中使用 `$skill-installer` 从仓库的 `skills/instagram-transcript-extractor` 安装整个目录，包括脚本和参考文件；具体安装、发现和触发流程仍需实测。不要将现有项目级发现结果当作 GitHub 安装验证。

另外在 Codex 的 Plugins 中安装并连接 Apify 官方插件，优先使用浏览器授权；可按 [Apify 的 Codex 安装说明](https://docs.apify.com/integrations/codex-app) 操作。也可使用宿主支持的官方 MCP 连接。安装 Skill 不会自动完成账户连接。如果需要备选方式，在宿主提供的私密设置中配置，不要把凭据发到聊天。首次使用可在 [Apify Console](https://console.apify.com/) 查看 Runs 和计费明细，也可查看 [Actor 页面](https://apify.com/apple_yang/instagram-transcripts-scraper)。随后把链接和希望得到的内容告诉 Codex。

### ChatGPT

Skill 或插件的安装、Apify 连接、账户授权、Actor 调用和结果验证均未通过本项目实测；此前 MCP 连接尝试被阻断，具体原因尚未确认。可用性取决于账户、套餐、工作区及权限；不要将 Codex 结果视为 ChatGPT 验证。相关官方资料与待测项见 [接口核实记录](docs/interface-verification.md)。

## 开发验证

需要 Python 3；离线辅助脚本和测试只使用 Python 标准库，不需要安装第三方 Python 包。运行 `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` 做离线测试，其中包含源目录与项目级副本的一致性检查；这些测试不能替代真实 Agent、MCP、Actor 或平台安装测试。设计和验收标准在 [docs](docs/) 中。未对其他平台宣称兼容。
