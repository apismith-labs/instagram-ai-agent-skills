# Project architecture

Instagram AI Agent Skills is one project containing independently maintained skills. The repository root is the project catalog and onboarding entry point; it is not itself an installable skill. Currently, only Instagram Transcript Extractor is implemented. Reels analysis, competitor research, creator analysis, and comment analysis are unapproved ideas, not available skills.

The [multi-skill, multi-platform PRD](prd-multi-skill-multi-platform-structure.md) describes the requirements for this structure.

## Responsibilities

- `skills/<skill-name>/` is the canonical distribution and maintenance source for each implemented skill, including its `SKILL.md` and any needed references and scripts. The current source is [Instagram Transcript Extractor](../skills/instagram-transcript-extractor/).
- `.agents/skills/<skill-name>/`, when maintained, is a separate Codex project discovery copy. It does not synchronize automatically. Before updating it, check for independent edits; synchronize deliberately and run the offline consistency test. A personal installation is separate from both repository copies.
- `README.md` is the public project catalog and onboarding entry point; `docs/` holds project and skill-specific designs, [platform evidence](platform-support.md), and [test details](test-status.md). `tests/` holds offline tests, including checks on maintained copies.
- A **skill** defines a user-facing task and workflow. An **Actor** is an underlying service a skill may use; an agent **platform** hosts or invokes a skill and supplies its own discovery, permissions, tools, and file capabilities. One project, skill, Actor, and platform are not interchangeable units.

## Adding a skill

First finish and review the independent new-user journey for the current skill. Propose the next skill's purpose, input and output scope, data sources, and acceptance criteria for approval before implementation. When implementation begins, add a complete, independently distributable `skills/<skill-name>/` unit with only the references and scripts it needs; do not create empty future-skill directories. Record its actual capabilities, tests, and platform evidence separately, then list it as available only when implemented. Update any maintained Codex discovery copy deliberately and extend appropriate offline checks.

Add `docs/shared/` only when multiple implemented skills actually share maintained material. Add host-specific guides only for workflows validated on that host; links to official setup guides alone do not demonstrate support. Platform support stages and evidence belong in the [matrix](platform-support.md), with detailed observations in [test status](test-status.md).

Transcript-based analysis is limited to the text actually obtained. Do not describe it as analysis of images, performance metrics, or audience response without adding and validating the relevant data sources. Scheduled monitoring is not a current feature; any future monitoring requires separate validation of discovery, scheduling, persistent state, and deduplication.

## Release maintenance

Review versioning and release records as skills evolve. The README installation example pins a tested commit and may not point to the latest skill; review and update the ref when releasing changes, after checking the associated installation evidence. Do not infer that a new ref or a different host has been verified from an earlier test.
