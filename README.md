# Instagram AI Agent Skills

Get spoken transcripts from public Instagram Reels and videos with AI agent skills. Start with **Instagram Transcript Extractor**: give it one or more links, then ask for a summary, translation, or analysis of the returned text.

## Available skill: Instagram Transcript Extractor

The Skill returns spoken words for accessible videos and may include timestamps when available. You can request a summary or translation alongside the transcript. Results are not guaranteed for every link.

Download the [v0.1.0 Skill ZIP](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.1.0/instagram-transcript-extractor.zip) for ChatGPT or Claude web. SHA-256: `cb5173bf999cb54feb06f190736111afaccb91ceae0bd845327391208ffcb331`. Download this named Release asset, not GitHub's automatically generated **Source code (zip)**. Keep the ZIP intact when uploading it to either platform.

## What you need

Use your own [Apify account](https://console.apify.com/). Actor runs use that account's plan allowance; check Apify Console for current Runs and billing details. Connecting Apify and installing a Skill are separate steps: the connection provides external tools, while the Skill provides the task workflow.

## Choose your platform

| Platform | Setup order |
| --- | --- |
| [ChatGPT](docs/platforms/chatgpt.md) | Connect Apify with the custom MCP/plugin OAuth flow → upload the named v0.1.0 ZIP → start a new conversation, select the Apify plugin with **@**, and request a transcript. Skill availability may depend on your account and workspace. |
| [Codex](docs/platforms/codex.md) | Install the Apify plugin and authorize with OAuth → install the Skill using the documented Codex installer flow → start a new session, confirm discovery, then explicitly invoke it. The guide covers Codex desktop and CLI separately. |
| [Manus](docs/platforms/manus.md) | Enable the existing Apify Connector and authorize with OAuth → import the Skill folder from GitHub → in chat select it with **/** and confirm the Apify Connector is enabled. Manus tasks using the Connector may consume Manus credits. |
| [Claude web](docs/platforms/claude-web.md) | Add the Apify Plugin and connect its Apify Connector with OAuth → upload and enable the named Skill ZIP → in chat select the Skill and enable the Apify Connector. |

## Try a request

Replace the example with a real public Instagram link:

First activate Instagram Transcript Extractor using the method in your platform guide. This example is the task request; it does not activate the Skill for you.

```text
Get the transcript of this public Instagram Reel and give me a short summary:
https://www.instagram.com/reel/REPLACE_WITH_A_REAL_LINK/
```

## What to expect

Some links may be private, deleted, restricted, or otherwise inaccessible; a video without detectable speech may not produce a transcript. A batch can have both successful and failed links. Missing timestamps alone do not mean transcription failed. Text-based analysis is based on the transcript, not video imagery, performance metrics, or audience response.

Questions or problems? [Open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues). This project is licensed under the [MIT License](LICENSE).

## Project documentation and maintenance

- [User guide index](docs/README.md)
- [Platform evidence matrix](docs/platform-support.md)
- [Detailed test status](docs/test-status.md)
- [Project architecture](docs/project-architecture.md)

The project currently provides this one Skill; Reels analysis, competitor research, creator analysis, and comment analysis remain future ideas. For maintainers, `skills/instagram-transcript-extractor/` is the distribution source and `.agents/skills/instagram-transcript-extractor/` is a separate Codex project discovery copy that does not sync automatically. See the [architecture guide](docs/project-architecture.md) for maintenance details.
