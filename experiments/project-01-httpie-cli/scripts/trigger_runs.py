#!/usr/bin/env python3
"""
trigger_runs.py
===============
Triggers GitHub Actions workflow_dispatch events for the CI/CD carbon study.
Waits for each run to complete before firing the next one and enforces a
minimum inter-run interval to reduce shared-runner thermal and warm-up effects.

Requirements:
    pip install requests

Environment variables (required):
    GITHUB_TOKEN   personal access token with repo + workflow scopes
    GITHUB_REPO    owner/repo  e.g. Umer-2612/msc-devops-dissertation

Usage examples:

    # 30 runs of C1 baseline tests (all on main branch)
    python scripts/trigger_runs.py \\
        --branch main \\
        --workflow p01-httpie-c1-tests.yml \\
        --runs 30

    # 30 runs of C4 combined workflow
    python scripts/trigger_runs.py \\
        --branch main \\
        --workflow p01-httpie-c4-combined.yml \\
        --runs 30

    # Shorter interval for testing (60 s instead of default 300 s)
    python scripts/trigger_runs.py \\
        --branch main \\
        --workflow p01-httpie-c2-tests.yml \\
        --runs 5 \\
        --interval 60

    # Resume from run 15 if the script was interrupted
    python scripts/trigger_runs.py \\
        --branch main \\
        --workflow p01-httpie-c1-tests.yml \\
        --runs 30 \\
        --start-from 15
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from datetime import datetime, timezone

import requests


GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO  = os.environ.get("GITHUB_REPO")

DEFAULT_INTERVAL   = 300   # seconds between runs (5 min)
POLL_INTERVAL      = 30    # seconds between status polls while a run is in progress
TRIGGER_TIMEOUT    = 120   # seconds to wait for a triggered run to appear in the API
RUN_TIMEOUT        = 1800  # seconds before giving up on a single run (30 min)


# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------

def headers() -> dict:
    if not GITHUB_TOKEN:
        sys.exit("ERROR: set the GITHUB_TOKEN environment variable first.")
    if not GITHUB_REPO:
        sys.exit("ERROR: set the GITHUB_REPO environment variable first.")
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get(url: str, params: dict | None = None) -> dict | list:
    resp = requests.get(url, headers=headers(), params=params, timeout=30)
    _handle_rate_limit(resp)
    resp.raise_for_status()
    return resp.json()


def post(url: str, payload: dict) -> None:
    resp = requests.post(url, headers=headers(), json=payload, timeout=30)
    _handle_rate_limit(resp)
    if resp.status_code not in (201, 204):
        resp.raise_for_status()


def _handle_rate_limit(resp: requests.Response) -> None:
    if resp.status_code in (403, 429):
        reset = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
        wait  = max(reset - int(time.time()), 10)
        print(f"  [rate limit] waiting {wait}s …")
        time.sleep(wait)


# ---------------------------------------------------------------------------
# Workflow helpers
# ---------------------------------------------------------------------------

def get_workflow_id(workflow_filename: str) -> str:
    """Resolve workflow filename to its numeric or filename-based ID."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows"
    data = get(url)
    for wf in data.get("workflows", []):
        # GitHub accepts both the numeric id and the filename
        if wf["path"].endswith(workflow_filename):
            return str(wf["id"])
    # Fallback: GitHub also accepts the filename directly in the dispatch URL
    return workflow_filename


def trigger_dispatch(workflow_id: str, branch: str) -> str:
    """Fire a workflow_dispatch event. Returns ISO timestamp just before trigger."""
    triggered_at = datetime.now(timezone.utc).isoformat()
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/{workflow_id}/dispatches"
    post(url, {"ref": branch})
    return triggered_at


