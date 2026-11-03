# Instagram AI Agent Skills

Use AI agent skills to get spoken-word transcripts from public Instagram Reels and videos. The first available Skill, **Instagram Transcript Extractor**, works with one or more links and can also summarize, translate, or analyze the returned transcript text.

## Available skill: Instagram Transcript Extractor

The Skill transcribes speech from accessible videos. Timestamps may be available, and you can ask for summaries, translations, or analysis based on the transcript. It does not analyze video imagery or engagement metrics.

For ChatGPT or Claude Web, download the [v0.2.0 Skill ZIP](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.0/instagram-transcript-extractor-v0.2.0.zip). Choose this named Release asset, not GitHub's automatically generated **Source code (zip)**, and keep the ZIP intact when uploading it.

## What you need

You need your own [Apify account](https://console.apify.com/) and must connect it to your AI platform. Using the Skill consumes usage from your Apify account's plan allowance; check Apify Console for current usage and billing details. Installing the Skill does not connect or configure Apify—the Skill and account connection are separate setup steps.

## Choose your platform

| Platform | Setup order |
| --- | --- |
| [ChatGPT](docs/platforms/chatgpt.md) | Connect Apify → upload the named v0.2.0 ZIP → start a new conversation, select the Apify plugin with **@**, and request a transcript. Skill availability may depend on your account and workspace. |
| [Codex](docs/platforms/codex.md) | Install the Apify plugin and authorize with OAuth → install the Skill using the documented Codex installer flow → start a new session, confirm discovery, then explicitly invoke it. The guide covers Codex desktop and CLI separately. |
| [Manus](docs/platforms/manus.md) | Enable the existing Apify Connector and authorize with OAuth → import the Skill folder from GitHub → in chat select it with **/** and confirm the Apify Connector is enabled. Manus tasks using the Connector may consume Manus credits. |
| [Claude Web, Claude Desktop regular chat, and Claude Code](docs/platforms/claude-web.md) | Set up Apify and upload/enable the Skill in Claude Web. To use it in Claude Desktop regular chat, sign in with the same Claude account; Claude Code has a separate guide. |
| [OpenClaw](docs/platforms/openclaw.md) | Recommended: install through the OpenClaw Control UI. Alternatives: use the ClawHub CLI or install directly from GitHub with Vercel Skills CLI. A GitHub local-directory install is also documented as a backup. |

### OpenClaw: install directly from GitHub with Skills CLI

The [Vercel Skills CLI](https://skills.sh/docs/cli) installs this Skill directly from GitHub. It requires [Node.js 22.20.0 or later](https://github.com/vercel-labs/skills#install-a-skill). Run it in the same environment as your OpenClaw Gateway and from that Gateway's actual workspace.

First check the workspace:

```bash
openclaw config get agents.defaults.workspace
```

If the command prints a path, use that workspace. If it says the runtime default applies, it has not printed a resolved path; confirm your Gateway's actual workspace before continuing. The example below uses `~/.openclaw/workspace`, which was the project owner's workspace in their test environment. Replace it with your own workspace path if different. See OpenClaw's [config guide](https://docs.openclaw.ai/cli/config) for how unset settings are reported.

```bash
cd ~/.openclaw/workspace
npx skills add apismith-labs/instagram-ai-agent-skills \
  --skill instagram-transcript-extractor \
  -a openclaw
```

When prompted for the installation scope, choose **Project**.

The CLI may offer to install `find-skills`, an optional search helper. You can skip it; it is not needed to install this Skill. After installation, check the Skill for the `main` agent:

```bash
openclaw skills check --agent main
```

Start a new session and select the Skill with `$instagram-transcript-extractor`. Direct installation from GitHub does not depend on the Skill appearing in the skills.sh search directory. See the [OpenClaw guide](docs/platforms/openclaw.md) for Apify setup and the other installation options.

## Try a request

After completing setup and selecting or activating the Skill as described in your platform guide, replace the example with a real public Instagram link:

```text
Get the transcript of this public Instagram Reel and give me a short summary:
https://www.instagram.com/reel/REPLACE_WITH_A_REAL_LINK/
```

## Copy-ready prompts

OpenClaw and Codex use `$instagram-transcript-extractor` for explicit invocation; other platforms use the method in their guide. Replace every bracketed placeholder and remove unused URL list lines before sending a prompt.

### Transcript and translation

```text
Use Instagram Transcript Extractor for this public Instagram Reel:
[PUBLIC_INSTAGRAM_REEL_URL]

Return the transcript in the language actually returned, followed by a faithful, natural translation into [TARGET_LANGUAGE, e.g., Korean]. Keep the original transcript and translation clearly separate. Include timestamps only if valid timestamps were actually returned. Do not invent missing words or timestamps.
```

### Subtitle file

```text
Use Instagram Transcript Extractor for this public Instagram Reel:
[PUBLIC_INSTAGRAM_REEL_URL]

Prepare [SRT or VTT] subtitles in [SUBTITLE_LANGUAGE, e.g., Korean]. Use the transcript and valid timestamps actually returned. If timing information is unavailable or invalid, say so; do not invent timings. Create a downloadable file only if this platform supports file export. Otherwise provide the complete subtitle text for me to copy. Label the subtitle language. The subtitle file or text is generated from the transcript; it is not supplied as a file by the transcript service.
```

### Single-video insight analysis

```text
Use Instagram Transcript Extractor for this public Instagram Reel:
[PUBLIC_INSTAGRAM_REEL_URL]

Base your analysis on the transcript actually returned. Identify the hook/opening, core idea, content structure and supporting points, call to action, likely target audience, and reusable presentation or topic angles. Separate transcript-supported facts from your interpretations. Do not infer views, likes, or other performance data that was not returned.
```

### Batch competitor-content comparison

```text
Use Instagram Transcript Extractor to process these URLs as one batch only if the connected processing tool accepts this input and it fits my account and platform limits. Report each URL separately:
- [PUBLIC_INSTAGRAM_URL_1]
- [PUBLIC_INSTAGRAM_URL_2]
- [ADD_MORE_PUBLIC_INSTAGRAM_URLS_AS_NEEDED]

For each input, preserve the exact URL and report its processing status. Match results by URL, never by result order. In a table, compare each video's hook, topic, core idea, call to action, and reusable presentation choices, then summarize shared themes and differences. Clearly flag failures, uncertain matches, and incomplete transcripts. Do not invent views, likes, comments, or other data. Do not add links or retry automatically.
```

### Batch translation and subtitles

```text
Use Instagram Transcript Extractor to process these URLs as one batch only if the connected processing tool accepts this input and it fits my account and platform limits. Use the same target language for every URL and report each separately:
- [PUBLIC_INSTAGRAM_URL_1]
- [PUBLIC_INSTAGRAM_URL_2]
- [ADD_MORE_PUBLIC_INSTAGRAM_URLS_AS_NEEDED]

For each URL, preserve the exact input and report its own processing status, transcript in the language actually returned, translation into [TARGET_LANGUAGE, e.g., Korean], and subtitle text in [SRT or VTT] format in that target language. Match results by URL, never by result order. Use only valid timestamps; do not invent timings. If this platform supports file export, create a separate file for each video with a filename that identifies its URL. Otherwise provide copyable subtitle text. List failed or uncertain matches separately. Do not guess or retry automatically.
```

## What to expect

Not every link will return a complete transcript. Some links may be private, deleted, restricted, or otherwise inaccessible, and videos without detectable speech may not produce a transcript. A batch may include both successful and failed links. Timestamps appear only when available; missing timestamps alone do not mean transcription failed. Summaries, translations, and analysis are based on the transcript, not video imagery, views, or audience response. Downloadable subtitle files depend on the host's export features; the subtitle text can still be provided for copying.

Questions or problems? [Open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues). This project is licensed under the [MIT License](LICENSE).

## Project documentation and maintenance

- [User guide index](docs/README.md)
- [Platform evidence matrix](docs/platform-support.md)
- [Detailed test status](docs/test-status.md)
- [Project architecture](docs/project-architecture.md)

The project currently provides one Skill, Instagram Transcript Extractor, which supports summaries, translations, and analysis based on returned transcript text. Separate Skills for Reels analysis, competitor research, creator analysis, and comment analysis remain future ideas. For maintainers, `skills/instagram-transcript-extractor/` is the distribution source and `.agents/skills/instagram-transcript-extractor/` is a separate Codex project discovery copy that does not sync automatically. See the [architecture guide](docs/project-architecture.md) for maintenance details.
