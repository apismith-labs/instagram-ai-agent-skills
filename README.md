# Instagram AI Agent Skills

Instagram AI Agent Skills is a collection of independent skills for creators, marketers, researchers, and other AI agent users working with Instagram content. Each skill addresses a focused task and can be installed separately.

## Skill catalog

**Available: [Instagram Transcript Extractor](skills/instagram-transcript-extractor/).** Give your agent one or more public Instagram Reel, video, or supported video post links to retrieve spoken transcripts. You can then ask for a summary, translation, or analysis based on the text. Timestamps may be included when available; transcripts may be incomplete or unavailable.

**Ideas only:** Reels analysis, competitor research, creator analysis, and comments are possible future directions; these skills are not implemented.

## Getting started with Instagram Transcript Extractor

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

**Validation status:** Codex is the only host with reported skill tests so far; the available records do not establish that every Codex interface has passed. The Git installer installed the personal skill files. A separate new Codex session reported explicitly using the personal skill to prepare an input; it did not run an Actor. Another test reported project-level explicit use. These tests do not establish that the installation request above works unchanged in every Codex interface. Automatic selection and the complete new-user journey from README installation through Apify connection to a transcript remain unverified. Codex in the ChatGPT desktop app, Codex CLI, and ChatGPT chat are distinct environments; Codex results do not establish support in ChatGPT chat, whose installation, connection, and full workflow have not been verified. See [platform support](docs/platform-support.md) and [test status](docs/test-status.md) for evidence and limitations.

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

The [project architecture](docs/project-architecture.md) describes how to add and maintain independent skills. `skills/instagram-transcript-extractor/` is the maintained distribution source. `.agents/skills/instagram-transcript-extractor/` is the project-level discovery copy; it does not update automatically. After changing the source, check the copy for independent changes and synchronize it. The installation example pins a tested commit, which may not be the latest version; review and update the pinned commit when releasing skill changes. Before committing, run the offline tests, including the consistency check:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```
