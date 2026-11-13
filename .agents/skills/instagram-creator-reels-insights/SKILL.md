---
name: instagram-creator-reels-insights
description: Review public creators’ recent Instagram videos, including Reels and regular video posts, in source-linked daily or weekly reports. Also select this Skill for first-use Apify setup or when Apify MCP is unconnected or its authorization/readiness is unconfirmed; provide the host-specific guidance before stopping.
---

# Instagram Creator Video Insights

Turn recent public Instagram videos—including Reels and regular video posts—from one or more creators into a source-linked report. Name the public accounts, choose Daily Scan or Weekly Review, and the Skill finds recent posts, transcribes the videos it can, and summarizes what was actually said, with a link to every source post.

## What you get

- **Daily Scan** reviews the most recent 24 hours for each creator you name.
- **Weekly Review** reviews the most recent 7 days and highlights recurring topics, hooks, and calls to action.

Every report keeps each creator in a separate section, ties findings to source posts, and separates transcript evidence from interpretation. Cross-creator comparisons appear only when the available transcripts support them.

## Copy-ready requests

Replace the placeholders with public accounts and your own brand.

**Daily Scan**

```text
Run a Daily Scan for [CREATOR_1], [CREATOR_2], and [CREATOR_3]. Review their recent public Instagram videos—including Reels and regular video posts—from the last 24 hours. Give each creator a separate section with links to source posts and transcript-based observations.
```

**Weekly Review**

```text
Run a Weekly Review for [CREATOR_1], [CREATOR_2], and [CREATOR_3] for the last 7 days. Review their public Instagram videos, including Reels and regular video posts. Summarize each creator separately, then compare themes only where the available transcripts support a comparison. Link each finding to its source post.
```

**Content ideas**

```text
Based on the available transcripts from [CREATOR_1], [CREATOR_2], and [CREATOR_3], suggest content angles for [MY_BRAND]. Link observations to source posts and distinguish transcript-supported observations from your suggestions.
```

## 首次使用：先检查 Apify 就绪状态，再按宿主引导

安装本 Skill 与连接 Apify 是两件独立的事。首次真实任务时，先检查当前会话实际暴露的 Apify 工具、实时 schema，以及宿主明确提供的授权/连接状态。若工具不可用、授权未确认或运行条件无法确认，必须先停止：明确说明“未启动 Actor、没有收到结果”，再直接给出下方已识别宿主的操作步骤。不要推断插件未安装；不要自动安装、修改配置或启动 OAuth；不要改用其他 Actor、HTTP/API、shell、token 或 cookie 绕过。若已确认就绪，不重复首次引导。设置完成后，只有当前会话实际暴露并确认 Actor 调用、schema、run 状态与结果读取能力可用，才继续；否则停止并说明缺口。

### ChatGPT 普通聊天与工作模式

除非用户明确表示已有 Apify 账号，否则必须在设置引导中单独显示：

