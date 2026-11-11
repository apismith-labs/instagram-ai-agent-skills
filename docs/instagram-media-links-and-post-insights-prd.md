# PRD: Instagram Media Links & Post Insights

**状态：** 已进入实现阶段；用户报告一次 ChatGPT Plus 单账号两 URL 成功路径（详见[测试状态记录](test-status.md#instagram-media-links-and-post-insights-chatgpt-plus-test-2026-11-10)），当前实现仍待必要的运行时验证和独立验收，尚不可标为已验证、可发布或已发布<br>
**版本：** 0.1  **日期：** 2026-11-10  **审批：** 用户已批准进入 Skill 实现（2026-11-10）

## 1. 定位与命名

为用户提交的、属于 Actor 可处理范围的公开视频帖子或 Reel URL 提取 Actor 返回的媒体直链，或整理该条内容实际返回的原始计数及其他已核实字段。用户是需要链接或单条/批量帖子数据的研究者、创作者和内容运营者。一次抓取是当次采集快照。

**推荐名称：** Instagram Media Links & Post Insights<br>
**推荐 slug：** `instagram-media-links-and-post-insights`

命名保留仓库现有 `instagram-...` slug 习惯，并同时表达两个明确模式。Actor 为 `apple_yang/instagram-video-scraper-api`。该名称及 slug 暂定；Skill 已进入实现阶段，当前实现仍待必要的运行时验证和独立验收，不能据此视为已验证或可发布。

## 2. 两个模式

| 模式 | 意图/触发示例 | 默认结果 |
| --- | --- | --- |
| Media links | “提取这个 Reel 的视频和音频链接：URL”；“检查这些公开视频帖/Reel 是否返回媒体链接：URL 列表” | 仅在内容可确认为 Actor 可处理的视频帖子或 Reel 时，按输入列出原始 URL、实际返回的 `videoUrl`/`audioUrl` 和字段状态。链接不是保存到设备的文件。若 URL 对应非视频内容或媒体类型无法确认，不猜测、不承诺链接，并说明当前无法确认内容是否受支持。 |
| Post insights | “整理这个视频帖/Reel 返回的作者、发布时间、点赞和评论”；“比较这些 URL 返回的点赞和评论数” | 只整理或比较本次实际返回的原始计数及其他已核实字段。一次抓取只是当次采集快照；不计算互动率等派生指标，不据此声称趋势、表现变化或受众反应，不作因果推断或将数值比较包装成已验证业务结论。 |

同一请求同时含两种意图时可合并输出两组字段。意图不清时询问要媒体直链、帖子数据或两者。示例须在首次使用设置介绍之前呈现。

## 3. Actor 契约（公开页面核验，2026-11-10）

证据：[Actor README](https://apify.com/apple_yang/instagram-video-scraper-api)、[Input](https://apify.com/apple_yang/instagram-video-scraper-api/input-schema)、[Output](https://apify.com/apple_yang/instagram-video-scraper-api/output-schema)、[API](https://apify.com/apple_yang/instagram-video-scraper-api/api/python)、[Examples](https://apify.com/apple_yang/instagram-video-scraper-api/examples)、[单条元数据示例](https://apify.com/apple_yang/instagram-video-scraper-api/examples/extract-instagram-video-data-metadata)、[批量链接示例](https://apify.com/apple_yang/instagram-video-scraper-api/examples/bulk-instagram-video-audio-url-extractor)。公开页面部分内容由动态 UI 提供；不可见处标为未核实。示例页可见名称和描述，但抓取视图未显示可检查的完整运行输入/输出样本。

### 输入

| 字段 | 已核实内容 | 证据/限制 |
| --- | --- | --- |
| `videoUrls` | 必填 array；元素描述为 Instagram URL。README 示例使用单个 `/p/` URL，README 声明支持单条及数组批量，支持 `/p/` 与 `/reel/`。 | Input schema 还展示 `videoUrls` 为必填 array；README Input 章节、FAQ。长度限制、URL 校验规则及其他 URL 类型未核实。 |
| `sessionid` | Input schema 显示可选 string。 | 具体认证用途/支持边界未核实；首版不要求或收集此字段。 |

### 输出

README 的字段目录与 JSON 输出样本明确列出下列名称及样本值类型；公开 Output schema 动态视图未提供足以核实每个字段必填性/类型定义的完整 schema。因此字段均按**可能返回**处理，不能假定每条必有。

| 字段 | README 样本类型 | 用途 |
| --- | --- | --- |
| `url` | string | 结果与原始输入匹配；若缺失/不一致则不猜测 |
| `code`, `pk`, `id` | string | 辅助标识；稳定性与唯一性未独立验证 |
| `title` | string | caption/title 文本（可能为空） |
| `img` | string | 缩略图 CDN URL |
| `videoUrl`, `audioUrl` | string | Actor 返回的媒体直链 |
| `createTime` | number | Unix 时间戳样例 |
| `likeCount`, `commentCount` | number | 点赞、评论数样例 |
| `userPk` | string | 作者 ID 样例 |
| `userName`, `userFullName` | string | 作者名称样例 |
| `avatarUri` | string | 头像 URL 样例 |
| `errMsg` | string | 错误信息样例；空串表示样本无错误 |
| `timestamp` | string | ISO 8601 抓取时间样例 |

**Views/play count/impressions：未确认。** README 的当前字段表及输出样本没有这些字段，故首版不承诺播放量、浏览量或曝光量。单条示例/批量示例的名称和宣传描述不能证明具体 schema、顺序保证或错误结构。

## 4. 结果匹配、缺失与错误

- 保存用户输入原文及其序号；以输出 `url` 经可验证的 URL 等价规则匹配输入。可用且一致的 shortcode/ID 可作为经核实的辅助线索，但不依返回顺序猜测。多个候选、缺 `url` 或冲突时标记“对应关系未知”，不拼接归属。
- 按以下情况分别向用户报告，不合并成“成功/失败”二分：
  1. 结果行存在且 `errMsg` 为非空字符串：报告 Actor 实际返回的错误信息，不自行扩写原因。
  2. 没有找到与输入可靠匹配的结果行：报告“未收到可匹配的结果”，不直接称 Actor 失败或帖子不存在。
  3. 结果行存在但字段缺失、为空或未返回：报告“该字段未返回/不可用”。缺少 `videoUrl`、`audioUrl` 或互动字段不代表媒体不存在，也不代表计数为零。
  4. 结果行缺少可匹配的 `url`、URL 冲突或有多个候选：报告“对应关系待确认”，不得按返回顺序猜归属。
  5. `errMsg` 缺失或为空：如实标记该字段缺失/空值；不得单凭此推断整条任务必然成功。
  6. 批次部分成功：逐条呈现可确认结果及未匹配/错误项目，不描述为全部完成。Actor README 声称批次其他 URL 可继续处理，但实际部分失败结构仍待验证。
- 媒体类型无法确认时，报告当前无法确认该内容是否受支持；不把路径 `/p/` 当作视频类型证据，也不承诺视频或音频链接。
- URL 可能已失效或不可访问；在 Actor 未返回有效结果时，不尝试绕过限制，不推断具体原因。

## 5. 用户体验与首次 Apify 引导

首屏先说用户价值并给两个模式的请求示例，再讲设置。**安装 Skill ≠ 配置 Apify。** 首次真实任务的就绪检查适用于所有宿主，但只检查当前会话实际暴露的 Apify 工具、实时 schema 及宿主明确提供的授权/连接状态。这是 Skill 指令层面的检查，不是安装检测程序；工具缺失不能证明插件未安装，也不能可靠区分未安装、未启用、未授权、工作区限制或宿主未暴露工具。无可用工具、宿主明确报告未授权或运行条件无法确认时，须在 Actor 调用前停止。

连接、安装及 OAuth 必须按宿主分别说明并由用户完成。Skill 不自动安装插件、修改宿主配置、启动 OAuth 或代用户授权；不要求用户在聊天中提供 API Key。宿主未知时只给通用说明，不猜测平台；确认 Apify 工具可用后不重复首次设置引导。OpenClaw 专属命令只在明确识别为 OpenClaw 时显示，并沿用其已批准引导。ChatGPT 设置说明须保持条件性：OpenAI 文档分别描述了自定义 MCP/完整 MCP 支持与 Skills 的计划范围，二者不可合并成所有账号均具备的能力。当前文档说明 ChatGPT Business 与 Enterprise/Edu web 的完整自定义 MCP 支持及相应管理员/RBAC 权限条件；Pro 用户可连接具有 read/fetch 权限的自定义 MCP；Skills 面向符合条件的 Business、Enterprise、Healthcare 与 Edu 用户，并受工作区设置及产品可用性限制。若账号缺少连接或 Skill 入口，须说明可能受计划、工作区策略、管理员权限或产品/界面可用性限制。非 ChatGPT 宿主按现有平台指南提供的方法引导；若项目指南未记录对应 Apify 接入，转至该平台官方设置文档，不泛化 OAuth/Connector/MCP/插件流程。

Apify 注册入口为 [https://console.apify.com/sign-up](https://console.apify.com/sign-up)，托管 MCP endpoint 为 `https://mcp.apify.com`。Skill 中应包含指向唯一 Actor 页面 [https://apify.com/apple_yang/instagram-video-scraper-api](https://apify.com/apple_yang/instagram-video-scraper-api) 的外链；未来进行用户文档/发布准备时，在第三个 Skill 的 README 介绍附近加入同一外链。英文引导应沿用 Creator canonical Skill 已批准的 OpenClaw 用户可见设置引用块，不在介绍开头放设置文本。

## 6. 范围、边界与职责区分

首版范围为用户提供且 Actor 能处理的公开视频帖子和 Reels URL。Actor README 称支持 `/p/` 与 `/reel/`；但 `/p/` 只是帖子 URL 路径，不能据此判断帖子一定是视频。照片帖和轮播帖在取得明确 schema 或样例证据并通过验证前，首版暂不承诺；这不是 Actor 实测证明其不支持。若输入对应非视频内容，或媒体类型无法确认，Skill 不猜测、不承诺视频/音频链接，并说明当前无法确认是否受支持。Actor README 称 private accounts、Stories、需要认证的内容不可访问。Input schema 显示 `sessionid` 可选，但其意义未核实，故不能据此扩大承诺。

Post Insights 仅整理或比较 Actor 实际返回的原始计数及其他已核实字段。一次抓取是当次采集的快照；不据此声称趋势、内容表现变化或受众反应，不作因果推断，也不把简单数值比较包装成已验证业务结论。除非所需输入字段（如 views、reach、impressions、粉丝数）的来源和定义经核实并获批准纳入范围，不计算互动率或其他派生指标。`views`、play count、impressions 仍未确认，不属于首版功能。

不把直链提取称为下载到本地，不宣称链接永久有效（README 称 URL 通常稳定但可能失效）；不承诺未核实的分享、收藏等指标；不做账号帖子发现、定时监控、transcript、视觉理解。用户应遵守适用的服务条款、版权和隐私要求；本文件不作法律结论。

与现有 Skill 的职责界线：Transcript Extractor 接收用户给定视频链接并提取语音转录；Creator Reels Insights 从创作者账号及时间窗口发现帖子并进行 transcript-based 分析。本 Skill 不转录，也不发现账号帖子；仅处理用户给定且媒体类型受支持或可确认的视频帖子/Reel URL，输出链接或返回的帖子字段。

## 7. 验收与待验证项

验收需覆盖两个模式、单条与批量、输入输出匹配、URL 失效/不可访问、Apify 未授权及工具不可用，以及下列具体情况：

- 在向用户承诺“将开始处理”前完成内部 preflight；preflight 未通过时不得暗示 Actor 已启动，并明确说明缺少的能力、未启动 Actor、未取得结果。
- ChatGPT 首次使用：若没有可用 Apify 工具、授权明确缺失或就绪状态无法确认，应停止 Actor，并显示 Skill 中完整的 ChatGPT 自定义 MCP 设置指引；不得用泛化的 Settings/Plugins 搜索说法、仅给链接或其他通用连接话术替代。不得声称可检查 ChatGPT 内部 Skill 加载状态，也不得仅凭引导未显示就断言 Skill 未加载。
- 专用 Actor 工具路径：必须从实时工具描述/schema 精确确认 owner 与 Actor 名称对应 `apple_yang/instagram-video-scraper-api`；名称相似、泛 Instagram 描述或身份含糊不够。身份不符/不明时仅在通用路径完整可用时回退，否则停止。
- 通用 Actor 调用路径：要求同时具备可读取 Actor 当前 schema 的工具（如 `fetch-actor-details` 等效项）和通用 Actor 调用工具；Actor identifier 格式及调用参数由当前工具 schema/权威文档确定，不从 Store URL 推断。
- 通用调用若返回 run 状态和 Dataset 标识，需据实记录并通过 `get-dataset-items` 或宿主等效能力读取结果行；按 live pagination 信息继续读取，直至有证据表明读全。缺少 Dataset 读取工具或无法核实分页完整性时，报告结果不可确认/部分，不称 Actor 无数据。
- 若 run 返回非终态，须依据实时状态与工具/宿主契约判断。存在 run 查询/等待能力时，按其实时 schema 继续查询同一 run，不重复启动；未结束或无法查询时报告仍在运行/待定/可能不完整，不称任务完成。非终态期间读取的 Dataset 除非有明确完整性证据，只能作为暂定/部分结果。
- 只有 run 到达工具契约定义的终态且 Dataset 读取具备完整性证据时，才可报告结果完整；不得硬编码未经确认的状态枚举、run ID 字段名、轮询次数、间隔或工具参数。
- 缺少目标 Actor 专用工具、通用调用工具、Actor schema 或所需 Dataset 读取能力时 fail closed；不得改用其他 Actor、猜工具参数或绕过宿主限制。
- 没有实际 Actor 结果行时，不得声称已处理 URL 或已返回媒体/帖子数据；专用工具直接返回行时不臆造额外 Dataset 读取步骤。

- 非视频内容或媒体类型无法确认（包括不能仅凭 `/p/` 认定为视频）：不承诺媒体链接，提示当前无法确认是否受支持。
- 非空 `errMsg`：仅报告 Actor 返回的原文信息，不补充猜测原因。
- `errMsg` 为空或缺失：记录字段状态，不由此单独推断成功。
- 没有可可靠匹配的结果行：报告未收到可匹配结果，不称为 Actor 失败或帖子不存在。
- 结果行中媒体链接或互动字段缺失/为空：报告字段未返回/不可用，不解释为媒体不存在或数值为零。
- 结果 URL 缺失、冲突或存在多个候选：报告对应关系待确认，不按顺序猜测。
- 批次部分成功：逐条呈现确认结果与未匹配/错误项，不声称全部完成。
- Post Insights 只呈现已核实字段的本次快照和原始计数比较；不承诺 views、play count、impressions，不计算依赖未核实输入的派生指标，不作趋势、受众反应或因果结论。

区分：静态检查、离线模拟、Actor 真实调用、平台端到端验证。目前仅有项目负责人报告的一次 ChatGPT Plus 两 URL 正向运行验证，范围与限制见[测试状态记录](test-status.md#instagram-media-links-and-post-insights-chatgpt-plus-test-2026-11-10)；该报告不替代失败/部分结果场景和完整平台端到端验证。完成必要的运行时验证和独立验收前不得将 Skill 标记为已验证或可发布。照片帖/轮播帖仅在获得明确 schema 或样例证据并通过验证、且经批准扩展范围后才能纳入。

待验证：Output schema 完整字段、必填性和类型；两个示例实际输入/输出；`errMsg` 失败行结构及顶层错误；结果 URL 的规范化与标识稳定性；批量上限/顺序；views/play count/impressions（目前无证据，不列入首版承诺）；媒体 URL 有效期及 HEAD/可访问保证；照片帖和轮播帖能否返回所需链接/帖子数据（首版暂不承诺，不代表已实测不支持）；当内容类型无法判定时 Actor 的输出形态；可选 `sessionid` 行为；派生指标所需字段的来源与定义（未核实且未批准前不实现）。

## 8. 发布门槛与流程

用户已批准本 PRD 进入实现阶段。项目负责人报告已在其 ChatGPT Plus 账号中完成一次两 URL 批量成功路径验证（Actor `SUCCEEDED`、Dataset 两条均读完且按返回 `url` 匹配）；该单账号证据不保证其他 Plus 用户，也不覆盖失败/部分结果边界、其他平台或前两个 Skill。Codex 实现后由 WorkBuddy 独立审核；完成必要的运行时验证和独立验收前，不得将 Skill 标为已验证、可发布或已发布。本轮已同步通用 ChatGPT 连接说明及有限验证状态；第三个 Skill 的正式用户介绍、可用入口和发行信息仍待达到发布门槛后更新。之后 GitHub ZIP 与 ClawHub 分别核验；用户手动处理 GitHub Release，WorkBuddy 仅按授权负责 ClawHub 发布。
