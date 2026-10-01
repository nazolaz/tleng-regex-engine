# tlengrep - Motor de Expresiones Regulares con Autómatas Finitos

Trabajo Práctico para la materia **Teoría de Lenguajes**  
**Departamento de Computación** – [Facultad de Ciencias Exactas y Naturales (FCEyN)](https://exactas.uba.ar), **Universidad de Buenos Aires (UBA)**.

---

## 📌 Descripción del Proyecto

`tlengrep` es una herramienta de búsqueda de patrones textuales por línea de comandos (similar a `grep`) basada en un motor propio de expresiones regulares. A diferencia de motores con evaluación ingenua o backtracking (que pueden incurrir en complejidades temporales exponenciales), este motor compila las expresiones regulares a **Autómatas Finitos Determinísticos Mínimos (AFD)**, garantizando tiempos de matching estrictamente **lineales** respecto a la longitud del texto analizado.

La consigna original brindada por los docentes se encuentra preservada en el documento [CONSIGNA.md](CONSIGNA.md).

---

## 🚀 Qué se resolvió

El trabajo práctico implicó el diseño y desarrollo desde cero del pipeline completo de teoría de autómatas y compilación de expresiones regulares:

### 1. Construcción inductiva de Thompson (Regex $\to$ AFND-$\lambda$)
- Traducción del Árbol de Sintaxis Abstracta (AST) de la expresión regular a un Autómata Finito No Determinístico con transiciones lambda ($\lambda$).
- Soporte para operadores fundamentales: concatenación, unión (`|`), clausura de Kleene (`*`), una o más repeticiones (`+`), opcional (`?`) y rangos de caracteres.
- Preservación y normalización continua de estados para asegurar invariantes de consistencia durante la construcción recursiva.

### 2. Determinizador por Construcción de Subconjuntos (AFND $\to$ AFD)
- Algoritmo de subconjuntos (*subset construction*) para calcular clausuras-$\lambda$ y determinar las transiciones del autómata determinístico resultante.
- Uso de `frozenset` de Python para representar metaconjuntos de estados inmutables y hashables.
- Tratamiento de autómatas como estructuras inmutables para evitar efectos de borde.

### 3. Eliminación de Estados Inaccesibles
- Detección y poda de estados inalcanzables desde el estado inicial mediante recorrido sobre el grafo de transiciones, paso previo necesario para la minimización formal.

### 4. Minimización de Hopcroft
- Implementación del algoritmo de partición de estados de **Hopcroft**, con complejidad temporal de orden $\mathcal{O}(n \cdot s \cdot \log n)$ (donde $n$ es la cantidad de estados y $s$ el tamaño del alfabeto).
- Generación del AFD mínimo equivalente y canónico para la expresión dada.

### 5. Motor de Coincidencia (Matching) Lineal
- Pre-cálculo y almacenamiento del AFD mínimo dentro de la clase `RegEx` al instanciarla (`self._afd`), evitando recomputaciones innecesarias durante las búsquedas.
- Ejecución de búsquedas en tiempo $\mathcal{O}(|texto|)$, sin riesgo de cuelgues o explosión combinatoria.

### 6. Suite de Benchmarking e Informe Técnico
- Generador de bancos de cadenas aleatorias (`cadenas_de_prueba/generar_cadenas.py`) evaluando longitudes de 10, 100 y 1.000 caracteres sobre tamaños de lote de hasta 1.000.000 de entradas.
- Comparativa de rendimiento entre la solución desarrollada y la implementación *naive* (recursiva) provista por la cátedra.
- Informe formal en formato LaTeX con carátula oficial del DC, gráficos de comparación y análisis asintótico: [informe/informe.pdf](informe/informe.pdf).

---

## 📂 Estructura del Repositorio

```text
tleng-regex-engine/
├── CONSIGNA.md                 # Enunciado original provisto por la cátedra
├── informe/
│   ├── informe.pdf             # Informe final completo en PDF
│   └── caratuladc/             # Fuentes LaTeX, gráficos de benchmarks y carátula
└── tlengrep/
    ├── tlengrep.py             # Punto de entrada CLI de la aplicación
    ├── automata/
    │   ├── af.py               # Clase base abstracta de autómatas finitos
    │   ├── afd.py              # Autómata Finito Determinístico (Hopcroft, poda)
    │   └── afnd.py             # Autómata Finito No Determinístico (Thompson, clausuras-λ)
    ├── regex/                  # Parser y wrapper de expresiones regulares
    ├── cadenas_de_prueba/      # Generador y datasets de benchmarking
    └── tests/                  # Suite de pruebas unitarias y de integración
```

---

## 🛠️ Instalación y Uso

### 1. Requisitos Previos

Python 3.9+ recomendado. Se aconseja utilizar un entorno virtual:

```bash
cd tlengrep
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Búsqueda con `tlengrep`

```bash
# Búsqueda desde archivo de texto
python3 tlengrep.py "[a-z]+[0-9]*" archivo.txt

# Búsqueda desde entrada estándar (pipe)
cat archivo.txt | python3 tlengrep.py "regex"

# Comparar contra la versión naive de la cátedra
python3 tlengrep.py -n "regex" archivo.txt
```

### 3. Ejecución de Tests

Para correr la suite de tests:

```bash
pytest
```

---

## 📊 Resultados de Rendimiento (Extracto)

Evaluación con la expresión regular $r = a^*$ sobre el alfabeto $\Sigma = \{a, b\}$:

| Longitud de cadena \ Cantidad | 1.000 | 100.000 | 1.000.000 |
| :--- | :---: | :---: | :---: |
| **Solución Naive** (1.000 chars) | 585 ms | 49.32 s | 8 min 34 s |
| **Nuestra Solución (AFD Mínimo)** (1.000 chars) | **68 ms** | **306 ms** | **2.91 s** |

*El detalle completo de mediciones y gráficos se encuentra en el [informe técnico](informe/informe.pdf).*
