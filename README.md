# Instagram AI Agent Skills

Instagram AI Agent Skills is a project for independent AI agent skills that help creators, marketers, researchers, and other users work with Instagram content. Each skill focuses on a separate task and can be installed on its own.

## Project overview

The repository is the project catalog and documentation home. It is not itself an installable skill. A skill contains the workflow for a user-facing task; a platform such as Codex or ChatGPT hosts that skill and provides its own tools and permissions. Apify supplies the external tools used by the current skill.

## Available skills

| Skill | What it does | Status |
| --- | --- | --- |
| [Instagram Transcript Extractor](skills/instagram-transcript-extractor/) | Gets spoken transcripts from public Instagram video links. You can request a summary, translation, or text-based analysis. | Available |

Download the Skill from the official [v0.1.0 Release asset](https://github.com/apismith-labs/instagram-ai-agent-skills/releases/download/v0.1.0/instagram-transcript-extractor.zip) (SHA-256: `cb5173bf999cb54feb06f190736111afaccb91ceae0bd845327391208ffcb331`). Use this named Release asset, not GitHub's automatically generated **Source code (zip)**. See the [ChatGPT guide](docs/platforms/chatgpt.md) or [Codex guide](docs/platforms/codex.md) for platform-specific instructions.

Reels analysis, competitor research, creator analysis, and comment analysis are possible future ideas, not available skills. Transcript-based analysis covers the returned text; it does not analyze video imagery, performance metrics, or audience response.

## Choose your platform

The skill uses your own Apify account. Runs use that account's plan allowance; check the [Apify Console](https://console.apify.com/) for current Runs and billing details. Connecting Apify provides external tool access. Installing the skill provides the task workflow. They are separate steps, and neither one completes the other.

- [Use the skill in ChatGPT](docs/platforms/chatgpt.md) — connect Apify, then upload the Skill ZIP.
- [Use the skill in Codex](docs/platforms/codex.md) — Codex desktop app and Codex CLI are separate environments with separate setup guidance.
- [Platform evidence matrix](docs/platform-support.md) — stage-by-stage project evidence. A published setup guide is not proof that a workflow passed testing.

Only this repository's Instagram Transcript Extractor is currently implemented. ChatGPT task reports, Codex installation/use reports, and earlier Actor tests come from separate sessions; they do not establish a complete new-user journey on either platform. ChatGPT chat is a different product from Codex, and Codex evidence does not establish ChatGPT support. Read the [detailed test status](docs/test-status.md) for the evidence boundaries.

## Documentation

- [User guide](docs/README.md)
- [Instagram Transcript Extractor user guide](docs/skills/instagram-transcript-extractor.md)
- [Project architecture](docs/project-architecture.md)
- [Platform support evidence](docs/platform-support.md)
- [Detailed test status](docs/test-status.md)
- [Transcript Extractor design](docs/transcript-extractor-design.md)
- [Acceptance test plan](docs/acceptance-test-plan.md)

## Support and license

For questions, problems, or ideas, [open a GitHub issue](https://github.com/apismith-labs/instagram-ai-agent-skills/issues). This project is licensed under the [MIT License](LICENSE).

## For maintainers

`skills/instagram-transcript-extractor/` is the maintained distribution source. `.agents/skills/instagram-transcript-extractor/` is the separate Codex project-discovery copy and does not synchronize automatically. Check it for independent edits before deliberately syncing changes from the source. The Codex installation example pins `v0.1.0`; review that ref when preparing a newer release. Before committing, run the offline tests, including the copy consistency check:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

The single-skill Release ZIP can be prepared with `python3 scripts/package_release.py --output /tmp/instagram-transcript-extractor.zip`; choose an output path outside the repository. See [project architecture](docs/project-architecture.md) for maintenance rules.
