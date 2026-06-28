# DFS Graph Visualizer

Step-by-step animated visualization of **Depth-First Search (DFS)** on directed graphs, with edge classification and discovery/finish timestamps.

<div align="center">
  <img src="./video.gif" width="700" height="400"/>
</div>

## Description

The program loads a directed graph from a text file, runs DFS according to the rules below, and displays a step-by-step animation using matplotlib:

1. The vertex with the highest out-degree is chosen as the starting point.
2. If DFS needs to restart, the vertex with the second highest out-degree is used, and so on.
3. Each edge is classified as: **Tree**, **Back**, **Forward**, or **Cross**.
4. The `d` (discovery time) and `f` (finish time) vectors are printed to the terminal and shown in the animation.

## Requirements

- Python 3.10+
- Dependencies: `matplotlib`, `networkx`, `numpy`

## Setup

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Usage

```bash
# Default graph (data/G1.txt)
python -m src.main

# Specific graph file
python -m src.main data/G2.txt

# Control animation speed (seconds between steps)
python -m src.main data/G1.txt --pause 0.5
```

## Graph file format

```
<num_vertices> <num_edges> [D]
<source> <target>
...
```

Example (`data/G1.txt`):
```
8 14 D
0 1
1 2
...
```

Vertices are zero-indexed.

## Project structure

```
src/
├── main.py                   # Entry point + CLI
├── algorithms/
│   └── dfs.py                # DFS algorithm + edge classification
├── graph/
│   └── builder.py            # File parser + graph construction
└── visualization/
    └── animator.py           # Step-by-step matplotlib animation
data/
├── G1.txt … G6.txt           # Sample graphs
```

## Animation colors

| Color | Meaning |
|-------|---------|
| Light gray | Unvisited vertex |
| Gold | Active vertex (currently being visited) |
| Steel blue | Finished vertex |
