# Answers to Supervisor Questions

Use this document to prepare for supervisor meetings. Written in plain language.

---

## Q1: What exactly are you doing, in simple words?

### The short version (30 seconds)

Every time a developer pushes code to GitHub, an automated pipeline runs — it downloads packages, runs tests, checks code quality. That takes electricity. I am measuring how much electricity (and therefore how much carbon) different pipeline setups use, and comparing which setup is the most efficient.

### The slightly longer version (2 minutes)

I took a real open-source project (HTTPie CLI — a Python HTTP tool with 34,000 GitHub stars) and set up its CI/CD pipeline in four different ways:

- **C1 — Baseline:** The original setup. Every run downloads all packages from scratch.
- **C2 — Caching:** Same setup, but now it saves downloaded packages so the next run doesn't re-download them.
- **C3 — Consolidation:** Three separate workflow files merged into one, eliminating repeated setup steps.
- **C4 — Combined:** Caching + consolidation + only run when relevant files change.

I run each version 30 times on GitHub's servers and measure the energy used each time using a tool called Eco-CI. I convert that energy into a carbon score (grams of CO₂ per pipeline run) using the international standard ISO/IEC 21031:2024. Then I compare the four versions statistically.

The question I'm answering: **Which change saves the most carbon, and by how much?**

---

## Q2: How is this different from existing research?

### What others have done

| Paper | What they did | What they didn't do |
|---|---|---|
| Saavedra et al. (2025) | Estimated carbon for ALL of GitHub Actions (456 tonnes CO₂ in 2024) | Didn't tell developers what to actually change |
| de Medeiros et al. (2025) | Measured which CI stage uses the most energy (tests use most) | Didn't test any changes or compare strategies |
| Bouzenia & Pradel (2024) | Counted how many repos use caching (only 32.9%) | Measured time savings, not carbon |
| IEEE (2026) | Found caching saves 30–90% energy in Java projects | Only Java, only caching, no carbon score (just kWh) |
| Claßen et al. (2023) | Showed running pipelines at night (low-carbon grid time) saves 25% | Different approach — doesn't change the pipeline itself |

### What nobody has done — until this dissertation

Nobody has:
1. **Experimentally applied** multiple strategies (not just observed who uses them)
2. **Compared them against each other** on the same project
3. **Measured actual carbon** using the official ISO standard (SCI)
4. **Tested whether it works the same** across different project types (RQ2)

The 2026 IEEE paper is the closest — it measured caching in 204 Java projects. But it:
- Only looked at one strategy (caching)
- Only studied Java
- Did not produce SCI carbon scores — just energy in kWh with no carbon unit

This dissertation is the first to run a proper controlled experiment comparing **three strategies, cross-language, with standardised carbon measurement**.

### The analogy

Imagine researchers have been counting how much fuel cars use (aggregate stats) and measuring how fast engines run (profiling). Nobody has actually taken the same car, tested three different driving techniques, and produced a fuel-efficiency score per kilometre.

That's what this dissertation does — but for CI/CD pipelines and carbon.

---

## Q3: What are the outcomes and benefits? (Simple version)

### For a developer

After reading this dissertation, a developer can look at a table and see:

> "If I add two lines of YAML to my workflow file (enable caching), I will save approximately X grams of CO₂ per pipeline run. My project runs 50 times a day, so that is X × 50 × 365 = Y kg CO₂ per year."

Right now, no such table exists anywhere in published research. Developers have no way to justify or quantify these changes.

### For the field

- The first evidence that these strategies work (measured, not estimated)
- A reusable methodology — any developer can apply the same Eco-CI + SCI approach to their own pipeline in a day
- A ranked list: which strategy saves the most carbon per hour of implementation work

---

## Q4: How does Eco-CI calculate carbon? (The formula)

This is a two-step process.

### Step 1: Energy (Joules)

```
Energy = Power × Time
```

Where:
- **Power** is estimated from CPU utilisation %
  - Eco-CI reads CPU usage every second from the GitHub runner
  - It looks up that CPU model in the SPECpower database (a standard benchmark that measures server power at different load levels)
  - SPECpower says: "at 30% CPU load, this Intel Xeon uses 4.2 Watts"
  - Power × Duration = Joules
- This gives energy per pipeline stage (e.g., dependency installation = 104 J, test execution = 367 J)

### Step 2: Carbon (ISO/IEC 21031:2024 — SCI formula)

```
SCI = (E × I) + M
```

Where:
- **E** = Energy in kWh  
  (Joules ÷ 3,600,000 = kWh — there are 3.6 million joules in 1 kWh)
- **I** = Carbon intensity of the electricity grid (gCO₂eq per kWh)
  - Eco-CI reports **472 gCO₂eq/kWh** for GitHub's Azure runners (this is their measured value)
  - For comparison: Ireland's grid is 345, Norway's is 25 (mostly hydroelectric)
- **M** = Embodied carbon — the carbon already "spent" manufacturing the server hardware, spread across its lifetime
  - Eco-CI includes this in its SCI output automatically
- **Result** = gCO₂eq per CI run

### Worked example (from real pilot data)

The C2 test matrix (3 Python versions) used **1,484 Joules** per run.

```
Energy in kWh = 1,484 / 3,600,000 = 0.000412 kWh
Carbon (Ireland) = 0.000412 × 345 = 0.142 gCO₂eq per run
```

C4 used **1,378 Joules**, so:
```
Carbon (Ireland) = (1,378 / 3,600,000) × 345 = 0.132 gCO₂eq per run
```

Difference: **0.010 gCO₂eq saved per run** from C2 to C4. At 10,000 runs/year = 100 gCO₂/year saved.

### Why Eco-CI is not exact (limitation — be honest about this)

- It only measures **CPU energy**, not RAM or network
- It uses a **model** (SPECpower), not a direct power meter
- GitHub doesn't tell us which exact server each run uses — Eco-CI makes a best estimate

But: any bias from the model affects all four configurations equally, so the **relative comparison** (C1 vs C2 vs C3 vs C4) is still valid.

---

## Q5: Is 1 project (HTTPie) enough for the dissertation?

### Honest answer

For a 2-week progress check: yes, one project with real data is excellent progress.

For the final dissertation: no — the research questions require multiple projects to answer RQ2 ("does it work the same across different project types?"). The plan is 6–8 projects spanning Python, Java, JavaScript/TypeScript.

The HTTPie study is the **pilot** that proves the methodology works. The remaining projects are the **scale-up** that makes the findings generalisable.

### What to say to the supervisor

"The HTTPie pilot demonstrates the complete methodology end-to-end — all four configurations instrumented, Eco-CI running, real data collected, analysis notebook ready. The next phase is applying the same methodology to 5–7 additional projects across different languages to answer RQ2."
