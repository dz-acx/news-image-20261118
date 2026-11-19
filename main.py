"""
news-image-20261118-v2
Fondasi Teks: Font Bitmap Proporsional, Renderer Teks, Downscale Box Filter, Penulis PNG.
Hanya menggunakan modul bawaan Python (Python stdlib murni).
"""

import os
import struct
import zlib
import time
import math


# =============================================================================
# DEFINISI GLYPH FONT (GRID KONSISTEN TINGGI 16 PIKSEL)
# Metrik grid:
#   Tinggi total: 16 baris (indeks 0..15)
#   Row 0..1: Margin atas / aksen
#   Row 2..12: Cap height & Ascender (tinggi 11 baris)
#   Row 6..12: X-height huruf kecil (tinggi 7 baris)
#   Row 12: Garis dasar (Baseline)
#   Row 13..15: Descender (tinggi 3 baris: g, j, p, q, y, koma, titik koma)
# =============================================================================

# Format raw glyph: (offset_y, [string_baris_bitmap])
RAW_GLYPHS = {}

# Huruf Besar A-Z (Row 2..12, tinggi 11)
RAW_GLYPHS['A'] = (2, [
    "..###..",
    ".#...#.",
    "#.....#",
    "#.....#",
    "#######",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#"
])
RAW_GLYPHS['B'] = (2, [
    "######.",
    "#.....#",
    "#.....#",
    "#.....#",
    "######.",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "######."
])
RAW_GLYPHS['C'] = (2, [
    ".#####.",
    "#.....#",
    "#......",
    "#......",
    "#......",
    "#......",
    "#......",
    "#......",
    "#......",
    "#.....#",
    ".#####."
])
RAW_GLYPHS['D'] = (2, [
    "######.",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "######."
])
RAW_GLYPHS['E'] = (2, [
    "######",
    "#.....",
    "#.....",
    "#.....",
    "#.....",
    "#####.",
    "#.....",
    "#.....",
    "#.....",
    "#.....",
    "######"
])
RAW_GLYPHS['F'] = (2, [
    "######",
    "#.....",
    "#.....",
    "#.....",
    "#.....",
    "#####.",
    "#.....",
    "#.....",
    "#.....",
    "#.....",
    "#....."
])
RAW_GLYPHS['G'] = (2, [
    ".#####.",
    "#.....#",
    "#......",
    "#......",
    "#......",
    "#.####.",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    ".#####."
])
RAW_GLYPHS['H'] = (2, [
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#######",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#"
])
RAW_GLYPHS['I'] = (2, [
    "###",
    ".#.",
    ".#.",
    ".#.",
    ".#.",
    ".#.",
    ".#.",
    ".#.",
    ".#.",
    ".#.",
    "###"
])
RAW_GLYPHS['J'] = (2, [
    "....##",
    ".....#",
    ".....#",
    ".....#",
    ".....#",
    ".....#",
    ".....#",
    "#....#",
    "#....#",
    "#....#",
    ".####."
])
RAW_GLYPHS['K'] = (2, [
    "#....#",
    "#...#.",
    "#..#..",
    "#.#...",
    "##....",
    "##....",
    "#.#...",
    "#..#..",
    "#...#.",
    "#....#",
    "#....#"
])
RAW_GLYPHS['L'] = (2, [
    "#.....",
    "#.....",
    "#.....",
    "#.....",
    "#.....",
    "#.....",
    "#.....",
    "#.....",
    "#.....",
    "#.....",
    "######"
])
RAW_GLYPHS['M'] = (2, [
    "#.......#",
    "##.....##",
    "#.#...#.#",
    "#..#.#..#",
    "#...#...#",
    "#.......#",
    "#.......#",
    "#.......#",
    "#.......#",
    "#.......#",
    "#.......#"
])
RAW_GLYPHS['N'] = (2, [
    "#......#",
    "##.....#",
    "#.#....#",
    "#..#...#",
    "#...#..#",
    "#....#.#",
    "#.....##",
    "#......#",
    "#......#",
    "#......#",
    "#......#"
])
RAW_GLYPHS['O'] = (2, [
    "..####..",
    ".#....#.",
    "#......#",
    "#......#",
    "#......#",
    "#......#",
    "#......#",
    "#......#",
    "#......#",
    ".#....#.",
    "..####.."
])
RAW_GLYPHS['P'] = (2, [
    "######.",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "######.",
    "#......",
    "#......",
    "#......",
    "#......",
    "#......"
])
RAW_GLYPHS['Q'] = (2, [
    "..####..",
    ".#....#.",
    "#......#",
    "#......#",
    "#......#",
    "#......#",
    "#......#",
    "#...#..#",
    "#....#.#",
    ".#....#.",
    "..####.#"
])
RAW_GLYPHS['R'] = (2, [
    "######.",
    "#.....#",
    "#.....#",
    "#.....#",
    "######.",
    "#...#..",
    "#....#.",
    "#....#.",
    "#.....#",
    "#.....#",
    "#.....#"
])
RAW_GLYPHS['S'] = (2, [
    ".#####.",
    "#.....#",
    "#......",
    "#......",
    ".#####.",
    "......#",
    "......#",
    "......#",
    "......#",
    "#.....#",
    ".#####."
])
RAW_GLYPHS['T'] = (2, [
    "#######",
    "...#...",
    "...#...",
    "...#...",
    "...#...",
    "...#...",
    "...#...",
    "...#...",
    "...#...",
    "...#...",
    "...#..."
])
RAW_GLYPHS['U'] = (2, [
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    ".#####."
])
RAW_GLYPHS['V'] = (2, [
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    ".#...#.",
    ".#...#.",
    ".#...#.",
    "..#.#..",
    "..#.#..",
    "..#.#..",
    "...#..."
])
RAW_GLYPHS['W'] = (2, [
    "#.......#",
    "#.......#",
    "#.......#",
    "#...#...#",
    "#...#...#",
    "#...#...#",
    ".#.#.#.#.",
    ".#.#.#.#.",
    ".#.#.#.#.",
    "..#...#..",
    "..#...#.."
])
RAW_GLYPHS['X'] = (2, [
    "#.....#",
    "#.....#",
    ".#...#.",
    "..#.#..",
    "...#...",
    "...#...",
    "...#...",
    "..#.#..",
    ".#...#.",
    "#.....#",
    "#.....#"
])
RAW_GLYPHS['Y'] = (2, [
    "#.....#",
    "#.....#",
    ".#...#.",
    "..#.#..",
    "...#...",
    "...#...",
    "...#...",
    "...#...",
    "...#...",
    "...#...",
    "...#..."
])
RAW_GLYPHS['Z'] = (2, [
    "#######",
    "......#",
    ".....#.",
    "....#..",
    "...#...",
    "...#...",
    "..#....",
    ".#.....",
    "#......",
    "#......",
    "#######"
])

# Huruf Kecil a-z
RAW_GLYPHS['a'] = (6, [
    ".####.",
    ".....#",
    ".#####",
    "#....#",
    "#....#",
    "#...##",
    ".###.#"
])
RAW_GLYPHS['b'] = (2, [
    "#.....",
    "#.....",
    "#.....",
    "#.....",
    "#.###.",
    "##...#",
    "#....#",
    "#....#",
    "#....#",
    "##...#",
    "#.###."
])
RAW_GLYPHS['c'] = (6, [
    ".####.",
    "#....#",
    "#.....",
    "#.....",
    "#.....",
    "#....#",
    ".####."
])
RAW_GLYPHS['d'] = (2, [
    ".....#",
    ".....#",
    ".....#",
    ".....#",
    ".###.#",
    "#...##",
    "#....#",
    "#....#",
    "#....#",
    "#...##",
    ".###.#"
])
RAW_GLYPHS['e'] = (6, [
    ".####.",
    "#....#",
    "######",
    "#.....",
    "#.....",
    "#....#",
    ".####."
])
RAW_GLYPHS['f'] = (2, [
    "..##.",
    ".#..#",
    ".#...",
    ".#...",
    "####.",
    ".#...",
    ".#...",
    ".#...",
    ".#...",
    ".#...",
    ".#..."
])
RAW_GLYPHS['g'] = (6, [
    ".####.",
    "#....#",
    "#....#",
    ".#####",
    ".....#",
    ".....#",
    ".####.",
    ".....#",
    "#....#",
    ".####."
])
RAW_GLYPHS['h'] = (2, [
    "#.....",
    "#.....",
    "#.....",
    "#.....",
    "#.###.",
    "##...#",
    "#....#",
    "#....#",
    "#....#",
    "#....#",
    "#....#"
])
RAW_GLYPHS['i'] = (2, [
    ".#.",
    ".#.",
    "...",
    "...",
    ".#.",
    ".#.",
    ".#.",
    ".#.",
    ".#.",
    ".#.",
    ".#."
])
RAW_GLYPHS['j'] = (2, [
    "..#.",
    "..#.",
    "....",
    "....",
    "..#.",
    "..#.",
    "..#.",
    "..#.",
    "..#.",
    "..#.",
    "..#.",
    "..#.",
    "#.#.",
    ".#.."
])
RAW_GLYPHS['k'] = (2, [
    "#.....",
    "#.....",
    "#.....",
    "#.....",
    "#...#.",
    "#..#..",
    "###...",
    "###...",
    "#..#..",
    "#...#.",
    "#....#"
])
RAW_GLYPHS['l'] = (2, [
    ".#.",
    ".#.",
    ".#.",
    ".#.",
    ".#.",
    ".#.",
    ".#.",
    ".#.",
    ".#.",
    ".#.",
    ".#."
])
RAW_GLYPHS['m'] = (6, [
    "#.##.##..",
    "##..#..#.",
    "#...#..#.",
    "#...#..#.",
    "#...#..#.",
    "#...#..#.",
    "#...#..#."
])
RAW_GLYPHS['n'] = (6, [
    "#.###.",
    "##...#",
    "#....#",
    "#....#",
    "#....#",
    "#....#",
    "#....#"
])
RAW_GLYPHS['o'] = (6, [
    ".####.",
    "#....#",
    "#....#",
    "#....#",
    "#....#",
    "#....#",
    ".####."
])
RAW_GLYPHS['p'] = (6, [
    "#.###.",
    "##...#",
    "#....#",
    "#....#",
    "#....#",
    "##...#",
    "#.###.",
    "#.....",
    "#.....",
    "#....."
])
RAW_GLYPHS['q'] = (6, [
    ".###.#",
    "#...##",
    "#....#",
    "#....#",
    "#....#",
    "#...##",
    ".###.#",
    ".....#",
    ".....#",
    ".....#"
])
RAW_GLYPHS['r'] = (6, [
    "#.##.",
    "##..#",
    "#....",
    "#....",
    "#....",
    "#....",
    "#...."
])
RAW_GLYPHS['s'] = (6, [
    ".###.",
    "#...#",
    ".##..",
    "...##",
    "#...#",
    "#...#",
    ".###."
])
RAW_GLYPHS['t'] = (3, [
    ".#...",
    ".#...",
    "####.",
    ".#...",
    ".#...",
    ".#...",
    ".#...",
    ".#...",
    ".#..#",
    "..##."
])
RAW_GLYPHS['u'] = (6, [
    "#....#",
    "#....#",
    "#....#",
    "#....#",
    "#....#",
    "#...##",
    ".###.#"
])
RAW_GLYPHS['v'] = (6, [
    "#....#",
    "#....#",
    ".#..#.",
    ".#..#.",
    "..##..",
    "..##..",
    "..##.."
])
RAW_GLYPHS['w'] = (6, [
    "#...#...#",
    "#...#...#",
    "#...#...#",
    ".#.#.#.#.",
    ".#.#.#.#.",
    "..#...#..",
    "..#...#.."
])
RAW_GLYPHS['x'] = (6, [
    "#....#",
    ".#..#.",
    "..##..",
    "..##..",
    ".#..#.",
    "#....#",
    "#....#"
])
RAW_GLYPHS['y'] = (6, [
    "#....#",
    "#....#",
    "#....#",
    ".#..#.",
    "..##..",
    "..##..",
    "...#..",
    "...#..",
    "..#...",
    ".#...."
])
RAW_GLYPHS['z'] = (6, [
    "######",
    "....#.",
    "...#..",
    "..#...",
    ".#....",
    "#.....",
    "######"
])

# Angka 0-9 (Row 2..12, tinggi 11)
RAW_GLYPHS['0'] = (2, [
    ".#####.",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    "#.....#",
    ".#####."
])
RAW_GLYPHS['1'] = (2, [
    "..#..",
    ".##..",
    "#.#..",
    "..#..",
    "..#..",
    "..#..",
    "..#..",
    "..#..",
    "..#..",
    "..#..",
    "#####"
])
RAW_GLYPHS['2'] = (2, [
    ".####.",
    "#....#",
    ".....#",
    ".....#",
    "....#.",
    "...#..",
    "..#...",
    ".#....",
    "#.....",
    "#.....",
    "######"
])
RAW_GLYPHS['3'] = (2, [
    "#####.",
    ".....#",
    ".....#",
    "....#.",
    "...##.",
    "....#.",
    ".....#",
    ".....#",
    ".....#",
    "#....#",
    ".####."
])
RAW_GLYPHS['4'] = (2, [
    "....#..",
    "...##..",
    "..#.#..",
    ".#..#..",
    "#...#..",
    "#######",
    "....#..",
    "....#..",
    "....#..",
    "....#..",
    "....#.."
])
RAW_GLYPHS['5'] = (2, [
    "######",
    "#.....",
    "#.....",
    "#.....",
    "#####.",
    ".....#",
    ".....#",
    ".....#",
    ".....#",
    "#....#",
    ".####."
])
RAW_GLYPHS['6'] = (2, [
    ".####.",
    "#....#",
    "#.....",
    "#.....",
    "######",
    "#....#",
    "#....#",
    "#....#",
    "#....#",
    "#....#",
    ".####."
])
RAW_GLYPHS['7'] = (2, [
    "######",
    ".....#",
    "....#.",
    "...#..",
    "...#..",
    "..#...",
    "..#...",
    ".#....",
    ".#....",
    "#.....",
    "#....."
])
RAW_GLYPHS['8'] = (2, [
    ".####.",
    "#....#",
    "#....#",
    "#....#",
    ".####.",
    "#....#",
    "#....#",
    "#....#",
    "#....#",
    "#....#",
    ".####."
])
RAW_GLYPHS['9'] = (2, [
    ".####.",
    "#....#",
    "#....#",
    "#....#",
    "#....#",
    ".#####",
    ".....#",
    ".....#",
    ".....#",
    "#....#",
    ".####."
])

