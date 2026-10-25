"""Cut the Nobody Builds illustration out of its flat cream background; report palette.
usage: python -I cutout.py <avatar.png> <out_dir>"""
import sys, os
from collections import deque, Counter
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
im = Image.open(src).convert("RGB")
W, H = im.size
px = im.load()

corners = [px[x, y] for x in (2, W - 3) for y in (2, H - 3)]
bg = tuple(sorted(c[i] for c in corners)[1] for i in range(3))
dist = lambda c: max(abs(c[i] - bg[i]) for i in range(3))

# 1. background = pixels near bg colour connected to the border
TOL = 14
isbg = [[False] * H for _ in range(W)]
q = deque((x, y) for x in range(W) for y in (0, H - 1)) + deque((x, y) for y in range(H) for x in (0, W - 1))
for x, y in q:
    isbg[x][y] = True
while q:
    x, y = q.popleft()
    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if 0 <= nx < W and 0 <= ny < H and not isbg[nx][ny] and dist(px[nx, ny]) <= TOL:
            isbg[nx][ny] = True
            q.append((nx, ny))

# 2. drop small foreground specks (e.g. the corner sparkle); keep real parts like the zzz
seen = [[False] * H for _ in range(W)]
keep = [[False] * H for _ in range(W)]
for sx in range(W):
    for sy in range(H):
        if isbg[sx][sy] or seen[sx][sy]:
            continue
        comp, q = [], deque([(sx, sy)])
        seen[sx][sy] = True
        while q:
            x, y = q.popleft()
            comp.append((x, y))
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < W and 0 <= ny < H and not isbg[nx][ny] and not seen[nx][ny]:
                    seen[nx][ny] = True
                    q.append((nx, ny))
        strong = sum(1 for p in comp if dist(px[p]) > 60)
        if strong >= 40:
            for x, y in comp:
                keep[x][y] = True
        else:
            print(f"dropped speck: {len(comp)} px at {comp[0]}")

# 3. alpha with soft, colour-decontaminated edges
outim = Image.new("RGBA", (W, H))
op = outim.load()
for x in range(W):
    for y in range(H):
        if not keep[x][y]:
            continue
        c = px[x, y]
        edge = any(0 <= x + dx < W and 0 <= y + dy < H and not keep[x + dx][y + dy]
                   for dx in (-1, 0, 1) for dy in (-1, 0, 1))
        a = 1.0 if not edge else min(1.0, max(0.15, dist(c) / 90))
        rgb = tuple(max(0, min(255, round((c[i] - (1 - a) * bg[i]) / a))) for i in range(3))
        op[x, y] = rgb + (round(a * 255),)

bbox = outim.getbbox()
cut = outim.crop(bbox)
cut.save(os.path.join(out, "illustration-cutout.png"))
print("bg", "#%02X%02X%02X" % bg, "bbox", bbox, "cutout", cut.size)

# palette: dominant saturated/dark colours of the illustration
cols = Counter()
for x in range(W):
    for y in range(H):
        if keep[x][y]:
            r, g, b = px[x, y]
            cols[(r // 12 * 12, g // 12 * 12, b // 12 * 12)] += 1
for (r, g, b), n in cols.most_common(14):
    print("#%02X%02X%02X" % (r, g, b), n)
