import os
import sys
import struct
import zlib

WIDTH = 1024
HEIGHT = 1024

COLOR_PAPER = (247, 243, 233)
COLOR_INK = (20, 20, 20)
COLOR_RED = (179, 32, 44)
COLOR_BLUE = (29, 78, 137)
COLOR_GRAY = (90, 90, 90)

FONT = {
    ' ': [
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
    ],
    'A': [
        ".###.",
        "#...#",
        "#...#",
        "#####",
        "#...#",
        "#...#",
        "#...#",
    ],
    'B': [
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#...#",
        "#...#",
        "####.",
    ],
    'C': [
        ".####",
        "#....",
        "#....",
        "#....",
        "#....",
        "#....",
        ".####",
    ],
    'D': [
        "####.",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "####.",
    ],
    'E': [
        "#####",
        "#....",
        "#....",
        "####.",
        "#....",
        "#....",
        "#####",
    ],
    'F': [
        "#####",
        "#....",
        "#....",
        "####.",
        "#....",
        "#....",
        "#....",
    ],
    'G': [
        ".####",
        "#....",
        "#....",
        "#.###",
        "#...#",
        "#...#",
        ".####",
    ],
    'H': [
        "#...#",
        "#...#",
        "#...#",
        "#####",
        "#...#",
        "#...#",
        "#...#",
    ],
    'I': [
        "#####",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "#####",
    ],
    'J': [
        "..###",
        "....#",
        "....#",
        "....#",
        "#...#",
        "#...#",
        ".###.",
    ],
    'K': [
        "#...#",
        "#..#.",
        "#.#..",
        "##...",
        "#.#..",
        "#..#.",
        "#...#",
    ],
    'L': [
        "#....",
        "#....",
        "#....",
        "#....",
        "#....",
        "#....",
        "#####",
    ],
    'M': [
        "#...#",
        "##.##",
        "#.#.#",
        "#.#.#",
        "#...#",
        "#...#",
        "#...#",
    ],
    'N': [
        "#...#",
        "##..#",
        "#.#.#",
        "#..##",
        "#...#",
        "#...#",
        "#...#",
    ],
    'O': [
        ".###.",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
    ],
    'P': [
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#....",
        "#....",
        "#....",
    ],
    'Q': [
        ".###.",
        "#...#",
        "#...#",
        "#...#",
        "#.#.#",
        "#..#.",
        ".##.#",
    ],
    'R': [
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#.#..",
        "#..#.",
        "#...#",
    ],
    'S': [
        ".####",
        "#....",
        "#....",
        ".###.",
        "....#",
        "....#",
        "####.",
    ],
    'T': [
        "#####",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
    ],
    'U': [
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
    ],
    'V': [
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        "#...#",
        ".#.#.",
        "..#..",
    ],
    'W': [
        "#...#",
        "#...#",
        "#...#",
        "#.#.#",
        "#.#.#",
        "##.##",
        "#...#",
    ],
    'X': [
        "#...#",
        "#...#",
        ".#.#.",
        "..#..",
        ".#.#.",
        "#...#",
        "#...#",
    ],
    'Y': [
        "#...#",
        "#...#",
        ".#.#.",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
    ],
    'Z': [
        "#####",
        "....#",
        "...#.",
        "..#..",
        ".#...",
        "#....",
        "#####",
    ],
    '0': [
        ".###.",
        "#...#",
        "#..##",
        "#.#.#",
        "##..#",
        "#...#",
        ".###.",
    ],
    '1': [
        "..#..",
        ".##..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".###.",
    ],
    '2': [
        ".###.",
        "#...#",
        "....#",
        "..##.",
        ".#...",
        "#....",
        "#####",
    ],
    '3': [
        "####.",
        "....#",
        "....#",
        ".###.",
        "....#",
        "....#",
        "####.",
    ],
    '4': [
        "#...#",
        "#...#",
        "#...#",
        "#####",
        "....#",
        "....#",
        "....#",
    ],
    '5': [
        "#####",
        "#....",
        "####.",
        "....#",
        "....#",
        "....#",
        "####.",
    ],
    '6': [
        ".###.",
        "#....",
        "####.",
        "#...#",
        "#...#",
        "#...#",
        ".###.",
    ],
    '7': [
        "#####",
        "....#",
        "...#.",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
    ],
    '8': [
        ".###.",
        "#...#",
        "#...#",
        ".###.",
        "#...#",
        "#...#",
        ".###.",
    ],
    '9': [
        ".###.",
        "#...#",
        "#...#",
        ".####",
        "....#",
        "....#",
        ".###.",
    ],
    '.': [
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".##..",
        ".##..",
    ],
    ',': [
        ".....",
        ".....",
        ".....",
        ".....",
        ".##..",
        "..#..",
        ".#...",
    ],
    "'": [
        ".##..",
        ".##..",
        "..#..",
        ".....",
        ".....",
        ".....",
        ".....",
    ],
    '-': [
        ".....",
        ".....",
        ".....",
        "#####",
        ".....",
        ".....",
        ".....",
    ],
    ':': [
        ".....",
        ".##..",
        ".##..",
        ".....",
        ".##..",
        ".##..",
        ".....",
    ],
    '/': [
        "....#",
        "...#.",
        "...#.",
        "..#..",
        ".#...",
        ".#...",
        "#....",
    ],
    '%': [
        "##..#",
        "##.#.",
        "...#.",
        "..#..",
        ".#...",
        ".#.##",
        "#..##",
    ],
    '$': [
        "..#..",
        ".####",
        "#.#..",
        ".###.",
        "..#.#",
        "####.",
        "..#..",
    ],
    '+': [
        ".....",
        "..#..",
        "..#..",
        "#####",
        "..#..",
        "..#..",
        ".....",
    ],
    '(': [
        "...#.",
        "..#..",
        ".#...",
        ".#...",
        ".#...",
        "..#..",
        "...#.",
    ],
    ')': [
        ".#...",
        "..#..",
        "...#.",
        "...#.",
        "...#.",
        "..#..",
        ".#...",
    ],
    '!': [
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        ".....",
        "..#..",
    ],
}

