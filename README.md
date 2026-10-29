# Instagram AI Agent Skills

Instagram AI Agent Skills is a collection of independent skills for creators, marketers, researchers, and other AI agent users working with Instagram content. Each skill addresses a focused task and can be installed separately.

## Skill catalog

**Available: [Instagram Transcript Extractor](skills/instagram-transcript-extractor/).** Give your agent one or more public Instagram Reel, video, or supported video post links to retrieve spoken transcripts. You can then ask for a summary, translation, or analysis based on the text. Timestamps may be included when available; transcripts may be incomplete or unavailable.

**Ideas only:** Reels analysis, competitor research, creator analysis, and comments are possible future directions; these skills are not implemented.

## Getting started with Instagram Transcript Extractor

### Download the skill

Download **`instagram-transcript-extractor.zip`** from the [v0.1.0 Release Assets](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.1.0/instagram-transcript-extractor.zip). On the Release page, use the file under **Assets**. Do not choose GitHub's automatically generated **Source code (zip)**. Keep the downloaded ZIP intact when uploading it to ChatGPT; do not unzip it first.

Optional SHA-256 check: `cb5173bf999cb54feb06f190736111afaccb91ceae0bd845327391208ffcb331`.

### Use in ChatGPT

1. Open **Plugins** in the sidebar, choose the **Skills** tab, select **Create**, then **Upload from your computer**. Select the intact `instagram-transcript-extractor.zip` file. Open the skill from the Skills list to confirm it appears. The owner reported that v0.1.0 initially displayed the Instagram icon. ChatGPT's editor may rewrite icon metadata when the skill is reloaded; see [known validation details](docs/test-status.md).
2. **Connect Apify separately.** Use the [Apify ChatGPT guide](https://docs.apify.com/integrations/chatgpt) and the current ChatGPT interface's **Plugins**, **Apps**, or **Connectors** entry to connect with OAuth. OpenAI's [connected apps guide](https://help.openai.com/en/articles/11487775-connected-apps-in-chatgpt) explains app availability and account connections. Follow the controls shown in your account: the official guides describe different interface paths, and Developer mode is not a universal prerequisite for every existing connection flow. Skill upload and Apify authorization are separate steps.
3. Start a new chat. If needed, select **+**, then **More** (or the equivalent app picker in your interface) and add the Apify connector to that conversation. A connection saved to your account may still need to be added to each new conversation.
4. Ask: `Use Instagram Transcript Extractor to get the transcript of this public Instagram Reel: https://www.instagram.com/reel/REPLACE_WITH_A_REAL_LINK/` Replace the example URL with a real public Instagram video link. Ask for a summary or translation if you want one.

Skills are currently documented by OpenAI as available to eligible Business, Enterprise, Healthcare, and Edu users, subject to workspace settings and product availability ([OpenAI Skills guide](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)). Access can vary by account and rollout: the project owner also reports seeing Skills on a Plus account. Check your own ChatGPT interface; Plus access is neither guaranteed nor ruled out here.

### Use in Codex

Codex in the ChatGPT desktop app and Codex CLI are different environments. Install the skill in the environment you intend to use, then follow the corresponding [Apify setup guide for Codex desktop](https://docs.apify.com/integrations/codex-app) or [Apify setup guide for Codex CLI](https://docs.apify.com/integrations/codex-cli).

In Codex, ask the built-in `$skill-installer` to install the GitHub skill using the `v0.1.0` ref and destination `~/.agents/skills/instagram-transcript-extractor/`. The installer needs Python 3, Git, and GitHub access; its Git method was reported to install the skill successfully. The exact natural-language request below has not been tested verbatim, and project evidence does not establish the same flow in both Codex desktop and CLI:

```text
Use $skill-installer to install the skill at
https://github.com/apismith-labs/instagram-ai-agent-skills/tree/v0.1.0/skills/instagram-transcript-extractor
using the Git method. Use ~/.agents/skills/ as the destination skills folder;
the installed skill should be ~/.agents/skills/instagram-transcript-extractor/.
If that destination already exists, stop and tell me; do not overwrite it.
```

The installer normally uses `$CODEX_HOME/skills` (usually `~/.codex/skills`) unless given another destination, and it stops when the destination already exists. If it reports that the folder exists, ask Codex to inspect it or choose a different empty destination; do not ask it to overwrite files. After installation, start a new Codex session and check discovery explicitly:

```text
Use $instagram-transcript-extractor to confirm that the skill is available.
Do not run an Actor yet.
```

If Codex says the skill is unavailable, check the install location for a complete `SKILL.md` folder and start a fresh session. If it still is not discovered, [open an issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues). The exact README installation request and discovery flow for each Codex environment remain unverified.

### Send a video and understand the result

Replace the example link with a real public Instagram Reel or supported video link:

```text
Get the transcript of this public Instagram video:
https://www.instagram.com/reel/REPLACE_WITH_A_REAL_LINK/
```

You can also ask for a summary or translation, or provide several links and ask for a transcript of each. Results may include timestamps when available. A video with no detectable speech may have no transcript; private, deleted, restricted, or otherwise inaccessible videos may not be processable. If a batch has mixed results, use the successful entries and review the listed failures individually. No timestamps means timing data was not available in the returned result; it does not by itself mean the transcript failed.

If the agent says Apify is not connected, complete the OAuth connection in the appropriate platform guide above, return to the conversation, add the Apify connector to that chat if the interface requires it, and ask again. Updates and uninstall steps have not been verified across these platforms; use the platform's current skill management controls or [ask for help in an issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues).

**Evidence limits:** ChatGPT v0.1.0 ZIP download and SHA-256 have been checked, and the owner reports importing it and initially seeing the brand icon. A later editor reload rewrote the icon reference and added a generic `assets/icon.svg`; this behavior is recorded in [test status](docs/test-status.md). Earlier ChatGPT transcript task results came from a separately uploaded version whose identity is not confirmed as v0.1.0. Codex Git installation and explicit use were reported, but the README request was not run verbatim and the Codex desktop and CLI results are not interchangeable. See the [platform evidence matrix](docs/platform-support.md) for the stage-by-stage status.

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
