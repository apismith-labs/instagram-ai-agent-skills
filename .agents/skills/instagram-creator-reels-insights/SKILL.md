---
name: instagram-creator-reels-insights
description: Review recent public Instagram Reels from one or more creators. Get daily or weekly insights with source links, based on available transcripts.
---

# Instagram Creator Reels Insights

Turn recent public Instagram Reels from one or more creators into a source-linked report. Name the public accounts, choose Daily Scan or Weekly Review, and the Skill finds recent posts, transcribes the videos it can, and summarizes what was actually said, with a link to every source post.

## What you get

- **Daily Scan** reviews the most recent 24 hours for each creator you name.
- **Weekly Review** reviews the most recent 7 days and highlights recurring topics, hooks, and calls to action.

Every report keeps each creator in a separate section, ties findings to source posts, and separates transcript evidence from interpretation. Cross-creator comparisons appear only when the available transcripts support them.

## Copy-ready requests

Replace the placeholders with public accounts and your own brand.

**Daily Scan**

```text
Run a Daily Scan for [CREATOR_1], [CREATOR_2], and [CREATOR_3]. Review their recent public Reels from the last 24 hours. Give each creator a separate section with links to source posts and transcript-based observations.
```

**Weekly Review**

```text
Run a Weekly Review for [CREATOR_1], [CREATOR_2], and [CREATOR_3] for the last 7 days. Summarize each creator separately, then compare themes only where the available transcripts support a comparison. Link each finding to its source post.
```

**Content ideas**

```text
Based on the available transcripts from [CREATOR_1], [CREATOR_2], and [CREATOR_3], suggest content angles for [MY_BRAND]. Link observations to source posts and distinguish transcript-supported observations from your suggestions.
```

## Before you start

- **Connect Apify in your host.** The Skill uses Apify Actors to read public posts and transcripts. Installing the Skill and connecting Apify are separate steps, and both are needed. If Apify is not connected, the Skill stops and points you to your host's connection settings.
- **Set a per-creator video limit.** It caps how many eligible videos are processed for transcripts in each report. It is a processing limit, not a full-account scan, and it does not cap usage or cost.
- **Check your Apify usage.** More creators or more videos can mean more usage on your own Apify account. Review current usage in the Apify Console; the Skill does not estimate a price or promise a fee cap.
- **Never paste credentials.** Do not share Instagram passwords, API tokens, cookies, or session values in chat. The Skill reads public accounts only.

