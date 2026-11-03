# Instagram AI Agent Skills

Get spoken transcripts from public Instagram Reels and videos with AI agent skills. Start with **Instagram Transcript Extractor**: give it one or more links, then ask for a summary, translation, or analysis of the returned text.

## Available skill: Instagram Transcript Extractor

The Skill returns spoken words for accessible videos and may include timestamps when available. You can request a summary or translation alongside the transcript. Results are not guaranteed for every link.

OpenClaw users can find [Instagram Transcript Extractor on ClawHub](https://clawhub.ai/apismith-labs/skills/instagram-transcript-extractor) as `@apismith-labs/instagram-transcript-extractor` (the project owner reports version 1.0.0). Before installing, review the linked [security audit](https://clawhub.ai/apismith-labs/skills/instagram-transcript-extractor/security-audit) for its listed findings and separate static-analysis result.

Download the [v0.1.0 Skill ZIP](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.1.0/instagram-transcript-extractor.zip) for ChatGPT or Claude Web. SHA-256: `cb5173bf999cb54feb06f190736111afaccb91ceae0bd845327391208ffcb331`. Download this named Release asset, not GitHub's automatically generated **Source code (zip)**. Keep the ZIP intact when uploading it in either web app. In the project owner's reported account, the Skill appeared in Claude Desktop regular chat after signing into that same account, without another upload.

## What you need

Use your own [Apify account](https://console.apify.com/). Actor runs use that account's plan allowance; check Apify Console for current Runs and billing details. Connecting Apify and installing a Skill are separate steps: the connection provides external tools, while the Skill provides the task workflow.

## Choose your platform

| Platform | Setup order |
| --- | --- |
| [ChatGPT](docs/platforms/chatgpt.md) | Connect Apify with the custom MCP/plugin OAuth flow → upload the named v0.1.0 ZIP → start a new conversation, select the Apify plugin with **@**, and request a transcript. Skill availability may depend on your account and workspace. |
| [Codex](docs/platforms/codex.md) | Install the Apify plugin and authorize with OAuth → install the Skill using the documented Codex installer flow → start a new session, confirm discovery, then explicitly invoke it. The guide covers Codex desktop and CLI separately. |
| [Manus](docs/platforms/manus.md) | Enable the existing Apify Connector and authorize with OAuth → import the Skill folder from GitHub → in chat select it with **/** and confirm the Apify Connector is enabled. Manus tasks using the Connector may consume Manus credits. |
| [Claude Web, Claude Desktop regular chat, and Claude Code](docs/platforms/claude-web.md) | Set up Apify and upload the Skill once in Claude Web → use the same account in Claude Desktop regular chat (one single-Reel call is reported successful). Claude Code has separate setup and remains untested for this project. |
| [OpenClaw](docs/platforms/openclaw.md) | Recommended: search/add through the OpenClaw Control UI. The ClawHub CLI is an alternative; GitHub local-directory `--global` install is a backup route the project owner reports testing. Control UI and ClawHub-native CLI installs are untested on the owner's Gateway; Actor runs remain untested. |

## Try a request

Replace the example with a real public Instagram link:

This is a task request; activate the Skill using the method in your platform guide before sending it.

```text
Get the transcript of this public Instagram Reel and give me a short summary:
https://www.instagram.com/reel/REPLACE_WITH_A_REAL_LINK/
```

## Copy-ready prompts

Before using a prompt, select or activate **Instagram Transcript Extractor** in your current host; the prompt is the task request and does not replace that step. OpenClaw and Codex use `$instagram-transcript-extractor` for explicit invocation; other hosts should follow their platform guides. The Skill also requires your own Apify connection, which installation does not configure. Replace every bracketed placeholder, and remove any unused URL list lines. Results are not guaranteed for every link.

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

Prepare subtitles in [SRT or VTT] format, in [SUBTITLE_LANGUAGE, e.g., Korean]. The subtitle language is configurable. Use only the transcript actually returned and valid timestamps. If timestamps are unavailable or invalid, say so and do not make up timings. Create a downloadable file only if this platform supports file export; otherwise provide the complete subtitle text for me to copy. Label the subtitle language clearly. Do not claim the Actor returned a subtitle file.
```

### Single-video insight analysis

```text
Use Instagram Transcript Extractor for this public Instagram Reel:
[PUBLIC_INSTAGRAM_REEL_URL]

Base your analysis on the transcript actually returned. Identify the hook/opening, core idea, content structure and supporting points, call to action, likely target audience, and reusable presentation or topic angles. Separate transcript-supported facts from your interpretations. Do not infer views, likes, or other performance data that was not returned.
```

### Batch competitor-content comparison

```text
Use Instagram Transcript Extractor to process these URLs as a batch when allowed by the current Actor schema and account or host limits, and report each URL separately:
- [PUBLIC_INSTAGRAM_URL_1]
- [PUBLIC_INSTAGRAM_URL_2]
- [ADD_MORE_PUBLIC_INSTAGRAM_URLS_AS_NEEDED]

For each input, preserve the exact original URL and report its own processing status. Match results to URLs explicitly; do not infer a match from result order. In a table, compare each video's hook, topic, core idea, call to action, and reusable presentation choices, then summarize shared themes and differences. Clearly flag failures, uncertain URL matches, and incomplete transcripts. Do not invent views, likes, comments, or other data that was not returned. Do not add links or retry automatically.
```

### Batch translation and subtitles

```text
Use Instagram Transcript Extractor to process these URLs as a batch when allowed by the current Actor schema and account or host limits, and report each URL separately:
- [PUBLIC_INSTAGRAM_URL_1]
- [PUBLIC_INSTAGRAM_URL_2]
- [ADD_MORE_PUBLIC_INSTAGRAM_URLS_AS_NEEDED]

Translate each transcript into [TARGET_LANGUAGE, e.g., Korean] and prepare subtitles in [SRT or VTT] format in that same target language. Use one target language for every URL in this batch. For every input, preserve the exact original URL and provide its own processing status, transcript in the language actually returned, translation, and subtitle text. Match results to URLs explicitly, never by result order. Use only validated timestamps; do not invent timings. If this platform supports file export, create a separate file for each video with a filename that identifies its URL. Otherwise provide copyable subtitle text. List failed or uncertain matches separately. Do not guess or retry automatically.
```

## What to expect

Some links may be private, deleted, restricted, or otherwise inaccessible; a video without detectable speech may not produce a transcript. A batch can have both successful and failed links. Missing timestamps alone do not mean transcription failed. Text-based analysis is based on the transcript, not video imagery, performance metrics, or audience response.

Questions or problems? [Open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues). This project is licensed under the [MIT License](LICENSE).

## Project documentation and maintenance

- [User guide index](docs/README.md)
- [Platform evidence matrix](docs/platform-support.md)
- [Detailed test status](docs/test-status.md)
- [Project architecture](docs/project-architecture.md)

The project currently provides one Skill, Instagram Transcript Extractor, which supports summaries, translations, and analysis based on returned transcript text. Separate Skills for Reels analysis, competitor research, creator analysis, and comment analysis remain future ideas. For maintainers, `skills/instagram-transcript-extractor/` is the distribution source and `.agents/skills/instagram-transcript-extractor/` is a separate Codex project discovery copy that does not sync automatically. See the [architecture guide](docs/project-architecture.md) for maintenance details.
