# Chapter 6: Conclusion

## 6.1 Summary of Work

This dissertation addressed the absence of project-level, evidence-based guidance on CI/CD pipeline carbon reduction. Using the Software Carbon Intensity specification (ISO/IEC 21031:2024) and the Eco-CI energy estimation tool, four progressively refined pipeline configurations were experimentally applied to real open-source GitHub Actions projects and their energy consumption measured under controlled conditions.

*[Full summary to be written after results and discussion chapters are complete.]*

---

## 6.2 Contributions

This dissertation makes the following contributions:

1. **First multi-strategy, cross-project empirical comparison** of CI/CD pipeline refinement strategies using standardised carbon measurement (SCI / ISO/IEC 21031:2024)

2. **A replicable green CI/CD audit methodology** applicable to any GitHub Actions project: Eco-CI instrumentation pattern, pre-study audit checklist, data collection scripts, and analysis notebooks, all publicly available

3. **Evidence-based recommendations** for open-source maintainers on which pipeline configuration changes produce the largest measured carbon reductions relative to implementation effort

4. **A multi-region SCI analysis** demonstrating the carbon impact of runner geographic location across five electricity grid regions (Ireland, Germany, Norway, USA, Singapore)

---

## 6.3 Limitations

The primary limitations are: (1) Eco-CI captures CPU energy only, so dependency installation savings are a lower bound on actual energy reductions; (2) the study is restricted to GitHub Actions on GitHub-hosted `ubuntu-latest` runners and results may not transfer directly to other CI platforms; (3) `workflow_dispatch`-based measurement bypasses path filter triggers, meaning the real-world energy saving of C4's trigger filtering is not reflected in per-run measurements.

*[Full limitations discussion to be expanded from Section 5.6.]*

---

## 6.4 Future Work

- **30-run full protocol:** Complete the statistical analysis with the full dataset (Wilcoxon, Bonferroni, Cliff's delta). This is the immediate next step.
- **Multi-project expansion:** Apply the same four configurations to the remaining 5–7 projects across languages (JavaScript/TypeScript, Java, Go) to address RQ2 fully
- **C3 isolation:** Collect C3 consolidation-only data to isolate the consolidation effect independently of caching
- **Self-hosted runner comparison:** Test whether Eco-CI measurements on self-hosted runners (with RAPL validation) confirm the model-based estimates on GitHub-hosted runners
- **Carbon dashboard:** Develop a reusable GitHub Actions workflow template that continuously reports SCI scores as part of the CI pipeline, making carbon visible to developers on every push
- **Test-suite optimisation:** The test execution stage is configuration-stable; future work should investigate test parallelisation and selective test execution as the next energy-reduction lever beyond pipeline configuration

---

## 6.5 Final Statement

*[To be written last, after results and discussion are complete.]*
