#!/usr/bin/env python3
"""Constellation generator: a random patch of sky, wired into a shape,
given a mythic name. For nights when you need something to wish on."""

import random

W, H = 46, 16

FIRST = ["Vel", "Cor", "Ly", "Andro", "Cassio", "Or", "Aquil", "Drac",
         "Pegas", "Cygn"]
MID = ["a", "e", "i", "o", "u", "ae"]
LAST = ["meda", "rion", "phus", "gni", "taurus", "pix", "don", "thys", "phor"]


def mythic_name(rng):
    # three-part names sound ancient; two-part names sound like a dog's name
    return rng.choice(FIRST) + rng.choice(MID) + rng.choice(LAST)


def main():
    rng = random.Random()

    stars = set()
    while len(stars) < 40:
        stars.add((rng.randrange(W), rng.randrange(H)))

    # the bright ones get connected; the rest are just scenery
    bright = rng.sample(sorted(stars), 7)
    bright.sort(key=lambda s: s[0])

    canvas = [[" " for _ in range(W)] for _ in range(H)]
    for x, y in stars:
        canvas[y][x] = "."

    prev = None
    for x, y in bright:
        canvas[y][x] = "*"
        if prev is not None:
            x0, y0 = prev
            dx, dy = x - x0, y - y0
            # pick a glyph that leans the right way
            if abs(dy) > abs(dx) * 2:
                ch = "|"
            elif abs(dx) > abs(dy) * 2:
                ch = "-"
            else:
                ch = "\\" if (dx > 0) == (dy > 0) else "/"
            steps = max(abs(dx), abs(dy), 1)
            for i in range(steps + 1):
                xi = round(x0 + dx * i / steps)
                yi = round(y0 + dy * i / steps)
                if canvas[yi][xi] == " ":
                    canvas[yi][xi] = ch
        prev = (x, y)

    print("\n".join("".join(row) for row in canvas))
    print("\n  ~ the constellation %s ~" % mythic_name(rng))
    print("  (visible only tonight, from wherever you happen to be standing)")


if __name__ == "__main__":
    main()
