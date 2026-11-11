---
name: instagram-media-links-and-post-insights
description: Return video/audio links or organize verified fields from user-provided public Instagram video posts and Reels. Also select this Skill for first-use Apify setup or when Apify MCP is unconnected or its authorization/readiness is unconfirmed; provide the host-specific guidance before stopping.
---

# Instagram Media Links & Post Insights

Get media links or a clear summary of fields actually returned for public Instagram video posts and Reels you provide. This Skill handles two tasks: **Media links** returns the `videoUrl` and `audioUrl` links the Actor provides; **Post insights** organizes or compares returned likes, comments, author, and publish-time fields. It does not download media files.

This Skill uses the [Instagram Video Scraper API Actor on Apify](https://apify.com/apple_yang/instagram-video-scraper-api).

## Example requests

**Media links**

```text
Return the video and audio links actually provided for this public Instagram Reel. Keep the original URL with the result, and say if either field is missing.
[INSTAGRAM_URL]
```

**Post insights**

```text
Organize the author, publish time, likes, and comments actually returned for these public Instagram video posts or Reels. Compare only the returned raw counts. Do not calculate rates or infer trends, audience response, performance changes, or causes.
[INSTAGRAM_URLS]
```

If the user requests both, return both sets of fields from one Actor result where possible. For an unclear request, ask whether they want media links, post fields, or both. Read [the workflow reference](references/workflow.md) before processing a request.

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

Codex Skill 和 Apify 插件是两项安装。先安装本 Skill 的完整目录：在 Codex 会话中若可用 `$skill-installer`，请求它从 `https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-media-links-and-post-insights` 以 Git 方式安装到 `~/.agents/skills/instagram-media-links-and-post-insights/`，目标已存在就停止不覆盖；若已有本地仓库，可把 `skills/instagram-media-links-and-post-insights/` 完整文件夹放入当前项目 `.agents/skills/`，或用户级 `~/.agents/skills/`。OpenAI 的[官方 Codex Skill 目录说明](https://developers.openai.com/api/reference/cli#use-the-cli-from-a-coding-agent)列出了这两个位置。开始新会话，并明确调用 `$instagram-media-links-and-post-insights`。就绪信号是新会话能发现该 Skill，且 Apify 工具和所需操作实际可用。

**Codex 桌面端：**在 ChatGPT 桌面应用左上角切换到 **Codex**；侧栏打开 **Plugins（插件）**，点 **+** 旁下拉菜单 → **Add marketplace（添加市场）**，Source 输入 `apify/apify-codex-plugin` 并添加。打开 **Personal** 页，在 Apify Plugin 下点 **Add** → **Add to Codex** → **Install Apify**；浏览器打开 Apify OAuth 后检查权限并点 **Allow access**。

**Codex CLI：**在 Codex CLI 输入 `/plugins`；选择 **Add Marketplace**，输入 `apify/apify-codex-plugin` 并确认；打开 **Apify Plugin** 页，选 Apify → **Install plugin**。首次调用需授权的 Apify 工具时，浏览器会打开 OAuth；检查权限并点 **Allow access**。两个 Codex 环境是不同设置入口，不要把桌面步骤用于 CLI 或反之。随后在新会话显式调用 `$instagram-media-links-and-post-insights`，并确认工具可用。详见[Codex 指南](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/codex.md)、[Apify Codex 桌面端指南](https://docs.apify.com/integrations/codex-app)和[Apify Codex CLI 指南](https://docs.apify.com/integrations/codex-cli)。

### Claude Web 与 Claude Desktop 聊天

**安装本 Skill：**在 Claude 左侧 **Customize（自定义；部分账号正在改为 Plugins/插件）→ Skills（技能）→ + → Create skill（创建技能）→ Upload a skill（上传技能）**，上传信任的 Skill ZIP，完成扫描并启用。企业管理员可限制代码执行、创建和上传权限；若看不到入口，查看[Claude Skills 官方说明](https://support.claude.com/en/articles/12512180-use-skills-in-claude)。

**连接 Apify：**在 Claude 左侧打开 **Customize/Plugins → Connectors（连接器）**，找到官方 Apify Plugin 并点 **Add（添加）**（正在逐步上线的新界面可能以 Plugins 页面和筛选器显示）。在 Apify 插件页打开 **Connectors**，对 `apify` 连接点 **Connect**；在对话框选择 **Continue → Add**，在浏览器的 Apify 授权页核对账号与权限并点 **Allow access**。检查连接显示 connected。新聊天中通过输入框 **+** 菜单启用 Apify Connector，再输入 `/` 选择本 Skill（若当前界面提供该选择器）；也可在请求中明确点名本 Skill。桌面版常规聊天使用同一 Claude 账号的设置；不要把 Claude Code CLI 的命令用于 Claude Desktop 聊天。若企业工作区限制连接器，由管理员配置。详见[Claude 指南](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/claude-web.md)、[Apify Claude.ai 指南](https://docs.apify.com/integrations/claude-ai)和[Anthropic 远程 MCP 说明](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)。

### Claude Code CLI

Claude Code CLI 与 Claude Desktop 聊天是不同产品。先在 Claude Web/Desktop 账号中按上方步骤安装并启用本 Skill；在已登录同一 `claude.ai` 账号且版本支持 Skills 同步的本地 Claude Code CLI 新会话中运行 `/skills`，确认它显示在 `claude.ai sync` 下，再用 `/` 选择显示的 Skill 命令。也可将本 Skill 的完整目录放入 `~/.claude/skills/instagram-media-links-and-post-insights/`。然后在 Claude Code CLI 中运行 `/plugin install apify`，选择安装范围；运行 `/mcp`，启用 `plugin:apify:apify` 并选择 **Authenticate**，在浏览器登录 Apify、检查权限并点 **Allow access**。`/mcp` 中连接状态和会话实际暴露工具是就绪检查；随后在新会话调用本 Skill。Apify 当前文档确认 Claude Code CLI 路径；不把它外推到 Claude 桌面应用的 Code tab 或 Web/远程代码会话。参阅[Claude Code Skills](https://code.claude.com/docs/en/skills)、[Apify Claude Code CLI 指南](https://docs.apify.com/integrations/claude-code-cli)和[项目 Claude 指南](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/claude-web.md)。

### Manus

**连接 Apify：**打开 **Settings（设置）→ Connectors（连接器）→ + Add connectors → Custom MCP → + Add custom MCP → Direct configuration（直接配置）**。填写 **Server name（服务器名称）** `Apify`、**Transport type（传输类型）** `HTTP`、**Server URL（服务器地址）** `https://mcp.apify.com`，点 **Save**。在聊天中首次调用 Apify 工具时，按 Manus 弹出的 OAuth 流程登录并授权；不要改用 API token。检查连接已保存且工具在当前会话可用。

**安装本 Skill 并调用：**打开 **Skills → + Add → Import from GitHub**，粘贴仓库中本 Skill 文件夹的公开 GitHub URL：`https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-media-links-and-post-insights`，点 **Import**；确认 Skill 出现在个人列表并启用。新任务中在输入框键入 `/` 选择本 Skill，并通过输入区下方的连接器按钮开启 Apify。就绪前须看到 Skill 可选且 Apify 连接开启。Manus 官方说明 MCP 在各计划均可用，但账号权限、界面更新和任务结果仍可能不同。详见[项目 Manus 指南](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/manus.md)、[Apify Manus 指南](https://docs.apify.com/integrations/manus)与[Manus Skills 指南](https://help.manus.im/en/articles/14753565-how-to-share-and-use-skills-in-manus)。

### OpenClaw

先安装本 Skill，再配置 Apify 插件。本 Skill 尚未发布到 ClawHub；先将仓库克隆到 OpenClaw Gateway 所在环境，然后从仓库根目录运行 `openclaw skills install ./skills/instagram-media-links-and-post-insights --global`，仅限当前工作区时去掉 `--global`。需要 OpenClaw 2026.1.0 或更新版本，以及 Node.js 22+；详见[当前 Apify 插件要求](https://docs.apify.com/integrations/openclaw)。运行 `openclaw skills check` 检查默认 Agent，开新会话并使用 `$instagram-media-links-and-post-insights`。若不知道自己的目录/Agent 权限，不猜配置，查看[项目 OpenClaw 指南](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/openclaw.md)及其官方链接。Apify 插件采用 OpenClaw 独立配置流程，不是 OAuth；完成下方原有 OpenClaw 引导后，在新会话确认 `apify` 工具可见。不要在聊天中发送 API Key。

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

Do not start an Actor until a usable Apify tool and required schema are visible and explicit host status does not report missing authorization. If readiness remains unclear, stop and direct the user to the corresponding setup guidance above. The Skill cannot install plugins or change host settings.

## Actor preflight and input

Before telling the user that processing will begin, complete the internal preflight in [the workflow reference](references/workflow.md). Do not first say “I’ll process these” or imply a run has started. Use only `apple_yang/instagram-video-scraper-api`. A visible Apify connection or OAuth success does not by itself confirm that this Actor's tool, schema, or result-reading tools are exposed.

The preflight must establish a supported tool path, the current input/output contract, a way to submit the user URLs in the required `videoUrls` array, and a way to obtain actual result rows. For a dedicated tool, verify that its live description/schema identifies the exact target owner and Actor; similar names or an unclear identity are insufficient. If any required capability is absent or unclear, stop before an Actor call. Tell the user which tool or capability is missing, and state that no Actor was started and no results were received. If the host is ChatGPT, then display the complete ChatGPT first-use guidance above; do not replace it with generic settings/search wording or a link-only reply. Do not infer that a public Actor is callable, guess tool names/arguments/Actor identifier format/result envelopes, use another Actor, or bypass the host with HTTP, shell, tokens, or `sessionid`.

Preserve each input URL exactly as supplied and its original order. Use one call for a single request or one batch call when supported. For combined Media links and Post insights requests, use one input set and one Actor result where possible; do not repeat calls without a task need. Never use API tokens, `sessionid`, shell commands, or direct HTTP requests to bypass host tools. Do not call another Actor.

## Media type and links

- Do not infer media type from URL path. `/p/` identifies a post path, not a video. Use only the user's stated intent and evidence in the Actor result.
- If media type is unknown, or no video/audio direct link is returned, say that support for this content cannot be confirmed. Do not guess or promise a link.
- Do not claim photo or carousel posts are supported or unsupported; they remain unverified and outside the first-release commitment.
- A returned `videoUrl` or `audioUrl` means the Actor supplied a direct link. It does not mean the Skill downloaded a file or that the link will remain valid.

## Post insights boundaries

Organize or compare only raw fields actually returned and otherwise verified, such as `likeCount`, `commentCount`, author fields, `createTime`, and `timestamp`. Treat each run as a snapshot of that collection. Do not promise or infer `views`, play count, impressions, reach, follower counts, shares, saves, or other unverified fields. Do not calculate engagement rates or other derived metrics needing unverified inputs. Do not infer trends, audience response, performance changes, or causation, and do not present a simple count comparison as a validated business conclusion. Missing fields are not zero.

## Match and report every input

Follow [the workflow reference](references/workflow.md). Match a result to an input using a verifiable match on the returned `url`. Do not rely on `code`, `pk`, or `id` unless their matching behavior has been independently verified for the current contract. Do not match by output order. Preserve exact input strings; do not merge URLs using unverified normalization. Deduplicate only exact identical strings, and retain their input positions.

Report each input separately and distinguish:

1. A non-empty `errMsg`: quote/report the actual returned message without adding a cause.
2. Empty or missing `errMsg`: state that the field is empty or missing; do not infer success from it.
3. No reliably matching result row: say “未收到可匹配的结果” / “No matching result was received”; do not say the Actor failed or the post does not exist.
4. A matched row with a missing, empty, or unreturned field: say that field is “未返回/不可用” / “not returned or unavailable”; do not interpret missing links as proof media does not exist or missing counts as zero.
5. Missing, conflicting, or multiple candidate URLs: say “对应关系待确认” / “input-to-result mapping needs confirmation”. Never guess by position.
6. Partial batch results: show each confirmed, errored, unmatched, and unresolved item; do not say the batch fully succeeded.

Do not assume top-level error formats, batch order guarantees, or that `errMsg` is always present. Report only the tool result actually visible to the host. If the result cannot establish media type, state that support cannot be confirmed.

## Scope and privacy

Handle only public video post and Reel URLs supplied by the user. Private accounts, Stories, and authentication-required content are outside the supported scope. Do not discover account posts, monitor on a schedule, extract transcripts, interpret visuals, or download/save media files. Do not ask for or expose passwords, API keys, cookies, or session IDs. Do not include fixed prices or estimates; if asked about usage, direct the user to their Apify Console. The user is responsible for following applicable service terms, copyright, and privacy requirements; do not give legal conclusions.
