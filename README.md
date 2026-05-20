# Optimal Retirement and Aged-Care Decisions under Australian Policy

A stochastic dynamic programming model of optimal consumption, savings, and home-downsizing decisions for Australian retirees. The model jointly accounts for the Age Pension, the Commonwealth Home Support Programme (CHSP), Home Care Packages (HCP), and Residential Aged Care Facilities (RACF), and is solved via backward induction with Epstein–Zin recursive utility.

---

## Table of contents

- [Model overview](#model-overview)
- [Repository structure](#repository-structure)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Running the baseline](#running-the-baseline)
- [Sensitivity analysis](#sensitivity-analysis)
  - [Initial wealth `W`](#1-initial-wealth-w)
  - [Risk aversion `gamma`](#2-risk-aversion-gamma)
  - [Bequest motive `b`](#3-bequest-motive-b)
  - [Elasticity of intertemporal substitution (EIS)](#4-elasticity-of-intertemporal-substitution-eis)
  - [Suggested batch workflow](#suggested-batch-workflow)
- [Output files](#output-files)
- [Citation](#citation)
- [License](#license)

---

## Model overview


A retiree chooses non-durable consumption `C_t` and a downsizing strategy over a 40-period (annual) horizon, taking as given:

- **Health states** `Hstate ∈ {1, 2, 3, 5}`: 1 and 2 are healthy / mildly assisted living at home; 3 is on a Home Care Package; 5 is in residential aged care. Transitions follow a non-homogeneous Markov chain (`National_Transit.pkl`).
- **Wealth split**: total initial wealth `W` is divided between liquid wealth and housing equity `H` by the ratio `alpha / (1+alpha)`.
- **Macroeconomic uncertainty**: interest rates, CPI, and house prices evolve along scenario grids (`ME_grid_ir.pkl`, `ME_grid_cpi.pkl`, `ME_grid_H.pkl`) indexed by an "economic index" `EI_t` that drifts up or down each period.
- **Preferences**: Epstein–Zin recursive utility with risk aversion `gamma`, the inverse of the elasticity of intertemporal substitution `rho` (so EIS = 1/`rho`), a bequest weight `b`, and discount factor `beta`.

The Bellman equation is solved by backward induction in two stages:

1. **`3_5.ipynb`** — solves health states 3 and 5 on a wide wealth grid and saves `Dict_35`.
2. **`1_2.ipynb`** — uses `Dict_35` as continuation values and solves states 1 and 2, saving `Dict_12`.
3. **`Combined.ipynb`** — simulates 20,000 life trajectories using the optimal policies and produces summary statistics.


For specific parameter settings, please refer to our paper. In the event of any discrepancies, the paper shall prevail.
```
@article{Lyu2026Financing,
  author  = {Lyu, Lingfeng and Shen, Yang and Sherris, Michael and Ziveyi, Jonathan},
  title   = {Financing aged care with home equity allowing for government age pension and aged care support},
  journal = {Insurance: Mathematics and Economics},
  year    = {2026},
  volume  = {126},
  pages   = {103193},
  issn    = {0167-6687},
  doi     = {10.1016/j.insmatheco.2025.103193}
}
```

---

## Repository structure

All files live at the repository root so that the relative paths inside the notebooks (e.g. `open('National_Transit.pkl', 'rb')`) work without modification.

```
.
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
│  # Notebooks (run in this order)
├── 3_5.ipynb
├── 1_2.ipynb
├── Combined.ipynb
│
│  # Source modules
├── age_pension.py
├── AIP.py
├── Calibrated_Variables.py
├── CHSP_GRandF.py
├── HCP_GRandF.py
├── RC_GRandF.py
├── FIstatus.py
├── DeltaW.py
├── comInterp.py
├── updown_prep.py
│
│  # Input data (committed)
├── National_Transit.pkl
├── ME_grid_ir.pkl
├── ME_grid_cpi.pkl
├── ME_grid_H.pkl
│
│  # Generated outputs (gitignored — produced by the notebooks)
├── Dict_35
└── Dict_12
```

---

## Installation

```bash
git clone https://github.com/<your-org>/<this-repo>.git
cd <this-repo>
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt`:
```
numpy
pandas
scipy
matplotlib
joblib
jupyter
```

The backward induction is parallelised with `joblib` (`n_jobs=25` in the baseline notebooks). On smaller machines, lower this in the relevant cells.

---

## Dependencies

### Source modules
| File | Purpose |
|---|---|
| `age_pension.py` | Means-tested Age Pension formula |
| `AIP.py` | `xiatt()` age-in-place utility weight, `Hstate2IRACF()` |
| `Calibrated_Variables.py` | `return_calib_var(alpha)` — baseline `W`, `H`, `tau` arrays, leasing flag |
| `CHSP_GRandF.py` | `GRandF_CHSP(W)` |
| `HCP_GRandF.py` | `GRandF_HCP(W, level)` for levels `'low'`, `'medium'`, `'high'` |
| `RC_GRandF.py` | `GRandF_RC(W, H, Leasing)` |
| `FIstatus.py` | `I_status(W, H, Hstate)`, `F_status(W, H, Hstate)` |
| `DeltaW.py` | `Delta_W_status(...)` wealth adjustment on health transitions |
| `comInterp.py` | `compress_interp(...)` |
| `updown_prep.py` | `derivatives_tp1`, `direct2EI`, `Hstate2Cf`, `reVC`, `Compare35` |

### Input data files
| File | Description |
|---|---|
| `National_Transit.pkl` | Period-specific 4×4 health-state transition matrices |
| `ME_grid_ir.pkl` | Macroeconomic scenarios for interest rates |
| `ME_grid_cpi.pkl` | Macroeconomic scenarios for CPI |
| `ME_grid_H.pkl` | Macroeconomic scenarios for house prices |

### Generated output files
`Dict_35` and `Dict_12` are **not** committed — they are produced by running `3_5.ipynb` and `1_2.ipynb` respectively and can be regenerated at any time.

---

## Running the baseline

The notebooks must be executed **in order** because each consumes the output of the previous step:

```bash
jupyter nbconvert --to notebook --execute 3_5.ipynb
jupyter nbconvert --to notebook --execute 1_2.ipynb
jupyter nbconvert --to notebook --execute Combined.ipynb
```

Expected runtime on a 32-core machine: ~30 min for `3_5.ipynb`, ~45 min for `1_2.ipynb`, ~5 min for `Combined.ipynb`.

Outputs `Dict_35` and `Dict_12` are written to the current working directory.

---

## Sensitivity analysis

The model has four economically interesting parameters. The recipe for each is the same:

1. Copy the three notebooks into a new experiment folder (e.g. `experiments/sensitivity/gamma_7/`).
2. Edit the parameter in **every notebook in which it appears** (listed below — they are *not* consolidated in one place in the current code).
3. Run the three notebooks in order.
4. Save the resulting `Dict_12`, `Dict_35`, and any simulation outputs into the experiment folder.

> **Important.** `gamma`, `b`, and `rho` are defined separately in each notebook. You must edit them in **every notebook that defines them** for a clean comparison. `theta = (1 - gamma) / (1 - rho)` must be updated whenever you change `gamma` or `rho`.

### 1. Initial wealth `W`

**What it is.** Total wealth at retirement (liquid + housing), split into housing equity `H = W·α/(1+α)` and liquid wealth `W/(1+α)`.

**Where to change it.** Edit `return_calib_var()`:
- `1_2.ipynb` — Cell 2 (`W = 560000`)
- `Combined.ipynb` — Cell 3 (`W = 560000`)
- *Optionally* `3_5.ipynb` — Cell 2 (`W = 1200000`). This sets the **upper bound of the wealth grid** for states 3 and 5; keep it at least as large as the largest `W` you intend to test, so that simulations never extrapolate.

**Baseline.** `W = 560,000` AUD.

**Grid.** `W ∈ {134000, 560000, 1210000}` — covers a low-wealth retiree relying mainly on the Age Pension, a representative middle-wealth retiree, and a high-wealth retiree near the upper means-test threshold.

**What to look for.** Downsizing probability, share of life spent in HCP vs. RACF, sensitivity of pension receipts.

### 2. Risk aversion `gamma`

**What it is.** Coefficient of relative risk aversion in the Epstein–Zin recursion. Higher `gamma` → more aversion to consumption and bequest gambles.

**Where to change it.** Search each notebook for `gamma = 5`:
- `3_5.ipynb` — Cell 4
- `1_2.ipynb` — Cell 3
- `Combined.ipynb` (if it is also defined there)

**Also update `theta`** in the same cell: `theta = (1 - gamma) / (1 - rho)`.

**Baseline.** `gamma = 5`.

**Grid.** `gamma ∈ {2, 5, 7}`.

**What to look for.** Precautionary saving (consumption profiles), willingness to retain housing as a buffer against late-life care shocks.

### 3. Bequest motive `b`

**What it is.** Weight on terminal wealth in the bequest term. Higher `b` → stronger motive to leave an estate.

**Where to change it.** Same cells as `gamma`:
- `3_5.ipynb` — Cell 4 (`b = 2`)
- `1_2.ipynb` — Cell 3 (`b = 2`)
- `Combined.ipynb` (if also defined)

**Baseline.** `b = 2`.

**Grid.** `b ∈ {0, 2, 10}`. `b = 0` shuts the bequest channel off entirely and is a useful diagnostic case (consumption should rise late in life); `b = 10` is a strong bequest motive.

**What to look for.** Late-life consumption levels, terminal wealth distribution, propensity to keep the home rather than sell to fund consumption.

### 4. Elasticity of intertemporal substitution (EIS)

**What it is.** EIS = `1 / rho`. It governs willingness to substitute consumption across time independently of risk aversion, which is the key separation Epstein–Zin gives you over CRRA.

**Where to change it.** Search each notebook for `rho = 2`:
- `3_5.ipynb` — Cell 4
- `1_2.ipynb` — Cell 3
- `Combined.ipynb` (if also defined)

**Also update `theta`** in the same cell: `theta = (1 - gamma) / (1 - rho)`.

**Baseline.** `rho = 2`, so EIS = 0.5.

**Grid.** `EIS ∈ {0.2, 0.5, 0.7}` → `rho ∈ {5, 2, 1/0.7}` (≈ 1.4286).

**What to look for.** Slope of the consumption profile (lower EIS → flatter consumption), sensitivity of consumption to interest-rate shocks.

### Suggested batch workflow

To run a sensitivity sweep cleanly, parameterise the notebooks rather than editing them by hand each time. One option is to keep all preference parameters in a single config file imported by every notebook:

```python
# params.py
W          = 560_000
gamma      = 5
rho        = 2
b          = 2
beta       = 0.96
theta      = (1 - gamma) / (1 - rho)
```

Then replace every literal in the notebooks with `from params import ...` and drive sweeps from a wrapper script:

```python
# run_sensitivity.py
import itertools, subprocess, shutil
from pathlib import Path

grid = {
    "gamma": [2, 5, 7],
    "b":     [0, 2, 10],
    "rho":   [1/0.2, 1/0.5, 1/0.7],          # EIS = 0.2, 0.5, 0.7
    "W":     [134_000, 560_000, 1_210_000],
}

for combo in itertools.product(*grid.values()):
    gamma, b, rho, W = combo
    outdir = Path(f"experiments/sensitivity/g{gamma}_b{b}_rho{rho:.4f}_W{W}")
    outdir.mkdir(parents=True, exist_ok=True)

    # 1. Write params.py for this run
    Path("params.py").write_text(
        f"W={W}\ngamma={gamma}\nrho={rho}\nb={b}\nbeta=0.96\n"
        f"theta=(1-{gamma})/(1-{rho})\n"
    )

    # 2. Execute the three notebooks in order
    for nb in ["3_5.ipynb", "1_2.ipynb", "Combined.ipynb"]:
        subprocess.run(
            ["jupyter", "nbconvert", "--to", "notebook",
             "--execute", nb, "--output-dir", str(outdir)],
            check=True,
        )

    # 3. Move the generated dictionaries into the experiment folder
    for f in ["Dict_12", "Dict_35"]:
        if Path(f).exists():
            shutil.move(f, outdir / f)
```

A full Cartesian sweep over the four grids is 3⁴ = **81 runs** and is heavy. For most papers a **one-factor-at-a-time** design around the baseline (4 parameters × 2 off-baseline values = 8 additional runs, plus the baseline) is enough to characterise the model.

---

## Output files

Each run produces two pickled dictionaries:

- **`Dict_35`** — for each of 25 housing/liquid splits `alpha`, the value functions `V3, V5` and consumption policies `C3, C5` on the wealth grid for `t = 1, …, 40`.
- **`Dict_12`** — same structure for states 1 and 2.

To load and inspect:

```python
import pickle
with open("Dict_12", "rb") as f:
    D = pickle.load(f)

# D[i] = results for the i-th alpha grid point
# D[i]['WC1'][t][EI_tm1] is an interp1d giving C(W) for state 1
```

`Combined.ipynb` produces:

- `Dict_arr_W` — 20,000 wealth trajectories
- `Dict_arr_C` — 20,000 consumption trajectories
- `Dict_arr_HS` — 20,000 health-state trajectories
- `Dict_arr_S` — downsizing decisions

Use these to compute means, percentiles, and survival-conditional averages for any comparison across experiments.

---


## License

<Choose a license — MIT and Apache-2.0 are the most common for academic code. Add the chosen license text in `LICENSE`.>
