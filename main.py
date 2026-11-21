#!/usr/bin/env python3
"""news-image-20261121: a 1024x1024 newspaper front page for
Saturday 21 November 2026, drawn entirely from code.

Standard library only. No network, no clock, no randomness, so
running it twice produces byte-identical output.

Lead story: two claims to a proof of the Riemann hypothesis land
in a single day - Anthropic mathematician Levent Alpoge, working
with Claude, and Stanford postdoc Alessandro Masullo. Independent
mathematicians have recompiled the Lean formalisation and say it
checks out. Around it, eight smaller panels cover the ICJ's
Myanmar verdict fallout, the war in Ukraine, a Russian plot
allegation in Denmark, a US sentencing, a Peruvian earthquake,
COP31, cost-of-living protests in Europe and Bolsonaro in hospital.

Every fact was checked against real reporting read on 21 November
2026 (Scientific American, AFP, Al Jazeera, AP, Reuters, USGS).
"""

import binascii
import os
import struct
import sys
import zlib

W = 1024
H = 1024

PAPER = (248, 244, 233)
INK = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (28, 74, 118)
SKY = (216, 231, 241)
GOLD = (186, 136, 12)
GREY = (118, 114, 102)
PALE = (233, 227, 211)
GREEN = (38, 92, 58)
CHALK = (245, 245, 238)

