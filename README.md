# tlengrep - Regular Expression Engine with Finite Automata

Practical Work for **Theory of Languages** (*Teoría de Lenguajes*)  
**Department of Computer Science** – [Faculty of Exact and Natural Sciences (FCEyN)](https://exactas.uba.ar), **University of Buenos Aires (UBA)**.

---

## 📌 Project Overview

`tlengrep` is a command-line pattern search tool (similar to `grep`) built upon a custom regular expression engine. Unlike naive backtracking engines—which can suffer from catastrophic backtracking and exponential worst-case time complexity—this engine compiles regular expressions into **Minimal Deterministic Finite Automata (DFA)**, guaranteeing strictly **linear** matching time $\mathcal{O}(|text|)$ with respect to the input text length.

The original course assignment prompt is preserved in [CONSIGNA.md](CONSIGNA.md).

---

## 🚀 Key Implementations

The project required designing and implementing the complete theory of computation and automata compilation pipeline from scratch:

### 1. Thompson's Construction (Regex $\to$ NFA-$\lambda$)
- Translates the Abstract Syntax Tree (AST) of the regular expression into a Non-Deterministic Finite Automaton with lambda transitions (NFA-$\lambda$).
- Full support for fundamental operators: concatenation, union (`|`), Kleene closure (`*`), one-or-more (`+`), optional (`?`), and character classes.
- Continuous state normalization to enforce consistency invariants across recursive inductive steps.

### 2. Subset Construction Determinizator (NFA $\to$ DFA)
- Classic powerset algorithm computing $\lambda$-closures and transitions for the resulting deterministic automaton.
- Leverages Python's immutable, hashable `frozenset` primitives to represent meta-states.
- Pure immutable automaton design to eliminate side effects during transformation steps.

### 3. Inaccessible State Elimination
- Graph traversal to detect and prune states unreachable from the initial state, fulfilling a required precondition for formal DFA minimization.

### 4. Hopcroft's DFA Minimization
- State partition minimization algorithm implementing **Hopcroft's algorithm**, with optimal time complexity $\mathcal{O}(n \cdot s \cdot \log n)$ (where $n$ is the number of states and $s$ is the alphabet size).
- Produces the canonical, minimal DFA equivalent for any given regular expression.

### 5. Linear-Time Matching Engine
- Pre-compiles and caches the minimal DFA within the `RegEx` class upon initialization (`self._afd`), eliminating redundant overhead during repeated matching.
- Performs linear string matching in $\mathcal{O}(|text|)$ time, avoiding performance degradation even on adversarial inputs.

### 6. Benchmarking Suite & Technical Report
- Synthetic test data generator (`cadenas_de_prueba/generar_cadenas.py`) testing inputs of 10, 100, and 1,000 characters across batch sizes up to 1,000,000 lines.
- Empirical performance comparison against the course's naive recursive baseline.
- Formal LaTeX report complete with methodology, asymptotic analysis, and benchmark charts: [informe/informe.pdf](informe/informe.pdf).

---

## 📂 Repository Structure

```text
tleng-regex-engine/
├── CONSIGNA.md                 # Original university assignment instructions
├── informe/
│   ├── informe.pdf             # Full technical report (PDF)
│   └── caratuladc/             # LaTeX sources, benchmark graphs, and cover page
└── tlengrep/
    ├── tlengrep.py             # CLI entry point
    ├── automata/
    │   ├── af.py               # Abstract base class for finite automata
    │   ├── afd.py              # Deterministic Finite Automaton (Hopcroft, pruning)
    │   └── afnd.py             # Non-Deterministic Finite Automaton (Thompson, λ-closure)
    ├── regex/                  # Regex parser and AST wrapper
    ├── cadenas_de_prueba/      # Dataset generator and test inputs
    └── tests/                  # Unit and integration test suite
```

---

## 🛠️ Setup & Usage

### 1. Prerequisites

Python 3.9+ recommended. Using a virtual environment is advised:

```bash
cd tlengrep
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Searching with `tlengrep`

```bash
# Search within a file
python3 tlengrep.py "[a-z]+[0-9]*" input.txt

# Pipe input from standard input (stdin)
cat input.txt | python3 tlengrep.py "regex"

# Compare against the course's naive baseline
python3 tlengrep.py -n "regex" input.txt
```

### 3. Running Tests

Execute the test suite with `pytest`:

```bash
pytest
```

---

## 📊 Benchmark Highlights

Evaluation using regex $r = a^*$ over alphabet $\Sigma = \{a, b\}$:

| String Length \ Quantity | 1,000 | 100,000 | 1,000,000 |
| :--- | :---: | :---: | :---: |
| **Naive Baseline** (1,000 chars) | 585 ms | 49.32 s | 8 min 34 s |
| **Our Engine (Minimal DFA)** (1,000 chars) | **68 ms** | **306 ms** | **2.91 s** |

*For complete benchmarks and charts, consult the [technical report](informe/informe.pdf).*
