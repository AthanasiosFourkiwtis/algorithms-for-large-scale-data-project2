# Algorithms for Large-Scale Data — Project 2

This is my second project for the **Algorithms for Large-Scale Data** course at CSE, University of Ioannina. I build a variant of the Count-Min Sketch and use it to find a "heavy" element inside a data stream.

## What the exercise asks

I have 1000 random binary strings, each one 100 bits. 999 of them show up with weight 10, and one special string shows up with weight 100 — that's the heavy element we want to find. The catch is that we're not allowed to keep the whole stream in memory, only a small summary of it.

The hard part is that a plain Count-Min Sketch only tells you how often something appears, not what it actually is. So I extended the structure: besides the weight sum of each cell, I also keep a separate sum for every bit. So when the heavy element lands alone in a cell, the cell's sum comes out 100 and every bit sum is either 0 or 100 — and I rebuild the string bit by bit.

## How I did it

All the code is in `project2.py`. The `CountMinSketch` class takes the parameters `d` (rows) and `w` (columns) and keeps both the normal Count-Min table and the per-bit sums. I keep the sums sparse, so I don't pointlessly initialize all the empty cells on every experiment.

For the hashing I use the vec_p family: I see each string as a vector of bits over Z_p, with p = 2^127 − 1, and the hash comes out as an inner product with random coefficients, then mod p and mod w. The `find_answer` method looks through the touched cells, finds the one where the heavy element got isolated, and returns the string. If it never gets isolated anywhere, it returns `None` and that counts as a failure.

## How I picked the parameters

The values `d = 7` and `w = 1370` aren't random. I compute analytically the probability that the heavy element gets isolated in at least one of the `d` rows, and the `find_best_parameters` function looks for the combination that hits at least 99% success with as few cells as possible. The two charts that come out when you run it, `success_probability.png` and `parameter_search.png`, show how the probability changes with the rows and where the cheapest combination is.

I deliberately don't set a fixed seed, so every run gives a different result and it's clear the ~99% success isn't staged.

## How to run

Just run:

```bash
python project2.py
```

You need `matplotlib` for the charts. When it runs, it prints the best parameters from the search, a detailed example that compares the real answer with the returned one, and at the end the overall success rate after 1000 experiments.

## What's in the folder

`project2.py` is the code. `success_probability.png` and `parameter_search.png` are the charts that come out automatically. The full report is `anafora_ergasias2.pdf` and the assignment description is `Assignment Sheet 2.pdf`.

## Author

Athanasios Fourkiotis — student ID 4940