pixels = bytearray(bytes(COLOR_PAPER) * (WIDTH * HEIGHT))


def fill_rect(x, y, w, h, color):
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(WIDTH, x + w)
    y1 = min(HEIGHT, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    r, g, b = color
    row_bytes = bytes([r, g, b]) * (x1 - x0)
    for py in range(y0, y1):
        idx = (py * WIDTH + x0) * 3
        pixels[idx:idx + len(row_bytes)] = row_bytes


def draw_rect(x, y, w, h, thickness, color):
    fill_rect(x, y, w, thickness, color)
    fill_rect(x, y + h - thickness, w, thickness, color)
    fill_rect(x, y, thickness, h, color)
    fill_rect(x + w - thickness, y, thickness, h, color)


def text(x, y, s, scale, color):
    s = s.upper()
    cur_x = x
    blank_glyph = ["....."] * 7
    for ch in s:
        glyph = FONT.get(ch, blank_glyph)
        for row_idx, row_str in enumerate(glyph):
            py = y + row_idx * scale
            for col_idx, col_char in enumerate(row_str):
                if col_char == '#':
                    px = cur_x + col_idx * scale
                    fill_rect(px, py, scale, scale, color)
        cur_x += 6 * scale


def text_width(s, scale):
    if not s:
        return 0
    return (len(s) - 1) * (6 * scale) + (5 * scale)


def wrap(s, maxchars):
    words = s.split(' ')
    lines = []
    cur = []
    cur_len = 0
    for w in words:
        if not cur:
            cur.append(w)
            cur_len = len(w)
        elif cur_len + 1 + len(w) <= maxchars:
            cur.append(w)
            cur_len += 1 + len(w)
        else:
            lines.append(" ".join(cur))
            cur = [w]
            cur_len = len(w)
    if cur:
        lines.append(" ".join(cur))
    return lines


def make_png(width, height, raw_rgb):
    scanlines = bytearray()
    row_bytes_len = width * 3
    for y in range(height):
        scanlines.append(0)
        start = y * row_bytes_len
        scanlines.extend(raw_rgb[start:start + row_bytes_len])

    compressed = zlib.compress(scanlines, level=6)

    def chunk(chunk_type, data):
        length = len(data)
        crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
        return struct.pack(">I", length) + chunk_type + data + struct.pack(">I", crc)

    png = bytearray(b"\x89PNG\r\n\x1a\n")
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png.extend(chunk(b"IHDR", ihdr_data))
    png.extend(chunk(b"IDAT", compressed))
    png.extend(chunk(b"IEND", b""))
    return bytes(png)


def render():
    # 1. Pita atas
    title_text = "THE WORLD IN ONE DAY"
    title_w = text_width(title_text, 8)
    title_x = (WIDTH - title_w) // 2
    text(title_x, 24, title_text, 8, COLOR_INK)

    # Garis tebal bawah judul
    fill_rect(32, 86, 960, 4, COLOR_INK)

    # Tanggal
    date_text = "WEDNESDAY 18 NOVEMBER 2026"
    date_w = text_width(date_text, 6)
    date_x = (WIDTH - date_w) // 2
    text(date_x, 96, date_text, 6, COLOR_RED)

    # Garis pembatas atas panel utama
    fill_rect(32, 144, 960, 2, COLOR_INK)

    # 2. Panel UTAMA (kotak merah tipis)
    panel_x = 32
    panel_y = 152
    panel_w = 960
    panel_h = 208
    draw_rect(panel_x, panel_y, panel_w, panel_h, 2, COLOR_RED)

    main_title = "US AND IRAN TRADE STRIKES ACROSS THE GULF"
    main_title_lines = wrap(main_title, 26)
    line1 = main_title_lines[0]
    line2 = main_title_lines[1]
    w1 = text_width(line1, 6)
    w2 = text_width(line2, 6)
    text(panel_x + (panel_w - w1) // 2, 162, line1, 6, COLOR_INK)
    text(panel_x + (panel_w - w2) // 2, 208, line2, 6, COLOR_INK)

    # Garis pemisah tipis dalam panel
    fill_rect(panel_x + 20, 258, panel_w - 40, 1, COLOR_RED)

    # 3 baris ringkas
    summary_lines = [
        "US JETS HIT IRGC LAUNCH SITE ON QESHM ISLAND",
        "KUWAIT AND BAHRAIN INTERCEPT IRANIAN DRONES",
        "TARA GAS TANKER HIT NEAR HORMUZ - 1 SAILOR MISSING",
    ]
    for idx, s_line in enumerate(summary_lines):
        sw = text_width(s_line, 3)
        sx = panel_x + (panel_w - sw) // 2
        sy = 268 + idx * 26
        text(sx, sy, s_line, 3, COLOR_INK)

    # 3. Kisi 3 kolom x 4 baris kartu cerita
    cards = [
        ("EUROPE", ["NORWAY RISK", "RISING"], ["EXTREMIST THREAT", "LEVEL STAYS 3 OF 5"]),
        ("ASIA", ["XI OPENS APEC", "IN SHENZHEN"], ["CALLS FOR", "OPEN TRADE"]),
        ("ASIA", ["TRUMP XI PUTIN", "TO MEET"], ["SUMMIT WEEK", "IN SHENZHEN"]),
        ("AMERICAS", ["PELTOLA WINS", "ALASKA RACE"], ["DEMOCRATS TAKE", "SENATE 56-44"]),
        ("MARKETS", ["NVIDIA BEATS", "FORECASTS"], ["ASIA STOCKS SNAP", "LOSING STREAK"]),
        ("MARKETS", ["ANTHROPIC TO", "MARKET DEBUT"], ["VALUE COULD HIT", "$1.4 TRILLION"]),
        ("ASIA", ["ASEAN SEA CODE", "NEARLY DONE"], ["80% AGREED", "TARGET NEXT YEAR"]),
        ("ASIA", ["THAILAND SEEKS", "TARIFF CUT"], ["12.5% TO 10%", "US DEAL TALKS"]),
        ("AFRICA", ["UN: 2,230 DEAD", "IN SUDAN"], ["MOST KILLED BY", "DRONE STRIKES"]),
        ("AFRICA", ["UGANDA RAIL", "$2.97BN DEAL"], ["FUNDING CLOSE", "SET JAN 2027"]),
        ("CLIMATE", ["ISLAND STATES", "PRESS COP31"], ["DEMAND STRONGER", "CLIMATE FINANCE"]),
        ("SCIENCE", ["VOYAGER 1 AT", "1 LIGHT-DAY"], ["SIGNAL TAKES", "24 HOURS - NASA"]),
    ]

    col_xs = [10, 346, 682]
    row_ys = [372, 522, 672, 822]

    # Garis pemisah vertikal antar kolom kartu
    fill_rect(344, 370, 1, 596, COLOR_GRAY)
    fill_rect(680, 370, 1, 596, COLOR_GRAY)

    # Garis pemisah horizontal antar baris kartu
    fill_rect(10, 517, 1004, 1, COLOR_GRAY)
    fill_rect(10, 667, 1004, 1, COLOR_GRAY)
    fill_rect(10, 817, 1004, 1, COLOR_GRAY)

    for index, (section, title_pair, detail_pair) in enumerate(cards):
        r = index // 3
        c = index % 3
        cx = col_xs[c]
        cy = row_ys[r]

        # Label seksi
        text(cx, cy, section, 3, COLOR_BLUE)

        # Judul kartu (scale 4, hitam)
        text(cx, cy + 27, title_pair[0], 4, COLOR_INK)
        text(cx, cy + 59, title_pair[1], 4, COLOR_INK)

        # Detail kartu (scale 3, abu)
        text(cx, cy + 94, detail_pair[0], 3, COLOR_GRAY)
        text(cx, cy + 118, detail_pair[1], 3, COLOR_GRAY)

    # 4. Kaki gambar
    fill_rect(32, 976, 960, 2, COLOR_INK)
    footer_text = "SOURCES: REUTERS, AP, BBC, NASA, UN"
    footer_w = text_width(footer_text, 3)
    footer_x = (WIDTH - footer_w) // 2
    text(footer_x, 988, footer_text, 3, COLOR_INK)


def main():
    render()
    png_bytes = make_png(WIDTH, HEIGHT, pixels)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as f:
        f.write(png_bytes)


if __name__ == "__main__":
    main()
