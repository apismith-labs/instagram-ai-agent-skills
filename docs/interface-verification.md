# 接口核实记录

本轮查阅时间：2026-10-28 12:14–12:17（北京时间）；上轮查询时间：2026-10-28 11:51–12:00。下文“有文档依据”只表示来源作出声明，不等于本项目实测。公开页面可能缓存，实时只读详情显示 Actor 修改时间为 2026-10-27 06:57:16 UTC；发布前重新查询。未运行 Actor，也未读取或配置凭据。

本文保留上述时点的接口核实记录；此后真实运行和平台测试的状态见 [测试状态](test-status.md)。本文中的“待测”“尚未测”描述原核实时间，不代表后续没有测试。

## OpenClaw 单账号运行报告（用户提供，2026-11-07）

以下是项目负责人提供的历史运行报告摘要，不是本轮独立取证：OpenClaw `2026.11.1 (4ffdd20)`、Apify 插件 `0.5.3`；对 `danmartell` 执行一次 Weekly Review（滚动 7 天，`Asia/Shanghai`）。报告自述 Profile Posts Actor `apple_yang~instagram-post-scraper` 的 run `C0OB4aJz8N6MpcQVW` 状态为 `SUCCEEDED`，输入包含该用户名、`resultsLimit=3`、`onlyPostsNewerThan="7 days"`、`skipPinnedPosts=true`，返回 3 行；helper 选中 1 条、因每作者上限省略 2 条，并报告 coverage 为 `partial`。报告还自述 Transcript Actor `apple_yang~instagram-transcripts-scraper` 的 run `8azQtSUezQSNKC3I0` 状态为 `SUCCEEDED`，对所选帖子执行转录并返回 1 行，helper 按 URL/code 匹配成功。

WorkBuddy 复审指出，以上 run 状态、输入/返回行数、coverage、helper 输出及调用过程没有原始 start/collect JSON、会话 trace 或原始 helper 输入输出可供独立核对；当时 helper 版本/安装副本哈希也未记录。因此它们仍是用户报告，不能说成独立复现。当前 helper 对形状相同但 `retrieval_complete=true` 且无 evidence 的输入会将完整性判为 `unknown`；不能声称当前代码复现了历史报告中的 `partial`。报告提及的两次 discover 属于此前预检，不计入上述两个 Actor run。实际费用未查，未设置 run 级费用上限；报告称本次未观察到 `[…truncated]`，但这不是完整性证据。WorkBuddy 对本机安装的 Apify 插件 `0.5.3` 源码作了只读核验，并报告：`apify-client.ts` 定义 `MAX_RESULT_CHARS = 50_000` 且超限时截断文本；`apify-scraper-tool.ts` 的 `collect` 调用 Dataset `listItems()` 时未传分页参数。Codex 本轮未独立复查该源码；这些事实仅归属于 WorkBuddy 核验的本机插件版本，不能推广到其他宿主或未来版本。未观察到截断标记不排除截断风险。

这次仅是一条单账号、小样本的用户运行报告；当时 helper 版本未记录。它不证明该账号整周已完整扫描，也不验证排序、媒体枚举、分页、费用、批量、多账号或 Daily Scan。helper 的 transcript URL/code 匹配成功仅表示该返回行与提交帖子匹配，不表示发现 Dataset 完整。

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

