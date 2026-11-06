#!/usr/bin/env python3
"""Deterministic offline planning and reconciliation; no network or persistence."""
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation, ROUND_CEILING
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

class ContractError(ValueError):
    pass

TRACKING = {"igsh", "igshid", "fbclid", "gclid"}

def money_cents(value, name, allow_zero=False):
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ContractError(f"{name} must be a USD amount with at most two decimal places")
    try:
        amount = Decimal(str(value))
    except InvalidOperation:
        raise ContractError(f"{name} is not a valid USD amount")
    if not amount.is_finite() or amount < 0 or (amount == 0 and not allow_zero):
        raise ContractError(f"{name} must be finite and greater than zero")
    if amount.as_tuple().exponent < -2:
        raise ContractError(f"{name} supports at most two decimal places")
    return int(amount * 100)

def usd_decimal(value, name, allow_zero=False):
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ContractError(f"{name} must be a USD amount")
    try:
        amount = Decimal(str(value))
    except InvalidOperation:
        raise ContractError(f"{name} is not a valid USD amount")
    if not amount.is_finite() or amount < 0 or (amount == 0 and not allow_zero):
        raise ContractError(f"{name} must be finite and {'non-negative' if allow_zero else 'greater than zero'}")
    if amount.as_tuple().exponent < -9:
        raise ContractError(f"{name} supports at most nine decimal places")
    return amount

def validate_settings(settings):
    if not isinstance(settings, dict):
        raise ContractError("settings must be an object")
    cents = money_cents(settings.get("report_budget_usd"), "report_budget_usd")
    cap = settings.get("per_creator_limit")
    if type(cap) is not int or cap <= 0:
        raise ContractError("per_creator_limit must be a positive integer")
    accounts = settings.get("accounts")
    if not isinstance(accounts, list) or not accounts:
        raise ContractError("accounts must be a non-empty list")
    normalized = []
    for raw in accounts:
        if not isinstance(raw, str):
            raise ContractError("account entries must be strings")
        value = raw.strip()
        if value.startswith("@"):
            value = value[1:]
        if "://" in value:
            try:
                u = urlsplit(value)
                if (u.scheme != "https" or u.hostname not in ("instagram.com", "www.instagram.com")
                        or u.query or u.fragment or not re.fullmatch(r"/[A-Za-z0-9._]{1,30}/?", u.path)):
                    raise ValueError
                value = u.path.strip("/")
            except ValueError:
                raise ContractError("unsupported or ambiguous Instagram profile URL")
        if not re.fullmatch(r"[A-Za-z0-9._]{1,30}", value) or value in {".", ".."}:
            raise ContractError("invalid Instagram username")
        normalized.append(value.lower())
    if len(set(normalized)) != len(normalized):
        raise ContractError("duplicate accounts after normalization")
    return {"report_budget_cents": cents, "report_budget_usd": f"{Decimal(cents)/100:.2f}", "per_creator_limit": cap, "accounts": normalized,
            "save_consent": settings.get("save_consent") is True}

def parse_time(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        try:
            seconds = value / 1000 if value > 100_000_000_000 else value
            return datetime.fromtimestamp(seconds, tz=timezone.utc)
        except (OverflowError, OSError, ValueError):
            return None
    if not isinstance(value, str):
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc) if dt.tzinfo else None
    except ValueError:
        return None

def window(now, mode):
    end = parse_time(now)
    if end is None or mode not in ("daily", "weekly"):
        raise ContractError("now must be timezone-aware ISO-8601 and mode daily or weekly")
    start = end - (timedelta(hours=24) if mode == "daily" else timedelta(days=7))
    return {"start_utc": start.isoformat().replace("+00:00", "Z"),
            "end_utc_exclusive": end.isoformat().replace("+00:00", "Z")}

def canonical_post_url(value):
    if not isinstance(value, str):
        return None
    try:
        u = urlsplit(value.strip())
        if u.scheme.lower() not in ("https", "http") or u.hostname not in ("instagram.com", "www.instagram.com", "m.instagram.com"):
            return None
        if u.username or u.password or u.port not in (None, 80, 443):
            return None
        match = re.fullmatch(r"/(p|reel|reels|tv)/([A-Za-z0-9_-]+)/?", u.path)
        if not match:
            return None
        query = []
        for key, val in parse_qsl(u.query, keep_blank_values=True):
            low = key.lower()
            if low in TRACKING or low.startswith("utm_"):
                continue
            query.append((key, val))
        query.sort()
        kind = "reel" if match.group(1) in ("reel", "reels") else match.group(1)
        return urlunsplit(("https", "www.instagram.com", f"/{kind}/{match.group(2)}/",
                           urlencode(query), ""))
    except ValueError:
        return None

def require_post_contract(contract):
    keys = ("creator", "url", "timestamp", "type", "id")
    if not isinstance(contract, dict) or any(not isinstance(contract.get(k), str) or not contract[k] for k in keys):
        raise ContractError("interface_error: exact Profile Posts output field contract is missing")
    if not isinstance(contract.get("video_values"), list) or not contract["video_values"]:
        raise ContractError("interface_error: verified video type values are missing")
    if not isinstance(contract.get("non_video_values"), list):
        raise ContractError("interface_error: verified non-video type values are missing")
    if any(not isinstance(value, str) or not value for value in contract["video_values"] + contract["non_video_values"]):
        raise ContractError("interface_error: media type values must be verified non-empty strings")
    if {value.casefold() for value in contract["video_values"]} & {value.casefold() for value in contract["non_video_values"]}:
        raise ContractError("interface_error: video and non-video type values overlap")
    if contract.get("id_kind") not in {"code", "pk"}:
        raise ContractError("interface_error: verified stable ID kind must be code or pk")

