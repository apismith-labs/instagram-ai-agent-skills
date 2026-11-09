# Instagram AI Agent Skills

A collection of independent AI agent Skills for working with public Instagram video content. Each Skill has its own scope and installation path; this repository is not a single Skill that installs every feature automatically.

## Choose a Skill

| Skill | What it does | Distribution status | Start here |
| --- | --- | --- | --- |
| **Instagram Transcript Extractor** (`instagram-transcript-extractor`) | Gets spoken-word transcripts from public Instagram Reels and videos. You can request translation, summaries, text-based analysis, or subtitles when the host supports file export and valid timestamps are returned. | The GitHub v0.2.0 ZIP and the separate ClawHub 1.0.0 listing are both available. | [Choose a platform below](#availability-and-installation), see the [OpenClaw guide](docs/platforms/openclaw.md#instagram-transcript-extractor), or inspect the [Skill source](skills/instagram-transcript-extractor/SKILL.md). |
| **Instagram Creator Reels Insights** (`instagram-creator-reels-insights`) | Reviews recent public videos for a creator and builds source-linked Daily Scan or Weekly Review analysis from transcripts. | Published on ClawHub as version 1.0.0. There is no separate GitHub Release ZIP. | [ClawHub page](https://clawhub.ai/apismith-labs/skills/instagram-creator-reels-insights) · [OpenClaw install guide](docs/platforms/openclaw.md#instagram-creator-reels-insights). |

## Availability and installation

Installation instructions below apply only to the named Skill. Installing a Skill and connecting Apify are separate steps.

### Instagram Transcript Extractor

The existing platform guides cover this Skill:

| Platform | Installation route in the project guide |
| --- | --- |
| ChatGPT chat | Upload the named v0.2.0 ZIP; select the Apify plugin when making a request. Skill availability may depend on your account and workspace. See the [ChatGPT guide](docs/platforms/chatgpt.md). The asset is available on the [v0.2.0 Release page](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/tag/v0.2.0). |
| Codex desktop app and Codex CLI | Separate setup guidance is provided for each environment. The installer example uses the Git method and pins source ref v0.1.0, which may not be the latest Release. See the [Codex guide](docs/platforms/codex.md). |
| Manus | The guide describes importing this Skill folder from GitHub. Tasks using the Apify Connector may consume Manus credits. See the [Manus guide](docs/platforms/manus.md). |
| Claude Web | Upload the named ZIP and connect Apify as described in the [Claude guide](docs/platforms/claude-web.md). A task using the exact v0.2.0 ZIP has not been confirmed. |
| Claude Desktop regular chat | The guide describes using the same account as Claude Web. See the [Claude guide](docs/platforms/claude-web.md). |
| Claude Code | The primary path is syncing a Skill from your Claude.ai account; local ZIP installation is an alternative. This project has not tested a Claude Code installation or transcript task. See the [Claude guide](docs/platforms/claude-web.md). |
| OpenClaw | Transcript Extractor: Control UI, the [ClawHub Skill for OpenClaw CLI installation](https://clawhub.ai/apismith-labs/skills/instagram-transcript-extractor), or GitHub source/local directory. GitHub/local installation has been reported to make the Skill visible, but an Apify transcript task is not confirmed; Control UI/ClawHub installation is also unconfirmed on the project Gateway. See the [OpenClaw guide](docs/platforms/openclaw.md#instagram-transcript-extractor). |

The uploaded [Instagram Transcript Extractor v0.2.0 ZIP](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.0/instagram-transcript-extractor-v0.2.0.zip) is available from the [v0.2.0 Release page](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/tag/v0.2.0). Do not substitute GitHub's automatically generated **Source code (zip)** for the Skill package.

### Instagram Creator Reels Insights — ClawHub 1.0.0

Use this Skill to review a creator's public videos through transcripts returned for your request. Daily Scan covers the most recent 24 hours; Weekly Review covers the most recent 7 days. It highlights topics, opening hooks, and speaking structures without implying that every post was found.

Install it in the same environment as your OpenClaw Gateway:

```sh
openclaw skills install @apismith-labs/instagram-creator-reels-insights
```

The OpenClaw CLI install command defaults to the active workspace's `skills/` directory. Add `--global` to install into the shared managed Skills directory. These install targets follow the [OpenClaw Skills CLI documentation](https://docs.openclaw.ai/cli/skills).

After installing, check that the Skill is ready:

```sh
openclaw skills check
```

To check a specific Agent, use `openclaw skills check --agent YOUR_AGENT_ID`, replacing `YOUR_AGENT_ID` with its ID. If you do not know the Agent ID, omit `--agent` to check the default Agent. Then start a new session and enter `$instagram-creator-reels-insights` to select the Skill.

The install command follows the OpenClaw CLI documentation. The ClawHub installation itself and an end-to-end task using this route have not yet been confirmed in this project's Gateway environment. Creator Reels Insights is published on [ClawHub](https://clawhub.ai/apismith-labs/skills/instagram-creator-reels-insights) as version 1.0.0, with no separate GitHub Release ZIP. Other platforms' installation paths are not documented here for this Skill. You can inspect the [source directory](skills/instagram-creator-reels-insights/) or [`SKILL.md`](skills/instagram-creator-reels-insights/SKILL.md); these are source links, not a packaged installer.

## Setup requirements

Both Skills use Apify Actors. Installing a Skill and connecting the Apify plugin are separate steps; OpenClaw users can follow the [Apify setup section](docs/platforms/openclaw.md#set-up-the-apify-plugin). Review actual usage in [Apify Console](https://console.apify.com/); usage follows your account and the Actors' current billing rules. No fixed fee or fee cap is promised here.

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

### Instagram Creator Reels Insights

**Daily Scan for one creator**

```text
Use Instagram Creator Reels Insights for [CREATOR_USERNAME]. Run a Daily Scan for the most recent 24 hours, processing up to [VIDEO_LIMIT] eligible videos. Analyze only the posts and transcripts actually returned, summarize each video's hook and main speaking points, and include source links. Separate transcript evidence from interpretation; do not imply that unreturned posts were reviewed.
```

**Weekly review for one creator**

```text
Use Instagram Creator Reels Insights for [CREATOR_USERNAME]. Review the most recent 7 days and process up to [VIDEO_LIMIT] eligible videos for this creator. Analyze only the posts and transcripts actually returned. Summarize recurring topics, hooks, and speaking structures with source links and short transcript evidence. Separate observations from interpretation. Do not imply that unreturned posts were reviewed or that every post was found.
```

**Transcript-based content ideas**

```text
For [CREATOR_USERNAME], review the most recent 7 days using Instagram Creator Reels Insights and process up to [VIDEO_LIMIT] eligible videos. Based only on the transcripts actually returned, suggest a few content ideas and explain which transcript evidence inspired each one. Separate observations from interpretation and link the source posts. Do not infer visuals, invent transcript text, or imply that unreturned posts were analyzed.
```

## Scope and limitations

- Transcript Extractor analyzes returned speech text. It does not analyze video imagery, editing, audience response, or unreturned engagement metrics. Timestamps, subtitle files, and batch processing depend on the returned data and host capabilities.
- Creator Reels Insights analyzes the posts and transcripts returned for the request. It does not guarantee that every post in a period was found, establish trends beyond the reviewed sample, or confirm multi-account behavior.
- Neither Skill bypasses private, deleted, restricted, or otherwise inaccessible content. Do not provide Instagram passwords, cookies, or session credentials in chat.

## Help and license

Questions or problems? [Open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues). Read the [Instagram Transcript Extractor user guide](docs/skills/instagram-transcript-extractor.md). The repository is licensed under [MIT](LICENSE); the ClawHub copies of both Skills are listed under [MIT-0](https://spdx.org/licenses/MIT-0.html).