# Tanda Baca & Simbol
RAW_GLYPHS[' '] = (12, ["...."])
RAW_GLYPHS['.'] = (11, [
    "##",
    "##"
])
RAW_GLYPHS[','] = (11, [
    "##.",
    "##.",
    ".#.",
    "#.."
])
RAW_GLYPHS[':'] = (6, [
    "##",
    "##",
    "..",
    "..",
    "..",
    "##",
    "##"
])
RAW_GLYPHS[';'] = (6, [
    "##.",
    "##.",
    "...",
    "...",
    "...",
    "##.",
    "##.",
    ".#.",
    "#.."
])
RAW_GLYPHS['!'] = (2, [
    "##",
    "##",
    "##",
    "##",
    "##",
    "##",
    "##",
    "..",
    "..",
    "##",
    "##"
])
RAW_GLYPHS['?'] = (2, [
    ".####.",
    "#....#",
    ".....#",
    "....#.",
    "...#..",
    "..#...",
    "..#...",
    "......",
    "......",
    "..##..",
    "..##.."
])
RAW_GLYPHS["'"] = (2, [
    "##",
    "##",
    ".#",
    ".#"
])
RAW_GLYPHS['"'] = (2, [
    "##.##",
    "##.##",
    ".#..#",
    ".#..#"
])
RAW_GLYPHS['-'] = (8, [
    "#####",
    "#####"
])
RAW_GLYPHS['\u2013'] = (8, [  # En-dash '–'
    "#######",
    "#######"
])
RAW_GLYPHS['\u2014'] = (8, [  # Em-dash '—'
    "##########",
    "##########"
])
RAW_GLYPHS['/'] = (2, [
    ".....#",
    "....#.",
    "....#.",
    "...#..",
    "...#..",
    "..#...",
    "..#...",
    ".#....",
    ".#....",
    "#.....",
    "#....."
])
RAW_GLYPHS['('] = (2, [
    "..#.",
    ".#..",
    "#...",
    "#...",
    "#...",
    "#...",
    "#...",
    "#...",
    "#...",
    ".#..",
    "..#."
])
RAW_GLYPHS[')'] = (2, [
    ".#..",
    "..#.",
    "...#",
    "...#",
    "...#",
    "...#",
    "...#",
    "...#",
    "...#",
    "..#.",
    ".#.."
])
RAW_GLYPHS['$'] = (2, [
    "..#..",
    ".####",
    "#.#.#",
    "#.#..",
    ".###.",
    "..#.#",
    "..#.#",
    "####.",
    "..#..",
    "..#..",
    "..#.."
])
RAW_GLYPHS['%'] = (2, [
    "##....#.",
    "#.#..#..",
    "##..#...",
    "...#....",
    "...#....",
    "..#.....",
    "..#.....",
    ".#...##.",
    "#....#.#",
    ".....##.",
    "........"
])
RAW_GLYPHS['+'] = (5, [
    "...#...",
    "...#...",
    "...#...",
    "#######",
    "...#...",
    "...#...",
    "...#..."
])
RAW_GLYPHS['\u00b7'] = (8, [  # Middle dot '·'
    "##",
    "##"
])
RAW_GLYPHS['\u2022'] = (7, [  # Bullet '•'
    ".###.",
    "#####",
    "#####",
    ".###."
])
RAW_GLYPHS['#'] = (2, [
    "..#..#..",
    "..#..#..",
    "########",
    "..#..#..",
    "..#..#..",
    "########",
    "..#..#..",
    "..#..#..",
    "..#..#..",
    "........",
    "........"
])
RAW_GLYPHS['&'] = (2, [
    "..###...",
    ".#...#..",
    ".#...#..",
    "..###...",
    ".#.#....",
    "#...#...",
    "#....#..",
    "#....#..",
    ".#..##.#",
    "..##..#.",
    "........"
])
RAW_GLYPHS['_'] = (12, [
    "######"
])
RAW_GLYPHS['='] = (7, [
    "######",
    "######",
    "......",
    "######",
    "######"
])


def _build_grid(top, rows, width):
    """Menyusun bitmap 16 baris standar dari pola potongan."""
    grid = [[0] * width for _ in range(16)]
    for r, row_str in enumerate(rows):
        for c, ch in enumerate(row_str):
            if ch == '#':
                grid[top + r][c] = 1
    return grid


def _make_bold_grid(grid, width):
    """
    Menghasilkan varian BOLD dengan pelebaran horizontal 1 piksel (stroke 2px).
    Pelebaran horizontal menjamin lubang/counter tengah (seperti pada 'o' dan 'O')
    tetap terbuka (bukan lingkaran padat) dan tinggi baseline tidak tergeser.
    """
    bold_width = width + 1
    bold_grid = [[0] * bold_width for _ in range(16)]
    for y in range(16):
        for x in range(width):
            if grid[y][x] == 1:
                bold_grid[y][x] = 1
                bold_grid[y][x + 1] = 1
    return bold_grid, bold_width


# Kompilasi FONT REGULAR dan FONT BOLD
FONT_REGULAR = {}
FONT_BOLD = {}

for _ch, (_top, _rows) in RAW_GLYPHS.items():
    _w = len(_rows[0])
    _reg_grid = _build_grid(_top, _rows, _w)
    _bold_grid, _bold_w = _make_bold_grid(_reg_grid, _w)
    FONT_REGULAR[_ch] = (_w, _reg_grid)
    FONT_BOLD[_ch] = (_bold_w, _bold_grid)


# =============================================================================
# KANVAS KERJA & RENDERER TEKS
# =============================================================================

