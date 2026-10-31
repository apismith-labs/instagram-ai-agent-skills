# Use Instagram Transcript Extractor with Claude

This guide covers three separate entry points: Claude Web, regular chat in Claude Desktop, and Claude Code. The Apify Connector and uploaded Skill are set up once in Claude Web. The project owner reports that signing into the same account in Claude Desktop made both available there without another installation or OAuth authorization.

You need an Apify account. Actor runs use that account's plan allowance; check the [Apify Console](https://console.apify.com/) for current Runs and billing details.

## Set up once in Claude Web

1. In Claude Web, open **Customize → Connectors**, find the official **Apify Web Connector**, and add it.
2. Complete the Apify OAuth flow and confirm that the Connector is connected.
3. Open **Customize → Skills → Add → Upload skill** and upload the named `instagram-transcript-extractor.zip` Release asset. Use the current link in the [project README](../../README.md), not GitHub's automatically generated **Source code (zip)**. Keep the ZIP intact. Review the preview and enable the Skill.

Connecting Apify provides access to external Apify tools; uploading the Skill provides the transcript workflow. They are separate setup steps, and both are needed to use the transcript workflow with Apify.

## Use it in Claude Web

In a Claude Web conversation, open the **+** menu and select `instagram-transcript-extractor`. In the **Connectors** menu, confirm the Apify Web Connector is enabled. Then send a request such as:

```text
Use instagram-transcript-extractor to return the original-language transcript for this public Instagram Reel. Include timestamps only if the tool returns them.
PUBLIC_INSTAGRAM_URL
```

Replace `PUBLIC_INSTAGRAM_URL` with an accessible public Instagram link. You can use the copyable transcript, batch, translation, summary, subtitle, and text-analysis requests below in either chat interface.

## Use it in Claude Desktop regular chat

1. Sign into Claude Desktop with the same Claude account used for the Web setup. In the reported account, the Apify Connector and Skill appeared in Desktop without reinstalling the Skill or repeating OAuth.
2. Open a regular chat, not Claude Code. Select `instagram-transcript-extractor` from the chat **+** menu and confirm the Apify Connector is enabled in the **Connectors** menu.
3. Send the same request format shown above, replacing the URL with a public Instagram link.

In the reported Desktop account, the Connector page showed Apify as type **Web**, marked **Custom**, with a normal status. This Web Connector worked in regular Desktop chat; a separate Desktop-only Apify Connector was not needed.

## Claude Code

Claude Code is a separate coding environment, not regular chat in Claude Desktop. The steps below follow Anthropic's documented Skill and connector setup; this project has not tested installation or a transcript call in Claude Code.

1. Install and sign in to Claude Code by following Anthropic's [Claude Code setup guide](https://docs.anthropic.com/en/docs/claude-code/getting-started). Use the same `claude.ai` account where you connected Apify and enabled the Skill in Claude Web.
2. Anthropic documents that Skills enabled in a `claude.ai` account sync into Claude Code when you sign in with that account. In a Claude Code session, run `/skills` and confirm that the Skill is listed under **claude.ai sync**. Type `/` and invoke the command shown for it; if its short name conflicts with another command, the synced command uses the `anthropic-skills:` prefix. Anthropic also documents the personal skills directory `~/.claude/skills/`; if you need a local installation instead, extract the named ZIP linked in the [project README](../../README.md) and place its top-level `instagram-transcript-extractor/` folder there. If that destination already exists, stop and inspect it; do not overwrite it.
3. At the Claude Code prompt, invoke the Skill using its displayed slash command. For a local personal installation, the command is `/instagram-transcript-extractor`; for example:

```text
/instagram-transcript-extractor Get the original-language transcript for this public Instagram Reel. Include timestamps only if returned.
PUBLIC_INSTAGRAM_URL
```

4. Anthropic documents that connectors added in Claude Web are available in Claude Code when you are signed in with a `claude.ai` account. Run `/mcp` to check the connector list. This project's Apify connection and Skill invocation have not been tested in Claude Code; do not treat the appearance of the Skill or Connector as proof that a transcript task will work.

See Anthropic's [Skills guide](https://code.claude.com/docs/en/skills) and [MCP guide](https://code.claude.com/docs/en/mcp) for current details.

## Copyable requests for Claude Web and Desktop chat

Replace every placeholder shown, including each `PUBLIC_INSTAGRAM_URL` and `[TARGET_LANGUAGE]`, with an accessible public Instagram link or your target language. In Claude Web or Desktop chat, select the Skill with the **+** menu and enable Apify in the **Connectors** menu before sending a request. These are request examples, not guarantees that every link will succeed.

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

## What has been reported

The project owner reports that a one-Reel request in Claude Desktop regular chat completed successfully: the Actor status was `SUCCEEDED`, one result was returned, the dataset was fully read, and the result contained an original-language transcript without per-sentence timestamps. This is one reported test; it does not guarantee results for other links. No transcript call in Claude Code has been tested.

Earlier Claude Web reports are separate: a single-link request returned a transcript and timestamps, and a separate two-link request returned two URL-matched transcripts but was marked provisional because dataset pagination metadata was inconsistent. These reports do not establish general batch completeness or verify that older task results used the current Release ZIP.
