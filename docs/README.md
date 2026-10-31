# User guide

This guide helps you choose a platform and start with the available [Instagram Transcript Extractor](skills/instagram-transcript-extractor.md). The project currently has one available skill; future ideas are listed in the [project README](../README.md), not as installable features.

## The common setup flow

```mermaid
flowchart LR
    A[Choose a platform] --> B[Create or sign in to Apify]
    B --> C[Connect Apify and authorize]
    C --> D[Install or enable the skill]
    D --> E[Start a new conversation and use it]
```

In words: choose ChatGPT, Codex, Manus, Claude Web, Claude Desktop regular chat, or Claude Code; create or sign in to your own Apify account; connect Apify and install or enable the Instagram Transcript Extractor Skill as needed for that environment; then start a conversation and request a transcript. Some clients reuse account-level setup. Follow the platform-specific guide because setup steps differ by environment.

The Apify plugin/MCP connection provides access to external Apify tools and account authorization. The Skill provides instructions for the transcript task. Installing the Skill does not connect Apify, and connecting Apify does not install the Skill.

## Choose a guide

- [ChatGPT](platforms/chatgpt.md): connect and authorize Apify first, then upload the Skill ZIP.
- [Codex](platforms/codex.md): separate instructions for the Codex desktop app and Codex CLI, followed by the Skill installation and discovery check.
- [Manus](platforms/manus.md): enable the Apify Connector, import the Skill from GitHub, and select it in chat.
- [Claude Web, Claude Desktop regular chat, and Claude Code](platforms/claude-web.md): set up Apify and upload the Skill in Claude Web, use the same account in Claude Desktop regular chat (one single-Reel call is reported successful), or follow the separate, untested Claude Code workflow.
- [Instagram Transcript Extractor](skills/instagram-transcript-extractor.md): what to request, what a result means, and common limitations.

These guides distinguish published platform instructions from this project's test evidence. See the [platform evidence matrix](platform-support.md) and [detailed test status](test-status.md) for what has and has not been tested.
