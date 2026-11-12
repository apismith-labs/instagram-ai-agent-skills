# Instagram Media Links & Post Insights

Instagram Media Links & Post Insights works with public Instagram video posts and Reels that you provide. It can return video/audio links supplied by its Actor or organize post fields that the Actor actually returns. It does not download media files, and it does not guarantee that every field will be present.

The Skill uses the [Instagram Video Scraper API Actor on Apify](https://apify.com/apple_yang/instagram-video-scraper-api). Its current public ClawHub listing is [v1.0.1](https://clawhub.ai/apismith-labs/skills/instagram-media-links-and-post-insights), checked on 2026-11-12. There is no named GitHub Release ZIP for this Skill. The ClawHub listing is an OpenClaw distribution, not a ZIP package version or a ChatGPT upload package.

## Before using it

To run the Skill, you need your own Apify account and an Apify MCP/plugin connection that your Agent host supports and has authorized. Installing the Skill and connecting or authorizing Apify are separate steps; installing the Skill does not create an account or configure the connection. You can install the Skill before setting up Apify.

Follow the setup guide for your host:

- [ChatGPT](../platforms/chatgpt.md): this project does not currently provide a named GitHub Release ZIP for uploading this Skill.
- [Codex](../platforms/codex.md): the repository provides general local Skill-directory installation guidance; it is not a Media-specific end-to-end verification.
- Manus: no Media-specific Manus installation route is documented. The [general Manus guide](../platforms/manus.md) covers only its documented platform setup and does not establish that this Skill is supported there.
- [Claude](../platforms/claude-web.md): this project does not currently provide a named GitHub Release ZIP for uploading this Skill.
- [OpenClaw](../platforms/openclaw.md#media-links-post-insights-installation)

## Choose a mode

### Media links

Ask for the `videoUrl` and/or `audioUrl` links actually returned by the Actor. A returned link is a direct URL, not a downloaded file, and it may not remain valid. If a field is missing, the Skill reports it as unavailable rather than treating it as zero or assuming the media does not exist.

Example:

```text
Return the video and audio links actually provided for this public Instagram Reel. Keep the original URL with the result, and say if either field is missing.
https://www.instagram.com/reel/REPLACE_WITH_A_REAL_LINK/
```

### Post insights

Ask the Skill to organize or compare raw fields returned by the Actor, such as likes, comments, author, and publish time. A run is a snapshot of that collection. The Skill does not calculate engagement rates from unverified inputs or infer trends, audience response, performance changes, or causes.

Example:

```text
Organize the author, publish time, likes, and comments actually returned for these public Instagram video posts or Reels. Compare only the returned raw counts. Do not calculate rates or infer trends, audience response, performance changes, or causes.
[PUBLIC_INSTAGRAM_URLS]
```

If you want both modes, ask for both; where possible, the Skill uses the same Actor result. If your request is unclear, it may ask which results you want.

## How results are matched

The Skill preserves each input URL and matches results using verifiable evidence from the returned `url` field. It does not assign results by output order or guess from unverified IDs. If a match cannot be established, it explains the observed state using your language; that does not prove the Actor failed or that the post does not exist. Missing, empty, or unreturned fields are reported as unavailable, not as zero.

If the tool returns an `errMsg`, the Skill reports the actual message without inventing a cause. In a batch, confirmed, errored, unmatched, and unresolved inputs are reported separately; partial results are not described as full success.

## Scope and limitations

- The Skill handles only public video post and Reel URLs you provide. A `/p/` URL is a post path and does not by itself establish that the content is a video.
- Photo and carousel posts are not included in the first-release support commitment; their behavior remains unverified. If the media type cannot be confirmed, the Skill does not guess or promise a video/audio link.
- Post insights include only raw fields actually returned and otherwise verified. The Skill does not promise views, play count, impressions, reach, follower counts, or other unverified fields.
- Missing fields are not zero. Comparisons are not trend analysis, performance conclusions, audience-reaction claims, or causal findings.
- The Skill does not discover account posts, monitor on a schedule, extract transcripts, interpret visuals, or save media files.
- Runs use your Apify account. Check the [Apify Console](https://console.apify.com/) for current usage; no fixed price or cost estimate is promised.

## Install for OpenClaw

The current ClawHub listing is `@apismith-labs/instagram-media-links-and-post-insights`. In the environment connected to your OpenClaw Gateway, run:

```sh
openclaw skills install @apismith-labs/instagram-media-links-and-post-insights
```

By default, the CLI installs into the active workspace. Add `--global` for the shared managed Skills directory. Check the installation with `openclaw skills check`, then select `$instagram-media-links-and-post-insights` in a new session. Set up and authorize the Apify plugin separately using the [OpenClaw guide](../platforms/openclaw.md#set-up-the-apify-plugin).

For platform-specific help, open a [GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues). Do not include credentials or private Instagram content.
