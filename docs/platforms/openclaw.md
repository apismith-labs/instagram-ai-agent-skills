# Use Instagram Transcript Extractor in OpenClaw

This guide covers the existing cross-platform Instagram Transcript Extractor Skill with the Apify OpenClaw plugin. It does not provide a separate OpenClaw-specific Skill. The project owner reports it is published on [ClawHub](https://clawhub.ai/apismith-labs/skills/instagram-transcript-extractor) as `@apismith-labs/instagram-transcript-extractor`, version 1.0.0. Before installing, review the [security audit page](https://clawhub.ai/apismith-labs/skills/instagram-transcript-extractor/security-audit) for its listed findings and separate static-analysis result.

## Find and add it in the Control UI (recommended)

In OpenClaw Control UI, open **Plugins → Skills**. Select the target Agent first; the Skills manager and its inline ClawHub search are scoped to that Agent. Search for `instagram-transcript-extractor`. The official [Skills guide](https://docs.openclaw.ai/skills) describes adding a Skill from ClawHub, and the [Control UI settings guide](https://docs.openclaw.ai/web/control-ui/settings) documents the per-Agent Skills manager and search.

Before adding it, confirm the publisher is `apismith-labs`, review the currently listed version, and inspect the audit page's listed findings and separate static-analysis result. Then use the ClawHub add flow presented by the UI; this guide does not assume a particular detail-page button. After adding it, run `openclaw skills check --agent main` in the Gateway's CLI, then start a new session and type `$instagram-transcript-extractor` to select the Skill. Picker availability does not establish a successful Skill invocation.

The project owner reports being able to search for and see this Skill in the OpenClaw Skills page after publication; a screenshot showed `openclaw-managed`, `eligible`, and `Enabled`, with a path under `~/.openclaw/skills/`. That path and display do not establish whether the Skill was installed through the UI, ClawHub CLI, or local-directory CLI. Control UI search/add has not been explicitly tested on the owner's Gateway.

## Install from ClawHub CLI (alternative)

Run these commands in the same environment that runs your OpenClaw Gateway. If the `openclaw` CLI is not on your PATH, replace `openclaw` with the full path to your CLI executable.

For a shared Gateway or use across agents, install to OpenClaw's shared managed Skill directory:

```sh
openclaw skills install @apismith-labs/instagram-transcript-extractor --global
openclaw skills check --agent main
```

Without `--global`, OpenClaw installs into the current workspace's `skills/` directory instead. The [Skills CLI documentation](https://docs.openclaw.ai/cli/skills) describes these targets and commands. After installation, run `openclaw skills check --agent main` and review the selected Agent's readiness and visibility. The CLI describes these as distinct inventory, readiness, and visibility states; exact status labels can vary. Then start a new session and type `$instagram-transcript-extractor` in the input box to select the Skill. The ClawHub-native install command has not been tested on the project owner's Gateway.

Installing the Skill does not set up Apify. The Apify plugin and its API key are separate prerequisites; see [Set up the Apify plugin](#set-up-the-apify-plugin). Do not paste an API key into chat or documentation.

## Install from a GitHub local directory (backup; owner-reported tested route)

The project owner reports cloning the GitHub repository and installing its local Skill directory with `openclaw skills install <local-path> --global`. The owner reports that `openclaw skills check --agent main` listed it as `eligible`, `visible`, and `available as command`, and that a new session's `$` picker could select it. This is evidence for the local-directory `--global` route only. The default workspace install (without `--global`) has not been tested. Do not install using both this route and ClawHub for the same setup.

OpenClaw loads Skills from multiple configured sources, including the active workspace and the shared managed directory. The [Skills guide](https://docs.openclaw.ai/skills) describes those sources and how ClawHub installation works.

## Set up the Apify plugin

The project owner reports manually installing the Apify plugin from the OpenClaw web interface's **Plugins** page. The plugin's [README](https://github.com/apify/apify-openclaw-plugin) documents this CLI alternative:

```sh
openclaw plugins install @apify/apify-openclaw-plugin
```

The CLI command is documented by the plugin, but was not the method used in the owner's reported installation. Follow the plugin README for any install-specific steps and restart the Gateway if instructed.

The plugin needs an Apify API key configured through the OpenClaw CLI/plugin configuration. Never paste the key into a chat, Skill file, issue, or other text field. Do not include it in logs or commands that may be saved in shell history. The plugin README documents `openclaw apify setup` as an interactive configuration alternative; this method was not reported as tested by the project owner. The README also says `tools.alsoAllow` can include `apify` to make the tool available to agents. This configuration step has not been tested in this project: inspect the current configuration first, then merge `apify` into the existing `alsoAllow` values if needed. Do not replace an existing list blindly. The project owner reports configuring the key through the CLI and seeing `openclaw apify status` report a successful connection; this is an account-specific report, not a universal guarantee. This guide does not include key setup commands or inspect any credentials.

## Discover-only check

This request asks only for Actor discovery/schema information; it must not start an Actor:

```text
Use Instagram Transcript Extractor in OpenClaw. Use the Apify plugin's apify tool with the discover action to look up the Actor apple_yang~instagram-transcripts-scraper and retrieve its current input schema. Do not use start or collect and do not run an Actor.
```

The project owner reports that the Gateway was running, its connectivity check was OK, `/health` returned a live status, the Apify plugin connection status succeeded, and an Actor `discover` query succeeded. The available report does not independently establish that this `discover` query was executed through the plugin's `apify` tool, so treat it as a reported discovery result, not an independently verified plugin tool call.

## Request a transcript

After the Skill and Apify plugin are available, start a new session, type `$` and select `instagram-transcript-extractor`, then replace the placeholder with a public Instagram link:

```text
$instagram-transcript-extractor Get the original-language transcript for this public Instagram Reel. Include only timestamps actually returned; do not invent them.
PUBLIC_INSTAGRAM_URL
```

This request asks OpenClaw to start an Apify Actor run and collect its result. It may use the connected Apify account. The plugin uses its `apify` tool and `discover` → `start` → `collect` flow; it is not an Apify MCP `call-actor`/`get-dataset-items` flow. Before any start, the Skill must obtain the current Actor schema and form input from it. If the plugin tool, authentication, Actor, or schema is unavailable or unclear, stop and report the issue; do not switch to shell, direct REST calls, another Actor, or another URL. Do not automatically retry.

The plugin's `collect` pagination/completeness evidence has not been verified for this Skill. If complete dataset reading cannot be established from the returned evidence, matched results must remain provisional/pending. A transcript without timestamps can still be a transcript result; never invent timestamps. Batch completeness and subtitle file creation have not been tested in OpenClaw.

## Evidence boundary

Gateway health, plugin connection status, Actor discovery, actual transcript extraction, and batch completeness are separate stages. Only the first status checks and a reported `discover` query are currently documented for OpenClaw; the `apify` tool-call trace for that query is not independently confirmed. `start`, `collect`, a real transcript, batch completeness, and subtitle export remain untested.