For installation steps and more prompt examples, see the [project README](https://github.com/apismith-labs/instagram-ai-agent-skills#instagram-creator-reels-insights).

## What the results mean

A report covers the posts and transcripts that run actually found and returned. Coverage can be partial or unknown, and the report states which. A creator with no returned post is not proof that the creator posted nothing, and an empty result is not evidence that the period had no new Reels. Missing metrics are never treated as zero.

## Scope

- Daily Scan and Weekly Review for user-specified public accounts only. Do not offer a single-URL analysis task or a posts-only report.
- Do not schedule runs, monitor in the background, or claim to remember accounts or transcripts across sessions.
- Process only public accounts. Do not bypass login, rate limits, or platform restrictions, and never ask for or reveal tokens, cookies, session IDs, passwords, or authorization headers.

## How this Skill runs

Before each report, read [the workflow contract](references/workflow.md). Use the bundled offline helper at `scripts/workflow.py` for settings validation, UTC window construction, candidate selection and coverage status, batch splitting, and transcript reconciliation. Invoke it with `python3 <skill-directory>/scripts/workflow.py` and one JSON object on stdin; consume its JSON result and treat any nonzero exit or `error` as a stop condition. The helper makes no network calls and stores no settings. If the host cannot safely execute it or provide private in-memory inputs, explain that limitation without starting Actor calls.

### First use and saved settings

The first setup confirms only: (1) the public accounts to monitor, (2) the maximum number of videos per creator to include in each report, and (3) whether the user agrees to save the account list and setting. Do not ask for a report budget or per-run cost setting. Save only if the host supports user-authorized persistence. Otherwise provide a reusable request containing the accounts and per-creator video limit. Routine runs reuse available settings and do not repeat setup.

The per-creator limit applies after candidate discovery: it selects how many eligible returned videos are sent for transcript processing and analysis. It is not an Actor retrieval limit, does not limit discovery reads, does not guarantee complete account coverage, and does not cap usage or cost. If an older saved settings object contains `report_budget_usd`, ignore that field; it is not a current setting and must not affect planning or Actor calls.

Use plain language. Do not expose schema fields or require users to configure Actor runs. If Apify is not connected, stop relevant calls and direct the user to the current host's connection settings. Never ask them to paste a token, cookie, password, session ID, or authorization value into chat.

Be transparent that Profile Posts discovery and Transcript processing may involve multiple Actor runs and may generate Apify usage according to the user's account and each Actor's current rules. Do not conceal calls, estimate a fixed fee, promise a fee cap, or repeatedly ask about a budget. Users can review actual usage in Apify Console. Follow approvals required by the host.

### Request and modes

- Accept public Instagram usernames or profile URLs, a report mode, and optional timezone/report language.
- If mode is omitted, use Daily Scan: the rolling 24 hours before the request. Weekly Review uses the rolling 7 days. Resolve explicit calendar periods in the user's timezone and show the exact UTC boundaries and displayed timezone.
- Explain briefly that the report discovers recent posts, transcribes eligible videos, and analyzes their spoken content.
- Normalize supplied account names/profile URLs conservatively. Keep each requested account mapped to its normalized identity. Reject ambiguous or unsupported input; never broaden to other accounts.

### Execution

1. Check the tools actually exposed by the selected host, their live schemas, authorization, pagination/completeness signals, and current Actor input/output contracts for `apple_yang/instagram-post-scraper` and `apple_yang/instagram-transcripts-scraper`. Tool names and argument shapes vary by host; do not assume every host exposes `call-actor` or the same contract. Do not use unverified field aliases. Give the helper exact field maps from the contracts currently available to the host. If an Actor/tool is unavailable, authorization is missing, required output fields or media values cannot be verified, or results cannot be reliably read, stop the affected calls and explain that interface/access blocker. These conditions do not create a budget-parameter requirement.
2. Run the helper `settings` operation using the accounts, positive integer per-creator video limit, and save consent. For Daily/Weekly boundaries, call `window` with the request timestamp and mode. Keep its `end_utc_exclusive` value through selection.
3. Use the host's live-supported input to discover posts for the requested accounts and time window. Preserve each run boundary, submitted account mapping, run status, all returned rows, and any explicit completeness evidence exposed by the host. Set `retrieval_complete` to `true` only when the caller has traceable, real host/Actor evidence establishing Dataset completeness. The helper checks only that the evidence is an object with non-empty string `source` and `detail`; it cannot authenticate the source or prove the description is true. The current Apify plugin has not provided this Skill with a verified completeness signal, so do not set `true` from `SUCCEEDED`, a result count below `resultsLimit`, an empty result, or not seeing a truncation marker. Otherwise leave completeness unknown/conservative. Profile Posts `resultsLimit`, where required by its live input schema, is an Actor retrieval parameter; never set it equal to the user's per-creator processing limit unless live evidence verifies that equivalence. Use a retrieval strategy based on the current schema and independently verified Actor behavior. If completeness is unknown, preserve validated candidates but report coverage as unknown; do not claim a complete scan or reliable zero new videos.
4. Run helper operation `select` with the exact verified Profile Posts field map and every per-run result. It checks raw run row counts before local window filtering, filters by returned account identity, URL, timestamp and verified media values, deduplicates candidates, and selects at most the user's per-creator limit from eligible returned videos. Keep unresolved identity or interface rows with reasons; unknown media rows retain the actual unverified type value, so do not assume every unresolved category has a `reason` field. Valid, attributable video rows returned by a FAILED, ABORTED, TIMED-OUT, or otherwise incomplete discovery run may still proceed to transcription; keep the source creator and report marked partial, or unknown when the run status itself is unknown. If run-to-creator metadata is missing, only independently verifiable rows that match a requested creator may continue; preserve the run source and keep coverage unknown. Do not send rows with unresolved identity or invalid required fields. A missing discovery run for a requested creator means that creator's coverage and additional candidates are unknown. Report per creator returned candidates, selected/processed videos, videos omitted by the user's limit, failures, and unknown/partial discovery coverage. Never describe the local processing cap as a discovery cap or complete account scan.
5. Build Transcript batches only from selected, deduplicated URLs and only within a batch size supported by the current Transcript schema/account. Split internally when supported. Use the host's currently exposed tool and live argument schema; do not require `callOptions`, `maxTotalChargeUsd`, `maxItems`, or run-options readback. Do not hide these calls. Do not automatically retry, create replacement runs, expand the user's request, or interrupt discovery/transcription merely to ask about a budget. If a functional interface, authorization, batch, or read failure prevents remaining work, retain usable results and mark affected videos/account coverage partial.
6. Pass the complete submitted-candidate set and every returned transcript row to helper operation `reconcile`. It canonicalizes verified Instagram URL variants, uses only verified URL/code/pk fields, supports verified stable-ID fallback, and returns a status for every submitted post even when no row returned. It distinguishes explicit empty text, missing text, malformed rows, segment-only results, Actor errors, duplicate rows, identity conflicts, unmatched rows, and run/Dataset pending states. Never match by row order.
7. If the host exposes Dataset pagination and a reliable completion signal, read all pages and preserve that signal as completeness evidence. If the host does not expose it, do not claim discovery completeness. A `reconcile` success means a returned transcript row matched its submitted post; it does not establish that discovery or transcript Dataset reading was complete. Incomplete or unknown discovery runs may still supply validated candidate rows for transcription as described above, but their creator and report coverage stays partial/unknown. If a transcript run or Dataset is incomplete, preserve affected transcript results as pending/provisional. Preserve confidently matched partial results.

### Analysis and report

Analyze only Actor-returned transcript text. Keep that text distinct from generated summaries and analysis. Do not infer visuals, editing, product display, creator intent, audience reaction, or causation. Link each insight to its post URL and quote a short supporting transcript excerpt where useful.

**Daily Scan:** show the exact window and timezone. For each creator show returned candidates, selected/processed videos, those omitted by the user limit, and coverage/failure status. For each selected video show its URL, publish time, transcript status and, when available, transcript highlights, opening Hook, core point, speaking structure, delivery and closing/CTA. Give a concise interpretation based on transcript evidence. Preserve post details when transcription fails.

**Weekly Review:** show the same coverage accounting. Summarize recurring topics, Hooks, speaking structures and CTAs only from successfully matched transcripts in this report. Link every pattern to representative posts and transcript evidence. Call out small samples and incomplete coverage; do not describe them as long-term trends.

Keep the default report readable: show transcript highlights and source-linked analysis rather than every full transcript inline. If asked to expand a video, provide its actual returned transcript separately, link its post, and label the transcript as Actor-returned text.

Never treat missing metrics as zero. Engagement counts, if returned, are optional collection-time context only; they must not replace or lead the report.

At the end, include a short copyable request containing the accounts, report mode, exact time range and per-creator limit. Do not imply that the Skill will remember settings or prior transcripts in another session.

### Privacy and safety

Process only user-specified public accounts. Respect Instagram, Apify and host access controls; do not bypass login, rate limits, or restrictions. Never request or reveal tokens, cookies, session IDs, passwords, or authorization headers. Persist the account list and per-creator limit only after explicit consent and only through supported host storage. Never persist transcript libraries or report history.
