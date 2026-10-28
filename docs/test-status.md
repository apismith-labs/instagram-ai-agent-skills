# Test status

This record distinguishes observed results from earlier reports. It contains no transcript, credentials, run identifiers, or personal paths.

For host-by-host stages and interface-specific evidence, see the [platform support matrix](platform-support.md). Evidence from separate tests must not be combined into a single end-to-end result.

## GitHub installation

- The Git method of the skill installer installed the complete skill into an isolated directory with a specified commit as its ref. The installed files matched the corresponding locally available Git commit's source directory byte for byte; the installer did not independently print the checked-out SHA. This verified file installation, not personal discovery or use.
- In the latest personal installation test, the Git method installed the skill from the public GitHub repository into the personal `.agents/skills` directory. `SKILL.md`, `references/workflow.md`, and `scripts/workflow.py` matched the target commit's locally available source files byte for byte. The installer was given the commit as its ref but did not print the checked-out SHA independently; its default download method was not tested in this attempt.
- The README's natural-language installation request has not been tested verbatim. The existing personal destination was already occupied when this was reviewed and was not changed. An earlier isolated Codex session could not initialize, so an isolated file installation is not evidence that this exact request works in a new session or real personal environment. The installer's default destination differs from the explicitly selected personal `.agents/skills` directory.
- A new Codex session was attempted outside the repository using `codex exec --ephemeral --ignore-user-config --skip-git-repo-check --sandbox read-only`. Initialization failed with `failed to initialize in-process app-server client: Operation not permitted`; the session also reported that its state database could not be opened. No discovery, explicit-use, or input-preparation event was observed in that session. The installed personal files remain in place.

## Personal-level explicit use

- The product owner provided a report of a separate new Codex session outside the repository. Following an explicit request to use `$instagram-transcript-extractor`, Codex reported reading the personal installation's `SKILL.md` and `references/workflow.md` and executing its `scripts/workflow.py`. Its `prepare` operation successfully produced Actor input. The session did not call an Actor, Apify MCP, or other network tools, and did not create a run. The original session trace was not independently reviewed for this update.
- This reported explicit-use test, the personal file installation, and the earlier Actor tests are distinct observations. Together they do not establish a complete post-installation Apify end-to-end test.

## Project-level discovery and use

- An earlier test report says a new Codex session in a temporary project outside the repository explicitly used `$instagram-transcript-extractor`, read the temporary project's `.agents/skills/instagram-transcript-extractor/SKILL.md` and `references/workflow.md`, and ran `scripts/workflow.py` to prepare Actor input. It did not call an Actor or Apify MCP and did not create a run. This was a project-level discovery and explicit-use test, separate from the GitHub installation tests. Its session trace was not independently reviewed in this update.
- A native Codex discovery interface previously recognized the project-level skill, and Codex reported explicit-use and natural-language request tests. Discovery, explicit use, automatic selection, and manually reading a workflow are different observations. The latest single-item end-to-end session has no independent host activation record, so automatic selection in that session cannot be confirmed.

## Previous Actor tests

- Earlier reports say that single and batch Actor and dataset processing succeeded after manually loading the project workflow. The details of the earlier batch inputs, count, and individual results were not independently checked in this update. These were separate from the latest single-item session.
- In that later single-item session, a first `call_actor` request was rejected by argument validation because it supplied `actorName` instead of the required `actor`. A subsequent request confirmed one successful run and returned nonempty transcript text. The validation error returned no run identifier, but alone cannot prove that no additional run was created. The reported input included `enhancedcrawl: true`; whether enhanced processing actually occurred inside the Actor was not verified.
- That session read the workflow reference and ran the preparation helper. Its trace did not record `next_action` or `reconcile`, so their execution is unconfirmed and the session does not establish that every workflow step was followed.

## Still unverified

Automatic selection from a natural-language request; the complete new-user journey from README installation through Apify connection to a transcript; ChatGPT chat installation, connection, and full use; cross-session recovery; real multi-page dataset reads; and host file upload and result export remain unverified. Simulated tests do not establish these platform behaviors.
