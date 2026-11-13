# 接口核实记录

本轮查阅时间：2026-10-28 12:14–12:17（北京时间）；上轮查询时间：2026-10-28 11:51–12:00。下文“有文档依据”只表示来源作出声明，不等于本项目实测。公开页面可能缓存，实时只读详情显示 Actor 修改时间为 2026-10-27 06:57:16 UTC；发布前重新查询。未运行 Actor，也未读取或配置凭据。

本文保留上述时点的接口核实记录；此后真实运行和平台测试的状态见 [测试状态](test-status.md)。本文中的“待测”“尚未测”描述原核实时间，不代表后续没有测试。

## OpenClaw 单账号运行报告（用户提供，2026-11-07）

以下是项目负责人提供的历史运行报告摘要，不是本轮独立取证：OpenClaw `2026.11.1 (4ffdd20)`、Apify 插件 `0.5.3`；对 `danmartell` 执行一次 Weekly Review（滚动 7 天，`Asia/Shanghai`）。报告自述 Profile Posts Actor `apple_yang~instagram-post-scraper` 的 run `C0OB4aJz8N6MpcQVW` 状态为 `SUCCEEDED`，输入包含该用户名、`resultsLimit=3`、`onlyPostsNewerThan="7 days"`、`skipPinnedPosts=true`，返回 3 行；helper 选中 1 条、因每作者上限省略 2 条，并报告 coverage 为 `partial`。报告还自述 Transcript Actor `apple_yang~instagram-transcripts-scraper` 的 run `8azQtSUezQSNKC3I0` 状态为 `SUCCEEDED`，对所选帖子执行转录并返回 1 行，helper 按 URL/code 匹配成功。

WorkBuddy 复审指出，以上 run 状态、输入/返回行数、coverage、helper 输出及调用过程没有原始 start/collect JSON、会话 trace 或原始 helper 输入输出可供独立核对；当时 helper 版本/安装副本哈希也未记录。因此它们仍是用户报告，不能说成独立复现。当前 helper 对形状相同但 `retrieval_complete=true` 且无 evidence 的输入会将完整性判为 `unknown`；不能声称当前代码复现了历史报告中的 `partial`。报告提及的两次 discover 属于此前预检，不计入上述两个 Actor run。实际费用未查，未设置 run 级费用上限；报告称本次未观察到 `[…truncated]`，但这不是完整性证据。WorkBuddy 对本机安装的 Apify 插件 `0.5.3` 源码作了只读核验，并报告：`apify-client.ts` 定义 `MAX_RESULT_CHARS = 50_000` 且超限时截断文本；`apify-scraper-tool.ts` 的 `collect` 调用 Dataset `listItems()` 时未传分页参数。Codex 本轮未独立复查该源码；这些事实仅归属于 WorkBuddy 核验的本机插件版本，不能推广到其他宿主或未来版本。未观察到截断标记不排除截断风险。

这次仅是一条单账号、小样本的用户运行报告；当时 helper 版本未记录。它不证明该账号整周已完整扫描，也不验证排序、媒体枚举、分页、费用、批量、多账号或 Daily Scan。helper 的 transcript URL/code 匹配成功仅表示该返回行与提交帖子匹配，不表示发现 Dataset 完整。

## OpenClaw 第二轮单账号运行观察（用户提供，2026-11-08）

以下内容来自用户提供的 OpenClaw 执行报告，不是 Codex 本轮独立取证。报告称 OpenClaw Agent 可见并调用已同步的 Creator Reels Insights Skill；安装 helper SHA-256 为 `ad9f31aeb9fc615d2d37f756a06e03e6029cbdb878d8e56d48963343a26f2e49`，报告称该值与此前同步核验报告一致。该运行环境中的 Git 历史无法确认；这不是“仓库没有 commit”的证据。Codex 本轮没有独立读取原始 `start`/`collect` JSON、会话 trace 或安装副本来复核上述报告与哈希。

