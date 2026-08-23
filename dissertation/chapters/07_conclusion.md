# Chapter 7: Conclusion

## 7.1 Summary

This dissertation addresses the absence of project-level, evidence-based guidance on CI/CD pipeline carbon reduction. Using the Software Carbon Intensity specification (ISO/IEC 21031:2024) and the Eco-CI energy estimation tool, four progressively refined pipeline configurations are experimentally applied to a set of real open-source GitHub Actions projects, and their energy consumption measured under controlled conditions. The cross-language comparison holds the application domain constant, studying HTTP-client libraries across Python, JavaScript, Java, and Go, so that language and ecosystem effects are isolated from what a project does, with a larger project added on the size axis. The pilot on HTTPie validates the methodology and shows caching acting primarily on the dependency-installation stage, with test execution configuration-stable, and shows runner geography dominating configuration-level optimisation by an order of magnitude.

## 7.2 Contributions

Section 1.3.2 previewed five contributions this dissertation set out to make. They are confirmed here, once the full dataset is available, as:

1. The first multi-strategy, cross-project empirical comparison of CI/CD pipeline refinement strategies using standardised carbon measurement (SCI / ISO/IEC 21031:2024).
2. A replicable green CI/CD audit methodology applicable to any GitHub Actions project: an Eco-CI instrumentation pattern (Section 4.4), a pre-study audit checklist (Appendix A), data-collection scripts, and analysis notebooks, all publicly available.
3. A cross-language design that isolates language and ecosystem effects by holding the application domain constant across HTTP-client libraries (Section 3.2.2).
4. Evidence-based recommendations for open-source maintainers on which pipeline configuration changes produce the largest measured carbon reduction relative to implementation effort.
5. A multi-region SCI analysis demonstrating the carbon impact of runner geographic location across five electricity grid regions (Section 5.6).

## 7.3 Limitations

Three limitations bound the findings. Eco-CI captures CPU energy only, so the dependency-installation savings are a lower bound on the true energy reduction. The study is restricted to GitHub Actions on GitHub-hosted `ubuntu-latest` runners, so results may not transfer directly to other CI platforms or runner types. And because measurement uses `workflow_dispatch`, the real-world benefit of C4's path-based trigger filtering, avoiding runs entirely, is not reflected in the per-run energy figures. These are examined in full, alongside the internal, external, and conclusion validity threats, in Section 6.6.

## 7.4 Future Work

Several extensions follow directly from this work: completing the full 30-run statistical analysis across all selected projects; expanding beyond the current language set; collecting consolidation-only data on every multi-workflow project to isolate that effect independently; validating the Eco-CI model-based estimates against hardware RAPL measurements on self-hosted runners; developing a reusable workflow template that reports SCI on every push, making carbon visible to developers continuously, in the spirit of the per-commit visibility Ehlers et al. (2026) demonstrate for containerised systems (Section 2.3.3); and, since test execution is configuration-stable, investigating test parallelisation and selective test execution as the next energy-reduction lever beyond pipeline configuration.

---
