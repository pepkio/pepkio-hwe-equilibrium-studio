# Pepkio HWE Equilibrium Studio

Test Hardy-Weinberg equilibrium for 2–6 alleles, run Wright-Fisher simulations, and obtain carrier frequencies from disease incidence—via browser or Python API.

# Overview

Population genetics workflows routinely ask whether observed genotype counts at a locus match Hardy-Weinberg equilibrium (HWE) expectations under random mating. Microsatellite panels, MHC loci, and multiallelic SNPs can carry three or more alleles, yet many free calculators only handle biallelic cases and return a p-value with no visualization or interpretation. Researchers often turn to R packages such as HardyWeinberg or batch tools like PLINK for genome-wide checks, while students encounter outdated Java applets for basic exercises.

The Pepkio HWE Equilibrium Studio (tool ID: `hwe-equilibrium-studio`) tests Hardy-Weinberg equilibrium for 2–6 alleles from observed genotype counts, derives expected genotype frequencies from allele frequencies, or converts biallelic disease incidence (q²) into carrier frequency (2pq). It reports chi-square and Guo-Thompson exact test p-values, inbreeding coefficient F, and a plain-language verdict. A Wright-Fisher simulator models allele frequency change across generations under selection, genetic drift (effective population size Ne), mutation, and migration.

