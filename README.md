# Instagram AI Agent Skills

Instagram AI Agent Skills is a collection of independent skills for creators, marketers, researchers, and other AI agent users working with Instagram content. Each skill addresses a focused task and can be installed separately.

## Skill catalog

**Available: [Instagram Transcript Extractor](skills/instagram-transcript-extractor/).** Give your agent one or more public Instagram Reel, video, or supported video post links to retrieve spoken transcripts. You can then ask for a summary, translation, or analysis based on the text. Timestamps may be included when available; transcripts may be incomplete or unavailable.

**Ideas only:** Reels analysis, competitor research, creator analysis, and comments are possible future directions; these skills are not implemented.

## Getting started with Instagram Transcript Extractor

### Codex

1. **Install the skill.** The complete [skill source](skills/instagram-transcript-extractor/) includes the instructions, reference, and helper script. A tester installed the skill from GitHub using the Codex skill installer's Git method and reported that installation was easy. The installer requires Python 3, Git, and access to GitHub; it stops if the destination already exists. After the distribution changes are published to `main`, you can ask Codex to install that branch using the following request; the exact request and the updated distribution version have not been tested:

   ```text
   Use $skill-installer to install skills/instagram-transcript-extractor from
   https://github.com/apismith-labs/instagram-ai-agent-skills using the Git
   method from the main branch. Install it in ~/.agents/skills/ without
   overwriting an existing skill.
   ```

   Start a new Codex session after installation and try this explicit request:

   ```text
   Use $instagram-transcript-extractor and confirm whether the skill is available.
   Do not run an Actor yet.
   ```

   If it is not available, see the [test status](docs/test-status.md) or [open an issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues).
2. **Connect Apify.** Use your own Apify account, or sign up at the [Apify Console](https://console.apify.com/) if you don't have one. Follow the official guide for [Codex in the ChatGPT desktop app](https://docs.apify.com/integrations/codex-app) or for [Codex CLI in a terminal](https://docs.apify.com/integrations/codex-cli). Installing the skill and connecting Apify are separate steps. You can review runs and billing details in your Apify Console.
3. **Ask for a transcript.** Explicitly request `$instagram-transcript-extractor`, give Codex a public link, and tell it what you would like to do with the text.

### ChatGPT

Once the first release is published, download the Instagram Transcript Extractor ZIP from [GitHub Releases](https://github.com/apismith-labs/instagram-ai-agent-skills/releases). In ChatGPT's Skills page, choose **Upload from computer** and select the ZIP. Connect your own Apify account through OAuth separately from uploading the skill, then ask for a transcript. Availability depends on your ChatGPT account and workspace. A user uploaded the verified release-candidate ZIP and confirmed that the Instagram icon appeared in the Skills list. Earlier ChatGPT task results were reported separately; completing a transcript task with this exact ZIP and an Apify connection remains unverified.

**Validation status:** A Codex tester reported installing a specified commit with Git, connecting Apify, and explicitly using the skill to obtain a transcript and Chinese translation; the tester first encountered a not-connected message. Separately, a ChatGPT tester reported uploading a skill, seeing it loaded for a natural-language task, and receiving matching single-link and two-link results. A user also confirmed that the verified release-candidate ZIP uploads to the ChatGPT Skills list and displays the Instagram icon; that check did not include an Apify task. The reports have not been independently checked against original traces. Codex automatic selection, authorization recovery, failure handling, and file import/export remain unverified. See [platform support](docs/platform-support.md) and [test status](docs/test-status.md).

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

The [project architecture](docs/project-architecture.md) describes how to add and maintain independent skills. `skills/instagram-transcript-extractor/` is the maintained distribution source. `.agents/skills/instagram-transcript-extractor/` is the project-level discovery copy; it does not update automatically. After changing the source, check the copy for independent changes and synchronize it. The installation example uses `main`, which can change; use a verified release ref when reproducibility matters. Before committing, run the offline tests, including the consistency check:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

To prepare a single-skill release ZIP, run `python3 scripts/package_release.py --output /tmp/instagram-transcript-extractor.zip` with a new output path outside the repository. The archive contains one top-level `instagram-transcript-extractor/` folder with the skill files and license. Upload it as a GitHub Release asset only after review.