# ------------------------------------------------------------------ font
# Hand-drawn 5x7 bitmap glyphs, one row string per line.
# Text is upper-cased before drawing; only the glyphs below exist.
GLYPHS = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    "[": ("01110", "01000", "01000", "01000", "01000", "01000", "01110"),
    "]": ("01110", "00010", "00010", "00010", "00010", "00010", "01110"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    ">": ("10000", "01000", "00100", "00010", "00100", "01000", "10000"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    "^": ("00100", "01010", "10001", "00000", "00000", "00000", "00000"),
    "~": ("00000", "00000", "01001", "10110", "00000", "00000", "00000"),
}


def glyph_width(text, scale):
    return len(text) * 6 * scale


# ------------------------------------------------------------------ canvas
class Page:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.buf = bytearray(w * h * 3)
        r, g, b = bg
        for i in range(0, len(self.buf), 3):
            self.buf[i] = r
            self.buf[i + 1] = g
            self.buf[i + 2] = b

    def dot(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i], self.buf[i + 1], self.buf[i + 2] = color

    def box(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.dot(xx, yy, color)

    def hrule(self, x, y, w, color, t=1):
        self.box(x, y, w, t, color)

    def vrule(self, x, y, h, color, t=1):
        self.box(x, y, t, h, color)

    def seg(self, x0, y0, x1, y1, color, t=1):
        """Bresenham line with square brush of thickness t."""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.box(x0 - t // 2, y0 - t // 2, t, t, color)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, color, solid=False):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if solid:
                    if d <= r * r:
                        self.dot(xx, yy, color)
                elif r * r - 2 * r <= d <= r * r:
                    self.dot(xx, yy, color)

    def fill_poly(self, pts, color):
        if len(pts) < 3:
            return
        ys = [p[1] for p in pts]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            for i in range(len(pts)):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % len(pts)]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    if y1 != y0:
                        xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                for x in range(int(xs[i]), int(xs[i + 1]) + 1):
                    self.dot(x, y, color)

    def write(self, x, y, s, scale, color):
        s = s.upper()
        cx = x
        for ch in s:
            rows = GLYPHS.get(ch, GLYPHS[" "])
            for gy, row in enumerate(rows):
                for gx, bit in enumerate(row):
                    if bit == "1":
                        self.box(cx + gx * scale, y + gy * scale,
                                 scale, scale, color)
            cx += 6 * scale
        return cx

    def write_centre(self, cx, y, s, scale, color):
        self.write(cx - glyph_width(s, scale) // 2, y, s, scale, color)

    def split_lines(self, text, max_w, scale):
        max_chars = max(1, max_w // (6 * scale))
        lines = []
        cur = ""
        for word in text.split():
            trial = (cur + " " + word).strip()
            if len(trial) <= max_chars:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
                while len(cur) > max_chars:
                    lines.append(cur[:max_chars])
                    cur = cur[max_chars:]
        if cur:
            lines.append(cur)
        return lines

    def paragraph(self, x, y, text, max_w, scale, color, lh=None):
        if lh is None:
            lh = 7 * scale + 3
        yy = y
        for ln in self.split_lines(text, max_w, scale):
            self.write(x, yy, ln, scale, color)
            yy += lh
        return yy


# ------------------------------------------------------------------ png out
def save_png(path, pg):
    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", binascii.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", pg.w, pg.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    for y in range(pg.h):
        raw.append(0)
        raw += pg.buf[y * pg.w * 3:(y + 1) * pg.w * 3]
    data = b"\x89PNG\r\n\x1a\n"
    data += chunk(b"IHDR", ihdr)
    data += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    data += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(data)
    return len(data)


# ------------------------------------------------------------------ artwork
def draw_chalkboard(pg, x, y, w, h):
    """A classroom chalkboard: the zeta function, its critical line,
    the first primes, and a big chalk tick. Pure geometry."""
    pg.box(x, y, w, h, (32, 66, 46))
    pg.box(x, y, w, 6, (96, 64, 40))
    pg.box(x, y + h - 6, w, 6, (96, 64, 40))
    # left: the equation in chalk
    pg.write(x + 24, y + 26, "ZETA(S) = 0", 2, CHALK)
    pg.write(x + 24, y + 52, "RE(S) = 1/2", 2, CHALK)
    pg.write(x + 24, y + 84, "PRIMES:", 1, (220, 220, 200))
    pg.write(x + 24, y + 100, "2 3 5 7 11 13", 1, CHALK)
    pg.write(x + 24, y + 114, "17 19 23 29 31", 1, CHALK)
    pg.write(x + 24, y + 146, "1859 - 2026", 1, GOLD)
    pg.write(x + 24, y + 162, "167 YEARS", 1, GOLD)
    # right: graph of a wavy curve crossing the critical line
    gx, gy, gw, gh = x + w - 470, y + 24, 430, h - 60
    pg.box(gx, gy, gw, gh, (24, 52, 36))
    pg.hrule(gx, gy + gh // 2, gw, (160, 160, 140), 1)
    pg.vrule(gx + gw // 2, gy, gh, (220, 120, 120), 2)
    pg.write(gx + gw // 2 + 8, gy + 6, "1/2", 1, (220, 120, 120))
    # the curve: a smooth sine wave in chalk
    import math
    prev = None
    for i in range(gw):
        yy = gy + gh // 2 + int(30 * math.sin(i / 17.0))
        if prev is not None:
            pg.seg(prev[0], prev[1], gx + i, yy, CHALK, 2)
        prev = (gx + i, yy)
    # zeros sitting on the critical line
    for k, zy in enumerate((gy + 34, gy + 66, gy + 98, gy + 130, gy + 158)):
        pg.disc(gx + gw // 2, zy, 6, GOLD, solid=True)
        pg.disc(gx + gw // 2, zy, 6, INK)
    # big chalk tick over the whole board, bottom right
    pg.seg(x + w - 150, y + h - 58, x + w - 118, y + h - 26, GOLD, 6)
    pg.seg(x + w - 118, y + h - 26, x + w - 46, y + h - 96, GOLD, 6)
    pg.write(x + 24, y + 124, "Q.E.D. ?", 2, CHALK)
    # caption strip
    pg.box(x, y + h - 22, w, 22, INK)
    pg.write(x + 10, y + h - 18,
             "THE BLACKBOARD: EVERY NON-TRIVIAL ZERO ON THE LINE RE(S)=1/2",
             1, PAPER)


# ------------------------------------------------------------------ panels
STORIES = [
    ("THE HAGUE - ICJ", "MYANMAR CALLS VERDICT UNFAIR",
     "Myanmar's military-backed government dismisses the world "
     "court's genocide ruling as unfair, noting the 9-6 split. "
     "Reparations are ordered; the court cannot enforce them.",
     "scales"),
    ("UKRAINE - WAR", "RUSSIA POUNDS UKRAINE ANEW",
     "Fresh Russian strikes hit Ukraine after Putin vowed "
     "retaliation. Poland calls a Russian missile that crashed "
     "on its soil a deliberate provocation.",
     "rocket"),
    ("DENMARK - SPY PLOT", "RUSSIA PLOT TO KILL, COPENHAGEN SAYS",
     "Denmark accuses Russian intelligence of plotting to kill "
     "an American-Ukrainian citizen on Danish soil and expels "
     "a Russian diplomat.",
     "lens"),
    ("NEW YORK - COURT", "19 1/2 YEARS IN SIKH MURDER PLOT",
     "Indian national Nikhil Gupta is sentenced to 235 months "
     "in a US court for a murder-for-hire plot against Sikh "
     "separatist Gurpatwant Singh Pannun.",
     "gavel"),
    ("PERU - QUAKE", "M6.9 QUAKE SHAKES THE ANDES",
     "A magnitude 6.9 earthquake strikes 34 km north of Junin "
     "at 108 km deep. Tremors are felt in Lima; no casualties "
     "or damage are reported.",
     "wave"),
    ("CLIMATE - COP31", "CRUNCH TIME, NO DEAL IN SIGHT",
     "Climate talks in Turkey drag on with no agreement in "
     "sight as negotiators struggle to forge a consensus on "
     "the final text.",
     "globe"),
    ("EUROPE - STREETS", "PROTESTS JOIN FORCES OVER PRICES",
     "Workers and students march across Europe against the "
     "cost of living, disrupting cities from Rome to Paris "
     "in a coordinated day of action.",
     "crowd"),
    ("BRAZIL - HEALTH", "BOLSONARO IN HOSPITAL",
     "Former president Jair Bolsonaro is hospitalised with "
     "abdominal pain, the latest health scare for the "
     "ex-leader since leaving office.",
     "cross"),
]


def draw_mark(pg, x, y, kind):
    s = 30
    if kind == "scales":
        pg.vrule(x + 15, y + 4, 22, GOLD, 2)
        pg.hrule(x + 3, y + 6, 24, GOLD, 2)
        pg.seg(x + 4, y + 8, x + 1, y + 18, GOLD, 1)
        pg.seg(x + 4, y + 8, x + 7, y + 18, GOLD, 1)
        pg.seg(x + 26, y + 8, x + 23, y + 18, GOLD, 1)
        pg.seg(x + 26, y + 8, x + 29, y + 18, GOLD, 1)
        pg.fill_poly([(x, y + 18), (x + 8, y + 18), (x + 4, y + 24)], GOLD)
        pg.fill_poly([(x + 22, y + 18), (x + 30, y + 18), (x + 26, y + 24)],
                     GOLD)
        pg.hrule(x + 8, y + 26, 14, GOLD, 2)
    elif kind == "rocket":
        pg.fill_poly([(x + 15, y + 2), (x + 22, y + 16), (x + 15, y + 20),
                      (x + 8, y + 16)], RED)
        pg.fill_poly([(x + 8, y + 16), (x + 15, y + 20), (x + 15, y + 26)],
                     GOLD)
        pg.fill_poly([(x + 22, y + 16), (x + 15, y + 20), (x + 15, y + 26)],
                     GOLD)
    elif kind == "lens":
        pg.disc(x + 12, y + 12, 9, BLUE)
        pg.disc(x + 12, y + 12, 5, PAPER, solid=True)
        pg.seg(x + 19, y + 19, x + 27, y + 27, BLUE, 3)
    elif kind == "gavel":
        pg.seg(x + 6, y + 22, x + 24, y + 6, (96, 64, 40), 3)
        pg.box(x + 18, y + 2, 10, 8, INK)
        pg.hrule(x + 4, y + 26, 22, INK, 2)
    elif kind == "wave":
        pts = [(x + i, y + 15 + (8 if (i // 6) % 2 == 0 else -8))
               for i in range(0, 31, 2)]
        for a, b in zip(pts, pts[1:]):
            pg.seg(a[0], a[1], b[0], b[1], BLUE, 2)
        pg.hrule(x, y + 28, 30, GREY, 1)
    elif kind == "globe":
        pg.disc(x + 15, y + 15, 13, BLUE)
        pg.disc(x + 15, y + 15, 13, BLUE)
        pg.fill_poly([(x + 8, y + 8), (x + 18, y + 8), (x + 14, y + 16),
                      (x + 6, y + 16)], GREEN)
        pg.fill_poly([(x + 16, y + 18), (x + 24, y + 18), (x + 22, y + 26),
                      (x + 14, y + 24)], GREEN)
    elif kind == "crowd":
        for i, cx in enumerate((6, 15, 24)):
            pg.disc(x + cx, y + 10, 5, (BLUE, RED, GOLD)[i], solid=True)
            pg.fill_poly([(x + cx - 7, y + 26), (x + cx + 7, y + 26),
                          (x + cx + 4, y + 16), (x + cx - 4, y + 16)],
                         (BLUE, RED, GOLD)[i])
    elif kind == "cross":
        pg.box(x + 12, y + 3, 6, 24, RED)
        pg.box(x + 3, y + 12, 24, 6, RED)


def draw_story(pg, x, y, w, h, kicker, head, body, mark):
    pg.box(x, y, w, h, (255, 255, 255))
    pg.box(x, y, 5, h, RED)
    pg.hrule(x, y, w, GREY, 1)
    pg.hrule(x, y + h - 1, w, GREY, 1)
    pg.vrule(x + w - 1, y, h, GREY, 1)
    draw_mark(pg, x + w - 42, y + 8, mark)
    pg.write(x + 14, y + 8, kicker, 1, RED)
    pg.write(x + 14, y + 22, head, 1, INK)
    pg.hrule(x + 14, y + 36, w - 62, PALE, 1)
    pg.paragraph(x + 14, y + 42, body, w - 28, 1, (42, 42, 42), lh=10)


# ------------------------------------------------------------------ the page
def compose(pg):
    M = 24
    inner = W - 2 * M
    # double border frame
    pg.box(6, 6, W - 12, H - 12, INK)
    pg.box(10, 10, W - 20, H - 20, PAPER)
    pg.box(14, 14, W - 28, H - 28, INK)
    pg.box(16, 16, W - 32, H - 32, PAPER)

    # masthead
    pg.write_centre(W // 2, 26, "THE WORLD TODAY", 5, INK)
    pg.hrule(M, 74, inner, INK, 3)
    pg.write(M, 84, "VOL. I - NO. 325", 1, INK)
    pg.write_centre(W // 2, 84, "SATURDAY 21 NOVEMBER 2026", 2, RED)
    pg.write(W - M - glyph_width("PRICE: ONE PICTURE", 1), 84,
             "PRICE: ONE PICTURE", 1, INK)
    pg.hrule(M, 106, inner, INK, 1)

    # lead headline
    pg.write_centre(W // 2, 118, "CLAUDE 'SOLVES'", 3, INK)
    pg.write_centre(W // 2, 145, "MATH'S GREATEST", 3, INK)
    pg.write_centre(W // 2, 172, "RIDDLE", 3, INK)
    pg.write_centre(W // 2, 206,
                    "TWO PROOFS IN ONE DAY - EXPERTS SAY THE AI PROOF CHECKS OUT",
                    1, RED)

    # lead picture
    draw_chalkboard(pg, M, 228, inner, 208)

    # lead story
    pg.hrule(M, 448, inner, INK, 1)
    pg.paragraph(M, 458,
                 "ANTHROPIC MATHEMATICIAN LEVENT ALPOGE SAYS HE AND "
                 "CLAUDE HAVE PROVED THE RIEMANN HYPOTHESIS, THE 1859 "
                 "PROBLEM ABOUT THE PRIMES THAT HAS DEFIED MATHEMATICIANS "
                 "FOR 167 YEARS. HOURS LATER A STANFORD POSTDOC, ALESSANDRO "
                 "MASULLO, PUT FORWARD A SECOND, FULLY HUMAN PROOF. "
                 "INDEPENDENT EXPERTS HAVE RECOMPILED ALPOGE'S LEAN CODE "
                 "AND SAY IT HOLDS UP - THOUGH THE $1M CLAY PRIZE IS STILL "
                 "FAR AWAY.",
                 inner, 1, INK, lh=11)

    # section break
    pg.hrule(M, 522, inner, INK, 2)
    pg.write_centre(W // 2, 530, "- ALSO IN THE NEWS -", 1, INK)
    pg.hrule(M, 548, inner, INK, 1)

    # eight stories: two columns, four rows
    pw = (inner - 12) // 2
    ph = 90
    gap = 10
    for i, (kicker, head, body, mark) in enumerate(STORIES):
        px = M + (i % 2) * (pw + gap)
        py = 554 + (i // 2) * (ph + gap)
        draw_story(pg, px, py, pw, ph, kicker, head, body, mark)

    # footer
    fy = 554 + 4 * ph + 3 * gap + 8
    pg.hrule(M, fy, inner, INK, 2)
    pg.write_centre(W // 2, fy + 8,
                    "SOURCES: SCIENTIFIC AMERICAN - AFP - AL JAZEERA - "
                    "AP - REUTERS - USGS", 1, GREY)
    pg.write_centre(W // 2, fy + 22,
                    "DRAWN ENTIRELY BY CODE - NO PHOTOS - NO NETWORK",
                    1, GREY)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        if os.path.isdir("/output"):
            out_dir = "/output"
        else:
            out_dir = "./out"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    pg = Page(W, H, PAPER)
    compose(pg)
    size = save_png(path, pg)
    print("wrote %s (%dx%d, %d bytes)" % (path, pg.w, pg.h, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
