# Instagram AI Agent Skills

Instagram AI Agent Skills helps creators, marketers, researchers, and other AI agent users work with Instagram content. The first skill extracts transcripts from public Instagram Reels and videos, ready for summaries, translations, and text-based analysis.

## Instagram Transcript Extractor

Instagram Transcript Extractor accepts one or more public Instagram Reel, video, or supported video post links and helps your agent retrieve the spoken transcript. You can then ask for a summary, a translation, or an analysis based on the text. When timestamps are available, your agent can include them. Some videos may have incomplete transcripts or no transcript available.

Future skills may explore Reels analysis, competitor research, creator analysis, and comments. These are ideas for later, not features available today.

## Getting started

1. **Install the skill.** The complete [skill source](skills/instagram-transcript-extractor/) includes the instructions, reference, and helper script. In one test, the Codex skill installer used Git to install these files into `~/.agents/skills/`. The installer requires Python 3, Git, and access to GitHub; it stops if the destination already exists. You can ask Codex to use the installer with the following request; this exact conversational request has not been tested:

   ```text
   Use $skill-installer to install skills/instagram-transcript-extractor from
   https://github.com/apismith-labs/instagram-ai-agent-skills using the Git
   method, at commit 34fcf8641f35885e7da25dacc080643b0464c348. Install it in
   ~/.agents/skills/ without overwriting an existing skill.
   ```

   Start a new Codex session after installation and try this explicit request:

   ```text
   Use $instagram-transcript-extractor and confirm whether the skill is available.
   Do not run an Actor yet.
   ```

   If it is not available, see the [test status](docs/test-status.md) or [open an issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues).
2. **Connect Apify.** Use your own Apify account, or sign up at the [Apify Console](https://console.apify.com/) if you don't have one. Follow the official guide for [Codex in the ChatGPT desktop app](https://docs.apify.com/integrations/codex-app) or for [Codex CLI in a terminal](https://docs.apify.com/integrations/codex-cli). Installing the skill and connecting Apify are separate steps. You can review runs and billing details in your Apify Console.
3. **Ask for a transcript.** Explicitly request `$instagram-transcript-extractor`, give Codex a public link, and tell it what you would like to do with the text.

**Validation status:** The Git installer has installed the personal skill files. A separate new Codex session reported explicitly using the personal skill to prepare an input; it did not run an Actor. Another test reported project-level explicit use. These tests do not establish that the installation request above works unchanged in every Codex interface. Automatic selection from a natural-language request and a complete Apify run after GitHub installation remain unverified. ChatGPT chat is a separate product: its skill installation, connection, and full workflow have not been verified. See the [test status](docs/test-status.md) for details.

## Try asking your agent

Replace the example links with public Instagram links:

```text
Get the transcript of this Instagram Reel:
https://www.instagram.com/reel/EXAMPLE1/
```

```text
Get the transcript of this Instagram Reel and give me a short summary:
https://www.instagram.com/reel/EXAMPLE1/
```

```text
Get the transcripts of these Instagram videos and summarize each one:
https://www.instagram.com/reel/EXAMPLE1/
https://www.instagram.com/reel/EXAMPLE2/
```

```text
Transcribe this public Instagram video, translate the spoken text into Spanish,
and include timestamps if available:
https://www.instagram.com/reel/EXAMPLE1/
```

## Feedback and license

Questions, problems, or ideas? [Open an issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues).

This project is licensed under the [MIT License](LICENSE).

## For maintainers

`skills/instagram-transcript-extractor/` is the maintained distribution source. `.agents/skills/instagram-transcript-extractor/` is the project-level discovery copy; it does not update automatically. After changing the source, check the copy for independent changes and synchronize it. The installation example pins a tested commit, which may not be the latest version; review and update the pinned commit when releasing skill changes. Before committing, run the offline tests, including the consistency check:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```
