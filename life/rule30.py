#!/usr/bin/env python3
"""Rule 30 — elementary cellular automaton.

Stephen Wolfram's favorite: one rule, one seed cell, and the middle
column is chaotic enough that Mathematica uses it as a random number
generator. Watch order dissolve into noise and back again.

Run:  python3 life/rule30.py [--rows 40] [--seed 7]
"""
import argparse, random, shutil

def step(row):
    # rule 30: new state = left XOR (center OR right)
    return [l ^ (c or r) for l, c, r in
            zip([0] + row, row, row[1:] + [0])]

def main():
    ap = argparse.ArgumentParser(description="rule 30 cellular automaton")
    ap.add_argument("--rows", type=int, default=40)
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()
    cols = min(shutil.get_terminal_size().columns, 120)
    rng = random.Random(args.seed) if args.seed is not None else random
    row = [0] * cols
    row[rng.randrange(cols)] = 1
    print(f"rule 30 · width {cols}")
    for _ in range(args.rows):
        print("".join("██" if c else "  " for c in row))
        row = step(row)

if __name__ == "__main__":
    main()
