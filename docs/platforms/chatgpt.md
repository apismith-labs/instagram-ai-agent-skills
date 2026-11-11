# Use Instagram Skills in ChatGPT

## Before you start

You need your own [Apify account](https://console.apify.com/). Actor runs use the allowance and billing terms of that account; the [Apify Console](https://console.apify.com/) shows current Runs and billing details. One Apify MCP connection can be shared by multiple Skills; you do not create a separate connection for each Skill.

ChatGPT Skills availability depends on account, workspace, administrator settings, and product rollout. OpenAI currently lists eligible Business, Enterprise, Healthcare, and Edu users for Skills, subject to workspace settings and product availability; this project's reported Plus observation is account-level evidence only. If the Skills page or upload option is unavailable, check the [official Skills guide](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) and your workspace administrator.

## 1. Add and authorize the Apify MCP connection

Apify connection and Skill installation are separate steps. The Apify connection gives ChatGPT access to external Apify tools; each Skill supplies its own task workflow.

1. 在 ChatGPT 打开 **Plugins（插件）→ + → Add custom MCP server（添加自定义 MCP 服务器）**。
2. 填写 **Name（名称）** `Apify MCP` 和 **Server URL（服务器地址）** `https://mcp.apify.com`。
3. 选择 **OAuth**。
4. 阅读风险提示、勾选确认框，然后选择 **Create as a plugin（创建为插件）**。
5. 随后按 ChatGPT 提示登录 Apify 并批准授权。
6. 检查发现的工具，再安装生成的 **Apify MCP** 插件/App。

该 Apify MCP 连接可供多个 Skill 共用；每个 Skill 仍需单独安装。不要在聊天中发送 API Key 或其他凭据。

Before a task, confirm the current connection exposes the target Actor call, its live input schema, run-status information, and a way to read the Actor's Dataset results. Do not assume every account or workspace has the same tool list. If a required capability is missing, do not start the task through a different Actor or authentication route.

These steps follow the current [OpenAI custom MCP server guide](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt) and [Apify MCP guide](https://docs.apify.com/mcp), which recommends hosted OAuth for remote connections. OpenAI's public documentation currently lists full custom MCP support for ChatGPT Business and Enterprise/Edu; Business creation is limited to admins and owners, while Enterprise/Edu admins can grant selected members permission to create connections. The same OpenAI guide says Pro users can connect custom MCP servers with read/fetch permissions. The public [Skills guide](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) separately lists eligible Business, Enterprise, Healthcare, and Edu users, subject to workspace settings and product availability. This project has observed one successful custom Apify MCP connection and third-Skill task on its owner's ChatGPT Plus account under the product state at test time. That account-level observation differs from the plans explicitly listed in public documentation; it does not establish general Plus availability or override plan, workspace, region, administrator, or product-rollout restrictions. If the option is unavailable, check current account/workspace access and the official guides; do not assume every Plus account has the same capability.

## 2. Upload a Skill package

Download `instagram-transcript-extractor-v0.2.2.zip` from the [v0.2.2 Release asset](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.2/instagram-transcript-extractor-v0.2.2.zip), or open the [v0.2.2 Release page](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/tag/v0.2.2) and choose that named file under **Assets**. Do not download GitHub's automatically generated **Source code (zip)**. Optional SHA-256 for the Transcript Extractor v0.2.2 ZIP:

```text
2bea93a3ffe3802acd302a2788ef03d07e1933dbb2ea66b57d97f24cf6f04f41
```

Keep the downloaded ZIP intact; do not unzip it before upload. In ChatGPT, open **Plugins → Plugin Directory → Skills → Create → Upload from your computer**, then select `instagram-transcript-extractor-v0.2.2.zip`. Wait for the upload scan. The Skill may become **Available**, show **Needs Review**, or show **Blocked**:

- **Available:** continue to a new conversation.
- **Needs Review:** read the displayed prompt and follow the review step before using it.
- **Blocked:** the Skill cannot be used in that state. The scan status alone does not show that the ZIP is damaged. Avoid repeatedly uploading the same ZIP. Note the release version and scan message, then [open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues) for help. Do not include credentials or personal sensitive information.

### Upload Creator Video Insights

Download the named GitHub Release asset [`instagram-creator-reels-insights-v1.0.2.zip`](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.2/instagram-creator-reels-insights-v1.0.2.zip), not GitHub's automatically generated **Source code (zip)**. Keep it intact. In ChatGPT, use **Plugins → Plugin Directory → Skills → Create → Upload from your computer** and select this ZIP. Check the upload scan: it may be **Available**, **Needs Review**, or **Blocked**, as described above. Using the Creator report workflow through ChatGPT and Apify has not been confirmed in this project.

Optional SHA-256 for the Creator Video Insights v1.0.2 ZIP:

```text
714de0c189e915f8555d055e54fb88f8796f030f2b3be6c031acb0525306b99b
```

## 3. 在新聊天中使用 Skill

**普通聊天：**OpenAI 官方说明已安装的 Skill 可在相关时自动使用；为明确表达意图，请在请求中写出 Skill 名称及任务。官方文档没有规定普通聊天必须使用 `@` 选择 Skill。

**ChatGPT 工作模式：**本项目收到过一次账号级验证，观察到在输入框键入 **@** 可选择 `Apify MCP`，并在请求中点名 Skill。官方公开说明没有保证所有账号、工作区或产品状态都提供此选择器，所以只在界面实际出现时使用。

两种模式都应在发出任务前确认该 Skill 已启用，Apify 连接已授权，当前会话显示可用工具。ChatGPT 的普通聊天和工作模式不能假定共享完全相同的选择流程。

For example, replace the sample URL with a real public Instagram Reel or supported video post link:

```text
Use Instagram Transcript Extractor to get the transcript of this public Instagram Reel:
https://www.instagram.com/reel/REPLACE_WITH_A_REAL_LINK/
```

### Creator Video Insights

For a multi-creator review, use this request:

```text
Use Instagram Creator Video Insights to review [CREATOR_1] and [CREATOR_2] for the most recent 7 days. Give each creator a separate section. Base findings only on transcripts actually returned and link each finding to its source post. Compare creators only where the returned transcripts support it. If results are partial or unknown, explain that they may be incomplete; do not treat no returned posts as proof that no posts were published.
```

Analyze only content returned through your connected tools.

## Copyable requests

Replace every placeholder shown, including each `PUBLIC_INSTAGRAM_URL` and `[TARGET_LANGUAGE]`, with an accessible public Instagram link or your target language. In regular chat, explicitly name Instagram Transcript Extractor in your request; in Work mode, use the **@** `Apify MCP` picker only if it appears in your account. These examples are not guarantees that every link will succeed.

**Single transcript**

```text
Use Instagram Transcript Extractor to return the original-language transcript for this public Instagram video. Include only timestamp segments actually returned by the tool; do not invent timestamps.
PUBLIC_INSTAGRAM_URL_1
```

**Batch transcripts**

```text
Use Instagram Transcript Extractor on exactly these public Instagram links:
1. PUBLIC_INSTAGRAM_URL_1
2. PUBLIC_INSTAGRAM_URL_2
For each input, return its original URL, processing status, original-language transcript, and timestamp segments if available. Match results by URL, never by result order. Do not add links or retry automatically.
```

**Subtitle file (SRT/VTT)**

```text
Transcribe this video and create an SRT or VTT file only if you can export files and the tool returned valid timestamps. Otherwise give me copyable subtitle text using only valid timestamps, or explain that timed subtitles are unavailable. Do not invent timestamps.
PUBLIC_INSTAGRAM_URL_1
```

**Translation**

```text
Return the original-language transcript for this video, then provide a separate [TARGET_LANGUAGE] translation. Preserve any timestamp segments actually returned; do not invent them.
PUBLIC_INSTAGRAM_URL_1
```

**Summary**

```text
Transcribe each video and give each link its own short summary. Keep the videos separate and match every result to its original URL.
1. PUBLIC_INSTAGRAM_URL_1
2. PUBLIC_INSTAGRAM_URL_2
```

**Content analysis**

```text
Based only on the transcript of this video, identify its hook, core insight, CTA, and content cues. Include timestamps only where valid timestamp segments were returned. Do not analyze visuals, engagement metrics, or audience response.
PUBLIC_INSTAGRAM_URL_1
```
