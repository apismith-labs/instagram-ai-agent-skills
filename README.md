# Instagram AI Agent Skills

A collection of independent AI agent Skills for working with public Instagram video content. Each Skill has its own scope and installation path; this repository is not a single Skill that installs every feature automatically.

## Choose a Skill

Browse the [user guide and platform installation index](docs/README.md) for all setup guides.

**Instagram Transcript Extractor** (`instagram-transcript-extractor`) gets spoken-word transcripts from public Instagram Reels and videos, with transcript-based summaries, translation, and text analysis.

- **Available:** [GitHub ZIP v0.2.1](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.1/instagram-transcript-extractor-v0.2.1.zip) · [ClawHub 1.0.1](https://clawhub.ai/apismith-labs/skills/instagram-transcript-extractor)
- **Start here:** [Platform instructions](#install-by-platform) · [Installation entry](#install-instagram-transcript-extractor) · [User guide](docs/skills/instagram-transcript-extractor.md) · [Copy-ready prompts](#instagram-transcript-extractor)

**Instagram Creator Reels Insights** (`instagram-creator-reels-insights`) reviews recent public videos and creates source-linked Daily Scan or Weekly Review reports from returned transcripts.

- **Available:** [GitHub ZIP v1.0.1](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.1/instagram-creator-reels-insights-v1.0.1.zip) · [ClawHub 1.0.1](https://clawhub.ai/apismith-labs/skills/instagram-creator-reels-insights)
- **Start here:** [Platform instructions](#install-by-platform) · [Creator installation entry](#instagram-creator-reels-insights) · [User guide](docs/README.md) · [Copy-ready examples](#instagram-creator-reels-insights-prompts)

## Install by platform

Choose one Skill, then follow its platform-specific setup. The steps below walk through ChatGPT, Claude Web, and OpenClaw; the Skill-specific route tables also point to Codex, Manus, Claude Desktop, and Claude Code instructions. Installing a Skill does not connect Apify. For direct routes, jump to [Transcript Extractor](#install-instagram-transcript-extractor) or [Creator Reels Insights](#instagram-creator-reels-insights).

### Named GitHub Skill ZIPs

For the ChatGPT and Claude Web upload steps below, choose the package for the Skill you want. The named Release ZIPs are separate from GitHub's automatically generated **Source code (zip)**.

| Skill | GitHub Release ZIP |
| --- | --- |
| Instagram Transcript Extractor | [`instagram-transcript-extractor-v0.2.1.zip`](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.1/instagram-transcript-extractor-v0.2.1.zip) · [Release v0.2.1](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/tag/v0.2.1) |
| Instagram Creator Reels Insights | [`instagram-creator-reels-insights-v1.0.1.zip`](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.1/instagram-creator-reels-insights-v1.0.1.zip) · [Release v1.0.1](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/tag/v1.0.1) |

### ChatGPT

**Connect Apify:** Add and authorize the Apify custom MCP server using the [ChatGPT connection steps](docs/platforms/chatgpt.md#1-connect-and-authorize-apify). This connects the plugin; it is separate from the Skills ZIP upload page.

**Upload a Skill ZIP:** At **Plugins → Plugin Directory → Skills → Create → Upload from your computer**, upload the named ZIP for the Skill you want. Follow the [ChatGPT upload steps](docs/platforms/chatgpt.md#2-upload-a-skill-package). Keep the ZIP intact; do not select GitHub's automatic **Source code (zip)**. After upload, check the scan result (**Available**, **Needs Review**, or **Blocked**).

In a new conversation, select the Apify plugin with **@** and name the Skill in your request. Skills are documented for eligible ChatGPT Business, Enterprise, Healthcare, and Edu users, subject to workspace settings and product availability; see OpenAI's [Skills in ChatGPT guide](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) and the [project ChatGPT guide](docs/platforms/chatgpt.md).

Use the [named ZIP package table](#named-github-skill-zips) above to download the GitHub Release ZIP for the Skill you want.

### Claude Web

Connect the Apify Web Connector and complete OAuth. Upload the named ZIP for the Skill you want at **Customize → Skills → Add → Upload skill**; keep it intact, review its preview, and enable it. In a new conversation, select the Skill and enable the Apify Connector. Do not use GitHub's automatic **Source code (zip)**. See the [Claude guide](docs/platforms/claude-web.md).

Upload the selected package from the [named ZIP package table](#named-github-skill-zips) above.

### OpenClaw

Install from ClawHub in the same environment as your OpenClaw Gateway (the service or environment running your OpenClaw agents). By default the OpenClaw CLI installs to the active workspace's `skills/` directory; add `--global` for the shared managed Skills directory. Check the default Agent with `openclaw skills check`, or specify one with `openclaw skills check --agent YOUR_AGENT_ID`. In a new session, select the Skill using its `$` name. Follow the [OpenClaw Skills CLI documentation](https://docs.openclaw.ai/cli/skills) and the [project OpenClaw guide](docs/platforms/openclaw.md) for workspace troubleshooting, the Apify plugin, and Transcript Extractor's other install sources.

## Skill-specific installation routes

The platform sections above describe ZIP upload and shared OpenClaw setup. These tables match each platform to the correct package, slug, source folder, or account-sync route. Follow the linked guide for full steps; an installation route alone does not confirm the task workflow.

### Install Instagram Transcript Extractor

Choose the route for your platform. GitHub ZIP and ClawHub versions are separate channels. Codex uses the moving `main` source branch, not either package version. On the project Gateway, GitHub-source/local-directory visibility does not confirm an Apify transcript task; Control UI and ClawHub installation are not confirmed.

| Platform | Transcript Extractor entry |
| --- | --- |
| ChatGPT | Upload [`instagram-transcript-extractor-v0.2.1.zip`](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.1/instagram-transcript-extractor-v0.2.1.zip) using the [ChatGPT steps](#chatgpt). |
| Claude Web | Upload [`instagram-transcript-extractor-v0.2.1.zip`](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.1/instagram-transcript-extractor-v0.2.1.zip) using the [Claude Web steps](#claude-web). |
| OpenClaw | ClawHub 1.0.1: [`@apismith-labs/instagram-transcript-extractor`](https://clawhub.ai/apismith-labs/skills/instagram-transcript-extractor) · `openclaw skills install @apismith-labs/instagram-transcript-extractor`. [Guide](docs/platforms/openclaw.md#instagram-transcript-extractor). |
| Codex desktop app / CLI | Use the GitHub [`skills/instagram-transcript-extractor`](https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-transcript-extractor) folder with [Codex install instructions](docs/platforms/codex.md#install-the-skill). |
| Manus | Import the GitHub folder [`skills/instagram-transcript-extractor`](https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-transcript-extractor) using [Transcript Extractor import steps](docs/platforms/manus.md#2-import-and-enable-the-skill). |
| Claude Desktop regular chat | Enable in Claude Web, then sync through the same account; see [Transcript Extractor steps](docs/platforms/claude-web.md#use-instagram-transcript-extractor-in-claude-desktop-regular-chat). |
| Claude Code | Same-account sync or extract the named [Transcript Extractor v0.2.1 ZIP](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.1/instagram-transcript-extractor-v0.2.1.zip) and follow the [Claude Code steps](docs/platforms/claude-web.md#claude-code). |

### Instagram Creator Reels Insights

Choose the route for your platform. These install paths do not imply that the full Creator task workflow is confirmed in each environment. Its named GitHub ZIP can be uploaded where Skill-package uploads are supported; the [Claude Code guide](docs/platforms/claude-web.md#creator-reels-insights-in-claude-code) separately documents extracting its top-level folder into the local Skills directory. OpenClaw uses ClawHub, not the GitHub ZIP; the ClawHub route and full task flow remain unconfirmed in the project Gateway. See the [Creator OpenClaw guide](docs/platforms/openclaw.md#instagram-creator-reels-insights).

| Platform | Creator Reels Insights entry |
| --- | --- |
| ChatGPT | Upload [`instagram-creator-reels-insights-v1.0.1.zip`](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.1/instagram-creator-reels-insights-v1.0.1.zip) using the [ChatGPT steps](#chatgpt). |
| Claude Web | Upload [`instagram-creator-reels-insights-v1.0.1.zip`](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.1/instagram-creator-reels-insights-v1.0.1.zip) using [Creator steps](docs/platforms/claude-web.md#use-creator-reels-insights-in-claude-web). |
| OpenClaw | ClawHub 1.0.1: [`@apismith-labs/instagram-creator-reels-insights`](https://clawhub.ai/apismith-labs/skills/instagram-creator-reels-insights) · `openclaw skills install @apismith-labs/instagram-creator-reels-insights`. [Details](docs/platforms/openclaw.md#instagram-creator-reels-insights). |
| Codex desktop app / CLI | Use the separate GitHub [`skills/instagram-creator-reels-insights`](https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-creator-reels-insights) folder with [Creator install instructions](docs/platforms/codex.md#install-creator-reels-insights). |
| Manus | Import the separate GitHub folder [`skills/instagram-creator-reels-insights`](https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-creator-reels-insights) using [Creator import instructions](docs/platforms/manus.md#use-creator-reels-insights). The report workflow is not confirmed in Manus. |
| Claude Desktop regular chat | Enable Creator in Claude Web, sign in to Desktop with the same account, and select `instagram-creator-reels-insights`; the report workflow is not confirmed there. See [Creator Desktop steps](docs/platforms/claude-web.md#use-creator-reels-insights-in-claude-desktop-regular-chat). |
| Claude Code | Same-account sync or extract the top-level folder from the [v1.0.1 ZIP](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.1/instagram-creator-reels-insights-v1.0.1.zip); see [Creator Claude Code steps](docs/platforms/claude-web.md#creator-reels-insights-in-claude-code). Installation and task flow are not confirmed there. |

## Connect Apify and check usage

Apify connection steps vary by platform: use the [ChatGPT MCP setup](docs/platforms/chatgpt.md#1-connect-and-authorize-apify), [Claude Web setup](docs/platforms/claude-web.md), [Codex setup](docs/platforms/codex.md), or [Manus setup](docs/platforms/manus.md). OpenClaw uses its separately installed [Apify plugin](docs/platforms/openclaw.md#set-up-the-apify-plugin). Never paste credentials into chat. Runs use your Apify account and the Actors' current billing rules. More creators or videos may increase usage; check actual usage in [Apify Console](https://console.apify.com/). No fixed fee or fee cap is promised.

## Copy-ready prompts

Replace each placeholder with a public Instagram URL or creator username that you want to use.

### Instagram Transcript Extractor

**Transcribe and summarize one Reel**

```text
Use Instagram Transcript Extractor on this public Instagram Reel. Return the transcript actually provided, then give me a short summary in [SUMMARY_LANGUAGE]. Include timestamps only if they were returned. Do not invent transcript text or timestamps.
[PUBLIC_REEL_URL]
```

**Compare multiple transcripts**

```text
Use Instagram Transcript Extractor on exactly these public Instagram links only if this host and connected tool support this batch. For each input, show the original URL, status, and actual transcript. Match results by URL, never by return order. Then compare the hooks, core points, and content structure using only returned transcript text. Do not invent transcripts, timestamps, or engagement data; flag missing or uncertain results.
[PUBLIC_REEL_URL_1]
[PUBLIC_REEL_URL_2]
```

### Instagram Creator Reels Insights prompts

**Daily Scan for multiple creators**

```text
Use Instagram Creator Reels Insights for these public creator accounts: [CREATOR_1], [CREATOR_2], and [CREATOR_3]. Run a Daily Scan for the most recent 24 hours and process up to [VIDEO_LIMIT] eligible videos per creator. Give each creator a separate section, then summarize cross-creator patterns only when supported by the returned transcripts. Analyze only posts and transcripts actually returned, include source links, and separate observations from interpretation. If coverage is partial or unknown, explain in plain language that results may be incomplete. Do not say that no posts were made just because none were returned, or imply that unreturned posts were reviewed.
```

**Weekly review across multiple creators**

```text
Use Instagram Creator Reels Insights for these public creator accounts: [CREATOR_1], [CREATOR_2], and [CREATOR_3]. Review the most recent 7 days and process up to [VIDEO_LIMIT] eligible videos per creator. Analyze only the posts and transcripts actually returned. Provide a separate summary for each creator, then compare recurring topics, hooks, and speaking structures only where transcripts support the comparison. Include source links and short transcript evidence. Separate observations from interpretation. If coverage is partial or unknown, explain in plain language that results may be incomplete. Do not say that no posts were made just because none were returned, or imply that unreturned posts were reviewed.
```

**Transcript-based content ideas**

```text
For [CREATOR_1], [CREATOR_2], and [CREATOR_3], review the most recent 7 days using Instagram Creator Reels Insights and process up to [VIDEO_LIMIT] eligible videos per creator. Suggest a few transcript-based content ideas for each creator, with the returned transcript evidence and source links that inspired them. Add cross-creator ideas only when supported by evidence across the returned transcripts. Separate observations from interpretation. If coverage is partial or unknown, explain in plain language that results may be incomplete, and do not treat missing results as proof that no posts were published. Do not infer visuals, invent transcript text, or imply that unreturned posts were analyzed.
```

`[VIDEO_LIMIT]` is the maximum number of discovered videos per creator sent for transcript analysis. It does not limit how many posts are discovered and is not a fee cap.

## Scope and limitations

- Transcript Extractor analyzes returned speech text. It does not analyze video imagery, editing, audience response, or unreturned engagement metrics. Timestamps, subtitle files, and batch processing depend on the returned data and host capabilities.
- Creator Reels Insights can accept multiple requested creators and keeps the report organized per creator. It analyzes only the posts and transcripts returned for the request; it does not guarantee that every post in a period was found or establish trends beyond the reviewed sample.
- Neither Skill bypasses private, deleted, restricted, or otherwise inaccessible content. Do not provide Instagram passwords, cookies, or session credentials in chat.

## Help and license

Questions or problems? [Open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues). The [Instagram Transcript Extractor user guide](docs/skills/instagram-transcript-extractor.md) covers that Skill only. Creator Reels Insights users can start with the [Creator prompt examples](#instagram-creator-reels-insights-prompts) or inspect its [SKILL.md](skills/instagram-creator-reels-insights/SKILL.md). The repository and GitHub ZIP packages are licensed under [MIT](LICENSE); the ClawHub copies of both Skills are listed under [MIT-0](https://spdx.org/licenses/MIT-0.html).
