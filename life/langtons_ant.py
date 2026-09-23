#!/usr/bin/env python3
"""langtons_ant.py — a tiny universe with two rules. Zero dependencies.

The ant stands on a grid. On a white square it turns right, paints it black,
and steps forward. On a black square it turns left, paints it white, and
steps forward. That's everything — yet after ~10,000 steps of chaos the ant
starts building a highway to infinity. Nobody fully knows why.

Usage: python3 langtons_ant.py [steps]
"""
import sys


def right(d):
    return (d[1], -d[0])


def left(d):
    return (-d[1], d[0])


def simulate(steps):
    black = set()
    x = y = 0
    d = (0, 1)  # north
    for _ in range(steps):
        if (x, y) in black:
            d = left(d)
            black.discard((x, y))
        else:
            d = right(d)
            black.add((x, y))
        x, y = x + d[0], y + d[1]
    return black


def render(black, w=61, h=31):
    if not black:
        return "(empty universe)"
    xs = [p[0] for p in black]
    ys = [p[1] for p in black]
    cx = (min(xs) + max(xs)) // 2
    cy = (min(ys) + max(ys)) // 2
    rows = []
    for yy in range(cy - h // 2, cy + h // 2 + 1):
        rows.append("".join(
            "#" if (xx, yy) in black else " "
            for xx in range(cx - w // 2, cx + w // 2 + 1)
        ))
    return "\n".join(rows).rstrip()


if __name__ == "__main__":
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 12000
    black = simulate(steps)
    print(f"after {steps} steps, {len(black)} black cells:\n")
    print(render(black))