报告描述一次 `danmartell` 的 Weekly Review，每作者处理上限为 1，锚点 `2026-11-08T10:08:00+08:00`，helper 半开 UTC 窗口为 `[2026-11-01T02:08:00Z, 2026-11-08T02:08:00Z)`。Profile Posts Actor `apple_yang~instagram-post-scraper` 的输入为 `usernames=["danmartell"]`、`resultsLimit=5`、`onlyPostsNewerThan="7 days"`、`skipPinnedPosts=true`。报告自述 run `gYklaQSlVA0qn7OwE`（Dataset `hhtAeFy11P3lpluRR`）为 `SUCCEEDED`，`resultCount=5`，一次 collect 即返回；5 行均在窗口内，其中 1 条 `Album`、4 条 `Video`。helper 据报选出最新 1 条视频，另 3 条视频因本地每作者上限未选；原始 5 行等于 `resultsLimit=5`，helper 据报标记 `possible_results_limit_reached=true`。这只是可能触顶信号，不证明结果已截断，也不证明覆盖完整。

报告自述未提供可信的 `retrieval_complete` 证据，因此为 `null`，整体状态为 `partial`、覆盖为 `unknown`；没有 Dataset 完整性证据，因此不能声称该账号在窗口内已完整发现。`skipPinnedPosts=true` 的实际效果没有置顶标记或对照运行支持，仍未验证。此次同时改变了请求上限和 `skipPinnedPosts` 输入；报告不证明其中任何一项导致候选数量变化。

报告还描述 Transcript Actor `apple_yang~instagram-transcripts-scraper` 对唯一选中 URL `https://www.instagram.com/p/DfdGTWpCTr6/` 执行处理。run `EkXH9zbOjYdyttYl7`（Dataset `GuhGoQhF7fORQTqva`）据报状态为 `SUCCEEDED`、`resultCount=1`；两次 collect 中第一次状态为 `RUNNING`，第二次为 `SUCCEEDED`。报告称返回行的 `text` 非空、含 17 个 `segments`、`errMsg=""`。helper `reconcile` 据报返回 `success`，`dataset_complete=null`、`run_status=SUCCEEDED`，未传 `run_error`；报告描述返回行的 URL 与 `code`/`shortCode` 和提交候选一致。没有原始 helper 输出可独立确认实际匹配键，因此不声称 helper 分别用 URL 与 code 两项完成匹配。`reconcile: success` 只表示该 transcript 返回行与提交候选成功对账，不证明 Transcript Dataset 完整。

这条报告只支持“一个账号、一次 Profile Posts run、一个候选视频、一次 Transcript run 的正向链路被报告为成功”。两个 Dataset 均无可信完整性证据，费用未查；它不是全面集成验证，也不证明可发布。仍未验证 Profile Posts 的完整 Dataset 覆盖、`resultsLimit` 排序和计数语义、完整媒体类型枚举、`skipPinnedPosts` 效果、多账号行为及实际费用。

## WorkBuddy OpenClaw 插件读取语义审计（只读，2026-11-11）

WorkBuddy 的只读审计记录：OpenClaw Apify 插件的 `allDone` 表示没有仍在运行的 Run；`resultCount` 表示单次 `listItems` 响应返回的条数，插件会丢弃 total。因此，不能仅凭 `allDone` 或 `resultCount` 断言 Dataset 已完整读取。Creator 报告中的 `dataset_complete=null` 符合 helper 契约，表示完整性未知；也不能据此确认时间窗已完整覆盖。该审计结论不把运行终止状态等同于结果读取完整性。

同一审计在 2026-11-11 的 OpenClaw Instagram 测试记录中未发现 REST 旁路；证据只支持“未发现旁路”，不能证明绝无旁路。另有 2026-11-02 的历史轨迹曾包含直接 REST 查询；那是不同日期的历史观察，不应与 2026-11-11 测试混为一谈。

## Creator OpenClaw Dataset 兼容性与后续受控运行（用户提供事实，2026-11-13）

原版 OpenClaw Apify 插件 v0.5.3 的 `collect` 会序列化 Dataset 输出并截在 50,000 字符，且未提供分页参数或结构化截断标志。该版本的 `resultCount` 表示读入插件内存的行数，不表示模型实际可见且可解析的行数。应分别记录 Dataset 总行数、插件/工具读到的行数、模型可见且传给 helper 的解析行数；不能将这些计数互换。

