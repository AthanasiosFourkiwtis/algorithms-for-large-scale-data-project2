# Algorithms for Large-Scale Data — Project 2

This is my second assignment for the **Algorithms for Large-Scale Data** course at the Department of Computer Science & Engineering, University of Ioannina. It builds a variant of the Count-Min Sketch and uses it to identify a "heavy" element inside a data stream.

## What the exercise asks for

There are 1000 random binary strings, each 100 bits long. 999 of them appear with weight 10, while one special string appears with weight 100 — that is the heavy element we want to recover. The catch is that we are not allowed to keep the whole stream in memory, only a small summary of it.

The hard part is that a plain Count-Min Sketch only tells you how often something appears, not what it actually is. So I extended the structure: besides the weight sum of each cell, it also keeps a separate sum for every bit. That way, when the heavy element lands alone in a cell, the cell's sum comes out as 100 and every bit sum is either 0 or 100 — so the string can be reconstructed bit by bit.

## How I implemented it

All the code lives in `project2.py`. The `CountMinSketch` class takes the parameters `d` (rows) and `w` (columns) and maintains both the standard Count-Min table and the per-bit accumulators. The accumulators are kept sparse, so all the empty cells don't get initialized needlessly on every experiment.

Hashing uses the vec_p family: each string is viewed as a bit vector over the field Z_p, with p = 2^127 − 1, and the hash is computed as an inner product with random coefficients, then mod p and mod w. The `find_answer` method scans the touched cells, finds the one where the heavy element got isolated, and returns the string. If it never gets isolated anywhere, it returns `None`, which counts as a failure.

## How I picked the parameters

The values `d = 7` and `w = 1370` are not arbitrary. I compute analytically the probability that the heavy element gets isolated in at least one of the `d` rows, and the `find_best_parameters` function searches for the combination that reaches at least 99% success with as few cells as possible. The two charts produced during execution, `success_probability.png` and `parameter_search.png`, show how the probability changes with the number of rows and where the most economical combination sits.

The randomness is deliberately left unseeded, so every run produces a different result — making it clear the ~99% success rate is not staged.

## Running it

Simply run:

```bash
python project2.py
```

The `matplotlib` library is needed for the charts. The run prints the best parameters found by the search, a verbose example comparing the true answer against the returned one, and finally the overall success rate over 1000 experiments.

## What's in the folder

`project2.py` holds the code. `success_probability.png` and `parameter_search.png` are the automatically generated charts. The full report is in `anafora_ergasias2.pdf` and the handout in `Assignment Sheet 2.pdf`.

## Author

Athanasios Fourkiotis — student ID 4940
