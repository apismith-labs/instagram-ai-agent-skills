# Instagram AI Agent Skills

A collection of independent AI agent Skills for working with public Instagram video content. Each Skill has its own scope and installation path; this repository is not a single Skill that installs every feature automatically.

## Choose a Skill

| Skill | What it does | Distribution status | Start here |
| --- | --- | --- | --- |
| **Instagram Transcript Extractor** (`instagram-transcript-extractor`) | Gets spoken-word transcripts from public Instagram Reels and videos. You can request translation, summaries, text-based analysis, or subtitles when the host supports file export and valid timestamps are returned. | The v0.2.0 ZIP Release asset is uploaded and available below. | [Choose a platform below](#availability-and-installation) or inspect the [Skill source](skills/instagram-transcript-extractor/SKILL.md). |
| **Instagram Creator Reels Insights** (`instagram-creator-reels-insights`) | Discovers recent public videos for a creator and builds source-linked Daily Scan or Weekly Review analysis from their actual transcripts. | Preview/source available; no standalone GitHub Release ZIP is available. Platform-specific installation paths have not yet been confirmed for it. | [Inspect the source](skills/instagram-creator-reels-insights/SKILL.md). |

## Availability and installation

Installation instructions below apply only to the named Skill. Installing a Skill and connecting Apify are separate steps.

### Instagram Transcript Extractor

The existing platform guides cover this Skill:

| Platform | Installation route in the project guide |
| --- | --- |
| ChatGPT chat | Upload the named v0.2.0 ZIP; select the Apify plugin when making a request. Skill availability may depend on your account and workspace. See the [ChatGPT guide](docs/platforms/chatgpt.md). The asset is available on the [v0.2.0 Release page](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/tag/v0.2.0). |
| Codex desktop app and Codex CLI | Separate setup guidance is provided for each environment. The installer example uses the Git method and pins source ref v0.1.0, which may not be the latest Release; the exact natural-language flow has not been verified word for word. See the [Codex guide](docs/platforms/codex.md). |
| Manus | The guide describes importing this Skill folder from GitHub. Tasks using the Apify Connector may consume Manus credits. One project-owner account reported a successful single-Reel task; this is not a general platform guarantee. See the [Manus guide](docs/platforms/manus.md). |
| Claude Web | Upload the named ZIP and connect Apify as described in the [Claude guide](docs/platforms/claude-web.md). A task using the exact v0.2.0 ZIP has not been confirmed. |
| Claude Desktop regular chat | The guide describes using the same account as Claude Web; the reported account saw the Skill and Apify connection there. See the [Claude guide](docs/platforms/claude-web.md). |
| Claude Code | The primary path is syncing a Skill from your Claude.ai account; local ZIP installation is an alternative. This project has not tested a Claude Code installation or transcript task. See the [Claude guide](docs/platforms/claude-web.md). |
| OpenClaw | The guide describes Control UI, ClawHub CLI, and GitHub source installation routes. GitHub/local installation and visibility have been reported, but a successful Skill task through the plugin has not been confirmed. See the [OpenClaw guide](docs/platforms/openclaw.md). |

The uploaded [Instagram Transcript Extractor v0.2.0 ZIP](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.0/instagram-transcript-extractor-v0.2.0.zip) is available from the [v0.2.0 Release page](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/tag/v0.2.0). Do not substitute GitHub's automatically generated **Source code (zip)** for the Skill package.

### Instagram Creator Reels Insights — Preview

There is **no Release ZIP** for this Skill at present. Platforms that require an uploaded ZIP or Release artifact therefore do not have a downloadable package for it. Existing platform guides specify installation paths for Transcript Extractor and do not yet confirm a corresponding Creator Reels Insights installation path. This does not mean that a platform is inherently incompatible; its installation route simply remains unconfirmed here.

Technical users can inspect the [Creator Reels Insights source directory](skills/instagram-creator-reels-insights/) or its [`SKILL.md`](skills/instagram-creator-reels-insights/SKILL.md). These are source links, not a packaged download or an installation instruction.

## Setup requirements

Both Skills use Apify Actors. You need an Apify account and a connection supported by your chosen host. Follow the matching platform guide for the Transcript Extractor; Creator Reels Insights does not yet have a confirmed platform installation guide. Review actual usage in [Apify Console](https://console.apify.com/); usage follows your account and the Actors' current billing rules. No fixed fee or fee cap is promised here.

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

**Weekly review for one creator**

```text
Use Instagram Creator Reels Insights for [CREATOR_USERNAME]. Review the most recent 7 days and process up to [VIDEO_LIMIT] eligible videos for this creator. Analyze only transcripts actually returned. Summarize recurring topics, hooks, and speaking structures with links to the source posts and short transcript evidence. Report partial or unknown coverage; do not claim a complete scan or infer that no videos exist from an empty result.
```

**Transcript-based content ideas**

```text
For [CREATOR_USERNAME], review the most recent 7 days using Instagram Creator Reels Insights and process up to [VIDEO_LIMIT] eligible videos. Based only on the transcripts actually returned, suggest a few content ideas and explain which transcript evidence inspired each one. Separate evidence from interpretation, link the source posts, and disclose partial or unknown coverage. Do not infer visuals, invent transcript text, or claim a complete scan.
```

## Scope and limitations

- Transcript Extractor analyzes returned speech text. It does not analyze video imagery, editing, audience response, or unreturned engagement metrics. Timestamps, subtitle files, and batch processing depend on the returned data and host capabilities.
- Creator Reels Insights is a preview. Its reports depend on videos and transcripts actually returned; discovery coverage may be `partial` or `unknown`. A successful transcript match does not prove that the Dataset was fully read. Results do not establish a complete account scan, trends beyond the reviewed sample, or multi-account behavior.
- Neither Skill bypasses private, deleted, restricted, or otherwise inaccessible content. Do not provide Instagram passwords, cookies, or session credentials in chat.

## Help and license

Questions or problems? [Open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues). Read the [Instagram Transcript Extractor user guide](docs/skills/instagram-transcript-extractor.md). This project is licensed under the [MIT License](LICENSE).
