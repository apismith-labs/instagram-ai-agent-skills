# 接口核实记录

本轮查阅时间：2026-10-28 12:14–12:17（北京时间）；上轮查询时间：2026-10-28 11:51–12:00。下文“有文档依据”只表示来源作出声明，不等于本项目实测。公开页面可能缓存，实时只读详情显示 Actor 修改时间为 2026-10-27 06:57:16 UTC；发布前重新查询。未运行 Actor，也未读取或配置凭据。

本文保留上述时点的接口核实记录；此后真实运行和平台测试的状态见 [测试状态](test-status.md)。本文中的“待测”“尚未测”描述原核实时间，不代表后续没有测试。

## Actor 输入和输出

来源：[Actor 页面及 README](https://apify.com/apple_yang/instagram-transcripts-scraper)、[输入页](https://apify.com/apple_yang/instagram-transcripts-scraper/input)，以及本轮 Apify MCP `fetch-actor-details` 返回的输入 schema 和输出推断。

- **有 schema 依据**：`videoUrl` 为 string；`bulkUrls` 为 array，schema 未声明数组元素类型，页面说明为字符串 URL 数组。`required: []` 不是空输入有效的保证。分模式提交，避免同时输入。`bulkUrls` 描述免费账户每 run 最多 5 条、付费 unlimited；这是 Actor 自述，仍受平台、时间和请求等限制，不保证可无限处理。运行表现和分批规则待验证。
- **增强解析**：本轮重新打开的页面输入表明确称 `enhancedcrawl` 默认 `true`；实时 schema 中类型为 boolean，`prefill: true`，描述普通抓取失败时增强抓取，并提及成功增强的额外计费。页面另列计费生效日期，属于时变内部证据，不写入产品配置或用户指南。`prefill` 并不单独证明 API 缺省行为；页面声明与真实执行仍须区分。产品已决定首版显式传 `enhancedcrawl: true`，避免依赖缺省值；需验证 Actor 实际接收和行为，不保证成功。
- **页面与 schema 差异**：页面示例提及可选 Instagram 会话字段，实时 schema 未列出；首版不使用，也不是开发或使用的前提。页面的其他个人主页模式不属于本 Skill。
- **输出证据**：页面声明 `url`、`code`、`pk`、`id`、`text`、`segments`、`errMsg` 等，`segments` 项含数字 `start`、`end` 和字符串 `text`。此次详情工具输出 schema 明确标注“根据近期成功运行推断”，另显示 `duration`；它不是 build/dataset schema 的声明，也不是每条实际返回保证。本轮没有取得可独立核验的 build/dataset 输出 schema，因此不声称其明确声明了这些字段。真实成功、错误、混合警告、缺字段、无身份及空 dataset 的结构待测。
- 页面称批量每 URL 一项、失败项可含 `errMsg`，但没有证明所有失败都可匹配或按输入顺序返回。run 终态成功不证明每条转录成功。

## 计费证据与差异

- 上轮 2026-10-28 11:51–12:00 本环境 `fetch-actor-details` 的原始结构字段 `actorInfo.pricing.model: "FREE"`，`userTier: "FREE"`；当时未把此当成计费保证。
- 产品审核转述 WorkBuddy 使用公开 Actor API 的 `pricingInfos` 返回 `PAY_PER_EVENT`；报告未提供查询时间或原始完整响应，本轮尝试读取 [公开 Actor API](https://api.apify.com/v2/acts/apple_yang~instagram-transcripts-scraper) 未能通过浏览工具访问，因此此条是**未独立复核的报告**，不能补造访问时间或原始字段路径。
- 本轮 2026-10-28 12:14–12:17，再次只读 `fetch-actor-details`，原始字段 `actorInfo.pricing.model: "PAY_PER_EVENT"`，`userTier: "FREE"`，`events` 包含 `result` 与 `Cost-Effective Audio-to-Text (Auto)`；[Actor 页面](https://apify.com/apple_yang/instagram-transcripts-scraper)也描述结果与音频转写计费。这些是当时的证据，不解释此前差异的原因，也不能推断未来价格。以用户自己的 Apify Console 账单为准，此差异不阻断首版开发。

## Apify MCP

[Apify MCP 官方文档](https://docs.apify.com/mcp)，本轮复核：远程 Streamable HTTP 推荐 OAuth；也提供 Bearer Token，本地 stdio 可使用 `APIFY_TOKEN`。调用和存储访问需授权。`call-actor` 接收 Actor 名和 input，`waitSecs` 0–45、默认 30，返回状态和存储 ID，不返回 dataset 数据；以 `get-actor-run` 查询同一个 run，以 `get-dataset-items` 按 dataset ID、limit/offset 读取。工具名和参数以宿主实际暴露的 schema 为准。此环境工具文档称资源读取约 256 KB 以上返回下载提示，不能推广到全部客户端；每用户每秒 30 请求为文档所述限制。客户端超时、输出截断、分页及恢复需分别实测。

提交成功响应丢失时，查询可用 run 列表或 Console 并谨慎核对；无法唯一确认就报告未知，不自动重发。记录 run ID、dataset ID 和每批状态以便继续查询；持久化可用性与数据保留取决于宿主。安全存储只保存必要信息，敏感凭据不放聊天、URL、仓库、日志或导出文件。

## 平台：官方依据与实测边界

- **Codex**：[Skill 官方文档](https://developers.openai.com/codex/skills)说明仓库从工作目录至仓库根目录扫描 `.agents/skills`，用户级位置为 `~/.agents/skills`；发行目录 `skills/` 不是自动扫描位置。文档支持通过 `$skill-installer` 从其他仓库安装，也建议可分发场景考虑插件。具体 GitHub 子目录安装、发现和触发本 Skill 尚未测。[MCP 文档](https://developers.openai.com/codex/mcp)提供 OAuth 配置；Apify 官方插件和实际工具访问需测。
- **ChatGPT**：[OpenAI Skill 文档](https://learn.chatgpt.com/docs/build-skills)和 [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)描述 Skill；后者说明符合条件的 Business、Enterprise、Healthcare、Edu 用户可在相应工作区设置下上传、创建或安装共享 Skill。[插件文档](https://help.openai.com/en/articles/20001256)说明插件可含 Skill 和连接的 app，安装不等于授权。具体账户、界面、地区与工作区可用性依产品而变。
- [OpenAI 自定义 MCP 文档](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt)当前说明 ChatGPT web 的 Business、Enterprise/Edu 自定义连接和完整 MCP、管理员及角色权限；当前 Plugins 流程与旧版 Developer mode 流程不同。[Apify ChatGPT 指南](https://docs.apify.com/integrations/chatgpt)仍描述 Developer mode，并在前提列 Token、配置步骤又选择 OAuth；须依当前 UI 和具体账号核实，不强行统一。ChatGPT 以前的连接尝试曾被阻断，原因与环境未在此核实，不能视为通过。产品本身不主动增加常规确认，但宿主权限可能要求确认，不能绕过。
- **Manus，后续平台**：[Apify Manus 集成指南](https://docs.apify.com/integrations/manus)描述首次工具调用 OAuth、失败时 Token 备选，并明确示例从含 `SKILL.md` 的 GitHub 子目录导入。[Manus 自身指南](https://help.manus.im/en/articles/14753565-how-to-share-and-use-skills-in-manus)举根目录放 Skill 的仓库例子；两者示例不同，不能推断所有版本行为一致。这些是官方文档依据，并非本项目实测；Manus、OpenClaw、Cursor 均非首版门槛。
- CSV/TXT 上传解析与 CSV/JSON/Markdown 导出均取决于宿主、权限、文件工具和真实测试；粘贴/复制是替代方式。不能从 Skill 或 MCP 支持推断端到端兼容。

## 分页证据补充（2026-10-28 12:32–12:40，北京时间）

本环境 `get-dataset-items` 工具描述列出 `items`、`itemCount`、`offset`、`limit`、`totalItemCount`；[Apify dataset API](https://docs.apify.com/api/v2/dataset-items-get) 列出分页总数、偏移、条数和限制响应头。此为文档/工具描述，并非实际运行结果，其他宿主可能不暴露或截断。完整性逻辑、无总数时的证据要求和宿主核对责任见 Skill 内的参考文档。

## 未确定事项分级

- **A 开发前产品决策**：本轮要求中的范围、默认增强、首版平台和费用体验均已确定；目前无必须先由负责人决策的问题。
- **B 开发中验证**：真实输入和默认执行行为、增强接收情况、失败与混合字段样本、可用账户限制、身份匹配、分页和宿主恢复能力。可用模拟先开发；会话字段及所有未知失败形态不阻断整个项目。
- **C 各平台宣称支持前**：独立验证该平台安装/加载、授权、实际 run、正确 transcript、恢复与文件能力；记录版本和失败原因。ChatGPT 阻断只限制 ChatGPT 声明，不阻断 Codex 开发。
