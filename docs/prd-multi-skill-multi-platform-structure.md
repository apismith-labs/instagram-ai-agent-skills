# PRD: Multi-Skill, Multi-Platform Project Structure

**Document status:** Draft for implementation and independent audit
**Project:** Instagram AI Agent Skills
**Version:** 1.0
**Date:** 2026-10-28
**Audience:** Codex implementing the repository changes; WorkBuddy auditing the result

## 1. Purpose

Reshape the repository so its public entry point represents the agreed product: one project containing multiple independent Instagram AI agent skills, with platform compatibility tracked separately for each host. The README must not present the first skill as the project's permanent or complete structure.

This PRD defines repository organization and user-facing project documentation. It does not authorize implementation of another skill, changes to the existing skill's behavior, new platform integrations, or claims that untested workflows work.

## 2. Product context

The repository currently contains one implemented skill, `instagram-transcript-extractor`. It accepts public Instagram video links and supports transcript retrieval, with optional summaries, translations, or analysis based on the returned text. The longer-term project is a set of focused skills that may use one or more Apify Actors each.

Potential future skills discussed so far include Instagram Reels Analyzer, Creator Analysis, Competitor Monitor, and comment analysis. These are roadmap candidates only. Their scope, data inputs, and implementation have not been approved as current features.

The first priority remains the independent user journey underway: a non-developer follows the public README, installs the skill, connects Apify, and obtains a transcript. Do not begin a second installable skill before that journey is reviewed.

## 3. Problem statement

The current README leads with the Transcript Extractor as if it were the project itself. The repository also lacks a concise, authoritative explanation of:

- how multiple skills are organized and owned;
- how skills differ from the platforms that host them;
- what evidence is required before describing a platform as supported;
- which capabilities are current, planned, or unverified.

This can cause contributors and users to mistake a repository layout, a published setup guide, or a test in one Codex interface for broad platform support.

## 4. Goals

1. Make the repository root README a project catalog and onboarding entry point.
2. Define each skill as an independently maintained and distributable unit under `skills/<skill-name>/`.
3. Track host/platform compatibility separately from the skill catalog.
4. Clearly distinguish Codex in the ChatGPT desktop app, Codex CLI, ChatGPT chat, and other agent platforms.
5. Record evidence by test stage so installation, discovery, explicit use, Apify connection, task completion, and end-to-end use are not conflated.
6. Preserve the current skill implementation, existing user-facing onboarding guidance, and all unrelated or uncommitted work.
7. Give future contributors a small, maintainable path for adding skills and platform-specific documentation.

## 5. Non-goals

This change must not:

- implement or scaffold another skill, such as Reels Analyzer or Competitor Monitor;
- change `SKILL.md`, helper scripts, workflow behavior, Actor inputs, or Apify calls;
- add a new platform integration or assert that a host supports the project;
- claim automatic skill selection, cross-session recovery, scheduled monitoring, or complete post-installation execution is validated;
- combine distinct prior tests into an end-to-end success claim;
- expose internal Actor parameters, credentials, private content, session IDs, or pricing estimates;
- submit, run, or retry an Apify Actor, create an Apify run, or inspect credentials;
- commit or push changes.

## 6. Users and use cases

### 6.1 New user

Can tell what the project is, which skill is available today, which platforms have evidence, and how to start without mistaking roadmap ideas for usable features.

### 6.2 Contributor

Can find the canonical skill source, understand the purpose of any Codex discovery copy, and know where to record platform and validation evidence.

### 6.3 Reviewer / auditor

Can compare README claims to the detailed validation record and determine whether evidence supports each claim without reconstructing unrelated test sessions as one journey.

## 7. Information architecture

The intended repository organization is:

```text
README.md                                      # Project catalog and onboarding
skills/<skill-name>/                           # Canonical independent skill source
  SKILL.md
  references/
  scripts/
.agents/skills/<skill-name>/                   # Codex project discovery copy, if maintained
docs/
  prd-multi-skill-multi-platform-structure.md  # This product and documentation requirement
  project-architecture.md                      # Repository responsibilities and extension rules
  platform-support.md                          # Host-by-host evidence matrix
  test-status.md                               # Detailed observed results and limitations
  <skill-name>-design.md                       # Per-skill design
  acceptance-test-plan.md                      # Acceptance scenarios
tests/                                         # Offline tests for code and maintained copies
```

Rules:

- Do not create empty directories for future skills. A skill appears in `skills/` only when implementation begins and its files exist.
- The repository root is a multi-skill project, not an installable skill by itself.
- `skills/<skill-name>/` is the canonical source. A Codex discovery copy is separate and must not be described as auto-synchronized unless tooling proves that.
- Add `docs/shared/` only when multiple implemented skills actually use shared maintained material.
- Add platform-specific how-to guides only when there is a validated workflow to document. A link to official instructions is not evidence that this project was tested there.
- The current public install example pins a commit. Do not silently change its ref as part of this structural work; document that maintainers must review pinned refs when releasing updates.

## 8. README requirements

The README must:

