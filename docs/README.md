# User guide

This index covers the project's three Instagram Skills and their platform setup instructions. Transcript Extractor and Media Links & Post Insights have current public ClawHub listings. Creator Video Insights v1.0.5 GitHub ZIP and ClawHub updates are prepared candidates pending publication; its current workflow remains in development and unverified.

- [Instagram Transcript Extractor](skills/instagram-transcript-extractor.md) retrieves speech transcripts from public Instagram videos and supports transcript-based summaries, translations, and analysis.
  - Available as the separate [GitHub Release ZIP v0.2.3](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.3/instagram-transcript-extractor-release-v0.2.3.zip) for ZIP-upload platforms and on [ClawHub v1.0.5](https://clawhub.ai/apismith-labs/skills/instagram-transcript-extractor) for OpenClaw (latest and Moderate CLEAN when checked 2026-11-12). These are separate distribution channels with different version numbers.
- [Instagram Media Links & Post Insights](skills/instagram-media-links-and-post-insights.md) returns Actor-supplied media links and verified post fields for public Instagram video posts and Reels.
  - Available as the separate [GitHub Release ZIP v1.0.0](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/instagram-media-links-and-post-insights-v1.0.0/instagram-media-links-and-post-insights-release-v1.0.0.zip) for ZIP-upload platforms and on [ClawHub v1.0.2](https://clawhub.ai/apismith-labs/skills/instagram-media-links-and-post-insights) for OpenClaw (latest and Moderate CLEAN when checked 2026-11-12). These are separate distribution channels with different version numbers.
- [Instagram Creator Video Insights](skills/instagram-creator-reels-insights.md) is intended to provide recent creator-video insights based on returned posts and transcripts. Its v1.0.5 GitHub ZIP and ClawHub updates are candidates pending publication. Its current workflow remains in development and unverified; distribution does not validate the workflow.
  - Its [Creator installation table](../README.md#instagram-creator-video-insights) lists distinct routes for ChatGPT, Claude Web, OpenClaw, Codex, Manus, Claude Desktop, and Claude Code.
  - The [GitHub Release ZIP v1.0.2](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.2/instagram-creator-reels-insights-v1.0.2.zip) and separate [ClawHub listing v1.0.2](https://clawhub.ai/apismith-labs/skills/instagram-creator-reels-insights) are historical distribution artifacts. The v1.0.5 GitHub ZIP and ClawHub updates described above remain candidates pending publication.
  - The ClawHub installation and full task flow have not been confirmed in the project's OpenClaw Gateway; see the [OpenClaw instructions](platforms/openclaw.md#instagram-creator-video-insights).

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

The Apify connection provides access to external Apify tools and account authorization. In ChatGPT, the user can share one `Apify MCP` custom connection across multiple Skills. Each Skill provides instructions for its own task workflow. Installing a Skill does not connect Apify, and connecting Apify does not install a Skill.

## Choose a guide

- [ChatGPT](platforms/chatgpt.md): install the Skill ZIP and add/authorize the `Apify MCP` custom server separately. Ordinary chat uses an explicit Skill name (Skills may auto-select when relevant); the tested Work mode's **@** picker is account-level evidence only. One connection can serve multiple Skills; confirm tools exposed to the current account/workspace.
- [Codex](platforms/codex.md): separate instructions for the Codex desktop app and Codex CLI, followed by the Skill installation and discovery check.
- [Manus](platforms/manus.md): add the Apify MCP endpoint as a custom connector, authorize through OAuth on first use, import the Skill from GitHub, and enable both in chat.
- [Claude Web, Claude Desktop regular chat, and Claude Code CLI](platforms/claude-web.md): Web/Desktop use the account's Apify Plugin/remote connector and separate Skill upload; Claude Code CLI uses its own plugin and MCP setup. The unified Plugins interface is still rolling out.
- [OpenClaw](platforms/openclaw.md):
  - **Instagram Transcript Extractor:** choose its [ClawHub route](platforms/openclaw.md#install-with-the-openclaw-cli-from-clawhub), Control UI, GitHub-source, Vercel Skills CLI, or local-directory route.
  - **Instagram Creator Video Insights:** the planned [ClawHub v1.0.5 candidate route](platforms/openclaw.md#instagram-creator-video-insights) and named GitHub ZIP candidate are separate routes, both pending publication; neither verifies the current workflow, which remains in development and unverified. The ClawHub installation and full task flow are not confirmed in the project Gateway.
  - Install and connect the Apify plugin separately using [Set up the Apify plugin](platforms/openclaw.md#set-up-the-apify-plugin).
- [Instagram Transcript Extractor](skills/instagram-transcript-extractor.md): what to request, what a result means, and common limitations.
- [Instagram Media Links & Post Insights](skills/instagram-media-links-and-post-insights.md): media links, returned post fields, setup, and result limitations.
- [Instagram Creator Video Insights](skills/instagram-creator-reels-insights.md): how to request Daily Scans or Weekly Reviews and understand transcript-based reports.

Follow each platform guide for the Skill-specific setup steps. Installation and Apify authorization are separate.
