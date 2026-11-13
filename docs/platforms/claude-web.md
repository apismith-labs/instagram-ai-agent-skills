# Use Instagram Skills with Claude

This guide covers Claude Web, regular chat in Claude Desktop, and Claude Code. Set up the Apify Connector and upload the Skill in Claude Web. Availability and setup can differ between these Claude products.

You need an Apify account. Actor runs use that account's plan allowance; check the [Apify Console](https://console.apify.com/) for current Runs and billing details.

## Connect Apify and install a Skill

Apify's current Claude integration offers an Apify Plugin in Claude Web and a hosted Apify MCP connector that also works in Claude Desktop. UI labels are rolling from **Customize** to **Plugins**; if the documented tab is not visible, consult the linked official guide instead of guessing another path.

1. Open the left sidebar's **Plugins** page if the unified interface has reached your account, filter to **Connectors** and open **Discover**; in the earlier interface use **Customize → Connectors → Discover**. Find the official Apify entry labeled **Plugin** and select **Add**. Do not select the separate Desktop extension for web chat.
2. Open the Apify Plugin page's **Connectors** tab and choose **Connect** for `apify`; select **Continue → Add**.
3. In the browser, sign into the correct Apify account, review the permissions, and select **Allow access**. Check that `apify` shows connected.
4. Upload the Skill separately: open **Plugins → Skills** in the unified interface, or **Customize → Skills** in the earlier one; select **+ → Create skill → Upload a skill**, choose the named ZIP, finish the scan, and enable it. Keep the ZIP intact; do not upload GitHub's auto-generated **Source code (zip)**.
5. In a new Claude Web chat, enable the Apify connector using the **+** menu → **Connectors**. Type `/` to choose the Skill if it appears in the chooser, or name it explicitly in your request. Confirm the Skill is enabled and Apify is available before starting a task.

The Claude account's settings also appear in regular chat on Claude Desktop when signed into the same account. Skill upload and Apify authorization are separate steps. Plans and organization policies can hide skills, connectors, or upload controls; check the [Anthropic Skills guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude) and [custom remote MCP guide](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp). The Apify setup steps are in its [Claude.ai guide](https://docs.apify.com/integrations/claude-ai).

## Use Instagram Transcript Extractor in Claude Web

In a Claude Web conversation, type `/` to select `instagram-transcript-extractor` if the current Skills menu offers it, or name it in your request. Confirm the Apify connector is enabled from **+ → Connectors**, then send a request such as:

```text
Use instagram-transcript-extractor to return the original-language transcript for this public Instagram Reel. Include timestamps only if the tool returns them.
PUBLIC_INSTAGRAM_URL
```

Replace `PUBLIC_INSTAGRAM_URL` with an accessible public Instagram link. You can use the copyable transcript, batch, translation, summary, subtitle, and text-analysis requests below in either chat interface.

## Use Creator Video Insights in Claude Web

In a Claude Web conversation, type `/` to select `instagram-creator-reels-insights` if available, and enable Apify from **+ → Connectors**. Ask for a multi-creator review such as:

```text
Use instagram-creator-reels-insights to review these public creator accounts for the most recent 7 days: CREATOR_1, CREATOR_2, and CREATOR_3. Process up to VIDEO_LIMIT eligible videos per creator. Give me a separate summary for each creator, then compare patterns only when supported by returned transcripts. Include source links and disclose when results are partial or unknown; do not imply that unreturned posts were reviewed.
```

`VIDEO_LIMIT` in the request above is the maximum number of discovered videos per creator sent for transcript analysis. It does not limit how many posts are discovered and is not a fee cap.

The ZIP upload steps are documented, but this project has not confirmed end-to-end Creator report execution with Claude and Apify. Tool availability and returned results depend on your account and Connector.

## Use Instagram Transcript Extractor in Claude Desktop regular chat

1. Sign into Claude Desktop with the same Claude account used for Web setup; remote connector and Skills account sync are separate from Claude Code CLI.
2. Open the **Chat** tab (regular chat), not the Code tab. Type `/` to select the Skill if offered, otherwise name it explicitly, then use **+ → Connectors** to enable Apify.
3. Send the same request format shown above, replacing the URL with a public Instagram link.

Claude Desktop regular chat is separate from Claude Code. If the Skill or Connector is not available in Desktop, complete setup in Claude Web and check the account signed in to Desktop.

## Use Creator Video Insights in Claude Desktop regular chat

Enable Instagram Creator Video Insights in Claude Web, then sign in to Claude Desktop with the same Claude account. In a regular chat, type `/` to select `instagram-creator-reels-insights` if available, and enable Apify from **+ → Connectors**. The project has not confirmed the full Creator report workflow in Claude Desktop.

## Claude Code

The Claude Code instructions below apply to Instagram Transcript Extractor. Claude Code is a separate coding environment, not regular chat in Claude Desktop. The steps follow Anthropic's documented Skill and connector setup; this project has not tested a Claude Code installation or transcript task.

1. Install and sign in to Claude Code by following Anthropic's [Claude Code setup guide](https://docs.anthropic.com/en/docs/claude-code/getting-started). Use the same `claude.ai` account where you connected Apify and enabled the Skill in Claude Web.
2. Anthropic documents that Skills enabled in a `claude.ai` account sync into Claude Code when you sign in with that account. In a Claude Code session, run `/skills` and confirm that the Skill is listed under **claude.ai sync**. Type `/` and invoke the command shown for it; if its short name conflicts with another command, the synced command uses the `anthropic-skills:` prefix. Anthropic also documents the personal skills directory `~/.claude/skills/`; as an alternative, download the exact [Instagram Transcript Extractor v0.2.3 ZIP](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.2.3/instagram-transcript-extractor-release-v0.2.3.zip), extract it, and place its top-level `instagram-transcript-extractor/` folder there. If that destination already exists, stop and inspect it; do not overwrite it.
3. At the Claude Code prompt, invoke the Skill using its displayed slash command. For a local personal installation, the command is `/instagram-transcript-extractor`; for example:

```text
/instagram-transcript-extractor Get the original-language transcript for this public Instagram Reel. Include timestamps only if returned.
PUBLIC_INSTAGRAM_URL
```

4. Anthropic documents that connectors added in Claude Web are available in Claude Code when you are signed in with a `claude.ai` account. Run `/mcp` to check the connector list. Skill or Connector visibility alone does not confirm that a transcript task will work.

See Anthropic's [Skills guide](https://code.claude.com/docs/en/skills) and [MCP guide](https://code.claude.com/docs/en/mcp) for current details.

### Creator Video Insights in Claude Code

The account-sync route applies to a Skill enabled in Claude Web when Claude Code is signed into the same `claude.ai` account. For a local installation instead, use the top-level `instagram-creator-reels-insights/` directory from the [Creator Video Insights v1.0.5 ZIP candidate](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v1.0.5/instagram-creator-video-insights-v1.0.5.zip) after publication in the personal skills directory documented above. After installation, use `/skills` to check visibility and invoke the displayed slash command. The project has not confirmed this Creator installation path or its full task workflow in Claude Code.

## Copyable requests for Claude Web and Desktop chat

Replace every placeholder shown, including each `PUBLIC_INSTAGRAM_URL` and `[TARGET_LANGUAGE]`, with an accessible public Instagram link or your target language. In Claude Web or Desktop Chat, type `/` and select the Skill if the current menu offers it (otherwise name it explicitly), then use **+ → Connectors** to enable Apify before sending a request. These are request examples, not guarantees that every link will succeed.

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
