# Instagram Transcript Extractor

This guide covers Instagram Transcript Extractor only. For Instagram Creator Video Insights, start with its [dedicated user guide](instagram-creator-reels-insights.md); you can also see the [Creator request examples in the project README](../../README.md#instagram-creator-video-insights-prompts) and its [SKILL.md](../../skills/instagram-creator-reels-insights/SKILL.md).

Instagram Transcript Extractor retrieves the spoken transcript actually returned for public Instagram video or Reel links. You can request a summary, translation, or analysis based on that text; a transcript is not guaranteed for every video. See the [Instagram Transcripts Scraper Actor on Apify](https://apify.com/apple_yang/instagram-transcripts-scraper).

The current ClawHub listing is [v1.0.4](https://clawhub.ai/apismith-labs/skills/instagram-transcript-extractor) (latest and moderation-clean when checked 2026-11-12). The separate GitHub Release package is [ZIP v0.2.2](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.2/instagram-transcript-extractor-v0.2.2.zip). ClawHub and GitHub ZIPs are separate distribution channels and use independent version numbers.

## Before using it

To run this Skill, you need your own Apify account and an Apify MCP/plugin connection supported and authorized by your Agent host. Installing the Skill does not create an account or connect or authorize Apify; you can install it before completing that setup. Runs use your account's plan allowance; check the [Apify Console](https://console.apify.com/) for current Runs and billing details. Follow the setup guide for your platform:

- [ChatGPT setup](../platforms/chatgpt.md)
- [Codex setup](../platforms/codex.md)
- [Manus setup](../platforms/manus.md)
- [Claude Web, Claude Desktop regular chat, and Claude Code setup](../platforms/claude-web.md)
- [OpenClaw setup](../platforms/openclaw.md)

For OpenClaw, install from the [ClawHub listing](https://clawhub.ai/apismith-labs/skills/instagram-transcript-extractor) with the OpenClaw CLI, use the Control UI, install from GitHub with Vercel Skills CLI, or install from a local repository directory. See the [OpenClaw guide](../platforms/openclaw.md#instagram-transcript-extractor) for steps and the distinct confirmation limits of these routes.

Connecting Apify makes external Apify tools available to the platform. Installing this Skill provides the transcript workflow. They are separate steps. In ChatGPT, install the Skill and connect `Apify MCP` separately. The [ChatGPT setup guide](../platforms/chatgpt.md#1-add-and-authorize-the-apify-mcp-connection) distinguishes regular chat from the Work mode picker observed in one account; the `@` picker is not guaranteed across accounts or surfaces. A separate reported ChatGPT Plus test covered only the Media Links Skill's two-URL success path; it does not verify this Transcript Extractor workflow.

## What to ask

For one link:

```text
Get the transcript of this public Instagram video:
https://www.instagram.com/reel/REPLACE_WITH_A_REAL_LINK/
```

For several links with summaries:

```text
Get the transcript of each public Instagram video and give me a short summary of each:
https://www.instagram.com/reel/REPLACE_WITH_A_REAL_LINK_1/
https://www.instagram.com/reel/REPLACE_WITH_A_REAL_LINK_2/
```

Replace each example with a real public link. You can request a translation or a text-based analysis as well. The Skill should keep results associated with their input links and identify items that could not be matched or completed; it should not guess a missing result.

## Understand the result

When successful, expect the spoken words returned for the accessible link. A requested summary, translation, or text analysis should be presented separately from the transcript. Timestamps may be included when available; missing timestamps do not by themselves mean transcription failed. The Skill does not guarantee a complete transcript for every video.

- A video with no detectable speech may not yield a transcript.
- A private, deleted, restricted, or otherwise inaccessible video may not be processable.
- In a batch, some links may succeed while others fail. Use the successful results and review the listed failures individually; one successful item does not mean every item succeeded.
- Text-based analysis uses the returned transcript. It does not establish what appears in the video, its performance metrics, or audience reaction.

If the platform says Apify is not connected, complete the connection in its platform guide and then try again. If a result is missing or unclear, ask the agent to explain which link it could not process. For help with the Skill, [open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues) without including credentials or private content.