隔离插件副本另有分页实现，返回 `datasetTotal`、`pageCount`、`returnedItems`、`truncated`、`hasMore`、`nextOffset`、`nextOffsetKind` 等字段。用户报告该副本实际分页读取 24/24，测试模型未发生二次截断；隔离副本不是正式安装的 v0.5.3，不能据此宣称原版支持分页，也不应将临时副本作为普通用户安装路径。

同一批用户提供的 OpenClaw 受控运行事实称：5 个历史 Transcript Run 与单 URL Run `U4pAuOCOKbbqvDXTf` 最终按 URL/PK 对账 6/6 `success`；新 Run 的输入含一个 `bulkUrls` 和 `enhancedcrawl: true`，Dataset 读取 1/1。Discovery 状态仍是 `partial_interface_error`、总体 `coverage_status=unknown`，因此 6/6 transcript 对账成功不能表述为 Discovery 时间窗完整覆盖。Codex 本轮未查询 Apify、未复跑 Actor；以上作为用户提供的运行事实记录。

## OpenClaw Transcript Extractor 运行记录核对（WorkBuddy 只读审计，2026-11-11）

对应报告 Run `N5jrbwOYW56bSCQz5` 的正向转录成功记录与另一次意外启动的 Run `4UJ2EpdzDnlpVHmU3` 是两条不同观察。后者的状态、结果数和费用无法核实。重复启动是测试操作失误，不是 Skill 自动重试；不得据此补写后者的运行结果或费用。

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
- **媒体类型值和状态：** Profile Posts Output schema 只规定 `type` 为 string，没有枚举。非精确 `"Video"` 的窗口内类型值对应行级状态 `unknown_media_type`，包含字段名、`field_present` 和实际 `value`；字符串未知值为 `field_present: true`，缺失字段为 `false`，null/非字符串值保留实际值。未知类型本身不增加 `row_interface_error_count`，也不单独导致 `partial_interface_error`；报告仍披露未知值。确认的 `"Video"` 行没有可用 URL、作者身份/结构无法验证等才计为接口错误。Creator 汇总中的 `unknown_media_type` 计数窗口内可归属的未知类型原始行，包括重复项且不要求 URL 可用；`discovered_returned_in_window` 计数窗口内可归属且 URL 可用的原始行，包括重复项并不限于媒体类型；`type_video_candidates` 统计去重后、URL 可用且 `type == "Video"` 精确匹配的候选数，在应用 `per_creator_limit` 前计算。发现 bundle 的 `retrieval_complete` 为三态；当前 helper 要求非空 `source`/`detail`，检查规范化证据字段类型及各计数与实际传入 `posts` 行数的一致性，并仅在 JSON 完整且总行数匹配或有可靠终页证据时接受 `true`。它仍不能认证来源真实性或证据真伪。2026-11-11 对正式安装 v0.5.3 的审计未发现可供 Skill 使用的分页/完整性信号；2026-11-13 单独测试的是隔离副本，不能推广为正式安装能力。run `SUCCEEDED`、返回数低于 `resultsLimit`、空结果或未见截断标记都不能证明完整。缺失/未知信号使覆盖为 unknown，并保留已验证候选；触顶仍是 possible cap/partial。失败 run 记录在 `run_failures`；成功但检索不完整/未知只反映在覆盖字段，不记为 Actor 失败。有行级选择错误时 helper 顶层状态为 `partial_interface_error`；身份冲突导致 partial 覆盖，无法归属的行导致 overall coverage unknown，但不无差别降低其他作者。顶层 `complete` 只依据显式完整性证据和本地检查，不超出该证据能支持的范围。缺少 schema/合同导致的 helper contract exception 则通过 CLI 非零退出和 `error` 字段报告。
- **结果限制与排序：** 公开输入 schema 对 `resultsLimit` 只写最大返回结果数。helper 的 select 输入为每次 Profile Posts run 一个 bundle（run ID、该次提交用户名、该次实际 `resultsLimit`、完整原始返回行、读取完整性信号）。它在时间窗筛选前按每个 run 的原始返回行数分别比较该 run 的上限；不同 run 不会合计。run 边界/上限/用户名映射缺失时返回顶层 `partial_interface_error` 和 `coverage_status: unknown`，不报完整。一个 run 包含多用户名且上限作用范围未核实时，输出 `unknown_multi_username_limit_scope` 或 `possible_results_limit_reached_scope_unknown`，不按作者拆分推断。单 run 行数达到上限只说明可能触顶。Actor 的真实单/多用户名计数语义、最新优先顺序、图片/非视频计入规则和完整性信号仍未核实；这些离线测试仅验证本地逻辑，不验证 Actor 行为。
- **运行费用参数（范围说明，2026-11-06）：** 公开 Apify MCP 与 API 文档存在运行费用选项的描述，见上文来源；这些信息不表示本 Skill 实现了参数透传或费用封顶。当前产品版本不要求报告总预算、run 级预算分配、`callOptions.maxTotalChargeUsd`、`maxItems` 或选项读回；相关预算规划/验证操作已从第二 Skill helper 和 CLI 移除。实际使用量按用户的 Apify 账户及 Actor 计费规则产生，不作固定费用或费用上限声明。
- **Profile Posts 待验证事项：** `resultsLimit` 对单/多用户名的实际语义、最新优先排序、图片/非视频计入规则、完整 media type 枚举和完整性信号仍无充分证据。候选行数达到传入 `resultsLimit` 时 helper 只标记“可能触及结果限制/额外候选未知”，不断言已截断或完整。必需字段或结构化接口契约缺失时，停止受影响的调用；只有媒体类型枚举/映射缺失时，仍可读取并保留原始帖子。按当前负责人确认的项目规则，只有 `type` 精确等于字符串 `"Video"` 且存在可用帖子 URL 才可进入 Transcript Actor；其他值保持未知，不得分类或声称没有视频。离线 `select` 通过不代表真实 Profile Posts 数据可用，也不能报告完整扫描或“没有新视频”。
- **执行状态：** URL/作者/稳定 ID 冲突对账、顶层选择状态、可能触及结果限制分类、窗口筛选、候选去重、转录批次拆分、transcript reconciliation 及 stdin JSON 入口已有离线实现。helper 的每作者数量设置只限制本地候选选择，不是 Actor `resultsLimit` 或费用上限。此前有两份用户提供的 Creator 单账号运行报告，日期为 2026-11-07 和 2026-11-08；原始运行输出未由 Codex 独立核实。2026-11-11 另有先后两次不同观察：先是首次预检在 Actor 调用前停止（未启动 Actor、无 Dataset），随后用户报告一次成功运行。预检停止不是 Actor run，也不与同日后续成功报告矛盾；后者同样未由 Codex 或 WorkBuddy 独立重放。以上报告不等于全面集成验证。离线测试不证明 Actor 输出、真实批次限制或宿主集成。Profile Posts 的媒体类型值、排序、结果限制语义与完整性仍待验证；选择结果中的 `returned_raw_rows` 表示单 Creator run 的 Dataset 原始行数（无法按 Creator 分配时为 null）；`discovered_returned_in_window` 表示窗口内可归属且 URL 可用的原始行数（含重复、任何媒体类型）；`type_video_candidates` 表示去重后、URL 可用且 `type == "Video"` 精确匹配的候选数，并在应用 `per_creator_limit` 前统计；`unknown_media_type` 表示窗口内可归属的未知类型原始行数（含重复、不要求 URL 可用）；`selected` 为应用本地处理上限后的数量。全面集成验证未完成，不能据此标为已完成或可发布。

