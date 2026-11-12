# Instagram Skills in OpenClaw

This guide covers Instagram Transcript Extractor and Instagram Media Links & Post Insights, which have current ClawHub listings, and the existing Creator Video Insights listing. Creator's current workflow remains in development and unverified. Install the Skill you need, then connect the Apify plugin separately using [Set up the Apify plugin](#set-up-the-apify-plugin).

## Instagram Creator Video Insights

Use this Skill to review one or more public creator accounts through their returned transcripts and identify topics, opening hooks, and speaking structures. Daily Scan covers the most recent 24 hours; Weekly Review covers the most recent 7 days. Reports keep findings separate by creator.

An existing [ClawHub listing v1.0.2](https://clawhub.ai/apismith-labs/skills/instagram-creator-reels-insights) is available. This is an earlier distribution; the current Creator workflow remains in development and unverified. The OpenClaw CLI documents this ClawHub install command:

```sh
openclaw skills install @apismith-labs/instagram-creator-reels-insights
```

By default, the OpenClaw CLI installs into the active workspace's `skills/` directory. Add `--global` to use the shared managed Skills directory:

```sh
openclaw skills install @apismith-labs/instagram-creator-reels-insights --global
```

After installation, check the default Agent's readiness and visibility:

```sh
openclaw skills check
```

To check a specific Agent, use `openclaw skills check --agent YOUR_AGENT_ID`, replacing `YOUR_AGENT_ID` with its ID; if you do not know the ID, omit `--agent`. Then open a new session and select `$instagram-creator-reels-insights`.

The command follows the [OpenClaw Skills CLI documentation](https://docs.openclaw.ai/cli/skills). The ClawHub installation itself and an end-to-end task using this route have not yet been confirmed in this project's Gateway environment. The current in-development Creator workflow has not been updated through this listing.

If the Skill is not listed, confirm you are checking the same Gateway where it was installed. You can inspect the active workspace setting with:

```sh
openclaw config get agents.defaults.workspace
```

If the command reports that the runtime default applies instead of printing a path, use the runtime default; do not treat an undisplayed path as a fixed location. Also confirm that the install went to the active workspace or shared managed directory. If it still does not appear, [report the issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues).

Before your first Creator report, complete the shared Apify setup below. After setup, start a new session or refresh the available tools, then select Creator Video Insights. For a multi-creator weekly review, you can ask:

```text
$instagram-creator-reels-insights Review these public creator accounts for the most recent 7 days: [CREATOR_1], [CREATOR_2], and [CREATOR_3]. Process up to [VIDEO_LIMIT] eligible videos per creator. Give each creator a separate summary, then compare topics, hooks, speaking structures, and CTAs only where the returned transcripts support it. Link each insight to its source post and short transcript evidence. Separate observations from interpretation. If results are partial or unknown, explain that they may be incomplete. Do not say no posts were made just because none were returned, and do not imply unreturned posts were reviewed.
```

`[VIDEO_LIMIT]` limits how many discovered videos per creator are sent to transcript analysis. It is not a discovery cap or a fee cap.

Reports are based on posts and transcripts returned for the request; they do not guarantee that every post in the period was found. The ClawHub copy is listed under MIT-0; the repository uses MIT.

<a id="media-links-post-insights-installation"></a>

## Instagram Media Links & Post Insights

The current [ClawHub listing is v1.0.1](https://clawhub.ai/apismith-labs/skills/instagram-media-links-and-post-insights). Install it in the environment used by your OpenClaw Gateway with:

```sh
openclaw skills install @apismith-labs/instagram-media-links-and-post-insights
```

By default, the CLI installs into the active workspace. Add `--global` for the shared managed Skills directory. Run `openclaw skills check`, open a new session, and select `$instagram-media-links-and-post-insights`. Confirm the selected Agent can see the Skill and the `apify` tool. The OpenClaw [Skills CLI guide](https://docs.openclaw.ai/cli/skills) documents installation and readiness checks. This ClawHub listing is not a GitHub Release ZIP; no named GitHub ZIP is currently available for this Skill. For behavior and limits, see the [Media Links & Post Insights user guide](../skills/instagram-media-links-and-post-insights.md) and the [Instagram Video Scraper API Actor](https://apify.com/apple_yang/instagram-video-scraper-api).

## Set up the Apify plugin

Use OpenClaw 2026.1.0 or later with Node.js 22+. An Apify account and the Apify plugin are separate prerequisites for these Skills. If you do not have an Apify account, [create one in the Apify Console](https://console.apify.com/sign-up). Choose one way to install the Apify OpenClaw plugin:

- Run the OpenClaw CLI command:

```sh
openclaw plugins install @apify/apify-openclaw-plugin
```

- Or, if your OpenClaw Control UI shows the plugin catalog, open **Plugins**, search for **Apify**, and install the Apify listing from ClawHub. If it is not available there, use the CLI command above.

Restart the OpenClaw Gateway after installing the plugin, as directed by the [official plugin README](https://github.com/apify/apify-openclaw-plugin#install). First, prepare an Apify API Key. The [official plugin README](https://github.com/apify/apify-openclaw-plugin) explains how to create and configure it. Then run the plugin's setup wizard and follow its prompts to connect your account:

```sh
openclaw apify setup
```

The plugin supports providing an API Key through its configuration or the `APIFY_API_KEY` environment variable; prefer the setup wizard where possible. Never send an API Key, password, cookie, or other credential in chat or commit it to the repository. See the [official plugin README](https://github.com/apify/apify-openclaw-plugin) for the wizard and other supported configuration options. After setup, run `openclaw gateway restart`, then `openclaw apify status`. Start a new OpenClaw session or refresh the available tools. If the Apify tool is still unavailable to your Agent, review OpenClaw's tool permissions and allow the plugin as needed without replacing existing settings.

## Instagram Transcript Extractor

Instagram Transcript Extractor is available on [ClawHub](https://clawhub.ai/apismith-labs/skills/instagram-transcript-extractor) as v1.0.4 (latest when checked 2026-11-12). Its GitHub [v0.2.2 ZIP package](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.2/instagram-transcript-extractor-v0.2.2.zip) is a separate distribution for platforms that support Skill package uploads; it is not an OpenClaw installation route. ClawHub and GitHub use independent version numbers. Before installing from ClawHub, confirm the publisher is `apismith-labs` and review the [Skill's security audit](https://clawhub.ai/apismith-labs/skills/instagram-transcript-extractor/security-audit). The Actor used by this Skill is the [Instagram Transcripts Scraper](https://apify.com/apple_yang/instagram-transcripts-scraper).

For Transcript Extractor, choose one source: Control UI, OpenClaw CLI from ClawHub, Vercel Skills CLI from GitHub, or the local repository directory. Do not install multiple copies of the same Skill, which can create duplicate entries or version confusion.

In the project Gateway, GitHub-source and local-directory installation have been reported to make this Skill visible to the Agent, but do not confirm a completed transcript task through Apify. Control UI and ClawHub CLI installation have not been confirmed there.

### Install from the Control UI

In OpenClaw Control UI, open **Plugins → Skills** and select the Agent that will use the Skill. Search for `instagram-transcript-extractor`, confirm the publisher, review the security audit linked above, and add it using the UI's ClawHub flow. Then check the Gateway and select `$instagram-transcript-extractor` in a new session.

### Install with the OpenClaw CLI from ClawHub

Run this command in the environment connected to your OpenClaw Gateway:

```sh
openclaw skills install @apismith-labs/instagram-transcript-extractor
```

This installs into the active workspace's `skills/` directory. Add `--global` to install into the shared managed Skills directory:

```sh
openclaw skills install @apismith-labs/instagram-transcript-extractor --global
```

Then run `openclaw skills check` (or `openclaw skills check --agent YOUR_AGENT_ID`) and select `$instagram-transcript-extractor` in a new session. See the [OpenClaw Skills CLI documentation](https://docs.openclaw.ai/cli/skills) for install and check options.

### Install from GitHub source with Vercel Skills CLI

The [Vercel Skills CLI](https://skills.sh/docs/cli) can install the Skill from this repository. It requires [Node.js 22.20.0 or later](https://github.com/vercel-labs/skills#install-a-skill). Run from the active OpenClaw workspace on the same machine or container as the Gateway:

```sh
npx skills add apismith-labs/instagram-ai-agent-skills \
  --skill instagram-transcript-extractor \
  -a openclaw
```

When prompted, choose **Project** scope. Then run `openclaw skills check` and select the Skill in a new session. This is a GitHub source installation route; do not confuse it with the v0.2.2 ZIP package or the ClawHub listing.

### Install from a local repository directory

If you have cloned this repository, run the following from its root to install the Skill into the shared managed directory:

```sh
openclaw skills install ./skills/instagram-transcript-extractor --global
```

For an active-workspace installation, omit `--global`. After installation, run `openclaw skills check` and select the Skill in a new session.

### Request a transcript

Connect the Apify plugin, start a new session, and select `$instagram-transcript-extractor`. Replace the placeholder with a public Instagram Reel or video URL:

```text
$instagram-transcript-extractor Get the transcript actually returned for this public Instagram Reel. Include timestamps only if they are returned; do not invent transcript text or timestamps.
[PUBLIC_INSTAGRAM_URL]
```

The Skill analyzes returned speech text; it does not establish what appears in the video. A transcript match means the returned transcript was matched to the submitted URL, not that every result page or post was retrieved. If the host cannot provide reliable results or the transcript is incomplete, report that limitation accurately.

## Further help

For OpenClaw command options, see the [Skills CLI documentation](https://docs.openclaw.ai/cli/skills). For installation or visibility problems with this project, [open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues).
