# Use Instagram Skills in ChatGPT

## Before you start

You need your own [Apify account](https://console.apify.com/). Actor runs use the allowance and billing terms of that account; the [Apify Console](https://console.apify.com/) shows current Runs and billing details. One Apify MCP connection can be shared by multiple Skills; you do not create a separate connection for each Skill.

ChatGPT Skills availability depends on account, workspace, administrator settings, and product rollout. OpenAI currently lists eligible Business, Enterprise, Healthcare, and Edu users for Skills, subject to workspace settings and product availability; this project's reported Plus observation is account-level evidence only. If the Skills page or upload option is unavailable, check the [official Skills guide](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) and your workspace administrator.

## 1. Add and authorize the Apify MCP connection

Apify connection and Skill installation are separate steps. The Apify connection gives ChatGPT access to external Apify tools; each Skill supplies its own task workflow.

1. In ChatGPT, open **Plugins → + → Add custom MCP server**.
2. Set **Name** to `Apify MCP` and **Server URL** to `https://mcp.apify.com`.
3. Select **OAuth**.
4. Read the risk notice, check the confirmation box, and select **Create as a plugin**.
5. Follow ChatGPT's prompts to sign in to Apify and authorize access.
6. Check the discovered tools, then install the generated **Apify MCP** plugin/App.

One Apify MCP connection can be shared by multiple Skills; each Skill must still be installed separately. Never send an API key or other credential in chat.

Before a task, confirm the current connection exposes the target Actor call, its live input schema, run-status information, and a way to read the Actor's Dataset results. Do not assume every account or workspace has the same tool list. If a required capability is missing, do not start the task through a different Actor or authentication route.

These steps follow the current [OpenAI custom MCP server guide](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt) and [Apify MCP guide](https://docs.apify.com/mcp), which recommends hosted OAuth for remote connections. OpenAI's public documentation currently lists full custom MCP support for ChatGPT Business and Enterprise/Edu; Business creation is limited to admins and owners, while Enterprise/Edu admins can grant selected members permission to create connections. The same OpenAI guide says Pro users can connect custom MCP servers with read/fetch permissions. The public [Skills guide](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) separately lists eligible Business, Enterprise, Healthcare, and Edu users, subject to workspace settings and product availability. This project has observed one successful custom Apify MCP connection and third-Skill task on its owner's ChatGPT Plus account under the product state at test time. That account-level observation differs from the plans explicitly listed in public documentation; it does not establish general Plus availability or override plan, workspace, region, administrator, or product-rollout restrictions. If the option is unavailable, check current account/workspace access and the official guides; do not assume every Plus account has the same capability.

## 2. Upload a Skill package

GitHub Release ZIPs and ClawHub listings are separate distribution channels with independent version numbers. The Transcript Extractor GitHub ZIP is v0.2.3; its ClawHub listing is v1.0.5. The Media Links & Post Insights GitHub ZIP is v1.0.0; its ClawHub listing is v1.0.2. Creator's GitHub ZIP and ClawHub listing are both v1.0.5; its current workflow remains in development and unverified.

Download `instagram-transcript-extractor-release-v0.2.3.zip` from the [v0.2.3 Release asset](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.3/instagram-transcript-extractor-release-v0.2.3.zip), or open the [v0.2.3 Release page](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/tag/v0.2.3) and choose that named file under **Assets**. Do not download GitHub's automatically generated **Source code (zip)**. Optional SHA-256 for the Transcript Extractor v0.2.3 ZIP:

```text
71b7531bb0b7e5413d6afc0a1d3430f77f836a0e1ba82b52a057fd5175a78a66
```

Keep the downloaded ZIP intact; do not unzip it before upload. In ChatGPT, open **Plugins → Plugin Directory → Skills → Create → Upload from your computer**, then select `instagram-transcript-extractor-release-v0.2.3.zip`. Wait for the upload scan. The Skill may become **Available**, show **Needs Review**, or show **Blocked**:

- **Available:** continue to a new conversation.
- **Needs Review:** read the displayed prompt and follow the review step before using it.
- **Blocked:** the Skill cannot be used in that state. The scan status alone does not show that the ZIP is damaged. Avoid repeatedly uploading the same ZIP. Note the release version and scan message, then [open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues) for help. Do not include credentials or personal sensitive information.

### Upload Creator Video Insights

Download [`instagram-creator-video-insights-v1.0.5.zip`](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.5/instagram-creator-video-insights-v1.0.5.zip) from the [v1.0.5 Release asset](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/tag/v1.0.5), then upload it using **Plugins → Plugin Directory → Skills → Create → Upload from your computer**; choose the named asset, not GitHub's automatically generated **Source code (zip)**. The current Creator workflow remains in development and unverified, and its ChatGPT report workflow has not been confirmed in this project.

SHA-256 for the Creator Video Insights v1.0.5 ZIP:

```text
81c2e5afae4f68d2e576dcc40e05ace9c2be7838df24be43ca7bc94f46e28c51
```

Historical SHA-256 for the earlier Creator Video Insights v1.0.2 ZIP:

```text
714de0c189e915f8555d055e54fb88f8796f030f2b3be6c031acb0525306b99b
```

### Instagram Media Links & Post Insights

Download the named [`instagram-media-links-and-post-insights-release-v1.0.0.zip` GitHub Release asset](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/instagram-media-links-and-post-insights-v1.0.0/instagram-media-links-and-post-insights-release-v1.0.0.zip), not GitHub's automatically generated **Source code (zip)**. Its optional SHA-256 is:

```text
e9d5d77b6e87a17cba91c4a170ef4b59e7179150b37bb1b0bc2d49854c5842f7
```

Upload the ZIP using **Plugins → Plugin Directory → Skills → Create → Upload from your computer**. This GitHub ZIP v1.0.0 is separate from the ClawHub v1.0.2 listing. See the [Media Links & Post Insights user guide](../skills/instagram-media-links-and-post-insights.md) for its scope and limitations.

## 3. Use a Skill in a new chat

**Regular chat:** OpenAI says an installed Skill may be selected automatically when relevant. To make your intent clear, name the Skill and task in your request. OpenAI's public documentation does not require using `@` to select a Skill in regular chat.

**ChatGPT Work mode:** In one account-level project test, typing **@** in the input box showed `Apify MCP` as a selectable connection, which the user then named in the request. OpenAI's public documentation does not guarantee this picker is available in every account, workspace, or product state, so use it only when it appears in your interface.

In either mode, before starting a task, confirm the Skill is enabled, the Apify connection is authorized, and the current chat exposes the needed tools. Do not assume regular chat and Work mode have the same selection flow.

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
