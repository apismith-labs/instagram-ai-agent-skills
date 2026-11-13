# Instagram Creator Video Insights

Instagram Creator Video Insights reviews public videos—including Reels and regular video posts—for the creator accounts you name. Use Daily Scan for a recent-day review or Weekly Review to summarize the past week. Unlike [Instagram Transcript Extractor](instagram-transcript-extractor.md), which starts from video links you provide, this Skill starts from creator accounts and a time window, then analyzes transcripts returned for eligible videos.

**Current workflow status: in development and unverified.** Creator Video Insights v1.0.6 is available as a GitHub Release ZIP and a ClawHub listing. Distribution does not validate the current workflow.

## Before using it

You need your own Apify account and must connect or authorize Apify separately in the platform where you use the Skill. Installing a Skill does not connect Apify. Usage follows your Apify account and current service terms; check the [Apify Console](https://console.apify.com/) for actual usage. No fixed price or fee cap is promised.

In ChatGPT, install the Skill and connect `Apify MCP` separately. Follow the [ChatGPT setup guide](../platforms/chatgpt.md#1-add-and-authorize-the-apify-mcp-connection); its Work mode `@` picker note is limited to one account-level observation. A separate reported ChatGPT Plus test covered the third Skill's two-URL success path. The Creator report workflow also has one user-reported successful run, but it was not independently replayed; coverage remains partial/uncertain and the number of excluded pinned posts is unknown.

Choose your platform's setup guide:

- [ChatGPT Creator upload instructions](../platforms/chatgpt.md#upload-creator-video-insights): one user-provided report records a successful Creator workflow run through ChatGPT and Apify. It was not independently replayed; coverage remains partial/uncertain and excluded pinned-post count is unknown.
- [Codex desktop app or CLI](../platforms/codex.md#install-creator-video-insights): the Creator task workflow has not been confirmed in Codex.
- [Manus](../platforms/manus.md#use-creator-video-insights): the report workflow has not been confirmed in Manus.
- [Claude Web](../platforms/claude-web.md#use-creator-video-insights-in-claude-web): the full Creator report workflow with Claude and Apify has not been confirmed in this project.
- [Claude Desktop regular chat](../platforms/claude-web.md#use-creator-video-insights-in-claude-desktop-regular-chat): the full Creator report workflow has not been confirmed there.
- [Claude Code](../platforms/claude-web.md#creator-video-insights-in-claude-code): the Creator installation path and full task workflow have not been confirmed in Claude Code.
- [OpenClaw](../platforms/openclaw.md#instagram-creator-video-insights): the ClawHub installation and full task flow have not been confirmed in the project's Gateway environment.

A single user-reported successful run is not independent verification, a complete-coverage guarantee, or evidence of long-term stability. An installation route or visible Skill alone does not verify the complete report workflow. See the [Creator-specific installation table](../../README.md#instagram-creator-video-insights) for the current route and distribution details.

The earlier GitHub [ZIP v1.0.2](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.2/instagram-creator-reels-insights-v1.0.2.zip) and separate [ClawHub listing v1.0.2](https://clawhub.ai/apismith-labs/skills/instagram-creator-reels-insights) are different distribution channels. Use the ZIP only with a platform route that supports it; OpenClaw uses the ClawHub route. Neither artifact should be read as verification of the current in-development workflow.

## What to ask

Replace the placeholders with public creator usernames. `[VIDEO_LIMIT]` is the local maximum number of eligible videos per creator sent for transcript analysis. It is distinct from the Actor `resultsLimit` and is not a fee cap. The project uses `resultsLimit=50` by default based on the owner’s prior runtime observation; the public schema only describes a maximum result count and does not guarantee per-Creator semantics.

**Daily Scan — most recent 24 hours**

```text
Run a Daily Scan for [CREATOR_1] and [CREATOR_2] covering the most recent 24 hours. Give each creator a separate section. Analyze only posts and transcripts actually returned, describe each video's transcript status, and link observations to source posts with short transcript evidence where available. Separate observations from interpretation. Compare creators only when the returned transcripts support it. If coverage is partial or unknown, say results may be incomplete; do not treat no returned posts as proof that no posts were published. Do not infer visuals or invent transcript text or metrics. Process up to [VIDEO_LIMIT] eligible videos per creator.
```

**Weekly Review — most recent 7 days**

```text
Run a Weekly Review for [CREATOR_1] and [CREATOR_2] covering the most recent 7 days. Give each creator a separate section, then summarize recurring topics, hooks, speaking structures, and CTAs only where the returned transcripts support them. Link every finding to its source post and include short transcript evidence. Separate observations from interpretation. If coverage is partial or unknown, say results may be incomplete; no returned post does not prove that no posts were published. Do not infer visuals or invent transcript text or metrics. Process up to [VIDEO_LIMIT] eligible videos per creator.
```

For more examples, see the [Creator Video Insights prompts in the README](../../README.md#instagram-creator-video-insights-prompts).

## Understand the result

The report is based only on posts and transcripts actually returned for your request. It organizes results by creator, shows transcript status, and links findings to the source posts. Coverage can be **partial** or **unknown**; an empty result does not prove that a creator published nothing during the period. Reports label `discovered_returned_in_window` as attributable in-window raw rows with usable URLs (duplicates included), `unknown_media_type` as attributable in-window unknown-type raw rows (duplicates included; URL not required), and `type_video_candidates` as deduplicated usable-URL rows with exact `type == "Video"` before the local processing limit. These counts have different bases and must not be collapsed into a generic “raw records in the target period” label.

Comparisons across creators are included only when the returned transcripts support them. The Skill separates transcript evidence from interpretation. Transcript-based analysis does not establish what appears in the video, how it was edited, the creator's intent, or how viewers responded. Generated summaries and suggestions are interpretations, not transcript text.

## Scope and limitations

- Publication times use the discovery Actor post-time field. Verified numeric Unix-second values are converted to a UTC instant, filtered against the UTC window, then displayed in the requested timezone from that same instant. The displayed timezone is labeled; unverified units remain unverified rather than being guessed. Transcript Actor `timestamp` is run time, not publication time.
- Daily Scan covers the most recent 24 hours; Weekly Review covers the most recent 7 days. Profile Posts requests explicitly set `skipPinnedPosts: true`, which excludes pinned posts, including posts inside the requested window. Reports use the posts and transcripts returned for that request and do not guarantee that every post in the window was found; an excluded-post count is shown only when the Actor returns a verifiable count.
- The per-creator video limit is a local maximum for eligible videos sent for transcript analysis. It is separate from Actor `resultsLimit`, does not limit discovery, and is not a fee cap. If a fully read successful Dataset has fewer returned rows than the configured results limit, the report says only that the returned data was read and the configured limit was not reached; this does not guarantee full time-window coverage. A count at the limit may indicate truncation.
- The Skill analyzes spoken content from returned transcripts. It does not analyze video imagery, editing, audience response, or causes of engagement.
- Runs are initiated by your request. The Skill does not provide automatic scheduling, background monitoring, or cross-session transcript history.
- Only public accounts are in scope. The Skill does not bypass access controls or restrictions.

For help, [open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues). Do not include passwords, API tokens, cookies, session values, or other credentials in an issue or chat.
