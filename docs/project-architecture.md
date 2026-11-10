# Project architecture

**阶段状态（2026-11-10）：** 第三个 Skill `Instagram Media Links & Post Insights` 已进入实现阶段，详见[专属 PRD](instagram-media-links-and-post-insights-prd.md)。运行时验证与独立验收仍待完成；在完成前，不可标为已验证、可发布或已发布。本架构快照中其他历史状态按其记录日期理解。

Instagram AI Agent Skills is one project containing independently maintained skills. The repository root is the project catalog and onboarding entry point; it is not itself an installable skill. Instagram Transcript Extractor is the first implemented and separately validated skill. At the time this architecture snapshot was written (2026-11-06), Instagram Creator Reels Insights was described as in development and not validated or publishable. See the [project README](../README.md) for its current distribution status. Its offline helper validates account and per-creator video-count settings, constructs time windows, selects candidates and coverage states, splits transcript batches, and reconciles results. It has no report-budget planner or run-option readback logic. Profile Posts public output field names/types are documented, while media type values, result semantics/order, and completeness remain unverified. Other Reels analysis, competitor research, and comment-analysis ideas remain unimplemented.

Host-specific observations, including dated Codex live tool inventories and their limits, belong in [interface verification](interface-verification.md); a missing tool in one session does not characterize every Codex setup or local plugin/cache configuration.

The [multi-skill, multi-platform PRD](prd-multi-skill-multi-platform-structure.md) describes the requirements for this structure.

## Responsibilities

- `skills/<skill-name>/` is the canonical distribution and maintenance source for each implemented skill, including its `SKILL.md` and any needed references and scripts. The current source is [Instagram Transcript Extractor](../skills/instagram-transcript-extractor/).
- At the time this architecture snapshot was written (2026-11-06), the [Instagram Creator Reels Insights source](../skills/instagram-creator-reels-insights/) was described as in development and unsupported; see the [project README](../README.md) for its current distribution status. Implementation and validation observations are recorded in [interface verification](interface-verification.md) and [test status](test-status.md).
- `.agents/skills/<skill-name>/`, when maintained, is a separate Codex project discovery copy. It does not synchronize automatically. Before updating it, check for independent edits; synchronize deliberately and run the offline consistency test. A personal installation is separate from both repository copies.
- `README.md` is the public project catalog and onboarding entry point. `docs/README.md` routes users to platform setup and skill guides; `docs/platforms/` contains separate host setup guides, and `docs/skills/` contains user guides for implemented skills. Project and skill design documents, the [platform evidence matrix](platform-support.md), and [test details](test-status.md) remain separate from these user instructions. `tests/` holds offline tests, including checks on maintained copies.
- A **skill** defines a user-facing task and workflow. An **Actor** is an underlying service a skill may use; an agent **platform** hosts or invokes a skill and supplies its own discovery, permissions, tools, and file capabilities. One project, skill, Actor, and platform are not interchangeable units.

## Adding a skill

For every skill, add a complete, independently distributable `skills/<skill-name>/` unit with only the references and scripts it needs; do not create empty future-skill directories. A directory or Codex discovery mirror does not make a skill available: record implementation, interface blockers, tests, and platform evidence separately, and list it as available only after required integration and validation gates pass. Update maintained Codex discovery copies deliberately and keep mirror tests discovery-based so new canonical skills cannot be omitted silently.

Add `docs/shared/` only when multiple implemented skills actually share maintained material. Platform guides may explain host-specific setup using current official instructions, but must identify when the project's own workflow is unverified; publishing a guide or linking official instructions does not demonstrate project support. Platform support stages and evidence belong in the [matrix](platform-support.md), with detailed observations in [test status](test-status.md).

Transcript-based analysis is limited to the text actually obtained. Do not describe it as analysis of images, performance metrics, or audience response without adding and validating the relevant data sources. Scheduled monitoring is not a current feature; any future monitoring requires separate validation of discovery, scheduling, persistent state, and deduplication.

## Release maintenance

Review versioning and release records as skills evolve. `scripts/package_release.py` builds a skill ZIP from its canonical `SKILL.md`, `references/workflow.md`, `scripts/workflow.py`, `agents/openai.yaml`, slug-named icon, and the root `LICENSE`. It supports the first skill by default and accepts `--skill <slug>` for a different canonical skill. Packaging checks exclude bytecode/cache files and do not establish runtime support. The Codex installation example in `docs/platforms/codex.md` pins `v0.1.0`; review the pinned ref when preparing a newer release. Do not infer that a new ref or a different host has been verified from an earlier test.
