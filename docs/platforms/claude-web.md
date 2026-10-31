# Use Instagram Transcript Extractor in Claude web

This guide is for Claude on the web. It is not a guide to Claude Desktop or Claude Code. You need a Claude account with the Customize, Connectors, and Skills controls available, plus your own [Apify account](https://console.apify.com/). Apify runs use your account's plan allowance; check the Apify Console for current Runs and billing details.

## 1. Add and connect the Apify Plugin

1. In Claude, open **Customize → Connectors** and search for Apify.
2. Choose the **Apify Plugin** in Anthropic Directory. The Directory entry displayed the identifier `apify/apify-claude-code-plugin`; this identifies that listing. The Claude web steps below do not require installing Claude Code or a Claude Desktop extension.
3. Add the plugin. On the plugin's **Connectors** page, find `apify` and click **Connect**.
4. Sign in to your own Apify account. Review the account and requested permissions, then choose **Allow access** to complete OAuth.
5. Return to Claude and confirm that `apify` shows **Connected**.

When Claude asks permission to read Actor information, start an Actor, or read a dataset, review the request and grant the needed access if you want the task to continue. The prompts depend on the action and account settings; the same number of confirmations is not guaranteed for everyone.

## 2. Upload and enable the Skill

Use the current named Skill ZIP linked in the repository [README](../../README.md). The current documented asset is the `v0.1.0` Release ZIP. Download the named asset from GitHub Releases; do not use GitHub's automatically generated **Source code (zip)**.

In Claude web, open **Customize → Skills → Add → Upload skill** and upload the ZIP. Review the preview, confirm it is `instagram-transcript-extractor`, and enable it.

## 3. Select both the Skill and Connector

In the chat input, open the **+** menu and select `instagram-transcript-extractor`. Open the **Connectors** menu and make sure `apify` is enabled. Then use one of the requests below. Replace every placeholder shown, including each `PUBLIC_INSTAGRAM_URL` and `[TARGET_LANGUAGE]`, with an accessible public Instagram link or your target language.

## Copyable requests

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

## What to expect

The project owner reports that a single-link Claude web request returned a successful status, an original-language transcript, and timestamps. In a separate two-link request, two transcripts were returned and matched by URL, but the dataset pagination metadata was inconsistent, so those results were marked provisional. These observations do not establish general batch completeness. Subtitle file creation/export depends on Claude's available file capabilities and valid timestamps; it has not been established for every account.
