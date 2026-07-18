"""
render_heatmap_svg.py
---------------------
Reads data/contributions.json (produced by fetch_contributions.py) and renders
an animated SVG contribution heatmap grid with a diagonal drop-in stagger.

Output:
    contrib-heatmap.svg
"""

import json

# GitHub-dark contribution palette (level 0 → level 5)
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]


def render_heatmap(
    data_path: str = "data/contributions.json",
    output: str = "contrib-heatmap.svg",
) -> None:
    try:
        with open(data_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"{data_path} not found. Run fetch_contributions.py first.")
        return

    days = data.get("days", [])

    # ── SVG grid math ─────────────────────────────────────────────────────────
    box_size, gap = 10, 4
    rows = 7
    cols = (len(days) // rows) + (1 if len(days) % rows else 0)

    width = (cols * (box_size + gap)) + 40
    height = (rows * (box_size + gap)) + 50
    # ─────────────────────────────────────────────────────────────────────────

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}">',
        "<style>",
        "  @keyframes drop { from { opacity: 0; transform: translateY(-3px); } "
        "to { opacity: 1; transform: translateY(0); } }",
        "  .box { opacity: 0; animation: drop 0.4s ease-out forwards; rx: 2; ry: 2; }",
        "  .text { font-family: monospace; font-size: 10px; fill: #8b949e; }",
        "</style>",
    ]

    # Render contribution boxes
    for i, day in enumerate(days):
        col, row = i // rows, i % rows
        x = 20 + col * (box_size + gap)
        y = 20 + row * (box_size + gap)

        level = min(day.get("level", 0), len(PALETTE) - 1)
        color = PALETTE[level]

        # Diagonal slide-down stagger
        delay = round((col * 0.015) + (row * 0.015), 4)

        svg.append(
            f'  <rect class="box" x="{x}" y="{y}" width="{box_size}" height="{box_size}" '
            f'fill="{color}" rx="2" ry="2" style="animation-delay: {delay}s" />'
        )

    # ── Legend & footer ───────────────────────────────────────────────────────
    leg_x = width - 130
    leg_y = height - 15

    svg.append(
        f'  <text x="{leg_x - 35}" y="{leg_y + 8}" class="text">Less</text>'
    )
    for i, color in enumerate(PALETTE):
        svg.append(
            f'  <rect x="{leg_x + (i * 14)}" y="{leg_y}" width="{box_size}" '
            f'height="{box_size}" fill="{color}" rx="2" ry="2"/>'
        )
    svg.append(
        f'  <text x="{leg_x + (len(PALETTE) * 14) + 5}" y="{leg_y + 8}" class="text">More</text>'
    )
    # ─────────────────────────────────────────────────────────────────────────

    svg.append("</svg>")

    with open(output, "w") as f:
        f.write("\n".join(svg))
    print(f"Generated {output}")


if __name__ == "__main__":
    render_heatmap()
