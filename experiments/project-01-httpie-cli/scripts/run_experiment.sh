#!/bin/bash
# run_experiment.sh
# Full 30-run protocol for all four experiment configurations.
# Run each branch block separately — don't run all four back-to-back
# in one sitting unless you have time to monitor (total ~10-12 hours).
#
# Prerequisites:
#   export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
#   export GITHUB_REPO=Umer-2612/httpie-cli-carbon-study
#   pip install requests

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TRIGGER="python3 $SCRIPT_DIR/trigger_runs.py"
COLLECT="python3 $SCRIPT_DIR/collect_results.py"

check_env() {
    if [ -z "$GITHUB_TOKEN" ]; then
        echo "ERROR: GITHUB_TOKEN is not set. Run: export GITHUB_TOKEN=ghp_..."
        exit 1
    fi
    if [ -z "$GITHUB_REPO" ]; then
        echo "ERROR: GITHUB_REPO is not set. Run: export GITHUB_REPO=Umer-2612/httpie-cli-carbon-study"
        exit 1
    fi
}

# ---------------------------------------------------------------------------
# Run one config block
# ---------------------------------------------------------------------------
run_config() {
    local label=$1
    local branch=$2
    local workflow=$3
    local runs=${4:-30}
    local interval=${5:-300}

    echo ""
    echo "============================================================"
    echo "Starting $label  ($runs runs, ${interval}s interval)"
    echo "Branch:   $branch"
    echo "Workflow: $workflow"
    echo "============================================================"
    $TRIGGER --branch "$branch" --workflow "$workflow" --runs "$runs" --interval "$interval"
}

# ---------------------------------------------------------------------------
# Choose which config to run via argument
# ---------------------------------------------------------------------------
check_env

case "${1:-help}" in
    c1)
        # C1 has 3 separate workflows — trigger each one 30 times
        run_config "C1 baseline (tests)"      experiment/c1-baseline tests.yml
        run_config "C1 baseline (code-style)" experiment/c1-baseline code-style.yml
        run_config "C1 baseline (coverage)"   experiment/c1-baseline coverage.yml
        ;;
    c2)
        # C2 same 3 workflows but with pip caching
        run_config "C2 cached (tests)"        experiment/c2-pip-cache tests.yml
        run_config "C2 cached (code-style)"   experiment/c2-pip-cache code-style.yml
        run_config "C2 cached (coverage)"     experiment/c2-pip-cache coverage.yml
        ;;
    c3)
        run_config "C3 consolidation"         experiment/c3-consolidation ci-consolidated.yml
        ;;
    c4)
        run_config "C4 combined"              experiment/c4-combined ci-consolidated.yml
        ;;
    collect)
        echo "Downloading all Eco-CI artifacts to results/raw_data.csv ..."
        $COLLECT
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
        echo "  c1       30 runs on experiment/c1-baseline (3 workflows)"
        echo "  c2       30 runs on experiment/c2-pip-cache (3 workflows)"
        echo "  c3       30 runs on experiment/c3-consolidation (1 workflow)"
        echo "  c4       30 runs on experiment/c4-combined (1 workflow)"
        echo "  collect  download all Eco-CI artifacts -> results/raw_data.csv"
        echo "  all      run c1 + c2 + c3 + c4 + collect in sequence"
        echo ""
        echo "Environment variables required:"
        echo "  GITHUB_TOKEN   personal access token (repo + workflow scopes)"
        echo "  GITHUB_REPO    e.g. Umer-2612/httpie-cli-carbon-study"
        ;;
esac
