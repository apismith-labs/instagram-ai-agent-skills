# User guide

This guide helps you choose between two Instagram Skills and find their platform setup instructions:

- [Instagram Transcript Extractor](skills/instagram-transcript-extractor.md) retrieves speech transcripts from public Instagram videos and supports transcript-based summaries, translations, and analysis.
- [Instagram Creator Reels Insights](platforms/openclaw.md#instagram-creator-reels-insights) is available on ClawHub v1.0.1 for OpenClaw and as the separate GitHub v1.0.0 ZIP for upload platforms. Use the ZIP for the Skill you want: [ChatGPT upload guide](platforms/chatgpt.md) or [Claude Web guide](platforms/claude-web.md). It creates per-creator Daily Scan or Weekly Review insights from posts and transcripts actually returned.

Each Skill has its own installation path. Connecting Apify is a separate setup step from installing a Skill.

## The common setup flow

```mermaid
flowchart LR
    A[Choose a platform] --> B[Create or sign in to Apify]
    B --> C[Connect Apify and authorize]
    C --> D[Install or enable the skill]
    D --> E[Start a new conversation and use it]
```

In words: choose a platform and Skill; create or sign in to your own Apify account; connect Apify and install or enable that Skill as supported in the environment; then start a conversation and make a request. Some clients reuse account-level setup. Follow the platform-specific guide because setup steps differ by environment.

The Apify plugin/MCP connection provides access to external Apify tools and account authorization. Each Skill provides instructions for its own task workflow. Installing a Skill does not connect Apify, and connecting Apify does not install a Skill.

## Choose a guide

- [ChatGPT](platforms/chatgpt.md): connect and authorize Apify first, then upload the ZIP for the Skill you need.
- [Codex](platforms/codex.md): separate instructions for the Codex desktop app and Codex CLI, followed by the Skill installation and discovery check.
- [Manus](platforms/manus.md): enable the Apify Connector, import the Skill from GitHub, and select it in chat.
- [Claude Web, Claude Desktop regular chat, and Claude Code](platforms/claude-web.md): set up Apify and upload the Skill in Claude Web, use the same account in Claude Desktop regular chat, or follow the separate Claude Code setup instructions.
- [OpenClaw](platforms/openclaw.md): install Instagram Creator Reels Insights v1.0.1 from ClawHub; this route and its full task flow are not yet confirmed in the project's Gateway. The same guide has separate ClawHub, GitHub, and local-directory installation instructions for Instagram Transcript Extractor.
- [Instagram Transcript Extractor](skills/instagram-transcript-extractor.md): what to request, what a result means, and common limitations.

Follow each platform guide for the Skill-specific setup steps. Installation and Apify authorization are separate.
