# tlengrep - Regular Expression Engine with Finite Automata

Course project for **Teoría de Lenguajes** (Theory of Languages)  
Departamento de Computación, Facultad de Ciencias Exactas y Naturales (FCEyN)  
Universidad de Buenos Aires (UBA)

---

## Overview

`tlengrep` is a command-line pattern search utility (similar to `grep`) built on a custom regular expression engine. While naive backtracking engines can suffer from exponential worst-case time complexity, this engine compiles expressions into **Minimal Deterministic Finite Automata (DFA)**, guaranteeing linear-time matching (`O(|text|)`) with respect to input length.

The original course assignment prompt is preserved in [CONSIGNA.md](CONSIGNA.md).

---

## Academic Context & Starter Code

The assignment provided a base template that included:
- A CLI wrapper (`tlengrep.py`) handling arguments, options, and input reading.
- A regular expression parser and AST hierarchy (`Concat`, `Union`, `Star`, `Symbol`, `Empty`).
- An initial naive backtracking matcher used as a baseline for correctness and benchmarking.
- Abstract base classes and method skeletons for `AF`, `AFD`, and `AFND`.

Our work focused on implementing the full automata transformation pipeline from scratch, optimizing data structures for state operations, and integrating the resulting minimal DFA into the search engine.

---

## Implemented Components

### 1. Thompson's Construction (Regex to NFA-λ)
- Inductive conversion from the regex AST to a Non-Deterministic Finite Automaton with λ-transitions (`AFND`).
- Supported operations: concatenation, union (`|`), Kleene star (`*`), positive closure (`+`), optional (`?`), and symbol sets.
- State normalization across intermediate automata to preserve construction invariants.

### 2. Subset Construction (NFA to DFA)
- Classic powerset construction computing λ-closures and deterministic transitions.
- State sets represented using Python's immutable `frozenset` to allow hashing and efficient set-of-sets lookups.
- Immutability-first approach: transformation steps produce fresh automata rather than mutating existing structures.

### 3. Inaccessible State Elimination
- Reachability analysis starting from the initial state to identify and prune unreachable states prior to minimization.

### 4. Hopcroft's Minimization Algorithm
- State partition refinement implementing Hopcroft's algorithm with `O(n · s · log n)` complexity (where `n` is the number of states and `s` the alphabet size).
- Produces the canonical, minimal DFA equivalent.

### 5. Linear-Time Match Engine
- Pre-compiles and caches the minimal DFA within `RegEx` upon initialization.
- Executes matching in `O(|text|)` time per line, preventing performance drops on adversarial inputs.

### 6. Benchmarks and Report
- Created synthetic test generators (`cadenas_de_prueba/generar_cadenas.py`) testing inputs of 10, 100, and 1,000 characters across batch sizes up to 1,000,000 strings.
- Compared execution times against the course's naive implementation.
- Written technical report in LaTeX with asymptotic analysis and experimental charts: [informe/informe.pdf](informe/informe.pdf).

---

## Performance Summary

Benchmark evaluating the regular expression `r = a*` over alphabet `Σ = {a, b}`:

| String Length \ Quantity | 1,000 strings | 100,000 strings | 1,000,000 strings |
| :--- | :---: | :---: | :---: |
| **Naive Baseline** (1,000 chars) | 585 ms | 49.32 s | 8 min 34 s |
| **Minimal DFA Engine** (1,000 chars) | **68 ms** | **306 ms** | **2.91 s** |

Detailed charts and analysis are available in the [technical report](informe/informe.pdf).

---

## Repository Structure

```text
tleng-regex-engine/
├── CONSIGNA.md                 # Original course assignment prompt
├── informe/
│   ├── informe.pdf             # Final technical report (PDF)
│   └── caratuladc/             # LaTeX source files and benchmark plots
└── tlengrep/
    ├── tlengrep.py             # CLI entry point
    ├── automata/
    │   ├── af.py               # Finite automaton base class
    │   ├── afd.py              # DFA implementation (Hopcroft, pruning)
    │   └── afnd.py             # NFA implementation (Thompson, λ-closure)
    ├── regex/                  # Regex parser and RegEx wrapper class
    ├── cadenas_de_prueba/      # Benchmark dataset generation scripts
    └── tests/                  # Unit tests (pytest)
```

---

## Setup and Usage

### Requirements

Python 3.9+ is recommended. Set up a virtual environment:

```bash
cd tlengrep
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the Search Tool

```bash
# Search within a file
python3 tlengrep.py "[a-z]+[0-9]*" input.txt

# Read from standard input
cat input.txt | python3 tlengrep.py "regex"

# Run with the naive baseline for comparison
python3 tlengrep.py -n "regex" input.txt
```

### Running Tests

```bash
pytest
```
