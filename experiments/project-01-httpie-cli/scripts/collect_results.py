#!/usr/bin/env python3
"""
collect_results.py
==================
Downloads Eco-CI JSON energy measurement artifacts from GitHub Actions
and consolidates them into a single CSV file for statistical analysis.

Workflow files across all projects live on a single `main` branch in this
repository, with the project and configuration encoded in the filename:
    p{NN}-{project}-c{1-4}-{type}.yml
e.g. p01-httpie-c1-tests.yml, p02-got-c2-tests.yml, p03-retrofit-c4-combined.yml

Usage:
    export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
    export GITHUB_REPO=Umer-2612/msc-devops-dissertation
    python scripts/collect_results.py

Output:
    results/raw_data.csv — columns: run_id, project, config, stage,
                                     energy_joules, duration_seconds,
                                     timestamp, workflow, python_version
"""

import csv
import json
import os
import re
import sys
import time
import zipfile
from io import BytesIO
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO")

# Matches workflow filenames like p01-httpie-c1-tests.yml -> project="httpie", config="C1"
WORKFLOW_FILENAME_RE = re.compile(r"^p\d+-(?P<project>[a-z0-9]+)-c(?P<config>[1-4])-")

OUTPUT_CSV = Path("results/raw_data.csv")
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

CSV_COLUMNS = [
    "run_id",
    "project",
    "config",
    "workflow",
    "stage",
    "energy_joules",
    "duration_seconds",
    "timestamp",
    "python_version",
]


# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------
def get_headers() -> dict:
    if not GITHUB_TOKEN:
        print("ERROR: GITHUB_TOKEN environment variable not set.", file=sys.stderr)
        sys.exit(1)
    if not GITHUB_REPO:
        print("ERROR: GITHUB_REPO environment variable not set.", file=sys.stderr)
        sys.exit(1)
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def api_get(url: str, params: dict = None) -> dict | list:
    """GET request with rate-limit handling."""
    headers = get_headers()
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    if resp.status_code == 429 or resp.status_code == 403:
        reset = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
        wait = max(reset - int(time.time()), 10)
        print(f"Rate-limited. Waiting {wait}s …")
        time.sleep(wait)
        return api_get(url, params)
    resp.raise_for_status()
    return resp.json()


def paginate(url: str, key: str, params: dict = None) -> list:
    """Fetch all pages from a paginated GitHub API endpoint."""
    params = params or {}
    params["per_page"] = 100
    results = []
    page = 1
    while True:
        params["page"] = page
        data = api_get(url, params)
        items = data.get(key, [])
        results.extend(items)
        if len(items) < 100:
            break
        page += 1
    return results


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------
def list_workflow_runs() -> list[dict]:
    """Fetch all completed workflow runs for the repository."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs"
    runs = paginate(url, "workflow_runs", {"status": "completed", "branch": "main"})
    print(f"Found {len(runs)} completed workflow runs.")
    return runs


def list_artifacts(run_id: int) -> list[dict]:
    """List artifacts for a specific workflow run."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs/{run_id}/artifacts"
    data = api_get(url)
    return data.get("artifacts", [])


def download_artifact(artifact: dict) -> bytes | None:
    """
    Download artifact zip and return raw bytes.

    GitHub's artifact download endpoint responds with a 302 redirect to a
    SAS-signed Azure Blob Storage URL. That URL authenticates via its own
    signed query parameters and rejects requests that also carry a GitHub
    Authorization header, so the redirect must be followed manually with a
    fresh, unauthenticated request rather than via requests' automatic
    redirect-following (which forwards the original headers).
    """
    download_url = artifact.get("archive_download_url")
    if not download_url:
        return None
    headers = get_headers()
    resp = requests.get(download_url, headers=headers, timeout=60, allow_redirects=False)
    if resp.status_code in (301, 302, 303, 307, 308):
        blob_url = resp.headers.get("Location")
        if not blob_url:
            print(f"  WARNING: Redirect response for '{artifact['name']}' had no Location header.")
            return None
        blob_resp = requests.get(blob_url, timeout=60)
        if blob_resp.status_code == 200:
            return blob_resp.content
        print(f"  WARNING: Could not download artifact {artifact['name']} from blob storage — HTTP {blob_resp.status_code}")
        return None
    if resp.status_code == 200:
        return resp.content
    print(f"  WARNING: Could not download artifact {artifact['name']} — HTTP {resp.status_code}")
    return None