def _selection_metadata_error(accounts, code, missing, detail):
    counts = {}
    for account in accounts if isinstance(accounts, list) else []:
        if isinstance(account, str) and account:
            counts[account.lower()] = {"discovered_returned_in_window": 0, "selected": 0,
                "returned_raw_rows": 0, "omitted_by_cap_observed": 0,
                "coverage_status": "unknown", "additional_candidates_unknown": True,
                "possible_results_limit_reached": None, "results_limit_scope_unknown": True,
                "run_coverage": [], "out_of_window": 0, "non_video": 0,
                "unknown_media_type": 0, "missing_timestamp": 0,
                "multi_username_run_observed": False,
                "results_limit_per_creator_unattributed": False,
                "row_issue_count": 0}
    return {"status": "partial_interface_error", "coverage_status": "unknown", "selected": [],
            "counts": counts, "unresolved": [], "run_coverage": [],
            "interface_errors": [{"code": code, "missing": missing, "detail": detail}],
            "row_interface_error_count": 0, "possible_results_limit_reached": None}

def select_posts(runs, accounts, cap, start, end, contract):
    """Select posts from per-run bundles; limit checks always use pre-filter run rows."""
    require_post_contract(contract)
    if not isinstance(accounts, list) or any(not isinstance(a, str) or not a for a in accounts):
        raise ContractError("accounts must be an array of non-empty usernames")
    if not isinstance(runs, list) or not runs:
        return _selection_metadata_error(accounts, "missing_run_boundary", ["runs"],
                                         "Per-run posts, usernames, and resultsLimit metadata are required")
    if type(cap) is not int or cap <= 0:
        raise ContractError("per_creator_limit must be a positive integer")
    wanted = {a.lower() for a in accounts}
    lo, hi = parse_time(start), parse_time(end)
    if lo is None or hi is None or hi <= lo:
        raise ContractError("invalid half-open report window")
    by_creator = {a: [] for a in wanted}
    unresolved, seen, seen_ids = [], {}, {}
    row_error_count = 0
    identity_conflict_count = 0
    unattributed_issue_count = 0
    classifications = {a: {"out_of_window": 0, "non_video": 0, "unknown_media_type": 0,
                           "missing_timestamp": 0, "returned_raw_rows": 0,
                           "additional_candidates_unknown": False, "run_coverage": [],
                           "multi_username_run_observed": False,
                           "results_limit_per_creator_unattributed": False,
                           "row_issue_count": 0}
                       for a in wanted}
    normalized_runs, missing_run_fields, used_run_ids, run_failures = [], [], set(), []
    for index, bundle in enumerate(runs):
        if not isinstance(bundle, dict):
            missing_run_fields.append({"run_index": index, "missing": ["run_id", "usernames", "results_limit", "posts", "retrieval_complete"]})
            continue
        required_run_fields = ("run_id", "usernames", "results_limit", "posts", "retrieval_complete")
        missing = [field for field in required_run_fields if field not in bundle]
        if missing:
            missing_run_fields.append({"run_index": index, "missing": missing})
            continue
        run_id, usernames = bundle["run_id"], bundle["usernames"]
        limit, raw_posts, retrieval_complete = bundle["results_limit"], bundle["posts"], bundle["retrieval_complete"]
        if (not isinstance(run_id, str) or not run_id or run_id in used_run_ids
                or not isinstance(usernames, list) or not usernames
                or any(not isinstance(name, str) or not name for name in usernames)
                or type(limit) is not int or limit <= 0 or not isinstance(raw_posts, list)
                or type(retrieval_complete) is not bool):
            missing_run_fields.append({"run_index": index, "missing": ["valid unique run_id, usernames, positive results_limit, posts array, or retrieval_complete"]})
            continue
        mapped = {name.lower() for name in usernames}
        if not mapped.issubset(wanted):
            missing_run_fields.append({"run_index": index, "missing": ["requested-account mapping"],
                                        "unexpected_usernames": sorted(mapped - wanted)})
            continue
        used_run_ids.add(run_id)
        raw_status = bundle.get("run_status")
        normalized_status = raw_status.upper().replace("_", "-") if isinstance(raw_status, str) else None
        known_statuses = {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT", "READY", "RUNNING", "ABORTING", "TIMING-OUT"}
        status_known = normalized_status in known_statuses
        run_succeeded = normalized_status == "SUCCEEDED" and retrieval_complete
        run_failed = normalized_status in {"FAILED", "ABORTED", "TIMED-OUT"}
        run_status_unknown = not status_known
        scope_verified = (bundle.get("results_limit_scope") == "run_total"
                          and bundle.get("results_limit_scope_verified") is True)
        multi_scope_unknown = len(mapped) > 1 and not scope_verified
        reached = len(raw_posts) >= limit
        if run_failed:
            coverage = "run_failed"
        elif run_status_unknown:
            coverage = "run_status_unknown"
        elif not run_succeeded:
            coverage = "run_incomplete"
        elif multi_scope_unknown:
            coverage = "possible_results_limit_reached_scope_unknown" if reached else "unknown_multi_username_limit_scope"
        elif reached:
            coverage = "possible_results_limit_reached"
        elif not retrieval_complete:
            coverage = "retrieval_incomplete"
        else:
            coverage = "returned_below_run_limit"
        run_record = {"run_id": run_id, "usernames": sorted(mapped), "results_limit": limit,
                      "raw_returned_rows": len(raw_posts), "possible_results_limit_reached": reached,
                      "coverage_status": coverage, "retrieval_complete": retrieval_complete,
                      "limit_scope_unknown": multi_scope_unknown, "run_status": normalized_status,
                      "status_message": bundle.get("status_message"),
                      "error": bundle.get("run_error")}
        normalized_runs.append((run_record, mapped, raw_posts))
        if not run_succeeded:
            run_failures.append({"run_id": run_id, "usernames": sorted(mapped),
                                 "run_status": normalized_status or "MISSING_OR_UNKNOWN",
                                 "error": bundle.get("run_error"),
                                 "status_message": bundle.get("status_message"),
                                 "coverage_status": coverage})
        for creator in mapped:
            classifications[creator]["run_coverage"].append({"run_id": run_id, "status": coverage})
            if len(mapped) > 1:
                classifications[creator]["multi_username_run_observed"] = True
                classifications[creator]["results_limit_per_creator_unattributed"] = True
                classifications[creator]["possible_results_limit_reached"] = None
            if multi_scope_unknown:
                classifications[creator]["results_limit_scope_unknown"] = True
                classifications[creator]["possible_results_limit_reached"] = None
                classifications[creator]["additional_candidates_unknown"] = True
            else:
                classifications[creator].setdefault("results_limit_scope_unknown", False)
                classifications[creator].setdefault("possible_results_limit_reached", False)
                if len(mapped) == 1 and not classifications[creator]["multi_username_run_observed"]:
                    classifications[creator]["possible_results_limit_reached"] = (
                        classifications[creator]["possible_results_limit_reached"] or reached)
            classifications[creator]["additional_candidates_unknown"] = (
                    classifications[creator]["additional_candidates_unknown"] or reached or not run_succeeded)
    missing_creators = sorted(wanted - {creator for _, mapped, _ in normalized_runs for creator in mapped})
    if missing_creators:
        missing_run_fields.append({"missing": ["run-to-creator mapping"], "usernames": missing_creators})
        for creator in missing_creators:
            classifications[creator]["additional_candidates_unknown"] = True
            classifications[creator]["results_limit_scope_unknown"] = True
            classifications[creator]["possible_results_limit_reached"] = None
    if missing_run_fields:
        result = _selection_metadata_error(accounts, "invalid_or_missing_run_metadata", missing_run_fields,
                                           "Cannot determine run-local resultsLimit coverage or creator mapping")
        # Malformed envelopes cannot safely establish a candidate set. Retain
        # any valid run rows only when their run boundary and author map exist.
        result["run_coverage"] = [record for record, _, _ in normalized_runs]
        if not normalized_runs:
            return result
        # Continue processing identifiable bundles, while preserving the
        # missing-run metadata error and forcing unknown aggregate coverage.

    video_values = {value.casefold() for value in contract["video_values"]}
    non_video_values = {value.casefold() for value in contract["non_video_values"]}
    required = [contract[k] for k in ("creator", "url", "timestamp", "type", "id")]
    raw_index = 0
    for run_record, run_usernames, raw_posts in normalized_runs:
        for row in raw_posts:
            if not isinstance(row, dict) or any(key not in row for key in required):
                raise ContractError(f"interface_error: Profile Posts row {raw_index} lacks a required contracted field")
            creator = row[contract["creator"]]
            url = row[contract["url"]]
            stamp = parse_time(row[contract["timestamp"]])
            kind = row[contract["type"]]
            stable_id = row[contract["id"]]
            if not isinstance(creator, str) or not isinstance(url, str) or not isinstance(kind, str):
                raise ContractError(f"interface_error: Profile Posts row {raw_index} has invalid contracted field types")
            creator = creator.lower()
            canon = canonical_post_url(url)
            ident = str(stable_id) if stable_id not in (None, "") else None
            if creator not in run_usernames or canon is None:
                unresolved.append({"row": row, "run_id": run_record["run_id"], "status": "interface_error",
                                   "reason": "creator mapping or public post URL does not match the run contract"})
                row_error_count += 1
                if creator in classifications:
                    classifications[creator]["row_issue_count"] += 1
                else:
                    unattributed_issue_count += 1
                raw_index += 1
                continue
            classifications[creator]["returned_raw_rows"] += 1
            key = ("url", canon)
            if key in seen:
                prior = seen[key]
                if (prior["creator"] != creator or prior["stable_id"] and ident and prior["stable_id"] != ident
                        or prior["timestamp"] != stamp):
                    reason = ("same canonical URL has conflicting creator, stable ID, or timestamp evidence")
                    unresolved.append({"row": row, "run_id": run_record["run_id"], "status": "identity_conflict",
                                       "reason": reason, "conflicts_with": prior["index"]})
                    identity_conflict_count += 1
                    classifications[creator]["row_issue_count"] += 1
                    prior_creator = prior["creator"]
                    if prior_creator in classifications:
                        classifications[prior_creator]["row_issue_count"] += 1
                else:
                    unresolved.append({"row": row, "run_id": run_record["run_id"], "status": "duplicate_candidate", "duplicate_of": prior["index"]})
                raw_index += 1
                continue
            if ident and ident in seen_ids and seen_ids[ident]["url"] != canon:
                unresolved.append({"row": row, "run_id": run_record["run_id"], "status": "identity_conflict",
                                   "reason": "same stable ID maps to a different canonical URL",
                                   "conflicts_with": seen_ids[ident]["index"]})
                identity_conflict_count += 1
                classifications[creator]["row_issue_count"] += 1
                prior_row = seen_ids[ident]
                prior_creator = prior_row.get("creator")
                if prior_creator in classifications:
                    classifications[prior_creator]["row_issue_count"] += 1
                raw_index += 1
                continue
            seen[key] = {"creator": creator, "stable_id": ident, "timestamp": stamp, "index": raw_index}
            if ident:
                seen_ids[ident] = {"url": canon, "index": raw_index, "creator": creator}
            if stamp is None:
                classifications[creator]["missing_timestamp"] += 1
                unresolved.append({"row": row, "run_id": run_record["run_id"], "status": "missing_timestamp"})
            elif not lo <= stamp < hi:
                classifications[creator]["out_of_window"] += 1
                unresolved.append({"row": row, "run_id": run_record["run_id"], "status": "out_of_window"})
            elif kind.casefold() in non_video_values:
                classifications[creator]["non_video"] += 1
                unresolved.append({"row": row, "run_id": run_record["run_id"], "status": "non_video"})
            elif kind.casefold() in video_values:
                by_creator[creator].append({"row": row, "creator": creator, "url": canon, "stable_id": ident,
                                           "stable_id_kind": contract["id_kind"], "timestamp": stamp,
                                           "source_run_id": run_record["run_id"]})
            else:
                classifications[creator]["unknown_media_type"] += 1
                unresolved.append({"row": row, "run_id": run_record["run_id"], "status": "unknown_media_type", "value": kind})
                row_error_count += 1
                classifications[creator]["row_issue_count"] += 1
            raw_index += 1
    at_limit_possible = any(record["possible_results_limit_reached"] for record, _, _ in normalized_runs)
    unknown_scope = any(record["limit_scope_unknown"] for record, _, _ in normalized_runs)
    selected, counts = [], {}
    for creator, rows in by_creator.items():
        rows.sort(key=lambda x: x["timestamp"], reverse=True)
        chosen = rows[:cap]
        selected.extend(chosen)
        creator_run_records = classifications[creator]["run_coverage"]
        creator_unknown = (classifications[creator].get("results_limit_scope_unknown", False)
                           or any(item["status"] == "run_status_unknown" for item in creator_run_records))
        creator_partial = (classifications[creator]["row_issue_count"] > 0
                           or classifications[creator]["additional_candidates_unknown"]
                           or len(rows) > len(chosen)
                           or classifications[creator]["unknown_media_type"] > 0
                           or classifications[creator]["missing_timestamp"] > 0
                           or bool(classifications[creator].get("possible_results_limit_reached")))
        creator_partial = creator_partial or any(item["status"] not in {
            "returned_below_run_limit", "possible_results_limit_reached",
            "unknown_multi_username_limit_scope", "possible_results_limit_reached_scope_unknown"
        } for item in creator_run_records)
        counts[creator] = {"discovered_returned_in_window": len(rows),
                           "returned_raw_rows": classifications[creator]["returned_raw_rows"], "selected": len(chosen),
                           "omitted_by_cap_observed": max(0, len(rows)-len(chosen)),
                           "coverage_status": "unknown" if creator_unknown else ("partial" if creator_partial or len(rows) > len(chosen) else "complete"),
                           "additional_candidates_unknown": classifications[creator]["additional_candidates_unknown"],
                           "possible_results_limit_reached": classifications[creator].get("possible_results_limit_reached"),
                           "results_limit_scope_unknown": classifications[creator].get("results_limit_scope_unknown", False),
                           "run_coverage": classifications[creator]["run_coverage"],
                           **classifications[creator]}
    unknown_types = any(counts[a]["unknown_media_type"] for a in counts)
    omitted = any(counts[a]["omitted_by_cap_observed"] for a in counts)
    missing_times = any(counts[a]["missing_timestamp"] for a in counts)
    run_incomplete = any(not (record["run_status"] == "SUCCEEDED" and record["retrieval_complete"])
                         for record, _, _ in normalized_runs)
    row_issues = identity_conflict_count > 0 or row_error_count > 0
    incomplete = (unknown_scope or at_limit_possible or omitted or missing_times or unknown_types
                  or run_incomplete
                  or any(counts[a]["row_issue_count"] for a in counts)
                  or unattributed_issue_count > 0 or bool(missing_run_fields))
    if row_error_count or missing_run_fields:
        status = "partial_interface_error"
    elif incomplete:
        status = "partial"
    elif selected:
        status = "complete"
    else:
        status = "no_candidates"
    coverage_unknown = (unknown_scope or unattributed_issue_count > 0 or bool(missing_run_fields)
                        or any(record["coverage_status"] == "run_status_unknown"
                               for record, _, _ in normalized_runs))
    interface_errors = ([{"code": "invalid_or_missing_run_metadata", "missing": missing_run_fields}]
                        if missing_run_fields else [])
    return {"status": status, "selected": selected, "counts": counts, "unresolved": unresolved,
            "coverage_status": "unknown" if coverage_unknown else ("partial" if incomplete else "complete"),
            "run_coverage": [record for record, _, _ in normalized_runs],
            "run_failures": run_failures, "row_interface_error_count": row_error_count,
            "identity_conflict_count": identity_conflict_count,
            "unattributed_issue_count": unattributed_issue_count,
            "interface_errors": interface_errors,
            "possible_results_limit_reached": at_limit_possible}

def reconcile_transcripts(submitted, rows, run_status, dataset_complete, post_contract, transcript_contract):
    require_post_contract(post_contract)
    names = ("url", "code", "pk", "creator", "text", "segments", "error", "segment_text")
    if not isinstance(transcript_contract, dict) or any(not isinstance(transcript_contract.get(k), str) or not transcript_contract[k] for k in names):
        raise ContractError("interface_error: exact Transcript output field contract is missing")
    if not isinstance(submitted, list) or not isinstance(rows, list):
        raise ContractError("interface_error: submitted candidates and transcript rows must be arrays")
    if type(dataset_complete) is not bool:
        raise ContractError("dataset_complete must be boolean evidence")
    if run_status not in {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT", "RUNNING", "UNKNOWN"}:
        raise ContractError("unrecognized run status")
    post_id_kind = transcript_contract.get("post_id_kind")
    if post_id_kind not in {"code", "pk"}:
        raise ContractError("interface_error: verified post stable-ID kind is missing")
    if post_id_kind != post_contract["id_kind"]:
        raise ContractError("interface_error: Profile Posts and Transcript stable ID kinds differ; no verified mapping exists")
    by_url, by_id = {}, {}
    for post in submitted:
        by_url.setdefault(post["url"], []).append(post)
        if post.get("stable_id"):
            by_id.setdefault((post_id_kind, str(post["stable_id"])), []).append(post)
    results = {}
    for p in submitted:
        prior = results.get(p["url"])
        if prior:
            prior["status"] = "duplicate_candidate"
            prior.setdefault("duplicates", []).append(p)
        else:
            results[p["url"]] = {"post": p, "status": "pending" if run_status in {"RUNNING", "UNKNOWN"} or not dataset_complete else ("not_returned" if run_status == "SUCCEEDED" else "run_failed")}
    row_counts, conflicted_posts = {}, set()
    url_field, code_field, pk_field, creator_field = (transcript_contract[k] for k in ("url", "code", "pk", "creator"))
    id_field = pk_field if post_id_kind == "pk" else code_field
    def mark_conflict(posts, row, row_index, reason):
        for candidate in posts:
            if candidate["url"] in results:
                results[candidate["url"]] = {"post": candidate, "row": row,
                    "status": "identity_conflict", "reason": reason, "row_index": row_index}
                conflicted_posts.add(candidate["url"])

    for row_index, row in enumerate(rows):
        if not isinstance(row, dict):
            results[f"unassigned:{row_index}"] = {"row": row, "status": "schema_invalid"}
            continue
        if url_field not in row:
            results[f"unassigned:{row_index}"] = {"row": row, "status": "schema_invalid", "reason": "URL field is missing"}
            continue
        raw_url = row.get(url_field)
        canon = canonical_post_url(raw_url) if raw_url is not None else None
        ident = row.get(id_field)
        id_candidates = by_id.get((post_id_kind, str(ident)), []) if ident not in (None, "") else []
        if raw_url is not None and canon is None:
            if id_candidates:
                mark_conflict(id_candidates, row, row_index, "transcript URL is invalid but the stable ID points to a submitted post")
            else:
                results[f"unassigned:{row_index}"] = {"row": row, "status": "schema_invalid", "reason": "invalid transcript URL"}
            continue
        if raw_url is None and not id_candidates:
            results[f"unassigned:{row_index}"] = {"row": row, "status": "schema_invalid"}
            continue
        url_candidates = by_url.get(canon, []) if canon else []
        if url_candidates and ident not in (None, "") and any(
                p.get("stable_id") and str(p["stable_id"]) != str(ident) for p in url_candidates):
            mark_conflict(url_candidates + id_candidates, row, row_index, "transcript URL and stable ID identify different posts")
            continue
        if url_candidates and id_candidates:
            url_keys = {p["url"] for p in url_candidates}
            id_keys = {p["url"] for p in id_candidates}
            if url_keys != id_keys:
                mark_conflict(url_candidates + id_candidates, row, row_index, "transcript URL and stable ID identify different submitted posts")
                continue
        if raw_url is not None and not url_candidates and id_candidates:
            mark_conflict(id_candidates, row, row_index, "transcript URL points to a different post than the stable ID")
            continue
        candidates = url_candidates or id_candidates
        if not candidates:
            results[f"unassigned:{row_index}"] = {"row": row, "status": "unmatched"}
            continue
        if len(candidates) != 1:
            mark_conflict(candidates, row, row_index, "transcript identity matches more than one submitted post")
            continue
        post = candidates[0]
        if post["url"] in conflicted_posts:
            results[post["url"]].setdefault("conflicting_rows", []).append(row)
            continue
        returned_creator = row.get(creator_field)
        if returned_creator not in (None, ""):
            if not isinstance(returned_creator, str):
                mark_conflict([post], row, row_index, "transcript creator field has an invalid type")
                continue
            if returned_creator.strip().lstrip("@").casefold() != str(post.get("creator", "")).strip().lstrip("@").casefold():
                mark_conflict([post], row, row_index, "transcript creator differs from the submitted post owner")
                continue
        text_key, seg_key, error_key = (transcript_contract[k] for k in ("text", "segments", "error"))
        row_counts[post["url"]] = row_counts.get(post["url"], 0) + 1
        if row_counts[post["url"]] > 1:
            previous = results[post["url"]]
            prior_rows = previous.get("rows", [previous["row"]])
            results[post["url"]] = {"post": post, "rows": prior_rows + [row], "status": "duplicate_transcript_rows"}
            continue
        if error_key in row and not isinstance(row[error_key], (str, type(None))):
            status, transcript = "schema_invalid", None
        elif error_key in row and row[error_key] not in (None, ""):
            status, transcript = "failed", None
        elif text_key not in row:
            segments = row.get(seg_key)
            segment_text_key = transcript_contract["segment_text"]
            if seg_key in row and not isinstance(segments, list):
                status, transcript = "schema_invalid", None
            elif isinstance(segments, list) and segments and all(isinstance(s, dict) and isinstance(s.get(segment_text_key), str) for s in segments):
                status, transcript = "segments_only", None
            elif isinstance(segments, list) and any(not isinstance(s, dict) or segment_text_key not in s or not isinstance(s.get(segment_text_key), str) for s in segments):
                status, transcript = "schema_invalid", None
            else:
                status, transcript = "schema_missing_text", None
        elif not isinstance(row[text_key], str):
            status, transcript = "schema_invalid", None
        elif not row[text_key].strip():
            status, transcript = "empty", ""
        else:
            status, transcript = "success", row[text_key]
        results[post["url"]] = {"post": post, "row": row, "transcript": transcript, "status": status}
    return list(results.values())

WAIT_SECS_MAX = 45

def require_mcp_run_contract(contract):
    required_call = {"actor", "input", "waitSecs", "callOptions"}
    required_options = {"maxItems", "maxTotalChargeUsd"}
    if (not isinstance(contract, dict) or contract.get("verified") is not True
            or contract.get("call_tool") != "call-actor"
            or not isinstance(contract.get("call_actor_fields"), list)
            or not required_call.issubset(set(contract["call_actor_fields"]))
            or not isinstance(contract.get("call_options_fields"), list)
            or not required_options.issubset(set(contract["call_options_fields"]))
            or type(contract.get("max_wait_secs")) is not int
            or not 0 <= contract["max_wait_secs"] <= WAIT_SECS_MAX):
        raise ContractError("budget_blocked: live call-actor tool contract is missing or unverified")
    readback = contract.get("run_readback")
    common = {"run_id_field", "options_field", "options_fields"}
    if (not isinstance(readback, dict) or readback.get("verified") is not True
            or readback.get("tool") not in {"get-actor-run", "get-actor-run-list"}
            or not common.issubset(readback)
            or not isinstance(readback.get("options_fields"), list)
            or not required_options.issubset(set(readback["options_fields"]))):
        raise ContractError("budget_blocked: no verified live readback tool contract exposes run options")
    if readback["tool"] == "get-actor-run-list" and not isinstance(readback.get("items_field"), str):
        raise ContractError("budget_blocked: get-actor-run-list item path is not verified")
    if type(contract["max_wait_secs"]) is int and contract["max_wait_secs"] > WAIT_SECS_MAX:
        raise ContractError("interface_error: waitSecs maximum exceeds the documented 45-second contract")
    return readback

def require_pricing_contract(pricing):
    if not isinstance(pricing, dict) or pricing.get("verified") is not True:
        raise ContractError("pricing_unverified: fetch the current Actor pricing contract before planning a paid run")
    if pricing.get("currency") != "USD" or not isinstance(pricing.get("source"), str) or not pricing["source"]:
        raise ContractError("pricing_contract_invalid: currency and traceable pricing source are required")
    if not isinstance(pricing.get("checked_at"), str) or not pricing["checked_at"]:
        raise ContractError("pricing_contract_invalid: pricing check date is required")
    model = pricing.get("model")
    minimum = money_cents(pricing.get("minimum_run_charge_usd"), "minimum_run_charge_usd", allow_zero=True)
    if model == "pay_per_result":
        unit = usd_decimal(pricing.get("max_total_cost_per_result_usd"), "max_total_cost_per_result_usd")
        fixed = usd_decimal(pricing.get("max_fixed_run_cost_usd"), "max_fixed_run_cost_usd", allow_zero=True)
        if pricing.get("all_billable_components_bounded_by_max_items") is not True:
            raise ContractError("pricing_unbounded: maxItems does not bound every billable component")
        if fixed * 100 > minimum:
            raise ContractError("pricing_contract_invalid: minimum_run_charge_usd must cover fixed run charges")
        return {"model": model, "minimum_run_charge_cents": minimum,
                "unit_cost_usd": unit, "fixed_cost_usd": fixed}
    if model == "pay_per_event":
        if pricing.get("all_billable_components_bounded_by_max_total_charge_usd") is not True:
            raise ContractError("pricing_unbounded: maxTotalChargeUsd does not cover every billable component")
        return {"model": model, "minimum_run_charge_cents": minimum}
    raise ContractError("pricing_unverified: billing model must be pay_per_result or pay_per_event")

def _required_ppr_cents(pricing, billable_items):
    charge = pricing["fixed_cost_usd"] + pricing["unit_cost_usd"] * billable_items
    return int((charge * 100).to_integral_value(rounding=ROUND_CEILING))

def _read_ledger(settings, ledger, stage):
    config = validate_settings(settings)
    total = config["report_budget_cents"]
    if ledger is None:
        if stage != "discovery":
            raise ContractError("budget_blocked: transcript planning requires a completed discovery ledger")
        return config, {"report_budget_cents": total, "reserved_cents": 0, "stages": []}
    if (not isinstance(ledger, dict) or ledger.get("report_budget_cents") != total
            or type(ledger.get("reserved_cents")) is not int or ledger["reserved_cents"] < 0
            or not isinstance(ledger.get("stages"), list)):
        raise ContractError("budget_blocked: prior stage ledger is invalid or does not match the report budget")
    stage_names = [item.get("name") for item in ledger["stages"] if isinstance(item, dict)]
    if stage == "discovery" and stage_names:
        raise ContractError("budget_blocked: discovery stage was already planned")
    if stage == "transcription" and stage_names != ["discovery"]:
        raise ContractError("budget_blocked: transcript replanning requires exactly one discovery stage")
    if stage not in {"discovery", "transcription"}:
        raise ContractError("stage must be discovery or transcription")
    if ledger["reserved_cents"] > total:
        raise ContractError("budget_blocked: prior stage reservations exceed the report budget")
    return config, ledger

def plan_budget_stage(settings, stage, runs, host_contract, ledger=None):
    """Plan only the currently known stage; reserve every prior run's full cap."""
    config, ledger = _read_ledger(settings, ledger, stage)
    readback_contract = require_mcp_run_contract(host_contract)
    if not isinstance(runs, list):
        raise ContractError("runs must be an array")
    total = config["report_budget_cents"]
    available = total - ledger["reserved_cents"]
    if not runs:
        if stage != "transcription":
            raise ContractError("discovery stage requires at least one run")
        next_ledger = {**ledger, "stages": ledger["stages"] + [{"name": stage, "reserved_cents": 0, "calls": []}]}
        return {"state": "no_transcript_runs_needed", "available_cents": available,
                "reserved_cents": next_ledger["reserved_cents"], "ledger": next_ledger, "calls": []}

    prepared, ppe_indices, allocated = [], [], 0
    for index, run in enumerate(runs):
        if not isinstance(run, dict) or not isinstance(run.get("actor"), str) or not run["actor"] or not isinstance(run.get("input"), dict):
            raise ContractError("run plan entries require actor and input")
        wait_secs = run.get("wait_secs")
        if type(wait_secs) is not int or not 0 <= wait_secs <= min(host_contract["max_wait_secs"], WAIT_SECS_MAX):
            raise ContractError("wait_secs is outside the verified call-actor range")
        pricing = require_pricing_contract(run.get("pricing"))
        if pricing["minimum_run_charge_cents"] <= 0:
            raise ContractError("pricing_contract_invalid: each paid run requires a positive minimum run charge")
        if pricing["model"] == "pay_per_result":
            items = run.get("billable_items_requested")
            if type(items) is not int or items <= 0:
                raise ContractError("billable_items_requested must be a positive integer for pay-per-result runs")
            cost_cents = _required_ppr_cents(pricing, items)
            if cost_cents < pricing["minimum_run_charge_cents"]:
                cost_cents = pricing["minimum_run_charge_cents"]
            prepared.append({"run": run, "pricing": pricing, "allocation_cents": cost_cents,
                             "call_options": {"maxItems": items}})
            allocated += cost_cents
        else:
            prepared.append({"run": run, "pricing": pricing, "allocation_cents": 0, "call_options": None})
            ppe_indices.append(index)

    ppe_minima = sum(prepared[i]["pricing"]["minimum_run_charge_cents"] for i in ppe_indices)
    remaining = available - allocated - ppe_minima
    if remaining < 0:
        raise ContractError("budget_blocked: this stage's safe run limits exceed the unreserved report budget; preserve prior results and mark this stage unprocessed")
    if ppe_indices:
        # Discovery keeps all non-minimum budget available for the still-unknown
        # transcript batch plan. Transcription is the final stage and may use it.
        distributable = remaining if stage == "transcription" else 0
        base_share, remainder = divmod(distributable, len(ppe_indices))
        for position, index in enumerate(ppe_indices):
            allocation = prepared[index]["pricing"]["minimum_run_charge_cents"] + base_share + (1 if position < remainder else 0)
            prepared[index]["allocation_cents"] = allocation
            prepared[index]["call_options"] = {"maxTotalChargeUsd": f"{Decimal(allocation)/100:.2f}"}
            allocated += allocation
    else:
        allocated = sum(item["allocation_cents"] for item in prepared)
    if allocated > available:
        raise ContractError("budget_blocked: current-stage run allocations exceed the unreserved report budget")

    calls = []
    for item in prepared:
        run = item["run"]
        options = item["call_options"]
        if options is None:
            raise ContractError("budget_blocked: run has no verified pricing cap")
        arguments = {"actor": run["actor"], "input": run["input"], "waitSecs": run["wait_secs"], "callOptions": options}
        reserve = item["allocation_cents"]
        calls.append({"tool_call": {"name": host_contract["call_tool"], "arguments": arguments},
                      "planning": {"billing_model": item["pricing"]["model"],
                          "allocation_cents": reserve, "reservation_cents": reserve,
                          "calculation": ("verified maxItems × conservative unit price" if item["pricing"]["model"] == "pay_per_result"
                                          else "run maxTotalChargeUsd cap"),
                          "readback_tool": readback_contract["tool"], "execution_status": "offline_plan_not_executed"}})
    next_ledger = {"report_budget_cents": total, "reserved_cents": ledger["reserved_cents"] + allocated,
                   "stages": ledger["stages"] + [{"name": stage, "reserved_cents": allocated,
                       "calls": [{"allocation_cents": c["planning"]["reservation_cents"]} for c in calls]}]}
    if next_ledger["reserved_cents"] > total:
        raise ContractError("budget_blocked: cumulative stage reservations exceed the report budget")
    return {"state": "offline_plan_not_executed", "stage": stage,
            "stage_reserved_cents": allocated, "available_before_stage_cents": available,
            "available_after_stage_cents": available-allocated,
            "reserved_cents": next_ledger["reserved_cents"], "report_budget_cents": total,
            "calls": calls, "ledger": next_ledger}

def _path_value(obj, path):
    value = obj
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value

def verify_run_limit(planned_call, response, run_id, host_contract):
    readback = require_mcp_run_contract(host_contract)
    if not isinstance(planned_call, dict) or not isinstance(response, dict) or not isinstance(run_id, str) or not run_id:
        raise ContractError("interface_error: planned call, readback response, and run ID are required")
    tool_call = planned_call.get("tool_call")
    args = tool_call.get("arguments") if isinstance(tool_call, dict) else None
    expected = args.get("callOptions") if isinstance(args, dict) else None
    if not isinstance(expected, dict):
        raise ContractError("interface_error: planned MCP callOptions are missing")
    if readback["tool"] == "get-actor-run-list":
        items = _path_value(response, readback["items_field"])
        records = [r for r in items if isinstance(r, dict) and r.get(readback["run_id_field"]) == run_id] if isinstance(items, list) else []
    else:
        records = [response] if response.get(readback["run_id_field"]) == run_id else []
    if len(records) != 1:
        return {"state": "budget_readback_unverified", "stop_subsequent_runs": True,
                "reason": "the configured readback response did not identify exactly one matching run"}
    actual = records[0].get(readback["options_field"])
    if not isinstance(actual, dict):
        return {"state": "budget_readback_unverified", "stop_subsequent_runs": True,
                "reason": "the configured readback response did not include the declared run options field"}
    for key, expected_value in expected.items():
        if key not in actual:
            return {"state": "budget_readback_unverified", "stop_subsequent_runs": True,
                    "reason": f"readback run options field {key} was not returned"}
        try:
            matches = Decimal(str(actual[key])) == Decimal(str(expected_value))
        except InvalidOperation:
            matches = actual[key] == expected_value
        if not matches:
            return {"state": "budget_readback_mismatch", "stop_subsequent_runs": True,
                    "reason": f"readback run options field {key} does not match the requested cap"}
    return {"state": "budget_readback_verified", "stop_subsequent_runs": False}

def remaining_budget(report_budget, actual_spend):
    total = money_cents(report_budget, "report_budget_usd")
    try:
        spend = Decimal(str(actual_spend))
    except InvalidOperation:
        raise ContractError("actual_spend must be a finite non-negative amount")
    if not spend.is_finite() or spend < 0:
        raise ContractError("actual_spend must be a finite non-negative amount")
    spent_cents = int((spend * 100).to_integral_value(rounding=ROUND_CEILING))
    return max(0, total - spent_cents)

def split_batches(urls, batch_size):
    if not isinstance(urls, list) or any(not isinstance(url, str) or not url for url in urls):
        raise ContractError("urls must be a list of non-empty strings")
    if type(batch_size) is not int or batch_size <= 0:
        raise ContractError("batch_size must come from a verified live limit")
    return [urls[i:i+batch_size] for i in range(0, len(urls), batch_size)]

def main():
    try:
        req = json.load(sys.stdin)
        op = req.get("operation")
        if op == "settings": result = validate_settings(req.get("settings"))
        elif op == "window": result = window(req.get("now"), req.get("mode"))
        elif op == "select": result = select_posts(req.get("runs"), req.get("accounts"), req.get("per_creator_limit"), req.get("start"), req.get("end_exclusive"), req.get("post_contract"))
        elif op == "plan_stage": result = plan_budget_stage(req.get("settings"), req.get("stage"), req.get("runs"), req.get("host_contract"), req.get("ledger"))
        elif op == "verify_run": result = verify_run_limit(req.get("planned_call"), req.get("response"), req.get("run_id"), req.get("host_contract"))
        elif op == "remaining": result = {"remaining_cents": remaining_budget(req.get("report_budget_usd"), req.get("actual_spend_usd"))}
        elif op == "split": result = {"batches": split_batches(req.get("urls"), req.get("batch_size"))}
        elif op == "reconcile":
            result = {"results": reconcile_transcripts(req.get("submitted"), req.get("rows"), req.get("run_status"), req.get("dataset_complete"), req.get("post_contract"), req.get("transcript_contract"))}
        else: raise ContractError("unknown operation")
        print(json.dumps(result, ensure_ascii=False, default=lambda x: x.isoformat()))
    except (ContractError, TypeError, AttributeError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
