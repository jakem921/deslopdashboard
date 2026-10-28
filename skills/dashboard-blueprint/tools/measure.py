#!/usr/bin/env python3
"""measure.py: exact, dependency-free screenshot measurement for UI teardowns.

Works anywhere Python 3.8+ runs. It reads 8-bit PNGs; convert other formats first, e.g.
`ffmpeg -i shot.webp shot.png` or `sips -s format png shot.jpg --out shot.png` (macOS).

Usage (coordinates are image pixels, origin top-left):
  measure.py IMG color X Y                 hex colour at a point (3x3 median)
  measure.py IMG mode  X0 Y0 X1 Y1         the most common colour in a region (a surface's fill)
  measure.py IMG peak  X0 Y0 X1 Y1         text colour in a region (the pixel furthest from the region's background)
  measure.py IMG scan  h|v AT FROM TO [THR] every edge along a line: positions where luminance jumps > THR (default 12)
                                           h = a horizontal line at y=AT from x=FROM..TO; v = a vertical line at x=AT
  measure.py IMG ink   X0 Y0 X1 Y1 [THR]   bounding box of everything that isn't background (diff > THR, default 40),
                                           plus ink rows (y-runs) and ink columns (x-runs): text sizes, row pitch, left edges
  measure.py IMG size                      image width and height

Typical uses:
  box edges / hairlines / radii   scan along a line crossing the element
  row pitch                       ink over a navigation column; read the row runs
  left edges                      ink over a strip; read the first column of each run
  text size                       ink over one word: cap height ~ 0.7 x font size
"""
import struct
import sys
import zlib


def read_png(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit("measure.py reads PNG only; convert first (see the header of this file).")
    pos, idat, width = 8, b"", None
    while pos < len(data):
        length, kind = struct.unpack(">I4s", data[pos:pos + 8])
        chunk = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if kind == b"IHDR":
            width, height, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", chunk)
            if depth != 8 or interlace:
                sys.exit("Only 8-bit, non-interlaced PNGs are supported; re-save the image (e.g. with ffmpeg).")
            channels = {0: 1, 2: 3, 4: 2, 6: 4}.get(ctype)
            if channels is None:
                sys.exit("Palette PNGs aren't supported; re-save as RGB (ffmpeg -i in.png -pix_fmt rgb24 out.png).")
        elif kind == b"IDAT":
            idat += chunk
        elif kind == b"IEND":
            break
    raw = zlib.decompress(idat)
    stride = width * channels
    rows, prev, i = [], bytearray(stride), 0
    for _ in range(height):
        ftype = raw[i]
        line = bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        for x in range(stride):
            a = line[x - channels] if x >= channels else 0
            b = prev[x]
            c = prev[x - channels] if x >= channels else 0
            if ftype == 1:
                line[x] = (line[x] + a) & 255
            elif ftype == 2:
                line[x] = (line[x] + b) & 255
            elif ftype == 3:
                line[x] = (line[x] + (a + b) // 2) & 255
            elif ftype == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(bytes(line))
        prev = line

    def px(x, y):
        x = min(max(x, 0), width - 1)
        y = min(max(y, 0), height - 1)
        r = rows[y]
        o = x * channels
        if channels >= 3:
            return r[o], r[o + 1], r[o + 2]
        return r[o], r[o], r[o]

    return width, height, px


def lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def hexc(c):
    return "#%02X%02X%02X" % c


def dist(p, q):
    return max(abs(p[0] - q[0]), abs(p[1] - q[1]), abs(p[2] - q[2]))


def mode_color(px, x0, y0, x1, y1):
    counts = {}
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            c = px(x, y)
            k = (c[0] >> 2, c[1] >> 2, c[2] >> 2)
            counts[k] = counts.get(k, 0) + 1
    k = max(counts, key=counts.get)
    return (k[0] << 2, k[1] << 2, k[2] << 2)


def runs(flags, offset, min_gap=2):
    out, start, gap = [], None, 0
    for i, f in enumerate(flags):
        if f:
            if start is None:
                start = i
            gap = 0
        elif start is not None:
            gap += 1
            if gap > min_gap:
                out.append((start + offset, i - gap + offset))
                start, gap = None, 0
    if start is not None:
        out.append((start + offset, len(flags) - 1 - gap + offset))
    return out


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    w, h, px = read_png(argv[1])
    cmd, a = argv[2], [int(v) if v.lstrip("-").isdigit() else v for v in argv[3:]]
    if cmd == "size":
        print(w, h)
    elif cmd == "color":
        x, y = a[0], a[1]
        cs = [px(x + dx, y + dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1)]
        c = tuple(sorted(ch[i] for ch in cs)[4] for i in range(3))
        print(hexc(c), "L=%d" % lum(c))
    elif cmd == "mode":
        c = mode_color(px, *a[:4])
        print(hexc(c), "L=%d" % lum(c))
    elif cmd == "peak":
        x0, y0, x1, y1 = a[:4]
        bg = mode_color(px, x0, y0, x1, y1)
        best = max((px(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)), key=lambda c: dist(c, bg))
        print("text %s L=%d  on bg %s L=%d" % (hexc(best), lum(best), hexc(bg), lum(bg)))
    elif cmd == "scan":
        horiz, at, frm, to = a[0] == "h", a[1], a[2], a[3]
        thr = float(a[4]) if len(a) > 4 else 12.0
        get = (lambda p: px(p, at)) if horiz else (lambda p: px(at, p))
        prev, out = lum(get(frm)), []
        for p in range(frm + 1, to + 1):
            c = get(p)
            l = lum(c)
            if abs(l - prev) > thr:
                out.append("%d:%s" % (p, hexc(c)))
            prev = l
        print(" ".join(out))
    elif cmd == "ink":
        x0, y0, x1, y1 = a[:4]
        thr = a[4] if len(a) > 4 else 40
        bg = mode_color(px, x0, y0, x1, y1)
        rowf = [False] * (y1 - y0 + 1)
        colf = [False] * (x1 - x0 + 1)
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if dist(px(x, y), bg) > thr:
                    rowf[y - y0] = True
                    colf[x - x0] = True
        rr, cc = runs(rowf, y0), runs(colf, x0, min_gap=6)
        if not rr:
            print("bg %s  (no ink above threshold)" % hexc(bg))
            return
        print("bg %s  bbox x%d-%d y%d-%d  (w%d h%d)" % (hexc(bg), cc[0][0], cc[-1][1], rr[0][0], rr[-1][1],
                                                        cc[-1][1] - cc[0][0] + 1, rr[-1][1] - rr[0][0] + 1))
        print("rows", " ".join("%d-%d(%d)" % (s, e, e - s + 1) for s, e in rr))
        print("cols", " ".join("%d-%d" % (s, e) for s, e in cc))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
