# Instagram Transcript Extractor

Instagram Transcript Extractor is the one currently available Skill in this project. Give your agent one or more public Instagram Reel, video, or supported video post links to request spoken transcripts. You can also ask for a summary, translation, or analysis based on the returned text.

## Before using it

You need your own Apify account, and Apify must be connected in the platform where you use the Skill. Runs use that account's plan allowance; check the [Apify Console](https://console.apify.com/) for current Runs and billing details. Follow the setup guide for your platform:

- [ChatGPT setup](../platforms/chatgpt.md)
- [Codex setup](../platforms/codex.md)

Connecting Apify makes external Apify tools available to the platform. Installing this Skill provides the transcript workflow. They are separate steps.

## What to ask

For one link:

```text
Get the transcript of this public Instagram video:
https://www.instagram.com/reel/REPLACE_WITH_A_REAL_LINK/
```

For several links with summaries:

```text
Get the transcript of each public Instagram video and give me a short summary of each:
https://www.instagram.com/reel/REPLACE_WITH_A_REAL_LINK_1/
https://www.instagram.com/reel/REPLACE_WITH_A_REAL_LINK_2/
```

Replace each example with a real public link. You can request a translation or a text-based analysis as well. The Skill should keep results associated with their input links and identify items that could not be matched or completed; it should not guess a missing result.

## Understand the result

When successful, expect the spoken words returned for the accessible link. A requested summary, translation, or text analysis should be presented separately from the transcript. Timestamps may be included when available; missing timestamps do not by themselves mean transcription failed. The Skill does not guarantee a complete transcript for every video.

- A video with no detectable speech may not yield a transcript.
- A private, deleted, restricted, or otherwise inaccessible video may not be processable.
- In a batch, some links may succeed while others fail. Use the successful results and review the listed failures individually; one successful item does not mean every item succeeded.
- Text-based analysis uses the returned transcript. It does not establish what appears in the video, its performance metrics, or audience reaction.

If the platform says Apify is not connected, complete the connection in its platform guide and then try again. If a result is missing or unclear, ask the agent to explain which link it could not process. For help with the Skill, [open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues) without including credentials or private content.
