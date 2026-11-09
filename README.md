# Instagram AI Agent Skills

A collection of independent AI agent Skills for working with public Instagram video content. Each Skill has its own scope and installation path; this repository is not a single Skill that installs every feature automatically.

## Choose a Skill

| Skill | What it does | Distribution status | Start here |
| --- | --- | --- | --- |
| **Instagram Transcript Extractor** (`instagram-transcript-extractor`) | Gets spoken-word transcripts from public Instagram Reels and videos. You can request translation, summaries, text-based analysis, or subtitles when the host supports file export and valid timestamps are returned. | The GitHub v0.2.1 ZIP and the separate ClawHub 1.0.0 listing are both available. | [Choose a platform below](#install-by-platform), see the [OpenClaw guide](docs/platforms/openclaw.md#instagram-transcript-extractor), or inspect the [Skill source](skills/instagram-transcript-extractor/SKILL.md). |
| **Instagram Creator Reels Insights** (`instagram-creator-reels-insights`) | Reviews recent public videos for one or more creators and builds source-linked Daily Scan or Weekly Review reports from returned transcripts. | ClawHub v1.0.1 is public. A separate GitHub v1.0.1 ZIP is available for platforms that accept Skill uploads. | [ClawHub page](https://clawhub.ai/apismith-labs/skills/instagram-creator-reels-insights) · [v1.0.1 ZIP package](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.1/instagram-creator-reels-insights-v1.0.1.zip) · [OpenClaw install guide](docs/platforms/openclaw.md#instagram-creator-reels-insights). |

## Install by platform

Choose the Skill package or listing for the platform you use. Installing a Skill and connecting Apify are separate steps.

### ChatGPT

Connect Apify as described in the [ChatGPT guide](docs/platforms/chatgpt.md). Then upload the named ZIP for the Skill you want at **Plugins → Plugin Directory → Skills → Create → Upload from your computer**. Keep the ZIP intact and follow the scan status shown after upload: **Available**, **Needs Review**, or **Blocked**. Do not use GitHub's automatically generated **Source code (zip)**.

Skill availability depends on your ChatGPT plan and workspace; see the [ChatGPT guide](docs/platforms/chatgpt.md).

| Skill | Package |
| --- | --- |
| Instagram Transcript Extractor | [instagram-transcript-extractor-v0.2.1.zip](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.1/instagram-transcript-extractor-v0.2.1.zip) · GitHub v0.2.1 |
| Instagram Creator Reels Insights | [instagram-creator-reels-insights-v1.0.1.zip](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.1/instagram-creator-reels-insights-v1.0.1.zip) · GitHub v1.0.1 |

### Claude Web

In Claude Web, connect the Apify Web Connector and complete OAuth, then upload the named ZIP for the Skill you want at **Customize → Skills → Add → Upload skill**. Keep the ZIP intact, review its preview, and enable that Skill. Do not use GitHub's automatically generated **Source code (zip)**. See the [Claude guide](docs/platforms/claude-web.md).

| Skill | Package |
| --- | --- |
| Instagram Transcript Extractor | [instagram-transcript-extractor-v0.2.1.zip](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.1/instagram-transcript-extractor-v0.2.1.zip) · GitHub v0.2.1 |
| Instagram Creator Reels Insights | [instagram-creator-reels-insights-v1.0.1.zip](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.1/instagram-creator-reels-insights-v1.0.1.zip) · GitHub v1.0.1 |

### OpenClaw

Install from ClawHub in the same environment as your OpenClaw Gateway. The CLI defaults to the active workspace's `skills/` directory; add `--global` to use the shared managed Skills directory. Run `openclaw skills check` to check the default Agent, or `openclaw skills check --agent YOUR_AGENT_ID` for a specific Agent. Start a new session and select the Skill by entering its `$` name. Follow the [OpenClaw Skills CLI documentation](https://docs.openclaw.ai/cli/skills).

| Skill | ClawHub listing | Install command |
| --- | --- | --- |
| Instagram Transcript Extractor | [`@apismith-labs/instagram-transcript-extractor`](https://clawhub.ai/apismith-labs/skills/instagram-transcript-extractor) · ClawHub 1.0.0. The [OpenClaw guide](docs/platforms/openclaw.md#instagram-transcript-extractor) also documents Control UI, Vercel Skills CLI/GitHub source, and local-directory routes. GitHub/local installation has been reported to make the Skill visible, but that does not confirm a transcript task; Control UI/ClawHub install remains unconfirmed on the project Gateway. | `openclaw skills install @apismith-labs/instagram-transcript-extractor` |
| Instagram Creator Reels Insights | [`@apismith-labs/instagram-creator-reels-insights`](https://clawhub.ai/apismith-labs/skills/instagram-creator-reels-insights) · ClawHub 1.0.1. Its ClawHub installation and full task flow have not yet been confirmed in this project's Gateway. | `openclaw skills install @apismith-labs/instagram-creator-reels-insights` |

The Creator Reels Insights GitHub ZIP above is for platforms that accept Skill uploads; it is not an OpenClaw installation route.

### Codex, Manus, Claude Desktop, and Claude Code

The project documents these routes for Instagram Transcript Extractor only. Creator Reels Insights installation paths for these environments are not recorded in this project; this does not mean the platforms are incompatible.

| Platform | Instagram Transcript Extractor guide |
| --- | --- |
| Codex desktop app and Codex CLI | [Codex guide](docs/platforms/codex.md) (separate instructions; the example pins source ref v0.1.0, which may not be the latest Release) |
| Manus | [Manus guide](docs/platforms/manus.md) (GitHub folder import; Connector tasks may consume Manus credits) |
| Claude Desktop regular chat and Claude Code | [Claude guide](docs/platforms/claude-web.md) (account sync/local ZIP alternative; Claude Code installation and transcript task have not been tested) |

## Connect Apify and check usage

Both Skills use Apify tools. Installing a Skill and connecting Apify are separate steps. Follow your platform guide to connect your own Apify account; never paste credentials into chat. More creators or videos can increase usage. Check actual usage in [Apify Console](https://console.apify.com/); usage follows your account and the Actors' current billing rules. No fixed fee or fee cap is promised.

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
