# Instagram AI Agent Skills

A collection of independent AI agent Skills for working with public Instagram video content. Each Skill has its own scope and installation path; this repository is not a single Skill that installs every feature automatically.

## Choose a Skill

Browse the [user guide and platform installation index](docs/README.md) for all setup guides. Transcript Extractor, Media Links & Post Insights, and Creator Video Insights have public ClawHub listings. Creator is a limited release: full time-window coverage and the complete task flow on the project OpenClaw Gateway remain unverified.

**Instagram Transcript Extractor** (`instagram-transcript-extractor`) retrieves the spoken transcript actually returned for a public Instagram video or Reel. Ask for a summary, translation, or analysis of that transcript; success is not guaranteed for every video. See the [Instagram Transcripts Scraper Actor](https://apify.com/apple_yang/instagram-transcripts-scraper).

- **Available:** [GitHub Release ZIP v0.2.3](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.3/instagram-transcript-extractor-release-v0.2.3.zip) · [ClawHub listing v1.0.5](https://clawhub.ai/apismith-labs/skills/instagram-transcript-extractor) (latest and Moderate CLEAN when checked 2026-11-12)
- **Start here:** [Platform instructions](#install-by-platform) · [Installation entry](#install-instagram-transcript-extractor) · [User guide](docs/skills/instagram-transcript-extractor.md) · [Copy-ready prompts](#instagram-transcript-extractor)

**Instagram Media Links & Post Insights** (`instagram-media-links-and-post-insights`) returns Actor-supplied video/audio links and post fields for public Instagram video posts and Reels. It only presents data the Actor actually returns; it does not download media or guarantee that every field is present. See the [Instagram Video Scraper API Actor](https://apify.com/apple_yang/instagram-video-scraper-api).

- **Available:** [GitHub Release ZIP v1.0.0](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/instagram-media-links-and-post-insights-v1.0.0/instagram-media-links-and-post-insights-release-v1.0.0.zip) · [ClawHub listing v1.0.2](https://clawhub.ai/apismith-labs/skills/instagram-media-links-and-post-insights) (latest and Moderate CLEAN when checked 2026-11-12). These are separate distribution channels with independent version numbers.
- **Start here:** [Platform instructions](#install-by-platform) · [Installation entry](#install-instagram-media-links-and-post-insights) · [User guide](docs/skills/instagram-media-links-and-post-insights.md) · [Copy-ready prompts](#instagram-media-links-and-post-insights-prompts)

**Instagram Creator Video Insights** (`instagram-creator-reels-insights`) is intended to review public Reels and regular video posts through returned transcripts. The v1.0.5 GitHub ZIP and ClawHub update are prepared as release candidates and are pending publication: [candidate ZIP](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.5/instagram-creator-video-insights-v1.0.5.zip) and [planned ClawHub v1.0.5 listing](https://clawhub.ai/apismith-labs/skills/instagram-creator-reels-insights). These are independent distribution channels; their planned version numbers happen to match. The release does not mean end-to-end workflow validation: full time-window coverage remains unverified, and 6/6 transcript URL reconciliation does not establish complete Discovery coverage. The official OpenClaw Apify plugin v0.5.3 does not provide Dataset pagination and has a 50,000-character serialization truncation limitation. A separate isolated paginated copy returned 24/24 rows, but that result does not establish behavior of the official plugin. Creator installation and the full task flow on the project OpenClaw Gateway remain unverified.

- **Start here:** [Platform instructions](#install-by-platform) · [Creator installation entry](#instagram-creator-video-insights) · [User guide](docs/skills/instagram-creator-reels-insights.md) · [Copy-ready examples](#instagram-creator-video-insights-prompts)

## Install by platform

Choose one Skill, then follow its platform-specific setup. The steps below walk through ChatGPT, Claude Web, and OpenClaw; the Skill-specific route tables also point to Codex, Manus, Claude Desktop, and Claude Code instructions. Installing a Skill does not connect Apify. For direct routes, jump to [Transcript Extractor](#install-instagram-transcript-extractor), [Media Links & Post Insights](#install-instagram-media-links-and-post-insights), or [Creator Video Insights](#instagram-creator-video-insights).

### Named GitHub Skill ZIPs

For the ChatGPT and Claude Web upload steps below, choose the package for the Skill you want. The named Release ZIPs are separate from GitHub's automatically generated **Source code (zip)**.

| Skill | GitHub Release ZIP |
| --- | --- |
| Instagram Transcript Extractor | [`instagram-transcript-extractor-release-v0.2.3.zip`](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.3/instagram-transcript-extractor-release-v0.2.3.zip) · [Release v0.2.3](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/tag/v0.2.3) |
| Instagram Media Links & Post Insights | [`instagram-media-links-and-post-insights-release-v1.0.0.zip`](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/instagram-media-links-and-post-insights-v1.0.0/instagram-media-links-and-post-insights-release-v1.0.0.zip) · [Release v1.0.0](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/tag/instagram-media-links-and-post-insights-v1.0.0) |
| Instagram Creator Video Insights (v1.0.5 candidate; pending publication) | [`instagram-creator-video-insights-v1.0.5.zip`](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.5/instagram-creator-video-insights-v1.0.5.zip) · [planned Release v1.0.5](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/tag/v1.0.5) · SHA-256 `81c2e5afae4f68d2e576dcc40e05ace9c2be7838df24be43ca7bc94f46e28c51` |

Download the named Release asset for installation; GitHub's automatically generated **Source code (zip)** is not a Skill package. ClawHub and GitHub Release ZIPs are separate distribution channels with independent version numbers, even when the displayed versions happen to match. ClawHub packages are not ZIP upload packages.

### ChatGPT

**Connect Apify:** Add and authorize the shared `Apify MCP` custom connection using the [ChatGPT connection steps](docs/platforms/chatgpt.md#1-add-and-authorize-the-apify-mcp-connection). It is separate from the Skills ZIP upload page and can be used by multiple Skills.

**Upload a Skill ZIP:** At **Plugins → Plugin Directory → Skills → Create → Upload from your computer**, upload the named ZIP for the Skill you want. Follow the [ChatGPT upload steps](docs/platforms/chatgpt.md#2-upload-a-skill-package). Keep the ZIP intact; do not select GitHub's automatic **Source code (zip)**. After upload, check the scan result (**Available**, **Needs Review**, or **Blocked**).

In a regular chat, name the Skill in your request; OpenAI says installed Skills can be selected automatically when relevant. In the ChatGPT Work mode tested for this project, the user could type **@** and select `Apify MCP`, then name the Skill. Treat that as account-level observation, not a guarantee that every account/surface has the same picker. One connection can serve multiple Skills. Skills are documented for eligible ChatGPT Business, Enterprise, Healthcare, and Edu users, subject to workspace settings and product availability. The public custom MCP guide lists full support for Business and Enterprise/Edu and says Pro can connect custom MCP servers with read/fetch permissions. The project owner has also completed one third-Skill success-path test on a ChatGPT Plus account, which is account-level evidence only and not a general Plus availability guarantee. See OpenAI's [Skills in ChatGPT guide](https://help.openai.com/en/articles/20001066-skills-in-chatgpt), [custom MCP guide](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt), and the [project ChatGPT guide](docs/platforms/chatgpt.md).

Use the [named ZIP package table](#named-github-skill-zips) above for Transcript Extractor, Media Links & Post Insights, or Creator Video Insights. Download the named Release asset, not GitHub's automatically generated **Source code (zip)**. ClawHub versions are independent of ZIP versions.

### Claude Web

Install the official Apify Plugin or connect its hosted MCP connector, complete Apify OAuth, and upload/enable the Skill ZIP separately. In new chats, enable Apify from the connector menu and select the Skill with `/` when the menu offers it, or name it in the request. Claude is rolling out a unified Plugins page, so the visible label may still be Customize. See the [Claude guide](docs/platforms/claude-web.md).

For ZIP-upload platforms, use a named GitHub Release ZIP from the table above when one is available for the Skill. Media Links & Post Insights has a v1.0.0 ZIP; ClawHub versions remain a separate distribution channel.

### OpenClaw

Install Transcript Extractor, Media Links & Post Insights, or Creator Video Insights from ClawHub in the same environment as your OpenClaw Gateway (the service or environment running your OpenClaw agents). The Creator ClawHub v1.0.5 update is a candidate pending publication; installation and the full task flow on the project Gateway remain unverified. The official OpenClaw Apify plugin v0.5.3 does not provide Dataset pagination and has a 50,000-character serialization truncation limitation; results from an isolated paginated copy do not verify the official plugin. By default the OpenClaw CLI installs to the active workspace's `skills/` directory; add `--global` for the shared managed Skills directory. Check the default Agent with `openclaw skills check`, or specify one with `openclaw skills check --agent YOUR_AGENT_ID`. In a new session, select the Skill using its `$` name. Follow the [OpenClaw Skills CLI documentation](https://docs.openclaw.ai/cli/skills) and the [project OpenClaw guide](docs/platforms/openclaw.md) for exact install routes and the separate Apify plugin setup.

## Skill-specific installation routes

The platform sections above describe ZIP upload and shared OpenClaw setup. These tables match each platform to the correct package, slug, source folder, or account-sync route. Follow the linked guide for full steps; an installation route alone does not confirm the task workflow.

### Install Instagram Transcript Extractor

Choose the route for your platform. GitHub ZIP and ClawHub versions are separate channels. Codex uses the moving `main` source branch, not either package version. On the project Gateway, GitHub-source/local-directory visibility does not confirm an Apify transcript task; Control UI and ClawHub installation are not confirmed.

| Platform | Transcript Extractor entry |
| --- | --- |
| ChatGPT | Upload [`instagram-transcript-extractor-release-v0.2.3.zip`](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.3/instagram-transcript-extractor-release-v0.2.3.zip) using the [ChatGPT steps](#chatgpt). |
| Claude Web | Upload [`instagram-transcript-extractor-release-v0.2.3.zip`](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.3/instagram-transcript-extractor-release-v0.2.3.zip) and separately connect Apify using the [Claude guide](docs/platforms/claude-web.md). |
| OpenClaw | ClawHub 1.0.5: [`@apismith-labs/instagram-transcript-extractor`](https://clawhub.ai/apismith-labs/skills/instagram-transcript-extractor) · `openclaw skills install @apismith-labs/instagram-transcript-extractor`. [Guide](docs/platforms/openclaw.md#instagram-transcript-extractor). |
| Codex desktop app / CLI | Use the GitHub [`skills/instagram-transcript-extractor`](https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-transcript-extractor) folder with [Codex install instructions](docs/platforms/codex.md#install-the-skill). |
| Manus | Import the GitHub folder [`skills/instagram-transcript-extractor`](https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-transcript-extractor) using [Transcript Extractor import steps](docs/platforms/manus.md#2-import-and-enable-the-skill). |
| Claude Desktop regular chat | Sign into the same account; use the Chat tab, enable Apify through the connector menu, and choose the Skill with `/` if offered. See the [Claude guide](docs/platforms/claude-web.md). |
| Claude Code | Same-account sync or extract the named [Transcript Extractor v0.2.3 ZIP](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.3/instagram-transcript-extractor-release-v0.2.3.zip) and follow the [Claude Code steps](docs/platforms/claude-web.md#claude-code). |

### Instagram Creator Video Insights

Choose the route for your platform. The named GitHub Release ZIP v1.0.5 and ClawHub v1.0.5 are prepared candidates pending publication; the channels remain independently versioned. Download the named Release asset after it is published, not GitHub's automatic **Source code (zip)**. These install paths do not imply full task-workflow validation. Full time-window coverage remains unverified; the official OpenClaw Apify plugin v0.5.3 does not provide Dataset pagination and has a 50,000-character serialization truncation limitation. The isolated paginated copy's 24/24 result does not represent the official plugin, and 6/6 transcript URL reconciliation does not prove Discovery coverage is complete. The ClawHub route and full task flow remain unverified on the project Gateway. See the [Creator OpenClaw guide](docs/platforms/openclaw.md#instagram-creator-video-insights).

| Platform | Creator Video Insights entry |
| --- | --- |
| ChatGPT | Upload the v1.0.5 candidate [`instagram-creator-video-insights-v1.0.5.zip`](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.5/instagram-creator-video-insights-v1.0.5.zip) after publication using the [ChatGPT steps](#chatgpt). Choose the named Release asset, not GitHub's automatic **Source code (zip)**. |
| Claude Web | Upload the v1.0.5 candidate [`instagram-creator-video-insights-v1.0.5.zip`](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.5/instagram-creator-video-insights-v1.0.5.zip) after publication and separately connect Apify using the [Claude guide](docs/platforms/claude-web.md). |
| OpenClaw | Planned ClawHub v1.0.5 candidate, pending publication: [`@apismith-labs/instagram-creator-reels-insights`](https://clawhub.ai/apismith-labs/skills/instagram-creator-reels-insights) · `openclaw skills install @apismith-labs/instagram-creator-reels-insights`. Installation and full task flow remain unverified on the project Gateway. [Details](docs/platforms/openclaw.md#instagram-creator-video-insights). |
| Codex desktop app / CLI | Use the separate GitHub [`skills/instagram-creator-reels-insights`](https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-creator-reels-insights) folder with [Creator install instructions](docs/platforms/codex.md#install-creator-video-insights). |
| Manus | Import the separate GitHub folder [`skills/instagram-creator-reels-insights`](https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-creator-reels-insights) using [Creator import instructions](docs/platforms/manus.md#use-creator-video-insights). The report workflow is not confirmed in Manus. |
| Claude Desktop regular chat | Sign into the same account; in the Chat tab, enable Apify through the connector menu and choose the Skill with `/` if offered. The report workflow is not confirmed there. See the [Claude guide](docs/platforms/claude-web.md). |
| Claude Code | Same-account sync or extract the top-level folder from the [v1.0.5 candidate ZIP](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.5/instagram-creator-video-insights-v1.0.5.zip) after publication; see [Creator Claude Code steps](docs/platforms/claude-web.md#creator-video-insights-in-claude-code). Installation and task flow are not confirmed there. |

<a id="install-instagram-media-links-and-post-insights"></a>

### Install Instagram Media Links & Post Insights

The GitHub Release ZIP v1.0.0 is for ZIP-upload platforms; ClawHub v1.0.2 is the separate OpenClaw distribution. These channels use independent version numbers.

| Platform | Media Links & Post Insights entry |
| --- | --- |
| OpenClaw | ClawHub 1.0.2 (latest and Moderate CLEAN when checked 2026-11-12): [`@apismith-labs/instagram-media-links-and-post-insights`](https://clawhub.ai/apismith-labs/skills/instagram-media-links-and-post-insights) · `openclaw skills install @apismith-labs/instagram-media-links-and-post-insights`. [OpenClaw setup](docs/platforms/openclaw.md#media-links-post-insights-installation). |
| ChatGPT / Claude Web | Upload the [GitHub Release ZIP v1.0.0](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/instagram-media-links-and-post-insights-v1.0.0/instagram-media-links-and-post-insights-release-v1.0.0.zip). ClawHub v1.0.2 is a separate OpenClaw distribution. |
| Codex | The repository documents a general local Skill-directory installation route; see the [Codex guide](docs/platforms/codex.md). This is not a Media-specific end-to-end verification. |
| Manus | No Media-specific Manus installation instructions are currently documented. The [Manus guide](docs/platforms/manus.md) covers only its documented platform setup; do not infer that this Skill's installation or workflow is supported there. |

## Connect Apify and check usage

Apify connection steps vary by platform: use the [ChatGPT Apify MCP custom-connection setup](docs/platforms/chatgpt.md#1-add-and-authorize-the-apify-mcp-connection), [Claude Web setup](docs/platforms/claude-web.md), [Codex setup](docs/platforms/codex.md), or [Manus setup](docs/platforms/manus.md). In ChatGPT, one Apify MCP connection can be shared by multiple Skills; a Skill install does not create or authorize that connection. OpenClaw uses its separately installed [Apify plugin](docs/platforms/openclaw.md#set-up-the-apify-plugin). Never paste credentials into chat. Runs use your Apify account and the Actors' current billing rules. More creators or videos may increase usage; check actual usage in [Apify Console](https://console.apify.com/). No fixed fee or fee cap is promised.

Transcript Extractor and Creator Video Insights use the [Instagram Transcripts Scraper on Apify](https://apify.com/apple_yang/instagram-transcripts-scraper). Media Links & Post Insights uses the separate [Instagram Video Scraper API Actor](https://apify.com/apple_yang/instagram-video-scraper-api).

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

### Instagram Creator Video Insights prompts

**Daily Scan for multiple creators**

```text
Use Instagram Creator Video Insights for these public creator accounts: [CREATOR_1], [CREATOR_2], and [CREATOR_3]. Run a Daily Scan for the most recent 24 hours and process up to [VIDEO_LIMIT] eligible videos per creator. Give each creator a separate section, then summarize cross-creator patterns only when supported by the returned transcripts. Analyze only posts and transcripts actually returned, include source links, and separate observations from interpretation. If coverage is partial or unknown, explain in plain language that results may be incomplete. Do not say that no posts were made just because none were returned, or imply that unreturned posts were reviewed.
```

**Weekly review across multiple creators**

```text
Use Instagram Creator Video Insights for these public creator accounts: [CREATOR_1], [CREATOR_2], and [CREATOR_3]. Review the most recent 7 days and process up to [VIDEO_LIMIT] eligible videos per creator. Analyze only the posts and transcripts actually returned. Provide a separate summary for each creator, then compare recurring topics, hooks, and speaking structures only where transcripts support the comparison. Include source links and short transcript evidence. Separate observations from interpretation. If coverage is partial or unknown, explain in plain language that results may be incomplete. Do not say that no posts were made just because none were returned, or imply that unreturned posts were reviewed.
```

**Transcript-based content ideas**

```text
For [CREATOR_1], [CREATOR_2], and [CREATOR_3], review the most recent 7 days using Instagram Creator Video Insights and process up to [VIDEO_LIMIT] eligible videos per creator. Suggest a few transcript-based content ideas for each creator, with the returned transcript evidence and source links that inspired them. Add cross-creator ideas only when supported by evidence across the returned transcripts. Separate observations from interpretation. If coverage is partial or unknown, explain in plain language that results may be incomplete, and do not treat missing results as proof that no posts were published. Do not infer visuals, invent transcript text, or imply that unreturned posts were analyzed.
```

`[VIDEO_LIMIT]` is the maximum number of discovered videos per creator sent for transcript analysis. It does not limit how many posts are discovered and is not a fee cap.

### Instagram Media Links and Post Insights prompts

**Get media links for one public video**

```text
Use Instagram Media Links & Post Insights for this public Instagram video or Reel. Return the video and audio links actually provided by the Actor, matching the result to my input by its returned `url`. If a link field is missing, mark it unavailable; do not infer that the media does not exist, and do not treat missing numeric fields as zero.
[INSTAGRAM_URL]
```

**Organize post insights for multiple links**

```text
Use Instagram Media Links & Post Insights for exactly these public Instagram video or Reel links. Organize the author, publish time, like count, and comment count only when those fields are actually returned. Match each result by its returned `url`; never guess from result order. Mark missing fields unavailable, not zero, and do not infer views, impressions, follower counts, or complete coverage.
[INSTAGRAM_URL_1]
[INSTAGRAM_URL_2]
```

## Scope and limitations

- Transcript Extractor analyzes returned speech text. It does not analyze video imagery, editing, audience response, or unreturned engagement metrics. Timestamps, subtitle files, and batch processing depend on the returned data and host capabilities.
- Media Links & Post Insights reports only Actor-supplied media links and returned post fields. It does not download media, promise missing fields, or infer unverified counts or trends.
- Creator Video Insights can accept multiple requested creators and keeps the report organized per creator. It sends a post for transcription only when the returned `type` is exactly `"Video"` and the Instagram post URL is usable; other or unknown type values are retained but not treated as videos. It analyzes only the posts and transcripts returned for the request; it does not guarantee that every post in a period was found or establish trends beyond the reviewed sample.
- These Skills do not bypass private, deleted, restricted, or otherwise inaccessible content. Do not provide Instagram passwords, cookies, or session credentials in chat.

## Help and license

Questions or problems? [Open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues). See the [Transcript Extractor guide](docs/skills/instagram-transcript-extractor.md), [Media Links & Post Insights guide](docs/skills/instagram-media-links-and-post-insights.md), or [Creator Video Insights guide](docs/skills/instagram-creator-reels-insights.md). Creator users can also browse the [Creator prompt examples](#instagram-creator-video-insights-prompts) or inspect its [SKILL.md](skills/instagram-creator-reels-insights/SKILL.md). The repository and GitHub ZIP packages are licensed under [MIT](LICENSE); the published ClawHub copies are listed under [MIT-0](https://spdx.org/licenses/MIT-0.html).