### ChatGPT 首次预检停止观察（用户报告，2026-11-11；先于随后成功运行）

用户报告称，当前 ChatGPT Apify MCP schema 将 Profile Posts 输出 `type` 暴露为普通 string、没有 enum；Actor README 虽说明抓取 Posts 和 Reels，但未定义 `type` / `productType` 的值与媒体类别映射。该次 Skill 预检因此在调用 Actor 前停止，没有启动 Actor，也没有 Dataset 结果。本段记录来自用户报告，不是本次独立查询实时 schema 或 Actor 的结果。仓库较早的用户报告记录过 `Album`、`Video` 等原始值，没有可独立核验的原始行；该历史观察本身不是 Actor 枚举定义。当前项目处理规则由负责人确认：仅 `type` 精确等于大小写敏感字符串 `"Video"` 且有可用帖子 URL 时才送入 Transcript Actor。公开 Output schema 仍只将 `type` 声明为普通 string，无 enum；因此这是项目处理规则，不应描述为 Actor 官方保证。Reels 与普通视频帖都可转录，不需要 `isReel`；`productType` 不作为资格门槛，其它、缺失、null、非字符串的 type 保留为 unknown。

### Creator ChatGPT 报告流程成功运行（用户报告；2026-11-11；未独立重放）

用户提供的报告称，首次预检停止之后，另一次 ChatGPT Creator 报告流程中 Profile Posts 发现 run 成功，Dataset 21/21 条已读取。报告记录窗口内且 URL 可用 18 条、去重后精确 `type == "Video"` 候选 16 条、未知 `Album` 2 条；Transcript 有 16 条按 URL 匹配，15 条用于主题分析，1 条低质量转录被排除。Dataset 其余 3 条的去向以及这些计数之间的逐行关系，留存报告没有足够细节进行核对；不推断其为窗口外、重复、无 URL 或其他状态。WorkBuddy 2026-11-11 只读审计另发现，留存材料中前三个 Transcript run 的状态摘要与 Dataset 行数不一致且无法核实；保留原有差异，不推断原因或调整总数。`skipPinnedPosts=true`，排除的置顶帖子数量未知，覆盖仍是 partial/不确定。此为用户报告，不是 Codex 或 WorkBuddy 独立重放，也不证明完整覆盖或长期稳定。报告中的数值型帖子时间使用项目已核验的 Unix 秒映射转换为 UTC 和请求时区；该单位不是实时 schema 保证。发布时间以发现记录为主；Transcript 字符串 `timestamp` 是运行时间，`createTime` 仅在同帖 URL/ID 对账后交叉核对。

