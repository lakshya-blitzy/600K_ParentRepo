# Parent Repository — Modular Sum/Average Demo

## Overview

This repository is a minimal, dependency-free Python demonstration of modular
arithmetic helpers (`service.py`) driven by a small console entry point
(`app.py`). It also serves as a worked example of **nested Git submodule
composition**: the parent repository embeds a child submodule (`ChildRepo`),
which in turn embeds a nested submodule (`ChildRepo/NestedChild`). The program
computes and prints the sum of a fixed list of numbers, making it an easy
reference for how a runnable entry point, a reusable helper module, and a
multi-level submodule layout fit together. The arithmetic helpers and the
console behavior are defined in the source modules
(`Source: service.py:L1-L14`, `Source: app.py:L1-L16`), and the three-level
parent → child → nested submodule composition is declared by the submodule
wiring (`Source: .gitmodules`, `Source: ChildRepo/.gitmodules`).

This document is the **canonical documentation exemplar** for the project; the
submodule READMEs mirror its structure and section ordering.

---

## Repository Structure

The project is a three-level submodule chain. The diagram below shows the
parent → child → nested relationship and highlights the nested module's
self-import defect (documented, not fixed — see
[Known Limitations / Troubleshooting](#known-limitations--troubleshooting)).

```mermaid
graph TD
    A["Parent Repository<br/>README.md, app.py, service.py"] -->|".gitmodules → ChildRepo"| B["ChildRepo (submodule)<br/>README.md, app.py, service.py"]
    B -->|".gitmodules → NestedChild"| C["ChildRepo/NestedChild (nested submodule)<br/>README.md, app.py, service.py"]
    C -.->|"self-import in service.py<br/>raises ImportError"| C
```

### File / folder tree

```text
.
├── README.md          # This file — parent repository documentation
├── app.py             # Console entry point; defines main()
├── service.py         # Arithmetic helpers: calculate_total, calculate_average
├── large.csv          # Excluded from Blitzy viewing/documentation by .blitzyignore (*.csv); still tracked by Git
└── ChildRepo/         # Git submodule → 600K_ChildRepo
    └── NestedChild/   # Nested Git submodule → 600K_Nested_ChildRepo
```

> **Note:** `ChildRepo/` is a Git submodule, and `ChildRepo/NestedChild/` is a
> nested Git submodule; Git does not populate either on a plain `git clone`
> (see [Setup / Installation](#setup--installation)).
> `Source: Git SCM documentation, "Git Tools - Submodules" (https://git-scm.com/book/en/v2/Git-Tools-Submodules)`.
> The `*.csv` rule in `.blitzyignore` excludes `large.csv` from Blitzy viewing
> and documentation only; it does **not** ignore the file in Git or remove it
> from version control (the file remains Git-tracked). `Source: .blitzyignore:1`.

### Submodules

The submodule wiring is declared in the `.gitmodules` files at each level.
`Source: .gitmodules`, `ChildRepo/.gitmodules`.

| Submodule path          | Repository URL                                             |
|-------------------------|------------------------------------------------------------|
| `ChildRepo`             | `https://github.com/lakshya-blitzy/600K_ChildRepo.git`         |
| `ChildRepo/NestedChild` | `https://github.com/lakshya-blitzy/600K_Nested_ChildRepo.git`  |

**Navigation:** For the child submodule's documentation, see
[`./ChildRepo/README.md`](./ChildRepo/README.md).

---

## Prerequisites

| Requirement           | Details                                                                                  |
|-----------------------|------------------------------------------------------------------------------------------|
| Python **>= 3.6**     | Required for the f-string formatting used by the entry point. `Source: app.py:L8`        |
| Git (submodule-aware) | Needed to clone and initialize the nested submodule repositories. `Source: Git SCM documentation, "Git Tools - Submodules" (https://git-scm.com/book/en/v2/Git-Tools-Submodules)` |
| Third-party packages  | **None.** The project uses only the Python standard library; the repository tree contains no dependency manifest (no `requirements.txt`, `pyproject.toml`, or `setup.py`). `Source: repository file tree (see [Repository Structure](#repository-structure))` |

---

## Setup / Installation

**Git does not download submodule contents by default.** If you clone without
initializing submodules, the `ChildRepo/` and `ChildRepo/NestedChild/`
directories will be **empty**. Use the recursive workflow below so that all
submodules — including the nested one — are populated. The `--recurse-submodules`
flag initializes and clones every submodule recursively, which also covers the
nested submodule.
`Source: Git SCM documentation, "Git Tools - Submodules" (https://git-scm.com/book/en/v2/Git-Tools-Submodules)`.
The submodule paths and URLs referenced here are declared in the `.gitmodules`
files at each level. `Source: .gitmodules`, `Source: ChildRepo/.gitmodules`.

```bash
# Clone with all submodules (including nested) initialized
git clone --recurse-submodules <repository-url>

# Or, if already cloned without submodules, populate them:
git submodule update --init --recursive
```

> **Keeping submodules in sync:** Submodules do **not** auto-update when you pull
> parent-repository changes; you must update them manually to match the commit
> the parent references. After pulling the parent, re-run
> `git submodule update --init --recursive`.
> `Source: Git SCM documentation, "Git Tools - Submodules" (https://git-scm.com/book/en/v2/Git-Tools-Submodules)`.

---

## API Documentation

The project exposes three functions across two modules. All signatures,
parameters, and return values below are transcribed directly from the source.

| Function            | Signature                     | Returns                                                                    |
|---------------------|-------------------------------|----------------------------------------------------------------------------|
| `calculate_total`   | `calculate_total(numbers)`    | Sum of the list; `0` if empty. `Source: service.py:L1-L7`                  |
| `calculate_average` | `calculate_average(numbers)`  | `0` if falsey/empty; else sum/len (float). `Source: service.py:L10-L14`    |
| `main`              | `main()`                      | `None`; prints total, each number, and a completion line. `Source: app.py:L3-L16` |

### `calculate_total(numbers)`

Sums a list of numbers using an accumulator that starts at `0`, returning the
running total. An empty list yields `0`. `Source: service.py:L1-L7`.

| Parameter | Description                                    |
|-----------|------------------------------------------------|
| `numbers` | An iterable/list of numeric (`int`/`float`) values to sum. |

**Returns:** the arithmetic sum of all elements; `0` for an empty list.

```python
>>> from service import calculate_total
>>> calculate_total([10, 20, 30, 40])
100
>>> calculate_total([])
0
```

### `calculate_average(numbers)`

Returns `0` when `numbers` is falsey/empty; otherwise returns
`calculate_total(numbers) / len(numbers)`. Because Python's `/` operator
performs true division, a non-empty input produces a `float`.
`Source: service.py:L10-L14`.

| Parameter | Description                                          |
|-----------|------------------------------------------------------|
| `numbers` | A list (or other **sized** iterable) of numeric (`int`/`float`) values to average. Because the implementation calls `len(numbers)`, unsized iterables such as generators are not supported. `Source: service.py:L10-L14` |

**Returns:** `0` for a falsey/empty input; otherwise the mean as a `float`.

```python
>>> from service import calculate_average
>>> calculate_average([10, 20, 30, 40])
25.0
>>> calculate_average([])
0
```

### `main()`

The console entry point. It builds the fixed list `[10, 20, 30, 40]`, computes
the total via `calculate_total`, prints `Total: {total}`, prints each number on
its own line, and finally prints `Application completed`. It returns `None` and
is guarded by `if __name__ == "__main__":` so it runs only on direct execution.
`Source: app.py:L3-L16`.

| Parameter | Description |
|-----------|-------------|
| *(none)*  | Takes no arguments. |

**Returns:** `None` (its effect is the text written to standard output).

```python
>>> import app
>>> app.main()
Total: 100
10
20
30
40
Application completed
```

---

## Usage / Running

Run the entry point from the repository root:

```bash
python app.py
```

Expected output (deterministic — it follows directly from the source logic in `main()`, `Source: app.py:L3-L16`):

```text
Total: 100
10
20
30
40
Application completed
```

The helper functions can also be used interactively:

```python
>>> from service import calculate_total, calculate_average
>>> calculate_total([10, 20, 30, 40])
100
>>> calculate_average([10, 20, 30, 40])
25.0
>>> calculate_total([])
0
>>> calculate_average([])
0
```

---

## Inline Code Explanation

A line-referenced walkthrough of both modules.

### `app.py`

- `app.py:L1` — imports `calculate_total` from the local `service` module (only
  `calculate_total` is imported; `calculate_average` is not).
- `app.py:L3` — defines the `main()` entry-point function.
- `app.py:L4` — defines the fixed input list `[10, 20, 30, 40]`.
- `app.py:L6` — computes the total via the `calculate_total` helper.
- `app.py:L8` — prints `Total: {total}` using an f-string (requires Python >= 3.6).
- `app.py:L10-L11` — loops over the list and prints each number on its own line.
- `app.py:L13` — prints the literal `Application completed`.
- `app.py:L15-L16` — the `__main__` guard runs `main()` only on direct execution.

### `service.py`

- `service.py:L1-L7` — `calculate_total` initializes an accumulator to `0`,
  adds each element in a loop, and returns the running total (`0` for an empty
  list).
- `service.py:L10-L14` — `calculate_average` guards against a falsey/empty input
  by returning `0`, otherwise returns `calculate_total(numbers) / len(numbers)`
  (true division → `float`).

### `main()` execution flow

```mermaid
flowchart LR
    S["Start main()"] --> L["numbers = [10, 20, 30, 40]"]
    L --> T["total = calculate_total(numbers)"]
    T --> P["print 'Total: 100'"]
    P --> E["for n in numbers: print(n)"]
    E --> D["print 'Application completed'"]
```

---

## Deployment Guide

There is **no build or packaging system** for this project — no compilation
step, no bundler, and no package manifest; the repository tree contains only the
two Python modules and this README.
`Source: repository file tree (see [Repository Structure](#repository-structure))`.
Deployment reduces to:

1. Place the repository directory on a host that has a Python **>= 3.6** runtime
   (required for the f-string in `main()`). The directory must contain a valid
   `service.py` providing `calculate_total`, because `app.py` imports it.
   `Source: app.py:L1`, `Source: app.py:L8`.
2. Run the entry point (the `__main__` guard invokes `main()` on direct
   execution):

   ```bash
   python app.py
   ```

   `Source: app.py:L15-L16`.

There are **no environment variables, no configuration files, and no
command-line arguments**: neither module imports `os`, `sys`, `argparse`, or any
configuration reader, and `main()` takes no parameters. The only runtime input
is the hard-coded list inside `main()`.
`Source: app.py:L1-L16`, `Source: service.py:L1-L14`, `Source: app.py:L4`.

---

## Known Limitations / Troubleshooting

The following are **documented, not fixed** — they describe the code as it
currently exists.

- **`calculate_average` is never called.** `app.py` imports only
  `calculate_total`, so `calculate_average` is defined but unused by the
  application. `Source: app.py:L1`.
- **Code duplication across levels.** The parent and `ChildRepo` copies of
  `app.py`/`service.py` share **identical executable logic** — their
  non-docstring code is the same — while their repository-specific docstrings
  and `Source:` citations differ, so the full files are not byte-identical.
  `Source: app.py:L1-L16`, `Source: ChildRepo/app.py:L1-L16`.
- **Hard-coded input; no engineering safeguards.** The input is hard-coded as
  `[10, 20, 30, 40]`, and neither module adds input validation, error handling,
  logging, or type annotations.
  `Source: app.py:L1-L16`, `Source: service.py:L1-L14`. There is likewise no
  test suite or CI configuration anywhere in the project — the repository tree
  contains no test files or CI configuration.
  `Source: repository file tree (see [Repository Structure](#repository-structure))`.
- **Nested submodule caveat (broken).** The `ChildRepo/NestedChild` submodule is
  broken: its `service.py` is a copy of `app.py` and performs a self-import
  `from service import calculate_total`, which raises `ImportError` at runtime.
  See [`./ChildRepo/NestedChild/README.md`](./ChildRepo/NestedChild/README.md)
  for details. `Source: ChildRepo/NestedChild/service.py:L1-L16`.

### Troubleshooting — empty submodule folders

If `ChildRepo/` or `ChildRepo/NestedChild/` is empty after cloning (because the
repository was cloned without `--recurse-submodules`), populate the submodules
with:

```bash
git submodule update --init --recursive
```
