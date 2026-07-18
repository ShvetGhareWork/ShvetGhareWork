"""
make_ascii_svg.py
-----------------
Portrait pipeline step 2:
  - Converts source-prepped.png into an animated SVG using ASCII art.
  - Each row uses a SMIL <animate> wipe that staggers top-to-bottom for a
    typewriter/reveal effect.

Prerequisites:
    Run prep_photo.py first to produce source-prepped.png.

Output:
    avi-ascii.svg
"""

from PIL import Image

# ASCII brightness ramp (darkest → brightest)
RAMP = " .`:-=+*cs#%@"

# Output dimensions in character cells
W, H = 100, 53


def generate_ascii_svg(
    source: str = "source-prepped.png",
    output: str = "avi-ascii.svg",
) -> None:
    try:
        img = Image.open(source).resize((W, H), Image.Resampling.LANCZOS)
    except FileNotFoundError:
        print(f"Error: {source} not found. Run prep_photo.py first.")
        return

    pixels = img.load()

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W * 6} {H * 12}" '
        f'width="{W * 6}" height="{H * 12}">',
        "<style>",
        "  text { font-family: monospace; font-size: 10px; fill: #8b949e; white-space: pre; }",
        "</style>",
    ]

    for y in range(H):
        line_chars = []
        for x in range(W):
            # 255 = white (index 0), 0 = black (index -1)
            val = pixels[x, y]
            idx = int(((255 - val) / 255) * (len(RAMP) - 1))
            line_chars.append(RAMP[idx])

        # Escape XML special characters
        row_str = (
            "".join(line_chars)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        # SMIL Animation: horizontal wipe staggered top-to-bottom
        delay = y * 0.04
        clip_id = f"wipe_{y}"

        svg.extend(
            [
                f'<clipPath id="{clip_id}">',
                f'  <rect x="0" y="{y * 12}" width="0" height="12">',
                f'    <animate attributeName="width" from="0" to="{W * 6}" '
                f'dur="0.8s" begin="{delay}s" fill="freeze" />',
                f"  </rect>",
                f"</clipPath>",
                f'<text x="0" y="{y * 12 + 10}" clip-path="url(#{clip_id})">{row_str}</text>',
            ]
        )

    svg.append("</svg>")

    with open(output, "w") as f:
        f.write("\n".join(svg))
    print(f"Generated {output}")


if __name__ == "__main__":
    generate_ascii_svg()
