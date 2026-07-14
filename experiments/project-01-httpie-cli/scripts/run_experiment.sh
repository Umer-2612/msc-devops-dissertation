#!/bin/bash
# run_experiment.sh
# Full 30-run protocol for all four experiment configurations.
# All workflows live in the dissertation repo on the main branch.
# They check out httpie/cli@3.2.4 externally — no separate fork needed.
#
# Run each config block separately; don't chain all four back-to-back
# unless you have 10-12 hours free to monitor them.
#
# Prerequisites:
#   export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
#   export GITHUB_REPO=Umer-2612/msc-devops-dissertation
#   pip install requests

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BRANCH="main"

run_trigger() { python3 "$SCRIPT_DIR/trigger_runs.py" "$@"; }
run_collect()  { python3 "$SCRIPT_DIR/collect_results.py" "$@"; }

check_env() {
    if [ -z "$GITHUB_TOKEN" ]; then
        echo "ERROR: GITHUB_TOKEN is not set. Run: export GITHUB_TOKEN=ghp_..."
        exit 1
    fi
    if [ -z "$GITHUB_REPO" ]; then
        echo "ERROR: GITHUB_REPO is not set. Run: export GITHUB_REPO=Umer-2612/msc-devops-dissertation"
        exit 1
    fi
}

run_config() {
    local label=$1
    local workflow=$2
    local runs=${3:-30}
    local interval=${4:-300}

    echo ""
    echo "============================================================"
    echo "Starting $label  ($runs runs, ${interval}s interval)"
    echo "Branch:   $BRANCH"
    echo "Workflow: $workflow"
    echo "============================================================"
    run_trigger --branch "$BRANCH" --workflow "$workflow" --runs "$runs" --interval "$interval"
}

check_env

case "${1:-help}" in
    c1)
        run_config "C1 baseline (tests)"      p01-httpie-c1-tests.yml
        run_config "C1 baseline (code-style)" p01-httpie-c1-code-style.yml
        run_config "C1 baseline (coverage)"   p01-httpie-c1-coverage.yml
        ;;
    c2)
        run_config "C2 pip-cache (tests)"     p01-httpie-c2-tests.yml
        run_config "C2 pip-cache (code-style)" p01-httpie-c2-code-style.yml
        run_config "C2 pip-cache (coverage)"  p01-httpie-c2-coverage.yml
        ;;
    c3)
        run_config "C3 consolidation"         p01-httpie-c3-consolidated.yml
        ;;
    c4)
        run_config "C4 combined"              p01-httpie-c4-combined.yml
        ;;
    collect)
        echo "Downloading all Eco-CI artifacts to results/raw_data.csv ..."
        run_collect
        ;;
    all)
        echo "WARNING: running all 4 configs back-to-back. This will take 10-12 hours."
        echo "Press Ctrl+C to cancel, or wait 10 seconds to continue ..."
        sleep 10
        bash "$0" c1
        bash "$0" c2
        bash "$0" c3
        bash "$0" c4
        bash "$0" collect
        ;;
    *)
        echo "Usage: $0 [c1|c2|c3|c4|collect|all]"
        echo ""
        echo "  c1       30 runs of C1 baseline (3 separate workflows)"
        echo "  c2       30 runs of C2 pip-cache (3 separate workflows)"
        echo "  c3       30 runs of C3 consolidation (1 consolidated workflow)"
        echo "  c4       30 runs of C4 combined (1 consolidated workflow + caching)"
        echo "  collect  download all Eco-CI artifacts -> results/raw_data.csv"
        echo "  all      run c1 + c2 + c3 + c4 + collect in sequence"
        echo ""
        echo "Environment variables required:"
        echo "  GITHUB_TOKEN   personal access token (repo + workflow scopes)"
        echo "  GITHUB_REPO    Umer-2612/msc-devops-dissertation"
        ;;
esac
