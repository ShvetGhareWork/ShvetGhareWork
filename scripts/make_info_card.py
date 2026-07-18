"""
make_info_card.py
-----------------
Generates the Neofetch-style info card SVG with staggered CSS slide-in animations.

Set the STATIC env-var to "1" to disable animations (useful for opengraph previews):
    STATIC=1 python make_info_card.py

Customise the `content` list below to reflect your own details.

Output:
    info-card.svg
"""

import os

STATIC = os.environ.get("STATIC", "0") == "1"


def generate_info_card(output: str = "info-card.svg") -> None:
    # ── Customise your details here ───────────────────────────────────────────
    content = [
        ("shvet@github ~ $",  "whoami",                             "#58a6ff"),
        ("Role",              "Full-Stack Software Engineer",        "#c9d1d9"),
        ("Stack",             "Java · React · Node.js · AWS",       "#c9d1d9"),
        ("Now",               "AI platforms & microservices",       "#c9d1d9"),
        ("Education",         "B.E. CSE · 9.39 SGPA · Top 5%",     "#c9d1d9"),
        ("Certs",             "AWS SAA · Cloud Practitioner",       "#c9d1d9"),
    ]
    # ─────────────────────────────────────────────────────────────────────────

    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 490 200" width="490" height="200">',
        "<style>",
        "  .txt { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 14px; }",
        "  .key { fill: #8b949e; font-weight: 600; }",
    ]

    if not STATIC:
        svg.extend(
            [
                "  @keyframes slide { from { opacity: 0; transform: translateX(-15px); } "
                "to { opacity: 1; transform: translateX(0); } }",
                "  .anim { opacity: 0; animation: slide 0.5s ease-out forwards; }",
            ]
        )
    else:
        svg.append("  .anim { opacity: 1; }")

    svg.append("</style>")

    y = 30
    for i, (key, val, color) in enumerate(content):
        delay = i * 0.15
        style = "" if STATIC else f'style="animation-delay: {delay}s"'

        if i == 0:
            # Title / prompt row
            svg.append(
                f'<text x="20" y="{y}" class="txt anim" {style}>'
                f'<tspan class="key">{key}</tspan> '
                f'<tspan fill="{color}">{val}</tspan></text>'
            )
        else:
            # Key : Value rows
            svg.append(
                f'<text x="20" y="{y}" class="txt anim" {style}>'
                f'<tspan class="key">{key}:</tspan> '
                f'<tspan fill="{color}">{val}</tspan></text>'
            )

        y += 28

    svg.append("</svg>")

    with open(output, "w") as f:
        f.write("\n".join(svg))
    print(f"Generated {output}")


if __name__ == "__main__":
    generate_info_card()
