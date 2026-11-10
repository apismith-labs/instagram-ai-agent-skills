---
name: instagram-media-links-and-post-insights
description: Return video and audio links or organize verified post fields from public Instagram video posts and Reels supplied by the user.
---

# Instagram Media Links & Post Insights

Get media links or a clear summary of fields actually returned for public Instagram video posts and Reels you provide. This Skill handles two tasks: **Media links** returns the `videoUrl` and `audioUrl` links the Actor provides; **Post insights** organizes or compares returned likes, comments, author, and publish-time fields. It does not download media files.

This Skill uses the [Instagram Video Scraper API Actor on Apify](https://apify.com/apple_yang/instagram-video-scraper-api).

## Example requests

**Media links**

```text
Return the video and audio links actually provided for this public Instagram Reel. Keep the original URL with the result, and say if either field is missing.
[INSTAGRAM_URL]
```

**Post insights**

```text
Organize the author, publish time, likes, and comments actually returned for these public Instagram video posts or Reels. Compare only the returned raw counts. Do not calculate rates or infer trends, audience response, performance changes, or causes.
[INSTAGRAM_URLS]
```

If the user requests both, return both sets of fields from one Actor result where possible. For an unclear request, ask whether they want media links, post fields, or both. Read [the workflow reference](references/workflow.md) before processing a request.

## First Apify use

Installing this Skill does not connect or authorize Apify. On the first real task, check only what the current session actually exposes: available Apify tools, their live schemas, and any explicit host-provided authorization or connection status. This is an instruction-level readiness check, not an installation detector: it cannot inspect host settings or local plugin directories, launch OAuth, or determine why a tool is absent.

If no usable Apify tool is available, the host explicitly reports missing authorization, or the required run conditions cannot be confirmed, stop before any Actor call. Say that this session has no confirmed usable Apify tool, state that no Actor was started and no results were received, and explain the specific unconfirmed condition. A missing tool alone does not establish whether Apify is uninstalled, disabled, unauthorized, restricted by the workspace, or simply not exposed by the host. Do not install a plugin, change host configuration, start OAuth, authorize for the user, ask for an API Key in chat, or switch to another Actor, tool, or authentication method to bypass the limitation. When Apify is confirmed ready, do not repeat first-use setup guidance.

### ChatGPT first-use guidance

Only when the host is explicitly identified as ChatGPT, and the current task must stop because no usable Apify tool is available, authorization is explicitly missing, or readiness cannot be confirmed, present this guidance verbatim. Do not show it when Apify is confirmed ready:

> There's no confirmed usable Apify tool available to me in this ChatGPT session, so I can't start the task. This doesn't necessarily mean the plugin is uninstalled: the connection may be disabled, your Apify account may not be authorized, or this workspace may not expose those tools. I have not started any Actor, and no results were received.
>
> To connect Apify in ChatGPT:
>
> 1. Open **Plugins → + → Add custom MCP server**.
> 2. Set **Name** to `Apify MCP` and **Server URL** to `https://mcp.apify.com`.
> 3. Choose **OAuth** and complete the Apify authorization in the window ChatGPT opens.
> 4. Review and acknowledge the risk notice, then choose **Create as a plugin**.
> 5. **Install the generated Apify MCP plugin/App.**
>
> Then start a **new chat**, type **@** in the message box, select `Apify MCP`, and name this Skill in your request.
>
> Connecting Apify and installing a Skill are two separate steps. One `Apify MCP` connection can be shared by several Skills, so you don't need a separate connection for each one. Never send an Apify API key or any other credential in chat.
>
> If you don't have an Apify account, [create one in the Apify Console](https://console.apify.com/sign-up). If the custom MCP option is missing, your plan, workspace policy, admin permission, or product availability may be limiting it — check your account access and the [OpenAI custom MCP guide](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt).
>
> After setup, open a new conversation and retry your request. For the full steps, see the [project ChatGPT guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/chatgpt.md).

### Other host setup guidance

Show only the instructions for a clearly identified host, and use that host's existing guide:

- **Codex desktop app or CLI:** follow the matching setup path in the [Codex guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/codex.md#choose-your-codex-environment-and-connect-apify). Do not use ChatGPT or OpenClaw instructions.
- **Claude Web, Claude Desktop regular chat, or Claude Code:** these are distinct products. Use the matching section in the [Claude guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/claude-web.md); the guide distinguishes Web Connector setup, Desktop account sync, and Code environment setup. If the current Claude product is unclear, ask which one the user uses before giving steps.
- **Manus:** follow the [Manus Apify Connector guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/manus.md#1-enable-apify-and-authorize-access). This is not ChatGPT custom MCP setup.
- **OpenClaw:** use only the OpenClaw-specific section below, and only when OpenClaw is explicitly identified.
- **Unknown host:** do not guess or show platform commands. Say Apify must be connected and authorized through that host's supported interface, ask which host the user uses, and stop.

Never infer that an absent tool means a plugin is uninstalled. The Skill cannot inspect local plugin directories, install software, edit host settings, start or complete OAuth, or authorize on the user's behalf. After the user completes setup, have them open a new session or refresh the host's tools, then retry. Do not use shell commands, direct REST/API requests, tokens, cookies, session IDs, or a different Actor to bypass missing tools or authorization.

For OpenClaw, show this exact guidance only when the first-use condition above applies:

> There's no confirmed usable Apify tool available to me in this OpenClaw session, so I can't start the analysis. This doesn't necessarily mean the plugin is uninstalled: it may be disabled, your Apify account may not be configured, or this Agent may not have permission. I have not started any Actor.
>
> If you don't have an Apify account, [create one in the Apify Console](https://console.apify.com/sign-up).
>
> Choose one way to install the Apify OpenClaw plugin:
> - Run `openclaw plugins install @apify/apify-openclaw-plugin`.
> - Or, if your OpenClaw Control UI shows the plugin catalog, open **Plugins**, search for **Apify**, and install the Apify listing from ClawHub. If it is not available there, use the CLI command above.
>
> Restart the OpenClaw Gateway after installation.
>
> First, prepare an Apify API Key. The [official plugin README](https://github.com/apify/apify-openclaw-plugin) explains how to create and configure it. Then run `openclaw apify setup` and follow the wizard to finish configuration. Never send your API Key in chat.
>
> After setup, open a new conversation and try your request again.
>
> For detailed steps, see the [OpenClaw setup guide](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/platforms/openclaw.md#set-up-the-apify-plugin).

Do not start an Actor until a usable Apify tool and required schema are visible and explicit host status does not report missing authorization. If readiness remains unclear, stop and direct the user to the corresponding setup guidance above. The Skill cannot install plugins or change host settings.

## Actor preflight and input

Before telling the user that processing will begin, complete the internal preflight in [the workflow reference](references/workflow.md). Do not first say “I’ll process these” or imply a run has started. Use only `apple_yang/instagram-video-scraper-api`. A visible Apify connection or OAuth success does not by itself confirm that this Actor's tool, schema, or result-reading tools are exposed.

The preflight must establish a supported tool path, the current input/output contract, a way to submit the user URLs in the required `videoUrls` array, and a way to obtain actual result rows. For a dedicated tool, verify that its live description/schema identifies the exact target owner and Actor; similar names or an unclear identity are insufficient. If any required capability is absent or unclear, stop before an Actor call. Tell the user which tool or capability is missing, and state that no Actor was started and no results were received. Do not infer that a public Actor is callable, guess tool names/arguments/Actor identifier format/result envelopes, use another Actor, or bypass the host with HTTP, shell, tokens, or `sessionid`.

Preserve each input URL exactly as supplied and its original order. Use one call for a single request or one batch call when supported. For combined Media links and Post insights requests, use one input set and one Actor result where possible; do not repeat calls without a task need. Never use API tokens, `sessionid`, shell commands, or direct HTTP requests to bypass host tools. Do not call another Actor.

## Media type and links

- Do not infer media type from URL path. `/p/` identifies a post path, not a video. Use only the user's stated intent and evidence in the Actor result.
- If media type is unknown, or no video/audio direct link is returned, say that support for this content cannot be confirmed. Do not guess or promise a link.
- Do not claim photo or carousel posts are supported or unsupported; they remain unverified and outside the first-release commitment.
- A returned `videoUrl` or `audioUrl` means the Actor supplied a direct link. It does not mean the Skill downloaded a file or that the link will remain valid.

## Post insights boundaries

Organize or compare only raw fields actually returned and otherwise verified, such as `likeCount`, `commentCount`, author fields, `createTime`, and `timestamp`. Treat each run as a snapshot of that collection. Do not promise or infer `views`, play count, impressions, reach, follower counts, shares, saves, or other unverified fields. Do not calculate engagement rates or other derived metrics needing unverified inputs. Do not infer trends, audience response, performance changes, or causation, and do not present a simple count comparison as a validated business conclusion. Missing fields are not zero.

## Match and report every input

Follow [the workflow reference](references/workflow.md). Match a result to an input using a verifiable match on the returned `url`. Do not rely on `code`, `pk`, or `id` unless their matching behavior has been independently verified for the current contract. Do not match by output order. Preserve exact input strings; do not merge URLs using unverified normalization. Deduplicate only exact identical strings, and retain their input positions.

Report each input separately and distinguish:

1. A non-empty `errMsg`: quote/report the actual returned message without adding a cause.
2. Empty or missing `errMsg`: state that the field is empty or missing; do not infer success from it.
3. No reliably matching result row: say “未收到可匹配的结果” / “No matching result was received”; do not say the Actor failed or the post does not exist.
4. A matched row with a missing, empty, or unreturned field: say that field is “未返回/不可用” / “not returned or unavailable”; do not interpret missing links as proof media does not exist or missing counts as zero.
5. Missing, conflicting, or multiple candidate URLs: say “对应关系待确认” / “input-to-result mapping needs confirmation”. Never guess by position.
6. Partial batch results: show each confirmed, errored, unmatched, and unresolved item; do not say the batch fully succeeded.

Do not assume top-level error formats, batch order guarantees, or that `errMsg` is always present. Report only the tool result actually visible to the host. If the result cannot establish media type, state that support cannot be confirmed.

## Scope and privacy

Handle only public video post and Reel URLs supplied by the user. Private accounts, Stories, and authentication-required content are outside the supported scope. Do not discover account posts, monitor on a schedule, extract transcripts, interpret visuals, or download/save media files. Do not ask for or expose passwords, API keys, cookies, or session IDs. Do not include fixed prices or estimates; if asked about usage, direct the user to their Apify Console. The user is responsible for following applicable service terms, copyright, and privacy requirements; do not give legal conclusions.
