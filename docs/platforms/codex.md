# Use Instagram Skills in Codex

Codex in the ChatGPT desktop app and Codex CLI are separate environments. Follow the matching setup section below for your Codex version.

You need your own [Apify account](https://console.apify.com/). Actor runs use the allowance and billing terms of that account; see the Apify Console for current Runs and billing details. Connect Apify before asking the Skill to run a transcript task.

## Choose your Codex environment and connect Apify

### Codex desktop app

Follow Apify's [Codex desktop app guide](https://docs.apify.com/integrations/codex-app). It describes installing the Apify plugin from the Plugins marketplace and completing the browser OAuth flow. Select **Allow access** when prompted, then return to Codex. Interface controls can change; follow the current guide and prompts.

### Codex CLI

Follow Apify's [Codex CLI guide](https://docs.apify.com/integrations/codex-cli). It describes opening `/plugins`, adding the Apify plugin marketplace, installing the plugin, and completing OAuth when the first authenticated tool is called. Follow the terminal and browser prompts. Do not use desktop app instructions as evidence for CLI behavior, or vice versa.

## Install the Skill

Codex reads Skills from project `.agents/skills/` or user `~/.agents/skills/` directories; these are listed in [OpenAI's Codex Skill directory reference](https://developers.openai.com/api/reference/cli#use-the-cli-from-a-coding-agent). If you have a local checkout, copy the Skill's complete folder into one of those locations, then start a new session. Alternatively, use the Codex Skill Installer as below.

The Codex Skill Installer documents GitHub URLs in the form `tree/<ref>/<path>` and uses `main` as the default ref. The examples below use `main` and each Skill's own folder. `main` follows repository changes; it is a source branch, not either Skill's GitHub ZIP or ClawHub version. A `v0.1.0` ref points to older repository source. This project has not confirmed whether the Transcript Extractor `v0.2.1` tag contains matching source for both Skills, so these instructions do not use it as a fixed ref. The `$skill-installer` must be available in your Codex environment, and the public GitHub repository must be reachable; its Git method requires Git. The exact natural-language request and complete journey in each Codex environment have not been verified verbatim. The installation path is separate from the Apify plugin setup above.

In a Codex session where `$skill-installer` is available, you can ask:

```text
Use $skill-installer to install the skill at
https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-transcript-extractor
using the Git method. Use ~/.agents/skills/ as the destination skills folder;
the installed skill should be ~/.agents/skills/instagram-transcript-extractor/.
If that destination already exists, stop and tell me; do not overwrite it.
```

If `$skill-installer` is not available in your Codex environment, do not substitute an unverified manual installation process. [Open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues) with your Codex version and environment (desktop app or CLI); do not include credentials or other private information. This project has not verified an alternative installation method.

This example follows the repository's `main` branch and can change as that branch changes. If `~/.agents/skills/instagram-transcript-extractor/` already exists, inspect that installation and stop before reinstalling. Do not overwrite it or guess at an update/removal procedure. The exact request above has not been tested word for word, and installer behavior can vary by Codex environment.

After installation, start a new Codex session and explicitly check that the Skill is discovered. You can also invoke it directly with `$instagram-transcript-extractor` or `$instagram-creator-reels-insights`:

```text
Use $instagram-transcript-extractor and confirm that you found the
instagram-transcript-extractor skill. Do not run an Actor yet.
```

Success means the new session identifies the Skill by the name `instagram-transcript-extractor`. If Codex cannot find it, check the requested installation directory and confirm that `SKILL.md` is present; do not treat the installation as usable until discovery succeeds. If it remains unavailable, [open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues).

## Install Creator Video Insights

Creator Video Insights is a separate Skill with its own source directory. In a Codex session where `$skill-installer` is available, use the same Git installation method documented above, but point it to the Creator directory and a matching destination:

```text
Use $skill-installer to install the skill at
https://github.com/apismith-labs/instagram-ai-agent-skills/tree/main/skills/instagram-creator-reels-insights
using the Git method. Use ~/.agents/skills/ as the destination skills folder;
the installed skill should be ~/.agents/skills/instagram-creator-reels-insights/.
If that destination already exists, stop and tell me; do not overwrite it.
```

Start a new Codex session and check that `instagram-creator-reels-insights` is discovered before using it. For an example Creator request, see the [README prompts](../../README.md#instagram-creator-video-insights-prompts). The Creator task workflow has not been confirmed in Codex. If `$skill-installer` is unavailable, do not substitute an unverified manual installation process; [open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues).

## Request a transcript

Once Apify is connected and the new session has discovered the Skill, explicitly request it and replace the example with a real public Instagram video link:

```text
Use $instagram-transcript-extractor to get the transcript of this public Instagram Reel:
https://www.instagram.com/reel/REPLACE_WITH_A_REAL_LINK/
```

## Copyable requests

Replace every placeholder shown, including each `PUBLIC_INSTAGRAM_URL` and `[TARGET_LANGUAGE]`, with an accessible public Instagram link or your target language. After confirming the Skill is discovered in a new session, invoke it with `$instagram-transcript-extractor` and add the task you need. These are request examples; they do not guarantee every link will succeed.

**Single transcript**

```text
Use $instagram-transcript-extractor to return the original-language transcript for this public Instagram video. Include only timestamp segments actually returned by the tool; do not invent timestamps.
PUBLIC_INSTAGRAM_URL_1
```

**Batch transcripts**

```text
Use $instagram-transcript-extractor on exactly these public Instagram links:
1. PUBLIC_INSTAGRAM_URL_1
2. PUBLIC_INSTAGRAM_URL_2
For each input, return its original URL, processing status, original-language transcript, and timestamp segments if available. Match results by URL, never by result order. Do not add links or retry automatically.
```

**Subtitle file (SRT/VTT)**

```text
Use $instagram-transcript-extractor to transcribe this video and create an SRT or VTT file only if this host can export files and the tool returned valid timestamps. Otherwise give me copyable subtitle text using only valid timestamps, or explain that timed subtitles are unavailable. Do not invent timestamps.
PUBLIC_INSTAGRAM_URL_1
```

**Translation**

```text
Use $instagram-transcript-extractor to return the original-language transcript for this video, then provide a separate [TARGET_LANGUAGE] translation. Preserve any timestamp segments actually returned; do not invent them.
PUBLIC_INSTAGRAM_URL_1
```

**Summary**

```text
Use $instagram-transcript-extractor to transcribe each video and give each link its own short summary. Keep the videos separate and match every result to its original URL.
1. PUBLIC_INSTAGRAM_URL_1
2. PUBLIC_INSTAGRAM_URL_2
```

**Content analysis**

```text
Use $instagram-transcript-extractor to identify the hook, core insight, CTA, and content cues based only on this video's transcript. Include timestamps only where valid timestamp segments were returned. Do not analyze visuals, engagement metrics, or audience response.
PUBLIC_INSTAGRAM_URL_1
```
