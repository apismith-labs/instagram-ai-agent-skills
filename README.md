# Instagram AI Agent Skills

Instagram AI Agent Skills is a collection of independent skills for creators, marketers, researchers, and other AI agent users working with Instagram content. Each skill addresses a focused task and can be installed separately.

## Skill catalog

**Available: [Instagram Transcript Extractor](skills/instagram-transcript-extractor/).** Give your agent one or more public Instagram Reel, video, or supported video post links to retrieve spoken transcripts. You can then ask for a summary, translation, or analysis based on the text. Timestamps may be included when available; transcripts may be incomplete or unavailable.

**Ideas only:** Reels analysis, competitor research, creator analysis, and comments are possible future directions; these skills are not implemented.

## Getting started with Instagram Transcript Extractor

You need your own Apify account to run the skill. Actor runs use the allowance and billing terms of your Apify account; check your Apify Console for current usage details. The Apify connection gives ChatGPT or Codex access to external Apify tools. The Skill itself supplies the transcript workflow instructions. Installing the Skill does not connect Apify, and connecting Apify does not install the Skill.

### Download the skill

Download **`instagram-transcript-extractor.zip`** from the [v0.1.0 Release asset](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.1.0/instagram-transcript-extractor.zip), or open the [v0.1.0 Release page](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/tag/v0.1.0) and choose that file under **Assets**. Do not choose GitHub's automatically generated **Source code (zip)**. Keep the downloaded ZIP intact when uploading it to ChatGPT; do not unzip it first.

Optional SHA-256 check: `cb5173bf999cb54feb06f190736111afaccb91ceae0bd845327391208ffcb331`.

### Use in ChatGPT

OpenAI currently documents ChatGPT Skills for eligible Business, Enterprise, Healthcare, and Edu users, subject to workspace settings and product availability ([OpenAI Skills guide](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)). Availability can vary by account and rollout: the project owner reports seeing the Skills page on a Plus account, but this does not confirm Plus availability for everyone. Check your own ChatGPT interface; Plus access is neither guaranteed nor ruled out here.

1. **Create your Apify account and connect it to ChatGPT.** If you do not have an Apify account, [sign up at Apify](https://console.apify.com/) and sign in. In ChatGPT, open **Plugins → + → Add custom MCP server**. Enter a name such as `Apify` and set the Server URL to `https://mcp.apify.com`. Choose **OAuth** in the authentication options and complete the Apify authorization. Review the risk notice, then select **Create as a plugin**. Check the discovered tools and metadata, then install the generated plugin. The [OpenAI custom MCP server guide](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt) documents this current flow; available controls may change.

   OpenAI currently documents custom MCP server connections on ChatGPT web for Business and Enterprise/Edu. Its guide says Business workspace admins and owners can create and publish workspace connections; Enterprise/Edu admins can grant selected members permission to create connections, while only admins or owners publish connections to the workspace. These are workspace-level permissions and are not a requirement that every user publish a personal plugin. If **Add custom MCP server** is missing, check your account plan and workspace permissions, then contact your workspace administrator if needed. The current evidence here does not confirm Plus users' custom MCP creation rights. Pro read/fetch access does not establish that an account can run Apify Actors. See OpenAI's [connected apps guide](https://help.openai.com/en/articles/11487775-connected-apps-in-chatgpt) for general app availability and account connections.

2. **Upload the Skill after connecting Apify.** Open **Plugins** in the sidebar, choose the **Skills** tab, select **Create**, then **Upload from your computer**. Select the intact `instagram-transcript-extractor.zip` file; do not unzip it. Wait for ChatGPT's upload scan. The Skill may become available immediately, show **Needs Review**, or show **Blocked**. For **Needs Review**, read and follow the displayed review prompt. A **Blocked** Skill cannot be used; the scan status alone does not mean the ZIP is damaged. Do not repeatedly upload the same ZIP. Record the release version and the scan message shown in your interface, then [open an issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues) for help. Do not include credentials or personal sensitive information in an issue. Open the Skill from the Skills list to confirm it appears. The owner reported that v0.1.0 initially displayed the Instagram icon. ChatGPT's editor may rewrite icon metadata when the Skill is reloaded; see [known validation details](docs/test-status.md).
3. Start a new chat. Type **@** in the message box and select the installed Apify plugin. If a later message needs new Apify data, select the plugin again; availability may apply per message.
4. Ask: `Use Instagram Transcript Extractor to get the transcript of this public Instagram Reel: https://www.instagram.com/reel/REPLACE_WITH_A_REAL_LINK/` Replace the example URL with a real public Instagram video link. Ask for a summary or translation if you want one.

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

The installer normally uses `$CODEX_HOME/skills` (usually `~/.codex/skills`) unless given another destination, and it stops when the destination already exists. If `~/.agents/skills/instagram-transcript-extractor/` already exists, inspect that installation first and stop before reinstalling or overwriting it. Do not delete it as part of troubleshooting. After installation, start a new Codex session and check discovery explicitly:

```text
Use $instagram-transcript-extractor and confirm that you found the
instagram-transcript-extractor skill.
Do not run an Actor yet.
```

Success means a new session identifies the `instagram-transcript-extractor` skill by name. If Codex says it cannot find the skill, check `~/.agents/skills/instagram-transcript-extractor/` and confirm it contains `SKILL.md`; do not report the installation as complete until the new session finds it. If it still is not discovered, [open an issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues). The exact README installation request and discovery flow for each Codex environment remain unverified.

### Send a video and understand the result

Replace the example link with a real public Instagram Reel or supported video link:

```text
Get the transcript of this public Instagram video:
https://www.instagram.com/reel/REPLACE_WITH_A_REAL_LINK/
```

When successful, the Skill should return the spoken words for each accessible link. It adds a summary or translation when you request one. A video may not be processable, and results are not guaranteed for every link. Results may include timestamps when available; missing timestamps do not by themselves mean transcription failed. A video with no detectable speech may have no transcript; private, deleted, restricted, or otherwise inaccessible videos may not be processable. If a batch has mixed results, use the successful transcripts and review the listed failures individually.

If the agent says Apify is not connected, complete the OAuth connection in the appropriate platform guide above, return to the conversation, add the Apify connector to that chat if the interface requires it, and ask again. If a Codex Skill directory already exists, inspect that installation and stop before overwriting it. No supported update or uninstall procedure has been verified across these platforms; existing users should inspect their installation and should not assume an upgrade procedure is available. For help, use the current platform's skill management controls or [open an issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues).

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

The [project architecture](docs/project-architecture.md) describes how to add and maintain independent skills. `skills/instagram-transcript-extractor/` is the maintained distribution source. `.agents/skills/instagram-transcript-extractor/` is the project-level discovery copy; it does not update automatically. After changing the source, check the copy for independent changes and synchronize it. The installation example uses the `v0.1.0` ref; review the release ref when newer versions are published. Before committing, run the offline tests, including the consistency check:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

To prepare a single-skill release ZIP, run `python3 scripts/package_release.py --output /tmp/instagram-transcript-extractor.zip` with a new output path outside the repository. The archive contains one top-level `instagram-transcript-extractor/` folder with the skill files and license. Upload it as a GitHub Release asset only after review.
