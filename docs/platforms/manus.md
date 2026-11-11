# Use Instagram Skills in Manus

This guide explains how to connect Apify and import either Instagram Transcript Extractor or Instagram Creator Video Insights from its own GitHub folder. Connector access and results can vary by account and request; the two Skills have separate paths and task scopes.

## Before you start

You need a Manus account and your own [Apify account](https://console.apify.com/). Apify runs use your Apify account's plan allowance, and Manus tasks that use the Connector may consume Manus credits. See the [Apify Console](https://console.apify.com/) for current Runs and billing details, and check Manus for current credit information. No specific cost is estimated here. See the [Apify Manus integration guide](https://docs.apify.com/integrations/manus) for current platform information.

## 1. Connect Apify and authorize access

Apify MCP is a custom connector in Manus; do not search the prebuilt connector directory for a packaged Apify connector.

1. Open **Settings → Connectors → + Add connectors**.
2. Select **Custom MCP → + Add custom MCP → Direct configuration**.
3. Set **Server name** to `Apify`, **Transport type** to `HTTP`, and **Server URL** to `https://mcp.apify.com`; select **Save**.
4. In the first chat that calls an Apify tool, sign in to Apify in the OAuth prompt and approve access. Do not paste an API token into chat.

For each new chat, use the connector toggle below the input to enable Apify. Confirm the connector is enabled and Apify tools are available before asking for a task. Apify's guide says MCP access is available on all Manus plans, including Free, but individual account or workspace controls may still affect access. See the [official Apify Manus guide](https://docs.apify.com/integrations/manus).

## 2. Import and enable the Skill

In Manus, open **Skills** and choose **+ Add → Import from GitHub**. Paste this Skill folder URL, which imports the current contents of the repository's `main` branch from the directory containing `SKILL.md`:

```text
https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-transcript-extractor
```

Select **Import**. Confirm that `instagram-transcript-extractor` appears in your personal Skill list and is enabled. The [Manus Skills guide](https://help.manus.im/en/articles/14753565-how-to-share-and-use-skills-in-manus) covers importing and using Skills. GitHub import does not mean that this Skill is listed in Manus's public Explore skills marketplace.

## 3. Request a transcript

In a new Manus conversation, type `/` and select `instagram-transcript-extractor`. Also enable Apify using the connector toggle below the message input and confirm Apify tools are available. Then request one public Reel, replacing the example with a real link:

```text
Use instagram-transcript-extractor to get the transcript of this public Instagram Reel:
https://www.instagram.com/reels/REPLACE_WITH_A_REAL_LINK/
```

The result depends on the requested public link and the connected tools. A restricted or inaccessible post, or a video without detectable speech, may not yield a transcript. Review the status shown for each requested link; do not assume that success for one link establishes batch behavior or results for other accounts.

## Use Creator Video Insights

Creator Video Insights is a separate Skill. After enabling the Apify Connector as described above, import this Skill from its own GitHub folder:

```text
https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-creator-reels-insights
```

Use the same **Skills → + Add → Import from GitHub** flow described in step 2, but choose the Creator folder URL above, not the Transcript Extractor folder. Confirm that `instagram-creator-reels-insights` appears in your personal Skill list and is enabled. In a conversation, type `/` and select that Skill. The Creator report workflow has not been confirmed in Manus.

For a single-account weekly review, replace the placeholder with a public creator username:

```text
Use instagram-creator-reels-insights to review [CREATOR_USERNAME] for the most recent 7 days. Analyze only posts and transcripts actually returned, include source links, and separate observations from interpretation. If results are partial or unknown, say they may be incomplete; do not imply that unreturned posts were reviewed.
```

## Official references

- [Apify integration with Manus](https://docs.apify.com/integrations/manus)
- [Manus: share, import, and use Skills](https://help.manus.im/en/articles/14753565-how-to-share-and-use-skills-in-manus)

## Copyable requests

Replace every placeholder shown, including each `PUBLIC_INSTAGRAM_URL` and `[TARGET_LANGUAGE]`, with an accessible public Instagram link or your target language. In chat, type `/` and select `instagram-transcript-extractor`, and check that the Apify Connector is enabled below the input. Then add one of these task requests. They do not guarantee every link will succeed.

**Single transcript**

```text
Return the original-language transcript for this public Instagram video. Include only timestamp segments actually returned by the tool; do not invent timestamps.
PUBLIC_INSTAGRAM_URL_1
```

**Batch transcripts**

```text
Process exactly these public Instagram links:
1. PUBLIC_INSTAGRAM_URL_1
2. PUBLIC_INSTAGRAM_URL_2
For each input, return its original URL, processing status, original-language transcript, and timestamp segments if available. Match results by URL, never by result order. Do not add links or retry automatically.
```

**Subtitle file (SRT/VTT)**

```text
Transcribe this video and create an SRT or VTT file only if Manus can export files and the tool returned valid timestamps. Otherwise give me copyable subtitle text using only valid timestamps, or explain that timed subtitles are unavailable. Do not invent timestamps.
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