Researchers use Hardy-Weinberg calculators for microsatellite and multiallelic SNP QC, population genetics teaching, classic examples such as the MN blood group, carrier-risk estimation from disease incidence, and exploring when equilibrium breaks down over time. This repository provides a Python client and CLI for the same calculation engine used by the hosted web application at [https://www.pepkio.com/tools/hwe-equilibrium-studio](https://www.pepkio.com/tools/hwe-equilibrium-studio).

Alternative terms include Hardy-Weinberg test, HWE calculator, Hardy-Weinberg equilibrium test, multiallelic HWE, population genetics calculator, Wright-Fisher simulation, De Finetti plot, inbreeding coefficient F, and carrier frequency calculator.

# Features

- **Calculator mode:** Test HWE for 2–6 alleles from genotype counts, or compute expected genotype proportions from allele frequencies without running a statistical test
- **Carrier incidence mode (biallelic):** Enter disease incidence as proportion (q²), percentage, or one-in-N to obtain carrier frequency 2pq
- **Dual statistical tests:** Chi-square goodness-of-fit and Guo-Thompson exact test; exact test is primary when any expected count is below 5
- **Inbreeding coefficient F:** F = 1 − (H_observed / H_expected) reported with heterozygosity values
- **Plain-language verdict:** Structured `verdict` with level, title, and message (e.g. consistent with HWE, possible deviation)
- **Simulator mode:** Wright-Fisher model with per-allele selection coefficients (fitness = 1 + s), drift (Ne), mutation rate, and migration rate
- **Multiallelic support:** Genotype keys use scalable notation (A1_A1, A1_A2, …) for 2–6 alleles
- **Manifest examples:** `mn_blood_group`, `cystic_fibrosis_carrier`, `cystic_fibrosis_carrier_percent`, `triallelic_counts`, `small_n_warning`, `low_expected_exact_primary`, `simulator_fixation`
- **Python API and CLI:** `PepkioClient`, `get_manifest`, `get_example_input`, `run`, `get_run`
- **Shareable runs:** API returns `permalink` URLs for each completed run
- **Structured JSON output:** `genotypes` (observed vs expected), `stats`, `verdict`, and `trajectory` (simulator)

The hosted web version adds Calculator and Simulator tabs on one page, De Finetti ternary plots for 2–3 alleles (bar charts for 4+ alleles), observed-vs-expected tables, dynamic Hardy-Weinberg equation display, tab-separated batch paste into the genotype grid, PNG and SVG chart export, CSV results download, copy-ready methods text for manuscripts, animated simulator trajectories, and shareable permalinks. No account or install is required for the browser calculator.

# Common Use Cases

- **Microsatellite QC:** Test whether multiallelic microsatellite genotype counts at a single locus depart from HWE before association analysis
- **MHC and multiallelic SNP checks:** Handle 3–6 alleles without rebuilding chi-square tables in a spreadsheet
- **MN blood group teaching:** Reproduce classic biallelic HWE examples (manifest example `mn_blood_group`, N=6129)
- **Carrier frequency from incidence:** Convert cystic fibrosis incidence (e.g. 1 in 2500 or 0.04%) to carrier frequency 2pq (`cystic_fibrosis_carrier`, `cystic_fibrosis_carrier_percent`)
- **Expected genotype proportions:** Enter allele frequencies to see expected counts under HWE without a significance test (`input_kind`: `allele_frequencies`)
- **Sparse contingency tables:** When expected counts fall below 5, the exact test becomes primary (`low_expected_exact_primary` example)
- **Population genetics teaching:** Demonstrate drift, selection, mutation, and migration with the Wright-Fisher simulator
- **Scripted pipelines:** Re-run HWE tests from notebooks, teaching scripts, or CI via the Python client

# Why This Tool Exists

Spreadsheets can compute chi-square by hand but lack multiallelic genotype enumeration, Guo-Thompson exact tests, and Wright-Fisher simulation in one workflow. R packages such as HardyWeinberg support multiallelic tests and ternary plots but require scripting and environment setup. PLINK batch-tests genome-wide data but offers no single-locus visualization or plain-language interpretation for a teaching context. Many free web calculators handle only two alleles and return a p-value with no chart, export, or simulation.

HWE Equilibrium Studio combines multiallelic HWE testing (chi-square and Guo-Thompson exact), F-statistic, De Finetti plots, plain-language verdicts, and a generation simulator with evolutionary forces on one page—free in the browser, with PNG/SVG/CSV export and copy-ready methods text. The Python client runs the same engine from scripts or pipelines via the Pepkio Tools REST API.

# Installation

```bash
pip install pepkio-hwe-equilibrium-studio
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add pepkio-hwe-equilibrium-studio
```

Programmatic runs require a Pepkio API key with **tools:run** scope. Create one at [https://www.pepkio.com/account/api-keys](https://www.pepkio.com/account/api-keys).

```bash
export PEPKIO_API_KEY="your-key"
```

| Variable | Description |
|----------|-------------|
| `PEPKIO_API_KEY` | Production API key |
| `LOCAL_PEPKIO_API_KEY` | Local dev key when base URL points to `tools.localtest.me` |
| `PEPKIO_API_BASE_URL` | Override API host (default: `https://tools.pepkio.com`) |

Manifest inspection does not require an API key.

# Quick Start

### Python

```python
from pepkio_hwe_equilibrium_studio import PepkioClient

with PepkioClient() as client:
    inp = client.get_example_input("mn_blood_group")
    result = client.run(inp)
    print(result.status, result.permalink)
    stats = result.result["stats"]
    verdict = result.result["verdict"]
    print(f"chi-square p = {stats['chi_square_p']:.4f}")
    print(f"exact p = {stats['exact_p']:.4f}")
    print(verdict["title"], "—", verdict["message"])
```

### CLI

```bash
# Manifest (no API key)
pepkio-hwe-equilibrium-studio manifest
pepkio-hwe-equilibrium-studio manifest --examples

# Run a named example (API key required)
pepkio-hwe-equilibrium-studio run --example mn_blood_group
pepkio-hwe-equilibrium-studio run --example cystic_fibrosis_carrier
pepkio-hwe-equilibrium-studio run --example simulator_fixation

# Run custom JSON input
pepkio-hwe-equilibrium-studio run --input-json '{"mode":"calculator","allele_count":2,"input_kind":"genotype_counts","genotype_counts":{"A1_A1":1787,"A1_A2":3039,"A2_A2":1303}}'
```

Options: `--api-key`, `--base-url`, `--label`, `--idempotency-key`.

# Example Output

Running the `mn_blood_group` manifest example against the production API returns:

```json
{
  "run_id": "52505885-bcd6-484d-b55e-fd03c4f9057e",
  "status": "completed",
  "result": {
    "mode": "calculator",
    "allele_count": 2,
    "input_kind": "genotype_counts",
    "total_n": 6129,
    "allele_frequencies": [0.5394844183390439, 0.46051558166095613],
    "genotypes": [
      {"key": "A1_A1", "observed": 1787, "expected": 1783.81, "observed_freq": 0.2916, "expected_freq": 0.2910},
      {"key": "A1_A2", "observed": 3039, "expected": 3045.39, "observed_freq": 0.4958, "expected_freq": 0.4969},
      {"key": "A2_A2", "observed": 1303, "expected": 1299.81, "observed_freq": 0.2126, "expected_freq": 0.2121}
    ],
    "stats": {
      "chi_square": 0.027,
      "chi_square_df": 1,
      "chi_square_p": 0.8695,
      "exact_p": 0.8774,
      "exact_method": "exhaustive",
      "primary_test": "chi_square",
      "f_statistic": 0.0021,
      "heterozygosity_observed": 0.4958,
      "heterozygosity_expected": 0.4969
    },
    "verdict": {
      "level": "consistent",
      "title": "Consistent with HWE",
      "message": "Observed genotype counts are compatible with Hardy-Weinberg equilibrium."
    },
    "carrier_frequency": 0.4969,
    "equation": "0.5395² + 2(0.5395)(0.4605) + 0.4605² = 1",
    "has_blocking_errors": false
  },
  "permalink": "https://tools.pepkio.com/r/52505885-bcd6-484d-b55e-fd03c4f9057e"
}
```

The `small_n_warning` example triggers a warning when total sample size N is below 10. The `low_expected_exact_primary` example switches the primary test to the exact test when expected counts are sparse.

# Scientific Background

**Hardy-Weinberg equilibrium.** For a diploid autosomal locus with k alleles and frequencies p₁, p₂, …, pₖ summing to 1, expected genotype frequencies under random mating follow the multinomial expansion: homozygote AᵢAᵢ has frequency pᵢ²; heterozygote AᵢAⱼ (i < j) has frequency 2pᵢpⱼ. For the biallelic case, p² + 2pq + q² = 1.

**Chi-square test.** Goodness-of-fit statistic χ² = Σ (observed − expected)² / expected, with degrees of freedom df = k(k+1)/2 − k for k alleles.

**Guo-Thompson exact test.** When any expected genotype count falls below 5, the exact test (MCMC or exhaustive enumeration for small tables) provides a more reliable p-value than the asymptotic chi-square approximation. The `exact_mcmc_steps` input controls MCMC steps (default 10000).

**Inbreeding coefficient F.** F = 1 − (H_observed / H_expected), where H is heterozygosity. Positive F suggests excess homozygosity relative to HWE expectations.

**Carrier incidence (biallelic).** For autosomal recessive disease incidence q², carrier frequency is 2pq. Inputs accept proportion (q²), percentage, or one-in-N incidence formats.

**Wright-Fisher simulator.** Discrete-generation model: selection modifies allele frequencies by fitness coefficients (fitness = 1 + s per allele); drift samples from a binomial process with effective population size Ne; mutation and migration shift frequencies each generation. Configurable from 1 to 10000 generations.

**Assumptions.** Diploid organism; autosomal locus; random mating assumed in calculator mode unless evolutionary forces are explicitly modeled in simulator mode.

**Terminology.** Researchers search for Hardy-Weinberg equilibrium test, HWE calculator, multiallelic Hardy-Weinberg, De Finetti plot, Guo-Thompson exact test, Wright-Fisher simulation, inbreeding coefficient, carrier frequency from disease incidence, and population genetics calculator—these workflows are what HWE Equilibrium Studio addresses.

# Frequently Asked Questions

**What is Hardy-Weinberg equilibrium?**
Hardy-Weinberg equilibrium describes the expected genotype frequencies at a locus when allele frequencies are stable and mating is random. For two alleles with frequencies p and q, genotype frequencies are p², 2pq, and q².

**How do I test Hardy-Weinberg equilibrium for more than two alleles?**
Set `allele_count` from 2 to 6 and provide observed counts for each genotype key (e.g. A1_A1, A1_A2, A2_A2, A1_A3, …). The tool computes expected counts under HWE and runs chi-square and exact tests.

**What is the Guo-Thompson exact test?**
It is a permutation-based exact test for HWE that does not rely on the chi-square asymptotic approximation. This tool uses it when expected counts are small; it becomes the primary test when any expected count is below 5.

**When should I use chi-square vs the exact test?**
Chi-square is reported for all calculator runs. When expected counts are adequate, chi-square is primary. When any expected count falls below 5, the exact test becomes primary (`primary_test` in output).

**What is the inbreeding coefficient F?**
F measures deviation from random mating: F = 1 − (observed heterozygosity / expected heterozygosity under HWE). Positive F indicates excess homozygosity.

**What is a De Finetti plot?**
A ternary plot showing genotype frequencies for biallelic or triallelic loci relative to Hardy-Weinberg expectations. The web application renders De Finetti plots for 2–3 alleles and bar charts for 4+ alleles.

**How do I calculate carrier frequency from disease incidence?**
For biallelic recessive incidence q², set `input_kind` to `carrier_incidence` and provide `carrier` with format `proportion`, `percentage`, or `one_in_n`. The tool returns carrier frequency 2pq. See manifest examples `cystic_fibrosis_carrier` and `cystic_fibrosis_carrier_percent`.

**What genotype count format does the API expect?**
An object with keys like `A1_A1`, `A1_A2`, `A2_A2` for biallelic data, expanding for higher allele counts. The web UI also supports tab-separated batch paste.

**Can I enter allele frequencies instead of counts?**
Yes. Set `input_kind` to `allele_frequencies` with a frequency vector summing to 1. The calculator returns expected genotype proportions without running a significance test.

**What does the simulator mode do?**
Simulator mode runs a Wright-Fisher model across generations with selection coefficients, effective population size (Ne) for drift, mutation rate, and migration rate. Output includes a `trajectory` array of allele frequencies per generation.

**What is effective population size (Ne)?**
Ne is the size of an ideal population that would experience the same rate of genetic drift as the population being modeled. Lower Ne increases random allele frequency fluctuation.

**How many generations can I simulate?**
From 1 to 10000 generations (`generations` input). See the `simulator_fixation` manifest example for strong selection driving fixation.

**What happens with very small sample sizes?**
Total N below 10 triggers a warning (`small_n_warning` example). Results should be interpreted cautiously with small samples.

**Does the Python client work offline?**
No. Calculator and simulator arithmetic run on Pepkio servers via the REST API. A network connection and API key are required for `run()`. Manifest fetch works without a key.

**How do I export results for a manuscript?**
The web application supports PNG and SVG chart export, CSV download of observed and expected counts with p-values and F-statistic, and a copy-ready methods sentence. The API returns structured JSON including `genotypes`, `stats`, and `verdict`.

**What is the MN blood group example?**
Classic biallelic HWE data (N=6129) that is consistent with equilibrium. Run manifest example `mn_blood_group` to reproduce.

**How does this compare to PLINK for HWE testing?**
PLINK batch-tests HWE across genome-wide markers. HWE Equilibrium Studio focuses on a single locus with 2–6 alleles, visualization, interpretation, and simulation—suited for teaching, QC at one locus, and carrier-risk calculations.

**Can I reproduce results with a fixed random seed?**
Set `random_seed` for the exact test MCMC and simulator. The `simulator_fixation` example uses `random_seed: 7`.

# Web Application

For researchers who prefer a graphical interface, an interactive [HWE Equilibrium Studio](https://www.pepkio.com/tools/hwe-equilibrium-studio) is available in the browser.

The web version provides Calculator and Simulator tabs on one page, allele count selection from 2 to 6, genotype count grids with tab-separated batch paste, allele-frequency mode for expected proportions only, biallelic carrier incidence input (proportion, percentage, or one-in-N), observed-vs-expected tables, chi-square and exact test p-values with F-statistic, plain-language verdict badges, De Finetti ternary plots for 2–3 alleles and bar charts for 4+ alleles, dynamic Hardy-Weinberg equation display, Wright-Fisher simulation with selection/drift/mutation/migration sliders, animated frequency trajectories, PNG and SVG export, CSV results download, copy-ready methods text, and shareable permalinks. No account or install is required.

Use the web tool for interactive charts and export; use this Python package for scripted analysis, teaching automation, or pipeline integration.

# Related Resources

GitHub Repository: [https://github.com/pepkio/pepkio-hwe-equilibrium-studio](https://github.com/pepkio/pepkio-hwe-equilibrium-studio)

PyPI Package: [https://pypi.org/project/pepkio-hwe-equilibrium-studio/](https://pypi.org/project/pepkio-hwe-equilibrium-studio/)

Web Application: [https://www.pepkio.com/tools/hwe-equilibrium-studio](https://www.pepkio.com/tools/hwe-equilibrium-studio)

# About Pepkio

[Pepkio](https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and [analysis services](https://www.pepkio.com/cro). Explore additional calculators on the Pepkio website.

# License

No license file is present in this repository at the time of writing.

# Keywords

Hardy-Weinberg equilibrium, HWE calculator, HWE test, multiallelic Hardy-Weinberg, population genetics calculator, Hardy-Weinberg test online, genotype frequency calculator, chi-square Hardy-Weinberg, Guo-Thompson exact test, inbreeding coefficient F, Wright-Fisher simulation, De Finetti plot, allele frequency simulation, genetic drift calculator, effective population size Ne, carrier frequency calculator, disease incidence q squared, 2pq carrier risk, cystic fibrosis carrier frequency, MN blood group Hardy-Weinberg, microsatellite HWE test, MHC Hardy-Weinberg, multiallelic SNP equilibrium, population genetics teaching tool, Hardy-Weinberg equilibrium p-value, exact test Hardy-Weinberg, heterozygosity calculator, genotype count expected frequency, pepkio-hwe-equilibrium-studio, Python Hardy-Weinberg API, REST API population genetics, HardyWeinberg R alternative, PLINK single locus HWE, Hardy-Weinberg equilibrium formula, p squared 2pq q squared, multinomial genotype expansion, selection coefficient simulation, migration rate allele frequency, mutation rate population genetics, Hardy-Weinberg deviation test, excess homozygosity F statistic, population genetics QC locus, triallelic Hardy-Weinberg, ternary plot population genetics, how to test Hardy-Weinberg equilibrium for three alleles, calculate carrier frequency from disease incidence 1 in 2500, when to use exact test instead of chi-square HWE, interpret inbreeding coefficient F population genetics, simulate genetic drift over 200 generations, Wright-Fisher model selection drift mutation, export Hardy-Weinberg results for manuscript methods section, multiallelic genotype count spreadsheet to HWE test, Hardy-Weinberg equilibrium teaching problem MN blood group, test microsatellite locus Hardy-Weinberg without R, Python script Hardy-Weinberg equilibrium API, share Hardy-Weinberg analysis permalink, De Finetti plot biallelic genotype frequencies, expected genotype counts from allele frequencies HWE, small sample Hardy-Weinberg warning N less than 10, sparse contingency table exact test primary, automate population genetics homework Hardy-Weinberg, compare observed expected genotype counts table, Hardy-Weinberg equilibrium browser calculator no install
