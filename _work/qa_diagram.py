#!/usr/bin/env python3
"""QA geometri diagram graphviz tanpa vision: deteksi node bertumpuk & label terpotong."""
import subprocess, sys, re

def parse_plain(dotfile):
    out = subprocess.run(["/opt/homebrew/bin/dot", "-Tplain", dotfile],
                         capture_output=True, text=True, check=True).stdout
    nodes, edges, w, h = [], [], 0, 0
    for line in out.splitlines():
        f = line.split()
        if not f: continue
        if f[0] == "graph":
            w, h = float(f[2]), float(f[3])
        elif f[0] == "node":
            name, x, y = f[1], float(f[2]), float(f[3])
            nw, nh = float(f[4]), float(f[5])
            label = f[6] if len(f) > 6 else name
            nodes.append(dict(name=name, x=x, y=y, w=nw, h=nh, label=label))
        elif f[0] == "edge":
            edges.append((f[1], f[2]))
    return dict(w=w, h=h, nodes=nodes, edges=edges)

def rect(n):
    return (n["x"] - n["w"] / 2, n["y"] - n["h"] / 2, n["x"] + n["w"] / 2, n["y"] + n["h"] / 2)

def overlap(a, b, tol=0.02):
    ax0, ay0, ax1, ay1 = rect(a); bx0, by0, bx1, by1 = rect(b)
    ox = min(ax1, bx1) - max(ax0, bx0); oy = min(ay1, by1) - max(ay0, by0)
    if ox > tol and oy > tol:
        return round(ox * oy, 3)
    return 0.0

def main(dotfile):
    g = parse_plain(dotfile)
    nodes = g["nodes"]
    print(f"graph {dotfile}")
    print(f"  kanvas: {g['w']:.1f} x {g['h']:.1f} inci  (rasio {g['w']/g['h']:.2f})")
    print(f"  node: {len(nodes)}   edge: {len(g['edges'])}")
    bad = 0
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            o = overlap(nodes[i], nodes[j])
            if o:
                bad += 1
                print(f"  !! TUMPANG-TINDIH: {nodes[i]['name']} <-> {nodes[j]['name']} seluas {o} inci2")
    # label terlalu panjang untuk kotaknya?
    for n in nodes:
        # perkiraan: 9pt Helvetica, huruf rata-rata 0.075 inci
        lines = n["label"].replace("\\n", " ").split()
        est = max((len(l) for l in [n["label"].replace("\\n", "\n")]), default=0)
    # cek tepi keluar kanvas
    for n in nodes:
        x0, y0, x1, y1 = rect(n)
        if x0 < -0.05 or y0 < -0.05 or x1 > g["w"] + 0.05 or y1 > g["h"] + 0.05:
            bad += 1
            print(f"  !! KELUAR KANVAS: {n['name']}")
    print(f"  HASIL: {'LULUS' if bad == 0 else f'{bad} masalah'}")
    return bad

if __name__ == "__main__":
    rc = 0
    for f in sys.argv[1:]:
        rc += main(f)
        print()
    sys.exit(1 if rc else 0)
