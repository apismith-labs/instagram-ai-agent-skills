# Use Instagram Transcript Extractor in Codex

Codex in the ChatGPT desktop app and Codex CLI are separate environments. Follow the matching setup section below for your Codex version.

You need your own [Apify account](https://console.apify.com/). Actor runs use the allowance and billing terms of that account; see the Apify Console for current Runs and billing details. Connect Apify before asking the Skill to run a transcript task.

## Choose your Codex environment and connect Apify

### Codex desktop app

Follow Apify's [Codex desktop app guide](https://docs.apify.com/integrations/codex-app). It describes installing the Apify plugin from the Plugins marketplace and completing the browser OAuth flow. Select **Allow access** when prompted, then return to Codex. Interface controls can change; follow the current guide and prompts.

### Codex CLI

Follow Apify's [Codex CLI guide](https://docs.apify.com/integrations/codex-cli). It describes opening `/plugins`, adding the Apify plugin marketplace, installing the plugin, and completing OAuth when the first authenticated tool is called. Follow the terminal and browser prompts. Do not use desktop app instructions as evidence for CLI behavior, or vice versa.

## Install the Skill

The following installation request is based on a reported successful use of the installer's Git method and a `v0.1.0` source ref. The `$skill-installer` must be available in your Codex environment, and the public GitHub repository must be reachable; its Git method requires Git. The installer supports multiple fetch methods; the request below explicitly selects the Git method. This project has not tested the installer's default method. The exact natural-language request and complete journey in each Codex environment have not been verified verbatim. The installation path is separate from the Apify plugin setup above.

In a Codex session where `$skill-installer` is available, you can ask:

```text
Use $skill-installer to install the skill at
https://github.com/apismith-labs/instagram-ai-agent-skills/tree/v0.1.0/skills/instagram-transcript-extractor
using the Git method. Use ~/.agents/skills/ as the destination skills folder;
the installed skill should be ~/.agents/skills/instagram-transcript-extractor/.
If that destination already exists, stop and tell me; do not overwrite it.
```

If `$skill-installer` is not available in your Codex environment, do not substitute an unverified manual installation process. [Open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues) with your Codex version and environment (desktop app or CLI); do not include credentials or other private information. This project has not verified an alternative installation method.

This pins the installation example to `v0.1.0`; it may not be the latest release. If `~/.agents/skills/instagram-transcript-extractor/` already exists, inspect that installation and stop before reinstalling. Do not overwrite it or guess at an update/removal procedure. The exact request above has not been tested word for word, and installer behavior can vary by Codex environment.

After installation, start a new Codex session and explicitly check that the Skill is discovered:

```text
Use $instagram-transcript-extractor and confirm that you found the
instagram-transcript-extractor skill. Do not run an Actor yet.
```

Success means the new session identifies the Skill by the name `instagram-transcript-extractor`. If Codex cannot find it, check the requested installation directory and confirm that `SKILL.md` is present; do not treat the installation as usable until discovery succeeds. If it remains unavailable, [open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues).

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