**如果你还没有 Apify 账号，请先[注册 Apify](https://console.apify.com/sign-up)，再继续连接。**

**连接 Apify：**按顺序完成以下步骤：

1. 打开 **Plugins → + → Add custom MCP server（添加自定义 MCP 服务器）**。
2. 填写 **Name（名称）** `Apify MCP` 和 **Server URL（服务器地址）** `https://mcp.apify.com`。
3. 将 **Authentication（身份验证）** 设为 **OAuth**。
4. 阅读风险提示，勾选确认框，然后选择 **Create as a plugin（创建为插件）**。
5. 之后按 ChatGPT 提示登录 Apify 并授权。
6. 连接完成后，建议在新的 ChatGPT **工作模式**聊天中重新提交任务；若继续使用当前会话，则刷新可用工具后再试。本项目测试观察到，普通聊天模式可能无法可靠调用 Skill，因此优先使用工作模式。

若找不到 **Add custom MCP server**，检查账号、工作区或管理员权限，并查看[OpenAI 自定义 MCP 指南](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt)。Apify MCP 连接与 Skill 安装是独立步骤；一个连接可供多个 Skill 共用。不要在聊天中提供 API Key、token 或其他凭据。就绪后仍须以当前会话实际可见的 Apify 工具为准。需要完整的 ChatGPT 安装与使用步骤，请查看[项目 ChatGPT 指南](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/chatgpt.md#1-add-and-authorize-the-apify-mcp-connection)。

### Codex 桌面端与 CLI

Codex Skill 和 Apify 插件是两项安装。先安装本 Skill 的完整目录：在 Codex 会话中若可用 `$skill-installer`，请求它从 `https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-creator-reels-insights` 以 Git 方式安装到 `~/.agents/skills/instagram-creator-reels-insights/`，目标已存在就停止不覆盖；若已有本地仓库，可把 `skills/instagram-creator-reels-insights/` 完整文件夹放入当前项目 `.agents/skills/`，或用户级 `~/.agents/skills/`。OpenAI 的[官方 Codex Skill 目录说明](https://developers.openai.com/api/reference/cli#use-the-cli-from-a-coding-agent)列出了这两个位置。开始新会话，并明确调用 `$instagram-creator-reels-insights`。就绪信号是新会话能发现该 Skill，且 Apify 工具和所需操作实际可用。

**Codex 桌面端：**在 ChatGPT 桌面应用左上角切换到 **Codex**；侧栏打开 **Plugins（插件）**，点 **+** 旁下拉菜单 → **Add marketplace（添加市场）**，Source 输入 `apify/apify-codex-plugin` 并添加。打开 **Personal** 页，在 Apify Plugin 下点 **Add** → **Add to Codex** → **Install Apify**；浏览器打开 Apify OAuth 后检查权限并点 **Allow access**。

**Codex CLI：**在 Codex CLI 输入 `/plugins`；选择 **Add Marketplace**，输入 `apify/apify-codex-plugin` 并确认；打开 **Apify Plugin** 页，选 Apify → **Install plugin**。首次调用需授权的 Apify 工具时，浏览器会打开 OAuth；检查权限并点 **Allow access**。两个 Codex 环境是不同设置入口，不要把桌面步骤用于 CLI 或反之。随后在新会话显式调用 `$instagram-creator-reels-insights`，并确认工具可用。详见[Codex 指南](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/codex.md)、[Apify Codex 桌面端指南](https://docs.apify.com/integrations/codex-app)和[Apify Codex CLI 指南](https://docs.apify.com/integrations/codex-cli)。

### Claude Web 与 Claude Desktop 聊天

**安装本 Skill：**在 Claude 左侧 **Customize（自定义；部分账号正在改为 Plugins/插件）→ Skills（技能）→ + → Create skill（创建技能）→ Upload a skill（上传技能）**，上传信任的 Skill ZIP，完成扫描并启用。企业管理员可限制代码执行、创建和上传权限；若看不到入口，查看[Claude Skills 官方说明](https://support.claude.com/en/articles/12512180-use-skills-in-claude)。

**连接 Apify：**在 Claude 左侧打开 **Customize/Plugins → Connectors（连接器）**，找到官方 Apify Plugin 并点 **Add（添加）**（正在逐步上线的新界面可能以 Plugins 页面和筛选器显示）。在 Apify 插件页打开 **Connectors**，对 `apify` 连接点 **Connect**；在对话框选择 **Continue → Add**，在浏览器的 Apify 授权页核对账号与权限并点 **Allow access**。检查连接显示 connected。新聊天中通过输入框 **+** 菜单启用 Apify Connector，再输入 `/` 选择本 Skill（若当前界面提供该选择器）；也可在请求中明确点名本 Skill。桌面版常规聊天使用同一 Claude 账号的设置；不要把 Claude Code CLI 的命令用于 Claude Desktop 聊天。若企业工作区限制连接器，由管理员配置。详见[Claude 指南](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/claude-web.md)、[Apify Claude.ai 指南](https://docs.apify.com/integrations/claude-ai)和[Anthropic 远程 MCP 说明](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)。

### Claude Code CLI

Claude Code CLI 与 Claude Desktop 聊天是不同产品。先在 Claude Web/Desktop 账号中按上方步骤安装并启用本 Skill；在已登录同一 `claude.ai` 账号且版本支持 Skills 同步的本地 Claude Code CLI 新会话中运行 `/skills`，确认它显示在 `claude.ai sync` 下，再用 `/` 选择显示的 Skill 命令。也可将本 Skill 的完整目录放入 `~/.claude/skills/instagram-creator-reels-insights/`。然后在 Claude Code CLI 中运行 `/plugin install apify`，选择安装范围；运行 `/mcp`，启用 `plugin:apify:apify` 并选择 **Authenticate**，在浏览器登录 Apify、检查权限并点 **Allow access**。`/mcp` 中连接状态和会话实际暴露工具是就绪检查；随后在新会话调用本 Skill。Apify 当前文档确认 Claude Code CLI 路径；不把它外推到 Claude 桌面应用的 Code tab 或 Web/远程代码会话。参阅[Claude Code Skills](https://code.claude.com/docs/en/skills)、[Apify Claude Code CLI 指南](https://docs.apify.com/integrations/claude-code-cli)和[项目 Claude 指南](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/claude-web.md)。

### Manus

**连接 Apify：**打开 **Settings（设置）→ Connectors（连接器）→ + Add connectors → Custom MCP → + Add custom MCP → Direct configuration（直接配置）**。填写 **Server name（服务器名称）** `Apify`、**Transport type（传输类型）** `HTTP`、**Server URL（服务器地址）** `https://mcp.apify.com`，点 **Save**。在聊天中首次调用 Apify 工具时，按 Manus 弹出的 OAuth 流程登录并授权；不要改用 API token。检查连接已保存且工具在当前会话可用。

**安装本 Skill 并调用：**打开 **Skills → + Add → Import from GitHub**，粘贴仓库中本 Skill 文件夹的公开 GitHub URL：`https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-creator-reels-insights`，点 **Import**；确认 Skill 出现在个人列表并启用。新任务中在输入框键入 `/` 选择本 Skill，并通过输入区下方的连接器按钮开启 Apify。就绪前须看到 Skill 可选且 Apify 连接开启。Manus 官方说明 MCP 在各计划均可用，但账号权限、界面更新和任务结果仍可能不同。详见[项目 Manus 指南](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/manus.md)、[Apify Manus 指南](https://docs.apify.com/integrations/manus)与[Manus Skills 指南](https://help.manus.im/en/articles/14753565-how-to-share-and-use-skills-in-manus)。

### OpenClaw

先安装本 Skill，再配置 Apify 插件。Creator Video Insights 的 ClawHub 路径可运行 `openclaw skills install @apismith-labs/instagram-creator-reels-insights`；如果你改用已克隆到 Gateway 环境的本地仓库，从仓库根目录运行 `openclaw skills install ./skills/instagram-creator-reels-insights --global`，仅限当前工作区时去掉 `--global`。需要 OpenClaw 2026.1.0 或更新版本，以及 Node.js 22+；详见[当前 Apify 插件要求](https://docs.apify.com/integrations/openclaw)。运行 `openclaw skills check` 检查默认 Agent，开新会话并使用 `$instagram-creator-reels-insights`。若不知道自己的目录/Agent 权限，不猜配置，查看[项目 OpenClaw 指南](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/openclaw.md)及其官方链接。Apify 插件采用 OpenClaw 独立配置流程，不是 OAuth；完成下方原有 OpenClaw 引导后，在新会话确认 `apify` 工具可见。不要在聊天中发送 API Key。

### 其他或无法识别的宿主

若宿主无法确认，先问用户正在使用哪个产品表面，不给猜测的菜单或命令。只有在明确识别上述宿主后才显示其对应步骤。若某账号/工作区没有相应入口，提示查看所链接的官方平台说明或咨询管理员；不把 MCP、Connector、插件市场或 CLI 配置互相替代。

### OpenClaw 首次设置引导

仅当当前宿主已明确识别为 OpenClaw，且 Apify 工具不可用、宿主明确报告缺少授权，或当前可见状态无法确认就绪时，才逐字呈现下面的 OpenClaw 设置引用块。此时先停止 Actor 调用并说明未启动 Actor、没有收到结果。不要把其他宿主的步骤替代为 OpenClaw 命令；工具缺失也不能证明插件未安装。

> There's no confirmed usable Apify tool available to me in this OpenClaw session, so I can't start the analysis. This doesn't necessarily mean the plugin is uninstalled: it may be disabled, your Apify account may not be configured, or this Agent may not have permission. I have not started any Actor.
>
> If you don't have an Apify account, [create one in the Apify Console](https://console.apify.com/sign-up).
>
> Choose one way to install the Apify OpenClaw plugin:
> - Run `openclaw plugins install @apify/apify-openclaw-plugin`.
> - Or, if your OpenClaw Control UI shows the plugin catalog, open **Plugins**, search for **Apify**, and install the Apify listing from ClawHub. If it is not available there, use the CLI command above.
>
> Restart the OpenClaw Gateway after installation.
>
> First, prepare an Apify API Key. The [official plugin README](https://github.com/apify/apify-openclaw-plugin) explains how to create and configure it. Then run `openclaw apify setup` and follow the wizard to finish configuration. Never send your API Key in chat.
>
> After setup, open a new conversation and try your request again.
>
> For detailed steps, see the [OpenClaw setup guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/openclaw.md#set-up-the-apify-plugin).

The Skill must not install the plugin or change OpenClaw configuration. Do not start an Actor until the user completes setup and a usable Apify tool is available. Do not ask the user to send an API Key in chat.

After the user completes setup, open a new OpenClaw conversation or refresh available tools before retrying the Creator request.

## Before you start

- **Connect Apify in your host.** The Skill uses Apify Actors to read public posts and transcripts. Installing the Skill and connecting Apify are separate steps, and both are needed. Use only tools actually exposed in the current session or explicit connection status from the host. At the first actual analysis request, if Apify is unavailable, the host reports missing authorization, or readiness cannot be confirmed from host-visible status, stop without starting an Actor. Tell the user that no Actor was started and no results were received; explain what readiness condition could not be confirmed. If the host cannot expose connection status, say it cannot be confirmed; do not infer it from Skill metadata. For OpenClaw, show the setup guidance above only when the host is identified as OpenClaw; for ChatGPT, show the complete ChatGPT first-use block above when its condition applies; for other identified hosts, use only the matching platform-specific guidance, without showing OpenClaw commands. Do not install plugins, change host configuration, or use shell, direct REST/API, tokens, cookies, or session IDs to bypass missing tools or authorization. After the user configures Apify, ask them to start a new session or refresh available tools and retry the request.
- **Set a per-creator video limit.** It caps how many eligible videos are processed for transcripts in each report. It is a processing limit, not a full-account scan, and it does not cap usage or cost.
- **Check your Apify usage.** More creators or more videos can mean more usage on your own Apify account. Review current usage in the Apify Console; the Skill does not estimate a price or promise a fee cap.
- **Never paste credentials.** Do not share Instagram passwords, API tokens, cookies, or session values in chat. The Skill reads public accounts only.

For installation steps and more prompt examples, see the [project README](https://github.com/apismith-labs/instagram-ai-agent-skills#instagram-creator-video-insights).

## What the results mean

A report covers the posts and transcripts that run actually found and returned. Coverage can be partial or unknown, and the report states which. A creator with no returned post is not proof that the creator posted nothing, and an empty result is not evidence that the period had no new videos. Missing metrics are never treated as zero.

## Scope

- Daily Scan and Weekly Review for user-specified public accounts only. Do not offer a single-URL analysis task or a posts-only report.
- Do not schedule runs, monitor in the background, or claim to remember accounts or transcripts across sessions.
- Process only public accounts. Do not bypass login, rate limits, or platform restrictions, and never ask for or reveal tokens, cookies, session IDs, passwords, or authorization headers.

## How this Skill runs

Before each report, read [the workflow contract](references/workflow.md). Use the bundled offline helper at `scripts/workflow.py` for settings validation, UTC window construction, candidate selection and coverage status, batch splitting, and transcript reconciliation. Invoke it with `python3 <skill-directory>/scripts/workflow.py` and one JSON object on stdin; consume its JSON result and treat any nonzero exit or `error` as a stop condition. The helper makes no network calls and stores no settings. If the host cannot safely execute it or provide private in-memory inputs, explain that limitation without starting Actor calls.

### First use and saved settings

The first setup confirms only: (1) the public accounts to monitor, (2) the maximum number of videos per creator to include in each report, and (3) whether the user agrees to save the account list and setting. Do not ask for a report budget or per-run cost setting. Save only if the host supports user-authorized persistence. Otherwise provide a reusable request containing the accounts and per-creator video limit. Routine runs reuse available settings and do not repeat setup.

The per-creator limit applies after candidate discovery: it selects how many eligible returned videos are sent for transcript processing and analysis. It is not an Actor retrieval limit, does not limit discovery reads, does not guarantee complete account coverage, and does not cap usage or cost. If an older saved settings object contains `report_budget_usd`, ignore that field; it is not a current setting and must not affect planning or Actor calls.

Use plain language. Do not expose schema fields or require users to configure Actor runs. If Apify readiness is not established, follow the first-use host-specific guidance above; for ChatGPT, display its complete setup block rather than generic connection-settings or plugin-search instructions. Never ask them to paste a token, cookie, password, session ID, or authorization value into chat.

Be transparent that Profile Posts discovery and Transcript processing may involve multiple Actor runs and may generate Apify usage according to the user's account and each Actor's current rules. Do not conceal calls, estimate a fixed fee, promise a fee cap, or repeatedly ask about a budget. Users can review actual usage in Apify Console. Follow approvals required by the host.

### Request and modes

- Accept public Instagram usernames or profile URLs, a report mode, and optional timezone/report language.
- If mode is omitted, use Daily Scan: the rolling 24 hours before the request. Weekly Review uses the rolling 7 days. Resolve explicit calendar periods in the user's timezone and show the exact UTC boundaries and displayed timezone. Pass the requested IANA timezone to the helper as `display_timezone`; if none is specified, use and label UTC.
- Explain briefly that the report discovers recent posts, transcribes eligible videos, and analyzes their spoken content.
- Normalize supplied account names/profile URLs conservatively. Keep each requested account mapped to its normalized identity. Reject ambiguous or unsupported input; never broaden to other accounts.

### Execution

1. At the first actual analysis request, check the tools actually exposed by the selected host, their live input schemas, authorization, run-status query, and result/Dataset read capabilities for `apple_yang/instagram-post-scraper`. Tool names and argument shapes vary by host; do not assume every host exposes `call-actor` or the same contract. Before Profile Posts discovery, do not require an output enum or a Reel/non-Reel mapping; a string `type` field without an enum is not a blocker to retrieving raw records or processing records that meet the project rule below. If the Profile Posts Actor/tool, authorization, required input contract, run-status query, or ability to read raw results is unavailable or unconfirmed, stop before that Actor call and explain the specific blocker; do not try another Actor. Inspect returned output fields and preserve their raw values after discovery without guessing aliases. Verify the Transcript Actor's live contract only before any Transcript call. If the host cannot expose plugin or authorization status, say it cannot be confirmed rather than inferring it. For OpenClaw, show the first-time setup guidance above only when the host is identified as OpenClaw; for ChatGPT, use the complete ChatGPT first-use block above when its condition applies; for other identified hosts, use the corresponding platform guide without showing OpenClaw commands. Never install a plugin or change host configuration automatically. These conditions do not create a budget-parameter requirement.
2. Run the helper `settings` operation using the accounts, positive integer per-creator video limit, and save consent. If the current request omits `per_creator_limit` and no existing user-authorized setting is available, ask the user to confirm that processing limit before discovery; do not save it without explicit consent. For Daily/Weekly boundaries, call `window` with the request timestamp and mode. Keep its `end_utc_exclusive` value through selection and pass the requested IANA timezone as `display_timezone` to `select` (use and label `UTC` when the request specifies none).
3. Use the host's live-supported input to discover posts for the requested accounts and time window. For every `apple_yang/instagram-post-scraper` request, explicitly include the JSON field `"skipPinnedPosts": true`; do not omit it and rely on the Actor default. Before the call, verify the live input schema accepts this field as a boolean; if it is absent or conflicts, stop and report the schema mismatch rather than omitting or changing the value. This setting applies only to Profile Posts discovery and must never be passed to the Transcript Actor. There is no user override for this project default. A true value skips pinned posts, including ones that fall within the requested time window. Disclose that exclusion and do not claim all time-matching posts were covered; report an excluded-post count only if the Actor returns a verifiable count. Keep `resultsLimit` separate from the local `per_creator_limit`; never pass `per_creator_limit` as Actor input. When the live schema supports it, use `resultsLimit=50` as the project default. This default reflects the project owner's prior runtime observation of a per-Creator result/usage limit; the public schema describes a maximum result count but does not guarantee per-Creator semantics. Submit one username per run while scope behavior remains unverified. Preserve each run boundary, submitted account mapping, exact run status, all raw returned rows (including original `type` and `productType` values), and any explicit Dataset completeness evidence. Set `retrieval_complete` to `true` only with traceable host/Actor evidence that the Dataset was fully read; the helper checks only evidence-object shape and cannot authenticate its truth. Do not infer completeness from `SUCCEEDED`, a count below `resultsLimit`, an empty result, or no truncation marker. Missing pagination metadata or extra completeness flags do not block processing exact-Video records after retrieval, but do not claim a full time-window scan. If the run is `SUCCEEDED`, the Dataset has been fully read, and that Creator's raw returned row count is below `resultsLimit`, report: “已读完 Actor 返回的数据，配置的结果上限未达到。” This says only that the returned Dataset was read and the configured limit was not reached; it does not guarantee every post in the requested window was found. If the returned row count reaches the limit, say results may have been capped or truncated.
4. Run helper operation `select` with the exact Profile Posts field map and every per-run result. The project processing rule is exact and case-sensitive: only a row whose `type` value is the string `"Video"` and whose `url` is a usable Instagram post URL is a transcription candidate. This is the project owner's confirmed handling rule, not an enum guaranteed by the Actor schema; the public schema currently types `type` as a string without enum values. `productType` is not a gate. Do not use `isReel`, `productType`, URL shape, or field names to infer media type. Any missing, null, non-string, or other `type` value stays unresolved as unknown and is never sent to the Transcript Actor. Retain the row and report the actual type field presence/value. The Transcript Actor can process Reels and regular video posts, so do not distinguish them or require Reel classification. The helper reports `returned_raw_rows` as the Dataset row count only when a run maps to one Creator; it is `null` if multiple creators share a run and cannot be apportioned. `discovered_returned_in_window` counts attributable raw rows with usable identity/URL and timestamps inside the requested window, including duplicates, regardless of media type. `type_video_candidates` counts deduplicated exact-Video rows with usable URLs before the processing cap. `unknown_media_type` counts attributable in-window raw rows whose type is missing, null, non-string, or not exactly `"Video"`, including duplicate rows and regardless of URL usability. This count reports unknown type rows, not interface errors; it does not by itself make the run `partial_interface_error`. A confirmed `"Video"` row without a usable URL is a structural interface error. Also report selected and actually processed counts, and each discovery run status. Preserve unresolved identity/interface rows with actual evidence. Valid, attributable exact-Video rows may proceed even when pagination or extra completeness metadata is unavailable; preserve run status and returned rows without claiming a full scan. Do not send rows with unresolved identity, invalid required fields/URL, or unknown type. A missing discovery run means no rows were returned for that Creator in this attempt, while coverage and additional candidates remain unknown. Report unknown type values, unverified publication-time values, selected/processed videos, omitted candidates, failures, and partial/unknown coverage. Never describe `per_creator_limit` as a discovery cap or complete account scan.

Use the Profile Posts Actor's contracted post-publication field as the primary publication-time source. The current observed numeric values for Profile Posts `timestamp` are Unix seconds; set `timestamp_unit: "unix_seconds"` in `post_contract` only when the current type/unit evidence confirms it. Never infer a numeric unit from magnitude or a field name. The helper filters the UTC instant against its UTC window, then derives `published_at_local` and `published_at_utc` from that same instant; display the local value with its `display_timezone` and do not relabel UTC as local time. For an unknown or unparseable type, unit, or timezone, preserve the raw value and report `timestamp_unverified`; do not guess window membership or publication date. The Transcript Actor's string `timestamp` is run time, not publication time. Its numeric `createTime` is a post-time cross-check only after URL/ID reconciliation confirms the same record; the Profile Posts time remains authoritative.
5. Build Transcript batches only from selected, deduplicated URLs and only within a batch size supported by the current Transcript schema/account. Split internally when supported. Use the host's currently exposed tool and live argument schema; do not require `callOptions`, `maxTotalChargeUsd`, `maxItems`, or run-options readback. Do not hide these calls. Do not automatically retry, create replacement runs, expand the user's request, or interrupt discovery/transcription merely to ask about a budget. If a functional interface, authorization, batch, or read failure prevents remaining work, retain usable results and mark affected videos/account coverage partial.
6. Call helper operation `reconcile` only after at least one exact-Video candidate was selected, submitted to the Transcript Actor, and a result set/run status is available. If selection yields no exact-Video candidates (including when all returned media types are unknown), do not call the Transcript Actor or `reconcile`; the helper also rejects an empty submitted-candidate list. For a valid Transcript run, pass the complete submitted-candidate set and every returned transcript row to `reconcile`. It requires the exact `Video` mapping in `post_contract`, canonicalizes verified Instagram URL variants, uses only verified URL/code/pk fields, supports verified stable-ID fallback, and returns a status for every submitted post even when no row returned. It distinguishes explicit empty text, missing text, malformed rows, segment-only results, Actor errors, duplicate rows, identity conflicts, unmatched rows, and run/Dataset pending states. Never match by row order.
7. If the host exposes Dataset pagination and a reliable completion signal, read all pages and preserve that signal as completeness evidence. If it does not, do not claim discovery completeness. A `reconcile` success means a returned transcript row matched its submitted post; it does not establish that discovery or transcript Dataset reading was complete. Incomplete or unknown discovery runs may still supply validated exact-Video rows for transcription; preserve their status and keep report coverage partial/unknown. If a transcript run or Dataset is incomplete, preserve affected transcript results as pending/provisional. Preserve confidently matched partial results.

Keep Dataset total rows (`dataset_total`), rows the plugin/tool read (`result_count` or `returned_items`), and model-visible, parseable rows (`model_visible_rows`, normally the number of records actually present in `posts`) separate. In original OpenClaw Apify plugin v0.5.3, `resultCount` describes rows read into plugin memory, not rows visible to the model; do not use it as either the visible-row count or Dataset total.

Inspect the actual tool payload before `select`. An observed `[…truncated]` marker, OpenClaw `... N more characters truncated` marker, incomplete JSON, `truncated: true`, `hasMore: true`, evidence that a source row count exceeds model-visible rows, or an unread page means retrieval is explicitly incomplete: set discovery `retrieval_complete` to `false` and preserve the source and detail in `retrieval_complete_evidence`. `truncation_markers` is the list of non-empty marker strings actually observed; any non-empty valid list means incomplete, including marker text not previously known. With no incomplete signal but no reliable proof of the end, use `null`/unknown. In particular, the original OpenClaw Apify plugin v0.5.3 was observed to serialize Dataset output with a 50,000-character cap and no pagination or structured truncation signal; for that version, `SUCCEEDED`, `allDone`, `resultCount`, one successful `collect`, and `resultCount` below the Actor's `resultsLimit` do not prove complete retrieval.

For a paginated tool, continue from each `nextOffset` until a reliable terminal signal. `nextOffset` must be `null` or a non-negative integer (a Boolean is invalid); reject malformed values as unverified evidence. The current evidence contract recognizes normalized `next_offset_kind` values `exact` and `speculative` (trim surrounding whitespace and compare case-insensitively); unknown values cannot establish completeness. `speculative` permits probing but does not establish that another page exists. `next_offset_kind` describes the cursor from the page represented by that evidence; when claiming all pages were read, it must describe the terminal page. If an earlier page's speculative cursor is retained for audit, put it in a separate `prior_page_cursors` field rather than reusing the terminal page field; the helper preserves this field but does not validate its contents. A terminal page with `has_more: false` conflicts if `next_offset` is non-null or `next_offset_kind` is `speculative`; a matching `dataset_total` cannot override that conflict. Mark `retrieval_completeness_conflict` and never report `retrieval_complete: true` for it. The discovery field `retrieval_complete` is tri-state: `false` means positively incomplete, while `null` or omission means unknown. An explicit `false` remains `false` when evidence is insufficient; if it conflicts with otherwise reliable complete evidence, keep `false` and set `retrieval_completeness_conflict: true`. Set it to `true` only when JSON is complete and either `dataset_total` equals `model_visible_rows`, or all pages were actually read (`all_pages_read: true`) and the terminal page says `has_more: false`; there must be no truncation, cursor conflict, or count contradiction. A claimed `true` that conflicts with an observed incomplete signal stays fail-closed (`false` for explicit truncation, otherwise `null`) and sets the conflict flag. The normalized `retrieval_complete_evidence` object must include non-empty `source` and `detail`, and may also include `dataset_total`, `result_count`, `returned_items`, `model_visible_rows`, `truncated`, `truncation_marker_detected`, `truncation_markers`, `json_complete`, `has_more`, `all_pages_read`, `next_offset`, and `next_offset_kind`. The helper validates the current page's cursor types/consistency and count consistency; it preserves but does not validate historical `prior_page_cursors`, and cannot authenticate the source or truth of the host's evidence. This normalization reflects the repository evidence contract; it does not confirm a live plugin enum. Discovery `retrieval_complete` is distinct from Transcript `dataset_complete` and must not be copied between them.

A separately tested isolated plugin copy exposed pagination fields and read a Dataset 24/24 without a second truncation in the tested model response. That copy is not the official installed v0.5.3 plugin; do not describe the original plugin as having those capabilities or direct users to install the isolated copy.

### Analysis and report

Call the user-facing report “创作者视频洞察.” Analyze only Actor-returned transcript text. Keep that text distinct from generated summaries and analysis. Do not infer visuals, editing, product display, creator intent, audience reaction, or causation. Link each insight to its post URL and quote a short supporting transcript excerpt where useful.

**Daily Scan:** show the exact UTC window and timezone. For each Creator label `returned_raw_rows` as raw Dataset rows read, `discovered_returned_in_window` as attributable in-window raw rows with usable URLs (duplicates included), `unknown_media_type` as attributable in-window unknown-type raw rows (duplicates included; URL not required), and `type_video_candidates` as deduplicated usable-URL rows with exact `type == "Video"` before the local limit. Then show selected/processed videos, those omitted by the user limit, each discovery run status, and coverage/failure status. Because `"skipPinnedPosts": true` excludes pinned posts, do not label returned rows as all posts in the time window; give an excluded count only if the Actor provides a verifiable count. For each selected video show its URL, `published_at_local` with the explicit `display_timezone`, the UTC instant if useful, transcript status and, when available, transcript highlights, opening Hook, core point, speaking structure, delivery and closing/CTA. If the helper marks the source timestamp `timestamp_unverified`, retain its raw value and say publication time could not be verified; do not guess. Give a concise interpretation based on transcript evidence. Preserve post details when transcription fails.

**Weekly Review:** show the same coverage accounting. Summarize recurring topics, Hooks, speaking structures and CTAs only from successfully matched transcripts in this report. Link every pattern to representative posts and transcript evidence. Call out small samples and incomplete coverage; do not describe them as long-term trends.

Keep the default report readable: show transcript highlights and source-linked analysis rather than every full transcript inline. If asked to expand a video, provide its actual returned transcript separately, link its post, and label the transcript as Actor-returned text.

Never treat missing metrics as zero. Engagement counts, if returned, are optional collection-time context only; they must not replace or lead the report.

At the end, include a short copyable request containing the accounts, report mode, exact time range and per-creator limit. Do not imply that the Skill will remember settings or prior transcripts in another session.

### Privacy and safety

Process only user-specified public accounts. Respect Instagram, Apify and host access controls; do not bypass login, rate limits, or restrictions. Never request or reveal tokens, cookies, session IDs, passwords, or authorization headers. Persist the account list and per-creator limit only after explicit consent and only through supported host storage. Never persist transcript libraries or report history.
