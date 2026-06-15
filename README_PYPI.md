# Pepkio HWE Equilibrium Studio

Call the Pepkio hwe-equilibrium-studio REST API from Python to test multiallelic Hardy-Weinberg equilibrium and run Wright-Fisher allele-frequency simulations.

# What It Does

Population genetics QC and teaching workflows need chi-square and exact HWE tests for loci with 2–6 alleles, plus optional Wright-Fisher simulation under selection, drift, mutation, and migration. Rebuilding multinomial expected counts and Guo-Thompson exact tests in a notebook for each locus is slow and error-prone.

This package submits genotype counts, allele frequencies, or biallelic disease incidence to the same Pepkio Tools engine as the hosted [HWE Equilibrium Studio](https://www.pepkio.com/tools/hwe-equilibrium-studio) web calculator. It returns observed-vs-expected genotypes, chi-square and exact p-values, inbreeding F, plain-language verdicts, simulator trajectories, and shareable run permalinks.

Programmatic runs require a network connection and a Pepkio API key. Calculations are not bundled for offline use.

# Features

- Calculator: `genotype_counts`, `allele_frequencies` (expected only), or `carrier_incidence` (biallelic q² → 2pq)
- 2–6 alleles with scalable genotype keys (A1_A1, A1_A2, …)
- Chi-square and Guo-Thompson exact p-values; exact primary when expected counts &lt; 5
- Inbreeding coefficient F and structured `verdict`
- Simulator: selection, drift (Ne), mutation, migration; 1–10000 generations
- Manifest examples: `mn_blood_group`, `cystic_fibrosis_carrier`, `triallelic_counts`, `simulator_fixation`, and more
- CLI: `pepkio-hwe-equilibrium-studio manifest` and `run`
- Configuration via `PEPKIO_API_KEY`, `LOCAL_PEPKIO_API_KEY`, and `PEPKIO_API_BASE_URL`

# Installation

```bash
pip install pepkio-hwe-equilibrium-studio
```

Set an API key with **tools:run** scope before calling `run()`:

```bash
export PEPKIO_API_KEY="your-key"
```

Create a key in your [Pepkio account API keys](https://www.pepkio.com/account/api-keys) settings.

# Quick Example

```python
from pepkio_hwe_equilibrium_studio import PepkioClient

with PepkioClient() as client:
    inp = client.get_example_input("mn_blood_group")
    result = client.run(inp)
    stats = result.result["stats"]
    print(result.permalink)
    print("chi-square p:", stats["chi_square_p"])
    print("verdict:", result.result["verdict"]["title"])
```

CLI:

```bash
pepkio-hwe-equilibrium-studio run --example mn_blood_group
```

Manifest inspection does not require an API key.

# Typical Use Cases

- HWE test for a microsatellite or multiallelic SNP locus from genotype counts
- Carrier frequency from disease incidence (e.g. 1 in 2500 recessive incidence)
- Triallelic or higher-allele contingency tables without hand-built spreadsheets
- Wright-Fisher drift and selection simulations for teaching
- Automated reanalysis of genotype tables in notebooks or CI

# Scientific Background

Under Hardy-Weinberg equilibrium, expected genotype frequencies follow the multinomial expansion from allele frequencies (biallelic: p² + 2pq + q² = 1). Chi-square goodness-of-fit uses df = k(k+1)/2 − k for k alleles. Guo-Thompson exact tests are preferred when expected counts are sparse. F = 1 − H_obs/H_exp measures inbreeding deviation. The simulator uses a discrete-generation Wright-Fisher model.

# Web Application

For researchers who prefer a graphical interface, an interactive [HWE Equilibrium Studio](https://www.pepkio.com/tools/hwe-equilibrium-studio) is available in the browser.

The web interface adds De Finetti ternary plots (2–3 alleles), bar charts (4+ alleles), observed-vs-expected tables, dynamic equation display, PNG/SVG export, CSV download, copy-ready methods text, animated simulator trajectories, and shareable permalinks.

# Documentation and Resources

Source code and issue tracking: [github.com/pepkio/pepkio-hwe-equilibrium-studio](https://github.com/pepkio/pepkio-hwe-equilibrium-studio)

Web calculator: [pepkio.com/tools/hwe-equilibrium-studio](https://www.pepkio.com/tools/hwe-equilibrium-studio)

# About Pepkio

Pepkio develops software tools and provides bioinformatics analysis services for life science research. See [pepkio.com](https://www.pepkio.com/) for additional calculators and [analysis services](https://www.pepkio.com/cro).

# Keywords

Hardy-Weinberg equilibrium, HWE test, multiallelic HWE, population genetics, Guo-Thompson exact test, inbreeding coefficient F, Wright-Fisher simulation, carrier frequency 2pq, genotype counts expected, chi-square Hardy-Weinberg, allele frequency drift, effective population size Ne, microsatellite HWE QC, MN blood group HWE, pepkio-hwe-equilibrium-studio, Python HWE API, REST API population genetics, disease incidence carrier risk, triallelic Hardy-Weinberg test, how to test Hardy-Weinberg for three alleles Python, carrier frequency from 1 in 2500 incidence API, multiallelic genotype HWE without R, Wright-Fisher selection drift simulation script, exact test when expected count below 5, automate Hardy-Weinberg notebook Pepkio, share HWE analysis permalink, population genetics teaching Hardy-Weinberg CLI
