# Instagram Creator Reels Insights

Instagram Creator Reels Insights reviews recent public Reels for the creator accounts you name. Use Daily Scan for a recent-day review or Weekly Review to summarize the past week. Unlike [Instagram Transcript Extractor](instagram-transcript-extractor.md), which starts from video links you provide, this Skill starts from creator accounts and a time window, then analyzes transcripts returned for eligible videos.

## Before using it

You need your own Apify account and must connect or authorize Apify separately in the platform where you use the Skill. Installing a Skill does not connect Apify. Usage follows your Apify account and current service terms; check the [Apify Console](https://console.apify.com/) for actual usage. No fixed price or fee cap is promised.

In ChatGPT, one authorized `Apify MCP` custom connection can be shared across Skills. Follow the [ChatGPT setup guide](../platforms/chatgpt.md#1-add-and-authorize-the-apify-mcp-connection) and confirm the tools currently exposed in your account. A separate reported ChatGPT Plus test covered only the third Skill's two-URL success path; it does not verify this Creator report workflow.

Choose your platform's setup guide:

- [ChatGPT Creator upload instructions](../platforms/chatgpt.md#upload-creator-reels-insights): the project has not confirmed the Creator report workflow through ChatGPT and Apify.
- [Codex desktop app or CLI](../platforms/codex.md#install-creator-reels-insights): the Creator task workflow has not been confirmed in Codex.
- [Manus](../platforms/manus.md#use-creator-reels-insights): the report workflow has not been confirmed in Manus.
- [Claude Web](../platforms/claude-web.md#use-creator-reels-insights-in-claude-web): the full Creator report workflow with Claude and Apify has not been confirmed in this project.
- [Claude Desktop regular chat](../platforms/claude-web.md#use-creator-reels-insights-in-claude-desktop-regular-chat): the full Creator report workflow has not been confirmed there.
- [Claude Code](../platforms/claude-web.md#creator-reels-insights-in-claude-code): the Creator installation path and full task workflow have not been confirmed in Claude Code.
- [OpenClaw](../platforms/openclaw.md#instagram-creator-reels-insights): the ClawHub installation and full task flow have not been confirmed in the project's Gateway environment.

An installation route or visible Skill does not by itself mean that the complete report workflow has been verified on that platform. See the [Creator-specific installation table](../../README.md#instagram-creator-reels-insights) for the current route and distribution details.

The GitHub [ZIP v1.0.2](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.2/instagram-creator-reels-insights-v1.0.2.zip) and the separate [ClawHub listing v1.0.2](https://clawhub.ai/apismith-labs/skills/instagram-creator-reels-insights) are different distribution channels. Use the ZIP only with a platform route that supports it; OpenClaw uses the ClawHub route.

## What to ask

Replace the placeholders with public creator usernames. `[VIDEO_LIMIT]` is the maximum number of discovered videos per creator sent for transcript analysis. It does not limit how many posts are discovered and is not a fee cap.

**Daily Scan — most recent 24 hours**

```text
Run a Daily Scan for [CREATOR_1] and [CREATOR_2] covering the most recent 24 hours. Give each creator a separate section. Analyze only posts and transcripts actually returned, describe each video's transcript status, and link observations to source posts with short transcript evidence where available. Separate observations from interpretation. Compare creators only when the returned transcripts support it. If coverage is partial or unknown, say results may be incomplete; do not treat no returned posts as proof that no posts were published. Do not infer visuals or invent transcript text or metrics. Process up to [VIDEO_LIMIT] eligible videos per creator.
```

**Weekly Review — most recent 7 days**

```text
Run a Weekly Review for [CREATOR_1] and [CREATOR_2] covering the most recent 7 days. Give each creator a separate section, then summarize recurring topics, hooks, speaking structures, and CTAs only where the returned transcripts support them. Link every finding to its source post and include short transcript evidence. Separate observations from interpretation. If coverage is partial or unknown, say results may be incomplete; no returned post does not prove that no posts were published. Do not infer visuals or invent transcript text or metrics. Process up to [VIDEO_LIMIT] eligible videos per creator.
```

For more examples, see the [Creator Reels Insights prompts in the README](../../README.md#instagram-creator-reels-insights-prompts).

## Understand the result

The report is based only on posts and transcripts actually returned for your request. It organizes results by creator, shows transcript status, and links findings to the source posts. Coverage can be **partial** or **unknown**; an empty result does not prove that a creator published nothing during the period.

Comparisons across creators are included only when the returned transcripts support them. The Skill separates transcript evidence from interpretation. Transcript-based analysis does not establish what appears in the video, how it was edited, the creator's intent, or how viewers responded. Generated summaries and suggestions are interpretations, not transcript text.

## Scope and limitations

- Daily Scan covers the most recent 24 hours; Weekly Review covers the most recent 7 days. Reports use the posts and transcripts returned for that request and do not guarantee that every post in the window was found.
- The per-creator video limit is the maximum number of discovered videos sent for transcript analysis. It does not limit how many posts are discovered and is not a fee cap.
- The Skill analyzes spoken content from returned transcripts. It does not analyze video imagery, editing, audience response, or causes of engagement.
- Runs are initiated by your request. The Skill does not provide automatic scheduling, background monitoring, or cross-session transcript history.
- Only public accounts are in scope. The Skill does not bypass access controls or restrictions.

For help, [open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues). Do not include passwords, API tokens, cookies, session values, or other credentials in an issue or chat.
