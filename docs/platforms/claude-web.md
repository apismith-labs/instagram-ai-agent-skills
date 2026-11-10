# Use Instagram Skills with Claude

This guide covers Claude Web, regular chat in Claude Desktop, and Claude Code. Set up the Apify Connector and upload the Skill in Claude Web. Availability and setup can differ between these Claude products.

You need an Apify account. Actor runs use that account's plan allowance; check the [Apify Console](https://console.apify.com/) for current Runs and billing details.

## Set up once in Claude Web

1. In Claude Web, open **Customize → Connectors**, find the official **Apify Web Connector**, and add it.
2. Complete the Apify OAuth flow and confirm that the Connector is connected.
3. Open **Customize → Skills → Add → Upload skill** and upload the ZIP package for the Skill you want to use. For Transcript Extractor, download [`instagram-transcript-extractor-v0.2.1.zip`](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.1/instagram-transcript-extractor-v0.2.1.zip); for Creator Reels Insights, download [`instagram-creator-reels-insights-v1.0.2.zip`](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.2/instagram-creator-reels-insights-v1.0.2.zip). Do not use GitHub's automatically generated **Source code (zip)**. Keep the ZIP intact, review its preview, and enable that Skill.

Connecting Apify provides access to external Apify tools; uploading a Skill provides that Skill's workflow instructions. They are separate setup steps, and both are needed to use a Skill with Apify.

## Use Instagram Transcript Extractor in Claude Web

In a Claude Web conversation, select `instagram-transcript-extractor` from the available Skills controls. Confirm the Apify Web Connector is enabled in **Connectors**, then send a request such as:

```text
Use instagram-transcript-extractor to return the original-language transcript for this public Instagram Reel. Include timestamps only if the tool returns them.
PUBLIC_INSTAGRAM_URL
```

Replace `PUBLIC_INSTAGRAM_URL` with an accessible public Instagram link. You can use the copyable transcript, batch, translation, summary, subtitle, and text-analysis requests below in either chat interface.

## Use Creator Reels Insights in Claude Web

In a Claude Web conversation, select `instagram-creator-reels-insights` from the available Skills controls and enable the Apify Web Connector. Ask for a multi-creator review such as:

```text
Use instagram-creator-reels-insights to review these public creator accounts for the most recent 7 days: CREATOR_1, CREATOR_2, and CREATOR_3. Process up to VIDEO_LIMIT eligible videos per creator. Give me a separate summary for each creator, then compare patterns only when supported by returned transcripts. Include source links and disclose when results are partial or unknown; do not imply that unreturned posts were reviewed.
```

`VIDEO_LIMIT` in the request above is the maximum number of discovered videos per creator sent for transcript analysis. It does not limit how many posts are discovered and is not a fee cap.

The ZIP upload steps are documented, but this project has not confirmed end-to-end Creator report execution with Claude and Apify. Tool availability and returned results depend on your account and Connector.

## Use Instagram Transcript Extractor in Claude Desktop regular chat

1. Sign into Claude Desktop with the same Claude account used for the Web setup. Account sync and Connector availability can depend on your Claude setup.
2. Open a regular chat, not Claude Code. Select `instagram-transcript-extractor` from the available Skills controls and confirm the Apify Connector is enabled in **Connectors**.
3. Send the same request format shown above, replacing the URL with a public Instagram link.

Claude Desktop regular chat is separate from Claude Code. If the Skill or Connector is not available in Desktop, complete setup in Claude Web and check the account signed in to Desktop.

## Use Creator Reels Insights in Claude Desktop regular chat

Enable Instagram Creator Reels Insights in Claude Web, then sign in to Claude Desktop with the same Claude account. In a regular chat, select `instagram-creator-reels-insights` from the available Skills controls and enable the Apify Web Connector. The project has not confirmed the full Creator report workflow in Claude Desktop.

## Claude Code

The Claude Code instructions below apply to Instagram Transcript Extractor. Claude Code is a separate coding environment, not regular chat in Claude Desktop. The steps follow Anthropic's documented Skill and connector setup; this project has not tested a Claude Code installation or transcript task.

