# Project architecture

Instagram AI Agent Skills is one project containing independently maintained skills. The repository root is the project catalog and onboarding entry point; it is not itself an installable skill. Instagram Transcript Extractor is the first implemented and separately validated skill. Instagram Creator Reels Insights has a source and Codex discovery mirror, but is still in development and not a validated or publishable capability. Profile Posts public output field names/types are documented, while media type values, result semantics/order, and completeness remain unverified. Its staged offline planner does not establish host run-option forwarding or verification. Other Reels analysis, competitor research, and comment-analysis ideas remain unimplemented.

Host-specific observations, including dated Codex live tool inventories and their limits, belong in [interface verification](interface-verification.md); a missing tool in one session does not characterize every Codex setup or local plugin/cache configuration.

The [multi-skill, multi-platform PRD](prd-multi-skill-multi-platform-structure.md) describes the requirements for this structure.

## Responsibilities

- `skills/<skill-name>/` is the canonical distribution and maintenance source for each implemented skill, including its `SKILL.md` and any needed references and scripts. The current source is [Instagram Transcript Extractor](../skills/instagram-transcript-extractor/).
- The in-development [Instagram Creator Reels Insights source](../skills/instagram-creator-reels-insights/) is not yet a supported user-facing feature. Its current implementation and validation blockers are recorded in [interface verification](interface-verification.md) and [test status](test-status.md).
- `.agents/skills/<skill-name>/`, when maintained, is a separate Codex project discovery copy. It does not synchronize automatically. Before updating it, check for independent edits; synchronize deliberately and run the offline consistency test. A personal installation is separate from both repository copies.
- `README.md` is the public project catalog and onboarding entry point. `docs/README.md` routes users to platform setup and skill guides; `docs/platforms/` contains separate host setup guides, and `docs/skills/` contains user guides for implemented skills. Project and skill design documents, the [platform evidence matrix](platform-support.md), and [test details](test-status.md) remain separate from these user instructions. `tests/` holds offline tests, including checks on maintained copies.
- A **skill** defines a user-facing task and workflow. An **Actor** is an underlying service a skill may use; an agent **platform** hosts or invokes a skill and supplies its own discovery, permissions, tools, and file capabilities. One project, skill, Actor, and platform are not interchangeable units.

## Adding a skill

For every skill, add a complete, independently distributable `skills/<skill-name>/` unit with only the references and scripts it needs; do not create empty future-skill directories. A directory or Codex discovery mirror does not make a skill available: record implementation, interface blockers, tests, and platform evidence separately, and list it as available only after required integration and validation gates pass. Update maintained Codex discovery copies deliberately and keep mirror tests discovery-based so new canonical skills cannot be omitted silently.

Add `docs/shared/` only when multiple implemented skills actually share maintained material. Platform guides may explain host-specific setup using current official instructions, but must identify when the project's own workflow is unverified; publishing a guide or linking official instructions does not demonstrate project support. Platform support stages and evidence belong in the [matrix](platform-support.md), with detailed observations in [test status](test-status.md).

Transcript-based analysis is limited to the text actually obtained. Do not describe it as analysis of images, performance metrics, or audience response without adding and validating the relevant data sources. Scheduled monitoring is not a current feature; any future monitoring requires separate validation of discovery, scheduling, persistent state, and deduplication.

## Release maintenance

Review versioning and release records as skills evolve. `scripts/package_release.py` builds a skill ZIP from its canonical `SKILL.md`, `references/workflow.md`, `scripts/workflow.py`, `agents/openai.yaml`, slug-named icon, and the root `LICENSE`. It supports the first skill by default and accepts `--skill <slug>` for a different canonical skill. Packaging checks exclude bytecode/cache files and do not establish runtime support. The Codex installation example in `docs/platforms/codex.md` pins `v0.1.0`; review the pinned ref when preparing a newer release. Do not infer that a new ref or a different host has been verified from an earlier test.