1. Introduce Instagram AI Agent Skills as a collection of independent skills.
2. Include a skill catalog. List `Instagram Transcript Extractor` as the first/current skill and summarize its actual scope. Mark future candidates as ideas, not available features.
3. Link to the existing skill source, test status, architecture, and platform matrix where those documents exist.
4. Preserve the existing installation request, Apify account/connection instructions, explicit-use example, sample prompts, and license unless a factual conflict requires a narrowly scoped correction.
5. State that Codex is the only host with reported tests so far, while avoiding an unsupported assertion that all Codex interfaces passed.
6. Explicitly distinguish Codex in the ChatGPT desktop app, Codex CLI, and ChatGPT chat. State that ChatGPT chat is a separate product and is not validated by Codex results.
7. Summarize important validation limits and link to `docs/test-status.md` for detail.
8. Keep ordinary-user prose free of internal Actor parameters and concrete prices or cost estimates.
9. Retain existing accurate installation caveats, including that the README natural-language installation request has not been tested verbatim.
10. Retain contributor guidance that the canonical skill source and Codex copy can diverge, and that a pinned install commit may not be the latest release.

The README is a concise public entry point. Detailed architecture and evidence definitions belong in the linked documents.

## 9. Platform support and evidence model

Create or update a platform matrix that contains separate rows for:

- Codex, where prior reports do not reliably record the exact interface;
- Codex in the ChatGPT desktop app;
- Codex CLI;
- ChatGPT chat product;
- other agent platforms (may be grouped until tested).

Track these stages independently for each host:

1. Skill installed/imported.
2. Skill discovered in a fresh session.
3. Skill explicitly used.
4. Natural-language automatic selection, if claimed.
5. Apify connection and authorization.
6. Complete task and checked user-visible result.
7. Optional file input/output.

Use explicit states such as `reported`, `observed`, `not tested`, or `not independently confirmed`, with a short evidence note. An official platform guide is a reference, not a test result. A report without its original trace must remain attributed and qualified. Do not combine tests from different sessions into one end-to-end result.

Known evidence that must remain distinct:

- Git-based installation of skill files;
- a separate new Codex session reportedly using a personal skill copy to prepare Actor input, without running an Actor;
- a separate project-level explicit-use report that prepared Actor input, without running an Actor;
- earlier single-item and batch Actor tests, reported separately;
- the README's natural-language installation request has not been tested verbatim;
- a complete journey from fresh README installation through Apify call remains unverified;
- ChatGPT chat installation, connection, and full workflow remain unverified.

If the current `docs/test-status.md` provides more precise evidence or qualifies any of the above, preserve its exact boundaries rather than flattening them.

## 10. Architecture document requirements

Create or update `docs/project-architecture.md` to explain:

- the multi-skill product shape and independent skill units;
- the separation between user-facing skills, underlying Actors, and host platforms;
- canonical source versus Codex discovery copy;
- when to create shared references or platform guides;
- the sequence and entry criteria for adding a future skill;
- that periodic monitoring requires separate validation of discovery, scheduling, persistent state, and deduplication;
- release/versioning guidance for pinned installation examples.

Future ideas must remain clearly labeled as unapproved or not implemented. Transcript-based analysis must not imply visual analysis, performance metrics, or audience response unless those data sources are actually added and validated.

## 11. Constraints and implementation guardrails

- First inspect `git status`, staged changes, and the full working diff. Preserve all pre-existing changes and do not overwrite unrelated work.
- If unexpected files or modifications are present, do not include them in this task; report them.
- Keep this a documentation and repository-organization change. Do not edit skill functionality or scripts.
- Do not call Apify, an Actor, or an Apify MCP tool. Do not create runs or inspect credentials.
- Do not make changes to the existing installation command/ref except for an independently verified factual error; report such a finding before broadening scope.
- Do not commit or push.
- Use the repository's existing language conventions: public README remains English; detailed project PRD/design docs may be Chinese or English, but each document must be internally consistent.

## 12. Acceptance criteria

The work is acceptable when all of the following are true:

1. The README presents a multi-skill project and a catalog rather than centering its identity on only the first skill.
2. Exactly the implemented skill is presented as available; future candidates are visibly labeled ideas.
3. README claims about platform support agree with the platform matrix and test-status record.
4. Codex desktop app, Codex CLI, and ChatGPT chat are not conflated.
5. The platform matrix separates installation, discovery/use, authorization, task completion, and full-journey evidence.
6. Historical installation, explicit-use, and Actor tests remain distinct; no unrelated-session evidence is promoted to end-to-end validation.
7. The README natural-language installation request remains labeled unverified unless a verbatim test is independently performed and recorded in this task.
8. The repository architecture and contribution rules are documented, including canonical skill source versus Codex discovery copy.
9. No new skill implementation, platform integration, Actor behavior, or credential handling is introduced.
10. All local Markdown links added or changed resolve within the repository; `git diff --check` passes.
11. Existing unrelated modifications are preserved and excluded from this change.
12. No Actor runs, credential access, commit, or push occurred.

## 13. WorkBuddy audit checklist

WorkBuddy should independently inspect the actual Git state and diff, then verify:

- scope stayed within README and project documentation (plus only necessary documentation indexes);
- no pre-existing changes were overwritten or included accidentally;
- actual catalog and roadmap claims are accurate;
- platform names and validation status are consistent across README, platform matrix, test status, and architecture;
- evidence limitations and separate test histories remain intact;
- the pinned installation example and its unverified conversational request were not misrepresented;
- no internal Actor parameter, credential, pricing estimate, or unsupported capability claim was added to user-facing copy;
- local links and `git diff --check` pass;
- no skill code, Actor, Apify tool, credential, commit, or push was touched.

The audit report should list commands run, results, actual modified files, any discrepancy with this PRD, and residual unverified items. If a substantive evidence or installation-accuracy issue is found, report it rather than silently widening implementation scope.

## 14. Out of scope after this PRD

The following require a separate approved requirement and validation plan: implementing the next skill; adding new host integrations; changing Apify Actor behavior; introducing scheduled/continuous monitoring; changing supported input/output formats; or publishing a release.