### Creator Profile Posts 置顶帖子请求约定（负责人确认；2026-11-11）

每次 `apple_yang/instagram-post-scraper` Profile Posts 调用应显式传入 JSON 布尔值 `skipPinnedPosts: true`，不得依赖 Actor 默认值，也不得传给 Transcript Actor。该设置表示跳过置顶帖子，因此目标时间窗内的置顶帖子也可能被排除；只有 Actor 返回可核验的排除数量时才报告具体数值。此前两份用户提供的运行摘要记录了该输入，但也明确说其实际效果未经验证；本记录没有 live input schema 原始材料可独立确认字段类型或语义。调用前仍须以当前 live schema 确认字段及布尔类型；字段缺失或类型冲突时停止 Profile Posts 调用并报告，不能省略或改值。

### 当前 Creator 视频处理规则补充（负责人确认；2026-11-11）

公共 Output schema 的 `type` 仍是无枚举的 string。当前实现按负责人明确的项目规则，仅接受 `type == "Video"`（大小写敏感）且有可用帖子 URL 的记录作为转录候选；不使用 `productType` 推断 Reels。未匹配该规则的记录保持未知，照片/carousel 不从字段名推断。Transcript Actor 可处理 Reels 和普通视频帖。该项目规则不是 Actor 官方 schema 枚举。

`resultsLimit=50` 是本项目的默认检索值，依据负责人此前运行观察称其为每位 Creator 的结果/预算上限；目前可见公共 schema 只定义最大结果数，并不保证“每位 Creator”语义。它与本地 `per_creator_limit` 不同，后者不传给 Actor。Actor run 成功且 Dataset 有证据已完整读完、Creator 返回行数低于 limit 时，只可报告“已读完 Actor 返回的数据，配置的结果上限未达到”；这不保证时间窗全覆盖。达到 limit 时提示可能受上限截断。

### Creator 帖子发布时间字段口径（项目规则与运行观察；2026-11-11）

