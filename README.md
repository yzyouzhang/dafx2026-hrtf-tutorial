# dafx2026-hrtf-tutorial

Materials for the DAFx 2026 tutorial **"From Neural Fields to Personalized Spatial Audio: A Hands-on Tutorial on HRTF Modeling"**, presented by [You (Neil) Zhang](https://yzyouzhang.com) (Dolby Laboratories) and [Yoshiki Masuyama](https://yoshiki-masuyama.com) (MERL).

This tutorial introduces neural fields as a continuous representation for head-related transfer functions (HRTFs), and walks through their evolution toward practical systems for sparse-measurement upsampling and personalization.

## Run in Colab

The four hands-on notebooks each open directly in Google Colab — no local setup required. The first two cells clone this repo and install dependencies automatically.

| Notebook | Open in Colab |
|---|---|
| 00 — Data & Sampling | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yzyouzhang/dafx2026-hrtf-tutorial/blob/main/00_data_and_sampling.ipynb) |
| 01 — Minimal Neural Field | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yzyouzhang/dafx2026-hrtf-tutorial/blob/main/01_minimal_neural_field.ipynb) |
| 02 — NIIRF Filter Field | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yzyouzhang/dafx2026-hrtf-tutorial/blob/main/02_niirf_filter_field.ipynb) |
| 03 — RANF Upsampling | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yzyouzhang/dafx2026-hrtf-tutorial/blob/main/03_upsampling_ranf.ipynb) |

Sessions are ephemeral — if Colab disconnects or times out, re-run the first two cells (clone + install) to restore state.

> Badges currently point at the `main` branch (placeholder); they'll be re-pointed to a release tag (e.g. `v1.0-dafx26`) closer to the tutorial date.

## Repository structure

```
dafx2026-hrtf-tutorial/
├── 00_data_and_sampling.ipynb        # loading SONICOM data, directional sampling
├── 01_minimal_neural_field.ipynb     # core HRTF Field formulation (SIREN + gradient-inferred latents)
├── 02_niirf_filter_field.ipynb       # NIIRF: differentiable IIR filter cascade (single-subject)
├── 03_upsampling_ranf.ipynb          # RANF: retrieval-augmented upsampling
├── src/
│   ├── data.py                       # SOFA loading, synthetic data, preprocessing helpers
│   └── iir_downstream.py             # differentiable IIR cascade, ported from the official NIIRF repo
├── data/
│   └── sonicom/                      # SONICOM .sofa files (notebooks 00–03)
├── requirements.txt
└── README.md
```

The tutorial sequence is `00 → 01 → 02 → 03`.

## Setup

```bash
conda create -n dafx-hrtf python=3.10 -y
conda activate dafx-hrtf
pip install -r requirements.txt jupyterlab ipykernel
```

Then launch, from the repo root:

```bash
jupyter lab .
```

> `requirements.txt` intentionally omits `jupyterlab`/`ipykernel`: it's also what the Colab bootstrap cell installs, and Colab already ships its own pinned Jupyter kernel stack — installing a newer one on top of it causes pip dependency-resolver conflicts (harmless there, but noisy). Install them separately for local use, as above.

## Data

The notebooks use the [SONICOM HRTF Dataset](https://www.sonicom.eu/tools-and-resources/hrtf-dataset/) (200 subjects total, CC BY-SA license). 30 real subjects (`p0001`–`p0030`) are bundled directly under `data/sonicom/`, so everything runs out of the box with no separate download. Each subject's `.sofa` file has 828 measured directions — see the note in `00_data_and_sampling.ipynb` on why that's not the 793 the dataset paper quotes.

To use a different or larger subset of SONICOM subjects:

1. Download additional `.sofa` files from the [SONICOM dataset portal](https://transfer.ic.ac.uk:9090/#/2022_SONICOM-HRTF-DATASET/).
2. Place them under `data/sonicom/`.
3. Each notebook auto-detects `.sofa` files in `SOFA_DIR`; `00_data_and_sampling.ipynb` also accepts a single-file override via `SOFA_PATH`.

## Background reading

Official materials for the papers covered in the tutorial:

- **HRTF Field** — [github.com/yzyouzhang/hrtf_field](https://github.com/yzyouzhang/hrtf_field)
- **NIIRF** — [github.com/merlresearch/neural-IIR-field](https://github.com/merlresearch/neural-IIR-field)
- **RANF** — [github.com/merlresearch/ranf-hrtf](https://github.com/merlresearch/ranf-hrtf)
- **SuDaField** — [github.com/merlresearch/SuDaField](https://github.com/merlresearch/SuDaField)

## Citation

If you use these materials, please cite the original papers above and this tutorial.

## License

Except as noted below, released under MIT license as found in [LICENSE.md](LICENSE.md) file:
```
Copyright (c) 2026 You (Neil) Zhang and Yoshiki Masuyama

SPDX-License-Identifier: MIT
```

The following file:
* `src/iir_downstream.py`

is copied from https://github.com/merlresearch/neural-IIR-field and was adapted from https://github.com/yoyolicoris/hrtf-notebooks (license included in LICENSES/MIT.md):
```
Copyright (c) 2023 Mitsubishi Electric Research Laboratories (MERL)
Copyright (c) 2023 Chin-Yun Yu
```

SOFA files for the SONICOM dataset
* `data/sonicom/*.sofa`

are copied from https://sofacoustics.org/data/database/axd/ and are licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
