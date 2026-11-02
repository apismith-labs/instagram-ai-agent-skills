# Use Instagram Transcript Extractor in OpenClaw

This guide covers the existing cross-platform Instagram Transcript Extractor Skill with the Apify OpenClaw plugin. It does not provide a separate OpenClaw-specific Skill. OpenClaw runs Skills from its workspace `skills/` directory; the official [Skills guide](https://docs.openclaw.ai/skills) also documents installation of a local Skill directory.

## Set up the Apify plugin

The project owner reports manually installing the Apify plugin from the OpenClaw web interface's **Plugins** page. The plugin's [README](https://github.com/apify/apify-openclaw-plugin) documents this CLI alternative:

```sh
openclaw plugins install @apify/apify-openclaw-plugin
```

The CLI command is documented by the plugin, but was not the method used in the owner's reported installation. Follow the plugin README for any install-specific steps and restart the Gateway if instructed.

The plugin needs an Apify API key configured through the OpenClaw CLI/plugin configuration. Never paste the key into a chat, Skill file, issue, or other text field. Do not include it in logs or commands that may be saved in shell history. The plugin README documents `openclaw apify setup` as an interactive configuration alternative; this method was not reported as tested by the project owner. The README also says `tools.alsoAllow` can include `apify` to make the tool available to agents. This configuration step has not been tested in this project: inspect the current configuration first, then merge `apify` into the existing `alsoAllow` values if needed. Do not replace an existing list blindly. The project owner reports configuring the key through the CLI and seeing `openclaw apify status` report a successful connection; this is an account-specific report, not a universal guarantee. This guide does not include key setup commands or inspect any credentials.

## Install and discover the Skill

Place the complete `instagram-transcript-extractor/` Skill directory in the active OpenClaw workspace's `skills/` directory. OpenClaw's official [Skills documentation](https://docs.openclaw.ai/skills) documents `openclaw skills install <local-skill-directory>` for local Skill directories; the exact install command has not been tested in this project. Do not replace an existing same-named Skill without first checking it.

Use the OpenClaw UI or the documented CLI to confirm the Skill is loaded. OpenClaw's [Skills guide](https://docs.openclaw.ai/tools/creating-skills) documents `openclaw skills list` and explicit `/skill instagram-transcript-extractor` invocation. If the Skill does not appear, check the active workspace and confirm its `skills/instagram-transcript-extractor/SKILL.md` exists; start a fresh session if the Skill was added while a session was already open.

## Discover-only check

This request asks only for Actor discovery/schema information; it must not start an Actor:

```text
Use Instagram Transcript Extractor in OpenClaw. Use the Apify plugin's apify tool with the discover action to look up the Actor apple_yang~instagram-transcripts-scraper and retrieve its current input schema. Do not use start or collect and do not run an Actor.
```

The project owner reports that the Gateway was running, its connectivity check was OK, `/health` returned a live status, the Apify plugin connection status succeeded, and an Actor `discover` query succeeded. The available report does not independently establish that this `discover` query was executed through the plugin's `apify` tool, so treat it as a reported discovery result, not an independently verified plugin tool call.

## Request a transcript

After the Skill and Apify plugin are available, explicitly invoke the Skill and replace the placeholder with a public Instagram link:

```text
/skill instagram-transcript-extractor Get the original-language transcript for this public Instagram Reel. Include only timestamps actually returned; do not invent them.
PUBLIC_INSTAGRAM_URL
```

This request asks OpenClaw to start an Apify Actor run and collect its result. It may use the connected Apify account. The plugin uses its `apify` tool and `discover` → `start` → `collect` flow; it is not an Apify MCP `call-actor`/`get-dataset-items` flow. Before any start, the Skill must obtain the current Actor schema and form input from it. If the plugin tool, authentication, Actor, or schema is unavailable or unclear, stop and report the issue; do not switch to shell, direct REST calls, another Actor, or another URL. Do not automatically retry.

The plugin's `collect` pagination/completeness evidence has not been verified for this Skill. If complete dataset reading cannot be established from the returned evidence, matched results must remain provisional/pending. A transcript without timestamps can still be a transcript result; never invent timestamps. Batch completeness and subtitle file creation have not been tested in OpenClaw.

## Evidence boundary

Gateway health, plugin connection status, Actor discovery, actual transcript extraction, and batch completeness are separate stages. Only the first status checks and a reported `discover` query are currently documented for OpenClaw; the `apify` tool-call trace for that query is not independently confirmed. `start`, `collect`, a real transcript, batch completeness, and subtitle export remain untested.