发现 Actor 的帖子时间字段是主要来源。项目运行观察确认本次所用数值型帖子时间可按 Unix 秒映射转换为 UTC instant，再转换到请求时区；这不是实时 Actor schema 明确声明的秒单位，也不代表所有字段/运行的普遍保证。helper 仅在字段映射明确为 `timestamp_unit: "unix_seconds"` 时按秒解释数值；单位未知时保留原值并标记 `timestamp_unverified`，不据此进行窗口筛选。窗口筛选使用 helper UTC 边界与同一 UTC instant，本地显示由该 instant 转换并标注时区。Transcript Actor 字符串 `timestamp` 是运行时间，不是帖子发布时间；`createTime` 只可在 URL/ID 对账确认同一帖子后作为交叉核对，发现 Actor 字段仍是主要来源。

## 第三个 Actor：Instagram Video Scraper API（2026-11-10）

**Review only:** public Apify pages for [`apple_yang/instagram-video-scraper-api`](https://apify.com/apple_yang/instagram-video-scraper-api), its [Input](https://apify.com/apple_yang/instagram-video-scraper-api/input-schema), [Output](https://apify.com/apple_yang/instagram-video-scraper-api/output-schema), [API](https://apify.com/apple_yang/instagram-video-scraper-api/api/python), and [examples](https://apify.com/apple_yang/instagram-video-scraper-api/examples) were inspected. No Actor/API/MCP call or platform UI was used.

- README and Input show required `videoUrls` (array); README supports one or more `/p/` and `/reel/` URLs. Input additionally shows optional `sessionid` string; its purpose is unverified. Input size/limits are unverified.
- README field list and JSON sample show `url`, `code`, `pk`, `id`, `title`, `img`, `videoUrl`, `audioUrl`, `createTime`, `likeCount`, `commentCount`, `userPk`, `userName`, `userFullName`, `avatarUri`, `errMsg`, `timestamp`. The README describes `createTime` as a Unix timestamp, while the Output schema declares only an integer. Seconds are inferred from the README sample's magnitude, not explicitly stated by the schema. Any seconds-based conversion for this Actor must retain that limitation; do not apply the Creator Profile Posts Actor's timestamp mapping to it. The dynamic Output schema did not expose a complete inspectable field/type contract, so per-field requiredness and schema types remain unverified beyond the displayed sample.
- No `views`, play count, or impressions field is shown in the README field list/sample. Treat these as unsupported until evidence appears.
- README describes direct CDN URLs, says they may become invalid, and states public content only; private accounts, Stories, and authentication-required content are inaccessible. README says a failing URL returns an `errMsg` and other batch URLs continue. Exact error-row/top-level error semantics remain unverified.
- The [single metadata example](https://apify.com/apple_yang/instagram-video-scraper-api/examples/extract-instagram-video-data-metadata) and [bulk URL example](https://apify.com/apple_yang/instagram-video-scraper-api/examples/bulk-instagram-video-audio-url-extractor) pages exposed titles/descriptions but no inspectable complete sample payloads. Promotional descriptions are not schema evidence.
- No run was made. Evidence is limited to public page content; see [the third Skill PRD](instagram-media-links-and-post-insights-prd.md) for field-level notes and open questions.

## ChatGPT Plus 账号第三个 Skill 运行报告（2026-11-10）

The project owner reports a later, separate test in their ChatGPT Plus account: a custom MCP server named `Apify MCP` at `https://mcp.apify.com` was added through the Plugins page, authorized with OAuth, and created as a plugin/App. The owner then used the latest installed third Skill for exactly one two-URL batch. Reported evidence: Actor `apple_yang/instagram-video-scraper-api`; run status `SUCCEEDED`; Dataset contained two rows and all two were read; both rows matched an input by returned `url`. No URL or Dataset ID is retained here.

This is an owner-provided summary, not an independently inspected trace. It supports only the successful connection/call/status/Dataset-read/URL-match path in that account and product state. It does not verify all Plus accounts, plans, regions, or workspaces, error or partial-result cases, other platforms, or the two existing Skills. The earlier “No run was made” statement above describes the public-page inspection and remains accurate for that inspection; this later account test is separate evidence. For the current status and remaining limits, see [test status](test-status.md#instagram-media-links-and-post-insights-chatgpt-plus-test-2026-11-10).