def parse_eco_ci_json(raw_bytes: bytes, artifact_name: str) -> list[dict]:
    """
    Extract measurement entries from an Eco-CI artifacts zip.
    Eco-CI writes an 'eco-ci-results.json' file (array of measurement objects).
    Field names are matched defensively since Eco-CI's exact schema has
    varied across releases; verify against a real downloaded artifact
    before relying on this for the final dataset.
    """
    rows = []
    try:
        with zipfile.ZipFile(BytesIO(raw_bytes)) as zf:
            json_files = [n for n in zf.namelist() if n.endswith(".json")]
            if not json_files:
                print(f"  WARNING: No JSON files found in artifact '{artifact_name}'")
                return rows
            for fname in json_files:
                with zf.open(fname) as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        measurements = data
                    elif isinstance(data, dict):
                        measurements = data.get("measurements", data.get("data", [data]))
                    else:
                        continue

                    for m in measurements:
                        rows.append({
                            "stage": m.get("label", m.get("note", "unknown")),
                            "energy_joules": m.get("total_energy_J", m.get("energy_value", m.get("cpu_energy_J", 0.0))),
                            "duration_seconds": m.get("duration", m.get("total_time", 0.0)),
                            "timestamp": m.get("time", m.get("timestamp", "")),
                        })
    except zipfile.BadZipFile:
        print(f"  WARNING: Artifact '{artifact_name}' is not a valid zip file.")
    except json.JSONDecodeError as e:
        print(f"  WARNING: JSON parse error in artifact '{artifact_name}': {e}")
    return rows


def infer_project_and_config(run: dict) -> tuple[str, str]:
    """Determine (project, config) from the workflow file path, e.g.
    '.github/workflows/p02-got-c2-tests.yml' -> ('got', 'C2')."""
    workflow_file = run.get("path", "").split("/")[-1]
    m = WORKFLOW_FILENAME_RE.match(workflow_file)
    if m:
        return m.group("project"), f"C{m.group('config')}"
    return "unknown", "unknown"


def infer_python_version(artifact_name: str) -> str:
    """Extract Python version from artifact name (e.g. 'eco-ci-p01-c1-tests-py3.11')."""
    for part in artifact_name.split("-"):
        if part.startswith("py") and len(part) > 2 and part[2].isdigit():
            return part[2:]
    return ""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print(f"Repository: {GITHUB_REPO}")
    print(f"Output: {OUTPUT_CSV}\n")

    runs = list_workflow_runs()
    all_rows: list[dict] = []

    for run in runs:
        run_id = run["id"]
        workflow_name = run.get("name", "unknown")
        project, config = infer_project_and_config(run)

        print(f"  Run #{run_id} | project={project} | config={config} | workflow={workflow_name}")

        artifacts = list_artifacts(run_id)
        eco_artifacts = [a for a in artifacts if "eco-ci" in a["name"].lower()]

        if not eco_artifacts:
            print(f"    No Eco-CI artifacts found for run #{run_id}")
            continue

        for artifact in eco_artifacts:
            print(f"    Downloading: {artifact['name']}")
            raw = download_artifact(artifact)
            if raw is None:
                continue

            rows = parse_eco_ci_json(raw, artifact["name"])
            python_version = infer_python_version(artifact["name"])

            for row in rows:
                all_rows.append({
                    "run_id": run_id,
                    "project": project,
                    "config": config,
                    "workflow": workflow_name,
                    "stage": row["stage"],
                    "energy_joules": row["energy_joules"],
                    "duration_seconds": row["duration_seconds"],
                    "timestamp": row["timestamp"],
                    "python_version": python_version,
                })

    if not all_rows:
        print("\nNo data collected. Have the workflows been triggered yet?")
        sys.exit(0)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\n✓ Wrote {len(all_rows)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
