# Pepkio HWE Equilibrium Studio

Container image for the Pepkio Hardy-Weinberg CLI—multiallelic HWE tests and Wright-Fisher simulations via the hosted API.

# What It Does

The image runs `pepkio-hwe-equilibrium-studio`, a client for the Pepkio HWE Equilibrium Studio REST API. Submit genotype counts, allele frequencies, or biallelic disease incidence; receive chi-square and Guo-Thompson exact p-values, inbreeding F, plain-language verdicts, and simulator allele-frequency trajectories.

Typical workflows include microsatellite HWE QC, carrier-risk estimation from disease incidence, population genetics teaching, and scripted Wright-Fisher simulations. Calculator logic runs on Pepkio servers; provide a network connection and API key for `run` commands.

# Features

- Calculator: genotype counts, allele frequencies (expected only), or carrier incidence (biallelic)
- 2–6 alleles; chi-square and exact tests; F-statistic and verdict
- Wright-Fisher simulator: selection, drift (Ne), mutation, migration
- Named manifest examples (`mn_blood_group`, `cystic_fibrosis_carrier`, `simulator_fixation`, etc.)
- Manifest inspection without an API key

# Quick Start

```bash
docker pull pepkio/hwe-equilibrium-studio:0.1.0
docker run --rm -e PEPKIO_API_KEY="your-key" pepkio/hwe-equilibrium-studio:0.1.0 \
  pepkio-hwe-equilibrium-studio run --example mn_blood_group
```

Manifest only (no API key):

```bash
docker run --rm pepkio/hwe-equilibrium-studio:0.1.0 \
  pepkio-hwe-equilibrium-studio manifest --examples
```

Set `PEPKIO_API_BASE_URL` to override the API host (default: `https://tools.pepkio.com`). Create an API key with **tools:run** scope at https://www.pepkio.com/account/api-keys.

# Quick Example

```bash
docker run --rm -e PEPKIO_API_KEY="$PEPKIO_API_KEY" pepkio/hwe-equilibrium-studio:0.1.0 \
  pepkio-hwe-equilibrium-studio run --example cystic_fibrosis_carrier
```

# Typical Use Cases

- HWE testing from genotype counts in CI or pipeline runners
- Carrier frequency from recessive disease incidence in fixed environments
- Triallelic contingency tables without local R installs
- Wright-Fisher simulation for teaching labs with reproducible containers
- Manifest inspection in deployment smoke tests

# Scientific Background

Hardy-Weinberg expected genotype frequencies follow the multinomial expansion from allele frequencies. Chi-square tests use df = k(k+1)/2 − k. Guo-Thompson exact tests are primary when expected counts are below 5. F = 1 − H_obs/H_exp measures inbreeding. The simulator uses a Wright-Fisher discrete-generation model.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/hwe-equilibrium-studio

The web UI adds De Finetti plots (2–3 alleles), bar charts (4+ alleles), observed-vs-expected tables, PNG/SVG export, CSV download, copy-ready methods text, animated simulator trajectories, and shareable permalinks.

# Documentation and Resources

GitHub Repository (source and Dockerfile): https://github.com/pepkio/pepkio-hwe-equilibrium-studio

Web Application: https://www.pepkio.com/tools/hwe-equilibrium-studio

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).