1. Install and sign in to Claude Code by following Anthropic's [Claude Code setup guide](https://docs.anthropic.com/en/docs/claude-code/getting-started). Use the same `claude.ai` account where you connected Apify and enabled the Skill in Claude Web.
2. Anthropic documents that Skills enabled in a `claude.ai` account sync into Claude Code when you sign in with that account. In a Claude Code session, run `/skills` and confirm that the Skill is listed under **claude.ai sync**. Type `/` and invoke the command shown for it; if its short name conflicts with another command, the synced command uses the `anthropic-skills:` prefix. Anthropic also documents the personal skills directory `~/.claude/skills/`; as an alternative, download the exact [Instagram Transcript Extractor v0.2.1 ZIP](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.1/instagram-transcript-extractor-v0.2.1.zip), extract it, and place its top-level `instagram-transcript-extractor/` folder there. If that destination already exists, stop and inspect it; do not overwrite it.
3. At the Claude Code prompt, invoke the Skill using its displayed slash command. For a local personal installation, the command is `/instagram-transcript-extractor`; for example:

```text
/instagram-transcript-extractor Get the original-language transcript for this public Instagram Reel. Include timestamps only if returned.
PUBLIC_INSTAGRAM_URL
```

4. Anthropic documents that connectors added in Claude Web are available in Claude Code when you are signed in with a `claude.ai` account. Run `/mcp` to check the connector list. Skill or Connector visibility alone does not confirm that a transcript task will work.

See Anthropic's [Skills guide](https://code.claude.com/docs/en/skills) and [MCP guide](https://code.claude.com/docs/en/mcp) for current details.

### Creator Reels Insights in Claude Code

The account-sync route applies to a Skill enabled in Claude Web when Claude Code is signed into the same `claude.ai` account. For a local installation instead, use the top-level `instagram-creator-reels-insights/` directory from the [Creator Reels Insights v1.0.2 ZIP](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.2/instagram-creator-reels-insights-v1.0.2.zip) in the personal skills directory documented above. After installation, use `/skills` to check visibility and invoke the displayed slash command. The project has not confirmed this Creator installation path or its full task workflow in Claude Code.

## Copyable requests for Claude Web and Desktop chat

Replace every placeholder shown, including each `PUBLIC_INSTAGRAM_URL` and `[TARGET_LANGUAGE]`, with an accessible public Instagram link or your target language. In Claude Web or Desktop chat, select the Skill from the available Skills controls and enable Apify in the **Connectors** menu before sending a request. These are request examples, not guarantees that every link will succeed.

**Single transcript**

```text
Use instagram-transcript-extractor to return the original-language transcript for this public Instagram video. Include only timestamp segments actually returned by the tool; do not invent timestamps.
PUBLIC_INSTAGRAM_URL_1
```

**Batch transcripts**

```text
Use instagram-transcript-extractor on exactly these public Instagram links:
1. PUBLIC_INSTAGRAM_URL_1
2. PUBLIC_INSTAGRAM_URL_2
For each input, return its original URL, processing status, original-language transcript, and timestamp segments if available. Match results by URL, never by result order. Do not add links or retry automatically.
```

**Subtitle file (SRT/VTT)**

```text
Transcribe this video and create an SRT or VTT file only if Claude can create or export files and the tool returned valid timestamps. Otherwise give me copyable subtitle text using only valid timestamps, or explain that timed subtitles are unavailable. Do not invent timestamps.
PUBLIC_INSTAGRAM_URL_1
```

**Translation**

```text
Return the original-language transcript for this video, then provide a separate [TARGET_LANGUAGE] translation. Preserve any timestamp segments actually returned; do not invent them.
PUBLIC_INSTAGRAM_URL_1
```

**Summary**

```text
Transcribe each video and give each link its own short summary. Keep the videos separate and match every result to its original URL.
1. PUBLIC_INSTAGRAM_URL_1
2. PUBLIC_INSTAGRAM_URL_2
```

**Content analysis**

```text
Based only on the transcript of this video, identify its hook, core insight, CTA, and content cues. Include timestamps only where valid timestamp segments were returned. Do not analyze visuals, engagement metrics, or audience response.
PUBLIC_INSTAGRAM_URL_1
```