def find_triggered_run(branch: str, triggered_after: str, workflow_id: str) -> int | None:
    """
    Poll the runs list until we find a run on the given branch that was
    created after triggered_after. Returns the run ID.
    """
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs"
    deadline = time.time() + TRIGGER_TIMEOUT
    while time.time() < deadline:
        time.sleep(5)
        data = get(url, {"branch": branch, "event": "workflow_dispatch", "per_page": 10})
        for run in data.get("workflow_runs", []):
            if run.get("created_at", "") >= triggered_after:
                return run["id"]
        print("  waiting for run to appear in API …")
    return None


def wait_for_run(run_id: int) -> str:
    """Poll until the run reaches a terminal status. Returns final conclusion string."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs/{run_id}"
    deadline = time.time() + RUN_TIMEOUT
    while time.time() < deadline:
        data = get(url)
        status     = data.get("status")
        conclusion = data.get("conclusion")
        if status == "completed":
            return conclusion or "unknown"
        elapsed = int(time.time() - (time.time() - POLL_INTERVAL))
        print(f"  run #{run_id} status={status} … (polling every {POLL_INTERVAL}s)")
        time.sleep(POLL_INTERVAL)
    return "timed_out"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Trigger repeated workflow_dispatch runs for carbon study.")
    p.add_argument("--branch",     required=True, help="Branch to trigger, e.g. experiment/c2-pip-cache")
    p.add_argument("--workflow",   required=True, help="Workflow filename, e.g. tests.yml")
    p.add_argument("--runs",       type=int, default=30, help="Number of runs to trigger (default: 30)")
    p.add_argument("--interval",   type=int, default=DEFAULT_INTERVAL,
                   help=f"Minimum seconds between run start times (default: {DEFAULT_INTERVAL})")
    p.add_argument("--start-from", type=int, default=1, dest="start_from",
                   help="Skip to this run number if resuming after interruption (default: 1)")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    print(f"\nRepo:       {GITHUB_REPO}")
    print(f"Branch:     {args.branch}")
    print(f"Workflow:   {args.workflow}")
    print(f"Runs:       {args.runs} total  (starting from run {args.start_from})")
    print(f"Interval:   {args.interval}s between runs")
    print()

    workflow_id = get_workflow_id(args.workflow)
    print(f"Workflow ID resolved to: {workflow_id}\n")

    completed  = 0
    failed     = 0

    for run_num in range(args.start_from, args.runs + 1):
        run_start = time.time()
        print(f"{'='*60}")
        print(f"Run {run_num}/{args.runs}   {datetime.now().strftime('%H:%M:%S')}")

        # Trigger
        triggered_at = trigger_dispatch(workflow_id, args.branch)
        print(f"  triggered at {triggered_at}")

        # Find the run ID
        run_id = find_triggered_run(args.branch, triggered_at, workflow_id)
        if run_id is None:
            print(f"  ERROR: run did not appear within {TRIGGER_TIMEOUT}s — skipping.")
            failed += 1
            continue

        print(f"  run ID: {run_id}")
        print(f"  URL: https://github.com/{GITHUB_REPO}/actions/runs/{run_id}")

        # Wait for completion
        conclusion = wait_for_run(run_id)
        elapsed = int(time.time() - run_start)
        print(f"  finished: {conclusion}  ({elapsed}s)")

        if conclusion in ("success", "neutral"):
            completed += 1
        else:
            failed += 1
            print(f"  WARNING: run concluded with '{conclusion}' — data may be incomplete.")

        # Inter-run interval: wait until at least `interval` seconds have passed
        # since this run started (not since it ended)
        wait_remaining = args.interval - int(time.time() - run_start)
        if run_num < args.runs and wait_remaining > 0:
            print(f"  waiting {wait_remaining}s before next run …")
            time.sleep(wait_remaining)

    print(f"\n{'='*60}")
    print(f"Done. {completed} succeeded, {failed} failed/skipped out of {args.runs - args.start_from + 1} attempted.")
    print(f"Run collect_results.py next to download the Eco-CI artifacts.")


if __name__ == "__main__":
    main()
