# Use Instagram Transcript Extractor in Manus

This guide records the setup used in a project-owner report from one Manus account on 2026-10-29. That single-account test completed one Reel request; it is not a guarantee for other accounts, links, or batches. See the [platform evidence matrix](../platform-support.md) and [test status](../test-status.md).

## Before you start

You need a Manus account and your own [Apify account](https://console.apify.com/). Apify runs use your Apify account's plan allowance, and Manus tasks that use the Connector may consume Manus credits. See the [Apify Console](https://console.apify.com/) for current Runs and billing details, and check Manus for current credit information. No specific cost is estimated here. See the [Apify Manus integration guide](https://docs.apify.com/integrations/manus) for current platform information.

## 1. Enable Apify and authorize access

1. In Manus, open the **Plugins / Connectors** directory and find the official **Apify Connector**. If there are multiple Apify entries, check the details. In the reported account, the selected first/left entry showed **Connector Type: MCP**, **Author: Apify**, and described searching the Apify Store, running Actors, reading datasets, and checking run records.
2. Click the **+** on that Connector. Manus redirects to Apify for OAuth; sign in if prompted and approve the authorization. In the reported account, the Connector became active after approval, with **Try it out** and **Manage** shown.

Use the existing Apify Connector from the directory; this flow does not require creating a Custom MCP server. Names and labels may vary by account or interface version.

## 2. Import and enable the Skill

In Manus, open **Skills** and choose **+ Add → Import from GitHub**. Paste this Skill folder URL, which imports the current contents of the repository's `main` branch from the directory containing `SKILL.md`:

```text
https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-transcript-extractor
```

Select **Import**. Confirm that `instagram-transcript-extractor` appears in your personal Skill list and is enabled. In the reported account, that list was labeled **My Skills**; wording may vary. The [Manus Skills guide](https://help.manus.im/en/articles/14753565-how-to-share-and-use-skills-in-manus) covers importing and using Skills. GitHub import does not mean that this Skill is listed in Manus's public Explore skills marketplace; the project's inquiry to Manus support about public marketplace submission policy is still awaiting a response.

## 3. Run one explicit test

In a Manus conversation, type `/` and select `instagram-transcript-extractor`. Also check that the Apify Connector icon below the message input is enabled. Then request one public Reel, replacing the example with a real link:

```text
Use instagram-transcript-extractor to get the transcript of this public Instagram Reel:
https://www.instagram.com/reels/REPLACE_WITH_A_REAL_LINK/
```

For an accessible video with speech, a successful result may include a transcript matched to that link and timestamps when available. In the reported test for [one Reel](https://www.instagram.com/reels/DeKRjqRFQuJ/), Manus returned an English transcript with timestamps; the Apify Actor status was `SUCCEEDED`, there was one matching transcript, and `errMsg` was empty. The owner reports one URL, no duplicate inputs, no retries, and no additional Actor. The transcript's individual words were not independently checked against the audio.

One successful URL does not establish batch behavior or success for every link. If a public link is unavailable, restricted, or otherwise inaccessible, the Actor may not return a transcript. A video without detectable speech may also have no transcript. If the Actor fails, report the actual failure and stop; do not automatically retry or expand the request. Check the link and the status shown in Manus/Apify, and only try another action if you choose to do so.

## Evidence and official references

The Connector selection, OAuth, Skill import/enabled state, and one-Reel result above are reported from the project owner's single Manus account, not independently replayed by this repository update. They do not establish batch behavior or general success for other accounts or links.

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
