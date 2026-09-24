#!/usr/bin/env python3
"""Terminal fireworks. ANSI particles, gravity, a grand finale.

Usage: python3 fireworks.py [--show N]  (N rockets, default 12)
Ctrl-C to stop early.
"""
import math
import os
import random
import sys
import time

COLORS = [31, 32, 33, 34, 35, 36, 91, 92, 93, 94, 95, 96]
TRAIL = ['.', ':', '*', '+', 'x']


def size():
    try:
        w, h = os.get_terminal_size()
    except OSError:
        w, h = 80, 24
    return w, h - 1


class Rocket:
    def __init__(self, w, h):
        self.x = random.uniform(w * 0.15, w * 0.85)
        self.y = h
        self.vy = random.uniform(1.6, 2.4)
        self.apex = random.uniform(h * 0.25, h * 0.55)
        self.color = random.choice(COLORS)

    def step(self):
        self.y -= self.vy
        return self.y <= self.apex


class Spark:
    def __init__(self, x, y, color):
        ang = random.uniform(0, 2 * math.pi)
        spd = random.uniform(0.4, 2.2)
        self.x, self.y = x, y
        self.vx = math.cos(ang) * spd
        self.vy = math.sin(ang) * spd
        self.life = random.uniform(18, 40)
        self.color = color

    def step(self):
        self.x += self.vx
        self.vy += 0.06  # gravity
        self.y += self.vy
        self.life -= 1
        return self.life > 0


def render(w, h, rockets, sparks):
    grid = [[' '] * w for _ in range(h)]
    for r in rockets:
        if 0 <= int(r.y) < h:
            grid[int(r.y)][min(w - 1, int(r.x))] = ('|', r.color)
    for s in sparks:
        ix, iy = int(s.x), int(s.y)
        if 0 <= ix < w and 0 <= iy < h:
            ch = TRAIL[min(len(TRAIL) - 1, int((40 - s.life) / 40 * len(TRAIL)))]
            grid[iy][ix] = (ch, s.color)
    out = ['\x1b[H']
    for row in grid:
        line = []
        for cell in row:
            if cell == ' ':
                line.append(' ')
            else:
                ch, c = cell
                line.append(f'\x1b[{c}m{ch}\x1b[0m')
        out.append(''.join(line).rstrip())
    sys.stdout.write('\n'.join(out))
    sys.stdout.flush()


def show(n=12):
    w, h = size()
    rockets, sparks = [], []
    launched = 0
    print('\x1b[2J', end='')
    try:
        while launched < n or rockets or sparks:
            if launched < n and (not rockets or random.random() < 0.25):
                rockets.append(Rocket(w, h))
                launched += 1
            for r in rockets[:]:
                if r.step():
                    rockets.remove(r)
                    sparks.extend(Spark(r.x, r.y, r.color) for _ in range(60))
            sparks = [s for s in sparks if s.step()]
            render(w, h, rockets, sparks)
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        print('\x1b[0m')


if __name__ == '__main__':
    count = 12
    if len(sys.argv) > 2 and sys.argv[1] == '--show':
        count = int(sys.argv[2])
    show(count)