[Apify MCP 官方 README（2026-11-06 只读核对）](https://github.com/apify/apify-mcp-server)描述 `call-actor` 参数 `actor`、`input`、`waitSecs` 与独立 `callOptions`；费用限制通过 `callOptions` 中的 `maxItems`（按结果计费）或 `maxTotalChargeUsd`（按事件计费）设置。`waitSecs` 是等待响应时长，不能限制 Actor 执行时长或费用。这些属于公开 MCP 文档，不证明当前 Codex 会话实际暴露相同 schema。

针对 `get-actor-run-list`，需区分工具输入、声明输出 schema 与实际响应体。[Apify MCP v0.16.0 发布说明（2026-09-17）](https://github.com/apify/apify-mcp-server/releases/tag/v0.16.0)显示该 tag 指向发布提交 `5e58ef3`，并列出新增 `actorId` 过滤器的功能提交 [`5264fe6`](https://github.com/apify/apify-mcp-server/commit/5264fe6)；官方 [issue #1351](https://github.com/apify/apify-mcp-server/issues/1351) 也记录了对应过滤器合并。**本次只读核验（2026-11-06）**能读取[当前 master 的 `get_actor_run_list.ts`](https://github.com/apify/apify-mcp-server/blob/master/src/tools/runs/get_actor_run_list.ts)：输入定义为非空字符串 `.optional()` 的 `actorId`，handler 用它选择按 Actor 过滤的 run-list 请求。它确认的是输入过滤能力。此前较早检查未能读取 tag 源文件；WorkBuddy 于 2026-11-06 的最新复审报告称 v0.16.0 tag 源码也已可读并含可选 `actorId`，但本次浏览器对 tag/commit 源文件链接仍返回 cache miss，因此 tag 源码这一点保留为 WorkBuddy 复核结论，而非本轮直接读取。**这些公开源码均不能证明目标部署版本或宿主 live schema 暴露该参数。** `actorId` 是输入过滤条件，不是 run 输出字段，也不表示输出含 `options`。公开声明输出 schema 未声明 `options`。handler 把 `apifyClient.runs().list(...)` 结果写入 JSON 文本并传入 `structuredContent`；这可能保留上游对象中的额外字段，但没有证据证明真实上游对象含 `options`，也没有证据证明目标 MCP 宿主会把 schema 外字段暴露给模型。

[`get-actor-run` 实现](https://github.com/apify/apify-mcp-server/blob/master/src/tools/runs/get_actor_run.ts)通过 run-response builder 构造许可字段的响应对象，再将该对象 JSON 序列化；[run response builder](https://github.com/apify/apify-mcp-server/blob/master/src/tools/actors/actor_run_response.ts)和输出 schema 均未包含 run `options`。所以该工具的当前公开实现不会把 API 原始对象中的 options 透传到响应。公开仓库 `master` 源码也不能替代目标部署版本证据：README 说明托管服务基于单独的私有仓库。

**Codex live tool inventory 历史观察（2026-11-06）：** 当时该会话目录未暴露 `call-actor`、`get-actor-run-list`、`get-actor-run` 或其他 Apify 工具；没有检查插件设置/缓存，也未实际调用工具。该观察只描述该次会话的工具目录，不能推广为其他 Codex 会话或部署。当前 v0.8 不要求 run 费用参数透传或 run-options readback，因此这两项不是本 Skill 的实现阻塞或发布前置条件；目标宿主是否能执行所需 Actor、是否具备授权及其实际输入/输出合同仍须在真实功能验证时核对。

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

## Creator Reels Insights 实现复核（2026-11-06，更新）

本次为只读公开资料与当前宿主工具目录核验；没有调用 Actor、登录 Apify、读取凭据或执行真实 run。公开页面可能滞后于账户实际运行限制，正式接入和真实验证前须再读取目标账户可见的 live schema 与所选宿主工具合同。

- **Profile Posts Actor 输入与输出 schema：** [公开 OpenAPI](https://apify.com/apple_yang/instagram-post-scraper/api/openapi) 列出必需输入 `usernames`（string array）、`resultsLimit`（integer）及可选 `onlyPostsNewerThan`；该时间过滤说明使用 UTC。[独立公开 Output schema 页面](https://apify.com/apple_yang/instagram-post-scraper/output-schema) 当前列出必需输出字段 `url`（string）、`shortCode`（string）、`pk`（string）、`type`（string）、`timestamp`（integer）和 `ownerUsername`（string）等。因此这些是可追溯的公开文档字段名，但仍需目标账户的 live schema 和真实返回样本确认运行时类型/完整性。页面未给出 `type` 的枚举值，不能据此确定视频/非视频类型值或默认筛选规则。`resultsLimit` 说明仅为“maximum number of results to return”；没有说明单用户名时是否按最新优先、是否把图片等非视频行计入上限，也没有说明多用户名时是总量或逐作者上限。当前不能声称每作者上限或完整时间窗覆盖已受控。
- **Transcript Actor 输入：** [公开 Actor 页面](https://apify.com/apple_yang/instagram-transcripts-scraper) 与 [OpenAPI](https://apify.com/apple_yang/instagram-transcripts-scraper/api/openapi) 当前列出 `videoUrl`、`bulkUrls`（array of strings）、`enhancedcrawl`（boolean）及另一种 `usernames` profile 模式。页面描述 `bulkUrls` 支持多 URL，但条数仍受实时账户/Actor 条件影响；不把旧的套餐数字或费用说明写为稳定实现常量。
- **Transcript Actor 输入/输出 schema：** [公开 OpenAPI](https://apify.com/apple_yang/instagram-transcripts-scraper/api/openapi) 当前列出 `videoUrl`、`bulkUrls`（string array）、`enhancedcrawl` 和 profile 输入；`bulkUrls` 描述有免费/付费账户差异，须以目标账户实时限制为准。其[公开 Output schema](https://apify.com/apple_yang/instagram-transcripts-scraper/output-schema) 列出 `url`、`pk`、`id`、`videoUrl`、`audioUrl` 为必需字段，`code`、`createTime`、`userName`、`text`、`segments`、`errMsg`、`timestamp` 等为可选字段。该文档不保证每种运行结果都含所有可选字段；仍需真实样本确认 `pk` 与 Profile Posts `pk` 可跨 Actor 可靠对账。当前 helper 会要求两端合同同时存在且 ID kind 一致；未知或缺失时返回 `interface_error`。
- **媒体类型值和状态：** Profile Posts Output schema 只规定 `type` 为 string，没有枚举。未知类型值对应行级状态 `unknown_media_type`；作者/URL 行级输入不匹配为 `interface_error`。发现 bundle 的 `retrieval_complete` 为三态；helper 仅校验 evidence 对象结构和非空 `source`/`detail` 字符串，不验证来源真实性或描述真伪。只有调用方持有真实、可追溯的宿主/Actor 完整性证据时才可设为 true；当前 OpenClaw Apify 插件没有向 Skill 提供已验证的分页/完整性信号。run `SUCCEEDED`、返回数低于 `resultsLimit`、空结果或未见截断标记都不能证明完整。缺失/未知信号使覆盖为 unknown，并保留已验证候选；触顶仍是 possible cap/partial。失败 run 记录在 `run_failures`；成功但检索不完整/未知只反映在覆盖字段，不记为 Actor 失败。有行级选择错误时 helper 顶层状态为 `partial_interface_error`；身份冲突导致 partial 覆盖，无法归属的行导致 overall coverage unknown，但不无差别降低其他作者。顶层 `complete` 只依据显式完整性证据和本地检查，不超出该证据能支持的范围。缺少 schema/合同导致的 helper contract exception 则通过 CLI 非零退出和 `error` 字段报告。
- **结果限制与排序：** 公开输入 schema 对 `resultsLimit` 只写最大返回结果数。helper 的 select 输入为每次 Profile Posts run 一个 bundle（run ID、该次提交用户名、该次实际 `resultsLimit`、完整原始返回行、读取完整性信号）。它在时间窗筛选前按每个 run 的原始返回行数分别比较该 run 的上限；不同 run 不会合计。run 边界/上限/用户名映射缺失时返回顶层 `partial_interface_error` 和 `coverage_status: unknown`，不报完整。一个 run 包含多用户名且上限作用范围未核实时，输出 `unknown_multi_username_limit_scope` 或 `possible_results_limit_reached_scope_unknown`，不按作者拆分推断。单 run 行数达到上限只说明可能触顶。Actor 的真实单/多用户名计数语义、最新优先顺序、图片/非视频计入规则和完整性信号仍未核实；这些离线测试仅验证本地逻辑，不验证 Actor 行为。
- **运行费用参数（范围说明，2026-11-06）：** 公开 Apify MCP 与 API 文档存在运行费用选项的描述，见上文来源；这些信息不表示本 Skill 实现了参数透传或费用封顶。当前产品版本不要求报告总预算、run 级预算分配、`callOptions.maxTotalChargeUsd`、`maxItems` 或选项读回；相关预算规划/验证操作已从第二 Skill helper 和 CLI 移除。实际使用量按用户的 Apify 账户及 Actor 计费规则产生，不作固定费用或费用上限声明。
- **Profile Posts 待验证事项：** `resultsLimit` 对单/多用户名的实际语义、最新优先排序、图片/非视频计入规则、完整 media type 枚举和完整性信号仍无充分证据。候选行数达到传入 `resultsLimit` 时 helper 只标记“可能触及结果限制/额外候选未知”，不断言已截断或完整。没有已核验媒体值/字段合同仍 fail closed；离线 `select` 通过不代表真实 Profile Posts 数据可用，也不能报告完整扫描或“没有新视频”。
- **执行状态：** URL/作者/稳定 ID 冲突对账、顶层选择状态、可能触及结果限制分类、窗口筛选、候选去重、转录批次拆分、transcript reconciliation 及 stdin JSON 入口已有离线实现。helper 的每作者数量设置只限制本地候选选择，不是 Actor `resultsLimit` 或费用上限。存在一条用户提供的第二 Skill 单账号真实运行报告，但原始 run 输出未独立核实；因此该报告不等于全面集成验证。离线测试不证明 Actor 输出、真实批次限制或宿主集成。Profile Posts 的媒体类型值、排序、结果限制语义与完整性仍待验证；全面集成验证未完成，不能据此标为已完成或可发布。