class Canvas:
    """
    Kanvas RGB murni di memori (2048x2048 kerja, downscale 2x ke 1024x1024).
    """
    def __init__(self, width=2048, height=2048, bg=(255, 255, 255)):
        self.width = width
        self.height = height
        self.bg = bg
        self.data = bytearray(width * height * 3)
        r, g, b = bg
        chunk = bytes([r, g, b]) * 1024
        chunk_len = len(chunk)
        for i in range(0, len(self.data), chunk_len):
            end = min(i + chunk_len, len(self.data))
            self.data[i:end] = chunk[:end - i]

    def set_pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            idx = (y * self.width + x) * 3
            self.data[idx] = color[0]
            self.data[idx + 1] = color[1]
            self.data[idx + 2] = color[2]

    def get_pixel(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            idx = (y * self.width + x) * 3
            return (self.data[idx], self.data[idx + 1], self.data[idx + 2])
        return self.bg

    def fill_rect(self, x, y, w, h, color):
        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(self.width, x + w)
        y2 = min(self.height, y + h)
        if x1 >= x2 or y1 >= y2:
            return
        r, g, b = color
        row_seg = bytes([r, g, b]) * (x2 - x1)
        stride = self.width * 3
        start_x = x1 * 3
        for cy in range(y1, y2):
            idx = cy * stride + start_x
            self.data[idx : idx + len(row_seg)] = row_seg

    def draw_rect(self, x, y, w, h, color, thickness=1):
        """Menggambar garis tepi persegi panjang."""
        if thickness <= 0:
            return
        if thickness == 1:
            self.fill_rect(x, y, w, 1, color)
            self.fill_rect(x, y + h - 1, w, 1, color)
            self.fill_rect(x, y, 1, h, color)
            self.fill_rect(x + w - 1, y, 1, h, color)
        else:
            self.fill_rect(x, y, w, thickness, color)
            self.fill_rect(x, y + h - thickness, w, thickness, color)
            self.fill_rect(x, y, thickness, h, color)
            self.fill_rect(x + w - thickness, y, thickness, h, color)

    def fill_circle(self, cx, cy, r, color):
        """Mengisi lingkaran penuh dengan warna."""
        if r < 0:
            return
        cx, cy, r = int(cx), int(cy), int(r)
        if r == 0:
            self.set_pixel(cx, cy, color)
            return
        x1 = max(0, cx - r)
        x2 = min(self.width - 1, cx + r)
        y1 = max(0, cy - r)
        y2 = min(self.height - 1, cy + r)
        r_sq = r * r
        stride = self.width * 3
        cr, cg, cb = color
        for y in range(y1, y2 + 1):
            dy = y - cy
            rem_sq = r_sq - dy * dy
            if rem_sq >= 0:
                dx = int(math.isqrt(rem_sq))
                lx = max(0, cx - dx)
                rx = min(self.width - 1, cx + dx)
                if lx <= rx:
                    seg = bytes([cr, cg, cb]) * (rx - lx + 1)
                    idx = y * stride + lx * 3
                    self.data[idx : idx + len(seg)] = seg

    def draw_circle(self, cx, cy, r, color, thickness=1):
        """Menggambar garis tepi lingkaran."""
        if r <= 0:
            return
        cx, cy, r = int(cx), int(cy), int(r)
        r_inner = max(0, r - thickness // 2)
        r_outer = r + (thickness - 1) // 2
        r_in_sq = r_inner * r_inner
        r_out_sq = r_outer * r_outer
        stride = self.width * 3
        cr, cg, cb = color
        for cy_offset in range(-r_outer, r_outer + 1):
            y = cy + cy_offset
            if 0 <= y < self.height:
                dy_sq = cy_offset * cy_offset
                if dy_sq <= r_out_sq:
                    dx_out = int(math.isqrt(r_out_sq - dy_sq))
                    if dy_sq < r_in_sq:
                        dx_in = int(math.isqrt(r_in_sq - dy_sq))
                        span1 = dx_out - dx_in
                        if span1 > 0:
                            lx1 = max(0, cx - dx_out)
                            rx1 = min(self.width - 1, cx - dx_in - 1)
                            if lx1 <= rx1:
                                seg1 = bytes([cr, cg, cb]) * (rx1 - lx1 + 1)
                                idx1 = y * stride + lx1 * 3
                                self.data[idx1 : idx1 + len(seg1)] = seg1
                            lx2 = max(0, cx + dx_in + 1)
                            rx2 = min(self.width - 1, cx + dx_out)
                            if lx2 <= rx2:
                                seg2 = bytes([cr, cg, cb]) * (rx2 - lx2 + 1)
                                idx2 = y * stride + lx2 * 3
                                self.data[idx2 : idx2 + len(seg2)] = seg2
                    else:
                        lx = max(0, cx - dx_out)
                        rx = min(self.width - 1, cx + dx_out)
                        if lx <= rx:
                            seg = bytes([cr, cg, cb]) * (rx - lx + 1)
                            idx = y * stride + lx * 3
                            self.data[idx : idx + len(seg)] = seg

    def fill_round_rect(self, x, y, w, h, r, color):
        """Mengisi persegi panjang bersudut melengkung (rounded rectangle)."""
        r = min(int(r), w // 2, h // 2)
        if r <= 0:
            self.fill_rect(x, y, w, h, color)
            return
        self.fill_rect(x + r, y, w - 2 * r, h, color)
        self.fill_rect(x, y + r, r, h - 2 * r, color)
        self.fill_rect(x + w - r, y + r, r, h - 2 * r, color)
        self.fill_circle(x + r, y + r, r, color)
        self.fill_circle(x + w - r - 1, y + r, r, color)
        self.fill_circle(x + r, y + h - r - 1, r, color)
        self.fill_circle(x + w - r - 1, y + h - r - 1, r, color)

    def draw_line(self, x0, y0, x1, y1, color, thickness=1):
        """Menggambar garis lurus (Bresenham) dengan ketebalan yang ditentukan."""
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        if thickness <= 1:
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            sx = 1 if x0 < x1 else -1
            sy = 1 if y0 < y1 else -1
            err = dx - dy
            while True:
                self.set_pixel(x0, y0, color)
                if x0 == x1 and y0 == y1:
                    break
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x0 += sx
                if e2 < dx:
                    err += dx
                    y0 += sy
        else:
            half = thickness // 2
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            sx = 1 if x0 < x1 else -1
            sy = 1 if y0 < y1 else -1
            err = dx - dy
            while True:
                self.fill_circle(x0, y0, half, color)
                if x0 == x1 and y0 == y1:
                    break
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x0 += sx
                if e2 < dx:
                    err += dx
                    y0 += sy

    def fill_polygon(self, points, color):
        """Mengisi poligon tertutup menggunakan algoritma scanline."""
        if len(points) < 3:
            return
        min_y = max(0, min(p[1] for p in points))
        max_y = min(self.height - 1, max(p[1] for p in points))
        n = len(points)
        stride = self.width * 3
        cr, cg, cb = color
        for y in range(min_y, max_y + 1):
            nodes = []
            j = n - 1
            for i in range(n):
                p1 = points[i]
                p2 = points[j]
                if (p1[1] < y <= p2[1]) or (p2[1] < y <= p1[1]):
                    x = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                    nodes.append(int(x))
                j = i
            nodes.sort()
            for k in range(0, len(nodes), 2):
                if k + 1 < len(nodes):
                    x_start = max(0, nodes[k])
                    x_end = min(self.width - 1, nodes[k + 1])
                    if x_start <= x_end:
                        seg = bytes([cr, cg, cb]) * (x_end - x_start + 1)
                        idx = y * stride + x_start * 3
                        self.data[idx : idx + len(seg)] = seg

    def fill_triangle(self, x0, y0, x1, y1, x2, y2, color):
        """Mengisi segitiga dengan warna."""
        self.fill_polygon([(x0, y0), (x1, y1), (x2, y2)], color)

    def draw_bezier(self, p0, p1, p2, color, thickness=2, dashed=False, steps=40):
        """Menggambar kurva Bézier kuadratik (misal untuk lintasan rudal)."""
        prev = None
        for i in range(steps + 1):
            t = i / steps
            it = 1.0 - t
            bx = int(it * it * p0[0] + 2 * it * t * p1[0] + t * t * p2[0])
            by = int(it * it * p0[1] + 2 * it * t * p1[1] + t * t * p2[1])
            curr = (bx, by)
            if prev is not None:
                if not dashed or (i % 6 < 4):
                    self.draw_line(prev[0], prev[1], curr[0], curr[1], color, thickness=thickness)
            prev = curr

    def draw_glyph(self, font, char, x, y, scale=1, color=(0, 0, 0)):
        if char not in font:
            char = '?'
            if char not in font:
                return 4 * scale
        w, grid = font[char]
        for gy in range(16):
            for gx in range(w):
                if grid[gy][gx] == 1:
                    if scale == 1:
                        self.set_pixel(x + gx, y + gy, color)
                    else:
                        self.fill_rect(x + gx * scale, y + gy * scale, scale, scale, color)
        # Advance proporsional: lebar glyph + 1 piksel tracking
        return (w + 1) * scale

    def draw_text(self, text, x, y, font, scale=1, color=(0, 0, 0)):
        cur_x = x
        for ch in text:
            adv = self.draw_glyph(font, ch, cur_x, y, scale=scale, color=color)
            cur_x += adv
        return cur_x - x

    def measure_text(self, text, font, scale=1):
        total_w = 0
        for ch in text:
            if ch in font:
                w, _ = font[ch]
                total_w += (w + 1) * scale
            else:
                total_w += 5 * scale
        return total_w

    def downscale_2x(self):
        """
        Downscale 2x2 box filter: setiap blok 2x2 piksel di kanvas 2048x2048
        dirata-ratakan menjadi 1 piksel di 1024x1024 untuk anti-aliasing halus.
        """
        ow = self.width // 2
        oh = self.height // 2
        dst = bytearray(ow * oh * 3)
        stride = self.width * 3
        src = self.data

        for oy in range(oh):
            r0 = src[(oy * 2) * stride : (oy * 2 + 1) * stride]
            r1 = src[(oy * 2 + 1) * stride : (oy * 2 + 2) * stride]
            out_row = bytearray(ow * 3)
            j = 0
            for i in range(0, stride, 6):
                out_row[j]     = (r0[i]     + r0[i + 3] + r1[i]     + r1[i + 3]) >> 2
                out_row[j + 1] = (r0[i + 1] + r0[i + 4] + r1[i + 1] + r1[i + 4]) >> 2
                out_row[j + 2] = (r0[i + 2] + r0[i + 5] + r1[i + 2] + r1[i + 2]) >> 2
                j += 3
            dst[oy * ow * 3 : (oy + 1) * ow * 3] = out_row

        return ow, oh, dst


# =============================================================================
# PENULIS BERKAS PNG (PURE PYTHON MURNI: STRUCT + ZLIB)
# =============================================================================

def write_png(filepath, width, height, rgb_data):
    """
    Menulis berkas PNG standar 8-bit truecolor (RGB).
    """
    row_bytes = width * 3
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # Filter byte: 0 (None)
        start = y * row_bytes
        raw.extend(rgb_data[start : start + row_bytes])

    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data))

    header = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
    idat = chunk(b'IDAT', zlib.compress(raw, level=6))
    iend = chunk(b'IEND', b'')

    parent_dir = os.path.dirname(filepath)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    with open(filepath, 'wb') as f:
        f.write(header + ihdr + idat + iend)


# =============================================================================
# UJI GLYPH & ANALISIS PIKSEL WAJIB
# =============================================================================

def verify_and_render_glyph_test(output_path="out/test-glyph.png"):
    """
    Menjalankan uji glyph:
    1. Render kata wajib 'Tuesday November of into opens across' ukuran besar,
       serta baris alfabet A-Z, a-z, dan angka 0-9.
    2. Analisis piksel otomatis:
       - Memastikan huruf 'o' dan 'O' memiliki piksel tengah berupa latar (lubang), bukan tinta.
       - Memastikan tidak ada piksel liar/menyendiri di bawah garis dasar (baseline).
    3. Simpan berkas PNG hasil downscale.
    """
    print("=" * 70)
    print("MEMULAI UJI GLYPH & ANALISIS PIKSEL OTOMATIS")
    print("=" * 70)

    canvas = Canvas(2048, 2048, bg=(255, 255, 255))

    # Judul pengujian
    canvas.draw_text("FONT BITMAP & GLYPH VERIFICATION SHEET", 80, 80, FONT_BOLD, scale=3, color=(20, 30, 80))

    # Kata wajib ukuran besar (scale 5 = 80px di canvas kerja, 40px setelah downscale)
    bold_test_text = "Tuesday November of into opens across"
    reg_test_text  = "Tuesday November of into opens across"

    y_pos = 180
    canvas.draw_text("BOLD (scale 5):", 80, y_pos - 40, FONT_BOLD, scale=2, color=(100, 100, 100))
    canvas.draw_text(bold_test_text, 80, y_pos, FONT_BOLD, scale=5, color=(10, 10, 10))

    y_pos += 150
    canvas.draw_text("REGULAR (scale 5):", 80, y_pos - 40, FONT_BOLD, scale=2, color=(100, 100, 100))
    canvas.draw_text(reg_test_text, 80, y_pos, FONT_REGULAR, scale=5, color=(20, 20, 20))

    # Alfabet lengkap A-Z, a-z, angka 0-9 (scale 4)
    y_pos += 160
    canvas.draw_text("ALFABET & ANGKA (BOLD, scale 4):", 80, y_pos - 35, FONT_BOLD, scale=2, color=(100, 100, 100))
    canvas.draw_text("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 80, y_pos, FONT_BOLD, scale=4, color=(10, 10, 10))
    y_pos += 90
    canvas.draw_text("abcdefghijklmnopqrstuvwxyz", 80, y_pos, FONT_BOLD, scale=4, color=(10, 10, 10))
    y_pos += 90
    canvas.draw_text("0123456789", 80, y_pos, FONT_BOLD, scale=4, color=(10, 10, 10))

    y_pos += 130
    canvas.draw_text("ALFABET & ANGKA (REGULAR, scale 4):", 80, y_pos - 35, FONT_BOLD, scale=2, color=(100, 100, 100))
    canvas.draw_text("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 80, y_pos, FONT_REGULAR, scale=4, color=(20, 20, 20))
    y_pos += 90
    canvas.draw_text("abcdefghijklmnopqrstuvwxyz", 80, y_pos, FONT_REGULAR, scale=4, color=(20, 20, 20))
    y_pos += 90
    canvas.draw_text("0123456789", 80, y_pos, FONT_REGULAR, scale=4, color=(20, 20, 20))

    # Tanda baca dari NEWS-final.md
    y_pos += 130
    canvas.draw_text("TANDA BACA & SIMBOL (BOLD & REGULAR, scale 3):", 80, y_pos - 30, FONT_BOLD, scale=2, color=(100, 100, 100))
    punct_text = ". , : ; ! ? ' \" - \u2013 \u2014 / ( ) $ % + \u00b7 \u2022 # & _ ="
    canvas.draw_text(punct_text, 80, y_pos, FONT_BOLD, scale=3, color=(30, 40, 100))
    y_pos += 70
    canvas.draw_text(punct_text, 80, y_pos, FONT_REGULAR, scale=3, color=(30, 40, 100))

    # -------------------------------------------------------------------------
    # VERIFIKASI 1: ANALISIS PIKSEL BITMAP 'o' KECIL DAN 'O' BESAR
    # -------------------------------------------------------------------------
    print("\n[VERIFIKASI 1: LUBANG TENGAH GLYPH 'o' DAN 'O']")
    tests_summary = []

    # 1a. 'o' REGULAR
    w_reg_o, g_reg_o = FONT_REGULAR['o']
    cx_reg_o = w_reg_o // 2
    cy_reg_o = 9  # baris tengah x-height (rows 6..12)
    val_reg_o = g_reg_o[cy_reg_o][cx_reg_o]
    print(f"  * REGULAR 'o': ukuran={w_reg_o}x16, piksel tengah ({cx_reg_o}, {cy_reg_o}) = {val_reg_o} "
          f"({'LOLOS (Latar/Lubang)' if val_reg_o == 0 else 'GAGAL (Tinta)'})")
    assert val_reg_o == 0, "REGULAR 'o' piksel tengah adalah tinta!"
    tests_summary.append(("REGULAR 'o' counter", True, f"pos=({cx_reg_o}, {cy_reg_o}), nilai={val_reg_o}"))

    # 1b. 'o' BOLD
    w_bold_o, g_bold_o = FONT_BOLD['o']
    cx_bold_o = w_bold_o // 2
    cy_bold_o = 9
    val_bold_o = g_bold_o[cy_bold_o][cx_bold_o]
    print(f"  * BOLD 'o':    ukuran={w_bold_o}x16, piksel tengah ({cx_bold_o}, {cy_bold_o}) = {val_bold_o} "
          f"({'LOLOS (Latar/Lubang)' if val_bold_o == 0 else 'GAGAL (Tinta)'})")
    assert val_bold_o == 0, "BOLD 'o' piksel tengah adalah tinta!"
    tests_summary.append(("BOLD 'o' counter", True, f"pos=({cx_bold_o}, {cy_bold_o}), nilai={val_bold_o}"))

    # 1c. 'O' REGULAR
    w_reg_O, g_reg_O = FONT_REGULAR['O']
    cx_reg_O = w_reg_O // 2
    cy_reg_O = 7  # baris tengah cap height (rows 2..12)
    val_reg_O = g_reg_O[cy_reg_O][cx_reg_O]
    print(f"  * REGULAR 'O': ukuran={w_reg_O}x16, piksel tengah ({cx_reg_O}, {cy_reg_O}) = {val_reg_O} "
          f"({'LOLOS (Latar/Lubang)' if val_reg_O == 0 else 'GAGAL (Tinta)'})")
    assert val_reg_O == 0, "REGULAR 'O' piksel tengah adalah tinta!"
    tests_summary.append(("REGULAR 'O' counter", True, f"pos=({cx_reg_O}, {cy_reg_O}), nilai={val_reg_O}"))

    # 1d. 'O' BOLD
    w_bold_O, g_bold_O = FONT_BOLD['O']
    cx_bold_O = w_bold_O // 2
    cy_bold_O = 7
    val_bold_O = g_bold_O[cy_bold_O][cx_bold_O]
    print(f"  * BOLD 'O':    ukuran={w_bold_O}x16, piksel tengah ({cx_bold_O}, {cy_bold_O}) = {val_bold_O} "
          f"({'LOLOS (Latar/Lubang)' if val_bold_O == 0 else 'GAGAL (Tinta)'})")
    assert val_bold_O == 0, "BOLD 'O' piksel tengah adalah tinta!"
    tests_summary.append(("BOLD 'O' counter", True, f"pos=({cx_bold_O}, {cy_bold_O}), nilai={val_bold_O}"))

    # -------------------------------------------------------------------------
    # VERIFIKASI 2: ANALISIS PIKSEL PADA KANVAS TER-RENDER
    # Memeriksa piksel tengah huruf 'o' di setiap kemunculan kata uji
    # -------------------------------------------------------------------------
    print("\n[VERIFIKASI 2: PIKSEL TENGAH HURUF 'o' PADA KANVAS TER-RENDER]")
    cur_x = 80
    start_y = 180
    scale = 5
    o_index = 1
    for ch in bold_test_text:
        w, _ = FONT_BOLD[ch]
        if ch == 'o':
            # Piksel tengah pada kanvas kerja
            px_center = cur_x + (w // 2) * scale + scale // 2
            py_center = start_y + 9 * scale + scale // 2
            pix_val = canvas.get_pixel(px_center, py_center)
            is_bg = (pix_val == (255, 255, 255))
            print(f"  * [BOLD 'o' #{o_index}] koordinat=({px_center}, {py_center}), RGB={pix_val} -> "
                  f"{'LOLOS (Latar)' if is_bg else 'GAGAL (Tinta)'}")
            assert is_bg, f"Huruf 'o' #{o_index} pada kanvas tidak berlubang!"
            tests_summary.append((f"Rendered BOLD 'o' #{o_index}", True, f"({px_center}, {py_center}) RGB={pix_val}"))
            o_index += 1
        cur_x += (w + 1) * scale

    # -------------------------------------------------------------------------
    # VERIFIKASI 3: PEMERIKSAAN TITIK LIAR DI BAWAH HURUF (BASELINE AUDIT)
    # -------------------------------------------------------------------------
    print("\n[VERIFIKASI 3: PEMERIKSAAN TITIK LIAR DI BAWAH BASELINE]")
    descenders = {'g', 'j', 'p', 'q', 'y', ',', ';'}

    # 3a. Audit definisi glyph FONT_REGULAR & FONT_BOLD
    glyph_leak_count = 0
    for font_name, font_dict in [("REGULAR", FONT_REGULAR), ("BOLD", FONT_BOLD)]:
        for ch, (w, grid) in font_dict.items():
            if ch not in descenders:
                for row_idx in range(13, 16):
                    for col_idx in range(w):
                        if grid[row_idx][col_idx] == 1:
                            print(f"  GAGAL: Titik liar pada font {font_name} huruf {ch!r} di baris {row_idx}, kolom {col_idx}!")
                            glyph_leak_count += 1
    assert glyph_leak_count == 0, f"Ditemukan {glyph_leak_count} titik liar di bawah garis dasar pada glyph!"
    print(f"  * Audit Glyph Bitmap: 0 titik liar di bawah baseline untuk semua huruf non-descender ({len(FONT_REGULAR)} karakter).")
    tests_summary.append(("Glyph definition baseline audit", True, "0 titik liar"))

    # 3b. Audit piksel terisolasi (orphan pixels tanpa tetangga 8-arah)
    orphan_count = 0
    for font_name, font_dict in [("REGULAR", FONT_REGULAR), ("BOLD", FONT_BOLD)]:
        for ch, (w, grid) in font_dict.items():
            if ch == ' ':
                continue
            for r in range(16):
                for c in range(w):
                    if grid[r][c] == 1:
                        nbrs = 0
                        for dr in (-1, 0, 1):
                            for dc in (-1, 0, 1):
                                if dr == 0 and dc == 0:
                                    continue
                                nr, nc = r + dr, c + dc
                                if 0 <= nr < 16 and 0 <= nc < w:
                                    if grid[nr][nc] == 1:
                                        nbrs += 1
                        if nbrs == 0:
                            print(f"  GAGAL: Piksel terisolasi pada {font_name} {ch!r} di ({c}, {r})")
                            orphan_count += 1
    assert orphan_count == 0, f"Ditemukan {orphan_count} piksel terisolasi!"
    print(f"  * Audit Piksel Terisolasi: 0 piksel terisolasi di semua karakter REGULAR dan BOLD.")
    tests_summary.append(("Orphan pixel audit", True, "0 piksel terisolasi"))

    # 3c. Audit baris ter-render pada kanvas: Baris A-Z dan 0-9
    # Karakter A-Z dan 0-9 tidak memiliki descender, sehingga area y di bawah garis dasar harus 100% latar.
    def audit_rendered_baseline(line_text, start_x, start_y, scale, font):
        cur_x = start_x
        for ch in line_text:
            w, _ = font[ch]
            char_x0 = cur_x
            char_x1 = cur_x + w * scale
            for y in range(start_y + 13 * scale, start_y + 16 * scale):
                for x in range(char_x0, char_x1):
                    pix = canvas.get_pixel(x, y)
                    if pix != (255, 255, 255):
                        raise AssertionError(f"Titik liar pada kanvas di bawah karakter {ch!r} di koordinat ({x}, {y}): {pix}")
            cur_x += (w + 1) * scale

    # Audit baris BOLD A-Z
    audit_rendered_baseline("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 80, 520, 4, FONT_BOLD)
    print("  * Audit Kanvas Baris A-Z (BOLD): 100% bersih, tidak ada titik liar di bawah garis dasar.")
    # Audit baris BOLD 0-9
    audit_rendered_baseline("0123456789", 80, 700, 4, FONT_BOLD)
    print("  * Audit Kanvas Baris 0-9 (BOLD): 100% bersih, tidak ada titik liar di bawah garis dasar.")
    tests_summary.append(("Canvas rendered baseline audit", True, "A-Z & 0-9 100% bersih"))

    # -------------------------------------------------------------------------
    # DOWNSCALE & TULIS BERKAS PNG
    # -------------------------------------------------------------------------
    print("\n[DOWNSCALE BOX FILTER KE 1024x1024 & TULIS PNG]")
    t0 = time.time()
    ow, oh, dst_rgb = canvas.downscale_2x()
    t_downscale = time.time() - t0
    print(f"  * Downscale 2x2 box filter selesai dalam {t_downscale:.3f} detik ({canvas.width}x{canvas.height} -> {ow}x{oh})")

    t0 = time.time()
    write_png(output_path, ow, oh, dst_rgb)
    t_png = time.time() - t0
    file_size_kb = os.path.getsize(output_path) / 1024
    print(f"  * Penulisan berkas PNG selesai dalam {t_png:.3f} detik: {output_path} ({file_size_kb:.1f} KB)")

    # -------------------------------------------------------------------------
    # VERIFIKASI 4: PEMERIKSAAN CITRA DOWNSCALE 1024x1024
    # Memverifikasi bahwa pada citra akhir 1024x1024, piksel tengah 'o' tetap putih (latar)
    # -------------------------------------------------------------------------
    print("\n[VERIFIKASI 4: PEMERIKSAAN CITRA HASIL DOWNSCALE 1024x1024]")
    cur_x = 80
    start_y = 180
    scale = 5
    o_index = 1
    for ch in bold_test_text:
        w, _ = FONT_BOLD[ch]
        if ch == 'o':
            px_center = cur_x + (w // 2) * scale + scale // 2
            py_center = start_y + 9 * scale + scale // 2
            dx = px_center // 2
            dy = py_center // 2
            d_idx = (dy * ow + dx) * 3
            dpix = (dst_rgb[d_idx], dst_rgb[d_idx + 1], dst_rgb[d_idx + 2])
            is_bg = (dpix == (255, 255, 255))
            print(f"  * [1024x1024 'o' #{o_index}] koordinat=({dx}, {dy}), RGB={dpix} -> "
                  f"{'LOLOS (Latar/Anti-aliased Clean)' if is_bg else 'GAGAL'}")
            assert is_bg, f"Huruf 'o' #{o_index} pada citra downscale 1024x1024 tertutup tinta!"
            o_index += 1
        cur_x += (w + 1) * scale

    print("\n" + "=" * 70)
    print("HASIL AKHIR: SEMUA UJI GLYPH & ANALISIS PIKSEL LOLOS 100%!")
    print("=" * 70)
    return tests_summary


# =============================================================================
# HELPER TEKS: FIT SKALA, UKUR LEBAR, & POTONG KATA PADA BATAS KATA
# =============================================================================

def measure_text_width(canvas, text, font, scale=1):
    """Mengukur lebar teks dalam satuan piksel pada kanvas kerja."""
    return canvas.measure_text(text, font, scale=scale)


def fit_text_scale(canvas, text, font, max_w, max_scale=8, min_scale=1):
    """
    Menemukan skala font terbesar (antara max_scale dan min_scale)
    sehingga seluruh string teks muat utuh di lebar kotak max_w tanpa terpotong.
    """
    scale = max_scale
    while scale > min_scale:
        if canvas.measure_text(text, font, scale=scale) <= max_w:
            return scale
        scale -= 1
    return min_scale


def truncate_at_word_boundary(canvas, text, font, scale, max_w, ellipsis="..."):
    """
    Memotong teks HANYA pada batas kata (word boundary) jika melebihi max_w.
    Tidak akan pernah memotong di tengah kata atau membuat elipsis di tengah kata.
    Jika seluruh teks sudah muat, mengembalikan teks asli tanpa perubahan.
    """
    if canvas.measure_text(text, font, scale=scale) <= max_w:
        return text

    words = text.split()
    for count in range(len(words), 0, -1):
        candidate = " ".join(words[:count]) + ellipsis
        if canvas.measure_text(candidate, font, scale=scale) <= max_w:
            return candidate

    return ellipsis if canvas.measure_text(ellipsis, font, scale=scale) <= max_w else ""


def fit_and_wrap_text(canvas, text, font, max_w, preferred_scale=2, min_scale=1):
    """
    Memastikan teks satu baris muat secara utuh:
    1. Menguji apakah muat pada skala preferred_scale.
    2. Bila belum muat, mengecilkan skala hingga min_scale agar teks tetap utuh.
    3. Bila pada min_scale masih belum muat, memotong kata hanya pada batas kata.
    Mengembalikan tuple: (final_text, final_scale).
    """
    for s in range(preferred_scale, min_scale - 1, -1):
        if canvas.measure_text(text, font, scale=s) <= max_w:
            return text, s

    truncated = truncate_at_word_boundary(canvas, text, font, min_scale, max_w)
    return truncated, min_scale


# =============================================================================
# ILUSTRASI FLAT 3 BERITA TERATAS (BENTUK DASAR: PERSEGI, LINGKARAN, POLIGON, GARIS)
# Palet Terbatas: Navy, Putih, Aksen Merah / Oranye / Hijau / Emas
# =============================================================================

def draw_illustration_gulf(canvas, x, y, w, h):
    """
    Panel 1: GULF STRIKES ESCALATE
    Elemen: laut + pulau (Pulau Qeshm) + kapal perang + lintasan rudal merah + ledakan + balasan.
    """
    # Latar Langit senja Teluk
    canvas.fill_rect(x, y, w, h, (16, 26, 46))

    # Bintang / titik koordinat radar
    for sx, sy in [(x + 40, y + 30), (x + 120, y + 60), (x + 220, y + 40), (x + 500, y + 50), (x + 560, y + 80)]:
        canvas.fill_circle(sx, sy, 1, (70, 95, 130))

    # Lingkaran jangkauan radar halus
    canvas.draw_circle(x + 430, y + 188, 70, (25, 45, 75), thickness=1)
    canvas.draw_circle(x + 430, y + 188, 120, (22, 38, 65), thickness=1)

    # Laut Teluk Persia
    y_sea = y + 155
    canvas.fill_rect(x, y_sea, w, y + h - y_sea, (20, 52, 90))

    # Riak gelombang laut
    for wy in [y + 185, y + 215, y + 245, y + 275, y + 295]:
        canvas.draw_line(x + 20, wy, x + w - 20, wy, (32, 72, 120), thickness=1)

    # Garis pantai utara (Daratan Iran) di kanan atas
    iran_coast = [
        (x + 360, y_sea),
        (x + 420, y + 125),
        (x + 520, y + 115),
        (x + w, y + 130),
        (x + w, y_sea)
    ]
    canvas.fill_polygon(iran_coast, (58, 72, 78))

    # Garis pantai selatan (Semenanjung Arab) di kiri bawah
    arabia_coast = [
        (x, y + 225),
        (x + 90, y + 205),
        (x + 180, y + 225),
        (x + 220, y + h),
        (x, y + h)
    ]
    canvas.fill_polygon(arabia_coast, (72, 72, 62))

    # Pulau Qeshm (pulau memanjang strategis di Selat Hormuz)
    qeshm_poly = [
        (x + 330, y + 195),
        (x + 380, y + 180),
        (x + 465, y + 178),
        (x + 515, y + 190),
        (x + 495, y + 210),
        (x + 415, y + 215),
        (x + 340, y + 210)
    ]
    canvas.fill_polygon(qeshm_poly, (145, 132, 95))
    for i in range(len(qeshm_poly)):
        p1 = qeshm_poly[i]
        p2 = qeshm_poly[(i + 1) % len(qeshm_poly)]
        canvas.draw_line(p1[0], p1[1], p2[0], p2[1], (115, 105, 75), thickness=1)

    # Label pulau
    canvas.draw_text("QESHM I.", x + 400, y + 192, FONT_BOLD, scale=1, color=(255, 255, 255))

    # Kapal penjelajah rudal AS (siluet kapal perang di laut)
    ship_hull = [
        (x + 55, y + 258),
        (x + 120, y + 258),
        (x + 110, y + 268),
        (x + 65, y + 268)
    ]
    canvas.fill_polygon(ship_hull, (165, 180, 200))
    canvas.fill_rect(x + 75, y + 246, 26, 12, (185, 200, 220))
    canvas.draw_line(x + 88, y + 246, x + 88, y + 234, (185, 200, 220), thickness=2)

    # Lintasan rudal AS (garis lengkung merah tebal)
    p0 = (x + 95, y + 240)
    p1 = (x + 250, y + 25)
    p2 = (x + 430, y + 188)
    canvas.draw_bezier(p0, p1, p2, (245, 55, 40), thickness=3, dashed=False, steps=45)

    # Anak panah arah lintasan rudal AS
    arrow_t = [
        (x + 295, y + 80),
        (x + 315, y + 90),
        (x + 300, y + 102)
    ]
    canvas.fill_polygon(arrow_t, (245, 55, 40))

    # Ledakan dampak pada target di Pulau Qeshm
    cx_hit, cy_hit = x + 430, y + 188
    # Bintang ledakan luar (oranye)
    burst_outer = [
        (cx_hit, cy_hit - 20), (cx_hit + 6, cy_hit - 8),
        (cx_hit + 18, cy_hit - 6), (cx_hit + 8, cy_hit + 4),
        (cx_hit + 14, cy_hit + 16), (cx_hit, cy_hit + 9),
        (cx_hit - 14, cy_hit + 16), (cx_hit - 8, cy_hit + 4),
        (cx_hit - 18, cy_hit - 6), (cx_hit - 6, cy_hit - 8)
    ]
    canvas.fill_polygon(burst_outer, (255, 115, 25))
    # Bintang ledakan dalam (kuning cerah)
    burst_inner = [
        (cx_hit, cy_hit - 12), (cx_hit + 4, cy_hit - 5),
        (cx_hit + 11, cy_hit - 4), (cx_hit + 5, cy_hit + 2),
        (cx_hit + 9, cy_hit + 10), (cx_hit, cy_hit + 5),
        (cx_hit - 9, cy_hit + 10), (cx_hit - 5, cy_hit + 2),
        (cx_hit - 11, cy_hit - 4), (cx_hit - 4, cy_hit - 5)
    ]
    canvas.fill_polygon(burst_inner, (255, 230, 50))
    canvas.fill_circle(cx_hit, cy_hit, 5, (255, 255, 255))

    # Asap ledakan
    canvas.fill_circle(cx_hit, cy_hit - 18, 6, (55, 62, 75))
    canvas.fill_circle(cx_hit + 8, cy_hit - 24, 7, (65, 72, 85))
    canvas.fill_circle(cx_hit - 6, cy_hit - 26, 6, (60, 68, 80))

    # Lintasan rudal balasan Iran (garis putus-putus oranye/emas ke barat)
    p_ret0 = (x + 465, y + 175)
    p_ret1 = (x + 310, y + 75)
    p_ret2 = (x + 175, y + 215)
    canvas.draw_bezier(p_ret0, p_ret1, p_ret2, (255, 150, 35), thickness=2, dashed=True, steps=40)

    # Label lencana
    canvas.fill_round_rect(x + 16, y + 14, 90, 20, 3, (215, 45, 40))
    canvas.draw_text("U.S. STRIKE", x + 24, y + 16, FONT_BOLD, scale=1, color=(255, 255, 255))

    canvas.fill_round_rect(x + w - 106, y + 14, 90, 20, 3, (210, 120, 25))
    canvas.draw_text("IRAN REPLY", x + w - 98, y + 16, FONT_BOLD, scale=1, color=(255, 255, 255))


def draw_illustration_kerch(canvas, x, y, w, h):
    """
    Panel 2: KERCH BRIDGE FALLS
    Elemen: jembatan di atas laut Selat Kerch dengan satu bentang jatuh/miring ke dalam laut + asap/api.
    """
    # Latar Langit malam kelam
    canvas.fill_rect(x, y, w, h, (14, 22, 38))

    # Garis daratan Krimea di kejauhan
    canvas.fill_polygon([(x, y + 168), (x + 200, y + 155), (x + 400, y + 158), (x + w, y + 166), (x + w, y + 172), (x, y + 172)], (24, 34, 52))

    # Laut Selat Kerch
    y_sea = y + 170
    canvas.fill_rect(x, y_sea, w, y + h - y_sea, (15, 42, 75))

    # Riak gelombang air laut
    for wy in [y + 195, y + 225, y + 255, y + 285]:
        canvas.draw_line(x + 20, wy, x + w - 20, wy, (25, 65, 105), thickness=1)

    # Pilar jembatan beton (pylons)
    piers_x = [x + 50, x + 125, x + 200, x + 275, x + 380, x + 460, x + 540]
    for px in piers_x:
        canvas.fill_rect(px, y + 165, 16, 70, (180, 190, 205))
        # Kaki pilar bawah air
        canvas.fill_rect(px - 3, y + 225, 22, 18, (150, 160, 175))

    # Lengkungan putih kembar Kerch (White Arches) di atas saluran navigasi
    arch_cx = x + 162
    for r_arch, col_arch, th in [(92, (245, 248, 255), 4), (84, (230, 235, 248), 3)]:
        for deg in range(0, 181, 4):
            rad = math.radians(deg)
            ax0 = arch_cx + int(r_arch * math.cos(rad))
            ay0 = y + 165 - int(r_arch * 0.9 * math.sin(rad))
            if deg > 0:
                rad_prev = math.radians(deg - 4)
                ax_p = arch_cx + int(r_arch * math.cos(rad_prev))
                ay_p = y + 165 - int(r_arch * 0.9 * math.sin(rad_prev))
                canvas.draw_line(ax_p, ay_p, ax0, ay0, col_arch, thickness=th)

    # Kabel suspensi vertikal putih pada lengkungan
    for sx in range(arch_cx - 70, arch_cx + 71, 10):
        # Ukur tinggi lengkungan di titik ini
        dx_val = abs(sx - arch_cx)
        if dx_val < 85:
            arch_top = y + 165 - int(math.sqrt(max(0, 85*85 - dx_val*dx_val)) * 0.9)
            canvas.draw_line(sx, arch_top, sx, y + 165, (220, 228, 242), thickness=1)

    # Dek jembatan jalan raya utuh (kiri & kanan)
    canvas.fill_rect(x + 20, y + 162, 255, 10, (215, 222, 235))
    canvas.fill_rect(x + 380, y + 162, w - 400, 10, (215, 222, 235))
    # Pagar pengaman jembatan
    canvas.draw_line(x + 20, y + 158, x + 275, y + 158, (170, 180, 195), thickness=1)
    canvas.draw_line(x + 380, y + 158, x + w - 20, y + 158, (170, 180, 195), thickness=1)

    # BENTANG JATUH / MIRING (satu bentang jatuh/miring antara pilar x+275 dan x+380)
    fallen_span = [
        (x + 277, y + 168),
        (x + 372, y + 242),
        (x + 366, y + 254),
        (x + 277, y + 180)
    ]
    canvas.fill_polygon(fallen_span, (150, 160, 175))
    # Lapisan aspal hitam pada bentang miring
    canvas.draw_line(x + 277, y + 169, x + 372, y + 243, (65, 70, 80), thickness=2)

    # Patahan besi/beton bergerigi di pilar patah
    canvas.draw_line(x + 274, y + 162, x + 278, y + 172, (120, 130, 145), thickness=2)
    canvas.draw_line(x + 276, y + 172, x + 272, y + 182, (120, 130, 145), thickness=2)

    # Buih air cipratan saat bentang menghantam laut
    splash_poly = [
        (x + 350, y + 242),
        (x + 370, y + 235),
        (x + 395, y + 240),
        (x + 400, y + 258),
        (x + 360, y + 258)
    ]
    canvas.fill_polygon(splash_poly, (200, 240, 255))

    # Api & ledakan di titik patahan
    canvas.fill_polygon([(x + 277, y + 158), (x + 288, y + 144), (x + 295, y + 165)], (255, 90, 25))
    canvas.fill_polygon([(x + 280, y + 160), (x + 287, y + 150), (x + 292, y + 163)], (255, 210, 40))

    # Asap tebal mengepul dari jembatan yang runtuh
    for ox, oy, r in [(x + 285, y + 135, 12), (x + 298, y + 115, 16), (x + 280, y + 105, 14), (x + 310, y + 85, 20), (x + 290, y + 70, 16)]:
        canvas.fill_circle(ox, oy, r, (50, 56, 68))

    # Peringatan segitiga bahaya merah
    canvas.fill_round_rect(x + 16, y + 14, 130, 20, 3, (215, 45, 40))
    canvas.draw_text("SPAN COLLAPSED", x + 24, y + 16, FONT_BOLD, scale=1, color=(255, 255, 255))


def draw_illustration_nvidia(canvas, x, y, w, h):
    """
    Panel 3: NVIDIA'S $115.8B QUARTER
    Elemen: silikon chip prosesor + grafik batang tumbuh naik + simbol dolar emas besar.
    """
    # Latar Tech Navy gelap
    canvas.fill_rect(x, y, w, h, (12, 20, 36))

    # Jalur sirkuit PCB (printed circuit board) di latar belakang
    pcb_traces = [
        ((x + 20, y + 40), (x + 80, y + 40)),
        ((x + 80, y + 40), (x + 110, y + 70)),
        ((x + 20, y + 260), (x + 90, y + 260)),
        ((x + 90, y + 260), (x + 120, y + 230)),
        ((x + 230, y + 280), (x + 320, y + 280)),
        ((x + 320, y + 280), (x + 360, y + 260))
    ]
    for p_start, p_end in pcb_traces:
        canvas.draw_line(p_start[0], p_start[1], p_end[0], p_end[1], (22, 52, 65), thickness=1)
        canvas.fill_circle(p_start[0], p_start[1], 2, (22, 52, 65))
        canvas.fill_circle(p_end[0], p_end[1], 2, (22, 52, 65))

    # 1. KEMASAN CHIP SILIKON (di kiri)
    pkg_x, pkg_y, pkg_w, pkg_h = x + 45, y + 72, 160, 160
    # Substrat hitam pekat
    canvas.fill_rect(pkg_x, pkg_y, pkg_w, pkg_h, (26, 38, 42))

    # Pin emas di keempat sisi luar kemasan
    for i in range(12):
        # Atas & Bawah
        canvas.fill_rect(pkg_x + 10 + i * 12, pkg_y - 4, 8, 4, (220, 180, 55))
        canvas.fill_rect(pkg_x + 10 + i * 12, pkg_y + pkg_h, 8, 4, (220, 180, 55))
        # Kiri & Kanan
        canvas.fill_rect(pkg_x - 4, pkg_y + 10 + i * 12, 4, 8, (220, 180, 55))
        canvas.fill_rect(pkg_x + pkg_w, pkg_y + 10 + i * 12, 4, 8, (220, 180, 55))

    # Die silikon di tengah chip
    die_x, die_y, die_w, die_h = pkg_x + 30, pkg_y + 30, 100, 100
    canvas.fill_rect(die_x, die_y, die_w, die_h, (42, 58, 72))

    # Bingkai hijau Nvidia mengelilingi die
    canvas.draw_rect(die_x, die_y, die_w, die_h, (118, 185, 0), thickness=3)

    # Teks merek chip di dalam die
    canvas.draw_text("NVIDIA", die_x + 15, die_y + 32, FONT_BOLD, scale=2, color=(118, 185, 0))
    canvas.draw_text("AI CORE", die_x + 22, die_y + 60, FONT_BOLD, scale=1, color=(240, 245, 250))

    # 2. GRAFIK BATANG PERTUMBUHAN KEUANGAN (di kanan)
    base_y = y + 245
    canvas.draw_line(x + 260, base_y, x + 580, base_y, (60, 75, 95), thickness=2)

    # 4 Batang Kuartal: Q4, Q1, Q2, Q3
    bars = [
        (x + 275, 48, 50, (35, 85, 100), "Q4"),
        (x + 345, 48, 88, (35, 135, 130), "Q1"),
        (x + 415, 48, 136, (60, 170, 85), "Q2"),
        (x + 485, 58, 194, (118, 185, 0), "Q3")
    ]
    for bx, bw_val, bh_val, bcol, blabel in bars:
        bar_top = base_y - bh_val
        canvas.fill_rect(bx, bar_top, bw_val, bh_val, bcol)
        # Highlight atas batang
        canvas.fill_rect(bx, bar_top, bw_val, 3, (255, 255, 255))
        # Label kuartal di bawah garis dasar
        canvas.draw_text(blabel, bx + 14, base_y + 6, FONT_BOLD, scale=1, color=(160, 180, 200))

    # Persentase lonjakan di atas batang tertinggi
    canvas.draw_text("+103%", x + 485, base_y - 224, FONT_BOLD, scale=2, color=(118, 185, 0))

    # 3. GARIS TREN NAIK EMAS DENGAN PANAH
    canvas.draw_line(x + 270, base_y - 25, x + 525, base_y - 205, (255, 215, 55), thickness=3)
    arrow_poly = [
        (x + 535, base_y - 215),
        (x + 510, base_y - 215),
        (x + 525, base_y - 190)
    ]
    canvas.fill_polygon(arrow_poly, (255, 215, 55))

    # 4. KOIN / SIMBOL DOLAR EMAS BESAR
    coin_cx, coin_cy = x + 340, y + 55
    canvas.fill_circle(coin_cx, coin_cy, 26, (185, 140, 30))
    canvas.fill_circle(coin_cx, coin_cy, 23, (245, 200, 50))
    # Simbol dolar di tengah koin
    canvas.draw_text("$", coin_cx - 9, coin_cy - 16, FONT_BOLD, scale=3, color=(15, 25, 45))

    # Lencana Pendapatan
    canvas.fill_round_rect(x + 16, y + 14, 110, 20, 3, (118, 185, 0))
    canvas.draw_text("RECORD Q3", x + 24, y + 16, FONT_BOLD, scale=1, color=(10, 20, 30))


# =============================================================================
# ENAM UBIN IKON (BERITA 4-9): IKON FLAT SEDERHANA SESUAI TEMA
# =============================================================================

def draw_icon_apec(canvas, bx, by, bw=64, bh=64):
    """Ubin 4: Gedung KTT APEC Shenzhen (fasad pilar, atap segitiga, bendera)."""
    cx, cy = bx + bw // 2, by + bh // 2
    # Atap segitiga (pediment)
    canvas.fill_polygon([(cx, cy - 18), (cx - 22, cy - 6), (cx + 22, cy - 6)], (240, 245, 255))
    # Balok emas (architrave)
    canvas.fill_rect(cx - 22, cy - 6, 44, 3, (225, 175, 45))
    # 4 Pilar vertikal putih
    for i in range(4):
        canvas.fill_rect(cx - 16 + i * 10, cy - 3, 4, 16, (240, 245, 255))
    # Tangga dasar
    canvas.fill_rect(cx - 22, cy + 13, 44, 3, (200, 212, 228))
    canvas.fill_rect(cx - 25, cy + 16, 50, 4, (165, 180, 200))
    # Bendera KTT di puncak
    canvas.draw_line(cx, cy - 18, cx, cy - 26, (200, 210, 225), thickness=1)
    canvas.fill_polygon([(cx, cy - 26), (cx + 8, cy - 23), (cx, cy - 20)], (235, 55, 45))


def draw_icon_alaska(canvas, bx, by, bw=64, bh=64):
    """Ubin 5: Kotak Suara Pemilu Senat Alaska (kotak suara + slot + kertas suara bintang)."""
    cx, cy = bx + bw // 2, by + bh // 2
    # Kotak suara biru sivik
    canvas.fill_rect(cx - 16, cy - 2, 32, 24, (45, 75, 125))
    # Tutup kotak
    canvas.fill_rect(cx - 18, cy - 4, 36, 4, (70, 105, 160))
    # Slot lubang suara
    canvas.fill_rect(cx - 9, cy - 4, 18, 2, (12, 20, 38))
    # Kertas suara putih masuk ke slot
    canvas.fill_rect(cx - 7, cy - 19, 14, 17, (255, 255, 255))
    # Centang biru pemilih pada kertas
    canvas.draw_line(cx - 4, cy - 11, cx - 1, cy - 7, (40, 130, 225), thickness=2)
    canvas.draw_line(cx - 1, cy - 7, cx + 4, cy - 14, (40, 130, 225), thickness=2)
    # Bintang emas Alaska di kotak suara
    star_poly = [
        (cx, cy + 4), (cx + 2, cy + 9), (cx + 7, cy + 9),
        (cx + 3, cy + 13), (cx + 5, cy + 18), (cx, cy + 15),
        (cx - 5, cy + 18), (cx - 3, cy + 13), (cx - 7, cy + 9), (cx - 2, cy + 9)
    ]
    canvas.fill_polygon(star_poly, (245, 200, 50))


def draw_icon_horn_africa(canvas, bx, by, bw=64, bh=64):
    """Ubin 6: Pegunungan & Pasukan Perbatasan Tanduk Afrika (puncak salju + chevron militer)."""
    cx, cy = bx + bw // 2, by + bh // 2
    # Puncak gunung kiri
    canvas.fill_polygon([(cx - 24, cy + 15), (cx - 8, cy - 15), (cx + 6, cy + 15)], (80, 95, 115))
    canvas.fill_polygon([(cx - 12, cy - 7), (cx - 8, cy - 15), (cx - 4, cy - 7)], (245, 250, 255))
    # Puncak gunung kanan
    canvas.fill_polygon([(cx - 4, cy + 15), (cx + 12, cy - 10), (cx + 25, cy + 15)], (105, 120, 140))
    canvas.fill_polygon([(cx + 8, cy - 3), (cx + 12, cy - 10), (cx + 16, cy - 3)], (245, 250, 255))
    # Chevron ganda pasukan militer di latar depan (oranye militer)
    for dy in [1, 7]:
        canvas.draw_line(cx - 10, cy + dy + 5, cx, cy + dy, (245, 140, 35), thickness=2)
        canvas.draw_line(cx, cy + dy, cx + 10, cy + dy + 5, (245, 140, 35), thickness=2)
    # Pos pengawas batas
    canvas.draw_line(cx + 18, cy + 14, cx + 18, cy - 2, (220, 180, 70), thickness=2)
    canvas.fill_polygon([(cx + 18, cy - 2), (cx + 25, cy), (cx + 18, cy + 2)], (235, 55, 45))


def draw_icon_refining(canvas, bx, by, bw=64, bh=64):
    """Ubin 7: Barel Minyak Rusia Terserang Drone (barel logam bergaris + semburan api)."""
    cx, cy = bx + bw // 2, by + bh // 2
    # Tabung drum minyak
    canvas.fill_rect(cx - 13, cy - 11, 26, 28, (55, 68, 85))
    # Bibir atas dan bawah barel
    canvas.fill_rect(cx - 15, cy - 13, 30, 3, (85, 105, 130))
    canvas.fill_rect(cx - 15, cy + 16, 30, 3, (85, 105, 130))
    # Dua rusuk penguat melintang
    canvas.fill_rect(cx - 15, cy - 4, 30, 2, (85, 105, 130))
    canvas.fill_rect(cx - 15, cy + 6, 30, 2, (85, 105, 130))
    # Semburan lidah api akibat serangan drone
    canvas.fill_polygon([(cx + 4, cy - 24), (cx - 4, cy - 12), (cx + 12, cy - 12)], (255, 90, 25))
    canvas.fill_polygon([(cx + 4, cy - 20), (cx, cy - 12), (cx + 8, cy - 12)], (255, 215, 45))
    # Tetesan minyak hitam di badan barel
    canvas.fill_circle(cx - 1, cy + 2, 4, (18, 22, 28))
    canvas.fill_polygon([(cx - 1, cy - 4), (cx - 4, cy + 1), (cx + 2, cy + 1)], (18, 22, 28))


def draw_icon_gaza(canvas, bx, by, bw=64, bh=64):
    """Ubin 8: Merpati Perdamaian Gaza Terancam (merpati putih + ranting zaitun + retakan merah)."""
    cx, cy = bx + bw // 2, by + bh // 2
    # Retakan peringatan gencatan senjata di latar
    canvas.draw_line(cx - 22, cy - 14, cx - 12, cy - 4, (225, 60, 50), thickness=1)
    canvas.draw_line(cx - 12, cy - 4, cx - 4, cy - 12, (225, 60, 50), thickness=1)
    # Badan merpati putih
    canvas.fill_polygon([(cx - 12, cy + 5), (cx, cy - 3), (cx + 10, cy + 2), (cx + 3, cy + 10)], (255, 255, 255))
    canvas.fill_circle(cx + 12, cy - 1, 5, (255, 255, 255))
    # Paruh emas
    canvas.fill_polygon([(cx + 16, cy - 2), (cx + 20, cy), (cx + 16, cy + 1)], (245, 195, 50))
    # Sayap terbang
    canvas.fill_polygon([(cx - 3, cy - 3), (cx - 14, cy - 17), (cx + 1, cy - 10)], (255, 255, 255))
    canvas.fill_polygon([(cx + 2, cy - 3), (cx + 9, cy - 15), (cx + 7, cy - 8)], (230, 238, 248))
    # Ekor kipas
    canvas.fill_polygon([(cx - 10, cy + 6), (cx - 20, cy + 11), (cx - 15, cy + 16)], (245, 248, 255))
    # Daun zaitun hijau di paruh
    canvas.fill_circle(cx + 19, cy - 1, 2, (70, 165, 60))
    canvas.fill_circle(cx + 22, cy - 4, 2, (70, 165, 60))


def draw_icon_measles(canvas, bx, by, bw=64, bh=64):
    """Ubin 9: Palang Kesehatan Status Campak Hilang (palang medis putih + lingkaran waspada)."""
    cx, cy = bx + bw // 2, by + bh // 2
    # Lingkaran peringatan waspada merah
    canvas.draw_circle(cx, cy, 24, (240, 70, 50), thickness=2)
    # Palang kesehatan putih
    canvas.fill_rect(cx - 16, cy - 5, 32, 10, (255, 255, 255))
    canvas.fill_rect(cx - 5, cy - 16, 10, 32, (255, 255, 255))
    # Titik tanda seru kehilangan status eliminasi
    canvas.fill_circle(cx + 14, cy - 14, 6, (255, 195, 45))
    canvas.draw_line(cx + 14, cy - 17, cx + 14, cy - 14, (20, 25, 40), thickness=2)
    canvas.set_pixel(cx + 14, cy - 12, (20, 25, 40))


# =============================================================================
# KOMPOSISI TATA LETAK HALAMAN KORAN LENGKAP
# =============================================================================

def draw_header(canvas):
    """
    Menggambar Pita Header Navy Gelap di bagian atas:
    - Judul besar: THE WORLD IN ONE DAY (BOLD)
    - Tanggal besar: Wednesday 18 November 2026
    - Jarak vertikal yang LEBIH BESAR dan proporsional antara judul dan tanggal.
    """
    ribbon_h = 206
    # Pita navy gelap
    canvas.fill_rect(0, 0, canvas.width, ribbon_h, (12, 22, 42))

    # Aksen pita emas tipis di paling atas
    canvas.fill_rect(0, 0, canvas.width, 6, (220, 168, 52))

    # Sub-header kicker
    kicker_text = "SPECIAL INFOGRAPHIC EDITION \u00b7 WEDNESDAY REPORT"
    kw = canvas.measure_text(kicker_text, FONT_REGULAR, scale=2)
    canvas.draw_text(kicker_text, (canvas.width - kw) // 2, 18, FONT_REGULAR, scale=2, color=(165, 190, 225))

    # Judul Besar: THE WORLD IN ONE DAY (BOLD, scale 5 untuk proporsi elegan)
    title_text = "THE WORLD IN ONE DAY"
    title_scale = 5
    tw = canvas.measure_text(title_text, FONT_BOLD, scale=title_scale)
    canvas.draw_text(title_text, (canvas.width - tw) // 2, 48, FONT_BOLD, scale=title_scale, color=(255, 255, 255))

    # Tanggal Besar: Wednesday 18 November 2026 (berjarak vertikal lega di bawah judul)
    date_text = "Wednesday 18 November 2026"
    date_scale = 2
    dw = canvas.measure_text(date_text, FONT_BOLD, scale=date_scale)
    canvas.draw_text(date_text, (canvas.width - dw) // 2, 154, FONT_BOLD, scale=date_scale, color=(242, 198, 78))

    # Garis ganda pembatas bawah pita header
    canvas.fill_rect(0, ribbon_h - 4, canvas.width, 2, (220, 168, 52))
    canvas.fill_rect(0, ribbon_h - 2, canvas.width, 2, (8, 16, 32))


def draw_top_stories_section(canvas):
    """
    Menggambar 3 Panel Berita Teratas (kolom 1, 2, 3):
    Panel 1: GULF STRIKES ESCALATE
    Panel 2: KERCH BRIDGE FALLS
    Panel 3: NVIDIA'S $115.8B QUARTER
    Masing-masing dengan judul + ilustrasi flat + 2 baris isi dari NEWS-final.md.
    """
    # Header Seksi Berita Teratas
    canvas.fill_rect(48, 228, 520, 2, (200, 212, 228))
    sec_title = "TOP STORIES \u2014 GLOBAL DEVELOPMENTS"
    sec_w = canvas.measure_text(sec_title, FONT_BOLD, scale=2)
    canvas.draw_text(sec_title, (canvas.width - sec_w) // 2, 220, FONT_BOLD, scale=2, color=(18, 32, 58))
    canvas.fill_rect(canvas.width - 48 - 520, 228, 520, 2, (200, 212, 228))

    # Data 3 Panel Berita Utama
    panels_data = [
        {
            "num": "01",
            "title": "GULF STRIKES ESCALATE",
            "line1": "U.S. hits missile sites on Qeshm Island",
            "line2": "Iran fires on Kuwait and Bahrain in reply",
            "tag": "STRAIT OF HORMUZ \u00b7 REUTERS / AP",
            "draw_illus": draw_illustration_gulf
        },
        {
            "num": "02",
            "title": "KERCH BRIDGE FALLS",
            "line1": "Second night of strikes drops road span",
            "line2": "Traffic halted; two killed in Crimea",
            "tag": "KERCH STRAIT \u00b7 AP / REUTERS",
            "draw_illus": draw_illustration_kerch
        },
        {
            "num": "03",
            "title": "NVIDIA'S $115.8B QUARTER",
            "line1": "Revenue up 103% in first post-Huang report",
            "line2": "Board rules out Huang's return as CEO",
            "tag": "SANTA CLARA, CA \u00b7 REUTERS",
            "draw_illus": draw_illustration_nvidia
        }
    ]

    panel_w = 628
    panel_h = 504
    col_xs = [48, 710, 1372]
    card_y = 248

    for idx, (px, data) in enumerate(zip(col_xs, panels_data)):
        # Kartu putih dengan garis tepi rapi
        canvas.fill_rect(px, card_y, panel_w, panel_h, (255, 255, 255))
        canvas.draw_rect(px, card_y, panel_w, panel_h, (205, 215, 230), thickness=2)

        # Bilah kepala kartu warna navy
        header_h = 52
        canvas.fill_rect(px, card_y, panel_w, header_h, (16, 28, 52))

        # Lencana nomor panel emas dengan kontur jelas
        badge_x = px + 16
        badge_y = card_y + 12
        badge_w = 46
        badge_h = 28
        canvas.fill_round_rect(badge_x, badge_y, badge_w, badge_h, 4, (32, 50, 80))
        canvas.draw_rect(badge_x, badge_y, badge_w, badge_h, (55, 80, 120), thickness=1)
        canvas.draw_text(data["num"], badge_x + 8, card_y + 18, FONT_BOLD, scale=2, color=(245, 195, 50))

        # Judul panel (BOLD, berjarak lega dari badge nomor)
        avail_tw = panel_w - 96
        t_scale = fit_text_scale(canvas, data["title"], FONT_BOLD, avail_tw, max_scale=3, min_scale=2)
        canvas.draw_text(data["title"], px + 80, card_y + 18, FONT_BOLD, scale=t_scale, color=(255, 255, 255))

        # Wadah ilustrasi flat
        ix = px + 12
        iy = card_y + 58
        iw = panel_w - 24
        ih = 304
        data["draw_illus"](canvas, ix, iy, iw, ih)
        canvas.draw_rect(ix, iy, iw, ih, (30, 45, 70), thickness=1)

        # Area teks berita (2 baris isi dari NEWS-final.md)
        ty = card_y + 372
        avail_bw = panel_w - 32

        # Baris 1
        l1_txt, l1_scale = fit_and_wrap_text(canvas, data["line1"], FONT_REGULAR, avail_bw, preferred_scale=2, min_scale=1)
        canvas.draw_text(l1_txt, px + 16, ty + 10, FONT_REGULAR, scale=l1_scale, color=(18, 25, 36))

        # Baris 2
        l2_txt, l2_scale = fit_and_wrap_text(canvas, data["line2"], FONT_REGULAR, avail_bw, preferred_scale=2, min_scale=1)
        canvas.draw_text(l2_txt, px + 16, ty + 50, FONT_REGULAR, scale=l2_scale, color=(55, 68, 85))

        # Kicker wilayah / sumber berita
        canvas.draw_text(data["tag"], px + 16, ty + 94, FONT_BOLD, scale=1, color=(125, 140, 160))


def draw_dispatches_tiles_section(canvas):
    """
    Menggambar 6 Ubin Ikon (Berita 4-9 dari NEWS-final.md):
    - 4. APEC SUMMIT IN SHENZHEN (gedung KTT)
    - 5. ALASKA SENATE FLIPS (kotak suara)
    - 6. HORN OF AFRICA TENSE (pegunungan/pasukan)
    - 7. RUSSIA'S REFINING HIT (barel minyak)
    - 8. GAZA CEASEFIRE AT RISK (merpati perdamaian)
    - 9. MEASLES STATUS LOST (palang kesehatan)
    Tiap ubin: ikon flat + nomor + judul + 1 baris isi utuh tanpa elipsis di tengah kata.
    """
    # Header Seksi Ubin Berita
    canvas.fill_rect(48, 780, 520, 2, (200, 212, 228))
    sec_title = "WORLD DISPATCHES \u2014 TOP DEVELOPMENTS"
    sec_w = canvas.measure_text(sec_title, FONT_BOLD, scale=2)
    canvas.draw_text(sec_title, (canvas.width - sec_w) // 2, 772, FONT_BOLD, scale=2, color=(18, 32, 58))
    canvas.fill_rect(canvas.width - 48 - 520, 780, 520, 2, (200, 212, 228))

    tiles_data = [
        # Baris 1
        {
            "num": "04",
            "category": "DIPLOMACY \u00b7 SUMMIT",
            "title": "APEC SUMMIT IN SHENZHEN",
            "body": "Trump, Xi and Putin to meet Thursday",
            "draw_icon": draw_icon_apec
        },
        {
            "num": "05",
            "category": "U.S. POLITICS \u00b7 CONGRESS",
            "title": "ALASKA SENATE FLIPS",
            "body": "Peltola wins; Democrats take 56\u201344 majority",
            "draw_icon": draw_icon_alaska
        },
        {
            "num": "06",
            "category": "SECURITY \u00b7 BORDER ALERT",
            "title": "HORN OF AFRICA TENSE",
            "body": "Ethiopia and Eritrea mass troops at border",
            "draw_icon": draw_icon_horn_africa
        },
        # Baris 2
        {
            "num": "07",
            "category": "ENERGY \u00b7 CONFLICT",
            "title": "RUSSIA'S REFINING HIT",
            "body": "Drone strikes cut output 45%",
            "draw_icon": draw_icon_refining
        },
        {
            "num": "08",
            "category": "MIDDLE EAST \u00b7 DIPLOMACY",
            "title": "GAZA CEASEFIRE AT RISK",
            "body": "Board of Peace faults Israel and Hamas",
            "draw_icon": draw_icon_gaza
        },
        {
            "num": "09",
            "category": "PUBLIC HEALTH \u00b7 CDC",
            "title": "MEASLES STATUS LOST",
            "body": "U.S. loses elimination tag after 26 years",
            "draw_icon": draw_icon_measles
        }
    ]

    tile_w = 628
    tile_h = 160
    col_xs = [48, 710, 1372]
    row_ys = [804, 980]

    for i, data in enumerate(tiles_data):
        c_idx = i % 3
        r_idx = i // 3
        tx = col_xs[c_idx]
        ty = row_ys[r_idx]

        # Kartu putih berbingkai
        canvas.fill_rect(tx, ty, tile_w, tile_h, (255, 255, 255))
        canvas.draw_rect(tx, ty, tile_w, tile_h, (210, 220, 235), thickness=2)

        # Lencana latar belakang ikon (navy gelap)
        bx, by, bw, bh = tx + 16, ty + 16, 64, 64
        canvas.fill_round_rect(bx, by, bw, bh, 6, (14, 26, 48))
        canvas.draw_rect(bx, by, bw, bh, (35, 55, 85), thickness=1)

        # Gambar ikon flat vektor sederhana
        data["draw_icon"](canvas, bx, by, bw, bh)

        # Nomor ubin emas
        canvas.draw_text(data["num"], tx + 92, ty + 20, FONT_BOLD, scale=2, color=(215, 160, 40))

        # Judul ubin (BOLD, fit ke lebar yang tersedia)
        avail_title_w = tile_w - 140
        t_txt, t_scale = fit_and_wrap_text(canvas, data["title"], FONT_BOLD, avail_title_w, preferred_scale=2, min_scale=1)
        canvas.draw_text(t_txt, tx + 130, ty + 20, FONT_BOLD, scale=t_scale, color=(15, 28, 52))

        # Kategori topik
        canvas.draw_text(data["category"], tx + 92, ty + 54, FONT_BOLD, scale=1, color=(115, 130, 150))

        # Garis pemisah halus
        canvas.fill_rect(tx + 16, ty + 90, tile_w - 32, 1, (225, 232, 242))

        # Satu baris isi berita dari NEWS-final.md
        # Teks harus muat utuh tanpa elipsis di tengah kata
        avail_body_w = tile_w - 40
        b_txt, b_scale = fit_and_wrap_text(canvas, data["body"], FONT_REGULAR, avail_body_w, preferred_scale=2, min_scale=1)
        canvas.draw_text(b_txt, tx + 20, ty + 104, FONT_REGULAR, scale=b_scale, color=(35, 45, 60))


def draw_by_the_numbers_section(canvas):
    """
    Menggambar Seksi BY THE NUMBERS (Strip 4 angka besar dari NEWS-final.md):
    - $115.8B — Nvidia Q3 revenue, up 103%
    - 45% — Russian oil refining cut by drones
    - 56–44 — Democrats' new U.S. Senate majority
    - 25.9B km — Voyager 1, one light-day from Earth
    Masing-masing angka besar BOLD + label pendek di bawahnya (utuh & terbaca).
    """
    sec_y = 1150
    canvas.fill_rect(48, sec_y + 8, 520, 2, (200, 212, 228))
    sec_title = "BY THE NUMBERS \u2014 KEY 24-HOUR METRICS"
    sec_w = canvas.measure_text(sec_title, FONT_BOLD, scale=2)
    canvas.draw_text(sec_title, (canvas.width - sec_w) // 2, sec_y, FONT_BOLD, scale=2, color=(18, 32, 58))
    canvas.fill_rect(canvas.width - 48 - 520, sec_y + 8, 520, 2, (200, 212, 228))

    stats_data = [
        {
            "num": "$115.8B",
            "badge": "+103%",
            "label": "Nvidia Q3 revenue, up 103%",
            "accent": (118, 185, 0),    # Nvidia Green
        },
        {
            "num": "45%",
            "badge": "CUT",
            "label": "Russian oil refining cut by drones",
            "accent": (235, 90, 30),    # Orange
        },
        {
            "num": "56\u201344",
            "badge": "MAJORITY",
            "label": "Democrats' new U.S. Senate majority",
            "accent": (35, 115, 225),   # Blue
        },
        {
            "num": "25.9B km",
            "badge": "1 LIGHT-DAY",
            "label": "Voyager 1, one light-day from Earth",
            "accent": (145, 75, 220),   # Purple / Space
        }
    ]

    card_y = 1172
    card_h = 104
    total_w = canvas.width - 96  # 1952 px
    gap = 16
    card_w = (total_w - 3 * gap) // 4  # 476 px

    for idx, data in enumerate(stats_data):
        cx = 48 + idx * (card_w + gap)

        # Kartu putih berbingkai
        canvas.fill_rect(cx, card_y, card_w, card_h, (255, 255, 255))
        canvas.draw_rect(cx, card_y, card_w, card_h, (210, 222, 236), thickness=2)

        # Garis aksen atas kartu
        canvas.fill_rect(cx, card_y, card_w, 4, data["accent"])

        # Angka Besar BOLD (scale 4, tinggi 64px)
        canvas.draw_text(data["num"], cx + 18, card_y + 14, FONT_BOLD, scale=4, color=(12, 24, 46))

        # Lencana samping penanda topik
        nw = canvas.measure_text(data["num"], FONT_BOLD, scale=4)
        badge_w = canvas.measure_text(data["badge"], FONT_BOLD, scale=1) + 14
        bx = cx + 24 + nw
        if bx + badge_w <= cx + card_w - 12:
            canvas.fill_round_rect(bx, card_y + 26, badge_w, 20, 3, data["accent"])
            canvas.draw_text(data["badge"], bx + 7, card_y + 28, FONT_BOLD, scale=1, color=(255, 255, 255))

        # Label pendek di bawah angka (satu baris utuh, terukur & tidak terpotong)
        avail_lw = card_w - 20
        lbl_txt, lbl_scale = fit_and_wrap_text(canvas, data["label"], FONT_REGULAR, avail_lw, preferred_scale=2, min_scale=1)
        canvas.draw_text(lbl_txt, cx + 10, card_y + 74, FONT_REGULAR, scale=lbl_scale, color=(55, 70, 90))


# =============================================================================
# DATA PETA DUNIA DOT-MATRIX (GRID TITIK DARATAN & PENANDA 1-9)
# =============================================================================

WORLD_MAP_DATA = [
    # 0..3: Arctic / Greenland / N.Russia
    "......###.....########........................####............#####............", # 0
    "....#####...############.....................######........###########.........", # 1
    "...#######..#############..................#########....###############........", # 2
    "....#####....###########.................###############################.......", # 3
    # 4..7: Alaska / Canada / Scandinavia / Russia
    "...###......###########..................#################################.....", # 4
    "..##.##.....############................###################################....", # 5 (Alaska 5: col 4, row 5)
    ".######.....############.........##..######################################.##.", # 6
    ".#####.....##############.......####.#######.###############################...", # 7 (Rusia 7: col 44, row 7)
    # 8..11: US North / Europe / Urals / Siberia
    "..###......#############.........##..#######.#############################.....", # 8
    "..........##############........####.########.#############################....", # 9
    ".........###############........###...##.###...############################....", # 10 (Kerch 2: col 41, row 10)
    ".........##############........#####..######...###########################.....", # 11
    # 12..15: US South / Mediterranean / Middle East / Central Asia / China / Japan
    ".........##############.........###...#####.....##########################..##.", # 12 (CA 3: col 9, row 12; US 9: col 17, row 12)
    "..........############..........##....####.......########################..###.", # 13
    "...........##########..................###...#...########################...#..", # 14 (Gaza 8: col 38, row 14)
    "............########...................####.###..########################......", # 15 (Teluk Persia 1: col 44, row 15)
    # 16..19: Mexico / Sahara / Arabia / India / S.China / SE Asia
    ".............######.............###########.###...######..##############.......", # 16 (Shenzhen 4: col 61, row 16)
    "..............####.............#############.##...#####....############........", # 17
    "..............###..............#############.......###......##########.........", # 18
    "...............##...............###########....#.............########..........", # 19 (Eth-Eri 6: col 43, row 19)
    # 20..23: Central America / N.South America / Central Africa / SE Asia / Indonesia
    "...............#................##########...................#######...........", # 20
    "..............###...............##########...................######............", # 21
    ".............#####...............########.....................####....##.......", # 22
    "............#######...............######.......................##....####......", # 23
    # 24..27: South America / Southern Africa / Indonesia
    "...........#########..............#####...............................##.......", # 24
    "...........##########..............###................................###......", # 25
    "..........############..............#................................####......", # 26
    "..........###########................................................###.......", # 27
    # 28..31: South America / Australia
    "...........#########............................................#########......", # 28
    "...........########............................................###########.....", # 29
    "............######.............................................############....", # 30
    "............#####...............................................##########.....", # 31
    # 32..35: S. America tip / Tasmania / NZ
    "............####.................................................########......", # 32
    "............###....................................................###...##....", # 33
    "............##............................................................#....", # 34
    ".............#.................................................................", # 35
]

WORLD_MAP_MARKERS = [
    ("1", 44, 15, "Teluk Persia", "Qeshm Island strike"),
    ("2", 41, 10, "Selat Kerch", "Bridge road span falls"),
    ("3", 9, 12, "California", "Nvidia $115.8B revenue"),
    ("4", 61, 16, "Shenzhen", "APEC leaders summit"),
    ("5", 4, 5, "Alaska", "Peltola Senate victory"),
    ("6", 43, 19, "perbatasan Ethiopia\u2013Eritrea", "Border troop buildup"),
    ("7", 44, 7, "Rusia", "Refining output cut 45%"),
    ("8", 38, 14, "Gaza", "Ceasefire monitoring"),
    ("9", 17, 12, "Amerika Serikat", "Measles status revoked")
]


def draw_geographic_theater_map(canvas, card_x, card_y, card_w, card_h):
    """
    Menggambar Peta Dunia Dot-Matrix Skematis:
    - Benua terdefinisi: Amerika, Eropa, Afrika, Asia, Australia
    - Grid titik (dot-matrix) daratan tertanam di kode
    - Penanda nomor MERAH 1–9 di lokasi berita 1–9
    - Label legenda lokasi terstruktur di bawah peta
    """
    # Kartu putih berbingkai
    canvas.fill_rect(card_x, card_y, card_w, card_h, (255, 255, 255))
    canvas.draw_rect(card_x, card_y, card_w, card_h, (205, 218, 235), thickness=2)

    # Bilah kepala kartu navy
    header_h = 44
    canvas.fill_rect(card_x, card_y, card_w, header_h, (16, 28, 52))
    canvas.draw_text("GEOGRAPHIC THEATER \u2014 NEWS LOCATIONS (1\u20139)", card_x + 18, card_y + 14, FONT_BOLD, scale=2, color=(255, 255, 255))

    # Grid Titik Peta Dunia
    map_ox = card_x + 32
    map_oy = card_y + 58
    pitch_x = 10.3
    pitch_y = 10.3

    for r, row in enumerate(WORLD_MAP_DATA):
        for col, ch in enumerate(row):
            px = int(map_ox + col * pitch_x)
            py = int(map_oy + r * pitch_y)
            if ch == '#':
                # Titik daratan benua (teal / slate navy)
                canvas.fill_circle(px, py, 3, (36, 76, 116))
            else:
                # Titik halus samudra (latar air faset)
                canvas.fill_circle(px, py, 1, (226, 234, 244))

    # Penanda Nomor MERAH 1–9 di Lokasi Berita
    for num_str, col, row, name, desc in WORLD_MAP_MARKERS:
        mx = int(map_ox + col * pitch_x)
        my = int(map_oy + row * pitch_y)

        # Lingkaran merah penanda dengan garis tepi putih kontras
        canvas.fill_circle(mx, my, 11, (225, 35, 30))
        canvas.draw_circle(mx, my, 11, (255, 255, 255), thickness=1)

        # Angka putih BOLD di tengah lingkaran
        nw = canvas.measure_text(num_str, FONT_BOLD, scale=1)
        canvas.draw_text(num_str, mx - nw // 2, my - 6, FONT_BOLD, scale=1, color=(255, 255, 255))

    # Garis pemisah antara area peta dan legenda
    leg_start_y = card_y + 440
    canvas.fill_rect(card_x + 18, leg_start_y - 8, card_w - 36, 1, (220, 230, 242))

    # Sub-header legenda
    canvas.draw_text("DISPATCH LOCATION INDEX (KEY 1\u20139):", card_x + 20, leg_start_y, FONT_BOLD, scale=1, color=(120, 135, 155))

    # 9 Lokasi dalam format 3 kolom x 3 baris
    col_w = (card_w - 40) // 3
    for i, (num_str, col, row, name, desc) in enumerate(WORLD_MAP_MARKERS):
        c_idx = i % 3
        r_idx = i // 3
        lx = card_x + 20 + c_idx * col_w
        ly = leg_start_y + 22 + r_idx * 70

        # Lencana merah kecil
        canvas.fill_circle(lx + 10, ly + 9, 8, (225, 35, 30))
        canvas.draw_text(num_str, lx + 7, ly + 3, FONT_BOLD, scale=1, color=(255, 255, 255))

        # Judul lokasi (BOLD)
        avail_name_w = col_w - 30
        n_txt, _ = fit_and_wrap_text(canvas, name, FONT_BOLD, avail_name_w, preferred_scale=1, min_scale=1)
        canvas.draw_text(n_txt, lx + 26, ly + 3, FONT_BOLD, scale=1, color=(18, 30, 50))

        # Deskripsi pendek di bawah judul lokasi
        d_txt, _ = fit_and_wrap_text(canvas, desc, FONT_REGULAR, avail_name_w, preferred_scale=1, min_scale=1)
        canvas.draw_text(d_txt, lx + 26, ly + 24, FONT_REGULAR, scale=1, color=(100, 115, 135))


# =============================================================================
# DAFTAR MORE STORIES DUA KOLOM (CERITA 10-38 DARI NEWS-final.md)
# =============================================================================

MORE_STORIES_DATA = [
    # Kolom 1 (10-24, 15 cerita)
    ("10.", "Voyager 1 reaches one light-day from Earth (NASA)"),
    ("11.", "Bangladesh deploys troops as Hasina return sparks unrest"),
    ("12.", "Anthropic prices record IPO; $1.4tn valuation in reach"),
    ("13.", "U.S. and Venezuela agree to restore military ties"),
    ("14.", "FAA pauses router installs after nationwide ground stop"),
    ("15.", "Jeffries nominated as next U.S. House Speaker"),
    ("16.", "Israeli troops in rare Gaza operation past Yellow Line"),
    ("17.", "William and Kate meet Modi to end India tour"),
    ("18.", "Critics call GTA 6 \"a masterpiece\""),
    ("19.", "Trump hails \"very big\" Philippines trade deal"),
    ("20.", "UN court delivers Myanmar genocide verdict"),
    ("21.", "UK inflation rises to 3.6% on fuel prices"),
    ("22.", "Russian military plane crash kills all 19 aboard"),
    ("23.", "Settler shooting kills Palestinian woman, 72"),
    ("24.", "U.S. soldier held in UK over spying suspicion"),
    # Kolom 2 (25-38, 14 cerita)
    ("25.", "London transport data breach hits 265,000"),
    ("26.", "UK asks YouTube to remove Russell Brand account"),
    ("27.", "Floods swamp streets across South Florida"),
    ("28.", "ASEAN\u2013China sea code talks about 80% done"),
    ("29.", "Thailand seeks U.S. tariff cut to 10%"),
    ("30.", "UN: 2,230 civilians killed in Sudan this year"),
    ("31.", "Island states demand stronger climate finance"),
    ("32.", "Brent crude settles near $92 a barrel"),
    ("33.", "Norway warns extremist threat is rising"),
    ("34.", "Uganda rail funding close targeted for January"),
    ("35.", "South African rand nears seven-month low"),
    ("36.", "Tanker hit near Hormuz; one sailor missing"),
    ("37.", "Asian shares end four-day slide; KOSPI up 3.3%"),
    ("38.", "Xi and Putin meet in Shenzhen before summit")
]


def draw_more_stories_section(canvas, card_x, card_y, card_w, card_h):
    """
    Menggambar Daftar MORE STORIES dua kolom:
    Cerita 10–38 dari NEWS-final.md, satu baris tiap cerita, bernomor.
    Teks diukur dan dipastikan muat utuh satu baris tanpa elipsis di tengah kata.
    """
    # Kartu putih berbingkai
    canvas.fill_rect(card_x, card_y, card_w, card_h, (255, 255, 255))
    canvas.draw_rect(card_x, card_y, card_w, card_h, (205, 218, 235), thickness=2)

    # Bilah kepala kartu navy
    header_h = 44
    canvas.fill_rect(card_x, card_y, card_w, header_h, (16, 28, 52))
    canvas.draw_text("MORE STORIES \u2014 COMPREHENSIVE DAILY WIRE (10\u201338)", card_x + 18, card_y + 14, FONT_BOLD, scale=2, color=(255, 255, 255))

    # Pemisahan dua kolom
    col_w = (card_w - 48) // 2
    c1_x = card_x + 18
    div_x = card_x + 24 + col_w
    c2_x = div_x + 12

    # Garis pembatas vertikal antara kolom 1 dan 2
    canvas.fill_rect(div_x, card_y + 54, 1, card_h - 72, (225, 234, 245))

    col1_items = MORE_STORIES_DATA[:15]  # 10..24
    col2_items = MORE_STORIES_DATA[15:]  # 25..38

    row_h = 41
    start_y = card_y + 56

    for col_items, base_x in [(col1_items, c1_x), (col2_items, c2_x)]:
        for idx, (num_str, text_str) in enumerate(col_items):
            ry = start_y + idx * row_h

            # Latar baris bergantian (zebra striping lembut)
            if idx % 2 == 1:
                canvas.fill_rect(base_x - 4, ry - 3, col_w - 4, row_h - 4, (248, 250, 254))

            # Nomor berita (BOLD navy)
            nw = canvas.measure_text(num_str, FONT_BOLD, scale=1)
            canvas.draw_text(num_str, base_x, ry + 8, FONT_BOLD, scale=1, color=(28, 55, 95))

            # Teks berita (BOLD scale 1: solid 1px stroke setelah 2x downscale)
            # Mengukur lebar agar muat utuh satu baris tanpa terpotong
            avail_w = col_w - nw - 18
            body_x = base_x + nw + 8

            # Ukur dan pastikan muat
            final_txt, final_scale = fit_and_wrap_text(canvas, text_str, FONT_BOLD, avail_w, preferred_scale=1, min_scale=1)
            canvas.draw_text(final_txt, body_x, ry + 8, FONT_BOLD, scale=final_scale, color=(25, 35, 50))


# =============================================================================
# KAKI (ATRIBUSI SUMBER DARI NEWS-final.md)
# =============================================================================

def draw_footer(canvas):
    """
    Menulis atribusi sumber dari NEWS-final.md:
    (Reuters, AP, BBC, NASA, United Nations — 18 November 2026)
    dalam satu baris rapi di bagian paling bawah.
    """
    footer_y = 2004
    # Garis aksen ganda di atas teks atribusi
    canvas.fill_rect(48, footer_y, canvas.width - 96, 2, (200, 212, 228))
    canvas.fill_rect(48, footer_y + 3, canvas.width - 96, 1, (225, 235, 245))

    footer_text = "Sources: Reuters, AP, BBC, NASA, United Nations \u2014 18 November 2026"
    fw = canvas.measure_text(footer_text, FONT_REGULAR, scale=2)
    canvas.draw_text(footer_text, (canvas.width - fw) // 2, footer_y + 12, FONT_REGULAR, scale=2, color=(95, 110, 130))


def render_newspaper_page(output_path="out/entry.png"):
    """
    Merender tata letak infografis koran penuh sesuai spesifikasi:
    - Kanvas kerja 2048x2048
    - Header pita navy gelap (judul & tanggal berjarak vertikal lega)
    - 3 Panel ilustrasi flat + teks (nomor badge berjarak lega dari judul)
    - 6 Ubin ikon flat + teks
    - By The Numbers (4 angka besar BOLD + label)
    - Peta dunia dot-matrix (benua lengkap + penanda MERAH 1-9)
    - More Stories dua kolom (cerita 10-38 satu baris utuh)
    - Kaki (atribusi sumber lengkap)
    - Downscale 2x box filter ke 1024x1024
    - Simpan ke output_path (PNG < 1 MB)
    """
    print("\n" + "=" * 70)
    print("MEMULAI RENDER HALAMAN KORAN INFOGRAFIS LENGKAP (FINAL ENTRY)")
    print("=" * 70)

    t0 = time.time()
    canvas = Canvas(2048, 2048, bg=(244, 246, 250))
    print(f"  * Kanvas kerja 2048x2048 diinisialisasi dalam {time.time() - t0:.3f} detik.")

    # 1. Header Pita Navy
    t_sec = time.time()
    draw_header(canvas)
    print(f"  * Header Masthead selesai digambar ({time.time() - t_sec:.3f} detik).")

    # 2. Tiga Panel Berita Teratas
    t_sec = time.time()
    draw_top_stories_section(canvas)
    print(f"  * Tiga Panel Ilustrasi Flat selesai digambar ({time.time() - t_sec:.3f} detik).")

    # 3. Enam Ubin Ikon
    t_sec = time.time()
    draw_dispatches_tiles_section(canvas)
    print(f"  * Enam Ubin Ikon selesai digambar ({time.time() - t_sec:.3f} detik).")

    # 4. Strip BY THE NUMBERS (4 Angka Besar BOLD)
    t_sec = time.time()
    draw_by_the_numbers_section(canvas)
    print(f"  * Seksi By The Numbers selesai digambar ({time.time() - t_sec:.3f} detik).")

    # 5. Peta Dunia Dot-Matrix & Legenda Penanda 1-9
    t_sec = time.time()
    map_card_x = 48
    map_card_y = 1294
    map_card_w = 880
    map_card_h = 692
    draw_geographic_theater_map(canvas, map_card_x, map_card_y, map_card_w, map_card_h)
    print(f"  * Peta Dunia Dot-Matrix (Penanda 1-9) selesai digambar ({time.time() - t_sec:.3f} detik).")

    # 6. Daftar More Stories Dua Kolom (Cerita 10-38)
    t_sec = time.time()
    stories_card_x = 944
    stories_card_y = 1294
    stories_card_w = 1056
    stories_card_h = 692
    draw_more_stories_section(canvas, stories_card_x, stories_card_y, stories_card_w, stories_card_h)
    print(f"  * Daftar More Stories Dua Kolom (10-38) selesai digambar ({time.time() - t_sec:.3f} detik).")

    # 7. Kaki Atribusi Sumber
    t_sec = time.time()
    draw_footer(canvas)
    print(f"  * Kaki Atribusi Sumber selesai digambar ({time.time() - t_sec:.3f} detik).")

    # 8. Downscale 2x Box Filter ke 1024x1024
    t_sec = time.time()
    ow, oh, dst_rgb = canvas.downscale_2x()
    print(f"  * Downscale 2x box filter (2048x2048 -> {ow}x{oh}) selesai ({time.time() - t_sec:.3f} detik).")

    # 9. Tulis Berkas PNG
    t_sec = time.time()
    write_png(output_path, ow, oh, dst_rgb)
    file_size_kb = os.path.getsize(output_path) / 1024
    print(f"  * Berkas PNG tersimpan di {output_path} ({file_size_kb:.1f} KB, selesai dalam {time.time() - t_sec:.3f} detik).")

    assert file_size_kb < 1024, f"Ukuran berkas melebihi 1 MB: {file_size_kb:.1f} KB"
    print(f"  * Validasi ukuran berkas: LOLOS ({file_size_kb:.1f} KB < 1024 KB).")

    print("=" * 70)
    print("RENDER HALAMAN KORAN LENGKAP BERHASIL 100%!")
    print("=" * 70)
    return file_size_kb


if __name__ == "__main__":
    # Jalankan uji glyph lama untuk memastikan tidak ada regresi
    verify_and_render_glyph_test("out/test-glyph.png")

    # Jalankan render tata letak halaman koran infografis run ini
    render_newspaper_page("out/entry.png")

